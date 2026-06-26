#!/usr/bin/env python3
"""从最新的日期日报文件生成或刷新 <应用根目录>/daily.json。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DATE_FILE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})\.md$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)(.*\S)\s*$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IGNORE_DIRS = {
    ".git",
    ".next",
    ".cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "tmp",
}

RECENT_HINTS = (
    "进展",
    "完成",
    "已",
    "解决",
    "修复",
    "发布",
    "上线",
    "结论",
    "决定",
    "发现",
    "更新",
    "风险",
    "阻塞",
    "问题",
    "异常",
    "important",
    "progress",
    "decision",
    "decided",
    "resolved",
    "fix",
    "fixed",
    "risk",
    "blocker",
    "issue",
    "update",
    "summary",
)
TOMORROW_HINTS = (
    "明天",
    "明日",
    "下周",
    "todo",
    "follow up",
    "follow-up",
    "next",
    "tomorrow",
)
ACTION_HINTS = (
    "待",
    "跟进",
    "确认",
    "推进",
    "修复",
    "排查",
    "补充",
    "继续",
    "安排",
    "重跑",
    "investigate",
    "confirm",
    "check",
    "verify",
    "ship",
    "prepare",
    "action",
)
BACKGROUND_HINTS = (
    "背景",
    "context",
    "overview",
    "简介",
    "介绍",
    "参考",
    "资料",
    "摘抄",
    "引用",
    "link",
    "链接",
)
EVENT_HINTS = (
    "今日",
    "今天",
    "发生",
    "讨论",
    "用户",
    "会议",
    "任务",
    "chat",
    "event",
    "meeting",
    "user",
    "calendar",
    "task",
)
TIME_PREFIX_RE = re.compile(r"^(?:\[[^\]]+\]\s*)+")
WHITESPACE_RE = re.compile(r"\s+")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[。！？!?；;])")


@dataclass(order=True)
class JournalCandidate:
    date_text: str
    journal_score: int
    relpath_length: int
    mtime: float
    path: Path
    relpath: str


@dataclass
class ContentBlock:
    kind: str
    text: str
    headings: list[str]
    order: int


@dataclass
class ExtractedPoint:
    text: str
    recent_score: int
    tomorrow_score: int
    order: int
    actionable: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--app-root",
        default=".",
        help="目标应用的根目录",
    )
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_existing_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def journal_path_score(relpath: str) -> int:
    lowered = relpath.lower()
    parts = [part.lower() for part in Path(relpath).parts]
    score = 0
    if "daily" in parts:
        score += 5
    if "journal" in parts:
        score += 5
    if "journals" in parts:
        score += 4
    if "log" in parts or "logs" in parts:
        score += 2
    if "note" in parts or "notes" in parts:
        score += 1
    if "/daily/" in lowered or "\\daily\\" in lowered:
        score += 2
    if "/journal/" in lowered or "\\journal\\" in lowered:
        score += 2
    return score


def find_latest_journal(app_root: Path) -> JournalCandidate | None:
    candidates: list[JournalCandidate] = []
    for root, dirs, files in os.walk(app_root, topdown=True):
        dirs[:] = [name for name in dirs if name not in IGNORE_DIRS]
        root_path = Path(root)
        for filename in files:
            match = DATE_FILE_RE.match(filename)
            if not match:
                continue
            file_path = root_path / filename
            relpath = file_path.relative_to(app_root).as_posix()
            stat = file_path.stat()
            candidates.append(
                JournalCandidate(
                    date_text=match.group("date"),
                    journal_score=journal_path_score(relpath),
                    relpath_length=len(relpath),
                    mtime=stat.st_mtime,
                    path=file_path,
                    relpath=relpath,
                )
            )

    if not candidates:
        return None

    latest_date = max(candidate.date_text for candidate in candidates)
    same_day = [candidate for candidate in candidates if candidate.date_text == latest_date]
    same_day.sort(
        key=lambda item: (
            -item.journal_score,
            item.relpath_length,
            -item.mtime,
            item.relpath,
        )
    )
    return same_day[0]


def strip_markdown(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = text.replace("`", "")
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("_", "")
    text = text.replace("~~", "")
    text = WHITESPACE_RE.sub(" ", text).strip()
    return text


def normalize_point_text(text: str, limit: int = 140) -> str:
    text = strip_markdown(text)
    text = TIME_PREFIX_RE.sub("", text).strip(" -:：")
    if len(text) <= limit:
        return text

    sentences = split_sentences(text)
    if sentences:
        truncated = []
        size = 0
        for sentence in sentences:
            projected = size + len(sentence) + (1 if truncated else 0)
            if projected > limit and truncated:
                break
            truncated.append(sentence)
            size = projected
            if size >= limit * 0.7:
                break
        text = " ".join(truncated).strip()

    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_BOUNDARY_RE.split(text) if part.strip()]


def parse_markdown_blocks(raw_text: str) -> list[ContentBlock]:
    lines = raw_text.splitlines()
    blocks: list[ContentBlock] = []
    headings: list[tuple[int, str]] = []
    order = 0
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = strip_markdown(heading_match.group(2))
            headings = [item for item in headings if item[0] < level]
            headings.append((level, heading_text))
            index += 1
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            item_lines = [bullet_match.group(1).strip()]
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if not candidate.strip():
                    index += 1
                    break
                if HEADING_RE.match(candidate) or BULLET_RE.match(candidate):
                    break
                item_lines.append(candidate.strip())
                index += 1
            blocks.append(
                ContentBlock(
                    kind="bullet",
                    text=strip_markdown(" ".join(item_lines)),
                    headings=[text for _, text in headings],
                    order=order,
                )
            )
            order += 1
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                index += 1
                break
            if HEADING_RE.match(candidate) or BULLET_RE.match(candidate):
                break
            paragraph_lines.append(candidate.strip())
            index += 1
        paragraph_text = strip_markdown(" ".join(paragraph_lines))
        sentences = split_sentences(paragraph_text)
        if len(sentences) > 1:
            for sentence in sentences:
                blocks.append(
                    ContentBlock(
                        kind="paragraph",
                        text=sentence,
                        headings=[text for _, text in headings],
                        order=order,
                    )
                )
                order += 1
        else:
            blocks.append(
                ContentBlock(
                    kind="paragraph",
                    text=paragraph_text,
                    headings=[text for _, text in headings],
                    order=order,
                )
            )
            order += 1

    return [block for block in blocks if block.text]


def contains_any(text: str, hints: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(hint.lower() in lowered for hint in hints)


def looks_like_timestamped_event(text: str) -> bool:
    return bool(re.search(r"\b\d{1,2}:\d{2}\b", text) or re.search(r"\b20\d{2}-\d{2}-\d{2}\b", text))


def classify_block(block: ContentBlock) -> ExtractedPoint | None:
    text = normalize_point_text(block.text)
    if not text or len(text) < 8:
        return None

    context = " / ".join(block.headings)
    combined = f"{context} {text}".strip()
    recent_score = 0
    tomorrow_score = 0

    if block.kind == "bullet":
        recent_score += 1
        tomorrow_score += 1

    if contains_any(combined, RECENT_HINTS):
        recent_score += 3
    if contains_any(combined, TOMORROW_HINTS):
        tomorrow_score += 4
    if contains_any(combined, ACTION_HINTS):
        tomorrow_score += 2
    if contains_any(combined, EVENT_HINTS) or looks_like_timestamped_event(text):
        recent_score += 2
    if contains_any(combined, BACKGROUND_HINTS):
        recent_score -= 2
        tomorrow_score -= 2

    if any(keyword in context.lower() for keyword in ("summary", "总结", "overview", "回顾")):
        recent_score += 2
    if any(keyword in context.lower() for keyword in ("next", "tomorrow", "follow", "todo", "明日", "明天", "后续")):
        tomorrow_score += 3

    actionable = contains_any(text, TOMORROW_HINTS) or contains_any(text, ACTION_HINTS)

    if len(text) > 160:
        recent_score -= 1
        tomorrow_score -= 1

    if recent_score <= 0 and tomorrow_score <= 0:
        return None

    return ExtractedPoint(
        text=text,
        recent_score=recent_score,
        tomorrow_score=tomorrow_score,
        order=block.order,
        actionable=actionable,
    )


def dedupe_points(points: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for point in points:
        normalized = point.strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered in seen:
            continue
        deduped.append(normalized)
        seen.add(lowered)
    return deduped


def fallback_points(blocks: list[ContentBlock], limit: int = 3) -> list[str]:
    points: list[str] = []
    for block in blocks:
        text = normalize_point_text(block.text)
        if len(text) < 12:
            continue
        points.append(text)
        if len(points) == limit:
            break
    return dedupe_points(points)


def extract_points(raw_text: str) -> tuple[list[str], list[str]]:
    blocks = parse_markdown_blocks(raw_text)
    extracted = [point for block in blocks if (point := classify_block(block)) is not None]

    best_by_text: dict[str, ExtractedPoint] = {}
    for point in extracted:
        existing = best_by_text.get(point.text)
        if existing is None or (
            point.recent_score + point.tomorrow_score,
            -point.order,
        ) > (
            existing.recent_score + existing.tomorrow_score,
            -existing.order,
        ):
            best_by_text[point.text] = point

    recent_bucket: list[ExtractedPoint] = []
    tomorrow_bucket: list[ExtractedPoint] = []
    for point in best_by_text.values():
        if point.tomorrow_score > point.recent_score:
            tomorrow_bucket.append(point)
        elif point.recent_score > point.tomorrow_score:
            recent_bucket.append(point)
        elif point.actionable:
            tomorrow_bucket.append(point)
        else:
            recent_bucket.append(point)

    recent_bucket.sort(key=lambda item: (-item.recent_score, item.order, len(item.text)))
    tomorrow_bucket.sort(key=lambda item: (-item.tomorrow_score, item.order, len(item.text)))

    recent_highlights = dedupe_points([item.text for item in recent_bucket[:5]])
    tomorrow_focus = dedupe_points([item.text for item in tomorrow_bucket[:5]])

    if not recent_highlights:
        recent_highlights = [item for item in fallback_points(blocks, limit=4) if item not in tomorrow_focus]
    if not tomorrow_focus:
        fallback_actions = [item.text for item in sorted(extracted, key=lambda item: (-item.tomorrow_score, item.order)) if item.tomorrow_score > 0]
        tomorrow_focus = dedupe_points(fallback_actions[:3])

    if tomorrow_focus:
        recent_highlights = [item for item in recent_highlights if item not in tomorrow_focus]
        if not recent_highlights:
            recent_highlights = fallback_points(blocks, limit=3)
            recent_highlights = [item for item in recent_highlights if item not in tomorrow_focus]

    return recent_highlights[:5], tomorrow_focus[:5]


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def placeholder_payload(timestamp: str) -> dict[str, Any]:
    return {
        "来源日期": None,
        "来源相对路径": None,
        "来源指纹": None,
        "生成时间": timestamp,
        "最后检查时间": timestamp,
        "Todo_Agent_RecentHighlights_Field": [],
        "Todo_Agent_TomorrowsFocus_Field": [],
    }


def failed_payload(timestamp: str, candidate: JournalCandidate | None) -> dict[str, Any]:
    return {
        "来源日期": candidate.date_text if candidate else None,
        "来源相对路径": candidate.relpath if candidate else None,
        "来源指纹": None,
        "生成时间": timestamp,
        "最后检查时间": timestamp,
        "Todo_Agent_RecentHighlights_Field": [],
        "Todo_Agent_TomorrowsFocus_Field": [],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    app_root = Path(args.app_root).resolve()
    if not app_root.exists() or not app_root.is_dir():
        raise SystemExit(f"无效的 --app-root: {app_root}")

    output_path = app_root / "daily.json"
    timestamp = now_iso()
    existing = load_existing_json(output_path)
    candidate = find_latest_journal(app_root)

    if candidate is None:
        if existing is None:
            write_json(output_path, placeholder_payload(timestamp))
            print(f"{output_path}\t已初始化空文件")
        else:
            existing["最后检查时间"] = timestamp
            write_json(output_path, existing)
            print(f"{output_path}\t已检查但暂无来源")
        return

    try:
        raw_text = candidate.path.read_text(encoding="utf-8")
    except OSError:
        write_json(output_path, failed_payload(timestamp, candidate))
        print(f"{output_path}\t解析失败")
        return

    fingerprint = sha256_text(raw_text)
    if existing and existing.get("来源指纹") == fingerprint:
        existing["最后检查时间"] = timestamp
        write_json(output_path, existing)
        print(f"{output_path}\t无变化")
        return

    try:
        recent_highlights, tomorrow_focus = extract_points(raw_text)
    except Exception:
        write_json(output_path, failed_payload(timestamp, candidate))
        print(f"{output_path}\t解析失败")
        return

    payload = {
        "来源日期": candidate.date_text,
        "来源相对路径": candidate.relpath,
        "来源指纹": fingerprint,
        "生成时间": timestamp,
        "最后检查时间": timestamp,
        "Todo_Agent_RecentHighlights_Field": recent_highlights,
        "Todo_Agent_TomorrowsFocus_Field": tomorrow_focus,
    }
    write_json(output_path, payload)
    print(f"{output_path}\t已更新")


if __name__ == "__main__":
    main()
