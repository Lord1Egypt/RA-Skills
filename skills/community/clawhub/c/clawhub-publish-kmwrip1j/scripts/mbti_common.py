#!/usr/bin/env python3
"""Shared helpers for the mbti skill scripts."""

from __future__ import annotations

import json
import hashlib
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List

DEFAULT_EXCLUDED_PATTERNS = [
    ".env",
    "credentials/*",
    "identity/*",
    "devices/*",
    "exec-approvals.json",
    "openclaw.json",
    "logs/*",
    "gateway*.log",
]

SOURCE_DEFINITIONS = {
    "workspace-long-memory": {
        "label": "Workspace long-term memory",
        "note": "Curated long-term memory from MEMORY.md.",
    },
    "workspace-daily-memory": {
        "label": "Workspace daily memory",
        "note": "Daily memory notes from memory/*.md.",
    },
    "openclaw-sessions": {
        "label": "OpenClaw sessions",
        "note": "Stored session history from ~/.openclaw/agents/*/sessions/*.jsonl.",
    },
    "openclaw-memory-index": {
        "label": "OpenClaw memory index",
        "note": "Indexed chunks from ~/.openclaw/memory/main.sqlite.",
    },
    "openclaw-task-runs": {
        "label": "OpenClaw task runs",
        "note": "Durable task metadata from ~/.openclaw/tasks/runs.sqlite.",
    },
    "openclaw-cron-runs": {
        "label": "OpenClaw cron runs",
        "note": "Cron execution traces from ~/.openclaw/cron/runs/*.jsonl.",
    },
}

AXIS_SIDES = [
    ("E/I", "E", "I"),
    ("S/N", "S", "N"),
    ("T/F", "T", "F"),
    ("J/P", "J", "P"),
]

TYPE_LABELS = {
    "INTJ": "Systems Strategist",
    "INTP": "Model Builder",
    "ENTJ": "Directive Architect",
    "ENTP": "Pattern Explorer",
    "INFJ": "Pattern Guide",
    "INFP": "Inner Idealist",
    "ENFJ": "Social Catalyst",
    "ENFP": "Possibility Spark",
    "ISTJ": "Reliable Operator",
    "ISFJ": "Steady Guardian",
    "ESTJ": "Execution Driver",
    "ESFJ": "Community Steward",
    "ISTP": "Practical Diagnostician",
    "ISFP": "Quiet Craftsman",
    "ESTP": "Adaptive Operator",
    "ESFP": "Expressive Connector",
}

TYPE_FUNCTIONS = {
    "INTJ": ["Ni", "Te", "Fi", "Se"],
    "INTP": ["Ti", "Ne", "Si", "Fe"],
    "ENTJ": ["Te", "Ni", "Se", "Fi"],
    "ENTP": ["Ne", "Ti", "Fe", "Si"],
    "INFJ": ["Ni", "Fe", "Ti", "Se"],
    "INFP": ["Fi", "Ne", "Si", "Te"],
    "ENFJ": ["Fe", "Ni", "Se", "Ti"],
    "ENFP": ["Ne", "Fi", "Te", "Si"],
    "ISTJ": ["Si", "Te", "Fi", "Ne"],
    "ISFJ": ["Si", "Fe", "Ti", "Ne"],
    "ESTJ": ["Te", "Si", "Ne", "Fi"],
    "ESFJ": ["Fe", "Si", "Ne", "Ti"],
    "ISTP": ["Ti", "Se", "Ni", "Fe"],
    "ISFP": ["Fi", "Se", "Ni", "Te"],
    "ESTP": ["Se", "Ti", "Fe", "Ni"],
    "ESFP": ["Se", "Fi", "Te", "Ni"],
}

PSEUDOSIGNAL_PATTERNS = [
    r"请你",
    r"你要",
    r"你应该",
    r"不要拍马屁",
    r"严谨",
    r"用 markdown",
    r"别用 emoji",
    r"输出格式",
    r"tool",
    r"assistant",
    r"agent",
    r"调用",
    r"shell",
    r"命令",
]

NOISE_PATTERNS = [
    r"^\s*```",
    r"^\s*\$ ",
    r"^\s*Traceback",
    r"^\s*Command:",
    r"^\s*\{.+\}\s*$",
]

