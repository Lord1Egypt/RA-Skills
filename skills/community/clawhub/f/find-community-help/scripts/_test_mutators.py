#!/usr/bin/env python3
"""Shared mutators for validator and ablation tests."""

from __future__ import annotations

import re


END = "<!-- find-community-help:suggestions:end -->"


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ValueError(f"missing expected text: {old}")
    return text.replace(old, new, 1)


def replace_line(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*.*$", re.MULTILINE)
    updated, count = pattern.subn(f"{key}: {value}", text, count=1)
    if count != 1:
        raise ValueError(f"missing line for {key}")
    return updated


def replace_block(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def replace_match_reasoning_block(text: str, replacement: str) -> str:
    pattern = re.compile(
        r"match_reasoning:\n(?P<body>(?:- .*\n)+)(?=version_scope:)",
        re.MULTILINE,
    )
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError("missing match_reasoning block")
    return updated


def extract_suggestion_block(text: str) -> str:
    start = text.index("## suggestion-1")
    end = text.index(END, start)
    return text[start:end].strip()


def append_suggestions(text: str, total: int) -> str:
    block = extract_suggestion_block(text)
    extras = []
    for index in range(2, total + 1):
        extra = block.replace("## suggestion-1", f"## suggestion-{index}", 1)
        extra = extra.replace(
            "title: Refresh the skill snapshot after edits",
            f"title: Refresh the skill snapshot after edits {index}",
            1,
        )
        extras.append(extra)
    insert_at = text.rindex(END)
    return text[:insert_at] + "\n\n" + "\n\n".join(extras) + "\n" + text[insert_at:]


def ensure_legacy_budget(text: str) -> str:
    if re.search(r"^budget:\s*", text, re.MULTILINE):
        return text
    search_mode_match = re.search(r"^search_mode:\s*(low|medium|high)\s*$", text, re.MULTILINE)
    if not search_mode_match:
        raise ValueError("missing search_mode line for legacy budget compatibility")
    budget_line = f"budget: {search_mode_match.group(1)}\n"
    needle = f"search_mode: {search_mode_match.group(1)}\n"
    return replace_once(text, needle, needle + budget_line)
