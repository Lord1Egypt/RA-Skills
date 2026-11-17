"""Build read-only Zotero synchronization and metadata-audit plans.

This module never connects to Zotero or external metadata providers. It
combines wiki ``sources_meta`` bindings with an optional MCP-produced snapshot
so an Agent can review a deterministic plan before performing Zotero writes
through the configured MCP integration.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..core import WikiManager

ACADEMIC_ITEM_TYPES = {
    "academic_paper",
    "conferencePaper",
    "journalArticle",
    "preprint",
}
MANAGED_TAG_PREFIX = "llm-wiki:"
PRESERVED_MANAGED_TAGS = {"llm-wiki:index-card"}


@dataclass(frozen=True)
class ZoteroBinding:
    """One wiki page's provenance binding to a Zotero item."""

    item_key: str
    page_stem: str
    page_title: str
    source_title: str
    source_type: str
    page_active: bool
    ingest_complete: bool
    doi: str = ""
    arxiv: str = ""
    citation_key: str = ""
    library_id: str = ""
    page_tags: tuple[str, ...] = ()

    @property
    def page_tag(self) -> str:
        """退役的页面级绑定标签(2026-08-28 起不再写入,仅用于识别历史残留)。"""
        return f"{MANAGED_TAG_PREFIX}{self.page_stem}"


def managed_topic_tags(
    tags: Iterable[str], collection_name: str = ""
) -> frozenset[str]:
    """把 wiki 页面主题标签投影为共享托管标签。

    - 逐值加 ``llm-wiki:`` 前缀,使同主题条目在 Zotero 标签选择器中聚合;
    - 跳过与目标集合同名的标签(集合成员关系已表达该范围);
    - 空值忽略。
    """
    projected = set()
    for tag in tags:
        name = str(tag).strip()
        if not name:
            continue
        if collection_name and name.casefold() == collection_name.casefold():
            continue
        projected.add(f"{MANAGED_TAG_PREFIX}{name}")
    return frozenset(projected)


@dataclass(frozen=True)
class SnapshotItem:
    """Minimal Zotero item state exported through MCP for planning."""

    item_key: str
    title: str
    item_type: str
    date: str = ""
    doi: str = ""
    doi_observed: bool = False
    arxiv: str = ""
    url: str = ""
    citation_key: str = ""
    tags: frozenset[str] = frozenset()
    tags_observed: bool = False
    collections: tuple[str, ...] = ()
    related_items: tuple[str, ...] = ()


@dataclass(frozen=True)
class ZoteroPlanItem:
    """Desired and observed state for one Zotero item."""

    item_key: str
    title: str
    item_type: str
    wiki_pages: tuple[str, ...]
    desired_tags: frozenset[str]
    current_tags: frozenset[str]
    add_tags: frozenset[str]
    remove_candidates: frozenset[str]
    relation_candidates: tuple[str, ...]
    doi: str
    doi_state: str
    actions: tuple[str, ...]


@dataclass(frozen=True)
class ZoteroPlan:
    """Read-only collection synchronization plan."""

    library_id: str
    collection_name: str
    collection_key: str
    items: tuple[ZoteroPlanItem, ...]
    warnings: tuple[str, ...] = ()


def normalize_doi(value: Any) -> str:
    """Normalize a DOI value without attempting network verification."""
    text = str(value or "").strip()
    text = re.sub(
        r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", text, flags=re.IGNORECASE
    )
    return text.rstrip(". ,;)").strip()


def _normalize_tags(raw_tags: Any) -> frozenset[str]:
    if raw_tags is None:
        return frozenset()
    if isinstance(raw_tags, str):
        return frozenset({raw_tags}) if raw_tags else frozenset()

    tags: set[str] = set()
    for raw in raw_tags:
        if isinstance(raw, Mapping):
            value = raw.get("tag", "")
        else:
            value = raw
        text = str(value or "").strip()
        if text:
            tags.add(text)
    return frozenset(tags)


