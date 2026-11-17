#!/usr/bin/env python3
"""Render normalized source text as lean Agent Asset Markdown entries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re


SCRIPT_DIR = Path(__file__).resolve().parent
EVIDENCE_SCRIPT = SCRIPT_DIR / "nontext_summary_evidence.py"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}
LARGE_TEXT_CHARS = 16_000


@dataclass(frozen=True)
class MaterializedAsset:
    markdown: str
    manifest_row: dict[str, object]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def rel(root: Path, path: Path) -> str:
    return path.resolve(strict=False).relative_to(root.resolve()).as_posix()


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values: list[str]) -> str:
    return "\n".join(f"  - {yaml_string(value)}" for value in values)


def asset_id(source_path: str) -> str:
    digest = hashlib.sha256(source_path.encode("utf-8")).hexdigest()[:16]
    return f"asset-{digest}"


def source_format(source: Path) -> str:
    return source.suffix.lower().lstrip(".") or "file"


def asset_type(source: Path) -> str:
    ext = source.suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext in {".ppt", ".pptx"}:
        return "presentation"
    if ext in {".xls", ".xlsx"}:
        return "workbook"
    if ext in IMAGE_EXTENSIONS:
        return "image"
    return "document"


def read_evidence(source: Path, text: str, limit: int = 4) -> list[str]:
    try:
        spec = importlib.util.spec_from_file_location("nontext_summary_evidence", EVIDENCE_SCRIPT)
        if spec is None or spec.loader is None:
            raise ImportError(EVIDENCE_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        lines = module.select_summary_evidence(source, text, limit=limit)
        if lines:
            return [str(line) for line in lines][:limit]
    except (ImportError, AttributeError, OSError, TypeError, ValueError):
        pass
    output: list[str] = []
    for raw in text.splitlines():
        line = raw.strip(" #*-\t")
        if not line or line.lower().startswith(("creator:", "producer:", "relative path:", "size bytes:")):
            continue
        if len(line) < 4 or line == source.stem:
            continue
        output.append(re.sub(r"\s+", " ", line)[:160])
        if len(output) >= limit:
            break
    return output


def sampled_text(text: str) -> str:
    if len(text) <= LARGE_TEXT_CHARS:
        return text.strip()
    return (
        "### Sampled Content Note / 采样内容说明\n\n"
        "- Long source: retained approximately the first and last 1000 tokens for retrieval. / 长文档仅保留约前后各 1000 tokens 用于检索。\n\n"
        "### Front Sample / 前部样本\n\n"
        + text[:4_000].rstrip()
        + "\n\n### Back Sample / 后部样本\n\n"
        + text[-4_000:].lstrip()
    )


def demote_headings(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", raw)
        if match:
            lines.append("### " + match.group(2).strip())
        else:
            lines.append(raw)
    return "\n".join(lines).strip()


def timestamp(path: Path, creation: bool = False) -> str:
    stat = path.stat()
    value = getattr(stat, "st_birthtime", stat.st_ctime) if creation else stat.st_mtime
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def materialize_document(
    root: Path,
    source: Path,
    archive_path: Path,
    target: Path,
    normalized_text: str | None,
) -> MaterializedAsset:
    source_ref = rel(root, archive_path)
    semantic_ref = rel(root, target)
    source_ref_active = rel(root, source)
    normalized_text = (normalized_text or "").strip()
    evidence = read_evidence(source, normalized_text) if normalized_text else []
    fmt = source_format(source)
    kind = asset_type(source)
    summary = "; ".join(evidence[:3]) if evidence else (
        f"A metadata-first Agent entry was created for the original {fmt} file {source.stem}. / 已为 {source.stem} 的 {fmt} 原件建立 metadata-first Agent 入口。"
    )
    insights = evidence[:3] or [
        "The original file remains the highest-fidelity source; open Source Map when layout, charts, or full content matter. / 原始文件仍是最高保真来源；需要版式、图表或完整内容时打开来源映射。"
    ]
    details = demote_headings(sampled_text(normalized_text)) if normalized_text else (
        "### File Metadata / 文件元数据\n\n"
        f"- Source format / 来源格式: `{fmt}`\n"
        f"- Size in bytes / 字节大小: `{source.stat().st_size}`\n"
        "- No reliable normalized body was available; this asset is metadata-first. / 没有可靠的规范化正文；本资产采用 metadata-first。"
    )
    row_id = asset_id(source_ref)
    tags = [fmt, kind][:3]
    markdown = "\n".join(
        [
            "---",
            f"id: {yaml_string(row_id)}",
            f"title: {yaml_string(source.stem)}",
            f"summary: {yaml_string(summary)}",
            "tags:",
            yaml_list(tags),
            "search_terms:",
            yaml_list([source.stem, fmt, *evidence[:2]]),
            "use_when:",
            yaml_list([f"Use when locating or understanding {source.stem}. / 适用于定位或理解 {source.stem}。"]),
            "skip_when:",
            yaml_list([
                "Skip when the original layout, charts, annotations, or non-text details are required. / 当需要原始版式、图表、批注或无法由文本表达的细节时不适用。"
            ]),
            "source_paths:",
            yaml_list([source_ref]),
            f"source_created_at: {yaml_string(timestamp(source, creation=True))}",
            f"source_modified_at: {yaml_string(timestamp(source))}",
            f"agent_modified_at: {yaml_string(utc_now())}",
            'version: "0.1.0"',
            "---",
            "",
            "## Summary / 摘要",
            "",
            f"- {summary}",
            "- The original file is the high-fidelity source of truth; open Source Map when needed. / 原始文件是高保真 source of truth；需要时打开来源映射。",
            "",
            "## Insight / 洞察",
            "",
            *[f"- {item}" for item in insights],
            "",
            "## Details / 详情",
            "",
            details,
            "",
            "## Source Map / 来源映射",
            "",
            f"- [[{source_ref}]]",
            "",
        ]
    )
    manifest_row: dict[str, object] = {
        "asset_id": row_id,
        "path": semantic_ref,
        "title": source.stem,
        "summary": summary,
        "insights": insights,
        "tags": tags,
        "search_terms": [source.stem, fmt, *evidence[:2]],
        "use_when": [f"Use when locating or understanding {source.stem}. / 适用于定位或理解 {source.stem}。"],
        "skip_when": [
            "Skip when the original layout, charts, annotations, or non-text details are required. / 当需要原始版式、图表、批注或无法由文本表达的细节时不适用。"
        ],
        "asset_type": kind,
        "privacy": "non_pii",
        "retention": "review",
        "index_status": "candidate",
        "source_paths": [source_ref],
        "semantic_paths": [semantic_ref],
        "source_formats": [fmt],
        "source_format": fmt,
        "semantic_format": "markdown",
        "semantic_formats": ["markdown"],
        "extraction_policy": (
            "agent-readable-doc normalized extraction / Agent 可读文档规范化抽取"
            if normalized_text
            else "metadata-first fallback / metadata-first 回退"
        ),
        "fidelity": "text_structure" if normalized_text else "metadata_only",
        "sampled_only": len(normalized_text) > LARGE_TEXT_CHARS,
        "sampling_policy": (
            "first/last 1000-token equivalent when long / 长文档取前后约 1000 tokens"
            if len(normalized_text) > LARGE_TEXT_CHARS
            else "full normalized text / 完整规范化文本"
        ),
        "chunk_strategy": "progressive disclosure: manifest -> .agent.md -> archived source / 渐进披露：manifest -> .agent.md -> 归档原文",
        "progressive_disclosure": [
            "search manifest / 搜索 manifest",
            "open .agent.md / 打开 .agent.md",
            "open archived source / 打开归档原文",
        ],
        "source_status": "available",
        "visual_status": "not_visual",
        "generated_by": "agent-readable-doc/scripts/materialize_agent_assets.py",
        "size": source.stat().st_size,
        "mtime_ns": source.stat().st_mtime_ns,
        "source_active_path": source_ref_active,
    }
    return MaterializedAsset(markdown=markdown, manifest_row=manifest_row)
