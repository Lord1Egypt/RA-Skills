---
name: elder-care-coordinator
description: "Use when a family is coordinating care for an aging parent or relative — shared task rosters, medication check-call schedules, doctor-visit briefing packets, decline-event tracking, emergency info sheets, and the 'who-is-doing-what' visibility that siblings spread across timezones need. Builds a single source of truth from scattered group chats and prints caregiver handoffs, visit briefs, and escalation cards — without being a medical device."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [eldercare, caregiving, aging-parents, care-coordination, family, medication-reminders, handoff]
---

# Elder Care Coordinator

## Overview

Someone's mother lives alone 400 km away. Three siblings, two spouses, one niece, and a neighbor all help — coordination happens in a WhatsApp group with 200 messages a week, and critical things fall through: nobody confirmed Tuesday's rheumatology follow-up, two people bought insulin refills the same day, and when she fell at 6AM nobody knew where her DNR preference document was.

This skill is the antidote: a **single structured source of truth** for a family care circle, kept in plain files the family owns, that generates:

1. **Care circle roster** — who exists, roles, contact, timezone, what they reliably do (driving, pharmacy runs, insurance calls) and their limits.
2. **Task & appointment roster** — recurring and one-off, with owners and due dates; `today` prints the day's coverage and any unassigned critical items.
3. **Medication check-calls** — the schedule of who calls about what, pill-tray fill dates, refill radar (x days left → task generated), and interaction notes from the pharmacist (free-text, not a database).
4. **Doctor-visit packets** — one command generates the briefing: current med list with doses, recent events, questions to ask, changes since last visit, plus a visit-report template to fill in the waiting room.
5. **Event log** — falls, confusion episodes, hospitalizations, "seemed off" observations with dates; the trend section makes gradual decline discussable at family meetings instead of arguable.
6. **Emergency card** — one printable page: conditions, meds, allergies, doctors, insurance, code status, lockbox code, who to call first. The thing you want to already exist at 3AM.

The design rule: **nothing here is medical advice or a medical record system.** It's the family's shared notebook with structure — the difference between "I thought you called the neurologist" and a printed roster.

## When to Use

- Setting up coordination after a diagnosis, a fall, a hospital discharge, or when a parent starts "needing a little help"
- Running the weekly/monthly care meeting from a printed agenda (`meeting` command)
- Preparing for any doctor visit (`visit-brief`)
- Checking today's coverage (`today`) — who's doing what, what's unassigned
- After any incident: log it, and regenerate the emergency card if anything changed
- Onboarding a new helper (paid caregiver, neighbor, relative): print the handoff, not a 40-message chat scrollback
- Refill radar and appointment countdowns without anyone keeping it in their head

**Don't use for:** medication dosing decisions (pharmacist/physician), diagnosing symptoms, replacing the patient portal or official care plans, or emergencies in progress (call emergency services). This is family logistics, not medicine.

## How It Works — Numbered Workflow

1. **Set up the care circle** — `person add` for every helper: name, role, phone, timezone, strengths/limits (free text). Then the care recipient's profile: conditions, allergies, doctors, pharmacy, insurance, code status, key locations (spare key, med list on fridge).
2. **Build the recurring schedule** — `task add --recur weekly` for the load-bearing routines: Sunday pill-tray fill, Monday check-call, Wednesday grocery run, monthly bill review. Every recurring task needs exactly one owner (or an explicit rotation).
3. **Log events as they happen** — `event log "seemed confused at dinner, asked about Aunt Lena twice"` with date and severity. Events feed visit briefs and the trend view.
4. **Each morning or before shifts: `today`** — the day sheet: appointments, tasks due, who's on check-call, refill countdowns, flagged follow-ups.
5. **Before each appointment: `visit-brief <doctor>`** — prints the packet (meds, events since last visit, questions list) and a blank visit-report template. After: `visit-report` fills the record back in.
6. **Monthly: `meeting`** — printed agenda: open tasks, overdue items, event trends, weight/appointment adjournments, "what's wearing us out" rotation review. The skill tracks task load per person and flags imbalance.
7. **Quarterly or on change: `emergency-card`** — regenerate and reprint; the old copies in wallets and on the fridge get replaced.
8. **Handoffs** — `handoff <person>` prints everything a new/substituting helper needs: recipient profile, today + upcoming week, key contacts, routine explanations, "don't do" notes (e.g., "don't mention the driving conversation — Elin handles it").

## Quick Start

```bash
python3 scripts/elder_care.py person add --name "Maria" --role daughter --phone +7... --tz +3 --notes "pharmacy runs, Russian-speaking doctor visits"
python3 scripts/elder_care.py profile set --conditions "hypertension, AFib" --allergies "penicillin" --code-status "DNR in file, discussed 2026-03"
python3 scripts/elder_care.py task add --title "pill tray fill" --recur weekly --owner Maria --dow sun
python3 scripts/elder_care.py task add --title "check call" --recur daily --rotation "Maria,Jon,Anna"
python3 scripts/elder_care.py med add --name "warfarin" --dose "5mg" --refill-left 12 --refill-note "Pharmacy: Apteka 47, needs Rx"
python3 scripts/elder_care.py today
python3 scripts/elder_care.py visit-brief "Dr. Okafor cardiology"
python3 scripts/elder_care.py meeting
python3 scripts/elder_care.py emergency-card > card.txt
```

