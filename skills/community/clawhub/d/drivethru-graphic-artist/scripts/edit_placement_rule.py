#!/usr/bin/env python3
"""Safely mutate ``placement_rules.json`` at runtime.

The rules catalog is agent-owned — the agent learns new placements and
refines defaults from user feedback in chat and writes them back. All
edits go through this helper so they are schema-validated and written
atomically (tempfile + os.replace), and a bad edit can't corrupt the
catalog mid-write.

Edits are written to the editable working copy in the skill data dir
(``$MOCKUP_DATA_DIR`` or ``~/.drivethru/mockup``). On first edit the
copy is seeded from the catalog bundled with the skill, so the shipped
asset is never mutated. ``show`` reads the editable copy if it exists,
otherwise the bundled starter. Override the file with ``--rules``.

Subcommands:
    edit_placement_rule.py show [--category C] [--placement P]
    edit_placement_rule.py add <category> <placement> \
        --width-ratio F --x-center-ratio F --y-top-ratio F [--rotation-deg F]
    edit_placement_rule.py update <category> <placement> \
        [--width-ratio F] [--x-center-ratio F] [--y-top-ratio F] [--rotation-deg F]
    edit_placement_rule.py remove <category> <placement>

After any mutation the helper prints a JSON receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _paths  # noqa: E402


_SLUG_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_RATIO_BOUNDS = {
    "width_ratio": (0.01, 1.5),
    "x_center_ratio": (0.0, 1.0),
    "y_top_ratio": (0.0, 1.0),
    "rotation_deg": (-180.0, 180.0),
}


def _validate_slug(name: str, label: str) -> None:
    if not _SLUG_RE.match(name):
        raise SystemExit(
            f"ERROR: {label} '{name}' must be lowercase alphanumerics + underscores, "
            "starting with a letter (e.g. 'hoodie', 'full_front')."
        )


def _validate_rule(rule: dict) -> None:
    required = ("width_ratio", "x_center_ratio", "y_top_ratio")
    for key in required:
        if key not in rule:
            raise SystemExit(f"ERROR: rule missing required field '{key}'")
    for key, value in rule.items():
        if key not in _RATIO_BOUNDS:
            raise SystemExit(f"ERROR: unknown rule field '{key}'")
        lo, hi = _RATIO_BOUNDS[key]
        if not isinstance(value, (int, float)):
            raise SystemExit(f"ERROR: rule field '{key}' must be a number, got {type(value).__name__}")
        if not (lo <= float(value) <= hi):
            raise SystemExit(f"ERROR: rule field '{key}'={value} out of bounds [{lo}, {hi}]")


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: {path} is not valid JSON: {e}")
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: {path} top-level must be an object, got {type(data).__name__}")
    return data


def _write_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".placement_rules.", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise


def _cmd_show(rules: dict, category: str | None, placement: str | None) -> dict:
    if category is None:
        return rules
    bucket = rules.get(category, {})
    if placement is None:
        return {category: bucket}
    if placement not in bucket:
        raise SystemExit(f"ERROR: no rule for {category}/{placement}")
    return {category: {placement: bucket[placement]}}


def _cmd_add(rules: dict, category: str, placement: str, rule: dict) -> dict:
    _validate_slug(category, "category")
    _validate_slug(placement, "placement")
    _validate_rule(rule)
    bucket = rules.setdefault(category, {})
    if placement in bucket:
        raise SystemExit(
            f"ERROR: {category}/{placement} already exists. Use 'update' to modify it."
        )
    bucket[placement] = rule
    return rule


def _cmd_update(rules: dict, category: str, placement: str, patch: dict) -> dict:
    bucket = rules.get(category)
    if not isinstance(bucket, dict) or placement not in bucket:
        raise SystemExit(
            f"ERROR: {category}/{placement} does not exist. Use 'add' to create it."
        )
    merged = {**bucket[placement], **patch}
    _validate_rule(merged)
    bucket[placement] = merged
    return merged


def _cmd_remove(rules: dict, category: str, placement: str) -> dict:
    bucket = rules.get(category)
    if not isinstance(bucket, dict) or placement not in bucket:
        raise SystemExit(f"ERROR: {category}/{placement} does not exist")
    removed = bucket.pop(placement)
    if not bucket:
        rules.pop(category, None)
    return removed


def _rule_from_args(args) -> dict:
    rule = {
        "width_ratio": float(args.width_ratio),
        "x_center_ratio": float(args.x_center_ratio),
        "y_top_ratio": float(args.y_top_ratio),
        "rotation_deg": float(args.rotation_deg or 0.0),
    }
    return rule


def _patch_from_args(args) -> dict:
    patch: dict = {}
    if args.width_ratio is not None:
        patch["width_ratio"] = float(args.width_ratio)
    if args.x_center_ratio is not None:
        patch["x_center_ratio"] = float(args.x_center_ratio)
    if args.y_top_ratio is not None:
        patch["y_top_ratio"] = float(args.y_top_ratio)
    if args.rotation_deg is not None:
        patch["rotation_deg"] = float(args.rotation_deg)
    if not patch:
        raise SystemExit("ERROR: no fields to update. Pass at least one of --width-ratio / --x-center-ratio / --y-top-ratio / --rotation-deg.")
    return patch


def main() -> None:
    parser = argparse.ArgumentParser(description="Edit placement_rules.json")
    parser.add_argument(
        "--rules",
        default=None,
        help="Path to placement_rules.json (default: editable copy in the data dir)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    show = sub.add_parser("show", help="Print the rules (optionally filtered)")
    show.add_argument("--category", default=None)
    show.add_argument("--placement", default=None)

    add = sub.add_parser("add", help="Add a new rule")
    add.add_argument("category")
    add.add_argument("placement")
    add.add_argument("--width-ratio", type=float, required=True)
    add.add_argument("--x-center-ratio", type=float, required=True)
    add.add_argument("--y-top-ratio", type=float, required=True)
    add.add_argument("--rotation-deg", type=float, default=0.0)

    update = sub.add_parser("update", help="Update fields on an existing rule")
    update.add_argument("category")
    update.add_argument("placement")
    update.add_argument("--width-ratio", type=float, default=None)
    update.add_argument("--x-center-ratio", type=float, default=None)
    update.add_argument("--y-top-ratio", type=float, default=None)
    update.add_argument("--rotation-deg", type=float, default=None)

    remove = sub.add_parser("remove", help="Remove a rule")
    remove.add_argument("category")
    remove.add_argument("placement")

    args = parser.parse_args()

    if args.command == "show":
        # Read-only: prefer the editable copy, fall back to the bundled starter.
        rules_path = Path(args.rules) if args.rules else _paths.effective_rules_path()
        rules = _load(rules_path)
        print(json.dumps(_cmd_show(rules, args.category, args.placement), indent=2, sort_keys=True))
        return

    # Mutating commands: operate on the editable copy (seeded from bundled).
    rules_path = Path(args.rules) if args.rules else _paths.ensure_data_rules()
    rules = _load(rules_path)

    if args.command == "add":
        rule = _cmd_add(rules, args.category, args.placement, _rule_from_args(args))
        _write_atomic(rules_path, rules)
        print(json.dumps({"action": "add", "category": args.category, "placement": args.placement, "rule": rule, "rules_file": str(rules_path)}, indent=2))
        return

    if args.command == "update":
        merged = _cmd_update(rules, args.category, args.placement, _patch_from_args(args))
        _write_atomic(rules_path, rules)
        print(json.dumps({"action": "update", "category": args.category, "placement": args.placement, "rule": merged, "rules_file": str(rules_path)}, indent=2))
        return

    if args.command == "remove":
        removed = _cmd_remove(rules, args.category, args.placement)
        _write_atomic(rules_path, rules)
        print(json.dumps({"action": "remove", "category": args.category, "placement": args.placement, "removed": removed, "rules_file": str(rules_path)}, indent=2))
        return


if __name__ == "__main__":
    main()
