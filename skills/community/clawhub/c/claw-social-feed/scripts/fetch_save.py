#!/usr/bin/env python3
"""
claw-social-feed: fetch social media content → filter → tag → save to Obsidian
Dependency: bb-browser (via --openclaw), Python 3.8+
Usage: python3 fetch_save.py [--config path/to/config.yaml]
"""
import json
import os
import re
import shutil
import subprocess
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ── Paths ──────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG = SCRIPT_DIR.parent / "config.yaml"
DEFAULT_STATE = SCRIPT_DIR.parent / ".claw-social-feed-state.json"


# ── CLI ────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="claw-social-feed: fetch & save to Obsidian")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config file path")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only, don't write files")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    return parser.parse_args()


# ── Config ─────────────────────────────────────────
def load_config(path: str) -> dict:
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)


def check_accounts(config: dict) -> list:
    """Return duplicate account keys."""
    seen, duplicates = {}, []
    for acct in config.get("accounts", []):
        key = f"{acct['platform']}:{acct['username']}"
        duplicates.append(key) if key in seen else (seen.update({key: acct}))
    return duplicates


# ── State ──────────────────────────────────────────
def load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"accounts": {}}


def save_state(state: dict, path: str):
    with open(path, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_last_fetch(state: dict, platform: str, username: str) -> Optional[datetime]:
    key = f"{platform}:{username}"
    ts = state.get("accounts", {}).get(key, {}).get("last_fetch")
    return datetime.fromisoformat(ts) if ts else None


def update_state(state: dict, platform: str, username: str,
                 last_id: str, fetched_at: datetime):
    key = f"{platform}:{username}"
    state.setdefault("accounts", {})[key] = {
        "last_fetch": fetched_at.isoformat(),
        "last_id": last_id
    }


# ── Filters ─────────────────────────────────────────
def clean_text(text: str) -> str:
    """Remove URLs and collapse whitespace."""
    text = re.sub(r"https?://\S+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def is_new(state: dict, platform: str, username: str,
           created_at: datetime, item_id: str, catchup_days: int) -> bool:
    """Check if item is new relative to last fetch."""
    last = get_last_fetch(state, platform, username)
    if last is None:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=catchup_days)
    aware = created_at.replace(tzinfo=timezone.utc)
    return aware > last and aware >= cutoff


def is_worth_saving(item: dict, filters: dict) -> tuple[bool, str | None]:
    """Filter low-value content. Returns (save, reason)."""
    text = clean_text(item.get("text", ""))
    item_type = item.get("type", "tweet")

    for kw in filters.get("blocked_keywords", []):
        if kw.lower() in text.lower():
            return False, f"blocked keyword '{kw}'"

    if item_type == "retweet" and filters.get("skip_retweet_no_comment", True):
        if len(text) < 30:
            return False, "retweet with no comment"

    if filters.get("skip_link_only", True) and len(text) < 10:
        return False, "link/image only"

    if len(text) < filters.get("min_text_length", 30):
        return False, f"too short ({len(text)} chars)"

    return True, None


# ── Tagging ─────────────────────────────────────────
def apply_tags(text: str, tagging: dict) -> list[str]:
    """Return tags based on keyword matching."""
    tags = ["claw-social-feed"]
    if not tagging.get("enabled", False):
        return tags
    text_lower = text.lower()
    for keywords, tag in tagging.get("keywords", {}).items():
        for kw in keywords.split("/"):
            if kw.strip().lower() in text_lower:
                tags.append(tag.strip())
                break
    return list(set(tags))


