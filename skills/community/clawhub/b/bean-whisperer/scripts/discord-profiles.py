#!/usr/bin/env python3
"""Fetch GaggiMate profiles from the Discord #profiles forum channel.

Usage:
  discord-profiles.py list [--limit N]              List recent profile threads
  discord-profiles.py search <query> [--limit N]    Search profiles by thread name
  discord-profiles.py download <thread-id>          Download profile JSONs from a thread
  discord-profiles.py download-all [--limit N]      Download all profile JSONs
  discord-profiles.py recommend <roast> [<origin>]  Find profiles matching bean characteristics

Environment:
  DISCORD_TOKEN    User token (required). Or store in ~/.config/gaggimate/discord-token
  PROFILES_DIR     Directory to save profiles (default: /tmp/gaggimate-profiles)

The GaggiMate Discord #profiles is a Forum Channel (type 15).
Each profile is a forum thread; JSON attachments are in thread messages.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import aiohttp

TOKEN_FILE = Path.home() / ".config" / "gaggimate" / "discord-token"
CHANNEL_ID = "1380352847387820082"
GUILD_ID = "951416527721230336"
PROFILES_DIR = Path(os.environ.get("PROFILES_DIR", "/tmp/gaggimate-profiles"))
API_BASE = "https://discord.com/api/v10"


def get_token() -> str:
    token = os.environ.get("DISCORD_TOKEN", "")
    if not token and TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text().strip()
    if not token:
        print(
            "ERROR: No Discord token. Set DISCORD_TOKEN or store in ~/.config/gaggimate/discord-token", file=sys.stderr
        )
        sys.exit(1)
    return token


HEADERS = {}


def init():
    global HEADERS
    token = get_token()
    HEADERS = {"Authorization": token}


class DiscordAPIError(Exception):
    def __init__(self, status, message=""):
        self.status = status
        super().__init__(f"Discord API {status}: {message}")


async def api_get(session: aiohttp.ClientSession, path: str) -> dict | list:
    url = f"{API_BASE}{path}"
    async with session.get(url, headers=HEADERS) as resp:
        if resp.status == 401:
            raise DiscordAPIError(401, "Invalid/expired Discord token")
        if resp.status == 403:
            raise DiscordAPIError(403, "No access")
        if resp.status == 429:
            retry = int(resp.headers.get("Retry-After", "5"))
            print(f"Rate limited, waiting {retry}s...", file=sys.stderr)
            await asyncio.sleep(retry)
            return await api_get(session, path)
        if resp.status != 200:
            raise DiscordAPIError(resp.status, await resp.text())
        return await resp.json()


async def fetch_forum_threads(session: aiohttp.ClientSession, limit: int = 100) -> list[dict]:
    """Fetch archived threads from the #profiles forum channel."""
    all_threads = []

    # Active threads — guild endpoint is bot-only, skip for user tokens
    try:
        data = await api_get(session, f"/guilds/{GUILD_ID}/threads/active")
        if isinstance(data, dict) and "threads" in data:
            active = [t for t in data["threads"] if t.get("parent_id") == CHANNEL_ID]
            all_threads.extend(active)
    except DiscordAPIError:
        pass  # User tokens can't access guild active threads — fine

    # Archived threads (paginated)
    before = None
    while len(all_threads) < limit:
        path = f"/channels/{CHANNEL_ID}/threads/archived/public?limit=50"
        if before:
            # Ensure proper ISO8601 format (fix space in timezone)
            ts = before.replace(" ", "+").replace("++", "+")
            path += f"&before={ts}"
        try:
            data = await api_get(session, path)
        except DiscordAPIError as e:
            if e.status == 400:
                break  # Pagination format issue, stop
            raise
        threads = data.get("threads", [])
        if not threads:
            break
        all_threads.extend(threads)
        if not data.get("has_more", False):
            break
        last = threads[-1].get("thread_metadata", {}).get("archive_timestamp")
        if last:
            before = last
        else:
            break

    return all_threads[:limit]


async def fetch_thread_attachments(session: aiohttp.ClientSession, thread_id: str) -> list[dict]:
    """Get JSON attachments from a forum thread, paginating through all messages."""
    attachments = []
    seen_ids: set[str] = set()

    def _collect(msg: dict) -> None:
        for a in msg.get("attachments", []):
            if a["filename"].endswith(".json") and a.get("size", 0) < 100000 and a["id"] not in seen_ids:
                seen_ids.add(a["id"])
                attachments.append(a)

    # Try OP message (thread_id == first message_id in forums)
    try:
        msg = await api_get(session, f"/channels/{thread_id}/messages/{thread_id}")
        _collect(msg)
    except Exception:
        pass

    # Paginate through all messages (100 per page, backwards using before=)
    before = None
    while True:
        path = f"/channels/{thread_id}/messages?limit=100"
        if before:
            path += f"&before={before}"
        msgs = await api_get(session, path)
        if not isinstance(msgs, list) or not msgs:
            break
        for msg in msgs:
            _collect(msg)
        if len(msgs) < 100:
            break
        before = msgs[-1]["id"]

    return attachments


async def download_attachment(url: str) -> dict | None:
    async with aiohttp.ClientSession() as session, session.get(url) as resp:
        if resp.status != 200:
            return None
        try:
            return json.loads(await resp.text())
        except Exception:
            return None


