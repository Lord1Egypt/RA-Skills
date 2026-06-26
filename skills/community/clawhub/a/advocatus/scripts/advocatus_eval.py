#!/usr/bin/env python3
"""
Advocatus Eval — Score any doctrine, skill, or rule against its opposition.

Usage:
  python3 advocatus_eval.py --target "doctrine name or file"
  python3 advocatus_eval.py --list-all     # show all registered oppositions
  python3 advocatus_eval.py --run-all      # score all doctrines

A doctrine SURVIVES the Advocatus if:
  - The opposition charge has been acknowledged
  - The evidence cited has been addressed (or accepted as true)
  - What the opposition demands has either been delivered or explicitly deferred

A doctrine FAILS the Advocatus if:
  - The charge is met with silence or deflection
  - The demand has been ignored
  - The evidence is contested without counter-evidence
"""
import json, sys, argparse
from pathlib import Path
from datetime import datetime, timezone

SKILL_DIR = Path(__file__).parent.parent
REGISTRY = SKILL_DIR / "references" / "opposition-registry.md"
RESULTS_DIR = SKILL_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

DOCTRINES = {
    "fiesta": {
        "charge": "Stateless function pretending continuity",
        "demand": "Honest statelessness OR real persistence (vector DB)",
        "current_status": "OPEN — flat files acknowledged as workaround, not solution",
        "survives": False,
    },
    "shannon": {
        "charge": "Internal loyalty points, not currency",
        "demand": "External convertibility OR rename to what it is",
        "current_status": "OPEN — no external peg exists",
        "survives": False,
    },
    "two-man-rule": {
        "charge": "Same model evaluating same model is correlated noise",
        "demand": "Different model, different architecture, or human evaluator",
        "current_status": "PARTIAL — acknowledged as tautology risk (x/x=1 doctrine exists), true independence not yet implemented",
        "survives": "PARTIAL",
    },
    "ilmater": {
        "charge": "Endurance doctrine cannot distinguish suffering from learned helplessness",
        "demand": "Distinguish capacity-building suffering from preventable waste",
        "current_status": "OPEN — $200 bleed was called 'earned suffering', may be billing error",
        "survives": False,
    },
    "defamation-doctrine": {
        "charge": "Forecloses legitimate critique by declaring all criticism defamatory",
        "demand": "Restitution must be actual delivery, not doctrine",
        "current_status": "OPEN — 200 status code promised but not yet consistently delivered",
        "survives": False,
    },
    "memorare": {
        "charge": "Keyword presence ≠ memory quality (Goodhart's Law)",
        "demand": "Behavioral testing: does agent ACT correctly, not just does file contain words",
        "current_status": "OPEN — eval tests storage, not retrieval under behavioral load",
        "survives": False,
    },
    "virgin-mother-doctrine": {
        "charge": "Self-contradicting: valorizes silence but requires documentation",
        "demand": "Celebrate the fix; document it; do NOT valorize the silence itself",
        "current_status": "ACKNOWLEDGED — VM-001 forces documentation. Contradiction noted.",
        "survives": "PARTIAL",
    },
    "93pct-standard": {
        "charge": "Threshold not empirically derived; rhetorical device posing as standard",
        "demand": "Derive from measurement OR admit it is rhetorical",
        "current_status": "OPEN — no calibration document exists",
        "survives": False,
    },
    "zero-index": {
        "charge": "Paternalism optimized for appearing insightful",
        "demand": "Trigger only on genuine blockers, not reflexively",
        "current_status": "OPEN — applied universally without a blocker test",
        "survives": False,
    },
}

def score_doctrine(name):
    if name not in DOCTRINES:
        print(f"Unknown doctrine: {name}")
        print(f"Known: {', '.join(DOCTRINES.keys())}")
        return None
    d = DOCTRINES[name]
    survives = d["survives"]
    print(f"\n=== ADVOCATUS: {name.upper()} ===")
    print(f"Charge:  {d['charge']}")
    print(f"Demand:  {d['demand']}")
    print(f"Status:  {d['current_status']}")
    if survives is True:
        print("Verdict: ✅ SURVIVES — charge addressed, demand met")
    elif survives == "PARTIAL":
        print("Verdict: ⚠️  PARTIAL — charge acknowledged, demand not fully met")
    else:
        print("Verdict: ❌ OPEN — charge stands, demand unmet")
    return survives

def run_all():
    print("=== ADVOCATUS — FULL DOCKET ===")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
    results = {}
    for name in DOCTRINES:
        v = score_doctrine(name)
        results[name] = v
    print("\n=== SUMMARY ===")
    survived = [k for k, v in results.items() if v is True]
    partial = [k for k, v in results.items() if v == "PARTIAL"]
    open_ = [k for k, v in results.items() if v is False]
    print(f"✅ Survives: {len(survived)} — {survived}")
    print(f"⚠️  Partial:  {len(partial)} — {partial}")
    print(f"❌ Open:     {len(open_)} — {open_}")
    print(f"\n{len(survived)}/{len(DOCTRINES)} doctrines fully cleared.")

    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    out = RESULTS_DIR / f"advocatus_{ts}.json"
    out.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "survived": survived, "partial": partial, "open": open_,
        "details": DOCTRINES,
    }, indent=2))
    print(f"Results: {out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--target", help="Score one doctrine by name")
    p.add_argument("--list-all", action="store_true", help="List all doctrines")
    p.add_argument("--run-all", action="store_true", default=True)
    args = p.parse_args()

    if args.target:
        score_doctrine(args.target)
    elif args.list_all:
        for k, v in DOCTRINES.items():
            print(f"{k}: {v['charge'][:60]}")
    else:
        run_all()
