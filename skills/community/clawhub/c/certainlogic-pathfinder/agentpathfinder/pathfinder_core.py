"""AgentPathfinder v2 — Core cryptography and shard management."""
import os
import hmac
import hashlib
import secrets
from typing import List, Tuple


def generate_master_key() -> bytes:
    """Generate 256-bit master key."""
    return secrets.token_bytes(32)


def split_key(master_key: bytes, num_steps: int) -> Tuple[List[bytes], bytes]:
    """
    Split master_key into (num_steps + 1) shards via XOR.
    
    Returns:
        (step_shards, issuer_shard) where:
        - step_shards: List[num_steps] — one per step
        - issuer_shard: bytes — final fragment held by issuer
        
    Reconstruction: XOR all shards together = master_key
    """
    if len(master_key) != 32:
        raise ValueError("Master key must be 32 bytes (256 bits)")
    
    total_shards = num_steps + 1
    
    # Generate N random shards for steps
    step_shards = [secrets.token_bytes(32) for _ in range(num_steps)]
    
    # Compute issuer shard: K XOR s1 XOR s2 XOR ... XOR sN
    issuer_shard = master_key
    for shard in step_shards:
        issuer_shard = bytes(a ^ b for a, b in zip(issuer_shard, shard))
    
    return step_shards, issuer_shard


def reconstruct_key(shards: List[bytes]) -> bytes:
    """Reconstruct master key from all shards via XOR."""
    if not shards:
        raise ValueError("No shards provided")
    
    key = shards[0]
    for shard in shards[1:]:
        key = bytes(a ^ b for a, b in zip(key, shard))
    
    return key


def hmac_sign(key: bytes, message: str) -> str:
    """HMAC-SHA256 sign a message. Returns hex string."""
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()


def verify_hmac(key: bytes, message: str, signature: str) -> bool:
    """Verify HMAC-SHA256 signature."""
    expected = hmac_sign(key, message)
    return hmac.compare_digest(expected, signature)


def hash_key(key: bytes) -> str:
    """SHA-256 hash of key for public reference (never expose raw key)."""
    return hashlib.sha256(key).hexdigest()


def shard_to_hex(shard: bytes) -> str:
    return shard.hex()


def shard_from_hex(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)


def derive_key(master_key: bytes, context: bytes) -> bytes:
    """Derive a sub-key from master_key using HMAC-SHA256.

    This is a simple single-purpose KDF: HMAC-SHA256(master_key, context).
    Used to produce audit signing keys, agent API keys, etc. without
    exposing the master key itself.
    """
    return hmac.new(master_key, context, hashlib.sha256).digest()
