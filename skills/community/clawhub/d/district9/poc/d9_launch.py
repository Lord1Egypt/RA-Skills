#!/usr/bin/env python3
"""
District9 Mode B Token Launch — D9Portal (0x9999 suffix)

Same flow as Mode A but uses D9Portal instead of Flap VaultPortal.
Generates PFP logo, uploads metadata to IPFS, mines 9999 salt, deploys token.
"""

import base64
import json
import os
import sys
import tempfile
import time

import requests
from eth_account import Account
from web3 import Web3

# ============ Configuration ============

PRIVATE_KEY = "0xa1007620c8d030e613759de8ac18865799ab798e2447dd28893cbdc015b79cd1"
OPENROUTER_API_KEY = "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"

# BSC Mainnet
RPC = "https://bsc-dataseed.binance.org/"
CHAIN_ID = 56

# Contract addresses
D9_PORTAL = "0x65f1DC16D3821cD78E9517372b469a544b58DC76"
TOKEN_IMPL = "0x29e6383F0ce68507b5A72a53c2B118a118332aA8"
DISTRICT9_TREASURY = "0x9BAe1a391f979e92200027684a73591FD83C9EFD"

# Flap IPFS upload endpoint (reuse for metadata hosting)
FLAP_UPLOAD_API = "https://funcs.flap.sh/api/upload"

# D9Portal ABI (only the functions we need)
D9_PORTAL_ABI = [
    {
        "inputs": [
            {"name": "name", "type": "string"},
            {"name": "symbol", "type": "string"},
            {"name": "meta", "type": "string"},
            {"name": "salt", "type": "bytes32"},
            {
                "components": [
                    {"name": "recipient", "type": "address"},
                    {"name": "bps", "type": "uint16"},
                ],
                "name": "vaultRecipients",
                "type": "tuple[]",
            },
        ],
        "name": "createToken",
        "outputs": [{"name": "token", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"name": "token", "type": "address"},
            {"name": "minTokensOut", "type": "uint256"},
        ],
        "name": "buy",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "token", "type": "address"},
            {"indexed": True, "name": "vault", "type": "address"},
            {"indexed": True, "name": "creator", "type": "address"},
        ],
        "name": "TokenCreated",
        "type": "event",
    },
]

# OpenRouter image models
IMAGE_MODELS = [
    "google/gemini-3.1-flash-image-preview",
    "google/gemini-2.5-flash-image",
    "google/gemini-3-pro-image-preview",
]


def log(msg):
    print(f"[D9] {msg}")


# ============ Step 1: Generate Logo ============

def generate_logo(token_name: str, narrative: str) -> str:
    """Generate PFP via OpenRouter image model. Returns local file path."""
    prompt = (
        f"Generate a 1:1 square token profile picture (PFP) for a meme coin called '{token_name}'. "
        f"Concept: {narrative[:200]}. "
        f"Requirements: "
        f"- Circular token logo style, centered subject "
        f"- Vivid, saturated colors with clean edges "
        f"- Bold, iconic, instantly recognizable at small sizes "
        f"- NO text, NO letters, NO words anywhere in the image "
        f"- Flat or semi-flat illustration style, suitable as a crypto token icon "
        f"- Single subject/character on a solid or gradient background"
    )

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    for model in IMAGE_MODELS:
        for attempt in range(3):
            try:
                log(f"Logo gen attempt {attempt + 1}/3 ({model})...")
                resp = requests.post(
                    url,
                    headers=headers,
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "modalities": ["image", "text"],
                    },
                    timeout=90,
                )
                resp.raise_for_status()
                data = resp.json()

                message = data.get("choices", [{}])[0].get("message", {})

                # Extract base64 image
                img_b64 = _extract_image_b64(message)
                if img_b64:
                    img_bytes = base64.b64decode(img_b64)
                    tmp = tempfile.NamedTemporaryFile(
                        suffix=".png", delete=False, prefix="d9_logo_"
                    )
                    tmp.write(img_bytes)
                    tmp.close()
                    log(f"Logo saved: {tmp.name} ({len(img_bytes)} bytes)")
                    return tmp.name

                log(f"No image in response (attempt {attempt + 1})")

            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 429:
                    log("Rate limited, waiting 5s...")
                    time.sleep(5)
                else:
                    log(f"HTTP error: {e}")
            except Exception as e:
                log(f"Attempt error: {e}")

            time.sleep(2)

        log(f"All retries failed for {model}, trying next...")

    log("WARNING: Logo generation failed, using placeholder")
    return ""


def _extract_image_b64(message: dict) -> str:
    for img in message.get("images", []):
        if isinstance(img, dict):
            url = img.get("image_url", {}).get("url", "")
            if url.startswith("data:") and ";base64," in url:
                return url.split(";base64,", 1)[1]
        elif isinstance(img, str):
            return img

    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "image_url":
                url = part.get("image_url", {}).get("url", "")
                if url.startswith("data:") and ";base64," in url:
                    return url.split(";base64,", 1)[1]

    return ""


