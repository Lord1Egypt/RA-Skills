"""
core/contradiction.py — Contradiction Detection v1.2.39

当新胶囊入库前，检查其内容是否与已有胶囊存在事实矛盾：
  - 日期/时间冲突（"3年经验" vs 已记录起始年份）
  - 人员/团队冲突（"团队有5人" vs 已记录人数）
  - 技术栈冲突（"用 Postgres" vs 已记录选了 MySQL）
  - 项目状态冲突（"项目已上线" vs 已记录仍在开发）

用法：
    from core.contradiction import detect_contradictions

    warnings = detect_contradictions(memo, valid_from, valid_to)
    # → [{"type": "date_conflict", "message": "..."}, ...]
"""

from __future__ import annotations

import re
from datetime import datetime, date
from typing import Optional

# ── Date patterns ──────────────────────────────────────────────────────────────

_MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}


def _month_to_date(m) -> str:
    mon = _MONTH_MAP.get(m.group(1).lower()[:3], "01")
    return f"{m.group(2)}-{mon}-01"


def _relative_to_date(m) -> str:
    now = datetime.now()
    unit = m.group(1).lower()
    num = int(m.group(1)) if m.group(1).isdigit() else 1
    if unit.startswith("year"):
        return f"{now.year - num}-01-01"
    if unit.startswith("month"):
        month = now.month - num
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
        return f"{year}-{month:02d}-01"
    if unit.startswith("week"):
        from datetime import timedelta
        d = now - timedelta(weeks=num)
        return d.strftime("%Y-%m-%d")
    return f"{now.year}-01-01"


_DATE_PATTERNS = [
    # "2023", "2023年", "in 2023"
    (r"\b(20\d{2})\s*年?\b", lambda m: f"{m.group(1)}-01-01"),
    # "Jan 2023", "January 2023"
    (r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(20\d{2})\b", _month_to_date),
    (r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})\b", _month_to_date),
    # ISO "2023-03-15"
    (r"\b(20\d{2}-\d{2}-\d{2})\b", None),
    # "3 years ago", "2 months ago"
    (r"\b(\d+)\s*(year|month|day|yr|mo)s?\s+ago\b", _relative_to_date),
    # "since 2023", "from 2023"
    (r"\b(?:since|from)\s+(20\d{2})\b", lambda m: f"{m.group(1)}-01-01"),
    # "started in 2023", "joined 2023"
    (r"\b(?:started?|joined?|begun?)\s+(?:in\s+)?(20\d{2})\b", lambda m: f"{m.group(1)}-01-01"),
    # "last month/year/week"
    (r"\blast\s+(month|year|week)\b", _relative_to_date),
    # "this year"
    (r"\bthis\s+year\b", lambda _: f"{datetime.now().year}-01-01"),
]


# ── Entity / value extractors ────────────────────────────────────────────────

# Patterns that extract <entity, attribute, value> triples from text
_ENTITY_VALUE_PATTERNS = [
    # "team has N people", "team of 5", "5 people on team"
    (r"(?:team|group)\s+(?:of\s+)?(?:\w+\s+)?(\d+)\s*(?:people|person|members?)?", "team_size", int),
    (r"(\d+)\s+(?:people|person|members?)\s+(?:on|in|with\s+)?(?:the\s+)?(?:team|group)", "team_size", int),
    # "using X", "use X", "with X", "chose X", "decided on X"
    (r"(?:using|use|chose|decided\s+on|went\s+with|pick(ed)?)\s+([A-Za-z][A-Za-z0-9_-]+)", "tech_stack", str),
    # "database is X", "DB is X"
    (r"(?:database|DB|db)\s+(?:is\s+)?([A-Za-z][A-Za-z0-9_-]+)", "db_type", str),
    # "Python/JS/Go developer" — standalone tech mentions
    (r"\b(Python|JavaScript|TypeScript|Go|Rust|Java|React|Vue|Node|Llama|Claude|GPT|Postgres|PostgreSQL|MySQL|MongoDB|Redis|Kubernetes|Docker|AWS|GCP|Azure|Flask|FastAPI|Django|Spring|Angular|Svelte)\b", "tech_stack", str),
    # "X years of experience", "X year experience"
    (r"(\d+)\s+(?:year|yr)s?\s+(?:of\s+)?experience", "years_exp", int),
    # "started in year X", "working since X"
    (r"(?:started|working)\s+(?:in\s+)?(?:the\s+)?year\s+(20\d{2})", "start_year", int),
    (r"working\s+(?:since|from)\s+(20\d{2})", "start_year", int),
    # "completed", "done", "finished" → project status
    (r"\b(?:complet|finish|done|launch|shipped|deployed)\b", "project_status", "completed"),
    # "in progress", "ongoing", "still building" → project status
    (r"\b(?:in\s+progress|ongoing|still\s+\w+|building|developing)\b", "project_status", "in_progress"),
    # "budget is $X"
    (r"budget\s+(?:of\s+)?\$?([\d,]+)", "budget", int),
]

# ── Conflict detection rules ──────────────────────────────────────────────────

_CONFLICT_RULES = [
    # (check_fn, warning_template)
    ("team_size", "team_size_conflict", "团队规模冲突：已有记录 {existing} 人，新输入 {new} 人"),
    ("years_exp", "tenure_conflict", "工龄冲突：已有记录 {existing} 年经验，新输入 {new} 年"),
    ("start_year", "start_year_conflict", "入职年份冲突：已有记录 {existing}，新输入 {new}"),
    ("db_type", "tech_conflict", "数据库冲突：已有记录用 {existing}，新输入用 {new}"),
    ("project_status", "status_conflict", "项目状态冲突：已有记录为 {existing}，新输入为 {new}"),
]


