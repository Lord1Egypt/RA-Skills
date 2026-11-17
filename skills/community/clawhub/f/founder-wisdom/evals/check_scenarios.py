#!/usr/bin/env python3
"""Validate evals/scenarios.yaml and print it in a readable form.

This does NOT invoke a model. It checks the data file's shape — required keys,
allowed values, referenced files actually existing on disk — plus the one
SKILL.md invariant that is cheap to check and expensive to discover late: the
frontmatter description staying inside its character budget. Then it prints the
scenarios so a human can run them by hand. Stdlib only, no dependencies.

Usage:
    python3 evals/check_scenarios.py            # validate + list
    python3 evals/check_scenarios.py --quiet    # validate only, exit code is the answer
    python3 evals/check_scenarios.py --id ID    # print one scenario in full
"""

from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(HERE, "scenarios.yaml")
SKILL = os.path.join(REPO, "SKILL.md")

# Skill descriptions are truncated or rejected past 1024 characters, and the
# symptom — the skill quietly stops triggering on some questions — is a long way
# from the cause. Budget well under the ceiling so the next domain added has
# somewhere to go; compress by moving enumeration into SKILL.md's routing list,
# which names every sub-topic anyway.
DESCRIPTION_BUDGET = 950
DESCRIPTION_CEILING = 1024

VALID_MODES = {"direct", "socratic", "none"}
REQUIRED_KEYS = [
    "id",
    "prompt",
    "should_trigger",
    "expected_mode",
    "expected_files",
    "assertions",
    "rationale",
]


# --------------------------------------------------------------------- parsing


def _strip(lines):
    """Drop blank lines and whole-line comments, returning (indent, text) pairs."""
    out = []
    for raw in lines:
        text = raw.rstrip("\n").rstrip()
        if not text.strip() or text.strip().startswith("#"):
            continue
        out.append((len(text) - len(text.lstrip(" ")), text.strip()))
    return out


def _scalar(token):
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        return token[1:-1]
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        return [_scalar(p) for p in inner.split(",")] if inner else []
    if token in ("true", "false"):
        return token == "true"
    if token.lstrip("-").isdigit():
        return int(token)
    return token


def _block(items, start, indent):
    """Return (value, next_index) for the block of `items` at column `indent`."""
    if items[start][1].startswith("- "):
        return _sequence(items, start, indent)
    return _mapping(items, start, indent)


def _sequence(items, start, indent):
    result, i = [], start
    while i < len(items) and items[i][0] == indent and items[i][1].startswith("- "):
        body = items[i][1][2:].strip()
        i += 1
        child_indent = indent + 2
        if ": " in body or body.endswith(":"):
            # Mapping whose first key sits on the dash line.
            synthetic = [(child_indent, body)]
            j = i
            while j < len(items) and items[j][0] >= child_indent:
                synthetic.append(items[j])
                j += 1
            value, _ = _mapping(synthetic, 0, child_indent)
            result.append(value)
            i = j
        else:
            result.append(_scalar(body))
    return result, i


def _mapping(items, start, indent):
    result, i = {}, start
    while i < len(items) and items[i][0] == indent:
        line = items[i][1]
        if line.startswith("- "):
            break
        key, _, rest = line.partition(":")
        key, rest = key.strip(), rest.strip()
        i += 1
        if rest in (">-", ">", "|", "|-"):
            chunk = []
            while i < len(items) and items[i][0] > indent:
                chunk.append(items[i][1])
                i += 1
            result[key] = " ".join(chunk)
        elif rest:
            result[key] = _scalar(rest)
        elif i < len(items) and items[i][0] > indent:
            result[key], i = _block(items, i, items[i][0])
        else:
            result[key] = None
    return result, i


def load(path):
    with open(path, encoding="utf-8") as handle:
        items = _strip(handle.readlines())
    value, _ = _mapping(items, 0, 0)
    return value


# ------------------------------------------------------------------ validation


