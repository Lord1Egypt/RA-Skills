#!/usr/bin/env python3
"""
extract_deck_numbers.py — project every cited hard number out of
`analysis.md` + `data-provenance.md` into a single `deck-numbers.json`
lookup that slide/docx generators can import instead of re-typing numbers.

Goal: close the number-flow loop. Today the chain is:
    raw-data/*.json  →  data-provenance.md  →  analysis.md  →  slides/*.js / memo.docx
Each hop is a chance for the agent to re-type the number slightly wrong
(or, in MiniMax-host cases, to hallucinate a new value). `slide_data_audit`
catches PPT drift, but only post-hoc. This helper lets generators pull
the canonical number+unit directly from a machine-readable export.

Output schema (`deck-numbers.json`):

    {
      "generated_at": "2026-04-20T12:00:00Z",
      "deliverable": "<absolute path>",
      "metrics": [
        {
          "metric":   "2024 营收",
          "value":    "7,771",
          "unit":     "亿元",
          "raw":      "7,771亿元",
          "source":   "公司年报2024",
          "provenance_line": 12
        },
        ...
      ]
    }

Usage:
    python3 extract_deck_numbers.py <deliverable_dir>
    # writes <deliverable_dir>/deck-numbers.json; exits 0 on non-empty

This is a PRODUCER script. It does not enforce anything by itself —
slide_data_audit / docx_data_audit remain the enforcement gates. The value
here is giving slides/*.js and memo.docx code a stable import path.
"""
from __future__ import annotations
import argparse
import datetime
import json
import pathlib
import re
import sys

UNITS = r"(?:亿元|亿|万元|万|%|元|倍|RMB|USD|CNY|HKD|M|B)"
NUM_CORE = r"\d+(?:,\d{3})*(?:\.\d+)?"
HARD_NUMBER = re.compile(rf"({NUM_CORE})\s*({UNITS})")

SOURCE_HEADER_PATTERN = re.compile(r"(?i)(source|来源|源|数据来源)")
METRIC_HEADER_PATTERN = re.compile(r"(?i)(指标|metric|item|数字|data)")


def parse_tables(text: str):
    lines = text.splitlines()
    tables = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines):
            sep = lines[i + 1].lstrip()
            if re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", sep):
                headers = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    row = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    rows.append((j + 1, row))  # 1-based line number
                    j += 1
                tables.append((i + 1, headers, rows))
                i = j
                continue
        i += 1
    return tables


BULLET_ARROW = re.compile(
    r"^\s*[-*]\s+(?P<pre>.*?)\s*(?:→|->|—|⇒|←|<-|←—|—>)\s*(?P<src>.+)$"
)


def extract_from_provenance(prov_text: str):
    """Extract numbers from provenance.md.

    Handles three provenance formats seen in real banker deliverables:
    1. Markdown table with a Source column (BYD / Midea style).
    2. Markdown table with just a metric + inline cited number (rare).
    3. Bulleted list `- <number><unit> → <source>` (CATL style, inherited
       from the Phase 4 slide-outline generator that writes provenance as
       slide-grouped bullets).

    The three paths are merged into one list; each entry is tagged with
    the best-guess metric label (column header row, or preceding H3 when
    parsing bullets).
    """
    metrics = []
    consumed_lines: set[int] = set()

    # --- Path 1/2: markdown tables ---
    for table_start, headers, rows in parse_tables(prov_text):
        metric_idx = next(
            (i for i, h in enumerate(headers) if METRIC_HEADER_PATTERN.search(h)),
            None,
        )
        source_idx = next(
            (i for i, h in enumerate(headers) if SOURCE_HEADER_PATTERN.search(h)),
            None,
        )
        if source_idx is None:
            # Skip untagged tables (e.g. a generic "financial summary" without source col)
            continue
        for line_no, row in rows:
            consumed_lines.add(line_no)
            if source_idx >= len(row):
                continue
            metric_label = (
                row[metric_idx] if metric_idx is not None and metric_idx < len(row)
                else row[0] if row else ""
            )
            source_cell = row[source_idx]
            # Scan per-cell first (handles "15.20%" combined). Then, to catch
            # "value + unit in separate columns" style (common in banker tables:
            # | 指标 | 数值 | 单位 | …), join the whole row with spaces and scan
            # the resulting string — HARD_NUMBER will match "15.20 %" pattern.
            seen_raw: set[str] = set()
            for cell in row:
                for m in HARD_NUMBER.finditer(cell):
                    num, unit = m.group(1), m.group(2)
                    raw = f"{num}{unit}"
                    seen_raw.add(raw)
                    metrics.append({
                        "metric": metric_label, "value": num, "unit": unit,
                        "raw": raw, "source": source_cell,
                        "provenance_line": line_no,
                    })
            joined = " ".join(row)
            for m in HARD_NUMBER.finditer(joined):
                num, unit = m.group(1), m.group(2)
                raw = f"{num}{unit}"
                if raw in seen_raw:
                    continue
                seen_raw.add(raw)
                metrics.append({
                    "metric": metric_label, "value": num, "unit": unit,
                    "raw": raw, "source": source_cell,
                    "provenance_line": line_no,
                })

    # --- Path 3: bullet-list with arrow separator ---
    current_heading = ""
    for i, raw_line in enumerate(prov_text.splitlines(), 1):
        if i in consumed_lines:
            continue
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            current_heading = stripped.lstrip("#").strip()
            continue
        m = BULLET_ARROW.match(raw_line)
        if not m:
            continue
        pre = m.group("pre")
        src = m.group("src").strip()
        for hn in HARD_NUMBER.finditer(pre):
            num, unit = hn.group(1), hn.group(2)
            metrics.append({
                "metric": current_heading or pre[:40],
                "value": num,
                "unit": unit,
                "raw": f"{num}{unit}",
                "source": src,
                "provenance_line": i,
            })

    return metrics


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("deliverable_dir", type=pathlib.Path)
    args = ap.parse_args(argv[1:])

    d = args.deliverable_dir.resolve()
    if not d.is_dir():
        print(f"ERR: {d} is not a directory", file=sys.stderr)
        return 2

    provenance = d / "data-provenance.md"
    if not provenance.exists():
        print(f"ERR: {provenance} missing", file=sys.stderr)
        return 2

    prov_text = provenance.read_text(encoding="utf-8", errors="replace")
    metrics = extract_from_provenance(prov_text)

    out = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "deliverable": str(d),
        "metric_count": len(metrics),
        "metrics": metrics,
    }
    out_path = d / "deck-numbers.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: wrote {out_path} with {len(metrics)} metric rows")
    return 0 if metrics else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
