---
name: co-parenting-custody-calendar
description: Use when separated/divorced parents need to build, check, or dispute a custody schedule — generates dated 50/50 rotations (alternating-week, 2-2-3, 3-4-4-3) with overnight counts, builds the alternating-priority holiday table (Mother's/Father's Day pinned), audits the time split for the <35% shared-custody threshold many US states use, patches travel overrides with make-up-time doctrine, and exports court-ready ICS calendars and plain-English plan wording.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [co-parenting, custody, parenting-plan, calendar, visitation, shared-custody, holidays, family-law]
---

# Co-Parenting Custody Calendar

A custody schedule is a 52-weeks-a-year logistical contract executed by two
people who may barely speak. Most parenting plans die not on big legal
questions but on calendar mechanics: whose Friday does the exchange happen,
who gets spring break in even years, does a 2-week vacation create a
9-day gap for the other parent, and whether the split is actually 50/50
or quietly 42/58. This skill turns plan language into dated reality —
and reality back into evidence.

## When to Use

- Drafting a parenting plan: choosing between alternating weeks, 2-2-3,
  3-4-4-3 — and seeing the actual overnight counts, not the brochure math
- Mediation or court prep: an honest audit of what a proposed schedule
  really gives each parent (overnights, weekends, longest gap)
- Holiday season planning: who has first pick this year, what the
  alternating-priority table says for the next 12 months
- One parent travels / deployment / work shift changes: patch the rotation
  and handle make-up time fairly
- Dispute about missed exchanges: a dated log with makeup-time doctrine
- Rebuilding after "we just sort of drifted" into an informal schedule

**Don't use for:** situations involving abuse, abduction risk, or urgent
child-safety concerns — those need a lawyer and possibly emergency orders
immediately, not calendar tooling. International parental abduction risk
(Hague Convention cases) is also out of scope.

## The Method

1. **`plan`** — generate the dated rotation from a block-boundary start
   date. Print run-by-run (which parent, from when to when), overnight
   counts and percentages, exchanges per month. `--ics` exports an
   all-day custody calendar plus exchange events with a 12-hour pack
   reminder.
2. **`holidays`** — the year's holiday table. Alternating priority
   (odd/even years flip first pick) with Mother's/Father's Day pinned
   to the named parent and the child's birthday as a listed holiday.
   Includes the plan-wording fix that kills edge disputes (6pm prior
   day / 8am next day).
3. **`fairness`** — audit any rotation over any period: overnights,
   percent, weekend days, longest gap without an overnight. Flags
   < 35% (the common US shared-custody threshold; below it, child
   support formulas and "custodial parent" designations shift).
4. **`override`** — patch a date range to one parent with the make-up-time
   rule: equal-length block offered in writing within 30 days, and a
   ready log entry. This is the single biggest source of quiet drift.

```bash
# See what 2-2-3 actually looks like for the next 4 weeks
python3 scripts/co_parenting_calendar.py plan --schedule 2-2-3 \
    --start 2026-11-02 --days 28 --label-a "Alex" --label-b "Sam"

# Full-year audit of alternating weeks
python3 scripts/co_parenting_calendar.py fairness --schedule alternating-week \
    --start 2026-01-01 --end 2026-12-31

# Holiday table for 2027, Sam first pick in odd years
python3 scripts/co_parenting_calendar.py holidays --year 2027 --odd B \
    --mother A --father B --birthday 2019-05-14

# Patch a trip + make-up doctrine
python3 scripts/co_parenting_calendar.py override --from 2027-03-30 \
    --to 2027-04-10 --parent A --reason "work trip"
```

## Rotation Cheat Sheet

| Schedule | Cycle | Overnights | Best for | Watch out |
|---|---|---|---|---|
| alternating-week | 14d | 50/50 | kids >10, parents far apart | long gaps; mid-week contact must be written in |
| 2-2-3 | 14d | 50/50 | younger kids, short gaps | 2 exchanges/week — needs low-conflict cooperation |
| 3-4-4-3 | 14d | 50/50 | school-age, weekend-focused | "which Thursday" confusion; print the calendar |
| primary + visits | varies | <35% | infants, high conflict, distance | child-support and designation effects |

## Common Pitfalls

1. **Starting the rotation on a non-boundary date.** `--start` must be a
   block boundary (Monday for week-based patterns); otherwise every
   printed block is shifted and the ICS lies.
2. **Trusting "50/50" marketing.** Alternating weeks over a school year
   is 50/50 only if holidays and summer are separately split — run
   `fairness` on the plan-as-written, not the label.
3. **Ignoring the longest-gap stat.** A vacation override can create a
   14+ day gap for a young child. Check `fairness` after every override.
4. **Holidays by date, not by rule.** "Thanksgiving with Mom" without an
   odd/even rule guarantees a 2027 fight. The `holidays` table alternates
   priority yearly and pins Mother's/Father's Day.
5. **No exchange-time wording.** Plans that say "exchange Friday" without
   a time produce parking-lot standoffs. Write 6pm/8am windows.
6. **Treating makeup time as optional.** The make-up rule (equal block,
   written offer within 30 days) is what keeps a one-off override from
   becoming the new normal.
7. **Using this output as legal advice.** It's a calculator and wording
   aid. State law varies (thresholds, holiday definitions); a family-law
   attorney should review anything filed with a court.

## Verification Checklist

- [ ] Start date is a block boundary (Mon for week-based schedules)
- [ ] Overnight percentages match expectations of both parents
- [ ] Longest-gap checked after adding any override
- [ ] Holiday table shows odd/even alternation and pinned days
- [ ] ICS imports into Google/Apple calendar with exchange times
- [ ] Make-up offers documented in writing when overrides happen

## References

- `references/parenting-plan-clauses.md` — clause library for exchanges,
  holidays, make-up time, right-of-first-refusal, communication protocols
  (parenting apps), and the dispute ladder short of court.
