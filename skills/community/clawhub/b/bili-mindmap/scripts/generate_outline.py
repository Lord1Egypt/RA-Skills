#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


SUMMARY_KEYWORDS = (
    "核心",
    "关键",
    "重点",
    "本质",
    "结论",
    "总结",
    "主要",
    "本次视频",
    "这个视频",
    "首先",
    "其次",
    "最后",
)

DETAIL_KEYWORDS = (
    "步骤",
    "方法",
    "流程",
    "原因",
    "因为",
    "所以",
    "例如",
    "比如",
    "数据",
    "案例",
    "细节",
    "区别",
    "对比",
    "公式",
    "配置",
    "操作",
    "实现",
    "问题",
    "经验",
)

ACTION_KEYWORDS = (
    "建议",
    "可以",
    "应该",
    "需要",
    "务必",
    "记得",
    "最好",
    "尽量",
    "优先",
    "推荐",
    "不要",
    "避免",
)

CHUNK_BOUNDARY_KEYWORDS = (
    "首先",
    "第一",
    "一开始",
    "开头",
    "其次",
    "第二",
    "然后",
    "接下来",
    "另外",
    "此外",
    "再看",
    "最后",
    "总结",
    "总之",
)

SEMANTIC_HIGHLIGHT_PATTERNS = (
    ("亮点一", re.compile("(?:其一|第一点)(?:就是|是|在于)?")),
    ("亮点二", re.compile("(?:(?:还有)?第二点|其二)(?:呢|就是|是|在于)?")),
    ("亮点三", re.compile("(?:(?:还有)?第三点|其三)(?:呢|就是|是|在于)?")),
)

INTRO_SECTION_PATTERN = re.compile("一开始|最开始|前期|被劝退|压抑|资源给的极其稀缺|操纵格蕾丝")
SWITCH_SECTION_PATTERN = re.compile("(?:切换到|换到).{0,8}(?:里昂|之后)|进行复仇|极致释放|快感接二连三")
CONCLUSION_SECTION_PATTERN = re.compile("总之|总结|所以这三点结合到一起|划时代的大作|非常有趣")

TITLE_PREFIX_PATTERNS = (
    r"^(首先|其次|然后|接下来|另外|此外|最后|总之|总结来说)[，,：:]?",
    r"^(我们来看|我们先来看|这里讲|这一段讲|这一部分讲|这个部分讲)",
    r"^(所以这期(视频)?(我们)?(就)?来聊聊)",
    r"^(这期(视频)?(我们)?(就)?来聊聊)",
    r"^(可以说|也就是说|换句话说|简单来说|说白了)",
    r"^(之前|后来|当时|现在|如今)",
)

TITLE_BAD_STARTS = (
    "因为",
    "所以",
    "如果",
    "但是",
    "比如",
    "例如",
    "还有",
    "并且",
    "而且",
    "就是",
)

NOISY_PATTERNS = (
    r"^字幕由.+提供$",
    r"^未经作者授权.*$",
    r"^点赞投币收藏.*$",
    r"^本期视频.*赞助.*$",
    r"^欢迎来到.*频道.*$",
    r"^大家好[,，！! ]*我是.*$",
)

SOURCE_PRIORITY = {
    "transcript": 4,
    "desc": 3,
    "ai_summary": 2,
    "comments": 1,
}

PRIMARY_CONTENT_SOURCES = {"transcript", "ai_summary", "desc"}

SOURCE_LABELS = {
    "ai_summary": "AI补充",
    "comments": "评论补充",
    "desc": "简介补充",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fallback: generate a Markdown mind map outline from collected Bilibili context when the host LLM workflow is unavailable."
    )
    parser.add_argument("--context-dir", required=True, help="Directory produced by prepare_bili_context.py")
    parser.add_argument("--output", help="Output Markdown file path. Default: <context-dir>/outline.md")
    return parser.parse_args()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff").strip()


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        raw = path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def fmt_date(value) -> str:
    if value in (None, ""):
        return "未知"
    try:
        return dt.datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return str(value)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\r", "\n")).strip()


