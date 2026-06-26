#!/usr/bin/env python3
"""Load market/FX context for portfolio analysis.

Phase 2 note:
- keep the contract small
- keep current HTTP-based implementation for now
- let analysis consume a normalized context instead of fetching directly
"""

from __future__ import annotations

import glob
import json
import re
import time
from pathlib import Path
from typing import Any

import requests


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def add_warning(warnings: list[str], message: str) -> None:
    if message not in warnings:
        warnings.append(message)


def ticker_to_yahoo_symbol(ticker: str, ticker_map: dict[str, str]) -> str:
    mapped = ticker_map.get(ticker)
    if mapped:
        return mapped

    exchange, code = ticker.split(":")
    if exchange == "SHA":
        return f"{code}.SS"
    if exchange == "SHE":
        return f"{code}.SZ"
    if exchange == "HKG":
        return f"{code}.HK"
    return code


def _request_json_with_retry(
    url: str,
    *,
    headers: dict[str, str],
    proxies: dict[str, str] | None,
    params: dict[str, Any],
    timeout: int,
    attempts: int = 3,
    retry_delay_seconds: float = 0.6,
) -> dict[str, Any]:
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_exc = exc
            if attempt < attempts:
                time.sleep(retry_delay_seconds * attempt)
    assert last_exc is not None
    raise last_exc


def _request_text_with_retry(
    url: str,
    *,
    headers: dict[str, str],
    proxies: dict[str, str] | None,
    timeout: int,
    params: dict[str, Any] | None = None,
    attempts: int = 3,
    retry_delay_seconds: float = 0.6,
) -> str:
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                params=params,
            )
            response.raise_for_status()
            return response.text
        except Exception as exc:
            last_exc = exc
            if attempt < attempts:
                time.sleep(retry_delay_seconds * attempt)
    assert last_exc is not None
    raise last_exc


def _fetch_otc_published_nav(
    code: str,
    *,
    headers: dict[str, str],
    proxies: dict[str, str] | None,
) -> tuple[float, str, str]:
    text = _request_text_with_retry(
        f"https://fund.eastmoney.com/pingzhongdata/{code}.js",
        headers=headers,
        proxies=proxies,
        timeout=15,
    )
    match = re.search(r"var\s+Data_netWorthTrend\s*=\s*(\[[\s\S]*?\]);", text)
    if not match:
        raise RuntimeError("otc published nav parse failed")
    data = json.loads(match.group(1))
    for item in reversed(data):
        nav = item.get("y")
        if nav not in (None, ""):
            return float(nav), "CNY", "pingzhongdata"
    raise RuntimeError("otc published nav missing")


def _fetch_otc_nav(
    code: str,
    *,
    headers: dict[str, str],
    proxies: dict[str, str] | None,
) -> tuple[float, str, str]:
    text = _request_text_with_retry(
        f"https://fundgz.1234567.com.cn/js/{code}.js",
        headers=headers,
        proxies=proxies,
        timeout=15,
    )
    match = re.search(r"jsonpgz\((.*)\);?", text)
    if not match:
        return _fetch_otc_published_nav(code, headers=headers, proxies=proxies)
    payload = match.group(1).strip()
    if not payload:
        return _fetch_otc_published_nav(code, headers=headers, proxies=proxies)
    data = json.loads(payload)
    nav = data.get("gsz") or data.get("dwjz")
    if nav in (None, ""):
        return _fetch_otc_published_nav(code, headers=headers, proxies=proxies)
    source = "fundgz_estimate" if data.get("gsz") else "fundgz_dwjz"
    return float(nav), "CNY", source


def _fetch_stooq_price(
    ticker: str,
    *,
    headers: dict[str, str],
    proxies: dict[str, str] | None,
) -> tuple[float | None, str | None]:
    exchange, code = ticker.split(":")
    if exchange not in ("NASDAQ", "NYSE"):
        return None, None

    text = _request_text_with_retry(
        "https://stooq.com/q/l/",
        headers=headers,
        proxies=proxies,
        timeout=15,
        params={"s": f"{code.lower()}.us", "f": "sd2t2ohlcvn", "i": "d"},
    )

    for line in text.strip().splitlines():
        parts = line.split(",")
        if not parts or parts[0].lower() == "symbol":
            continue
        if len(parts) < 7:
            continue
        close_price = parts[6].strip()
        if close_price in ("", "N/D", "Close"):
            continue
        return float(close_price), "USD"

    raise RuntimeError("unexpected stooq response")


def _find_last_nonzero_price(
    portfolio_dir: Path,
    ticker: str,
    before_date: str,
) -> tuple[float | None, str | None]:
    snap_dir = portfolio_dir / "snapshots"
    files = sorted(glob.glob(str(snap_dir / "*.json")))
    for file_path in reversed(files):
        snapshot_date = Path(file_path).stem
        if snapshot_date >= before_date:
            continue
        try:
            snapshot = load_json(Path(file_path))
            for group in snapshot.get("groups", {}).values():
                for position in group.get("positions", []):
                    if position.get("ticker") == ticker and float(position.get("current_price", 0)) > 0:
                        return float(position["current_price"]), position.get("currency", "CNY")
        except Exception:
            continue
    return None, None


