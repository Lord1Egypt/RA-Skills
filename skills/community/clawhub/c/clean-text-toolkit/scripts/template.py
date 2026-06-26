#!/usr/bin/env python3
"""
template.py - Substitute placeholders in a text file with values from a
JSON / key=value source. No Jinja2, no `eval`, no remote calls.

Placeholder syntax (default):
    {{name}}          required
    {{name | filter}} pipe a filter (e.g. {{user_name | upper}})
    {{name?default}}  fallback value if name is missing or empty
    {{name | upper ?DEFAULT}}   filter + default

Usage:
    template.py TEMPLATE OUTPUT --vars FILE.json
    template.py TEMPLATE OUTPUT --set k=v --set k2=v2
    template.py TEMPLATE OUTPUT --vars FILE.json --set override=newval

Sources (merged left-to-right; --set wins):
    --vars PATH     JSON object (top-level dict only). Supports .json.
    --set K=V       inline override; may repeat.

Options:
    --syntax mustache|dollar|percent
                    mustache (default) -> {{name}}
                    dollar              -> ${name}
                    percent             -> %(name)s
    --strict        error out (exit 1) if any placeholder is unresolved
    --json          emit machine-readable summary on stderr
    --quiet         suppress the text summary on stderr
    -h, --help      show this help

Built-in filters:
    upper, lower, title, strip, capitalize,
    reverse, len, escape-html, escape-json, urlencode

Exit codes:
    0  success
    1  --strict mode and at least one placeholder was unresolved
    2  bad arguments / unsafe path / missing file / bad --vars JSON /
       unknown filter / unknown syntax
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List

from _common import read_text, safe_path, write_text


FILTERS = {
    "upper":       lambda s: str(s).upper(),
    "lower":       lambda s: str(s).lower(),
    "title":       lambda s: str(s).title(),
    "strip":       lambda s: str(s).strip(),
    "capitalize":  lambda s: str(s).capitalize(),
    "reverse":     lambda s: str(s)[::-1],
    "len":         lambda s: str(len(str(s))),
    "escape-html": lambda s: html.escape(str(s)),
    "escape-json": lambda s: json.dumps(str(s))[1:-1],
    "urlencode":   lambda s: urllib.parse.quote(str(s), safe=""),
}


SYNTAX_RE = {
    "mustache": re.compile(r"\{\{\s*([^{}]+?)\s*\}\}"),
    "dollar":   re.compile(r"\$\{\s*([^${}]+?)\s*\}"),
    "percent":  re.compile(r"%\(\s*([^)\s]+?)\s*\)s"),
}


def render(template: str, syntax: str, values: Dict[str, str],
           strict: bool) -> tuple[str, List[str], List[str]]:
    """Returns (rendered, resolved_names, unresolved_names)."""
    pat = SYNTAX_RE[syntax]
    resolved: List[str] = []
    unresolved: List[str] = []

    def repl(m: re.Match) -> str:
        body = m.group(1).strip()
        # Parse "name | filter1 | filter2 ? default"
        default = ""
        if "?" in body:
            body, default = body.split("?", 1)
            default = default.strip()
        parts = [p.strip() for p in body.split("|")]
        name = parts[0]
        filters = parts[1:]

        value = values.get(name, None)
        if value is None or value == "":
            if default != "":
                value = default
            elif strict:
                unresolved.append(name)
                return m.group(0)  # leave as-is
            else:
                unresolved.append(name)
                value = ""

        for f in filters:
            if f not in FILTERS:
                # We can't raise here cleanly because re.sub swallows exceptions;
                # store a sentinel and check after.
                raise KeyError(f"unknown filter: {f!r}")
            value = FILTERS[f](value)
        resolved.append(name)
        return str(value)

    rendered = pat.sub(repl, template)
    return rendered, resolved, unresolved


def parse_set(specs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for s in specs:
        if "=" not in s:
            raise ValueError(f"--set expects KEY=VALUE, got: {s!r}")
        k, _, v = s.partition("=")
        out[k.strip()] = v
    return out


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("template", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--vars")
    p.add_argument("--set", dest="sets", action="append", default=[])
    p.add_argument("--syntax", choices=("mustache", "dollar", "percent"),
                   default="mustache")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.template or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        tpl_path = safe_path(args.template)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not tpl_path.is_file():
        print(f"Error: not a file: {tpl_path}", file=sys.stderr)
        return 2

    values: Dict[str, str] = {}
    if args.vars:
        try:
            vars_path = safe_path(args.vars)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if not vars_path.is_file():
            print(f"Error: --vars file not found: {vars_path}", file=sys.stderr)
            return 2
        try:
            obj = json.loads(vars_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Error: --vars JSON parse error: {e}", file=sys.stderr)
            return 2
        if not isinstance(obj, dict):
            print(f"Error: --vars must contain a top-level JSON object", file=sys.stderr)
            return 2
        for k, v in obj.items():
            values[str(k)] = "" if v is None else str(v)

    try:
        inline = parse_set(args.sets)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    values.update(inline)

    template = read_text(tpl_path)
    try:
        rendered, resolved, unresolved = render(template, args.syntax, values, args.strict)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    write_text(out_path, rendered)

    summary = {
        "template": str(tpl_path),
        "output": str(out_path),
        "syntax": args.syntax,
        "vars_count": len(values),
        "placeholders_resolved": len(resolved),
        "placeholders_unresolved": len(unresolved),
        "unresolved_names": sorted(set(unresolved)),
        "strict": args.strict,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            u = f", {len(unresolved)} unresolved" if unresolved else ""
            print(f"Template: {len(resolved)} placeholder(s) resolved{u} -> {out_path}",
                  file=sys.stderr)
            if unresolved:
                names = sorted(set(unresolved))
                preview = ", ".join(names[:5])
                more = f" (+{len(names)-5} more)" if len(names) > 5 else ""
                print(f"  unresolved: {preview}{more}", file=sys.stderr)

    if args.strict and unresolved:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
