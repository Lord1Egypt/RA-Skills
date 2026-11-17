#!/usr/bin/env python3
"""Manage runtime configuration without modifying immutable skill defaults."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from auto_reply_permissions import (
    load_pending,
    load_permissions,
    migrate_legacy_memory_permissions,
)

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
DISCLOSURE = "This email is automatically processed by AI. If manual processing is required, please include the words 'requires manual processing' in your reply."
DEFAULTS = {
    "config": ASSETS_DIR / "default-config.json",
    "system-prompt": ASSETS_DIR / "default-system-prompt.md",
    "workflow": ASSETS_DIR / "default-workflow.md",
    "persona": ASSETS_DIR / "default-persona.md",
    "user-memory": ASSETS_DIR / "default-user-memory.md",
    "auto-reply-permissions": ASSETS_DIR / "default-auto-reply-permissions.json",
    "pending-category-confirmations": ASSETS_DIR
    / "default-pending-category-confirmations.json",
}
RUNTIME_NAMES = {
    "config": "config.json",
    "system-prompt": "system-prompt.md",
    "workflow": "workflow.md",
    "persona": "persona.md",
    "user-memory": "user_memory.md",
    "auto-reply-permissions": "auto_reply_permissions.json",
    "pending-category-confirmations": "pending_category_confirmations.json",
}


def require_explicit_owner_confirmation(args: argparse.Namespace) -> None:
    if not getattr(args, "confirm_owner_request", False):
        raise SystemExit(
            "This changes operator-owned runtime state. Confirm the current owner's request and rerun with --confirm-owner-request"
        )


def validate_iana_timezone(value: str) -> str:
    timezone_name = value.strip()
    if not timezone_name:
        raise SystemExit("Timezone must be a non-empty IANA timezone name")
    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise SystemExit(f"Unknown IANA timezone: {timezone_name}") from exc
    return timezone_name


def runtime_dir() -> Path:
    state_override = os.environ.get("OPENCLAW_STATE_DIR")
    state_root = (
        Path(state_override).expanduser()
        if state_override
        else Path.home() / ".openclaw"
    )
    return state_root / "ecommerce-gmail-customer-service"


def runtime_path(kind: str) -> Path:
    return runtime_dir() / RUNTIME_NAMES[kind]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = target.with_suffix(target.suffix + ".tmp")
    shutil.copyfile(source, temporary)
    os.chmod(temporary, 0o600)
    os.replace(temporary, target)


def atomic_json(path: Path, data: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def merge_missing(target: dict, defaults: dict) -> bool:
    """Add new safe defaults without replacing any configured value."""
    changed = False
    for key, value in defaults.items():
        if key not in target:
            target[key] = value
            changed = True
        elif isinstance(value, dict) and isinstance(target[key], dict):
            changed = merge_missing(target[key], value) or changed
    return changed


def upgrade_runtime_config() -> bool:
    config_path = runtime_path("config")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    defaults = json.loads(DEFAULTS["config"].read_text(encoding="utf-8"))
    previous_version = config.get("version")
    changed = merge_missing(config, defaults)
    if (
        isinstance(previous_version, int)
        and previous_version < defaults["version"]
    ):
        automation = config.setdefault("automation", {})
        if not isinstance(automation, dict):
            automation = {}
            config["automation"] = automation
        if previous_version < 4:
            # A legacy auto_send value had no owner-confirmation record or
            # per-playbook approval gate. Migration fails closed until the
            # owner explicitly enables the new category-based mode.
            if automation.get("send_mode") == "auto_send":
                automation["send_mode"] = "draft_only"
                automation["auto_send_confirmed_at"] = None
                changed = True
            if "auto_send_allowlist" in automation:
                automation.pop("auto_send_allowlist")
                changed = True
        if previous_version < 5:
            storefront = config.setdefault("storefront", {})
            if not isinstance(storefront, dict):
                storefront = {}
                config["storefront"] = storefront
            legacy_status = storefront.get("status")
            if legacy_status == "confirmed":
                # A legacy confirmation has no durable current-owner record.
                # Keep the snapshot for review but require re-confirmation
                # before it can be refreshed automatically.
                storefront["status"] = (
                    "discovered" if storefront.get("url") else "unconfigured"
                )
                changed = True
            elif legacy_status == "none":
                storefront["status"] = "unconfigured"
                changed = True
            if storefront.get("owner_confirmed_at") is not None:
                storefront["owner_confirmed_at"] = None
                changed = True
        if previous_version < 6:
            # Existing releases treated learning.enabled as both permission to
            # learn from new draft edits and permission to use prior memory.
            # Long-term memory now participates in draft generation by default;
            # only a deliberate later opt-out disables it.
            memory = config.setdefault("memory", {})
            if not isinstance(memory, dict):
                memory = {}
                config["memory"] = memory
            if memory.get("usage_enabled") is not True:
                memory["usage_enabled"] = True
                changed = True
            if memory.get("usage_confirmed_at") is not None:
                memory["usage_confirmed_at"] = None
                changed = True
            learning = config.setdefault("learning", {})
            if isinstance(learning, dict) and "learn_from_draft_edits" in learning:
                learning.pop("learn_from_draft_edits")
                changed = True
        if previous_version < 7:
            # Per-category automatic-reply permissions now live in an
            # independent runtime state file. Any legacy flags found in
            # user_memory.md are removed by init and re-created as disabled
            # category records, so the migration fails closed.
            if automation.get("send_mode") == "auto_send":
                automation["send_mode"] = "draft_only"
                automation["auto_send_confirmed_at"] = None
            if "auto_send_allowlist" in automation:
                automation.pop("auto_send_allowlist")
            changed = True
        config["version"] = defaults["version"]
        changed = True
    if changed:
        atomic_json(config_path, config)
    return changed


def protect_baseline() -> None:
    """Make the shipped recovery source read-only at install/runtime, not in Git."""
    try:
        os.chmod(DEFAULTS["system-prompt"], 0o444)
    except OSError as exc:
        raise SystemExit(
            f"Unable to protect the default system prompt baseline: {exc}"
        ) from exc


def ensure_initialized() -> None:
    missing = [name for name in RUNTIME_NAMES if not runtime_path(name).exists()]
    if missing:
        raise SystemExit(
            "The running configuration has not been initialized or is incomplete:"
            + ", ".join(missing)
            + ". Please run python3 scripts/configure.py init first"
        )


def init_runtime(_: argparse.Namespace) -> None:
    protect_baseline()
    destination = runtime_dir()
    destination.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(destination, 0o700)
    created = []
    kept = []
    for kind, source in DEFAULTS.items():
        target = runtime_path(kind)
        if target.exists():
            kept.append(str(target))
            continue
        atomic_copy(source, target)
        created.append(str(target))
    try:
        upgraded = upgrade_runtime_config()
        migrated_legacy_permissions = migrate_legacy_memory_permissions(
            runtime_path("user-memory")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to safely upgrade the running config: {exc}") from exc
    print(f"Running directory: {destination}")
    for path in created:
        print(f"Created: {path}")
    for path in kept:
        print(f"Existing file reserved: {path}")
    if upgraded:
        print(
            "Added newly introduced safe defaults to config.json without replacing configured values"
        )
    if migrated_legacy_permissions:
        print(
            "Moved legacy in-memory category permissions to disabled independent records; the owner must confirm them again"
        )
    print("Default sending mode: draft_only")
    print(
        "Next step: Review config.json, system-prompt.md, workflow.md, persona.md, user_memory.md, and auto_reply_permissions.json. Automatic sending stays disabled until the owner enables it and confirms matching categories after a sent-Draft event. Record an owner-confirmed timezone and quiet-hours policy before creating any cron task."
    )


def read_config() -> dict:
    ensure_initialized()
    try:
        return json.loads(runtime_path("config").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read running configuration: {exc}") from exc


def print_status(args: argparse.Namespace) -> None:
    destination = runtime_dir()
    initialized = all(runtime_path(name).exists() for name in RUNTIME_NAMES)
    payload = {
        "skill_dir": str(SKILL_DIR),
        "runtime_dir": str(destination),
        "initialized": initialized,
        "files": {name: str(runtime_path(name)) for name in RUNTIME_NAMES},
        "immutable_baseline": str(DEFAULTS["system-prompt"]),
    }
    if initialized:
        config = read_config()
        automation = config.get("automation", {})
        memory = config.get("memory", {})
        payload.update(
            {
                "store_name": config.get("store_name", ""),
                "config_version": config.get("version"),
                "gmail_account": config.get("gmail", {}).get("account", ""),
                "commerce_provider": config.get("commerce", {}).get(
                    "provider", "unconfigured"
                ),
                "storefront_url": config.get("storefront", {}).get("url", ""),
                "storefront_status": config.get("storefront", {}).get(
                    "status", "unconfigured"
                ),
                "storefront_owner_confirmed_at": config.get(
                    "storefront", {}
                ).get("owner_confirmed_at"),
                "store_discovery_file": config.get("storefront", {}).get(
                    "discovery_file", ""
                ),
                "store_last_discovered_at": config.get("storefront", {}).get(
                    "last_discovered_at"
                ),
                "send_mode": automation.get("send_mode", "unknown"),
                "auto_send_confirmed_at": automation.get("auto_send_confirmed_at"),
                "ai_disclosure": automation.get("ai_disclosure", {}).get("enabled"),
                "learning_enabled": config.get("learning", {}).get("enabled", False),
                "memory_usage_enabled": memory.get("usage_enabled", True),
                "memory_usage_confirmed_at": memory.get("usage_confirmed_at"),
                "timezone": config.get("timezone", ""),
                "schedule_timezone_confirmed_at": config.get("scheduling", {}).get(
                    "timezone_confirmed_at"
                ),
                "schedule_quiet_hours": config.get("scheduling", {}).get(
                    "quiet_hours", ""
                ),
                "schedule_quiet_hours_confirmed_at": config.get(
                    "scheduling", {}
                ).get("quiet_hours_confirmed_at"),
            }
        )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for key, value in payload.items():
        if key == "files":
            print("Run file:")
            for name, path in value.items():
                print(f"  {name}: {path}")
        else:
            print(f"{key}: {value}")


def resolve_named_path(name: str) -> Path:
    if name in RUNTIME_NAMES:
        return runtime_path(name)
    if name == "default-system-prompt":
        return DEFAULTS["system-prompt"]
    if name == "runtime":
        return runtime_dir()
    if name == "store-discovery":
        return runtime_dir() / "store-discovery.json"
    raise SystemExit(f"Unknown path name: {name}")


def print_path(args: argparse.Namespace) -> None:
    if args.name in RUNTIME_NAMES:
        ensure_initialized()
    print(resolve_named_path(args.name))


SENSITIVE_CONFIG_KEY_PARTS = (
    "account",
    "connector",
    "credential",
    "token",
    "secret",
    "password",
    "api_key",
)


def redact_config(value: object, key: str = "") -> object:
    if any(part in key.lower() for part in SENSITIVE_CONFIG_KEY_PARTS):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {item_key: redact_config(item_value, item_key) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [redact_config(item, key) for item in value]
    return value


def show_runtime(args: argparse.Namespace) -> None:
    if args.name == "runtime":
        raise SystemExit("Use path runtime to display the runtime directory")
    if args.name in RUNTIME_NAMES:
        ensure_initialized()
    target = resolve_named_path(args.name)
    try:
        if args.name == "config":
            payload = json.loads(target.read_text(encoding="utf-8"))
            print(json.dumps(redact_config(payload), ensure_ascii=False, indent=2))
        else:
            print(target.read_text(encoding="utf-8"), end="")
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to display {args.name}: {exc}") from exc


def set_disclosure(args: argparse.Namespace) -> None:
    require_explicit_owner_confirmation(args)
    config = read_config()
    automation = config.setdefault("automation", {})
    disclosure = automation.setdefault("ai_disclosure", {})
    disclosure["enabled"] = args.value == "on"
    disclosure["text"] = DISCLOSURE
    atomic_json(runtime_path("config"), config)
    print(f"AI statement: {'open' if disclosure['enabled'] else 'closed'}")
    print(DISCLOSURE)


def set_learning(args: argparse.Namespace) -> None:
    require_explicit_owner_confirmation(args)
    config = read_config()
    learning = config.setdefault("learning", {})
    enabled = args.value == "on"
    learning["enabled"] = enabled
    learning["consent_granted_at"] = (
        datetime.now(timezone.utc).isoformat() if enabled else None
    )
    atomic_json(runtime_path("config"), config)
    print(
        f"Ongoing draft-edit learning: {'enabled' if enabled else 'disabled'}"
    )
    if enabled:
        print(
            "This enables automatic detection and redacted learning from later owner-edited AI drafts. It does not control one-time onboarding history import or use of existing user memory."
        )


def set_memory_usage(args: argparse.Namespace) -> None:
    require_explicit_owner_confirmation(args)
    config = read_config()
    memory = config.setdefault("memory", {})
    enabled = args.value == "on"
    memory["usage_enabled"] = enabled
    memory["usage_confirmed_at"] = (
        datetime.now(timezone.utc).isoformat() if enabled else None
    )
    atomic_json(runtime_path("config"), config)
    if enabled:
        print("Existing user memory: enabled for draft generation")
        print(
            "Only matching approved playbooks may guide drafts; current order evidence, policy, law, and safety gates still take precedence."
        )
    else:
        print("Existing user memory: disabled for draft generation")


def set_auto_send(args: argparse.Namespace) -> None:
    require_explicit_owner_confirmation(args)
    config = read_config()
    automation = config.setdefault("automation", {})
    enabled = args.value == "on"
    automation["send_mode"] = "auto_send" if enabled else "draft_only"
    automation["auto_send_confirmed_at"] = (
        datetime.now(timezone.utc).isoformat() if enabled else None
    )
    atomic_json(runtime_path("config"), config)
    if enabled:
        print("Automatic sending: enabled")
        print(
            "No category is approved by this global setting. A message may be sent only when every atomic issue has an enabled independent automatic-reply permission confirmed after a sent-Draft event. Otherwise create a draft."
        )
    else:
        print("Automatic sending: disabled; all messages remain drafts")


def configure_schedule(args: argparse.Namespace) -> None:
    require_explicit_owner_confirmation(args)
    timezone_name = validate_iana_timezone(args.timezone)
    quiet_hours = args.quiet_hours.strip()
    if not quiet_hours:
        raise SystemExit(
            "Quiet-hours policy is required; use 'none' only when the owner explicitly confirms that no quiet period applies"
        )
    config = read_config()
    confirmed_at = datetime.now(timezone.utc).isoformat()
    config["timezone"] = timezone_name
    scheduling = config.setdefault("scheduling", {})
    scheduling.update(
        {
            "timezone_confirmed_at": confirmed_at,
            "quiet_hours": quiet_hours,
            "quiet_hours_confirmed_at": confirmed_at,
        }
    )
    atomic_json(runtime_path("config"), config)
    print(f"Confirmed timezone: {timezone_name}")
    print(f"Confirmed quiet-hours policy: {quiet_hours}")
    print("Run python3 scripts/configure.py verify --require-schedule before creating a disabled cron task")


def set_storefront_status(args: argparse.Namespace) -> None:
    require_explicit_owner_confirmation(args)
    config = read_config()
    storefront = config.setdefault("storefront", {})
    confirmed_at = datetime.now(timezone.utc).isoformat()
    if args.value == "confirmed":
        url = storefront.get("url")
        discovery_path = Path(
            storefront.get("discovery_file") or resolve_named_path("store-discovery")
        )
        if not url or not discovery_path.is_file():
            raise SystemExit(
                "Run scripts/discover_store.py with the merchant-supplied URL before confirming the storefront"
            )
        storefront.update(
            {
                "status": "confirmed",
                "owner_confirmed_at": confirmed_at,
            }
        )
        message = f"Confirmed public storefront: {url}"
    else:
        storefront.update(
            {
                "status": "none",
                "url": "",
                "discovery_file": "",
                "last_discovered_at": None,
                "owner_confirmed_at": confirmed_at,
            }
        )
        message = "Recorded: this merchant has no public storefront"
    atomic_json(runtime_path("config"), config)
    print(message)


def restore_runtime(args: argparse.Namespace) -> None:
    if args.name not in {"system-prompt", "workflow", "persona"}:
        raise SystemExit("restore only supports system-prompt, workflow or persona")
    ensure_initialized()
    require_explicit_owner_confirmation(args)
    target = runtime_path(args.name)
    backup_dir = runtime_dir() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = backup_dir / f"{target.name}.{timestamp}.bak"
    atomic_copy(target, backup)
    atomic_copy(DEFAULTS[args.name], target)
    print(f"Backed up: {backup}")
    print(f"Restored from read-only baseline: {target}")


def verify_runtime(args: argparse.Namespace) -> None:
    protect_baseline()
    ensure_initialized()
    errors = []
    prompt = runtime_path("system-prompt").read_text(encoding="utf-8")
    workflow = runtime_path("workflow").read_text(encoding="utf-8")
    persona = runtime_path("persona").read_text(encoding="utf-8")
    rule_numbers = [int(value) for value in re.findall(r"\[R(\d{3})\]", prompt)]
    if len(rule_numbers) < 100:
        errors.append(
            f"The running version system prompt words only have {len(rule_numbers)} numbering rules, at least 100 are required"
        )
    if len(rule_numbers) != len(set(rule_numbers)):
        errors.append(
            "There is a duplicate rule number in the running version system prompt word"
        )
    required_workflow = [
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "complete orders",
        "Activities",
        "Policy",
    ]
    for marker in required_workflow:
        if marker not in workflow:
            errors.append(f"The running version of the workflow is missing: {marker}")
    if not persona.strip():
        errors.append("Run version user is set to empty")
    config = read_config()
    if config.get("version") != 7:
        errors.append(
            "config.version must be 7; run python3 scripts/configure.py init to add new safe defaults"
        )
    automation = config.get("automation", {})
    if not isinstance(automation, dict):
        errors.append("automation must be an object")
        automation = {}
    send_mode = automation.get("send_mode")
    if send_mode not in {"draft_only", "auto_send"}:
        errors.append("automation.send_mode must be draft_only or auto_send")
    auto_send_confirmed_at = automation.get("auto_send_confirmed_at")
    if send_mode == "auto_send" and (
        not isinstance(auto_send_confirmed_at, str) or not auto_send_confirmed_at
    ):
        errors.append(
            "automation.auto_send_confirmed_at is required when automatic sending is enabled"
        )
    if send_mode == "draft_only" and auto_send_confirmed_at is not None:
        errors.append(
            "automation.auto_send_confirmed_at must be null while draft_only is enabled"
        )
    if "auto_send_allowlist" in automation:
        errors.append(
            "automation.auto_send_allowlist is no longer supported; use independent category automatic-reply permissions instead"
        )
    disclosure = automation.get("ai_disclosure", {})
    if disclosure.get("text") != DISCLOSURE:
        errors.append(
            "AI statement text has been rewritten; please restore the specified original text"
        )
    if not isinstance(disclosure.get("enabled"), bool):
        errors.append("ai_disclosure.enabled must be a Boolean value")
    learning = config.get("learning", {})
    if not isinstance(learning.get("enabled"), bool):
        errors.append("learning.enabled must be a Boolean value")
    memory = config.get("memory", {})
    if not isinstance(memory, dict):
        errors.append("memory must be an object")
        memory = {}
    memory_usage_enabled = memory.get("usage_enabled")
    if not isinstance(memory_usage_enabled, bool):
        errors.append("memory.usage_enabled must be a Boolean value")
    memory_usage_confirmed_at = memory.get("usage_confirmed_at")
    if memory_usage_confirmed_at is not None and (
        not isinstance(memory_usage_confirmed_at, str)
        or not memory_usage_confirmed_at
    ):
        errors.append(
            "memory.usage_confirmed_at must be null or a non-empty timestamp"
        )
    if memory_usage_enabled is False and memory_usage_confirmed_at is not None:
        errors.append(
            "memory.usage_confirmed_at must be null while existing memory use is disabled"
        )
    retention = config.get("retention", {})
    if not isinstance(retention, dict):
        errors.append("retention must be an object")
    elif (
        type(retention.get("pending_category_confirmation_days")) is not int
        or retention.get("pending_category_confirmation_days") < 0
    ):
        errors.append(
            "retention.pending_category_confirmation_days must be a non-negative integer"
        )
    timezone_name = config.get("timezone", "")
    if not isinstance(timezone_name, str):
        errors.append("timezone must be a string")
    elif timezone_name:
        try:
            ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            errors.append("timezone must be a valid IANA timezone name when set")
    scheduling = config.get("scheduling", {})
    if not isinstance(scheduling, dict):
        errors.append("scheduling must be an object")
    elif args.require_schedule:
        if not timezone_name:
            errors.append(
                "A scheduled task requires a confirmed timezone; run scripts/configure.py schedule first"
            )
        if not isinstance(scheduling.get("timezone_confirmed_at"), str) or not scheduling.get(
            "timezone_confirmed_at"
        ):
            errors.append("A scheduled task requires timezone_confirmed_at")
        if not isinstance(scheduling.get("quiet_hours"), str) or not scheduling.get(
            "quiet_hours"
        ):
            errors.append("A scheduled task requires an explicit quiet-hours policy")
        if not isinstance(
            scheduling.get("quiet_hours_confirmed_at"), str
        ) or not scheduling.get("quiet_hours_confirmed_at"):
            errors.append("A scheduled task requires quiet_hours_confirmed_at")
    storefront = config.get("storefront", {})
    if not isinstance(storefront, dict):
        errors.append("storefront must be an object")
        storefront = {}
    if storefront.get("status") not in {
        "unconfigured",
        "discovered",
        "confirmed",
        "none",
    }:
        errors.append(
            "storefront.status must be unconfigured, discovered, confirmed, or none"
        )
    if not isinstance(storefront.get("discovery_enabled", False), bool):
        errors.append("storefront.discovery_enabled must be a Boolean value")
    if storefront.get("respect_robots_txt") is not True:
        errors.append("storefront.respect_robots_txt must remain true")
    if storefront.get("public_sources_only") is not True:
        errors.append("storefront.public_sources_only must remain true")
    storefront_url = storefront.get("url", "")
    if storefront.get("status") in {"discovered", "confirmed"} and not storefront_url:
        errors.append(
            "A discovered or confirmed storefront must include storefront.url"
        )
    if storefront.get("status") == "none" and storefront_url:
        errors.append("storefront.url must be empty when storefront.status is none")
    storefront_confirmed_at = storefront.get("owner_confirmed_at")
    if storefront.get("status") in {"confirmed", "none"} and (
        not isinstance(storefront_confirmed_at, str) or not storefront_confirmed_at
    ):
        errors.append(
            "storefront.owner_confirmed_at is required when storefront status is confirmed or none"
        )
    if storefront.get("status") in {"unconfigured", "discovered"} and (
        storefront_confirmed_at is not None
    ):
        errors.append(
            "storefront.owner_confirmed_at must be null until the owner confirms the storefront state"
        )
    if storefront_url:
        discovery_path = Path(
            storefront.get("discovery_file") or resolve_named_path("store-discovery")
        )
        if not discovery_path.is_file():
            errors.append(
                "A storefront URL is configured but store-discovery.json is missing; run scripts/discover_store.py again"
            )
        else:
            try:
                discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
                if discovery.get("public_sources_only") is not True:
                    errors.append(
                        "store-discovery.json is not marked public_sources_only"
                    )
                if discovery.get("storefront_url") != storefront_url:
                    errors.append(
                        "The configured storefront URL does not match store-discovery.json"
                    )
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"Unable to read store-discovery.json: {exc}")
    memory = runtime_path("user-memory").read_text(encoding="utf-8")
    if "ECS_MEMORY_JSON_BEGIN" not in memory or "ECS_MEMORY_JSON_END" not in memory:
        errors.append("user_memory.md is missing its managed-memory markers")
    for legacy_field in (
        "auto_send_approved",
        "auto_send_approved_at",
        "auto_send_confirmation",
        "sent_draft_confirmation",
    ):
        if legacy_field in memory:
            errors.append(
                f"user_memory.md must not contain legacy automatic-reply field: {legacy_field}"
            )
    try:
        permissions = load_permissions()
        pending = load_pending()
        if permissions.get("schema_version") != 1:
            errors.append("auto_reply_permissions.json must use schema_version 1")
        if pending.get("schema_version") != 1:
            errors.append(
                "pending_category_confirmations.json must use schema_version 1"
            )
        for key, permission in permissions.get("categories", {}).items():
            if not isinstance(permission, dict) or permission.get("enabled") not in {
                True,
                False,
            }:
                errors.append(f"Invalid automatic-reply permission record: {key}")
    except SystemExit as exc:
        errors.append(str(exc))
    manifest_path = ASSETS_DIR / "baseline-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected = manifest.get("default-system-prompt.md")
        if expected and sha256(DEFAULTS["system-prompt"]) != expected:
            errors.append(
                "The hash of the read-only default system prompt word is inconsistent with the release baseline"
            )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Verification passed: {len(rule_numbers)} system rules")
    print(f"Send mode: {send_mode}")
    print(f"AI statement: {'open' if disclosure['enabled'] else 'closed'}")
    print(f"Running directory: {runtime_dir()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Configuring a running copy of the e-commerce Gmail customer service skill"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Create missing run configuration, do not overwrite existing files"
    )
    init_parser.set_defaults(func=init_runtime)

    status_parser = subparsers.add_parser(
        "status", help="Display path and non-sensitive configuration status"
    )
    status_parser.add_argument("--json", action="store_true")
    status_parser.set_defaults(func=print_status)

    path_parser = subparsers.add_parser("path", help="Display the specified file path")
    path_parser.add_argument(
        "name",
        choices=[*RUNTIME_NAMES, "default-system-prompt", "runtime", "store-discovery"],
    )
    path_parser.set_defaults(func=print_path)

    show_parser = subparsers.add_parser(
        "show", help="Display a running file read-only; config values are redacted"
    )
    show_parser.add_argument(
        "name",
        choices=[*RUNTIME_NAMES, "default-system-prompt", "store-discovery"],
    )
    show_parser.set_defaults(func=show_runtime)

    set_parser = subparsers.add_parser("set", help="Set controlled options")
    set_parser.add_argument(
        "setting", choices=["disclosure", "learning", "memory-usage", "auto-send"]
    )
    set_parser.add_argument("value", choices=["on", "off"])
    set_parser.add_argument(
        "--confirm-owner-request",
        action="store_true",
        help="Required because this changes an operator-owned runtime file",
    )
    set_parser.set_defaults(
        func=lambda args: (
            set_disclosure(args)
            if args.setting == "disclosure"
            else set_learning(args)
            if args.setting == "learning"
            else set_memory_usage(args)
            if args.setting == "memory-usage"
            else set_auto_send(args)
        )
    )

    schedule_parser = subparsers.add_parser(
        "schedule", help="Record owner-confirmed timezone and quiet-hours safeguards"
    )
    schedule_parser.add_argument("--timezone", required=True)
    schedule_parser.add_argument("--quiet-hours", required=True)
    schedule_parser.add_argument(
        "--confirm-owner-request",
        action="store_true",
        help="Required because this records operator-approved scheduling state",
    )
    schedule_parser.set_defaults(func=configure_schedule)

    storefront_parser = subparsers.add_parser(
        "storefront", help="Confirm a discovered storefront or record that none exists"
    )
    storefront_parser.add_argument("value", choices=["confirmed", "none"])
    storefront_parser.add_argument(
        "--confirm-owner-request",
        action="store_true",
        help="Required because this records an owner-confirmed storefront state",
    )
    storefront_parser.set_defaults(func=set_storefront_status)

    restore_parser = subparsers.add_parser(
        "restore", help="Restore running files from read-only baseline after backup"
    )
    restore_parser.add_argument(
        "name", choices=["system-prompt", "workflow", "persona"]
    )
    restore_parser.add_argument(
        "--confirm-owner-request",
        action="store_true",
        help="Required because restore writes an operator-owned runtime file",
    )
    restore_parser.set_defaults(func=restore_runtime)

    verify_parser = subparsers.add_parser(
        "verify", help="Verify running copy and read-only baseline"
    )
    verify_parser.add_argument(
        "--require-schedule",
        action="store_true",
        help="Also require owner-confirmed timezone and quiet-hours safeguards",
    )
    verify_parser.set_defaults(func=verify_runtime)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if (
        getattr(args, "setting", None)
        not in {None, "disclosure", "learning", "memory-usage", "auto-send"}
        and args.command == "set"
    ):
        raise SystemExit("Unknown setting")
    args.func(args)


if __name__ == "__main__":
    main()
