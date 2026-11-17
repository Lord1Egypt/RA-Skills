# Garage Door Safety Audit

The largest moving object in your home is suspended over your car and your kids by springs under lethal tension — and almost nobody ever tests whether it auto-reverses. US emergency rooms treat ~30,000 garage-door injuries a year; doors that fail the 2×4 reverse test have killed children.

This skill gives an AI agent (or you) two instruments:

1. **A 90-second safety audit** — the 2×4 contact-reverse test, photo-eye sweep, hand-balance check, manual-release drill, and control-placement rules, with pass/fail logging and crush-hazard escalation when a reverse test fails.
2. **A spring cycle-life forecaster** — springs are wear parts rated in cycles (10k/20k/33k), not years. From install year and daily openings the tool computes cycles used, remaining life %, a dated replace-by window, and REPLACE NOW / THIS SEASON / SCHEDULE / OK verdicts — so you replace both springs on your schedule, not after the 7 PM bang.

## Real problem it solves
- "Is my garage door safe?" is unanswerable without a test protocol nobody remembers. This makes it a 12-point, 90-second, twice-a-year routine with a log.
- "Are my springs about to go?" is invisible until the door slams or jams shut with the car inside. Cycle math makes it a date on the calendar.
- Pre-1993 openers without photo-eyes, drifting down-force settings, keypad codes left at 1234 — the audit names each and tells you what to do tonight.

## Quick start
```bash
python3 scripts/garage_door_audit.py init --installed 2018 --openings 5 --rating 10000
python3 scripts/garage_door_audit.py status
python3 scripts/garage_door_audit.py audit        # 12-point interactive checklist
python3 scripts/garage_door_audit.py log-test --test reverse_2x4 --result pass
```

## Example verdict
```
Cycles used: ~16,145 (8.8 yrs) -> remaining 0%
Verdict: REPLACE SPRINGS NOW — replace BOTH springs (they age together). Torsion = pro only.
Open safety issues: reverse_2x4: FAIL on 2026-11-04 -> crush hazard, fix before tonight's close.
```

## What it deliberately will NOT help with
Torsion-spring adjustment, snapped cables, off-track doors — stored-energy components are pro-only. The skill names them, explains why, and stops.

## Contents
- `SKILL.md` — trigger conditions, 90-second test protocol, spring math, pitfalls, verification checklist
- `references/safety-and-springs.md` — injury data, opener force/limit mechanics, spring economics, US cost bands
- `scripts/garage_door_audit.py` — stdlib-only CLI (init / audit / log-test / status)

## License
MIT
