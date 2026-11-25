---
name: aging-in-place-auditor
description: "Use when an older parent or relative is staying in their home, after a fall or near-fall, when visiting and noticing trip hazards, or when the family asks 'is the house safe for grandma / can dad keep living here'. Room-by-room fall-risk audit with scored hazards, prioritized fixes priced in cost bands, and the weekend top-5 action list."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [aging, seniors, fall-prevention, home-safety, accessibility, eldercare]
---

# Aging-in-Place Auditor

## The problem it solves
1 in 4 adults 65+ falls every year; falls are the leading cause of injury death in that group and the #1 driver of the nursing-home transition. Almost every serious-home-hazard is a **$25–$300 fix** — a grab bar, a LED bulb, a threshold ramp — but families don't know what to look at, in what order, and what each fix costs. After a first fall, an OT home assessment takes weeks to schedule; this skill is the structured 45-minute pass you can do during a holiday visit.

## When to trigger
- A parent/relative is aging in place; a fall, near-fall, new walker/cane, or hospital discharge happened.
- User asks "what should I check in my mom's house" / "how do I fall-proof a bathroom".
- A family is deciding **stay-with-modifications vs. downsize/move** and needs the priced fix list first.

## Steps
1. Gather profile: age, mobility aid (none / cane / walker / wheelchair), fall history (none / 1 / 2+), vision/hearing notes, single-story vs stairs, live-alone.
2. Run the room audit (bathroom, bedroom, stairs/hallways, kitchen, entries, exterior) — the script scores each hazard item 0–3 (absent … severe) with the **why** and the fix attached. Input: interactive answers, a JSON file, or `--demo`.
3. Score → three priority tiers:
   - **TIER 1 (do this weekend, <$100 total):** grab bars, pathway lighting, rug removal, cord rerouting, raised toilet seat, non-slip mats.
   - **TIER 2 (this month, contractor):** stair rail second side, walk-in shower conversion, thresholds >13 mm ramped, motion lights, reachable storage re-org.
   - **TIER 3 (plan/budget):** stair lift, first-floor bedroom conversion, doorway widening (wheelchair 815 mm), curbless shower.
4. Print the priced fix list (cost bands, DIY vs contractor), the lighting upgrade table (aging eyes need 2–3× the lux), and a printable summary to bring to the doctor/OT.
5. Escalation flags: repeat falls + live-alone → medical alert device row; multiple Tier-1 findings → recommend a professional OT home assessment; cognitive decline signs → route to care-coordination, not just hardware.

## The knowledge base (see references/)
- **Bathroom is half the battle:** toilet grab bar (17–19 in seat height), shower grab bars *in stud, weight-rated 250 lb+* (towel bars are not grab bars), non-slip strips, handheld shower for seated bathing, night light with dusk sensor.
- **Stairs:** rail on BOTH sides at 34–36 in, contrast strip on top/bottom steps, switch at top AND bottom, no clutter, and the "can this become a first-floor bedroom?" question.
- **Lighting:** hallway/bedroom/bathroom night paths; ~2–3× lumens vs a 30-year-old's needs; bedside lamp reachable without getting up; motion-sensor plugs.
- **Floors:** throw rugs = the single most-common trip object; thresholds >13 mm bevel or ramp; no cord crossings; stair carpet wear = slide hazard.
- **Bed/toilet height:** knees ~90° when seated; too-low beds and soft sofas are extraction traps after a fall.
- **The dose of honesty:** hardware reduces risk, but 2+ falls in a year, live-alone status, and vision loss together justify an OT assessment and a medical-alert decision — the script says so instead of selling grab bars.

## Pitfalls
- Towel bars and suction-cup bars are NOT grab bars — must hit studs or use blocking, weight-rated.
- Don't "surprise-remodel" a parent: autonomy matters; frame the audit as *their* checklist, offer choices.
- A single grab bar won't fix a balance problem — pair hardware findings with a doctor/PT balance review (ask about vitamin D, meds with sedating side effects, orthostatic hypotension).
- Wheelchair numbers ≠ walker numbers: plan doorways 815 mm clear for chairs, 610 mm for walkers, and 1500 mm turning circles if a chair is realistic.
- Rental/landlord: grab bars need permission (Fair Housing Act reasonable-modification rights apply — see references).

## Example
```
$ python3 scripts/aging_audit.py --demo
PROFILE: 82F, walker, 1 fall (6 mo ago), stairs, lives alone
TOTAL RISK SCORE: 41/78 — HIGH
TIER 1 — this weekend (<$100):
  1. Bathroom: no grab bar at toilet           [8 pts] fix: mounted bar $25-50   WHY: #1 transfer-fall point
  2. Hallway: no night lighting on bed->bath   [6 pts] fix: 2 motion plugs $25
  3. Throw rugs in hallway + kitchen           [6 pts] fix: remove/dual-sided tape $15
...
ESCALATION: repeat-fall + lives alone → discuss medical alert device this week.
```

## Files
- `scripts/aging_audit.py` — scored audit engine, tiering, priced fix list (stdlib only, interactive/JSON/demo).
- `references/hazard-catalog.md` — every scored item with why/fix/cost band.
- `references/modification-costs.md` — Tier-3 project pricing, wheelchair dimensions, funding routes (Medicare/Medicaid waivers/VASH/HOME).
- `README.md` — the real-world framing for adult children.
