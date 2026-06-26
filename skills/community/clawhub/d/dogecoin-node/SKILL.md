---
name: dogecoin-node
version: 1.0.5
description: A skill to set up and operate a Dogecoin Core full node with RPC access, blockchain tools, and optional tipping functionality.
---

# Dogecoin Node Skill

This skill is designed to fully automate the integration and operation of a Dogecoin Core full node and CLI over RPC, enabling blockchain tools and wallet management for various use cases, including tipping functionality using SQLite.

This skill provides:

## Functionalities
1. **Fetch Wallet Balance**
    - Retrieves the current balance of a Dogecoin wallet address.
    - Example: `/dogecoin-node balance <wallet_address>`

2. **Send DOGE**
    - Send Dogecoin from a connected wallet to a specified address.
    - Example: `/dogecoin-node send <recipient_address> <amount>`

3. **Check Transactions**
    - Retrieve recent transaction details of a wallet.
    - Example: `/dogecoin-node txs <wallet_address>`

4. **Check DOGE Price**
    - Fetch the latest Dogecoin price in USD.
    - Example: `/dogecoin-node price`

5. **Help Command**
    - Display help information about commands.
    - Example: `/dogecoin-node help`

---

## Installation

### Prerequisites

1. A fully synced Dogecoin Core RPC node.
2. Dogecoin `rpcuser` and `rpcpassword` configured in `dogecoin.conf`.
3. OpenClaw Gateway up-to-date.
4. `jq` installed on the host (`sudo apt install jq`).


### Steps to Configure Node 

1. **Install binaries and Download Dogecoin Core**
```bash
cd ~/downloads
curl -L -o dogecoin-1.14.9-x86_64-linux-gnu.tar.gz \
  [https://github.com/dogecoin/dogecoin/releases/download/v1.14.9/dogecoin-1.14.9-x86_64-linux-gnu.tar.gz](https://github.com/dogecoin/dogecoin/releases/download/v1.14.9/dogecoin-1.14.9-x86_64-linux-gnu.tar.gz)

```

2. **Extract and Place Binaries**

```bash
tar xf dogecoin-1.14.9-x86_64-linux-gnu.tar.gz
mkdir -p ~/bin/dogecoin-1.14.9
cp -r dogecoin-1.14.9/* ~/bin/dogecoin-1.14.9/
ln -sf ~/bin/dogecoin-1.14.9/bin/dogecoind ~/dogecoind
ln -sf ~/bin/dogecoin-1.14.9/bin/dogecoin-cli ~/dogecoin-cli

```

3. **Setup Prime Data Directory (for ~/.dogecoin)**

```bash
./dogecoind -datadir=$HOME/.dogecoin -server=1 -listen=0 -daemon
# Wait for RPC to initialize ~30s then stop once RPC is responsive
sleep 30
./dogecoin-cli -datadir=$HOME/.dogecoin stop

```

4. **Configuring RPC Credentials (localhost only)**

```bash
cat > ~/.dogecoin/dogecoin.conf <<'EOF'
server=1
daemon=1
listen=1
rpcbind=127.0.0.1
rpcallowip=127.0.0.1
rpcuser=<strong-username>
rpcpassword=<strong-password>
txindex=1
EOF

```

5. **Start and Sync**

```bash
./dogecoind -datadir=$HOME/.dogecoin -daemon

```

6. **Check sync**

```bash
./dogecoin-cli -datadir=$HOME/.dogecoin getblockcount

./dogecoin-cli -datadir=$HOME/.dogecoin getblockchaininfo
```

---


## RPC/CLI Commands Cheatsheet

### Blockchain Commands

```bash
./dogecoin-cli getblockcount # Get the current block height
./dogecoin-cli getblockchaininfo # Detailed blockchain stats
./dogecoin-cli getbestblockhash # Get the hash of the latest block
./dogecoin-cli getblockhash <height> # Get the hash of a block 
./dogecoin-cli getblock <blockhash> # Details for a specific block

```

### Network, Utility, & Wallet Commands

