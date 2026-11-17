#!/usr/bin/env python3
"""Build or update the local second-brain index. English is normative; ZH-CN is paired. / 构建或更新本地第二大脑索引；英文为规范文本，简体中文为配对译文。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import runtime_paths

try:
    import yaml
except ImportError:  # pragma: no cover - only used in minimal Python envs.
    yaml = None


DOCUMENT_SCHEMA_VERSION = 4
MANIFEST_SCHEMA_VERSION = 5
SCHEMA_VERSION = DOCUMENT_SCHEMA_VERSION
EXTRACTOR_VERSION = 5
SUMMARY_VERSION = 5
SOURCE_MODE_AGENT_READABLE = "agent-readable"
SOURCE_MODE_ALL_MARKDOWN = "all-markdown"
SOURCE_MODE_ASSET_MANIFEST = "asset-manifest"
SOURCE_MODES = {SOURCE_MODE_AGENT_READABLE, SOURCE_MODE_ALL_MARKDOWN, SOURCE_MODE_ASSET_MANIFEST}
DEFAULT_SOURCE_MODE = os.environ.get("SECOND_BRAIN_SOURCE_MODE", SOURCE_MODE_AGENT_READABLE)
DEFAULT_LLM_WORKERS = int(os.environ.get("SECOND_BRAIN_LLM_WORKERS", "1"))
DEFAULT_VAULT = runtime_paths.DEFAULT_PATHS.vault
DEFAULT_OUT = runtime_paths.DEFAULT_PATHS.index_dir
DEFAULT_EXCLUDE_PARTS = {
    ".git",
    ".obsidian",
    ".pandoc",
    ".pytest_cache",
    ".smart-env",
    ".trash",
    ".Trash",
    "050 Template",
    "990 Attachment",
    "Archived",
    "extracted",
    "__pycache__",
    "skills",
    "tests",
}
ROOT_EXCLUDED_FILES = {"AGENTS.md", "PROGRESS.md", "README.md"}
PROFILE_FILENAMES = {"关于我.md", "关于我.agent.md", "about me.md", "about me.agent.md"}  # bilingual-compat: Chinese and English profile filenames.
FRONTMATTER_LIMIT = 16384
MAX_KEY_POINTS = 8
MAX_SEARCH_TERMS = 40
NOISE_PREFIXES = (
    "date created:",
    "date modified:",
    "status:",
    "生成时间:",  # bilingual-compat: generated-at metadata label.
    "发布时间:",  # bilingual-compat: published-at metadata label.
    "发布日期:",  # bilingual-compat: publication-date metadata label.
    "链接:",  # bilingual-compat: link metadata label.
    "总字数:",  # bilingual-compat: total-word-count metadata label.
    "预估阅读时长:",  # bilingual-compat: estimated-reading-time metadata label.
    "覆盖时长:",  # bilingual-compat: coverage-duration metadata label.
    "投入:",  # bilingual-compat: investment metadata label.
    "收益:",  # bilingual-compat: return metadata label.
    "紧急度:",  # bilingual-compat: urgency metadata label.
)
NOISE_HEADINGS = {"封面", "目录", "references", "reference", "参考资料"}  # bilingual-compat: cover, contents, and references headings.
SUMMARY_HEADINGS = {"摘要", "tldr", "tl;dr", "结论", "核心观点", "关键观点", "模型总结", "summary"}  # bilingual-compat: summary and conclusion headings.
INSIGHT_HEADINGS = {"insight", "insights", "洞察", "关键洞察"}  # bilingual-compat: insight headings.
SUMMARY_INPUT_TOKEN_LIMIT = 4000
SUMMARY_EDGE_TOKENS = 1000
ASSET_SEMANTIC_READ_LIMIT = 65536
PROJECT_ALIAS_VARIANTS = {
    "planner": ("plan", "planning"),
    "planning": ("plan", "planner"),
    "ranker": ("rank", "ranking"),
    "ranking": ("rank", "ranker"),
    "recommender": ("recommend", "recommendation"),
    "recommendation": ("recommend", "recommender"),
}


class BuildSummary:
    def __init__(
        self,
        *,
        total_documents: int,
        indexed_documents: int,
        reused_documents: int,
        removed_documents: int,
        excluded_pii_documents: int,
    ) -> None:
        self.total_documents = total_documents
        self.indexed_documents = indexed_documents
        self.reused_documents = reused_documents
        self.removed_documents = removed_documents
        self.excluded_pii_documents = excluded_pii_documents

    def as_dict(self) -> dict[str, int]:
        return {
            "total_documents": self.total_documents,
            "indexed_documents": self.indexed_documents,
            "reused_documents": self.reused_documents,
            "removed_documents": self.removed_documents,
            "excluded_pii_documents": self.excluded_pii_documents,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel_path(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()


def should_exclude(
    path: Path,
    vault: Path,
    out_dir: Path,
    source_mode: str = DEFAULT_SOURCE_MODE,
) -> bool:
    try:
        relative_parts = path.relative_to(vault).parts
    except ValueError:
        return True
    if any(part in DEFAULT_EXCLUDE_PARTS or part.startswith(".") for part in relative_parts):
        return True
    if len(relative_parts) == 1 and relative_parts[0] in ROOT_EXCLUDED_FILES:
        return True
    if path.name.lower() in PROFILE_FILENAMES:
        return True
    if source_mode == SOURCE_MODE_AGENT_READABLE and not path.name.endswith(".agent.md"):
        return True
    try:
        path.relative_to(out_dir)
        return True
    except ValueError:
        return False


def read_prefix(path: Path, limit: int = FRONTMATTER_LIMIT) -> str:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read(limit)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    match = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)(.*)$", text, re.S)
    if not match:
        return "", text
    return match.group(1), match.group(2)


def parse_frontmatter_data(frontmatter: str) -> dict[str, Any]:
    if not frontmatter.strip():
        return {}
    if yaml is not None:
        try:
            data = yaml.safe_load(frontmatter)
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict):
            return data
    data: dict[str, Any] = {}
    current_key = ""
    for raw in frontmatter.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+:", raw):
            key, value = raw.split(":", 1)
            current_key = key.strip()
            data[current_key] = value.strip().strip("\"'")
            continue
        if current_key and re.match(r"^\s*-\s+", raw):
            value = re.sub(r"^\s*-\s*", "", raw).strip().strip("\"'")
            existing = data.get(current_key)
            if not isinstance(existing, list):
                existing = [] if not existing else [str(existing)]
            existing.append(value)
            data[current_key] = existing
    return data


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        return [item.strip().strip("\"'") for item in text.strip("[]").split(",") if item.strip()]
    return [text]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "；".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def parse_tags(frontmatter: str) -> list[str]:
    frontmatter_tags = as_list(parse_frontmatter_data(frontmatter).get("tags"))
    if frontmatter_tags:
        return frontmatter_tags
    tags: list[str] = []
    lines = frontmatter.splitlines()
    in_tags = False
    for line in lines:
        starts_top_key = bool(re.match(r"^[A-Za-z0-9_-]+:", line))
        if starts_top_key and not line.startswith("tags:"):
            in_tags = False
        if line.startswith("tags:"):
            in_tags = True
            value = line.split(":", 1)[1].strip()
            if value.startswith("[") and value.endswith("]"):
                tags.extend(
                    item.strip().strip("\"'")
                    for item in value.strip("[]").split(",")
                    if item.strip()
                )
            elif value:
                tags.append(value.strip().strip("\"'"))
            continue
        if in_tags and re.match(r"^\s*-\s+", line):
            tags.append(re.sub(r"^\s*-\s*", "", line).strip().strip("\"'"))
    return [tag for tag in tags if tag]


def load_report_pii_paths(vault: Path) -> set[str]:
    paths: set[str] = set()
    for report in vault.glob("tag_report*.json"):
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for item in data.get("pii_files", []):
            file_value = item.get("file") if isinstance(item, dict) else None
            if isinstance(file_value, str) and file_value:
                paths.add(file_value)
    return paths


def has_pii_tag(path: Path, vault: Path, report_pii_paths: set[str]) -> bool:
    relative = rel_path(path, vault)
    if relative in report_pii_paths:
        return True
    prefix = read_prefix(path)
    frontmatter, _ = split_frontmatter(prefix)
    return any(tag.strip().lower() == "pii" for tag in parse_tags(frontmatter))


def has_archived_tag(path: Path) -> bool:
    prefix = read_prefix(path)
    frontmatter, _ = split_frontmatter(prefix)
    return any(tag.strip().lower() == "archived" for tag in parse_tags(frontmatter))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_line(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^[-*+]\s+", "", line)
    line = re.sub(r"^\d+[.)]\s+", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def is_noise_line(line: str) -> bool:
    stripped = normalize_line(line)
    lower = stripped.lower()
    if not stripped:
        return True
    if stripped.startswith("![[") or stripped.startswith("```"):
        return True
    if lower in {"---", "todo", "to do"}:
        return True
    if any(lower.startswith(prefix) for prefix in NOISE_PREFIXES):
        return True
    if re.match(r"^(date|status|created|modified)\s*[:：]", lower):
        return True
    return False


def clean_body_lines(body: str) -> list[str]:
    lines = []
    skip_code = False
    for raw in body.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            skip_code = not skip_code
            continue
        if skip_code:
            continue
        if re.match(r"^#{1,6}\s+", stripped):
            heading = re.sub(r"^#{1,6}\s+", "", stripped).strip()
            if heading.lower() in NOISE_HEADINGS:
                continue
            lines.append(heading)
            continue
        line = normalize_line(stripped)
        if is_noise_line(line):
            continue
        lines.append(line)
    return lines


def extract_headings(body: str) -> list[str]:
    headings = []
    for match in re.finditer(r"(?m)^#{1,4}\s+(.+?)\s*$", body):
        heading = match.group(1).strip()
        if heading.lower() not in NOISE_HEADINGS:
            headings.append(heading)
    return headings[:20]


def extract_summary_section(body: str) -> str | None:
    current_heading = None
    captured: list[str] = []
    for raw in body.splitlines():
        heading_match = re.match(r"^#{1,4}\s+(.+?)\s*$", raw.strip())
        if heading_match:
            heading = heading_match.group(1).strip()
            if current_heading in SUMMARY_HEADINGS and captured:
                break
            current_heading = heading.lower()
            continue
        if current_heading in SUMMARY_HEADINGS:
            if captured and re.match(r"^\s*[-*+]\s+", raw):
                break
            line = normalize_line(raw)
            if not is_noise_line(line):
                captured.append(line)
    if not captured:
        return None
    return " ".join(captured)[:500]


def extract_heading_section(body: str, heading_names: set[str], max_level: int = 2) -> str:
    current_match = False
    captured: list[str] = []
    for raw in body.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", raw.strip())
        if heading_match:
            level = len(heading_match.group(1))
            heading = heading_match.group(2).strip().lower()
            if current_match and level <= max_level:
                break
            current_match = level <= max_level and heading in heading_names
            continue
        if current_match:
            captured.append(raw)
    return "\n".join(captured).strip()


def extract_agent_summary_section(body: str) -> str:
    return extract_heading_section(body, {"摘要"}) or extract_heading_section(body, {"先给结论"})  # bilingual-compat: summary and conclusion-first legacy headings.


def extract_insight_section(body: str) -> str:
    return extract_heading_section(body, INSIGHT_HEADINGS)


def extract_conclusion_points(body: str) -> list[str]:
    section = extract_agent_summary_section(body)
    points = []
    for raw in section.splitlines():
        line = normalize_line(raw)
        if is_noise_line(line) or len(line) < 4:
            continue
        if line not in points:
            points.append(line)
        if len(points) >= MAX_KEY_POINTS:
            break
    return points


def extract_insight_points(body: str) -> list[str]:
    section = extract_insight_section(body)
    points = []
    for raw in section.splitlines():
        line = normalize_line(raw)
        if is_noise_line(line) or len(line) < 4:
            continue
        if line not in points:
            points.append(line)
        if len(points) >= MAX_KEY_POINTS:
            break
    return points


def extract_key_points(lines: list[str], headings: list[str]) -> list[str]:
    candidates = []
    heading_set = set(headings)
    for line in lines:
        if line in heading_set:
            continue
        if len(line) < 6:
            continue
        if line not in candidates:
            candidates.append(line)
        if len(candidates) >= MAX_KEY_POINTS:
            break
    return candidates


def rough_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./+-]+|[\u4e00-\u9fff]", text)


def select_summary_input(title: str, body: str) -> str:
    cleaned = "\n".join(clean_body_lines(body))
    tokens = rough_tokens(cleaned)
    if len(tokens) > SUMMARY_INPUT_TOKEN_LIMIT:
        # Leave the title outside the truncation budget; the budget applies to note content.
        selected = tokens[:SUMMARY_EDGE_TOKENS] + ["\n...\n"] + tokens[-SUMMARY_EDGE_TOKENS:]
        cleaned = " ".join(selected)
    return f"Title: {title}\n\nContent:\n{cleaned}"


def summary_prompt_variants(title: str, summary_input: str) -> list[str]:
    """Build English-normative prompts that require paired ZH-CN output."""

    return [
        (
            "Summarize this note for agent retrieval. English is normative and ZH-CN must be "
            "a faithful paired translation. Return exactly two concise lines: `EN: ...` and "
            "`ZH-CN: ...`. Focus on durable ideas, tasks, decisions, technical concepts, and "
            "user preferences. Do not include boilerplate metadata or invent facts. / "
            # bilingual-compat: paired English prompt text appears in the same prompt.
            "为 agent 检索总结此笔记；英文为规范文本，简体中文必须是忠实的配对译文。"
            # bilingual-compat: paired English prompt text appears in the same prompt.
            "严格返回两行：`EN: ...` 与 `ZH-CN: ...`。聚焦长期有效的观点、任务、决策、"
            # bilingual-compat: paired English prompt text appears in the same prompt.
            "技术概念和用户偏好；不要包含样板元数据，也不要虚构事实。\n\n"
            f"{summary_input}"
        ),
        (
            "Summarize this note for agent retrieval using only the non-sensitive title and "
            "high-level terms below. English is normative and ZH-CN must be a faithful paired "
            "translation. Return exactly two concise lines: `EN: ...` and `ZH-CN: ...`. Do not "
            "infer private or explicit details. / 仅使用下方非敏感标题和高层词语，为 agent "
            # bilingual-compat: paired English prompt text appears in the same prompt.
            "检索总结此笔记；英文为规范文本，简体中文必须是忠实的配对译文。严格返回两行："
            # bilingual-compat: paired English prompt text appears in the same prompt.
            "`EN: ...` 与 `ZH-CN: ...`。不要推断隐私或显式细节。\n\n"
            f"Title: {title}\n\nHigh-level retrieval context:\n"
            f"{sanitize_summary_input(summary_input)}"
        ),
    ]


def call_llm_summary(title: str, summary_input: str) -> str:
    status = summary_remote_status()
    require_llm = os.environ.get("SECOND_BRAIN_REQUIRE_LLM", "0") == "1"
    if not status["available"]:
        if require_llm:
            raise RuntimeError(f"LLM summary required but unavailable / 必需的 LLM 摘要不可用: {status['reason']}")
        return ""
    try:
        from openai import OpenAI
    except ImportError:
        if require_llm:
            raise RuntimeError("LLM summary required but openai package is unavailable. / 必需的 LLM 摘要不可用：缺少 openai package。")
        return ""
    api_key = os.environ.get("SECOND_BRAIN_SUMMARY_API_KEY", "").strip()
    client = OpenAI(base_url=status["base_url"], api_key=api_key)
    last_error: Exception | None = None
    for prompt_variant in summary_prompt_variants(title, summary_input):
        for attempt in range(4):
            try:
                response = client.chat.completions.create(
                    model=status["model"],
                    messages=[{"role": "user", "content": prompt_variant}],
                )
                content = response.choices[0].message.content or ""
                return re.sub(r"\s+", " ", content).strip()[:700]
            except Exception as exc:
                last_error = exc
                if is_content_filter_error(exc):
                    break
                time.sleep(min(2**attempt, 8))
    if require_llm:
        raise RuntimeError(f"LLM summary failed / LLM 摘要失败 for {title}: {last_error}") from last_error
    return ""


def summary_remote_status(
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return explicit remote-summary configuration without reading general credentials."""

    values = os.environ if environ is None else environ
    if values.get("SECOND_BRAIN_SUMMARY_ENABLED", "").strip().lower() not in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return {"available": False, "reason": "explicit_opt_in_required"}
    api_key = values.get("SECOND_BRAIN_SUMMARY_API_KEY", "").strip()
    if not api_key:
        return {"available": False, "reason": "missing_summary_api_key"}
    base_url = values.get("SECOND_BRAIN_SUMMARY_BASE_URL", "").strip()
    if not base_url:
        return {"available": False, "reason": "missing_base_url"}
    if not runtime_paths.is_https_url(base_url):
        return {"available": False, "reason": "https_required"}
    model = values.get("SECOND_BRAIN_SUMMARY_MODEL", "").strip()
    if not model:
        return {"available": False, "reason": "missing_model"}
    return {
        "available": True,
        "provider": "openai-compatible",
        "base_url": base_url,
        "model": model,
    }


