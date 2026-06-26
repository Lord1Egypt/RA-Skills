"""Wallet management — private key to address, signing."""

from eth_account import Account
from web3 import Web3


def get_public_address(private_key: str) -> str:
    """Derive public address from private key."""
    acct = Account.from_key(private_key)
    return acct.address


def get_balance(rpc_url: str, address: str) -> float:
    """Get wallet balance in native token (BNB/ETH)."""
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
    return float(w3.from_wei(balance_wei, "ether"))
