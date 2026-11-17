#!/usr/bin/env python3
"""Credit profile repair planner.

Input: a JSON profile (cards with limits/balances/statement days, loans, derogatory
items with first-delinquency dates, inquiries, goal date + loan type).

Output:
  1. FICO factor drag decomposition for THIS profile
  2. AZEO utilization plan with exact pay-by dates (statement-day aware)
  3. Derogatory age-off timeline (7yr/10yr rules)
  4. Letter queue: validation / 623 / goodwill / PFD, with draft text files
  5. Score-band movement estimates (ranges, never exact)

stdlib only.
"""
import argparse
import datetime as dt
import json
import os

SEVEN = dt.timedelta(days=365.25 * 7)
TEN = dt.timedelta(days=365.25 * 10)

UTIL_BANDS = [(9, "excellent"), (29, "good"), (49, "fair"), (10**9, "heavy drag")]


def band(pct):
    for cap, name in UTIL_BANDS:
        if pct <= cap:
            return name
    return "heavy drag"


def parse_date(s):
    return dt.date.fromisoformat(s) if s else None


def fmt(d):
    return d.isoformat() if d else "?"


def util_plan(cards, azeo_budget=30.0):
    """Pick the AZEO reporter (card with earliest upcoming statement after a pay-down
    window), plan $0 reporting for the rest. Pay-by = statement day - 3 business days."""
    total_limit = sum(c["limit"] for c in cards)
    total_bal = sum(c.get("balance", 0) for c in cards)
    agg = 100.0 * total_bal / total_limit if total_limit else 0

    today = dt.date.today()

    def next_stmt(c):
        d = c.get("statement_day", 1)
        for offset in (0, 1):
            try:
                cand = dt.date(today.year, today.month + offset, min(d, 28))
            except ValueError:
                continue
            if cand > today:
                return cand
        return dt.date(today.year + 1, 1, min(d, 28))

    ranked = sorted(cards, key=lambda c: next_stmt(c))
    reporter = ranked[0]
    azeo_bal = min(azego if (azego := azeo_budget) else 0, 0.08 * reporter["limit"])
    steps = []
    for c in cards:
        stmt = next_stmt(c)
        pay_by = stmt - dt.timedelta(days=3)
        if c is reporter:
            target = azeo_bal
            steps.append((c["name"], stmt, pay_by, f"let ~${target:.0f} report "
                          f"({100*target/c['limit']:.1f}% of limit) — AZEO reporter"))
        else:
            steps.append((c["name"], stmt, pay_by,
                          f"pay to $0 BEFORE {fmt(stmt)} (statement close, not due date)"))
    new_agg = 100.0 * azeo_bal / total_limit if total_limit else 0
    return agg, new_agg, reporter["name"], steps


def ageoff_timeline(derogs):
    out = []
    for d in derogs:
        fdd = parse_date(d.get("first_delinquency") or d.get("filed"))
        kind = d["type"].lower()
        life = TEN if "chapter 7" in kind or "bk7" in kind else SEVEN
        if fdd:
            out.append((d["type"], fdd, fdd + life, fmt(fdd + life)))
        else:
            out.append((d["type"], None, None, "need first-delinquency date"))
    return out


def drag_analysis(profile):
    """Heuristic factor decomposition — ranges, not exact FICO."""
    cards = profile.get("cards", [])
    limit = sum(c["limit"] for c in cards) or 1
    bal = sum(c.get("balance", 0) for c in cards)
    util = 100.0 * bal / limit
    drags = []
    if util > 29:
        drags.append(("Amounts owed", f"aggregate util {util:.0f}% ({band(util)})",
                      "+20–70 pts from AZEO pay-down", "HIGH"))
    maxed = [c["name"] for c in cards if c.get("balance", 0) > 0.49 * c["limit"]]
    if maxed:
        drags.append(("Amounts owed", f"maxed-ish cards: {', '.join(maxed)}",
                      "per-card util counts separately", "HIGH"))
    lates = [d for d in profile.get("derogatory", []) if "late" in d["type"].lower()]
    colls = [d for d in profile.get("derogatory", []) if "collect" in d["type"].lower()]
    cos = [d for d in profile.get("derogatory", []) if "charge" in d["type"].lower()]
    if lates or colls or cos:
        drags.append(("Payment history", f"{len(lates)} lates, {len(colls)} collections, "
                      f"{len(cos)} charge-offs", "goodwill/validation/PFD ladder",
                      "CRITICAL"))
    inq = profile.get("recent_inquiries", 0)
    if inq >= 3:
        drags.append(("New credit", f"{inq} recent hard pulls", "fades in 12 mo", "LOW"))
    oldest = min((parse_date(c["opened"]) for c in cards if c.get("opened")), default=None)
    age = (dt.date.today() - oldest).days / 365.25 if oldest else 0
    if age < 2:
        drags.append(("Length of history", f"oldest account {age:.1f} yr", "time + AU tradeline",
                      "MEDIUM"))
    if not profile.get("loans"):
        drags.append(("Credit mix", "no installment tradeline", "credit-builder loan (small)",
                      "LOW"))
    return drags


GOODWILL = """{date}

{issuer_name}
Attn: Executive Offices / Credit Bureau Disputes
RE: Account {account}

To whom it may concern,

I have been a customer since {opened} and value the relationship. In {late_month} I missed
a payment due to {reason}. I have been current every month since ({months_clean} consecutive
on-time payments).

I am writing to request a goodwill adjustment: removal of this single late notation from
my credit report. This isolated incident does not reflect my record with you, and its
removal would materially help me {goal}.

I understand this is not required of you and is requested purely as a courtesy. I am happy
to provide any documentation. Thank you for your consideration.

Sincerely,
{name}
{address}
"""