def is_content_filter_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return "content_filter" in text or "responsibleaipolicyviolation" in text


def sanitize_summary_input(summary_input: str) -> str:
    safe_lines = []
    for raw in summary_input.splitlines():
        line = normalize_line(raw)
        if not line or len(line) > 180:
            continue
        if re.search(r"https?://|@|\\b\\d{6,}\\b", line):
            continue
        safe_lines.append(line)
        if len(safe_lines) >= 30:
            break
    return "\n".join(safe_lines)[:2000]


def current_summary_mode() -> str:
    return "llm-with-local-fallback" if summary_remote_status()["available"] else "local-fallback"


def build_summary(
    title: str,
    body: str,
    lines: list[str],
    key_points: list[str],
    frontmatter_summary: str = "",
) -> tuple[str, str]:
    if frontmatter_summary:
        return frontmatter_summary[:700], "agent-frontmatter"
    conclusion = extract_agent_summary_section(body)
    conclusion_lines = [
        normalize_line(line)
        for line in conclusion.splitlines()
        if not is_noise_line(normalize_line(line))
    ]
    if conclusion_lines:
        return "；".join(conclusion_lines[:3])[:500], "agent-conclusion"
    explicit = extract_summary_section(body)
    if explicit:
        return explicit, "explicit-section"
    summary_input = select_summary_input(title, body)
    llm_summary = call_llm_summary(title, summary_input)
    if llm_summary:
        return llm_summary, "llm"
    if key_points:
        joined = "；".join(key_points[:3])
        return f"{title}: {joined}"[:500], "local-fallback"
    if lines:
        return f"{title}: {'；'.join(lines[:3])}"[:500], "local-fallback"
    return title, "local-fallback"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9_./+-]*|[A-Z]{2,}|[\u4e00-\u9fff]{2,4}", text)