SELF_REPORT_PATTERNS = [
    r"我通常",
    r"我一般",
    r"我往往",
    r"我习惯",
    r"我更喜欢",
    r"我更倾向",
    r"我宁愿",
    r"我常常",
    r"对我来说更自然",
    r"\bI usually\b",
    r"\bI tend to\b",
    r"\bI prefer\b",
    r"\bI am more likely to\b",
]

HABIT_PATTERNS = [
    r"通常",
    r"一般",
    r"往往",
    r"经常",
    r"常常",
    r"习惯",
    r"每次",
    r"大多数时候",
    r"\busually\b",
    r"\btypically\b",
    r"\bnormally\b",
    r"\bmost of the time\b",
]

DECISION_PATTERNS = [
    r"我决定",
    r"我会选",
    r"最后选",
    r"最终选",
    r"取舍",
    r"权衡",
    r"先.+再",
    r"最终",
    r"最后",
    r"\bI decided\b",
    r"\bI chose\b",
    r"\btrade-?off\b",
]

PRESSURE_PATTERNS = [
    r"截止",
    r"来不及",
    r"赶时间",
    r"赶进度",
    r"上线",
    r"发布",
    r"紧急",
    r"出问题",
    r"交付",
    r"\bdeadline\b",
    r"\bunder pressure\b",
    r"\bship\b",
    r"\blaunch\b",
]

