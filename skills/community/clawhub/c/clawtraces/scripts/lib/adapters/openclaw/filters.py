# FILE_META
# INPUT:  (consumed by pipeline filter stage + config_loader overrides)
# OUTPUT: DEFAULT_FILTERS dict registered through AdapterSpec
# POS:    skill lib adapters/openclaw — filter defaults
# MISSION: Ship OpenClaw's default filter config; config.json overrides remain the
#          user-facing tuning knob.

"""Default filter config for the OpenClaw adapter.

Mirrors the historical ``config.json.eligibility`` block that predates
the adapter refactor. During Phase 4 migration the authoritative source
still lives at the top-level ``eligibility`` key for backward compat;
``config_loader`` is expected to promote it into
``config.json.adapters.openclaw.filters`` transparently.

Filter semantics (consumed by the pipeline filter stage):

- ``model_whitelist``       substring match against the session's model
- ``min_turns``             minimum number of user-role messages
- ``min_tool_use_count``    drop sessions with fewer tool_calls
- ``min_reasoning_turns``   drop sessions without enough reasoning_content
- ``allow_non_cache_trace`` accept sessions without cache-trace data by
                            falling back to reconstructed system prompt
- ``include_cron_tasks``    whether ``[cron: …]`` seeded sessions count
"""

from __future__ import annotations

DEFAULT_FILTERS: dict = {
    "model_whitelist": ["sonnet-4.6", "opus-4.5", "opus-4.6", "opus-4.7"],
    "min_turns": 5,
    "min_tool_use_count": 1,
    "min_reasoning_turns": 1,
    "allow_non_cache_trace": True,
    "include_cron_tasks": True,
    "exclude_compaction": False,  # OpenClaw handles compaction via DAG concat
    "exclude_sidechain": False,
}
