"""Real-time LLM pricing fetcher with caching.

Primary source: OpenRouter API (no auth required).
Fallback source: LiteLLM pricing database on GitHub.
Cache: ~/.token-economy-intel/pricing_cache.json (24-hour TTL).
"""
import json
import logging
import time
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_CACHE_DIR = Path.home() / ".token-economy-intel"
_CACHE_FILE = _CACHE_DIR / "pricing_cache.json"
_CACHE_TTL_SECONDS = 86400  # 24 hours

_OPENROUTER_URL = "https://openrouter.ai/api/v1/models"
_LITELLM_URL = (
    "https://raw.githubusercontent.com/BerriAI/litellm/main/"
    "model_prices_and_context_window.json"
)

# Published cached-token discount rates (verifiable from provider docs)
CACHED_TOKEN_DISCOUNTS: dict[str, Decimal] = {
    "anthropic": Decimal("0.10"),  # 90% discount — cached tokens cost 10% of input
    "openai": Decimal("0.50"),     # 50% discount — automatic caching at half price
}

# Tier thresholds (per million input tokens)
# Flagship: gpt-4o ($2.50), claude-sonnet ($3), gemini-pro, etc.
# Mid-tier: gpt-4o-mini ($0.15), claude-haiku ($0.25), gemini-flash, etc.
# Efficient: very cheap/free models
_FLAGSHIP_THRESHOLD = Decimal("2.00")
_MIDTIER_THRESHOLD = Decimal("0.10")


def _classify_tier(input_per_million: Decimal) -> str:
    """Classify a model into a pricing tier."""
    if input_per_million >= _FLAGSHIP_THRESHOLD:
        return "flagship"
    if input_per_million >= _MIDTIER_THRESHOLD:
        return "mid-tier"
    return "efficient"


# Synthetic / offline fallback pricing for models used in synthetic data
_SYNTHETIC_PRICING: dict[str, dict[str, Any]] = {
    "gpt-4o": {
        "input_per_million": Decimal("2.50"),
        "output_per_million": Decimal("10.00"),
        "context_window": 128000,
    },
    "gpt-4o-mini": {
        "input_per_million": Decimal("0.15"),
        "output_per_million": Decimal("0.60"),
        "context_window": 128000,
    },
    "text-embedding-3-small": {
        "input_per_million": Decimal("0.02"),
        "output_per_million": Decimal("0"),
        "context_window": 8191,
    },
    "claude-sonnet": {
        "input_per_million": Decimal("3.00"),
        "output_per_million": Decimal("15.00"),
        "context_window": 200000,
    },
    "claude-haiku": {
        "input_per_million": Decimal("0.25"),
        "output_per_million": Decimal("1.25"),
        "context_window": 200000,
    },
    "claude-opus": {
        "input_per_million": Decimal("15.00"),
        "output_per_million": Decimal("75.00"),
        "context_window": 200000,
    },
}


