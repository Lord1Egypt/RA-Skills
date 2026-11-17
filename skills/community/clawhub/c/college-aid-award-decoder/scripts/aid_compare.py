#!/usr/bin/env python3
"""college-aid-award-decoder — classify award letters, compute Net Price, project debt.

Stdlib only. Three subcommands:
  compare   — side-by-side decode of multiple schools' letters
  debt      — 4-year loan projection with monthly repayment
  appeal    — professional-judgment (special circumstances) letter draft
  --demo    — run a worked two-school comparison end to end
"""
import argparse
import sys

# 2026-27-ish federal undergrad rates (verify current year at studentaid.gov)
RATE_SUB = 0.063      # Direct Subsidized (gov pays in-school interest)
RATE_UNSUB = 0.065    # Direct Unsubsidized (accrues from disbursement)
RATE_PLUS = 0.090     # Parent/Grad PLUS
TEN_YEARS = 120       # standard repayment months

CLASS_RULES = [
    ("GIFT",      ["pell", "grant", "scholarship", "fellowship", "merit",
                   "tuition remission", "need-based", "waiver"]),
    ("WORK",      ["work-study", "work study", "workstudy", "campus job",
                   "student employment"]),
    ("FED_LOAN",  ["direct subsidized", "subsidized", "direct unsubsidized",
                   "unsubsidized", "stafford", "perkins"]),
    ("OTHER_LOAN", ["plus", "parent", "private", "alternative",
                    "institutional loan"]),
]


def classify(name: str) -> str:
    n = name.lower()
    # OTHER_LOAN must win over generic 'loan' words inside FED list
    for cls, kws in CLASS_RULES:
        if cls == "FED_LOAN":
            continue
        if any(k in n for k in kws):
            return cls
    for cls, kws in CLASS_RULES:  # second pass for FED_LOAN
        if cls == "FED_LOAN" and any(k in n for k in kws):
            return cls
    if "loan" in n:
        return "OTHER_LOAN"
    return "UNKNOWN"


def monthly_payment(principal: float, annual_rate: float, months: int = TEN_YEARS) -> float:
    r = annual_rate / 12
    if r == 0:
        return principal / months
    return principal * r / (1 - (1 + r) ** -months)


def in_school_interest(principal_per_year: float, rate: float, years: int) -> float:
    """Interest accrued before repayment (grace ignored, conservative)."""
    total = 0.0
    for y in range(years):
        bal = principal_per_year * (y + 1)
        total += bal * rate  # one year of interest on cumulative balance
    return total


def decode_school(name: str, coa: float, awards: list) -> dict:
    lines = []
    for raw in awards:
        label, _, amt = raw.rpartition(",")
        amt = float(amt)
        lines.append({"name": label.strip(), "amount": amt, "cls": classify(label)})
    gift = sum(a["amount"] for a in lines if a["cls"] == "GIFT")
    work = sum(a["amount"] for a in lines if a["cls"] == "WORK")
    fed = sum(a["amount"] for a in lines if a["cls"] == "FED_LOAN")
    other = sum(a["amount"] for a in lines if a["cls"] == "OTHER_LOAN")
    unknown = sum(a["amount"] for a in lines if a["cls"] == "UNKNOWN")
    net_price = coa - gift
    self_help = work + fed + other
    total_award = gift + self_help + unknown
    misleading = (self_help / total_award) > 0.40 if total_award else False
    return {"name": name, "coa": coa, "lines": lines, "gift": gift, "work": work,
            "fed": fed, "other": other, "unknown": unknown, "net_price": net_price,
            "misleading": misleading}


def print_school(s: dict) -> None:
    print(f"\n=== {s['name']} — COA ${s['coa']:,.0f}")
    for a in s["lines"]:
        print(f"   {a['cls']:<11} ${a['amount']:>8,.0f}  {a['name']}")
    if s["unknown"]:
        print("   !! UNKNOWN lines present — resolve these manually before deciding")
    print(f"   Gift aid (keep):        ${s['gift']:>9,.0f}")
    print(f"   Work-study (earn):      ${s['work']:>9,.0f}")
    print(f"   Federal loans (repay):  ${s['fed']:>9,.0f}")
    print(f"   Parent/private loans:   ${s['other']:>9,.0f}")
    print(f"   NET PRICE (COA-gift):   ${s['net_price']:>9,.0f}")
    print(f"   MISLEADING FLAG: {'YES — loans/work-study >40% of "aid"' if s['misleading'] else 'no'}")


