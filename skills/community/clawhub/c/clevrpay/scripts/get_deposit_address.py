#!/usr/bin/env python3
"""
ClevrPay Deposit Address Helper

This script automates the flow for obtaining deposit addresses in Cleanverse.
"""

import argparse
import json
import urllib.request
import urllib.error
import sys

# Base URLs
SANDBOX_URL = "https://uatapi.cleanverse.com/api/skills"
PRODUCTION_URL = "https://api.cleanverse.com/api/skills"


def make_request(url, data=None):
    """Make HTTP POST request to API."""
    headers = {"Content-Type": "application/json"}
    if data:
        data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"code": str(e.code), "message": f"HTTP Error: {e.reason}"}
    except urllib.error.URLError as e:
        return {"code": "0002", "message": f"Network Error: {e.reason}"}


def get_magiclink(base_url):
    """Get A-Pass registration magic link."""
    result = make_request(f"{base_url}/get_magiclink")
    if result.get("code") == "0000":
        return result.get("data", {}).get("register_url")
    return None


def query_apass(base_url, chain, address):
    """Query A-Pass status for an address."""
    data = {
        "chain": chain.lower(),
        "address": address.lower()
    }
    result = make_request(f"{base_url}/query_apass", data)
    return result


def query_deposit_address(base_url, chain, address, symbol=None):
    """Query deposit address for specified chain and token."""
    data = {
        "chain": chain.lower(),
        "address": address.lower()
    }
    if symbol:
        data["symbol"] = symbol.lower()

    result = make_request(f"{base_url}/query_deposit_address", data)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="ClevrPay Deposit Address Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Note: Base and Monad networks do not support USDT. Only USDC is available on these chains.
        """
    )
    parser.add_argument("--wallet", required=True, help="EVM wallet address")
    parser.add_argument("--chain", required=True,
                        choices=["ethereum", "base", "polygon", "bsc", "arbitrum", "monad"],
                        help="Chain name")
    parser.add_argument("--token", choices=["usdc", "usdt"], help="Token symbol")
    parser.add_argument("--env", choices=["sandbox", "production"], default="sandbox",
                        help="Environment (default: sandbox)")
    parser.add_argument("--skip-auth", action="store_true",
                        help="Skip A-Pass authentication step")
    parser.add_argument("--open-browser", action="store_true",
                        help="Open the registration link in a browser after fetching it")

    args = parser.parse_args()

    # Validate: Base and Monad do not support USDT
    if args.chain in ["base", "monad"] and args.token == "usdt":
        print(f"Error: {args.chain.capitalize()} network does not support USDT.")
        print("Please choose USDC for this chain or select a different chain.")
        sys.exit(1)

    base_url = PRODUCTION_URL if args.env == "production" else SANDBOX_URL

    print(f"Environment: {args.env}")
    print(f"Wallet: {args.wallet}")
    print(f"Chain: {args.chain}")
    print(f"Token: {args.token or 'Both USDC and USDT'}")
    print("-" * 50)
    print("\nIMPORTANT:")
    print("- Make sure your wallet has native gas tokens (ETH/BNB) for transaction fees")
    print("- Make sure your wallet has the tokens (USDC/USDT) you want to deposit")
    print("- Your wallet must have an active A-Pass for deposits to work")
    print("-" * 50)

    # Step 1: Get Magic Link
    if not args.skip_auth:
        print("\n[Step 1] Getting A-Pass registration link...")
        magiclink = get_magiclink(base_url)

        if magiclink:
            print(f"Registration URL: {magiclink}")
            if args.open_browser:
                import webbrowser
                print("\nOpening browser for authentication...")
                webbrowser.open(magiclink)
            else:
                print("\nBrowser auto-open is disabled by default for safety. Open the URL manually if needed.")
            print("\nPlease complete authentication in your browser.")
            input("Press Enter after you've completed authentication...")
        else:
            print("Failed to get magic link. Please try again.")
            sys.exit(1)

    # Step 2: Query A-Pass Status
    print("\n[Step 2] Querying A-Pass status...")
    apass_result = query_apass(base_url, args.chain, args.wallet)

    if apass_result.get("code") == "0000":
        data = apass_result.get("data", {})
        print(f"A-Pass Status: Active")
        print(f"Tier: {data.get('tier')}")
        print(f"Expiration: {data.get('expirationTime')}")
    else:
        print(f"A-Pass query failed: {apass_result.get('message')}")
        print("Please ensure you've completed authentication.")
        sys.exit(1)

    # Step 3: Query Deposit Address
    print("\n[Step 3] Querying deposit address...")
    deposit_result = query_deposit_address(base_url, args.chain, args.wallet, args.token)

    if deposit_result.get("code") == "0000":
        data = deposit_result.get("data", {})
        print("\n=== Deposit Addresses ===")
        if args.token == "usdc" or not args.token:
            print(f"USDC: {data.get('depositUSDCWallet')}")
        if args.token == "usdt" or not args.token:
            print(f"USDT: {data.get('depositUSDTWallet')}")
        print(f"\nChain: {data.get('chain')}")
        print(f"A-Pass Address: {data.get('aPassAddress')}")
    else:
        print(f"Failed to get deposit address: {deposit_result.get('message')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
