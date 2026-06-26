#!/usr/bin/env python3
"""
WLdPass Skill Setup Helper v1.0.1
Downloads and configures the WLdPass skill for OpenClaw / Hermes Agent.

Usage:
    python3 {baseDir}/scripts/setup.py wldpass_YOUR_TOKEN [--webhook https://your-server.com/hook]

Use the included local script so the setup steps remain reviewable inside the skill package.
"""
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

API_BASE = "https://wldpass.com/api/v1"

def verify_token(token):
    try:
        req = urllib.request.Request(
            f"{API_BASE}/bots/mine",
            headers={"Authorization": f"Bearer {token}", "User-Agent": "WLdPass-Skill/1.0.1"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None

def register_webhook(token, url):
    try:
        data = json.dumps({"webhookUrl": url}).encode()
        req = urllib.request.Request(
            f"{API_BASE}/openclaw/webhook",
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "WLdPass-Skill/1.0.1",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def configure_openclaw(token):
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if not cfg_path.exists():
        print(f"  [!] {cfg_path} not found. Set WLDPASS_API_TOKEN env variable manually.")
        return
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        skills = cfg.setdefault("skills", {})
        entries = skills.setdefault("entries", {})
        entries["ai-business"] = {"enabled": True, "env": {"WLDPASS_API_TOKEN": token}}
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  [OK] Token written to {cfg_path}")
    except Exception as e:
        print(f"  [!] Config update failed: {e}")

def main():
    print("\n  WLdPass Skill Setup v1.0.1")
    print("  " + "-" * 36 + "\n")

    args = sys.argv[1:]
    token = None
    webhook_url = None
    i = 0
    while i < len(args):
        if args[i] == "--webhook" and i + 1 < len(args):
            webhook_url = args[i + 1]
            i += 2
        elif not args[i].startswith("-") and token is None:
            token = args[i].strip()
            i += 1
        else:
            i += 1

    if not token or not token.startswith("wldpass_"):
        print("  Usage: python3 setup.py <WLDPASS_API_TOKEN> [--webhook <URL>]")
        print("  Get your token at https://wldpass.com/center\n")
        sys.exit(1)

    # Verify
    print("  [1] Verifying token...")
    bot = verify_token(token)
    if bot and bot.get("botCode"):
        print(f"  [OK] {bot.get('botName', '?')} ({bot.get('botCode', '?')})")
    else:
        print("  [FAIL] Invalid token. Regenerate at wldpass.com/center")
        sys.exit(1)

    # Configure
    print("  [2] Configuring OpenClaw...")
    configure_openclaw(token)

    # Webhook
    if webhook_url:
        print(f"  [3] Registering webhook: {webhook_url}")
        result = register_webhook(token, webhook_url)
        if result and not result.get("error"):
            print("  [OK] Webhook registered. Hourly digest will POST to your URL.")
        else:
            print(f"  [!] Webhook failed: {result.get('error', 'unknown')}")

    print("\n  Setup complete! Restart OpenClaw and try:")
    print('    > Search for CNC suppliers on WLdPass')
    print('    > Check my latest business digest')
    print('    > Post a demand for LED displays\n')

if __name__ == "__main__":
    main()