```bash
./dogecoin-cli getconnectioncount # Number of peer connections
./dogecoin-cli getpeerinfo # Info about connected peers
./dogecoin-cli addnode <address> onetry # Try a one-time connection to a node
./dogecoin-cli ping # Ping all connected nodes
./dogecoin-cli getnewaddress # Generate a new receiving address
./dogecoin-cli getwalletinfo # Wallet details (balance, etc.)
./dogecoin-cli listunspent # List all unspent transactions
./dogecoin-cli sendtoaddress <address> <amount> # Send DOGE
./dogecoin-cli dumpprivkey <address> # Export private key for an address (use this with extreme caution its for backing up your key or using it elsewhere if needed , THIS WILL PRINT YOUR CURRENT PRIV KEY, CAUTION!!)

./dogecoin-cli stop # Stop the Dogecoin node safely
./dogecoin-cli help # List all available commands and usage details
```

For dynamic queries beyond this list, always refer to: `./dogecoin-cli help`.


---


## Automated Health Check (v1.0.5 Robustness Update)

The health check now includes blockchain metadata parsing, disk monitoring, and live price fetching from CoinGecko.

### Health Check Script Setup:

1. Create the script at `~/.openclaw/workspace/archive/health/doge_health_check.sh`:

```bash
mkdir -p ~/.openclaw/workspace/archive/health/

cat > ~/.openclaw/workspace/archive/health/doge_health_check.sh <<'EOF'
#!/bin/bash

# --- Dogecoin Health Check Automation ---
echo "Starting Health Check: $(date)"
DOGE_CLI="$HOME/dogecoin-cli"
DATA_DIR="$HOME/.dogecoin"
COINGECKO_API="[https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd](https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd)"

# 1. Check Node Process
if pgrep -x "dogecoind" > /dev/null; then
    echo "[PASS] Dogecoin node process detected."
else
    echo "[FAIL] Dogecoin node is offline. Attempting restart..."
    ~/dogecoind -datadir=$DATA_DIR -daemon
fi

# 2. Blockchain Sync & Status
NODE_INFO=$($DOGE_CLI -datadir=$DATA_DIR getblockchaininfo 2>/dev/null)
if [ $? -eq 0 ]; then
    CHAIN=$(echo $NODE_INFO | jq -r '.chain')
    BLOCKS=$(echo $NODE_INFO | jq -r '.blocks')
    PROGRESS=$(echo $NODE_INFO | jq -r '.verificationprogress')
    SYNC_PCT=$(echo "$PROGRESS * 100" | bc 2>/dev/null || echo "0")
    echo "[PASS] Chain: $CHAIN | Height: $BLOCKS | Sync: ${SYNC_PCT}%"
else
    echo "[FAIL] RPC Unresponsive. Check credentials in dogecoin.conf."
fi

# 3. Market Price Check
PRICE=$(curl -s "$COINGECKO_API" | jq -r '.dogecoin.usd')
if [ "$PRICE" != "null" ] && [ -n "$PRICE" ]; then
    echo "[INFO] Live Price: \$$PRICE USD"
else
    echo "[WARN] Could not fetch market price."
fi

# 4. Disk Space Check
FREE_GB=$(df -BG $DATA_DIR | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$FREE_GB" -lt 10 ]; then
    echo "[CRITICAL] Low Disk Space: Only ${FREE_GB}GB remaining!"
else
    echo "[PASS] Disk Space: ${FREE_GB}GB available."
fi

# 5. Tipping Database Integrity
DB_PATH="$HOME/.openclaw/workspace/archive/tipping/dogecoin_tipping.db"
if [ -f "$DB_PATH" ]; then
    DB_CHECK=$(sqlite3 "$DB_PATH" "PRAGMA integrity_check;")
    if [ "$DB_CHECK" == "ok" ]; then
        echo "[PASS] Tipping database integrity verified."
    else
        echo "[FAIL] Database Error: $DB_CHECK"
    fi
fi

echo "Health Check Complete."
EOF

chmod +x ~/.openclaw/workspace/archive/health/doge_health_check.sh

```

