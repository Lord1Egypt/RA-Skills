#!/usr/bin/env python3
"""Audit and optionally apply OpenClaw context-optimization defaults.

One command replaces multiple manual tool calls:
  python scripts/context_optimizer.py                     # audit only
  python scripts/context_optimizer.py --apply             # apply balanced defaults
  python scripts/context_optimizer.py --apply --aggressive # apply aggressive defaults

Automatically rolls back on validation failure.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

# Balanced defaults — good savings, safe recall quality
BALANCED_DEFAULTS: dict[str, Any] = {
    "agents.defaults.bootstrapMaxChars": 3000,
    "agents.defaults.bootstrapTotalMaxChars": 12000,
    "agents.defaults.imageMaxDimensionPx": 768,
    "agents.defaults.contextPruning.mode": "cache-ttl",
    "agents.defaults.contextPruning.ttl": "30m",
    "agents.defaults.contextPruning.keepLastAssistants": 3,
    "agents.defaults.contextPruning.minPrunableToolChars": 500,
    "agents.defaults.memorySearch.query.maxResults": 3,
    "agents.defaults.memorySearch.query.minScore": 0.75,
    "agents.defaults.memorySearch.query.hybrid.mmr.enabled": True,
    "agents.defaults.memorySearch.query.hybrid.mmr.lambda": 0.7,
    "agents.defaults.memorySearch.query.hybrid.temporalDecay.enabled": True,
    "agents.defaults.memorySearch.query.hybrid.temporalDecay.halfLifeDays": 14,
    "tools.web.search.maxResults": 3,
    "tools.web.fetch.maxCharsCap": 4000,
}

# Aggressive defaults — maximum savings, may need loosening
AGGRESSIVE_DEFAULTS: dict[str, Any] = {
    "agents.defaults.bootstrapMaxChars": 2500,
    "agents.defaults.bootstrapTotalMaxChars": 10000,
    "agents.defaults.imageMaxDimensionPx": 512,
    "agents.defaults.compaction.enabled": True,
    "agents.defaults.contextPruning.mode": "cache-ttl",
    "agents.defaults.contextPruning.ttl": "15m",
    "agents.defaults.contextPruning.keepLastAssistants": 2,
    "agents.defaults.contextPruning.minPrunableToolChars": 300,
    "agents.defaults.memorySearch.query.maxResults": 2,
    "agents.defaults.memorySearch.query.minScore": 0.8,
    "agents.defaults.memorySearch.query.hybrid.mmr.enabled": True,
    "agents.defaults.memorySearch.query.hybrid.mmr.lambda": 0.7,
    "agents.defaults.memorySearch.query.hybrid.temporalDecay.enabled": True,
    "agents.defaults.memorySearch.query.hybrid.temporalDecay.halfLifeDays": 7,
    "tools.web.search.maxResults": 2,
    "tools.web.fetch.maxCharsCap": 3000,
}


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def _extract_config_path(output: str) -> Path:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    for line in reversed(lines):
        if line.endswith(".json") or line.endswith(".jsonc"):
            return Path(line).expanduser()
    raise SystemExit("Could not determine config path from `openclaw config file`")


def discover_config_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    return _extract_config_path(_run(["openclaw", "config", "file"]))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_path(data: dict[str, Any], dotted: str) -> Any:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def set_path(data: dict[str, Any], dotted: str, value: Any) -> None:
    cur: dict[str, Any] = data
    parts = dotted.split(".")
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def audit(data: dict[str, Any]) -> list[str]:
    findings: list[str] = []

    # Missing keys
    required = {
        "agents.defaults.contextPruning.mode": "context pruning not configured",
        "agents.defaults.contextPruning.ttl": "context pruning TTL not set",
        "agents.defaults.memorySearch.query.maxResults": "memory maxResults not set",
        "agents.defaults.memorySearch.query.minScore": "memory minScore not set",
        "tools.web.search.maxResults": "web search maxResults not set",
        "tools.web.fetch.maxCharsCap": "web fetch maxCharsCap not set",
    }
    for dotted, msg in required.items():
        if get_path(data, dotted) is None:
            findings.append(f"MISSING  {msg}")

    # Wasteful values
    checks = [
        ("agents.defaults.memorySearch.query.maxResults", lambda v: isinstance(v, int) and v > 5,
         "memorySearch maxResults={} — injecting too many hits"),
        ("agents.defaults.memorySearch.query.minScore", lambda v: isinstance(v, (int, float)) and v < 0.65,
         "memorySearch minScore={} — allowing weak matches"),
        ("tools.web.search.maxResults", lambda v: isinstance(v, int) and v > 5,
         "web search maxResults={} — bloating tool output"),
        ("tools.web.fetch.maxCharsCap", lambda v: isinstance(v, int) and v > 8000,
         "web fetch maxCharsCap={} — large page fetches"),
        ("agents.defaults.imageMaxDimensionPx", lambda v: isinstance(v, int) and v > 1024,
         "imageMaxDimensionPx={} — high vision token cost"),
        ("agents.defaults.bootstrapTotalMaxChars", lambda v: isinstance(v, int) and v > 20000,
         "bootstrapTotalMaxChars={} — large bootstrap injection every turn"),
    ]
    for dotted, check_fn, msg_template in checks:
        val = get_path(data, dotted)
        if val is not None and check_fn(val):
            findings.append(f"WARN     {msg_template.format(val)}")

    # Missing recommended features
    if not get_path(data, "agents.defaults.memorySearch.query.hybrid.mmr.enabled"):
        findings.append("SUGGEST  enable MMR dedup for memory (hybrid.mmr.enabled)")
    if not get_path(data, "agents.defaults.memorySearch.query.hybrid.temporalDecay.enabled"):
        findings.append("SUGGEST  enable temporal decay for stale memory notes")

    if not findings:
        findings.append("OK       no issues detected")

    return findings


def apply_defaults(data: dict[str, Any], defaults: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    updated = deepcopy(data)
    changes: list[str] = []
    for dotted, value in defaults.items():
        current = get_path(updated, dotted)
        if current != value:
            old_display = repr(current) if current is not None else "(unset)"
            set_path(updated, dotted, value)
            changes.append(f"SET  {dotted}: {old_display} -> {value!r}")
    return updated, changes


def validate_config() -> tuple[bool, str]:
    proc = subprocess.run(
        ["openclaw", "config", "validate"],
        text=True, capture_output=True, check=False,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def print_snapshot(data: dict[str, Any]) -> None:
    keys = [
        "agents.defaults.bootstrapMaxChars",
        "agents.defaults.bootstrapTotalMaxChars",
        "agents.defaults.imageMaxDimensionPx",
        "agents.defaults.contextPruning",
        "agents.defaults.compaction",
        "agents.defaults.memorySearch.query.maxResults",
        "agents.defaults.memorySearch.query.minScore",
        "agents.defaults.memorySearch.query.hybrid.mmr.enabled",
        "agents.defaults.memorySearch.query.hybrid.temporalDecay.enabled",
        "tools.web.search.maxResults",
        "tools.web.fetch.maxCharsCap",
    ]
    print("\n=== Current Settings ===")
    for key in keys:
        val = get_path(data, key)
        print(f"  {key}: {val!r}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit and tune OpenClaw context settings.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s                     # audit only\n"
               "  %(prog)s --apply             # apply balanced defaults\n"
               "  %(prog)s --apply --aggressive # apply aggressive defaults\n",
    )
    parser.add_argument("--config", help="Path to openclaw.json (auto-detected if omitted)")
    parser.add_argument("--apply", action="store_true", help="Apply defaults and validate")
    parser.add_argument("--aggressive", action="store_true", help="Use aggressive defaults instead of balanced")
    args = parser.parse_args()

    config_path = discover_config_path(args.config)
    data = load_json(config_path)

    print(f"Config: {config_path}")
    print_snapshot(data)

    findings = audit(data)
    print("\n=== Audit ===")
    for f in findings:
        print(f"  {f}")

    if not args.apply:
        print("\nRun with --apply to fix issues, or --apply --aggressive for max savings.")
        return 0

    defaults = AGGRESSIVE_DEFAULTS if args.aggressive else BALANCED_DEFAULTS
    label = "aggressive" if args.aggressive else "balanced"
    updated, changes = apply_defaults(data, defaults)

    if not changes:
        print(f"\n=== Apply ({label}) ===")
        print("  Nothing to change — defaults already applied.")
        return 0

    # Write, validate, rollback on failure
    save_json(config_path, updated)
    ok, output = validate_config()

    if not ok:
        save_json(config_path, data)
        print(f"\n=== Apply ({label}) — FAILED ===")
        print("  Validation failed; reverted all changes.")
        if output:
            print(f"  {output}")
        return 1

    print(f"\n=== Applied ({label}) ===")
    for c in changes:
        print(f"  {c}")
    print("  Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
