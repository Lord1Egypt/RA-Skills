#!/usr/bin/env python3
"""Calculate production and delivery milestones for a custom order."""

import argparse
import math
from datetime import date, timedelta


def business_days_ahead(start: date, days: int) -> date:
    """Return the date that is *days* business days after *start*."""
    current = start
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Mon–Fri
            added += 1
    return current


def calculate_timeline(
    order_date: date,
    production_days: int = 7,
    shipping_days: int = 5,
    rush: bool = False,
) -> dict:
    effective_production = (
        max(1, math.ceil(production_days * 0.6)) if rush else production_days
    )

    modification_deadline = order_date + timedelta(hours=24)
    production_start = business_days_ahead(order_date, 1)
    production_complete = business_days_ahead(order_date, effective_production)
    ship_date = business_days_ahead(production_complete, 1)
    delivery_earliest = business_days_ahead(ship_date, shipping_days - 1)
    delivery_latest = business_days_ahead(ship_date, shipping_days + 1)

    return {
        "order_date": order_date,
        "rush": rush,
        "production_days_used": effective_production,
        "modification_deadline": modification_deadline,
        "production_start": production_start,
        "production_complete": production_complete,
        "ship_date": ship_date,
        "delivery_window": (delivery_earliest, delivery_latest),
    }


def format_timeline(t: dict) -> str:
    lines = [
        "=" * 50,
        "  CUSTOM ORDER TIMELINE",
        "=" * 50,
        f"  Order placed:          {t['order_date']}",
        f"  Modification deadline: {t['modification_deadline'].strftime('%Y-%m-%d %H:%M')}",
        f"  Production start:      {t['production_start']}",
        f"  Production days:       {t['production_days_used']}"
        + (" (rush −40%)" if t["rush"] else ""),
        f"  Production complete:   {t['production_complete']}",
        f"  Ships on:              {t['ship_date']}",
        f"  Estimated delivery:    {t['delivery_window'][0]} – {t['delivery_window'][1]}",
    ]
    if t["rush"]:
        lines.append("")
        lines.append("  ⚡ Rush order — a surcharge applies. Confirm with")
        lines.append("    the customer before committing to this timeline.")
    lines.append("=" * 50)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate ETA milestones for a custom order."
    )
    parser.add_argument(
        "--order-date",
        required=True,
        type=lambda s: date.fromisoformat(s),
        help="Order date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--production-days",
        type=int,
        default=7,
        help="Business days needed for production (default: 7).",
    )
    parser.add_argument(
        "--shipping-days",
        type=int,
        default=5,
        help="Business days for shipping transit (default: 5).",
    )
    parser.add_argument(
        "--rush",
        action="store_true",
        help="Rush order — reduces production time by 40%%.",
    )

    args = parser.parse_args()
    timeline = calculate_timeline(
        order_date=args.order_date,
        production_days=args.production_days,
        shipping_days=args.shipping_days,
        rush=args.rush,
    )
    print(format_timeline(timeline))


if __name__ == "__main__":
    main()
