#!/usr/bin/env python3
"""
blotato_post.py - Post content to multiple platforms via Blotato API

Usage:
  python blotato_post.py --help

Examples:
  python blotato_post.py --api-key KEY --platforms twitter linkedin --content "Your content"
  python blotato_post.py --api-key KEY --platforms all --content "Your content" --schedule "2026-05-01T10:00:00+07:00"
  python blotato_post.py --api-key KEY --platforms twitter --list-accounts
"""

import argparse
import json
import sys
import time
import os
import mimetypes
import urllib.request
import urllib.error

BASE_URL = "https://backend.blotato.com/v2"

PLATFORM_LIMITS = {
    "twitter": 280,
    "linkedin": 3000,
    "facebook": 63206,
    "instagram": 2200,
    "threads": 500,
    "bluesky": 300,
    "tiktok": 2200,
    "pinterest": 500,
    "youtube": 5000,
}

ALL_PLATFORMS = list(PLATFORM_LIMITS.keys())


def api_request(method, path, api_key, data=None):
    url = f"{BASE_URL}{path}"
    headers = {
        "blotato-api-key": api_key,
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"[ERROR] HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def list_accounts(api_key):
    resp = api_request("GET", "/users/me/accounts", api_key)
    return resp.get("items", [])


def get_subaccounts(api_key, account_id):
    resp = api_request("GET", f"/users/me/accounts/{account_id}/subaccounts", api_key)
    return resp.get("items", [])


def adapt_content(original_text, platform):
    """Adapt content for platform limits and style."""
    limit = PLATFORM_LIMITS.get(platform, 500)
    text = original_text.strip()

    if platform == "twitter":
        if len(text) <= limit:
            return {"text": text, "additionalPosts": None}
        # Split into thread
        words = text.split()
        tweets = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= limit - 10:  # leave room for numbering
                current = (current + " " + word).strip()
            else:
                tweets.append(current)
                current = word
        if current:
            tweets.append(current)
        additional = [{"text": t, "mediaUrls": []} for t in tweets[1:]]
        return {"text": tweets[0], "additionalPosts": additional if additional else None}

    elif platform == "linkedin":
        # Professional tone hint kept — agent should adapt before calling
        if len(text) > limit:
            text = text[:limit - 3] + "..."
        return {"text": text, "additionalPosts": None}

    else:
        if len(text) > limit:
            text = text[:limit - 3] + "..."
        return {"text": text, "additionalPosts": None}


def upload_media_from_url(api_key, url):
    """Upload media to Blotato from a public URL. Returns hosted Blotato URL."""
    resp = api_request("POST", "/media", api_key, {"url": url})
    return resp.get("url")


def upload_local_file(api_key, file_path):
    """Upload a local file to Blotato via presigned URL. Returns public URL."""
    filename = os.path.basename(file_path)
    # Step 1: Get presigned URL
    resp = api_request("POST", "/media/uploads", api_key, {"filename": filename})
    presigned_url = resp.get("presignedUrl")
    public_url = resp.get("publicUrl")

    if not presigned_url:
        print(f"[ERROR] Failed to get presigned URL for {filename}", file=sys.stderr)
        sys.exit(1)

    # Step 2: PUT file to presigned URL
    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_data = f.read()

    req = urllib.request.Request(presigned_url, data=file_data, method="PUT")
    req.add_header("Content-Type", mime_type)
    try:
        with urllib.request.urlopen(req) as r:
            pass  # 200 OK = success
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Upload failed: {e.code} {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    print(f"       Uploaded: {filename} → {public_url}")
    return public_url


def resolve_media(api_key, media_inputs):
    """
    Resolve a list of media inputs to public URLs.
    Each item can be:
      - local file path (e.g. /path/to/photo.jpg)
      - public URL (https://...)
    Returns list of public URLs ready for mediaUrls.
    """
    resolved = []
    for item in media_inputs:
        if item.startswith("http://") or item.startswith("https://"):
            resolved.append(item)
        elif os.path.isfile(item):
            print(f"[UPLOAD] Local file: {item}")
            url = upload_local_file(api_key, item)
            resolved.append(url)
        else:
            print(f"[WARN] Media not found, skipping: {item}")
    return resolved


def publish_post(api_key, account_id, platform, text, additional_posts=None,
                 media_urls=None, page_id=None, board_id=None,
                 scheduled_time=None, use_next_slot=False,
                 tiktok_opts=None, youtube_opts=None):
    content = {
        "text": text,
        "mediaUrls": media_urls or [],
        "platform": platform,
    }
    if additional_posts:
        content["additionalPosts"] = additional_posts

    target = {"targetType": platform}
    if page_id and platform in ("facebook", "linkedin"):
        target["pageId"] = page_id
    if board_id and platform == "pinterest":
        target["boardId"] = board_id
    if platform == "tiktok" and tiktok_opts:
        target.update(tiktok_opts)
    if platform == "youtube" and youtube_opts:
        target.update(youtube_opts)

    payload = {
        "post": {
            "accountId": account_id,
            "content": content,
            "target": target,
        }
    }

    if scheduled_time:
        payload["scheduledTime"] = scheduled_time
    elif use_next_slot:
        payload["useNextFreeSlot"] = True

    resp = api_request("POST", "/posts", api_key, payload)
    return resp


def poll_post_status(api_key, submission_id, max_wait=60):
    for _ in range(max_wait // 5):
        time.sleep(5)
        resp = api_request("GET", f"/posts/{submission_id}", api_key)
        status = resp.get("status", "unknown")
        if status in ("published", "scheduled", "failed", "error"):
            return resp
    return {"status": "timeout", "postSubmissionId": submission_id}


def main():
    parser = argparse.ArgumentParser(description="Post to multiple platforms via Blotato API")
    parser.add_argument("--api-key", required=True, help="Blotato API key")
    parser.add_argument("--content", help="Content to post (will be adapted per platform)")
    parser.add_argument("--platforms", nargs="+", default=["twitter"],
                        help=f"Platforms to post to. Use 'all' for all. Options: {', '.join(ALL_PLATFORMS)}")
    parser.add_argument("--media-urls", nargs="*", default=[], help="Public media URLs to attach")
    parser.add_argument("--schedule", help="ISO 8601 datetime to schedule (e.g. 2026-05-01T10:00:00+07:00)")
    parser.add_argument("--use-next-slot", action="store_true", help="Use next available calendar slot")
    parser.add_argument("--list-accounts", action="store_true", help="List connected accounts and exit")
    parser.add_argument("--no-poll", action="store_true", help="Don't poll for post status")
    parser.add_argument("--accounts-json", help="JSON file mapping platform->accountId (skip auto-detect)")
    args = parser.parse_args()

    if args.list_accounts:
        accounts = list_accounts(args.api_key)
        print(json.dumps(accounts, indent=2))
        return

    if not args.content:
        print("[ERROR] --content is required", file=sys.stderr)
        sys.exit(1)

    platforms = ALL_PLATFORMS if "all" in args.platforms else args.platforms

    # Resolve media (upload local files if needed)
    media_urls = resolve_media(args.api_key, args.media_urls) if args.media_urls else []
    account_map = {}
    if args.accounts_json:
        with open(args.accounts_json) as f:
            account_map = json.load(f)
    else:
        print("[INFO] Fetching connected accounts...")
        all_accounts = list_accounts(args.api_key)
        for acc in all_accounts:
            plat = acc["platform"]
            if plat not in account_map:
                account_map[plat] = {"accountId": acc["id"], "fullname": acc.get("fullname", "")}

    results = []
    for platform in platforms:
        if platform not in account_map:
            print(f"[SKIP] No account connected for: {platform}")
            continue

        acc_info = account_map[platform]
        account_id = acc_info["accountId"] if isinstance(acc_info, dict) else acc_info
        page_id = acc_info.get("pageId") if isinstance(acc_info, dict) else None

        # Auto-fetch pageId for Facebook/LinkedIn if not provided
        if platform in ("facebook", "linkedin") and not page_id:
            subaccs = get_subaccounts(args.api_key, account_id)
            if subaccs:
                page_id = subaccs[0]["id"]

        adapted = adapt_content(args.content, platform)
        text = adapted["text"]
        additional = adapted["additionalPosts"]

        print(f"[POST] {platform} | {len(text)} chars" + (" | thread" if additional else ""))

        resp = publish_post(
            api_key=args.api_key,
            account_id=account_id,
            platform=platform,
            text=text,
            additional_posts=additional,
            media_urls=media_urls,
            page_id=page_id,
            scheduled_time=args.schedule,
            use_next_slot=args.use_next_slot,
        )

        submission_id = resp.get("postSubmissionId") or resp.get("id")
        if not args.no_poll and submission_id:
            status_resp = poll_post_status(args.api_key, submission_id)
            resp["polledStatus"] = status_resp.get("status")
            print(f"       Status: {resp['polledStatus']}")
        else:
            print(f"       Submitted: {submission_id}")

        results.append({"platform": platform, "result": resp})

    print("\n[DONE] Summary:")
    for r in results:
        status = r["result"].get("polledStatus") or r["result"].get("status", "submitted")
        print(f"  {r['platform']:12} → {status}")


if __name__ == "__main__":
    main()
