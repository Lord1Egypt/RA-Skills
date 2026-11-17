#!/usr/bin/env python3
"""
late_invoice_nudge.py — escalating, professional late-payment workflow
for freelancers and small studios.

Commands:
  status    Aging bucket report of outstanding invoices.
  ladders   Payment-reminder ladder: which step an invoice is on, the
            email draft, late-fee math (simple or compound), and the
            send date given a min-interval cadence.
  smallclaims  Small-claims readiness: amount vs local cap, evidence
            checklist, filing math (fee vs recovery), demand-letter draft.
  stopwork   Stop-work / suspension notice for active projects.

Stdlib only. Offline. Informational — check contract and local law.
"""
import argparse
import json
from datetime import date, timedelta

# Small-claims caps (USD). Sources vary; treat as of-2024-ish reference.
SC_CAPS = {
    # US states with distinctive caps
    "AL": 6000, "AK": 10000, "AZ": 3500, "AR": 5000, "CA": 10000,
    "CO": 7500, "CT": 5000, "DE": 25000, "DC": 10000, "FL": 8000,
    "GA": 15000, "HI": 5000, "ID": 5000, "IL": 10000, "IN": 10000,
    "IA": 6500, "KS": 4000, "KY": 2500, "LA": 5000, "ME": 6000,
    "MD": 5000, "MA": 7000, "MI": 6500, "MN": 15000, "MS": 3500,
    "MO": 5000, "MT": 7000, "NE": 3900, "NV": 10000, "NH": 10000,
    "NJ": 5000, "NM": 10000, "NY": 10000, "NC": 10000, "ND": 15000,
    "OH": 6000, "OK": 10000, "OR": 10000, "PA": 12000, "RI": 5000,
    "SC": 7500, "SD": 12000, "TN": 25000, "TX": 20000, "UT": 15000,
    "VT": 5000, "VA": 5000, "WA": 10000, "WV": 10000, "WI": 10000,
    "WY": 6000,
    # Reference points
    "UK": 10000, "DE#": 5000, "ON": 35000,
}

# Statutory/prompt-payment interest reference rates (annual, %) — reference only.
LATE_RATES = {"default": 10.0, "UK-late-payment-act": 8.0, "EU-late-dir": 8.0}

LADDER = [
    # (days late, step name, tone)
    (-3, "courtesy pre-due reminder", "friendly"),
    (1, "reminder #1 (same day it's late)", "friendly firm"),
    (7, "reminder #2 + late fee notice", "firm"),
    (14, "reminder #3 + final notice framing", "firm"),
    (30, "final demand + formal demand letter", "formal"),
    (45, "decision point: collections / small claims / write-off", "formal"),
    (60, "escalate: collections agency or court filing", "formal"),
]


def pdate(s):
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def fmt_money(x):
    return f"{x:,.2f}"


def load(a):
    data = json.loads(a.invoices)
    return data if isinstance(data, list) else data.get("invoices", [])


def aging(inv, today):
    due = pdate(inv["due"])
    if today <= due:
        return 0
    return (today - due).days


def bucket(days):
    if days <= 0:
        return "current"
    if days <= 30:
        return "1-30"
    if days <= 60:
        return "31-60"
    if days <= 90:
        return "61-90"
    return "90+"


def late_fees(principal, days, annual_pct, mode):
    """Late-fee interest: simple or monthly-compound on monthly rate."""
    if days <= 0:
        return 0.0
    if mode == "simple":
        return principal * (annual_pct / 100.0) * (days / 365.0)
    # compound monthly
    months = days / 30.0
    mrate = (annual_pct / 100.0) / 12.0
    return principal * ((1 + mrate) ** months - 1)


def cmd_status(a):
    today = pdate(a.today)
    invs = sorted(load(a), key=lambda i: aging(i, today), reverse=True)
    print(f"AGING REPORT — {a.today}\n")
    print(f"{'client':<22}{'invoice':<12}{'due':<12}{'days late':>10}{'amount':>12}{'bucket':>8}")
    total = 0.0
    for i in invs:
        d = aging(i, today)
        amt = i["amount"]
        total += amt
        print(f"{i['client'][:20]:<22}{i.get('no', '-'):<12}{i['due']:<12}{d:>10}{amt:>12,.2f}{bucket(d):>8}")
    print("-" * 76)
    print(f"TOTAL OUTSTANDING: {fmt_money(total)}  ({len(invs)} invoices)")
    old = [i for i in invs if aging(i, today) > 60]
    if old:
        print(f"At-risk (>60d, escalation candidates): "
              f"{fmt_money(sum(i['amount'] for i in old))} across {len(old)} invoice(s)")


def ladder_step(days):
    step = None
    for d, name, tone in LADDER:
        if days >= d:
            step = (d, name, tone)
    return step


