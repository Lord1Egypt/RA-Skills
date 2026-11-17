"""Deterministic, source-aware depth signals for wiki pages."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BOILERPLATE_H2 = {
    "相关页面",
    "Related Pages",
    "来源",
    "Sources",
    "变更日志",
    "Changelog",
}
TEXT_SOURCE_SUFFIXES = {".md", ".txt", ".json"}


@dataclass(frozen=True)
class DepthLintConfig:
    enabled: bool = True
    min_knowledge_chars: int = 500
    min_meaningful_paragraphs: int = 3
    multi_source_threshold: int = 3
    multi_source_min_knowledge_chars: int = 800
    source_volume_threshold: int = 10_000
    compression_ratio_warning: float = 0.01
    extreme_source_volume_threshold: int = 20_000
    extreme_compression_max_knowledge_chars: int = 1_500
    skip_tags: tuple[str, ...] = ("QRF",)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> DepthLintConfig:
        if not value:
            return cls()
        data = dict(value)
        data["skip_tags"] = tuple(data.get("skip_tags", cls().skip_tags))
        return cls(**data)


@dataclass(frozen=True)
class DepthMetrics:
    knowledge_chars: int
    meaningful_paragraphs: int
    substantive_sections: int
    source_count: int
    local_source_chars: int
    compression_ratio: float | None


@dataclass(frozen=True)
class DepthIssue:
    page_title: str
    page_stem: str
    metrics: DepthMetrics
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_title": self.page_title,
            "page_stem": self.page_stem,
            "knowledge_chars": self.metrics.knowledge_chars,
            "meaningful_paragraphs": self.metrics.meaningful_paragraphs,
            "substantive_sections": self.metrics.substantive_sections,
            "source_count": self.metrics.source_count,
            "local_source_chars": self.metrics.local_source_chars,
            "compression_ratio": self.metrics.compression_ratio,
            "reasons": list(self.reasons),
        }

    def render(self) -> str:
        ratio = (
            f"{self.metrics.compression_ratio:.2%}"
            if self.metrics.compression_ratio is not None
            else "n/a"
        )
        return (
            f"{self.page_title} ({self.page_stem}): knowledge={self.metrics.knowledge_chars} chars, "
            f"paragraphs={self.metrics.meaningful_paragraphs}, "
            f"sections={self.metrics.substantive_sections}, "
            f"sources={self.metrics.source_count}, source_chars={self.metrics.local_source_chars}, "
            f"compression={ratio}; reasons={','.join(self.reasons)}"
        )


def _strip_boilerplate(content: str) -> str:
    kept: list[str] = []
    skip = False
    for line in content.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if heading:
            skip = heading.group(1) in BOILERPLATE_H2
        if not skip:
            kept.append(line)
    return "\n".join(kept)


def _normalize_markdown(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[\[([^]|]+)\|([^]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^]]+)\]\]", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[`*_~>]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_knowledge_body(content: str) -> str:
    return _normalize_markdown(_strip_boilerplate(content))


def _knowledge_blocks(content: str) -> tuple[list[str], list[str]]:
    raw = _strip_boilerplate(content)
    paragraphs = [
        _normalize_markdown(block)
        for block in re.split(r"\n\s*\n", raw)
        if block.strip() and not block.lstrip().startswith("#")
    ]
    sections: list[str] = []
    current: list[str] = []
    in_section = False
    for line in raw.splitlines():
        if re.match(r"^##\s+", line):
            if in_section:
                sections.append(_normalize_markdown("\n".join(current)))
            current = []
            in_section = True
        elif in_section:
            current.append(line)
    if in_section:
        sections.append(_normalize_markdown("\n".join(current)))
    return paragraphs, sections


import functools


@functools.lru_cache(maxsize=1024)
def _read_source_file_chars(path_str: str) -> int:
    try:
        return len(Path(path_str).read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return 0


def _local_source_chars(sources: Sequence[Any], project_root: Path) -> int:
    total = 0
    root = project_root.absolute()
    for raw in sources:
        source = Path(str(raw))
        if source.is_absolute() or ".." in source.parts:
            continue
        candidate = (root / source).absolute()
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        if (
            not candidate.exists()
            or candidate.suffix.lower() not in TEXT_SOURCE_SUFFIXES
        ):
            continue
        total += _read_source_file_chars(str(candidate))
    return total


def analyze_depth(
    *,
    page_title: str,
    page_stem: str,
    content: str,
    frontmatter: Mapping[str, Any],
    project_root: Path,
    config: DepthLintConfig,
) -> DepthIssue | None:
    # draft/seed 是未成熟状态,archived 已退役,均不做深度要求;
    # developing 起即给出 advisory 提示(active 为 legacy 写法)。
    _DEPTH_ANALYZED = ("active", "developing", "mature", "evergreen")
    if not config.enabled or frontmatter.get("status", "draft") not in _DEPTH_ANALYZED:
        return None
    if str(frontmatter.get("lint_depth", "")).lower() == "skip":
        return None
    tags = {str(tag) for tag in frontmatter.get("tags", []) or []}
    if tags.intersection(config.skip_tags):
        return None
    knowledge = extract_knowledge_body(content)
    paragraphs, sections = _knowledge_blocks(content)
    meaningful = sum(len(value) >= 40 for value in paragraphs)
    substantive = sum(len(value) >= 80 for value in sections)
    sources = frontmatter.get("sources", []) or []
    local_chars = _local_source_chars(sources, project_root)
    ratio = len(knowledge) / local_chars if local_chars else None
    metrics = DepthMetrics(
        len(knowledge), meaningful, substantive, len(sources), local_chars, ratio
    )
    reasons: list[str] = []
    if metrics.knowledge_chars < config.min_knowledge_chars:
        reasons.append("short-knowledge-body")
    if meaningful < config.min_meaningful_paragraphs and substantive < 2:
        reasons.append("insufficient-substantive-structure")
    if (
        len(sources) >= config.multi_source_threshold
        and local_chars >= config.source_volume_threshold
        and len(knowledge) < config.multi_source_min_knowledge_chars
    ):
        reasons.append("multi-source-underdeveloped")
    if (
        ratio is not None
        and local_chars >= config.extreme_source_volume_threshold
        and len(knowledge) < config.extreme_compression_max_knowledge_chars
        and ratio < config.compression_ratio_warning
    ):
        reasons.append("extreme-compression")
    if not reasons:
        return None
    return DepthIssue(page_title, page_stem, metrics, tuple(reasons))
