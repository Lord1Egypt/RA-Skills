#!/usr/bin/env python3
"""
Compute useful timing statistics for an SRT file.
"""

from __future__ import annotations

import argparse
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


TIME_LINE_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$"
)


@dataclass
class SrtEntry:
    index: int
    start: float
    end: float
    text: str


def to_seconds(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt(path: Path) -> List[SrtEntry]:
    raw = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]
    entries: List[SrtEntry] = []

    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue

        try:
            idx = int(lines[0])
        except ValueError:
            continue

        m = TIME_LINE_RE.match(lines[1])
        if not m:
            continue

        start = to_seconds(*m.groups()[:4])
        end = to_seconds(*m.groups()[4:])
        if end < start:
            continue
        text = " ".join(lines[2:]).strip()
        entries.append(SrtEntry(index=idx, start=start, end=end, text=text))

    entries.sort(key=lambda e: (e.start, e.end, e.index))
    return entries


def avg(items: Sequence[float]) -> float:
    return sum(items) / len(items) if items else 0.0


def fmt(v: float) -> str:
    return f"{v:.3f}s"


def print_top(entries: Sequence[tuple[int, float]], title: str, n: int) -> None:
    print(title)
    if not entries:
        print("  (none)")
        return
    for idx, value in entries[:n]:
        print(f"  #{idx}: {value:.3f}s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Show quality stats for an SRT file.")
    parser.add_argument("--srt", required=True, help="Path to .srt file")
    parser.add_argument(
        "--warn-duration",
        type=float,
        default=8.0,
        help="Flag entries longer than this duration in seconds.",
    )
    parser.add_argument(
        "--warn-gap",
        type=float,
        default=0.8,
        help="Flag silent gaps longer than this threshold in seconds.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Show top N longest durations and gaps.",
    )
    args = parser.parse_args()

    srt_path = Path(args.srt).expanduser().resolve()
    if not srt_path.exists():
        raise SystemExit(f"SRT file not found: {srt_path}")

    rows = parse_srt(srt_path)
    if not rows:
        raise SystemExit("No valid SRT entries found.")

    durations = [e.end - e.start for e in rows]
    gaps = [rows[i + 1].start - rows[i].end for i in range(len(rows) - 1)]
    overlaps = [g for g in gaps if g < 0]

    total_span = rows[-1].end - rows[0].start
    subtitle_span = sum(durations)
    coverage = (subtitle_span / total_span * 100.0) if total_span > 0 else 0.0

    print(f"file: {srt_path}")
    print(f"entries: {len(rows)}")
    print(f"timeline start: {rows[0].start:.3f}s")
    print(f"timeline end: {rows[-1].end:.3f}s")
    print(f"timeline span: {fmt(total_span)}")
    print(f"subtitle visible span: {fmt(subtitle_span)} ({coverage:.1f}%)")
    print()
    print(
        "duration: "
        f"min={fmt(min(durations))}, "
        f"max={fmt(max(durations))}, "
        f"avg={fmt(avg(durations))}, "
        f"median={fmt(statistics.median(durations))}"
    )
    if gaps:
        print(
            "gap: "
            f"min={fmt(min(gaps))}, "
            f"max={fmt(max(gaps))}, "
            f"avg={fmt(avg(gaps))}, "
            f"median={fmt(statistics.median(gaps))}"
        )
    else:
        print("gap: (single entry)")
    print()
    long_count = sum(1 for d in durations if d > args.warn_duration)
    long_gap_count = sum(1 for g in gaps if g > args.warn_gap)
    print(f"entries longer than {args.warn_duration:.2f}s: {long_count}")
    print(f"gaps longer than {args.warn_gap:.2f}s: {long_gap_count}")
    print(f"overlaps (negative gaps): {len(overlaps)}")
    print()

    top_durations = sorted(
        ((e.index, e.end - e.start) for e in rows), key=lambda x: x[1], reverse=True
    )
    top_gaps = sorted(
        ((rows[i].index, rows[i + 1].start - rows[i].end) for i in range(len(rows) - 1)),
        key=lambda x: x[1],
        reverse=True,
    )
    print_top(top_durations, "longest entry durations:", args.top)
    print_top(top_gaps, "longest gaps (after entry #):", args.top)


if __name__ == "__main__":
    main()
