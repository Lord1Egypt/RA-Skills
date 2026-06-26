import logging
import re
from typing import Dict, List, Optional


logger = logging.getLogger(__name__)

MAX_EVENTS = 10


LAYOFF_HINTS = [
    "layoff",
    "lays off",
    "job cuts",
    "cut jobs",
    "redundancies",
    "workforce reduction",
    "reduce headcount",
    "slash jobs",
]

REASON_HINTS = [
    "automation",
    "ai",
    "artificial intelligence",
    "efficiency",
    "cost reduction",
]

LAYOFF_COUNT_PATTERNS = [
    r"(\d{1,3}(?:,\d{3})+|\d+)\s+(?:employees|workers|staff|jobs|people)",
    r"(?:cut|cuts|lay off|lays off|laid off)\s+(\d{1,3}(?:,\d{3})+|\d+)",
]


def _normalize_text(article: Dict) -> str:
    return " ".join(
        [
            (article.get("title") or "").strip(),
            (article.get("summary") or "").strip(),
            (article.get("text") or "").strip(),
        ]
    ).lower()


def _extract_company_name(article: Dict) -> str:
    title = (article.get("title") or "").strip()
    if not title:
        return "Unknown"

    # Common headline style: "IBM cuts 1000 jobs after AI rollout"
    first_segment = re.split(r"[:\-\|]", title)[0].strip()
    tokens = first_segment.split()
    if not tokens:
        return "Unknown"

    company_tokens = []
    for token in tokens:
        if token.lower() in {"cuts", "lays", "jobs", "to", "after", "amid"}:
            break
        company_tokens.append(token)
    company = " ".join(company_tokens).strip()
    return company or "Unknown"


def _extract_layoff_count(text: str) -> Optional[int]:
    for pattern in LAYOFF_COUNT_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            num = match.group(1).replace(",", "")
            try:
                return int(num)
            except ValueError:
                continue
    return None


def _extract_country(article: Dict) -> str:
    text = _normalize_text(article)
    country_map = {
        "usa": "USA",
        "united states": "USA",
        "uk": "UK",
        "united kingdom": "UK",
        "canada": "Canada",
        "india": "India",
        "china": "China",
        "germany": "Germany",
        "france": "France",
        "japan": "Japan",
        "australia": "Australia",
    }
    for k, v in country_map.items():
        if k in text:
            return v
    return "Unknown"


def _extract_reason(article: Dict) -> str:
    text = _normalize_text(article)
    sentence_candidates = re.split(r"[.!?]\s+", text)
    for sentence in sentence_candidates:
        if "layoff" in sentence or "job cut" in sentence:
            if any(h in sentence for h in REASON_HINTS):
                return sentence.strip().capitalize()
    return "Layoffs mentioned; specific AI-related reason pending classification"


def detect_layoffs(articles: List[Dict]) -> List[Dict]:
    """
    Detect layoff events and extract:
    company_name, date, country, layoff_count, reason, source_url
    """
    events: List[Dict] = []

    for article in articles:
        full_text = _normalize_text(article)
        if not any(hint in full_text for hint in LAYOFF_HINTS):
            continue

        layoff_count = _extract_layoff_count(full_text)
        event = {
            "company_name": _extract_company_name(article),
            "date": article.get("published_at"),
            "country": _extract_country(article),
            "layoff_count": layoff_count,
            "layoffs": layoff_count,
            "reason": _extract_reason(article),
            "source_url": article.get("url"),
            "title": article.get("title"),
            "summary": article.get("summary"),
            "text": article.get("text"),
        }
        events.append(event)

    events = sorted(events, key=lambda x: x["layoffs"] or 0, reverse=True)
    events = events[:MAX_EVENTS]

    logger.info("Detected %d layoff candidate events", len(events))
    return events