def extract_terms(parts: list[str]) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()
    for part in parts:
        for token in tokenize(part):
            cleaned = token.strip()
            key = cleaned.lower()
            if len(cleaned) < 2 or key in seen:
                continue
            seen.add(key)
            terms.append(cleaned)
            if len(terms) >= MAX_SEARCH_TERMS:
                return terms
    return terms


def extract_entities(parts: list[str]) -> list[str]:
    text = " ".join(parts)
    entities = re.findall(
        r"\b[A-Z][A-Za-z0-9]{2,}\b|[\u4e00-\u9fff]{2,8}(?:模型|算法|特征|系统|任务|评估|工程)",  # bilingual-compat: Chinese domain entity suffixes.
        text,
    )
    output = []
    seen = set()
    for entity in entities:
        key = entity.lower()
        if key not in seen:
            seen.add(key)
            output.append(entity)
    return output[:30]


def display_snippet(summary: str, key_points: list[str], max_chars: int = 420) -> str:
    snippet = summary
    if key_points:
        snippet = f"{summary}\n- " + "\n- ".join(key_points[:3])
    return snippet[:max_chars]


def synthesize_search_text(record: dict[str, Any]) -> str:
    parts = [
        record.get("path", ""),
        record.get("title", ""),
        record.get("doc_type", ""),
        " ".join(record.get("tags", [])),
        " ".join(record.get("aliases", [])),
        " ".join(record.get("headings", [])),
        record.get("summary", ""),
        " ".join(record.get("insights", [])),
        " ".join(record.get("key_points", [])),
        " ".join(record.get("entities", [])),
        " ".join(record.get("search_terms", [])),
        " ".join(record.get("use_when", [])),
    ]
    return " ".join(part for part in parts if part)