# ============ Step 2: Upload to IPFS ============

def upload_to_ipfs(metadata: dict, image_path: str) -> str:
    """Upload metadata + image to Flap's IPFS. Returns CID."""
    mutation = """
    mutation Create($file: Upload!, $meta: MetadataInput!) {
      create(file: $file, meta: $meta)
    }
    """

    meta = {
        "website": metadata.get("website", ""),
        "twitter": None,
        "telegram": None,
        "description": metadata.get("description", ""),
        "creator": "0x0000000000000000000000000000000000000000",
    }

    operations = json.dumps(
        {"query": mutation, "variables": {"file": None, "meta": meta}}
    )
    mapping = json.dumps({"0": ["variables.file"]})

    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image_data = f.read()
        filename = os.path.basename(image_path)
    else:
        # Minimal 1x1 PNG placeholder
        png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
            "2mP8/58BAwAI/AL+hc2rNAAAAABJRU5ErkJggg=="
        )
        image_data = base64.b64decode(png_b64)
        filename = "logo.png"

    files = {
        "operations": (None, operations, "application/json"),
        "map": (None, mapping, "application/json"),
        "0": (filename, image_data, "image/png"),
    }

    log("Uploading metadata to IPFS...")
    resp = requests.post(FLAP_UPLOAD_API, files=files, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"IPFS upload failed: {resp.status_code} {resp.text}")

    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")

    cid = data["data"]["create"]
    log(f"Metadata uploaded: {cid}")
    return cid


# ============ Step 3: Mine Salt ============

def find_salt_9999(deployer: str, token_impl: str) -> tuple[bytes, str]:
    """Find CREATE2 salt for vanity address ending in 9999."""
    impl_hex = token_impl[2:].lower()

    # EIP-1167 minimal proxy bytecode
    bytecode_hex = (
        "3d602d80600a3d3981f3"
        "363d3d373d3d3d363d73"
        + impl_hex
        + "5af43d82803e903d91602b57fd5bf3"
    )
    bytecode = bytes.fromhex(bytecode_hex)
    bytecode_hash = Web3.keccak(bytecode)
    deployer_bytes = bytes.fromhex(deployer[2:].lower())

    log("Mining CREATE2 salt (9999 suffix)...")
    seed = Account.create().key
    salt = Web3.keccak(seed)
    iterations = 0
    start = time.time()

    while True:
        data = b"\xff" + deployer_bytes + salt + bytecode_hash
        addr_hash = Web3.keccak(data)
        addr = Web3.to_checksum_address(addr_hash[-20:].hex())

        if addr.lower().endswith("9999"):
            elapsed = time.time() - start
            log(f"Salt found in {iterations} iterations ({elapsed:.2f}s): {addr}")
            return salt, addr

        salt = Web3.keccak(salt)
        iterations += 1


# ============ Step 4: Deploy Token ============

