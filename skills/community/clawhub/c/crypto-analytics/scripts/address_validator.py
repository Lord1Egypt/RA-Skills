#!/usr/bin/env python3
"""
Address validation and format detection for multiple blockchains
"""

import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class AddressInfo:
    validated: bool
    chain: str
    address: str
    is_contract: bool = False
    error: Optional[str] = None

class AddressValidator:
    """Validate and classify blockchain addresses"""

    # Chain-specific patterns
    PATTERNS = {
        'ethereum': r'^0x[a-fA-F0-9]{40}$',
        'bitcoin': r'^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,61}$',  # Simplified
        'solana': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$',
        'bsc': r'^0x[a-fA-F0-9]{40}$',  # Same format as ETH
        'polygon': r'^0x[a-fA-F0-9]{40}$',
        'avalanche': r'^0x[a-fA-F0-9]{40}$',
    }

    @staticmethod
    def validate(address: str) -> AddressInfo:
        """Validate address and return chain info"""
        addr = address.strip()

        # Check ETH/EVM chains first
        if re.fullmatch(AddressValidator.PATTERNS['ethereum'], addr, re.IGNORECASE):
            return AddressInfo(validated=True, chain='ethereum', address=addr.lower())

        # Bitcoin
        if re.fullmatch(AddressValidator.PATTERNS['bitcoin'], addr):
            return AddressInfo(validated=True, chain='bitcoin', address=addr)

        # Solana
        if re.fullmatch(AddressValidator.PATTERNS['solana'], addr):
            return AddressInfo(validated=True, chain='solana', address=addr)

        return AddressInfo(validated=False, chain='unknown', address=addr, error='Invalid address format')

    @staticmethod
    def is_contract_address(address: str, chain: str = 'ethereum') -> bool:
        """Check if an EVM address is a contract (not EOA)"""
        # Basic heuristic: contracts often have upper-case letters? Not reliable
        # For real detection, need to fetch code hash from blockchain
        # This is just a stub - in production, check code size via RPC
        return False

    @staticmethod
    def normalize(address: str, chain: Optional[str] = None) -> str:
        """Normalize address to standard format"""
        info = AddressValidator.validate(address)
        if info.validated:
            if info.chain in ('ethereum', 'bsc', 'polygon', 'avalanche'):
                return info.address.lower()
            return info.address
        return address

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: address_validator.py <address>")
        sys.exit(1)

    result = AddressValidator.validate(sys.argv[1])
    if result.validated:
        print(f"Chain: {result.chain}")
        print(f"Normalized: {result.address}")
    else:
        print(f"Error: {result.error}")
