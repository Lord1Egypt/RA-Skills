import json
import logging
import os
from typing import Dict

from openai import OpenAI


logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "You are a strict classifier. Return only JSON with key 'ai_related' as TRUE or FALSE. "
    "Mark TRUE only when layoffs are clearly caused by AI adoption, automation with AI, "
    "AI replacing workers, or AI efficiency programs."
)


def _heuristic_fallback(event: Dict) -> bool:
    text = " ".join(
        [
            (event.get("title") or ""),
            (event.get("summary") or ""),
            (event.get("reason") or ""),
            (event.get("text") or ""),
        ]
    ).lower()
    ai_signals = [
        "ai",
        "artificial intelligence",
        "automation",
        "replaced workers",
        "efficiency",
        "ai agents",
    ]
    layoff_signals = ["layoff", "job cuts", "cut jobs", "redundancies", "laid off"]
    return any(a in text for a in ai_signals) and any(l in text for l in layoff_signals)


def compute_risk_score(event: Dict) -> int:
    layoffs = event.get("layoffs")
    if layoffs is None:
        layoffs = event.get("layoff_count") or 0
    reason = (event.get("reason") or "").lower()

    score = 0

    if layoffs > 1000:
        score += 40
    elif layoffs > 100:
        score += 20

    if "ai" in reason or "automation" in reason:
        score += 40

    if "efficiency" in reason:
        score += 10

    return min(score, 100)


def is_ai_related_layoff(event: Dict, model: str = "gpt-4o-mini") -> bool:
    """
    Return TRUE only if layoffs are related to AI adoption.
    Falls back to conservative heuristic when LLM call fails.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY missing; using heuristic fallback")
        return _heuristic_fallback(event)

    client = OpenAI(api_key=api_key)
    user_prompt = f"""
Classify this layoff event.

TRUE examples:
- Company cuts 500 workers after deploying AI automation
- Company replaces support team with AI agents

FALSE examples:
- Company cuts jobs due to recession
- Company restructures after merger

Event:
{json.dumps({
    "title": event.get("title"),
    "summary": event.get("summary"),
    "reason": event.get("reason"),
    "text_excerpt": (event.get("text") or "")[:2000]
}, ensure_ascii=True)}

Return JSON only:
{{"ai_related": true}}
or
{{"ai_related": false}}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)
        value = parsed.get("ai_related", False)
        return bool(value)
    except Exception:
        logger.exception("LLM classification failed; using heuristic fallback")
        return _heuristic_fallback(event)
