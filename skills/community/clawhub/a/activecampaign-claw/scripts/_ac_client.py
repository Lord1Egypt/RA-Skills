"""Backward-compatible facade — implementation lives in the `_skill/` package.

Every script in `scripts/` imports from `_ac_client`. This file re-exports the
public surface from the split modules under `_skill/` so those imports keep
working.

If you're adding new helpers, put them in the appropriate `_skill/` module and
re-export them here.
"""

# HTTP client + errors
# CLI driver — opt-in helper that scripts can use instead of writing main()
from _skill.cli import cli_main
from _skill.client import (
    ACClient,
    ACClientError,
    ReadOnlyModeError,
    WriteCapExceededError,
)

# Date and numeric coercion
from _skill.dates import parse_date, safe_float, safe_int

# History log + insights + trends + pattern detection
from _skill.history import (
    compare_to_previous,
    detect_patterns,
    load_history,
    load_insights,
    log_outcome,
    write_insight,
)

# Markdown reporting helpers + plan-tier message
from _skill.reports import (
    emit_files,
    render_feature_unavailable,
    write_report,
)

# String sanitization for API-sourced values
from _skill.safety import sanitize

# Optional structural shapes (TypedDicts) for AC v3 records.
# Scripts may import these for type hints; existing code keeps using plain dicts.
from _skill.schemas import (
    Campaign,
    Contact,
    Deal,
    DealTask,
    Note,
    Tag,
    User,
)

# Credential resolution (env var first, OS keychain second)
from _skill.secrets import (
    delete_credential,
    describe_sources,
    get_credential,
    has_keyring,
    set_credential,
)

# State file paths + load/save/age helpers + env var helper
from _skill.state import (
    HISTORY_FILE,
    INSIGHTS_FILE,
    STATE_DIR,
    STATE_FILE,
    _ensure_state_dir,
    ensure_state,
    env_or_die,
    load_state,
    save_state,
    state_age_days,
)

__all__ = [
    "ACClient",
    "ACClientError",
    "Campaign",
    "Contact",
    "Deal",
    "DealTask",
    "Note",
    "ReadOnlyModeError",
    "Tag",
    "User",
    "WriteCapExceededError",
    "cli_main",
    "delete_credential",
    "describe_sources",
    "get_credential",
    "has_keyring",
    "set_credential",
    "HISTORY_FILE",
    "INSIGHTS_FILE",
    "STATE_DIR",
    "STATE_FILE",
    "_ensure_state_dir",
    "compare_to_previous",
    "detect_patterns",
    "emit_files",
    "ensure_state",
    "env_or_die",
    "load_history",
    "load_insights",
    "load_state",
    "log_outcome",
    "parse_date",
    "render_feature_unavailable",
    "safe_float",
    "safe_int",
    "sanitize",
    "save_state",
    "state_age_days",
    "write_insight",
    "write_report",
]