SIGNAL_RULES = [
    {
        "id": "i-think-before-speaking",
        "axis": "E/I",
        "side": "I",
        "strength": "strong",
        "tag": "think-before-speaking",
        "patterns": [r"先自己想", r"先想一会", r"想清楚再", r"让我想一想", r"自己消化", r"think it through first", r"need time to think"],
        "functions": ["Ti", "Fi"],
        "basis": "self-report",
        "reason": "Prefers to process internally before responding outwardly.",
        "report_summary": "The user often prefers to process important issues internally before speaking.",
    },
    {
        "id": "i-inner-reflection",
        "axis": "E/I",
        "side": "I",
        "strength": "moderate",
        "tag": "inner-reflection",
        "patterns": [r"独处", r"独自", r"自己琢磨", r"在脑子里", r"在头脑里", r"安静地想", r"沉浸", r"inside my head", r"on my own", r"quietly think"],
        "functions": ["Ni", "Ti", "Fi"],
        "basis": "behavior",
        "reason": "Shows inner-world reflection and self-contained processing.",
        "report_summary": "The user often works ideas through in a self-contained, reflective way.",
    },
    {
        "id": "e-think-out-loud",
        "axis": "E/I",
        "side": "E",
        "strength": "strong",
        "tag": "think-out-loud",
        "patterns": [r"边聊边", r"一边聊一边", r"讨论一下", r"一起过一遍", r"talk it through", r"think out loud", r"brainstorm"],
        "functions": ["Fe", "Te", "Ne"],
        "basis": "self-report",
        "reason": "Prefers to develop clarity through interaction and live discussion.",
        "report_summary": "The user often sharpens judgment through live discussion and outward engagement.",
    },
    {
        "id": "e-outer-engagement",
        "axis": "E/I",
        "side": "E",
        "strength": "moderate",
        "tag": "outer-engagement",
        "patterns": [r"当面聊", r"现场推进", r"直接拉人", r"先同步一下", r"先去聊", r"go talk", r"work with the room"],
        "functions": ["Te", "Fe", "Se"],
        "basis": "behavior",
        "reason": "Moves toward action and direct engagement in the outer world.",
        "report_summary": "The user often moves outward quickly when progress depends on direct engagement.",
    },
    {
        "id": "n-pattern-language",
        "axis": "S/N",
        "side": "N",
        "strength": "moderate",
        "tag": "abstract-patterning",
        "patterns": [r"框架", r"模型", r"模式", r"本质", r"趋势", r"可能性", r"演化", r"抽象", r"pattern", r"framework", r"possibility"],
        "functions": ["Ni", "Ne"],
        "basis": "behavior",
        "reason": "Frames material through patterns, possibilities, or abstraction.",
        "report_summary": "The user repeatedly frames issues in terms of patterns, possibilities, and abstraction.",
    },
    {
        "id": "n-associative-leap",
        "axis": "S/N",
        "side": "N",
        "strength": "strong",
        "tag": "associative-leap",
        "patterns": [r"联想到", r"顺着这个想到", r"从.+跳到.+", r"从.+想到.+", r"jump from", r"connect distant"],
        "functions": ["Ne"],
        "basis": "behavior",
        "reason": "Makes cross-domain associative jumps rather than staying local.",
        "report_summary": "The user often moves from one domain to another through associative jumps.",
    },
    {
        "id": "s-concrete-detail",
        "axis": "S/N",
        "side": "S",
        "strength": "moderate",
        "tag": "concrete-detail",
        "patterns": [r"具体怎么", r"具体步骤", r"一步一步", r"细节", r"落地", r"现实约束", r"先验证", r"先测", r"可复现", r"specific steps", r"step by step"],
        "functions": ["Si", "Te"],
        "basis": "behavior",
        "reason": "Returns to concrete details, verification, and immediate actualities.",
        "report_summary": "The user repeatedly anchors discussion in concrete detail and immediate execution realities.",
    },
    {
        "id": "s-precedent-anchor",
        "axis": "S/N",
        "side": "S",
        "strength": "moderate",
        "tag": "precedent-anchor",
        "patterns": [r"之前这样", r"上次", r"按经验", r"先看已有", r"现成例子", r"previous case", r"what worked before"],
        "functions": ["Si"],
        "basis": "behavior",
        "reason": "Uses prior experience or precedent as an anchor for perception.",
        "report_summary": "The user often relies on precedent or prior concrete examples before widening the frame.",
    },
    {
        "id": "t-impersonal-analysis",
        "axis": "T/F",
        "side": "T",
        "strength": "strong",
        "tag": "impersonal-analysis",
        "patterns": [r"逻辑", r"一致性", r"证据", r"代价", r"收益", r"权衡", r"因果", r"系统性", r"trade-?off", r"internally consistent"],
        "functions": ["Ti", "Te"],
        "basis": "decision",
        "reason": "Evaluates through impersonal logic, evidence, and tradeoffs.",
        "report_summary": "The user often evaluates options through logic, evidence, and tradeoff analysis.",
    },
    {
        "id": "t-contradiction-check",
        "axis": "T/F",
        "side": "T",
        "strength": "strong",
        "tag": "contradiction-check",
        "patterns": [r"不合理", r"矛盾", r"说不通", r"有漏洞", r"对不上", r"flaw", r"contradiction", r"doesn't add up"],
        "functions": ["Ti"],
        "basis": "decision",
        "reason": "Spots contradiction and weak reasoning directly.",
        "report_summary": "The user often tests ideas by surfacing contradiction or structural weakness directly.",
    },
    {
        "id": "f-value-weighting",
        "axis": "T/F",
        "side": "F",
        "strength": "moderate",
        "tag": "value-weighting",
        "patterns": [r"意义", r"价值", r"初心", r"在乎", r"是否合适", r"对我重要", r"meaning", r"value", r"what matters"],
        "functions": ["Fi", "Fe"],
        "basis": "decision",
        "reason": "Evaluates options through meaning, fit, and value significance.",
        "report_summary": "The user often weights decisions in terms of meaning, fit, and lived value.",
    },
    {
        "id": "f-human-impact",
        "axis": "T/F",
        "side": "F",
        "strength": "moderate",
        "tag": "human-impact",
        "patterns": [r"别人会怎么感受", r"对人影响", r"团队感受", r"关系会不会受伤", r"会不会伤到人", r"how will people feel"],
        "functions": ["Fe"],
        "basis": "decision",
        "reason": "Evaluates through interpersonal impact and felt consequences.",
        "report_summary": "The user often checks how a decision will land on people and relationships.",
    },
    {
        "id": "j-outer-closure",
        "axis": "J/P",
        "side": "J",
        "strength": "strong",
        "tag": "outer-closure",
        "patterns": [r"先定案", r"敲定", r"收口", r"不再扩", r"截止", r"排期", r"行动项", r"最终版", r"timeline", r"deadline"],
        "functions": ["Te", "Si"],
        "basis": "decision",
        "reason": "Prefers closure and organized external dealing with the world.",
        "report_summary": "The user often deals with the outer world by closing options and imposing clear structure.",
    },
    {
        "id": "j-external-order",
        "axis": "J/P",
        "side": "J",
        "strength": "moderate",
        "tag": "external-order",
        "patterns": [r"按计划", r"按顺序", r"有序推进", r"清单", r"排好", r"整理完", r"organized", r"systematic"],
        "functions": ["Te", "Si"],
        "basis": "behavior",
        "reason": "Shows preference for ordered external handling.",
        "report_summary": "The user often wants external work and commitments arranged in a clear order.",
    },
    {
        "id": "p-keep-options-open",
        "axis": "J/P",
        "side": "P",
        "strength": "strong",
        "tag": "keep-options-open",
        "patterns": [r"先别定死", r"保留选项", r"多开几个方向", r"边试边", r"先探索", r"看情况", r"keep options open", r"try a few directions"],
        "functions": ["Ne", "Se"],
        "basis": "decision",
        "reason": "Keeps outer-world options open while learning or adapting.",
        "report_summary": "The user often keeps outer-world options open and narrows only after more evidence arrives.",
    },
    {
        "id": "p-adaptive-pacing",
        "axis": "J/P",
        "side": "P",
        "strength": "moderate",
        "tag": "adaptive-pacing",
        "patterns": [r"走一步看一步", r"适应变化", r"边做边调", r"先理解情况", r"先摸清", r"explore", r"improvise", r"adapt as we go"],
        "functions": ["Ne", "Se"],
        "basis": "behavior",
        "reason": "Adapts in motion rather than structuring prematurely.",
        "report_summary": "The user often adapts in motion and prefers flexibility over premature closure.",
    },
]