def source_metadata(path: Path, text: str) -> dict[str, Any]:
    stat = path.stat()
    return {
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": sha256_text(text),
    }


def make_document_record(path: Path, vault: Path, text: str) -> dict[str, Any]:
    frontmatter, body = split_frontmatter(text)
    frontmatter_data = parse_frontmatter_data(frontmatter)
    tags = parse_tags(frontmatter)
    headings = extract_headings(body)
    lines = clean_body_lines(body)
    insights = as_list(frontmatter_data.get("insights")) or extract_insight_points(body)
    key_points = insights or extract_conclusion_points(body) or extract_key_points(lines, headings)
    relative = rel_path(path, vault)
    title = as_text(frontmatter_data.get("title"))
    if not title:
        title = (
            path.name.removesuffix(".agent.md")
            if path.name.endswith(".agent.md")
            else path.stem
        )
    top_dir = relative.split("/", 1)[0] if "/" in relative else "."
    aliases = as_list(frontmatter_data.get("aliases"))
    frontmatter_terms = as_list(frontmatter_data.get("search_terms"))
    use_when = as_list(frontmatter_data.get("use_when"))
    skip_when = as_list(frontmatter_data.get("skip_when"))
    doc_type = as_text(frontmatter_data.get("doc_type"))
    version = as_text(frontmatter_data.get("version"))
    asset_type = as_text(frontmatter_data.get("asset_type"))
    privacy = as_text(frontmatter_data.get("privacy"))
    retention = as_text(frontmatter_data.get("retention"))
    source_paths = as_list(frontmatter_data.get("source_paths")) or [relative]
    source_formats = as_list(frontmatter_data.get("source_formats"))
    fidelity = as_text(frontmatter_data.get("fidelity"))
    extraction_policy = as_text(frontmatter_data.get("extraction_policy"))
    summary, summary_provider = build_summary(
        title,
        body,
        lines,
        key_points,
        as_text(frontmatter_data.get("summary")),
    )
    generated_terms = extract_terms(
        [
            relative,
            title,
            " ".join(tags),
            " ".join(aliases),
            " ".join(headings),
            summary,
            *insights,
            *key_points,
            *frontmatter_terms,
            *use_when,
        ]
    )
    terms = (frontmatter_terms or generated_terms)[:MAX_SEARCH_TERMS]
    entities = extract_entities(
        [title, " ".join(aliases), " ".join(headings), summary, *insights, *key_points]
    )
    snippet = display_snippet(summary, key_points)
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_id": f"doc:{relative}",
        "record_type": "document",
        "path": relative,
        "source_paths": source_paths,
        "title": title,
        "top_dir": top_dir,
        "doc_type": doc_type,
        "version": version,
        "asset_type": asset_type,
        "privacy": privacy,
        "retention": retention,
        "source_formats": source_formats,
        "fidelity": fidelity,
        "extraction_policy": extraction_policy,
        "tags": tags,
        "aliases": aliases,
        "headings": headings,
        "summary": summary,
        "insights": insights,
        "key_points": key_points,
        "entities": entities,
        "search_terms": terms,
        "use_when": use_when,
        "skip_when": skip_when,
        "display_snippet": snippet,
        "excerpt": snippet,
        "size": path.stat().st_size,
        "mtime_ns": path.stat().st_mtime_ns,
        "sha256": sha256_text(text),
        "indexed_at": utc_now(),
        "source_fingerprints": {
            "sha256": sha256_text(text),
            "summary_version": SUMMARY_VERSION,
            "extractor_version": EXTRACTOR_VERSION,
            "summary_provider": summary_provider,
            "summary_model": (
                str(summary_remote_status().get("model", "")) if summary_provider == "llm" else ""
            ),
        },
    }
    record["search_text"] = synthesize_search_text(record)
    return record


