"""Human-readable Component Atlas suitability reports."""

from __future__ import annotations


def build_component_suitability_table(atlas: dict) -> dict:
    if not isinstance(atlas, dict) or atlas.get("status") != "reviewed":
        raise ValueError("component suitability report requires a reviewed atlas")
    rows = []
    for component in atlas.get("components", []):
        count = component.get("parameters", {}).get("element_count", {})
        data = component.get("data_contract", {})
        guidance = component.get("page_guidance", {})
        adaptation = component.get("adaptation_contract", {})
        responsive = adaptation.get("responsive", {})
        background = adaptation.get("background", {})
        density = adaptation.get("density", {})
        rows.append({
            "component_id": component.get("component_id"),
            "family": component.get("family"),
            "source_slide": component.get("slide_index"),
            "suitable_scenarios": component.get("semantic_uses", []),
            "topologies": component.get("topologies", []),
            "archetypes": component.get("archetypes", []),
            "composition_roles": component.get("composition_roles", []),
            "data_kinds": data.get("kinds", ["none"]),
            "chart_types": data.get("chart_types", []),
            "data_capacity": {
                key: data.get(key) for key in (
                    "max_series", "max_categories", "max_rows", "max_columns",
                ) if data.get(key) is not None
            },
            "element_capacity": {"minimum": count.get("minimum"), "maximum": count.get("maximum")},
            "required_slots": component.get("semantic_contract", {}).get("required_fields", []),
            "text_capacity": component.get("text_capacity", {}),
            "native_fidelity": component.get("native_fidelity"),
            "renderer": component.get("renderer", "native_component"),
            "can_stand_alone": guidance.get("can_stand_alone"),
            "supported_page_roles": guidance.get("supported_page_roles", []),
            "minimum_information_units": guidance.get("minimum_information_units"),
            "recommended_page_recipes": guidance.get("recommended_page_recipes", []),
            "required_companion_roles": guidance.get("required_companion_roles", []),
            "recommended_companion_families": guidance.get(
                "recommended_companion_families", []
            ),
            "annotation_requirements": guidance.get("annotation_requirements", []),
            "prohibited_scenarios": guidance.get("prohibited_scenarios", []),
            "content_bbox": adaptation.get("content_bbox"),
            "decoration_bbox": adaptation.get("decoration_bbox"),
            "background_policy": background.get("policy"),
            "background_shape_names": background.get("shape_names", []),
            "responsive_modes": responsive.get("modes", []),
            "supported_aspect_ratio": responsive.get("supported_aspect_ratio"),
            "minimum_label_chars": density.get("minimum_label_chars"),
            "minimum_numeric_annotations": density.get("minimum_numeric_annotations"),
            "preferred_aspect_ratios": adaptation.get("preferred_aspect_ratios", []),
            "series_role": adaptation.get("series_role"),
        })
    return {"schema_version": "1.0.0", "component_count": len(rows), "rows": rows}


def render_component_suitability_markdown(report: dict) -> str:
    lines = [
        "# Template Component Suitability Table", "",
        "| Component | Family | Suitable scenarios | Page role | Stand-alone | Page recipes | Companions | Capacity | Data/annotation | Background | Responsive | Prohibited | Source |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---:|",
    ]
    for row in report.get("rows", []):
        capacity = row.get("element_capacity", {})
        element_range = f"{capacity.get('minimum')}–{capacity.get('maximum')}"
        data = ", ".join(row.get("data_kinds", []))
        charts = row.get("chart_types", [])
        if charts:
            data += " (" + ", ".join(charts) + ")"
        annotation = ", ".join(row.get("annotation_requirements", []))
        data_and_annotation = data + (f"; {annotation}" if annotation else "")
        companions = ", ".join(
            [*row.get("required_companion_roles", []),
             *row.get("recommended_companion_families", [])]
        )
        values = [
            row.get("component_id", ""), row.get("family", ""),
            "; ".join(row.get("suitable_scenarios", [])),
            ", ".join(row.get("supported_page_roles", [])),
            "yes" if row.get("can_stand_alone") is True else "no",
            ", ".join(row.get("recommended_page_recipes", [])), companions,
            f"elements {element_range}; min info {row.get('minimum_information_units', '')}",
            data_and_annotation,
            row.get("background_policy", ""),
            ", ".join(row.get("responsive_modes", [])),
            "; ".join(row.get("prohibited_scenarios", [])),
            str(row.get("source_slide", "")),
        ]
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in values) + " |")
    return "\n".join(lines) + "\n"
