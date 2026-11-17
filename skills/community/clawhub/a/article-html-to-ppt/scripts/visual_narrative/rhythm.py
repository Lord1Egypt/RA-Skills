from __future__ import annotations

from typing import Any


def evaluate_deck_rhythm(plan: Any) -> dict[str, Any]:
    slides = _validated_slides(plan)
    if slides is None:
        return {
            "status": "failed",
            "metrics": _empty_metrics(),
            "issues": [
                _issue(
                    "RHYTHM_PLAN_INVALID",
                    "视觉计划必须包含结构合法的 slides 数组。",
                )
            ],
        }

    total = len(slides)
    key_count = sum(slide["priority"] == "key" for slide in slides)
    archetypes = [slide["page_archetype"] for slide in slides]
    card_count = sum(slide["primary_expression"] == "cards" for slide in slides)
    max_run = _max_consecutive(archetypes)
    archetype_count = len(set(archetypes))
    card_ratio = card_count / total if total else 0.0

    issues: list[dict[str, str]] = []
    if 10 <= total <= 14 and not 2 <= key_count <= 3:
        issues.append(
            _issue(
                "RHYTHM_KEY_SLIDE_COUNT",
                "正式 Deck 必须包含 2–3 张关键视觉页。",
            )
        )
    if archetype_count < 4:
        issues.append(
            _issue(
                "RHYTHM_ARCHETYPE_DIVERSITY",
                "整套 Deck 至少需要 4 种主要页面原型。",
            )
        )
    if max_run > 2:
        issues.append(
            _issue(
                "RHYTHM_CONSECUTIVE_ARCHETYPE",
                "同一种页面原型不得连续超过 2 页。",
            )
        )
    if card_ratio > 0.30:
        issues.append(
            _issue(
                "RHYTHM_CARD_RATIO",
                "卡片主导页面占比不得超过 30%。",
            )
        )

    return {
        "status": "failed" if issues else "passed",
        "metrics": {
            "slide_count": total,
            "key_slide_count": key_count,
            "archetype_count": archetype_count,
            "max_consecutive_archetype": max_run,
            "card_ratio": card_ratio,
        },
        "issues": issues,
    }


def _validated_slides(plan: Any) -> list[dict[str, str]] | None:
    if not isinstance(plan, dict):
        return None
    slides = plan.get("slides")
    if not isinstance(slides, list) or not slides:
        return None

    validated: list[dict[str, str]] = []
    for slide in slides:
        if not isinstance(slide, dict):
            return None
        required = {
            "priority": slide.get("priority"),
            "page_archetype": slide.get("page_archetype"),
            "primary_expression": slide.get("primary_expression"),
        }
        if any(not isinstance(value, str) or not value.strip() for value in required.values()):
            return None
        validated.append({key: value.strip() for key, value in required.items()})
    return validated


def _max_consecutive(values: list[str]) -> int:
    longest = 0
    current = 0
    previous: str | None = None
    for value in values:
        if value == previous:
            current += 1
        else:
            previous = value
            current = 1
        longest = max(longest, current)
    return longest


def _empty_metrics() -> dict[str, float | int]:
    return {
        "slide_count": 0,
        "key_slide_count": 0,
        "archetype_count": 0,
        "max_consecutive_archetype": 0,
        "card_ratio": 0.0,
    }


def _issue(code: str, message_zh: str) -> dict[str, str]:
    return {
        "code": code,
        "severity": "error",
        "message_zh": message_zh,
    }
