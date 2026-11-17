from __future__ import annotations

from collections.abc import Callable
from typing import Any

from . import (
    causal_chain,
    drill_down_stair,
    heat_matrix,
    interaction_storyboard,
    layered_architecture,
    phase_roadmap,
    product_ui_overview,
)


Renderer = Callable[[Any, dict[str, Any], dict[str, Any], dict[str, Any]], dict[str, Any]]

RENDERERS: dict[str, Renderer] = {
    "causal_chain": causal_chain.render,
    "heat_matrix": heat_matrix.render,
    "layered_architecture": layered_architecture.render,
    "drill_down_stair": drill_down_stair.render,
    "phase_roadmap": phase_roadmap.render,
    "product_ui_overview": product_ui_overview.render,
    "interaction_storyboard": interaction_storyboard.render,
}


def get_renderer(component_type: str) -> Renderer | None:
    return RENDERERS.get(component_type)
