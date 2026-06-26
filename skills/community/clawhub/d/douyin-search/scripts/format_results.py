#!/usr/bin/env python3
"""Douyin Search via OpenClaw Browser — uses the existing openclaw browser profile
which may already have login cookies from user interaction.

This script is designed to be called by the OpenClaw agent using `browser` tool calls,
not run standalone. See SKILL.md for the agent-driven search protocol.

For standalone usage with a persistent login profile, use douyin_search.py instead.
"""

import json
import sys


def format_results(raw_json: str) -> str:
    """Format intercepted API results into a readable summary."""
    try:
        data = json.loads(raw_json)
    except Exception:
        return raw_json

    if data.get("status") == "login_required":
        return f"⚠️ 需要登录：{data['message']}"

    results = data.get("results", [])
    if not results:
        return f'搜索 "{data.get("keyword", "")}" 没有找到结果。可能需要先登录抖音。'

    lines = [f'🔍 搜索 "{data["keyword"]}" — 共 {len(results)} 个结果\n']
    for i, r in enumerate(results, 1):
        title = r.get("title", "")[:80]
        author = r.get("author", "")
        likes = r.get("likes", 0)
        url = r.get("url", "")
        lines.append(f"{i}. **{author}** — {title}")
        if likes:
            lines.append(f"   ❤️ {likes}")
        lines.append(f"   🔗 {url}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(format_results(sys.argv[1]))
    else:
        print("Usage: format_results.py '<json_string>'")