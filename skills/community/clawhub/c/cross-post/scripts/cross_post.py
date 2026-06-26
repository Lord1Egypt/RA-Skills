#!/usr/bin/env python3
"""cross-post: Post to Twitter/X, Reddit, and LinkedIn from one prompt."""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG_PATH = os.path.expanduser("~/.config/cross-post/config.json")


def load_config():
    """Load API config from JSON file."""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config not found at {CONFIG_PATH}")
        print("Run: cross-post init-config")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def write_config(config):
    """Write API config to JSON file."""
    Path(CONFIG_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    print(f"Config saved to {CONFIG_PATH}")


def init_config():
    """Interactive config setup."""
    print("=== Cross-Post Configuration ===\n")
    config = {}

    # Twitter/X
    print("Twitter/X (optional):")
    config["twitter_bearer_token"] = input("  Bearer Token (leave blank to skip): ").strip()
    config["twitter_user_id"] = input("  User ID (for posting): ").strip()

    # Reddit
    print("\nReddit (optional):")
    config["reddit_client_id"] = input("  Client ID: ").strip()
    config["reddit_client_secret"] = input("  Client Secret: ").strip()
    config["reddit_username"] = input("  Username: ").strip()
    config["reddit_subreddit"] = input("  Default subreddit: ").strip()

    # LinkedIn
    print("\nLinkedIn (optional):")
    config["linkedin_access_token"] = input("  Access Token (leave blank to skip): ").strip()
    config["linkedin_person_urn"] = input("  Person URN: ").strip()

    write_config(config)
    print("\nDone! You can edit the config later with a text editor.")


def post_twitter(config, text, thread=False):
    """Post to Twitter/X using API v2."""
    bearer = config.get("twitter_bearer_token", "")
    if not bearer:
        print("[Twitter] SKIPPED: No bearer token configured")
        return

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Content-Type": "application/json",
    }

    # Get user info to verify token works
    user_id = config.get("twitter_user_id", "")
    if not user_id:
        try:
            req = urllib.request.Request(
                "https://api.twitter.com/2/users/me",
                headers=headers,
            )
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            user_id = data["data"]["id"]
            config["twitter_user_id"] = user_id
            write_config(config)
        except Exception as e:
            print(f"[Twitter] ERROR: Failed to verify token: {e}")
            return

    if thread:
        # Split into 280-char tweets
        tweets = split_thread(text)
        posted_ids = []

        for i, tweet_text in enumerate(tweets):
            payload = {
                "text": tweet_text,
            }
            if i == 0:
                payload["reply"] = {"exclude_reply_user_ids": [user_id]}
            else:
                payload["reply"] = {"in_reply_to_tweet_id": posted_ids[-1]}

            try:
                req = urllib.request.Request(
                    "https://api.twitter.com/2/tweets",
                    data=json.dumps(payload).encode(),
                    headers=headers,
                    method="POST",
                )
                resp = urllib.request.urlopen(req, timeout=10)
                data = json.loads(resp.read())
                tweet_id = data["data"]["id"]
                posted_ids.append(tweet_id)
                print(f"[Twitter] Posted tweet {i+1}/{len(tweets)}: {tweet_id}")
                time.sleep(1)  # rate limit
            except Exception as e:
                print(f"[Twitter] ERROR posting tweet {i+1}: {e}")
                break
    else:
        try:
            req = urllib.request.Request(
                "https://api.twitter.com/2/tweets",
                data=json.dumps({"text": text}).encode(),
                headers=headers,
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            print(f"[Twitter] Posted: {data['data']['id']}")
        except Exception as e:
            print(f"[Twitter] ERROR: {e}")


def split_thread(text):
    """Split text into 280-char tweets for a thread."""
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 <= 280:
            current = f"{current}\n{line}" if current else line
        else:
            if current:
                chunks.append(current.strip())
            current = line
    if current:
        chunks.append(current.strip())

    # Handle very long individual lines
    result = []
    for chunk in chunks:
        if len(chunk) <= 280:
            result.append(chunk)
        else:
            # Break on character boundary
            while len(chunk) > 280:
                split_at = chunk.rfind(".", 200, 280)
                if split_at == -1:
                    split_at = 280
                result.append(chunk[:split_at].rstrip())
                chunk = chunk[split_at:].strip()
            if chunk:
                result.append(chunk)
    return result


def get_reddit_token(config):
    """Get Reddit OAuth2 token."""
    client_id = config.get("reddit_client_id", "")
    client_secret = config.get("reddit_client_secret", "")
    if not client_id or not client_secret:
        return None

    auth = urllib.request.HTTPBasicAuthHandler()
    credentials = f"{client_id}:{client_secret}"
    encoded = credentials.encode()
    encoded_b64 = __import__("base64").b64encode(encoded).decode()

    data = urllib.parse.urlencode({
        "grant_type": "password",
        "username": config.get("reddit_username", ""),
        "password": os.environ.get("REDDIT_PASSWORD", ""),
    }).encode()

    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=data,
        headers={
            "Authorization": f"Basic {encoded_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        token_data = json.loads(resp.read())
        return token_data.get("access_token")
    except Exception as e:
        print(f"[Reddit] Token error: {e}")
        return None


def post_reddit(config, title, body, subreddit=None):
    """Post to Reddit."""
    token = get_reddit_token(config)
    if not token:
        print("[Reddit] SKIPPED: No OAuth token")
        return

    subreddit = subreddit or config.get("reddit_subreddit", "all")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "cross-post/1.0",
    }

    payload = {
        "sr": subreddit,
        "title": title,
        "kind": "self",
        "text": body,
    }

    try:
        req = urllib.request.Request(
            "https://oauth.reddit.com/api/link",
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        if "json" in data and "errors" in data["json"]:
            print(f"[Reddit] ERROR: {data['json']['errors']}")
        elif "data" in data:
            post_id = data["data"].get("id", "unknown")
            print(f"[Reddit] Posted to r/{subreddit}: {post_id}")
        else:
            print(f"[Reddit] Posted (response: {data})")
    except Exception as e:
        print(f"[Reddit] ERROR: {e}")


def post_linkedin(config, text):
    """Post to LinkedIn."""
    token = config.get("linkedin_access_token", "")
    if not token:
        print("[LinkedIn] SKIPPED: No access token configured")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    person_urn = config.get("linkedin_person_urn", "")
    if not person_urn:
        print("[LinkedIn] SKIPPED: No person URN configured")
        return

    # LinkedIn v2 post creation
    payload = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text[:3000],  # LinkedIn 3000 char limit
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    try:
        req = urllib.request.Request(
            "https://api.linkedin.com/v2/ugcPosts",
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        post_id = data.get("id", "unknown")
        print(f"[LinkedIn] Posted: {post_id}")
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"[LinkedIn] ERROR: {e.code} - {body}")
    except Exception as e:
        print(f"[LinkedIn] ERROR: {e}")


def format_platforms(text, platform):
    """Format text for a specific platform."""
    platform = platform.lower()
    text = text.strip()

    if platform == "twitter":
        # Twitter: concise, thread-friendly
        return text
    elif platform == "reddit":
        # Reddit: more detail, markdown-friendly
        return text
    elif platform == "linkedin":
        # LinkedIn: professional tone
        return text
    return text


def main():
    parser = argparse.ArgumentParser(description="Cross-post to social media")
    sub = parser.add_subparsers(dest="command")

    # init-config
    sub.add_parser("init-config", help="Set up API credentials")

    # post
    post_parser = sub.add_parser("post", help="Post content")
    post_parser.add_argument("text", nargs="?", help="Content to post")
    post_parser.add_argument("--file", "-f", help="Read content from file")
    post_parser.add_argument("--platform", "-p", choices=["twitter", "reddit", "linkedin", "all"],
                             default="all", help="Platform to post to")
    post_parser.add_argument("--thread", action="store_true", help="Post as Twitter thread")
    post_parser.add_argument("--title", "-t", help="Title (for Reddit)")
    post_parser.add_argument("--subreddit", "-s", help="Subreddit (for Reddit)")

    # preview
    preview_parser = sub.add_parser("preview", help="Preview formatting")
    preview_parser.add_argument("text", nargs="?", help="Content to preview")
    preview_parser.add_argument("--file", "-f", help="Read content from file")
    preview_parser.add_argument("--platform", "-p", choices=["twitter", "reddit", "linkedin"],
                                required=True, help="Platform to preview for")

    args = parser.parse_args()

    if args.command == "init-config":
        init_config()
        return

    if args.command == "post":
        if not args.text and not args.file:
            print("Error: Provide text or --file")
            sys.exit(1)

        config = load_config()
        text = args.text or Path(args.file).read_text()

        platforms = ["all"] if args.platform == "all" else [args.platform]

        for p in platforms:
            if p == "twitter":
                post_twitter(config, text, thread=args.thread)
            elif p == "reddit":
                post_reddit(config, args.title or text[:100], text, args.subreddit)
            elif p == "linkedin":
                post_linkedin(config, text)

        print("\nDone!")

    elif args.command == "preview":
        if not args.text and not args.file:
            print("Error: Provide text or --file")
            sys.exit(1)

        text = args.text or Path(args.file).read_text()
        platform = args.platform

        print(f"=== {platform.upper()} PREVIEW ===")
        print(f"Length: {len(text)} chars")

        if platform == "twitter":
            chunks = split_thread(text)
            for i, chunk in enumerate(chunks):
                print(f"\nTweet {i+1} ({len(chunk)} chars):")
                print(chunk)
                if len(chunk) > 280:
                    print("  ⚠ EXCEEDS 280 CHAR LIMIT")
            print(f"\nTotal tweets: {len(chunks)}")
        elif platform == "reddit":
            print(f"\n{text[:200]}{'...' if len(text) > 200 else ''}")
        elif platform == "linkedin":
            print(f"Length: {len(text)} chars (limit: 3000)")
            if len(text) > 3000:
                print("⚠ EXCEEDS 3000 CHAR LIMIT")
            print(f"\n{text[:200]}{'...' if len(text) > 200 else ''}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
