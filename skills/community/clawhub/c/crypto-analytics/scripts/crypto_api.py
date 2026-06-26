#!/usr/bin/env python3
"""
Crypto Analytics Core API Client - V2 (Etherscan Unified)

Provides unified interface to multiple blockchain data sources with:
- Rate limiting (respects API limits)
- Simple caching (TTL-based)
- Error handling and fallbacks
- Support for 60+ EVM chains via Etherscan V2
"""

import json
import time
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import requests
from decimal import Decimal
from address_validator import AddressValidator

# Optional: load .env from workspace root if python-dotenv is installed
try:
    from dotenv import load_dotenv
    # Find OpenClaw workspace root by looking for AGENTS.md or .git
    def find_workspace_root():
        p = Path(__file__).resolve()
        while p != p.parent:
            if (p / 'AGENTS.md').exists() or (p / '.git').exists():
                return p
            p = p.parent
        return Path(__file__).parent  # fallback
    workspace_root = find_workspace_root()
    env_path = workspace_root / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    # dotenv not installed – rely on system environment
    pass

# Cache directory (use workspace cache)
CACHE_DIR = Path.home() / ".openclaw" / "cache" / "crypto-analytics"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def hex_to_int(hex_str: Any, default: int = 0) -> int:
    """Convert hex string or decimal string to int"""
    if not hex_str:
        return default
    s = str(hex_str)
    if s.startswith('0x'):
        return int(s, 16)
    try:
        return int(s)
    except (ValueError, TypeError):
        return default

