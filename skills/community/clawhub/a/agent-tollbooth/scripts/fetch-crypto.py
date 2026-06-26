#!/usr/bin/env python3
"""Fetch CoinGecko crypto prices with disk caching and structured web-access logging."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

SCRIPT_DIR = Path(__file__).resolve().parent
OPENCLAW_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace")).expanduser()
DATA_DIR = OPENCLAW_WORKSPACE / "data" / "agent-tollbooth"
CACHE_DIR = DATA_DIR / "cache"


def _load_logger():
    logger_path = SCRIPT_DIR / "web-log.py"
    spec = importlib.util.spec_from_file_location("web_log", logger_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load logger at {logger_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.log_event


log_event = _load_logger()


def _cache_path(coins: List[str]) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    normalized = ",".join(sorted({coin.strip().lower() for coin in coins if coin.strip()}))
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"coingecko-{digest}.json"


def _load_cached(coins: List[str], ttl_seconds: int) -> Dict[str, Any] | None:
    path = _cache_path(coins)
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    ts = payload.get("cached_at")
    if not ts:
        return None

    try:
        cached_at = datetime.fromisoformat(ts)
    except ValueError:
        return None

    age = (datetime.now(timezone.utc) - cached_at).total_seconds()
    if age <= ttl_seconds:
        requested = ",".join(sorted({coin.strip().lower() for coin in coins if coin.strip()}))
        log_event(
            service="CoinGecko",
            event_type="cache_hit",
            detail=f"Used cached batch quote for {requested}",
            worked="true",
        )
        return payload.get("prices")

    return None


def _save_cache(coins: List[str], prices: Dict[str, Any]) -> None:
    payload = {
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "prices": prices,
    }
    _cache_path(coins).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _fetch_prices(coins: List[str], timeout_seconds: float) -> Dict[str, Any]:
    requested = [coin.strip().lower() for coin in coins if coin.strip()]
    joined = ",".join(requested)
    encoded_ids = quote(joined, safe=",")
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={encoded_ids}&vs_currencies=usd&include_24hr_change=true"
    )

    try:
        with urlopen(url, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        if exc.code == 429:
            log_event(
                service="CoinGecko",
                event_type="429",
                detail=f"HTTP 429 while fetching ids={joined}",
                worked="false",
            )
        elif exc.code in {401, 403}:
            log_event(
                service="CoinGecko",
                event_type="auth_failure",
                detail=f"HTTP {exc.code} while fetching ids={joined}",
                worked="false",
            )
        raise
    except (TimeoutError, socket.timeout) as exc:
        log_event(
            service="CoinGecko",
            event_type="timeout",
            detail=f"Timeout while fetching ids={joined}: {exc}",
            worked="false",
        )
        raise
    except URLError as exc:
        if isinstance(exc.reason, socket.timeout):
            log_event(
                service="CoinGecko",
                event_type="timeout",
                detail=f"URLError timeout while fetching ids={joined}: {exc.reason}",
                worked="false",
            )
        raise

    payload = json.loads(body)
    log_event(
        service="CoinGecko",
        event_type="success",
        detail=f"Fetched live batch quote for ids={joined}",
        worked="true",
    )
    return payload


def fetch_crypto(coins: List[str], timeout_seconds: float, cache_ttl_seconds: int) -> Dict[str, Any]:
    cached = _load_cached(coins, cache_ttl_seconds)
    if cached is not None:
        return cached

    prices = _fetch_prices(coins, timeout_seconds)
    _save_cache(coins, prices)
    return prices


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch CoinGecko prices in a single batch")
    parser.add_argument("coins", nargs="+", help="CoinGecko IDs (e.g., bitcoin ethereum solana)")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds")
    parser.add_argument("--cache-ttl", type=int, default=300, help="Cache TTL in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested = [coin.strip().lower() for coin in args.coins if coin.strip()]
    prices = fetch_crypto(requested, timeout_seconds=args.timeout, cache_ttl_seconds=args.cache_ttl)
    as_of = datetime.now(timezone.utc).isoformat()

    output: List[Dict[str, Any]] = []
    for coin in requested:
        quote = prices.get(coin, {})
        output.append(
            {
                "symbol": coin,
                "price": quote.get("usd"),
                "change24h": quote.get("usd_24h_change"),
                "asOf": as_of,
            }
        )

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
