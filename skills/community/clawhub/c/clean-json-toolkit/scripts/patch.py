#!/usr/bin/env python3
"""
patch.py - Apply RFC 6902 JSON Patch operations to a JSON document, or
build patches programmatically.

A JSON Patch is a list of operations, each of the form:
    {"op": "add",     "path": "/users/0/email", "value": "alice@example.com"}
    {"op": "remove",  "path": "/users/0/email"}
    {"op": "replace", "path": "/users/0/email", "value": "new@example.com"}
    {"op": "move",    "from": "/users/0/email", "path": "/contact/email"}
    {"op": "copy",    "from": "/users/0/email", "path": "/contact/email"}
    {"op": "test",    "path": "/users/0/email", "value": "alice@example.com"}

Paths use JSON Pointer (RFC 6901): /a/b/0/c. Use "-" as the last segment to
append to an array (e.g. "/items/-").

Usage:
    patch.py INPUT OUTPUT --patch PATCH.json [options]
    patch.py INPUT OUTPUT --op add --path /name --value '"Alice"' [options]

Modes:
    --patch FILE              read patch operations from a JSON file (list)
    --op OP --path P [--value V] [--from F]
                              build a single-op patch on the command line.
                              For --value, pass a JSON literal (use quotes
                              around strings, e.g. --value '"Alice"').

Options:
    --dry-run         do NOT write OUTPUT; print the result on stdout
    --strict          abort on first test/op failure (default: keep going,
                      collect errors)
    --json            emit a machine-readable summary on stderr
    --quiet           suppress the text summary
    -h, --help        show this help

Exit codes:
    0   patch applied cleanly (all operations succeeded)
    1   at least one operation failed (test mismatch, missing path, etc.)
        \u2014 in --strict mode this aborts after the first failure
    2   bad arguments / unsafe path / missing file / invalid JSON /
        unknown op / bad pointer syntax
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from _common import load_json, safe_path


VALID_OPS = {"add", "remove", "replace", "move", "copy", "test"}


def parse_pointer(p: str) -> List[str]:
    """Parse a JSON Pointer like '/a/b/0/c' into tokens ['a','b','0','c']."""
    if p == "":
        return []
    if not p.startswith("/"):
        raise ValueError(f"JSON Pointer must start with '/' or be empty: {p!r}")
    parts = p.split("/")[1:]
    # Decode ~1 -> '/' and ~0 -> '~' (RFC 6901)
    return [seg.replace("~1", "/").replace("~0", "~") for seg in parts]


def _walk(doc: Any, parts: List[str]) -> Tuple[Any, Any, Any]:
    """Walk to (parent, last_key, current_value) for the given pointer parts.
    For an empty pointer, parent is None and last_key is None (the document
    itself is the target).
    """
    if not parts:
        return None, None, doc
    parent = doc
    for i, seg in enumerate(parts[:-1]):
        if isinstance(parent, list):
            try:
                idx = int(seg)
            except ValueError:
                raise KeyError(f"expected array index at segment {i}: {seg!r}")
            if idx < 0 or idx >= len(parent):
                raise KeyError(f"array index {idx} out of bounds (len={len(parent)})")
            parent = parent[idx]
        elif isinstance(parent, dict):
            if seg not in parent:
                raise KeyError(f"missing key at segment {i}: {seg!r}")
            parent = parent[seg]
        else:
            raise KeyError(f"cannot descend into {type(parent).__name__} at segment {i}")
    last = parts[-1]
    if isinstance(parent, list):
        if last == "-":
            return parent, "-", None
        try:
            idx = int(last)
        except ValueError:
            raise KeyError(f"expected array index at last segment: {last!r}")
        if idx < 0 or idx > len(parent):
            raise KeyError(f"array index {idx} out of bounds (len={len(parent)})")
        return parent, idx, (parent[idx] if idx < len(parent) else None)
    if isinstance(parent, dict):
        return parent, last, parent.get(last)
    raise KeyError(f"cannot address inside {type(parent).__name__}")


def _set(parent: Any, key: Any, value: Any) -> None:
    if isinstance(parent, list):
        if key == "-":
            parent.append(value)
        elif isinstance(key, int):
            if key == len(parent):
                parent.append(value)
            else:
                parent.insert(key, value)
    elif isinstance(parent, dict):
        parent[key] = value


def _remove(parent: Any, key: Any) -> Any:
    if isinstance(parent, list):
        if isinstance(key, int):
            return parent.pop(key)
    elif isinstance(parent, dict):
        return parent.pop(key, None)
    return None


def apply_op(doc: Any, op: Dict[str, Any]) -> Tuple[Any, bool, str]:
    """Apply one operation. Returns (new_doc, ok, error_msg)."""
    name = op.get("op")
    if name not in VALID_OPS:
        return doc, False, f"unknown op {name!r}"
    if "path" not in op:
        return doc, False, "missing 'path'"
    try:
        parts = parse_pointer(op["path"])
    except ValueError as e:
        return doc, False, str(e)

    try:
        if name == "add":
            if "value" not in op:
                return doc, False, "'add' requires 'value'"
            if not parts:
                return op["value"], True, ""
            parent, key, _ = _walk(doc, parts)
            _set(parent, key, op["value"])
            return doc, True, ""

        if name == "remove":
            if not parts:
                return None, True, ""
            parent, key, _ = _walk(doc, parts)
            # RFC 6902: remove MUST fail if the target location does not exist.
            if isinstance(parent, dict):
                if key not in parent:
                    return doc, False, f"remove target {op['path']!r} does not exist"
            elif isinstance(parent, list):
                if not isinstance(key, int) or key < 0 or key >= len(parent):
                    return doc, False, f"remove target {op['path']!r} out of bounds"
            _remove(parent, key)
            return doc, True, ""

        if name == "replace":
            if "value" not in op:
                return doc, False, "'replace' requires 'value'"
            if not parts:
                return op["value"], True, ""
            parent, key, _ = _walk(doc, parts)
            if isinstance(parent, list) and isinstance(key, int):
                if 0 <= key < len(parent):
                    parent[key] = op["value"]
                else:
                    return doc, False, "replace target out of bounds"
            elif isinstance(parent, dict):
                if key not in parent:
                    return doc, False, f"replace target {op['path']!r} does not exist"
                parent[key] = op["value"]
            return doc, True, ""

        if name in ("move", "copy"):
            if "from" not in op:
                return doc, False, f"{name!r} requires 'from'"
            try:
                from_parts = parse_pointer(op["from"])
            except ValueError as e:
                return doc, False, str(e)
            try:
                fparent, fkey, fval = _walk(doc, from_parts)
            except KeyError as e:
                return doc, False, f"{name}: 'from' invalid: {e}"
            if isinstance(fparent, list) and isinstance(fkey, int):
                value = fparent[fkey]
            elif isinstance(fparent, dict):
                value = fparent[fkey]
            else:
                return doc, False, f"{name}: cannot read from {op['from']!r}"
            if name == "move":
                _remove(fparent, fkey)
            # Now add at path
            if not parts:
                return value, True, ""
            try:
                parent, key, _ = _walk(doc, parts)
            except KeyError as e:
                return doc, False, f"{name}: path invalid: {e}"
            _set(parent, key, value)
            return doc, True, ""

        if name == "test":
            if "value" not in op:
                return doc, False, "'test' requires 'value'"
            try:
                _parent, _key, cur = _walk(doc, parts)
            except KeyError as e:
                return doc, False, f"test path missing: {e}"
            if cur != op["value"]:
                return doc, False, f"test failed at {op['path']}: " \
                                   f"got {cur!r}, expected {op['value']!r}"
            return doc, True, ""

    except KeyError as e:
        return doc, False, str(e)
    return doc, False, "unhandled op"


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--patch")
    p.add_argument("--op")
    p.add_argument("--path")
    p.add_argument("--value")
    p.add_argument("--from", dest="from_path")
    p.add_argument("--dry-run", dest="dry_run", action="store_true")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2
    if out_path.suffix.lower() != ".json":
        print(f"Error: output must be a .json file (got {out_path.suffix!r})",
              file=sys.stderr)
        return 2

    # Build operations list
    if args.patch and (args.op or args.path or args.value):
        print("Error: use either --patch FILE or --op/--path/--value, not both",
              file=sys.stderr)
        return 2
    if not args.patch and not args.op:
        print("Error: provide --patch FILE or --op ... --path ...",
              file=sys.stderr)
        return 2

    if args.patch:
        try:
            patch_path = safe_path(args.patch)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if not patch_path.is_file():
            print(f"Error: patch file not found: {patch_path}", file=sys.stderr)
            return 2
        try:
            ops = json.loads(patch_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Error: patch file is not valid JSON: {e}", file=sys.stderr)
            return 2
        if not isinstance(ops, list):
            print("Error: patch file must contain a top-level JSON array",
                  file=sys.stderr)
            return 2
    else:
        if args.op not in VALID_OPS:
            print(f"Error: unknown --op {args.op!r}. "
                  f"Valid: {', '.join(sorted(VALID_OPS))}", file=sys.stderr)
            return 2
        if not args.path:
            print("Error: --path is required when using --op", file=sys.stderr)
            return 2
        op: Dict[str, Any] = {"op": args.op, "path": args.path}
        if args.value is not None:
            try:
                op["value"] = json.loads(args.value)
            except json.JSONDecodeError as e:
                print(f"Error: --value must be valid JSON: {e}", file=sys.stderr)
                return 2
        if args.from_path is not None:
            op["from"] = args.from_path
        ops = [op]

    try:
        data, _kind = load_json(in_path)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        return 2

    results: List[Dict[str, Any]] = []
    n_ok = 0
    n_fail = 0
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            results.append({"index": i, "ok": False,
                            "error": "op must be an object"})
            n_fail += 1
            if args.strict:
                break
            continue
        data, ok, err = apply_op(data, op)
        results.append({"index": i, "op": op.get("op"), "path": op.get("path"),
                        "ok": ok, "error": err})
        if ok:
            n_ok += 1
        else:
            n_fail += 1
            if args.strict:
                break

    if not args.dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                            encoding="utf-8")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    summary = {
        "input": str(in_path),
        "output": str(out_path) if not args.dry_run else None,
        "ops_total": len(ops),
        "ops_ok": n_ok,
        "ops_failed": n_fail,
        "results": results,
        "strict": args.strict,
    }
    if not args.quiet:
        if args.as_json:
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            dest = "" if args.dry_run else f" -> {out_path}"
            print(f"patch: {n_ok}/{len(ops)} op(s) OK, {n_fail} failed{dest}",
                  file=sys.stderr)
            if n_fail:
                for r in results:
                    if not r["ok"]:
                        print(f"  #{r['index']} FAIL: "
                              f"{r.get('op','?')} {r.get('path','?')} - "
                              f"{r['error']}", file=sys.stderr)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
