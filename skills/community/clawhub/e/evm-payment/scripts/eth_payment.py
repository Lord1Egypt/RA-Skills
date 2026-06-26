#!/usr/bin/env python3
"""
EIP-681 Payment Link Generator

Generate EIP-681 compliant payment links and QR codes for any EVM chain.
Zero configuration required.

Usage:
    eth-payment create --to 0x... --amount 10 --token USDC --network base
    eth-payment create --to 0x... --amount 0.1 --qr payment.png
    eth-payment chains
    eth-payment tokens --network base
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# ============================================================================
# Configuration Loading
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
CHAINS_CONFIG = CONFIG_DIR / "chains.json"


def load_chains() -> Dict[str, Any]:
    """Load chain configuration from JSON file."""
    if not CHAINS_CONFIG.exists():
        raise FileNotFoundError(f"Chain config not found: {CHAINS_CONFIG}")
    
    with open(CHAINS_CONFIG, "r") as f:
        return json.load(f)["chains"]


# ============================================================================
# EIP-681 Link Generation
# ============================================================================

def generate_payment_link(
    to: str,
    amount: float,
    token: str,
    network: str = "base"
) -> Dict[str, Any]:
    """
    Generate EIP-681 compliant payment link.
    
    Args:
        to: Recipient address (0x...)
        amount: Amount in human-readable units (e.g., 10.5)
        token: Token symbol (ETH, USDC, USDT, etc.)
        network: Network name (base, ethereum, arbitrum, etc.)
    
    Returns:
        Dict with payment details and links
    """
    chains = load_chains()
    
    # Validate network
    if network not in chains:
        return {
            "success": False,
            "error": f"Unsupported network: {network}. Supported: {list(chains.keys())}"
        }
    
    chain_config = chains[network]
    chain_id = chain_config["chain_id"]
    tokens = chain_config["tokens"]
    token = token.upper()
    
    # Validate token
    if token not in tokens:
        return {
            "success": False,
            "error": f"Unsupported token: {token} on {network}. Supported: {list(tokens.keys())}"
        }
    
    # Validate recipient address
    if not to.startswith("0x") or len(to) != 42:
        return {
            "success": False,
            "error": f"Invalid address format: {to}. Expected 0x followed by 40 hex characters."
        }
    
    token_config = tokens[token]
    token_address = token_config["address"]
    decimals = token_config["decimals"]
    is_native = token_config.get("is_native", False)
    
    # Convert amount to smallest unit (wei/smallest token unit)
    amount_raw = int(amount * (10 ** decimals))
    
    # Generate EIP-681 link
    if is_native:
        # Native token transfer (ETH, MATIC, etc.)
        eip681_link = f"ethereum:{to}@{chain_id}?value={amount_raw}"
        calldata = None
    else:
        # ERC-20 transfer
        # Transfer function: 0xa9059cbb(to, amount)
        to_padded = to[2:].lower().zfill(64)
        amount_hex = hex(amount_raw)[2:].zfill(64)
        calldata = f"0xa9059cbb{to_padded}{amount_hex}"
        
        # EIP-681 format for ERC-20
        eip681_link = f"ethereum:{token_address}@{chain_id}/transfer?address={to}&uint256={amount_raw}"
    
    # MetaMask deep link
    if is_native:
        metamask_link = f"https://metamask.app.link/send/{to}@{chain_id}?value={amount_raw}"
    else:
        metamask_link = f"https://metamask.app.link/send/{token_address}@{chain_id}/transfer?address={to}&uint256={amount_raw}"
    
    return {
        "success": True,
        "network": network,
        "chain_name": chain_config["name"],
        "chain_id": chain_id,
        "token": token,
        "token_address": token_address,
        "recipient": to,
        "amount": str(amount),
        "amount_raw": str(amount_raw),
        "decimals": decimals,
        "is_native": is_native,
        "links": {
            "eip681": eip681_link,
            "metamask": metamask_link
        },
        "transaction": {
            "to": to if is_native else token_address,
            "value": f"0x{hex(amount_raw)[2:]}" if is_native else "0x0",
            "data": calldata if calldata else "0x",
            "chain_id": chain_id
        }
    }


def generate_qr_code(link: str, output_path: str) -> Dict[str, Any]:
    """
    Generate QR code for payment link using Python qrcode library.
    
    Args:
        link: URL to encode
        output_path: Path to save PNG file
    
    Returns:
        Dict with success status and path
    """
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        import qrcode
        from PIL import Image
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        
        if os.path.exists(output_path):
            return {
                "success": True,
                "qr_path": output_path,
                "method": "python-qrcode"
            }
        else:
            return {
                "success": False,
                "error": "QR file was not created"
            }
    except ImportError:
        return {
            "success": False,
            "error": "qrcode or PIL not installed. Run: pip install qrcode pillow"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# Output Formatting
# ============================================================================

def format_human_output(result: Dict[str, Any]) -> str:
    """Format result for human-readable display."""
    if not result.get("success"):
        return f"❌ Error: {result.get('error', 'Unknown error')}"
    
    lines = [
        "=" * 60,
        "EIP-681 Payment Link",
        "=" * 60,
        "",
        f"Network:  {result['chain_name']} (Chain ID: {result['chain_id']})",
        f"Token:    {result['token']}",
        f"Recipient: {result['recipient']}",
        f"Amount:   {result['amount']} {result['token']}",
        "",
        "-" * 60,
        "Mobile (MetaMask)",
        "-" * 60,
        f"Tap to pay: {result['links']['metamask']}",
        "",
        "-" * 60,
        "Desktop",
        "-" * 60,
        "Scan QR code or use transaction details:",
        "",
        f"  To:    {result['transaction']['to']}",
        f"  Value: {result['transaction']['value']}",
    ]
    
    if result['transaction']['data'] != "0x":
        lines.append(f"  Data:  {result['transaction']['data'][:30]}...")
    else:
        lines.append("  Data:  (none - native transfer)")
    
    lines.extend([
        "",
        "-" * 60,
        "Raw EIP-681 Link",
        "-" * 60,
        result['links']['eip681'],
    ])
    
    if result.get("qr_path"):
        lines.extend([
            "",
            "-" * 60,
            "QR Code",
            "-" * 60,
            f"Generated at: {result['qr_path']}",
        ])
    
    return "\n".join(lines)


# ============================================================================
# CLI Commands
# ============================================================================

def cmd_create(args):
    """Handle 'create' command."""
    result = generate_payment_link(
        to=args.to,
        amount=args.amount,
        token=args.token,
        network=args.network
    )
    
    # Generate QR if requested
    if args.qr and result.get("success"):
        qr_result = generate_qr_code(result["links"]["metamask"], args.qr)
        result["qr"] = qr_result
        if qr_result["success"]:
            result["qr_path"] = qr_result["qr_path"]
    
    # Output
    if args.json:
        # Clean output for JSON
        output = {k: v for k, v in result.items() if not k.startswith("_")}
        print(json.dumps(output, indent=2))
    else:
        print(format_human_output(result))
    
    return 0 if result.get("success") else 1


def cmd_chains(args):
    """Handle 'chains' command - list supported networks."""
    chains = load_chains()
    
    if args.json:
        output = {
            name: {
                "name": config["name"],
                "chain_id": config["chain_id"],
                "native_token": config["native_token"],
                "token_count": len(config["tokens"])
            }
            for name, config in chains.items()
        }
        print(json.dumps(output, indent=2))
    else:
        print("Supported Networks:")
        print("-" * 50)
        for name, config in chains.items():
            print(f"  {name:12} - {config['name']} (ID: {config['chain_id']})")
            print(f"               Native: {config['native_token']}, Tokens: {len(config['tokens'])}")
    
    return 0


def cmd_tokens(args):
    """Handle 'tokens' command - list tokens for a network."""
    chains = load_chains()
    
    if args.network not in chains:
        print(f"❌ Error: Unknown network '{args.network}'")
        print(f"   Supported: {list(chains.keys())}")
        return 1
    
    chain_config = chains[args.network]
    tokens = chain_config["tokens"]
    
    if args.json:
        print(json.dumps(tokens, indent=2))
    else:
        print(f"Tokens on {chain_config['name']}:")
        print("-" * 50)
        for symbol, config in tokens.items():
            native_marker = " (native)" if config.get("is_native") else ""
            print(f"  {symbol:8} - {config['address']}{native_marker}")
    
    return 0


def cmd_validate(args):
    """Handle 'validate' command - validate an address."""
    address = args.address
    
    if not address.startswith("0x"):
        print(f"❌ Invalid: Address must start with '0x'")
        return 1
    
    if len(address) != 42:
        print(f"❌ Invalid: Address must be 42 characters (0x + 40 hex)")
        return 1
    
    try:
        int(address[2:], 16)
        print(f"✅ Valid Ethereum address: {address}")
        return 0
    except ValueError:
        print(f"❌ Invalid: Address contains non-hex characters")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="EIP-681 Payment Link Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # create command
    create_parser = subparsers.add_parser("create", help="Generate payment link")
    create_parser.add_argument("--to", required=True, help="Recipient address (0x...)")
    create_parser.add_argument("--amount", type=float, required=True, help="Amount to request")
    create_parser.add_argument("--token", default="ETH", help="Token symbol (default: ETH)")
    create_parser.add_argument("--network", default="base", help="Network name (default: base)")
    create_parser.add_argument("--qr", help="Generate QR code and save to path")
    create_parser.add_argument("--json", action="store_true", help="Output as JSON")
    create_parser.set_defaults(func=cmd_create)
    
    # chains command
    chains_parser = subparsers.add_parser("chains", help="List supported networks")
    chains_parser.add_argument("--json", action="store_true", help="Output as JSON")
    chains_parser.set_defaults(func=cmd_chains)
    
    # tokens command
    tokens_parser = subparsers.add_parser("tokens", help="List tokens for a network")
    tokens_parser.add_argument("--network", required=True, help="Network name")
    tokens_parser.add_argument("--json", action="store_true", help="Output as JSON")
    tokens_parser.set_defaults(func=cmd_tokens)
    
    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate an Ethereum address")
    validate_parser.add_argument("address", help="Address to validate")
    validate_parser.set_defaults(func=cmd_validate)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())