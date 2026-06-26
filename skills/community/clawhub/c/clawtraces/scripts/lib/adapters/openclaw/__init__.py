# FILE_META
# INPUT:  lib.adapters registry
# OUTPUT: registered AdapterSpec(name='openclaw')
# POS:    skill lib adapters — OpenClaw adapter entry point (Phase 4 migration)
# MISSION: Wire discover/parse/build_harness/default_filters into the global adapter registry.

"""OpenClaw adapter.

Source data: ``~/.openclaw/agents/*/sessions/*.jsonl`` — OpenClaw writes
one JSONL per session. Trajectory assembly requires ``cache-trace.jsonl``
for authoritative system prompt (fallback to reconstruction when absent).

See ``docs/adapter-design.md`` §8.1 for the full interface contract.
Phase 4 of the adapter migration: moves OpenClaw-specific DAG walk /
cache-trace / metadata stripper logic from ``lib/pipeline`` into this
package, retiring ``scan_and_convert.py``.
"""

from __future__ import annotations

from .. import AdapterSpec, register
from . import discover as _discover
from . import parse as _parse
from . import harness as _harness
from .filters import DEFAULT_FILTERS

register(
    AdapterSpec(
        name="openclaw",
        discover=_discover.discover,
        parse=_parse.parse,
        build_harness=_harness.build_harness,
        list_scopes=_harness.list_scopes,
        default_filters=DEFAULT_FILTERS,
    )
)
