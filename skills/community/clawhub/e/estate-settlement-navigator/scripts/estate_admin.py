#!/usr/bin/env python3
"""Estate settlement navigator — certificates, cascade, benefits, timeline, letters.

Subcommands:
  certificates  Count organizations -> certified death-certificate order
  cascade       Ordered notification list (US/UK) with the WHY per slot
  benefits      SSA survivor-benefit screening from ages + switch strategy
  timeline      Dated milestone plan from date of death
  letter        Generate close/claim/transfer notification letter

Stdlib only. Offline. General information, not legal or tax advice.
"""
import argparse
import json
from datetime import date, timedelta

FIRST_COPY = 24.0   # USD, typical vital-records first copy
ADDL_COPY = 6.0     # additional copies in the same order


def cmd_certificates(a):
    need = a.orgs
    spare = max(3, a.spares)
    total = need + spare
    cost = FIRST_COPY + (total - 1) * ADDL_COPY
    reorder_cost = 3 * (FIRST_COPY + ADDL_COPY)
    print(f"CERTIFIED DEATH CERTIFICATES — order plan")
    print(f"  Organizations needing an original: {need}")
    print(f"  Spares: {spare} (minimum 3 — surprises are routine)")
    print(f"  ORDER: {total} certified copies now, at the funeral home")
    print(f"  Estimated cost: ${cost:.0f} (first ~${FIRST_COPY:.0f} + "
          f"${ADDL_COPY:.0f}/additional)")
    print(f"  Reordering 3 later costs ~${reorder_cost:.0f} + trips + delays")
    print()
    print("RULES")
    print("  - Originals only; photocopies are rejected by banks/insurers.")
    print("  - An institution may KEEP the copy — that's why counts run high.")
    print("  - Cheapest copies are ordered through the funeral home at arrangement.")
    return {"order_copies": total, "est_cost_usd": round(cost, 2)}


US_CASCADE = [
    ("day 0-2", "Funeral home / vital records", "Order certificates NOW; get 10-15", "stops the expensive reorder"),
    ("day 1-5", "Social Security 1-800-772-1213", "Verify the funeral home actually filed the electronic notice", "stop payments before clawback; opens $255 + survivor claims"),
    ("day 2-7", "Secure home, mail, valuables, pets", "halt mail, locks, perishables", "vacant homes get robbed; mail gets stolen"),
    ("week 1-2", "Credit bureaus (Equifax, Experian, TransUnion)", "deceased flag + freeze, copy of cert enclosed", "deceased identity theft is a million-a-year industry"),
    ("week 1-3", "Each bank / credit union / card issuer", "close solo accounts; KEEP the joint/estate account", "final bills and the funeral invoice still clear here"),
    ("week 1-3", "Life insurers + every employer's HR", "claim form + original cert", "group-life windows are short; unclaimed policies end up at state unclaimed property"),
    ("week 2-4", "Retirement plans (401k/IRA/pension)", "cert + beneficiary form", "spousal rollover vs inherited-IRA (10-yr) decision is irreversible"),
    ("week 2-4", "DMV (titles) + auto insurers", "transfer/cancel correctly", "mis-cancelled insurance is a claims fight later"),
    ("month 1-2", "Utilities, landlord, phone, subscriptions", "transfer or close AFTER final bills", "early closure = collections letters to the estate"),
    ("month 1-2", "USPS forward + DMA 'Deceased Do Not Contact'", "online forms", "stops the mail avalanche for years"),
    ("ongoing", "Digital accounts", "see digital-legacy pattern", "email recovery = key to everything else"),
]

