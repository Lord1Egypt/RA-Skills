#!/usr/bin/env python3
"""
Amazon FBA Fee Calculator — Know your REAL profit before you sell
Calculates all Amazon fees: referral, FBA fulfillment, storage, and more.
Updated for 2026 fee schedule.
"""

import json
import sys

# 2026 Amazon FBA Fee Schedule (US marketplace)
# Source: https://sellercentral.amazon.com/help/hub/reference/G200336920

# Referral fees by category (percentage)
REFERRAL_FEES = {
    "default": 0.15,           # 15% for most categories
    "amazon_device_accessories": 0.45,
    "automotive": 0.12,
    "baby": 0.08,              # 8% for items <= $10, 15% for > $10
    "beauty": 0.08,            # 8% for items <= $10, 15% for > $10
    "books": 0.15,
    "clothing": 0.17,
    "electronics": 0.08,
    "furniture": 0.15,
    "grocery": 0.08,           # 8% for items <= $15, 15% for > $15
    "health": 0.08,            # 8% for items <= $10, 15% for > $10
    "home": 0.15,
    "jewelry": 0.20,
    "kitchen": 0.15,
    "lawn_garden": 0.15,
    "pet": 0.15,
    "shoes": 0.15,
    "sports": 0.15,
    "toys": 0.15,
    "video_games": 0.15,
    "watches": 0.16,
}

# FBA fulfillment fees (2026) — based on size tier and weight
# Small Standard (up to 15" x 12" x 0.75", up to 1 lb)
# Large Standard (up to 18" x 14" x 8", up to 20 lbs)
# Large Bulky, Extra-Large

FBA_FEES = {
    "small_standard": [
        (6, 3.22),     # 6 oz or less
        (12, 3.40),    # 6-12 oz
        (16, 3.58),    # 12-16 oz
    ],
    "large_standard": [
        (4, 3.86),     # 4 oz or less
        (8, 4.08),     # 4-8 oz
        (12, 4.32),    # 8-12 oz
        (16, 5.32),    # 12-16 oz
        (32, 5.77),    # 1-1.5 lb
        (48, 6.15),    # 1.5-2 lb
        (80, 6.53),    # 2-2.5 lb
        (128, 6.92),   # 2.5-3 lb
        (320, 7.11),   # 3+ lb (base), +$0.16/half lb after
    ],
}

# Monthly storage fees (per cubic foot)
STORAGE_FEES = {
    "jan_sep": 0.87,     # January-September
    "oct_dec": 2.40,     # October-December (peak)
}

# Minimum referral fee
MIN_REFERRAL_FEE = 0.30


def get_size_tier(length, width, height, weight_oz):
    """Determine Amazon size tier."""
    longest = max(length, width, height)
    median = sorted([length, width, height])[1]
    shortest = min(length, width, height)

    if longest <= 15 and median <= 12 and shortest <= 0.75 and weight_oz <= 16:
        return "small_standard"
    elif longest <= 18 and median <= 14 and shortest <= 8 and weight_oz <= 320:
        return "large_standard"
    elif longest <= 59 and median <= 33 and shortest <= 33 and weight_oz <= 50 * 16:
        return "large_bulky"
    else:
        return "extra_large"


def calculate_fba_fee(weight_oz, size_tier):
    """Calculate FBA fulfillment fee based on weight and size tier."""
    if size_tier in FBA_FEES:
        for max_oz, fee in FBA_FEES[size_tier]:
            if weight_oz <= max_oz:
                return fee
        # Over max weight in tier — use formula
        if size_tier == "large_standard":
            base = FBA_FEES["large_standard"][-1][1]
            extra_half_lbs = max(0, (weight_oz - 48) / 8)
            return base + (extra_half_lbs * 0.16)

    # Large bulky/extra-large
    if size_tier == "large_bulky":
        return 9.73 + max(0, (weight_oz / 16 - 1)) * 0.42
    else:
        return 26.33 + max(0, (weight_oz / 16 - 1)) * 0.38


def calculate_referral_fee(price, category="default"):
    """Calculate Amazon referral fee."""
    rate = REFERRAL_FEES.get(category, REFERRAL_FEES["default"])

    # Category-specific thresholds
    if category in ["baby", "beauty", "health"] and price <= 10:
        rate = 0.08
    elif category == "grocery" and price <= 15:
        rate = 0.08

    fee = price * rate
    return max(fee, MIN_REFERRAL_FEE)


def calculate_storage_fee(length, width, height, month=6):
    """Calculate monthly storage fee."""
    cubic_feet = (length * width * height) / 1728  # Convert cubic inches to cubic feet
    if month >= 10:  # Oct-Dec
        rate = STORAGE_FEES["oct_dec"]
    else:
        rate = STORAGE_FEES["jan_sep"]
    return cubic_feet * rate