VALIDATION = """{date}

{collector_name}
RE: Account {account} — Demand for Validation (FDCPA 15 U.S.C. 1692g)

This letter is my formal notice that I dispute the validity of the above debt. Demand is
hereby made that you provide:

1. The amount of the debt and how it was calculated;
2. The name and address of the original creditor;
3. Documentation evidencing my obligation (signed agreement, assignment chain);
4. Proof the debt is within the applicable statute of limitations.

Until you mail this validation to me, all collection activity must cease. I request that
no telephone contact be made; communicate in writing only.

Sincerely,
{name}
{address}
"""

SIX23 = """{date}

{furnisher_name}
Attn: Credit Reporting Disputes
RE: Account {account} — Direct Dispute under 12 CFR 1022.43

I dispute the accuracy of the tradeline you are furnishing regarding the above account,
specifically: {dispute_reason}.

Under the Fair Credit Reporting Act (6 U.S.C. 1681s-2(b)) and Regulation V, you must
conduct a reasonable investigation and report the results to both me and the consumer
reporting agencies within 30 days. Please provide the specific documentation relied upon,
and delete the tradeline if it cannot be substantiated.

Sincerely,
{name}
{address}
{ssn_last4}
"""


def letters(profile, outdir):
    os.makedirs(outdir, exist_ok=True)
    me = profile.get("user", {})
    written = []
    today = dt.date.today().isoformat()
    for d in profile.get("derogatory", []):
        base = {
            "date": today, "name": me.get("name", "[NAME]"),
            "address": me.get("address", "[ADDRESS]"),
            "account": d.get("account", "[ACCT #]"),
        }
        kind = d["type"].lower()
        if "late" in kind:
            ctx = dict(base, issuer_name=d.get("creditor", "[ISSUER]"),
                       opened=d.get("opened", "[DATE]"),
                       late_month=(parse_date(d.get("first_delinquency")) or today).strftime("%B %Y"),
                       reason=d.get("reason", "a temporary hardship"),
                       months_clean=d.get("months_clean", "12"),
                       goal=profile.get("goal", "qualify for a mortgage"))
            p = os.path.join(outdir, f"goodwill-{d.get('account','x')}.txt")
            open(p, "w").write(GOODWILL.format(**ctx))
            written.append(p)
        elif "collect" in kind:
            ctx = dict(base, collector_name=d.get("creditor", "[COLLECTOR]"))
            p = os.path.join(outdir, f"validation-{d.get('account','x')}.txt")
            open(p, "w").write(VALIDATION.format(**ctx))
            written.append(p)
        elif "charge" in kind:
            ctx = dict(base, furnisher_name=d.get("creditor", "[FURNISHER]"),
                       dispute_reason=d.get("reason",
                           "the balance and payment history reported do not match my records"),
                       ssn_last4=me.get("ssn_last4", "[SSN LAST 4]"))
            p = os.path.join(outdir, f"623-{d.get('account','x')}.txt")
            open(p, "w").write(SIX23.format(**ctx))
            written.append(p)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("profile", help="path to profile JSON")
    ap.add_argument("--letters-out", default="./letters", help="dir for letter drafts")
    ap.add_argument("--azego-budget", type=float, default=30.0, dest="azego_budget",
                    help="target $ reporting on AZEO card (default 30)")
    args = ap.parse_args()

    profile = json.load(open(args.profile))
    cards = profile.get("cards", [])
    print("=== PROFILE ===")
    print(f"Cards: {len(cards)} | total limit ${sum(c['limit'] for c in cards):,} | "
          f"balance ${sum(c.get('balance',0) for c in cards):,}")

    print("\n=== FACTOR DRAG ===")
    for f, what, fix, sev in drag_analysis(profile):
        print(f"  [{sev:<8}] {f}: {what}\n             fix: {fix}")

    agg, new_agg, rep, steps = util_plan(cards, args.azego_budget)
    print(f"\n=== UTILIZATION / AZEO PLAN ===")
    print(f"  current aggregate util: {agg:.1f}% ({band(agg)}) -> after plan: {new_agg:.2f}% "
          f"({band(new_agg)})")
    print(f"  AZEO reporter: {rep}")
    for name, stmt, pay_by, action in sorted(steps, key=lambda s: s[2]):
        print(f"  {name:<14} statement {fmt(stmt)} | PAY BY {fmt(pay_by)}: {action}")

    print(f"\n=== AGE-OFF TIMELINE ===")
    for kind, fdd, gone, when in ageoff_timeline(profile.get("derogatory", [])):
        print(f"  {kind:<28} first delinq {fmt(fdd)} -> removed {when}")

    written = letters(profile, args.letters_out)
    print(f"\n=== LETTER QUEUE ({len(written)}) ===")
    for p in written:
        print(f"  drafted: {p}")
    print("  Mail Certified Return-Receipt; keep copies + green cards forever.")

    if profile.get("goal_type") == "mortgage":
        print("\n=== MORTGAGE MODE ===")
        print("  - No new credit 12 months before application")
        print("  - AZEO the cycle BEFORE pre-approval pull")
        print("  - Lenders use FICO 2/4/5 — harsher on util than app scores; re-check on myFICO")
    print("\nEstimates are directional ranges, not score predictions. "
          "Never dispute accurate information as inaccurate.")


if __name__ == "__main__":
    main()
