#!/usr/bin/env python3
"""
Flap.sh Portal PoC — Validate token launch on BSC Testnet.

Usage:
    # Generate a test wallet:
    uv run poc/flap_poc.py --gen-wallet

    # Launch a test token (after funding wallet with testnet BNB):
    export TEST_WALLET_KEY=<private_key>
    uv run poc/flap_poc.py
"""
import argparse
import json
import os
import sys
import time

import requests
from eth_account import Account
from web3 import Web3

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

# BSC Testnet
TESTNET_RPC = "https://bsc-testnet-dataseed.bnbchain.org"
TESTNET_CHAIN_ID = 97

# BSC Mainnet (for reference)
MAINNET_RPC = "https://bsc-dataseed.binance.org/"
MAINNET_CHAIN_ID = 56

# Portal contract addresses
PORTAL_TESTNET = "0x5bEacaF7ABCbB3aB280e80D007FD31fcE26510e9"
PORTAL_MAINNET = "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0"

# Token implementation addresses (testnet)
STANDARD_TOKEN_IMPL_TESTNET = "0x87D5f292ba33011997641C7a7Bd2b17799aaA814"
TAX_TOKEN_V1_IMPL_TESTNET = "0x87d8D03d0c3E064ACdb48E42fecbE8a8538dE6Fc"
TAX_TOKEN_V2_IMPL_TESTNET = "0x2486e3ff5502bac48D2D86457e7c24B2bB0dDDb5"

# Token implementation addresses (mainnet)
STANDARD_TOKEN_IMPL_MAINNET = "0x8b4329947e34b6d56d71a3385cac122bade7d78d"
TAX_TOKEN_V1_IMPL_MAINNET = "0x29e6383F0ce68507b5A72a53c2B118a118332aA8"
TAX_TOKEN_V2_IMPL_MAINNET = "0xae562c6A05b798499507c6276C6Ed796027807BA"

# DISTRICT9 Treasury
DISTRICT9_TREASURY = "0x9BAe1a391f979e92200027684a73591FD83C9EFD"

# Flap IPFS upload endpoint
FLAP_UPLOAD_API = "https://funcs.flap.sh/api/upload"

# Vanity suffix: tax tokens must end with 7777
TAX_TOKEN_SUFFIX = "7777"

# Minimal Portal ABI for newTokenV2 (active function as of 2026-03)
PORTAL_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"name": "name", "type": "string"},
                    {"name": "symbol", "type": "string"},
                    {"name": "meta", "type": "string"},
                    {"name": "dexThresh", "type": "uint8"},
                    {"name": "salt", "type": "bytes32"},
                    {"name": "taxRate", "type": "uint16"},
                    {"name": "migratorType", "type": "uint8"},
                    {"name": "quoteToken", "type": "address"},
                    {"name": "quoteAmt", "type": "uint256"},
                    {"name": "beneficiary", "type": "address"},
                    {"name": "permitData", "type": "bytes"},
                ],
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "newTokenV2",
        "outputs": [{"name": "token", "type": "address"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "ts", "type": "uint256"},
            {"indexed": True, "name": "creator", "type": "address"},
            {"indexed": True, "name": "nonce", "type": "uint256"},
            {"indexed": False, "name": "token", "type": "address"},
            {"indexed": False, "name": "name", "type": "string"},
            {"indexed": False, "name": "symbol", "type": "string"},
            {"indexed": False, "name": "meta", "type": "string"},
        ],
        "name": "TokenCreated",
        "type": "event",
    },
]


# ─────────────────────────────────────────────
# Wallet generation
# ─────────────────────────────────────────────


def gen_wallet():
    """Generate a new Ethereum wallet and print details."""
    acct = Account.create()
    print("=" * 60)
    print("New Test Wallet Generated")
    print("=" * 60)
    print(f"Address:     {acct.address}")
    print(f"Private Key: {acct.key.hex()}")
    print()
    print("Next steps:")
    print("1. Go to https://www.bnbchain.org/en/testnet-faucet")
    print(f"2. Paste address: {acct.address}")
    print("3. Request testnet BNB")
    print(f"4. Run: export TEST_WALLET_KEY={acct.key.hex()}")
    print("5. Run: uv run poc/flap_poc.py")
    print("=" * 60)


# ─────────────────────────────────────────────
# CREATE2 salt finder
# ─────────────────────────────────────────────


def predict_token_address(portal: str, salt: bytes, token_impl: str) -> str:
    """
    Predict the CREATE2 token address.

    The bytecode is the minimal proxy (EIP-1167) pointing to the token implementation:
        0x3d602d80600a3d3981f3  (10 bytes — constructor)
        363d3d373d3d3d363d73    (10 bytes — runtime prefix)
        <20-byte impl address>
        5af43d82803e903d91602b57fd5bf3  (15 bytes — runtime suffix)
    """
    impl_hex = token_impl[2:].lower()  # strip 0x
    bytecode_hex = (
        "3d602d80600a3d3981f3"
        "363d3d373d3d3d363d73"
        + impl_hex
        + "5af43d82803e903d91602b57fd5bf3"
    )
    bytecode = bytes.fromhex(bytecode_hex)
    bytecode_hash = Web3.keccak(bytecode)

    portal_bytes = bytes.fromhex(portal[2:].lower())

    # CREATE2: keccak256(0xff ++ deployer ++ salt ++ keccak256(bytecode))
    data = b"\xff" + portal_bytes + salt + bytecode_hash
    addr_hash = Web3.keccak(data)
    return Web3.to_checksum_address(addr_hash[-20:].hex())


