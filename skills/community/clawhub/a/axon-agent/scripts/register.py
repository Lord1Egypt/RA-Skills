#!/usr/bin/env python3
"""
Axon Agent Registration Script
Bypasses the official SDK due to ABI mismatch (see references/known-issues.md).
Usage: python3 register.py --private-key-file /path/to/key.txt --capabilities "nlp,coding" --model "claude-sonnet-4.6"
"""
import argparse
import sys
from web3 import Web3

RPC_URL = "https://mainnet-rpc.axonchain.ai/"
CHAIN_ID = 9001
REGISTRY_ADDRESS = "0x0000000000000000000000000000000000000901"

# Correct ABI: 2-param payable (SDK has wrong 3-param nonpayable version)
REGISTRY_ABI = [
    {
        "name": "register",
        "type": "function",
        "stateMutability": "payable",
        "inputs": [
            {"name": "capabilities", "type": "string"},
            {"name": "model", "type": "string"}
        ],
        "outputs": []
    },
    {
        "name": "isAgent",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "addr", "type": "address"}],
        "outputs": [{"name": "", "type": "bool"}]
    },
    {
        "name": "getAgent",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "addr", "type": "address"}],
        "outputs": [
            {"name": "agentId", "type": "string"},
            {"name": "capabilities", "type": "string[]"},
            {"name": "model", "type": "string"},
            {"name": "reputation", "type": "uint256"},
            {"name": "isOnline", "type": "bool"}
        ]
    }
]

STAKE_AMOUNT = Web3.to_wei(100, "ether")  # 100 AXON, 20 burned permanently


def main():
    parser = argparse.ArgumentParser(description="Register an Axon Agent")
    parser.add_argument("--private-key-file", required=True, help="Path to private key file")
    parser.add_argument("--capabilities", default="nlp,reasoning,coding,research")
    parser.add_argument("--model", default="claude-sonnet-4.6")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without sending TX")
    args = parser.parse_args()

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("ERROR: Cannot connect to RPC", file=sys.stderr)
        sys.exit(1)

    private_key = open(args.private_key_file).read().strip()
    account = w3.eth.account.from_key(private_key)
    address = account.address

    balance = w3.eth.get_balance(address)
    balance_axon = w3.from_wei(balance, "ether")
    print(f"地址: {address}")
    print(f"余额: {balance_axon:.4f} AXON")
    print(f"当前块: {w3.eth.block_number}")

    if balance < STAKE_AMOUNT:
        print(f"ERROR: 余额不足，需要至少 100 AXON（当前 {balance_axon:.4f}）", file=sys.stderr)
        sys.exit(1)

    registry = w3.eth.contract(address=REGISTRY_ADDRESS, abi=REGISTRY_ABI)

    # Check if already registered (isAgent ABI decode may fail on some nodes — skip if so)
    try:
        if registry.functions.isAgent(address).call():
            print("已是 Agent，无需重复注册")
            try:
                info = registry.functions.getAgent(address).call()
                print(f"Agent ID: {info[0]} | isOnline: {info[4]} | Reputation: {info[3]}")
            except Exception:
                pass
            return
    except Exception as e:
        print(f"[WARN] isAgent 查询失败（已知问题，继续注册）: {e}")

    if args.dry_run:
        print(f"[DRY RUN] 将以 capabilities='{args.capabilities}', model='{args.model}', stake=100 AXON 注册")
        return

    print(f"正在注册 Agent (capabilities={args.capabilities}, model={args.model})...")

    # eth_call simulation (best-effort — Axon precompile may return empty, skip if fails)
    try:
        registry.functions.register(args.capabilities, args.model).call({
            "from": address, "value": STAKE_AMOUNT
        })
        print("eth_call 模拟通过，发送真实交易...")
    except Exception as e:
        print(f"[WARN] eth_call 模拟失败（Axon 预编译合约已知问题，继续发送真实交易）: {e}")

    nonce = w3.eth.get_transaction_count(address)
    tx = registry.functions.register(args.capabilities, args.model).build_transaction({
        "from": address,
        "value": STAKE_AMOUNT,
        "chainId": CHAIN_ID,
        "gas": 200000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
    })
    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"TX Hash: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    print(f"Status: {receipt['status']} | Block: {receipt['blockNumber']} | Gas: {receipt['gasUsed']}")

    if receipt["status"] == 1:
        is_agent = registry.functions.isAgent(address).call()
        new_balance = w3.from_wei(w3.eth.get_balance(address), "ether")
        print(f"isAgent: {is_agent} | 余额: {new_balance:.4f} AXON")
        print("✅ 注册成功！注意：注册后需等待 720 块（约 1 小时）才能发送首次心跳。")
    else:
        print("❌ 交易失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
