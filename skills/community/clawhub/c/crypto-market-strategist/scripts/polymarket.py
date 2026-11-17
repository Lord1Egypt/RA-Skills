"""Public Polymarket BTC/ETH terminal and barrier market collector."""
from __future__ import annotations

import json
import re
import argparse
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
ASSET_TAG = {"BTC": "235", "ETH": "39"}
WORDS = {"BTC": ("bitcoin", "btc"), "ETH": ("ethereum", "eth")}
MACRO_TOPICS = {
    "fed_policy": ("fomc", "federal reserve", "fed decision", "interest rate", "fed decrease", "fed increase"),
    "inflation": ("cpi", "pce", "inflation"),
    "employment": ("nonfarm", "payroll", "unemployment", "jobs report"),
    "growth": ("gdp", "gross domestic product"),
}
NON_PRICE_TOPICS = (
    "dominance", "market cap", "volatility index", "vol index", "kimchi premium",
    "etf flow", "etf inflow", "etf outflow", "transaction fee", "hashrate",
)


def request(url, *, body=None):
    headers = {"User-Agent": "crypto-market-strategist/0.1"}
    if body is not None:
        body, headers = json.dumps(body).encode(), {**headers, "Content-Type": "application/json"}
    with urlopen(Request(url, data=body, headers=headers), timeout=30) as response:  # noqa: S310
        return json.load(response)


def list_value(raw):
    if isinstance(raw, list):
        return raw
    try:
        return json.loads(raw or "[]")
    except (json.JSONDecodeError, TypeError):
        return []


def number(value):
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def classify(title, rules):
    text = f"{title} {rules}".lower()
    if any(topic in text for topic in NON_PRICE_TOPICS):
        return "other"
    if "immediately resolve" in text or re.search(r"\b(hit|reach|dip)\b", text):
        return "barrier"
    if "up or down" in text:
        return "other"
    if "close" in text or "above" in text or "price on" in text:
        return "terminal"
    return "other"


def parse_time(raw):
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None


def books(token_ids):
    results = {}
    for start in range(0, len(token_ids), 500):
        for book in request(f"{CLOB}/books", body=[{"token_id": token} for token in token_ids[start : start + 500]]):
            if book.get("asset_id"):
                results[book["asset_id"]] = book
    return results


def bbo(book):
    bids = [number(row.get("price")) for row in book.get("bids", [])]
    asks = [number(row.get("price")) for row in book.get("asks", [])]
    bid, ask = max((x for x in bids if x is not None), default=None), min((x for x in asks if x is not None), default=None)
    depth = sum((number(row.get("size")) or 0) * (number(row.get("price")) or 0) for row in book.get("bids", []) + book.get("asks", []))
    return bid, ask, (bid + ask) / 2 if bid is not None and ask is not None else None, depth


def macro_topic(*texts):
    text = " ".join(texts).lower()
    return next((topic for topic, keywords in MACRO_TOPICS.items() if any(word in text for word in keywords)), None)


def run(asset, event_limit=1000):
    asset = asset.upper()
    if asset not in ASSET_TAG:
        raise ValueError("Polymarket collector supports BTC and ETH only.")
    events = []
    for offset in range(0, event_limit, 100):
        params = urlencode({"tag_id": ASSET_TAG[asset], "active": "true", "closed": "false", "order": "volume24hr", "ascending": "false", "limit": min(100, event_limit - offset), "offset": offset})
        page = request(f"{GAMMA}/events?{params}")
        if not isinstance(page, list):
            break
        events.extend(page)
        if len(page) < 100:
            break
    now = datetime.now(timezone.utc)
    raw = []
    for event in events:
        event_title = event.get("title", "")
        if not any(re.search(rf"\b{word}\b", event_title, re.I) for word in WORDS[asset]):
            continue
        for market in event.get("markets") or []:
            if market.get("closed") or not market.get("active", True) or not market.get("enableOrderBook", True):
                continue
            rules, title = market.get("description") or "", market.get("question") or event_title
            kind = classify(title, rules)
            if kind == "other":
                continue
            outcomes, token_ids = list_value(market.get("outcomes")), list_value(market.get("clobTokenIds"))
            if len(outcomes) != len(token_ids):
                continue
            close_time = parse_time(market.get("endDate") or event.get("endDate"))
            days = (close_time - now).total_seconds() / 86400 if close_time else None
            for outcome, token_id in zip(outcomes, token_ids):
                # Only selected YES legs of strike/range and barrier events are
                # returned. Up/down markets are excluded at classification time.
                if outcome.lower() != "yes":
                    continue
                raw.append({"event_slug": event.get("slug"), "event_title": event_title, "market_title": title, "slug": market.get("slug"), "outcome": outcome, "token_id": token_id, "market_type": kind, "rule_window_at": close_time.isoformat() if close_time else None, "approx_days_to_rule_window": round(days, 2) if days is not None else None, "rules": rules, "reported_liquidity": number(market.get("liquidity")), "reported_volume_24h": number(market.get("volume24hr"))})
    current_books = books(list(dict.fromkeys(row["token_id"] for row in raw)))
    rows = []
    for row in raw:
        book = current_books.get(row["token_id"])
        if not book:
            continue
        bid, ask, mid, depth = bbo(book)
        if mid is None:
            continue
        rows.append({**row, "best_bid": bid, "best_ask": ask, "spread_pct_points": round((ask - bid) * 100, 3), "book_depth_notional": round(depth, 3), "midpoint_probability_pct": round(mid * 100, 2), "book_timestamp": book.get("timestamp")})
    rows.sort(key=lambda row: ((row["reported_volume_24h"] or 0), (row["reported_liquidity"] or 0)), reverse=True)
    panels = {name: [row for row in rows if row["market_type"] == name] for name in ("terminal", "barrier")}
    windows = {}
    for row in rows:
        entry = windows.setdefault(row["event_slug"], {"event_slug": row["event_slug"], "event_title": row["event_title"], "rule_window_at": row["rule_window_at"], "approx_days_to_rule_window": row["approx_days_to_rule_window"], "terminal_count": 0, "barrier_count": 0, "reported_volume_24h": 0})
        entry[{"terminal": "terminal_count", "barrier": "barrier_count"}[row["market_type"]]] += 1
        entry["reported_volume_24h"] += row["reported_volume_24h"] or 0
    return {"asset": asset, "as_of": datetime.now(timezone.utc).isoformat(), "source": "Polymarket Gamma active asset-tag discovery plus public CLOB best-bid/best-ask midpoint", "event_windows": sorted(windows.values(), key=lambda row: row["reported_volume_24h"], reverse=True), "terminal_markets": panels["terminal"], "barrier_markets": panels["barrier"], "method": "Returns only strike/range terminal events and hit/reach/dip barriers; up/down markets are excluded. Event windows use actual rule-window timing, not artificial daily/weekly/monthly labels. Terminal markets are suitable for closest-horizon comparison with vanilla options; barriers are path-dependent touch probabilities and remain separate.", "limitations": ["Midpoint is a display estimate, not an executable fill.", "Rule text is included because Binance source/time wording determines each contract.", "Rule-window time is supplied for sorting and must be checked against the rules before analysis."]}


