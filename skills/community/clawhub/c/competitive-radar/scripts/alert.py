#!/usr/bin/env python3
"""
alert.py — Daily critical-change detector for competitor-radar.

Runs a fast, lightweight check (curl only, no Playwright) on pricing pages
and homepages. Fires an immediate notification if:
  - A configured alert_keyword is found on the page
  - Content changed by more than 15% since last snapshot
  - Pricing-specific patterns detected ($ amounts changed)

This runs daily at 8am (cron: 0 8 * * *). The full weekly digest still
runs on Mondays — this is only for same-day critical alerts.

Usage:
  python3 alert.py <slug>
  python3 alert.py --all
"""

from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
ALERTS_DIR = DATA_DIR / "alerts"
COMPETITORS_FILE = DATA_DIR / "competitors.json"
SCRIPTS_DIR = SKILL_DIR / "scripts"

TODAY = date.today().isoformat()
NOW = datetime.now(timezone.utc).isoformat()

# Default keywords that always trigger an alert regardless of user config
DEFAULT_ALERT_KEYWORDS = [
    "new pricing", "price increase", "updated pricing", "pricing update",
    "we're raising", "we are raising",
    "acqui", "acquired by", "acquisition",
    "raises $", "series a", "series b", "series c", "raised $",
    "shutdown", "shutting down", "end of life", "eol",
    "no longer available", "sunsetting",
    "enterprise plan", "new enterprise",
    "free plan removed", "discontinuing free",
]

# Threshold: % of word change that triggers a content-changed alert
CONTENT_CHANGE_THRESHOLD = 15.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_competitors() -> dict:
    if not COMPETITORS_FILE.exists():
        return {"competitors": []}
    return json.loads(COMPETITORS_FILE.read_text())


def get_competitor(slug: str) -> dict | None:
    data = load_competitors()
    return next((c for c in data["competitors"] if c["slug"] == slug), None)


def curl_fetch(url: str, timeout: int = 10) -> str | None:
    try:
        result = subprocess.run(
            [
                "curl", "-sL", "--max-time", str(timeout),
                "--user-agent", "Mozilla/5.0",
                "--compressed", url,
            ],
            capture_output=True, text=True, timeout=timeout + 5
        )
        return result.stdout if result.returncode == 0 and result.stdout.strip() else None
    except Exception:
        return None


