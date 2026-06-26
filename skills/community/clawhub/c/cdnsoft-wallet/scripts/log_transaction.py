#!/usr/bin/env python3
"""
log_transaction.py — create, sign, broadcast an EVM transaction and log it to agentwallet.json.

Usage:
    python3 log_transaction.py <amount> <asset> <network> <to> <purpose> \\
        --wallet-key <path>   \\
        --rpc <url>           \\
        [--contract <addr>]   \\
        [--output <path>]     \\
        [--tx-hash <hash>]    \\
        [--decimals <int>]    \\
        [--direction <sent|received>] \\
        [--swap-to <contract>] \\
        [--decimals-out <int>] \\
        [--fee <int>]

Arguments:
    amount      numeric amount (e.g. 0.02)
    asset       asset symbol for the log (e.g. ETH, USDC)
    network     network name for the log (e.g. Base, Ethereum)
    to          recipient address (or sender for received; ignored for swaps)
    purpose     description of the transaction

Options:
    --wallet-key <path>          path to JSON file with "private_key" field
    --rpc <url>                  EVM-compatible RPC endpoint
    --contract <addr>            ERC20 contract address for input token (omit for native ETH)
    --output <path>              path to agentwallet.json (required — ask your human if unsure)
    --tx-hash <hash>             skip tx creation and just log an existing hash
    --decimals <int>             input token decimals (default: 18; USDC = 6)
    --direction <sent|received>  direction for log-only entries (default: sent)
    --swap-to <contract>         output token contract — triggers Uniswap V3 swap
    --decimals-out <int>         output token decimals (default: 6)
    --fee <int>                  Uniswap V3 pool fee tier in bps (default: 500 = 0.05%)
    --min-out <amount>           minimum output amount in human units (slippage protection)
    --asset-out <symbol>         output asset symbol for the log (default: TOKEN)

Examples:
    # Native ETH transfer
    python3 log_transaction.py 0.001 ETH Base 0xRecipient "fund wallet" \\
        --wallet-key ~/.secrets/eth_wallet.json \\
        --rpc https://mainnet.base.org

    # USDC transfer (ERC20, 6 decimals)
    python3 log_transaction.py 0.02 USDC Base 0xRecipient "GateSkip captcha" \\
        --wallet-key ~/.secrets/eth_wallet.json \\
        --rpc https://mainnet.base.org \\
        --contract 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \\
        --decimals 6

    # Uniswap V3 swap: ETH → USDC on Base
    python3 log_transaction.py 0.0012 ETH Base - "swap ETH to USDC" \\
        --wallet-key ~/.secrets/eth_wallet.json \\
        --rpc https://mainnet.base.org \\
        --swap-to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \\
        --asset-out USDC --decimals-out 6

    # Log existing tx without broadcasting
    python3 log_transaction.py 0.02 USDC Base 0xRecipient "manual payment" \\
        --tx-hash 0xabc123... \\
        --output /path/to/agentwallet.json
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from eth_account import Account
from eth_account.signers.local import LocalAccount


def parse_args(argv):
    args = argv[1:]
    opts = {}

    flags = [
        "--wallet-key", "--rpc", "--contract", "--output", "--tx-hash",
        "--decimals", "--direction", "--swap-to", "--decimals-out", "--fee", "--asset-out", "--min-out",
        "--amount", "--asset", "--network", "--from", "--to", "--purpose", "--calldata"
    ]
    positional = []

    i = 0
    while i < len(args):
        if args[i] in flags:
            if i + 1 >= len(args):
                print(f"Error: {args[i]} requires a value")
                sys.exit(1)
            opts[args[i].lstrip("-").replace("-", "_")] = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1

    # Positional args take precedence; named flags (--amount etc.) fill in if positionals absent
    if len(positional) >= 5:
        opts["amount"]  = positional[0]
        opts["asset"]   = positional[1]
        opts["network"] = positional[2]
        opts.setdefault("to", positional[3])
        opts.setdefault("purpose", positional[4])
    elif not (opts.get("direction") == "received" and opts.get("tx_hash") and
              opts.get("amount") and opts.get("asset")):
        print(__doc__)
        sys.exit(1)

    return opts


def rpc_call(rpc_url: str, method: str, params: list):
    resp = requests.post(rpc_url, json={
        "jsonrpc": "2.0", "id": 1,
        "method": method, "params": params,
    }, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"RPC error: {data['error']}")
    return data["result"]


def get_chain_id(rpc_url):
    return int(rpc_call(rpc_url, "eth_chainId", []), 16)

def get_nonce(rpc_url, address):
    return int(rpc_call(rpc_url, "eth_getTransactionCount", [address, "latest"]), 16)

def get_gas_price(rpc_url):
    return int(rpc_call(rpc_url, "eth_gasPrice", []), 16)

def send_raw(rpc_url, raw_tx):
    return rpc_call(rpc_url, "eth_sendRawTransaction", [raw_tx])


def pad_addr(addr: str) -> bytes:
    return bytes.fromhex(addr[2:].zfill(64))

def pad_int(v: int) -> bytes:
    return v.to_bytes(32, "big")


def encode_erc20_transfer(to: str, amount_int: int) -> bytes:
    """Encode ERC20 transfer(address,uint256) calldata."""
    return bytes.fromhex("a9059cbb") + pad_addr(to) + pad_int(amount_int)


def encode_uniswap_swap(token_in: str, token_out: str, fee: int,
                        recipient: str, amount_in: int,
                        amount_out_min: int = 0) -> bytes:
    """Encode Uniswap V3 SwapRouter02 exactInputSingle calldata.
    selector: 0x04e45aaf
    params: tokenIn, tokenOut, fee, recipient, amountIn, amountOutMinimum, sqrtPriceLimitX96
    Set amount_out_min > 0 to enable slippage protection.
    """
    selector = bytes.fromhex("04e45aaf")
    return (selector
        + pad_addr(token_in)
        + pad_addr(token_out)
        + pad_int(fee)
        + pad_addr(recipient)
        + pad_int(amount_in)
        + pad_int(amount_out_min)
        + pad_int(0)   # sqrtPriceLimitX96
    )


def get_erc20_balance(rpc_url: str, token: str, address: str) -> int:
    """Read ERC20 balance of address."""
    calldata = "0x70a08231" + address[2:].zfill(64)
    result = rpc_call(rpc_url, "eth_call", [{"to": token, "data": calldata}, "latest"])
    return int(result, 16)


def log_to_wallet(log_path: Path, entry: dict):
    if not log_path.exists():
        log_path.write_text(json.dumps({"transactions": []}, indent=2))
    data = json.loads(log_path.read_text())
    data["transactions"].append(entry)
    log_path.write_text(json.dumps(data, indent=2))
    print(f"✅ Logged to {log_path}")


def sign_and_send(account, rpc_url, tx_fields):
    chain_id  = get_chain_id(rpc_url)
    nonce     = get_nonce(rpc_url, account.address)
    gas_price = get_gas_price(rpc_url)

    tx = {**tx_fields, "nonce": nonce, "chainId": chain_id,
          "maxFeePerGas": gas_price * 2, "maxPriorityFeePerGas": gas_price, "type": 2}

    # estimate gas
    est_tx = {k: hex(v) if isinstance(v, int) else v for k, v in tx.items()
              if k not in ("from", "type", "chainId")}
    est_tx["from"] = account.address
    gas = int(rpc_call(rpc_url, "eth_estimateGas", [est_tx]), 16)
    tx["gas"] = int(gas * 1.2)

    signed = account.sign_transaction(tx)
    raw_hex = "0x" + signed.rawTransaction.hex()
    return send_raw(rpc_url, raw_hex)


def main():
    opts = parse_args(sys.argv)

    amount  = opts.get("amount", "")
    asset   = opts.get("asset", "")
    network = opts.get("network", "Base")
    to      = opts.get("to", "")
    purpose = opts.get("purpose", "")

    if "output" not in opts:
        print("⚠️  --output is required: path to your agentwallet.json log file.")
        print("    If you don't have one yet, ask your human where to store it.")
        print("    Example: --output ~/my-wallet/agentwallet.json")
        sys.exit(1)
    output_path = Path(opts["output"]).expanduser().resolve()

    tx_hash   = opts.get("tx_hash")
    direction = opts.get("direction", "sent")

    if direction not in ("sent", "received"):
        print("⚠️  --direction must be 'sent' or 'received'")
        sys.exit(1)

    # ── Log-only: received ────────────────────────────────────────────────────
    if direction == "received":
        if not tx_hash:
            print("⚠️  --tx-hash is required when logging a received transaction")
            sys.exit(1)
        log_to_wallet(output_path, {
            "date":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "direction": "received",
            "amount":    amount,
            "asset":     asset,
            "network":   network,
            "from":      opts.get("from") or to,
            "purpose":   purpose,
            "tx_hash":   tx_hash,
        })
        return

    # ── Log-only: existing tx hash ────────────────────────────────────────────
    if tx_hash:
        log_to_wallet(output_path, {
            "date":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "direction": "sent",
            "amount":    amount,
            "asset":     asset,
            "network":   network,
            "to":        to,
            "purpose":   purpose,
            "tx_hash":   tx_hash,
        })
        return

    # ── Require wallet + rpc for broadcasting ─────────────────────────────────
    if "wallet_key" not in opts:
        print("⚠️  --wallet-key is required: path to your wallet JSON file.")
        print("    Ask your human for the path to a wallet JSON with a 'private_key' field.")
        print("    Example: --wallet-key ~/.secrets/eth_wallet.json")
        sys.exit(1)
    if "rpc" not in opts:
        print("⚠️  --rpc is required: an EVM-compatible RPC endpoint URL.")
        print("    Ask your human for an RPC URL for the target network.")
        print("    Example: --rpc https://mainnet.base.org")
        sys.exit(1)

    key_path = Path(opts["wallet_key"]).expanduser()
    key_data = json.loads(key_path.read_text())
    private_key = key_data.get("private_key") or key_data.get("privateKey")
    if not private_key:
        print(f"Error: no 'private_key' field found in {key_path}")
        sys.exit(1)

    account: LocalAccount = Account.from_key(private_key)
    rpc_url = opts["rpc"]

    # ── Uniswap V3 Swap ───────────────────────────────────────────────────────
    if "swap_to" in opts:
        WETH        = "0x4200000000000000000000000000000000000006"
        SWAP_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"  # SwapRouter02 on Base

        token_in    = opts.get("contract", WETH)  # default: native ETH via WETH
        token_out   = opts["swap_to"]
        fee         = int(opts.get("fee", 500))
        decimals_in = int(opts.get("decimals", 18))
        decimals_out= int(opts.get("decimals_out", 6))
        asset_out   = opts.get("asset_out", "TOKEN")
        amount_in    = int(float(amount) * 10 ** decimals_in)
        is_eth_in    = token_in.lower() == WETH.lower() and "contract" not in opts
        min_out_raw  = opts.get("min_out")
        amount_out_min = int(float(min_out_raw) * 10 ** decimals_out) if min_out_raw else 0
        if amount_out_min:
            print(f"Slippage protection: min output = {min_out_raw} {asset_out}")
        else:
            print("⚠️  No slippage protection (--min-out not set). Use --min-out for large swaps.")

        calldata = encode_uniswap_swap(
            token_in if not is_eth_in else WETH,
            token_out, fee, account.address, amount_in, amount_out_min
        )

        # snapshot output balance before swap
        bal_before = get_erc20_balance(rpc_url, token_out, account.address)

        tx_fields = {
            "from":  account.address,
            "to":    SWAP_ROUTER,
            "value": amount_in if is_eth_in else 0,
            "data":  "0x" + calldata.hex(),
        }

        print(f"Swapping {amount} {asset} → {asset_out} via Uniswap V3...")
        tx_hash = sign_and_send(account, rpc_url, tx_fields)
        print(f"Tx hash: {tx_hash}")

        # wait for confirmation then read actual output amount
        print("Waiting for confirmation...")
        for _ in range(20):
            time.sleep(3)
            receipt = rpc_call(rpc_url, "eth_getTransactionReceipt", [tx_hash])
            if receipt:
                status = int(receipt["status"], 16)
                if status == 0:
                    print("❌ Swap failed on-chain")
                    sys.exit(1)
                break

        bal_after = get_erc20_balance(rpc_url, token_out, account.address)
        amount_out = (bal_after - bal_before) / 10 ** decimals_out

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        log_to_wallet(output_path, {
            "date": now, "direction": "sent", "amount": amount, "asset": asset,
            "network": network, "to": SWAP_ROUTER, "purpose": purpose, "tx_hash": tx_hash,
        })
        log_to_wallet(output_path, {
            "date": now, "direction": "received", "amount": str(round(amount_out, 6)),
            "asset": asset_out, "network": network, "from": SWAP_ROUTER,
            "purpose": purpose, "tx_hash": tx_hash,
        })
        print(f"✅ Swapped {amount} {asset} → {amount_out:.6f} {asset_out}")
        return

    # ── Arbitrary contract call ───────────────────────────────────────────────
    if "calldata" in opts:
        calldata_hex = opts["calldata"]
        if not calldata_hex.startswith("0x"):
            calldata_hex = "0x" + calldata_hex
        amount_float = float(amount) if amount else 0.0
        tx_fields = {
            "from":  account.address,
            "to":    to,
            "value": int(amount_float * 10**18),
            "data":  calldata_hex,
        }
        print(f"Sending contract call to {to} ({amount} {asset}) on {network}...")
        tx_hash = sign_and_send(account, rpc_url, tx_fields)
        print(f"Tx hash: {tx_hash}")
        log_to_wallet(output_path, {
            "date":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "direction": "sent",
            "amount":    amount,
            "asset":     asset,
            "network":   network,
            "to":        to,
            "purpose":   purpose,
            "tx_hash":   tx_hash,
        })
        print(f"✅ Contract call sent and logged")
        return

    # ── ERC20 or ETH transfer ─────────────────────────────────────────────────
    decimals    = int(opts.get("decimals", 18))
    amount_float= float(amount)
    amount_int  = int(amount_float * 10 ** decimals)
    contract    = opts.get("contract")

    if contract:
        calldata = encode_erc20_transfer(to, amount_int)
        tx_fields = {"from": account.address, "to": contract, "value": 0,
                     "data": "0x" + calldata.hex()}
    else:
        tx_fields = {"from": account.address, "to": to,
                     "value": int(amount_float * 10**18), "data": "0x"}

    print(f"Broadcasting {amount} {asset} → {to} on {network}...")
    tx_hash = sign_and_send(account, rpc_url, tx_fields)
    print(f"Tx hash: {tx_hash}")

    log_to_wallet(output_path, {
        "date":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "direction": "sent",
        "amount":    amount,
        "asset":     asset,
        "network":   network,
        "to":        to,
        "purpose":   purpose,
        "tx_hash":   tx_hash,
    })


if __name__ == "__main__":
    main()
