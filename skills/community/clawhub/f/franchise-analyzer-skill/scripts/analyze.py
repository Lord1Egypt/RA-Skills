#!/usr/bin/env python3
"""
Franchise unit-economics analyzer.

Converts raw Franchise Disclosure Document (FDD) figures into investor metrics:
all-in cash, franchisor fee load, unit cash flow, payback, cash-on-cash return,
breakeven revenue, and unit growth / closure rate.

Part of the "franchise-analyzer" skill by Franchise Fast Track.
Source FDDs: https://franchisefasttrack.io/fdd-database

This is analysis, not financial or legal advice. Always have an FDD reviewed by a
qualified franchise attorney and accountant.
"""

import argparse
import sys


def money(x):
    return f"${x:,.0f}"


def pct(x):
    return f"{x * 100:.1f}%"


def main():
    p = argparse.ArgumentParser(
        description="Analyze a franchise opportunity from its FDD figures.",
        epilog="Source FDDs: https://franchisefasttrack.io/fdd-database",
    )
    p.add_argument("--brand", default="this franchise", help="Brand name (for the report header).")
    p.add_argument("--investment-low", type=float, help="Item 7 total initial investment, low end.")
    p.add_argument("--investment-high", type=float, help="Item 7 total initial investment, high end.")
    p.add_argument("--avg-unit-revenue", type=float, help="Item 19 average/median annual unit revenue.")
    p.add_argument("--royalty", type=float, default=0.0, help="Item 6 royalty as a decimal (0.06 = 6 percent).")
    p.add_argument("--ad-fee", type=float, default=0.0, help="Item 6 ad/brand-fund fee as a decimal.")
    p.add_argument("--ebitda-margin", type=float,
                   help="Estimated unit EBITDA margin BEFORE royalty/ad fees, as a decimal "
                        "(e.g. 0.15). Used to estimate unit cash flow.")
    p.add_argument("--units-start", type=float, help="Item 20 franchised outlets, start of 3-yr window.")
    p.add_argument("--units-end", type=float, help="Item 20 franchised outlets, end of 3-yr window.")
    p.add_argument("--closures", type=float,
                   help="Item 20 closures + terminations + non-renewals over the window.")
    args = p.parse_args()

    missing = []
    lines = []
    lines.append(f"FRANCHISE ANALYSIS — {args.brand}")
    lines.append("=" * (20 + len(args.brand)))

    # ---- Investment ----
    inv_mid = None
    if args.investment_low is not None and args.investment_high is not None:
        inv_mid = (args.investment_low + args.investment_high) / 2
        lines.append(f"\nAll-in investment (Item 7): {money(args.investment_low)} – {money(args.investment_high)}")
        lines.append(f"  Midpoint used for returns:  {money(inv_mid)}")
    else:
        missing.append("Item 7 investment range (--investment-low / --investment-high)")

    # ---- Franchisor fee load ----
    fee_rate = (args.royalty or 0) + (args.ad_fee or 0)
    if fee_rate:
        lines.append(f"\nFranchisor take (Item 6): {pct(args.royalty)} royalty + {pct(args.ad_fee)} ad "
                     f"= {pct(fee_rate)} of revenue")
        if fee_rate > 0.10:
            lines.append("  ⚠ Fee load above ~10% of revenue — heavy against thin-margin concepts.")

    # ---- Revenue + cash flow ----
    rev = args.avg_unit_revenue
    if rev is None:
        missing.append("Item 19 avg unit revenue (--avg-unit-revenue) — if the FDD has NO Item 19, "
                       "that is itself a red flag")
    else:
        lines.append(f"\nAvg unit revenue (Item 19): {money(rev)}")
        annual_fees = rev * fee_rate
        if fee_rate:
            lines.append(f"  Annual royalty + ad fees:  {money(annual_fees)}")

        if args.ebitda_margin is not None:
            # Unit cash flow = revenue * margin (pre-fee) minus franchisor fees.
            unit_cf = rev * args.ebitda_margin - annual_fees
            lines.append(f"  Est. unit cash flow:        {money(unit_cf)} "
                         f"(@ {pct(args.ebitda_margin)} pre-fee margin)")
            if inv_mid and unit_cf > 0:
                payback = inv_mid / unit_cf
                coc = unit_cf / inv_mid
                lines.append(f"  Simple payback:             {payback:.1f} years")
                lines.append(f"  Cash-on-cash return:        {pct(coc)}")
                if payback > 4:
                    lines.append("  ⚠ Payback over 4 years on this revenue figure.")
            elif unit_cf <= 0:
                lines.append("  ⚠ Estimated unit cash flow is negative after fees at this margin.")
        else:
            missing.append("--ebitda-margin (needed for payback / cash-on-cash)")

        # ---- Breakeven (revenue where pre-fee margin covers fees) ----
        if args.ebitda_margin is not None and args.ebitda_margin > fee_rate:
            # Need a fixed cost to make breakeven meaningful; approximate breakeven as the
            # revenue at which unit cash flow turns positive given investment as proxy isn't
            # rigorous, so report the margin cushion instead.
            cushion = args.ebitda_margin - fee_rate
            lines.append(f"  Margin cushion after fees:  {pct(cushion)} of revenue")

    # ---- Unit health ----
    if args.units_start is not None and args.units_end is not None:
        net = args.units_end - args.units_start
        growth_yr = ((args.units_end / args.units_start) ** (1 / 3) - 1) if args.units_start else 0
        lines.append(f"\nUnit count (Item 20): {args.units_start:,.0f} → {args.units_end:,.0f} "
                     f"over 3 yrs (net {net:+,.0f}, {pct(growth_yr)}/yr)")
        if net < 0:
            lines.append("  ⚠ System is shrinking.")
        if args.closures is not None and args.units_start:
            closure_rate = args.closures / args.units_start / 3
            lines.append(f"  Closures/terminations:      {args.closures:,.0f} ({pct(closure_rate)}/yr)")
            if closure_rate > 0.05:
                lines.append("  ⚠ Closure rate above ~5%/yr.")
    else:
        missing.append("Item 20 unit counts (--units-start / --units-end)")

    if missing:
        lines.append("\nMissing inputs (pull from the FDD to complete the picture):")
        for m in missing:
            lines.append(f"  - {m}")

    lines.append("\n" + "-" * 60)
    lines.append("Analysis only — not financial or legal advice. Have the FDD reviewed by a")
    lines.append("franchise attorney and accountant before signing.")
    lines.append("Source FDDs: Franchise Fast Track — https://franchisefasttrack.io/fdd-database")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