def iso_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def stable_id(parts: Iterable[str]) -> str:
    digest = hashlib.sha1("||".join(parts).encode("utf-8")).hexdigest()
    return digest[:16]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return list(iter_jsonl(path))


def iter_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_for_match(text: str) -> str:
    text = clean_text(text).lower()
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
    return text


def shorten(text: str, limit: int = 180) -> str:
    text = clean_text(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "report"


def strength_to_weight(label: str) -> float:
    return {"weak": 1.0, "moderate": 2.0, "strong": 3.0}.get(label, 1.0)


def confidence_to_weight(label: str) -> float:
    return {"low": 0.55, "medium": 0.8, "high": 1.0}.get(label, 0.7)


def confidence_label(score: float) -> str:
    if score >= 0.78:
        return "High confidence"
    if score >= 0.58:
        return "Medium confidence"
    return "Low confidence"


def family_for_type(type_code: str) -> str:
    if len(type_code) != 4:
        return "nt"
    middle = type_code[1:3]
    return {
        "NT": "nt",
        "NF": "nf",
        "ST": "st",
        "SF": "sf",
    }.get(middle, "nt")


def theme_for_type(type_code: str) -> str:
    """Map a type code to the 16Personalities-style visual role theme."""
    if len(type_code) != 4:
        return "analyst"
    if type_code[1:3] == "NT":
        return "analyst"
    if type_code[1:3] == "NF":
        return "diplomat"
    if type_code[1] == "S" and type_code[3] == "J":
        return "sentinel"
    if type_code[1] == "S" and type_code[3] == "P":
        return "explorer"
    return "analyst"


def family_label(type_code: str) -> str:
    return {
        "nt": "Analytical Temperament",
        "nf": "Idealist Temperament",
        "st": "Practical Temperament",
        "sf": "Relational Temperament",
    }[family_for_type(type_code)]


def type_label(type_code: str) -> str:
    return TYPE_LABELS.get(type_code, "Best-Fit Type")


def function_name(process_letter: str, orientation: str) -> str:
    return f"{process_letter.upper()}{orientation.lower()}"


def process_roles(type_code: str) -> Dict[str, str]:
    if len(type_code) != 4:
        raise ValueError(f"Expected 4-letter MBTI code, got {type_code!r}")

    ei, perceiving_letter, judging_letter, jp = type_code
    is_extravert = ei == "E"
    if is_extravert:
        dominant_letter = judging_letter if jp == "J" else perceiving_letter
        auxiliary_letter = perceiving_letter if jp == "J" else judging_letter
        dominant_orientation = "e"
        auxiliary_orientation = "i"
    else:
        dominant_letter = perceiving_letter if jp == "J" else judging_letter
        auxiliary_letter = judging_letter if jp == "J" else perceiving_letter
        dominant_orientation = "i"
        auxiliary_orientation = "e"

    dominant_function = f"{dominant_letter}{dominant_orientation}"
    auxiliary_function = f"{auxiliary_letter}{auxiliary_orientation}"
    outer_function = dominant_function if is_extravert else auxiliary_function
    inner_function = auxiliary_function if is_extravert else dominant_function

    return {
        "dominant_letter": dominant_letter,
        "auxiliary_letter": auxiliary_letter,
        "dominant_function": dominant_function,
        "auxiliary_function": auxiliary_function,
        "outer_function": outer_function,
        "inner_function": inner_function,
        "jp_reflects": "dominant" if is_extravert else "auxiliary",
    }


def visible_function_order(type_code: str) -> List[str]:
    stack = TYPE_FUNCTIONS[type_code]
    if type_code.startswith("E"):
        return stack
    roles = process_roles(type_code)
    visible = [roles["outer_function"], roles["dominant_function"]]
    visible.extend(function_name for function_name in stack if function_name not in visible)
    return visible


def load_sqlite_rows(db_path: Path, query: str) -> List[sqlite3.Row]:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        return list(conn.execute(query))
    finally:
        conn.close()


def detect_language_mix(text: str) -> str:
    has_zh = bool(re.search(r"[\u4e00-\u9fff]", text))
    has_en = bool(re.search(r"[A-Za-z]", text))
    if has_zh and has_en:
        return "mixed"
    if has_zh:
        return "zh"
    if has_en:
        return "en"
    return "unknown"


def is_noise_segment(text: str) -> bool:
    compact = text.strip()
    if not compact:
        return True
    if len(compact) < 8:
        return True
    return any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in NOISE_PATTERNS)