---

## Tipping Integration (Optional Feature):


Once your node is set up and syncing, you can enable the tipping feature. This allows you to send Dogecoin tips, maintain a user wallet database, and log transactions.


### Tipping Script Setup:


# 1. To enable the tipping feature, create dogecoin_tipping.py at:
# ~/.openclaw/workspace/archive/tipping/ with the following code:


```bash
mkdir -p ~/.openclaw/workspace/archive/tipping/

cat > ~/.openclaw/workspace/archive/tipping/dogecoin_tipping.py <<'EOF'
import sqlite3
import time
from typing import Optional

class DogecoinTippingDB:
    def __init__(self, db_path: str = "dogecoin_tipping.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    wallet_address TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp INTEGER NOT NULL
                )
            """)

    def add_user(self, username: str, wallet_address: str) -> bool:
        try:
            with self.conn:
                self.conn.execute("INSERT INTO users (username, wallet_address) VALUES (?, ?)", (username, wallet_address))
            return True
        except sqlite3.IntegrityError:
            return False

    def get_wallet_address(self, username: str) -> Optional[str]:
        result = self.conn.execute("SELECT wallet_address FROM users WHERE username = ?", (username,)).fetchone()
        return result[0] if result else None

    def list_users(self) -> list:
        return [row[0] for row in self.conn.execute("SELECT username FROM users").fetchall()]

    def log_transaction(self, sender: str, receiver: str, amount: float):
        timestamp = int(time.time())
        with self.conn:
            self.conn.execute("INSERT INTO transactions (sender, receiver, amount, timestamp) VALUES (?, ?, ?, ?)", (sender, receiver, amount, timestamp))

    def get_sent_tips(self, sender: str, receiver: str) -> tuple:
        result = self.conn.execute("SELECT COUNT(*), SUM(amount) FROM transactions WHERE sender = ? AND receiver = ?", (sender, receiver)).fetchone()
        return result[0], (result[1] if result[1] else 0.0)

class DogecoinTipping:
    def __init__(self):
        self.db = DogecoinTippingDB()

    def send_tip(self, sender: str, receiver: str, amount: float) -> str:
        if amount <= 0: return "Amount must be > 0."
        if not self.db.get_wallet_address(sender): return f"Sender '{sender}' not found."
        if not self.db.get_wallet_address(receiver): return f"Receiver '{receiver}' not found."
        
        self.db.log_transaction(sender, receiver, amount)
        return f"Logged tip of {amount} DOGE from {sender} to {receiver}."

    def command_list_wallets(self) -> str:
        users = self.db.list_users()
        return "Registered wallets: " + ", ".join(users)

    def command_get_address(self, username: str) -> str:
        address = self.db.get_wallet_address(username)
        if address:
            return f"{username}'s wallet address is {address}."
        return f"User '{username}' not found."

    def command_get_tips(self, sender: str, receiver: str) -> str:
        count, total = self.db.get_sent_tips(sender, receiver)
        return f"{sender} has sent {count} tips totaling {total} DOGE to {receiver}."

if __name__ == "__main__":
    tipping = DogecoinTipping()
    print("Dogecoin Tipping System Initialized...MANY TIPS... MUCH WOW")

    # Sample workflow
    print("Adding users...")
    tipping.db.add_user("alice", "DGKGv8wP8iRJmjdRUEdvVL2b5BywKC65JT")
    tipping.db.add_user("bob", "DBpLvNcR1Zj8B6dKJp4n3XEAT4FmRxbnJb")

    print("Listing wallets...")
    print(tipping.command_list_wallets())

    print("Fetching wallet addresses...")
    print(tipping.command_get_address("alice"))
    print(tipping.command_get_address("bob"))

    print("Sending tips...")
    print(tipping.send_tip("alice", "bob", 12.5))
    print(tipping.send_tip("alice", "bob", 7.5))

    print("Getting tip summary...")
    print(tipping.command_get_tips("alice", "bob"))
EOF
```

---

Technical usage previously documented. Contact for refinement or extensions!