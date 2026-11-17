#!/usr/bin/env python3
"""
fish_voices.py — 管理 Fish Audio 已克隆声音。

用法:
    python fish_voices.py list                        # 后端 + 本地缓存
    python fish_voices.py list --json
    python fish_voices.py sync                        # 后端 voice 同步进本地缓存
    python fish_voices.py delete --voice-id <id> --yes
    python fish_voices.py delete --cached-name "锋哥的声音" --yes
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_BASE = "https://api.fish.audio"
CACHE_FILE = Path(__file__).parent / "voices_cache.json"


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        print("✗ 环境变量 FISH_API_KEY 未设置 → python setup.py set-fish", file=sys.stderr)
        sys.exit(1)
    return key


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict):
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def http(method: str, url: str, api_key: str):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        print(f"✗ 网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    api_key = get_api_key()
    status, body = http("GET", f"{API_BASE}/model?pageSize=50", api_key)
    if status != 200:
        print(f"✗ Fish API {status}: {body[:300]}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(body)
    items = data.get("items", []) if isinstance(data, dict) else data
    cache = load_cache()

    if args.json:
        print(json.dumps({"backend": items, "local_cache": cache}, indent=2, ensure_ascii=False))
        return

    print(f"🐟 后端 voice 模型 ({len(items)} 个):")
    for i, v in enumerate(items, 1):
        state = v.get("state", "?")
        mark = {"trained": "✓", "created": "⏳", "training": "⏳"}.get(state, "✗")
        print(f"  {i}. [{mark}] {v.get('title', '(无标题)')}")
        print(f"     id={v.get('_id')} state={state} visibility={v.get('visibility', '?')}")
    print(f"\n📁 本地缓存 ({len(cache)} 个) → voices_cache.json:")
    for name, entry in cache.items():
        print(f"  • '{name}' → {entry.get('voice_id', '?')[:12]}... (state={entry.get('state', '?')})")


def cmd_sync(args):
    api_key = get_api_key()
    status, body = http("GET", f"{API_BASE}/model?pageSize=50", api_key)
    if status != 200:
        print(f"✗ Fish API {status}: {body[:300]}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(body)
    items = data.get("items", []) if isinstance(data, dict) else data
    cache = load_cache()
    added = 0
    for v in items:
        vid = v.get("_id") or v.get("id")
        title = v.get("title", "(no title)")
        if vid and title and title not in cache:
            cache[title] = {
                "voice_id": vid,
                "title": title,
                "state": v.get("state", "unknown"),
                "engine": "fish-audio",
                "visibility": v.get("visibility", "private"),
            }
            added += 1
    save_cache(cache)
    print(f"✅ 同步完成，新增 {added} 个（缓存共 {len(cache)} 个）")


def cmd_delete(args):
    if not args.voice_id and not args.cached_name:
        print("✗ --voice-id 或 --cached-name 至少传一个", file=sys.stderr)
        sys.exit(1)
    cache = load_cache()
    cache_key = None
    voice_id = args.voice_id
    if args.cached_name:
        if args.cached_name not in cache:
            print(f"✗ 缓存里没有 '{args.cached_name}'", file=sys.stderr)
            sys.exit(1)
        voice_id = cache[args.cached_name]["voice_id"]
        cache_key = args.cached_name

    if not args.yes:
        print(f"⚠️ 即将删除 Fish voice {voice_id}，加 --yes 确认执行", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    status, body = http("DELETE", f"{API_BASE}/model/{voice_id}", api_key)
    if status in (200, 204):
        print(f"✅ 已删除 voice_id={voice_id} (HTTP {status})")
        if cache_key:
            del cache[cache_key]
            save_cache(cache)
            print(f"✅ 已从本地缓存移除 '{cache_key}'")
    else:
        print(f"✗ HTTP {status}: {body[:300]}", file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Fish Audio voice 模型管理")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_list = sub.add_parser("list")
    p_list.add_argument("--json", action="store_true")
    sub.add_parser("sync")
    p_del = sub.add_parser("delete")
    p_del.add_argument("--voice-id")
    p_del.add_argument("--cached-name")
    p_del.add_argument("--yes", action="store_true", help="跳过确认")
    args = ap.parse_args()

    {"list": cmd_list, "sync": cmd_sync, "delete": cmd_delete}[args.cmd](args)


if __name__ == "__main__":
    main()
