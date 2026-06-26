#!/usr/bin/env python3
"""GaggiMate WebSocket client for profile management.

Usage:
  gaggimate-ws.py list                          List all profiles
  gaggimate-ws.py get <profile-id>              Get profile by ID
  gaggimate-ws.py save <profile.json>           Save/upload a profile JSON file
  gaggimate-ws.py favorite <profile-id>         Favorite a profile (show on machine)
  gaggimate-ws.py select <profile-id>           Select profile as active
  gaggimate-ws.py delete <profile-id>           Delete a profile
  gaggimate-ws.py push <profile.json>           Save + favorite + select (full deploy)

Environment:
  GAGGIMATE_HOST  (default: gaggimate.local)
"""

import asyncio
import json
import os
import sys
import uuid

try:
    import websockets
except ImportError:
    print("ERROR: websockets not installed. Run: pip3 install websockets", file=sys.stderr)
    sys.exit(1)


HOST = os.environ.get("GAGGIMATE_HOST", "gaggimate.local")
WS_URL = f"ws://{HOST}/ws"
TIMEOUT = 10


async def send_and_receive(msg: dict) -> dict:
    """Send a message and wait for matching response."""
    rid = str(uuid.uuid4())[:8]
    msg["rid"] = rid

    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps(msg))
            while True:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=TIMEOUT)
                    data = json.loads(raw)
                    # Match on rid or on response type
                    if data.get("rid") == rid:
                        return data
                    # Skip status events
                    if data.get("tp", "").startswith("evt:"):
                        continue
                except TimeoutError:
                    return {"error": f"Timeout waiting for response to {msg['tp']}"}
    except OSError as e:
        print(f"ERROR: Cannot reach GaggiMate at {HOST} ({e})", file=sys.stderr)
        print("Check that the machine is powered on and reachable on your network.", file=sys.stderr)
        sys.exit(1)
    except websockets.exceptions.WebSocketException as e:
        print(f"ERROR: WebSocket connection failed: {e}", file=sys.stderr)
        sys.exit(1)


async def list_profiles():
    result = await send_and_receive({"tp": "req:profiles:list"})
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    profiles = result.get("profiles", [])
    if not profiles:
        print("No profiles found.")
        return
    for p in profiles:
        fav = "★" if p.get("favorite") else " "
        sel = "→" if p.get("selected") else " "
        print(
            f"  {fav}{sel} {p.get('id', '?')[:8]}  {p.get('label', 'unnamed'):30s}  {p.get('type', '?'):8s}  {p.get('temperature', '?')}°C  {len(p.get('phases', []))} phases"
        )
    print(f"\n{len(profiles)} profile(s) total")


async def get_profile(profile_id: str):
    result = await send_and_receive({"tp": "req:profiles:load", "id": profile_id})
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    profile = result.get("profile", {})
    print(json.dumps(profile, indent=2))


async def save_profile(filepath: str) -> dict:
    with open(filepath) as f:
        profile = json.load(f)
    # Ensure it has an ID
    if not profile.get("id"):
        profile["id"] = str(uuid.uuid4())
    result = await send_and_receive({"tp": "req:profiles:save", "profile": profile})
    if result.get("error"):
        print(f"Error saving: {result['error']}", file=sys.stderr)
        sys.exit(1)
    saved = result.get("profile", profile)
    print(f"Saved: {saved.get('label', 'unnamed')} ({saved.get('id', '?')[:8]})")
    return saved


async def favorite_profile(profile_id: str):
    result = await send_and_receive({"tp": "req:profiles:favorite", "id": profile_id})
    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(f"Favorited: {profile_id[:8]}")


async def select_profile(profile_id: str):
    result = await send_and_receive({"tp": "req:profiles:select", "id": profile_id})
    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(f"Selected: {profile_id[:8]}")


async def delete_profile(profile_id: str):
    result = await send_and_receive({"tp": "req:profiles:delete", "id": profile_id})
    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(f"Deleted: {profile_id[:8]}")


async def push_profile(filepath: str):
    """Save, favorite, and select a profile in one go."""
    saved = await save_profile(filepath)
    pid = saved.get("id", "")
    if pid:
        await favorite_profile(pid)
        await select_profile(pid)
        print(f"\n✅ Profile '{saved.get('label', '')}' deployed and ready to brew!")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "list":
        asyncio.run(list_profiles())
    elif cmd == "get" and len(sys.argv) >= 3:
        asyncio.run(get_profile(sys.argv[2]))
    elif cmd == "save" and len(sys.argv) >= 3:
        asyncio.run(save_profile(sys.argv[2]))
    elif cmd == "favorite" and len(sys.argv) >= 3:
        asyncio.run(favorite_profile(sys.argv[2]))
    elif cmd == "select" and len(sys.argv) >= 3:
        asyncio.run(select_profile(sys.argv[2]))
    elif cmd == "delete" and len(sys.argv) >= 3:
        asyncio.run(delete_profile(sys.argv[2]))
    elif cmd == "push" and len(sys.argv) >= 3:
        asyncio.run(push_profile(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