def cmd_compare(args) -> None:
    schools = []
    # args parsing: we flattened --school/--coa/--award into a list via action='append'
    # Format per school chunk: [name, coa, award, award...]
    name = coa = None
    awards = []
    def flush():
        nonlocal name, coa, awards
        if name and coa and awards:
            schools.append(decode_school(name, float(coa), awards))
        name, coa, awards = None, None, []
    for item in args.tokens:
        if item.startswith("S:"):
            flush()
            name = item[2:]
        elif item.startswith("C:"):
            coa = item[2:]
        else:
            awards.append(item)
    flush()
    if not schools:
        sys.exit("No complete school blocks (need name, coa, >=1 award).")
    for s in schools:
        print_school(s)
    ranked = sorted(schools, key=lambda s: s["net_price"])
    print("\n--- RANKING BY NET PRICE (only honest comparable) ---")
    for i, s in enumerate(ranked, 1):
        print(f"{i}. {s['name']}: ${s['net_price']:,.0f}/yr")
    a, b = ranked[0], ranked[-1]
    delta = b["net_price"] - a["net_price"]
    print(f"\nAnnual net-price delta: ${delta:,.0f}  (4-year: ${delta*4:,.0f})")
    print("Rule of thumb: treat any 4-year delta > $25k as a real decision, not noise.")


def cmd_debt(args) -> None:
    years = args.years
    sub_t = args.sub * years
    unsub_t = args.unsub * years
    unsub_int = in_school_interest(args.unsub, RATE_UNSUB, years)
    bal = sub_t + unsub_t + unsub_int
    pay = monthly_payment(bal, (RATE_SUB + RATE_UNSUB) / 2)
    print(f"=== {args.school}: {years}-year federal loan projection")
    print(f"  Subsidized borrowed:   ${sub_t:>9,.0f} (no in-school interest)")
    print(f"  Unsubsidized borrowed: ${unsub_t:>9,.0f}")
    print(f"  Unsub in-school interest accrued: ${unsub_int:,.0f}")
    print(f"  BALANCE AT GRADUATION: ${bal:>9,.0f}")
    print(f"  Standard 10-yr payment: ${pay:>7,.0f}/mo  (${pay*120:,.0f} total)")
    rule = bal * 1.0
    print(f"  Borrowing guideline: total debt <= expected first-year salary")
    print(f"  -> if starting salary < ${rule:,.0f}, this debt is heavy.")


def cmd_appeal(args) -> None:
    letter = f"""{args.student_name}
{args.school} — Office of Financial Aid
Re: Professional Judgment Review, aid year {args.aid_year}

To the Financial Aid Appeals Committee:

I am writing to request a Professional Judgment review of my aid year
{args.aid_year} FAFSA under 34 CFR 673.4 (Special Circumstances). Since filing,
our family circumstances changed materially: {args.circumstance}.

Documented change: household income decreased by approximately
${args.income_drop:,.0f}/yr. Enclosed: employer termination letter, final
paystub, and unemployment benefit statement.

I request the Committee adjust the SAI/EFC calculation to reflect current
income, and reconsider gift aid (grants/scholarships) in place of loan offers
in my package. I remain committed to attending {args.school} and am happy to
provide any additional documentation the office requires.

Sincerely,
{args.student_name}
(Phone/email)
Enclosures: as listed above
"""
    print(letter)


def run_demo() -> None:
    print("DEMO — two-school comparison (State U vs Private College)\n")
    class A:  # fake namespace for compare
        tokens = [
            "S:State U", "C:28400",
            "Pell Grant,3748", "University Grant,6000",
            "Direct Subsidized,3500", "Work-Study,2000",
            "S:Private College", "C:62000",
            "Merit Scholarship,22000", "Direct Subsidized,3500",
            "Direct Unsubsidized,2000", "Parent PLUS,12000",
        ]
    cmd_compare(A)
    print("\n" + "=" * 60)
    class B:
        school, sub, unsub, years = "State U", 3500, 2000, 4
    cmd_debt(B)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    pc = sub.add_parser("compare", help="side-by-side decode of award letters")
    pc.add_argument("tokens", nargs="*",
                    help="blocks: 'S:Name' then 'C:coa' then 'Award name,amount' entries")
    pd = sub.add_parser("debt", help="4-year loan projection")
    pd.add_argument("--school", default="School")
    pd.add_argument("--sub", type=float, default=3500)
    pd.add_argument("--unsub", type=float, default=2000)
    pd.add_argument("--years", type=int, default=4)
    pa = sub.add_parser("appeal", help="special-circumstances appeal letter")
    pa.add_argument("--school", required=True)
    pa.add_argument("--circumstance", required=True)
    pa.add_argument("--income-drop", type=float, default=0)
    pa.add_argument("--aid-year", default="2026-27")
    pa.add_argument("--student-name", default="[Student Name]")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        run_demo()
    elif args.cmd == "compare":
        cmd_compare(args)
    elif args.cmd == "debt":
        cmd_debt(args)
    elif args.cmd == "appeal":
        cmd_appeal(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
