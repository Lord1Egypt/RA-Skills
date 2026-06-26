#!/usr/bin/env python3
"""
Basic Usage Example - 基础使用示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from wallet_manager import WalletManager


def main():
    print("=" * 60)
    print("Blockchain Web3 Toolkit - Basic Usage Example")
    print("=" * 60)
    
    # 1. Create a new wallet
    print("\n[Step 1] Creating a new Ethereum wallet...")
    wallet = WalletManager.create_wallet()
    print(f"✓ Address: {wallet.address}")
    print(f"✓ Private Key: {wallet.private_key[:20]}...{wallet.private_key[-10:]}")
    print("  ⚠️  IMPORTANT: Save this private key securely!")
    
    # 2. Validate the address
    print("\n[Step 2] Validating the address...")
    is_valid = WalletManager.validate_address(wallet.address)
    print(f"✓ Address is valid: {is_valid}")
    
    # 3. Import wallet from private key
    print("\n[Step 3] Importing wallet from private key...")
    imported = WalletManager.import_from_private_key(wallet.private_key)
    print(f"✓ Imported address: {imported.address}")
    print(f"✓ Addresses match: {wallet.address.lower() == imported.address.lower()}")
    
    # 4. Save to file (example)
    print("\n[Step 4] Saving wallet information...")
    wallet_data = wallet.to_dict()
    print(f"✓ Wallet data ready for storage")
    print(f"  Keys: {list(wallet_data.keys())}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Use get_balance() to check ETH balance")
    print("  - Use ContractInterface to interact with smart contracts")
    print("  - Use NFTTools for NFT operations")
    print("=" * 60)


if __name__ == "__main__":
    main()