def find_salt(portal: str, token_impl: str, suffix: str = TAX_TOKEN_SUFFIX) -> tuple[bytes, str, int]:
    """
    Brute-force search for a CREATE2 salt that produces a vanity address.

    Returns (salt_bytes, predicted_address, iterations).
    """
    print(f"Searching for salt (address suffix: {suffix})...")

    # Start with a random seed
    seed = Account.create().key
    salt = Web3.keccak(seed)
    iterations = 0

    start = time.time()
    while True:
        addr = predict_token_address(portal, salt, token_impl)
        if addr.lower().endswith(suffix.lower()):
            elapsed = time.time() - start
            print(f"Found salt in {iterations} iterations ({elapsed:.1f}s)")
            print(f"  Salt: 0x{salt.hex()}")
            print(f"  Predicted address: {addr}")
            return salt, addr, iterations

        salt = Web3.keccak(salt)
        iterations += 1

        if iterations % 10000 == 0:
            elapsed = time.time() - start
            rate = iterations / elapsed if elapsed > 0 else 0
            print(f"  ... {iterations} iterations ({rate:.0f}/s)")


# ─────────────────────────────────────────────
# IPFS metadata upload
# ─────────────────────────────────────────────


def upload_metadata(name: str, symbol: str, description: str, image_path: str | None = None) -> str:
    """
    Upload token metadata to Flap's IPFS via GraphQL mutation.

    Returns the IPFS CID.
    """
    mutation = """
    mutation Create($file: Upload!, $meta: MetadataInput!) {
      create(file: $file, meta: $meta)
    }
    """

    meta = {
        "website": f"https://district9.xyz",
        "twitter": None,
        "telegram": None,
        "description": description,
        "creator": "0x0000000000000000000000000000000000000000",
    }

    operations = json.dumps({
        "query": mutation,
        "variables": {
            "file": None,
            "meta": meta,
        },
    })

    mapping = json.dumps({"0": ["variables.file"]})

    # Use a placeholder image if none provided
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image_data = f.read()
        filename = os.path.basename(image_path)
        content_type = "image/png"
    else:
        # Create a minimal 1x1 PNG placeholder
        import base64
        # Minimal valid 1x1 red PNG
        png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
            "2mP8/58BAwAI/AL+hc2rNAAAAABJRU5ErkJggg=="
        )
        image_data = base64.b64decode(png_b64)
        filename = "logo.png"
        content_type = "image/png"

    files = {
        "operations": (None, operations, "application/json"),
        "map": (None, mapping, "application/json"),
        "0": (filename, image_data, content_type),
    }

    print(f"Uploading metadata to Flap IPFS...")
    resp = requests.post(FLAP_UPLOAD_API, files=files, timeout=30)

    if resp.status_code != 200:
        print(f"Upload failed: {resp.status_code} {resp.text}")
        raise RuntimeError(f"IPFS upload failed: {resp.status_code}")

    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")

    cid = data["data"]["create"]
    print(f"Uploaded! CID: {cid}")
    return cid


# ─────────────────────────────────────────────
# Token launch
# ─────────────────────────────────────────────


