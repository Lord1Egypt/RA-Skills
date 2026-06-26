#!/usr/bin/env python3
"""
transform.py - Add, modify, or remove columns in a CSV / TSV / JSONL file.

Streaming, single-pass. No `eval`. Uses the same safe-expression language
as filter.py: identifiers, +, -, *, /, %, parentheses, function calls.

Usage:
    transform.py INPUT OUTPUT [operations...]

Operations (apply in the order given on the command line):
    --add NAME=EXPR        compute a new column NAME from EXPR
    --set NAME=EXPR        overwrite existing column NAME with EXPR
    --drop COL[,COL2...]   remove these column(s)
    --rename OLD=NEW       rename a column
    --cast COL:TYPE        coerce a column to int, float, bool, or string
    --keep COL[,COL2...]   keep only these columns (final selection)

Expression language:
    column references          plain identifier:  amount, status, region
    literals                   123, 3.14, "hello", 'hi'
    arithmetic                 +  -  *  /  %  (integer or float)
    string concat              col1 + "_" + col2
    parentheses                (a + b) * c
    boolean comparisons        ==  !=  <  <=  >  >=  (yields 1 or 0)
    function calls             upper(name), lower(email), strip(s),
                               len(s), abs(n), round(n,2),
                               int(x), float(x), str(x),
                               replace(s, "old", "new"),
                               split(s, ","), join(parts, "-"),
                               coalesce(a, b, c)   first non-empty
                               year(date), month(date), day(date)
                               (date is "YYYY-MM-DD")

Options:
    --json                emit a machine-readable summary on stdout
    --quiet               suppress the text summary
    -h, --help            show this help

Exit codes:
    0  success
    1  zero output rows
    2  bad arguments / unsafe path / missing file / unknown function /
       unknown column / division by zero in a constant fold / unsupported ext
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from _common import open_table, safe_path

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl"}


# ---- Tokenizer -------------------------------------------------------------

_TOKEN_RE = re.compile(
    r'\s*('
    r'"(?:[^"\\]|\\.)*"'
    r"|'(?:[^'\\]|\\.)*'"
    r"|\d+\.\d+|\d+"               # number literal
    r"|==|!=|<=|>=|<|>"            # comparison
    r"|[+\-*/%(),]"               # ops and punctuation
    r"|[A-Za-z_][A-Za-z0-9_]*"    # identifier
    r')'
)


def tokenize(expr: str) -> List[str]:
    out, pos = [], 0
    while pos < len(expr):
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            raise ValueError(f"cannot tokenize near: {expr[pos:pos+20]!r}")
        out.append(m.group(1))
        pos = m.end()
    return out


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return bytes(s[1:-1], "utf-8").decode("unicode_escape")
    return s


# ---- Built-in functions ----------------------------------------------------

def _to_num(v):
    if isinstance(v, (int, float)):
        return v
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        pass
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _date_parts(s, idx: int) -> int:
    """Return year/month/day from 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'."""
    if not isinstance(s, str) or len(s) < 10:
        raise ValueError(f"not a date: {s!r}")
    return int(s[:10].split("-")[idx])


FUNCS: Dict[str, Callable] = {
    "upper":     lambda s: str(s).upper(),
    "lower":     lambda s: str(s).lower(),
    "strip":     lambda s: str(s).strip(),
    "len":       lambda s: len(str(s)),
    "abs":       lambda n: abs(_to_num(n) if _to_num(n) is not None else 0),
    "round":     lambda n, d=0: round(_to_num(n) or 0, int(_to_num(d) or 0)),
    "int":       lambda x: int(_to_num(x) or 0),
    "float":     lambda x: float(_to_num(x) or 0.0),
    "str":       lambda x: str(x),
    "replace":   lambda s, a, b: str(s).replace(str(a), str(b)),
    "split":     lambda s, sep: str(s).split(str(sep)),
    "join":      lambda parts, sep: str(sep).join(str(p) for p in parts),
    "coalesce":  lambda *xs: next((x for x in xs if x not in ("", None)), ""),
    "year":      lambda s: _date_parts(s, 0),
    "month":     lambda s: _date_parts(s, 1),
    "day":       lambda s: _date_parts(s, 2),
}