def collect_zotero_bindings(wiki: WikiManager) -> list[ZoteroBinding]:
    """Collect stable Zotero item bindings from wiki ``sources_meta``."""
    bindings: list[ZoteroBinding] = []
    for page in wiki.list_pages():
        sources_meta = page.frontmatter.get("sources_meta") or []
        if not isinstance(sources_meta, list):
            continue

        coverage_verified = page.frontmatter.get("coverage_verified") is True
        page_active = page.status == "active"
        for source in sources_meta:
            if not isinstance(source, Mapping):
                continue
            item_key = str(source.get("zotero_item_key") or "").strip()
            if not item_key:
                continue
            bindings.append(
                ZoteroBinding(
                    item_key=item_key,
                    page_stem=page.path.stem,
                    page_title=page.title,
                    source_title=str(source.get("title") or page.title),
                    source_type=str(source.get("type") or ""),
                    page_active=page_active,
                    ingest_complete=page_active and coverage_verified,
                    doi=normalize_doi(source.get("doi")),
                    arxiv=str(source.get("arxiv") or "").strip(),
                    citation_key=str(source.get("citation_key") or "").strip(),
                    library_id=str(source.get("library_id") or "").strip(),
                    page_tags=tuple(str(tag) for tag in page.tags),
                )
            )
    return bindings


def load_snapshot(path: Path) -> tuple[str, str, str, list[SnapshotItem]]:
    """Load a versioned MCP-produced Zotero snapshot from YAML or JSON."""
    path = Path(path)
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    if data.get("version") != 1:
        raise ValueError("snapshot must declare version: 1")

    collection = data.get("collection") or {}
    if not isinstance(collection, Mapping):
        raise TypeError("snapshot collection must be a mapping")

    items_raw = data.get("items") or []
    if not isinstance(items_raw, list):
        raise TypeError("snapshot items must be a list")

    items: list[SnapshotItem] = []
    seen_keys: set[str] = set()
    for raw in items_raw:
        if not isinstance(raw, Mapping):
            raise TypeError("each snapshot item must be a mapping")
        item_key = str(raw.get("item_key") or "").strip()
        if not item_key:
            raise ValueError("snapshot item is missing item_key")
        if item_key in seen_keys:
            raise ValueError(f"duplicate snapshot item_key: {item_key}")
        seen_keys.add(item_key)

        collections_raw = raw.get("collections") or []
        if isinstance(collections_raw, str):
            collections = (collections_raw,)
        else:
            collections = tuple(str(value) for value in collections_raw)

        related_raw = raw.get("related_items") or []
        if isinstance(related_raw, str):
            related_items = (related_raw,)
        else:
            related_items = tuple(str(value) for value in related_raw)

        items.append(
            SnapshotItem(
                item_key=item_key,
                title=str(raw.get("title") or item_key),
                item_type=str(raw.get("item_type") or ""),
                date=str(raw.get("date") or ""),
                doi=normalize_doi(raw.get("doi")),
                doi_observed="doi" in raw,
                arxiv=str(raw.get("arxiv") or "").strip(),
                url=str(raw.get("url") or "").strip(),
                citation_key=str(raw.get("citation_key") or "").strip(),
                tags=_normalize_tags(raw.get("tags")),
                tags_observed="tags" in raw,
                collections=collections,
                related_items=related_items,
            )
        )

    return (
        str(data.get("library_id") or ""),
        str(collection.get("name") or ""),
        str(collection.get("key") or ""),
        items,
    )


def extract_doi_from_text(value: Any) -> str:
    """Extract a DOI-looking identifier from a URL or metadata string."""
    match = re.search(r"10\.\d{4,9}/[^\s?#]+", str(value or ""), flags=re.IGNORECASE)
    return normalize_doi(match.group(0)) if match else ""


def _doi_state(
    item: SnapshotItem, bindings: Sequence[ZoteroBinding]
) -> tuple[str, str]:
    binding_doi = next((binding.doi for binding in bindings if binding.doi), "")
    url_doi = extract_doi_from_text(item.url)

    if item.doi:
        conflicts = [candidate for candidate in (binding_doi, url_doi) if candidate]
        if any(item.doi.casefold() != candidate.casefold() for candidate in conflicts):
            return item.doi, "conflict"
        if item.doi.lower().startswith("10.48550/arxiv."):
            return item.doi, "arxiv-doi"
        return item.doi, "recorded"

    if binding_doi and url_doi and binding_doi.casefold() != url_doi.casefold():
        return binding_doi, "conflict"
    if url_doi:
        return url_doi, "url-candidate"
    if item.doi_observed:
        if binding_doi:
            return binding_doi, "wiki-candidate"
        return "", "missing"
    if binding_doi:
        return binding_doi, "wiki-recorded"
    return "", "unknown"


