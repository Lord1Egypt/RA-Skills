#!/usr/bin/env bash
# Construction Law Skill — Tutorial Demo Runner
# Run from the skill root: bash demo/run-demos.sh
# Each section pauses so you can hit Enter when ready (good for live recording).

set -e
clear

pause() { read -rp "  ── press Enter for next demo ── " _; clear; }

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  CONSTRUCTION LAW SKILL — TUTORIAL DEMO RUNNER              ║"
echo "║  v2.5.0 · MIT-0 · Offline                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo
echo "  Three demos coming up:"
echo "    1) Matter Intake     — kills the repetition"
echo "    2) FIDIC Comparator  — kills the clause hunt"
echo "    3) SOP Calculator    — kills the timeline-memorising"
echo
pause

# ─── DEMO 1: Matter Intake (FIDIC Red 1999, late site access, SG) ───
echo "▶ DEMO 1 — Matter Intake"
echo "  Scenario: FIDIC Red 1999 · Singapore · Contractor · Late site access · EOT + money"
echo
python3 scripts/intake.py --file demo/matter.json
pause

# ─── DEMO 2: FIDIC Comparator (Red vs Yellow vs Silver, risk topic) ───
echo "▶ DEMO 2 — FIDIC Comparator (Risk allocation: Red vs Yellow vs Silver)"
echo
python3 scripts/construction_law.py compare --forms red,yellow,silver --topic risk
echo
echo "  Now exporting Red vs Silver claims comparison to CSV..."
python3 scripts/construction_law.py compare --forms red,silver --topic claims --format csv --output comparison.csv
echo "  ✓ Saved: comparison.csv"
pause

# ─── DEMO 3: Singapore SOP Act payment timeline ───
echo "▶ DEMO 3 — SOP Act Calculator (Payment Claim served 30 Jun 2026)"
echo
python3 scripts/sop_calculator.py --claim-date 2026-06-30
echo
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Demo complete.                                              ║"
echo "║  Install: openclaw skills install construction-law           ║"
echo "║  Listing: clawhub.ai/redkiwi1688-prog/construction-law       ║"
echo "╚════════════════════════════════════════════════════════════╝"
