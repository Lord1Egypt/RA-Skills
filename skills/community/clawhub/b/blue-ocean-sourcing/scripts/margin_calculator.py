#!/usr/bin/env python3
"""
Margin calculator for blue-ocean product sourcing.

Accepts cost inputs and a target margin, then outputs a formatted pricing
report including suggested retail price, actual margin, and break-even units.
"""

import argparse
import math
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Calculate retail price, margin, and break-even for a blue-ocean product."
    )
    parser.add_argument(
        "--cogs",
        type=float,
        required=True,
        help="Cost of goods sold per unit (e.g. factory price + packaging).",
    )
    parser.add_argument(
        "--shipping",
        type=float,
        default=0.0,
        help="Per-unit shipping / logistics cost (default: 0).",
    )
    parser.add_argument(
        "--marketing-pct",
        type=float,
        default=25.0,
        help="Marketing spend as a percentage of revenue (default: 25).",
    )
    parser.add_argument(
        "--target-margin",
        type=float,
        default=40.0,
        help="Desired net margin as a percentage of revenue (default: 40).",
    )
    parser.add_argument(
        "--aov",
        type=float,
        default=None,
        help="Optional: merchant's stated AOV for comparison.",
    )
    parser.add_argument(
        "--fixed-costs",
        type=float,
        default=0.0,
        help="Monthly fixed costs (rent, salaries, SaaS) for break-even calc (default: 0).",
    )
    return parser.parse_args(argv)


def calculate(cogs, shipping, marketing_pct, target_margin):
    """Return a dict with pricing metrics.

    The retail price is derived so that after subtracting COGS, shipping, and
    marketing spend (as % of revenue), the remaining margin equals the target.

    retail = landed_cost / (1 - marketing_pct/100 - target_margin/100)
    """
    landed_cost = cogs + shipping
    non_cost_share = 1.0 - (marketing_pct / 100.0) - (target_margin / 100.0)

    if non_cost_share <= 0:
        return {
            "error": (
                f"Marketing ({marketing_pct}%) + target margin ({target_margin}%) "
                f"= {marketing_pct + target_margin}% — leaves no room for COGS. "
                "Lower one of them."
            )
        }

    retail = landed_cost / non_cost_share
    marketing_abs = retail * (marketing_pct / 100.0)
    margin_abs = retail * (target_margin / 100.0)
    actual_margin_pct = (margin_abs / retail) * 100.0 if retail else 0.0
    markup = retail / landed_cost if landed_cost else float("inf")

    return {
        "landed_cost": landed_cost,
        "suggested_retail": retail,
        "marketing_spend": marketing_abs,
        "margin_abs": margin_abs,
        "actual_margin_pct": actual_margin_pct,
        "markup": markup,
    }


def break_even_units(fixed_costs, margin_per_unit):
    if margin_per_unit <= 0:
        return None
    return math.ceil(fixed_costs / margin_per_unit)


def format_report(metrics, args):
    if "error" in metrics:
        return f"\n⚠  {metrics['error']}\n"

    lines = [
        "",
        "=" * 52,
        "  BLUE-OCEAN MARGIN REPORT",
        "=" * 52,
        "",
        "  COST STRUCTURE",
        f"    COGS per unit:          ${args.cogs:>10.2f}",
        f"    Shipping per unit:      ${args.shipping:>10.2f}",
        f"    Landed cost:            ${metrics['landed_cost']:>10.2f}",
        "",
        "  PRICING",
        f"    Suggested retail:       ${metrics['suggested_retail']:>10.2f}",
        f"    Markup (retail/landed):  {metrics['markup']:>10.2f}x",
        "",
        "  MARGIN BREAKDOWN (per unit)",
        f"    Marketing ({args.marketing_pct:.0f}% of rev): ${metrics['marketing_spend']:>10.2f}",
        f"    Net margin:             ${metrics['margin_abs']:>10.2f}",
        f"    Net margin %:            {metrics['actual_margin_pct']:>9.1f}%",
    ]

    if args.fixed_costs > 0:
        be = break_even_units(args.fixed_costs, metrics["margin_abs"])
        lines += [
            "",
            "  BREAK-EVEN",
            f"    Monthly fixed costs:    ${args.fixed_costs:>10.2f}",
            f"    Break-even units/month:  {be:>10d}" if be else "    Break-even units/month:       N/A",
        ]

    if args.aov is not None:
        delta = args.aov - metrics["suggested_retail"]
        direction = "above" if delta > 0 else "below"
        lines += [
            "",
            "  AOV COMPARISON",
            f"    Stated AOV:             ${args.aov:>10.2f}",
            f"    Suggested retail:       ${metrics['suggested_retail']:>10.2f}",
            f"    Difference:             ${abs(delta):>10.2f} {direction}",
        ]
        if delta < 0:
            shortfall_pct = (abs(delta) / metrics["suggested_retail"]) * 100
            lines.append(
                f"    → Retail is {shortfall_pct:.1f}% above stated AOV. "
                "Consider lowering COGS or accepting a thinner margin."
            )

    lines += ["", "=" * 52, ""]
    return "\n".join(lines)


def main(argv=None):
    args = parse_args(argv)

    if args.marketing_pct < 0 or args.marketing_pct > 100:
        print("Error: --marketing-pct must be between 0 and 100.", file=sys.stderr)
        sys.exit(1)
    if args.target_margin < 0 or args.target_margin > 100:
        print("Error: --target-margin must be between 0 and 100.", file=sys.stderr)
        sys.exit(1)

    metrics = calculate(args.cogs, args.shipping, args.marketing_pct, args.target_margin)
    print(format_report(metrics, args))


if __name__ == "__main__":
    main()