def full_profitability(
    selling_price,
    product_cost,
    shipping_to_fba=0,
    weight_oz=16,
    length=10,
    width=8,
    height=4,
    category="default",
    monthly_units=100,
    ppc_cost_per_unit=0,
):
    """Full profitability calculation."""
    size_tier = get_size_tier(length, width, height, weight_oz)
    referral_fee = calculate_referral_fee(selling_price, category)
    fba_fee = calculate_fba_fee(weight_oz, size_tier)
    storage_fee = calculate_storage_fee(length, width, height) / max(monthly_units, 1)

    total_amazon_fees = referral_fee + fba_fee + storage_fee
    total_cost = product_cost + shipping_to_fba + ppc_cost_per_unit + total_amazon_fees

    profit_per_unit = selling_price - total_cost
    margin = (profit_per_unit / selling_price * 100) if selling_price > 0 else 0
    roi = (profit_per_unit / (product_cost + shipping_to_fba) * 100) if (product_cost + shipping_to_fba) > 0 else 0

    monthly_profit = profit_per_unit * monthly_units
    annual_profit = monthly_profit * 12

    result = {
        "selling_price": selling_price,
        "product_cost": product_cost,
        "shipping_to_fba": shipping_to_fba,
        "size_tier": size_tier,
        "referral_fee": round(referral_fee, 2),
        "fba_fulfillment_fee": round(fba_fee, 2),
        "storage_fee_per_unit": round(storage_fee, 2),
        "ppc_cost_per_unit": ppc_cost_per_unit,
        "total_amazon_fees": round(total_amazon_fees, 2),
        "total_cost_per_unit": round(total_cost, 2),
        "profit_per_unit": round(profit_per_unit, 2),
        "margin_pct": round(margin, 1),
        "roi_pct": round(roi, 1),
        "monthly_units": monthly_units,
        "monthly_profit": round(monthly_profit, 2),
        "annual_profit": round(annual_profit, 2),
        "break_even_price": round(total_cost, 2),
    }

    return result


def print_report(result):
    """Pretty print the profitability report."""
    profitable = result["profit_per_unit"] > 0

    print(f"\n{'=' * 50}")
    print(f"💰 AMAZON FBA PROFITABILITY REPORT")
    print(f"{'=' * 50}")

    print(f"\n📦 Product Details:")
    print(f"   Selling Price:     ${result['selling_price']:.2f}")
    print(f"   Product Cost:      ${result['product_cost']:.2f}")
    print(f"   Ship to FBA:       ${result['shipping_to_fba']:.2f}")
    print(f"   Size Tier:         {result['size_tier'].replace('_', ' ').title()}")

    print(f"\n💸 Amazon Fees:")
    print(f"   Referral Fee:      ${result['referral_fee']:.2f}")
    print(f"   FBA Fulfillment:   ${result['fba_fulfillment_fee']:.2f}")
    print(f"   Storage/unit:      ${result['storage_fee_per_unit']:.2f}")
    if result['ppc_cost_per_unit'] > 0:
        print(f"   PPC/unit:          ${result['ppc_cost_per_unit']:.2f}")
    print(f"   ─────────────────────────")
    print(f"   Total Fees:        ${result['total_amazon_fees']:.2f}")

    print(f"\n{'🟢' if profitable else '🔴'} Profitability:")
    print(f"   Total Cost/Unit:   ${result['total_cost_per_unit']:.2f}")
    print(f"   Profit/Unit:       ${result['profit_per_unit']:.2f}")
    print(f"   Margin:            {result['margin_pct']}%")
    print(f"   ROI:               {result['roi_pct']}%")

    print(f"\n📊 Projections ({result['monthly_units']} units/month):")
    print(f"   Monthly Profit:    ${result['monthly_profit']:.2f}")
    print(f"   Annual Profit:     ${result['annual_profit']:.2f}")
    print(f"   Break-even Price:  ${result['break_even_price']:.2f}")

    if not profitable:
        gap = abs(result['profit_per_unit'])
        print(f"\n⚠️  You need to either:")
        print(f"   • Raise price by ${gap:.2f}+ to break even")
        print(f"   • Lower COGS by ${gap:.2f}")
        print(f"   • Or reduce PPC spend")

    print()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 calculator.py <selling_price> <product_cost> [options]")
        print()
        print("Options:")
        print("  --ship COST        Shipping to FBA per unit (default: 0)")
        print("  --weight OZ        Weight in ounces (default: 16)")
        print("  --dims L W H       Dimensions in inches (default: 10 8 4)")
        print("  --category CAT     Product category (default: default)")
        print("  --units N          Monthly units sold (default: 100)")
        print("  --ppc COST         PPC cost per unit (default: 0)")
        print()
        print("Examples:")
        print("  python3 calculator.py 9.95 2.00")
        print("  python3 calculator.py 9.95 2.00 --ship 0.50 --weight 8 --category grocery --units 200")
        print()
        print("Categories: " + ", ".join(sorted(REFERRAL_FEES.keys())))
        sys.exit(1)

    price = float(sys.argv[1])
    cost = float(sys.argv[2])

    # Parse optional args
    kwargs = {}
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--ship":
            kwargs["shipping_to_fba"] = float(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == "--weight":
            kwargs["weight_oz"] = float(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == "--dims":
            kwargs["length"] = float(sys.argv[i+1])
            kwargs["width"] = float(sys.argv[i+2])
            kwargs["height"] = float(sys.argv[i+3])
            i += 4
        elif sys.argv[i] == "--category":
            kwargs["category"] = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--units":
            kwargs["monthly_units"] = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == "--ppc":
            kwargs["ppc_cost_per_unit"] = float(sys.argv[i+1])
            i += 2
        else:
            i += 1

    result = full_profitability(price, cost, **kwargs)
    print_report(result)
