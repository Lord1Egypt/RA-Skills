#!/usr/bin/env python3
"""Douyin Automation Status Check - Cross-platform.

Reads CONFIG.md and checks: database, Chrome CDP, cover images, creator tools.
Works on Windows, macOS, and Linux.
"""

import json
import re
import sqlite3
import sys
import urllib.request
import urllib.error
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "CONFIG.md"


def load_config():
    """Load and parse CONFIG.md JSON block."""
    if not CONFIG_FILE.exists():
        return None
    text = CONFIG_FILE.read_text(encoding="utf-8")
    m = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if not m:
        return None
    config = json.loads(m.group(1))
    if config.get("douyin_home") == "REQUIRED - run setup.py or edit manually":
        return None
    return config


def check_db(config):
    """Check database and return pending/published counts."""
    db_path = config["chatgroup_db"]
    if not Path(db_path).exists():
        return None, f"NOT FOUND: {db_path}"
    try:
        conn = sqlite3.connect(db_path)
        pending = conn.execute(
            "SELECT COUNT(*) FROM monitor_items WHERE imagetext_published=0 "
            "AND transcript_status='full' AND rank_score>=0"
        ).fetchone()[0]
        today = conn.execute(
            "SELECT COUNT(*) FROM monitor_items WHERE (imagetext_published=1 OR article_published=1) "
            "AND publish_time >= date('now','localtime','+8 hours')"
        ).fetchone()[0]
        conn.close()
        return (pending, today), None
    except Exception as e:
        return None, f"DB Error: {e}"


def check_cdp(config):
    """Check Chrome CDP connection."""
    port = config.get("chrome_cdp_port", 9222)
    try:
        url = f"http://localhost:{port}/json/version"
        req = urllib.request.urlopen(url, timeout=3)
        data = json.loads(req.read())
        return True, data.get("Browser", "Unknown")
    except Exception:
        return False, f"CDP port {port} not responding"


def check_covers(config):
    """Count cover images in uploads directory."""
    uploads = Path(config.get("uploads_dir", ""))
    if not uploads.exists():
        return 0
    count = sum(1 for f in uploads.rglob("*") if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"))
    return count


def check_tools(config):
    """Check creator tools scripts."""
    ct_dir = Path(config.get("creator_tools", ""))
    scripts = {
        "publish-douyin-article.mjs": ct_dir / "src" / "publish-douyin-article.mjs",
        "export-douyin-comments.mjs": ct_dir / "src" / "export-douyin-comments.mjs",
        "reply-douyin-comments.mjs": ct_dir / "src" / "reply-douyin-comments.mjs",
    }
    return {name: path.exists() for name, path in scripts.items()}


def main():
    print("=== Douyin Automation Status ===")
    print(f"OS: {__import__('os').name} / {__import__('sys').platform}")
    print()

    config = load_config()
    if not config:
        print("[CONFIG] NOT CONFIGURED - run 'python scripts/setup.py'")
        sys.exit(1)

    print(f"[CONFIG] Project: {config['douyin_home']}")

    # Database
    print()
    db_result, db_error = check_db(config)
    if db_error:
        print(f"[DB] {db_error}")
    else:
        pending, today = db_result
        color_pending = "!" if pending > 0 else "ok"
        print(f"[DB] Pending: {pending} | Today published: {today} {color_pending}")

    # Chrome CDP
    cdp_ok, cdp_info = check_cdp(config)
    cdp_status = "OK" if cdp_ok else "DOWN"
    if cdp_ok:
        print(f"[CDP] {cdp_status} - {cdp_info}")
    else:
        print(f"[CDP] {cdp_status} - {cdp_info}")

    # Covers
    covers = check_covers(config)
    print(f"[Cover] Image files: {covers}")

    # Creator Tools
    tools = check_tools(config)
    for name, exists in tools.items():
        status = "OK" if exists else "MISSING"
        print(f"[Tools] {name}: {status}")

    # Orchestrator
    orch = Path(config.get("orchestrator", ""))
    print(f"[Orchestrator] {'OK' if orch.exists() else 'MISSING'}: {config.get('orchestrator', '?')}")

    # Agent Backend
    backend = Path(config.get("agent_backend", ""))
    print(f"[Agent Backend] {'OK' if backend.exists() else 'MISSING'}: {config.get('agent_backend', '?')}")
    print()

    all_ok = (
        db_result is not None
        and cdp_ok
        and all(tools.values())
        and orch.exists()
    )
    if all_ok:
        print("All systems operational. Ready to publish.")
    else:
        print("Some issues detected. Review above.")
        print("Run 'python scripts/setup.py' to reconfigure.")


if __name__ == "__main__":
    main()