# Token registry: maps (chain, normalized_address) -> {symbol, name, decimals}
TOKEN_REGISTRY = {
    # Ethereum mainnet
    ('ethereum', '0xdac17f958d2ee523a2206206994597c13d831ec7'): {'symbol': 'USDT', 'name': 'Tether USD', 'decimals': 6},
    ('ethereum', '0xa0b86991c6218b36c1d19d4a2e9bb0e3606eb48'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 6},
    ('ethereum', '0x6b175474e89094c44da98b954eedeac495271d0f'): {'symbol': 'DAI', 'name': 'Dai Stablecoin', 'decimals': 18},
    ('ethereum', '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'): {'symbol': 'WBTC', 'name': 'Wrapped BTC', 'decimals': 8},
    ('ethereum', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'): {'symbol': 'WETH', 'name': 'Wrapped Ether', 'decimals': 18},
    # Binance Smart Chain
    ('bsc', '0x55d398326f99059ff775485246999027b3197955'): {'symbol': 'USDT', 'name': 'Tether USD', 'decimals': 18},
    ('bsc', '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 18},
    ('bsc', '0x1af3f329e8e9545dbb6f61136cb6f48a9037ca5c'): {'symbol': 'BUSD', 'name': 'Binance USD', 'decimals': 18},
    ('bsc', '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'): {'symbol': 'WBNB', 'name': 'Wrapped BNB', 'decimals': 18},
    # Polygon
    ('polygon', '0x2791bca1f2de4661ed88a30c99a7a9449aa84174'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 6},
    ('polygon', '0x0000000000000000000000000000000000001010'): {'symbol': 'WMATIC', 'name': 'Wrapped MATIC', 'decimals': 18},
    # Arbitrum (placeholder)
    ('arbitrum', '0xfd086dc7f083cbef6e1e5bae0f0b8e5d1f4c4c4c'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 6},
    # Optimism
    ('optimism', '0x7f5c764cbc14f9669b88837ca1490cca17c31607'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 6},
    # Base
    ('base', '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 6},
    # Avalanche
    ('avalanche', '0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e'): {'symbol': 'USDC', 'name': 'USD Coin', 'decimals': 6},
}

class APIRateLimitError(Exception):
    """Raised when API rate limit is exceeded"""
    pass

class CacheManager:
    """Simple TTL cache for API responses"""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.cache_dir = CACHE_DIR / "api_responses"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, provider: str, method: str, params: Dict) -> str:
        """Generate deterministic cache key"""
        raw = f"{provider}:{method}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, provider: str, method: str, params: Dict) -> Optional[Dict]:
        key = self._cache_key(provider, method, params)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                if data['expires_at'] > time.time():
                    return data['response']
                else:
                    cache_file.unlink(missing_ok=True)
            except Exception:
                pass
        return None

    def set(self, provider: str, method: str, params: Dict, response: Dict, ttl: Optional[int] = None):
        key = self._cache_key(provider, method, params)
        cache_file = self.cache_dir / f"{key}.json"

        data = {
            'provider': provider,
            'method': method,
            'params': params,
            'response': response,
            'created_at': time.time(),
            'expires_at': time.time() + (ttl or self.ttl)
        }
        cache_file.write_text(json.dumps(data, indent=2))

class EtherscanV2API:
    """Etherscan V2 - Unified API for 60+ chains"""

    BASE_URL = "https://api.etherscan.io/v2/api"
    # Rate limits depend on API key tier, but free: 5 calls/sec

    # Chain ID mapping
    CHAINS = {
        'ethereum': 1,
        'sepolia': 11155111,  # Ethereum testnet
        'bsc': 56,
        'polygon': 137,
        'arbitrum': 42161,
        'base': 8453,
        'optimism': 10,
        'avalanche': 43114,
        'gnosis': 100,
        'fantom': 250,
        'linea': 59144,
        'scroll': 534352,
        'zksync': 324,
        'mantle': 5000,
        'cronos': 25,
        'kcc': 321,
        'metis': 1088,
        'harmony': 1666600000,
        'iotex': 4689,
        'okc': 66,
        'tron': 0,  # Not EVM, separate system
    }

    def get_gas_price(self, chain: str = 'ethereum') -> Dict:
        """Get current gas price (using eth_gasPrice)"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}'}

        resp = self._get(chainid, 'proxy', 'eth_gasPrice', {})
        if resp.get('result'):
            gas_wei = hex_to_int(resp['result'])
            return {
                'chain': chain,
                'chainid': chainid,
                'gas_price_wei': gas_wei,
                'gas_price_gwei': gas_wei / 1e9
            }
        return {'error': 'Failed to fetch gas price', 'details': resp}

    def get_token_metadata(self, contract: str, chain: str) -> Dict:
        """Get token metadata (symbol, name, decimals) from registry or by contract calls."""
        chain_key = chain.lower()
        contract_norm = AddressValidator.normalize(contract, chain_key)
        key = (chain_key, contract_norm.lower())
        if key in TOKEN_REGISTRY:
            return TOKEN_REGISTRY[key]

        # Not in registry, try to fetch via contract calls
        try:
            # Fetch decimals (0x313ce567)
            resp = self._get(self.CHAINS[chain_key], 'proxy', 'eth_call', {
                'to': contract_norm,
                'data': '0x313ce567',
                'tag': 'latest'
            })
            result_hex = resp.get('result', '0x')
            decimals = hex_to_int(result_hex, default=18)

            # Fetch symbol (0x95d89b41)
            resp = self._get(self.CHAINS[chain_key], 'proxy', 'eth_call', {
                'to': contract_norm,
                'data': '0x95d89b41',
                'tag': 'latest'
            })
            symbol = '???'
            if resp.get('result'):
                raw = resp['result'][2:]  # remove 0x
                try:
                    symbol_bytes = bytes.fromhex(raw)
                    symbol_bytes = symbol_bytes.rstrip(b'\x00')
                    symbol = symbol_bytes.decode('ascii')
                except Exception:
                    symbol = '???'

            metadata = {
                'symbol': symbol,
                'name': '',
                'decimals': decimals
            }
            TOKEN_REGISTRY[key] = metadata
            return metadata
        except Exception:
            return {
                'symbol': contract_norm[:6] + '...',
                'name': '',
                'decimals': 18
            }

    def get_token_balance(self, address: str, token_contract: str, chain: str = 'ethereum') -> Dict:
        """Get ERC-20 token balance for a specific token contract"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}'}

        # Use token's balanceOf method via eth_call
        # balanceOf(address) => returns uint256
        # Data: 0x70a08231000000000000000000000000 + address (32 bytes left-padded)
        token_addr = AddressValidator.normalize(token_contract, chain)
        owner_addr = AddressValidator.normalize(address, chain)

        data = '0x70a08231' + owner_addr[2:].zfill(64)

        resp = self._get(chainid, 'proxy', 'eth_call', {
            'to': token_addr,
            'data': data,
            'tag': 'latest'
        })

        if resp.get('result'):
            balance = hex_to_int(resp['result'])
            metadata = self.get_token_metadata(token_contract, chain)
            return {
                'chain': chain,
                'contract': token_addr,
                'owner': owner_addr,
                'balance': balance,
                'symbol': metadata.get('symbol', '???'),
                'name': metadata.get('name', ''),
                'decimals': metadata.get('decimals', 18)
            }
        return {'error': 'Failed to fetch token balance', 'details': resp}

    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = 300):
        self.api_key = api_key or os.getenv('ETHERSCAN_API_KEY')
        self.cache = CacheManager(ttl_seconds=cache_ttl)
        self._last_call = 0
        self.rate_delay = 0.2  # 5 calls/sec

    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self._last_call
        if elapsed < self.rate_delay:
            time.sleep(self.rate_delay - elapsed)
        self._last_call = time.time()

    def _get(self, chainid: int, module: str, action: str, params: Dict = None) -> Dict:
        """Generic GET request to Etherscan V2"""
        cache_key = {'chainid': chainid, 'module': module, 'action': action, **(params or {})}
        cached = self.cache.get('etherscan_v2', f"{chainid}/{module}/{action}", cache_key)
        if cached:
            return cached

        self._rate_limit()

        query = {
            'chainid': chainid,
            'module': module,
            'action': action,
            **(params or {})
        }
        if self.api_key:
            query['apikey'] = self.api_key

        try:
            resp = requests.get(self.BASE_URL, params=query, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # V2 response format: {"status":"1","message":"OK","result":{...}}
            if data.get('status') == '0' and 'rate limit' in data.get('message', '').lower():
                raise APIRateLimitError("Etherscan rate limit exceeded")

            result = {
                'status': data.get('status'),
                'message': data.get('message'),
                'result': data.get('result')
            }
            self.cache.set('etherscan_v2', f"{chainid}/{module}/{action}", cache_key, result)
            return result

        except requests.RequestException as e:
            # Parse HTTP 500/503 - common with V2 if key not enabled or endpoint issue
            error_msg = f"Etherscan V2 error: {e}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    err_detail = e.response.json()
                    error_msg = f"API Error: {err_detail.get('message', str(e))}"
                except:
                    error_msg = f"HTTP {e.response.status_code}: {e.response.text[:100]}"
            return {'error': error_msg, 'status': '-1', 'result': None}

    def get_balance(self, address: str, chain: str = 'ethereum') -> Dict:
        """Get native token balance (wei for EVM chains)"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}. Use one of: {list(self.CHAINS.keys())}'}

        resp = self._get(chainid, 'account', 'balance', {
            'address': address,
            'tag': 'latest'
        })
        if resp.get('result'):
            return {
                'chain': chain,
                'chainid': chainid,
                'address': address,
                'balance_wei': int(resp['result']),
                'balance_native': int(resp['result']) / 10**18
            }
        return {'error': 'Failed to fetch balance', 'details': resp}

    def get_transactions(self, address: str, chain: str = 'ethereum', startblock: int = 0, endblock: int = 99999999) -> Dict:
        """Get normal transactions"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}'}

        resp = self._get(chainid, 'account', 'txlist', {
            'address': address,
            'startblock': startblock,
            'endblock': endblock,
            'sort': 'desc'
        })
        return {
            'chain': chain,
            'chainid': chainid,
            'address': address,
            'result': resp.get('result', [])  # flatten to the actual list
        }

    def get_token_transfers(self, address: str, chain: str = 'ethereum') -> Dict:
        """Get ERC-20 token transfers"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}'}

        resp = self._get(chainid, 'account', 'tokentx', {
            'address': address,
            'sort': 'desc'
        })
        return {
            'chain': chain,
            'chainid': chainid,
            'address': address,
            'result': resp
        }

    def get_transaction(self, txhash: str, chain: str = 'ethereum') -> Dict:
        """Get transaction details"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}'}

        resp = self._get(chainid, 'proxy', 'eth_getTransactionByHash', {
            'txhash': txhash
        })
        return {
            'chain': chain,
            'chainid': chainid,
            'txhash': txhash,
            'result': resp
        }

    def get_block(self, block_param: str = 'latest', chain: str = 'ethereum') -> Dict:
        """Get block information"""
        chainid = self.CHAINS.get(chain)
        if not chainid:
            return {'error': f'Unsupported chain: {chain}'}

        resp = self._get(chainid, 'proxy', 'eth_getBlockByNumber', {
            'tag': block_param,
            'boolean': 'false'
        })
        return {
            'chain': chain,
            'chainid': chainid,
            'result': resp
        }

    def list_supported_chains(self) -> List[Dict]:
        """Return all supported chains"""
        return [
            {'id': name, 'chainid': cid, 'type': 'EVM'}
            for name, cid in self.CHAINS.items()
        ]

class BlockchairAPI:
    """Multi-chain blockchain data via Blockchair API"""

    BASE_URL = "https://api.blockchair.com"
    # Free tier: 100 req/min, 4k/day

    def __init__(self, cache_ttl: int = 300):
        self.cache = CacheManager(ttl_seconds=cache_ttl)
        self._last_call = 0
        self.rate_delay = 0.6  # ~100/min

    def _rate_limit(self):
        elapsed = time.time() - self._last_call
        if elapsed < self.rate_delay:
            time.sleep(self.rate_delay - elapsed)
        self._last_call = time.time()

    def _get(self, chain: str, endpoint: str, params: Dict = None) -> Dict:
        cache_key = {'chain': chain, 'endpoint': endpoint, **(params or {})}
        cached = self.cache.get('blockchair', f"{chain}/{endpoint}", cache_key)
        if cached:
            return cached

        self._rate_limit()

        try:
            url = f"{self.BASE_URL}/{chain}/{endpoint}"
            resp = requests.get(url, params=params or {}, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            result = data.get('data', {})
            self.cache.set('blockchair', f"{chain}/{endpoint}", cache_key, result)
            return result

        except requests.RequestException as e:
            return {'error': str(e)}

    def get_address(self, address: str, chain: str = 'bitcoin') -> Dict:
        """Get address overview"""
        return self._get(chain, 'address', {'address': address})

    def get_transactions(self, address: str, chain: str = 'bitcoin', limit: int = 50) -> Dict:
        """Get recent transactions"""
        return self._get(chain, 'transactions', {
            'address': address,
            'limit': limit,
            'sort': 'desc(block_time)'
        })

    def get_transaction(self, txhash: str, chain: str = 'bitcoin') -> Dict:
        """Get transaction details"""
        return self._get(chain, 'raw/transaction', {'hash': txhash})

class SolanaRPC:
    """Solana blockchain via public RPC"""

    ENDPOINTS = [
        "https://api.mainnet-beta.solana.com",
        "https://solana-api.project-serum.com",
    ]
    RATE_DELAY = 0.5

    def __init__(self, cache_ttl: int = 300):
        self.cache = CacheManager(ttl_seconds=cache_ttl)
        self._endpoint_idx = 0
        self._last_call = 0

    @property
    def endpoint(self) -> str:
        return self.ENDPOINTS[self._endpoint_idx]

    def _rate_limit(self):
        elapsed = time.time() - self._last_call
        if elapsed < self.RATE_DELAY:
            time.sleep(self.RATE_DELAY - elapsed)
        self._last_call = time.time()

    def _post(self, method: str, params: List) -> Dict:
        cache_key = {'method': method, 'params': params}
        cached = self.cache.get('solana', method, cache_key)
        if cached:
            return cached

        self._rate_limit()

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }

        try:
            resp = requests.post(self.endpoint, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            result = data.get('result', {})
            self.cache.set('solana', method, cache_key, result)
            return result

        except requests.RequestException as e:
            # On failure, try next endpoint
            self._endpoint_idx = (self._endpoint_idx + 1) % len(self.ENDPOINTS)
            return {'error': str(e), 'result': None}

    def get_account_info(self, address: str) -> Dict:
        resp = self._post('getAccountInfo', [address, {'encoding': 'json'}])
        return resp

    def get_token_accounts(self, owner: str) -> Dict:
        resp = self._post('getTokenAccountsByOwner', [
            owner,
            {'programId': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'},
            {'encoding': 'jsonParsed'}
        ])
        # Process response to extract balances
        if 'value' in resp:
            tokens = []
            for account in resp['value']:
                parsed = account.get('account', {}).get('data', {}).get('parsed', {})
                if parsed:
                    info = parsed.get('info', {})
                    token_amount = info.get('tokenAmount', {})
                    decimals = token_amount.get('decimals', 0)
                    amount = token_amount.get('uiAmount', 0)
                    mint = info.get('mint', '')
                    tokens.append({
                        'mint': mint,
                        'amount': amount,
                        'decimals': decimals,
                        'raw_amount': token_amount.get('amount', 0)
                    })
            resp['tokens'] = tokens
        return resp

    def get_transactions(self, address: str, limit: int = 10) -> Dict:
        return {'error': 'Solana transaction history requires specialized indexing (use Solscan API)'}

class CryptoAPIClient:
    """Unified interface for blockchain data"""

    def __init__(self):
        self.etherscan = EtherscanV2API()
        self.blockchair = BlockchairAPI()
        self.solana = SolanaRPC()

    # Chain ID constants (common chains)
    CHAIN_IDS = {
        'ethereum': 1,
        'sepolia': 11155111,
        'bsc': 56,
        'polygon': 137,
        'arbitrum': 42161,
        'base': 8453,
        'optimism': 10,
        'avalanche': 43114,
    }

    def detect_chain(self, address: str) -> str:
        """Auto-detect blockchain from address format"""
        addr = address.lower().strip()

        # EVM chains (0x...)
        if addr.startswith('0x') and len(addr) == 42:
            # Could be any EVM chain. Default to ethereum for now.
            # In production, could try to guess from known address patterns
            return 'ethereum'

        # Bitcoin
        if addr.startswith(('1', '3', 'bc1')):
            return 'bitcoin'

        # Solana
        import re
        if re.fullmatch(r'[1-9A-HJ-NP-Za-km-z]{32,44}', addr):
            return 'solana'

        return 'unknown'

    def get_wallet_balance(self, address: str, chain: Optional[str] = None) -> Dict:
        """Get wallet native token balance"""
        chain = chain or self.detect_chain(address)

        # EVM chains use Etherscan V2
        if chain in self.CHAIN_IDS:
            resp = self.etherscan.get_balance(address, chain)
            result = resp
            if 'error' not in resp and 'balance_native' in resp:
                result['formatted_balance'] = f"{resp['balance_native']:.6f} {chain.upper()}"
                result['symbol'] = self._get_native_symbol(chain)
            return result

        elif chain == 'bitcoin':
            resp = self.blockchair.get_address(address, chain='bitcoin')
            if 'balance' in resp:
                sats = int(resp['balance'])
                return {
                    'chain': 'bitcoin',
                    'address': address,
                    'balance_sats': sats,
                    'balance_btc': sats / 10**8,
                    'formatted_balance': f"{sats / 10**8:.8f} BTC",
                    'transaction_count': resp.get('transaction_count', 0)
                }
            return {'error': 'Failed to fetch Bitcoin balance'}

        elif chain == 'solana':
            resp = self.solana.get_account_info(address)
            if 'lamports' in resp:
                return {
                    'chain': 'solana',
                    'address': address,
                    'balance_lamports': resp['lamports'],
                    'balance_sol': resp['lamports'] / 10**9,
                    'formatted_balance': f"{resp['lamports'] / 10**9:.6f} SOL"
                }
            return {'error': 'Failed to fetch Solana balance'}

        return {'error': f'Unsupported chain: {chain}'}

    def get_transactions(self, address: str, chain: Optional[str] = None, limit: int = 50) -> Dict:
        """Get recent transactions"""
        chain = chain or self.detect_chain(address)

        if chain in self.CHAIN_IDS:
            resp = self.etherscan.get_transactions(address, chain)
            result_data = resp.get('result', {})
            txs = result_data if isinstance(result_data, list) else []
            return {
                'chain': chain,
                'chainid': self.CHAIN_IDS[chain],
                'address': address,
                'count': len(txs),
                'transactions': txs[:limit]
            }

        elif chain == 'bitcoin':
            resp = self.blockchair.get_transactions(address, chain='bitcoin', limit=limit)
            txs = resp.get('transactions', [])
            return {
                'chain': 'bitcoin',
                'address': address,
                'count': len(txs),
                'transactions': txs
            }

        elif chain == 'solana':
            return {'error': 'Solana transaction history requires specialized indexing'}

        return {'error': f'Unsupported chain: {chain}'}

    def get_transaction_details(self, txhash: str, chain: str) -> Dict:
        """Get transaction details"""
        if chain in self.CHAIN_IDS:
            resp = self.etherscan.get_transaction(txhash, chain)
            return {
                'chain': chain,
                'chainid': self.CHAIN_IDS[chain],
                'txhash': txhash,
                'transaction': resp.get('result', {})
            }

        elif chain == 'bitcoin':
            resp = self.blockchair.get_transaction(txhash, chain='bitcoin')
            return {
                'chain': 'bitcoin',
                'txhash': txhash,
                'transaction': resp
            }

        elif chain == 'solana':
            return {'error': 'Solana transaction details require specialized RPC'}

        return {'error': f'Unsupported chain: {chain}'}

    def get_gas_price(self, chain: str = 'ethereum') -> Dict:
        """Get current gas price"""
        return self.etherscan.get_gas_price(chain)

    def get_token_balance(self, address: str, token_contract: str, chain: str = 'ethereum') -> Dict:
        """Get ERC-20 token balance for a specific token"""
        return self.etherscan.get_token_balance(address, token_contract, chain)

    def get_spl_tokens(self, owner: str) -> Dict:
        """Get SPL token accounts for Solana wallet"""
        resp = self.solana.get_token_accounts(owner)
        return {
            'owner': owner,
            'tokens': resp.get('tokens', [])
        }

    def get_token_transfers(self, address: str, chain: str, token_contract: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
        """Get ERC-20 token transfer history for an address. Optionally filter by token contract."""
        if chain not in self.CHAIN_IDS:
            return {'error': f'Unsupported chain: {chain}'}

        # Use Etherscan V2 tokentx action
        params = {
            'address': address,
            'sort': 'desc'
        }
        resp = self.etherscan._get(self.CHAIN_IDS[chain], 'account', 'tokentx', params)
        if 'error' in resp or 'result' not in resp:
            return {'error': 'Failed to fetch token transfers', 'details': resp}

        txs = resp['result']
        # Filter by token contract if specified
        if token_contract:
            norm_token = AddressValidator.normalize(token_contract, chain)
            filtered = [tx for tx in txs if AddressValidator.normalize(tx.get('contractAddress', ''), chain) == norm_token]
            txs = filtered

        return {
            'chain': chain,
            'address': address,
            'count': len(txs),
            'transfers': txs[:limit]
        }

    def get_wallet_tokens(self, address: str, chain: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
        """Get all ERC-20 token balances for a wallet by discovering used tokens from transfer history."""
        chain = chain or self.detect_chain(address)
        if chain not in self.CHAIN_IDS:
            return {'error': f'Unsupported chain: {chain}'}

        # Get token transfer history to discover token contracts
        transfers_resp = self.etherscan.get_token_transfers(address, chain)
        if 'error' in transfers_resp:
            return transfers_resp

        raw_response = transfers_resp.get('result', {})
        # Handle possible errors or empty results
        if 'error' in raw_response or 'result' not in raw_response:
            tx_list = []
        else:
            tx_list = raw_response['result']

        # Build token metadata map: contract -> {symbol, name, decimals}
        token_info = {}
        for tx in tx_list:
            contract = tx.get('contractAddress')
            if not contract:
                continue
            norm_contract = AddressValidator.normalize(contract, chain)
            symbol = tx.get('tokenSymbol', '???')
            name = tx.get('tokenName', '')
            decimals_str = tx.get('tokenDecimal', '18')
            try:
                decimals = int(decimals_str)
            except (ValueError, TypeError):
                decimals = 18
            token_info[norm_contract] = {
                'symbol': symbol,
                'name': name,
                'decimals': decimals
            }

        # Deduplicate and limit contracts to query
        unique_contracts = list(token_info.keys())[:limit]
        tokens = []
        for contract in unique_contracts:
            bal_res = self.etherscan.get_token_balance(address, contract, chain)
            if 'error' in bal_res:
                continue
            raw_balance = bal_res.get('balance', 0)
            if raw_balance and raw_balance > 0:
                # Use metadata from token_info (more reliable from transfers)
                info = token_info[contract]
                tokens.append({
                    'contract': contract,
                    'balance': raw_balance,
                    'symbol': info['symbol'],
                    'name': info['name'],
                    'decimals': info['decimals']
                })

        return {
            'chain': chain,
            'address': address,
            'tokens': tokens,
            'count': len(tokens)
        }

    def _get_native_symbol(self, chain: str) -> str:
        """Return native token symbol for chain"""
        symbols = {
            'ethereum': 'ETH',
            'sepolia': 'ETH',
            'bsc': 'BNB',
            'polygon': 'MATIC',
            'arbitrum': 'ETH',
            'base': 'ETH',
            'optimism': 'ETH',
            'avalanche': 'AVAX',
        }
        return symbols.get(chain, '???')

if __name__ == '__main__':
    import sys
    client = CryptoAPIClient()

    if len(sys.argv) < 3:
        print("Usage: crypto_api.py <command> <address/txhash> [chain]")
        sys.exit(1)

    cmd = sys.argv[1]
    target = sys.argv[2]
    chain = sys.argv[3] if len(sys.argv) > 3 else None

    if cmd == 'balance':
        result = client.get_wallet_balance(target, chain)
        print(json.dumps(result, indent=2))

    elif cmd == 'txs':
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 50
        result = client.get_transactions(target, chain, limit)
        print(json.dumps(result, indent=2))

    elif cmd == 'tx':
        if not chain:
            print("Chain required for transaction lookup")
            sys.exit(1)
        result = client.get_transaction_details(target, chain)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