# ── Core API ─────────────────────────────────────────────────────────────────

def parse_dates(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    从文本中解析时间范围，返回 (valid_from, valid_to)。
    能解析"since 2023" → (2023-01-01, None)
    能解析"2023 to 2024" → (2023-01-01, 2024-12-31)
    能解析"X years ago" → (derived-ago-date, None)
    """
    valid_from, valid_to = None, None

    # Try "YYYY to YYYY" range
    range_m = re.search(r"(20\d{2})\s*(?:to|-|–)\s*(20\d{2})", text)
    if range_m:
        valid_from = f"{range_m.group(1)}-01-01"
        valid_to = f"{range_m.group(2)}-12-31"
        return valid_from, valid_to

    # Try single date patterns in order
    for pattern, converter in _DATE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            if converter:
                try:
                    valid_from = converter(m)
                except Exception:
                    valid_from = m.group(0) if m.lastindex else m.group(0)
            else:
                valid_from = m.group(1) if m.lastindex else m.group(0)
            break

    # Check for "until YYYY" / "through YYYY"
    until_m = re.search(r"(?:until|through|up to)\s+(20\d{2})", text, re.IGNORECASE)
    if until_m:
        valid_to = f"{until_m.group(1)}-12-31"

    return valid_from, valid_to


def extract_entity_values(text: str) -> dict[str, str | int]:
    """
    从文本中提取实体属性值。
    返回 {"team_size": 5, "tech_stack": "Postgres", ...}
    """
    results = {}
    text_lower = text.lower()

    for pattern, attr, extractor in _ENTITY_VALUE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            val = m.group(1) if m.lastindex else (m.group(0) if not m.lastindex else None)
            if val is None:
                continue
            try:
                if extractor is int:
                    val = int(re.sub(r"[^\d]", "", str(val)))
                elif extractor is str:
                    val = str(val).strip()
            except (ValueError, AttributeError):
                continue

            # Deduplicate — first match wins
            if attr not in results:
                results[attr] = val

    return results


def detect_contradictions(
    memo: str,
    valid_from: Optional[str] = None,
    valid_to: Optional[str] = None,
    category_path: str = "general/default",
) -> list[dict]:
    """
    检查新记忆是否与已有胶囊矛盾。
    返回警告列表：[{type, message, conflicting_capsule_id}, ...]
    如果返回空列表 = 无矛盾。
    """
    import sqlite3
    from pathlib import Path

    warnings = []
    extracted = extract_entity_values(memo)
    if not extracted:
        return []  # Nothing concrete to check

    # Auto-parse dates if not provided
    if valid_from is None or valid_to is None:
        parsed_from, parsed_to = parse_dates(memo)
        valid_from = valid_from or parsed_from
        valid_to = valid_to or parsed_to

    try:
        db_path = Path.home() / ".amber-hunter" / "hunter.db"
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
    except Exception:
        return []  # DB not ready — skip contradiction check

    # 只取同 category_path 的胶囊（最多20条）做对比
    rows = c.execute(
        "SELECT id, memo FROM capsules WHERE category_path=? LIMIT 20",
        (category_path,)
    ).fetchall()

    for (cid, existing_memo) in rows:
        existing_vals = extract_entity_values(existing_memo)
        for attr, new_val in extracted.items():
            if attr not in existing_vals:
                continue

            existing_val = existing_vals[attr]

            # Same value = no conflict
            if existing_val == new_val:
                continue

            # Type-specific conflict logic
            conflict = False
            if attr == "team_size":
                diff = abs(int(existing_val) - int(new_val))
                conflict = diff >= 2  # 2+ people difference = conflict
            elif attr == "years_exp":
                diff = abs(int(existing_val) - int(new_val))
                conflict = diff >= 1  # 1+ year difference = conflict
            elif attr == "start_year":
                conflict = True  # Any different start year = conflict
            elif attr == "db_type":
                # Only conflict if both mention specific DBs (not just generic)
                if len(str(existing_val)) >= 4 and len(str(new_val)) >= 4:
                    conflict = existing_val.lower() != new_val.lower()
            elif attr == "project_status":
                conflict = existing_val != new_val

            if conflict:
                warnings.append({
                    "type": f"{attr}_conflict",
                    "message": f"🔴 {attr} 矛盾：已有记录为 {existing_val}，新输入为 {new_val}。现有胶囊: {cid[:8]}",
                    "conflicting_capsule_id": cid,
                    "existing_value": existing_val,
                    "new_value": new_val,
                })

    conn.close()
    return warnings


def check_contradiction_on_ingest(
    memo: str,
    category_path: str = "general/default",
) -> tuple[Optional[str], Optional[str], list[dict]]:
    """
    ingest_memory 前调用此函数，解析时间并检查矛盾。
    返回 (valid_from, valid_to, warnings)。

    用法：
        valid_from, valid_to, warnings = check_contradiction_on_ingest(memo, category_path)
        if warnings:
            # 可以选择：返回给用户确认，或记录警告但不阻止写入
    """
    valid_from, valid_to = parse_dates(memo)
    warnings = detect_contradictions(memo, valid_from, valid_to, category_path)
    return valid_from, valid_to, warnings
