"""Fail-closed family-diversity checks for Template-route body pages."""

from __future__ import annotations


GENERIC_FAMILIES = frozenset({"card_grid", "icon_card_grid"})
MAX_CONSECUTIVE_FAMILY = 2
MAX_GENERIC_BODY_RATIO = 0.35


def _page_family(page: dict) -> str | None:
    family = page.get("family")
    if isinstance(family, str):
        return family
    families = page.get("families")
    if isinstance(families, list):
        distinct = {
            item for item in families
            if isinstance(item, str) and item
        }
        if len(distinct) == 1:
            return next(iter(distinct))
    return None


def evaluate_family_diversity(pages: list[dict]) -> dict:
    """Report repeated component families without treating a style as a topology."""
    body = [page for page in pages if page.get("archetype", "body") == "body"]
    issues: list[dict] = []
    current_family: str | None = None
    run_start = 0
    for index, page in enumerate(body, 1):
        family = _page_family(page)
        if family != current_family:
            current_family, run_start = family, index
        if isinstance(family, str) and index - run_start + 1 == MAX_CONSECUTIVE_FAMILY + 1:
            issues.append({
                "code": "COMPONENT_FAMILY_CONSECUTIVE_LIMIT",
                "family": family,
                "first_page_index": run_start,
                "last_page_index": index,
            })
    generic_count = sum(_page_family(page) in GENERIC_FAMILIES for page in body)
    generic_ratio = round(generic_count / len(body), 4) if body else 0.0
    # A one- or two-page deck has no meaningful family distribution; the
    # delivery floor applies once there are enough body pages to diversify.
    if len(body) >= 3 and generic_ratio > MAX_GENERIC_BODY_RATIO:
        issues.append({
            "code": "GENERIC_COMPONENT_FAMILY_OVERUSED",
            "generic_family_ratio": generic_ratio,
            "maximum_ratio": MAX_GENERIC_BODY_RATIO,
        })
    return {
        "status": "pass" if not issues else "fail",
        "body_page_count": len(body),
        "generic_family_ratio": generic_ratio,
        "issues": issues,
    }
