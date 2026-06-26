from __future__ import annotations

import time
from typing import Any

from capacities_cache import load_lookup_cache, load_structures_cache, save_lookup_cache
from capacities_client import load_config, lookup


RELATED_TERMS: dict[str, list[str]] = {
    "recovery": ["sleep", "hydration", "mobility", "protocol"],
    "protocol": ["recovery", "routine", "plan"],
    "meeting": ["1:1", "sync", "review"],
    "meetings": ["1:1", "sync", "review"],
    "project": ["projects", "roadmap", "plan"],
    "projects": ["project", "roadmap", "plan"],
}

MATCH_ORDER = {"exact": 0, "prefix": 1, "substring": 2, "fallback": 3}
LOOKUP_CACHE_VERSION = 4

INTENT_TYPE_PREFERENCES: dict[str, list[str]] = {
    "note": ["note", "reference", "page", "knowledge", "pdf", "file"],
    "meeting": ["meeting", "note", "reference"],
    "project": ["project", "page", "knowledge", "note", "reference"],
    "person": ["person"],
}

GENERIC_TYPE_ALIASES: dict[str, list[str]] = {
    "people": ["person"],
    "person": ["person"],
    "notes": ["note"],
    "note": ["note"],
    "meetings": ["meeting"],
    "meeting": ["meeting"],
    "projects": ["project"],
    "project": ["project"],
    "references": ["reference"],
    "reference": ["reference"],
    "pages": ["page"],
    "page": ["page"],
    "tags": ["tag"],
    "tag": ["tag"],
    "tasks": ["task"],
    "task": ["task"],
    "books": ["book"],
    "book": ["book"],
    "organizations": ["organization"],
    "organization": ["organization"],
    "emails": ["email"],
    "email": ["email"],
    "courses": ["course"],
    "course": ["course"],
    "recipes": ["recipe"],
    "recipe": ["recipe"],
}

STOPWORDS = {
    "find", "my", "on", "about", "for", "that", "the", "a", "an", "do", "does", "is",
    "are", "part", "of", "at", "in", "with", "who", "what", "give", "me", "show", "all",
    "any", "related", "from", "to", "named", "called",
}


def build_deep_link(space_id: str, object_id: str) -> str:
    return f"capacities://{space_id}/{object_id}"


def _normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def _match_kind(search_term: str, title: str) -> str:
    s = _normalize_text(search_term)
    t = _normalize_text(title)
    if t == s:
        return "exact"
    if t.startswith(s) and s:
        return "prefix"
    if s and s in t:
        return "substring"
    return "fallback"


def _query_role(term: str, primary_term: str) -> str:
    return "primary" if _normalize_text(term) == _normalize_text(primary_term) else "related"


def _structure_penalty(structure_id: str | None) -> int:
    if structure_id == "RootSpace":
        return 3
    if structure_id == "RootStructure":
        return 2
    if structure_id == "RootTag":
        return 1
    return 0


def _baseline_type_penalty(structure_label: str | None) -> int:
    label = (structure_label or "").lower()
    if label in {"note", "reference", "meeting", "project", "page", "knowledge", "person", "pdf", "file", "organization", "email", "book", "task", "course", "recipe"}:
        return 0
    if label in {"tag", "query"}:
        return 2
    return 1


def _detect_intent(search_term: str) -> str | None:
    s = _normalize_text(search_term)
    if any(phrase in s for phrase in ["notes on", "note on", "my notes on", "find my notes", "find my note", "notes about", "note about"]):
        return "note"
    if any(phrase in s for phrase in ["meeting with", "meeting note", "meetings about", "1:1 with"]):
        return "meeting"
    if any(phrase in s for phrase in ["project", "projects", "roadmap"]):
        return "project"
    if any(phrase in s for phrase in ["people", "person", "who is", "who are"]):
        return "person"
    return None


def _extract_core_query(search_term: str) -> str:
    s = _normalize_text(search_term)
    prefixes = [
        "find my notes on ", "find my note on ", "my notes on ", "my note on ", "notes on ", "note on ",
        "find my notes about ", "find my note about ", "notes about ", "note about ",
        "find my notes for ", "find my note for ", "notes for ", "note for ",
        "find people at ", "find people in ", "find people from ", "find people that are part of ",
        "people at ", "people in ", "people from ", "people that are part of ",
        "who is at ", "who is in ", "who are at ", "who are in ",
    ]
    for prefix in prefixes:
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return search_term.strip()


