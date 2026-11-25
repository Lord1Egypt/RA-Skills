#!/usr/bin/env python3
"""Generate reproducible embedded evidence; never calls a model or a network API."""

import argparse
import json
from pathlib import Path
import re
import sys

import armor_lint

ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile(r'(<script id="evidence" type="application/json">)(.*?)(</script>)', re.DOTALL)


def build_evidence():
    source = json.loads((ROOT / "assets/cases.json").read_text(encoding="utf-8"))
    if source["schema_version"] != 2 or not source["cases"]:
        raise ValueError("expected nonempty v2 cases")
    seen = set()
    cases = []
    for case in source["cases"]:
        if case["id"] in seen:
            raise ValueError("duplicate case id")
        seen.add(case["id"])
        for key in ("id", "title", "short", "tag", "request", "context", "before", "after", "counterexample", "outcome"):
            if not armor_lint.nonempty_string(case[key]):
                raise ValueError("empty case field: " + key)
        if not case["operations"] or not all(armor_lint.nonempty_string(s) for s in case["operations"]):
            raise ValueError("case operations must be nonempty strings")
        reports = {name: armor_lint.audit(case[name], case["before"], case["contract"])
                   for name in ("before", "after", "counterexample")}
        if not reports["after"]["passed"] or reports["counterexample"]["passed"]:
            raise ValueError("case did not meet expected contract outcomes: " + case["id"])
        cases.append(dict(case, reports=reports))
    return {
        "schema_version": 2,
        "engine_version": armor_lint.VERSION,
        "cases": cases,
        "summary": {
            "cases": len(cases),
            "anchors_total": sum(c["reports"]["after"]["anchors"]["total"] for c in cases),
            "anchors_matched": sum(c["reports"]["after"]["anchors"]["matched"] for c in cases),
            "counterexamples_blocked": sum(not c["reports"]["counterexample"]["passed"] for c in cases),
        },
    }


def serialize(evidence):
    return json.dumps(evidence, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def update(write=False):
    target = ROOT / "assets/de-armor-demo.html"
    html = target.read_text(encoding="utf-8")
    matches = list(MARKER.finditer(html))
    if len(matches) != 1:
        raise ValueError("expected exactly one embedded evidence block")
    match = matches[0]
    evidence = build_evidence()
    payload = serialize(evidence)
    if write:
        target.write_text(html[:match.start(2)] + payload + html[match.end(2):], encoding="utf-8")
    elif match.group(2) != payload:
        raise ValueError("embedded evidence is stale; run build_demo.py --write")
    print(json.dumps({"status": "written" if write else "current", **evidence["summary"]}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        update(args.write)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("build error: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
