#!/usr/bin/env python3
"""Shared helpers for ClawExpert bundled scripts."""

from __future__ import annotations

import datetime as _dt
import glob
import json
import os
import pathlib
import re
from typing import Iterable

TOKEN_RE = re.compile(r"[A-Za-z0-9\u4e00-\u9fff]+")
LIST_SPLIT_RE = re.compile(r"\s*(?:\||;|；|,|，|/|、)\s*")
SEMANTIC_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "that",
    "this",
    "topic",
    "node",
    "method",
    "methods",
    "study",
    "analysis",
    "framework",
    "frameworks",
    "system",
    "systems",
    "方法",
    "研究",
    "分析",
    "问题",
    "系统",
    "框架",
}
GENERIC_QUERY_FILLERS = [
    "之间的",
    "之间",
    "如何",
    "什么是",
    "是什么",
    "关于",
    "有关",
    "的",
    "和",
    "与",
    "及",
]


def knowledge_dir(value: str | None = None) -> pathlib.Path:
    if value:
        return pathlib.Path(value).expanduser().resolve()
    return pathlib.Path.home().joinpath(".openclaw", "workspace", "knowledge").resolve()


def utc_now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def topic_dir(kb: pathlib.Path, slug: str) -> pathlib.Path:
    return kb / slug


def meta_path(kb: pathlib.Path, slug: str) -> pathlib.Path:
    return topic_dir(kb, slug) / "meta.json"


def progress_path(kb: pathlib.Path, slug: str, subtopic_id: str) -> pathlib.Path:
    return topic_dir(kb, slug) / f"progress-{subtopic_id}.json"


def flag_path(kb: pathlib.Path, slug: str, subtopic_id: str) -> pathlib.Path:
    return topic_dir(kb, slug) / f"done-{subtopic_id}.flag"


def ensure_dir(path: pathlib.Path) -> pathlib.Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: pathlib.Path, default=None):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: pathlib.Path, data) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def count_source_files(topic_root: pathlib.Path) -> int:
    web = glob.glob(str(topic_root / "raw" / "web" / "*.md"))
    pdf_single = glob.glob(str(topic_root / "raw" / "pdf" / "*.md"))
    pdf_split = glob.glob(str(topic_root / "raw" / "pdf" / "*" / "_index.md"))
    return len(web) + len(pdf_single) + len(pdf_split)


def count_formal_nodes(topic_root: pathlib.Path) -> int:
    return len(glob.glob(str(topic_root / "nodes" / "node-*.md")))


def list_formal_nodes(topic_root: pathlib.Path) -> list[pathlib.Path]:
    return sorted((topic_root / "nodes").glob("node-*.md"))


def list_framework_nodes(topic_root: pathlib.Path) -> list[pathlib.Path]:
    return sorted((topic_root / "nodes").glob("framework-*.md"))


