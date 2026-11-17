---
name: border-buddy
description: "Pre-trip border intelligence: visa requirements by nationality, passport validity rules, Schengen 90/180 day stay calculators, yellow-fever certificate requirements, duty-free/cash customs limits, and transit-visa checks for any route. Use when the user asks about visas, entry rules, passport validity, how long they can stay, customs allowances, or whether they need vaccinations for a trip."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, visas, schengen, customs, border, passport, trip-planning]
---

# Border Buddy

Answer the three questions every international trip actually depends on — *Do I need a visa? Is my passport valid enough? What can I bring through customs?* — plus the one people always get wrong: *how long can I legally stay?* (the Schengen 90/180 trap).

## Overview

`border-buddy` combines an embedded rules engine (visa policy snapshots, passport validity rules, health certificate requirements, customs allowances for ~50 countries) with a precise **Schengen 90/180-day rolling-window calculator**. It turns "I'm a Brazilian passport holder flying to Portugal via Frankfurt for 6 weeks" into a structured entry-readiness report — before you book non-refundable tickets.

The scripts run fully offline on an embedded knowledge snapshot. Immigration rules change — always pair this skill with a live check of the destination's official immigration site (the report includes the right authority to verify with, per country).

## When to Use

- User asks: "do I need a visa for X?", "how long can I stay in Europe?", "is my passport valid for Japan?"
- Planning any international itinerary with connections (transit visa checks are the #1 surprise)
- Counting Schengen days across a multi-trip year — the rolling window defeats manual counting
- Checking what can be carried through customs: alcohol, tobacco, cash (the €10,000 / $10,000 declaration threshold)
- Verifying vaccination certificate needs (yellow fever is the big one for Africa/South America routes)

**Don't use for:** asylum/immigration-law advice, work-permit or residency applications, or anything involving criminal-record entry waivers (ETA/ESTA eligibility denials) — those need official channels or a lawyer. This is trip-planning intelligence, not legal advice.

## How It Works

1. **Load nationality + destinations** (IATA-style country codes or names).
2. **Visa matrix lookup** — each destination has a policy table keyed by nationality group: `visa_free`, `visa_on_arrival`, `eta`, `evisa`, `visa_required`, plus max stay days and notes.
3. **Passport validity check** — applies the 6-month rule (or the country-specific exceptions) against the passport expiry date; flags the "3-month + valid-for-stay" Schengen nuance.
4. **Health rules** — yellow fever certificate required if coming from (or transiting through) an endemic country; lists the relevant endemic set.
5. **Customs snapshot** — duty-free alcohol/tobacco allowances and the cash-declaration threshold for the destination.
6. **Transit checks** — every layover country over the airside-transit threshold gets its own visa row (China, UK, US, Canada, Australia require transit visas for many nationalities).
7. **Schengen calculator** (separate command) — reads a visit log (JSON/CSV), computes the rolling 180-day window from any reference date, and reports days used / remaining / overstay warnings.

## Quick Start

```bash
# Entry-readiness report for a trip
python3 scripts/border_buddy.py check \
  --nationality BR --destination PT \
  --transit DE --stay-days 42 --purpose tourism \
  --passport-expiry 2027-03-01

# How many Schengen days do I have left after this year's trips?
python3 scripts/border_buddy.py schengen --visits visits.json --on 2026-09-15

# See it work end-to-end with built-in sample data
python3 scripts/border_buddy.py demo

# List every country rule in the snapshot
python3 scripts/border_buddy.py rules --destination JP
```

## Steps (Agent Workflow)

1. Collect: **nationality**, **destination(s)**, **transit point(s)**, **trip purpose**, **dates**, **passport expiry**. (Transits are optional but ask — most surprises live there.)
2. Run `check` with what you have; the report flags every missing input that matters.
3. If any destination is Schengen and the user travels repeatedly, run `schengen` with their visit history.
4. Read the report back to the user **with the verification links/authorities listed** — never present the snapshot as guaranteed-current.
5. If a rule looks stale (snapshot includes `as_of` dates), do a live web check of the official source and reconcile.

## Output Shape

```
ENTRY READINESS ─ Portugal (PT) for BR nationals
  Visa:         NOT REQUIRED (Schengen 90/180) ✓
  Max stay:     90 days in any 180-day window
  Passport:     VALID — expires 2027-03-01, must be valid 3 mo beyond
                departure and issued within 10 years ✓
  Transit DE:   AIRSIDE TRANSIT OK (no visa) ✓
  Yellow fever: not required (not arriving from endemic country)
  Customs:      1L spirits / 4L wine · cash > €10,000 must be declared
  VERIFY WITH:  sef.pt (Serviço de Estrangeiros e Fronteiras)
```

## Common Pitfalls

1. **Counting Schengen days with a calendar app.** The 90/180 rule is a *rolling* window — the day you leave doesn't count as a stay day, and old trips fall out of the window mid-trip. Use the calculator; manual counting is how people get 5-year bans.
2. **Forgetting transit visas.** A 3-hour layover in London (LHR) or Toronto (YYZ) still requires a transit visa for many nationalities. Always pass `--transit`.
3. **Trusting the 6-month rule everywhere.** Some countries require 6 months validity, others only "valid for the duration of stay". The rules table encodes per-country requirements — don't apply one rule globally.
4. **Treating the snapshot as live law.** Visa policy changed weekly somewhere in the world since this snapshot's `as_of` date. The report always names the official source to verify against — show it to the user.
5. **Confusing visa-free stay length with the Schengen allowance.** e.g., Americans get 90 days in *Portugal* under the PT rule but it's the *same 90/180 pool* as the rest of Schengen. Multi-destination European trips must be budgeted from one pool.
6. **Purpose changes everything.** "Tourism" answers don't apply to work, study, or paid performances. Always confirm purpose before answering.

## Verification Checklist

- [ ] Nationality and every destination (including transits) passed as ISO codes or names
- [ ] Passport expiry checked against the destination's specific validity rule
- [ ] Schengen destinations cross-checked with `schengen` if the user has prior visits
- [ ] Report shown with "verify with" authorities — never as a guarantee
- [ ] Purpose of travel confirmed (tourism vs work/study changes visa class)

## One-Shot Recipes

**"I'm Indian, flying Delhi → Paris in May, 10 days, passport expires November"**
```bash
python3 scripts/border_buddy.py check --nationality IN --destination FR \
  --stay-days 10 --purpose tourism --passport-expiry 2026-11-30
# → visa required (Schengen short-stay), passport OK but tight, apply ≥3 weeks out
```

**"How many days can I still spend in Europe this year?"**
```bash
python3 scripts/border_buddy.py schengen --visits my_visits.json --on 2026-10-01
# → days used, days remaining, date the oldest trip exits the window
```

## References

- [`references/visa-rules.md`](references/visa-rules.md) — how the policy matrix is structured, nationality groups, transit rules
- [`references/schengen-180.md`](references/schengen-180.md) — the 90/180 algorithm, worked examples, common edge cases
