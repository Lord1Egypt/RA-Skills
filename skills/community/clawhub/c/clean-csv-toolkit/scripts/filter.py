#!/usr/bin/env python3
"""
filter.py - Filter rows from CSV / TSV / JSONL by a simple expression.

Streams one row at a time, evaluates a safe predicate language (NO Python
eval, NO arbitrary code), and writes matching rows to OUTPUT.

Usage:
    filter.py INPUT OUTPUT --where "EXPR" [--limit N]

Expression language (deliberately small):
    column-name  op  value
    optional --and / --or / parentheses

Operators:
    ==  !=  <  <=  >  >=         numeric or string compare
    =~                           regex match (right-hand side is the pattern)
    in                           value in comma-separated list  e.g.  status in pending,approved
    contains                     substring match
    is_empty / is_not_empty      no right-hand side
    is_number / is_not_number    no right-hand side

Examples:
    --where "amount > 100"
    --where "status == approved and country in IN,US"
    --where "email =~ @example\\.com$"
    --where "(status == approved or status == pending) and amount >= 50"
    --where "phone is_not_empty"

Options:
    --where EXPR         predicate to apply (required)
    --limit N            stop after writing N matching rows
    --invert             keep rows that DO NOT match (set-complement)
    --columns COL[,..]   write only these output columns (default: all)
    --json               emit machine-readable summary on stdout
    -h, --help           show this help

Exit codes:
    0  one or more rows matched
    1  zero rows matched
    2  bad arguments / unsafe path / missing file / parse error / missing column
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Callable, List, Tuple

from _common import open_table, safe_path

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl"}

# Two-operand operators sorted longest-first so the tokenizer matches the
# longest before a shorter substring (e.g. ">=" before ">").
BIN_OPS = ("==", "!=", "<=", ">=", "=~", "<", ">", "in", "contains")
NULL_OPS = ("is_empty", "is_not_empty", "is_number", "is_not_number")


# ---- Tokenizer -------------------------------------------------------------

_TOKEN_RE = re.compile(
    r'\s*('
    r'"(?:[^"\\]|\\.)*"'          # double-quoted string
    r"|'(?:[^'\\]|\\.)*'"        # single-quoted string
    r"|\(|\)"                      # parens
    r"|==|!=|<=|>=|=~|<|>"       # comparison
    r'|[A-Za-z_][A-Za-z0-9_]*'    # identifier / op-word
    r"|[^\s()]+"                   # any other contiguous non-space chunk
    r')'
)


def tokenize(expr: str) -> List[str]:
    out, pos = [], 0
    while pos < len(expr):
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            raise ValueError(f"cannot tokenize near: {expr[pos:pos+20]!r}")
        tok = m.group(1)
        pos = m.end()
        out.append(tok)
    return out


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return bytes(s[1:-1], "utf-8").decode("unicode_escape")
    return s


# ---- Parser (precedence: or < and; parentheses supported) -----------------

class Parser:
    def __init__(self, tokens: List[str]) -> None:
        self.t = tokens
        self.i = 0

    def peek(self) -> str:
        return self.t[self.i] if self.i < len(self.t) else ""

    def eat(self) -> str:
        tok = self.peek()
        self.i += 1
        return tok

    def parse(self) -> Callable[[dict], bool]:
        fn = self.parse_or()
        if self.i != len(self.t):
            raise ValueError(f"unexpected token: {self.peek()!r}")
        return fn

    def parse_or(self) -> Callable[[dict], bool]:
        left = self.parse_and()
        while self.peek().lower() == "or":
            self.eat()
            right = self.parse_and()
            l, r = left, right
            left = (lambda l, r: lambda row: l(row) or r(row))(l, r)
        return left

    def parse_and(self) -> Callable[[dict], bool]:
        left = self.parse_atom()
        while self.peek().lower() == "and":
            self.eat()
            right = self.parse_atom()
            l, r = left, right
            left = (lambda l, r: lambda row: l(row) and r(row))(l, r)
        return left

    def parse_atom(self) -> Callable[[dict], bool]:
        if self.peek() == "(":
            self.eat()
            inner = self.parse_or()
            if self.peek() != ")":
                raise ValueError("missing closing ')'")
            self.eat()
            return inner
        if self.peek().lower() == "not":
            self.eat()
            inner = self.parse_atom()
            return (lambda f: lambda row: not f(row))(inner)
        return self.parse_predicate()

    def parse_predicate(self) -> Callable[[dict], bool]:
        col = self.eat()
        if not col:
            raise ValueError("expected column name")
        op = self.eat().lower() if self.peek() else ""
        if not op:
            raise ValueError(f"expected operator after column {col!r}")
        if op in NULL_OPS:
            return _make_null_pred(col, op)
        if op not in BIN_OPS and op not in {x.lower() for x in BIN_OPS}:
            raise ValueError(f"unknown operator: {op!r}")

        # 'in' has a comma-separated list as RHS. Our tokenizer splits
        # `pending,approved` into [`pending`, `,approved`] (identifier match
        # wins for `pending`), so we slurp tokens until we hit a logical
        # operator, a paren, or end-of-input, then rejoin them.
        if op == "in":
            parts: List[str] = []
            while self.peek():
                nxt = self.peek()
                if nxt.lower() in ("and", "or") or nxt == ")":
                    break
                parts.append(self.eat())
            if not parts:
                raise ValueError("expected comma-separated values after 'in'")
            rhs = "".join(parts)
            return _make_bin_pred(col, op, _strip_quotes(rhs))

        rhs = self.eat()
        if not rhs:
            raise ValueError(f"expected value after operator {op!r}")
        return _make_bin_pred(col, op, _strip_quotes(rhs))


def _to_number(v: str):
    try:
        return int(v)
    except (TypeError, ValueError):
        pass
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _make_null_pred(col: str, op: str) -> Callable[[dict], bool]:
    def f(row: dict) -> bool:
        v = row.get(col, "")
        if op == "is_empty":
            return v == ""
        if op == "is_not_empty":
            return v != ""
        if op == "is_number":
            return _to_number(v) is not None
        if op == "is_not_number":
            return _to_number(v) is None
        return False
    return f


def _make_bin_pred(col: str, op: str, rhs: str) -> Callable[[dict], bool]:
    op = op.lower()
    if op == "=~":
        try:
            pat = re.compile(rhs)
        except re.error as e:
            raise ValueError(f"bad regex {rhs!r}: {e}")
        return lambda row: bool(pat.search(row.get(col, "")))
    if op == "in":
        choices = {x.strip() for x in rhs.split(",")}
        return lambda row: row.get(col, "") in choices
    if op == "contains":
        return lambda row: rhs in row.get(col, "")

    rhs_num = _to_number(rhs)

    def cmp_fn(row: dict) -> bool:
        v = row.get(col, "")
        if rhs_num is not None:
            v_num = _to_number(v)
            if v_num is not None:
                a, b = v_num, rhs_num
            else:
                a, b = v, rhs
        else:
            a, b = v, rhs
        try:
            if op == "==": return a == b
            if op == "!=": return a != b
            if op == "<":  return a < b
            if op == "<=": return a <= b
            if op == ">":  return a > b
            if op == ">=": return a >= b
        except TypeError:
            return False
        return False
    return cmp_fn


def compile_predicate(expr: str) -> Callable[[dict], bool]:
    return Parser(tokenize(expr)).parse()


# ---- Main ------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--where")
    p.add_argument("--limit", type=int)
    p.add_argument("--invert", action="store_true")
    p.add_argument("--columns")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2
    if not args.where:
        print("Error: --where EXPR is required", file=sys.stderr)
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

    ext = out_path.suffix.lower()
    if ext not in ALLOWED_OUTPUT_EXTS:
        print(f"Error: unsupported output extension '{ext}'. "
              f"Allowed: {', '.join(sorted(ALLOWED_OUTPUT_EXTS))}.", file=sys.stderr)
        return 2

    try:
        pred = compile_predicate(args.where)
    except ValueError as e:
        print(f"Error: bad --where expression: {e}", file=sys.stderr)
        return 2

    with open_table(in_path) as (_kind, header, _it):
        out_cols = [c.strip() for c in args.columns.split(",")] if args.columns else list(header)
        missing = [c for c in out_cols if c not in header]
        if missing:
            print(f"Error: column(s) not in header: {','.join(missing)}", file=sys.stderr)
            return 2

    fmt = "jsonl" if ext == ".jsonl" else ("tsv" if ext == ".tsv" else "csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    matched = 0
    scanned = 0
    limit = args.limit if args.limit and args.limit > 0 else None

    with open(out_path, "w", encoding="utf-8", newline="") as fout:
        if fmt == "jsonl":
            writer = fout
            def emit(row):
                fout.write(json.dumps(row, ensure_ascii=False) + "\n")
        else:
            delim = "\t" if fmt == "tsv" else ","
            csvw = csv.DictWriter(fout, fieldnames=out_cols, delimiter=delim,
                                  extrasaction="ignore")
            csvw.writeheader()
            def emit(row):
                csvw.writerow(row)

        with open_table(in_path) as (_kind, _hdr, reader):
            for row in reader:
                scanned += 1
                try:
                    keep = pred(row)
                except Exception:
                    keep = False
                if args.invert:
                    keep = not keep
                if keep:
                    out_row = {c: row.get(c, "") for c in out_cols}
                    emit(out_row)
                    matched += 1
                    if limit is not None and matched >= limit:
                        break

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "where": args.where,
        "invert": args.invert,
        "scanned": scanned,
        "matched": matched,
    }
    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Filter: scanned {scanned} rows, kept {matched} -> {out_path}")

    return 0 if matched > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