class PricingFetcher:
    """Fetches and caches real-time LLM pricing data."""

    def __init__(self) -> None:
        self._pricing: dict[str, dict[str, Any]] = {}
        self._last_updated: datetime | None = None
        self._source: str = "none"
        self._loaded = False

    def load(self) -> None:
        """Load pricing — from cache if fresh, otherwise fetch."""
        if self._loaded:
            return

        # Try cache first
        if self._load_cache():
            self._loaded = True
            return

        # Try OpenRouter
        if self._fetch_openrouter():
            self._save_cache()
            self._loaded = True
            return

        # Try LiteLLM fallback
        if self._fetch_litellm():
            self._save_cache()
            self._loaded = True
            return

        # Try stale cache
        if self._load_cache(ignore_ttl=True):
            logger.warning("Using stale pricing cache — fetch failed")
            self._loaded = True
            return

        # Final fallback: synthetic pricing
        logger.warning("No pricing data available — using built-in fallback")
        self._pricing = {
            name: {**data, "source": "fallback"}
            for name, data in _SYNTHETIC_PRICING.items()
        }
        self._source = "fallback"
        self._last_updated = datetime.now()
        self._loaded = True

    def get_price(self, model_name: str) -> dict[str, Any] | None:
        """Get pricing for a model.

        Returns dict with keys: input_per_million, output_per_million,
        context_window, source, last_updated. Returns None if unknown.
        """
        self.load()
        normalized = self._normalize_name(model_name)

        data = self._pricing.get(normalized)
        if data is None:
            # Try fuzzy match
            for key in self._pricing:
                if normalized in key or key in normalized:
                    data = self._pricing[key]
                    break

        if data is None:
            return None

        return {
            "input_per_million": data["input_per_million"],
            "output_per_million": data["output_per_million"],
            "context_window": data.get("context_window", 0),
            "source": data.get("source", self._source),
            "last_updated": self._last_updated,
        }

    def get_comparable_models(self, model_name: str) -> list[dict[str, Any]]:
        """Return models in the same pricing tier only.

        Flagship models (gpt-4o, claude-sonnet) only compare against other
        flagships. Mid-tier (gpt-4o-mini, claude-haiku) only against mid-tier.
        Never suggests a small/efficient model as replacement for flagship.
        """
        self.load()
        price = self.get_price(model_name)
        if price is None:
            return []

        source_tier = _classify_tier(price["input_per_million"])

        # Only compare within the same tier — no cross-tier downgrades
        tiers_to_include = {source_tier}

        normalized = self._normalize_name(model_name)
        results = []
        for name, data in self._pricing.items():
            if name == normalized:
                continue
            tier = _classify_tier(data["input_per_million"])
            if tier in tiers_to_include:
                results.append({
                    "model": name,
                    "tier": tier,
                    "input_per_million": data["input_per_million"],
                    "output_per_million": data["output_per_million"],
                    "context_window": data.get("context_window", 0),
                })

        results.sort(key=lambda m: m["input_per_million"])
        return results

    def get_tier(self, model_name: str) -> str | None:
        """Return the pricing tier for a model."""
        price = self.get_price(model_name)
        if price is None:
            return None
        return _classify_tier(price["input_per_million"])

    @property
    def source(self) -> str:
        return self._source

    @property
    def last_updated(self) -> datetime | None:
        return self._last_updated

    @property
    def available(self) -> bool:
        self.load()
        return bool(self._pricing)

    # ── Private methods ────────────────────────────────────────

    def _normalize_name(self, name: str) -> str:
        """Normalize model name for lookup."""
        # Strip provider prefixes like "openai/", "anthropic/"
        if "/" in name:
            name = name.split("/")[-1]
        return name.lower().strip()

    def _load_cache(self, ignore_ttl: bool = False) -> bool:
        """Load pricing from disk cache. Returns True if successful."""
        if not _CACHE_FILE.exists():
            return False
        try:
            raw = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
            cached_at = raw.get("cached_at", 0)
            if not ignore_ttl and (time.time() - cached_at) > _CACHE_TTL_SECONDS:
                return False

            self._pricing = {
                name: {
                    "input_per_million": Decimal(str(d["input_per_million"])),
                    "output_per_million": Decimal(str(d["output_per_million"])),
                    "context_window": d.get("context_window", 0),
                    "source": "cache",
                }
                for name, d in raw.get("models", {}).items()
            }
            self._source = "cache"
            self._last_updated = datetime.fromtimestamp(cached_at)
            return bool(self._pricing)
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            logger.warning("Corrupt pricing cache: %s", exc)
            return False

    def _save_cache(self) -> None:
        """Save pricing to disk cache."""
        try:
            _CACHE_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "cached_at": time.time(),
                "source": self._source,
                "models": {
                    name: {
                        "input_per_million": str(d["input_per_million"]),
                        "output_per_million": str(d["output_per_million"]),
                        "context_window": d.get("context_window", 0),
                    }
                    for name, d in self._pricing.items()
                },
            }
            _CACHE_FILE.write_text(
                json.dumps(data, indent=2), encoding="utf-8"
            )
        except OSError as exc:
            logger.warning("Failed to save pricing cache: %s", exc)

    def _fetch_openrouter(self) -> bool:
        """Fetch pricing from OpenRouter API."""
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.get(_OPENROUTER_URL)
                resp.raise_for_status()
                data = resp.json()

            for model in data.get("data", []):
                model_id = model.get("id", "")
                pricing = model.get("pricing", {})
                prompt_price = pricing.get("prompt")
                completion_price = pricing.get("completion")

                if prompt_price is None or completion_price is None:
                    continue

                # OpenRouter returns per-token prices as strings
                try:
                    per_token_input = Decimal(str(prompt_price))
                    per_token_output = Decimal(str(completion_price))
                except Exception:
                    continue

                # Skip models with negative or zero pricing (garbage data)
                if per_token_input <= 0 or per_token_output < 0:
                    continue

                # Convert to per-million
                input_per_m = (per_token_input * Decimal("1000000")).normalize()
                output_per_m = (per_token_output * Decimal("1000000")).normalize()

                name = self._normalize_name(model_id)
                self._pricing[name] = {
                    "input_per_million": input_per_m,
                    "output_per_million": output_per_m,
                    "context_window": model.get("context_length", 0),
                    "source": "openrouter",
                }

            self._source = "openrouter"
            self._last_updated = datetime.now()
            logger.info("Fetched pricing for %d models from OpenRouter", len(self._pricing))
            return bool(self._pricing)

        except httpx.HTTPError as exc:
            logger.warning("OpenRouter fetch failed: %s", exc)
            return False
        except (KeyError, ValueError) as exc:
            logger.warning("OpenRouter parse error: %s", exc)
            return False
        except Exception as exc:
            logger.warning("OpenRouter unavailable: %s", exc)
            return False

    def _fetch_litellm(self) -> bool:
        """Fetch pricing from LiteLLM GitHub database."""
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.get(_LITELLM_URL)
                resp.raise_for_status()
                data = resp.json()

            for model_name, info in data.items():
                if not isinstance(info, dict):
                    continue

                input_cost = info.get("input_cost_per_token")
                output_cost = info.get("output_cost_per_token")
                if input_cost is None or output_cost is None:
                    continue

                try:
                    per_token_in = Decimal(str(input_cost))
                    per_token_out = Decimal(str(output_cost))
                    if per_token_in <= 0 or per_token_out < 0:
                        continue
                    input_per_m = (per_token_in * Decimal("1000000")).normalize()
                    output_per_m = (per_token_out * Decimal("1000000")).normalize()
                except Exception:
                    continue

                name = self._normalize_name(model_name)
                self._pricing[name] = {
                    "input_per_million": input_per_m,
                    "output_per_million": output_per_m,
                    "context_window": info.get("max_tokens", 0),
                    "source": "litellm",
                }

            self._source = "litellm"
            self._last_updated = datetime.now()
            logger.info("Fetched pricing for %d models from LiteLLM", len(self._pricing))
            return bool(self._pricing)

        except httpx.HTTPError as exc:
            logger.warning("LiteLLM fetch failed: %s", exc)
            return False
        except (KeyError, ValueError) as exc:
            logger.warning("LiteLLM parse error: %s", exc)
            return False
        except Exception as exc:
            logger.warning("LiteLLM unavailable: %s", exc)
            return False
