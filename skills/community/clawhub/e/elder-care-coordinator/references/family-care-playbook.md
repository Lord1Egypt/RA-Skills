# The Family Care Coordination Playbook — Reference

## 1. Why family care coordination fails (and what actually works)

The research on family caregiving converges on the same failure points, regardless of country:

1. **Distributed, implicit coordination.** Siblings in different timezones coordinate by group chat and assumption. "I thought you were calling the neurologist" is the canonical post-mortem line of every care crisis.
2. **Invisible coordinator burnout.** One person (usually the eldest daughter, per the literature) silently accumulates 70–80% of the load. Resentment builds for a year, then detonates at a holiday.
3. **Information fragmentation.** Med list on the fridge (out of date), appointment cards in a drawer, advance directive in a safe-deposit box nobody can open, insurance portal login in one person's head.
4. **Decline blindness.** Gradual decline is invisible day-to-day and undeniable only in retrospect — unless someone logs observations. "Seemed confused at dinner" × 3 in a month is a doctor conversation; individually, each instance gets explained away.
5. **Handoff loss.** When a new helper (paid caregiver, respite worker, relative) starts, the tribal knowledge lives in chat scrollback and gets transmitted verbally in 20 rushed minutes.

The fixes are structural, not motivational: **explicit owners + due dates, load visibility, an event log, printable artifacts** (day sheet, visit brief, emergency card, handoff). This skill implements exactly those five.

## 2. Roster design

**Every helper record**: name, role/relation, phone, timezone, and free-text strengths/limits. The strengths field matters more than it looks — "can do weekday mornings", "comfortable with insurance calls", "will NOT do bathing care" lets the coordinator route instead of guess.

**The recipient profile**: conditions, allergies, current doctors (name/specialty/clinic/phone), pharmacy, insurance IDs, code status (DNR/DNI/full code — and WHERE the document is), POA holders (healthcare and financial — separate documents in most jurisdictions!), key locations (spare key, med list, documents binder), and preferred hospital.

**Rotation rule** (state it explicitly in the state file and at meetings): if a rotation member can't take their turn, they (a) notify the group ≥48h out and (b) find their replacement — or the task auto-defaults to the next person in the ring (pick ONE of these rules; ambiguity is how Monday's call gets skipped).

## 3. Task & schedule mechanics

- **Recurring tasks** need: title, frequency (daily / weekly + day-of-week / monthly + day), owner (single person or rotation list), and a "critical" flag for load-bearing items (pill-tray fill, check calls, refills).
- **One-off tasks** need: title, owner, due date. Unassigned critical items with near due dates get flagged on every `today` until assigned or explicitly dropped.
- **Refill radar**: every med carries `refill_left` (days) and a threshold (default 7). At threshold, `today` starts printing a pharmacy task suggestion. The refill note field holds the pharmacy's quirks ("needs 48h notice", "Rx expires — Dr. Okafor renews").
- **Load balancing**: the meeting agenda computes tasks-per-person over the trailing 30 days. Differences >2× within the family = a rebalancing conversation. The point isn't perfect equality — it's that imbalance is a decision, not an accident.

## 4. Doctor visits: the briefing packet

Before the visit (`visit-brief <doctor>`):

1. **Med list** — name, dose, times, prescriber, last-change date. The single most-valuable page in geriatrics: the doctor reconciles against their chart and catches drift.
2. **Events since THIS doctor's last visit** — falls, confusion episodes, weight changes, ER trips, "seemed off" days. Filtered to their specialty window (cardiology cares about the syncope, less about the hip).
3. **Questions list** — accumulated in the state file between visits (family members append as things come up; nobody trusts memory in the waiting room).
4. **Changes since last visit** — meds started/stopped/dosed, new diagnoses, other doctors' interventions.
5. **Blank visit-report template** — date, provider, what changed, follow-ups, next appointment. Fill it in the waiting room or the car; `visit-report` files it the same day.

The visit-report closes the loop: it feeds the next brief's "changes since last visit" and updates the doctor's last-visit date for the event filter.