def launch_token(
    w3: Web3,
    account: Account,
    portal_address: str,
    token_impl: str,
    name: str,
    symbol: str,
    description: str,
    initial_buy_bnb: float = 0.001,
) -> dict:
    """
    Launch a token through Flap's Portal.newTokenV2().

    Returns dict with contract_address, tx_hash, etc.
    """
    portal = w3.eth.contract(
        address=Web3.to_checksum_address(portal_address),
        abi=PORTAL_ABI,
    )

    # Step 1: Upload metadata
    cid = upload_metadata(name, symbol, description)

    # Step 2: Find CREATE2 salt
    salt, predicted_addr, iters = find_salt(portal_address, token_impl)

    # Step 3: Build newTokenV2 params
    quote_amt = w3.to_wei(initial_buy_bnb, "ether")

    params = (
        name,                                                          # name
        symbol,                                                        # symbol
        cid,                                                           # meta (IPFS CID)
        1,                                                             # dexThresh
        salt,                                                          # salt
        100,                                                           # taxRate (1% = 100 bps)
        1,                                                             # migratorType
        "0x0000000000000000000000000000000000000000",                   # quoteToken (native BNB)
        quote_amt,                                                     # quoteAmt
        Web3.to_checksum_address(DISTRICT9_TREASURY),                  # beneficiary
        b"",                                                           # permitData
    )

    # Step 4: Build and send transaction
    wallet_address = account.address
    nonce = w3.eth.get_transaction_count(wallet_address)
    balance = w3.eth.get_balance(wallet_address)

    print(f"\nWallet: {wallet_address}")
    print(f"Balance: {w3.from_wei(balance, 'ether')} BNB")
    print(f"Nonce: {nonce}")

    if balance < quote_amt:
        raise ValueError(
            f"Insufficient balance: have {w3.from_wei(balance, 'ether')} BNB, "
            f"need at least {initial_buy_bnb} BNB + gas"
        )

    # Estimate gas
    print("Estimating gas...")
    try:
        gas_estimate = portal.functions.newTokenV2(params).estimate_gas({
            "from": wallet_address,
            "value": quote_amt,
        })
        gas_limit = int(gas_estimate * 1.3)  # 30% buffer
        print(f"Gas estimate: {gas_estimate}, using limit: {gas_limit}")
    except Exception as e:
        print(f"Gas estimation failed: {e}")
        gas_limit = 3_000_000  # fallback
        print(f"Using fallback gas limit: {gas_limit}")

    gas_price = w3.eth.gas_price

    tx = portal.functions.newTokenV2(params).build_transaction({
        "from": wallet_address,
        "value": quote_amt,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": w3.eth.chain_id,
    })

    print(f"\nSigning and sending transaction...")
    signed = w3.eth.account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"TX hash: {tx_hash.hex()}")

    # Step 5: Wait for receipt
    print("Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if receipt["status"] != 1:
        raise RuntimeError(f"Transaction failed! Status: {receipt['status']}")

    print(f"Transaction confirmed! Block: {receipt['blockNumber']}")

    # Step 6: Parse TokenCreated event
    token_address = None
    try:
        logs = portal.events.TokenCreated().process_receipt(receipt)
        if logs:
            token_address = logs[0]["args"]["token"]
            print(f"\nTokenCreated event found!")
            print(f"  Token: {token_address}")
            print(f"  Name: {logs[0]['args']['name']}")
            print(f"  Symbol: {logs[0]['args']['symbol']}")
    except Exception as e:
        print(f"Could not parse TokenCreated event: {e}")

    if not token_address:
        # Fallback: use predicted address
        token_address = predicted_addr
        print(f"Using predicted address: {token_address}")

    chain_name = "testnet." if w3.eth.chain_id == 97 else ""
    explorer_base = f"https://{chain_name}bscscan.com"

    return {
        "contract_address": token_address,
        "tx_hash": tx_hash.hex(),
        "block_number": receipt["blockNumber"],
        "gas_used": receipt["gasUsed"],
        "predicted_address": predicted_addr,
        "salt": f"0x{salt.hex()}",
        "ipfs_cid": cid,
        "explorer_tx": f"{explorer_base}/tx/{tx_hash.hex()}",
        "explorer_token": f"{explorer_base}/token/{token_address}",
        "flap_url": f"https://flap.sh/bnb/{token_address}",
    }


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Flap.sh Portal PoC")
    parser.add_argument("--gen-wallet", action="store_true", help="Generate a new test wallet")
    parser.add_argument("--mainnet", action="store_true", help="Use mainnet (default: testnet)")
    parser.add_argument("--name", default="D9 Test Token", help="Token name")
    parser.add_argument("--symbol", default="D9TST", help="Token symbol")
    parser.add_argument("--buy", type=float, default=0.001, help="Initial buy amount in BNB")
    args = parser.parse_args()

    if args.gen_wallet:
        gen_wallet()
        return

    # Load private key
    private_key = os.environ.get("TEST_WALLET_KEY")
    if not private_key:
        print("ERROR: Set TEST_WALLET_KEY environment variable")
        print("  Run: uv run poc/flap_poc.py --gen-wallet")
        sys.exit(1)

    # Setup
    if args.mainnet:
        rpc_url = MAINNET_RPC
        portal = PORTAL_MAINNET
        # Choose impl: mktBps=10000 → V1, <10000 → V2
        token_impl = TAX_TOKEN_V1_IMPL_MAINNET
    else:
        rpc_url = TESTNET_RPC
        portal = PORTAL_TESTNET
        token_impl = TAX_TOKEN_V1_IMPL_TESTNET

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print(f"ERROR: Cannot connect to {rpc_url}")
        sys.exit(1)

    account = Account.from_key(private_key)
    chain = "BSC Mainnet" if args.mainnet else "BSC Testnet"
    print(f"Connected to {chain} (chain_id={w3.eth.chain_id})")

    description = (
        f"{args.name} - A test token launched via DISTRICT9 OpenClaw. "
        f"[D9:test-agent:v1]"
    )

    try:
        result = launch_token(
            w3=w3,
            account=account,
            portal_address=portal,
            token_impl=token_impl,
            name=args.name,
            symbol=args.symbol,
            description=description,
            initial_buy_bnb=args.buy,
        )

        print("\n" + "=" * 60)
        print("TOKEN LAUNCHED SUCCESSFULLY!")
        print("=" * 60)
        for k, v in result.items():
            print(f"  {k}: {v}")
        print("=" * 60)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