def macro_events(event_limit=500, max_events=40):
    """Discover liquid active US macro-policy/release events, including FOMC."""
    events = []
    for offset in range(0, event_limit, 100):
        params = urlencode({"active": "true", "closed": "false", "order": "volume24hr", "ascending": "false", "limit": min(100, event_limit - offset), "offset": offset})
        page = request(f"{GAMMA}/events?{params}")
        if not isinstance(page, list):
            break
        events.extend(page)
        if len(page) < 100:
            break
    selected = []
    for event in events:
        title, rules = event.get("title", ""), event.get("description", "")
        topic = macro_topic(title, rules)
        if topic:
            selected.append((event, topic))
    selected.sort(key=lambda item: number(item[0].get("volume24hr")) or 0, reverse=True)
    selected = selected[:max_events]
    raw = []
    now = datetime.now(timezone.utc)
    for event, topic in selected:
        for market in event.get("markets") or []:
            if market.get("closed") or not market.get("active", True) or not market.get("enableOrderBook", True):
                continue
            outcomes, token_ids = list_value(market.get("outcomes")), list_value(market.get("clobTokenIds"))
            if len(outcomes) != len(token_ids):
                continue
            close_time = parse_time(market.get("endDate") or event.get("endDate"))
            days = (close_time - now).total_seconds() / 86400 if close_time else None
            for outcome, token_id in zip(outcomes, token_ids):
                if outcome.lower() != "yes":
                    continue
                raw.append({"event_slug": event.get("slug"), "event_title": event.get("title"), "macro_topic": topic, "market_title": market.get("question") or event.get("title"), "answer_label": market.get("groupItemTitle") or "Yes", "slug": market.get("slug"), "outcome": outcome, "token_id": token_id, "rule_window_at": close_time.isoformat() if close_time else None, "approx_days_to_rule_window": round(days, 2) if days is not None else None, "rules": market.get("description") or event.get("description") or "", "reported_liquidity": number(market.get("liquidity")), "reported_volume_24h": number(market.get("volume24hr")), "event_neg_risk": bool(event.get("negRisk"))})
    current_books = books(list(dict.fromkeys(row["token_id"] for row in raw)))
    rows = []
    for row in raw:
        book = current_books.get(row["token_id"])
        if not book:
            continue
        bid, ask, mid, depth = bbo(book)
        if mid is not None:
            rows.append({**row, "best_bid": bid, "best_ask": ask, "spread_pct_points": round((ask - bid) * 100, 3), "book_depth_notional": round(depth, 3), "midpoint_probability_pct": round(mid * 100, 2), "book_timestamp": book.get("timestamp")})
    return {"as_of": datetime.now(timezone.utc).isoformat(), "source": "Polymarket Gamma active macro discovery plus public CLOB best-bid/best-ask midpoint", "events": [{"event_slug": event.get("slug"), "event_title": event.get("title"), "macro_topic": topic, "rule_window_at": event.get("endDate"), "reported_liquidity": number(event.get("liquidity")), "reported_volume_24h": number(event.get("volume24hr"))} for event, topic in selected], "markets": sorted(rows, key=lambda row: row["reported_volume_24h"] or 0, reverse=True), "method": "Includes active FOMC/Fed policy, inflation, employment, and growth events. FOMC bracket rows are commonly mutually exclusive neg-risk outcomes; do not sum their Yes midpoint probabilities or treat them as independent trades.", "limitations": ["These are macro event-risk inputs, not crypto price or spot signals.", "Read each rule and official resolution source before interpreting a probability.", "Midpoint is not an executable fill."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset", choices=("BTC", "ETH", "btc", "eth"))
    args = parser.parse_args()
    print(json.dumps(run(args.asset), indent=2))
