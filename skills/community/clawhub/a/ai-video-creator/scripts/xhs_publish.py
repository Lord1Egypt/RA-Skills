#!/usr/bin/env python3
"""
Xiaohongshu Video Publisher - Publishes video to Xiaohongshu via MCP Server.

Usage:
    python xhs_publish.py status
    python xhs_publish.py video --title "Title" --content "Content" --video /path/to/video.mp4
    python xhs_publish.py video --title "Title" --content "Content" --video /path/to/video.mp4 --tags "tag1,tag2"

Requires xiaohongshu-mcp server running at localhost:18060.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

BASE_URL = "http://localhost:18060"
TIMEOUT = 300  # 5 minutes, video upload can be slow

# Bypass proxy for localhost connections
_proxy_handler = urllib.request.ProxyHandler({})
_opener = urllib.request.build_opener(_proxy_handler)


def _post_json(path: str, data: dict, timeout: int = TIMEOUT) -> dict:
    """POST JSON to MCP server."""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with _opener.open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Cannot connect to MCP server at {BASE_URL}: {e}")
        print("Make sure xiaohongshu-mcp is running:")
        print("  ./xiaohongshu-mcp -headless=true -port :18060")
        sys.exit(1)


def _get_json(path: str) -> dict:
    """GET JSON from MCP server."""
    url = f"{BASE_URL}{path}"
    try:
        with _opener.open(urllib.request.Request(url), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Cannot connect to MCP server at {BASE_URL}: {e}")
        print("Make sure xiaohongshu-mcp is running:")
        print("  ./xiaohongshu-mcp -headless=true -port :18060")
        sys.exit(1)


def check_status() -> bool:
    """Check login status. Returns True if logged in."""
    data = _get_json("/api/v1/login/status")
    if data.get("success"):
        login_info = data.get("data", {})
        if login_info.get("is_logged_in"):
            username = login_info.get("username", "Unknown")
            print(f"Logged in as: {username}")
            return True
        else:
            print("Not logged in. Run the login tool first:")
            print("  ./xiaohongshu-login-darwin-arm64")
            return False
    else:
        print(f"Error: {data.get('error', 'Unknown error')}")
        return False


def publish_video(
    title: str,
    content: str,
    video_path: str,
    tags: list = None,
    schedule_at: str = None,
    visibility: str = "公开可见",
) -> bool:
    """Publish a video note to Xiaohongshu. Returns True on success."""
    # Ensure absolute path
    if not os.path.isabs(video_path):
        video_path = os.path.abspath(video_path)

    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        sys.exit(1)

    # Validate title length (max 20 Chinese chars)
    if len(title) > 20:
        print(f"Warning: title is {len(title)} chars, max is 20. Truncating...")
        title = title[:20]

    payload = {
        "title": title,
        "content": content,
        "video": video_path,
        "visibility": visibility,
    }
    if tags:
        payload["tags"] = tags
    if schedule_at:
        payload["schedule_at"] = schedule_at

    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"Publishing video to Xiaohongshu...")
    print(f"  Title: {title}")
    print(f"  Video: {video_path} ({size_mb:.1f} MB)")
    if tags:
        print(f"  Tags: {', '.join(tags)}")
    if schedule_at:
        print(f"  Scheduled: {schedule_at}")

    data = _post_json("/api/v1/publish_video", payload)

    if data.get("success"):
        result = data.get("data", {})
        print(f"Published successfully!")
        print(f"  Status: {result.get('status', 'unknown')}")
        if result.get("post_id"):
            print(f"  Post ID: {result['post_id']}")
        return True
    else:
        print(f"Publish failed: {data.get('error', 'Unknown error')}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Xiaohongshu Video Publisher")
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Check login status")

    # video publish
    video_parser = subparsers.add_parser("video", help="Publish video note")
    video_parser.add_argument("--title", required=True, help="Note title (max 20 chars)")
    video_parser.add_argument("--content", required=True, help="Note content")
    video_parser.add_argument("--video", required=True, help="Local video file path")
    video_parser.add_argument("--tags", help="Comma-separated tags")
    video_parser.add_argument("--schedule-at", help="Schedule time (ISO8601, e.g. 2026-03-15T18:00:00+08:00)")
    video_parser.add_argument(
        "--visibility",
        default="公开可见",
        choices=["公开可见", "仅自己可见", "仅互关好友可见"],
        help="Visibility (default: 公开可见)",
    )

    args = parser.parse_args()

    if args.command == "status":
        check_status()
    elif args.command == "video":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        publish_video(
            args.title, args.content, args.video, tags, args.schedule_at, args.visibility
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
