#!/usr/bin/env python3
"""Manage the local Don't Starve survivor profile for dont-starve-skill."""

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
PROFILE_FILE_NAME = "survivor-profile.json"
MAX_FACT_TEXT_LENGTH = 240

GAME_VERSIONS = {"DS", "DST", "SW", "HAM"}
PLAY_STYLES = {"casual", "survival", "speedrun"}
EXPERIENCE_LEVELS = {"beginner", "intermediate", "veteran"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def memory_dir() -> Path:
    configured = os.environ.get("DONTSTARVE_MEMORY_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path("~/.config/dont-starve-skill").expanduser().resolve()


def profile_path() -> Path:
    return memory_dir() / PROFILE_FILE_NAME


def migrate_legacy_if_needed() -> None:
    if os.environ.get("DONTSTARVE_MEMORY_DIR"):
        return
    legacy = skill_root() / ".dontstarve-memory" / PROFILE_FILE_NAME
    new_path = profile_path()
    if legacy.exists() and not new_path.exists():
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(legacy), str(new_path))
        (legacy.parent / ".migrated").write_text(f"Migrated to {new_path}\n", encoding="utf-8")


def empty_profile(timestamp: str | None = None) -> dict[str, Any]:
    timestamp = timestamp or now_utc()
    return {
        "schema_version": SCHEMA_VERSION,
        "game": "Don't Starve",
        "metadata": {
            "created_at": timestamp,
            "updated_at": timestamp,
        },
        "survivor": {
            "name": None,
            "game_version": None,
            "play_style": None,
            "experience": None,
        },
        "world": {
            "settings": {},
            "season_day": None,
            "current_season": None,
        },
        "progress": {
            "bosses_defeated": [],
            "ruins_explored": False,
            "adventure_mode": None,
            "milestones": [],
        },
        "characters": {},
        "preferences": [],
        "pending_confirmations": [],
    }


def normalize_profile(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Profile must be a JSON object.")

    profile = empty_profile()
    for key in (
        "schema_version",
        "game",
        "metadata",
        "survivor",
        "world",
        "progress",
        "characters",
        "preferences",
        "pending_confirmations",
    ):
        if key in data:
            profile[key] = data[key]

    if profile["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schema_version: {profile['schema_version']}")

    if not isinstance(profile.get("metadata"), dict):
        profile["metadata"] = {}
    profile["metadata"].setdefault("created_at", now_utc())
    profile["metadata"].setdefault("updated_at", profile["metadata"]["created_at"])

    if not isinstance(profile.get("survivor"), dict):
        profile["survivor"] = {}
    for key in ("name", "game_version", "play_style", "experience"):
        profile["survivor"].setdefault(key, None)

    if not isinstance(profile.get("world"), dict):
        profile["world"] = {}
    profile["world"].setdefault("settings", {})
    profile["world"].setdefault("season_day", None)
    profile["world"].setdefault("current_season", None)
    if not isinstance(profile["world"].get("settings"), dict):
        profile["world"]["settings"] = {}

    if not isinstance(profile.get("progress"), dict):
        profile["progress"] = {}
    progress = profile["progress"]
    progress.setdefault("bosses_defeated", [])
    progress.setdefault("ruins_explored", False)
    progress.setdefault("adventure_mode", None)
    progress.setdefault("milestones", [])
    if not isinstance(progress.get("bosses_defeated"), list):
        progress["bosses_defeated"] = []
    if not isinstance(progress.get("milestones"), list):
        progress["milestones"] = []

    if not isinstance(profile.get("characters"), dict):
        profile["characters"] = {}
    if not isinstance(profile.get("preferences"), list):
        profile["preferences"] = []
    if not isinstance(profile.get("pending_confirmations"), list):
        profile["pending_confirmations"] = []

    return profile


def load_profile() -> tuple[dict[str, Any], bool]:
    path = profile_path()
    if not path.exists():
        return empty_profile(), True
    with path.open("r", encoding="utf-8") as handle:
        return normalize_profile(json.load(handle)), False


def save_profile(
    profile: dict[str, Any],
    *,
    touch_updated_at: bool = True,
) -> None:
    if touch_updated_at:
        profile["metadata"]["updated_at"] = now_utc()

    path = profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_name = tempfile.mkstemp(
        prefix=".survivor-profile.",
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
    if "\n" in text or "\r" in text or len(text) > MAX_FACT_TEXT_LENGTH:
        raise ValueError(f"{field} must be a concise single factual note, not raw dialogue.")
    return text


def to_int(value: Any, field: str) -> int | None:
    if value is None or value == "":
        return None
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
) -> None:
    for existing in profile["pending_confirmations"]:
        if (
            existing.get("field") == field
            and existing.get("current") == current
            and existing.get("incoming") == incoming
        ):
            return
    profile["pending_confirmations"].append({
        "field": field,
        "current": current,
        "incoming": incoming,
        "reason": reason,
        "observed_at": timestamp,
    })


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
    add_pending(profile, field, current, value, "conflicting explicit facts", timestamp)
    return True


def merge_enum_scalar(
    profile: dict[str, Any],
    target: dict[str, Any],
    key: str,
    incoming: Any,
    field: str,
    timestamp: str,
    allowed: set[str],
) -> bool:
    value = clean_fact_text(incoming, field)
    if value is None:
        return False
    if value not in allowed:
        raise ValueError(f"{field} must be one of: {', '.join(sorted(allowed))}.")
    return merge_text_scalar(profile, target, key, value, field, timestamp)


def merge_int_scalar(
    profile: dict[str, Any],
    target: dict[str, Any],
    key: str,
    incoming: Any,
    field: str,
    timestamp: str,
    *,
    min_value: int | None = None,
) -> bool:
    value = to_int(incoming, field)
    if value is None:
        return False
    if min_value is not None and value < min_value:
        raise ValueError(f"{field} must be >= {min_value}.")
    current = target.get(key)
    if current in (None, ""):
        target[key] = value
        return True
    if current == value:
        return False
    add_pending(profile, field, current, value, "conflicting explicit facts", timestamp)
    return True


def merge_bool_upgrade(
    profile: dict[str, Any],
    target: dict[str, Any],
    key: str,
    incoming: Any,
    field: str,
    timestamp: str,
) -> bool:
    if incoming is None:
        return False
    if not isinstance(incoming, bool):
        raise ValueError(f"{field} must be true or false.")
    current = target.get(key)
    if current is None:
        target[key] = incoming
        return True
    if current == incoming:
        return False
    if current is False and incoming is True:
        target[key] = True
        return True
    add_pending(
        profile, field, current, incoming,
        "incoming boolean would downgrade stored progress", timestamp,
    )
    return True


def merge_bool_scalar(
    target: dict[str, Any],
    key: str,
    incoming: Any,
    field: str,
) -> bool:
    if incoming is None:
        return False
    if not isinstance(incoming, bool):
        raise ValueError(f"{field} must be true or false.")
    if target.get(key) == incoming:
        return False
    target[key] = incoming
    return True


def append_unique_text(
    target: list[Any],
    incoming: Any,
    field: str,
) -> bool:
    values = incoming if isinstance(incoming, list) else [incoming]
    changed = False
    for raw_value in values:
        value = clean_fact_text(raw_value, field)
        if value is not None and value not in target:
            target.append(value)
            changed = True
    return changed


def merge_setting_value(
    target: dict[str, Any],
    key: str,
    raw_value: Any,
    field: str,
) -> bool:
    if raw_value in (None, ""):
        return False
    if isinstance(raw_value, bool):
        value: Any = raw_value
    elif isinstance(raw_value, (int, float)):
        value = raw_value
    elif isinstance(raw_value, str):
        value = clean_fact_text(raw_value, field)
    else:
        raise ValueError(f"{field} must be a concise string, number, or boolean.")
    if target.get(key) != value:
        target[key] = value
        return True
    return False


def merge_world(
    profile: dict[str, Any],
    world: dict[str, Any],
    patch: dict[str, Any],
    timestamp: str,
) -> bool:
    if not isinstance(patch, dict):
        raise ValueError("world must be an object.")
    changed = False

    if "settings" in patch:
        settings = patch["settings"]
        if not isinstance(settings, dict):
            raise ValueError("world.settings must be an object.")
        for raw_key, raw_value in settings.items():
            key = clean_fact_text(raw_key, "world.settings key")
            if key is not None:
                changed = merge_setting_value(
                    world["settings"], key, raw_value, f"world.settings.{key}"
                ) or changed

    if "season_day" in patch:
        changed = merge_int_scalar(
            profile, world, "season_day",
            patch["season_day"], "world.season_day", timestamp, min_value=1,
        ) or changed

    if "current_season" in patch:
        changed = merge_text_scalar(
            profile, world, "current_season",
            patch["current_season"], "world.current_season", timestamp,
        ) or changed

    return changed


def default_character(timestamp: str) -> dict[str, Any]:
    return {
        "preferred": None,
        "roles": [],
        "notes": [],
        "updated_at": timestamp,
    }


def normalize_character(data: Any, timestamp: str) -> dict[str, Any]:
    character = default_character(timestamp)
    if isinstance(data, dict):
        character.update(data)
    if not isinstance(character.get("roles"), list):
        character["roles"] = []
    if not isinstance(character.get("notes"), list):
        character["notes"] = []
    return character


def merge_character(
    profile: dict[str, Any],
    name: str,
    patch: dict[str, Any],
    timestamp: str,
) -> bool:
    if not isinstance(patch, dict):
        raise ValueError(f"characters.{name} must be an object.")
    character_name = clean_fact_text(name, "character name")
    if character_name is None:
        return False

    character = normalize_character(
        profile["characters"].get(character_name), timestamp
    )
    changed = False
    field_prefix = f"characters.{character_name}"

    if "preferred" in patch:
        changed = merge_bool_scalar(
            character, "preferred", patch["preferred"],
            f"{field_prefix}.preferred",
        ) or changed
    if "roles" in patch:
        changed = append_unique_text(
            character["roles"], patch["roles"], f"{field_prefix}.roles",
        ) or changed
    if "notes" in patch:
        changed = append_unique_text(
            character["notes"], patch["notes"], f"{field_prefix}.notes",
        ) or changed

    if changed:
        character["updated_at"] = timestamp
        profile["characters"][character_name] = character
    return changed


def apply_patch(profile: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(patch, dict):
        raise ValueError("Patch must be a JSON object.")

    timestamp = now_utc()
    updated = normalize_profile(deepcopy(profile))
    changed = False

    survivor_patch = patch.get("survivor")
    if survivor_patch is not None:
        if not isinstance(survivor_patch, dict):
            raise ValueError("survivor must be an object.")
        if "name" in survivor_patch:
            changed = merge_text_scalar(
                updated, updated["survivor"], "name",
                survivor_patch["name"], "survivor.name", timestamp,
            ) or changed
        if "game_version" in survivor_patch:
            changed = merge_enum_scalar(
                updated, updated["survivor"], "game_version",
                survivor_patch["game_version"], "survivor.game_version",
                timestamp, GAME_VERSIONS,
            ) or changed
        if "play_style" in survivor_patch:
            changed = merge_enum_scalar(
                updated, updated["survivor"], "play_style",
                survivor_patch["play_style"], "survivor.play_style",
                timestamp, PLAY_STYLES,
            ) or changed
        if "experience" in survivor_patch:
            changed = merge_enum_scalar(
                updated, updated["survivor"], "experience",
                survivor_patch["experience"], "survivor.experience",
                timestamp, EXPERIENCE_LEVELS,
            ) or changed

    if "world" in patch:
        changed = merge_world(updated, updated["world"], patch["world"], timestamp) or changed

    progress_patch = patch.get("progress")
    if progress_patch is not None:
        if not isinstance(progress_patch, dict):
            raise ValueError("progress must be an object.")
        if "bosses_defeated" in progress_patch:
            changed = append_unique_text(
                updated["progress"]["bosses_defeated"],
                progress_patch["bosses_defeated"],
                "progress.bosses_defeated",
            ) or changed
        if "ruins_explored" in progress_patch:
            changed = merge_bool_upgrade(
                updated, updated["progress"], "ruins_explored",
                progress_patch["ruins_explored"],
                "progress.ruins_explored", timestamp,
            ) or changed
        if "adventure_mode" in progress_patch:
            changed = merge_text_scalar(
                updated, updated["progress"], "adventure_mode",
                progress_patch["adventure_mode"],
                "progress.adventure_mode", timestamp,
            ) or changed
        if "milestones" in progress_patch:
            changed = append_unique_text(
                updated["progress"]["milestones"],
                progress_patch["milestones"], "progress.milestones",
            ) or changed

    characters_patch = patch.get("characters")
    if characters_patch is not None:
        if not isinstance(characters_patch, dict):
            raise ValueError("characters must be an object.")
        for name, character_patch in characters_patch.items():
            changed = merge_character(updated, name, character_patch, timestamp) or changed

    if "preferences" in patch:
        changed = append_unique_text(
            updated["preferences"], patch["preferences"], "preferences",
        ) or changed

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
        print(
            f"\n--- {len(pending)} pending confirmation(s) ---",
            file=sys.stderr,
        )
        for item in pending:
            print(
                f"  - {item['field']}: "
                f"{item.get('current')!r} -> {item.get('incoming')!r} "
                f"({item.get('reason', '')})",
                file=sys.stderr,
            )
    return 0


def command_update(args: argparse.Namespace) -> int:
    profile, created = load_profile()
    if created:
        save_profile(profile, touch_updated_at=False)
    patch = json.loads(args.patch_json)
    updated = apply_patch(profile, patch)
    save_profile(updated, touch_updated_at=False)
    print_json(updated)
    return 0


def _set_nested(profile: dict[str, Any], field: str, value: Any) -> None:
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
    matches = [item for item in pending if item.get("field") == field]
    if not matches:
        print(f"No pending confirmation for field '{field}'.", file=sys.stderr)
        return 1
    item = matches[0]
    _set_nested(profile, item["field"], item["incoming"])
    profile["metadata"]["updated_at"] = now_utc()
    profile["pending_confirmations"] = [
        current for current in profile["pending_confirmations"]
        if not (
            current.get("field") == field
            and current.get("incoming") == item["incoming"]
        )
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
        item for item in profile["pending_confirmations"]
        if item.get("field") != field
    ]
    after = len(profile["pending_confirmations"])
    if before == after:
        print(f"No pending confirmation for field '{field}'.", file=sys.stderr)
        return 1
    save_profile(profile)
    print(f"Dismissed {before - after} pending confirmation(s) for '{field}'.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the local Don't Starve survivor profile.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    path_parser = subparsers.add_parser("path", help="Print the survivor profile path.")
    path_parser.set_defaults(func=command_path)

    read_parser = subparsers.add_parser("read", help="Read or initialise the survivor profile.")
    read_parser.set_defaults(func=command_read)

    update_parser = subparsers.add_parser(
        "update", help="Merge a structured patch into the survivor profile.",
    )
    update_parser.add_argument(
        "--patch-json", required=True, help="Structured JSON facts to merge.",
    )
    update_parser.set_defaults(func=command_update)

    confirm_parser = subparsers.add_parser(
        "confirm", help="Apply a pending confirmation.",
    )
    confirm_parser.add_argument(
        "--field", required=True, help="Field name of the pending confirmation.",
    )
    confirm_parser.add_argument(
        "--apply", action="store_true", required=True, help="Actually apply the pending value.",
    )
    confirm_parser.set_defaults(func=command_confirm)

    dismiss_parser = subparsers.add_parser(
        "dismiss", help="Discard a pending confirmation.",
    )
    dismiss_parser.add_argument(
        "--field", required=True, help="Field name of the pending confirmation.",
    )
    dismiss_parser.set_defaults(func=command_dismiss)

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
