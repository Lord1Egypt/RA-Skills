"""P1: Zotero 条目死链自愈 — 探测失效 → 二次寻址 → 原地修复。

Wiki frontmatter 的 ``sources_meta[].zotero_item_key`` 可能因 Zotero 条目合并、
重新导入或附件转换而悬空。本模块基于 MCP 产出的集合快照做确定性二次寻址
(DOI → citation_key → 标准化标题),默认产出 review-only 计划;apply 时原地
更新受影响页面的 frontmatter — 不涉及文件重命名,也不直接写 Zotero。

注意:寻址候选池限定在快照范围内(通常是一个 collection)。若条目被移出
该集合,匹配会落空并报告为未命中 — 这是安全的失败方向,不会误绑。
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..core import WikiManager
from .plan import (
    SnapshotItem,
    ZoteroBinding,
    _normalize_work_title,
    normalize_doi,
)


@dataclass(frozen=True)
class HealCandidate:
    """一条悬空绑定的寻址结果;new_item_key 为空表示未命中。"""

    item_key: str
    page_stem: str
    source_title: str
    matched_by: str
    new_item_key: str
    new_title: str


@dataclass(frozen=True)
class HealPlan:
    """只读自愈计划;apply 前的审查对象。"""

    collection_name: str
    collection_key: str
    stale: tuple[HealCandidate, ...]


def _unique_match(matches: list[SnapshotItem]) -> SnapshotItem | None:
    return matches[0] if len(matches) == 1 else None


def match_stale_binding(
    binding: ZoteroBinding,
    items: Sequence[SnapshotItem],
) -> tuple[str, str, str]:
    """按 DOI → citation_key → 标准化标题二次寻址;唯一命中才采纳。"""
    doi = normalize_doi(binding.doi)
    if doi:
        match = _unique_match(
            [item for item in items if item.doi and normalize_doi(item.doi) == doi]
        )
        if match:
            return "doi", match.item_key, match.title

    if binding.citation_key:
        match = _unique_match(
            [
                item
                for item in items
                if item.citation_key and item.citation_key == binding.citation_key
            ]
        )
        if match:
            return "citation_key", match.item_key, match.title

    title = _normalize_work_title(binding.source_title)
    if title:
        match = _unique_match(
            [item for item in items if _normalize_work_title(item.title) == title]
        )
        if match:
            return "title", match.item_key, match.title

    return "", "", ""


def plan_heal(
    bindings: Iterable[ZoteroBinding],
    snapshot_items: Sequence[SnapshotItem],
    *,
    collection_name: str = "",
    collection_key: str = "",
) -> HealPlan:
    """找出不在快照中的绑定(悬空 key),并逐条二次寻址。"""
    live_keys = {item.item_key for item in snapshot_items}
    stale: list[HealCandidate] = []
    for binding in bindings:
        if binding.item_key in live_keys:
            continue
        matched_by, new_key, new_title = match_stale_binding(binding, snapshot_items)
        stale.append(
            HealCandidate(
                item_key=binding.item_key,
                page_stem=binding.page_stem,
                source_title=binding.source_title,
                matched_by=matched_by,
                new_item_key=new_key,
                new_title=new_title,
            )
        )
    return HealPlan(
        collection_name=collection_name,
        collection_key=collection_key,
        stale=tuple(stale),
    )


def plan_to_heal_manifest(plan: HealPlan) -> dict[str, Any]:
    """序列化为 review-only 清单(供 temp/ 落盘与人工审查)。"""
    return {
        "version": 1,
        "mode": "review-only",
        "collection": {"name": plan.collection_name, "key": plan.collection_key},
        "stale": [
            {
                "item_key": candidate.item_key,
                "page_stem": candidate.page_stem,
                "source_title": candidate.source_title,
                "matched_by": candidate.matched_by,
                "new_item_key": candidate.new_item_key,
                "new_title": candidate.new_title,
            }
            for candidate in plan.stale
        ],
    }


def apply_heal_plan(wiki: WikiManager, plan: HealPlan) -> list[Path]:
    """把命中的重绑定写回受影响页面的 frontmatter(原地,文件名不变)。"""
    changed: list[Path] = []
    details: list[str] = []
    for candidate in plan.stale:
        if not candidate.new_item_key:
            continue
        page = wiki.get_page(candidate.page_stem)
        if page is None:
            continue
        sources_meta = [
            dict(source) if isinstance(source, Mapping) else source
            for source in (page.frontmatter.get("sources_meta") or [])
        ]
        touched = False
        for entry in sources_meta:
            if (
                isinstance(entry, dict)
                and str(entry.get("zotero_item_key") or "") == candidate.item_key
            ):
                entry["zotero_item_key"] = candidate.new_item_key
                touched = True
        if not touched:
            continue
        frontmatter = dict(page.frontmatter)
        frontmatter["sources_meta"] = sources_meta
        frontmatter["updated"] = datetime.now(UTC).strftime("%Y-%m-%d")
        wiki.create_page(page.title, page.content, frontmatter, path=page.path)
        changed.append(page.path)
        details.append(
            f"{candidate.page_stem}: {candidate.item_key} -> {candidate.new_item_key} "
            f"(matched by {candidate.matched_by})"
        )
    if changed:
        wiki.append_log(
            "zotero-heal",
            f"rebound {len(changed)} page(s) from stale Zotero item keys",
            details=details,
        )
    return changed
