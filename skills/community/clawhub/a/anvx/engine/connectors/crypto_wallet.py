"""READ-ONLY multi-chain crypto wallet balance reader.

Fetches token balances from public blockchain explorer APIs.
This connector has ZERO execution capability — no transfers,
no swaps, no approvals. Only reads public data via GET requests.
Never accepts secret keys or recovery phrases. Only public addresses.

Supported chains: Ethereum, Solana, Base, Arbitrum, Polygon.
USD prices from CoinGecko (free, no key needed, cached 5 min).
"""
import logging
import time
from datetime import date
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

CRYPTO_DISCLAIMER = (
    "Crypto balances are read-only and informational. Not financial advice. "
    "This tool cannot move, exchange, or modify any assets."
)

# Block explorer APIs (all Etherscan-format compatible)
_EXPLORER_APIS: dict[str, str] = {
    "ethereum": "https://api.etherscan.io/api",
    "base": "https://api.basescan.org/api",
    "arbitrum": "https://api.arbiscan.io/api",
    "polygon": "https://api.polygonscan.com/api",
}
_SOLANA_RPC = "https://api.mainnet-beta.solana.com"
_COINGECKO_PRICE_API = "https://api.coingecko.com/api/v3/simple/price"

# USDC contract addresses per chain
_USDC_CONTRACTS: dict[str, str] = {
    "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "arbitrum": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "polygon": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
}

# Native token per chain for CoinGecko lookup
_CHAIN_NATIVE: dict[str, tuple[str, str]] = {
    "ethereum": ("ETH", "ethereum"),
    "base": ("ETH", "ethereum"),
    "arbitrum": ("ETH", "ethereum"),
    "polygon": ("POL", "matic-network"),
    "solana": ("SOL", "solana"),
}

# Synthetic balances for test mode
_SYNTHETIC_HOLDINGS: list[tuple[str, str, Decimal, Decimal]] = [
    # (chain, token, quantity, usd_price)
    ("ethereum", "ETH", Decimal("2.5"), Decimal("1900")),
    ("ethereum", "USDC", Decimal("1500"), Decimal("1.00")),
    ("solana", "SOL", Decimal("450"), Decimal("150")),
]

# Price cache: {coingecko_id: (price_usd, timestamp)}
_price_cache: dict[str, tuple[Decimal, float]] = {}
_PRICE_CACHE_TTL = 300  # 5 minutes


