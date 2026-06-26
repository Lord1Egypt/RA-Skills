#!/usr/bin/env python3
"""
Crypto Whale Alert Script
Tracks large on-chain transactions and whale wallet movements
to generate actionable alerts for crypto trading.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from math import log10

# Configurable thresholds
MIN_TX_VALUE_USD = int(os.environ.get("WHALE_MIN_USD", "100000"))  # $100k minimum
ALERT_COOLDOWN_MINUTES = int(os.environ.get("WHALE_COOLDOWN", "60"))

# Known whale addresses (sample - in production load from external source)
WHALE_WALLETS = {
    "0x28C6c06298d514Db089934071355E5743bf21d60": {"label": "Binance Hot", "type": "exchange"},
    "0x21a31Ee1afC51d94C2efCCaa2092aD1028285549": {"label": "Binance 2", "type": "exchange"},
    "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d": {"label": "Binance 3", "type": "exchange"},
    "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE": {"label": "Binance 4", "type": "exchange"},
    "0x21a31Ee1afC51d94C2efCCaa2092aD1028285549": {"label": "FTX", "type": "exchange"},
}

# Mock large transactions (in production, query Blockchair/Etherscan API)
MOCK_TRANSACTIONS = [
    {"hash": "0xabc123", "from": "0x28C6c06298d514Db089934071355E5743bf21d60", "to": "0x47a9d3d...", "value": 25000000, "token": "USDC", "time": datetime.now().isoformat()},
    {"hash": "0xdef456", "from": "0x21a31Ee1afC51d94C2efCCaa2092aD1028285549", "to": "0x58b2c4d...", "value": 15000000, "token": "USDT", "time": datetime.now().isoformat()},
    {"hash": "0xghi789", "from": "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE", "to": "0x69c3d5e...", "value": 500000000, "token": "ETH", "time": datetime.now().isoformat()},
    {"hash": "0xjkl012", "from": "0xd8dA1bfb8b2c54D5E8C6F7E9f0a1B2c3D4e5f6A7", "to": "0x7ad4e6f...", "value": 85000000, "token": "WBTC", "time": datetime.now().isoformat()},
]


def format_value(value: float, token: str) -> str:
    """Format transaction value with appropriate suffix."""
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.2f}K"
    else:
        return f"${value:.2f}"


def get_wallet_label(address: str) -> str:
    """Look up known whale wallet label."""
    return WHALE_WALLETS.get(address, {}).get("label", "Unknown")


def is_watchlisted(address: str) -> bool:
    """Check if address is in our whale list."""
    return address in WHALE_WALLETS


def detect_accumulation_distribution(txs: list) -> dict:
    """Analyze recent transactions to detect accumulation or distribution patterns."""
    if len(txs) < 3:
        return {"pattern": "insufficient_data", "confidence": 0}

    buy_txs = [t for t in txs if t.get("direction") == "inflow"]
    sell_txs = [t for t in txs if t.get("direction") == "outflow"]

    buy_ratio = len(buy_txs) / len(txs) if txs else 0.5

    if buy_ratio > 0.7:
        return {"pattern": "accumulation", "confidence": buy_ratio * 100}
    elif buy_ratio < 0.3:
        return {"pattern": "distribution", "confidence": (1 - buy_ratio) * 100}
    else:
        return {"pattern": "neutral", "confidence": 50}


def generate_alert(tx: dict) -> str:
    """Generate formatted alert message for a whale transaction."""
    value = tx["value"]
    token = tx["token"]
    tx_hash = tx["hash"]
    from_addr = tx["from"]
    to_addr = tx["to"]

    from_label = get_wallet_label(from_addr)
    to_label = get_wallet_label(to_addr) if is_watchlisted(to_addr) else "External"

    direction = "🟢 INFLOW" if from_label != "Unknown" else "🔴 OUTFLOW"

    alert = f"""
🐋 WHALE ALERT 🐋
{'='*40}
{direction} Detected

Token:     {token}
Value:     {format_value(value, token)}
From:      {from_label} ({from_addr[:10]}...)
To:        {to_label} ({to_addr[:10]}...)
Time:      {tx['time'][:19]}

Tx Hash:   {tx_hash}
Link:      https://etherscan.io/tx/{tx_hash}

#WhaleAlert #Crypto
"""
    return alert.strip()


def check_transactions(transactions: list, min_value: int = MIN_TX_VALUE_USD) -> list:
    """Filter transactions that meet whale threshold criteria."""
    whale_txs = []
    for tx in transactions:
        if tx["value"] >= min_value:
            whale_txs.append(tx)
    return whale_txs


def print_alerts(transactions: list) -> None:
    """Print all whale alerts to console."""
    whale_txs = check_transactions(transactions)

    if not whale_txs:
        print(f"\nNo whale transactions above ${MIN_TX_VALUE_USD:,} threshold in this scan.")
        return

    print(f"\n🐋 WHALE ALERTS - {len(whale_txs)} detected")
    print(f"Threshold: ${MIN_TX_VALUE_USD:,} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for tx in whale_txs:
        print(generate_alert(tx))
        print()


def get_whale_summary() -> None:
    """Get summary of recent whale activity."""
    whale_txs = check_transactions(MOCK_TRANSACTIONS)

    print("\n" + "=" * 60)
    print("  CRYPTO WHALE ACTIVITY SUMMARY")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    if not whale_txs:
        print("\nNo significant whale activity detected.")
        return

    total_value = sum(tx["value"] for tx in whale_txs)
    tokens = set(tx["token"] for tx in whale_txs)

    print(f"\nWhale Txs:    {len(whale_txs)}")
    print(f"Total Value:  ${total_value:,.0f}")
    print(f"Tokens:       {', '.join(tokens)}")
    print(f"Watchlist:    {len(WHALE_WALLETS)} addresses tracked")
    print()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"

    if cmd == "scan":
        print_alerts(MOCK_TRANSACTIONS)

    elif cmd == "summary":
        get_whale_summary()

    elif cmd == "watch":
        print("\nWatched Whale Wallets:\n")
        for addr, info in WHALE_WALLETS.items():
            print(f"  {info['label']:20s} | {addr[:20]}...")
            print(f"  Type: {info['type']}")
            print()

    elif cmd == "set-threshold" and len(sys.argv) > 2:
        new_threshold = int(sys.argv[2])
        print(f"Whale threshold set to ${new_threshold:,}")

    else:
        print("Usage:")
        print("  python whale_alerts.py scan       - Scan for whale transactions")
        print("  python whale_alerts.py summary    - Get whale activity summary")
        print("  python whale_alerts.py watch      - List watched whale wallets")
        print("  python whale_alerts.py set-threshold <usd>  - Set alert threshold")


if __name__ == "__main__":
    main()