def _build_type_phrase_map(structures_by_id: dict[str, Any]) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for structure in structures_by_id.values():
        title = _normalize_text(structure.get("title") or "")
        plural = _normalize_text(structure.get("pluralName") or "")
        for phrase in [title, plural]:
            if not phrase:
                continue
            mapping.setdefault(phrase, [])
            if title and title not in mapping[phrase]:
                mapping[phrase].append(title)
    for alias, labels in GENERIC_TYPE_ALIASES.items():
        mapping.setdefault(alias, [])
        for label in labels:
            if label not in mapping[alias]:
                mapping[alias].append(label)
    return mapping


def _detect_requested_types(search_term: str, structures_by_id: dict[str, Any]) -> list[str]:
    normalized = _normalize_text(search_term)
    phrase_map = _build_type_phrase_map(structures_by_id)
    requested: list[str] = []
    for phrase in sorted(phrase_map.keys(), key=len, reverse=True):
        if not phrase:
            continue
        if phrase in normalized:
            for label in phrase_map[phrase]:
                if label not in requested:
                    requested.append(label)
    return requested


def _strip_requested_type_phrases(search_term: str, structures_by_id: dict[str, Any]) -> str:
    normalized = _normalize_text(search_term)
    phrase_map = _build_type_phrase_map(structures_by_id)
    for phrase in sorted(phrase_map.keys(), key=len, reverse=True):
        if not phrase:
            continue
        normalized = normalized.replace(phrase, " ")
    tokens = [t for t in normalized.split() if t not in STOPWORDS]
    return " ".join(tokens).strip()


def _type_penalty(structure_label: str | None, intent: str | None, requested_types: list[str]) -> int:
    label = (structure_label or "").lower()
    if requested_types:
        if label in requested_types:
            return requested_types.index(label)
        if label in {"tag", "query"}:
            return len(requested_types) + 4
        return len(requested_types) + 2
    if intent:
        preferred = INTENT_TYPE_PREFERENCES.get(intent, [])
        if label in preferred:
            return preferred.index(label)
        if label in {"tag", "query"}:
            return len(preferred) + 3
        return len(preferred) + 1
    return _baseline_type_penalty(structure_label)


def _expansion_terms(search_term: str) -> list[str]:
    normalized = _normalize_text(search_term)
    terms: list[str] = [search_term]

    if normalized in RELATED_TERMS:
        terms.extend(RELATED_TERMS[normalized])

    for token in normalized.split():
        if token in RELATED_TERMS:
            for term in RELATED_TERMS[token]:
                if term not in terms:
                    terms.append(term)

    seen: set[str] = set()
    unique_terms: list[str] = []
    for term in terms:
        key = _normalize_text(term)
        if not key or key in seen:
            continue
        seen.add(key)
        unique_terms.append(term)
    return unique_terms