def cmd_ladders(a):
    today = pdate(a.today)
    invs = load(a)
    for i in invs:
        d = aging(i, today)
        step = ladder_step(d)
        fee = late_fees(i["amount"], max(d - 7, 0), a.rate, a.mode)
        print(f"=== {i['client']} — {i.get('no','—')} — {fmt_money(i['amount'])} — {d}d late")
        if step:
            print(f"step: {step[1]}  (tone: {step[2]})")
        if d > 7:
            print(f"late fees accrued ({a.rate}%/yr {a.mode}, from day 8): {fmt_money(fee)}")
            print(f"total with fees: {fmt_money(i['amount'] + fee)}")
        nxt = next(((dd, n) for dd, n, _ in LADDER if dd > d), None)
        if nxt:
            send_on = today + timedelta(days=(nxt[0] - d))
            print(f"next step on {send_on.isoformat()}: {nxt[1]}")
        print()


def cmd_smallclaims(a):
    today = pdate(a.today)
    invs = [i for i in load(a) if aging(i, today) > 0]
    cap = SC_CAPS.get(a.jurisdiction)
    if cap is None:
        cap = SC_CAPS["default"] * 100  # unknown: show as open question
        print(f"Jurisdiction '{a.jurisdiction}' not in table — verify local cap.")
    print(f"SMALL-CLAIMS READINESS — cap reference {a.jurisdiction}: {cap:,.0f}\n")
    for i in invs:
        d = aging(i, today)
        amt = i["amount"] + late_fees(i["amount"], max(d - 7, 0), a.rate, a.mode)
        fit = "FITS small claims" if amt <= cap else "OVER cap — collections/civil court instead"
        net = amt - a.fee
        print(f"{i['client']}: claim {fmt_money(amt)} ({d}d late) — {fit}")
        if amt <= cap:
            print(f"   filing fee ~{fmt_money(a.fee)} -> net recovery {fmt_money(net)} "
                  f"({100*net/amt:.0f}% of claim)")
    print("\nEvidence checklist (each invoice):")
    for line in [
        "1. Signed contract/proposal (scope + price + payment terms)",
        "2. The invoice itself (delivered: email sent-date)",
        "3. Proof of delivery of work (files, deploys, handoff emails)",
        "4. Client acceptance (approval email, 'looks great', go-live)",
        "5. Payment reminder trail (this ladder's sent log)",
        "6. Any client acknowledgment of the debt ('will pay Friday')",
    ]:
        print("  " + line)
    print("\nDemand letter (attach as exhibit A when filing):\n")
    client = invs[0]["client"] if invs else "[CLIENT]"
    amt = invs[0]["amount"] if invs else 0
    print(f"""{date.today().isoformat()}

RE: FINAL DEMAND FOR PAYMENT — Invoice(s) {[i.get('no') for i in invs]}

Dear {client},

Despite repeated reminders, payment of {fmt_money(amt)} for delivered
services (per our agreement of [DATE]) remains outstanding, now
{aging(invs[0], today) if invs else 0} days past due.

This is a formal demand for payment in full, including late charges,
within 10 business days of this letter's date, to [ACCOUNT].

If payment is not received, I will pursue all available remedies,
including small-claims court and recovery of costs permitted by
contract and law, without further notice.

This letter is sent in good faith to resolve this matter without court
action. I'd still prefer to settle this professionally.

Sincerely,
[YOUR NAME]""")


def cmd_stopwork(a):
    invs = load(a)
    tot = sum(i["amount"] for i in invs)
    print(f"""{date.today().isoformat()}

RE: PAUSE OF SERVICES — OUTSTANDING INVOICES

Hi [CLIENT],

Per our agreement (payment terms: Net-30), invoices totaling
{fmt_money(tot)} are now past due. Effective [DATE], I'm pausing
active work on [PROJECT] until the account is current.

This isn't a cancellation — I'd like to continue, on the schedule we
agreed. To resume work: pay the outstanding balance, and confirm
whether the project timeline should shift.

Deliverables already delivered remain licensed per our agreement's
payment terms. Happy to jump on a 15-minute call to sort the plan.

[YOUR NAME]""")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--invoices", required=True,
                    help='JSON list: [{"client":"Acme","no":"INV-42","due":"2026-09-01","amount":4200}]')
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--rate", type=float, default=10.0, help="late interest %%/yr")
    ap.add_argument("--mode", choices=["simple", "compound"], default="compound")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="aging buckets")
    sub.add_parser("ladders", help="reminder ladder + drafts + fees")
    sc = sub.add_parser("smallclaims", help="readiness + demand letter")
    sc.add_argument("--jurisdiction", default="CA")
    sc.add_argument("--fee", type=float, default=75.0, help="filing fee estimate")
    sub.add_parser("stopwork", help="stop-work notice")
    a = ap.parse_args()
    {"status": cmd_status, "ladders": cmd_ladders,
     "smallclaims": cmd_smallclaims, "stopwork": cmd_stopwork}[a.cmd](a)
    if getattr(a, "json", False):
        pass  # structured flag reserved; human output is canonical here


if __name__ == "__main__":
    main()