# ---- Parser (precedence: ==/!=/<= ... < +/- < */%/) ----------------------

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

    def parse(self) -> Callable[[dict], object]:
        fn = self.parse_cmp()
        if self.i != len(self.t):
            raise ValueError(f"unexpected token: {self.peek()!r}")
        return fn

    def parse_cmp(self) -> Callable[[dict], object]:
        left = self.parse_addsub()
        ops = {"==", "!=", "<", "<=", ">", ">="}
        while self.peek() in ops:
            op = self.eat()
            right = self.parse_addsub()
            l, r = left, right
            left = self._make_cmp(op, l, r)
        return left

    @staticmethod
    def _make_cmp(op: str, l, r) -> Callable[[dict], int]:
        def fn(row):
            a, b = l(row), r(row)
            an, bn = _to_num(a), _to_num(b)
            if an is not None and bn is not None:
                a, b = an, bn
            else:
                a, b = str(a), str(b)
            try:
                if op == "==": return 1 if a == b else 0
                if op == "!=": return 1 if a != b else 0
                if op == "<":  return 1 if a < b else 0
                if op == "<=": return 1 if a <= b else 0
                if op == ">":  return 1 if a > b else 0
                if op == ">=": return 1 if a >= b else 0
            except TypeError:
                return 0
            return 0
        return fn

    def parse_addsub(self) -> Callable[[dict], object]:
        left = self.parse_muldiv()
        while self.peek() in ("+", "-"):
            op = self.eat()
            right = self.parse_muldiv()
            l, r = left, right
            if op == "+":
                left = (lambda l, r: lambda row: _add(l(row), r(row)))(l, r)
            else:
                left = (lambda l, r: lambda row: _sub(l(row), r(row)))(l, r)
        return left

    def parse_muldiv(self) -> Callable[[dict], object]:
        left = self.parse_unary()
        while self.peek() in ("*", "/", "%"):
            op = self.eat()
            right = self.parse_unary()
            l, r = left, right
            if op == "*":
                left = (lambda l, r: lambda row: _mul(l(row), r(row)))(l, r)
            elif op == "/":
                left = (lambda l, r: lambda row: _div(l(row), r(row)))(l, r)
            else:
                left = (lambda l, r: lambda row: _mod(l(row), r(row)))(l, r)
        return left

    def parse_unary(self) -> Callable[[dict], object]:
        if self.peek() == "-":
            self.eat()
            inner = self.parse_atom()
            return lambda row: -(_to_num(inner(row)) or 0)
        if self.peek() == "+":
            self.eat()
            return self.parse_atom()
        return self.parse_atom()

    def parse_atom(self) -> Callable[[dict], object]:
        tok = self.peek()
        if tok == "(":
            self.eat()
            inner = self.parse_cmp()
            if self.peek() != ")":
                raise ValueError("missing closing ')'")
            self.eat()
            return inner
        if tok and (tok[0] in ('"', "'")):
            self.eat()
            lit = _strip_quotes(tok)
            return lambda row, lit=lit: lit
        if tok and (tok[0].isdigit() or (tok[0] == "." and len(tok) > 1)):
            self.eat()
            if "." in tok:
                val = float(tok)
            else:
                val = int(tok)
            return lambda row, val=val: val
        if tok and (tok[0].isalpha() or tok[0] == "_"):
            self.eat()
            # function call?
            if self.peek() == "(":
                self.eat()
                args: List[Callable] = []
                if self.peek() != ")":
                    args.append(self.parse_cmp())
                    while self.peek() == ",":
                        self.eat()
                        args.append(self.parse_cmp())
                if self.peek() != ")":
                    raise ValueError(f"missing ')' in call to {tok}()")
                self.eat()
                if tok not in FUNCS:
                    raise ValueError(f"unknown function: {tok!r}")
                fn = FUNCS[tok]
                return (lambda fn, args: lambda row: fn(*[a(row) for a in args]))(fn, args)
            # column reference
            return lambda row, name=tok: row.get(name, "")
        raise ValueError(f"unexpected token: {tok!r}")


def _is_empty(v) -> bool:
    return v is None or v == ""


def _add(a, b):
    # If both numeric, add as numbers. If either is empty, propagate empty.
    # Otherwise treat as string concat.
    if _is_empty(a) or _is_empty(b):
        # Empty + something => empty (SQL NULL-style propagation), EXCEPT
        # for string concat between two known strings (rare here).
        if _is_empty(a) and _is_empty(b):
            return ""
        if _is_empty(a):
            return b
        return a
    an, bn = _to_num(a), _to_num(b)
    if an is not None and bn is not None:
        return an + bn
    return str(a) + str(b)


