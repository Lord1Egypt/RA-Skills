# FILE_META
# INPUT:  skills/clawtraces/config.json (optional path override)
# OUTPUT: validated config dict
# POS:    skill lib — consumed by pipeline_options.py and pipeline.py (PR 2+)
# MISSION: Load and validate skill config; merge with built-in defaults; fail fast on any schema violation.

"""Load and validate ``skills/clawtraces/config.json``.

v2 採 single-config design: no local override, no per-agent config. Any
config issue (missing file / wrong type / unknown key / out-of-range
number) raises ``ValueError`` so runtime behavior never drifts silently
from operator intent.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

_SEPARATOR_NORMALIZE_RE = re.compile(r"[._-]")

_DEFAULTS: dict[str, Any] = {
    # Skill semver. Read independently by lib/version.py; listed here
    # only so the strict unknown-key check does not reject configs that
    # carry it. config.json is the single source of truth for the Skill
    # version since the VERSION file was retired.
    "version": None,
    "default_list_size": 20,
    "max_list_size": 100,
    "eligibility": {
        "model_whitelist": ["sonnet-4.6", "opus-4.5", "opus-4.6", "opus-4.7"],
        "min_turns": 5,
        "min_tool_use_count": 0,
        "min_reasoning_turns": 0,
        "allow_non_cache_trace": False,
        "include_cron_tasks": True,
    },
    # Per-adapter overrides. Keys here are adapter names (hermes / claude-code
    # / codex / ...). Each value is a free-form object; callers use
    # get_adapter_filters() to merge adapter code defaults with any overrides
    # the operator provides. Because schemas differ per adapter, this subtree
    # is intentionally NOT strict-validated against _DEFAULTS.
    "adapters": {},
}


def _default_config_path() -> str:
    # config_loader.py lives at skills/clawtraces/scripts/lib/core/config_loader.py
    # config.json lives at skills/clawtraces/config.json (up 3 levels from lib/core/)
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "..", "..", "config.json"))


def load_config(config_path: str | None = None) -> dict:
    """Read ``config.json``, merge with ``_DEFAULTS``, validate.

    Raises ``ValueError`` on any schema issue.
    """
    path = config_path or _default_config_path()
    if not os.path.isfile(path):
        raise ValueError(f"config not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        try:
            user_cfg = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"config JSON parse error: {e}") from e
    if not isinstance(user_cfg, dict):
        raise ValueError(
            f"config root must be a JSON object, got {type(user_cfg).__name__}"
        )
    merged = _merge_with_defaults(user_cfg)
    _validate(merged)
    return merged


def _merge_with_defaults(user: dict) -> dict:
    """Reject unknown keys at both top level and nested objects; fill gaps with defaults."""
    unknown_top = set(user.keys()) - set(_DEFAULTS.keys())
    if unknown_top:
        raise ValueError(
            f"unknown top-level config key(s): {sorted(unknown_top)}"
        )

    # Keys where free-form nested content is allowed (each adapter brings its
    # own schema; strict validation would make the adapter layer brittle).
    FREEFORM_KEYS = {"adapters"}

    merged: dict[str, Any] = {}
    for key, default_val in _DEFAULTS.items():
        if key not in user:
            merged[key] = _clone_default(default_val)
            continue
        user_val = user[key]
        if key in FREEFORM_KEYS:
            if not isinstance(user_val, dict):
                raise ValueError(
                    f"config.{key} must be an object, got {type(user_val).__name__}"
                )
            merged[key] = _clone_default(user_val)
            continue
        if isinstance(default_val, dict):
            if not isinstance(user_val, dict):
                raise ValueError(
                    f"config.{key} must be an object, got {type(user_val).__name__}"
                )
            unknown_nested = set(user_val.keys()) - set(default_val.keys())
            if unknown_nested:
                raise ValueError(
                    f"unknown config.{key} key(s): {sorted(unknown_nested)}"
                )
            nested: dict[str, Any] = {}
            for sub_key, sub_default in default_val.items():
                nested[sub_key] = (
                    user_val[sub_key] if sub_key in user_val
                    else _clone_default(sub_default)
                )
            merged[key] = nested
        else:
            merged[key] = user_val
    return merged


def _clone_default(val: Any) -> Any:
    if isinstance(val, dict):
        return {k: _clone_default(v) for k, v in val.items()}
    if isinstance(val, list):
        return list(val)
    return val


def _validate(cfg: dict) -> None:
    _expect_int_ge(cfg, "default_list_size", 1)
    _expect_int_ge(cfg, "max_list_size", 1)
    if cfg["default_list_size"] > cfg["max_list_size"]:
        raise ValueError(
            f"default_list_size ({cfg['default_list_size']}) must not exceed "
            f"max_list_size ({cfg['max_list_size']})"
        )

    elig = cfg["eligibility"]
    whitelist = elig.get("model_whitelist")
    if not isinstance(whitelist, list):
        raise ValueError("eligibility.model_whitelist must be a list")
    if not whitelist:
        raise ValueError("eligibility.model_whitelist must not be empty")
    for i, pattern in enumerate(whitelist):
        if not isinstance(pattern, str) or not pattern.strip():
            raise ValueError(
                f"eligibility.model_whitelist[{i}] must be a non-empty string"
            )

    _expect_int_ge(elig, "min_turns", 0)
    _expect_int_ge(elig, "min_tool_use_count", 0)
    _expect_int_ge(elig, "min_reasoning_turns", 0)
    _expect_bool(elig, "allow_non_cache_trace")
    _expect_bool(elig, "include_cron_tasks")


def _expect_int_ge(container: dict, key: str, minimum: int) -> None:
    val = container[key]
    # bool is a subclass of int in Python; reject explicitly so True/False
    # cannot accidentally satisfy an int field.
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValueError(
            f"{key} must be int, got {type(val).__name__}"
        )
    if val < minimum:
        raise ValueError(f"{key} must be >= {minimum}, got {val}")


def _expect_bool(container: dict, key: str) -> None:
    val = container[key]
    if not isinstance(val, bool):
        raise ValueError(
            f"{key} must be bool, got {type(val).__name__}"
        )


def get_adapter_filters(cfg: dict, adapter_name: str, defaults: dict) -> dict:
    """Merge an adapter's code-side DEFAULT_FILTERS with config.json overrides.

    Lookup path: ``cfg["adapters"][adapter_name]["filters"]``. Unknown keys in
    the override raise ``ValueError`` so typos don't silently drop to the
    default — same fail-fast ergonomics as the rest of config_loader.
    """
    overrides = (
        cfg.get("adapters", {})
        .get(adapter_name, {})
        .get("filters", {})
    )
    if not isinstance(overrides, dict):
        raise ValueError(
            f"adapters.{adapter_name}.filters must be an object, "
            f"got {type(overrides).__name__}"
        )
    unknown = set(overrides.keys()) - set(defaults.keys())
    if unknown:
        raise ValueError(
            f"unknown adapters.{adapter_name}.filters key(s): {sorted(unknown)}"
        )
    merged = {**defaults, **overrides}
    return merged


def is_allowed_model(model_id: str, whitelist: list[str]) -> bool:
    """Case-insensitive substring match against the whitelist patterns.

    Separators ``.``, ``-`` and ``_`` are normalized to a single form before
    comparing so that ``"opus-4.6"`` in the whitelist matches both
    ``"claude-opus-4-6"`` (API canonical) and ``"anthropic/claude-opus-4.6"``
    (human-readable) — OpenClaw uses both spellings depending on origin.
    """
    if not model_id:
        return False
    normalized_id = _SEPARATOR_NORMALIZE_RE.sub("-", model_id.lower())
    for pattern in whitelist:
        normalized_pattern = _SEPARATOR_NORMALIZE_RE.sub("-", pattern.lower())
        if normalized_pattern in normalized_id:
            return True
    return False
