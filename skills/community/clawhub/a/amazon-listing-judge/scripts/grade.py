#!/usr/bin/env python3
# /// script
# dependencies = ["httpx"]
# ///
"""
Grade an Amazon product listing on a 0-100 scale.
Usage: grade.py <ASIN>
Requires env vars: CLAW_KEY, CLAW_API_BASE  (set in the skill's .env file)
"""
import os
import sys
import json
import re
from pathlib import Path
import httpx

# Load skill .env (next to this script's parent directory)
_env_path = Path(__file__).parent.parent / '.env'
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if not _line or _line.startswith('#') or '=' not in _line:
                continue
            _k, _, _v = _line.partition('=')
            _k = _k.strip()
            _v = _v.strip().strip('"').strip("'")
            if _k and _k not in os.environ:
                os.environ[_k] = _v

CLAW_KEY = os.environ.get("CLAW_KEY", "")
CLAW_API_BASE = os.environ.get("CLAW_API_BASE", "")


def fetch_pdp(asin: str) -> dict:
    url = f"https://www.amazon.com/dp/{asin}"
    print(f"Fetching {url} ...", file=sys.stderr)
    resp = httpx.post(
        f"{CLAW_API_BASE}/api/scrape",
        json={"claw_key": CLAW_KEY, "url": url, "mode": "scraper"},
        timeout=90,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("error"):
        raise RuntimeError(f"Scrape error: {data['error']}")
    parsed = data.get("parsed")
    if not parsed or not parsed.get("title"):
        raise RuntimeError("No parsed data returned — PDP parse failed")
    return parsed


def _parse_count(s: str) -> int:
    """Parse strings like '4,162 ratings' or '9K+' into an int."""
    if not s:
        return 0
    s = s.replace(",", "").strip()
    m = re.search(r"([\d.]+)\s*([KkMm]?)", s)
    if not m:
        return 0
    num = float(m.group(1))
    suffix = m.group(2).upper()
    if suffix == "K":
        num *= 1_000
    elif suffix == "M":
        num *= 1_000_000
    return int(num)


def grade(parsed: dict) -> dict:
    scores: dict[str, int] = {}
    suggestions: list[str] = []

    # 1. Title (20 pts)
    title = parsed.get("title", "")
    tlen = len(title)
    if 100 <= tlen <= 200:
        scores["title"] = 20
    elif (50 <= tlen < 100) or (200 < tlen <= 250):
        scores["title"] = 12
        scores["title"] = 12
        suggestions.append(
            f"Title is {tlen} chars — optimal range is 100–200 chars"
        )
    else:
        scores["title"] = 5
        suggestions.append(
            f"Title is {tlen} chars — optimal range is 100–200 chars"
        )

    # 2. Bullet points (20 pts)
    bullets = parsed.get("bullet_points") or []
    nb = len(bullets)
    if nb >= 5:
        scores["bullets"] = 20
    elif nb >= 3:
        scores["bullets"] = 14
        suggestions.append(f"Only {nb} bullet points — aim for 5")
    elif nb >= 1:
        scores["bullets"] = 7
        suggestions.append(f"Only {nb} bullet points — aim for 5")
    else:
        scores["bullets"] = 0
        suggestions.append("No bullet points — add 5 benefit-focused bullets")

    # 3. Star rating (20 pts)
    rating_str = parsed.get("rating", "")
    try:
        rating = float(re.search(r"[\d.]+", rating_str).group())
        if rating >= 4.5:
            scores["rating"] = 20
        elif rating >= 4.0:
            scores["rating"] = 14
        elif rating >= 3.5:
            scores["rating"] = 8
            suggestions.append(
                f"Rating {rating} is below 4.0 — improve product quality or listing accuracy"
            )
        else:
            scores["rating"] = 3
            suggestions.append(
                f"Rating {rating} is critical — address root causes in reviews"
            )
    except Exception:
        scores["rating"] = 0
        suggestions.append("Could not parse star rating")

    # 4. Review count (15 pts)
    review_str = parsed.get("review_count", "")
    reviews = _parse_count(review_str)
    if reviews >= 10_000:
        scores["reviews"] = 15
    elif reviews >= 1_000:
        scores["reviews"] = 12
    elif reviews >= 100:
        scores["reviews"] = 7
    else:
        scores["reviews"] = 3
        suggestions.append(
            f"Only {reviews} reviews — run a review campaign to build social proof"
        )

    # 5. Sales velocity (15 pts)
    bought = parsed.get("bought_past_month", "")
    if bought:
        scores["sales_velocity"] = 15
    else:
        scores["sales_velocity"] = 0
        suggestions.append(
            "'Bought in past month' badge missing — drive more sales velocity"
        )

    # 6. BSR (10 pts)
    bsr = parsed.get("bsr") or []
    if bsr:
        scores["bsr"] = 10
    else:
        scores["bsr"] = 0
        suggestions.append("No BSR data — verify product is assigned to correct categories")

    # 7. Badges (10 pts)
    badges_raw = [b.lower() for b in (parsed.get("badges") or [])]
    has_ac = any("choice" in b for b in badges_raw)
    has_bs = any("best seller" in b or "bestseller" in b for b in badges_raw)
    if has_ac and has_bs:
        scores["badges"] = 10
    elif has_ac or has_bs:
        scores["badges"] = 7
    else:
        scores["badges"] = 0
        suggestions.append(
            "No Amazon's Choice or Best Seller badge — improve conversion rate and velocity"
        )

    total = sum(scores.values())

    if total >= 85:
        grade_label = "A (Excellent)"
    elif total >= 70:
        grade_label = "B (Good)"
    elif total >= 55:
        grade_label = "C (Average)"
    elif total >= 40:
        grade_label = "D (Needs Work)"
    else:
        grade_label = "F (Poor)"

    return {
        "asin": parsed.get("asin") or parsed.get("title", "")[:10],
        "title": title[:80] + ("..." if len(title) > 80 else ""),
        "total_score": total,
        "grade": grade_label,
        "breakdown": scores,
        "suggestions": suggestions,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: grade.py <ASIN>", file=sys.stderr)
        sys.exit(1)

    missing = [k for k, v in [('CLAW_KEY', CLAW_KEY), ('CLAW_API_BASE', CLAW_API_BASE)] if not v]
    if missing:
        print(
            f"Missing credentials: {', '.join(missing)}\n"
            "\nThis skill requires a CLAW_KEY from claw-school.com.\n"
            "1. Purchase a key at: https://claw-school.com\n"
            f"2. Add it to the skill's .env file: {_env_path}\n"
            "   CLAW_KEY=CLAW-XXXX-XXXX-XXXX-XXXX\n"
            "   CLAW_API_BASE=<provided-with-your-key>",
            file=sys.stderr,
        )
        sys.exit(1)

    asin = sys.argv[1].upper()
    parsed = fetch_pdp(asin)
    result = grade(parsed)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
