# Co-Parenting Custody Calendar

A custody schedule is a 52-weeks-a-year logistical contract executed by two
people who may barely speak. This skill turns parenting-plan language into
dated reality — and reality back into evidence.

## The Real Problem

~1 million US couples divorce each year; roughly half involve minor
children, and every one of them needs a custody schedule. The plans are
usually written in general language ("alternating weeks, holidays
alternating") — and then reality hits: which Monday does the rotation
start? Who has spring break 2027? Does Dad's 2-week work trip mean Mom
waits 20 days? Is the split actually 50/50 or quietly 42/58?

Meanwhile the stakes are concrete: below 35% of overnights, many US
state child-support formulas and "custodial parent" designations change.
Holiday ambiguity is the #1 source of re-litigation. And informal
overrides without make-up time quietly rewrite the plan.

## What It Does

- **plan** — dated 50/50 rotations (alternating-week, 2-2-3, 3-4-4-3):
  runs, overnight counts, exchanges/month, ICS calendar export with
  exchange events + pack reminders
- **holidays** — year's holiday table with alternating odd/even priority,
  Mother's/Father's Day pinned to the named parent, child's birthday listed
- **fairness** — overnight/weekend/longest-gap audit with the <35%
  shared-custody threshold flag
- **override** — travel/vacation patches with make-up-time doctrine and
  a ready log entry
- **references/** — model parenting-plan clauses (exchange mechanics,
  holiday rules, vacation caps, right of first refusal, communication
  protocol, dispute ladder)

## Quick Start

```bash
python3 scripts/co_parenting_calendar.py plan --schedule 2-2-3 --start 2026-11-02 --days 28
python3 scripts/co_parenting_calendar.py fairness --schedule alternating-week --start 2026-01-01 --end 2026-12-31
python3 scripts/co_parenting_calendar.py holidays --year 2027 --odd B --mother A --father B --birthday 2019-05-14
python3 scripts/co_parenting_calendar.py override --from 2027-03-30 --to 2027-04-10 --parent A --reason "work trip"
```

Stdlib only, offline, no accounts. Informational tool — not legal advice.

## License

MIT © Denis Voronin
