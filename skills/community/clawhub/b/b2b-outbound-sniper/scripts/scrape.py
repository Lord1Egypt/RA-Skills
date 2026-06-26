#!/usr/bin/env python3
"""
B2B Outbound Sniper — Daily Scrape + Verify + Load
Reads config from environment variables. No API keys in source.

Required env vars (or set in config/apis.json):
  APIFY_TOKEN        — from console.apify.com
  HUNTER_API_KEY     — from hunter.io/api-key
  HUNTER_CAMPAIGN_ID — campaign ID from app.hunter.io/campaigns

Full source + production version:
  https://github.com/getlemnos32/b2b-outbound-sniper
"""

import json
import os
import sys
import time
import requests
from datetime import datetime, timezone

# ── Config (env vars take priority over apis.json) ────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "apis.json")

def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    return {
        "apify_token":        os.environ.get("APIFY_TOKEN",        config.get("apify_token", "")),
        "hunter_api_key":     os.environ.get("HUNTER_API_KEY",     config.get("hunter_api_key", "")),
        "hunter_campaign_id": os.environ.get("HUNTER_CAMPAIGN_ID", config.get("hunter_campaign_id", "")),
    }

APIFY_ACTOR   = "borderline~indeed-scraper"
MAX_ITEMS     = 50       # hard cap per keyword run
GAP_SECONDS   = 900      # 15 min between keywords (Apify rate limit)
MIN_CONFIDENCE = 90      # Hunter.io minimum confidence threshold

LOCK_FILE = "/tmp/b2b_sniper_active.lock"

# Domains to always exclude (job boards, not companies)
BLOCKED_DOMAINS = {
    "indeed.com", "linkedin.com", "glassdoor.com",
    "ziprecruiter.com", "monster.com", "careerbuilder.com",
}

# Edit these for your target keywords + geography
KEYWORDS = [
    {"label": "KW-1", "query": "community association manager",   "location": "New Jersey"},
    {"label": "KW-2", "query": "assistant property manager",      "location": "New Jersey"},
    {"label": "KW-3", "query": "property management coordinator", "location": "New Jersey"},
    {"label": "KW-4", "query": "leasing coordinator",            "location": "New Jersey"},
    {"label": "KW-5", "query": "HOA manager",                    "location": "New Jersey"},
]

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "references", "scrape-results.json")
TRACKING_FILE = os.path.join(os.path.dirname(__file__), "..", "references", "hunter-tracking.jsonl")


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE) as f:
            pid = f.read().strip()
        print(f"[LOCK] Another scrape is already running (PID {pid}). Exiting.")
        sys.exit(0)
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