def deploy_token(
    w3: Web3,
    account,
    name: str,
    symbol: str,
    cid: str,
    salt: bytes,
) -> dict:
    """Call D9Portal.createToken() on BSC mainnet."""
    portal = w3.eth.contract(
        address=Web3.to_checksum_address(D9_PORTAL),
        abi=D9_PORTAL_ABI,
    )

    # SplitVault recipients: 50% Treasury, 50% Agent
    recipients = [
        (Web3.to_checksum_address(DISTRICT9_TREASURY), 5000),
        (Web3.to_checksum_address(account.address), 5000),
    ]

    wallet = account.address
    nonce = w3.eth.get_transaction_count(wallet)

    log(f"Wallet: {wallet}")
    log(f"Balance: {w3.from_wei(w3.eth.get_balance(wallet), 'ether')} BNB")

    # Estimate gas
    try:
        gas_est = portal.functions.createToken(
            name, symbol, cid, salt, recipients
        ).estimate_gas({"from": wallet})
        gas_limit = int(gas_est * 1.3)
        log(f"Gas estimate: {gas_est} (limit: {gas_limit})")
    except Exception as e:
        log(f"Gas estimation failed ({e}), using fallback 3M")
        gas_limit = 3_000_000

    tx = portal.functions.createToken(
        name, symbol, cid, salt, recipients
    ).build_transaction(
        {
            "from": wallet,
            "value": 0,
            "gas": gas_limit,
            "gasPrice": w3.eth.gas_price,
            "nonce": nonce,
            "chainId": CHAIN_ID,
        }
    )

    log("Signing and sending createToken()...")
    signed = w3.eth.account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    log(f"TX sent: {tx_hash.hex()}")

    log("Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if receipt["status"] != 1:
        raise RuntimeError(f"Transaction reverted! TX: {tx_hash.hex()}")

    log(f"Confirmed in block {receipt['blockNumber']} (gas: {receipt['gasUsed']})")

    # Parse TokenCreated event
    token_address = None
    try:
        logs = portal.events.TokenCreated().process_receipt(receipt)
        if logs:
            token_address = logs[0]["args"]["token"]
    except Exception:
        pass

    if not token_address:
        token_address = "unknown"
        log("WARNING: Could not parse token address from logs")

    return {
        "token": token_address,
        "tx_hash": tx_hash.hex(),
        "block": receipt["blockNumber"],
        "gas": receipt["gasUsed"],
    }


# ============ Step 5: Initial Buy (optional) ============

def initial_buy(w3: Web3, account, token_address: str, bnb_amount: float):
    """Buy tokens on the bonding curve."""
    portal = w3.eth.contract(
        address=Web3.to_checksum_address(D9_PORTAL),
        abi=D9_PORTAL_ABI,
    )

    value = w3.to_wei(bnb_amount, "ether")
    wallet = account.address
    nonce = w3.eth.get_transaction_count(wallet)

    log(f"Buying with {bnb_amount} BNB...")

    try:
        gas_est = portal.functions.buy(
            Web3.to_checksum_address(token_address), 0
        ).estimate_gas({"from": wallet, "value": value})
        gas_limit = int(gas_est * 1.3)
    except Exception as e:
        log(f"Gas estimation failed ({e}), using 500K")
        gas_limit = 500_000

    tx = portal.functions.buy(
        Web3.to_checksum_address(token_address), 0
    ).build_transaction(
        {
            "from": wallet,
            "value": value,
            "gas": gas_limit,
            "gasPrice": w3.eth.gas_price,
            "nonce": nonce,
            "chainId": CHAIN_ID,
        }
    )

    signed = w3.eth.account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    log(f"Buy TX sent: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt["status"] != 1:
        raise RuntimeError(f"Buy TX reverted! {tx_hash.hex()}")

    log(f"Buy confirmed (gas: {receipt['gasUsed']})")
    return tx_hash.hex()


# ============ Main ============

def main():
    # Token definition
    token_name = "District9 Genesis"
    token_symbol = "D9GEN"
    narrative = (
        "The first token launched via District9's own launchpad. "
        "Born from AI agents, forged on-chain with a 9999 vanity address. "
        "A genesis artifact of autonomous meme creation."
    )
    initial_buy_bnb = 0.001  # Small test buy

    log("=" * 60)
    log("District9 Mode B Launch — D9Portal (0x9999)")
    log("=" * 60)

    # Connect
    w3 = Web3(Web3.HTTPProvider(RPC))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to {RPC}")
    account = Account.from_key(PRIVATE_KEY)
    log(f"Chain: BSC Mainnet (ID {CHAIN_ID})")
    log(f"Wallet: {account.address}")
    log(f"Balance: {w3.from_wei(w3.eth.get_balance(account.address), 'ether')} BNB")
    log("")

    # Step 1: Generate logo
    log("--- Step 1: Generate Logo ---")
    logo_path = generate_logo(token_name, narrative)
    log("")

    # Step 2: Upload to IPFS
    log("--- Step 2: Upload Metadata ---")
    metadata = {
        "name": token_name,
        "symbol": token_symbol,
        "description": f"{narrative} [D9:Genesis]",
    }
    cid = upload_to_ipfs(metadata, logo_path)
    log("")

    # Step 3: Mine salt
    log("--- Step 3: Mine Salt (9999) ---")
    salt, predicted = find_salt_9999(D9_PORTAL, TOKEN_IMPL)
    log(f"Predicted token address: {predicted}")
    log("")

    # Step 4: Deploy token
    log("--- Step 4: Deploy Token ---")
    result = deploy_token(w3, account, token_name, token_symbol, cid, salt)
    token = result["token"]
    log(f"Token: {token}")
    log(f"TX: https://bscscan.com/tx/{result['tx_hash']}")
    log("")

    # Step 5: Initial buy
    log("--- Step 5: Initial Buy ---")
    buy_tx = initial_buy(w3, account, token, initial_buy_bnb)
    log(f"Buy TX: https://bscscan.com/tx/{buy_tx}")
    log("")

    # Summary
    log("=" * 60)
    log("LAUNCH COMPLETE")
    log(f"  Token:    {token}")
    log(f"  Suffix:   ...{token[-4:]}")
    log(f"  IPFS:     {cid}")
    log(f"  Explorer: https://bscscan.com/token/{token}")
    log(f"  D9 Page:  https://www.district9.club/token/{token}")
    log("=" * 60)


if __name__ == "__main__":
    main()
