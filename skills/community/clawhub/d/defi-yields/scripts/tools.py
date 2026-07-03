from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_yield_pools(
    chain: Optional[str] = None,
    project: Optional[str] = None
) -> Dict[str, Any]:
    """
    
Fetch DeFi yield pools from the yields.llama.fi API, optionally filtering by chain or project.
Returns symbol, project, tvlUsd, apy, apyMean30d, and predictions for each pool.

Args:
    chain: Optional filter for blockchain (e.g., 'Ethereum', 'Solana')
    project: Optional filter for project name (e.g., 'lido', 'aave-v3')

    
    Args:
        chain: null
        project: null
    
    Returns:
        null
    """
    arguments = {
        "chain": chain,
        "project": project
    }
    
    return call_api("1777419071388675", "get_yield_pools", arguments)

