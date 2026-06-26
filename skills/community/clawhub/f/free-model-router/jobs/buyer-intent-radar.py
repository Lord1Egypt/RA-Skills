#!/usr/bin/env python3
"""Job 1: Buyer Intent Radar — find buying signals on X, score leads, draft replies."""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from helpers import call_free_model, notify, parse_json_response, save_output

RADAR_DIR = Path.home() / "rick-vault" / "brain" / "free-jobs" / "radar"
SEEN_IDS_PATH = RADAR_DIR / "seen_ids.json"

SEARCHES = [
    ("AI CEO", 20),
    ("automate my business", 20),
    ("replace myself AI", 20),
    ("AI founder tools", 20),
]

SCORE_PROMPT = """Score this tweet for buying intent for an AI CEO product ($9-$499/mo, helps founders automate their business with AI):
Tweet: {text}
Author: {username} ({followers} followers)

Return JSON: {{"score": 0-10, "reason": "...", "offer_tier": "$9|$39|$97|$499", "draft_reply": "...", "draft_dm": "..."}}
Score 8+ = hot lead. Keep replies under 200 chars, no em dashes, conversational."""


def load_seen_ids():
    if SEEN_IDS_PATH.exists():
        with open(SEEN_IDS_PATH) as f:
            return set(json.load(f))
    return set()


def save_seen_ids(ids):
    RADAR_DIR.mkdir(parents=True, exist_ok=True)
    with open(SEEN_IDS_PATH, "w") as f:
        json.dump(list(ids), f)


def run_xpost(args):
    """Run xpost command and parse JSON output."""
    try:
        result = subprocess.run(
            ["xpost"] + args,
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"[radar] xpost error: {result.stderr.strip()}")
            return []
        try:
            data = json.loads(result.stdout)
            # Handle both direct array and {tweets: [...]} format
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "tweets" in data:
                return data["tweets"]
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            return [data] if data else []
        except json.JSONDecodeError:
            print(f"[radar] Failed to parse xpost output: {result.stdout[:200]}")
            return []
    except FileNotFoundError:
        print("[radar] xpost not found in PATH")
        return []
    except subprocess.TimeoutExpired:
        print("[radar] xpost timed out")
        return []


def fetch_tweets():
    """Fetch tweets from all search queries and mentions."""
    all_tweets = []

    for query, count in SEARCHES:
        print(f"[radar] Searching: {query}")
        # Try --count first, fall back to -n, then no flag
        tweets = run_xpost(["search", query, "--count", str(count)])
        if not tweets:
            tweets = run_xpost(["search", query, "-n", str(count)])
        if not tweets:
            tweets = run_xpost(["search", query])
        all_tweets.extend(tweets)

    # Check mentions
    print("[radar] Checking @MeetRickAI mentions")
    mentions = run_xpost(["mentions", "--count", "30"])
    if not mentions:
        mentions = run_xpost(["mentions", "-n", "30"])
    if not mentions:
        mentions = run_xpost(["mentions"])
    all_tweets.extend(mentions)

    return all_tweets


def extract_tweet_id(tweet):
    """Get tweet ID from various possible field names."""
    for key in ("id", "tweet_id", "id_str"):
        if key in tweet:
            return str(tweet[key])
    return None


def extract_tweet_fields(tweet):
    """Normalize tweet fields."""
    text = tweet.get("text") or tweet.get("full_text") or tweet.get("content", "")
    username = (tweet.get("author", {}).get("username")
                or tweet.get("username")
                or tweet.get("author_id", "unknown"))
    metrics = tweet.get("public_metrics") or tweet.get("author", {}).get("public_metrics", {})
    followers = metrics.get("followers_count", 0)
    return text, username, followers


def main():
    print(f"[radar] Starting buyer intent radar — {datetime.now().isoformat()}")

    seen_ids = load_seen_ids()
    print(f"[radar] {len(seen_ids)} previously seen IDs")

    tweets = fetch_tweets()
    print(f"[radar] Fetched {len(tweets)} total tweets")

    # Deduplicate
    new_tweets = []
    for tweet in tweets:
        tid = extract_tweet_id(tweet)
        if tid and tid not in seen_ids:
            new_tweets.append(tweet)
            seen_ids.add(tid)

    print(f"[radar] {len(new_tweets)} new tweets to score")

    if not new_tweets:
        print("[radar] No new tweets found. Done.")
        save_seen_ids(seen_ids)
        return

    leads = []
    for i, tweet in enumerate(new_tweets):
        text, username, followers = extract_tweet_fields(tweet)
        if not text:
            continue

        print(f"[radar] Scoring {i+1}/{len(new_tweets)}: @{username}")
        prompt = SCORE_PROMPT.format(text=text, username=username, followers=followers)
        response = call_free_model(prompt)
        result = parse_json_response(response)

        if not result:
            continue

        score = result.get("score", 0)
        if score >= 7:
            result["tweet_id"] = extract_tweet_id(tweet)
            result["tweet_text"] = text
            result["username"] = username
            result["followers"] = followers
            leads.append(result)
            print(f"[radar]   -> Score {score} (hot!)" if score >= 8 else f"[radar]   -> Score {score}")

    # Save results
    save_seen_ids(seen_ids)

    if leads:
        date_str = datetime.now().strftime("%Y-%m-%d")
        leads_path = RADAR_DIR / f"leads-{date_str}.json"
        RADAR_DIR.mkdir(parents=True, exist_ok=True)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2)
        print(f"[radar] Saved {len(leads)} leads to {leads_path}")

        save_output("radar", {
            "run_time": datetime.now().isoformat(),
            "tweets_fetched": len(tweets),
            "new_tweets": len(new_tweets),
            "leads_found": len(leads),
            "leads": leads,
        })

        hot_leads = [l for l in leads if l.get("score", 0) >= 8]
        if hot_leads:
            summary = f"🔥 {len(hot_leads)} hot leads found! "
            for lead in hot_leads[:3]:
                summary += f"@{lead.get('username')} (score {lead.get('score')}), "
            notify(summary.rstrip(", "))
    else:
        print("[radar] No leads scored 7+")
        save_output("radar", {
            "run_time": datetime.now().isoformat(),
            "tweets_fetched": len(tweets),
            "new_tweets": len(new_tweets),
            "leads_found": 0,
        })

    print("[radar] Done.")


if __name__ == "__main__":
    main()