def summarize_profile(p: dict) -> str:
    label = p.get("label", "unnamed")
    ptype = p.get("type", "?")
    temp = p.get("temperature", "?")
    phases = p.get("phases", [])
    phase_chain = " → ".join(ph.get("name", "?") for ph in phases)
    return f'"{label}" | {ptype} | {temp}°C | {len(phases)} phases: {phase_chain}'


# ============================================================
# Commands
# ============================================================


async def cmd_list(limit: int = 50) -> None:
    async with aiohttp.ClientSession() as session:
        threads = await fetch_forum_threads(session, limit)

    for t in threads[:limit]:
        name = t.get("name", "?")[:65]
        msgs = t.get("message_count", "?")
        tid = t["id"]
        print(f"  {tid}  {name:67s}  msgs:{msgs}")

    print(f"\n{min(len(threads), limit)} thread(s)")


async def cmd_search(query: str, limit: int = 20) -> None:
    query_lower = query.lower()
    async with aiohttp.ClientSession() as session:
        threads = await fetch_forum_threads(session, 200)

    matches = [t for t in threads if query_lower in t.get("name", "").lower()]

    if not matches:
        print(f"No threads matching '{query}'")
        return

    for t in matches[:limit]:
        name = t.get("name", "?")[:65]
        msgs = t.get("message_count", "?")
        print(f"  {t['id']}  {name:67s}  msgs:{msgs}")

    print(f"\n{len(matches)} match(es) for '{query}'")


async def cmd_download(thread_id: str) -> None:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        atts = await fetch_thread_attachments(session, thread_id)

    if not atts:
        print("No JSON attachments found in this thread.")
        return

    for a in atts:
        profile = await download_attachment(a["url"])
        if profile:
            outpath = PROFILES_DIR / a["filename"]
            with open(outpath, "w") as f:
                json.dump(profile, f, indent=2)
            print(f"  ✅ {a['filename']}: {summarize_profile(profile)}")
            print(f"     → {outpath}")


async def cmd_download_all(limit: int = 50) -> None:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        threads = await fetch_forum_threads(session, limit * 2)

        count = 0
        for t in threads:
            if count >= limit:
                break
            atts = await fetch_thread_attachments(session, t["id"])
            for a in atts:
                if count >= limit:
                    break
                profile = await download_attachment(a["url"])
                if profile:
                    fname = a["filename"]
                    outpath = PROFILES_DIR / fname
                    if outpath.exists():
                        outpath = PROFILES_DIR / f"{outpath.stem}_{t['id'][:8]}{outpath.suffix}"
                    with open(outpath, "w") as f:
                        json.dump(profile, f, indent=2)
                    label = profile.get("label", "unnamed")
                    print(f'  ✅ {fname}: "{label}"')
                    count += 1
            # Rate limit protection
            await asyncio.sleep(0.5)

    print(f"\n{count} profile(s) downloaded to {PROFILES_DIR}")


async def cmd_recommend(roast: str, origin: str = "") -> None:
    roast_keywords = {
        "light": [
            "light",
            "nordic",
            "turbo",
            "bloom",
            "low contact",
            "geisha",
            "filter",
            "allonge",
            "allongé",
            "bright",
        ],
        "medium-light": ["medium", "lever", "bloom", "specialty", "balanced", "adaptive"],
        "medium": ["medium", "lever", "classic", "balanced", "contact", "18g"],
        "medium-dark": ["dark", "traditional", "italian", "declining", "9 bar", "nine bar", "londonium"],
        "dark": ["dark", "italian", "traditional", "crema", "ristretto", "9bar", "londonium", "old school"],
    }
    terms = roast_keywords.get(roast, [roast])

    async with aiohttp.ClientSession() as session:
        threads = await fetch_forum_threads(session, 200)

    scored = []
    for t in threads:
        name = t.get("name", "").lower()
        score = sum(1 for term in terms if term in name)
        if origin and origin.lower() in name:
            score += 2
        if score > 0:
            scored.append((score, t))

    scored.sort(key=lambda x: -x[0])

    if not scored:
        print(f"No threads matching roast='{roast}'" + (f" origin='{origin}'" if origin else ""))
        return

    print(f"Recommended for {roast} roast" + (f", {origin}" if origin else "") + ":\n")
    for score, t in scored[:10]:
        name = t.get("name", "?")[:65]
        print(f"  [{score}★] {t['id']}  {name}")

    print(f"\n{len(scored)} potential match(es)")


def main():
    init()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "list":
        limit = 50
        for i, arg in enumerate(sys.argv):
            if arg == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        asyncio.run(cmd_list(limit))

    elif cmd == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        limit = 20
        for i, arg in enumerate(sys.argv):
            if arg == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        asyncio.run(cmd_search(query, limit))

    elif cmd == "download" and len(sys.argv) >= 3:
        asyncio.run(cmd_download(sys.argv[2]))

    elif cmd == "download-all":
        limit = 50
        for i, arg in enumerate(sys.argv):
            if arg == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        asyncio.run(cmd_download_all(limit))

    elif cmd == "recommend" and len(sys.argv) >= 3:
        roast = sys.argv[2]
        origin = sys.argv[3] if len(sys.argv) > 3 else ""
        asyncio.run(cmd_recommend(roast, origin))

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
