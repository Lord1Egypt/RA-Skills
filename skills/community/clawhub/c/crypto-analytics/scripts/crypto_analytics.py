#!/usr/bin/env python3
"""
Crypto Analytics Skill - Main entry point

Command-line interface for blockchain analysis operations
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any
from decimal import Decimal

# Add skill directory to path
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / 'scripts'))

from crypto_api import CryptoAPIClient
from address_validator import AddressValidator
from formatter import (
    format_wallet_summary,
    format_etherscan_tx,
    format_blockchair_tx,
    format_transaction_list,
    format_token_balance
)

def cmd_wallet_balance(address: str, chain: str = None) -> Dict[str, Any]:
    """Get wallet balance"""
    client = CryptoAPIClient()
    chain = chain or client.detect_chain(address)
    result = client.get_wallet_balance(address, chain)

    if 'error' not in result:
        # Add human-readable formatted output
        result['formatted'] = format_wallet_summary(result)

    return result

def cmd_wallet_transactions(address: str, chain: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get wallet transaction history"""
    client = CryptoAPIClient()
    chain = chain or client.detect_chain(address)
    result = client.get_transactions(address, chain, limit)

    if 'error' not in result and 'transactions' in result:
        formatted = format_transaction_list(result['transactions'], chain)
        result['formatted_transactions'] = formatted[:10]  # Limit output size

    return result