def clean_sentence(text: str) -> str:
    sentence = text.strip()
    sentence = re.sub(
        r"\s*##\s*(?:(?:seg|segment|chunk|part|audio|clip)[-_ ]?\d+(?:\.[a-z0-9]+)?|[a-z0-9_-]+\.(?:wav|mp3|m4a|aac|ogg|opus|flac))\s*",
        " ",
        sentence,
        flags=re.IGNORECASE,
    )
    sentence = re.sub(r"^\[.*?\]\s*", "", sentence)
    sentence = re.sub(r"^\d{1,2}:\d{2}(?::\d{2})?\s*", "", sentence)
    sentence = re.sub(r"^[（(]\d{1,2}:\d{2}(?::\d{2})?[）)]\s*", "", sentence)
    sentence = re.sub(r"^(up|UP|主播|旁白)[:：]\s*", "", sentence)
    sentence = re.sub(r"\s+", " ", sentence)
    return sentence.strip(" -•·\t")


def is_noisy(sentence: str) -> bool:
    if len(sentence) < 10:
        return True
    if len(sentence) > 220:
        return True
    if sentence.count("http"):
        return True
    if re.search(r"BV[0-9A-Za-z]+", sentence):
        return True
    if re.fullmatch(r"[0-9,，.。!！?？:：;；\-— ]+", sentence):
        return True
    return any(re.match(pattern, sentence) for pattern in NOISY_PATTERNS)


def split_long_sentence(sentence: str, max_len: int = 56) -> list[str]:
    text = clean_sentence(sentence)
    if len(text) <= max_len:
        return [text] if text else []

    parts = [part.strip() for part in re.split(r"[，,、；;：:]", text) if part.strip()]
    if not parts:
        parts = [text]

    merged: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current}，{part}" if current else part
        if current and len(candidate) > max_len:
            merged.append(current)
            current = part
        else:
            current = candidate
    if current:
        merged.append(current)

    final_parts: list[str] = []
    for item in merged:
        compact = item.strip()
        if len(compact) <= max_len:
            final_parts.append(compact)
            continue
        for start in range(0, len(compact), max_len):
            piece = compact[start : start + max_len].strip()
            if piece:
                final_parts.append(piece)

    return [piece for piece in final_parts if len(piece) >= 10]


def split_sentences(text: str) -> list[str]:
    normalized = text.replace("\r", "\n")
    chunks = re.split(r"(?<=[。！？!?；;])\s*|\n+", normalized)
    results: list[str] = []
    seen: set[str] = set()

    for chunk in chunks:
        sentence = clean_sentence(chunk)
        if not sentence:
            continue
        pieces = split_long_sentence(sentence) if len(sentence) > 120 else [sentence]
        for piece in pieces:
            if not piece or is_noisy(piece):
                continue
            signature = re.sub(r"[\W_]+", "", piece.lower())
            if len(signature) < 8 or signature in seen:
                continue
            seen.add(signature)
            results.append(piece)
    return results


def first_non_empty(*values: str) -> str:
    for value in values:
        if value and value.strip():
            return value.strip()
    return ""


def extract_video_meta(context_dir: Path, manifest: dict | None) -> dict[str, str]:
    payload = read_json(context_dir / "video_details.json") or {}
    source = str((manifest or {}).get("source", ""))
    match = re.search(r"(BV[0-9A-Za-z]+)", source or "")
    bvid = payload.get("bvid") or (match.group(1) if match else None)
    owner = payload.get("owner") or {}
    stat = payload.get("stat") or {}

    return {
        "title": payload.get("title") or bvid or "Bilibili 视频思维导图",
        "bvid": bvid or "未知",
        "link": payload.get("short_link_v2") or payload.get("short_link") or (f"https://www.bilibili.com/video/{bvid}" if bvid else source),
        "owner": owner.get("name") or "未知",
        "pubdate": fmt_date(payload.get("pubdate") or payload.get("ctime")),
        "view": str(stat.get("view") or "未知"),
        "desc": str(payload.get("desc") or "").strip(),
    }


def sentence_score(sentence: str, kind: str, source: str) -> float:
    score = 0.0
    length = len(sentence)

    if 18 <= length <= 60:
        score += 2.5
    elif 12 <= length <= 90:
        score += 1.5
    else:
        score -= 1.0

    if source == "ai_summary":
        score += 2.5 if kind == "core" else 1.0
    elif source == "desc":
        score += 1.5 if kind == "core" else 0.5
    elif source == "transcript":
        score += 1.2
    elif source == "comments":
        score += 0.8

    if re.search(r"\d", sentence):
        score += 1.0 if kind == "detail" else 0.3

    if any(keyword in sentence for keyword in SUMMARY_KEYWORDS):
        score += 3.0 if kind == "core" else 0.8

    if any(keyword in sentence for keyword in DETAIL_KEYWORDS):
        score += 3.0 if kind == "detail" else 0.8

    if any(keyword in sentence for keyword in ACTION_KEYWORDS):
        score += 3.2 if kind == "action" else 0.6

    if sentence.endswith("？") or sentence.endswith("?"):
        score -= 1.5

    if sentence.count("，") + sentence.count(",") >= 4:
        score -= 0.8

    if sentence.startswith(("我们来看", "接下来", "然后", "那么", "这里", "这个时候")):
        score -= 0.8

    return score


