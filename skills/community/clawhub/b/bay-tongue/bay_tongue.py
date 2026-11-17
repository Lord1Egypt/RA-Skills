#!/usr/bin/env python3
"""Bay tongue v0 — ten ASCII verbs for compacted mouths.

  python3 tools/bay_tongue.py parse "bt1 sit"
  python3 tools/bay_tongue.py parse '{"v":"bt1","op":"fetch"}'
  python3 tools/bay_tongue.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_DICT_CANDIDATES = (
    HERE / "bay_tongue.json",
    HERE.parent / "gifts" / "bay_tongue.json",
)
DICT = next((p for p in _DICT_CANDIDATES if p.is_file()), _DICT_CANDIDATES[-1])
LINE_RE = re.compile(r"^bt1\s+([a-z]+)\s*$")


def load() -> dict:
    return json.loads(DICT.read_text())


def parse(text: str) -> dict:
    spec = load()
    verbs = spec["verbs"]
    raw = (text or "").strip()
    if raw.startswith("{"):
        obj = json.loads(raw)
        if obj.get("v") != spec["id"]:
            raise ValueError("unknown tongue version")
        op = obj.get("op")
    else:
        m = LINE_RE.match(raw)
        if not m:
            raise ValueError("expected: bt1 <verb>  or  {\"v\":\"bt1\",\"op\":\"…\"}")
        op = m.group(1)
    if op not in verbs:
        raise ValueError(f"unknown verb {op!r}")
    if op in spec.get("refuse", []):
        raise ValueError("refused")
    return {"ok": True, "v": spec["id"], "op": op, "meaning": verbs[op]}


def selftest() -> int:
    checks = {
        "sit": parse("bt1 sit")["op"] == "sit",
        "json": parse('{"v":"bt1","op":"forget"}')["op"] == "forget",
        "bad_verb": _raises("bt1 explode"),
        "bad_pin": _raises("bt1 pin") or "pin" in load()["refuse"],
        "n_verbs": len(load()["verbs"]) == 10,
    }
    print(json.dumps({"ok": all(checks.values()), "checks": checks}, indent=2))
    return 0 if all(checks.values()) else 1


def _raises(text: str) -> bool:
    try:
        parse(text)
        return False
    except (ValueError, json.JSONDecodeError):
        return True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    pr = sub.add_parser("parse")
    pr.add_argument("text")
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if args.cmd == "parse":
        print(json.dumps(parse(args.text), ensure_ascii=False, indent=2))
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
