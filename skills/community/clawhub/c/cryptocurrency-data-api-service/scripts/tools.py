from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def getNetworks(
) -> Dict[str, Any]:
    """
    REQUIRED FIRST STEP: Get all supported blockchain networks. Always call this first to see available networks before using any network-specific functions. Returns network IDs like "ethereum", "solana", etc.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659592195", "getNetworks", arguments)

def getNetworkDexes(
    network: str,
    page: Optional[float] = 0.0,
    limit: Optional[float] = 10.0,
    sort: Optional[str] = "desc",
    orderBy: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get available DEXes on a specific network. First call getNetworks to see valid network IDs.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        page: Page number for pagination
        limit: Number of items per page (max 100)
        sort: Sort order
        orderBy: How to order the returned data
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "page": page,
        "limit": limit,
        "sort": sort,
        "orderBy": orderBy
    }
    
    return call_api("1777316659592195", "getNetworkDexes", arguments)

def getNetworkPools(
    network: str,
    page: Optional[float] = 0.0,
    limit: Optional[float] = 10.0,
    sort: Optional[str] = "desc",
    orderBy: Optional[str] = "volume_usd"
) -> Dict[str, Any]:
    """
    PRIMARY POOL FUNCTION: Get top liquidity pools on a specific network. This is the MAIN way to get pool data - there is NO global pools function. Use this instead of any "getTopPools" or "getAllPools" concepts.
    
    Args:
        network: Network ID from getNetworks (required) - e.g., "ethereum", "solana"
        page: Page number for pagination
        limit: Number of items per page (max 100)
        sort: Sort order
        orderBy: Field to order by
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "page": page,
        "limit": limit,
        "sort": sort,
        "orderBy": orderBy
    }
    
    return call_api("1777316659592195", "getNetworkPools", arguments)

def getDexPools(
    network: str,
    dex: str,
    page: Optional[float] = 0.0,
    limit: Optional[float] = 10.0,
    sort: Optional[str] = "desc",
    orderBy: Optional[str] = "volume_usd"
) -> Dict[str, Any]:
    """
    Get pools from a specific DEX on a network. First use getNetworks, then getNetworkDexes to find valid DEX IDs.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        dex: DEX identifier from getNetworkDexes (e.g., "uniswap_v3")
        page: Page number for pagination
        limit: Number of items per page (max 100)
        sort: Sort order
        orderBy: Field to order by
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "dex": dex,
        "page": page,
        "limit": limit,
        "sort": sort,
        "orderBy": orderBy
    }
    
    return call_api("1777316659592195", "getDexPools", arguments)

def getPoolDetails(
    network: str,
    poolAddress: str,
    inversed: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get detailed information about a specific pool. Requires network ID from getNetworks and a pool address.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        poolAddress: Pool address or identifier
        inversed: Whether to invert the price ratio
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "poolAddress": poolAddress,
        "inversed": inversed
    }
    
    return call_api("1777316659592195", "getPoolDetails", arguments)

def getTokenDetails(
    network: str,
    tokenAddress: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific token on a network. First use getNetworks to get valid network IDs.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        tokenAddress: Token address or identifier
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "tokenAddress": tokenAddress
    }
    
    return call_api("1777316659592195", "getTokenDetails", arguments)

def getTokenPools(
    network: str,
    tokenAddress: str,
    page: Optional[float] = 0.0,
    limit: Optional[float] = 10.0,
    sort: Optional[str] = "desc",
    orderBy: Optional[str] = "volume_usd",
    reorder: Optional[bool] = None,
    address: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get liquidity pools containing a specific token on a network. Great for finding where a token is traded.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        tokenAddress: Token address or identifier
        page: Page number for pagination
        limit: Number of items per page (max 100)
        sort: Sort order
        orderBy: Field to order by
        reorder: If true, reorders the pool so that the specified token becomes the primary token for all metrics
        address: Filter pools that contain this additional token address
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "tokenAddress": tokenAddress,
        "page": page,
        "limit": limit,
        "sort": sort,
        "orderBy": orderBy,
        "reorder": reorder,
        "address": address
    }
    
    return call_api("1777316659592195", "getTokenPools", arguments)

def getPoolOHLCV(
    network: str,
    poolAddress: str,
    start: str,
    end: Optional[str] = None,
    limit: Optional[float] = 1.0,
    interval: Optional[str] = "24h",
    inversed: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get historical price data (OHLCV) for a pool - essential for price analysis, backtesting, and visualization. Requires network and pool address.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        poolAddress: Pool address or identifier
        start: Start time for historical data (Unix timestamp, RFC3339 timestamp, or yyyy-mm-dd format)
        end: End time for historical data (max 1 year from start)
        limit: Number of data points to retrieve (max 366) - adjust for different analysis needs
        interval: Interval granularity: 1m, 5m, 10m, 15m, 30m, 1h, 6h, 12h, 24h
        inversed: Whether to invert the price ratio for alternative pair perspective (e.g., ETH/USDC vs USDC/ETH)
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "poolAddress": poolAddress,
        "start": start,
        "end": end,
        "limit": limit,
        "interval": interval,
        "inversed": inversed
    }
    
    return call_api("1777316659592195", "getPoolOHLCV", arguments)

def getPoolTransactions(
    network: str,
    poolAddress: str,
    page: Optional[float] = 0.0,
    limit: Optional[float] = 10.0,
    cursor: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get recent transactions for a specific pool. Shows swaps, adds, removes. Requires network and pool address.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        poolAddress: Pool address or identifier
        page: Page number for pagination (up to 100 pages)
        limit: Number of items per page (max 100)
        cursor: Transaction ID used for cursor-based pagination
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "poolAddress": poolAddress,
        "page": page,
        "limit": limit,
        "cursor": cursor
    }
    
    return call_api("1777316659592195", "getPoolTransactions", arguments)

def search(
    query: str
) -> Dict[str, Any]:
    """
    Search across ALL networks for tokens, pools, and DEXes by name, symbol, or address. Good starting point when you don't know the specific network.
    
    Args:
        query: Search term (e.g., "uniswap", "bitcoin", or a token address)
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777316659592195", "search", arguments)

def getStats(
) -> Dict[str, Any]:
    """
    Get high-level statistics about the DexPaprika ecosystem: total networks, DEXes, pools, and tokens available.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659592195", "getStats", arguments)

def getTokenMultiPrices(
    network: str,
    tokens: null
) -> Dict[str, Any]:
    """
    Get batched prices for multiple tokens on a specific network. Pass an array of token addresses; unknown tokens are omitted.
    
    Args:
        network: Network ID from getNetworks (e.g., "ethereum", "solana")
        tokens: Array of token contract addresses. Serialized as repeatable query (?tokens=a&tokens=b).
    
    Returns:
        
    """
    arguments = {
        "network": network,
        "tokens": tokens
    }
    
    return call_api("1777316659592195", "getTokenMultiPrices", arguments)

