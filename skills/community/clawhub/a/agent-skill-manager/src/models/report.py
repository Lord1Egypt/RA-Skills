"""Typed shapes of the static security-audit report."""

from __future__ import annotations

from typing import TypedDict


class Finding(TypedDict):
    severity: str  # critical | high | medium | low | info
    category: str
    file: str
    line: int | None
    pattern: str
    message: str


class SkillReport(TypedDict):
    skill: str
    path: str
    files: int
    total_bytes: int
    score: int
    grade: str  # A | B | C | D | F
    verdict: str  # safe | caution | risky | dangerous
    summary: dict  # {critical, high, medium, low, info}
    findings: list[Finding]


class StatusEntry(TypedDict):
    skill_name: str
    product_short: str
    product_name: str
    status: str  # ok | missing | manual | n/a
    method: str  # symlink | junction | copy | native | pack