def _normalize_work_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def build_zotero_plan(
    bindings: Iterable[ZoteroBinding],
    snapshot_items: Sequence[SnapshotItem] | None = None,
    *,
    library_id: str = "",
    collection_name: str = "",
    collection_key: str = "",
    item_keys: set[str] | None = None,
) -> ZoteroPlan:
    """Build a deterministic, non-mutating Zotero sync and audit plan."""
    binding_map: dict[str, list[ZoteroBinding]] = {}
    all_bindings = list(bindings)
    for binding in all_bindings:
        if item_keys and binding.item_key not in item_keys:
            continue
        binding_map.setdefault(binding.item_key, []).append(binding)

    # 托管标签全集 = 主题投影 ∪ 退役的页面绑定标签(后者仅用于识别历史残留)
    known_managed_tags = {binding.page_tag for binding in all_bindings}
    for binding in all_bindings:
        known_managed_tags.update(
            managed_topic_tags(binding.page_tags, collection_name)
        )
    if snapshot_items is None:
        snapshot_items = [
            SnapshotItem(
                item_key=item_key,
                title=group[0].source_title,
                item_type=group[0].source_type,
                doi=next((binding.doi for binding in group if binding.doi), ""),
                doi_observed=True,
                arxiv=next((binding.arxiv for binding in group if binding.arxiv), ""),
            )
            for item_key, group in sorted(binding_map.items())
        ]

    selected_items = [
        item for item in snapshot_items if not item_keys or item.item_key in item_keys
    ]
    warnings: list[str] = []
    if collection_name and not collection_key:
        warnings.append("Collection name is present but collection key is missing.")

    title_groups: dict[str, list[SnapshotItem]] = {}
    for item in selected_items:
        normalized_title = _normalize_work_title(item.title)
        if normalized_title:
            title_groups.setdefault(normalized_title, []).append(item)

    relation_candidates: dict[str, set[str]] = {}
    for group in title_groups.values():
        if len(group) < 2:
            continue
        has_preprint = any(item.item_type == "preprint" for item in group)
        has_published = any(
            item.item_type in {"conferencePaper", "journalArticle"} for item in group
        )
        if not (has_preprint and has_published):
            continue
        for item in group:
            existing = set(item.related_items)
            candidates = {
                other.item_key
                for other in group
                if other.item_key != item.item_key and other.item_key not in existing
            }
            if candidates:
                relation_candidates[item.item_key] = candidates

    plans: list[ZoteroPlanItem] = []
    for item in selected_items:
        item_bindings = binding_map.get(item.item_key, [])
        desired_tags: set[str] = set()
        for binding in item_bindings:
            desired_tags.update(managed_topic_tags(binding.page_tags, collection_name))
        if any(binding.ingest_complete for binding in item_bindings):
            desired_tags.add("llm-wiki:ingested")

        current_tags = set(item.tags)
        add_tags = desired_tags - current_tags if item.tags_observed else set()

        remove_candidates: set[str] = set()
        if item.tags_observed:
            if item_bindings:
                remove_candidates.update(
                    tag
                    for tag in current_tags
                    if tag in known_managed_tags and tag not in desired_tags
                )
            if collection_name:
                collection_equivalents = {
                    collection_name.casefold(),
                    f"{MANAGED_TAG_PREFIX}{collection_name}".casefold(),
                }
                remove_candidates.update(
                    tag
                    for tag in current_tags
                    if tag.casefold() in collection_equivalents
                )
            remove_candidates.difference_update(PRESERVED_MANAGED_TAGS)

        doi, doi_state = _doi_state(item, item_bindings)
        actions: list[str] = []
        if item.item_type in ACADEMIC_ITEM_TYPES:
            if doi_state == "unknown":
                actions.append("read DOI field from Zotero")
            elif doi_state == "missing":
                actions.append("search DOI candidate")
            elif doi_state == "arxiv-doi":
                actions.append("check for published version")
            elif doi_state == "url-candidate":
                actions.append("verify DOI candidate from URL")
            elif doi_state == "wiki-candidate":
                actions.append("verify DOI candidate from wiki provenance")
            elif doi_state == "wiki-recorded":
                actions.append("read DOI field and verify wiki DOI")
            elif doi_state == "conflict":
                actions.append("review DOI/URL conflict")
            else:
                actions.append("verify DOI metadata")
            if item.item_type == "preprint":
                actions.append("check preprint-to-publication relation")

        if not item.tags_observed:
            actions.append("read current tags from Zotero")
        elif add_tags:
            actions.append("add managed tags")
        if remove_candidates:
            actions.append("review tag removals")
        item_relation_candidates = tuple(
            sorted(relation_candidates.get(item.item_key, set()))
        )
        if item_relation_candidates:
            actions.append("review same-title preprint/published relation")
        if not item_bindings:
            actions.append("not linked from wiki sources_meta")

        plans.append(
            ZoteroPlanItem(
                item_key=item.item_key,
                title=item.title,
                item_type=item.item_type,
                wiki_pages=tuple(
                    sorted(binding.page_stem for binding in item_bindings)
                ),
                desired_tags=frozenset(desired_tags),
                current_tags=frozenset(current_tags),
                add_tags=frozenset(add_tags),
                remove_candidates=frozenset(remove_candidates),
                relation_candidates=item_relation_candidates,
                doi=doi,
                doi_state=doi_state,
                actions=tuple(actions),
            )
        )

    if snapshot_items is not None:
        snapshot_keys = {item.item_key for item in selected_items}
        stale_keys = sorted(
            {binding.item_key for binding in all_bindings} - snapshot_keys
        )
        if stale_keys:
            warnings.append(
                f"{len(stale_keys)} wiki binding(s) reference item keys absent from "
                f"the snapshot ({', '.join(stale_keys)}); run `zotero-heal --snapshot` "
                "to diagnose and rebind stale keys."
            )

    return ZoteroPlan(
        library_id=library_id,
        collection_name=collection_name,
        collection_key=collection_key,
        items=tuple(plans),
        warnings=tuple(warnings),
    )


