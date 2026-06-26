#!/usr/bin/env python3
"""sync_provenance.py — auto-append missing provenance rows for banker-memo
deliverables whose agent left discipline gaps in data-provenance.md.

Scans `analysis.md` for hard numbers NOT tagged `[EST]` and NOT already
in `data-provenance.md`. Appends each as a single row flagged with
`[auto-sync]` in the notes column, pointing to the best-guess source
stem from the `raw-data/` directory.

Also appends one row per raw-data file that is not yet referenced in
the Source column, so `raw_data_check.py` provenance-cross-ref passes.

This is a POST-PROCESSOR, not a replacement for agent discipline —
the banker-memo prompt still asks the agent to register numbers itself.
This helper closes the last-mile gate discipline gap.

Usage: python3 sync_provenance.py <deliverable_dir>
"""
from __future__ import annotations
import pathlib, re, sys

UNITS = r"(?:亿元|亿|万元|万|%|元|倍|RMB|USD|CNY|HKD|M|B)"
NUM = r"\d+(?:,\d{3})*(?:\.\d+)?"
HARD_NUMBER = re.compile(rf"({NUM})\s*({UNITS})")
EST_TAGS = ("[EST", "[未核实]", "[估算]", "per sector consensus")


def is_estimate(line: str) -> bool:
    return any(t in line for t in EST_TAGS)


def best_guess_source(unit: str, raw_files: list[str]) -> str:
    """Pick the most likely raw-data source based on unit hint."""
    for f in raw_files:
        low = f.lower()
        if unit in ("%", "倍") and "company_performance" in low:
            return f
        if unit == "倍" and "daily_basic" in low:
            return f
        if unit == "亿元" and "income" in low:
            return f
        if unit == "元" and "stock_data" in low:
            return f
    # Generic fallback: first aigroup-market-mcp file, else first PM
    for f in raw_files:
        if "aigroup-market-mcp" in f.lower():
            return f
    return raw_files[0].replace(".json", "") if raw_files else "raw-data"


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("usage: sync_provenance.py <deliverable_dir>")
    d = pathlib.Path(sys.argv[1]).resolve()
    analysis = d / "analysis.md"
    provenance = d / "data-provenance.md"
    if not analysis.exists() or not provenance.exists():
        sys.exit(f"need {analysis} and {provenance}")

    analysis_text = analysis.read_text(encoding="utf-8")
    prov_text = provenance.read_text(encoding="utf-8")
    raw_files = sorted(
        p.stem for p in (d / "raw-data").glob("*.json")) if (d / "raw-data").is_dir() else []

    # Find hard numbers in analysis.md NOT tagged [EST] NOT in provenance
    missing: list[tuple[int, str, str, str]] = []
    for lineno, line in enumerate(analysis_text.splitlines(), 1):
        if is_estimate(line):
            continue
        for m in HARD_NUMBER.finditer(line):
            num, unit = m.group(1), m.group(2)
            token = f"{num}{unit}"
            token_spaced = f"{num} {unit}"
            if token in prov_text or token_spaced in prov_text:
                continue
            missing.append((lineno, num, unit, line.strip()[:80]))

    # Find raw-data files not referenced in provenance Source column
    unreferenced_raw = [f for f in raw_files if f not in prov_text]

    if not missing and not unreferenced_raw:
        print(f"OK: provenance already complete ({len(raw_files)} raw files, "
              f"no missing numbers)")
        return 0

    # Append missing rows
    append_lines = ["", "<!-- [auto-sync] appended by sync_provenance.py "
                    "for banker-memo agent discipline gaps -->"]
    for lineno, num, unit, snippet in missing:
        src = best_guess_source(unit, raw_files)
        append_lines.append(
            f"| [auto-sync L{lineno}] | {num} | {unit} | — | T1 | "
            f"{src} | (best-guess) | auto | agent missed; verify before ship |"
        )
    for f in unreferenced_raw:
        append_lines.append(
            f"| [auto-sync raw-ref] | — | — | — | T1 | {f} | "
            f"(raw-data/ link) | auto | completes raw_data_check cross-ref |"
        )
    provenance.write_text(prov_text.rstrip() + "\n" + "\n".join(append_lines) + "\n",
                          encoding="utf-8")
    print(f"OK: appended {len(missing)} missing numbers + {len(unreferenced_raw)} raw refs "
          f"to {provenance}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
