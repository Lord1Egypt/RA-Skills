#!/usr/bin/env python3
"""
Bitcoin L1 Blockchain CLI Tool for Hermes Agent
-----------------------------------------------
Queries the Bitcoin blockchain via Mempool.space REST API and CoinGecko for BTC pricing.
Uses only Python standard library — no external packages required.

Usage:
  python3 bitcoin_client.py address   <address> [--limit N]
  python3 bitcoin_client.py tx        <txid>
  python3 bitcoin_client.py fees
  python3 bitcoin_client.py mempool
  python3 bitcoin_client.py blocks    [--limit N]
  python3 bitcoin_client.py stats
  python3 bitcoin_client.py price     [--currency CURRENCY]

Environment:
  BITCOIN_API_URL     Override Mempool.space API endpoint (default: https://mempool.space/api)
  COINGECKO_API_KEY   Optional CoinGecko API key for better rate limits
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# Constants
SATOSHI_PER_BTC = 100_000_000
MEMPOOL_API_DEFAULT = "https://mempool.space/api"

# Supported currencies for price conversion
SUPPORTED_CURRENCIES = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CHF": "CHF",
    "CAD": "CAD",
    "AUD": "AUD",
    "SGD": "SGD",
    "INR": "₹",
    "HKD": "HK$",
}


# ---------------------------------------------------------------------------
# HTTP / API helpers
# ---------------------------------------------------------------------------

def _get_mempool_api_url() -> str:
    """Get Mempool.space API base URL, with optional override from environment."""
    # Inline: load API URL at point of use, never extract to module-level
    try:
        from dotenv import dotenv_values
        env_data = dotenv_values()
        api_url = env_data.get("BITCOIN_API_URL") or MEMPOOL_API_DEFAULT
    except Exception:
        api_url = MEMPOOL_API_DEFAULT
    
    return api_url


def _http_get_json(url: str, timeout: int = 10, retries: int = 2) -> Optional[Any]:
    """GET JSON from a URL with retry on 429 rate-limit. Returns parsed JSON or None."""
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": "HermesAgent/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries:
                time.sleep(2.0 * (attempt + 1))
                continue
            return None
        except Exception:
            return None
    return None


def _get_price_usd(currency: str = "USD") -> Optional[float]:
    """Get current BTC price in specified currency from CoinGecko."""
    currency_lower = currency.lower()
    
    # Load CoinGecko API key inline at point of use
    try:
        from dotenv import dotenv_values
        env_data = dotenv_values()
        cg_key = env_data.get("COINGECKO_API_KEY", "") or ""
    except Exception:
        cg_key = ""
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency_lower}"
    
    # Inline: use key immediately if available
    if cg_key:
        url += f"&x_cg_pro_api_key={cg_key}"
    
    data = _http_get_json(url, timeout=10, retries=1)
    if data and "bitcoin" in data and currency_lower in data["bitcoin"]:
        return data["bitcoin"][currency_lower]
    return None


def _format_satoshis(sat: int, price_usd: Optional[float] = None, currency: str = "USD") -> str:
    """Format satoshis as BTC + currency value."""
    btc = sat / SATOSHI_PER_BTC
    btc_str = f"{btc:.8f} BTC".rstrip("0").rstrip(".")
    
    if price_usd is None:
        return btc_str
    
    usd_value = btc * price_usd
    currency_symbol = SUPPORTED_CURRENCIES.get(currency, currency)
    
    if currency == "JPY":
        return f"{btc_str} ({currency_symbol}{usd_value:,.0f})"
    else:
        return f"{btc_str} ({currency_symbol}{usd_value:,.2f})"


def _format_time_relative(timestamp: int) -> str:
    """Convert unix timestamp to relative time string (e.g., '2 hours ago')."""
    now = datetime.utcnow()
    dt = datetime.utcfromtimestamp(timestamp)
    diff = now - dt
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} min{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


def _get_address_type(address: str) -> str:
    """Detect Bitcoin address type from prefix/format."""
    if address.startswith("1"):
        return "P2PKH (Legacy)"
    elif address.startswith("3"):
        return "P2SH (Legacy)"
    elif address.startswith("bc1q"):
        return "P2WPKH (SegWit v0)"
    elif address.startswith("bc1p"):
        return "P2TR (Taproot)"
    elif address.lower().startswith("bc1"):
        return "Bech32 (SegWit)"
    else:
        return "Unknown"


# ---------------------------------------------------------------------------
# Bitcoin API commands
# ---------------------------------------------------------------------------

def cmd_address(address: str, limit: int = 20, currency: str = "USD") -> None:
    """Get address balance, UTXO info, and transaction history."""
    print(f"\n📍 Bitcoin Address: {address}")
    print(f"   Type: {_get_address_type(address)}")
    print()
    
    # Get address data from Mempool (inline: get URL here)
    api_url = _get_mempool_api_url()
    url = f"{api_url}/address/{address}"
    data = _http_get_json(url)
    
    if not data:
        print("❌ Failed to fetch address data. Address may not exist or API is down.")
        return
    
    # Get price for conversions
    price = _get_price_usd(currency)
    price_usd = price if currency == "USD" else price  # Convert if needed
    
    # Extract key metrics
    confirmed_balance = data.get("chain_stats", {}).get("funded_txo_sum", 0)
    spent_balance = data.get("chain_stats", {}).get("spent_txo_sum", 0)
    unconfirmed_balance = data.get("mempool_stats", {}).get("funded_txo_sum", 0) - data.get("mempool_stats", {}).get("spent_txo_sum", 0)
    
    total_received = confirmed_balance + spent_balance
    current_balance = confirmed_balance + unconfirmed_balance
    
    tx_count = data.get("chain_stats", {}).get("tx_count", 0) + data.get("mempool_stats", {}).get("tx_count", 0)
    
    print(f"💰 Balance:")
    print(f"   Confirmed:   {_format_satoshis(confirmed_balance, price_usd, currency)}")
    print(f"   Unconfirmed: {_format_satoshis(unconfirmed_balance, price_usd, currency)}")
    print(f"   Total:       {_format_satoshis(current_balance, price_usd, currency)}")
    print()
    
    print(f"📊 Statistics:")
    print(f"   Total Received:  {_format_satoshis(total_received, price_usd, currency)}")
    print(f"   Total Spent:     {_format_satoshis(spent_balance, price_usd, currency)}")
    print(f"   Transaction Count: {tx_count}")
    print()
    
    # Get UTXOs
    url_utxos = f"{api_url}/address/{address}/utxo"
    utxos = _http_get_json(url_utxos)
    
    if utxos:
        print(f"🔑 UTXOs ({len(utxos)} total):")
        
        # Sort by value descending
        utxos_sorted = sorted(utxos, key=lambda x: x.get("value", 0), reverse=True)[:limit]
        
        for i, utxo in enumerate(utxos_sorted, 1):
            value = utxo.get("value", 0)
            txid = utxo.get("txid", "")[:16] + "..."
            confirmed = "✓ Confirmed" if utxo.get("status", {}).get("confirmed") else "⏳ Unconfirmed"
            print(f"   {i}. {_format_satoshis(value, price_usd, currency)} - {txid} ({confirmed})")
        
        if len(utxos) > limit:
            print(f"   ... and {len(utxos) - limit} more UTXOs")


def cmd_tx(txid: str, currency: str = "USD") -> None:
    """Get transaction details."""
    print(f"\n🔗 Bitcoin Transaction: {txid[:16]}...")
    print()
    
    # Get tx data (inline: get URL here)
    api_url = _get_mempool_api_url()
    url = f"{api_url}/tx/{txid}"
    tx = _http_get_json(url)
    
    if not tx:
        print("❌ Failed to fetch transaction. TXID may be invalid or API is down.")
        return
    
    # Get price
    price = _get_price_usd(currency)
    
    # Get status
    url_status = f"{api_url}/tx/{txid}/status"
    status = _http_get_json(url_status)
    confirmed = status.get("confirmed", False) if status else False
    block_height = status.get("block_height") if status else None
    block_time = status.get("block_time") if status else None
    
    # Calculate inputs/outputs
    total_in = sum(inp.get("prevout", {}).get("value", 0) for inp in tx.get("vin", []))
    total_out = sum(out.get("value", 0) for out in tx.get("vout", []))
    fee = total_in - total_out
    
    tx_size = tx.get("size", 0)
    vsize = tx.get("vsize", tx_size)  # Virtual size for fee calculation
    
    fee_rate = (fee / vsize) if vsize > 0 else 0
    
    print(f"📋 Transaction Info:")
    print(f"   TXID: {txid}")
    print(f"   Status: {'✓ Confirmed' if confirmed else '⏳ Unconfirmed'}")
    if block_height:
        print(f"   Block Height: {block_height}")
    if block_time:
        print(f"   Block Time: {_format_time_relative(block_time)}")
    print()
    
    print(f"💸 Value:")
    print(f"   Input Total:  {_format_satoshis(total_in, price, currency)}")
    print(f"   Output Total: {_format_satoshis(total_out, price, currency)}")
    print(f"   Fee: {fee} satoshis ({fee_rate:.2f} sat/vB) = {_format_satoshis(fee, price, currency)}")
    print()
    
    print(f"📦 Size:")
    print(f"   Raw Size: {tx_size} bytes")
    print(f"   Virtual Size (vB): {vsize}")
    print()
    
    # Inputs
    print(f"📥 Inputs ({len(tx.get('vin', []))} total):")
    for i, inp in enumerate(tx.get("vin", [])[:5], 1):
        prev_value = inp.get("prevout", {}).get("value", 0)
        prev_addr = inp.get("prevout", {}).get("scriptpubkey_address", "N/A")
        print(f"   {i}. {_format_satoshis(prev_value, price, currency)} from {prev_addr}")
    if len(tx.get("vin", [])) > 5:
        print(f"   ... and {len(tx.get('vin', [])) - 5} more inputs")
    print()
    
    # Outputs
    print(f"📤 Outputs ({len(tx.get('vout', []))} total):")
    for i, out in enumerate(tx.get("vout", [])[:5], 1):
        value = out.get("value", 0)
        addr = out.get("scriptpubkey_address", "N/A")
        print(f"   {i}. {_format_satoshis(value, price, currency)} to {addr}")
    if len(tx.get("vout", [])) > 5:
        print(f"   ... and {len(tx.get('vout', [])) - 5} more outputs")


def cmd_fees(currency: str = "USD") -> None:
    """Get current fee estimates."""
    print(f"\n⛽ Bitcoin Network Fees")
    print()
    
    api_url = _get_mempool_api_url()
    url = f"{api_url}/v1/fees/recommended"
    fees = _http_get_json(url)
    
    if not fees:
        print("❌ Failed to fetch fee estimates.")
        return
    
    price = _get_price_usd(currency)
    
    print(f"📊 Fee Estimates (sat/vB):")
    print(f"   Slow (24h):     {fees.get('hourFee', 'N/A')} sat/vB")
    print(f"   Standard (10m): {fees.get('halfHourFee', 'N/A')} sat/vB")
    print(f"   Fast (1m):      {fees.get('fastestFee', 'N/A')} sat/vB")
    print()
    
    # Estimate tx cost for 250 vB (typical tx)
    if price:
        typical_vsize = 250
        std_fee_sat = fees.get('halfHourFee', 1) * typical_vsize
        std_fee_btc = std_fee_sat / SATOSHI_PER_BTC
        
        currency_symbol = SUPPORTED_CURRENCIES.get(currency, currency)
        std_fee_usd = std_fee_btc * price
        
        if currency == "JPY":
            fee_str = f"{currency_symbol}{std_fee_usd:,.0f}"
        else:
            fee_str = f"{currency_symbol}{std_fee_usd:,.2f}"
        
        print(f"💡 Typical 250vB transaction fee (standard):")
        print(f"   {std_fee_sat} sat ({std_fee_btc:.8f} BTC ≈ {fee_str})")
    print()


def cmd_mempool(currency: str = "USD") -> None:
    """Get mempool statistics."""
    print(f"\n💾 Bitcoin Mempool")
    print()
    
    api_url = _get_mempool_api_url()
    url = f"{api_url}/mempool"
    mempool = _http_get_json(url)
    
    if not mempool:
        print("❌ Failed to fetch mempool data.")
        return
    
    # Extract stats
    tx_count = mempool.get("count", 0)
    mempool_bytes = mempool.get("vsize", 0)  # Virtual size in bytes
    mempool_mb = mempool_bytes / 1_000_000
    total_fees = mempool.get("total_fee_sat", 0)
    
    # Fee distribution
    fee_histogram = mempool.get("fee_histogram", [])
    
    price = _get_price_usd(currency)
    
    print(f"📊 Mempool State:")
    print(f"   Pending Transactions: {tx_count}")
    print(f"   Mempool Size: {mempool_mb:.2f} MB ({mempool_bytes:,} vB)")
    print(f"   Total Fees Pending: {_format_satoshis(total_fees, price, currency)}")
    print()
    
    if fee_histogram:
        print(f"⛽ Fee Distribution (sat/vB | cumulative tx count):")
        cumulative = 0
        for fee_range, count in fee_histogram[:10]:
            cumulative += count
            print(f"   {fee_range:>8} sat/vB: {count:>6} tx (cumulative: {cumulative})")


def cmd_blocks(limit: int = 10, currency: str = "USD") -> None:
    """Get recent blocks."""
    print(f"\n📦 Recent Bitcoin Blocks (last {limit})")
    print()
    
    api_url = _get_mempool_api_url()
    url = f"{api_url}/blocks"
    blocks = _http_get_json(url)
    
    if not blocks:
        print("❌ Failed to fetch block data.")
        return
    
    price = _get_price_usd(currency)
    
    for i, block in enumerate(blocks[:limit], 1):
        height = block.get("height", "N/A")
        hash_str = block.get("id", "")[:8] + "..." + block.get("id", "")[-8:] if block.get("id") else "N/A"
        time = _format_time_relative(block.get("timestamp", 0))
        tx_count = block.get("tx_count", 0)
        size_kb = block.get("size", 0) / 1024
        
        print(f"   {i}. Block {height} ({hash_str})")
        print(f"      Time: {time} | TXs: {tx_count} | Size: {size_kb:.1f} KB")


def cmd_stats(currency: str = "USD") -> None:
    """Get network statistics."""
    print(f"\n🌐 Bitcoin Network Statistics")
    print()
    
    # Get latest block height (inline: get URL here)
    api_url = _get_mempool_api_url()
    url_tip = f"{api_url}/blocks/tip/height"
    tip_height = _http_get_json(url_tip)
    
    # Get mempool stats
    url_mempool = f"{api_url}/mempool"
    mempool = _http_get_json(url_mempool)
    
    # Get fee estimates
    url_fees = f"{api_url}/v1/fees/recommended"
    fees = _http_get_json(url_fees)
    
    # Get price
    price = _get_price_usd(currency)
    price_str = f"{SUPPORTED_CURRENCIES.get(currency, currency)}{price:,.2f}" if price else "N/A"
    
    print(f"📊 Chain Status:")
    print(f"   Latest Block Height: {tip_height if tip_height else 'N/A'}")
    print(f"   Current Time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if mempool:
        tx_count = mempool.get("count", 0)
        mempool_mb = mempool.get("vsize", 0) / 1_000_000
        print(f"💾 Mempool:")
        print(f"   Pending Transactions: {tx_count}")
        print(f"   Pool Size: {mempool_mb:.2f} MB")
        print()
    
    if fees:
        print(f"⛽ Fee Environment:")
        print(f"   Slow: {fees.get('hourFee', 'N/A')} sat/vB (24h)")
        print(f"   Standard: {fees.get('halfHourFee', 'N/A')} sat/vB (10m)")
        print(f"   Fast: {fees.get('fastestFee', 'N/A')} sat/vB (1m)")
        print()
    
    print(f"💰 Price:")
    print(f"   BTC/USD: {price_str}")
    print()


def cmd_price(currency: str = "USD") -> None:
    """Get BTC price."""
    price = _get_price_usd(currency)
    
    if price:
        currency_symbol = SUPPORTED_CURRENCIES.get(currency, currency)
        if currency == "JPY":
            print(f"\n💰 BTC Price: {currency_symbol}{price:,.0f}")
        else:
            print(f"\n💰 BTC Price: {currency_symbol}{price:,.2f}")
    else:
        print(f"\n❌ Failed to fetch BTC price.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Bitcoin L1 blockchain CLI tool for Hermes Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 bitcoin_client.py address 1A1z7agoat3bLsCywJ6H7qqyiB8t6SE2Kt
  python3 bitcoin_client.py tx 1e4e745d32e6cfbb7ee778cdec5d9e5be1b5ea3c5f9c8d3e1b5a3f9e6d7c4b1a
  python3 bitcoin_client.py fees
  python3 bitcoin_client.py mempool
  python3 bitcoin_client.py blocks --limit 5
  python3 bitcoin_client.py stats
  python3 bitcoin_client.py price --currency EUR
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Address command
    addr_parser = subparsers.add_parser("address", help="Get address info")
    addr_parser.add_argument("address", help="Bitcoin address")
    addr_parser.add_argument("--limit", type=int, default=20, help="Max UTXOs to show (default: 20)")
    addr_parser.add_argument("--currency", default="USD", help="Currency for prices (default: USD)")
    
    # TX command
    tx_parser = subparsers.add_parser("tx", help="Get transaction details")
    tx_parser.add_argument("txid", help="Transaction ID (TXID)")
    tx_parser.add_argument("--currency", default="USD", help="Currency for prices (default: USD)")
    
    # Fees command
    fees_parser = subparsers.add_parser("fees", help="Get fee estimates")
    fees_parser.add_argument("--currency", default="USD", help="Currency for prices (default: USD)")
    
    # Mempool command
    mempool_parser = subparsers.add_parser("mempool", help="Get mempool stats")
    mempool_parser.add_argument("--currency", default="USD", help="Currency for prices (default: USD)")
    
    # Blocks command
    blocks_parser = subparsers.add_parser("blocks", help="Get recent blocks")
    blocks_parser.add_argument("--limit", type=int, default=10, help="Number of blocks to show (default: 10)")
    blocks_parser.add_argument("--currency", default="USD", help="Currency for prices (default: USD)")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get network stats")
    stats_parser.add_argument("--currency", default="USD", help="Currency for prices (default: USD)")
    
    # Price command
    price_parser = subparsers.add_parser("price", help="Get BTC price")
    price_parser.add_argument("--currency", default="USD", help="Currency for price (default: USD)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == "address":
            cmd_address(args.address, args.limit, args.currency)
        elif args.command == "tx":
            cmd_tx(args.txid, args.currency)
        elif args.command == "fees":
            cmd_fees(args.currency)
        elif args.command == "mempool":
            cmd_mempool(args.currency)
        elif args.command == "blocks":
            cmd_blocks(args.limit, args.currency)
        elif args.command == "stats":
            cmd_stats(args.currency)
        elif args.command == "price":
            cmd_price(args.currency)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