def load_manifest(out_dir: Path) -> dict[str, Any]:
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.exists():
        return {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "sources": {},
            "groups": {},
            "records": {},
        }
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "sources": {},
            "groups": {},
            "records": {},
        }
    if manifest.get("schema_version") not in {DOCUMENT_SCHEMA_VERSION, MANIFEST_SCHEMA_VERSION}:
        return {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "sources": {},
            "groups": {},
            "records": {},
        }
    return manifest


def load_existing_records(out_dir: Path) -> dict[str, dict[str, Any]]:
    documents_path = out_dir / "documents.jsonl"
    if not documents_path.exists():
        return {}
    records = {}
    for line in documents_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        record_id = record.get("record_id")
        if isinstance(record_id, str):
            records[record_id] = record
    return records


def asset_manifest_path(vault: Path) -> Path:
    return vault / ".cleanup-extracted" / "asset-manifest.jsonl"


def iter_asset_manifest_entries(vault: Path) -> list[dict[str, Any]]:
    path = asset_manifest_path(vault)
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


def should_index_asset(entry: dict[str, Any]) -> bool:
    if str(entry.get("privacy", "")).lower() == "pii":
        return False
    if str(entry.get("asset_type", "")).lower() in {"embedded_attachment", "temp", "generated_report"}:
        return False
    return str(entry.get("index_status", "")).lower() in {"final", "keep", "retained", "indexed"}


def unique_texts(*groups: Any, limit: int | None = None) -> list[str]:
    values: list[str] = []
    for group in groups:
        for value in as_list(group):
            text = str(value).strip()
            if text and text not in values:
                values.append(text)
                if limit is not None and len(values) >= limit:
                    return values
    return values


def safe_asset_semantic_path(vault: Path, raw_path: str) -> Path | None:
    candidate = Path(raw_path)
    target = (candidate if candidate.is_absolute() else vault / candidate).resolve(strict=False)
    try:
        target.relative_to(vault.resolve())
    except ValueError:
        return None
    return target if target.is_file() else None


def semantic_asset_evidence(entry: dict[str, Any], vault: Path) -> dict[str, Any]:
    for raw_path in as_list(entry.get("semantic_paths")):
        path = safe_asset_semantic_path(vault, raw_path)
        if path is None:
            continue
        text = read_prefix(path, ASSET_SEMANTIC_READ_LIMIT)
        frontmatter, body = split_frontmatter(text)
        data = parse_frontmatter_data(frontmatter)
        tags = parse_tags(frontmatter)
        if any(tag.lower() == "pii" for tag in tags):
            return {"pii": True, "path": raw_path}
        summary = as_text(data.get("summary"))
        if not summary:
            points = extract_conclusion_points(body)
            summary = "；".join(points[:3])
        return {
            "path": raw_path,
            "summary": summary[:700],
            "aliases": as_list(data.get("aliases")),
            "search_terms": as_list(data.get("search_terms")),
            "use_when": as_list(data.get("use_when")),
            "tags": tags,
            "headings": extract_headings(body),
            "insights": extract_insight_points(body),
            "key_points": extract_conclusion_points(body),
            "fingerprint": sha256_text(text),
            "size": len(text.encode("utf-8")),
            "mtime_ns": path.stat().st_mtime_ns,
        }
    return {}