## 5. The event log (decline documentation)

Log **observations, not interpretations** (pitfall #8 in the SKILL.md): "asked the same question twice at dinner", "needed a hand getting up from the chair", "left stove on — found by neighbor". Each with date and severity 1–3 (1 noticed, 2 function-limiting, 3 safety incident).

The `meeting` trend view groups by 30-day window. A doubling of confusion-episode counts is the difference between "Mom's fine, stop worrying" and "here's the log, we need a cognitive workup". Doctors respond to dated series; they dismiss anecdotes — and families argue about anecdotes for years.

Sensitive-events caveat: the log may contain material the recipient wouldn't want broadcast (incontinence, finances, family conflict). State who sees the raw log vs. the printed briefs; the emergency card contains the clinical minimum, not the diary.

## 6. The emergency card (what goes on it)

One page, large print, generation date in the footer:

- Name, DOB, address, phone
- Emergency contacts in call order (who's called FIRST — usually the local person, not the loudest sibling)
- Conditions (the ones ER needs: diabetes, AFib on anticoagulation, epilepsy, dementia)
- Allergies & adverse reactions (drug name + reaction, not just "allergic")
- Current meds with doses (or "med list attached, updated <date>")
- Doctors + pharmacy with phones
- Insurance IDs
- Code status + where the directive physically is
- Baseline function ("normally walks unaided, glasses, hearing aid left ear") — so responders can tell deficit from baseline
- Practical: door lockbox code, pet present ("cat will hide"), preferred hospital

Distribute: recipient's wallet, fridge door, each helper's phone photo, car glovebox of the local helper. **Reprint quarterly and after every med change.**

## 7. Family meeting agenda (the `meeting` output)

Monthly, 30 minutes, from paper:

1. Coverage review — overdue items, unassigned items, next 30 days' appointments
2. Event trends — counts vs. prior window; anything to raise with a doctor
3. Load review — tasks/person; rebalance; explicitly ask the overloaded one what to hand off
4. Upcoming seasonal — flu shots, heating/AC service, driving conversation status, holiday coverage
5. Documents check — advance directive current? POA accessible? Insurance cards expiring?
6. Respite — who's tired, who needs a weekend off next month

The last two items are the ones families skip and wish they hadn't. Burnout prevention IS care quality: a burned-out coordinator makes mistakes, and the replacement curve is brutal.

## 8. Privacy, ethics, and dignity

- The recipient is an adult with rights. Where cognition allows, they attend the meetings, see the log, and veto entries. Coordinating care FOR someone vs. AGAINST their will are different projects; document their preferences ("doesn't want to discuss the care home option with the whole family").
- Data minimization: the state file has names, phones, diagnoses, insurance IDs. Sync only via channels the family controls (encrypted share or family git repo); never a public link, never a shared "family" account of unclear ownership. Note in the file who holds access.
- This is not a medical record system. No clinical decision logic. When the skill's output and the physician/pharmacist disagree, the clinician wins, and the record gets corrected the same day.

## 9. When to escalate beyond family coordination

This skill routes to professionals, never substitutes:

- Medication questions, interactions, dosing → pharmacist (free, underused) and prescriber
- Repeat falls, weight loss, confusion trend → geriatrician workup (the event log is your referral letter)
- Caregiver depression/burnout (constant exhaustion, dread, anger) → family doctor; caregiver support lines exist in most countries
- Suspected abuse by a paid helper → adult protective services; the event log is evidence
- Sudden severe symptoms → emergency services, then update the event log after

## 10. Geographies and systems

The structure is jurisdiction-agnostic; the specifics differ:

- **Home services** (aide hours, meals, transport) — via national/local programs (Medicaid waivers in the US, social care assessments in the UK, municipal services in the EU). The task roster tracks applications and assessments as tasks with owners.
- **Insurance/paperwork** — the most-hated, most-deferred category. One owner, calendar-blocked time, and a "documents needed" checklist per case.
- **Cross-border families** — the roster's timezone field prevents the 6AM check-call assignment mistakes; `today` renders each person's local time for their tasks.
