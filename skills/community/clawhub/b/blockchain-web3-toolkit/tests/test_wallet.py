#!/usr/bin/env python3
"""
Wallet Manager Tests - 钱包管理器测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from wallet_manager import WalletManager, Wallet


class TestWalletManager(unittest.TestCase):
    """测试钱包管理器 / Test Wallet Manager"""
    
    def test_create_wallet(self):
        """测试创建钱包 / Test wallet creation"""
        wallet = WalletManager.create_wallet()
        
        self.assertIsNotNone(wallet.address)
        self.assertIsNotNone(wallet.private_key)
        self.assertTrue(wallet.address.startswith('0x'))
        self.assertEqual(len(wallet.address), 42)  # 0x + 40 hex chars
    
    def test_import_from_private_key(self):
        """测试从私钥导入 / Test import from private key"""
        # Generate a wallet first
        original = WalletManager.create_wallet()
        
        # Import it
        imported = WalletManager.import_from_private_key(original.private_key)
        
        self.assertEqual(original.address.lower(), imported.address.lower())
    
    def test_validate_address(self):
        """测试地址验证 / Test address validation"""
        # Valid address
        self.assertTrue(WalletManager.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"))
        
        # Invalid address (too short)
        self.assertFalse(WalletManager.validate_address("0x123"))
        
        # Invalid address (no 0x prefix)
        self.assertFalse(WalletManager.validate_address("742d35Cc6634C0532925a3b844Bc9e7595f0bEb"))
    
    def test_wallet_serialization(self):
        """测试钱包序列化 / Test wallet serialization"""
        wallet = WalletManager.create_wallet()
        
        # Convert to dict
        data = wallet.to_dict()
        self.assertIn('address', data)
        self.assertIn('private_key', data)
        
        # Convert back
        restored = Wallet.from_dict(data)
        self.assertEqual(wallet.address, restored.address)
        self.assertEqual(wallet.private_key, restored.private_key)


class TestWallet(unittest.TestCase):
    """测试钱包类 / Test Wallet class"""
    
    def test_wallet_creation(self):
        """测试钱包对象创建 / Test wallet object creation"""
        wallet = Wallet("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "0x1234567890abcdef")
        
        self.assertEqual(wallet.address, "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
        self.assertEqual(wallet.private_key, "0x1234567890abcdef")


if __name__ == '__main__':
    unittest.main()
