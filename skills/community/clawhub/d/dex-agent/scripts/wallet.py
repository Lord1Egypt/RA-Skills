"""
Wallet Manager — Generate and manage trading wallets
Stores encrypted private keys locally. Never transmits keys externally.
"""

import json
import os
import sys
from pathlib import Path
from eth_account import Account
from web3 import Web3

WALLET_DIR = Path(__file__).parent / "wallets"
WALLET_FILE = WALLET_DIR / "trading-wallet.json"


def generate_wallet():
    """Generate a new trading wallet."""
    account = Account.create()
    wallet_data = {
        "address": account.address,
        "private_key": account.key.hex(),
        "note": "DEX Agent trading wallet. NEVER share this key. Generated locally."
    }

    WALLET_DIR.mkdir(exist_ok=True)
    with open(WALLET_FILE, "w") as f:
        json.dump(wallet_data, f, indent=2)
    os.chmod(WALLET_FILE, 0o600)

    print(f"✅ Wallet generated: {account.address}")
    print(f"   Saved to: {WALLET_FILE}")
    print(f"   ⚠️  Fund this wallet with ETH (for gas) and USDC (for trading)")
    return account.address


def load_wallet():
    """Load the trading wallet."""
    if not WALLET_FILE.exists():
        print("❌ No wallet found. Run: python3 wallet.py generate")
        return None, None

    with open(WALLET_FILE) as f:
        data = json.load(f)

    return data["address"], data["private_key"]


def get_balances(address):
    """Get ETH and token balances for a wallet."""
    from config import RPC_URL, TOKENS

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Cannot connect to Base RPC")
        return

    # ETH balance
    eth_bal = w3.from_wei(w3.eth.get_balance(address), "ether")
    print(f"\n📊 Balances for {address[:10]}...{address[-6:]}")
    print(f"   ETH: {eth_bal:.6f}")

    # ERC20 balances
    erc20_abi = [{"constant": True, "inputs": [{"name": "account", "type": "address"}],
                  "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],
                  "type": "function"},
                 {"constant": True, "inputs": [], "name": "decimals",
                  "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
                 {"constant": True, "inputs": [], "name": "symbol",
                  "outputs": [{"name": "", "type": "string"}], "type": "function"}]

    for name, addr in TOKENS.items():
        try:
            contract = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=erc20_abi)
            balance = contract.functions.balanceOf(address).call()
            decimals = contract.functions.decimals().call()
            human_balance = balance / (10 ** decimals)
            if human_balance > 0:
                print(f"   {name}: {human_balance:,.4f}")
        except Exception as e:
            pass


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generate_wallet()
    elif len(sys.argv) > 1 and sys.argv[1] == "balances":
        addr, _ = load_wallet()
        if addr:
            get_balances(addr)
    else:
        addr, _ = load_wallet()
        if addr:
            print(f"Wallet: {addr}")
            get_balances(addr)
        else:
            print("Usage: python3 wallet.py [generate|balances]")
