# Garage Door Safety — Deep Reference

## 1. Injury mechanics (why this audit exists)
- CPSC/NEISS data: ~20,000–30,000 emergency-room injuries per year in the US involve garage doors; fingers crushed in section joints are the most common, followed by falling doors and "raced the door" impacts.
- A two-car door weighs 130–180 kg (250–400 lb). Fully wound torsion springs store enough energy to lift that mass in ~2 seconds — or to accelerate a steel winding bar through a wall.
- Children ≤ 15 account for a large share of pinches and impacts; since 1993, UL 325 has required photo-electric sensors (photo-eyes) and auto-reverse on all US openers.

## 2. The two reverse systems — and why both must be tested
| System | Trigger | Test | Standard behavior |
|---|---|---|---|
| Contact reversal | Door physically hits obstruction | 2×4 flat under center of closing door | Reverse within 2 s after touching |
| Non-contact (photo-eye) | Beam broken across the opening | Broomstick swept through beam ~5 cm above floor | Immediate reversal, no contact |
Contact reversal protects objects/limbs already under the door; photo-eyes protect what enters while it closes. Neither covers a child lying flat directly under a closing panel — the 2×4 test matters precisely because the beam is 10–15 cm up.

## 3. Opener mechanics that change the verdict
- **Down-force setting**: a friction-based "how hard before giving up" dial. Drift upward over years (vibration, cheap design) → door starts crushing. Symptom: door closes, then reopens after hitting the floor. Fix: turn down force 1/8 turn, re-run 2×4 test, repeat.
- **Down-limit setting**: how far the door travels. Set too far → door hits floor, opener "thinks" it hit an obstacle, reverses (the classic "door won't stay closed"). Fix: reduce travel 1 turn at a time.
- **Speed/openers with battery backup**: required in California (SB-969) for new openers; nice elsewhere for power-outage egress.
- **Pre-1993 openers**: no photo-eyes, often fixed-code remotes. UL 325 made them obsolete; the industry position is replacement, not repair. Destroy the old remotes.

## 4. Springs — the wear part nobody budgets
### Types
- **Torsion** (shaft + drums above door): modern standard, smoother, cycle ratings 10k/20k/33k/50k. Adjustment is PRO-ONLY (winding cones store lethal energy).
- **Extension** (stretch along horizontal tracks): older/lighter doors, cheaper, ~10k cycles. Replacement is more DIY-tolerant but still involves stretched steel under the door's full weight; safety cables through the spring are mandatory.

### Cycle economics (what the script computes)
```
cycles_used = years_in_service × openings_per_day × 365
remaining_pct = rating − cycles_used, floored at 0
replace_by = install_date + (rating / (openings/day × 365)) years
```
Realistic openings/day: 1-car commuting household 3–4; family with teen drivers 6–8; pedestrian-only entries add 1–2. A 10k spring at 6/day is done in 4.6 years — far short of the "10-year warranty" intuition. Labor ($100–200) dominates the visit, so replacing both springs (and aged rollers) in one visit is the correct move.

### Failure signatures to read aloud
- **Loud bang from garage, door stuck open or slamming** — torsion spring snapped. Do NOT disengage opener. Pro.
- **Door feels dead-heavy, opener runs but door doesn't move** — broken spring or stripped gear (LiftMaster/Chamberlain nylon main gear is a known 8–12 yr wear item).
- **Door stops mid-travel and reverses** — force/limit drift, or binding track; run the 2×4 and hand-balance checks before suspecting electronics.
- **Cable fray/pile-up on drum** — pro; cables are matched to springs.

## 5. The 12-point audit checklist (script walks these)
1. 2×4 contact reverse — PASS/FAIL
2. Photo-eye sweep — PASS/FAIL
3. Door hand-balance (half-open, no drift)
4. Manual release known + practiced (door closed)
5. Wall button ≥ 1.5 m and visible
6. Remote code rolling (post-1996) / opener age
7. Keypad code non-trivial + changed at move-in
8. Hinge/roller wear — no play, no screaming
9. Track alignment — no rub marks on door edges
10. Lubrication done this season (lithium/silicone)
11. Springs visually intact (gaps, kinks, rust = pro)
12. Safety cables through extension springs (older doors)

## 6. Maintenance calendar
| Cadence | Task |
|---|---|
| Monthly-ish | Open-door visual: springs, cables, rollers |
| Quarterly | 2×4 + photo-eye test |
| 2×/year | Lube hinges/rollers/springs; tighten hinge bolts |
| Every 5–7 yrs | Rollers; nylon upgrade pays for itself in noise |
| On schedule | Both springs at cycle forecast end (see script) |

## 7. What things should cost (US bands, 2026)
- Pair of torsion springs, installed: $150–$350
- Nylon roller set: $60–$120 installed
- Photo-eye pair replacement: $40–$80
- New opener (½ HP, battery backup): $250–$550 installed DIY-light
- Off-track door re-rail: $125–$250 (pro — cable tension)

If a quote is far above these bands, the audit sheet gives you a defensible scope to question — but never let cost pressure turn torsion work into DIY.

## 8. Sources & standing caveats
- UL 325 (garage door openers), DASMA spring cycle guidance, CPSC garage door safety publications, CA SB-969 battery-backup law.
- Cycle ratings are nominal; coastal corrosion, door weight creep (added insulation), and unlubricated coils cut life 20–40%.
- This reference is a safety instrument, not a repair manual for stored-energy components. Torsion = technician, full stop.
