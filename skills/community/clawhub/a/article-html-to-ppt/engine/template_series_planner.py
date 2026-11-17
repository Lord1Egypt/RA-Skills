"""Template-route series planning and main-narrative limits."""

from __future__ import annotations

from collections import Counter, defaultdict


SERIES_PURPOSES = frozenset({"comparison", "sequence", "appendix"})
NARRATIVE_TIERS = frozenset({"main", "appendix"})


def evaluate_template_series(page_reports: list[dict]) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    issues: list[dict] = []
    for page in page_reports:
        context = page.get("series_context")
        if context is None:
            continue
        slide_id = page.get("slide_id")
        if not isinstance(context, dict):
            issues.append({"code": "TEMPLATE_SERIES_CONTEXT_INVALID", "slide_id": slide_id})
            continue
        group_id = context.get("group_id")
        purpose = context.get("purpose")
        tier = context.get("narrative_tier", "main")
        position = context.get("position")
        total = context.get("total")
        hero = context.get("hero_visual_type")
        if (
            not isinstance(group_id, str) or not group_id
            or purpose not in SERIES_PURPOSES
            or tier not in NARRATIVE_TIERS
            or isinstance(position, bool) or not isinstance(position, int) or position < 1
            or isinstance(total, bool) or not isinstance(total, int) or total < 1
            or not isinstance(hero, str) or not hero
        ):
            issues.append({"code": "TEMPLATE_SERIES_CONTEXT_INVALID", "slide_id": slide_id})
            continue
        groups[group_id].append({"slide_id": slide_id, **context})

    summaries: list[dict] = []
    for group_id, pages in sorted(groups.items()):
        positions = [page["position"] for page in pages]
        totals = {page["total"] for page in pages}
        purposes = {page["purpose"] for page in pages}
        tiers = {page.get("narrative_tier", "main") for page in pages}
        heroes = Counter(page["hero_visual_type"] for page in pages)
        if len(set(positions)) != len(positions) or len(totals) != 1 or len(purposes) != 1:
            issues.append({"code": "TEMPLATE_SERIES_SEQUENCE_INVALID", "series_group_id": group_id})
        purpose = next(iter(purposes)) if len(purposes) == 1 else "invalid"
        if purpose == "comparison":
            anchors = {page.get("comparison_anchor") for page in pages}
            shared_scale = all(page.get("shared_scale") is True for page in pages)
            if None in anchors or len(anchors) != 1 or not shared_scale:
                issues.append({
                    "code": "TEMPLATE_COMPARISON_SERIES_ANCHOR_REQUIRED",
                    "series_group_id": group_id,
                })
        if "main" in tiers and len(pages) > 5:
            issues.append({
                "code": "TEMPLATE_SERIES_MAIN_NARRATIVE_TOO_LONG",
                "series_group_id": group_id,
                "page_count": len(pages),
                "maximum_main_narrative_pages": 5,
                "recommended_action": "consolidate into small multiples or move detail to appendix",
            })
        if purpose != "comparison" and max(heroes.values(), default=0) > 2:
            issues.append({
                "code": "TEMPLATE_SERIES_HERO_REPETITION",
                "series_group_id": group_id,
                "hero_visual_counts": dict(sorted(heroes.items())),
            })
        summaries.append({
            "series_group_id": group_id,
            "purpose": purpose,
            "page_count": len(pages),
            "positions": sorted(positions),
            "hero_visual_counts": dict(sorted(heroes.items())),
            "recommendation": (
                "retain comparable grid" if purpose == "comparison" and len(pages) <= 5
                else "consolidate or move detail to appendix" if len(pages) > 5
                else "vary hero visual while preserving the narrative sequence"
            ),
        })
    return {
        "status": "pass" if not issues else "fail",
        "series": summaries,
        "issues": issues,
    }
