#!/usr/bin/env python3
"""
Contract Interface - 智能合约交互接口
"""

import os
import json
from typing import Any, List
from web3 import Web3
from eth_account import Account


class ContractInterface:
    """智能合约交互类 / Smart Contract Interface"""
    
    def __init__(self, network: str = "sepolia", private_key: str = None):
        """
        初始化合约接口
        Initialize contract interface
        
        Args:
            network: 网络名称 (mainnet/sepolia/goerli)
            private_key: 用于发送交易的私钥
        """
        from wallet_manager import NETWORKS
        
        self.network = network
        self.rpc_url = NETWORKS.get(network, NETWORKS["sepolia"])
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Cannot connect to {network}")
        
        self.account = None
        if private_key:
            self.account = Account.from_key(private_key)
    
    def deploy(self, abi: list, bytecode: str, *args) -> str:
        """
        部署智能合约 / Deploy smart contract
        
        Returns:
            合约地址 / Contract address
        """
        if not self.account:
            raise ValueError("Private key required for deployment")
        
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        # Build transaction
        tx = Contract.constructor(*args).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 5000000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt.contractAddress
    
    def call(self, contract_address: str, abi: list, function_name: str, *args):
        """
        调用只读函数 / Call view function
        """
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi
        )
        
        func = getattr(contract.functions, function_name)
        return func(*args).call()
    
    def send_transaction(self, contract_address: str, abi: list, function_name: str, *args) -> str:
        """
        发送状态变更交易 / Send state-changing transaction
        
        Returns:
            交易哈希 / Transaction hash
        """
        if not self.account:
            raise ValueError("Private key required for transactions")
        
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi
        )
        
        func = getattr(contract.functions, function_name)
        
        tx = func(*args).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()


def main():
    """示例用法 / Example usage"""
    print("Contract Interface Demo")
    print("This module provides smart contract interaction capabilities.")
    print("\nUsage:")
    print("  interface = ContractInterface('sepolia', 'your_private_key')")
    print("  address = interface.deploy(abi, bytecode)")
    print("  result = interface.call(address, abi, 'functionName', arg1, arg2)")


if __name__ == "__main__":
    main()
