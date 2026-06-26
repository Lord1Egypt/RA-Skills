#!/usr/bin/env python3
import json
import sys
from pathlib import Path

# local imports from sibling scripts
sys.path.insert(0, str(Path(__file__).resolve().parent))
import query_router  # type: ignore
import dynamic_guard  # type: ignore
import build_urls  # type: ignore
import score_result  # type: ignore
import search_report  # type: ignore


def derive_seed_scores(intent: str, is_dynamic: bool):
    # Conservative defaults for planning stage, before actual fetch/verification.
    source_level = 2 if is_dynamic else 3
    freshness = 2 if is_dynamic else 3
    cross_check = 2
    page_type = 2
    return source_level, freshness, cross_check, page_type


def prioritize_sites(intent: str, route: str, is_dynamic: bool, sites, urls):
    if is_dynamic:
        priority = [u["name"] for u in urls[:4]]
        return {
            "mode": "human-like-dynamic-priority",
            "why": "Dynamic queries should start from real-time or transaction-adjacent pages before broad search.",
            "priority": priority,
        }
    return {
        "mode": "standard",
        "why": "Use route-selected engines and site classes.",
        "priority": [u["name"] for u in urls[:4]] or sites,
    }


def build_plan(query: str):
    intent = query_router.detect_intent(query)
    route = query_router.detect_route(query, intent)
    sites = query_router.suggest_sites(intent, route)

    q = query.lower()
    matched = [k for k in dynamic_guard.DYNAMIC_KEYWORDS if k.lower() in q]
    is_dynamic = len(matched) > 0
    dynamic_subtype = dynamic_guard.detect_subtype(query) if is_dynamic else None
    guidance = dynamic_guard.guidance(is_dynamic)

    urls = build_urls.build(query, route, intent, dynamic_subtype)
    search_priority = prioritize_sites(intent, route, is_dynamic, sites, urls)

    seed = derive_seed_scores(intent, is_dynamic)
    total, band = score_result.score(*seed)

    conclusion = f"Query classified as {intent}; suggested route is {route}."
    key_points = [
        f"Suggested sites: {', '.join(sites)}",
        f"Generated {len(urls)} starter URLs",
        f"Priority order: {', '.join(search_priority['priority'])}",
    ]
    if is_dynamic:
        key_points.append("Dynamic-info guard triggered; final decision should rely on real-time pages.")
        if dynamic_subtype:
            key_points.append(f"Dynamic subtype: {dynamic_subtype}")

    markdown = search_report.build_markdown(
        route,
        primary=urls[0]['name'] if urls else 'N/A',
        cross_check=urls[1]['name'] if len(urls) > 1 else 'N/A',
        reliability=band,
        conclusion=conclusion,
        points=key_points,
    )

    return {
        "query": query,
        "intent": intent,
        "route": route,
        "isDynamic": is_dynamic,
        "dynamicSubtype": dynamic_subtype,
        "matchedDynamicKeywords": matched,
        "guidance": guidance,
        "suggestedSites": sites,
        "searchPriority": search_priority,
        "starterUrls": urls,
        "seedReliability": {
            "sourceLevel": seed[0],
            "freshness": seed[1],
            "crossCheck": seed[2],
            "pageType": seed[3],
            "total": total,
            "reliability": band,
            "note": "Planning-stage seed score only; rerun with real evidence after search."
        },
        "reportMarkdown": markdown,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: run_search_workflow.py <query>", file=sys.stderr)
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    print(json.dumps(build_plan(query), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
