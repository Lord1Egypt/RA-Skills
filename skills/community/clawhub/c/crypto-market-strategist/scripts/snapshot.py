#!/usr/bin/env python3
"""Public, keyless BTC/ETH Deribit volatility-surface snapshot."""
from __future__ import annotations

import json
import math
import time
from collections import defaultdict
from datetime import datetime, timezone
from threading import Lock
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from market_models import black76_greeks, fit_option_surface

API = "https://www.deribit.com/api/v2/public"
_INSTRUMENT_LOCK = Lock()
_LAST_INSTRUMENT_REQUEST = 0.0


def get(method: str, **params):
    """One bounded public request, retrying only transient exchange failures."""
    global _LAST_INSTRUMENT_REQUEST
    if method == "get_instruments":
        with _INSTRUMENT_LOCK:
            delay = 1.05 - (time.monotonic() - _LAST_INSTRUMENT_REQUEST)
            if delay > 0:
                time.sleep(delay)
            _LAST_INSTRUMENT_REQUEST = time.monotonic()
    url = f"{API}/{method}?{urlencode(params)}"
    last_error = None
    for attempt in range(4):
        try:
            with urlopen(url, timeout=30) as response:  # noqa: S310
                payload = json.load(response)
            if "error" in payload:
                raise RuntimeError(payload["error"])
            return payload["result"]
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 3:
                raise
        except RuntimeError:
            raise
        time.sleep(0.75 * (2 ** attempt))
    raise last_error or RuntimeError(f"Deribit request failed: {method}")


def number(value):
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def nearest(chain, target, option_type, count=1):
    """Return the most liquid contracts nearest a target strike."""
    rows = [row for row in chain if row["option_type"] == option_type and number(row.get("mark_iv"))]
    return sorted(
        rows,
        key=lambda row: (
            abs(float(row["strike"]) / target - 1),
            -(number(row.get("open_interest")) or 0),
        ),
    )[:count]


def consolidated_market_snapshot(asset, fit: bool = True):
    """Build the entire listed option surface and dated-futures curve in 3 calls.

    Deribit permits `kind` to be omitted on both currency-level endpoints. This
    returns active options and futures together, so one analysis never needs to
    poll once per expiry or make duplicate inventory/futures calls.
    """
    asset = asset.upper()
    if asset not in {"BTC", "ETH"}:
        raise ValueError("Deribit snapshot supports BTC and ETH only.")
    now = datetime.now(timezone.utc)
    specs = {row["instrument_name"]: row for row in get("get_instruments", currency=asset, expired="false")}
    books = {row["instrument_name"]: row for row in get("get_book_summary_by_currency", currency=asset)}
    spot = number(get("get_index_price", index_name=f"{asset.lower()}_usd")["index_price"])
    chains = defaultdict(list)
    future_rows = []
    for name, spec in specs.items():
        quote = books.get(name)
        if not quote or not spec.get("is_active"):
            continue
        if spec.get("kind") == "option" and number(quote.get("mark_iv")) is not None:
            expiry = int(spec["expiration_timestamp"])
            if expiry > now.timestamp() * 1000:
                chains[expiry].append({**spec, **quote})
        elif spec.get("kind") == "future" and spec.get("settlement_period") != "perpetual":
            expiry = int(spec["expiration_timestamp"])
            days = (expiry / 1000 - now.timestamp()) / 86400
            mark, index = number(quote.get("mark_price")), number(quote.get("estimated_delivery_price"))
            if days > 0 and mark and index:
                basis = mark / index - 1
                future_rows.append({"instrument_name": name, "expiry_timestamp": expiry, "expiry": datetime.fromtimestamp(expiry / 1000, timezone.utc).isoformat(), "days_to_expiry": round(days, 2), "mark_price": mark, "best_bid": number(quote.get("bid_price")), "best_ask": number(quote.get("ask_price")), "index_price": index, "basis_pct": basis * 100, "basis_annualized_simple_pct": basis * 365 / days * 100, "open_interest": number(quote.get("open_interest")), "volume_24h_usd": number(quote.get("volume_usd"))})
    grid, slices = [], {}
    for expiry, chain in sorted(chains.items()):
        days = (expiry - now.timestamp() * 1000) / 86_400_000
        atm = nearest(chain, spot, "call") + nearest(chain, spot, "put")
        if not atm:
            continue
        iv = sum(float(row["mark_iv"]) for row in atm) / len(atm)
        call_oi = sum(number(row.get("open_interest")) or 0 for row in chain if row["option_type"] == "call")
        put_oi = sum(number(row.get("open_interest")) or 0 for row in chain if row["option_type"] == "put")
        grid.append({"expiry_timestamp": expiry, "expiry": datetime.fromtimestamp(expiry / 1000, timezone.utc).isoformat(), "days_to_expiry": round(days, 2), "contract_count": len(chain), "atm_iv_pct": round(iv, 2), "one_sigma_move_pct": round(iv / 100 * math.sqrt(days / 365) * 100, 2), "call_open_interest": call_oi, "put_open_interest": put_oi, "call_put_oi_ratio": round(call_oi / put_oi, 3) if put_oi else None, "strike_min": min(float(row["strike"]) for row in chain), "strike_max": max(float(row["strike"]) for row in chain)})
        fields = ("instrument_name", "strike", "option_type", "mark_iv", "bid_iv", "ask_iv", "mark_price", "bid_price", "ask_price", "open_interest", "volume", "underlying_price", "underlying_index", "interest_rate", "settlement_currency", "instrument_type")
        sliced = []
        for row in sorted(chain, key=lambda row: (float(row["strike"]), row["option_type"])):
            compact = {field: row.get(field) for field in fields}
            years = max(days, 0) / 365
            forward = number(row.get("underlying_price"))
            implied_rate = math.log(forward / spot) / years if forward and spot and years else 0
            compact["derived_greeks_black76"] = black76_greeks(forward, number(row.get("strike")), years, number(row.get("mark_iv")), row.get("option_type"), implied_rate, spot)
            sliced.append(compact)
        slices[str(expiry)] = sliced
    snapshot = {"asset": asset, "as_of": now.isoformat(), "request_count": 3, "source": "Deribit public get_instruments (all kinds), get_book_summary_by_currency (all kinds), and get_index_price", "spot_index_usd": spot, "surface_inventory": {"expiry_grid": grid}, "expiry_slices": slices, "dated_futures_curve": sorted(future_rows, key=lambda row: row["expiry_timestamp"]), "limitations": ["This is one coherent public snapshot, not a live stream.", "The book summary supplies quoted IV, BBO, OI, and volume; fetch a specific ticker only when exchange Greeks are indispensable."]}
    if fit:
        snapshot["surface_dossier"] = fit_option_surface(snapshot)
    return snapshot
