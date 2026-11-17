"""Decoration location name → placement. Owned by the skill, not Odoo.

Odoo's ``web_mockup_plan`` returns each decoration's ``location_name`` exactly
as entered ("Adult Full Front", "Left Chest", "RT SLEEVE", "Left Leg"). What
that means on a flat front photo is a mockup decision, so it lives here next to
``placement_rules.json`` and ships with the skill.

LEFT/RIGHT ARE THE WEARER'S. "Left chest" is over the wearer's left pec, which
in a front-facing photo sits on the IMAGE's RIGHT half. ``image_side`` carries
that resolved answer so nothing downstream re-derives (or mirrors) it.
"""

from __future__ import annotations

import re

# placement -> (view, image_side)
PLACEMENTS = {
    "full_front": ("front", "center"),
    "center_chest": ("front", "center"),
    "left_chest": ("front", "right"),    # wearer's left  → image right
    "right_chest": ("front", "left"),    # wearer's right → image left
    "left_sleeve": ("front", "right"),   # wearer's left sleeve → image right edge
    "right_sleeve": ("front", "left"),   # wearer's right sleeve → image left edge
    "left_leg": ("front", "right"),      # front of the wearer's left leg (shorts, pants)
    "right_leg": ("front", "left"),
    "front": ("front", "center"),        # hats, mugs, bags: the one front panel
    "full_back": ("back", "center"),
    "back_yoke": ("back", "center"),
}

_WORD = re.compile(r"[a-z]+")

# Abbreviations seen in location names.
_ALIASES = {
    "lt": "left", "lft": "left", "l": "left",
    "rt": "right", "rgt": "right", "r": "right",
    "lc": "left chest", "rc": "right chest",
    "fb": "full back", "ff": "full front",
}


def normalize_location(name: str | None) -> dict | None:
    """Map a free-text location name to a placement.

    Returns ``{"placement", "view", "image_side", "wearer_side"}`` or ``None``
    when the name is not something a flat front/back photo can show (hips,
    inside labels, a sleeve without a side, …) — never a guess.
    """
    words = []
    for w in _WORD.findall((name or "").lower()):
        words.extend(_ALIASES.get(w, w).split())
    ws = set(words)
    if not ws:
        return None

    side = "left" if "left" in ws else ("right" if "right" in ws else None)

    placement = None
    if ws & {"yoke", "nape", "neck", "collar"} or {"upper", "back"} <= ws:
        placement = "back_yoke"
    elif "back" in ws:
        placement = "full_back"
    elif ws & {"sleeve", "sleeves", "arm", "shoulder", "bicep"}:
        placement = f"{side}_sleeve" if side else None
    elif ws & {"leg", "thigh"}:
        placement = f"{side}_leg" if side else None
    elif ws & {"chest", "pocket", "pec", "breast", "heart"}:
        if side:
            placement = f"{side}_chest"
        elif ws & {"center", "centre", "middle", "mid"}:
            placement = "center_chest"
        else:
            placement = "full_front"
    elif ws & {"hat", "cap", "beanie", "visor", "mug", "tumbler", "bag", "tote"}:
        placement = "front"
    elif ws & {"front", "jersey", "body"} or ws == {"full"}:
        placement = "full_front"

    if placement is None:
        return None
    view, image_side = PLACEMENTS[placement]
    return {"placement": placement, "view": view,
            "image_side": image_side, "wearer_side": side}


def resolve_layers(decorations: list[dict]) -> dict:
    """Decide which decorations go on the FRONT photo.

    Takes the plan's raw decorations and returns ``{"layers", "omitted",
    "skip_reason"}``. Layers are the decorations enriched with placement /
    view / image_side. ``omitted`` lists each left-off decoration with why
    (``back_view`` / ``unmapped_location`` / ``no_art``). ``skip_reason`` is
    set when nothing can go on the front photo.
    """
    layers, omitted = [], []
    for d in decorations:
        loc = normalize_location(d.get("location_name"))
        if not loc:
            reason = "unmapped_location"
        elif not d.get("art_sources"):
            reason = "no_art"
        elif loc["view"] != "front":
            reason = "back_view"
        else:
            layers.append({**d, **loc})
            continue
        omitted.append({"decoration_id": d["decoration_id"],
                        "location_name": d.get("location_name"), "reason": reason})
    skip = None
    if not layers:
        reasons = {o["reason"] for o in omitted}
        if not decorations:
            skip = "no_decoration"
        elif reasons == {"back_view"}:
            skip = "back_only_no_back_blank"
        elif "unmapped_location" in reasons:
            skip = "unmapped_location"
        else:
            skip = "no_usable_decoration"
    return {"layers": layers, "omitted": omitted, "skip_reason": skip}
