# FILE_META
# INPUT:  (consumed by pipeline filter stage + config_loader overrides)
# OUTPUT: DEFAULT_FILTERS dict registered through AdapterSpec
# POS:    skill lib adapters/claude_code — filter defaults
# MISSION: Ship sensible default filter config for Claude Code that config.json can override.

"""Default filter config for the Claude Code adapter.

Claude Code sessions are the user-facing CLI/IDE product. Most sessions
are genuine coding work, so the defaults are quite permissive; the one
hard default is ``exclude_sidechain=True`` to keep sub-agent runs out of
the main trajectory until we have sample data that says otherwise (risk
#3 in docs/adapter-design.md §12).

Override pattern::

    {
      "adapters": {
        "claude-code": {
          "filters": {
            "model_whitelist": ["claude-opus-4-6", "claude-sonnet-4-6"],
            "min_turns": 3,
            "exclude_sidechain": false
          }
        }
      }
    }

Filter semantics (consumed by the pipeline filter stage):

- ``model_whitelist``   substring match against the session's model;
                        empty list = accept everything.
- ``min_turns``         minimum number of user-role messages.
- ``require_tool_use``  drop sessions with zero tool_calls.
- ``require_thinking``  drop sessions without any reasoning_content.
- ``exclude_compaction`` drop auto-compact summary sessions. No real
                        sample observed in 200+ local sessions yet, but
                        kept on so we do not mis-emit when they appear.
- ``exclude_sidechain`` drop sub-agent (Task tool) runs. Also kept on
                        until we have enough samples to judge the
                        alternative of emitting them as independent
                        sessions.
"""

from __future__ import annotations

DEFAULT_FILTERS: dict = {
    "model_whitelist": [],
    "min_turns": 2,
    "require_tool_use": False,
    "require_thinking": False,
    "exclude_compaction": True,
    "exclude_sidechain": True,
}
