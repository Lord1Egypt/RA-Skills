#!/usr/bin/env python3
"""Debt Blitz Planner — month-by-month payoff simulation for personal debt.

Strategies:
  min-only  : pay minimums everywhere (baseline)
  avalanche : minimums + all spare cash to highest-APR debt (interest-optimal)
  snowball  : minimums + all spare cash to smallest-balance debt (morale-optimal)

Mechanics: monthly interest = balance * APR/12. When a debt is paid off its
minimum is freed and re-routed to the current target (freed-minimum cascade).
Detects negative amortization (minimums < interest) and prints the minimum
survivable payment. All arithmetic in cents (int) to avoid float drift.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

MAX_MONTHS = 600  # 50 years — beyond this, plan is unsustainable


# ---------------------------------------------------------------------------
# Parsing / input

def parse_debt(spec: str) -> dict:
    """Parse NAME,BALANCE,APR,MINIMUM into a dict with cent-precision fields."""
    parts = [p.strip() for p in spec.split(",")]
    if len(parts) != 4:
        raise ValueError(f"debt spec must be NAME,BALANCE,APR,MINIMUM — got: {spec!r}")
    name, balance, apr, minimum = parts
    balance_c = _to_cents(balance)
    apr_f = float(apr)
    min_c = _to_cents(minimum)
    if balance_c <= 0:
        raise ValueError(f"{name}: balance must be positive")
    if apr_f < 0 or apr_f > 200:
        raise ValueError(f"{name}: APR looks wrong ({apr}%). Use annual %, e.g. 22.9")
    if min_c <= 0:
        raise ValueError(f"{name}: minimum must be positive")
    return {"name": name, "balance": balance_c, "apr": apr_f, "min": min_c}


def _to_cents(s: str) -> int:
    f = float(s)
    c = round(f * 100)
    if abs(f * 100 - c) > 0.499:  # tolerate display-level rounding only
        raise ValueError(f"amount {s!r} not representable in cents")
    return c


def fmt(c: int) -> str:
    return f"${c/100:,.2f}"


# ---------------------------------------------------------------------------
# Simulation

def simulate(debts: list[dict], strategy: str, budget_c: int | None = None,
             extra_c: int = 0) -> dict:
    """Run one strategy. budget overrides extra (total monthly payment pool)."""
    live = [{"name": d["name"], "bal": d["balance"], "apr": d["apr"],
             "min": d["min"]} for d in debts]
    total_min = sum(d["min"] for d in live)
    extra_eff = extra_c
    if budget_c is not None:
        extra_eff = budget_c - total_min
        if extra_eff < 0:
            raise ValueError(
                f"budget {fmt(budget_c)} < sum of minimums {fmt(total_min)} — "
                "raise the budget or negotiate minimums")

    interest_total = 0
    payments_total = 0
    schedule = []  # (month, target_name, payment, balance_after)
    payoff_order = []
    month = 0

    while any(d["bal"] > 0 for d in live) and month < MAX_MONTHS:
        month += 1
        # 1. accrue interest on live balances (rounded to cent each month)
        for d in live:
            if d["bal"] > 0:
                interest = round(d["bal"] * d["apr"] / 100.0 / 12.0)
                d["bal"] += interest
                interest_total += interest

        # 2. pool = sum of minimums of still-live debts + extra
        pool = extra_eff + sum(d["min"] for d in live if d["bal"] > 0)

        # 3. pay minimums (capped at payoff)
        for d in live:
            if d["bal"] > 0:
                pay = min(d["min"], d["bal"])
                d["bal"] -= pay
                pool -= pay
                payments_total += pay

        # 4. bury the dead, freeing their minimums next month
        for d in live:
            if d["bal"] <= 0 and d["name"] not in payoff_order:
                payoff_order.append(d["name"])

        # 5. spare cash to target
        if strategy != "min-only" and pool > 0:
            alive = [d for d in live if d["bal"] > 0]
            if alive:
                if strategy == "avalanche":
                    target = max(alive, key=lambda d: (d["apr"], -d["bal"]))
                elif strategy == "snowball":
                    target = min(alive, key=lambda d: (d["bal"], -d["apr"]))
                else:
                    raise ValueError(f"unknown strategy {strategy!r}")
                pay = min(pool, target["bal"])
                target["bal"] -= pay
                pool -= pay
                payments_total += pay
                schedule.append((month, target["name"], pay, target["bal"]))
                if target["bal"] <= 0 and target["name"] not in payoff_order:
                    payoff_order.append(target["name"])

    if month >= MAX_MONTHS and any(d["bal"] > 0 for d in live):
        # find minimum survivable payment: needs > max monthly interest
        worst = max(round(d["balance"] * d["apr"] / 100.0 / 12.0) for d in debts)
        return {
            "ok": False,
            "strategy": strategy,
            "error": (
                f"NOT SOLVABLE in {MAX_MONTHS} months — payments don't cover interest. "
                f"Minimum survivable total payment ≈ {fmt(worst + sum(d['min'] for d in debts if round(d['balance']*d['apr']/100/12) < worst))} "
                "or contact a credit counselor."),
            "remaining": sum(d["bal"] for d in live if d["bal"] > 0),
        }

    return {
        "ok": True,
        "strategy": strategy,
        "months": month,
        "years": round(month / 12, 1),
        "total_interest": interest_total,
        "total_paid": payments_total,
        "payoff_order": payoff_order,
        "schedule": schedule,
    }


# ---------------------------------------------------------------------------
# Reporting

def run_all(debts: list[dict], extra_c: int, budget_c: int | None) -> list[dict]:
    results = []
    for strat in ("min-only", "avalanche", "snowball"):
        r = simulate(debts, strat, budget_c=budget_c, extra_c=extra_c)
        results.append(r)
        if not r.get("ok"):
            break  # baseline failing makes comparisons meaningless
    return results


def print_report(debts, results, extra_c, budget_c) -> None:
    print("=" * 68)
    print("DEBT BLITZ PLANNER")
    print("=" * 68)
    print(f"{'Debt':<18}{'Balance':>12}{'APR':>7}{'Minimum':>11}")
    print("-" * 68)
    for d in debts:
        print(f"{d['name']:<18}{fmt(d['balance']):>12}{d['apr']:>6.2f}%{fmt(d['min']):>11}")
    total_min = sum(d["min"] for d in debts)
    total_bal = sum(d["balance"] for d in debts)
    print("-" * 68)
    print(f"{'TOTAL':<18}{fmt(total_bal):>12}{'':>7}{fmt(total_min):>11}")
    if budget_c is not None:
        print(f"\nMonthly budget: {fmt(budget_c)}  (spare after minimums: {fmt(budget_c - total_min)})")
    else:
        print(f"\nExtra monthly payment: {fmt(extra_c)}  (total committed: {fmt(total_min + extra_c)})")
    print()

    base = next((r for r in results if r["strategy"] == "min-only" and r.get("ok")), None)
    for r in results:
        if not r.get("ok"):
            print(f"!! {r['strategy'].upper()}: {r['error']}")
            continue
        save = base["total_interest"] - r["total_interest"] if base and r is not base else 0
        tag = "  (baseline)" if r["strategy"] == "min-only" else ""
        print(f"{r['strategy']:<11} : {r['months']:>3} months ({r['years']} yr) | "
              f"interest {fmt(r['total_interest'])} | saved {fmt(save)}{tag}")
        if r.get("payoff_order"):
            order = " → ".join(r["payoff_order"])
            print(f"{'':<11}   payoff order: {order}")
    print()

    ok = [r for r in results if r.get("ok") and r["strategy"] != "min-only"]
    if len(ok) == 2:
        a, s = (ok[0], ok[1]) if ok[0]["strategy"] == "avalanche" else (ok[1], ok[0])
        diff = s["total_interest"] - a["total_interest"]
        mdiff = s["months"] - a["months"]
        print(f"avalanche vs snowball: avalanche saves {fmt(diff)} and finishes "
              f"{abs(mdiff)} month{'s' if abs(mdiff) != 1 else ''} "
              f"{'earlier' if mdiff > 0 else 'later (or same)'}")
        if diff == 0:
            print("identical outcomes — pick either")
        elif diff < 20000:  # under $200
            print("gap is small — snowball's quick wins may be worth it for motivation")
        else:
            print("gap is material — avalanche is clearly worth sticking to")
    print("=" * 68)


# ---------------------------------------------------------------------------
# CLI

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Debt payoff strategy planner (avalanche vs snowball vs minimums)")
    p.add_argument("--debt", action="append", required=True, metavar="NAME,BALANCE,APR,MIN",
                   help="a debt, e.g. 'Visa,4200,22.9,105' (repeatable)")
    p.add_argument("--extra", type=float, default=0.0, metavar="USD",
                   help="extra money per month toward debt (default 0)")
    p.add_argument("--budget", type=float, default=None, metavar="USD",
                   help="total monthly payment pool (overrides --extra)")
    p.add_argument("--schedule", action="store_true", help="print yearly milestone schedule")
    p.add_argument("--csv", metavar="FILE", help="write month-by-month plan to CSV")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    try:
        debts = [parse_debt(s) for s in args.debt]
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    extra_c = round(args.extra * 100)
    budget_c = round(args.budget * 100) if args.budget is not None else None

    try:
        results = run_all(debts, extra_c, budget_c)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "schedule"} for r in results],
                         indent=2, default=str))
        return 0

    print_report(debts, results, extra_c, budget_c)

    # schedule / csv from the best strategy (avalanche when available)
    best = next((r for r in results if r.get("ok") and r["strategy"] == "avalanche"),
                next((r for r in results if r.get("ok")), None))
    if best:
        if args.schedule:
            print("\nYEARLY MILESTONES (avalanche plan)")
            for month, name, pay, bal in best["schedule"]:
                if month == 1 or month % 12 == 0 or bal <= 0:
                    print(f"  month {month:>3}: {name:<15} extra {fmt(pay):>10} → balance {fmt(bal) if bal > 0 else 'PAID OFF'}")
        if args.csv:
            with open(args.csv, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["month", "target", "extra_payment_usd", "target_balance_after"])
                for month, name, pay, bal in best["schedule"]:
                    w.writerow([month, name, pay / 100, max(bal, 0) / 100])
            print(f"\nCSV plan written to {args.csv}")

    # invariants
    oks = [r for r in results if r.get("ok")]
    if len(oks) == 3:
        ai = {r["strategy"]: r["total_interest"] for r in oks}
        assert ai["avalanche"] <= ai["snowball"] <= ai["min-only"] + 1, "invariant broken: interest ordering"
    return 0


if __name__ == "__main__":
    sys.exit(main())
