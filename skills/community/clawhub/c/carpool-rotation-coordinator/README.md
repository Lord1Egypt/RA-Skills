# Carpool Rotation Coordinator

**Problem.** School-run and activity carpools collapse because fairness is
measured in driving days while the real resource is **seat-trips**. The
family with 3 kids in the pool owes 3 seats every run; a rotation that
splits days "equally" quietly overcharges single-kid families until someone
quits. Add weekday availability, booster capacity, and holidays, and the
paper-schedule version breaks within a month.

**What it does.** `scripts/carpool_plan.py` keeps a live seat-credit ledger
(every occupied seat you supply = credit; every ride your kid takes = debt)
and greedily assigns each trip to the **lowest-balance eligible driver** —
so load provably spreads instead of drifting:

- weekday availability + seat/booster hard-constraint checks per trip;
- holiday/blackout calendar; absences charge no debt;
- fairness audit with ±15 % band, DRIFT warnings and a correction hint;
- minimum-transfer fuel settlement (`--cost-per-km`) saying exactly who
  pays whom.

**Why broadly useful.** Millions of families run school/activity carpools;
"the carpool fell apart because it wasn't fair" is a universal experience,
and every parent who has driven 3 days/week for a semester knows the
feeling. This tool makes the fairness legible — you can even show the table
to the other families.

**Example.**

```bash
python3 scripts/carpool_plan.py plan sample_carpool.json --weeks 12 \
  --cost-per-km 0.18 --km-one-way 6
# -> week grid of drivers, Novak/Kowalski/Rossi balances near zero,
#    "Kowalski pays Rossi: 4.32" style settlement
```

MIT license.
