"""
RPC Manager — Handles rate limits, failover, and retries
"""

import time
from web3 import Web3

RPCS = [
    "https://mainnet.base.org",
    "https://base.llamarpc.com",
    "https://base.meowrpc.com",
    "https://base-rpc.publicnode.com",
    "https://1rpc.io/base",
]

_current_idx = 0
_last_request = 0
_min_interval = 0.5  # 500ms between requests


def get_w3():
    """Get a working Web3 instance with automatic failover."""
    global _current_idx, _last_request

    # Rate limit ourselves
    elapsed = time.time() - _last_request
    if elapsed < _min_interval:
        time.sleep(_min_interval - elapsed)

    for attempt in range(len(RPCS)):
        idx = (_current_idx + attempt) % len(RPCS)
        rpc = RPCS[idx]
        try:
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))
            if w3.is_connected():
                _current_idx = idx
                _last_request = time.time()
                return w3
        except Exception:
            continue

    raise ConnectionError("All Base RPCs are down or rate-limited")


def call_with_retry(fn, max_retries=3, backoff=2):
    """Call a web3 function with exponential backoff on rate limits."""
    global _current_idx
    for attempt in range(max_retries):
        try:
            result = fn()
            return result
        except Exception as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                _current_idx = (_current_idx + 1) % len(RPCS)
                wait = backoff ** attempt
                time.sleep(wait)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