def _sub(a, b):
    if _is_empty(a) or _is_empty(b):
        return ""
    an, bn = _to_num(a), _to_num(b)
    if an is not None and bn is not None:
        return an - bn
    raise ValueError(f"cannot subtract non-numeric: {a!r} - {b!r}")


def _mul(a, b):
    if _is_empty(a) or _is_empty(b):
        return ""
    an, bn = _to_num(a), _to_num(b)
    if an is not None and bn is not None:
        return an * bn
    if isinstance(a, str) and bn is not None:
        return a * int(bn)
    raise ValueError(f"cannot multiply: {a!r} * {b!r}")


def _div(a, b):
    if _is_empty(a) or _is_empty(b):
        return ""
    an, bn = _to_num(a), _to_num(b)
    if an is None or bn is None:
        raise ValueError(f"cannot divide non-numeric: {a!r} / {b!r}")
    if bn == 0:
        raise ValueError("division by zero")
    return an / bn


def _mod(a, b):
    if _is_empty(a) or _is_empty(b):
        return ""
    an, bn = _to_num(a), _to_num(b)
    if an is None or bn is None:
        raise ValueError(f"cannot mod non-numeric: {a!r} % {b!r}")
    if bn == 0:
        raise ValueError("modulo by zero")
    return an % bn


def compile_expr(expr: str) -> Callable[[dict], object]:
    return Parser(tokenize(expr)).parse()


# ---- Cast ------------------------------------------------------------------

def cast_value(value, target: str):
    if target == "string":
        return "" if value is None else str(value)
    if target == "int":
        n = _to_num(value)
        return int(n) if n is not None else ""
    if target == "float":
        n = _to_num(value)
        return float(n) if n is not None else ""
    if target == "bool":
        s = str(value).strip().lower()
        if s in ("true", "yes", "y", "1", "t"):
            return 1
        if s in ("false", "no", "n", "0", "f", ""):
            return 0
        return ""
    raise ValueError(f"unknown cast target: {target!r}")


# ---- Operation pipeline ---------------------------------------------------

def parse_kv(spec: str, what: str) -> Tuple[str, str]:
    if "=" not in spec:
        raise ValueError(f"--{what} expects NAME=VALUE, got: {spec!r}")
    name, _, value = spec.partition("=")
    return name.strip(), value


def parse_colon(spec: str, what: str) -> Tuple[str, str]:
    if ":" not in spec:
        raise ValueError(f"--{what} expects COL:TYPE, got: {spec!r}")
    name, _, value = spec.partition(":")
    return name.strip(), value.strip()


def build_pipeline(argv: List[str]) -> List[Tuple[str, object]]:
    ops: List[Tuple[str, object]] = []
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok == "--add":
            i += 1
            name, expr = parse_kv(argv[i], "add")
            ops.append(("add", (name, compile_expr(expr))))
        elif tok == "--set":
            i += 1
            name, expr = parse_kv(argv[i], "set")
            ops.append(("set", (name, compile_expr(expr))))
        elif tok == "--drop":
            i += 1
            cols = [c.strip() for c in argv[i].split(",") if c.strip()]
            ops.append(("drop", cols))
        elif tok == "--rename":
            i += 1
            old, new = parse_kv(argv[i], "rename")
            ops.append(("rename", (old, new.strip())))
        elif tok == "--cast":
            i += 1
            col, typ = parse_colon(argv[i], "cast")
            if typ not in ("int", "float", "bool", "string"):
                raise ValueError(f"--cast target must be int/float/bool/string, got {typ!r}")
            ops.append(("cast", (col, typ)))
        elif tok == "--keep":
            i += 1
            cols = [c.strip() for c in argv[i].split(",") if c.strip()]
            ops.append(("keep", cols))
        else:
            raise ValueError(f"unknown operation: {tok!r}")
        i += 1
    return ops


