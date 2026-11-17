#!/usr/bin/env python3
"""Validate a new-wine commission profile and derive construction gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CORE = {
    "strategy": ("organization", "occasion", "audience", "objective"),
    "commercial": ("bottle_count", "release_date", "delivery_country", "budget_range"),
    "wine_target": ("format", "color", "freshness", "texture", "service_moment"),
    "brand": ("brand_name", "label_direction", "approval_owner"),
}


def route(profile: dict) -> str:
    wine_format = str(profile.get("format", "")).lower()
    if "traditional" in wine_format or "cava" in wine_format:
        return "traditional_method_sparkling"
    if "ancestral" in wine_format or "pet-nat" in wine_format or "petnat" in wine_format:
        return "ancestral_sparkling"
    if "sparkling" in wine_format:
        return "sparkling_route_unresolved"
    color = str(profile.get("color", "")).lower()
    if color == "red":
        return "still_red"
    if color == "orange":
        return "skin_contact"
    return "still_white_or_rose"


def gate_requirements(selected: str) -> dict[str, list[str]]:
    common = {
        "reception": ["lot identity", "Brix", "pH", "TA", "YAN", "temperature", "sanitary state"],
        "microbial_succession": ["yeast route", "starting density", "temperature", "YAN", "oxygen strategy"],
        "fermentation": ["density trend", "temperature", "VA", "sensory H2S/reduction", "oxygen or ORP when useful"],
        "bottling_release": ["alcohol", "pH", "TA", "VA", "residual sugar", "microbial stability", "label approval", "traceability"],
    }
    if selected == "ancestral_sparkling":
        common["bottling_release"] += ["bottling density", "pressure calculation", "bottle rating", "active yeast state"]
    elif selected == "traditional_method_sparkling":
        common["bottling_release"] += ["stable base wine", "tirage dose", "tirage yeast", "pressure calculation", "lees time"]
    elif selected in {"still_red", "skin_contact"}:
        common["fermentation"] += ["cap temperature", "extraction state", "pressing decision"]
        common["bottling_release"] += ["malolactic status", "headspace and protection plan"]
    return common


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("--site", default="https://vin-q.com")
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    missing_by_section = {
        section: [field for field in fields if not profile.get(field)]
        for section, fields in CORE.items()
    }
    selected = route(profile)
    missing_count = sum(len(values) for values in missing_by_section.values())
    output = {
        "report_type": "vin_q_new_wine_commission",
        "readiness": "ready_for_constructor" if missing_count == 0 else "needs_input",
        "selected_route": selected,
        "missing_by_section": missing_by_section,
        "four_gate_measurements": gate_requirements(selected),
        "constructor_url": f"{args.site}/",
        "registration_url": f"{args.site}/login?mode=register&role=investor",
        "requires_inventory_match": True,
        "requires_vintage_measurements": True,
        "requires_producer_acceptance": True,
        "submission_requires_user_confirmation": True,
        "credentials_entered_by_user_only": True,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
