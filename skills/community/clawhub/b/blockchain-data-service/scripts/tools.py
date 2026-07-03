from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_core_contracts(
) -> Dict[str, Any]:
    """
    Get core contract addresses
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659581955", "get_core_contracts", arguments)

def get_chain_info(
) -> Dict[str, Any]:
    """
    Get information about an EVM network
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659581955", "get_chain_info", arguments)

def get_supported_networks(
) -> Dict[str, Any]:
    """
    Get a list of supported EVM networks
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659581955", "get_supported_networks", arguments)

def get_block_by_number(
    blockNumber: float
) -> Dict[str, Any]:
    """
    Get a block by its block number
    
    Args:
        blockNumber: The block number to fetch
    
    Returns:
        
    """
    arguments = {
        "blockNumber": blockNumber
    }
    
    return call_api("1777316659581955", "get_block_by_number", arguments)

def get_latest_block(
) -> Dict[str, Any]:
    """
    Get the latest block from the EVM
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659581955", "get_latest_block", arguments)

def get_balance(
    address: str
) -> Dict[str, Any]:
    """
    Get the native token balance (ETH, MATIC, etc.) for an address
    
    Args:
        address: The wallet address or ENS name (e.g., '0x1234...' or 'vitalik.eth') to check the balance for
    
    Returns:
        
    """
    arguments = {
        "address": address
    }
    
    return call_api("1777316659581955", "get_balance", arguments)

def get_erc20_balance(
    address: str,
    tokenAddress: str
) -> Dict[str, Any]:
    """
    Get the ERC20 token balance of an Ethereum address
    
    Args:
        address: The Ethereum address to check
        tokenAddress: The ERC20 token contract address
    
    Returns:
        
    """
    arguments = {
        "address": address,
        "tokenAddress": tokenAddress
    }
    
    return call_api("1777316659581955", "get_erc20_balance", arguments)

def get_token_balance(
    tokenAddress: str,
    ownerAddress: str
) -> Dict[str, Any]:
    """
    Get the balance of an ERC20 token for an address
    
    Args:
        tokenAddress: The contract address or ENS name of the ERC20 token (e.g., '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48' for USDC or 'uniswap.eth')
        ownerAddress: The wallet address or ENS name to check the balance for (e.g., '0x1234...' or 'vitalik.eth')
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress,
        "ownerAddress": ownerAddress
    }
    
    return call_api("1777316659581955", "get_token_balance", arguments)

def get_transaction(
    txHash: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific transaction by its hash. Includes sender, recipient, value, data, and more.
    
    Args:
        txHash: The transaction hash to look up (e.g., '0x1234...')
    
    Returns:
        
    """
    arguments = {
        "txHash": txHash
    }
    
    return call_api("1777316659581955", "get_transaction", arguments)

def get_transaction_receipt(
    txHash: str
) -> Dict[str, Any]:
    """
    Get a transaction receipt by its hash
    
    Args:
        txHash: The transaction hash to look up
    
    Returns:
        
    """
    arguments = {
        "txHash": txHash
    }
    
    return call_api("1777316659581955", "get_transaction_receipt", arguments)

def estimate_gas(
    to: str,
    value: Optional[str] = None,
    data: Optional[str] = None
) -> Dict[str, Any]:
    """
    Estimate the gas cost for a transaction
    
    Args:
        to: The recipient address
        value: The amount of ETH to send in ether (e.g., '0.1')
        data: The transaction data as a hex string
    
    Returns:
        
    """
    arguments = {
        "to": to,
        "value": value,
        "data": data
    }
    
    return call_api("1777316659581955", "estimate_gas", arguments)

def read_contract(
    contractAddress: str,
    abi: null,
    functionName: str,
    args: Optional[null] = None
) -> Dict[str, Any]:
    """
    Read data from a smart contract by calling a view/pure function. This doesn't modify blockchain state and doesn't require gas or signing.
    
    Args:
        contractAddress: The address of the smart contract to interact with
        abi: The ABI (Application Binary Interface) of the smart contract function, as a JSON array
        functionName: The name of the function to call on the contract (e.g., 'balanceOf')
        args: The arguments to pass to the function, as an array (e.g., ['0x1234...'])
    
    Returns:
        
    """
    arguments = {
        "contractAddress": contractAddress,
        "abi": abi,
        "functionName": functionName,
        "args": args
    }
    
    return call_api("1777316659581955", "read_contract", arguments)

