#!/usr/bin/env python3
"""
Discord AI Hub Builder
Builds a full AI command center server structure via Discord REST API.
Usage: python3 build_hub.py --token BOT_TOKEN --guild GUILD_ID [--dry-run]
"""

import argparse
import json
import time
import sys
import urllib.request
import urllib.error

BASE = "https://discord.com/api/v10"


def api(method, path, token, data=None):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw-Discord-Hub-Builder/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            time.sleep(0.5)  # basic rate limit respect
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ERROR {e.code} on {method} {path}: {body}", file=sys.stderr)
        return None


def build_hub(token, guild_id, dry_run=False):
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Building AI Hub for guild {guild_id}\n")

    # ── Roles ──────────────────────────────────────────────────────────────
    print("── Creating roles ──")
    roles = {
        "Agent": {"color": 0x5865F2, "hoist": True},
        "Reviewer": {"color": 0x57F287, "hoist": True},
    }
    role_ids = {}
    existing_roles = api("GET", f"/guilds/{guild_id}/roles", token) or []
    existing_names = {r["name"]: r["id"] for r in existing_roles}

    for name, opts in roles.items():
        if name in existing_names:
            role_ids[name] = existing_names[name]
            print(f"  ✓ {name} (exists)")
        elif not dry_run:
            r = api("POST", f"/guilds/{guild_id}/roles", token, {"name": name, **opts})
            if r:
                role_ids[name] = r["id"]
                print(f"  + {name} created (id={r['id']})")
        else:
            print(f"  [dry] Would create role: {name}")

    # ── Categories & Channels ──────────────────────────────────────────────
    print("\n── Creating categories & channels ──")

    STRUCTURE = [
        {
            "category": "COMMAND CENTER",
            "channels": [
                {"name": "daily-brief", "topic": "Daily summaries and briefings from agents.", "readonly_humans": False},
                {"name": "task-queue", "topic": "Owner-only task intake. Drop requests here.", "owner_only_send": True},
            ],
        },
        {
            "category": "AGENT CHANNELS",
            "channels": [
                {"name": "agent-openclaw", "topic": "OpenClaw agent outputs and status.", "workflow_card": True, "tool": "OpenClaw", "trigger": "Heartbeat + direct task", "input": "Plain English task or cron", "output": "Summaries, files, confirmations", "frequency": "On-demand + 2-4x/day heartbeat"},
                {"name": "agent-perplexity", "topic": "Perplexity research outputs.", "workflow_card": True, "tool": "Perplexity", "trigger": "Research request", "input": "Question or topic", "output": "Research brief with sources", "frequency": "On-demand"},
                {"name": "agent-manus", "topic": "Manus agent outputs.", "workflow_card": True, "tool": "Manus", "trigger": "Complex multi-step task", "input": "Detailed task description", "output": "Completed task artifacts", "frequency": "On-demand"},
            ],
        },
        {
            "category": "RESEARCH & OUTPUTS",
            "channels": [
                {"name": "financial-briefs", "topic": "Financial research and analysis outputs.", "readonly_humans": True},
                {"name": "content-drafts", "topic": "Draft content from agents for review.", "readonly_humans": True},
                {"name": "research-archive", "topic": "Completed research drops.", "readonly_humans": True},
            ],
        },
        {
            "category": "OPERATIONS",
            "channels": [
                {"name": "agent-logs", "topic": "Agent activity logs.", "readonly_humans": True},
                {"name": "ops-notes", "topic": "Operational notes and config changes."},
                {"name": "personal", "topic": "Personal channel — Owner only."},
            ],
        },
    ]

    created = []

    for block in STRUCTURE:
        cat_name = block["category"]
        if not dry_run:
            cat = api("POST", f"/guilds/{guild_id}/channels", token, {
                "name": cat_name,
                "type": 4,  # GUILD_CATEGORY
            })
            cat_id = cat["id"] if cat else None
            print(f"\n  [Category] {cat_name} (id={cat_id})")
        else:
            cat_id = "DRY_RUN_ID"
            print(f"\n  [dry] Category: {cat_name}")

        for ch in block["channels"]:
            ch_data = {
                "name": ch["name"],
                "type": 0,  # GUILD_TEXT
                "parent_id": cat_id,
                "topic": ch.get("topic", ""),
            }

            if not dry_run:
                channel = api("POST", f"/guilds/{guild_id}/channels", token, ch_data)
                if channel:
                    ch_id = channel["id"]
                    print(f"    + #{ch['name']} (id={ch_id})")
                    created.append({"name": ch["name"], "id": ch_id, "data": ch})
                else:
                    print(f"    ! Failed to create #{ch['name']}")
            else:
                print(f"    [dry] #{ch['name']}")

    # ── Workflow Cards ─────────────────────────────────────────────────────
    if not dry_run and created:
        print("\n── Pinning workflow cards ──")
        for ch in created:
            if not ch["data"].get("workflow_card"):
                continue
            d = ch["data"]
            card = (
                f"```\n"
                f"TOOL      : {d.get('tool','—')}\n"
                f"TRIGGER   : {d.get('trigger','—')}\n"
                f"INPUT     : {d.get('input','—')}\n"
                f"OUTPUT    : {d.get('output','—')}\n"
                f"FREQUENCY : {d.get('frequency','—')}\n"
                f"```"
            )
            msg = api("POST", f"/channels/{ch['id']}/messages", token, {"content": card})
            if msg:
                api("PUT", f"/channels/{ch['id']}/pins/{msg['id']}", token)
                print(f"  ✓ Pinned card in #{ch['name']}")

    print("\n── Done ──")
    print(f"Created {len(created)} channels across {len(STRUCTURE)} categories.")
    if created:
        print("\nChannel IDs:")
        for ch in created:
            print(f"  #{ch['name']}: {ch['id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Discord AI Hub")
    parser.add_argument("--token", required=True, help="Discord bot token")
    parser.add_argument("--guild", required=True, help="Guild (server) ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = parser.parse_args()
    build_hub(args.token, args.guild, args.dry_run)
