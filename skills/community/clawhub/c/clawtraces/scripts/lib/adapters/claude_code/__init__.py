# FILE_META
# INPUT:  lib.adapters registry
# OUTPUT: registered AdapterSpec(name='claude-code')
# POS:    skill lib adapters — Claude Code (Anthropic CLI/IDE) entry point
# MISSION: Wire discover/parse/build_harness/default_filters into the global adapter registry.

"""Claude Code adapter.

Source data: ``~/.claude/projects/<cwd-slug>/<sessionId>.jsonl``. Each
line is one event emitted by the Claude Code CLI. The content format is
Anthropic Messages API style (content blocks: text / thinking / tool_use
/ tool_result); this adapter translates it into the OpenAI IR the rest
of the pipeline expects.

See ``docs/adapter-design.md`` §8.3 for the full interface map.

Adapter name is ``claude-code`` (hyphenated) to stay consistent with how
prompt templates and filters keys are written across the codebase.
"""

from __future__ import annotations

from .. import AdapterSpec, register
from . import discover as _discover
from . import parse as _parse
from . import harness as _harness
from .filters import DEFAULT_FILTERS

register(
    AdapterSpec(
        name="claude-code",
        discover=_discover.discover,
        parse=_parse.parse,
        build_harness=_harness.build_harness,
        list_scopes=_harness.list_scopes,
        default_filters=DEFAULT_FILTERS,
    )
)
