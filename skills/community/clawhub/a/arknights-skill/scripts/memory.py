#!/usr/bin/env python3
"""Manage the local Arknights doctor profile for arknights-skill."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
PROFILE_FILE_NAME = "doctor-profile.json"
MAX_FACT_TEXT_LENGTH = 240


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def memory_dir() -> Path:
    configured = os.environ.get("ARKNIGHTS_MEMORY_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path("~/.config/arknights-skill").expanduser().resolve()


def profile_path() -> Path:
    return memory_dir() / PROFILE_FILE_NAME


def migrate_legacy_if_needed() -> None:
    """One-time migration: copy data from old skill-relative path to new default."""
    if os.environ.get("ARKNIGHTS_MEMORY_DIR"):
        return
    legacy = skill_root() / ".arknights-memory" / PROFILE_FILE_NAME
    new_path = profile_path()
    if legacy.exists() and not new_path.exists():
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(legacy), str(new_path))
        (legacy.parent / ".migrated").write_text(
            f"Migrated to {new_path}\n", encoding="utf-8"
        )


def empty_profile(timestamp: str | None = None) -> dict[str, Any]:
    timestamp = timestamp or now_utc()
    return {
        "schema_version": SCHEMA_VERSION,
        "game": "Arknights",
        "metadata": {
            "created_at": timestamp,
            "updated_at": timestamp,
        },
        "doctor": {
            "name": None,
            "server": None,
            "level": None,
            "uid": None,
        },
        "account": {
            "progress": {},
            "resources": {},
            "goals": [],
            "preferences": [],
        },
        "operators": {},
        "pending_confirmations": [],
    }


def normalize_profile(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Profile must be a JSON object.")

    profile = empty_profile()
    for key in ("schema_version", "game", "metadata", "doctor", "account", "operators", "pending_confirmations"):
        if key in data:
            profile[key] = data[key]

    if profile["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schema_version: {profile['schema_version']}")

    if not isinstance(profile.get("metadata"), dict):
        profile["metadata"] = {}
    profile["metadata"].setdefault("created_at", now_utc())
    profile["metadata"].setdefault("updated_at", profile["metadata"]["created_at"])

    if not isinstance(profile.get("doctor"), dict):
        profile["doctor"] = {}
    for key in ("name", "server", "level", "uid"):
        profile["doctor"].setdefault(key, None)

    if not isinstance(profile.get("account"), dict):
        profile["account"] = {}
    profile["account"].setdefault("progress", {})
    profile["account"].setdefault("resources", {})
    profile["account"].setdefault("goals", [])
    profile["account"].setdefault("preferences", [])

    if not isinstance(profile.get("operators"), dict):
        profile["operators"] = {}
    if not isinstance(profile.get("pending_confirmations"), list):
        profile["pending_confirmations"] = []

    return profile


def load_profile() -> tuple[dict[str, Any], bool]:
    path = profile_path()
    if not path.exists():
        return empty_profile(), True
    with path.open("r", encoding="utf-8") as handle:
        return normalize_profile(json.load(handle)), False


def save_profile(profile: dict[str, Any], *, touch_updated_at: bool = True) -> None:
    if touch_updated_at:
        profile["metadata"]["updated_at"] = now_utc()

    path = profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=".doctor-profile.",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(profile, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def clean_fact_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    # Reject any line break form so profile facts stay compact across platforms.
    if "\n" in text or "\r" in text or len(text) > MAX_FACT_TEXT_LENGTH:
        raise ValueError(f"{field} must be a concise single factual note, not raw dialogue.")
    return text


def to_int(value: Any, field: str) -> int | None:
    if value is None or value == "":
        return None
    # bool is an int subclass in Python, but profile progression fields must be numeric facts.
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer.")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer.") from exc


def add_pending(
    profile: dict[str, Any],
    field: str,
    current: Any,
    incoming: Any,
    reason: str,
    timestamp: str,
) -> bool:
    item = {
        "field": field,
        "current": current,
        "incoming": incoming,
        "reason": reason,
        "observed_at": timestamp,
    }
    for existing in profile["pending_confirmations"]:
        if (
            existing.get("field") == field
            and existing.get("current") == current
            and existing.get("incoming") == incoming
        ):
            # A repeated confirmation request should not refresh metadata.
            return False
    profile["pending_confirmations"].append(item)
    return True


def merge_text_scalar(
    profile: dict[str, Any],
    target: dict[str, Any],
    key: str,
    incoming: Any,
    field: str,
    timestamp: str,
) -> bool:
    value = clean_fact_text(incoming, field)
    if value is None:
        return False
    current = target.get(key)
    if current in (None, ""):
        target[key] = value
        return True
    if current == value:
        return False
    return add_pending(profile, field, current, value, "conflicting explicit facts", timestamp)


def merge_monotonic_int(
    profile: dict[str, Any],
    target: dict[str, Any],
    key: str,
    incoming: Any,
    field: str,
    timestamp: str,
    *,
    min_value: int | None = None,
    max_value: int | None = None,
) -> bool:
    value = to_int(incoming, field)
    if value is None:
        return False
    if min_value is not None and value < min_value:
        raise ValueError(f"{field} must be >= {min_value}.")
    if max_value is not None and value > max_value:
        raise ValueError(f"{field} must be <= {max_value}.")

    current = target.get(key)
    if current in (None, ""):
        target[key] = value
        return True

    current_int = to_int(current, field)
    if current_int is None or value > current_int:
        target[key] = value
        return True
    if value == current_int:
        return False

    return add_pending(profile, field, current, value, "incoming value is lower than stored progression", timestamp)


def append_unique_text(target: list[Any], incoming: Any, field: str) -> bool:
    values = incoming if isinstance(incoming, list) else [incoming]
    changed = False
    for raw_value in values:
        value = clean_fact_text(raw_value, field)
        if value is not None and value not in target:
            target.append(value)
            changed = True
    return changed


def default_operator(timestamp: str) -> dict[str, Any]:
    return {
        "owned": None,
        "elite": None,
        "level": None,
        "potential": None,
        "skill_level": None,
        "masteries": {},
        "modules": {},
        "notes": [],
        "updated_at": timestamp,
    }


def normalize_operator(data: Any, timestamp: str) -> dict[str, Any]:
    operator = default_operator(timestamp)
    if isinstance(data, dict):
        operator.update(data)
    if not isinstance(operator.get("masteries"), dict):
        operator["masteries"] = {}
    if not isinstance(operator.get("modules"), dict):
        operator["modules"] = {}
    if not isinstance(operator.get("notes"), list):
        operator["notes"] = []
    return operator


def merge_owned(profile: dict[str, Any], operator: dict[str, Any], incoming: Any, field: str, timestamp: str) -> bool:
    if incoming is None:
        return False
    if not isinstance(incoming, bool):
        raise ValueError(f"{field} must be true or false.")

    current = operator.get("owned")
    if current is None:
        operator["owned"] = incoming
        return True
    if current == incoming:
        return False
    if current is False and incoming is True:
        operator["owned"] = True
        return True

    return add_pending(profile, field, current, incoming, "owned status conflicts with stored profile", timestamp)


def merge_elite_and_level(
    profile: dict[str, Any],
    operator: dict[str, Any],
    patch: dict[str, Any],
    field_prefix: str,
    timestamp: str,
) -> bool:
    changed = False
    has_elite = "elite" in patch
    has_level = "level" in patch
    incoming_elite = to_int(patch.get("elite"), f"{field_prefix}.elite") if has_elite else None
    incoming_level = to_int(patch.get("level"), f"{field_prefix}.level") if has_level else None

    if incoming_elite is not None and not 0 <= incoming_elite <= 2:
        raise ValueError(f"{field_prefix}.elite must be between 0 and 2.")
    if incoming_level is not None and incoming_level < 1:
        raise ValueError(f"{field_prefix}.level must be >= 1.")

    current_elite = to_int(operator.get("elite"), f"{field_prefix}.elite")
    current_level = to_int(operator.get("level"), f"{field_prefix}.level")

    if has_elite and incoming_elite is not None:
        if current_elite is None or incoming_elite > current_elite:
            operator["elite"] = incoming_elite
            changed = True
            if incoming_level is not None:
                operator["level"] = incoming_level
                changed = True
            return changed
        if incoming_elite < current_elite:
            changed = add_pending(
                profile, f"{field_prefix}.elite", current_elite, incoming_elite, "incoming elite is lower", timestamp,
            ) or changed
            if incoming_level is not None:
                changed = add_pending(
                    profile, f"{field_prefix}.level", current_level, incoming_level,
                    "incoming level belongs to lower elite", timestamp,
                ) or changed
            return changed

    if has_level and incoming_level is not None:
        if current_level is None:
            operator["level"] = incoming_level
            return True
        if incoming_level > current_level:
            operator["level"] = incoming_level
            return True
        if incoming_level < current_level:
            return add_pending(
                profile, f"{field_prefix}.level", current_level, incoming_level, "incoming level is lower", timestamp,
            )

    return changed


def merge_masteries(
    profile: dict[str, Any], operator: dict[str, Any], incoming: Any, field_prefix: str, timestamp: str,
) -> bool:
    if not isinstance(incoming, dict):
        raise ValueError(f"{field_prefix}.masteries must be an object.")
    changed = False
    for skill_id, mastery in incoming.items():
        skill_key = str(skill_id)
        changed = merge_monotonic_int(
            profile,
            operator["masteries"],
            skill_key,
            mastery,
            f"{field_prefix}.masteries.{skill_key}",
            timestamp,
            min_value=0,
            max_value=3,
        ) or changed
    return changed


def merge_legacy_skills(
    profile: dict[str, Any], operator: dict[str, Any], incoming: Any, field_prefix: str, timestamp: str,
) -> bool:
    if not isinstance(incoming, dict):
        raise ValueError(f"{field_prefix}.skills must be an object.")
    changed = False
    for skill_id, value in incoming.items():
        if isinstance(value, dict):
            if "mastery" in value:
                mastery = value["mastery"]
            elif "mastery_level" in value:
                mastery = value["mastery_level"]
            else:
                continue
        else:
            mastery = value
        skill_key = str(skill_id)
        changed = merge_monotonic_int(
            profile,
            operator["masteries"],
            skill_key,
            mastery,
            f"{field_prefix}.masteries.{skill_key}",
            timestamp,
            min_value=0,
            max_value=3,
        ) or changed
    return changed


def merge_modules(
    profile: dict[str, Any], operator: dict[str, Any], incoming: Any, field_prefix: str, timestamp: str,
) -> bool:
    if not isinstance(incoming, dict):
        raise ValueError(f"{field_prefix}.modules must be an object.")
    changed = False
    for module_id, value in incoming.items():
        module_key = str(module_id)
        stage = value.get("stage") if isinstance(value, dict) else value
        changed = merge_monotonic_int(
            profile,
            operator["modules"],
            module_key,
            stage,
            f"{field_prefix}.modules.{module_key}",
            timestamp,
            min_value=0,
            max_value=3,
        ) or changed
    return changed


def merge_operator(profile: dict[str, Any], name: str, patch: Any, timestamp: str) -> bool:
    if not isinstance(patch, dict):
        raise ValueError(f"operators.{name} must be an object.")

    operator_name = clean_fact_text(name, "operator name")
    if operator_name is None:
        return False

    operators = profile["operators"]
    operator = normalize_operator(operators.get(operator_name), timestamp)
    changed = False
    field_prefix = f"operators.{operator_name}"

    if "owned" in patch:
        changed = merge_owned(profile, operator, patch["owned"], f"{field_prefix}.owned", timestamp) or changed
    if "elite" in patch or "level" in patch:
        changed = merge_elite_and_level(profile, operator, patch, field_prefix, timestamp) or changed
    if "potential" in patch:
        changed = merge_monotonic_int(
            profile,
            operator,
            "potential",
            patch["potential"],
            f"{field_prefix}.potential",
            timestamp,
            min_value=0,
            max_value=6,
        ) or changed
    if "skill_level" in patch:
        changed = merge_monotonic_int(
            profile,
            operator,
            "skill_level",
            patch["skill_level"],
            f"{field_prefix}.skill_level",
            timestamp,
            min_value=1,
            max_value=7,
        ) or changed
    if "masteries" in patch:
        changed = merge_masteries(profile, operator, patch["masteries"], field_prefix, timestamp) or changed
    if "skills" in patch:
        changed = merge_legacy_skills(profile, operator, patch["skills"], field_prefix, timestamp) or changed
    if "modules" in patch:
        changed = merge_modules(profile, operator, patch["modules"], field_prefix, timestamp) or changed
    if "notes" in patch:
        changed = append_unique_text(operator["notes"], patch["notes"], f"{field_prefix}.notes") or changed

    if changed:
        operator["updated_at"] = timestamp
        operators[operator_name] = operator
    return changed


def merge_mapping_latest(
    profile: dict[str, Any],
    target: dict[str, Any],
    incoming: Any,
    field: str,
    timestamp: str,
    *,
    numeric_strategy: str = "monotonic",
) -> bool:
    if not isinstance(incoming, dict):
        raise ValueError(f"{field} must be an object.")
    if numeric_strategy not in {"monotonic", "latest"}:
        raise ValueError(f"Unsupported numeric merge strategy: {numeric_strategy}")
    changed = False
    for raw_key, raw_value in incoming.items():
        key = clean_fact_text(raw_key, f"{field} key")
        if key is None or raw_value in (None, ""):
            continue
        sub_field = f"{field}.{key}"
        if isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool):
            if numeric_strategy == "monotonic":
                changed = merge_monotonic_int(
                    profile, target, key, raw_value, sub_field, timestamp,
                ) or changed
            elif target.get(key) != raw_value:
                target[key] = raw_value
                changed = True
        elif isinstance(raw_value, str):
            value: Any = clean_fact_text(raw_value, sub_field)
            if target.get(key) != value:
                target[key] = value
                changed = True
        elif isinstance(raw_value, bool):
            if target.get(key) != raw_value:
                target[key] = raw_value
                changed = True
        else:
            raise ValueError(f"{sub_field} must be a concise string, number, or boolean.")
    return changed


def apply_patch(profile: dict[str, Any], patch: Any) -> dict[str, Any]:
    if not isinstance(patch, dict):
        raise ValueError("Patch must be a JSON object.")

    timestamp = now_utc()
    updated = deepcopy(profile)
    changed = False

    doctor_patch = patch.get("doctor")
    if doctor_patch is not None:
        if not isinstance(doctor_patch, dict):
            raise ValueError("doctor must be an object.")
        if "name" in doctor_patch:
            changed = merge_text_scalar(
                updated, updated["doctor"], "name", doctor_patch["name"], "doctor.name", timestamp,
            ) or changed
        if "server" in doctor_patch:
            changed = merge_text_scalar(
                updated, updated["doctor"], "server", doctor_patch["server"], "doctor.server", timestamp,
            ) or changed
        if "uid" in doctor_patch:
            changed = merge_text_scalar(
                updated, updated["doctor"], "uid", doctor_patch["uid"], "doctor.uid", timestamp,
            ) or changed
        if "level" in doctor_patch:
            changed = merge_monotonic_int(
                updated,
                updated["doctor"],
                "level",
                doctor_patch["level"],
                "doctor.level",
                timestamp,
                min_value=1,
            ) or changed

    account_patch = patch.get("account")
    if account_patch is not None:
        if not isinstance(account_patch, dict):
            raise ValueError("account must be an object.")
        if "progress" in account_patch:
            changed = merge_mapping_latest(
                updated, updated["account"]["progress"], account_patch["progress"], "account.progress", timestamp,
            ) or changed
        if "resources" in account_patch:
            changed = merge_mapping_latest(
                updated,
                updated["account"]["resources"],
                account_patch["resources"],
                "account.resources",
                timestamp,
                numeric_strategy="latest",
            ) or changed
        if "goals" in account_patch:
            changed = append_unique_text(
                updated["account"]["goals"], account_patch["goals"], "account.goals",
            ) or changed
        if "preferences" in account_patch:
            changed = append_unique_text(
                updated["account"]["preferences"], account_patch["preferences"], "account.preferences",
            ) or changed

    operators_patch = patch.get("operators")
    if operators_patch is not None:
        if not isinstance(operators_patch, dict):
            raise ValueError("operators must be an object.")
        for name, operator_patch in operators_patch.items():
            changed = merge_operator(updated, name, operator_patch, timestamp) or changed

    if changed:
        updated["metadata"]["updated_at"] = timestamp
    return updated


def command_path(_: argparse.Namespace) -> int:
    print(profile_path())
    return 0


def command_read(_: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    print_json(profile)
    pending = profile.get("pending_confirmations", [])
    if pending:
        print(f"\n--- {len(pending)} pending confirmation(s) ---", file=sys.stderr)
        for p in pending:
            reason = p.get("reason", "")
            print(f"  - {p['field']}: {p.get('current')} -> {p.get('incoming')} ({reason})", file=sys.stderr)
    return 0


def _format_operator_summary(name: str, op: dict[str, Any], pending_fields: set[str]) -> str:
    """Format a single operator as a one-line summary."""
    owned = op.get("owned")
    status = "owned" if owned is True else ("not owned" if owned is False else "unknown")
    elite = op.get("elite")
    elite_str = f"E{elite}" if elite is not None else ""
    level = op.get("level")
    level_str = f"Lv{level}" if level is not None else ""

    masteries = op.get("masteries", {})
    mastery_parts = sorted(masteries.items())
    mastery_str = " ".join(f"S{k}:M{v}" for k, v in mastery_parts if v)

    modules = op.get("modules", {})
    module_count = sum(1 for v in modules.values() if v and v > 0)
    module_str = f"{module_count}mod" if module_count else ""

    pending_marker = " [pending]" if any(f.startswith(f"operators.{name}.") for f in pending_fields) else ""

    parts = [name, status]
    if elite_str:
        parts.append(elite_str)
    if level_str:
        parts.append(level_str)
    if mastery_str:
        parts.append(mastery_str)
    if module_str:
        parts.append(module_str)
    if pending_marker:
        parts.append(pending_marker)
    return " | ".join(parts)


def _matching_operators(profile: dict[str, Any], *, owned_only: bool, pending_only: bool) -> list[str]:
    """Return sorted operator names matching the given filters."""
    operators = profile.get("operators", {})
    pending_fields = {p["field"] for p in profile.get("pending_confirmations", [])}
    result = []
    for name, op in operators.items():
        if owned_only and op.get("owned") is not True:
            continue
        if pending_only and not any(f.startswith(f"operators.{name}.") for f in pending_fields):
            continue
        result.append(name)
    return sorted(result)


def command_list(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    pending_fields = {p["field"] for p in profile.get("pending_confirmations", [])}
    names = _matching_operators(profile, owned_only=args.owned, pending_only=args.has_pending)
    if not names:
        print("No operators recorded." if not args.owned else "No owned operators recorded.")
        return 0
    for name in names:
        print(_format_operator_summary(name, profile["operators"][name], pending_fields))
    return 0


def command_search(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    keyword = args.keyword.lower()
    operators = profile.get("operators", {})
    pending_fields = {p["field"] for p in profile.get("pending_confirmations", [])}
    matched = []
    for name, op in operators.items():
        if keyword in name.lower():
            matched.append((name, op))
            continue
        for note in op.get("notes", []):
            if keyword in str(note).lower():
                matched.append((name, op))
                break
    if not matched:
        print("No operators matched.")
        return 0
    for name, op in sorted(matched, key=lambda x: x[0]):
        print(_format_operator_summary(name, op, pending_fields))
    return 0


def command_delete_operator(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    name = args.name
    if name not in profile.get("operators", {}):
        print(f"No operator '{name}' found.", file=sys.stderr)
        return 1
    del profile["operators"][name]
    prefix = f"operators.{name}."
    profile["pending_confirmations"] = [
        p for p in profile.get("pending_confirmations", [])
        if not p.get("field", "").startswith(prefix)
    ]
    save_profile(profile)
    print(f"Deleted operator '{name}'.")
    return 0


def command_gc(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    dry_run = getattr(args, "dry_run", False)
    threshold = now_utc()
    cutoff_days = args.days

    kept = []
    removed = 0
    for item in profile.get("pending_confirmations", []):
        observed = item.get("observed_at", "")
        try:
            obs_dt = datetime.fromisoformat(observed.replace("Z", "+00:00"))
            thr_dt = datetime.fromisoformat(threshold.replace("Z", "+00:00"))
            age = (thr_dt - obs_dt).days
        except (ValueError, TypeError):
            kept.append(item)
            continue
        if age > cutoff_days:
            removed += 1
        else:
            kept.append(item)

    if dry_run:
        print(f"Dry run: would remove {removed} stale pending confirmation(s).")
        return 0

    profile["pending_confirmations"] = kept
    save_profile(profile)
    print(f"Removed {removed} stale pending confirmation(s).")
    return 0


def command_update(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    patch = json.loads(args.patch_json)
    updated = apply_patch(profile, patch)
    dry_run = getattr(args, "dry_run", False)
    if dry_run:
        print_json(updated)
        return 0
    if updated != profile:
        save_profile(updated, touch_updated_at=False)
    print_json(updated)
    return 0


def _set_nested(profile: dict[str, Any], field: str, value: Any) -> None:
    """Set a value deep in the profile tree by dot-separated field path."""
    parts = field.split(".")
    current: Any = profile
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value


def command_confirm(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    field = args.field
    pending = profile.get("pending_confirmations", [])
    matches = [p for p in pending if p.get("field") == field]
    if not matches:
        print(f"No pending confirmation for field '{field}'.", file=sys.stderr)
        return 1
    item = matches[0]
    _set_nested(profile, item["field"], item["incoming"])
    profile["metadata"]["updated_at"] = now_utc()
    profile["pending_confirmations"] = [
        p for p in profile["pending_confirmations"]
        if not (p.get("field") == field and p.get("incoming") == item["incoming"])
    ]
    save_profile(profile, touch_updated_at=False)
    print(f"Applied pending value for '{field}': {item['incoming']}")
    return 0


def command_dismiss(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    field = args.field
    before = len(profile.get("pending_confirmations", []))
    profile["pending_confirmations"] = [
        p for p in profile["pending_confirmations"]
        if p.get("field") != field
    ]
    after = len(profile["pending_confirmations"])
    if before == after:
        print(f"No pending confirmation for field '{field}'.", file=sys.stderr)
        return 1
    save_profile(profile)
    print(f"Dismissed {before - after} pending confirmation(s) for '{field}'.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the local Arknights doctor profile.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    path_parser = subparsers.add_parser("path", help="Print the doctor profile path.")
    path_parser.set_defaults(func=command_path)

    read_parser = subparsers.add_parser("read", help="Read or initialize the doctor profile.")
    read_parser.set_defaults(func=command_read)

    update_parser = subparsers.add_parser("update", help="Merge a structured patch into the doctor profile.")
    update_parser.add_argument("--patch-json", required=True, help="Structured JSON facts to merge.")
    update_parser.add_argument("--dry-run", action="store_true", help="Preview merged result without saving.")
    update_parser.set_defaults(func=command_update)

    confirm_parser = subparsers.add_parser("confirm", help="Apply a pending confirmation.")
    confirm_parser.add_argument("--field", required=True, help="Field name of the pending confirmation.")
    confirm_parser.add_argument("--apply", action="store_true", required=True, help="Actually apply the pending value.")
    confirm_parser.set_defaults(func=command_confirm)

    dismiss_parser = subparsers.add_parser("dismiss", help="Discard a pending confirmation.")
    dismiss_parser.add_argument("--field", required=True, help="Field name of the pending confirmation.")
    dismiss_parser.set_defaults(func=command_dismiss)

    list_parser = subparsers.add_parser("list", help="List recorded operators.")
    list_parser.add_argument("--owned", action="store_true", help="Show only owned operators.")
    list_parser.add_argument(
        "--has-pending", action="store_true", help="Show only operators with pending confirmations."
    )
    list_parser.set_defaults(func=command_list)

    search_parser = subparsers.add_parser("search", help="Search operators by name or notes.")
    search_parser.add_argument("keyword", help="Search keyword (case-insensitive).")
    search_parser.set_defaults(func=command_search)

    delete_parser = subparsers.add_parser("delete-operator", help="Delete a recorded operator.")
    delete_parser.add_argument("name", help="Operator name to delete.")
    delete_parser.set_defaults(func=command_delete_operator)

    gc_parser = subparsers.add_parser("gc", help="Remove stale pending confirmations.")
    gc_parser.add_argument("--days", type=int, default=30, help="Remove entries older than N days (default: 30).")
    gc_parser.add_argument("--dry-run", action="store_true", help="Preview what would be removed.")
    gc_parser.set_defaults(func=command_gc)

    return parser


def main() -> int:
    migrate_legacy_if_needed()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"memory.py: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