def cmd_token_transfers(address: str, token_contract: str = None, chain: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get ERC-20 token transfer history. If token_contract is provided, filter for that token; else show all token transfers."""
    client = CryptoAPIClient()
    chain = chain or client.detect_chain(address)
    result = client.get_token_transfers(address, chain, token_contract, limit)

    if 'error' not in result and 'transfers' in result:
        # Format transfers similar to transactions
        result['formatted_transfers'] = format_transaction_list(result['transfers'], chain)[:10]
    return result

def cmd_transaction_details(txhash: str, chain: str) -> Dict[str, Any]:
    """Get transaction details by hash"""
    client = CryptoAPIClient()
    result = client.get_transaction_details(txhash, chain)

    if 'error' not in result:
        tx = result.get('transaction', {})
        if chain == 'ethereum':
            result['formatted'] = format_etherscan_tx(tx)
        elif chain in ('bitcoin', 'litecoin', 'dogecoin'):
            result['formatted'] = format_blockchair_tx(tx)

    return result

def cmd_validate_address(address: str) -> Dict[str, Any]:
    """Validate and identify address chain"""
    info = AddressValidator.validate(address)
    return {
        'valid': info.validated,
        'chain': info.chain,
        'normalized': info.address if info.validated else address,
        'error': info.error
    }

def cmd_gas_price(chain: str = 'ethereum') -> Dict[str, Any]:
    """Get current gas price"""
    client = CryptoAPIClient()
    result = client.get_gas_price(chain)
    if 'error' not in result:
        result['formatted'] = format_gas_price(result)
    return result

def cmd_token_balance(address: str, token_contract: str, chain: str = 'ethereum') -> Dict[str, Any]:
    """Get ERC-20 token balance"""
    client = CryptoAPIClient()
    result = client.get_token_balance(address, token_contract, chain)
    if 'error' not in result:
        result['formatted'] = format_token_balance([result])
    return result

def cmd_spl_tokens(owner: str) -> Dict[str, Any]:
    """Get SPL token accounts for Solana wallet"""
    client = CryptoAPIClient()
    result = client.get_spl_tokens(owner)
    if 'tokens' in result:
        # Add formatted output
        lines = [f"Owner: {owner}", f"Token count: {len(result['tokens'])}"]
        for token in result['tokens'][:10]:  # limit display
            lines.append(f"  {token.get('mint', '???')}: {token.get('amount', 0)}")
        result['formatted'] = '\n'.join(lines)
    return result

def cmd_wallet_tokens(address: str, chain: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get all ERC-20 token balances for a wallet"""
    client = CryptoAPIClient()
    chain = chain or client.detect_chain(address)
    result = client.get_wallet_tokens(address, chain, limit)
    if 'error' not in result:
        result['formatted'] = format_token_balance(result.get('tokens', []))
    return result

def cmd_chain_info() -> Dict[str, Any]:
    """Return supported chains and their details"""
    return {
        'supported_chains': [
            {
                'id': 'ethereum',
                'name': 'Ethereum',
                'currency': 'ETH',
                'address_format': '0x... (42 chars)',
                'explorer': 'etherscan.io',
                'rate_limit': '5 calls/sec (free tier)'
            },
            {
                'id': 'sepolia',
                'name': 'Sepolia',
                'currency': 'ETH (testnet)',
                'address_format': '0x... (42 chars)',
                'explorer': 'sepolia.etherscan.io',
                'rate_limit': '5 calls/sec (free tier)'
            },
            {
                'id': 'bitcoin',
                'name': 'Bitcoin',
                'currency': 'BTC',
                'address_format': '1..., 3..., bc1...',
                'explorer': 'blockchair.com',
                'rate_limit': '100/min (free tier)'
            },
            {
                'id': 'solana',
                'name': 'Solana',
                'currency': 'SOL',
                'address_format': 'Base58 (32-44 chars)',
                'explorer': 'solscan.io',
                'rate_limit': 'Depends on RPC endpoint'
            }
        ],
        'api_providers': [
            'Etherscan API',
            'Blockchair API',
            'Solana Public RPC'
        ],
        'note': 'No API keys required for basic usage. Limited by free tier rate limits.'
    }

def print_output(data: Dict[str, Any], format_json: bool = False):
    """Print results to stdout"""
    if format_json:
        print(json.dumps(data, indent=2))
    else:
        if 'formatted' in data:
            print(data['formatted'])
        elif 'formatted_transactions' in data:
            for line in data['formatted_transactions']:
                print(line)
        else:
            print(json.dumps(data, indent=2))

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Crypto Analytics Skill - Blockchain analysis tool")
        print("\nCommands:")
        print("  balance <address> [chain]                 Get wallet balance")
        print("  transactions <address> [chain] [limit=20] Get native transaction history")
        print("  tokentx <address> [token_contract] [chain] [limit=20] Get ERC-20 token transfer history")
        print("  tx <txhash> <chain>                       Get transaction details")
        print("  validate <address>                        Validate address format")
        print("  chains                                    List supported chains")
        print("  gas [chain=ethereum]                      Get current gas price")
        print("  token <address> <token_contract> [chain]  Get ERC-20 token balance")
        print("  tokens <address> [chain] [limit=20]       Get all ERC-20 token balances")
        print("  spl-tokens <owner>                        Get SPL token accounts (Solana)")
        print("\nExamples:")
        print("  crypto-analytics balance 0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45 ethereum")
        print("  crypto-analytics gas ethereum")
        print("  crypto-analytics token 0x... 0xA0b86991c6218b36c1d19D4a2e9bB0e3606EB48 ethereum")
        print("  crypto-analytics tokentx 0x... 0x4fec827b696e2c25a3f803e6df73b5d48ee07814 sepolia")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    try:
        if cmd == 'balance':
            addr = sys.argv[2]
            chain = sys.argv[3] if len(sys.argv) > 3 else None
            result = cmd_wallet_balance(addr, chain)
            print_output(result)

        elif cmd == 'transactions':
            addr = sys.argv[2]
            chain = sys.argv[3] if len(sys.argv) > 3 else None
            limit = int(sys.argv[4]) if len(sys.argv) > 4 else 20
            result = cmd_wallet_transactions(addr, chain, limit)
            print_output(result)

        elif cmd == 'tx':
            txhash = sys.argv[2]
            chain = sys.argv[3]
            if not chain:
                raise ValueError("Chain required for transaction lookup")
            result = cmd_transaction_details(txhash, chain)
            print_output(result)

        elif cmd == 'tokentx':
            # Usage: tokentx <address> [token_contract] [chain] [limit=20]
            if len(sys.argv) < 3:
                raise ValueError("tokentx requires at least address")
            addr = sys.argv[2]
            token_contract = sys.argv[3] if len(sys.argv) > 3 else None
            chain = sys.argv[4] if len(sys.argv) > 4 else None
            limit = int(sys.argv[5]) if len(sys.argv) > 5 else 20
            result = cmd_token_transfers(addr, token_contract, chain, limit)
            print_output(result)

        elif cmd == 'validate':
            addr = sys.argv[2]
            result = cmd_validate_address(addr)
            print_output(result, format_json=True)

        elif cmd == 'chains':
            result = cmd_chain_info()
            print_output(result, format_json=True)

        elif cmd == 'gas':
            chain = sys.argv[2] if len(sys.argv) > 2 else 'ethereum'
            result = cmd_gas_price(chain)
            print_output(result)

        elif cmd == 'token':
            if len(sys.argv) < 4:
                raise ValueError("token requires address and token_contract")
            addr = sys.argv[2]
            token_contract = sys.argv[3]
            chain = sys.argv[4] if len(sys.argv) > 4 else 'ethereum'
            result = cmd_token_balance(addr, token_contract, chain)
            print_output(result)

        elif cmd == 'tokens':
            addr = sys.argv[2]
            chain = sys.argv[3] if len(sys.argv) > 3 else None
            limit = int(sys.argv[4]) if len(sys.argv) > 4 else 20
            result = cmd_wallet_tokens(addr, chain, limit)
            print_output(result)

        elif cmd == 'spl-tokens':
            owner = sys.argv[2]
            result = cmd_spl_tokens(owner)
            print_output(result)

        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