UK_CASCADE = [
    ("day 0-5", "Registrar + Tell Us Once", "one call covers DWP/HMRC/DVLA/Passport/council", "do it in week one or you notify each agency by hand"),
    ("week 1", "DWP Bereavement Service", "Bereavement Support Payment claim", "within 3 months for FULL backdating — money dies monthly"),
    ("week 1-2", "Banks (grant of probate if needed)", "each bank has its own no-grant threshold £5k-£50k", "ask BEFORE applying for probate"),
    ("week 1-3", "Pension providers + employers", "survivor annuity / death-in-service benefits", "death-in-service is often 2-4x salary, unclaimed constantly"),
    ("week 2-4", "Insurers, DVLA, Passport Office", "cert + forms", " Tell Us Once covers most of it — verify"),
    ("month 1-2", "Utilities, council tax (single-person discount)", "transfer or close after final bills", "council tax single discount is backdated only to notification"),
    ("month 1-6", "HMRC: IHT forms by 6 months after month of death", "even when no tax due", "penalties are real; ISA extra-permitted-subscription for spouse"),
]


def cmd_cascade(a):
    rows = US_CASCADE if a.country.lower() == "us" else UK_CASCADE
    print(f"NOTIFICATION CASCADE — {a.country.upper()}")
    print(f"{'WHEN':<12}{'WHO':<42}{'WHY THIS SLOT'}")
    for when, who, what, why in rows:
        print(f"{when:<12}{who:<42}{why}")
        print(f"{'':<12}{'':<42}-> {what}")
    print()
    print("ORDER IS MONEY: SSA before bank closures (clawback lands on an")
    print("emptied account); bureaus before collectors; employer windows first.")
    return {"country": a.country, "steps": len(rows)}


def cmd_benefits(a):
    print("SSA SURVIVOR-BENEFIT SCREEN")
    flags = []
    if a.spouse_age is not None:
        age = a.spouse_age
        if age >= 60:
            pct_lo, pct_hi = 71.5, 99.0
            print(f"  Widow(er) at {age}: YES — 71.5%-99% of deceased's PIA")
            print(f"    (reduction shrinks to 0 at full retirement age)")
            if age < 66:
                flags.append("claiming before FRA permanently reduces the survivor %")
        elif age >= 50 and a.spouse_disabled:
            print(f"  Disabled widow(er) at {age}: YES — 71.5% of PIA")
        elif a.kids_under16:
            print(f"  Widow(er) at {age} caring for child <16: YES — 75% of PIA")
            print(f"    (mother's/father's benefit ends when the child turns 16)")
        else:
            print(f"  Widow(er) at {age}: NOT YET — gate is 60 (50 disabled).")
            flags.append(f"calendar reminder at age 60 — benefits are not automatic")
    if a.kids_under16:
        print(f"  Children x{a.kids_under16}: 75% of PIA each to 18 (19 in high school)")
        print(f"  Family maximum ~150-180% of PIA — multiple claims hit the cap")
    print(f"  Lump-sum death payment: $255, surviving spouse, claim within 2 YEARS")
    flags.append("$255 claim window: 2 years from death — file with SSA report")
    if a.spouse_age is not None and 60 <= a.spouse_age < 70:
        print()
        print("SWITCH STRATEGY (two records = model both):")
        print("  Option A: survivor now (reduced), switch to OWN at 70 (8%/yr credits)")
        print("  Option B: own now (reduced), switch to SURVIVOR at FRA (100%)")
        print("  Take the smaller check first; the bigger one grows.")
    print()
    print("PENSION/EMPLOYER CHECKS")
    for line in (
        "  - DB pension: survivor annuity elected? payments continue automatically",
        "  - Died before retirement? pre-retirement survivor benefit usually exists",
        "  - 401k/IRA: named beneficiary wins over the will; spouse=rollover,",
        "    non-spouse=inherited IRA emptied in ~10 years (SECURE)",
        "  - Group life: claim via HR now; conversion window can be 31 days",
        "  - VA burial allowance + income-tested survivor pension if veteran",
    ):
        print(line)
    return {"flags": flags}