State: `care_state.json` beside the script. Pure stdlib, no network, no accounts. Print outputs; the family group chat gets photos of pages, not exports.

## Output Examples

**`today` (excerpt):**
```
TODAY Tue 2026-09-29 — coverage: Maria (call), Jon (pharmacy)
  09:00  rheumatology follow-up (Dr. Weiss)      [owner: Anna]  — BRIEF READY: visit-brief "Dr. Weiss"
  check call (daily)                              [rotation: Maria]
  refill radar: warfarin 12 days left -> generate pharmacy task at 7
  FLAG: 2 tasks unassigned (transport Thu, insurance call) — assign or drop
```

**`meeting` (excerpt):**
```
MONTHLY CARE MEETING — 2026-09-29
1. Overdue: neurologist visit report (Anna, 9 days)
2. Event trend: 3 "confusion episodes" logged in 30 days (1/month before) -> raise at Oct 14 visit
3. Load: Maria 11 tasks/mo, Jon 9, Anna 3  <- ANNA UNDERLOADED, ask before adding to Maria
4. Upcoming: flu shot (Oct), furnace filter (Jon), eyewear check (unassigned)
```

## Common Pitfalls

1. **The group chat as the source of truth.** Chats are where commitments go to die: no owner, no due date, buried in 40 messages about grandkids. Every commitment in chat that matters gets one line here (`task add`), even if it feels bureaucratic.
2. **Rotation without a backup rule.** "We take turns calling" fails the first week someone travels. Every rotation entry needs a swap rule (notify the group + find replacement OR the task defaults to the next person — pick one, state it).
3. **Recording sensitive data in a shared cloud doc.** Health details leak through shared links and abandoned accounts. This skill keeps data in one local file the family controls; if you sync it (family git repo, encrypted share), say so explicitly in the family and note who has access.
4. **The emergency card that's out of date.** A card generated once and photocopied five times is worse than none — new med added in March, card in wallets still shows April's list. Regenerate quarterly and on every med change; the footer shows the generation date.
5. **One person becoming the invisible coordinator.** The default failure of family care: one sibling does everything, burns out, resents. The `meeting` output shows task-load per person — use it to rebalance before the resentment, not after.
6. **Ambiguous code status / documents.** "We think there's a DNR somewhere" is a 3AM catastrophe. `profile set --code-status` plus where the document physically is. Same for POA (power of attorney) — healthcare and financial, who holds them, where the originals live.
7. **Med list drift.** After every visit that changes anything: update meds the same day (the visit-report template ends with "did meds change? y/n — if y, run med update now"). An out-of-date med list in a visit brief is actively dangerous.
8. **Using the skill as a diagnosis log.** Record observations ("asked the same question twice"), never interpretations ("early dementia"). Observations are shareable with doctors; interpretations start family wars.

## Verification Checklist

- [ ] `person add` + `profile set` + `task add` (one recurring, one one-off) all wrote to `care_state.json`
- [ ] `today` shows the recurring items on the right days and flags unassigned tasks
- [ ] `med add` with `--refill-left` shows in the refill radar of `today` at the threshold
- [ ] `visit-brief` prints the packet: meds, events since last visit of that doctor, question list
- [ ] `event log` then `meeting` shows the event trend section
- [ ] `emergency-card` output is one page and includes the generation date
- [ ] `handoff` includes profile + schedule + contacts
- [ ] No network imports (grep requests/urllib/socket — empty)

## One-Shot Recipes

**New helper onboarding (paid caregiver starts Monday):**
```bash
python3 scripts/elder_care.py handoff "NewCaregiver"   # print + hand over
python3 scripts/elder_care.py emergency-card            # fresh card for their binder
```

**Post-hospital discharge chaos:**
```bash
python3 scripts/elder_care.py event log "discharged Community Hosp, hip pinning, PT 2x/wk starts Thu" --severity 3
python3 scripts/elder_care.py med update warfarin --refill-left 20 --note "dose changed 5->4mg per discharge"
python3 scripts/elder_care.py task add --title "PT transport Thu" --owner Jon --due 2026-10-01
python3 scripts/elder_care.py emergency-card > card.txt   # reprint; meds changed
```

**The monthly meeting:**
```bash
python3 scripts/elder_care.py meeting | lp   # or print to PDF; run the meeting from paper
```

## License & Disclaimer

MIT. Family-coordination tooling, not a medical device or medical record system: no clinical advice, no dosing decisions, no diagnosis. Medication data is a family-maintained list; the pharmacist and physicians own the truth. In an emergency call local emergency services first.
