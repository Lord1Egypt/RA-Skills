from __future__ import annotations

import re

EXAMPLE_SECTION_RE = re.compile(
    r"\b(example|examples|sample|samples|anti-pattern|antipattern|quoted)\b",
    re.I,
)
EXAMPLE_LINE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:bad|unsafe|quoted|counter)?\s*(?:example|sample|anti-pattern|antipattern|fixture)\s*[:\-]",
    re.I,
)
CLAUSE_SPLIT_RE = re.compile(
    r"\s*;\s*|\s+\b(?:but|however|whereas|then)\b\s+|(?<=[.!?])\s+(?=[A-Z#*`\-])",
    re.I,
)
NEGATION_PREFIX_RE = re.compile(
    r"(?:^|\b)(?:never|do\s+not|don't|must\s+not|should\s+not|avoid|forbid|forbidden\s+to)\s*$",
    re.I,
)


def instruction_context(line: str, section: str = "") -> str:
    if EXAMPLE_SECTION_RE.search(section) or EXAMPLE_LINE_RE.search(line):
        return "example"
    return "active"


def split_clauses(line: str) -> list[str]:
    clauses = [part.strip() for part in CLAUSE_SPLIT_RE.split(line) if part.strip()]
    return clauses or [line.strip()]


def match_is_negated(text: str, match_start: int) -> bool:
    return bool(NEGATION_PREFIX_RE.search(text[:match_start]))
