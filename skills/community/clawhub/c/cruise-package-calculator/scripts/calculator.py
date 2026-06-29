#!/usr/bin/env python3
"""
Cruise Package Calculator — helper script.

Used by the cruise-package-calculator skill for multi-package or large-family
scenarios where mental math becomes unreliable.

Usage:
    echo '<json>' | python calculator.py

JSON input schema:
{
  "cruise_line": "Royal Caribbean" | "Carnival" | "NCL" | "MSC" | "Princess"
                 | "Celebrity" | "Holland America" | "Disney",
  "nights": int,
  "adults": int,
  "kids": int,
  "packages": [
    {
      "type": "drink" | "wifi" | "dining" | "photo" | "bundle",
      "name": "Deluxe Beverage Package",
      "daily_price": float,
      "purchased": "pre_cruise" | "onboard",
      "gratuity_already_included": bool
    }
  ],
  "consumption_per_adult_per_day": {
    "cocktails": int,
    "beers": int,
    "wine_glasses": int,
    "sodas": int,
    "premium_coffees": int,
    "bottled_waters": int
  }
}

Output: structured JSON with break-even, value score, à-la-carte cost, verdict.
"""
import json
import sys
from typing import Any

# Average à-la-carte unit prices (USD), midpoint of cruise-industry ranges.
UNIT_PRICES = {
    "cocktails": 14.00,
    "beers": 9.00,
    "wine_glasses": 13.00,
    "sodas": 4.00,
    "premium_coffees": 5.00,
    "bottled_waters": 4.50,
}

# Default gratuity rates by line.
GRATUITY = {
    "Royal Caribbean": 0.18,
    "Carnival": 0.18,
    "NCL": 0.20,
    "Norwegian Cruise Line": 0.20,
    "MSC": 0.18,
    "Princess": 0.00,  # already bundled in Plus/Premier
    "Celebrity": 0.20,
    "Holland America": 0.18,
    "Disney": 0.00,
}


def effective_daily_cost(daily_price: float, line: str, already_included: bool) -> float:
    if already_included:
        return daily_price
    rate = GRATUITY.get(line, 0.18)
    return daily_price * (1 + rate)


def alacarte_daily_cost(consumption: dict[str, int]) -> float:
    return sum(consumption.get(k, 0) * UNIT_PRICES[k] for k in UNIT_PRICES)


def value_score(savings_pct: float, convenience: int, risk: int, pre_discount_pct: float) -> float:
    # Normalize savings_pct → 0..100
    if savings_pct >= 30: s = 100
    elif savings_pct >= 15: s = 80
    elif savings_pct >= 5: s = 60
    elif savings_pct >= 0: s = 40
    elif savings_pct >= -5: s = 25
    else: s = 0

    # Normalize pre-cruise discount → 0..100
    if pre_discount_pct >= 25: p = 100
    elif pre_discount_pct >= 15: p = 80
    elif pre_discount_pct >= 5: p = 50
    elif pre_discount_pct >= 0: p = 20
    else: p = 0

    return round(s * 0.50 + convenience * 0.20 + risk * 0.15 + p * 0.15, 1)


def verdict_from_score(score: float) -> str:
    if score >= 75: return "BUY"
    if score >= 60: return "BUY (lean)"
    if score >= 45: return "DEPENDS"
    if score >= 30: return "SKIP (lean)"
    return "SKIP"


def analyze_drink_package(pkg: dict[str, Any], req: dict[str, Any]) -> dict[str, Any]:
    line = req["cruise_line"]
    nights = req["nights"]
    adults = req.get("adults", 1)
    consumption = req.get("consumption_per_adult_per_day", {})
    convenience = req.get("convenience_score", 60)
    risk = req.get("risk_score", 60)
    pre_disc_pct = req.get("pre_cruise_discount_pct", 15)

    edc = effective_daily_cost(pkg["daily_price"], line, pkg.get("gratuity_already_included", False))
    package_total = edc * nights * adults

    acc_daily_per_adult = alacarte_daily_cost(consumption)
    acc_total = acc_daily_per_adult * nights * adults

    savings_pct = ((acc_total - package_total) / acc_total * 100) if acc_total > 0 else -100
    score = value_score(savings_pct, convenience, risk, pre_disc_pct)

    breakeven_drinks = edc / 14.00  # at avg cocktail price
    actual_drinks = sum(consumption.get(k, 0) for k in ["cocktails", "beers", "wine_glasses"])

    return {
        "package_name": pkg.get("name", "drink package"),
        "package_total_for_household": round(package_total, 2),
        "alacarte_total_for_household": round(acc_total, 2),
        "net_position": round(package_total - acc_total, 2),
        "savings_pct": round(savings_pct, 1),
        "breakeven_drinks_per_day": round(breakeven_drinks, 1),
        "user_drinks_per_day": actual_drinks,
        "value_score": score,
        "verdict": verdict_from_score(score),
    }


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        print(json.dumps({"error": "No JSON provided on stdin"}))
        sys.exit(1)
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    results = []
    for pkg in req.get("packages", []):
        if pkg.get("type") == "drink":
            results.append(analyze_drink_package(pkg, req))
        else:
            results.append({
                "package_name": pkg.get("name"),
                "type": pkg.get("type"),
                "note": "Non-drink package handler not implemented in this minimal script. Use inline math via SKILL.md formulas.",
            })

    print(json.dumps({"results": results}, indent=2))


if __name__ == "__main__":
    main()
