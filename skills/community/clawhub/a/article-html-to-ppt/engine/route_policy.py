"""Route ownership and QA policy for PPT Smith V4.

The three production routes may share verification machinery, but a route is
never allowed to inherit another route's authoring or QA exemptions by
accident.  Keep route-specific exceptions explicit here.
"""
from __future__ import annotations


PRODUCTION_ROUTES = frozenset({"standard", "bespoke", "template"})


def require_production_route(route: str) -> str:
    normalized = str(route or "").strip().lower()
    if normalized not in PRODUCTION_ROUTES:
        raise ValueError(f"UNKNOWN_PRODUCTION_ROUTE: {route}")
    return normalized


def allows_source_bound_component_fragmentation(route: str) -> bool:
    """Only Path C may discount reviewed component item/detail text boxes."""
    return require_production_route(route) == "template"
