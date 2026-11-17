#!/usr/bin/env python3
"""
agent-caps — Agent Capability Manifest toolkit (zero-dependency).

Validates, generates, and cross-checks machine-readable capability manifests for
Hermes / OpenClaw / Paperclip-style AI agents. Implements the standard agent
interface defined in agents/registry.md so agents can be swapped safely.

Subcommands:
  validate   <manifest.json>        Validate a manifest against the schema.
  scaffold   <dir> [--name X]       Generate a manifest scaffold from a project dir.
  check-deps <manifest.json>...     Cross-check dependencies between agents.
  schema                           Print the JSON schema (for agents/tooling).

Exit codes: 0 = OK, 1 = validation error, 2 = usage error.

No third-party deps. Runs on Python 3.8+ (the low-RAM box's interpreter is fine).
"""
import argparse
import json
import os
import sys

SCHEMA_VERSION = "1.0.0"

# The canonical agent schema (mirrors agents/registry.md standard interface).
SCHEMA = {
    "type": "object",
    "required": ["name", "version", "capabilities", "dependencies",
                 "memory_requirements", "tools", "api", "status"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "version": {"type": "string", "pattern": r"^\d+\.\d+(\.\d+)?$"},
        "capabilities": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "dependencies": {"type": "array", "items": {"type": "string"}},
        "memory_requirements": {"type": "string"},
        "tools": {"type": "array", "items": {"type": "string"}},
        "api": {"type": "string"},
        "status": {"type": "string", "enum": ["active", "standby", "deprecated"]},
    },
}

VALID_STATUSES = SCHEMA["properties"]["status"]["enum"]


def _err(msg):
    print(f"ERROR: {msg}", file=sys.stderr)


def validate_manifest(doc):
    """Return (ok, list_of_errors). Pure logic, easy to unit-test."""
    errors = []
    if not isinstance(doc, dict):
        return False, ["manifest root must be a JSON object"]
    for field in SCHEMA["required"]:
        if field not in doc:
            errors.append(f"missing required field: {field}")
    props = SCHEMA["properties"]
    if "name" in doc and not isinstance(doc["name"], str):
        errors.append("name must be a string")
    if "version" in doc:
        import re
        if not re.match(props["version"]["pattern"], str(doc["version"])):
            errors.append(f"version '{doc['version']}' must match N.N or N.N.N")
    if "capabilities" in doc:
        if not isinstance(doc["capabilities"], list) or not doc["capabilities"]:
            errors.append("capabilities must be a non-empty array")
    if "status" in doc and doc["status"] not in VALID_STATUSES:
        errors.append(f"status must be one of {VALID_STATUSES}")
    if "tools" in doc and not isinstance(doc["tools"], list):
        errors.append("tools must be an array")
    if "dependencies" in doc and not isinstance(doc["dependencies"], list):
        errors.append("dependencies must be an array")
    return (len(errors) == 0, errors)


def cmd_validate(path):
    if not os.path.isfile(path):
        _err(f"file not found: {path}")
        return 2
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except json.JSONDecodeError as e:
        _err(f"invalid JSON in {path}: {e}")
        return 2
    ok, errors = validate_manifest(doc)
    if ok:
        print(f"OK: {doc.get('name')} v{doc.get('version')} ({doc.get('status')})")
        return 0
    for e in errors:
        print(f"  - {e}")
    return 1


def cmd_scaffold(directory, name=None):
    if not os.path.isdir(directory):
        _err(f"directory not found: {directory}")
        return 2
    base = name or os.path.basename(os.path.normpath(directory))
    # infer a few capabilities/tools from common files
    tools = []
    for marker, tool in [("README", "file"), ("package.json", "node"),
                         (".py", "python"), ("requirements.txt", "python"),
                         ("Dockerfile", "docker")]:
        if marker == ".py":
            if any(f.endswith(".py") for _, _, files in os.walk(directory) for f in files):
                tools.append("python")
        elif os.path.exists(os.path.join(directory, marker)):
            tools.append(tool)
    manifest = {
        "name": base,
        "version": "0.1.0",
        "capabilities": ["<describe what this agent does>"],
        "dependencies": [],
        "memory_requirements": "<e.g. 256MB>",
        "tools": tools or ["<list tools>"],
        "api": "<adapter or endpoint>",
        "status": "active",
    }
    out = os.path.join(directory, "agent-manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"scaffold written: {out}")
    return 0


def cmd_check_deps(paths):
    docs = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                docs.append(json.load(f))
        except Exception as e:
            _err(f"cannot read {p}: {e}")
            return 2
    # detect name collisions / version conflicts
    by_name = {}
    warnings = 0
    for d in docs:
        ok, errs = validate_manifest(d)
        if not ok:
            warnings += 1
            print(f"INVALID manifest {d.get('name','?')}: {errs}")
            continue
        n = d["name"]
        if n in by_name:
            warnings += 1
            print(f"WARN: duplicate agent name '{n}' "
                  f"(v{by_name[n]} vs v{d['version']})")
        by_name[n] = d["version"]
    # naive dependency resolution: every dependency should name a known agent
    known = set(by_name)
    for d in docs:
        for dep in d.get("dependencies", []):
            if dep not in known:
                warnings += 1
                print(f"WARN: {d['name']} depends on unknown agent '{dep}'")
    print(f"checked {len(docs)} manifest(s); {warnings} warning(s).")
    return 1 if warnings else 0


def cmd_schema():
    print(json.dumps({
        "schema_version": SCHEMA_VERSION,
        "fields": list(SCHEMA["required"]),
        "schema": SCHEMA,
    }, indent=2))
    return 0


def _self_test():
    """Real test of the core validation logic. Returns 0 on pass, 1 on fail."""
    good = {
        "name": "demo", "version": "1.0.0", "capabilities": ["x"],
        "dependencies": [], "memory_requirements": "256MB", "tools": ["python"],
        "api": "noop", "status": "active",
    }
    ok, errors = validate_manifest(good)
    if not ok:
        print("self-test: FAIL (valid manifest rejected)")
        print("  errors:", errors)
        return 1
    # A manifest missing required fields and with a bad status must be rejected.
    bad = {"name": 123, "status": "bogus"}
    ok2, errors2 = validate_manifest(bad)
    if ok2:
        print("self-test: FAIL (invalid manifest accepted)")
        return 1
    if "status" not in str(errors2):
        print("self-test: FAIL (status error not detected)")
        return 1
    print("self-test: PASS")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Agent Capability Manifest toolkit")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").add_argument("manifest")
    sc = sub.add_parser("scaffold")
    sc.add_argument("directory")
    sc.add_argument("--name", default=None)
    cd = sub.add_parser("check-deps")
    cd.add_argument("manifests", nargs="+")
    sub.add_parser("schema")
    sub.add_parser("self-test")
    args = p.parse_args(argv)

    if args.cmd == "validate":
        return cmd_validate(args.manifest)
    if args.cmd == "scaffold":
        return cmd_scaffold(args.directory, args.name)
    if args.cmd == "check-deps":
        return cmd_check_deps(args.manifests)
    if args.cmd == "schema":
        return cmd_schema()
    if args.cmd == "self-test":
        return _self_test()
    return 2


if __name__ == "__main__":
    sys.exit(main())