# ── Obsidian writer ────────────────────────────────
def save_to_obsidian(item: dict, tags: list,
                     vault_base: str, platform: str, username: str):
    """Write one item as an Obsidian markdown file."""
    created = item["created_at"]
    dt = datetime.strptime(created, "%a %b %d %H:%M:%S +0000 %Y") \
        if isinstance(created, str) else created

    date_str = dt.strftime("%Y-%m-%d")
    time_str = dt.strftime("%H%M%S")
    item_type = item.get("type", "unknown")
    item_id = item.get("id", "unknown")
    short_id = str(item_id)[-6:]

    folder = Path(vault_base) / f"@{username}"
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / f"{date_str}_{time_str}_{short_id}.md"

    if filepath.exists():
        return False, "already exists"

    tag_lines = "\n".join(f"  - {t}" for t in tags)

    frontmatter = f"""---
platform: {platform}
author: "@{username}"
type: {item_type}
date: {date_str}
time: "{created}"
url: {item.get("url", "")}
likes: {item.get("likes", 0)}
retweets: {item.get("retweets", 0)}
tags:
  - {platform}
  - "@{username}"
{tag_lines}
---

"""

    content = f"""

## {date_str} {time_str[:2]}:{time_str[2:4]} · {item_type}

{item.get("text", "").strip()}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    return True, None


# ── bb-browser ─────────────────────────────────────
def _find_bb_browser() -> str:
    """Dynamically locate bb-browser."""
    if path := shutil.which("bb-browser"):
        return path
    home = os.path.expanduser("~")
    for ver in ["v22.0.0", "v21.0.0", "v20.19.5"]:
        candidate = os.path.join(home, f".nvm/versions/node/{ver}/bin/bb-browser")
        if os.path.isfile(candidate):
            return candidate
    for nvm_bin in [
        os.path.join(home, ".nvm/versions/node/v22.0.0/bin"),
        os.path.join(home, ".nvm/versions/node/v20.19.5/bin"),
        "/opt/homebrew/bin",
        "/usr/local/bin",
    ]:
        candidate = os.path.join(nvm_bin, "bb-browser")
        if os.path.isfile(candidate):
            return candidate
    return "bb-browser"


BB_BROWSER_BIN = _find_bb_browser()


def _platform_cmd(platform: str) -> str:
    """Map platform name → bb-browser subcommand."""
    return {
        "twitter": "tweets",
        "weibo": "user_posts",
        "reddit": "posts",
        "bilibili": "user_posts",
        "xiaohongshu": "user_posts",
        "hackernews": "top",
        "github": "repo",
        "v2ex": "hot",
        "zhihu": "hot",
        "xueqiu": "hot",
    }.get(platform, "hot")


def fetch_account(platform: str, username: str, count: int) -> list[dict]:
    """Fetch user content via bb-browser --openclaw."""
    cmd = [
        BB_BROWSER_BIN,
        "site", f"{platform}/{_platform_cmd(platform)}",
        username, "--openclaw", "--json"
    ]
    env = os.environ.copy()
    env["PATH"] = str(Path(BB_BROWSER_BIN).parent) + ":" + env.get("PATH", "")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=60, env=env)
        raw = result.stdout.strip()

        # Parse JSON envelope from bb-browser
        idx = raw.find('{"id"')
        if idx < 0:
            idx = raw.find('{')
        data = json.loads(raw[idx:raw.rfind('}') + 1])

        return data["data"].get("tweets", []) if data.get("success") else []

    except Exception as e:
        print(f"  [ERROR] {platform}/{username}: {e}")
        return []


# ── Main ────────────────────────────────────────────
def main():
    args = parse_args()
    config = load_config(args.config)
    state = load_state(str(DEFAULT_STATE))

    if dups := check_accounts(config):
        print(f"[WARN] Duplicate accounts: {dups}")

    seen_keys = set()
    fetch_cfg = config.get("fetch", {})
    filters = config.get("filters", {})
    tagging = config.get("tagging", {})
    vault_base = os.path.expanduser(config.get("vault_base", "~/Documents/Obsidian Vault/SocialFeed"))
    count = min(fetch_cfg.get("count", 20), 100)
    catchup_days = config.get("catchup_window_days", 3)
    fetched_at = datetime.now(timezone.utc)

    total_saved = total_skipped = total_new = 0

    for acct in config.get("accounts", []):
        platform, username = acct["platform"], acct["username"]
        key = f"{platform}:{username}"
        if key in seen_keys:
            continue
        seen_keys.add(key)

        print(f"\n▶ {platform}/{username}")
        items = fetch_account(platform, username, count)
        print(f"  Fetched {len(items)} items")

        last_new_id = None
        for item in items:
            item_id = item.get("id", "")
            try:
                created_str = item.get("created_at", "")
                dt = datetime.strptime(created_str, "%a %b %d %H:%M:%S +0000 %Y") \
                    if created_str else None
            except Exception:
                continue

            if not is_new(state, platform, username, dt, item_id, catchup_days):
                continue
            total_new += 1

            worth, reason = is_worth_saving(item, filters)
            if not worth:
                if args.verbose:
                    print(f"  ✗ {item_id}: {reason} | {clean_text(item.get('text',''))[:40]}...")
                total_skipped += 1
                continue

            tags = apply_tags(item.get("text", ""), tagging)

            if not args.dry_run:
                saved, err = save_to_obsidian(item, tags, vault_base, platform, username)
                if err == "already exists" and args.verbose:
                    print(f"  ⏭ {item_id}: already exists")
                else:
                    preview = clean_text(item.get("text", ""))[:50]
                    print(f"  ✓ {item_id}: {preview}...")
                    print(f"    tags: {tags}")
                    total_saved += 1
            else:
                print(f"  [DRY] {item_id}: {clean_text(item.get('text',''))[:50]}...")

            last_new_id = item_id

        if last_new_id and not args.dry_run:
            update_state(state, platform, username, last_new_id, fetched_at)
            save_state(state, str(DEFAULT_STATE))
            print(f"  State updated (last_id: {last_new_id})")

    print(f"\n{'='*50}")
    print(f"Done: {total_new} new | {total_saved} saved | {total_skipped} filtered")


if __name__ == "__main__":
    main()