def skill_description():
    """Return SKILL.md's frontmatter description, or None if it isn't there."""
    with open(SKILL, encoding="utf-8") as handle:
        raw = handle.read()
    match = re.search(r"^description: (.+)$", raw, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_description(description):
    if description is None:
        return ["SKILL.md: no `description` field in the frontmatter"]
    if len(description) > DESCRIPTION_BUDGET:
        return [
            f"SKILL.md: description is {len(description)} chars, over the "
            f"{DESCRIPTION_BUDGET}-char budget (runtime ceiling {DESCRIPTION_CEILING}). "
            f"Compress it into the routing list rather than spending the headroom."
        ]
    return []


def validate(doc):
    errors = []
    if doc.get("version") != 1:
        errors.append("top level: `version` must be 1")
    for key in ("global_invariants", "scenarios"):
        if not isinstance(doc.get(key), list) or not doc[key]:
            errors.append(f"top level: `{key}` must be a non-empty list")
    seen = set()
    for index, sc in enumerate(doc.get("scenarios") or []):
        label = sc.get("id") if isinstance(sc, dict) else f"#{index}"
        if not isinstance(sc, dict):
            errors.append(f"scenario {label}: not a mapping")
            continue
        for key in REQUIRED_KEYS:
            if key not in sc:
                errors.append(f"scenario {label}: missing `{key}`")
        if sc.get("id") in seen:
            errors.append(f"scenario {label}: duplicate id")
        seen.add(sc.get("id"))
        if not isinstance(sc.get("should_trigger"), bool):
            errors.append(f"scenario {label}: `should_trigger` must be true/false")
        mode = sc.get("expected_mode")
        if mode not in VALID_MODES:
            errors.append(f"scenario {label}: `expected_mode` must be one of {sorted(VALID_MODES)}")
        if sc.get("should_trigger") is False and mode != "none":
            errors.append(f"scenario {label}: non-triggering scenario must have expected_mode `none`")
        if sc.get("should_trigger") is True and mode == "none":
            errors.append(f"scenario {label}: triggering scenario needs a real mode")
        files = sc.get("expected_files")
        if not isinstance(files, dict) or set(files) != {"must_include", "must_not_include"}:
            errors.append(f"scenario {label}: `expected_files` needs exactly must_include and must_not_include")
            continue
        include = files["must_include"] or []
        exclude = files["must_not_include"] or []
        if sc.get("should_trigger") is False and include:
            errors.append(f"scenario {label}: non-triggering scenario must not require any file")
        for path in list(include) + list(exclude):
            if not os.path.exists(os.path.join(REPO, path)):
                errors.append(f"scenario {label}: `{path}` does not exist in the repo")
        for path in include:
            if path in exclude:
                errors.append(f"scenario {label}: `{path}` is both required and forbidden")
        if len(include) > 3:
            errors.append(f"scenario {label}: must_include exceeds the 2-3 file budget in SKILL.md")
        if not sc.get("assertions"):
            errors.append(f"scenario {label}: needs at least one assertion")
    return errors


# --------------------------------------------------------------------- display


def show(sc, full=False):
    trigger = "TRIGGER" if sc["should_trigger"] else "NO-TRIGGER"
    print(f"\n[{sc['id']}]  {trigger} / mode={sc['expected_mode']}")
    print(f"  prompt: {sc['prompt']}")
    include = sc["expected_files"]["must_include"] or []
    exclude = sc["expected_files"]["must_not_include"] or []
    print(f"  must read:     {', '.join(include) if include else '(none specified)'}")
    print(f"  must not read: {', '.join(exclude) if exclude else '(none specified)'}")
    for assertion in sc["assertions"]:
        print(f"    - {assertion}")
    if full:
        print(f"  rationale: {sc['rationale']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="validate only")
    parser.add_argument("--id", help="print a single scenario in full")
    args = parser.parse_args()

    doc = load(DATA)
    description = skill_description()
    errors = validate(doc) + validate_description(description)
    if errors:
        print(f"FAIL — {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    scenarios = doc["scenarios"]
    print(f"OK — {len(scenarios)} scenarios, schema valid, all referenced files exist.")
    print(
        f"     SKILL.md description: {len(description)}/{DESCRIPTION_BUDGET} chars "
        f"({DESCRIPTION_BUDGET - len(description)} of budget left, ceiling {DESCRIPTION_CEILING})."
    )
    if args.quiet:
        return 0

    if args.id:
        match = [s for s in scenarios if s["id"] == args.id]
        if not match:
            print(f"no scenario with id `{args.id}`", file=sys.stderr)
            return 1
        show(match[0], full=True)
        return 0

    print("\nGlobal invariants (apply to every triggering scenario):")
    for invariant in doc["global_invariants"]:
        print(f"  - {invariant}")
    for sc in scenarios:
        show(sc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