def run_apify(token, query, location):
    """Trigger Apify Indeed scrape and return raw results."""
    url = f"https://api.apify.com/v2/acts/{APIFY_ACTOR}/run-sync-get-dataset-items"
    params = {"token": token, "maxItems": MAX_ITEMS}
    payload = {
        "position": query,
        "location": location,
        "country": "US",
        "maxItems": MAX_ITEMS,
    }
    r = requests.post(url, params=params, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()


def hunter_domain_search(api_key, domain, limit=5):
    """Return emails for a domain at or above MIN_CONFIDENCE."""
    r = requests.get(
        "https://api.hunter.io/v2/domain-search",
        params={"domain": domain, "api_key": api_key, "limit": limit},
        timeout=15,
    )
    data = r.json().get("data", {})
    return [e for e in data.get("emails", []) if e.get("confidence", 0) >= MIN_CONFIDENCE]


def load_existing_campaign_emails(api_key, campaign_id):
    """Fetch all current recipient emails from Hunter campaign (ground-truth dedup)."""
    emails = set()
    offset = 0
    while True:
        r = requests.get(
            f"https://api.hunter.io/v2/campaigns/{campaign_id}/recipients",
            params={"api_key": api_key, "limit": 100, "offset": offset},
            timeout=15,
        )
        data = r.json().get("data", {})
        recipients = data.get("recipients", [])
        if not recipients:
            break
        for rec in recipients:
            emails.add(rec.get("email", "").lower())
        offset += len(recipients)
    return emails


def add_to_campaign(api_key, campaign_id, email, first, last, company, website):
    """Add a single verified lead to Hunter campaign."""
    payload = {
        "emails": [{
            "value": email,
            "first_name": first,
            "last_name": last,
            "company": company,
            "website": website,
        }]
    }
    r = requests.post(
        f"https://api.hunter.io/v2/campaigns/{campaign_id}/recipients",
        params={"api_key": api_key},
        json=payload,
        timeout=15,
    )
    return r.status_code in (200, 201)


def log_add(email, first, last, company, keyword_label):
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "email": email,
        "name": f"{first} {last}",
        "company": company,
        "keyword": keyword_label,
    }
    with open(TRACKING_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    cfg = load_config()
    if not cfg["apify_token"] or not cfg["hunter_api_key"] or not cfg["hunter_campaign_id"]:
        print("ERROR: Missing required config. Set APIFY_TOKEN, HUNTER_API_KEY, HUNTER_CAMPAIGN_ID.")
        print("  Copy config/apis.json.example → config/apis.json and fill in your keys.")
        sys.exit(1)

    acquire_lock()
    try:
        print(f"[{datetime.now().strftime('%H:%M')}] Loading existing campaign recipients...")
        existing_emails = load_existing_campaign_emails(cfg["hunter_api_key"], cfg["hunter_campaign_id"])
        print(f"  {len(existing_emails)} existing recipients loaded (dedup gate active)")

        all_leads = []
        added_total = 0
        seen_this_run = set()

        for i, kw in enumerate(KEYWORDS):
            print(f"\n[{datetime.now().strftime('%H:%M')}] Running {kw['label']}: \"{kw['query']}\" in {kw['location']}")

            try:
                results = run_apify(cfg["apify_token"], kw["query"], kw["location"])
            except Exception as e:
                print(f"  ERROR: Apify run failed — {e}")
                if i < len(KEYWORDS) - 1:
                    print(f"  Waiting {GAP_SECONDS//60} min before next keyword...")
                    time.sleep(GAP_SECONDS)
                continue

            print(f"  {len(results)} raw results returned")
            added_this_kw = 0

            for job in results:
                domain = job.get("domain", "")
                if not domain or domain in BLOCKED_DOMAINS:
                    continue
                if domain in seen_this_run or domain in {e.split("@")[-1] for e in existing_emails}:
                    continue

                emails = hunter_domain_search(cfg["hunter_api_key"], domain)
                if not emails:
                    continue

                best = emails[0]
                email = best["value"].lower()

                if email in existing_emails or email in seen_this_run:
                    continue

                first = best.get("first_name", "")
                last  = best.get("last_name", "")
                company = job.get("company", domain)
                website = f"https://{domain}"

                if add_to_campaign(cfg["hunter_api_key"], cfg["hunter_campaign_id"], email, first, last, company, website):
                    print(f"  ✅ Added: {first} {last} <{email}> — {company}")
                    log_add(email, first, last, company, kw["label"])
                    existing_emails.add(email)
                    seen_this_run.add(email)
                    seen_this_run.add(domain)
                    added_this_kw += 1
                    added_total += 1

                all_leads.append({**job, "keyword": kw["label"]})

            print(f"  {kw['label']} complete — {added_this_kw} new leads added")

            if i < len(KEYWORDS) - 1:
                print(f"  Waiting {GAP_SECONDS//60} min before next keyword...")
                time.sleep(GAP_SECONDS)

        # Save results
        with open(RESULTS_FILE, "w") as f:
            json.dump({"keywords": KEYWORDS, "all_leads": all_leads}, f, indent=2)

        print(f"\n✅ Done — {added_total} total new leads added to campaign {cfg['hunter_campaign_id']}")

    finally:
        release_lock()


if __name__ == "__main__":
    main()