def strip_html(html: str) -> str:
    text = re.sub(
        r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", "",
        html, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def word_change_pct(old: str, new: str) -> float:
    old_words = set(old.lower().split())
    new_words = set(new.lower().split())
    if not old_words:
        return 100.0
    diff = len(old_words.symmetric_difference(new_words))
    return round(diff / max(len(old_words), len(new_words)) * 100, 1)


def latest_snapshot_text(slug: str, page_type: str) -> str | None:
    d = SNAPSHOTS_DIR / slug
    if not d.exists():
        return None
    files = sorted(d.glob(f"{page_type}_*.txt"), reverse=True)
    if not files:
        return None
    return files[0].read_text(encoding="utf-8")


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def log_alert(slug: str, alert: dict):
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = ALERTS_DIR / f"{TODAY}-alerts.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(alert, default=str) + "\n")


# ---------------------------------------------------------------------------
# Keyword + change detection
# ---------------------------------------------------------------------------

def check_page_for_alerts(
    slug: str,
    page_type: str,
    url: str,
    alert_keywords: list[str],
) -> dict | None:
    """
    Fetch the page, compare to last snapshot, check for alert conditions.
    Returns an alert dict if triggered, else None.
    """
    html = curl_fetch(url)
    if not html:
        return {
            "triggered": False,
            "warning": f"Could not fetch {page_type} page for {slug}",
        }

    text = strip_html(html)
    prev_text = latest_snapshot_text(slug, page_type) or ""
    pct_changed = word_change_pct(prev_text, text) if prev_text else 0.0

    # Check for keyword matches
    all_keywords = list(set(DEFAULT_ALERT_KEYWORDS + alert_keywords))
    matched_keywords = [kw for kw in all_keywords if kw in text]

    # Check for pricing pattern changes (fast heuristic)
    price_pattern = re.compile(r"\$\s?(\d[\d,]*)", re.IGNORECASE)
    old_prices = set(price_pattern.findall(prev_text)) if prev_text else set()
    new_prices = set(price_pattern.findall(text))
    price_changes = bool(old_prices and old_prices != new_prices)

    # Determine if alert should fire
    triggered = bool(
        matched_keywords or
        price_changes or
        (prev_text and pct_changed > CONTENT_CHANGE_THRESHOLD)
    )

    if not triggered:
        return None

    reasons = []
    if matched_keywords:
        reasons.append(f"Keywords detected: {', '.join(matched_keywords[:5])}")
    if price_changes:
        added = new_prices - old_prices
        removed = old_prices - new_prices
        if added:
            reasons.append(f"New prices: ${', $'.join(list(added)[:3])}")
        if removed:
            reasons.append(f"Removed prices: ${', $'.join(list(removed)[:3])}")
    if pct_changed > CONTENT_CHANGE_THRESHOLD:
        reasons.append(f"Content changed {pct_changed}%")

    return {
        "triggered": True,
        "slug": slug,
        "page_type": page_type,
        "url": url,
        "reasons": reasons,
        "pct_changed": pct_changed,
        "matched_keywords": matched_keywords,
        "price_changes": price_changes,
        "checked_at": NOW,
    }


# ---------------------------------------------------------------------------
# Alert message formatter
# ---------------------------------------------------------------------------

def format_alert_message(competitor_name: str, alerts: list[dict]) -> str:
    lines = [
        f"🚨 Competitor Alert — {competitor_name} ({TODAY})",
        "",
    ]
    for alert in alerts:
        lines.append(f"📍 {alert['page_type'].replace('_', ' ').title()} page changed")
        for reason in alert.get("reasons", []):
            lines.append(f"  → {reason}")
        lines.append(f"  View: {alert['url']}")
        lines.append("")

    lines.append("Full analysis will appear in Monday's weekly digest.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_alert_for_competitor(slug: str) -> dict:
    competitor = get_competitor(slug)
    if not competitor:
        return {"error": f"Competitor '{slug}' not found", "slug": slug}

    name = competitor["name"]
    urls = competitor.get("urls", {})
    keywords = competitor.get("alert_keywords", [])
    channels = competitor.get("notify_channels", [])

    triggered_alerts: list[dict] = []

    # Check pricing page
    if urls.get("pricing"):
        result = check_page_for_alerts(slug, "pricing", urls["pricing"], keywords)
        if result and result.get("triggered"):
            triggered_alerts.append(result)

    # Check homepage hero
    if urls.get("homepage"):
        result = check_page_for_alerts(slug, "homepage_hero", urls["homepage"], keywords)
        if result and result.get("triggered"):
            triggered_alerts.append(result)

    if not triggered_alerts:
        print(f"[alert] {name}: no critical changes detected")
        return {"slug": slug, "name": name, "triggered": False}

    # Format and send alert
    message = format_alert_message(name, triggered_alerts)
    print(f"[alert] 🚨 ALERT for {name}: {len(triggered_alerts)} change(s) detected")
    print(message)

    # Log the alert
    alert_record = {
        "slug": slug,
        "name": name,
        "triggered": True,
        "alerts": triggered_alerts,
        "message": message,
        "notified_channels": channels,
        "timestamp": NOW,
    }
    log_alert(slug, alert_record)

    # Deliver via configured channels
    if channels:
        deliver_script = SCRIPTS_DIR / "deliver.py"
        # Write message to a temp file to avoid shell escaping issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md",
                                         delete=False, encoding="utf-8") as f:
            f.write(message)
            temp_path = f.name

        cmd = (
            ["python3", str(deliver_script), temp_path]
            + ["--channels"] + channels
        )
        try:
            subprocess.run(cmd, timeout=30)
        except Exception as e:
            print(f"[alert] Delivery error: {e}", file=sys.stderr)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    return alert_record


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar daily alert checker")
    parser.add_argument("slug", nargs="?", help="Competitor slug")
    parser.add_argument("--all", action="store_true", help="Check all competitors")
    args = parser.parse_args()

    data = load_competitors()
    active = [c for c in data["competitors"] if c.get("active", True)]

    if args.all:
        slugs = [c["slug"] for c in active]
    elif args.slug:
        slugs = [args.slug]
    else:
        parser.print_help()
        sys.exit(1)

    results = [run_alert_for_competitor(s) for s in slugs]
    triggered = [r for r in results if r.get("triggered")]

    print(f"\n[alert] Done. {len(triggered)} of {len(results)} competitor(s) triggered alerts.")
    sys.exit(0)


if __name__ == "__main__":
    main()