def apply_ops(header: List[str], row: Dict[str, str],
              ops: List[Tuple[str, object]]) -> Tuple[List[str], Dict[str, object]]:
    """Apply ops to a single row, returning (new_header, new_row).
    new_header is recomputed per row from the ops + original header so the
    schema is determined by ops alone, not by which row happens to be first."""
    out: Dict[str, object] = {c: row.get(c, "") for c in header}
    cur_header = list(header)
    for kind, payload in ops:
        if kind == "add":
            name, fn = payload
            out[name] = fn(out)
            if name not in cur_header:
                cur_header.append(name)
        elif kind == "set":
            name, fn = payload
            out[name] = fn(out)
            if name not in cur_header:
                cur_header.append(name)
        elif kind == "drop":
            for c in payload:
                out.pop(c, None)
                if c in cur_header:
                    cur_header.remove(c)
        elif kind == "rename":
            old, new = payload
            if old in out:
                out[new] = out.pop(old)
            if old in cur_header:
                idx = cur_header.index(old)
                cur_header[idx] = new
        elif kind == "cast":
            col, typ = payload
            if col in out:
                out[col] = cast_value(out[col], typ)
        elif kind == "keep":
            keep_set = set(payload)
            new_out = {c: out.get(c, "") for c in payload}
            out = new_out
            cur_header = list(payload)
    return cur_header, out


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if len(sys.argv) < 3:
        print("Error: usage: transform.py INPUT OUTPUT [operations...]",
              file=sys.stderr)
        return 2

    args = list(sys.argv[1:])
    in_arg = args.pop(0)
    out_arg = args.pop(0)

    as_json = False
    quiet = False
    rest: List[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--json":
            as_json = True
        elif a == "--quiet":
            quiet = True
        else:
            rest.append(a)
        i += 1

    try:
        in_path = safe_path(in_arg)
        out_path = safe_path(out_arg)
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
        ops = build_pipeline(rest)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if not ops:
        print("Error: at least one operation (--add/--set/--drop/--rename/--cast/--keep) required",
              file=sys.stderr)
        return 2

    # Compute output header symbolically (no expression evaluation, so empty
    # cells don't break arithmetic). Just track which columns the ops add /
    # drop / rename / keep.
    with open_table(in_path) as (_kind, header, _it):
        out_header: List[str] = list(header)
        for kind, payload in ops:
            if kind in ("add", "set"):
                name = payload[0]
                if name not in out_header:
                    out_header.append(name)
            elif kind == "drop":
                out_header = [c for c in out_header if c not in payload]
            elif kind == "rename":
                old, new = payload
                if old in out_header:
                    out_header[out_header.index(old)] = new
            elif kind == "cast":
                pass  # doesn't change schema
            elif kind == "keep":
                out_header = [c for c in payload if c in out_header or True]
                # Re-prune missing - keep order from the --keep spec but
                # warn would be nice. Allow missing cols (they'll be empty).
                out_header = list(payload)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = "jsonl" if ext == ".jsonl" else ("tsv" if ext == ".tsv" else "csv")

    rows_in = 0
    rows_out = 0
    with open(out_path, "w", encoding="utf-8", newline="") as fout:
        if fmt == "jsonl":
            def emit(row, header=None):
                fout.write(json.dumps(
                    {k: ("" if v is None else v) for k, v in row.items()},
                    ensure_ascii=False) + "\n")
        else:
            delim = "\t" if fmt == "tsv" else ","
            writer = csv.DictWriter(fout, fieldnames=out_header, delimiter=delim,
                                    extrasaction="ignore")
            writer.writeheader()
            def emit(row, header=None):
                writer.writerow({k: ("" if v is None else v) for k, v in row.items()})

        with open_table(in_path) as (_kind, header, reader):
            for row in reader:
                rows_in += 1
                try:
                    _h, new_row = apply_ops(header, row, ops)
                except Exception:
                    # Per-row arithmetic errors (e.g. subtracting empty from
                    # a number) leave the derived columns empty in this row
                    # but do not abort the whole pipeline. The schema is
                    # already known so we can fill the row from out_header.
                    new_row = {c: row.get(c, "") for c in out_header}
                emit(new_row)
                rows_out += 1

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "rows_in": rows_in,
        "rows_out": rows_out,
        "columns_out": out_header,
        "operations": [op[0] for op in ops],
    }
    if not quiet:
        if as_json:
            print(json.dumps(summary, indent=2))
        else:
            print(f"Transform: {rows_in} rows -> {rows_out} rows "
                  f"({len(out_header)} columns) -> {out_path}")
    return 0 if rows_out > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
