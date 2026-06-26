# FILE_META
# INPUT:  (consumed by pipeline filter stage + config_loader overrides)
# OUTPUT: DEFAULT_FILTERS dict registered through AdapterSpec
# POS:    skill lib adapters/hermes — filter defaults
# MISSION: Ship sensible default filter config for Hermes that config.json can override.

"""Default filter config for the Hermes adapter.

Hermes supports 200+ backend models (per Nous docs), so the shipped
whitelist is empty — semantically "accept any model". Deployments that
want to narrow the scope override it via ``config.json``::

    {
      "adapters": {
        "hermes": {
          "filters": {
            "model_whitelist": ["gpt-4o", "claude-opus-4-6"],
            "min_turns": 3
          }
        }
      }
    }

The merged view is produced by ``core.config_loader.get_adapter_filters``
(P1-4). Unknown keys in the override raise ``ValueError`` so typos fail
fast.

Filter semantics (consumed by the pipeline filter stage):

- ``model_whitelist``   substring match against the session's model;
                        empty list = accept everything.
- ``min_turns``         minimum number of user-role messages.
- ``require_tool_use``  drop sessions with zero tool_calls.
- ``require_thinking``  drop sessions without any reasoning_content.
- ``exclude_compaction`` drop sessions flagged as compaction summaries.
                        (Hermes has no equivalent today; kept for
                        symmetry with other adapters.)
- ``exclude_sidechain`` drop sessions marked as sub-agent sidechain runs.
                        Hermes subagents are spawned as independent
                        sessions, so the default is False (don't drop).
"""

from __future__ import annotations

DEFAULT_FILTERS: dict = {
    "model_whitelist": [],
    "min_turns": 2,
    "require_tool_use": False,
    "require_thinking": False,
    "exclude_compaction": True,
    "exclude_sidechain": False,
}

