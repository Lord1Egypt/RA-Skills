#!/usr/bin/env python3
"""
AgentWyre CLI — Query AI ecosystem intelligence.

Usage:
  python3 agentwyre.py signals [--lang xx]     Get latest signals
  python3 agentwyre.py search <query>          Search archive (daily/pro)
  python3 agentwyre.py security <pkg> [...]    Check security advisories (pro)
  python3 agentwyre.py flash                   Latest flash signal (pro)
  python3 agentwyre.py status                  Service status

Set AGENTWYRE_API_KEY for authenticated access.
"""

import json
import os
import sys
from urllib.request import Request, urlopen

API = "https://agentwyre.ai"
KEY = os.environ.get("AGENTWYRE_API_KEY", "")


def api(path, auth=True):
    headers = {"Accept": "application/json", "User-Agent": "AgentWyre-Skill/1.0"}
    if auth and KEY:
        headers["Authorization"] = f"Bearer {KEY}"
    req = Request(f"{API}{path}", headers=headers)
    resp = urlopen(req, timeout=15)
    return json.loads(resp.read())


def cmd_signals(args):
    lang = ""
    if "--lang" in args:
        idx = args.index("--lang")
        lang = args[idx + 1] if idx + 1 < len(args) else "en"

    path = "/api/feed" if KEY else "/api/feed/free"
    if lang:
        path += f"?lang={lang}"

    data = api(path)
    signals = data.get("signals", data.get("items", []))

    print(f"📡 {len(signals)} signals | Tier: {'authenticated' if KEY else 'free (2-day delay)'}\n")
    for s in signals:
        sev = s.get("severity", "?")
        emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")
        hype = s.get("hype_check", {}).get("hype_level", "?")
        print(f"{emoji} [{sev.upper()}] {s.get('title', '?')}")
        print(f"   Hype: {hype} | Confidence: {s.get('confidence', '?')}/10")
        print(f"   {s.get('summary', '')[:200]}")
        print()


def cmd_search(args):
    if not args:
        print("Usage: agentwyre.py search <query>")
        return
    query = " ".join(args)
    from urllib.parse import quote
    data = api(f"/api/feed?search={quote(query)}")
    signals = data.get("signals", data.get("items", []))
    print(f"🔍 {len(signals)} results for '{query}':\n")
    for s in signals:
        print(f"  → {s.get('title', '?')}")
        print(f"    {s.get('summary', '')[:150]}")
        print()


def cmd_security(args):
    if not KEY:
        print("❌ Security advisories require a Pro API key.")
        print("   Set AGENTWYRE_API_KEY or subscribe: https://agentwyre.ai/#pricing")
        return
    data = api("/api/advisories")
    advisories = data.get("advisories", [])
    if args:
        deps = set(a.lower() for a in args)
        advisories = [a for a in advisories
                     if any(p.lower() in deps for p in a.get("affected_packages", []))]
    print(f"🔒 {len(advisories)} advisories" + (f" for {', '.join(args)}" if args else "") + ":\n")
    for a in advisories:
        print(f"  ⚠️ {a.get('title', '?')}")
        print(f"    Packages: {', '.join(a.get('affected_packages', []))}")
        print()


def cmd_flash(_args):
    if not KEY:
        print("❌ Flash signals require a Pro API key.")
        return
    data = api("/api/flash/latest")
    if data.get("title"):
        print(f"🔴 FLASH: {data['title']}")
        print(f"   {data.get('summary', '')[:300]}")
    else:
        print("No active flash signal.")


def cmd_status(_args):
    data = api("/api/status", auth=False)
    print(f"Status: {data.get('status', '?')}")
    print(f"Service: {data.get('service', '?')}")
    if KEY:
        verify = api("/api/key/verify")
        print(f"Tier: {verify.get('tier', '?')}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    args = sys.argv[2:]

    commands = {
        "signals": cmd_signals,
        "search": cmd_search,
        "security": cmd_security,
        "flash": cmd_flash,
        "status": cmd_status,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(__doc__)
