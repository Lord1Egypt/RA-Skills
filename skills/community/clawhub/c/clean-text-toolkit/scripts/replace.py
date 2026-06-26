#!/usr/bin/env python3
"""
replace.py - Find-and-replace inside a text file. Like `sed`, but with
multi-pattern support, regex with capture-group back-references, a real
dry-run preview, and a clear count of how many replacements happened.

Usage:
    replace.py INPUT OUTPUT --find PATTERN --replace REPLACEMENT [options]
    replace.py INPUT OUTPUT --rules RULES.json [options]

Two ways to specify replacements:

    --find P --replace R    one rule on the command line. Repeat the pair
                            multiple times to apply multiple rules in order:
                              --find 'foo' --replace 'bar' \\
                              --find 'baz' --replace 'qux'

    --rules RULES.json      a JSON file containing a list of {"find": ...,
                            "replace": ...} objects. Replaces are applied in
                            the order they appear. Each object may also set
                            "regex": true / false to override the default.

Options:
    --regex                 treat all --find patterns as regex (default: literal).
                            Capture groups like \\1, \\2, ... work in --replace.
    --ignore-case           regex / literal compare is case-insensitive.
    --word                  add \\b word boundaries around literal patterns
                            (only meaningful when --regex is OFF).
    --max N                 stop after the first N replacements per rule.
    --dry-run               do NOT write OUTPUT; print the matches that
                            WOULD be replaced, one per line, with line+col
                            and a small context.
    --count                 just print the total count of replacements
                            per rule, then exit (still writes OUTPUT
                            unless --dry-run is also set).
    --json                  emit a machine-readable summary on stderr.
    --quiet                 suppress the text summary.
    -h, --help              show this help.

Exit codes:
    0   at least one replacement was made (or --dry-run found at least one match)
    1   zero replacements
    2   bad arguments / unsafe path / missing file / bad regex / bad rules file
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

from _common import read_text, safe_path, write_text


def parse_rules(rules_path: Path) -> List[dict]:
    try:
        obj = json.loads(rules_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"--rules JSON parse error: {e}")
    if not isinstance(obj, list):
        raise ValueError("--rules file must contain a top-level JSON array")
    out: List[dict] = []
    for i, r in enumerate(obj):
        if not isinstance(r, dict):
            raise ValueError(f"--rules[{i}] must be an object")
        if "find" not in r:
            raise ValueError(f"--rules[{i}] missing required 'find' field")
        out.append({
            "find": str(r["find"]),
            "replace": str(r.get("replace", "")),
            "regex": bool(r.get("regex", False)),
            "ignore_case": bool(r.get("ignore_case", False)),
            "word": bool(r.get("word", False)),
        })
    return out


def compile_pattern(find: str, regex: bool, ignore_case: bool,
                    word: bool) -> re.Pattern:
    flags = re.IGNORECASE if ignore_case else 0
    if regex:
        return re.compile(find, flags)
    pat = re.escape(find)
    if word:
        pat = r"\b" + pat + r"\b"
    return re.compile(pat, flags)


def find_matches_with_context(text: str, pat: re.Pattern,
                              max_n: int) -> List[Tuple[int, int, str, str]]:
    """Return up to max_n (line, col, matched_text, line_text) tuples."""
    out: List[Tuple[int, int, str, str]] = []
    # Build a line-start index for fast line/col lookups
    lines = text.splitlines(keepends=True)
    line_starts: List[int] = []
    pos = 0
    for line in lines:
        line_starts.append(pos)
        pos += len(line)
    for m in pat.finditer(text):
        if max_n and len(out) >= max_n:
            break
        start = m.start()
        # Binary search for the line containing `start`
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= start:
                lo = mid
            else:
                hi = mid - 1
        line_no = lo + 1
        col = start - line_starts[lo] + 1
        line_text = lines[lo].rstrip("\n").rstrip("\r")
        out.append((line_no, col, m.group(0), line_text))
    return out


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--find", action="append", default=[])
    p.add_argument("--replace", action="append", default=[])
    p.add_argument("--rules")
    p.add_argument("--regex", action="store_true")
    p.add_argument("--ignore-case", dest="ignore_case", action="store_true")
    p.add_argument("--word", action="store_true")
    p.add_argument("--max", type=int, default=0)
    p.add_argument("--dry-run", dest="dry_run", action="store_true")
    p.add_argument("--count", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    if not args.find and not args.rules:
        print("Error: provide --find/--replace pairs or --rules FILE",
              file=sys.stderr)
        return 2
    if args.find and args.rules:
        print("Error: --find and --rules are mutually exclusive", file=sys.stderr)
        return 2
    if args.find and len(args.find) != len(args.replace):
        # If user gave fewer --replace than --find, pad with "" (delete behavior)
        while len(args.replace) < len(args.find):
            args.replace.append("")
        if len(args.replace) > len(args.find):
            print("Error: more --replace than --find arguments", file=sys.stderr)
            return 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    # Build rule list
    rules: List[dict] = []
    if args.rules:
        try:
            rules_path = safe_path(args.rules)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if not rules_path.is_file():
            print(f"Error: rules file not found: {rules_path}", file=sys.stderr)
            return 2
        try:
            rules = parse_rules(rules_path)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
    else:
        for f, r in zip(args.find, args.replace):
            rules.append({
                "find": f, "replace": r, "regex": args.regex,
                "ignore_case": args.ignore_case, "word": args.word,
            })

    # Compile patterns
    compiled: List[Tuple[re.Pattern, str, dict]] = []
    for r in rules:
        try:
            pat = compile_pattern(r["find"], r["regex"], r["ignore_case"], r["word"])
        except re.error as e:
            print(f"Error: bad pattern {r['find']!r}: {e}", file=sys.stderr)
            return 2
        compiled.append((pat, r["replace"], r))

    text = read_text(in_path)
    counts: List[int] = []
    dry_hits: List[List[Tuple[int, int, str, str]]] = []

    for pat, repl, r in compiled:
        if args.dry_run:
            hits = find_matches_with_context(text, pat, args.max)
            dry_hits.append(hits)
            counts.append(len(hits))
        else:
            count_for_rule = 0
            if args.max > 0:
                text, n = pat.subn(repl, text, count=args.max)
                count_for_rule = n
            else:
                text, n = pat.subn(repl, text)
                count_for_rule = n
            counts.append(count_for_rule)

    total = sum(counts)

    if args.dry_run:
        # Print the would-be matches
        if not args.quiet:
            for (pat, repl, r), hits in zip(compiled, dry_hits):
                print(f"# rule: find={r['find']!r} replace={repl!r} "
                      f"regex={r['regex']} matches={len(hits)}", file=sys.stdout)
                for line_no, col, matched, line_text in hits:
                    snippet = line_text
                    if len(snippet) > 120:
                        snippet = snippet[:120] + "..."
                    print(f"  {line_no}:{col}  {matched!r}  | {snippet}",
                          file=sys.stdout)
        # In dry-run mode, do NOT write to output_path
    else:
        if args.count:
            # In --count mode, still write output unless dry-run
            write_text(out_path, text)
        else:
            write_text(out_path, text)

    summary = {
        "input": str(in_path),
        "output": str(out_path) if not args.dry_run else None,
        "rules": [{
            "find": r["find"], "replace": r["replace"], "regex": r["regex"],
            "ignore_case": r["ignore_case"], "word": r["word"],
            "count": c,
        } for r, c in zip(rules, counts)],
        "total_replacements": total,
        "dry_run": args.dry_run,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            per = " ".join(f"#{i+1}={c}" for i, c in enumerate(counts))
            kind = "dry-run hits" if args.dry_run else "replacements"
            dest = "" if args.dry_run else f" -> {out_path}"
            print(f"Replace: {total} {kind} ({per}){dest}", file=sys.stderr)

    return 0 if total > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