def load_market_context(
    holdings: dict[str, Any],
    portfolio_dir: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    proxy = config.get("proxy", "")
    proxies = {"http": proxy, "https": proxy} if proxy else None
    headers = {"User-Agent": "Mozilla/5.0"}
    ticker_map = config.get("ticker_map", {})
    yahoo_base = config.get("yahoo_base", "https://query1.finance.yahoo.com/v8/finance/chart")
    fx_tickers = config.get("fx_tickers", {"HKD_CNY": "HKDCNY=X", "USD_CNY": "USDCNY=X"})

    prices: dict[str, float] = {}
    currencies: dict[str, str] = {}
    fx_rates: dict[str, float] = {"CNY": 1.0}
    warnings: list[str] = []
    meta: dict[str, Any] = {}

    all_tickers = {
        pos["ticker"]
        for group in holdings.get("groups", {}).values()
        for pos in group.get("positions", [])
    }

    for ticker in all_tickers:
        if ticker in prices:
            continue
        yahoo_symbol = ticker_to_yahoo_symbol(ticker, ticker_map)
        try:
            exchange, code = ticker.split(":")
            if exchange == "OTC":
                nav, currency, source = _fetch_otc_nav(code, headers=headers, proxies=proxies)
                prices[ticker] = nav
                currencies[ticker] = currency
                meta[ticker] = {"source": source, "fallback": source != "fundgz_estimate"}
                if source == "pingzhongdata":
                    add_warning(warnings, f"{ticker} 当日估值不可用，已回退为最近披露净值")
                continue

            data = _request_json_with_retry(
                f"{yahoo_base}/{yahoo_symbol}",
                headers=headers,
                proxies=proxies,
                timeout=15,
                params={"interval": "1d", "range": "1d"},
            )
            meta_info = data["chart"]["result"][0]["meta"]
            prices[ticker] = meta_info["regularMarketPrice"]
            currencies[ticker] = meta_info.get("currency", "CNY")
            meta[ticker] = {"source": "yahoo", "fallback": False}
        except Exception as exc:
            try:
                fallback_price, fallback_currency = _fetch_stooq_price(
                    ticker,
                    headers=headers,
                    proxies=proxies,
                )
                if fallback_price is not None:
                    prices[ticker] = fallback_price
                    currencies[ticker] = fallback_currency or "USD"
                    meta[ticker] = {"source": "stooq", "fallback": True}
                    add_warning(warnings, f"{ticker} Yahoo 价格获取失败，已回退为 stooq 报价")
                    continue
            except Exception as fallback_exc:
                add_warning(warnings, f"{ticker} stooq 回退失败（{fallback_exc.__class__.__name__}）")

            if ticker.startswith("OTC:"):
                fallback_price, fallback_currency = _find_last_nonzero_price(
                    portfolio_dir,
                    ticker,
                    holdings["date"],
                )
                if fallback_price is not None:
                    prices[ticker] = fallback_price
                    currencies[ticker] = fallback_currency or "CNY"
                    meta[ticker] = {"source": "snapshot_history", "fallback": True}
                    add_warning(warnings, f"{ticker} 当日净值获取失败，已回退为最近一次非 0 历史净值")
                    continue

            prices[ticker] = 0.0
            currencies[ticker] = "CNY"
            meta[ticker] = {"source": "unavailable", "fallback": True}
            add_warning(warnings, f"{ticker} 当前价格获取失败，已回退为 0（{exc.__class__.__name__}）")

    for key, yahoo_symbol in fx_tickers.items():
        currency = key.split("_")[0]
        try:
            data = _request_json_with_retry(
                f"{yahoo_base}/{yahoo_symbol}",
                headers=headers,
                proxies=proxies,
                timeout=15,
                params={"interval": "1d", "range": "1d"},
            )
            rate = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            fx_rates[currency] = rate
            meta[f"fx:{currency}"] = {"source": "yahoo", "fallback": False}
        except Exception as exc:
            if currency == "HKD":
                fx_rates["HKD"] = 0.88
                meta["fx:HKD"] = {"source": "static_default", "fallback": True}
                add_warning(warnings, f"HKD 汇率获取失败，已回退为 0.88（{exc.__class__.__name__}）")
            elif currency == "USD":
                fx_rates["USD"] = 6.90
                meta["fx:USD"] = {"source": "static_default", "fallback": True}
                add_warning(warnings, f"USD 汇率获取失败，已回退为 6.90（{exc.__class__.__name__}）")

    return {
        "prices": prices,
        "currencies": currencies,
        "fx_rates": fx_rates,
        "warnings": warnings,
        "meta": meta,
    }
