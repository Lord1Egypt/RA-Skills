#!/usr/bin/env python3
"""portfolio_risk.py - position sizing and portfolio heat for US equities.

Risk-first sizing: size the trade from the stop distance, then check the
portfolio against the user's own risk rules. Stdlib only.

Usage:
    python3 portfolio_risk.py --equity 25000 --risk-pct 0.5 --entry 182.40 --stop 178.10
    python3 portfolio_risk.py --equity 25000 --risk-pct 0.5 --entry 182.40 --stop 178.10 \
        --target 195.00 --open-positions positions.csv --out plan.json

positions.csv header: symbol,shares,entry,stop,sector
Short positions are supported with --side short (stop above entry).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys

DEFAULTS = {
    "risk_pct": 0.5,
    "max_position_pct": 10.0,
    "max_sector_pct": 25.0,
    "max_heat_pct": 6.0,
    "daily_loss_pct": 2.0,
}


def load_positions(path: str) -> list:
    positions = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = {f.strip().lower(): f for f in (reader.fieldnames or [])}
        for key in ("symbol", "shares", "entry", "stop"):
            if key not in fields:
                raise SystemExit(f"positions.csv must have a '{key}' column.")
        for row in reader:
            try:
                positions.append(
                    {
                        "symbol": str(row[fields["symbol"]]).strip().upper(),
                        "shares": float(row[fields["shares"]]),
                        "entry": float(row[fields["entry"]]),
                        "stop": float(row[fields["stop"]]),
                        "sector": str(row.get(fields.get("sector", ""), "") or "unknown").strip() or "unknown",
                        "side": str(row.get(fields.get("side", ""), "") or "long").strip().lower(),
                    }
                )
            except (TypeError, ValueError):
                continue
    return positions


def position_risk(entry: float, stop: float, shares: float, side: str) -> float:
    per_share = abs(entry - stop)
    return per_share * shares


def build_plan(args, positions: list) -> dict:
    side = args.side.lower()
    per_share_risk = abs(args.entry - args.stop)
    if per_share_risk == 0:
        raise SystemExit("error: entry and stop are identical - no risk per share.")

    risk_budget = args.equity * (args.risk_pct / 100.0)
    shares = math.floor(risk_budget / per_share_risk)
    if shares <= 0:
        return {
            "error": "Risk budget too small for this stop distance.",
            "risk_budget_usd": round(risk_budget, 2),
            "risk_per_share": round(per_share_risk, 4),
            "max_shares": 0,
            "recommendation": "Do not trade. Either widen the stop (with a smaller size) or skip the setup.",
        }

    position_value = shares * args.entry
    position_pct = position_value / args.equity * 100.0
    dollar_risk = shares * per_share_risk

    open_risk = sum(position_risk(p["entry"], p["stop"], p["shares"], p.get("side", "long")) for p in positions)
    open_heat_pct = open_risk / args.equity * 100.0

    sector_value = 0.0
    for p in positions:
        if p.get("sector") == args.sector and p.get("side", "long") != "short":
            sector_value += p["shares"] * p["entry"]
    sector_pct = (sector_value + position_value) / args.equity * 100.0

    r_multiple = None
    if args.target:
        if side == "short":
            r_multiple = round((args.entry - args.target) / per_share_risk, 2)
        else:
            r_multiple = round((args.target - args.entry) / per_share_risk, 2)

    violations = []
    if position_pct > args.max_position_pct:
        violations.append(
            f"Position {position_pct:.2f}% exceeds max single position {args.max_position_pct}%. Reduce shares."
        )
    if sector_pct > args.max_sector_pct:
        violations.append(
            f"Sector '{args.sector}' would be {sector_pct:.2f}% of equity, above the {args.max_sector_pct}% cap."
        )
    if open_heat_pct + args.risk_pct > args.max_heat_pct:
        violations.append(
            f"Portfolio heat after this trade would be {open_heat_pct + args.risk_pct:.2f}%, above the {args.max_heat_pct}% cap."
        )
    if args.risk_pct > 1.0:
        violations.append(f"Risk per trade {args.risk_pct}% is above the 1% hard ceiling.")

    if args.overnight and args.risk_pct > 0.5:
        violations.append("Overnight gap risk: recommended size halved - use half the shares above.")

    plan = {
        "inputs": {
            "equity_usd": args.equity,
            "risk_pct": args.risk_pct,
            "entry": args.entry,
            "stop": args.stop,
            "target": args.target,
            "side": side,
            "sector": args.sector,
        },
        "sizing": {
            "risk_budget_usd": round(risk_budget, 2),
            "risk_per_share": round(per_share_risk, 4),
            "max_shares": int(shares),
            "position_value_usd": round(position_value, 2),
            "position_pct_of_equity": round(position_pct, 2),
            "dollar_risk_usd": round(dollar_risk, 2),
            "r_multiple_to_target": r_multiple,
        },
        "portfolio": {
            "open_positions": len(positions),
            "open_risk_usd": round(open_risk, 2),
            "open_heat_pct": round(open_heat_pct, 2),
            "heat_after_trade_pct": round(open_heat_pct + args.risk_pct, 2),
            "sector_pct_after_trade": round(sector_pct, 2),
        },
        "rules": {
            "max_position_pct": args.max_position_pct,
            "max_sector_pct": args.max_sector_pct,
            "max_heat_pct": args.max_heat_pct,
            "daily_loss_limit_pct": args.daily_loss_pct,
        },
        "violations": violations,
        "approved_for_review": not violations,
        "execution": {
            "gate": "HUMAN APPROVAL REQUIRED - this tool does not place orders.",
            "checklist": [
                "Thesis written in one sentence",
                "Stop defined and placed before entry",
                "Size from the plan above, not from conviction",
                "Earnings date checked (gap risk)",
                "Liquidity checked (avg dollar volume)",
                "No single position above the cap",
                "Broker order typed and reviewed manually",
            ],
        },
        "disclaimer": "Risk-first sizing tool. Not investment advice. Verify every input before trading.",
    }
    return plan


def render(plan: dict) -> str:
    if "error" in plan:
        return f"BLOCKED: {plan['error']}\n  risk budget: ${plan['risk_budget_usd']}\n  risk per share: ${plan['risk_per_share']}"
    s, p = plan["sizing"], plan["portfolio"]
    lines = [
        "=== POSITION PLAN (review only - no order is placed) ===",
        f"Equity            : ${plan['inputs']['equity_usd']:,.2f}",
        f"Risk per trade    : {plan['inputs']['risk_pct']}%  ->  ${s['risk_budget_usd']:,.2f}",
        f"Entry / Stop      : ${plan['inputs']['entry']} / ${plan['inputs']['stop']}",
        f"Risk per share    : ${s['risk_per_share']}",
        f"SIZE              : {s['max_shares']} shares (${s['position_value_usd']:,.2f}, {s['position_pct_of_equity']}% of equity)",
        f"Dollar risk       : ${s['dollar_risk_usd']:,.2f}",
    ]
    if s["r_multiple_to_target"] is not None:
        lines.append(f"R multiple to tgt : {s['r_multiple_to_target']}R")
    lines += [
        "",
        f"Open heat         : {p['open_heat_pct']}%  ->  after trade {p['heat_after_trade_pct']}% (cap {plan['rules']['max_heat_pct']}%)",
        f"Sector exposure   : {p['sector_pct_after_trade']}% (cap {plan['rules']['max_sector_pct']}%)",
        "",
    ]
    if plan["violations"]:
        lines.append("VIOLATIONS:")
        lines += [f"  ! {v}" for v in plan["violations"]]
    else:
        lines.append("No rule violations detected.")
    lines += ["", plan["execution"]["gate"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Risk-first position sizing and portfolio checks.")
    ap.add_argument("--equity", type=float, required=True, help="Account equity in USD")
    ap.add_argument("--risk-pct", type=float, default=DEFAULTS["risk_pct"], help="Risk per trade as %% of equity")
    ap.add_argument("--entry", type=float, required=True)
    ap.add_argument("--stop", type=float, required=True)
    ap.add_argument("--target", type=float, help="Optional target price for R multiple")
    ap.add_argument("--side", default="long", choices=["long", "short"])
    ap.add_argument("--sector", default="unknown", help="Sector label used for concentration checks")
    ap.add_argument("--open-positions", help="CSV of open positions")
    ap.add_argument("--max-position-pct", type=float, default=DEFAULTS["max_position_pct"])
    ap.add_argument("--max-sector-pct", type=float, default=DEFAULTS["max_sector_pct"])
    ap.add_argument("--max-heat-pct", type=float, default=DEFAULTS["max_heat_pct"])
    ap.add_argument("--daily-loss-pct", type=float, default=DEFAULTS["daily_loss_pct"])
    ap.add_argument("--overnight", action="store_true", help="Flag gap risk (halves recommended size)")
    ap.add_argument("--out", help="Write JSON plan to this path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.equity <= 0:
        print("error: --equity must be positive.", file=sys.stderr)
        return 2
    if args.open_positions:
        if not os.path.exists(args.open_positions):
            print(f"error: positions file not found: {args.open_positions}", file=sys.stderr)
            return 2
        positions = load_positions(args.open_positions)
    else:
        positions = []

    plan = build_plan(args, positions)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(plan, fh, indent=2)
        print(f"written: {args.out}")
    print(json.dumps(plan, indent=2) if args.json else render(plan))
    return 0 if not plan.get("violations") else 1


if __name__ == "__main__":
    raise SystemExit(main())
