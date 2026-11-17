# College Aid Award Decoder

**Comparing college financial aid offers honestly — gift aid vs loans vs jobs, Net Price per school, 4-year debt projection, and the appeal letter nobody sends.**

## The problem
Award letters have no enforced standard format. Schools label parent loans "financial aid," hide Cost of Attendance, front-load scholarships to freshman year, and present a big bottom-line number that families compare across schools — even though that number mixes free money, hourly jobs, and debt at three different interest rates. The result is systematic misdecision: families pick the letter that looks biggest, not the school that costs least. A 4-year mistake here runs $25,000–$150,000, and it's made in a 3-week window every spring.

## What this skill does
- **Classifies every award line** into gift aid / work-study / federal loans / parent-private loans using the letter's own wording
- **Computes Net Price** (COA − gift aid) — the only number that compares fairly across schools — and ranks schools by it
- **Flags MISLEADING letters** where loans + work-study exceed 40% of the "award"
- **Projects debt at graduation** with in-school interest accrual and the standard 10-year monthly payment
- **Drafts the professional-judgment appeal** (34 CFR 673.4) for income changes — the request that converts loans to grants and most families never make

## Quick example
```bash
python3 scripts/aid_compare.py --demo
```
Decodes two letters: "State U" (COA $28,400, Pell + grant + sub loan + work-study) vs "Private College" (COA $62,000, $22k merit + loans + PLUS). The private letter's "$39,500 award" shrinks to a $38,500 net price vs State U's $18,700 — and gets flagged misleading because 44% of its "aid" is loans and a parent loan.

## Who needs this
- Parents of high-school seniors comparing 2–5 award letters each spring (~3.5M first-time FAFSA filers/yr in the US)
- Returning/adult students decoding a single offer before accepting loans
- School counselors and advisors without a financial-aid background
- Anyone whose family income dropped after filing FAFSA

## Install
Clone the repo and run with Python 3.9+ (stdlib only — no dependencies):

```bash
python3 scripts/aid_compare.py --demo
```

## License
MIT © Denis Voronin
