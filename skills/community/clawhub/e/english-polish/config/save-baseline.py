#!/usr/bin/env python3
"""
Save or compare baseline scores.

Usage:
    python3 config/save-baseline.py          # Compare only
    python3 config/save-baseline.py --save   # Save as reference
"""
import json, sys, os
from pathlib import Path

REPORT = Path(__file__).parent.parent / "detector-report.json"
REF = Path(__file__).parent / "baseline-reference.json"

if not REPORT.exists():
    print("❌ No detector-report.json found. Run 'make baseline' first.")
    sys.exit(1)

results = json.loads(REPORT.read_text())
scores = [r["nativization_score"] for r in results if "nativization_score" in r]
avg = sum(scores) / len(scores) if scores else 0

if "--save" in sys.argv:
    ref = {
        "average_score": round(avg, 3),
        "file_count": len(scores),
        "detector_version": "19-class (A-S)",
    }
    REF.write_text(json.dumps(ref, indent=2) + "\n")
    print(f"✅ Saved reference baseline: {avg:.3f}/5 ({len(scores)} files)")
    sys.exit(0)

# Compare mode
if REF.exists():
    ref = json.loads(REF.read_text())
    ref_avg = ref.get("average_score", 0)
    diff = avg - ref_avg
    symbol = "" if abs(diff) < 0.1 else ("⬆️" if diff > 0 else "⬇️")
    print(f"\nCurrent:  {avg:.3f}/5 ({len(scores)} files)")
    print(f"Reference: {ref_avg:.3f}/5 ({ref.get('file_count', '?')} files)")
    print(f"Diff:     {diff:+.4f}  {symbol}")
    if diff < -0.1:
        print("⚠️  Score dropped >0.1 — review recent changes")
    elif diff > 0.1:
        print("✅ Score improved >0.1 — new patterns working")
    else:
        print("✅ No significant change (within ±0.1)")
else:
    print(f"Current baseline: {avg:.3f}/5 ({len(scores)} files)")
    print("No saved reference. Run 'make save-baseline' to create one.")