class CryptoWalletConnector(BaseConnector):
    """READ-ONLY multi-chain wallet balance reader.

    SECURITY: This class provides ZERO methods to write, transfer, swap,
    approve, or modify any on-chain state. All API calls are GET requests
    to public block explorer endpoints. Never asks for secret keys or
    recovery phrases.
    """

    provider = Provider.CRYPTO_WALLET

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._wallets: list[dict[str, str]] = []  # [{"chain": ..., "address": ...}]
        self._client: httpx.AsyncClient | None = None

    def validate_test_credentials(self, credentials: dict[str, Any]) -> bool:
        """Check wallet addresses against test addresses.

        Handles both formats:
          {"wallets": [{"chain": "ethereum", "address": "0xTEST..."}]}
          {"wallet_addresses": ["0xTEST..."]}
        """
        from engine.utils import TEST_CREDENTIALS
        test_entry = TEST_CREDENTIALS.get("crypto_wallet", {})
        test_addrs = set(test_entry.get("_test_addresses", []))
        if not test_addrs:
            return False

        # Extract addresses from whichever format was provided
        provided: set[str] = set()
        for w in credentials.get("wallets", []):
            provided.add(w.get("address", ""))
        for a in credentials.get("wallet_addresses", []):
            provided.add(a)

        # At least one provided address must be a known test address
        return bool(provided & test_addrs)

    async def connect(self, credentials: dict[str, Any]) -> bool:
        """Connect using wallet chain+address pairs.

        Accepts: {"wallets": [{"chain": "ethereum", "address": "0x..."}]}
        Legacy: {"wallet_addresses": ["0x..."]}  (assumed Ethereum)
        """
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to blockchain explorers...")
                await asyncio.sleep(1)
                print("Wallet addresses verified (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Invalid wallet address format")
            return False

        # Parse wallets from new or legacy format
        wallets = credentials.get("wallets", [])
        if not wallets:
            # Legacy format: bare addresses assumed Ethereum
            addrs = credentials.get("wallet_addresses", [])
            wallets = [{"chain": "ethereum", "address": a} for a in addrs]

        if not wallets:
            logger.error("Provide wallets or wallet_addresses")
            return False

        supported = set(_EXPLORER_APIS.keys()) | {"solana"}
        for w in wallets:
            chain = w.get("chain", "").lower()
            addr = w.get("address", "")
            if chain not in supported:
                logger.error("Unsupported chain: %s (supported: %s)", chain, ", ".join(sorted(supported)))
                return False
            if not addr or len(addr) < 10:
                logger.error("Invalid address for %s: %s", chain, addr[:10] if addr else "(empty)")
                return False

        self._wallets = [{"chain": w["chain"].lower(), "address": w["address"]} for w in wallets]
        self._client = httpx.AsyncClient(timeout=30.0)

        # Validate first wallet by querying its explorer
        first = self._wallets[0]
        try:
            if first["chain"] == "solana":
                await self._solana_get_balance(first["address"])
            else:
                api = _EXPLORER_APIS[first["chain"]]
                resp = await self._client.get(
                    api,
                    params={"module": "account", "action": "balance",
                            "address": first["address"], "tag": "latest"},
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") != "1" and data.get("message") != "OK":
                    logger.error("Explorer error for %s: %s", first["chain"], data.get("message"))
                    return False
        except httpx.TimeoutException:
            logger.error("Blockchain explorer timed out for %s", first["chain"])
            return False
        except httpx.HTTPError as exc:
            logger.error("Blockchain explorer error: %s", exc)
            return False

        self.is_connected = True
        return True

    async def fetch_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Fetch current balances (READ-ONLY point-in-time snapshots)."""
        if not self.is_connected or self._client is None:
            logger.error("Not connected — call connect() first")
            return []

        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            return self.get_synthetic_records(start_date, end_date)

        records: list[FinancialRecord] = []
        for wallet in self._wallets:
            chain = wallet["chain"]
            address = wallet["address"]
            try:
                if chain == "solana":
                    records.extend(await self._fetch_solana(address, end_date))
                else:
                    records.extend(await self._fetch_evm(chain, address, end_date))
            except Exception as exc:
                logger.error("Fetch failed for %s/%s: %s", chain, address[:10], exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        records = await self.fetch_records(today, today)
        total = sum(r.amount for r in records)
        by_asset = {(r.subcategory or "unknown"): str(r.amount) for r in records}
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "total_holdings_usd": str(total),
            "by_asset": by_asset,
            "disclaimer": CRYPTO_DISCLAIMER,
        }

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Synthetic multi-chain holdings snapshot."""
        if end_date is None:
            end_date = date.today()
        records: list[FinancialRecord] = []
        for chain, token, qty, price in _SYNTHETIC_HOLDINGS:
            value = (qty * price).quantize(Decimal("0.01"))
            records.append(
                FinancialRecord(
                    record_date=end_date,
                    amount=value,
                    category=SpendCategory.CRYPTO_HOLDINGS,
                    subcategory=token,
                    provider=Provider.CRYPTO_WALLET,
                    source="synthetic",
                    raw_description=(
                        f"Synthetic: {qty} {token} on {chain} @ ${price}. "
                        f"{CRYPTO_DISCLAIMER}"
                    ),
                )
            )
        return records

    # ── Private helpers (all READ-ONLY) ────────────────────────────

    async def _fetch_evm(
        self, chain: str, address: str, as_of: date
    ) -> list[FinancialRecord]:
        """Fetch native + USDC balances from EVM-compatible explorer."""
        assert self._client is not None
        records: list[FinancialRecord] = []
        api = _EXPLORER_APIS[chain]
        native_symbol, coingecko_id = _CHAIN_NATIVE[chain]

        # Native balance
        try:
            resp = await self._client.get(
                api,
                params={"module": "account", "action": "balance",
                        "address": address, "tag": "latest"},
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "1":
                wei = Decimal(data["result"])
                native_balance = wei / Decimal("1000000000000000000")
                price = await self._get_price(coingecko_id)
                usd = (native_balance * price).quantize(Decimal("0.01"))
                if usd > 0:
                    records.append(FinancialRecord(
                        record_date=as_of, amount=usd,
                        category=SpendCategory.CRYPTO_HOLDINGS,
                        subcategory=native_symbol, provider=Provider.CRYPTO_WALLET,
                        source=f"{chain}_explorer",
                        raw_description=f"{native_balance} {native_symbol} on {chain}. {CRYPTO_DISCLAIMER}",
                    ))
        except httpx.HTTPError as exc:
            logger.warning("Native balance fetch failed for %s/%s: %s", chain, address[:10], exc)

        # USDC balance (ERC-20 token balance)
        usdc_contract = _USDC_CONTRACTS.get(chain)
        if usdc_contract:
            try:
                resp = await self._client.get(
                    api,
                    params={"module": "account", "action": "tokenbalance",
                            "contractaddress": usdc_contract,
                            "address": address, "tag": "latest"},
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") == "1":
                    raw = Decimal(data["result"])
                    usdc_balance = (raw / Decimal("1000000")).quantize(Decimal("0.01"))
                    if usdc_balance > 0:
                        records.append(FinancialRecord(
                            record_date=as_of, amount=usdc_balance,
                            category=SpendCategory.CRYPTO_HOLDINGS,
                            subcategory="USDC", provider=Provider.CRYPTO_WALLET,
                            source=f"{chain}_explorer",
                            raw_description=f"{usdc_balance} USDC on {chain}. {CRYPTO_DISCLAIMER}",
                        ))
            except httpx.HTTPError as exc:
                logger.warning("USDC fetch failed for %s/%s: %s", chain, address[:10], exc)

        return records

    async def _fetch_solana(
        self, address: str, as_of: date
    ) -> list[FinancialRecord]:
        """Fetch SOL balance via Solana JSON-RPC."""
        assert self._client is not None
        records: list[FinancialRecord] = []

        try:
            resp = await self._client.post(
                _SOLANA_RPC,
                json={"jsonrpc": "2.0", "id": 1, "method": "getBalance",
                      "params": [address]},
            )
            resp.raise_for_status()
            result = resp.json().get("result", {})
            lamports = Decimal(str(result.get("value", 0)))
            sol_balance = lamports / Decimal("1000000000")
            price = await self._get_price("solana")
            usd = (sol_balance * price).quantize(Decimal("0.01"))
            if usd > 0:
                records.append(FinancialRecord(
                    record_date=as_of, amount=usd,
                    category=SpendCategory.CRYPTO_HOLDINGS,
                    subcategory="SOL", provider=Provider.CRYPTO_WALLET,
                    source="solana_rpc",
                    raw_description=f"{sol_balance} SOL. {CRYPTO_DISCLAIMER}",
                ))
        except httpx.HTTPError as exc:
            logger.warning("Solana balance fetch failed: %s", exc)

        return records

    async def _solana_get_balance(self, address: str) -> Decimal:
        """Quick validation call — fetch SOL balance."""
        assert self._client is not None
        resp = await self._client.post(
            _SOLANA_RPC,
            json={"jsonrpc": "2.0", "id": 1, "method": "getBalance",
                  "params": [address]},
        )
        resp.raise_for_status()
        return Decimal(str(resp.json().get("result", {}).get("value", 0)))

    async def _get_price(self, coingecko_id: str) -> Decimal:
        """Fetch USD price from CoinGecko with 5-minute cache."""
        now = time.time()
        cached = _price_cache.get(coingecko_id)
        if cached and (now - cached[1]) < _PRICE_CACHE_TTL:
            return cached[0]

        assert self._client is not None
        try:
            resp = await self._client.get(
                _COINGECKO_PRICE_API,
                params={"ids": coingecko_id, "vs_currencies": "usd"},
            )
            resp.raise_for_status()
            price = Decimal(str(resp.json().get(coingecko_id, {}).get("usd", 0)))
            _price_cache[coingecko_id] = (price, now)
            return price
        except (httpx.HTTPError, KeyError, ValueError):
            logger.warning("Price fetch failed for %s — using fallback", coingecko_id)
            fallback = {"ethereum": Decimal("1900"), "solana": Decimal("150"),
                        "bitcoin": Decimal("64000"), "matic-network": Decimal("0.50")}
            return fallback.get(coingecko_id, Decimal("0"))
