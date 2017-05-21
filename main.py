import sys
import shlex
import ezibpy
import time
import prettytable

SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP = 0


tickers_ = []
# initialize ezIBpy
ibConn_ = ezibpy.ezIBpy()

def ibCallback(caller, msg, table=None, **kwargs):
    if table is None:
        return
    if caller in ["handleAccount", "handlePortfolio"]:
        print("\n", caller)
        prettytable.pprint_table(sys.stdout, table)

def initConnection():
    global ibConn_
    # connect to IB (7496/7497 = TWS, 4001 = IBGateway)
    ibConn_.accountCode = 'xxxxxxx'
    ibConn_.connect(clientId=100, host="localhost", port=7496)

def initCallback():
    global ibConn_
    ibConn_.ibCallback = ibCallback

def init():
    global tickers_
    initConnection()
    initCallback()
    filename = "stocksymbol"
    FILE = open(filename, 'r')
    tickarr = []
    i = 0
    for line in FILE:
        tickarr.append(line.upper().rstrip("\n"))
    tickers_ = tickarr
    print(tickers_)

def deInit():
    global ibConn_
    ibConn_.cancelMarketData()
    ibConn_.disconnect()



#commands supported: show acct1; watchlist [updateinterval];
def execute(command, args):
    global ibConn_
    global tickers_
    if command is 'print':
        contracts = []
        for tickid in tickers_:
            contracts.append(ibConn_.createStockContract(tickid))
        print(contracts)
        ibConn_.requestMarketData(contracts=contracts)
        time.sleep(10)
        # print market data
        #print("Market Data")
    elif command is 'show':
        ibConn_.requestAccountUpdates(subscribe=True)
        ibConn_.requestPositionUpdates(subscribe=True)
        time.sleep(10)



def tokenize(string):
    return shlex.split(string)


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        # Display a command prompt
        sys.stdout.write('> ')
        sys.stdout.flush()

        # Read command input
        cmd = sys.stdin.readline()

        # Tokenize the command input
        cmd_tokens = tokenize(cmd)

        if len(cmd_tokens <=1):
            next

        # Execute the command and retrieve new status
        status = execute(cmd_tokens[0], cmd_tokens[1,:])





if __name__=="__main__":
    init();
    #execute('print', '')
    execute('show', '')