def add_months(d, months):
    m = d.month - 1 + months
    return date(d.year + m // 12, m % 12 + 1, min(d.day, 28))


def cmd_timeline(a):
    d0 = date.fromisoformat(a.date)
    print(f"SETTLEMENT TIMELINE — death {d0.isoformat()}")
    plan = [
        (d0 + timedelta(days=5), "Certificates ordered; SSA verified; home secured"),
        (d0 + timedelta(days=14), "Bureaus flagged; banks/insurers notified; will located; executor decided"),
        (d0 + timedelta(days=30), "Benefit claims filed; employer HR done; mail redirected"),
        (add_months(d0, 2), "Probate decision: designations/POD/joint pass outside it; small-estate affidavit if remainder fits"),
        (add_months(d0, 4), "Titles transferred; utilities settled; estate account reconciled"),
        (add_months(d0, 6), "Estate income check: 1041 if >$600/yr earned"),
        (date(d0.year + 1, 4, 15), "FINAL 1040 for year of death (marked 'deceased')"),
        (add_months(d0, 9), "Form 706 ONLY if gross estate over federal exclusion (~$14M) — state rules lower"),
        (add_months(d0, 12), "Unclaimed-property sweep; close estate account; final distribution"),
    ]
    for when, what in plan:
        print(f"  {when.isoformat()}  {what}")
    return {"milestones": len(plan)}


def cmd_letter(a):
    letter = f"""{a.requester}
{date.today().isoformat()}

{a.to}
RE: Estate of {a.deceased} — Date of death: {a.dod}

To whom it may concern:

I am {a.requester}, {'surviving spouse / executor' if 'spouse' in a.requester.lower() or 'executor' in a.requester.lower() else 'authorized representative'} in the
estate of the above-named deceased. A certified copy of the death
certificate is enclosed.

I request that you:
  1. Close the account(s) held solely in the deceased's name and remit
     any balance to the estate;
  2. Stop all recurring charges and autopayments on those accounts;
  3. Confirm in writing, to the address below, the closing balance,
     final statement, and that no further liability accrues.

{'I additionally claim any beneficiary proceeds or death benefit payable under the policy/plan, payable per the named beneficiary designation.' if a.type == 'claim' else ''}
{'For jointly held property, please transfer sole registration to the surviving owner(s) and confirm.' if a.type == 'transfer' else ''}

Please direct all future correspondence to me at the address above.
Enclosed: certified death certificate{' (original)' if a.type != 'close' else ''}.

Sincerely,
{a.requester}
"""
    print(letter)
    return {"letters_bytes": len(letter)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="emit JSON summary")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("certificates", help="order-size math")
    sp.add_argument("--orgs", type=int, default=10, help="organizations needing an original")
    sp.add_argument("--spares", type=int, default=3)
    sp.set_defaults(fn=cmd_certificates)

    sp = sub.add_parser("cascade", help="ordered notification list")
    sp.add_argument("--country", default="us", choices=["us", "uk"])
    sp.set_defaults(fn=cmd_cascade)

    sp = sub.add_parser("benefits", help="survivor screening")
    sp.add_argument("--spouse-age", type=int, default=None)
    sp.add_argument("--spouse-disabled", action="store_true")
    sp.add_argument("--kids-under16", type=int, default=0)
    sp.set_defaults(fn=cmd_benefits)

    sp = sub.add_parser("timeline", help="dated milestones")
    sp.add_argument("--date", required=True, help="date of death YYYY-MM-DD")
    sp.set_defaults(fn=cmd_timeline)

    sp = sub.add_parser("letter", help="notification letter")
    sp.add_argument("--type", default="close", choices=["close", "claim", "transfer"])
    sp.add_argument("--to", required=True)
    sp.add_argument("--deceased", required=True)
    sp.add_argument("--dod", required=True)
    sp.add_argument("--requester", required=True)
    sp.set_defaults(fn=cmd_letter)

    a = p.parse_args()
    out = a.fn(a)
    if a.json:
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
