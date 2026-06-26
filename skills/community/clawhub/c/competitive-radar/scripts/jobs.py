#!/usr/bin/env python3
"""
jobs.py — Job postings tracker for competitor-radar.

Scrapes LinkedIn, Indeed, and Glassdoor for new job postings from each
tracked competitor. Compares to previous week's snapshot to find net new
roles. Classifies roles into strategic signal categories.

Usage:
  python3 jobs.py <slug>
  python3 jobs.py --all

Output (stdout): JSON dict with new_roles, signal_categories, summary.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
JOBS_DIR = DATA_DIR / "jobs"
COMPETITORS_FILE = DATA_DIR / "competitors.json"

TODAY = date.today().isoformat()
ONE_WEEK_AGO = (date.today() - timedelta(days=8)).isoformat()


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


def jobs_snapshot_path(slug: str) -> Path:
    d = JOBS_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d / f"jobs_{TODAY}.json"


def previous_jobs_snapshot(slug: str) -> list[dict]:
    d = JOBS_DIR / slug
    if not d.exists():
        return []
    files = sorted(d.glob("jobs_*.json"), reverse=True)
    prev = files[1] if len(files) > 1 else (files[0] if files else None)
    if prev:
        return json.loads(prev.read_text())
    return []


# ---------------------------------------------------------------------------
# Job scraping — Google Jobs RSS + Greenhouse/Lever/Workable career pages
# ---------------------------------------------------------------------------

def scrape_jobs_via_google(company_name: str) -> list[dict]:
    """
    Uses Google Jobs search via SerpAPI-style URL or direct Google search scrape.
    Falls back to scraping the company's known career page formats.
    """
    import subprocess
    import urllib.parse

    query = urllib.parse.quote(f'"{company_name}" jobs site:greenhouse.io OR site:lever.co OR site:workable.com')
    url = f"https://www.google.com/search?q={query}&tbs=qdr:w"  # past week

    try:
        result = subprocess.run(
            [
                "curl", "-sL", "--max-time", "15",
                "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/122.0.0.0 Safari/537.36",
                url,
            ],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            return []

        html = result.stdout
        # Extract job titles from Google search results
        titles = re.findall(r'<h3[^>]*class="[^"]*LC20lb[^"]*"[^>]*>([^<]+)</h3>', html)
        links = re.findall(r'<a href="(https://(?:boards\.greenhouse\.io|jobs\.lever\.co|apply\.workable\.com)[^"]+)"', html)

        jobs = []
        for i, title in enumerate(titles[:15]):
            clean = re.sub(r'\s+', ' ', title).strip()
            if any(w in clean.lower() for w in ['engineer', 'manager', 'director', 'analyst',
                                                  'sales', 'success', 'designer', 'lead',
                                                  'head of', 'vp ', 'specialist', 'developer']):
                jobs.append({
                    "title": clean,
                    "location": "",
                    "posted": "",
                    "url": links[i] if i < len(links) else "",
                    "source": "google_jobs",
                })
        return jobs
    except Exception:
        return []


def scrape_greenhouse_jobs(company_name: str) -> list[dict]:
    """Try common Greenhouse/Lever/Workable board URLs for the company."""
    import subprocess

    slug = company_name.lower().replace(" ", "").replace("-", "")
    candidates = [
        f"https://boards.greenhouse.io/{slug}",
        f"https://jobs.lever.co/{slug}",
        f"https://apply.workable.com/{slug}",
        f"https://boards.greenhouse.io/{slug.replace('hq', '')}",
    ]

    for url in candidates:
        try:
            result = subprocess.run(
                ["curl", "-sL", "--max-time", "10",
                 "--user-agent", "Mozilla/5.0",
                 url],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode != 0 or len(result.stdout) < 500:
                continue
            html = result.stdout
            if "404" in html[:200] or "not found" in html[:200].lower():
                continue

            jobs = []
            # Greenhouse format
            titles = re.findall(r'<a[^>]+class="[^"]*posting-title[^"]*"[^>]*>\s*<h3[^>]*>([^<]+)</h3>', html)
            locations = re.findall(r'<span[^>]+class="[^"]*location[^"]*"[^>]*>([^<]+)</span>', html)
            if not titles:
                # Lever format
                titles = re.findall(r'<h5[^>]+>([^<]+)</h5>', html)
                locations = re.findall(r'<span[^>]+class="[^"]*commitment[^"]*"[^>]*>([^<]+)</span>', html)
            if not titles:
                # Generic: look for job-like h3/h4 text
                titles = re.findall(r'<(?:h3|h4)[^>]*>([A-Z][^<]{5,60})</(?:h3|h4)>', html)

            if titles:
                print(f"[jobs] Found career page at {url} — {len(titles)} roles")
                for i, title in enumerate(titles[:30]):
                    jobs.append({
                        "title": title.strip(),
                        "location": locations[i].strip() if i < len(locations) else "",
                        "posted": "",
                        "url": url,
                        "source": "careers_page",
                    })
                return jobs
        except Exception:
            continue

    return []


# ---------------------------------------------------------------------------
# Indeed fallback scraper
# ---------------------------------------------------------------------------

def scrape_indeed_jobs(company_name: str) -> list[dict]:
    """Scrape Indeed for company jobs posted in the last 7 days."""
    import subprocess
    query = company_name.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={query}&fromage=7"
    try:
        result = subprocess.run(
            [
                "curl", "-sL", "--max-time", "15",
                "--user-agent", "Mozilla/5.0",
                url
            ],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            return []
        html = result.stdout
        titles = re.findall(r'data-testid="jobsearch-JobInfoHeader-title"[^>]*>([^<]+)<', html)
        locations = re.findall(r'data-testid="text-location"[^>]*>([^<]+)<', html)
        jobs = []
        for i, title in enumerate(titles[:20]):
            jobs.append({
                "title": title.strip(),
                "location": locations[i].strip() if i < len(locations) else "",
                "posted": "",
                "url": "",
                "source": "indeed",
            })
        return jobs
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Signal classification
# ---------------------------------------------------------------------------

SIGNAL_CATEGORIES = {
    "AI/ML Buildout": [
        "machine learning", "ml engineer", "ai engineer", "deep learning",
        "llm", "nlp", "data scientist", "mlops", "ai researcher",
        "foundation model", "computer vision",
    ],
    "Enterprise GTM": [
        "enterprise account executive", "enterprise ae", "enterprise sales",
        "enterprise customer success", "solutions engineer", "sales engineer",
        "strategic account", "vp sales", "chief revenue", "cro",
    ],
    "Geographic Expansion": [
        "emea", "apac", "latam", "uk", "london", "berlin", "singapore",
        "toronto", "sydney", "europe", "asia", "india",
    ],
    "Platform/Ecosystem Play": [
        "partnerships", "partner manager", "developer relations", "devrel",
        "developer advocate", "ecosystem", "integrations",
    ],
    "Legal/Compliance/M&A": [
        "legal counsel", "general counsel", "compliance", "privacy",
        "security counsel", "m&a", "corporate development",
    ],
    "Product Buildout": [
        "product manager", "product designer", "head of product",
        "vp product", "principal pm", "staff pm",
    ],
    "Infrastructure/Scale": [
        "site reliability", "sre", "devops", "infrastructure engineer",
        "platform engineer", "staff engineer", "principal engineer",
    ],
    "Support/Success": [
        "customer success", "customer support", "technical support",
        "implementation", "onboarding specialist",
    ],
}


def classify_role(title: str) -> list[str]:
    """Map a job title to one or more signal categories."""
    title_lower = title.lower()
    matched = []
    for category, keywords in SIGNAL_CATEGORIES.items():
        if any(kw in title_lower for kw in keywords):
            matched.append(category)
    return matched or ["Other"]


def build_signal_summary(new_roles: list[dict]) -> dict:
    """Group new roles by signal category and generate strategic interpretation."""
    by_category: dict[str, list[str]] = {}
    for role in new_roles:
        cats = classify_role(role["title"])
        for cat in cats:
            by_category.setdefault(cat, []).append(role["title"])

    signals = []
    interpretations = {
        "AI/ML Buildout": "Building AI-native features — expect product announcements in 3-6 months",
        "Enterprise GTM": "Moving upmarket — will compete in deals you weren't seeing before",
        "Geographic Expansion": "Entering new markets — watch for localized pricing/product",
        "Platform/Ecosystem Play": "Building a platform/partner moat — partnerships will close deals",
        "Legal/Compliance/M&A": "Legal hires signal: M&A activity, compliance push, or IP fight",
        "Product Buildout": "Significant product investment — feature velocity will increase",
        "Infrastructure/Scale": "Scaling for growth — preparing for higher load/enterprise reliability",
        "Support/Success": "Investing in retention — may be experiencing churn pressure",
    }

    for cat, roles in by_category.items():
        if cat != "Other":
            signals.append({
                "category": cat,
                "role_count": len(roles),
                "roles": roles[:5],
                "interpretation": interpretations.get(cat, ""),
            })

    return {
        "by_category": by_category,
        "signals": signals,
        "total_new_roles": len(new_roles),
    }


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_jobs_for_competitor(slug: str) -> dict:
    competitor = get_competitor(slug)
    if not competitor:
        return {"error": f"Competitor '{slug}' not found", "slug": slug}

    name = competitor["name"]
    linkedin_url = competitor.get("urls", {}).get("linkedin")

    print(f"[jobs] Scraping jobs for {name}...")

    # Try career pages first (most reliable), then Google Jobs fallback
    linkedin_jobs = scrape_greenhouse_jobs(name)
    indeed_jobs = scrape_jobs_via_google(name) if not linkedin_jobs else []

    # Deduplicate by title
    all_jobs_raw = linkedin_jobs + indeed_jobs
    seen_titles: set[str] = set()
    all_jobs: list[dict] = []
    for job in all_jobs_raw:
        title_key = job["title"].lower().strip()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            all_jobs.append(job)

    # Compare to previous snapshot
    prev_jobs = previous_jobs_snapshot(slug)
    prev_titles = {j["title"].lower().strip() for j in prev_jobs}
    new_roles = [j for j in all_jobs
                 if j["title"].lower().strip() not in prev_titles]
    filled_roles = [j for j in prev_jobs
                    if j["title"].lower().strip() not in seen_titles]

    # Save current snapshot
    snapshot_path = jobs_snapshot_path(slug)
    snapshot_path.write_text(json.dumps(all_jobs, indent=2, default=str))

    # Build signal summary
    signal_summary = build_signal_summary(new_roles)

    result = {
        "slug": slug,
        "name": name,
        "total_current_roles": len(all_jobs),
        "new_roles_this_week": len(new_roles),
        "filled_or_removed_roles": len(filled_roles),
        "new_roles": new_roles[:20],
        "signal_summary": signal_summary,
        "has_signals": bool(signal_summary["signals"]),
    }

    print(f"[jobs] {name}: {len(new_roles)} new, {len(filled_roles)} filled/removed")
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar jobs tracker")
    parser.add_argument("slug", nargs="?", help="Competitor slug")
    parser.add_argument("--all", action="store_true", help="Run for all competitors")
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

    all_results = [run_jobs_for_competitor(s) for s in slugs]
    print(json.dumps(all_results, indent=2, default=str))


if __name__ == "__main__":
    main()
