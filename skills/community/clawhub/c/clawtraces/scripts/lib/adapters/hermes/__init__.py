# FILE_META
# INPUT:  lib.adapters registry
# OUTPUT: registered AdapterSpec(name='hermes')
# POS:    skill lib adapters — Hermes Agent (Nous Research) entry point
# MISSION: Wire discover/parse/build_harness/default_filters into the global adapter registry.

"""Hermes Agent adapter.

Source data: ``~/.hermes/state.db`` (SQLite) — the Hermes CLI writes every
session + message there. Preferred access path is ``hermes sessions export``
(stable public contract); direct SQLite reads serve as fallback.

See ``docs/adapter-design.md`` §8.2 for the full interface map.
"""

from __future__ import annotations

from .. import AdapterSpec, register
from . import discover as _discover
from . import parse as _parse
from . import harness as _harness
from .filters import DEFAULT_FILTERS

register(
    AdapterSpec(
        name="hermes",
        discover=_discover.discover,
        parse=_parse.parse,
        build_harness=_harness.build_harness,
        list_scopes=_harness.list_scopes,
        default_filters=DEFAULT_FILTERS,
    )
)
