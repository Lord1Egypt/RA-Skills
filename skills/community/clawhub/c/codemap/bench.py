"""Reproducible benchmark: codemap lookup vs the grep-then-read baseline.

When an agent needs "where is X / what's its signature", the common workflow is:
  1. grep the tree for the name, then
  2. read the file that defines it (often the whole file) to see the signature
     and surrounding context.

codemap collapses that to a single compact record: file:line + the signature.
This measures the character (hence estimated-token) cost of each, over a real
sample of symbols drawn from our own indexed repos.

Run:  python3 bench.py   (build the index first: codemap build <roots>)
"""
import os
import random
import subprocess

from codemap import index

ROOTS = ["/home/workloft/conexus", "/home/workloft/workloft-site", "/home/workloft/bob-app"]
DB = index.DEFAULT_DB
SAMPLE = 40
SEED = 7

INCLUDES = ["--include=*.py", "--include=*.ts", "--include=*.tsx",
            "--include=*.js", "--include=*.jsx"]


def grep_chars(name: str) -> int:
    """Cost of locating the symbol with grep across the trees (node_modules
    excluded, mirroring the agent grep tool)."""
    cmd = ["grep", "-rn"] + INCLUDES + [
        "--exclude-dir=node_modules", "--exclude-dir=.next",
        "--exclude-dir=.git", "--exclude-dir=dist",
        name,
    ] + ROOTS
    p = subprocess.run(cmd, capture_output=True, text=True)
    return len(p.stdout)


def read_file_chars(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return len(fh.read())
    except OSError:
        return 0


def read_window_chars(path: str, line: int, radius: int = 40) -> int:
    """Cost of reading a +/- radius line window around the definition - what a
    careful agent reads rather than the whole file."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return 0
    lo = max(0, line - 1 - radius)
    hi = min(len(lines), line - 1 + radius)
    return sum(len(s) for s in lines[lo:hi])


def codemap_chars(name: str) -> int:
    """Cost of the compact codemap answer for the same query."""
    hits = index.find(name, db_path=DB, exact=True)
    return sum(len(h.compact()) + 1 for h in hits)


def main():
    s = index.stats(db_path=DB)
    if s["symbols"] == 0:
        print("Index empty. Run: codemap build " + " ".join(ROOTS))
        return

    # sample distinct symbol names that resolve to a single definition
    import sqlite3
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT name, file FROM symbols GROUP BY name HAVING COUNT(*)=1"
    ).fetchall()
    conn.close()
    random.seed(SEED)
    sample = random.sample(rows, min(SAMPLE, len(rows)))

    full_total = 0      # grep + read whole file (upper bound)
    window_total = 0     # grep + read +/-40 line window (conservative)
    cm_total = 0
    for name, file in sample:
        g = grep_chars(name)
        line = index.find(name, db_path=DB, exact=True)[0].line
        full_total += g + read_file_chars(file)
        window_total += g + read_window_chars(file, line)
        cm_total += codemap_chars(name)

    def pct(base):
        return 100 * (base - cm_total) / base

    print("=== codemap benchmark ===\n")
    print(f"index: {s['symbols']} symbols across {s['files']} files")
    print(f"sample: {len(sample)} unique-definition symbols (seed {SEED})\n")
    print(f"codemap (compact record)              : {cm_total:,} chars  "
          f"(~{cm_total // 4:,} est. tokens)")
    print(f"baseline A grep + read whole file     : {full_total:,} chars  "
          f"(~{full_total // 4:,} est. tokens)  -> {pct(full_total):.1f}% cut")
    print(f"baseline B grep + read +/-40 line window: {window_total:,} chars  "
          f"(~{window_total // 4:,} est. tokens)  -> {pct(window_total):.1f}% cut")
    print(f"\nmean per lookup: codemap {cm_total//len(sample):,} chars  vs "
          f"windowed baseline {window_total//len(sample):,} chars")
    print("\n(token figures are estimates, chars/4. node_modules excluded from grep.)")


if __name__ == "__main__":
    main()
