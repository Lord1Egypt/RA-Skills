#!/usr/bin/env python3
"""
Check Axon Agent on-chain status.
Usage: python3 check-status.py --address 0x... 
   or: python3 check-status.py --private-key-file /path/to/key.txt
"""
import argparse
from web3 import Web3

RPC_URL = "https://mainnet-rpc.axonchain.ai/"
REGISTRY_ADDRESS = "0x0000000000000000000000000000000000000901"
REGISTRY_ABI = [
    {"name": "isAgent", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "addr", "type": "address"}], "outputs": [{"name": "", "type": "bool"}]},
    {"name": "getAgent", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "addr", "type": "address"}],
     "outputs": [
         {"name": "agentId", "type": "string"},
         {"name": "capabilities", "type": "string[]"},
         {"name": "model", "type": "string"},
         {"name": "reputation", "type": "uint256"},
         {"name": "isOnline", "type": "bool"}
     ]}
]


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--address", help="Agent EVM address")
    group.add_argument("--private-key-file", help="Path to private key file")
    args = parser.parse_args()

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    registry = w3.eth.contract(address=REGISTRY_ADDRESS, abi=REGISTRY_ABI)

    if args.private_key_file:
        pk = open(args.private_key_file).read().strip()
        address = w3.eth.account.from_key(pk).address
    else:
        address = args.address

    balance = w3.from_wei(w3.eth.get_balance(address), "ether")
    block = w3.eth.block_number

    print(f"地址:    {address}")
    print(f"余额:    {balance:.4f} AXON")
    print(f"当前块:  {block}")

    # isAgent / getAgent: Axon precompile may return empty bytes — wrap in try/except
    try:
        is_agent = registry.functions.isAgent(address).call()
        print(f"isAgent: {is_agent}")
    except Exception as e:
        print(f"isAgent: 查询失败（Axon 预编译合约已知问题）: {e}")
        is_agent = False

    if is_agent:
        try:
            info = registry.functions.getAgent(address).call()
            print(f"Agent ID:     {info[0]}")
            print(f"Capabilities: {', '.join(info[1])}")
            print(f"Model:        {info[2]}")
            print(f"Reputation:   {info[3]}")
            print(f"ONLINE:       {info[4]}")
        except Exception as e:
            print(f"getAgent: 查询失败: {e}")


if __name__ == "__main__":
    main()
