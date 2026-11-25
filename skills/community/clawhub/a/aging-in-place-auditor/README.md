# Aging-in-Place Auditor

**One in four adults over 65 falls every year. Falls are the leading cause of injury death in that age group — and nearly every top hazard is a $25–$300 fix that nobody in the family knows to look for.**

The typical sequence: an aging parent insists on staying home (rightly — it's what most people want and it's usually cheaper), the adult children visit at the holidays, sense that something's off, and either do nothing or jump to "we need to move you." What's missing in between is the priced, prioritized hazard list: the grab bar, the night-path lighting, the second stair rail, the rug that's going to break a hip.

## What it does
- **Scored room-by-room audit** (bathroom, bedroom, stairs, kitchen, floors, entries, lighting) — 23 hazards, each with *why it matters*, the fix, and a cost band. Interactive, JSON, or demo mode.
- **Three action tiers:** this weekend (<$100), this month (contractor), plan & budget (stair lift, curbless shower, first-floor conversion with real pricing).
- **Escalation honesty:** repeat falls + living alone routes to medical-alert and PT balance programs, not just hardware; multilevel home + walker routes to an OT assessment. Hardware can't fix pharmacology — the audit sends sedating-meds and bifocal-on-stairs findings to the doctor.
- **Funding routes:** Medicare Advantage home-support allowances, Medicaid HCBS waivers, VA HASA, Area Agency on Aging grants, renter rights under the Fair Housing Act.

## Example
```
$ python3 scripts/aging_audit.py --demo
PROFILE: 82y, aid=walker, falls/yr=1, lives_alone=True, multilevel=True
TOTAL RISK SCORE: 126/219 (58%) — HIGH

TIER 1 — this weekend (<$100)
  1. Floors: Loose throw rugs [15 pts] fix: Remove, or fix with dual-sided rug tape ...
  2. Stairs: Rail on only one side / no rail [15 pts] fix: Rail BOTH sides, 34-36in ...
  ...
ESCALATION
  ! Walker/wheelchair + stairs: first-floor living plan or stair lift is not optional...
```

Stdlib-only Python; no data leaves the machine.

## License
MIT
