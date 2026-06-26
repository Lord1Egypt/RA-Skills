#!/usr/bin/env python3
"""Fortytwo Prime preflight check — verify wallet, dependencies, and USDC balance."""

import os
import sys

USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_MONAD = "0x754704Bc059F8C67012fEd69BC8A327a5aafb603"
RPC_BASE = "https://mainnet.base.org"
RPC_MONAD = "https://rpc.monad.xyz"

BALANCE_ABI = [
    {"name": "balanceOf", "type": "function",
     "inputs": [{"type": "address"}],
     "outputs": [{"type": "uint256"}],
     "stateMutability": "view"}
]


def main():
    errors = []

    # 1. Check evm_private_key
    key = os.environ.get("evm_private_key")
    if not key:
        errors.append("evm_private_key not set")
        print("FAIL: evm_private_key environment variable not set")
        print("  Fix: export evm_private_key=\"0x...\"")
        print("  Use a dedicated low-value wallet with USDC on Base or Monad.")
        sys.exit(1)

    # 2. Check dependencies
    try:
        from eth_account import Account
        from web3 import Web3
    except ImportError as e:
        print(f"FAIL: missing dependency: {e}")
        print("  Fix: pip install eth-account web3")
        sys.exit(1)

    # 3. Derive wallet address
    try:
        account = Account.from_key(key)
    except Exception as e:
        print(f"FAIL: invalid private key: {e}")
        sys.exit(1)

    print(f"Wallet: {account.address}")

    # 4. Check USDC balance on all networks
    networks = [
        ("Base",  RPC_BASE,  USDC_BASE),
        ("Monad", RPC_MONAD, USDC_MONAD),
    ]
    ready_networks = []
    for name, rpc, usdc_addr in networks:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc))
            usdc = w3.eth.contract(
                address=Web3.to_checksum_address(usdc_addr), abi=BALANCE_ABI
            )
            balance = usdc.functions.balanceOf(account.address).call()
            balance_usdc = balance / 1e6
            print(f"USDC balance ({name}): {balance_usdc:.2f} USDC")
            if balance_usdc >= 2.0:
                ready_networks.append(name)
        except Exception as e:
            print(f"WARN: could not check {name} balance: {e}")

    # 5. Summary
    if not ready_networks:
        print("\nStatus: NOT READY (no network with >= 2.0 USDC)")
        sys.exit(1)
    else:
        print(f"\nStatus: READY (available: {', '.join(ready_networks)})")
        sys.exit(0)


if __name__ == "__main__":
    main()
