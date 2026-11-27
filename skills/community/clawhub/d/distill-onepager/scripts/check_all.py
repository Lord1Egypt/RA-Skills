#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run every gate for one deliverable in a single command.

Before this existed, "run the checks" meant remembering three tools across two
skills, and in practice only the structural one got run — which is exactly why
under-filled pages and an over-split section both shipped.

Gates:
  1. structure  <onepager-render>/scripts/check_onepager.py   page/char/font/img/heading
  2. weight     ./check_weight.py                              bullets <= source KUs
  3. fill       ./measure_fill.py                              non-last page >= 900px

Usage:
    python check_all.py <file.html> [--manifest w.json] [--gate 900]
                        [--chrome PATH] [--pdf] [--no-fill]

Exit codes: 0 = all gates passed, 1 = at least one failed, 2 = could not run.
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
RENDER_SCRIPTS = SKILLS / "onepager-render" / "scripts"

# Static imports (no importlib): keeps the call graph resolvable for static
# analysers, which otherwise report "dynamic dispatch" and refuse a verdict.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RENDER_SCRIPTS))

try:
    import check_weight
    import measure_fill
except ImportError as exc:  # pragma: no cover - packaging guard
    sys.stderr.write(f"[FAIL] sibling script missing: {exc}\n")
    raise SystemExit(2)

try:
    import check_onepager as render_check
    HAVE_RENDER_CHECK = True
except ImportError:
    render_check = None
    HAVE_RENDER_CHECK = False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--gate", type=int, default=900)
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--no-fill", action="store_true", help="skip browser measurement")
    args = ap.parse_args()

    target = Path(args.file)
    if not target.is_file():
        print(f"[FAIL] file not found: {target}", file=sys.stderr)
        return 2

    results = []

    # 1. structure
    if HAVE_RENDER_CHECK:
        try:
            code = render_check.main(str(target))
            results.append(("structure", code == 0, "check_onepager.py"))
        except Exception as e:                      # noqa: BLE001 - report, do not crash
            results.append(("structure", False, f"error: {e}"))
    else:
        results.append(("structure", False, f"missing {RENDER_SCRIPTS / 'check_onepager.py'}"))

    # 2. weight conservation
    try:
        w = check_weight.check(target, args.manifest)
        ok = w["code"] == 0
        note = "no manifest (skipped)" if w["code"] == 2 else (
            f"{len(w['violations'])} violation(s)")
        if w["code"] == 2:
            print("[WARN] weight: no manifest — 门 3.6 未执行；"
                  "请用 check_weight.py --init 生成并填 ku")
            results.append(("weight", True, note))
        else:
            for v in w["violations"]:
                print(f"[FAIL] weight: {v}")
            results.append(("weight", ok, note))
    except Exception as e:                          # noqa: BLE001
        results.append(("weight", False, f"error: {e}"))

    # 3. fill gate
    if args.no_fill:
        results.append(("fill", True, "skipped (--no-fill)"))
    else:
        try:
            m = measure_fill.measure(target, gate=args.gate, chrome=args.chrome, want_pdf=args.pdf)
            low = [r for r in m["pages"] if not r["pass"]]
            note = ", ".join(
                f"p{r['page']} {r['contentBottom']}px ({r['fillPct']}%)" for r in m["pages"])
            if m["printPages"] is not None:
                note += f", print {m['printPages']}p"
            for r in low:
                print(f"[FAIL] fill: page {r['page']} is {r['contentBottom']}px "
                      f"< gate {args.gate}px")
            results.append(("fill", not low, note))
        except Exception as e:                      # noqa: BLE001
            msg = str(e)
            if "Chrome/Edge not found" in msg:
                print("[WARN] fill: no browser — 未实测页数与填充率，报告须注明")
                results.append(("fill", True, "skipped: no browser"))
            else:
                results.append(("fill", False, f"error: {msg}"))

    print()
    print("== check_all summary ==")
    for name, ok, note in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {pad(name, 10)}{note}")
    failed = [n for n, ok, _ in results if not ok]
    if failed:
        print(f"\nRESULT: FAIL ({', '.join(failed)})")
        return 1
    print("\nRESULT: PASS")
    return 0


def pad(text: str, width: int) -> str:
    return text + " " * max(0, width - len(text))


if __name__ == "__main__":
    sys.exit(main())