def is_contract(
    address: str
) -> Dict[str, Any]:
    """
    Check if an address is a smart contract or an externally owned account (EOA)
    
    Args:
        address: The wallet or contract address or ENS name to check (e.g., '0x1234...' or 'uniswap.eth')
    
    Returns:
        
    """
    arguments = {
        "address": address
    }
    
    return call_api("1777316659581955", "is_contract", arguments)

def get_token_info(
    tokenAddress: str
) -> Dict[str, Any]:
    """
    Get comprehensive information about an ERC20 token including name, symbol, decimals, total supply, and other metadata. Use this to analyze any token on EVM chains.
    
    Args:
        tokenAddress: The contract address of the ERC20 token (e.g., '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48' for USDC on Ethereum)
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress
    }
    
    return call_api("1777316659581955", "get_token_info", arguments)

def get_token_balance_erc20(
    address: str,
    tokenAddress: str
) -> Dict[str, Any]:
    """
    Get ERC20 token balance for an address
    
    Args:
        address: The address to check balance for
        tokenAddress: The ERC20 token contract address
    
    Returns:
        
    """
    arguments = {
        "address": address,
        "tokenAddress": tokenAddress
    }
    
    return call_api("1777316659581955", "get_token_balance_erc20", arguments)

def get_nft_info(
    tokenAddress: str,
    tokenId: str,
    network: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific NFT (ERC721 token), including collection name, symbol, token URI, and current owner if available.
    
    Args:
        tokenAddress: The contract address of the NFT collection (e.g., '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D' for Bored Ape Yacht Club)
        tokenId: The ID of the specific NFT token to query (e.g., '1234')
        network: Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. Most NFTs are on Ethereum mainnet, which is the default.
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress,
        "tokenId": tokenId,
        "network": network
    }
    
    return call_api("1777316659581955", "get_nft_info", arguments)

def check_nft_ownership(
    tokenAddress: str,
    tokenId: str,
    ownerAddress: str
) -> Dict[str, Any]:
    """
    Check if an address owns a specific NFT
    
    Args:
        tokenAddress: The contract address or ENS name of the NFT collection (e.g., '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D' for BAYC or 'boredapeyachtclub.eth')
        tokenId: The ID of the NFT to check (e.g., '1234')
        ownerAddress: The wallet address or ENS name to check ownership against (e.g., '0x1234...' or 'vitalik.eth')
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress,
        "tokenId": tokenId,
        "ownerAddress": ownerAddress
    }
    
    return call_api("1777316659581955", "check_nft_ownership", arguments)

def get_erc1155_token_uri(
    tokenAddress: str,
    tokenId: str,
    network: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the metadata URI for an ERC1155 token (multi-token standard used for both fungible and non-fungible tokens). The URI typically points to JSON metadata about the token.
    
    Args:
        tokenAddress: The contract address of the ERC1155 token collection (e.g., '0x76BE3b62873462d2142405439777e971754E8E77')
        tokenId: The ID of the specific token to query metadata for (e.g., '1234')
        network: Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. ERC1155 tokens exist across many networks. Defaults to Ethereum mainnet.
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress,
        "tokenId": tokenId,
        "network": network
    }
    
    return call_api("1777316659581955", "get_erc1155_token_uri", arguments)

def get_nft_balance(
    tokenAddress: str,
    ownerAddress: str,
    network: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the total number of NFTs owned by an address from a specific collection. This returns the count of NFTs, not individual token IDs.
    
    Args:
        tokenAddress: The contract address of the NFT collection (e.g., '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D' for Bored Ape Yacht Club)
        ownerAddress: The wallet address to check the NFT balance for (e.g., '0x1234...')
        network: Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. Most NFTs are on Ethereum mainnet, which is the default.
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress,
        "ownerAddress": ownerAddress,
        "network": network
    }
    
    return call_api("1777316659581955", "get_nft_balance", arguments)

def get_erc1155_balance(
    tokenAddress: str,
    tokenId: str,
    ownerAddress: str,
    network: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the balance of a specific ERC1155 token ID owned by an address. ERC1155 allows multiple tokens of the same ID, so the balance can be greater than 1.
    
    Args:
        tokenAddress: The contract address of the ERC1155 token collection (e.g., '0x76BE3b62873462d2142405439777e971754E8E77')
        tokenId: The ID of the specific token to check the balance for (e.g., '1234')
        ownerAddress: The wallet address to check the token balance for (e.g., '0x1234...')
        network: Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. ERC1155 tokens exist across many networks. Defaults to Ethereum mainnet.
    
    Returns:
        
    """
    arguments = {
        "tokenAddress": tokenAddress,
        "tokenId": tokenId,
        "ownerAddress": ownerAddress,
        "network": network
    }
    
    return call_api("1777316659581955", "get_erc1155_balance", arguments)

