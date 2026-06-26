#!/usr/bin/env python3
"""
NFT Tools - NFT工具集
"""

from typing import Dict, List
from contract_interface import ContractInterface

# Standard ERC721 ABI (partial)
ERC721_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "tokenId", "type": "uint256"}
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "tokenId", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": True, "name": "tokenId", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]


class NFTTools:
    """NFT工具类 / NFT Tools"""
    
    def __init__(self, network: str = "sepolia", private_key: str = None):
        self.interface = ContractInterface(network, private_key)
    
    def get_owner(self, contract_address: str, token_id: int) -> str:
        """查询NFT持有者 / Get NFT owner"""
        return self.interface.call(contract_address, ERC721_ABI, "ownerOf", token_id)
    
    def get_token_uri(self, contract_address: str, token_id: int) -> str:
        """查询NFT元数据URI / Get NFT metadata URI"""
        return self.interface.call(contract_address, ERC721_ABI, "tokenURI", token_id)
    
    def mint_nft(self, contract_address: str, to_address: str, token_id: int) -> str:
        """铸造NFT / Mint NFT"""
        return self.interface.send_transaction(
            contract_address, ERC721_ABI, "mint", to_address, token_id
        )
    
    def transfer_nft(self, contract_address: str, from_address: str, to_address: str, token_id: int) -> str:
        """转移NFT / Transfer NFT"""
        return self.interface.send_transaction(
            contract_address, ERC721_ABI, "transferFrom", from_address, to_address, token_id
        )


def main():
    """示例用法 / Example usage"""
    print("NFT Tools Demo")
    print("\nExample: Query NFT owner")
    print("  nft = NFTTools('mainnet')")
    print("  owner = nft.get_owner('0x...', 1234)")


if __name__ == "__main__":
    main()
