from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import replace
from typing import Any, Protocol

from .config import ConfigError, ScanConfig
from .models import Quote, Stock


logger = logging.getLogger(__name__)


class SecurityListClient(Protocol):
    def get_security_count(self, market: int) -> int:
        ...

    def get_security_list(self, market: int, start: int) -> list[dict[str, Any]]:
        ...

    def get_quotes(self, stocks: list[Stock]) -> list[Quote]:
        ...


SH_PREFIXES = ("600", "601", "603", "605", "688", "689")
SZ_PREFIXES = ("000", "001", "002", "003", "300", "301")
BSE_PREFIXES = ("8", "4", "920")
STAR_PREFIXES = ("688", "689")
SECURITY_LIST_BATCH_SIZE = 1000
QUOTE_VALIDATE_BATCH_SIZE = 80


def build_universe(config: ScanConfig, client: SecurityListClient) -> list[Stock]:
    if config.mode == "watchlist":
        return parse_watchlist(config.watchlist, config)
    return load_market_universe(client, config)


def parse_watchlist(raw_codes: Iterable[str], config: ScanConfig) -> list[Stock]:
    stocks: list[Stock] = []
    seen: set[tuple[int, str]] = set()
    for raw in raw_codes:
        stock = parse_stock_code(raw)
        if not should_include_stock(stock, config):
            continue
        if stock.key in seen:
            continue
        seen.add(stock.key)
        stocks.append(stock)
    return stocks


def parse_stock_code(raw: str) -> Stock:
    value = raw.strip().upper()
    if value.startswith("SH"):
        market = 1
        code = value[2:]
    elif value.startswith("SZ"):
        market = 0
        code = value[2:]
    else:
        code = value
        market = infer_market(code)

    if not code.isdigit() or len(code) != 6:
        raise ConfigError(f"Invalid stock code: {raw}")
    return Stock(market=market, code=code)


def infer_market(code: str) -> int:
    if not code.isdigit() or len(code) != 6:
        raise ConfigError(f"Invalid stock code: {code}")
    if code.startswith(SH_PREFIXES):
        return 1
    if code.startswith(SZ_PREFIXES) or is_bse_code(code):
        return 0
    raise ConfigError(f"Cannot infer market for stock code: {code}")


def load_market_universe(client: SecurityListClient, config: ScanConfig) -> list[Stock]:
    stocks: list[Stock] = []
    seen: set[tuple[int, str]] = set()
    for market in (0, 1):
        try:
            count = client.get_security_count(market)
        except Exception:
            logger.exception("Failed to read TDX security count for market=%s", market)
            continue
        logger.info("TDX security count: market=%s count=%s", market, count)
        for start in range(0, count, SECURITY_LIST_BATCH_SIZE):
            try:
                securities = client.get_security_list(market, start)
            except Exception:
                logger.exception("Failed to read TDX security list: market=%s start=%s", market, start)
                continue
            for item in securities:
                stock = _stock_from_security_item(market, item)
                if stock is None:
                    continue
                if not should_include_stock(stock, config):
                    continue
                if stock.key in seen:
                    continue
                seen.add(stock.key)
                stocks.append(stock)

    if stocks:
        logger.info("Loaded stock universe from TDX security list: %s", len(stocks))
        return stocks

    logger.warning("TDX security list returned no usable stocks; falling back to generated A-share universe.")
    return load_generated_universe(client, config)


def load_generated_universe(client: SecurityListClient, config: ScanConfig) -> list[Stock]:
    candidates = generated_a_share_candidates(config)
    logger.info("Generated A-share candidates: %s", len(candidates))

    valid: list[Stock] = []
    seen: set[tuple[int, str]] = set()
    for batch in _chunks(candidates, QUOTE_VALIDATE_BATCH_SIZE):
        try:
            quotes = client.get_quotes(batch)
        except Exception:
            logger.exception("Failed to validate generated stock batch starting at %s", batch[0].display_code)
            continue
        for quote in quotes:
            if not _quote_looks_valid(quote):
                continue
            stock = quote.stock
            if not should_include_stock(stock, config):
                continue
            if stock.key in seen:
                continue
            seen.add(stock.key)
            valid.append(stock)

    logger.info("Validated generated A-share universe: %s", len(valid))
    return valid


def generated_a_share_candidates(config: ScanConfig) -> list[Stock]:
    ranges = [
        (0, "000", 1, 999),
        (0, "001", 0, 999),
        (0, "002", 0, 999),
        (0, "003", 0, 999),
        (0, "300", 0, 999),
        (0, "301", 0, 999),
        (1, "600", 0, 999),
        (1, "601", 0, 999),
        (1, "603", 0, 999),
        (1, "605", 0, 999),
    ]

    stocks: list[Stock] = []
    for market, prefix, start, end in ranges:
        for suffix in range(start, end + 1):
            code = f"{prefix}{suffix:03d}"
            stock = Stock(market=market, code=code)
            if should_include_stock(stock, config):
                stocks.append(stock)
    return stocks


def should_include_stock(stock: Stock, config: ScanConfig) -> bool:
    code = stock.code
    if config.exclude_star_market and is_star_market_code(code):
        return False
    if config.exclude_bse and is_bse_code(code):
        return False
    return is_supported_a_share(stock)


def is_supported_a_share(stock: Stock) -> bool:
    code = stock.code
    if stock.market == 1:
        return code.startswith(SH_PREFIXES)
    if stock.market == 0:
        return code.startswith(SZ_PREFIXES) or is_bse_code(code)
    return False


def is_star_market_code(code: str) -> bool:
    return code.startswith(STAR_PREFIXES)


def is_bse_code(code: str) -> bool:
    return code.startswith(BSE_PREFIXES)


def _stock_from_security_item(market: int, item: dict[str, Any]) -> Stock | None:
    code = str(item.get("code", "")).strip()
    if not code.isdigit() or len(code) != 6:
        return None
    name = str(item.get("name", "")).strip()
    return replace(Stock(market=market, code=code), name=name)


def _quote_looks_valid(quote: Quote) -> bool:
    return quote.price > 0 or quote.open > 0 or quote.last_close > 0 or bool(quote.stock.name)


def _chunks(items: list[Stock], size: int) -> Iterable[list[Stock]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]
