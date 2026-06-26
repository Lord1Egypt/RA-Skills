#!/usr/bin/env python3
"""
Output formatters for crypto analytics data - V2 compatible
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from decimal import Decimal

def format_eth_balance(balance_wei: int) -> str:
    """Format ETH balance with proper decimal places"""
    eth = Decimal(balance_wei) / Decimal('1000000000000000000')
    return f"{eth:.6f} ETH"

def format_btc_balance(sats: int) -> str:
    """Format Bitcoin balance"""
    btc = Decimal(sats) / Decimal('100000000')
    return f"{btc:.8f} BTC"

def format_sol_balance(lamports: int) -> str:
    """Format Solana balance"""
    sol = Decimal(lamports) / Decimal('1000000000')
    return f"{sol:.6f} SOL"

def format_usd(value: float, price: float) -> str:
    """Format USD value"""
    usd = Decimal(value) * Decimal(price)
    return f"${usd:,.2f}"

def format_timestamp(timestamp: int) -> str:
    """Format unix timestamp to human readable"""
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def hex_to_int(hex_str: Any, default: int = 0) -> int:
    """Convert hex string or decimal string to int"""
    if not hex_str:
        return default
    s = str(hex_str)
    if s.startswith('0x'):
        return int(s, 16)
    try:
        return int(s)
    except (ValueError, TypeError):
        return default

def format_etherscan_tx(tx: Dict) -> str:
    """Format an Ethereum transaction (V2 compatible)"""
    # Handle both V1 (decimal strings) and V2 (hex strings)
    block_number = hex_to_int(tx.get('blockNumber'))
    block_hash = tx.get('blockHash', 'N/A')
    tx_hash = tx.get('hash', 'N/A')
    from_addr = tx.get('from', 'N/A')
    to_addr = tx.get('to', 'N/A')
    if not to_addr and tx.get('contractAddress'):
        to_addr = f"Contract: {tx['contractAddress']}"

    # Value in wei (V2: hex, V1: decimal string)
    value_wei = hex_to_int(tx.get('value', 0))
    value_eth = Decimal(value_wei) / Decimal('1000000000000000000')

    # Gas fields
    gas_used = hex_to_int(tx.get('gasUsed', 0))
    gas_limit = hex_to_int(tx.get('gas', 0))
    gas_price_wei = hex_to_int(tx.get('gasPrice', 0))
    gas_price_gwei = Decimal(gas_price_wei) / Decimal('1000000000')

    # Timestamp (V2: hex, V1: decimal string)
    timestamp = hex_to_int(tx.get('timeStamp') or tx.get('blockTimestamp', 0))

    lines = [
        f"TxHash: {tx_hash}",
        f"Block: {block_number}",
        f"Block Hash: {block_hash[:20]}..." if block_hash != 'N/A' else "Block Hash: N/A",
        f"From: {from_addr}",
        f"To: {to_addr}",
        f"Value: {value_eth:.6f} ETH",
        f"Gas Limit: {gas_limit:,}",
        f"Gas Used: {gas_used:,}",
        f"Gas Price: {gas_price_gwei:.2f} Gwei",
        f"Nonce: {hex_to_int(tx.get('nonce'), 0):,}",
        f"Timestamp: {format_timestamp(timestamp) if timestamp else 'N/A'}",
        f"Status: {'Success' if tx.get('txreceipt_status') == '1' or tx.get('status') == '1' else 'Failed' if tx.get('isError') == '1' or tx.get('status') == '0' else 'Pending'}"
    ]
    return '\n'.join(lines)

def format_blockchair_tx(tx: Dict) -> str:
    """Format a Bitcoin/other chain transaction for display"""
    lines = [
        f"TxHash: {tx.get('transaction_hash', 'N/A')}",
        f"Block: {tx.get('block_id', 'N/A')}",
        f"Time: {tx.get('time', 'N/A')}",
    ]
    if 'input' in tx:
        lines.append(f"Input Addresses: {', '.join(tx.get('input', []))}")
    if 'output' in tx:
        lines.append(f"Output Addresses: {', '.join(tx.get('output', []))}")
    lines.extend([
        f"Value (BTC): {tx.get('value', 0) / 100000000:.8f}",
        f"Confirmations: {tx.get('confirmations', 'N/A')}"
    ])
    return '\n'.join(lines)

def format_wallet_summary(data: Dict) -> str:
    """Create a human-readable wallet summary"""
    chain = data.get('chain', 'unknown').upper()
    address = data.get('address', 'N/A')

    lines = [f"=== Wallet Summary ===", f"Chain: {chain}", f"Address: {address}"]

    if 'balance_eth' in data:
        lines.append(f"Balance: {format_eth_balance(data['balance_wei'])}")
    if 'balance_btc' in data:
        lines.append(f"Balance: {format_btc_balance(data['balance_sats'])}")
    if 'balance_sol' in data:
        lines.append(f"Balance: {format_sol_balance(data['balance_lamports'])}")

    # Token balances
    if 'tokens' in data:
        lines.append("\n--- Token Balances ---")
        for token in data['tokens'][:5]:  # limit to 5 tokens
            symbol = token.get('symbol', '???')
            balance = token.get('balance', 0)
            decimals = token.get('decimals', 18)
            contract = token.get('contract', '')
            lines.append(f"  {symbol}: {balance / (10**decimals):.6f} ({contract[:20]}...)")

    if 'transaction_count' in data:
        lines.append(f"\nTotal Transactions: {data['transaction_count']}")

    return '\n'.join(lines)

def format_transaction_list(transactions: List[Dict], chain: str) -> List[str]:
    """Format list of transactions for display"""
    output = []
    for i, tx in enumerate(transactions[:10], 1):  # Limit to 10
        output.append(f"\n--- Transaction #{i} ---")
        if chain == 'ethereum':
            output.append(format_etherscan_tx(tx))
        elif chain in ('bitcoin', 'litecoin', 'dogecoin'):
            output.append(format_blockchair_tx(tx))
        else:
            output.append(f"Raw data: {tx}")
    return output

def format_gas_price(gas_data: Dict) -> str:
    """Format current gas price information"""
    lines = ["=== Gas Price Tracker ==="]

    # Safe, Standard, Fast (gwei)
    if 'low' in gas_data:
        lines.append(f"Safe: {gas_data['low'] / 1e9:.2f} Gwei")
    if 'standard' in gas_data:
        lines.append(f"Standard: {gas_data['standard'] / 1e9:.2f} Gwei")
    if 'fast' in gas_data:
        lines.append(f"Fast: {gas_data['fast'] / 1e9:.2f} Gwei")

    # Base fee (EIP-1559)
    if 'base_fee' in gas_data:
        lines.append(f"Base Fee: {gas_data['base_fee'] / 1e9:.2f} Gwei")

    # Timestamp
    if 'timestamp' in gas_data:
        lines.append(f"Updated: {format_timestamp(gas_data['timestamp'])}")

    return '\n'.join(lines)

def format_token_balance(tokens: List[Dict]) -> str:
    """Format ERC-20 token balances"""
    if not tokens:
        return "No token balances found."

    lines = ["=== Token Balances ==="]
    for token in tokens:
        symbol = token.get('symbol', '???')
        name = token.get('name', '')
        balance = token.get('balance', 0)
        decimals = token.get('decimals', 18)
        contract = token.get('contract', '')

        # Convert from smallest unit
        human_balance = Decimal(balance) / (10 ** decimals)

        lines.append(f"{symbol} ({name})")
        lines.append(f"  Balance: {human_balance:,.6f}")
        lines.append(f"  Contract: {contract}")
        lines.append("")

    return '\n'.join(lines)

if __name__ == '__main__':
    # Test with V2 format
    sample_tx = {
        'hash': '0xcea44b227b9052e199f7f1941dca226175e1cf4e714d340a20a1e5304ba52864',
        'blockNumber': '0x17a0bb2',
        'blockHash': '0x0f1a4555d25395de34649486c31648856f89ff4a537ebb2d307aace74c01e50e',
        'timeStamp': '1774936187',
        'from': '0x28c6c06298d514db089934071355e5743bf21d60',
        'to': '0xbbbbca6a901c926f240b89eacb641d8aec7aeafd',
        'value': '0x0',
        'gas': '0x32918',
        'gasPrice': '0x445d2a60',
        'gasUsed': '0xca2f',
        'nonce': '0xf348a4',
        'txreceipt_status': '1'
    }
    print(format_etherscan_tx(sample_tx))
    print("\n--- Gas price test ---")
    print(format_gas_price({'low': 20000000000, 'standard': 50000000000, 'fast': 80000000000, 'base_fee': 15000000000, 'timestamp': 1774936187}))
