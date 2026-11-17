"""Template-neutral semantic contracts for whole-page composition recipes."""

from __future__ import annotations


FOCUSED_ARCHETYPES = frozenset({"focused_message", "focused_evidence"})

PAGE_ARCHETYPES = {
    "focused_message": {
        "required_roles": {"primary_evidence"},
        "minimum_modules": 1, "minimum_information_units": 1,
    },
    "focused_evidence": {
        "required_roles": {"primary_evidence"},
        "minimum_modules": 1, "minimum_information_units": 2,
        "quantitative": True,
    },
    "executive_summary": {
        "required_roles": {"primary_evidence", "interpretation", "implication"},
        "minimum_modules": 3,
        "minimum_information_units": 6,
    },
    "data_evidence": {
        "required_roles": {"primary_evidence", "interpretation", "implication"},
        "minimum_modules": 3,
        "minimum_information_units": 5,
        "quantitative": True,
    },
    "mechanism": {
        "required_roles": {"primary_evidence", "interpretation", "implication"},
        "minimum_modules": 3,
        "minimum_information_units": 5,
    },
    "case_study": {
        "required_roles": {"context", "primary_evidence", "implication"},
        "minimum_modules": 3,
        "minimum_information_units": 6,
    },
    "comparison_series": {
        "required_roles": {"primary_evidence", "interpretation", "implication"},
        "minimum_modules": 3,
        "minimum_information_units": 5,
    },
    "action_framework": {
        "required_roles": {"primary_evidence", "implication"},
        "minimum_modules": 2,
        "minimum_information_units": 5,
    },
    "methodology": {
        "required_roles": {"primary_evidence", "interpretation"},
        "minimum_modules": 2,
        "minimum_information_units": 4,
    },
    "concept_framework": {
        "required_roles": {"primary_evidence", "interpretation"},
        "minimum_modules": 2,
        "minimum_information_units": 4,
    },
    "custom": {
        "required_roles": {"primary_evidence"},
        "minimum_modules": 2,
        "minimum_information_units": 4,
    },
}


def evaluate_template_page_recipe(
    contract: dict,
    *,
    slide_id: str,
    require_declaration: bool,
    is_quantitative: bool,
) -> dict:
    archetype = contract.get("composition_archetype")
    if not isinstance(archetype, str) or not archetype:
        return {
            "status": "fail" if require_declaration else "legacy",
            "composition_archetype": None,
            "issues": ([{
                "code": "TEMPLATE_PAGE_ARCHETYPE_REQUIRED",
                "slide_id": slide_id,
            }] if require_declaration else []),
        }
    definition = PAGE_ARCHETYPES.get(archetype)
    if definition is None:
        return {
            "status": "fail",
            "composition_archetype": archetype,
            "issues": [{
                "code": "TEMPLATE_PAGE_ARCHETYPE_UNKNOWN",
                "slide_id": slide_id,
                "composition_archetype": archetype,
                "allowed_archetypes": sorted(PAGE_ARCHETYPES),
            }],
        }

    modules = [
        module for module in contract.get("content_modules", [])
        if isinstance(module, dict)
        and module.get("role") not in {"navigation", "decoration"}
    ]
    roles = {module.get("role") for module in modules}
    units = sum(
        module.get("information_unit_count", 0)
        for module in modules
        if isinstance(module.get("information_unit_count"), int)
    )
    issues: list[dict] = []
    missing_roles = sorted(definition["required_roles"] - roles)
    if missing_roles:
        issues.append({
            "code": "TEMPLATE_PAGE_ARCHETYPE_ROLES_MISSING",
            "slide_id": slide_id,
            "composition_archetype": archetype,
            "missing_roles": missing_roles,
        })
    if len(modules) < definition["minimum_modules"]:
        issues.append({
            "code": "TEMPLATE_PAGE_ARCHETYPE_MODULES_LOW",
            "slide_id": slide_id,
            "composition_archetype": archetype,
            "module_count": len(modules),
            "minimum_modules": definition["minimum_modules"],
        })
    if units < definition["minimum_information_units"]:
        issues.append({
            "code": "TEMPLATE_PAGE_ARCHETYPE_INFORMATION_LOW",
            "slide_id": slide_id,
            "composition_archetype": archetype,
            "information_unit_count": units,
            "minimum_information_units": definition["minimum_information_units"],
        })
    if definition.get("quantitative") is True and not is_quantitative:
        issues.append({
            "code": "TEMPLATE_PAGE_ARCHETYPE_DATA_REQUIRED",
            "slide_id": slide_id,
            "composition_archetype": archetype,
        })
    return {
        "status": "pass" if not issues else "fail",
        "composition_archetype": archetype,
        "module_count": len(modules),
        "information_unit_count": units,
        "issues": issues,
    }