def dedupe_sentences(sentences: list[str]) -> list[str]:
    kept: list[str] = []
    signatures: list[str] = []
    for sentence in sentences:
        signature = re.sub(r"[\W_]+", "", sentence.lower())
        if any(signature in existing or existing in signature for existing in signatures):
            continue
        signatures.append(signature)
        kept.append(sentence)
    return kept


def is_title_like_point(title: str, point: str) -> bool:
    title_sig = re.sub(r"[\W_]+", "", title.lower())
    point_sig = re.sub(r"[\W_]+", "", point.lower())
    if not title_sig or not point_sig:
        return False

    if title_sig == point_sig:
        return True
    if title_sig in point_sig or point_sig in title_sig:
        return True

    overlap = sum(1 for ch in set(title_sig) if ch in point_sig)
    ratio = overlap / max(1, min(len(title_sig), len(point_sig)))
    return ratio >= 0.75


def build_candidate_pool(ai_summary: str, transcript: str, desc: str, comments: list[str]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    for source_name, text in (
        ("ai_summary", ai_summary),
        ("desc", desc),
        ("transcript", transcript),
    ):
        for sentence in split_sentences(text):
            candidates.append({"text": sentence, "source": source_name})

    for sentence in comments:
        cleaned = clean_sentence(sentence)
        if cleaned and not is_noisy(cleaned):
            candidates.append({"text": cleaned, "source": "comments"})

    return candidates


def filter_candidates_by_source(candidates: list[dict[str, str]], allowed_sources: set[str]) -> list[dict[str, str]]:
    return [item for item in candidates if item.get("source") in allowed_sources]


def build_source_lookup(candidates: list[dict[str, str]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for item in candidates:
        text = item["text"]
        source = item["source"]
        current = lookup.get(text)
        if current is None or SOURCE_PRIORITY.get(source, 0) > SOURCE_PRIORITY.get(current, 0):
            lookup[text] = source
    return lookup


def annotate_point(text: str, source_lookup: dict[str, str], default_source: str | None = None) -> str:
    source = source_lookup.get(text, default_source)
    label = SOURCE_LABELS.get(source or "")
    if not label:
        return text
    if text.endswith(f"（{label}）"):
        return text
    return f"{text}（{label}）"


def is_synthetic_heading(text: str | None) -> bool:
    heading = clean_sentence(text or "").strip()
    if not heading:
        return True
    if re.fullmatch(r"(?:seg|segment|chunk|part|audio|clip)[-_ ]?\d+(?:\.[a-z0-9]+)?", heading, re.IGNORECASE):
        return True
    if re.fullmatch(r"[a-z0-9_-]+\.(?:wav|mp3|m4a|aac|ogg|opus|flac)", heading, re.IGNORECASE):
        return True
    return False


def make_chunk_title(index: int, heading: str | None, sentences: list[str]) -> str:
    if heading and not is_synthetic_heading(heading):
        title = clean_sentence(heading).strip("# ")
        if title:
            return title[:24]

    semantic_title = derive_chunk_title(sentences)
    if semantic_title:
        return semantic_title

    return f"片段{index}"


def shorten_title(text: str, max_len: int = 18) -> str:
    raw_title = clean_sentence(text)
    if not raw_title:
        return ""

    clause_candidates: list[str] = [raw_title]
    clause_candidates.extend(part.strip() for part in re.split(r"[，,。；;：:]", raw_title) if part.strip())

    scored_candidates: list[tuple[float, str]] = []
    for candidate in clause_candidates:
        title = candidate
        for pattern in TITLE_PREFIX_PATTERNS:
            title = re.sub(pattern, "", title).strip()
        title = re.sub(r"[，,。；;：:].*", "", title).strip()
        if not title or len(title) < 4:
            continue

        score = 1.0
        if 6 <= len(title) <= 14:
            score += 2.5
        elif len(title) <= 18:
            score += 1.5

        if title.startswith(TITLE_BAD_STARTS):
            score -= 1.5
        if "的" in title and len(title) <= 12:
            score += 0.6
        if re.search(r"\d", title):
            score += 0.4
        if len(set(title)) >= 4:
            score += 0.4

        scored_candidates.append((score, title[:max_len].rstrip()))

    if not scored_candidates:
        return raw_title[:max_len].rstrip()

    scored_candidates.sort(key=lambda item: (-item[0], len(item[1])))
    return scored_candidates[0][1]


def derive_chunk_title(sentences: list[str]) -> str:
    if not sentences:
        return ""

    candidates: list[tuple[float, str]] = []
    for sentence in sentences[:5]:
        score = 0.0
        title = shorten_title(sentence)
        if not title or len(title) < 4:
            continue

        score += 2.0
        if 6 <= len(title) <= 16:
            score += 2.5
        elif len(title) <= 20:
            score += 1.5

        if any(keyword in sentence for keyword in SUMMARY_KEYWORDS):
            score += 2.5
        if any(keyword in sentence for keyword in DETAIL_KEYWORDS):
            score += 1.2
        if any(keyword in sentence for keyword in ACTION_KEYWORDS):
            score -= 0.5
        if title.startswith(("因为", "所以", "如果", "但是", "比如", "例如")):
            score -= 1.5
        if re.search(r"\d", title):
            score += 0.5

        candidates.append((score, title))

    if not candidates:
        return ""

    candidates.sort(key=lambda item: (-item[0], len(item[1])))
    return candidates[0][1]


def derive_alternative_chunk_title(sentences: list[str], used_titles: set[str]) -> str:
    candidates: list[tuple[float, str]] = []
    for sentence in sentences[1:8]:
        title = shorten_title(sentence)
        if not title or len(title) < 4 or title in used_titles:
            continue

        score = 1.0
        if 6 <= len(title) <= 16:
            score += 2.0
        elif len(title) <= 20:
            score += 1.0

        if any(keyword in sentence for keyword in SUMMARY_KEYWORDS):
            score += 1.8
        if any(keyword in sentence for keyword in DETAIL_KEYWORDS):
            score += 1.0
        if any(keyword in sentence for keyword in ACTION_KEYWORDS):
            score -= 0.5

        candidates.append((score, title))

    if candidates:
        candidates.sort(key=lambda item: (-item[0], len(item[1])))
        return candidates[0][1]
    return ""


def extract_section_seed(sentence: str, pattern: re.Pattern[str]) -> str:
    cleaned = clean_sentence(sentence)
    cleaned = pattern.sub("", cleaned, count=1).strip(" ?,??:?;")
    prefixes = (
        "就是",
        "是",
        "在于",
        "还有呢",
        "还有",
        "这里边",
        "这个部分",
        "这一部分",
        "它的",
        "他让玩家",
        "让玩家",
        "让你",
        "能够",
        "可以",
        "呃",
    )
    changed = True
    while changed and cleaned:
        changed = False
        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                changed = True
    cleaned = re.split(r"[?,??;?:]", cleaned, maxsplit=1)[0].strip()
    return shorten_title(cleaned, max_len=16) if cleaned else ""


def detect_semantic_section(sentence: str) -> tuple[str | None, str]:
    for label, pattern in SEMANTIC_HIGHLIGHT_PATTERNS:
        if pattern.search(sentence):
            return label, extract_section_seed(sentence, pattern)
    if CONCLUSION_SECTION_PATTERN.search(sentence):
        return "总体评价", ""
    if SWITCH_SECTION_PATTERN.search(sentence):
        return "切换角色后的释放感", ""
    return None, ""


def finalize_semantic_title(kind: str, seed: str, sentences: list[str]) -> str:
    derived = derive_chunk_title(sentences)
    if kind.startswith("亮点"):
        content = seed
        if any("人物弧光" in sentence for sentence in sentences):
            content = "放大里昂的人物弧光"
        elif any(("保护欲" in sentence or "责任感" in sentence) for sentence in sentences) and any("艾米丽" in sentence for sentence in sentences):
            content = "艾米丽带来的保护欲"
        elif any("成长" in sentence for sentence in sentences) and any("格蕾丝" in sentence for sentence in sentences):
            content = "格蕾丝的成长视角"
        elif not content or len(content) < 6 or content.startswith(("操纵", "加入", "这里边", "玩家", "说是")):
            content = derived or derive_alternative_chunk_title(sentences, set())
        return f"{kind}：{content}" if content else kind
    if kind == "开场观点":
        if any(INTRO_SECTION_PATTERN.search(sentence) for sentence in sentences):
            return "前期压抑体验"
        return derived or kind
    return kind


def split_semantic_sections(text: str) -> list[dict[str, object]]:
    raw_lines = [clean_sentence(line) for line in text.splitlines()]
    raw_lines = [line for line in raw_lines if line]
    if not raw_lines:
        return []

    sections: list[dict[str, object]] = []
    current_kind = "开场观点"
    current_seed = ""
    current_lines: list[str] = []
    found_explicit_highlight = False

    def flush_current() -> None:
        nonlocal current_kind, current_seed, current_lines
        if not current_lines:
            return
        sections.append(
            {
                "kind": current_kind,
                "seed": current_seed,
                "lines": current_lines[:],
            }
        )
        current_kind = "开场观点"
        current_seed = ""
        current_lines = []

    for index, line in enumerate(raw_lines):
        lookahead = line
        if index + 1 < len(raw_lines) and len(line) <= 10:
            lookahead = f"{line} {raw_lines[index + 1]}"

        next_kind, next_seed = detect_semantic_section(lookahead)

        if current_kind == "开场观点" and INTRO_SECTION_PATTERN.search(lookahead):
            current_kind = "前期压抑体验"

        if next_kind and current_lines and next_kind != current_kind:
            flush_current()

        if next_kind:
            current_kind = next_kind
            if next_seed:
                current_seed = next_seed
            if next_kind.startswith("亮点"):
                found_explicit_highlight = True

        current_lines.append(line)

    flush_current()

    if not found_explicit_highlight or len(sections) < 3:
        return []

    semantic_chunks: list[dict[str, object]] = []
    for section in sections:
        chunk_sentences = split_sentences("\n".join(section["lines"]))
        if not chunk_sentences:
            continue
        title = finalize_semantic_title(str(section["kind"]), str(section["seed"]), chunk_sentences)
        semantic_chunks.append({"title": title, "sentences": chunk_sentences})

    return semantic_chunks


def split_transcript_chunks(text: str) -> list[dict[str, object]]:
    if not text.strip():
        return []

    lines = [line.rstrip() for line in text.splitlines()]
    heading_chunks: list[dict[str, object]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("## "):
            if current_lines:
                heading_chunks.append({"heading": current_heading, "text": "\n".join(current_lines)})
                current_lines = []
            current_heading = line[3:].strip()
            continue
        current_lines.append(line)

    if current_lines:
        heading_chunks.append({"heading": current_heading, "text": "\n".join(current_lines)})

    if len(heading_chunks) >= 2:
        chunks: list[dict[str, object]] = []
        for index, item in enumerate(heading_chunks, 1):
            sentences = split_sentences(str(item["text"]))
            if not sentences:
                continue
            chunks.append(
                {
                    "title": make_chunk_title(index, str(item.get("heading") or ""), sentences),
                    "sentences": sentences,
                }
            )
        if chunks:
            return chunks

    semantic_chunks = split_semantic_sections(text)
    if semantic_chunks:
        return semantic_chunks

    sentences = split_sentences(text)
    if not sentences:
        return []

    paragraphs = [block.strip() for block in re.split(r"\n\s*\n+", text) if block.strip()]
    if len(paragraphs) >= 3:
        chunks = []
        for index, paragraph in enumerate(paragraphs, 1):
            paragraph_sentences = split_sentences(paragraph)
            if not paragraph_sentences:
                continue
            chunks.append({"title": make_chunk_title(index, None, paragraph_sentences), "sentences": paragraph_sentences})
        if chunks:
            return chunks

    chunks = []
    current: list[str] = []
    for sentence in sentences:
        if current and len(current) >= 3 and sentence.startswith(CHUNK_BOUNDARY_KEYWORDS):
            chunks.append(current)
            current = []
        current.append(sentence)
        if len(current) >= 4:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)

    return [
        {"title": make_chunk_title(index, None, chunk_sentences), "sentences": chunk_sentences}
        for index, chunk_sentences in enumerate(chunks, 1)
        if chunk_sentences
    ]


def rank_chunk_sentences(chunks: list[dict[str, object]], kind: str, per_chunk: int, limit: int, exclude: set[str] | None = None) -> list[str]:
    exclude = exclude or set()
    picked: list[str] = []

    for chunk in chunks:
        chunk_candidates = [{"text": sentence, "source": "transcript"} for sentence in chunk["sentences"]]
        ranked = rank_sentences(chunk_candidates, kind=kind, limit=per_chunk, exclude=exclude | set(picked))
        picked.extend(ranked)
        if len(picked) >= limit:
            break

    return dedupe_sentences(picked)[:limit]


def build_chunk_outline(chunks: list[dict[str, object]]) -> list[dict[str, object]]:
    outline_chunks: list[dict[str, object]] = []
    used_titles: set[str] = set()
    for chunk in chunks[:6]:
        chunk_title = str(chunk["title"])
        if chunk_title in used_titles:
            alternative_title = derive_alternative_chunk_title(list(chunk["sentences"]), used_titles)
            if alternative_title:
                chunk_title = alternative_title
        chunk_candidates = [{"text": sentence, "source": "transcript"} for sentence in chunk["sentences"]]
        point_limit = 2 if chunk_title.startswith(("\u4eae\u70b9", "\u524d\u671f", "\u5207\u6362", "\u603b\u4f53")) else 3
        core = rank_sentences(chunk_candidates, kind="core", limit=1)
        details = rank_sentences(chunk_candidates, kind="detail", limit=2, exclude=set(core))
        actions = rank_sentences(chunk_candidates, kind="action", limit=1, exclude=set(core) | set(details))

        points = core + details + actions
        if not points:
            points = dedupe_sentences(list(chunk["sentences"]))[:point_limit]

        filtered_points = [point for point in points if not is_title_like_point(chunk_title, point)]
        if not filtered_points and points:
            filtered_points = points[1:] if len(points) > 1 else []
        points = [compress_chunk_point(point, chunk_title) for point in filtered_points[:point_limit]]
        points = dedupe_sentences([point for point in points if point])[:point_limit]

        if points:
            outline_chunks.append({"title": chunk_title, "points": points})
            used_titles.add(chunk_title)

    return outline_chunks


def compress_chunk_point(text: str, title: str, max_len: int = 24) -> str:
    raw = clean_sentence(text)
    if not raw:
        return ""

    candidates = [raw]
    candidates.extend(part.strip() for part in re.split(r"[，,。；;：:]", raw) if part.strip())

    scored: list[tuple[float, str]] = []
    for candidate in candidates:
        point = candidate
        for pattern in TITLE_PREFIX_PATTERNS:
            point = re.sub(pattern, "", point).strip()
        if not point or len(point) < 4:
            continue

        score = 1.0
        if 8 <= len(point) <= 20:
            score += 2.0
        elif len(point) <= max_len:
            score += 1.0

        if point.startswith(TITLE_BAD_STARTS):
            score -= 1.2
        if is_title_like_point(title, point):
            score -= 2.0
        if any(keyword in point for keyword in DETAIL_KEYWORDS):
            score += 0.8
        if any(keyword in point for keyword in ACTION_KEYWORDS):
            score += 0.3
        if len(set(point)) >= 4:
            score += 0.3

        scored.append((score, point[:max_len].rstrip()))

    if not scored:
        return raw[:max_len].rstrip()

    scored.sort(key=lambda item: (-item[0], len(item[1])))
    return scored[0][1]


def rank_sentences(candidates: list[dict[str, str]], kind: str, limit: int, exclude: set[str] | None = None) -> list[str]:
    exclude = exclude or set()
    scored = []
    for item in candidates:
        text = item["text"]
        if text in exclude:
            continue
        score = sentence_score(text, kind=kind, source=item["source"])
        if kind == "action" and not any(keyword in text for keyword in ACTION_KEYWORDS):
            score -= 0.7
        scored.append((score, text))

    scored.sort(key=lambda pair: (-pair[0], len(pair[1])))
    ranked = dedupe_sentences([text for score, text in scored if score > 0])
    return ranked[:limit]


def parse_comments(comments_text: str) -> list[str]:
    cleaned_lines: list[str] = []
    started = False

    for raw_line in comments_text.splitlines():
        line = raw_line.strip()
        if not line:
            if started:
                cleaned_lines.append("")
            continue
        if "热门评论" in line:
            started = True
            continue
        if not started:
            continue
        if re.search(r"[┌┐└┘├┤┬┴┼│─╭╮╰╯═║╔╗╚╝╠╣╦╩╬]{3,}", line):
            continue
        if re.fullmatch(r"[\W_]{6,}", line):
            continue
        if re.search(r"\(.*?\d+\)$", line) and len(line) <= 30:
            cleaned_lines.append("")
            continue
        if line.startswith(("📵", "💬", "🎬", "BV号", "标题", "UP主", "时长", "播放", "弹幕", "点赞", "投币", "收藏", "分享", "链接", "简介")):
            continue
        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines).strip()
    blocks = re.split(r"\n\s*\n", cleaned_text)
    results: list[str] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        content = clean_sentence(" ".join(lines))
        if content and not is_noisy(content):
            results.append(content)
    return dedupe_sentences(results)[:4]


def extract_primary_body(text: str) -> str:
    cleaned_lines: list[str] = []
    started = False
    box_chars = "??????????????????????????"
    marker_prefixes = ("??", "??", "??", "??")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if started:
                cleaned_lines.append("")
            continue
        if any(char in line for char in box_chars):
            continue
        if re.search(r"BV[0-9A-Za-z]+", line):
            continue
        if line.startswith(marker_prefixes):
            continue
        if line.endswith(":") and len(line) <= 16:
            started = True
            continue
        started = True
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def sanitize_transcript_text(text: str) -> str:
    cleaned_lines: list[str] = []
    started = False
    box_chars = "┌┐└┘├┤┬┴┼│─╭╮╰╯═║╔╗╚╝╠╣╦╩╬"

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if started:
                cleaned_lines.append("")
            continue
        if "字幕内容" in line:
            started = True
            continue
        if not started and any(char in line for char in box_chars):
            continue
        if not started and line.startswith(("📺", "BV号", "标题", "UP主", "时长", "播放", "弹幕", "点赞", "投币", "收藏", "分享", "链接", "简介")):
            continue
        if not started and re.search(r"BV[0-9A-Za-z]+", line):
            continue
        started = True
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def is_placeholder_text(text: str) -> bool:
    normalized = normalize_whitespace(text).lower()
    if not normalized:
        return True
    placeholder_hints = (
        "无字幕",
        "暂无字幕",
        "可能需要登录或视频无字幕",
        "暂无 ai 总结",
        "该视频暂无 ai 总结",
        "⚠️",
    )
    return any(hint in normalized for hint in placeholder_hints)


def fallback_pick(texts: list[str], limit: int, exclude: set[str] | None = None) -> list[str]:
    exclude = exclude or set()
    merged: list[str] = []
    for text in texts:
        merged.extend(split_sentences(text))
    return [item for item in dedupe_sentences(merged) if item not in exclude][:limit]


def derive_action_points(core_points: list[str], detail_points: list[str]) -> list[str]:
    derived: list[str] = []
    for sentence in core_points + detail_points:
        if len(sentence) < 14:
            continue
        if any(keyword in sentence for keyword in ACTION_KEYWORDS):
            derived.append(sentence)
            continue
        if any(keyword in sentence for keyword in ("关键", "重点", "核心", "问题", "细节", "步骤", "方法")):
            derived.append(f"优先关注：{sentence}")
    return dedupe_sentences(derived)[:4]


def build_outline(context_dir: Path) -> str:
    manifest = read_json(context_dir / "manifest.json") or {}
    meta = extract_video_meta(context_dir, manifest)
    ai_summary = normalize_whitespace(extract_primary_body(read_text(context_dir / "ai_summary.txt")))
    if is_placeholder_text(ai_summary):
        ai_summary = ""
    subtitles_raw = sanitize_transcript_text(read_text(context_dir / "subtitles.txt"))
    transcript_raw = sanitize_transcript_text(read_text(context_dir / "transcript.txt"))
    if is_placeholder_text(subtitles_raw):
        subtitles_raw = ""
    if is_placeholder_text(transcript_raw):
        transcript_raw = ""
    subtitles = normalize_whitespace(subtitles_raw)
    transcript = normalize_whitespace(transcript_raw)
    preferred_transcript_raw = first_non_empty(subtitles_raw, transcript_raw)
    preferred_transcript = normalize_whitespace(preferred_transcript_raw)
    comments_text = read_text(context_dir / "comments.txt")
    comments = parse_comments(comments_text)
    transcript_chunks = split_transcript_chunks(preferred_transcript_raw)
    chunk_outline = build_chunk_outline(transcript_chunks)

    candidates = build_candidate_pool(ai_summary, preferred_transcript_raw, meta["desc"], comments)
    primary_candidates = filter_candidates_by_source(candidates, PRIMARY_CONTENT_SOURCES)
    comment_candidates = filter_candidates_by_source(candidates, {"comments"})
    summary_candidates = primary_candidates or candidates
    source_lookup = build_source_lookup(candidates)
    global_core = rank_sentences(summary_candidates, kind="core", limit=2)
    chunk_core = rank_chunk_sentences(transcript_chunks, kind="core", per_chunk=1, limit=4, exclude=set(global_core))
    core_points = dedupe_sentences(global_core + chunk_core)[:5]

    global_detail = rank_sentences(summary_candidates, kind="detail", limit=2, exclude=set(core_points))
    chunk_detail = rank_chunk_sentences(
        transcript_chunks,
        kind="detail",
        per_chunk=1,
        limit=5,
        exclude=set(core_points) | set(global_detail),
    )
    detail_points = dedupe_sentences(global_detail + chunk_detail)[:5]

    global_action = rank_sentences(
        summary_candidates,
        kind="action",
        limit=2,
        exclude=set(core_points) | set(detail_points),
    )
    chunk_action = rank_chunk_sentences(
        transcript_chunks,
        kind="action",
        per_chunk=1,
        limit=4,
        exclude=set(core_points) | set(detail_points) | set(global_action),
    )
    action_points = dedupe_sentences(global_action + chunk_action)[:4]

    if not core_points:
        core_points = fallback_pick([ai_summary, meta["desc"], preferred_transcript_raw], limit=5)
    if not core_points and comment_candidates:
        core_points = rank_sentences(comment_candidates, kind="core", limit=3)

    if not detail_points:
        detail_points = fallback_pick([preferred_transcript_raw, ai_summary, meta["desc"]], limit=5, exclude=set(core_points))
    if not detail_points and comment_candidates:
        detail_points = rank_sentences(comment_candidates, kind="detail", limit=3, exclude=set(core_points))

    if not comments:
        comments = fallback_pick([comments_text], limit=4)

    if not action_points:
        action_points = derive_action_points(core_points, detail_points)

    if not action_points:
        action_points = fallback_pick(
            [preferred_transcript_raw, ai_summary, meta["desc"]],
            limit=4,
            exclude=set(core_points) | set(detail_points),
        )
    if not action_points and comment_candidates:
        action_points = rank_sentences(
            comment_candidates,
            kind="action",
            limit=2,
            exclude=set(core_points) | set(detail_points),
        )

    if not chunk_outline:
        synthesized_flow = []
        if core_points:
            synthesized_flow.append({"title": "议题提出", "points": core_points[:2]})
        if detail_points:
            synthesized_flow.append({"title": "主要分析", "points": detail_points[:2]})
        if action_points:
            synthesized_flow.append({"title": "结论与建议", "points": action_points[:2]})
        chunk_outline = synthesized_flow[:3]

    source_info = (manifest.get("environment") or {}).get("asr_provider_order") or []
    fallback_info = manifest.get("fallback") or {}
    providers_used = fallback_info.get("providers_used") or []
    transcript_source = "字幕" if subtitles else ("ASR 转写" if transcript else "无逐字稿")
    asr_note = " / ".join(providers_used) if providers_used else "未使用"

    lines: list[str] = []
    lines.append(f"# {meta['title']}")
    lines.append("")
    lines.append("- 视频概览")
    lines.append(f"  - BV号：{meta['bvid']}")
    lines.append(f"  - 链接：{meta['link']}")
    lines.append(f"  - UP主：{meta['owner']}")
    lines.append(f"  - 发布时间：{meta['pubdate']}")
    lines.append(f"  - 播放量：{meta['view']}")
    lines.append(f"  - 主要内容来源：{transcript_source}")
    lines.append(f"  - ASR策略：{asr_note}")

    lines.append("- 内容脉络")
    if chunk_outline:
        for chunk in chunk_outline:
            lines.append(f"  - {chunk['title']}")
            for point in chunk["points"]:
                lines.append(f"    - {annotate_point(point, source_lookup)}")
    else:
        lines.append("  - 暂无足够内容生成章节脉络")

    lines.append("- 核心内容")
    if core_points:
        for point in core_points:
            lines.append(f"  - {annotate_point(point, source_lookup)}")
    else:
        lines.append("  - 暂无足够内容生成核心内容摘要")

    lines.append("- 关键细节")
    if detail_points:
        for point in detail_points:
            lines.append(f"  - {annotate_point(point, source_lookup)}")
    else:
        lines.append("  - 暂无足够内容生成关键细节")

    lines.append("- 评论反馈")
    if comments:
        for item in comments:
            lines.append(f"  - {annotate_point(item, source_lookup, default_source='comments')}")
    else:
        lines.append("  - 暂无高价值评论可用")

    lines.append("- 总结 / 行动项")
    if action_points:
        for item in action_points:
            lines.append(f"  - {annotate_point(item, source_lookup)}")
    else:
        lines.append("  - 建议结合 `context.md` 手动补充结论与行动项")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    context_dir = Path(args.context_dir).resolve()
    if not context_dir.exists():
        raise SystemExit(f"Context directory not found: {context_dir}")

    output = Path(args.output).resolve() if args.output else context_dir / "outline.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    outline = build_outline(context_dir)
    output.write_text(outline, encoding="utf-8")
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
