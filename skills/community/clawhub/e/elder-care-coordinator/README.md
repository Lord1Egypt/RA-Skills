# Elder Care Coordinator

**Skill:** `elder-care-coordinator` · v1.0.0 · MIT · ClawHub `@voronindenis5/elder-care-coordinator`

## The real-world problem

An aging parent living far away, three siblings in different timezones, a niece, and a helpful neighbor — coordinating care through a group chat with 200 messages a week. That's the reality for the ~50M+ family caregivers in the US alone (and comparable shares in Europe and East Asia as populations age). The failure modes repeat everywhere:

- Nobody confirmed Tuesday's rheumatology follow-up; two people bought the same refill
- The "invisible coordinator" (usually one sibling) accumulates 70–80% of the load and burns out
- When she fell at 6AM, nobody knew where the advance directive or the current med list was
- Gradual decline is invisible day-to-day — each "seemed confused at dinner" gets explained away until the crisis that makes it undeniable

Doctors respond to dated observation series; they dismiss anecdotes — and families argue about anecdotes for years.

## What it does

A single structured source of truth in a local JSON the family owns, generating printable artifacts. Pure stdlib Python, no accounts, no cloud:

- **`person add` / `profile`** — care-circle roster (strengths/limits/timezones) + recipient profile (conditions, allergies, doctors, pharmacy, code status, POA, key locations)
- **`task add --recur daily|weekly --rotation A,B,C`** — recurring and one-off tasks with owners; `today` prints the day sheet: coverage, overdue items, unassigned flags, refill radar
- **`med add --refill-left N`** — med list with refill countdown; radar fires at ≤7 days
- **`event log`** — observations (never interpretations), severity 1–3, dated — the decline documentation doctors take seriously
- **`visit-brief <doctor>`** — the appointment packet: med list, events since *that doctor's* last visit, accumulated questions list, plus a blank visit-report template; `visit-report` files it back and nags you to update meds the same day
- **`meeting`** — printed monthly agenda: overdue items, event trend vs. prior 30 days, task-load-per-person imbalance flag, refill/upcoming, documents check, respite
- **`emergency-card`** — one printable page: call order, conditions, allergies, meds, code status, baseline function, generation date ("reprint after any med change")
- **`handoff <person>`** — everything a new paid caregiver or respite helper needs, replacing the 40-message chat scrollback

## Who needs this

- **The sandwich generation** coordinating a parent's care from a distance
- **Families after a diagnosis, fall, or hospital discharge** — the exact moment chaos peaks
- **The overloaded sibling** — the load-imbalance report turns resentment into a rebalancing conversation
- **Anyone hiring paid caregivers** — a printed handoff beats an hour of verbal briefing
- **The parent themselves**, where cognition allows: attend the meeting, see the log, keep dignity and veto rights

## Example

```bash
python3 scripts/elder_care.py task add "check call" --recur daily --rotation "Maria,Jon,Anna" --critical
python3 scripts/elder_care.py med add warfarin --dose 5mg --refill-left 6 --refill-note "Apteka 47, needs Rx"
python3 scripts/elder_care.py today
# TODAY Tue 2026-09-29 — coverage: Jon
#   check call   [Jon (rot 2/3)] *CRIT
#   insurance call  []  (due 2026-09-20 OVERDUE)
#   refill radar: warfarin 6d left | Apteka 47, needs Rx renewal
python3 scripts/elder_care.py emergency-card > card.txt   # wallets, fridge, glovebox
```

## Scope

Family logistics, explicitly **not** a medical device or medical record system: no clinical advice, no dosing decisions. The pharmacist and physicians own the clinical truth. Emergencies: local emergency services first.

## License

MIT © Denis Voronin