def normalize_lookup_results(
    raw_results: list[dict[str, Any]],
    structures_by_id: dict[str, Any],
    space_id: str,
    matched_on: str,
    primary_search_term: str,
    intent: str | None,
    requested_types: list[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in raw_results:
        structure_id = item.get("structureId")
        structure = structures_by_id.get(structure_id, {})
        structure_label = _normalize_text(structure.get("title") or structure_id or "unknown")
        object_id = item.get("id")
        title = item.get("title")
        results.append(
            {
                "id": object_id,
                "title": title,
                "structureId": structure_id,
                "structureLabel": structure.get("title") or structure_id or "Unknown",
                "deepLink": build_deep_link(space_id, object_id),
                "matchedOn": matched_on,
                "queryRole": _query_role(matched_on, primary_search_term),
                "matchKind": _match_kind(matched_on, title or ""),
                "intent": intent,
                "requestedTypes": requested_types,
                "structurePenalty": _structure_penalty(structure_id),
                "preferredTypePenalty": _type_penalty(structure_label, intent, requested_types),
            }
        )
    return results


def _ranking_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return (
        item.get("preferredTypePenalty", 0),
        0 if item.get("queryRole") == "primary" else 1,
        MATCH_ORDER.get(item.get("matchKind"), 99),
        item.get("structurePenalty", 0),
        len(item.get("title") or ""),
        (item.get("title") or "").lower(),
    )


def rank_lookup_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for item in results:
        object_id = item.get("id")
        if not object_id:
            continue
        existing = deduped.get(object_id)
        if existing is None or _ranking_key(item) < _ranking_key(existing):
            deduped[object_id] = item
        else:
            matched_terms = set(existing.get("allMatchedTerms", [existing.get("matchedOn")]))
            if item.get("matchedOn"):
                matched_terms.add(item.get("matchedOn"))
            existing["allMatchedTerms"] = sorted(matched_terms)

    ranked = list(deduped.values())
    for item in ranked:
        if "allMatchedTerms" not in item:
            item["allMatchedTerms"] = [item.get("matchedOn")]
    ranked.sort(key=_ranking_key)
    return ranked


def _cache_key(space_id: str, search_term: str, include_structures: bool, expand_related: bool) -> str:
    return f"v={LOOKUP_CACHE_VERSION}::{space_id}::{_normalize_text(search_term)}::include_structures={include_structures}::expand_related={expand_related}"


def lookup_with_metadata(
    search_term: str,
    use_cache: bool = True,
    include_structures: bool = False,
    expand_related: bool = True,
) -> dict[str, Any]:
    config = load_config()
    space_id = config["mainSpaceId"]
    cache_ttl = int(config.get("lookupCacheTtlSeconds", 86400))
    cache = load_lookup_cache()
    key = _cache_key(space_id, search_term, include_structures, expand_related)
    now = int(time.time())

    if use_cache:
        entry = cache.get(key)
        if entry and int(entry.get("expiresAt", 0)) > now:
            return entry["value"]

    structures_cache = load_structures_cache()
    structures_by_id = structures_cache.get("structuresById", {})

    intent = _detect_intent(search_term)
    extracted_core = _extract_core_query(search_term)
    requested_types = _detect_requested_types(search_term, structures_by_id)
    stripped_core = _strip_requested_type_phrases(extracted_core, structures_by_id)
    core_query = stripped_core or extracted_core or search_term.strip()

    query_terms = [core_query]
    if expand_related:
        query_terms = _expansion_terms(core_query)

    combined_results: list[dict[str, Any]] = []
    for term in query_terms:
        raw = lookup(space_id, term)
        combined_results.extend(
            normalize_lookup_results(
                raw.get("results", []),
                structures_by_id,
                space_id,
                matched_on=term,
                primary_search_term=core_query,
                intent=intent,
                requested_types=requested_types,
            )
        )

    ranked = rank_lookup_results(combined_results)

    if not include_structures:
        ranked = [r for r in ranked if r.get("structureId") not in {"RootStructure", "RootSpace"}]

    requested_type_results = []
    fallback_results = []
    if requested_types:
        requested_type_results = [r for r in ranked if (r.get("structureLabel") or "").lower() in requested_types]
        fallback_results = [r for r in ranked if (r.get("structureLabel") or "").lower() not in requested_types]

    limit = int(config.get("defaultResultLimit", 10))
    result = {
        "searchTerm": search_term,
        "coreQuery": core_query,
        "intent": intent,
        "requestedTypes": requested_types,
        "spaceId": space_id,
        "resultCount": len(ranked),
        "includeStructures": include_structures,
        "expandRelated": expand_related,
        "queryTerms": query_terms,
        "requestedTypeFound": (len(requested_type_results) > 0) if requested_types else None,
        "requestedTypeResultCount": len(requested_type_results) if requested_types else None,
        "fallbackResultCount": len(fallback_results) if requested_types else None,
        "results": ranked[:limit],
        "fallbackResults": fallback_results[: min(5, limit)] if requested_types and not requested_type_results else [],
    }

    cache[key] = {
        "cachedAt": now,
        "expiresAt": now + cache_ttl,
        "value": result,
    }
    save_lookup_cache(cache)
    return result