def list_all_knowledge_nodes(topic_root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(list_formal_nodes(topic_root) + list_framework_nodes(topic_root))


def list_subtopic_nodes(topic_root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(topic_root.glob("nodes/sub-*/node*.md"))


def list_flags(topic_root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(topic_root.glob("done-*.flag"))


def list_progress_files(topic_root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(topic_root.glob("progress-*.json"))


def slugify(text: str, max_length: int = 60) -> str:
    text = text.strip().lower()
    chars: list[str] = []
    for char in text:
        if char.isascii() and (char.isalnum() or char == "-"):
            chars.append(char)
            continue
        if _is_cjk(char) or char.isdigit():
            chars.append(char)
            continue
        chars.append("-")
    slug = re.sub(r"-{2,}", "-", "".join(chars)).strip("-")
    if not slug:
        slug = "topic"
    return slug[:max_length].rstrip("-")


def _is_cjk(char: str) -> bool:
    code = ord(char)
    return (
        0x3400 <= code <= 0x4DBF
        or 0x4E00 <= code <= 0x9FFF
        or 0xF900 <= code <= 0xFAFF
    )


def parse_frontmatter_and_body(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    raw_meta, body = parts
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body.lstrip()


def split_inline_list(value: str | None) -> list[str]:
    if not value:
        return []
    if "\n" in value:
        parts = [line.strip("- ").strip() for line in value.splitlines()]
    else:
        parts = LIST_SPLIT_RE.split(value.strip())
    output: list[str] = []
    seen: set[str] = set()
    for item in parts:
        normalized = normalize_space(item)
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        output.append(normalized)
    return output


def extract_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    current: list[str] = []
    capture = False
    pattern = f"## {heading}".strip()
    for line in lines:
        if line.strip() == pattern:
            capture = True
            current = []
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            current.append(line)
    return "\n".join(current).strip()


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def best_label(frontmatter: dict[str, str], body: str, fallback: str) -> str:
    label = normalize_space(frontmatter.get("label", "")) or fallback
    if re.match(r"^(node|framework|subtopic|topic)-\d+", label.lower()):
        heading = first_heading(body)
        if heading:
            return heading
    return label


def extract_bullets(section: str) -> list[str]:
    bullets: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
        elif re.match(r"^\d+\.\s+", stripped):
            bullets.append(re.sub(r"^\d+\.\s+", "", stripped))
    return bullets


def extract_checklist_items(section: str, checked: bool | None = None) -> list[str]:
    items: list[str] = []
    pattern = re.compile(r"^- \[(?P<mark>[ xX])\]\s+(?P<text>.+?)\s*$")
    for line in section.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        is_checked = match.group("mark").lower() == "x"
        if checked is None or checked == is_checked:
            items.append(match.group("text").strip())
    return items


def first_paragraph(text: str) -> str:
    chunks = [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]
    return chunks[0] if chunks else ""


def first_sentence(text: str) -> str:
    text = " ".join(text.split())
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?。！？])\s+", text)
    return parts[0].strip()


def relpath(target: pathlib.Path, start: pathlib.Path) -> str:
    return pathlib.Path(os.path.relpath(target, start)).as_posix()


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: pathlib.Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def sum_int(values: Iterable[int]) -> int:
    total = 0
    for value in values:
        total += int(value)
    return total


def normalize_space(text: str) -> str:
    return " ".join(str(text).split()).strip()


def compact_text(text: str) -> str:
    return "".join(char.lower() for char in str(text) if char.isalnum() or _is_cjk(char))


def semantic_strip(text: str) -> str:
    cleaned = normalize_space(text).lower()
    for filler in sorted(GENERIC_QUERY_FILLERS, key=len, reverse=True):
        cleaned = cleaned.replace(filler.lower(), "")
    return compact_text(cleaned)


def cjk_phrase_abbreviation(text: str) -> str:
    stripped = semantic_strip(text)
    chars = [char for char in stripped if _is_cjk(char)]
    if len(chars) >= 4 and len(chars) % 2 == 0:
        return "".join(chars[idx] for idx in range(0, len(chars), 2))
    return ""


def semantic_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for token in TOKEN_RE.findall(str(text).lower()):
        token = normalize_space(token)
        if len(token) <= 1:
            continue
        tokens.add(token)
        if all(_is_cjk(ch) for ch in token):
            if len(token) <= 8 and len(token) % 2 == 0:
                for idx in range(0, len(token), 2):
                    piece = token[idx : idx + 2]
                    if len(piece) == 2:
                        tokens.add(piece)
            for idx in range(len(token) - 1):
                bigram = token[idx : idx + 2]
                if len(bigram) == 2:
                    tokens.add(bigram)
    return {token for token in tokens if token not in SEMANTIC_STOPWORDS}


def char_bigrams(text: str) -> set[str]:
    compact = semantic_strip(text)
    if len(compact) < 2:
        return {compact} if compact else set()
    return {compact[idx : idx + 2] for idx in range(len(compact) - 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def semantic_signature(texts: Iterable[str]) -> dict[str, object]:
    raw_values = [normalize_space(text) for text in texts if normalize_space(text)]
    compact_values = {compact_text(text) for text in raw_values if compact_text(text)}
    stripped_values = {semantic_strip(text) for text in raw_values if semantic_strip(text)}
    abbreviations = {abbr for text in raw_values if (abbr := cjk_phrase_abbreviation(text))}
    token_sets = [semantic_tokens(text) for text in raw_values]
    bigram_sets = [char_bigrams(text) for text in raw_values]
    tokens: set[str] = set()
    bigrams: set[str] = set()
    for token_set in token_sets:
        tokens.update(token_set)
    for bigram_set in bigram_sets:
        bigrams.update(bigram_set)
    return {
        "texts": raw_values,
        "compact": compact_values,
        "stripped": stripped_values,
        "abbreviations": abbreviations,
        "tokens": tokens,
        "bigrams": bigrams,
    }


def frontmatter_aliases(frontmatter: dict[str, str]) -> list[str]:
    aliases: list[str] = []
    for key in ("aliases", "alternate_labels", "routing_aliases"):
        aliases.extend(split_inline_list(frontmatter.get(key)))
    canonical = normalize_space(frontmatter.get("canonical_intent", ""))
    if canonical:
        aliases.append(canonical)
    return split_inline_list(" | ".join(aliases))
