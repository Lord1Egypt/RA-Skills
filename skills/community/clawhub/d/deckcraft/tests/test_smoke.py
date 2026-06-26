#!/usr/bin/env python3
"""
DeckCraft v5.2 — Smoke Test

Validates that all 20 layout methods + 5 canvas presets produce PPTX files
that pass the gate_check.py QA gate (zero user errors, zero overflow).

Run:
    python3 tests/test_smoke.py
    python3 tests/test_smoke.py -v    # verbose

Exit codes:
    0 — all pass
    1 — at least one layout/canvas combo failed
"""
import sys, os, subprocess, re, tempfile, json
from pathlib import Path

# Add engine to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import DeckEngine  # noqa: E402
from engine.constants import list_canvases  # noqa: E402


# 20 layout methods (all of DeckEngine's public page builders)
ALL_LAYOUTS = [
    ("cover",             lambda e: e.cover(title="Test Cover", subtitle="Sub", author="T", date="D")),
    ("toc",               lambda e: e.toc(items=[("01", "A", "B"), ("02", "C", "D")])),
    ("section_divider",   lambda e: e.section_divider("Section", section_number=1, subtitle="Sub")),
    ("content",           lambda e: e.content(title="C", bullets=["a", "b", "c"], key_point="k")),
    ("content_with_icon", lambda e: e.content_with_icon(title="C", items=[("01", "H", "D")])),
    ("two_col",           lambda e: e.two_col(title="D", left_title="L", left_items=["a", "b"],
                                              right_title="R", right_items=["c", "d"])),
    ("vs_compare",        lambda e: e.vs_compare(title="V", left_title="A", right_title="B",
                                                 rows=[("D", "1", "2"), ("E", "3", "4")])),
    ("table",             lambda e: e.table(title="T", headers=["H1", "H2", "H3"],
                                            rows=[["a", "b", "c"], ["d", "e", "f"]],
                                            insights=["key insight"])),
    ("stat_cards",        lambda e: e.stat_cards(title="K", stats=[("99%", "U"), ("$2M", "R")])),
    ("chart_bar",         lambda e: e.chart_bar(title="C", data=[[1, 2, 3]], labels=["A", "B", "C"])),
    ("chart_pie",         lambda e: e.chart_pie(title="P", data=[1, 2, 3], labels=["X", "Y", "Z"])),
    ("chart_line",        lambda e: e.chart_line(title="L", data=[[1, 2, 3]], labels=["Q1", "Q2", "Q3"])),
    ("chart_gauge",       lambda e: e.chart_gauge(title="G", value=87, max_value=100, label="NPS")),
    ("timeline",          lambda e: e.timeline(title="T", milestones=[("Q1", "X"), ("Q2", "Y"), ("Q3", "Z")])),
    ("process_flow",      lambda e: e.process_flow(title="F", steps=["A", "B", "C"])),
    ("matrix_2x2",        lambda e: e.matrix_2x2(title="M", quadrants=[("TL", "x"), ("TR", "x"),
                                                                       ("BL", "x"), ("BR", "x")])),
    ("quote",             lambda e: e.quote(title="Q", quote_text="Words matter.", attribution="Author")),
    ("summary",           lambda e: e.summary(title="S", key_points=["a", "b"], conclusion="next")),
    ("closing",           lambda e: e.closing(title="Thank You", message="Q?", contact="x@y.com")),
]

# All canvas presets to test
ALL_CANVASES = ["16:9", "9:16", "1:1", "4:3", "A4"]


def run_smoke(verbose: bool = False) -> int:
    """Run all canvas × layout combinations. Returns exit code (0=pass, 1=fail)."""
    results = {"passed": 0, "failed": 0, "errors": []}
    tmpdir = tempfile.mkdtemp(prefix="deckcraft_test_")

    total = len(ALL_CANVASES) * len(ALL_LAYOUTS)
    print(f"Running {len(ALL_CANVASES)} canvases × {len(ALL_LAYOUTS)} layouts = {total} tests")
    print("=" * 70)

    for canvas in ALL_CANVASES:
        for layout_name, builder in ALL_LAYOUTS:
            try:
                # Build deck
                eng = DeckEngine(theme_name="business", canvas=canvas)
                builder(eng)
                out_path = os.path.join(tmpdir, f"{canvas.replace(':', 'x')}_{layout_name}.pptx")
                eng.save(out_path)

                # Verify slide count
                if eng.slide_count != 1:
                    raise AssertionError(f"Expected 1 slide, got {eng.slide_count}")

                # Run gate check
                result = subprocess.run(
                    ["python3", str(ROOT / "scripts" / "gate_check.py"), out_path, tmpdir],
                    capture_output=True, text=True, timeout=30,
                )
                if "GATE PASSED" not in result.stdout:
                    score_m = re.search(r'"overall_score":\s*(\d+)', result.stdout)
                    err_m = re.search(r'"user_code_errors":\s*(\d+)', result.stdout)
                    raise AssertionError(
                        f"gate failed: score={score_m.group(1) if score_m else '?'}, "
                        f"errors={err_m.group(1) if err_m else '?'}"
                    )

                results["passed"] += 1
                if verbose:
                    print(f"  ✓ {canvas:8s} × {layout_name:20s}")

            except Exception as e:
                results["failed"] += 1
                results["errors"].append((canvas, layout_name, str(e)))
                print(f"  ✗ {canvas:8s} × {layout_name:20s}: {e}")

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)

    print("=" * 70)
    print(f"Passed: {results['passed']} / {total}")
    if results["failed"] > 0:
        print(f"Failed: {results['failed']}")
        print()
        print("Failures:")
        for canvas, layout_name, err in results["errors"]:
            print(f"  - {canvas} × {layout_name}: {err}")
        return 1
    print()
    print("✓ All smoke tests passed.")
    return 0


if __name__ == "__main__":
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    sys.exit(run_smoke(verbose=verbose))