def identifier_aliases(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    basename = Path(value).name
    split = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", basename)
    words = [word.lower() for word in re.split(r"[_./+-]+|\s+", split) if word]
    aliases = [basename]
    if words:
        phrase = " ".join(words)
        aliases.append(phrase)
        for index, word in enumerate(words):
            for replacement in PROJECT_ALIAS_VARIANTS.get(word, ()):
                variant = list(words)
                variant[index] = replacement
                aliases.append(" ".join(variant))
    return unique_texts(aliases, limit=12)


def asset_project_aliases(entry: dict[str, Any], semantic_aliases: list[str]) -> list[str]:
    values = unique_texts(semantic_aliases, entry.get("aliases"))
    if str(entry.get("asset_type", "")).lower() == "code_project":
        values = unique_texts(values, identifier_aliases(as_text(entry.get("title"))))
        for path in as_list(entry.get("source_paths")):
            values = unique_texts(values, identifier_aliases(path))
    return values[:20]


def asset_entry_metadata(
    entry: dict[str, Any],
    vault: Path | None = None,
    semantic: dict[str, Any] | None = None,
) -> dict[str, Any]:
    semantic = semantic if semantic is not None else (semantic_asset_evidence(entry, vault) if vault is not None else {})
    payload = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    semantic_fingerprint = str(semantic.get("fingerprint", ""))
    return {
        "size": int(entry.get("size") or entry.get("size_bytes") or len(payload)) + int(semantic.get("size", 0) or 0),
        "mtime_ns": max(int(entry.get("mtime_ns") or 0), int(semantic.get("mtime_ns", 0) or 0)),
        "sha256": sha256_text(payload + "\nsemantic:" + semantic_fingerprint),
    }


def make_asset_record(
    entry: dict[str, Any],
    vault: Path | None = None,
    semantic: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_paths = as_list(entry.get("source_paths")) or as_list(entry.get("path"))
    semantic_paths = as_list(entry.get("semantic_paths"))
    path = semantic_paths[0] if semantic_paths else as_text(entry.get("path"))
    if not path and source_paths:
        path = source_paths[0]
    title = as_text(entry.get("title")) or Path(path).stem
    top_dir = path.split("/", 1)[0] if "/" in path else "."
    semantic = semantic if semantic is not None else (semantic_asset_evidence(entry, vault) if vault is not None else {})
    summary = as_text(semantic.get("summary")) or as_text(entry.get("summary")) or title
    aliases = asset_project_aliases(entry, as_list(semantic.get("aliases")))
    insights = unique_texts(entry.get("insights"), semantic.get("insights"), limit=MAX_KEY_POINTS)
    key_points = unique_texts(semantic.get("key_points"), entry.get("key_points"), insights, limit=MAX_KEY_POINTS)
    search_terms = unique_texts(
        semantic.get("search_terms"),
        entry.get("search_terms"),
        aliases,
        extract_terms([path, title, summary, *insights, *key_points, *source_paths]),
        limit=MAX_SEARCH_TERMS,
    )
    use_when = unique_texts(semantic.get("use_when"), entry.get("use_when"))
    tags = unique_texts(entry.get("tags"), semantic.get("tags"))
    headings = unique_texts(entry.get("headings"), semantic.get("headings"), limit=20)
    entities = extract_entities([title, summary, *aliases, *insights, *key_points])
    snippet = display_snippet(summary, key_points)
    meta = asset_entry_metadata(entry, vault, semantic)
    asset_id = as_text(entry.get("asset_id")) or sha256_text(path)[:16]
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_id": f"asset:{asset_id}",
        "record_type": "document",
        "path": path,
        "source_paths": source_paths,
        "semantic_paths": semantic_paths,
        "attachments": as_list(entry.get("attachments")),
        "title": title,
        "top_dir": top_dir,
        "doc_type": as_text(entry.get("doc_type")) or as_text(entry.get("asset_type")),
        "asset_type": as_text(entry.get("asset_type")),
        "version": as_text(entry.get("version")),
        "privacy": as_text(entry.get("privacy")),
        "retention": as_text(entry.get("retention")),
        "source_formats": as_list(entry.get("source_formats")),
        "fidelity": as_text(entry.get("fidelity")),
        "extraction_policy": as_text(entry.get("extraction_policy")),
        "tags": tags,
        "aliases": aliases,
        "headings": headings,
        "summary": summary,
        "insights": insights,
        "key_points": key_points,
        "entities": entities,
        "search_terms": search_terms[:MAX_SEARCH_TERMS],
        "use_when": use_when,
        "skip_when": as_list(entry.get("skip_when")),
        "display_snippet": snippet,
        "excerpt": snippet,
        "size": meta["size"],
        "mtime_ns": meta["mtime_ns"],
        "sha256": meta["sha256"],
        "indexed_at": utc_now(),
        "source_fingerprints": {
            "sha256": meta["sha256"],
            "summary_version": SUMMARY_VERSION,
            "extractor_version": EXTRACTOR_VERSION,
            "summary_provider": "asset-manifest",
            "summary_model": "",
        },
    }
    record["search_text"] = synthesize_search_text(record)
    return record


def iter_markdown_files(
    vault: Path,
    out_dir: Path,
    source_mode: str = DEFAULT_SOURCE_MODE,
) -> list[Path]:
    files = []
    for path in vault.rglob("*.md"):
        if path.is_file() and not should_exclude(path, vault, out_dir, source_mode):
            files.append(path)
    return sorted(files)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_documents(out_dir: Path, records: list[dict[str, Any]]) -> None:
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    (out_dir / "documents.jsonl").write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )


def common_tag_ratio(records: list[dict[str, Any]]) -> float:
    tag_counts = Counter(tag for record in records for tag in record.get("tags", []))
    if not records or not tag_counts:
        return 0.0
    return tag_counts.most_common(1)[0][1] / len(records)


def group_candidates(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        parent = str(Path(record["path"]).parent).replace(".", "")
        if parent:
            by_parent[parent].append(record)
    groups = {}
    for parent, members in by_parent.items():
        sizes = [member.get("size", 0) for member in members]
        if len(members) < 5:
            continue
        median_size = statistics.median(sizes)
        explicit = parent == "Notion/RP Rank Task"
        if explicit or (median_size <= 1500 and common_tag_ratio(members) >= 0.6):
            groups[f"collection:{parent}"] = members
    return groups


def combined_hash(records: list[dict[str, Any]]) -> str:
    payload = [
        (
            f"{record['path']}:{record['source_fingerprints']['sha256']}:"
            f"{SUMMARY_VERSION}:{EXTRACTOR_VERSION}"
        )
        for record in sorted(records, key=lambda item: item["path"])
    ]
    return sha256_text("\n".join(payload))


def make_collection_record(group_id: str, members: list[dict[str, Any]]) -> dict[str, Any]:
    parent = group_id.removeprefix("collection:")
    source_paths = [member["path"] for member in sorted(members, key=lambda item: item["path"])]
    tags = [
        tag
        for tag, _ in Counter(
            tag for member in members for tag in member.get("tags", [])
        ).most_common(12)
    ]
    key_points = []
    for member in members:
        for point in member.get("key_points", []):
            if point not in key_points:
                key_points.append(point)
            if len(key_points) >= MAX_KEY_POINTS:
                break
        if len(key_points) >= MAX_KEY_POINTS:
            break
    title = parent.split("/")[-1]
    summary = (
        f"{title}: collection of {len(members)} related notes / {len(members)} 篇相关笔记的集合，涵盖 "
        + "；".join(key_points[:4])
    )
    headings = [member.get("title", "") for member in members[:20]]
    terms = extract_terms([parent, title, " ".join(tags), summary, *key_points, *headings])
    entities = extract_entities([title, summary, *key_points])
    snippet = display_snippet(summary, key_points)
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_id": group_id,
        "record_type": "collection",
        "path": parent,
        "source_paths": source_paths,
        "title": title,
        "top_dir": parent.split("/", 1)[0],
        "doc_type": "collection",
        "version": "",
        "tags": tags,
        "aliases": [],
        "headings": headings,
        "summary": summary,
        "key_points": key_points,
        "entities": entities,
        "search_terms": terms,
        "use_when": [],
        "skip_when": [],
        "display_snippet": snippet,
        "excerpt": snippet,
        "size": sum(member.get("size", 0) for member in members),
        "mtime_ns": max(member.get("mtime_ns", 0) for member in members),
        "sha256": combined_hash(members),
        "indexed_at": utc_now(),
        "source_fingerprints": {
            "combined_hash": combined_hash(members),
            "summary_version": SUMMARY_VERSION,
            "extractor_version": EXTRACTOR_VERSION,
        },
    }
    record["search_text"] = synthesize_search_text(record)
    return record


