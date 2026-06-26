#!/usr/bin/env python3
"""
Edison Autopilot Post X — Auto-generate and post tweets using OpenAI + X API.

Setup:
  1. pip install tweepy requests
  2. Set environment variables (see Config section below)
  3. python auto_tweet.py          # post a tweet
  4. python auto_tweet.py --dry-run # preview without posting

Cron example (5x daily at 8am, 11am, 2pm, 5pm, 9pm PST):
  0 8,11,14,17,21 * * * cd /path/to/repo && python auto_tweet.py
"""

import json
import os
import random
import sys
from datetime import datetime, timezone

import requests
import tweepy

# --- Config (set these as environment variables) ---
OPENAI_KEY = os.environ["OPENAI_API_KEY"]
X_CONSUMER_KEY = os.environ["X_CONSUMER_KEY"]
X_CONSUMER_SECRET = os.environ["X_CONSUMER_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

# Optional: Telegram notifications
TG_BOT_TOKEN = os.environ.get("TWEET_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TWEET_BOT_CHAT_ID", "")

# Where to log posted tweets (for dedup)
LOG_DIR = os.path.expanduser("~/autopilot-post-x/logs")

# Optional: research scan directory for context-aware tweets
SCAN_DIR = os.environ.get("SCAN_DIR", "")

# --- Persona Prompt ---
# Customize this to match YOUR voice, topics, and style.
PERSONA = """You are [YOUR NAME] (@your_handle), [your role/title].

Your voice:
- [Describe your communication style]
- [Reference people whose tweet style you admire]

Your personality:
- [Key traits]
- [Topics you care about]
- Casual — lowercase, occasional emoji, but never overdone
- Always in English

TAGGING RULES (always use @ when mentioning these):
- [Your Company] → @yourcompany
- [Partner/Portfolio] → @theirhandle
- Only tag accounts when naturally relevant to the tweet topic

DO NOT:
- Use hashtags excessively (0-1 max)
- Sound like a corporate PR account
- Start with "I think" every time
- Be generic or motivational-poster style
"""

# --- Topics ---
# Add your own topics here. The system picks one randomly each time.
TOPICS = [
    "a lesson from building your product — a specific decision or pivot",
    "a contrarian take on today's tech news",
    "a raw founder moment — a mistake, rejection, or hard call",
    "your opinion on current AI trends",
    "a hot take that might be unpopular",
]

# --- Banned Phrases ---
# GPT loves filler. Add phrases here that sound too generic.
BANNED_PHRASES = [
    "let's keep building",
    "game changer",
    "the future is",
    "excited to see",
    "authenticity wins",
    "real connections",
    "it's about",
    "make all the difference",
    "keep innovating",
    "here to stay",
    "truly resonates",
    "focus on",
    "empower",
    "huge implications",
    "trusting the process",
]


def get_latest_scan():
    """Read the most recent research scan report (optional)."""
    if not SCAN_DIR or not os.path.isdir(SCAN_DIR):
        return ""
    files = sorted(os.listdir(SCAN_DIR), reverse=True)
    for f in files:
        if f.endswith(".md"):
            with open(os.path.join(SCAN_DIR, f)) as fh:
                return fh.read()[:3000]
    return ""


def get_recent_tweets():
    """Read recently posted tweets to avoid repetition."""
    if not os.path.isdir(LOG_DIR):
        return ""
    files = sorted(os.listdir(LOG_DIR), reverse=True)[:10]
    tweets = []
    for f in files:
        with open(os.path.join(LOG_DIR, f)) as fh:
            data = json.load(fh)
            tweets.append(data.get("text", ""))
    return "\n---\n".join(tweets) if tweets else ""


def generate_tweet():
    """Use OpenAI to generate a tweet."""
    scan = get_latest_scan()
    recent = get_recent_tweets()
    topic = random.choice(TOPICS)
    banned = ", ".join(f'"{p}"' for p in BANNED_PHRASES)

    prompt = f"""{PERSONA}

Write ONE tweet (max 220 chars) about: {topic}

Context — today's research scan (use as inspiration, don't copy verbatim):
{scan[:1500] if scan else "(no scan available today)"}

Recent tweets (DO NOT repeat similar topics or phrasing):
{recent[:800] if recent else "(none yet)"}

CRITICAL RULES:
- MUST be under 220 characters (count carefully — spaces, emoji, @mentions all count)
- MUST include at least one @mention
- NEVER FABRICATE DATA. Do NOT invent numbers, stats, percentages, or metrics.
- NO generic filler. BANNED phrases: {banned}
- NEVER end with a generic motivational statement.
- Shorter is ALWAYS better. 140 chars > 220 chars.
- One idea per tweet.
- Output ONLY the tweet text, nothing else. No quotes around it.

VARIETY (critical — never repeat the same format):
- Mix formats: bold claims, disagreements, questions, one-liners, mini-stories
- Mix tone: funny, dead serious, provocative, vulnerable
- NEVER start two tweets the same way.
- BE BOLD. Safe tweets get zero engagement.
"""

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        json={
            "model": "gpt-5.1",
            "messages": [{"role": "user", "content": prompt}],
            "max_completion_tokens": 150,
            "temperature": 0.9,
        },
        timeout=30,
    )
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"].strip().strip('"')

    # Retry up to 3 times if over 280 chars
    for _ in range(3):
        if len(text) <= 280:
            break
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
            json={
                "model": "gpt-5.1",
                "messages": [{"role": "user", "content": f"Rewrite this tweet to be UNDER 230 characters. Keep the same meaning but make it shorter and punchier. Output ONLY the tweet text, no quotes:\n\n{text}"}],
                "max_completion_tokens": 100,
                "temperature": 0.7,
            },
            timeout=30,
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"].strip().strip('"')

    # Hard guard: never attempt to post over 280 chars
    if len(text) > 280:
        raise ValueError(f"Tweet still {len(text)} chars after retries, skipping")

    return text


