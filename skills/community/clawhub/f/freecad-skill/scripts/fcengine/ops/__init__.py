"""Operation handlers, keyed by catalog op name.

A handler takes ``(ctx, params)`` and returns either the FreeCAD object it
created/modified, ``None``, or a dict with optional ``object`` and ``data``.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

from . import (
    assembly,
    booleans,
    drawing,
    edit,
    export,
    features,
    fem,
    importer,
    material,
    measure,
    partdesign,
    patterns,
    query,
    render,
    solids,
    sweeps,
    text,
    transforms,
)

Handler = Callable[..., Any]

HANDLERS: Dict[str, Handler] = {}
for _mod in (
    solids,
    booleans,
    features,
    patterns,
    transforms,
    edit,
    query,
    export,
    render,
    partdesign,
    measure,
    drawing,
    fem,
    assembly,
    sweeps,
    material,
    importer,
    text,
):
    HANDLERS.update(_mod.HANDLERS)
