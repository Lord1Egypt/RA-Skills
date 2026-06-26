#!/usr/bin/env python3
"""Fetch stock prices with lightweight disk caching and structured web-access logging."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_DIR = SCRIPT_DIR.parent

# Write cache outside the skill bundle.
# Resolves to $OPENCLAW_WORKSPACE/data/agent-tollbooth/ on any standard OpenClaw install.
# Falls back to a local data/ dir if the workspace is not found.
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
OCLAW_DATA_DIR = _WORKSPACE / "data" / "agent-tollbooth"
DATA_DIR = OCLAW_DATA_DIR if _WORKSPACE.exists() else MODULE_DIR / "data"
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


def _cache_path(symbol: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(symbol.encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"{symbol.upper()}-{digest}.json"


def _load_cached(symbol: str, ttl_seconds: int) -> Dict[str, Any] | None:
    path = _cache_path(symbol)
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
        log_event(
            service="Yahoo Finance",
            event_type="cache_hit",
            detail=f"Used cached quote for {symbol}",
            worked="true",
        )
        return payload.get("quote")

    return None


def _save_cache(symbol: str, quote: Dict[str, Any]) -> None:
    payload = {
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "quote": quote,
    }
    _cache_path(symbol).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _fetch_quote(symbol: str, timeout_seconds: float) -> Dict[str, Any]:
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d"

    try:
        with urlopen(url, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        if exc.code == 429:
            log_event(
                service="Yahoo Finance",
                event_type="429",
                detail=f"HTTP 429 while fetching {symbol}",
                worked="false",
            )
        elif exc.code in {401, 403}:
            log_event(
                service="Yahoo Finance",
                event_type="auth_failure",
                detail=f"HTTP {exc.code} while fetching {symbol}",
                worked="false",
            )
        raise
    except (TimeoutError, socket.timeout) as exc:
        log_event(
            service="Yahoo Finance",
            event_type="timeout",
            detail=f"Timeout while fetching {symbol}: {exc}",
            worked="false",
        )
        raise
    except URLError as exc:
        if isinstance(exc.reason, socket.timeout):
            log_event(
                service="Yahoo Finance",
                event_type="timeout",
                detail=f"URLError timeout while fetching {symbol}: {exc.reason}",
                worked="false",
            )
        raise

    payload = json.loads(body)
    results = payload.get("chart", {}).get("result", [])
    if not results:
        raise RuntimeError(f"No quote data returned for {symbol}")

    meta = results[0].get("meta", {})
    quote = {
        "symbol": meta.get("symbol", symbol.upper()),
        "regularMarketPrice": meta.get("regularMarketPrice"),
        "currency": meta.get("currency"),
        "regularMarketTime": meta.get("regularMarketTime"),
    }
    log_event(
        service="Yahoo Finance",
        event_type="success",
        detail=f"Fetched live quote for {symbol}",
        worked="true",
    )
    return quote


def fetch_price(symbol: str, timeout_seconds: float, cache_ttl_seconds: int) -> Dict[str, Any]:
    symbol = symbol.upper().strip()

    cached = _load_cached(symbol, cache_ttl_seconds)
    if cached is not None:
        return cached

    quote = _fetch_quote(symbol, timeout_seconds)
    _save_cache(symbol, quote)
    return quote


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch quotes from Yahoo Finance")
    parser.add_argument("symbols", nargs="+", help="Ticker symbols (e.g., AAPL MSFT TSLA)")
    parser.add_argument("--timeout", type=float, default=8.0, help="HTTP timeout in seconds")
    parser.add_argument("--cache-ttl", type=int, default=300, help="Cache TTL in seconds")
    parser.add_argument("--sleep", type=float, default=0.0, help="Sleep between requests")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output: List[Dict[str, Any]] = []

    for idx, symbol in enumerate(args.symbols):
        quote = fetch_price(symbol, timeout_seconds=args.timeout, cache_ttl_seconds=args.cache_ttl)
        output.append(
            {
                "symbol": quote.get("symbol", symbol.upper()),
                "price": quote.get("regularMarketPrice"),
                "currency": quote.get("currency"),
                "asOf": quote.get("regularMarketTime"),
            }
        )

        if args.sleep and idx < len(args.symbols) - 1:
            time.sleep(args.sleep)

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