def write_generated_references(
    out_dir: Path,
    vault: Path,
    records: list[dict[str, Any]],
    excluded_pii_paths: list[str],
    summary: BuildSummary,
    source_mode: str,
) -> None:
    by_dir = Counter(record["top_dir"] for record in records)
    by_tag = Counter(tag for record in records for tag in record.get("tags", []))
    by_type = Counter(record["record_type"] for record in records)
    generated_at = utc_now()
    summary_lines = [
        "# Second Brain Index Summary / 第二大脑索引摘要",
        "",
        f"- Generated at / 生成时间: `{generated_at}`",
        f"- Vault / 知识库: `{vault}`",
        f"- Source mode / 来源模式: `{source_mode}`",
        f"- Total search records / 检索记录总数: `{summary.total_documents}`",
        f"- Document records / 文档记录: `{by_type.get('document', 0)}`",
        f"- Collection records / 集合记录: `{by_type.get('collection', 0)}`",
        f"- Indexed this run / 本次已索引: `{summary.indexed_documents}`",
        f"- Reused this run / 本次已复用: `{summary.reused_documents}`",
        f"- Removed this run / 本次已移除: `{summary.removed_documents}`",
        f"- PII-excluded documents / PII 排除文档: `{summary.excluded_pii_documents}`",
        "",
        "Use `query_index.py` for targeted retrieval before opening source notes. / 打开源笔记前，先使用 `query_index.py` 进行定向检索。",
        "",
    ]
    (out_dir / "index-summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    vault_map = ["# Vault Map / 知识库地图", ""]
    for name, count in by_dir.most_common():
        vault_map.append(f"- `{name}`: {count} records / {count} 条记录")
    vault_map.append("")
    (out_dir / "vault-map.md").write_text("\n".join(vault_map), encoding="utf-8")

    tag_map = ["# Tag Map / 标签地图", ""]
    for tag, count in by_tag.most_common(80):
        tag_map.append(f"- `{tag}`: {count} records / {count} 条记录")
    tag_map.append("")
    (out_dir / "tag-map.md").write_text("\n".join(tag_map), encoding="utf-8")

    (out_dir / "excluded-pii-paths.txt").write_text(
        "\n".join(excluded_pii_paths) + ("\n" if excluded_pii_paths else ""),
        encoding="utf-8",
    )


def manifest_versions_match(
    old_manifest: dict[str, Any],
    old_source: dict[str, Any],
    source_mode: str,
) -> bool:
    extractor_version = old_manifest.get("extractor_version", old_source.get("extractor_version"))
    summary_version = old_manifest.get("summary_version", old_source.get("summary_version"))
    manifest_source_mode = old_manifest.get("source_mode", old_source.get("source_mode"))
    return (
        extractor_version == EXTRACTOR_VERSION
        and summary_version == SUMMARY_VERSION
        and manifest_source_mode == source_mode
    )


def summary_reusable(record: dict[str, Any]) -> bool:
    fingerprints = record.get("source_fingerprints", {})
    provider = fingerprints.get("summary_provider", "")
    remote = summary_remote_status()
    if provider == "local-fallback" and remote["available"]:
        return False
    if (
        provider == "llm"
        and remote["available"]
        and fingerprints.get("summary_model") != remote.get("model", "")
    ):
        return False
    return True


def source_unchanged(
    old_manifest: dict[str, Any],
    old_source: dict[str, Any],
    meta: dict[str, Any],
    old_record: dict[str, Any] | None,
    source_mode: str,
) -> bool:
    return (
        old_record is not None
        and old_source.get("size") == meta["size"]
        and old_source.get("mtime_ns") == meta["mtime_ns"]
        and old_source.get("sha256") == meta["sha256"]
        and manifest_versions_match(old_manifest, old_source, source_mode)
        and summary_reusable(old_record)
    )


def extract_record_job(path: Path, vault: Path) -> tuple[str, dict[str, Any], dict[str, Any]]:
    text = read_text(path)
    meta = source_metadata(path, text)
    record = make_document_record(path, vault, text)
    return rel_path(path, vault), meta, record


def build_index(
    vault: Path,
    out_dir: Path,
    force: bool = False,
    llm_workers: int = DEFAULT_LLM_WORKERS,
    source_mode: str = DEFAULT_SOURCE_MODE,
) -> BuildSummary:
    if source_mode not in SOURCE_MODES:
        raise ValueError(f"Unsupported source mode / 不支持的来源模式: {source_mode}")
    vault = vault.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    old_manifest = load_manifest(out_dir)
    old_sources = {} if force else old_manifest.get("sources", {})
    old_groups = {} if force else old_manifest.get("groups", {})
    old_records = {} if force else load_existing_records(out_dir)
    report_pii_paths = load_report_pii_paths(vault)
    source_records: dict[str, dict[str, Any]] = {}
    sources: dict[str, dict[str, Any]] = {}
    excluded_pii_paths: list[str] = []
    indexed = 0
    reused = 0

    if source_mode == SOURCE_MODE_ASSET_MANIFEST:
        for entry in iter_asset_manifest_entries(vault):
            entry_path = as_text(entry.get("path")) or as_text(entry.get("asset_id"))
            if str(entry.get("privacy", "")).lower() == "pii":
                excluded_pii_paths.append(entry_path)
                continue
            if not should_index_asset(entry):
                continue
            semantic = semantic_asset_evidence(entry, vault)
            if semantic.get("pii"):
                excluded_pii_paths.append(entry_path)
                continue
            meta = asset_entry_metadata(entry, vault, semantic)
            record_id = f"asset:{as_text(entry.get('asset_id')) or sha256_text(entry_path)[:16]}"
            old_source = old_sources.get(record_id, {})
            old_record = old_records.get(record_id)
            if source_unchanged(old_manifest, old_source, meta, old_record, source_mode):
                record = old_record
                reused += 1
            else:
                record = make_asset_record(entry, vault, semantic)
                indexed += 1
            source_records[record_id] = record
            sources[record_id] = meta

        records_by_id = {record["record_id"]: record for record in source_records.values()}
        current_record_ids = set(records_by_id)
        removed = len(set(old_records) - current_record_ids)
        records = [records_by_id[record_id] for record_id in sorted(records_by_id)]
        summary = BuildSummary(
            total_documents=len(records),
            indexed_documents=indexed,
            reused_documents=reused,
            removed_documents=removed,
            excluded_pii_documents=len(excluded_pii_paths),
        )
        manifest = {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "extractor_version": EXTRACTOR_VERSION,
            "summary_version": SUMMARY_VERSION,
            "vault_path": vault.as_posix(),
            "source_mode": source_mode,
            "asset_manifest": asset_manifest_path(vault).as_posix(),
            "generated_at": utc_now(),
            "summary": summary.as_dict(),
            "sources": sources,
            "groups": {},
            "excluded_pii_paths": sorted(excluded_pii_paths),
        }
        write_documents(out_dir, records)
        write_json(out_dir / "manifest.json", manifest)
        write_generated_references(
            out_dir,
            vault,
            records,
            sorted(excluded_pii_paths),
            summary,
            source_mode,
        )
        return summary

    jobs: list[tuple[Path, str, dict[str, Any]]] = []
    for path in iter_markdown_files(vault, out_dir, source_mode):
        relative = rel_path(path, vault)
        if has_pii_tag(path, vault, report_pii_paths):
            excluded_pii_paths.append(relative)
            continue
        if has_archived_tag(path):
            continue
        text = read_text(path)
        meta = source_metadata(path, text)
        old_source = old_sources.get(relative, {})
        record_id = f"doc:{relative}"
        old_record = old_records.get(record_id)
        if source_unchanged(old_manifest, old_source, meta, old_record, source_mode):
            record = old_record
            reused += 1
            source_records[relative] = record
            sources[relative] = meta
        else:
            jobs.append((path, relative, meta))

    worker_count = max(1, llm_workers)
    if jobs and worker_count > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = {
                executor.submit(extract_record_job, path, vault): (relative, meta)
                for path, relative, meta in jobs
            }
            for future in as_completed(futures):
                relative, _ = futures[future]
                _, meta, record = future.result()
                source_records[relative] = record
                sources[relative] = meta
                indexed += 1
    else:
        for path, relative, _ in jobs:
            _, meta, record = extract_record_job(path, vault)
            source_records[relative] = record
            sources[relative] = meta
            indexed += 1

    records_by_id = {record["record_id"]: record for record in source_records.values()}
    groups = {}
    for group_id, members in group_candidates(list(source_records.values())).items():
        group_hash = combined_hash(members)
        old_group = old_groups.get(group_id, {})
        if (
            old_group.get("combined_hash") == group_hash
            and manifest_versions_match(old_manifest, {}, source_mode)
            and group_id in old_records
        ):
            collection = old_records[group_id]
            reused += 1
        else:
            collection = make_collection_record(group_id, members)
            indexed += 1
        records_by_id[group_id] = collection
        groups[group_id] = {
            "source_paths": collection["source_paths"],
            "combined_hash": group_hash,
        }

    current_record_ids = set(records_by_id)
    removed = len(set(old_records) - current_record_ids)
    records = [records_by_id[record_id] for record_id in sorted(records_by_id)]
    summary = BuildSummary(
        total_documents=len(records),
        indexed_documents=indexed,
        reused_documents=reused,
        removed_documents=removed,
        excluded_pii_documents=len(excluded_pii_paths),
    )
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "extractor_version": EXTRACTOR_VERSION,
        "summary_version": SUMMARY_VERSION,
        "vault_path": vault.as_posix(),
        "source_mode": source_mode,
        "generated_at": utc_now(),
        "summary": summary.as_dict(),
        "sources": sources,
        "groups": groups,
        "excluded_pii_paths": sorted(excluded_pii_paths),
    }
    write_documents(out_dir, records)
    write_json(out_dir / "manifest.json", manifest)
    write_generated_references(
        out_dir,
        vault,
        records,
        sorted(excluded_pii_paths),
        summary,
        source_mode,
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path(os.environ.get("SECOND_BRAIN_VAULT", DEFAULT_VAULT)),
        help="Vault root path; defaults to SECOND_BRAIN_VAULT or the configured vault. / 知识库根路径；默认使用 SECOND_BRAIN_VAULT 或已配置的知识库。",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Runtime index output directory outside the installed Skill tree. / 位于已安装 Skill 目录之外的运行时索引输出目录。",
    )
    parser.add_argument("--force", action="store_true", help="Rebuild all documents. / 重建所有文档。")
    parser.add_argument(
        "--source-mode",
        choices=sorted(SOURCE_MODES),
        default=DEFAULT_SOURCE_MODE,
        help="Source scan policy; defaults to SECOND_BRAIN_SOURCE_MODE or agent-readable. / 来源扫描策略；默认使用 SECOND_BRAIN_SOURCE_MODE 或 agent-readable。",
    )
    parser.add_argument(
        "--llm-workers",
        type=int,
        default=DEFAULT_LLM_WORKERS,
        help="Workers for changed/new document extraction and LLM summaries. / 用于变更或新增文档提取与 LLM 摘要的并发 worker 数。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_index(
        args.vault,
        args.out,
        force=args.force,
        llm_workers=args.llm_workers,
        source_mode=args.source_mode,
    )
    print(json.dumps(summary.as_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