def is_pseudosignal(text: str) -> bool:
    compact = clean_text(text)
    if any(token in compact for token in ["assistant", "agent", "工具", "输出", "格式", "prompt"]):
        return True
    return any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in PSEUDOSIGNAL_PATTERNS)


def segment_context_flags(text: str) -> Dict[str, bool]:
    compact = clean_text(text)
    return {
        "self_report": any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in SELF_REPORT_PATTERNS),
        "habit": any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in HABIT_PATTERNS),
        "decision": any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in DECISION_PATTERNS),
        "pressure": any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in PRESSURE_PATTERNS),
    }


def context_signal_score(flags: Dict[str, bool]) -> float:
    score = 0.0
    if flags["self_report"]:
        score += 0.34
    if flags["habit"]:
        score += 0.22
    if flags["decision"]:
        score += 0.18
    if flags["pressure"]:
        score += 0.12
    return round(min(0.86, score), 3)


def confidence_band(score: float) -> str:
    if score >= 0.74:
        return "high"
    if score >= 0.56:
        return "medium"
    return "low"


def match_signal_rules(text: str) -> List[Dict[str, Any]]:
    matches: List[Dict[str, Any]] = []
    for rule in SIGNAL_RULES:
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in rule["patterns"]):
            matches.append(rule)
    return matches


def summarize_line(text: str) -> str:
    compact = clean_text(text)
    if not compact:
        return "Empty segment"
    if len(compact) <= 110:
        return compact
    pivot = compact[:110].rsplit(" ", 1)[0].rstrip()
    return (pivot or compact[:109]).rstrip() + "…"


def split_into_segments(text: str) -> List[str]:
    if not text.strip():
        return []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    segments: List[str] = []
    bullet_buffer: List[str] = []
    paragraph_buffer: List[str] = []
    for line in lines:
        is_bullet = bool(re.match(r"^[-*•]\s+", line)) or bool(re.match(r"^\d+\.\s+", line))
        if is_bullet:
            if paragraph_buffer:
                segments.append(" ".join(paragraph_buffer))
                paragraph_buffer = []
            bullet_buffer.append(re.sub(r"^[-*•]\s+|^\d+\.\s+", "", line))
        else:
            if bullet_buffer:
                segments.extend(bullet_buffer)
                bullet_buffer = []
            paragraph_buffer.append(line)
    if bullet_buffer:
        segments.extend(bullet_buffer)
    if paragraph_buffer:
        segments.append(" ".join(paragraph_buffer))
    return [segment for segment in (clean_text(part) for part in segments) if segment]


def resolve_path(path_str: str) -> Path:
    return Path(path_str).expanduser().resolve()