def plan_to_manifest(plan: ZoteroPlan) -> dict[str, Any]:
    """Serialize a plan into an explicit, review-only mutation manifest."""
    mutations: list[dict[str, Any]] = []
    for item in plan.items:
        mutation: dict[str, Any] = {
            "item_key": item.item_key,
            "title": item.title,
        }
        if item.add_tags:
            mutation["add_tags"] = sorted(item.add_tags)
        if item.remove_candidates:
            mutation["remove_tags_review"] = sorted(item.remove_candidates)
        if item.relation_candidates:
            mutation["relation_candidates_review"] = list(item.relation_candidates)
        if item.doi_state != "recorded":
            mutation["metadata_review"] = {
                "doi": item.doi,
                "doi_state": item.doi_state,
            }
        if len(mutation) > 2:
            mutations.append(mutation)

    return {
        "version": 1,
        "mode": "review-only",
        "library_id": plan.library_id,
        "collection": {
            "name": plan.collection_name,
            "key": plan.collection_key,
        },
        "mutations": mutations,
    }


def build_retired_binding_removal_plan(
    plan: ZoteroPlan,
    bindings: Iterable[ZoteroBinding],
) -> dict[str, Any]:
    """Build an authorized-write plan removing ONLY retired page-stem binding tags.

    A tag is whitelisted for removal only when it is some binding's retired
    ``page_tag`` (``llm-wiki:<page_stem>``) and is not also a live topic
    projection of any binding. Topic tags, ``llm-wiki:ingested``, preserved
    tags, and unmanaged user tags are never proposed. The result still requires
    human review and a separate ``zotero-writeback`` apply; the write-back
    loader re-checks every removal against its own managed-tag guardrails.

    Requires ``plan.collection_key`` (a snapshot-backed plan) so each item can
    declare ``expected_collections``; raises ``ValueError`` otherwise.
    """
    if not plan.collection_key:
        raise ValueError(
            "retired-binding removal plan requires a snapshot-backed collection key"
        )

    all_bindings = list(bindings)
    retired = {binding.page_tag for binding in all_bindings}
    live_topics: set[str] = set()
    for binding in all_bindings:
        live_topics |= managed_topic_tags(binding.page_tags, plan.collection_name)
    whitelist = (
        retired
        - live_topics
        - PRESERVED_MANAGED_TAGS
        - {f"{MANAGED_TAG_PREFIX}ingested"}
    )

    items: list[dict[str, Any]] = []
    for item in plan.items:
        removable = sorted(item.remove_candidates & whitelist)
        if not removable:
            continue
        items.append(
            {
                "item_key": item.item_key,
                "expected_collections": [plan.collection_key],
                "desired_managed_tags": [],
                "reviewed_removals": removable,
                "reviewed_relations": [],
            }
        )

    return {
        "version": 1,
        "mode": "authorized-write",
        "library_id": plan.library_id,
        "collection": {
            "key": plan.collection_key,
            "name": plan.collection_name,
        },
        "policy": {
            "preserve_existing_tags": True,
            "replace_tags": False,
            "write_notes": False,
            "change_collections": False,
            "change_metadata": False,
            "relation_policy": "reviewed-only",
            "allow_managed_removals": True,
        },
        "items": items,
    }