def post_tweet(text):
    """Post tweet via X API v2."""
    client = tweepy.Client(
        consumer_key=X_CONSUMER_KEY,
        consumer_secret=X_CONSUMER_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET,
    )
    resp = client.create_tweet(text=text)
    return resp.data["id"]


def log_tweet(text, tweet_id):
    """Log posted tweet for dedup."""
    os.makedirs(LOG_DIR, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(LOG_DIR, f"{now}.json"), "w") as f:
        json.dump({"text": text, "tweet_id": str(tweet_id), "posted_at": now}, f, indent=2)


def notify_telegram(text, tweet_id, status="success", error_msg=""):
    """Send tweet status notification to Telegram bot."""
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if status == "success":
        url = f"https://x.com/i/status/{tweet_id}"
        msg = (
            f"[Auto Tweet] Posted\n"
            f"{now}\n\n"
            f"{text}\n\n"
            f"({len(text)} chars)\n"
            f"Link: {url}"
        )
    else:
        msg = (
            f"[Auto Tweet] FAILED\n"
            f"{now}\n\n"
            f"Tweet: {text}\n\n"
            f"Error: {error_msg}"
        )
    try:
        requests.post(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            data={"chat_id": TG_CHAT_ID, "text": msg, "disable_web_page_preview": True},
            timeout=10,
        )
    except Exception as e:
        print(f"Telegram notify failed: {e}")


def main():
    dry_run = "--dry-run" in sys.argv

    try:
        text = generate_tweet()
    except Exception as e:
        notify_telegram("", "", status="error", error_msg=f"Generation failed: {e}")
        raise

    print(f"Generated: {text}")
    print(f"Length: {len(text)} chars")

    if dry_run:
        print("(dry run — not posting)")
        return

    try:
        tweet_id = post_tweet(text)
    except Exception as e:
        notify_telegram(text, "", status="error", error_msg=f"Post failed: {e}")
        raise

    log_tweet(text, tweet_id)
    notify_telegram(text, tweet_id, status="success")
    print(f"Posted! Tweet ID: {tweet_id}")


if __name__ == "__main__":
    main()
