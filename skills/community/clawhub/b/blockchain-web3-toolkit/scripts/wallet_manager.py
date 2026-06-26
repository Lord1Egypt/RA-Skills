#!/usr/bin/env python3
"""
Wallet Manager - 钱包管理器
"""

import os
import json
from typing import Optional, Dict
from eth_account import Account
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Network RPC endpoints
NETWORKS = {
    "mainnet": f"https://mainnet.infura.io/v3/{os.getenv('INFURA_API_KEY', '')}",
    "sepolia": f"https://sepolia.infura.io/v3/{os.getenv('INFURA_API_KEY', '')}",
    "goerli": f"https://goerli.infura.io/v3/{os.getenv('INFURA_API_KEY', '')}",
}


class Wallet:
    """以太坊钱包类 / Ethereum Wallet Class"""
    
    def __init__(self, address: str, private_key: str):
        self.address = address
        self.private_key = private_key
    
    def to_dict(self) -> Dict:
        return {
            "address": self.address,
            "private_key": self.private_key
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Wallet":
        return cls(data["address"], data["private_key"])


class WalletManager:
    """钱包管理器 / Wallet Manager"""
    
    @staticmethod
    def create_wallet() -> Wallet:
        """创建新钱包 / Create new wallet"""
        account = Account.create()
        return Wallet(account.address, account.key.hex())
    
    @staticmethod
    def import_from_private_key(private_key: str) -> Wallet:
        """从私钥导入钱包 / Import wallet from private key"""
        account = Account.from_key(private_key)
        return Wallet(account.address, private_key)
    
    @staticmethod
    def import_from_mnemonic(mnemonic: str) -> Wallet:
        """从助记词导入钱包 / Import wallet from mnemonic"""
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(mnemonic)
        return Wallet(account.address, account.key.hex())
    
    @staticmethod
    def get_balance(address: str, network: str = "mainnet") -> float:
        """查询ETH余额 / Get ETH balance"""
        rpc_url = NETWORKS.get(network, NETWORKS["mainnet"])
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            raise ConnectionError(f"Cannot connect to {network}")
        
        checksum_address = Web3.to_checksum_address(address)
        balance_wei = w3.eth.get_balance(checksum_address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        return float(balance_eth)
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """验证地址格式 / Validate address format"""
        try:
            return Web3.is_address(address)
        except:
            return False


def main():
    """示例用法 / Example usage"""
    print("=" * 50)
    print("Blockchain Web3 Toolkit - Wallet Manager")
    print("=" * 50)
    
    # 创建新钱包
    print("\n[1] Creating new wallet...")
    wallet = WalletManager.create_wallet()
    print(f"Address: {wallet.address}")
    print(f"Private Key: {wallet.private_key[:20]}...{wallet.private_key[-10:]}")
    
    # 验证地址
    print(f"\n[2] Validating address...")
    is_valid = WalletManager.validate_address(wallet.address)
    print(f"Valid: {is_valid}")
    
    print("\n" + "=" * 50)
    print("Done! Remember to save your private key securely.")
    print("=" * 50)


if __name__ == "__main__":
    main()
