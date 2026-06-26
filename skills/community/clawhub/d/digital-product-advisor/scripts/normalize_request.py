#!/usr/bin/env python3
"""Lightweight heuristic request normalizer for MVP demos.

This is intentionally simple and should not replace agent judgment.
"""

import argparse
import json
import re

BRANDS = ["Sony", "Bose", "Apple", "Samsung", "Huawei", "Xiaomi", "Redmi", "OPPO", "Vivo", "Edifier", "Soundcore", "Jabra", "Sennheiser", "Beats"]


def detect_currency(query):
    q = query.lower()
    if "rmb" in q or "cny" in q or "元" in query:
        return "CNY"
    if "usd" in q or "$" in query:
        return "USD"
    if "eur" in q or "€" in query:
        return "EUR"
    if "jpy" in q or "円" in query:
        return "JPY"
    return None


def detect_region(query, currency):
    q = query.lower()
    if any(x in q for x in ["china", "jd", "tmall", "pinduoduo", "taobao"]) or currency == "CNY":
        return "China"
    if any(x in q for x in ["us", "usa", "best buy", "amazon us"]):
        return "US"
    return None


def detect_budget(query):
    match = re.search(r"(?:under|below|around|about|预算|以内|低于)?\s*([0-9]{2,6})\s*(?:rmb|cny|元|usd|eur|jpy|dollars?)?", query, re.I)
    return int(match.group(1)) if match else None


def detect_brands(query):
    found = [brand for brand in BRANDS if re.search(rf"\b{re.escape(brand)}\b", query, re.I)]
    q = query.lower()
    if found and any(x in q for x in ["only", "just", "brand", "compare", "vs"]):
        mode = "brand_vs_brand" if len(found) > 1 and (" vs " in q or "compare" in q) else "include_only"
    elif found:
        mode = "brand_first"
    else:
        mode = "open_market"
    return {"mode": mode, "include": found, "exclude": []}


def detect_use_case(query):
    q = query.lower()
    cases = []
    mapping = {
        "commuting": ["commute", "commuting", "subway", "metro", "train"],
        "calls": ["call", "calls", "meeting", "mic", "microphone"],
        "music": ["music", "sound", "audio"],
        "gym": ["gym", "running", "workout", "sport"],
        "gaming": ["gaming", "game", "latency"],
        "office": ["office", "study", "work"]
    }
    for name, needles in mapping.items():
        if any(n in q for n in needles):
            cases.append(name)
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    currency = detect_currency(args.query)
    region = detect_region(args.query, currency)
    budget_max = detect_budget(args.query)
    normalized = {
        "product_category": "bluetooth_earbuds",
        "region": region,
        "currency": currency,
        "budget": {"min": None, "max": budget_max, "currency": currency},
        "brand_scope": detect_brands(args.query),
        "marketplaces": ["JD", "Tmall", "official_store"] if region == "China" else [],
        "use_case": detect_use_case(args.query),
        "phone_ecosystem": "iPhone" if re.search(r"\biphone\b", args.query, re.I) else ("Android" if re.search(r"\bandroid\b", args.query, re.I) else None),
        "must_have": [],
        "nice_to_have": [],
        "deal_breakers": [],
        "purchase_timeline": None,
        "notes": ["Heuristic MVP normalization; agent should verify assumptions."]
    }
    print(json.dumps(normalized, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
