#!/usr/bin/env python3
"""
5E CS2 Real-time Match Monitor (Generic Version)
Continuously polls specified players' latest matches,
automatically outputs detailed reports when new matches are detected.

Usage:
  python cs_monitor.py --players player1 player2        # Monitor specified players
  python cs_monitor.py --players player1 --interval 30  # 30s polling
  python cs_monitor.py --once --players player1 player2 # Query once
  python cs_monitor.py --reset                          # Reset monitoring state
"""

import asyncio
import argparse
import json
import os
import sys
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Set

import aiohttp

# ── Configuration ────────────────────────────────────
DEFAULT_INTERVAL = 60  # seconds
STATE_FILE = os.path.join(os.path.dirname(__file__), ".cs_monitor_state.json")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")

# ── Load Config File ─────────────────────────────────
def load_config():
    """Load config file if exists"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

CONFIG = load_config()
DEFAULT_PLAYERS = CONFIG.get("default_players", [])

# ── HTTP Headers ─────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Accept-Encoding": "gzip, deflate",
}

GATE_HEADERS = {
    **HEADERS,
    "Accept-Language": "zh-cn",
    "Origin": "https://arena-next.5eplaycdn.com",
    "Referer": "https://arena-next.5eplaycdn.com/",
    "Accept-Encoding": "gzip, deflate",
}


# ── Helpers ───────────────────────────────────────────
def _si(v) -> int:
    try: return int(v or 0)
    except: return 0

def _sf(v) -> float:
    try: return float(v or 0.0)
    except: return 0.0


# ── API ───────────────────────────────────────────────
async def search_player(s: aiohttp.ClientSession, name: str) -> Optional[str]:
    encoded = urllib.parse.quote(name.encode("utf-8"))
    h = {**HEADERS, "X-Requested-With": "XMLHttpRequest",
         "Referer": f"https://arena.5eplay.com/search?keywords={encoded}"}
    async with s.get("https://arena.5eplay.com/api/search/player/1/16",
                     params={"keywords": name}, headers=h) as r:
        d = await r.json()
        users = d.get("data", {}).get("user", {}).get("list", [])
        for u in users:
            if u.get("username") == name:
                return u.get("domain", "")
    return None


async def get_uuid(s: aiohttp.ClientSession, domain: str) -> Optional[str]:
    h = {**GATE_HEADERS, "Content-Type": "application/json"}
    async with s.post("https://gate.5eplay.com/userinterface/http/v1/userinterface/idTransfer",
                      json={"trans": {"domain": domain}}, headers=h) as r:
        d = await r.json()
        return d.get("data", {}).get("uuid", "") or None


async def get_match_ids(s: aiohttp.ClientSession, uuid: str) -> List[str]:
    url = f"https://gate.5eplay.com/crane/http/api/data/player_match?uuid={uuid}"
    async with s.get(url, headers=GATE_HEADERS) as r:
        d = await r.json()
        return [m["match_id"] for m in d.get("data", {}).get("match_data", []) if m.get("match_id")]


async def get_match_detail(s: aiohttp.ClientSession, match_id: str) -> Optional[dict]:
    url = f"https://gate.5eplay.com/crane/http/api/data/match/{match_id}"
    h = {**GATE_HEADERS, "Content-Type": "application/json"}
    async with s.get(url, headers=h) as r:
        d = await r.json()
        return d.get("data") or None


# ── Data Extraction ───────────────────────────────────
@dataclass
class PlayerMatchReport:
    """Player report for a single match"""
    player_name: str
    match_id: str
    map_name: str
    start_time: int
    duration_min: int
    # Score
    my_score: int
    enemy_score: int
    win: bool
    half_detail: str  # e.g. "T 6:9 / CT 7:4"
    # Core
    rating: float
    adr: float
    kast: float
    rws: float
    # KDA
    kill: int
    death: int
    assist: int
    headshot: int
    headshot_rate: float
    # First K/D
    first_kill: int
    first_death: int
    awp_kill: int
    # Multi-kills
    kill_3: int
    kill_4: int
    kill_5: int
    # Clutches
    clutches: str
    # Elo
    elo_change: float
    origin_elo: float
    level_name: str
    # MVP
    is_mvp: bool
    # Sides
    t_kill: int
    t_death: int
    t_rating: float
    ct_kill: int
    ct_death: int
    ct_rating: float
    # Utility
    flash_enemy: int
    flash_enemy_time: float
    flash_team: int
    throw_harm_enemy: float
    planted_bomb: int
    defused_bomb: int
    # Full 10-player data
    scoreboard: List[dict] = field(default_factory=list)


def extract_report(match_json: dict, player_name: str, match_id: str) -> Optional[PlayerMatchReport]:
    """Extract player report from match detail JSON"""
    main = match_json.get("main", {})

    # Find player
    target = None
    target_group = 0
    for gn, gk in [(1, "group_1"), (2, "group_2")]:
        for p in match_json.get(gk, []):
            uname = p.get("user_info", {}).get("user_data", {}).get("username", "")
            if uname == player_name:
                target = p
                target_group = gn
                break

    if not target:
        return None

    fight = target.get("fight", {})
    sts = target.get("sts", {})
    li = target.get("level_info", {})
    ft = target.get("fight_t", {})
    fc = target.get("fight_ct", {})

    start = _si(main.get("start_time"))
    end = _si(main.get("end_time"))
    kill = _si(fight.get("kill"))
    hs = _si(fight.get("headshot"))

    # Score & Half
    if target_group == 1:
        my_s, en_s = _si(main.get("group1_all_score")), _si(main.get("group2_all_score"))
        fh_s, sh_s = _si(main.get("group1_fh_score")), _si(main.get("group1_sh_score"))
        efh, esh = _si(main.get("group2_fh_score")), _si(main.get("group2_sh_score"))
        fh_side = main.get("group1_fh_role", "T")
    else:
        my_s, en_s = _si(main.get("group2_all_score")), _si(main.get("group1_all_score"))
        fh_s, sh_s = _si(main.get("group2_fh_score")), _si(main.get("group2_sh_score"))
        efh, esh = _si(main.get("group1_fh_score")), _si(main.get("group1_sh_score"))
        fh_side = "CT" if main.get("group1_fh_role") == "T" else "T"
    sh_side = "CT" if fh_side == "T" else "T"
    half_detail = f"{fh_side} {fh_s}:{efh} / {sh_side} {sh_s}:{esh}"

    # Clutches
    cl = []
    for n in [1, 2, 3, 4, 5]:
        v = _si(fight.get(f"end_1v{n}"))
        if v: cl.append(f"1v{n}×{v}")
    clutch_str = " ".join(cl) if cl else ""

    # Scoreboard
    scoreboard = []
    for gn, gk in [(1, "group_1"), (2, "group_2")]:
        for p in match_json.get(gk, []):
            pf = p.get("fight", {})
            un = p.get("user_info", {}).get("user_data", {}).get("username", "")
            pk = _si(pf.get("kill"))
            scoreboard.append({
                "name": un,
                "group": gn,
                "kill": pk,
                "death": _si(pf.get("death")),
                "assist": _si(pf.get("assist")),
                "rating": _sf(pf.get("rating2")),
                "adr": _sf(pf.get("adr")),
                "kast": _sf(pf.get("kast")),
                "hs_rate": _si(pf.get("headshot")) / pk * 100 if pk > 0 else 0,
                "first_kill": _si(pf.get("first_kill")),
                "first_death": _si(pf.get("first_death")),
                "awp_kill": _si(pf.get("awp_kill")),
                "is_mvp": bool(_si(pf.get("is_mvp"))),
            })

    return PlayerMatchReport(
        player_name=player_name, match_id=match_id,
        map_name=main.get("map_desc", "?"),
        start_time=start, duration_min=(end - start) // 60 if end > start else 0,
        my_score=my_s, enemy_score=en_s,
        win=bool(_si(fight.get("is_win"))),
        half_detail=half_detail,
        rating=_sf(fight.get("rating2")),
        adr=_sf(fight.get("adr")),
        kast=_sf(fight.get("kast")),
        rws=_sf(fight.get("rws")),
        kill=kill, death=_si(fight.get("death")),
        assist=_si(fight.get("assist")),
        headshot=hs, headshot_rate=hs / kill if kill > 0 else 0,
        first_kill=_si(fight.get("first_kill")),
        first_death=_si(fight.get("first_death")),
        awp_kill=_si(fight.get("awp_kill")),
        kill_3=_si(fight.get("kill_3")), kill_4=_si(fight.get("kill_4")),
        kill_5=_si(fight.get("kill_5")),
        clutches=clutch_str,
        elo_change=_sf(sts.get("change_elo")),
        origin_elo=_sf(sts.get("origin_elo")),
        level_name=li.get("level_name", "?"),
        is_mvp=bool(_si(fight.get("is_mvp"))),
        t_kill=_si(ft.get("kill")), t_death=_si(ft.get("death")),
        t_rating=_sf(ft.get("rating2")),
        ct_kill=_si(fc.get("kill")), ct_death=_si(fc.get("death")),
        ct_rating=_sf(fc.get("rating2")),
        flash_enemy=_si(fight.get("flash_enemy")),
        flash_enemy_time=_sf(fight.get("flash_enemy_time")),
        flash_team=_si(fight.get("flash_team")),
        throw_harm_enemy=_sf(fight.get("throw_harm_enemy")),
        planted_bomb=_si(fight.get("planted_bomb")),
        defused_bomb=_si(fight.get("defused_bomb")),
        scoreboard=scoreboard,
    )


# ── Report Formatting ────────────────────────────────
def _bar(val: float, mx: float, w: int = 12) -> str:
    filled = int(min(val / mx, 1.0) * w) if mx > 0 else 0
    return "█" * filled + "░" * (w - filled)


def format_report(r: PlayerMatchReport) -> str:
    """Format single player single match report"""
    result_emoji = "🏆" if r.win else "💀"
    elo_str = f"+{r.elo_change:.1f}" if r.elo_change >= 0 else f"{r.elo_change:.1f}"
    kd_ratio = f"{r.kill / r.death:.2f}" if r.death > 0 else "∞"
    mvp_str = " ⭐MVP" if r.is_mvp else ""
    dt_str = datetime.fromtimestamp(r.start_time).strftime("%m-%d %H:%M") if r.start_time else "?"

    multikills = []
    if r.kill_3: multikills.append(f"3K×{r.kill_3}")
    if r.kill_4: multikills.append(f"4K×{r.kill_4}")
    if r.kill_5: multikills.append(f"ACE×{r.kill_5}")

    lines = [
        f"┌─── {r.player_name}{mvp_str}  |  {r.map_name}  |  {dt_str} ───",
        f"│ {result_emoji} {r.my_score}:{r.enemy_score}  ({r.half_detail})  Elo {elo_str} ({r.level_name})",
        f"│",
        f"│ Rating {r.rating:.2f} {_bar(r.rating, 2.0)}  ADR {r.adr:.1f}  KAST {r.kast*100:.0f}%  RWS {r.rws:.2f}",
        f"│ K/D/A {r.kill}/{r.death}/{r.assist} ({kd_ratio})  🎯 HS {r.headshot_rate*100:.0f}%  🔭 AWP {r.awp_kill}",
        f"│ FK {r.first_kill} FD {r.first_death}  T:{r.t_kill}K/{r.t_death}D({r.t_rating:.2f})  CT:{r.ct_kill}K/{r.ct_death}D({r.ct_rating:.2f})",
    ]

    extras = []
    if multikills: extras.append("✨ " + " ".join(multikills))
    if r.clutches: extras.append("🎪 " + r.clutches)
    if extras:
        lines.append(f"│ {' | '.join(extras)}")

    if r.flash_enemy or r.throw_harm_enemy or r.planted_bomb or r.defused_bomb:
        parts = []
        if r.flash_enemy: parts.append(f"Flash×{r.flash_enemy}({r.flash_enemy_time:.1f}s)")
        if r.flash_team: parts.append(f"TeamFlash×{r.flash_team}")
        if r.throw_harm_enemy: parts.append(f"UtilDmg{r.throw_harm_enemy:.0f}")
        if r.planted_bomb: parts.append(f"Plants×{r.planted_bomb}")
        if r.defused_bomb: parts.append(f"Defuses×{r.defused_bomb}")
        lines.append(f"│ 💣 {' '.join(parts)}")

    lines.append(f"└{'─' * 60}")
    return "\n".join(lines)


def format_scoreboard_compact(reports: List[PlayerMatchReport]) -> str:
    """Output compact scoreboard when multiple players in same match"""
    if not reports:
        return ""
    sb = reports[0].scoreboard
    if not sb:
        return ""
    tracked = {r.player_name for r in reports}
    lines = [f"  {'Player':<14} {'K':>3} {'D':>3} {'A':>3} {'Rating':>7} {'ADR':>6} {'HS%':>5} {'AWP':>3}"]
    lines.append(f"  {'─' * 52}")
    for gn in [1, 2]:
        group = sorted([p for p in sb if p["group"] == gn], key=lambda x: x["rating"], reverse=True)
        for p in group:
            marker = "→" if p["name"] in tracked else " "
            mvp = "★" if p["is_mvp"] else " "
            lines.append(f"{marker}{mvp}{p['name']:<13} {p['kill']:>3} {p['death']:>3} {p['assist']:>3} "
                         f"{p['rating']:>7.2f} {p['adr']:>6.1f} {p['hs_rate']:>4.0f}% {p['awp_kill']:>3}")
        if gn == 1:
            lines.append(f"  {'─' * 52}")
    return "\n".join(lines)


def format_match_group_report(match_id: str, reports: List[PlayerMatchReport]) -> str:
    """Merge report for all tracked players in same match"""
    parts = []
    # Match header
    r0 = reports[0]
    dt_str = datetime.fromtimestamp(r0.start_time).strftime("%Y-%m-%d %H:%M") if r0.start_time else "?"
    emoji = "🏆" if any(r.win for r in reports) else "💀"
    parts.append(f"\n{'═' * 65}")
    parts.append(f"🎮 {r0.map_name}  |  {dt_str}  |  {r0.duration_min}min  {emoji}")
    parts.append(f"{'═' * 65}")

    # Player reports
    for r in sorted(reports, key=lambda x: x.rating, reverse=True):
        parts.append(format_report(r))

    # Shared scoreboard
    parts.append("")
    parts.append(format_scoreboard_compact(reports))

    return "\n".join(parts)


# ── State Management ──────────────────────────────────
def load_state() -> Dict[str, str]:
    """Load known latest match_id"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: Dict[str, str]):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Player Resolution ────────────────────────────────
async def resolve_players(s: aiohttp.ClientSession, names: List[str]) -> Dict[str, str]:
    """Batch resolve player_name -> uuid"""
    result = {}
    for name in names:
        domain = await search_player(s, name)
        if not domain:
            print(f"⚠️  Player not found: {name}")
            continue
        uuid = await get_uuid(s, domain)
        if uuid:
            result[name] = uuid
            print(f"  ✓ {name} → {uuid[:12]}...")
        else:
            print(f"⚠️  {name}: Failed to get UUID")
    return result


# ── Core Monitor Logic ───────────────────────────────
async def check_new_matches(
    s: aiohttp.ClientSession,
    player_uuids: Dict[str, str],
    known_ids: Dict[str, str],
) -> List[str]:
    """
    Check latest matches for all players.
    Returns list of newly discovered match_ids.
    """
    new_match_ids: Set[str] = set()

    for name, uuid in player_uuids.items():
        try:
            ids = await get_match_ids(s, uuid)
            if ids:
                latest = ids[0]
                prev = known_ids.get(name)
                if prev != latest:
                    known_ids[name] = latest
                    if prev is not None:  # Not first time, new match detected
                        # Find all new match_ids
                        for mid in ids:
                            if mid == prev:
                                break
                            new_match_ids.add(mid)
                    else:
                        # First run, mark latest
                        new_match_ids.add(latest)
        except Exception as e:
            print(f"⚠️  Query {name} failed: {e}")

    return list(new_match_ids)


async def generate_reports(
    s: aiohttp.ClientSession,
    match_ids: List[str],
    player_names: List[str],
) -> str:
    """Generate reports for each new match"""
    output_parts = []

    for mid in match_ids:
        detail = await get_match_detail(s, mid)
        if not detail:
            continue

        # Find all tracked players in this match
        reports = []
        for name in player_names:
            r = extract_report(detail, name, mid)
            if r:
                reports.append(r)

        if reports:
            output_parts.append(format_match_group_report(mid, reports))

    return "\n".join(output_parts)


# ── Main Loops ───────────────────────────────────────
async def run_once(players: List[str]):
    """Query all players' latest matches once, detect new matches and output"""
    if not players:
        print("❌ No players specified. Use --players or set default players in config.json")
        return
        
    print(f"🔍 Querying players: {', '.join(players)}\n")
    
    state = load_state()
    
    async with aiohttp.ClientSession() as s:
        uuids = await resolve_players(s, players)
        if not uuids:
            print("❌ No valid players available")
            return

        # Get current latest match IDs
        current_ids: Dict[str, str] = {}
        for name, uuid in uuids.items():
            ids = await get_match_ids(s, uuid)
            if ids:
                current_ids[name] = ids[0]

        # Detect new matches (compare with state file)
        new_matches = []
        for name, mid in current_ids.items():
            if name not in state or state[name] != mid:
                new_matches.append(mid)
                state[name] = mid

        if new_matches:
            print(f"🆕 Detected {len(new_matches)} new matches!\n")
            report = await generate_reports(s, new_matches, players)
            print(report)
            save_state(state)  # Save new state
        else:
            print("📭 No new matches")
            
        # First run init state
        if not any(name in state for name in uuids):
            for name, mid in current_ids.items():
                state[name] = mid
            save_state(state)
            print("\n✅ Monitoring state initialized")


async def run_monitor(players: List[str], interval: int):
    """Continuous monitoring loop"""
    if not players:
        print("❌ No players specified. Use --players or set default players in config.json")
        return
        
    print(f"🔄 Starting real-time monitoring")
    print(f"   Players: {', '.join(players)}")
    print(f"   Polling interval: {interval}s")
    print(f"   Ctrl+C to exit\n")

    state = load_state()

    async with aiohttp.ClientSession() as s:
        # Resolve player UUIDs
        uuids = await resolve_players(s, players)
        if not uuids:
            print("❌ No valid players available")
            return

        # Init state (first run record current latest, no report)
        first_run = not any(name in state for name in uuids)
        if first_run:
            print("\n📋 Initializing: recording current latest match state...")
            for name, uuid in uuids.items():
                ids = await get_match_ids(s, uuid)
                if ids:
                    state[name] = ids[0]
            save_state(state)
            print("✅ Initialization complete. Will monitor for new matches.\n")

        poll_count = 0
        while True:
            try:
                poll_count += 1
                now = datetime.now().strftime("%H:%M:%S")

                new_ids = await check_new_matches(s, uuids, state)

                if new_ids:
                    save_state(state)
                    print(f"\n🆕 [{now}] Detected {len(new_ids)} new matches!")
                    report = await generate_reports(s, new_ids, players)
                    print(report)
                    print(f"\n{'─' * 65}")
                    print(f"⏳ Continuing monitoring... (every {interval}s)")
                else:
                    if poll_count % 10 == 1:  # Heartbeat every 10 polls
                        print(f"⏳ [{now}] No new matches (checked {poll_count} times)")

                await asyncio.sleep(interval)

            except KeyboardInterrupt:
                print("\n\n👋 Monitoring stopped")
                save_state(state)
                break
            except Exception as e:
                print(f"⚠️  [{now}] Poll error: {e}, retry in {interval}s...")
                await asyncio.sleep(interval)


# ── CLI ───────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="5E CS2 Real-time Match Monitor")
    parser.add_argument("--players", nargs="+", default=None,
                        help="List of players to monitor (space-separated)")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL,
                        help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")
    parser.add_argument("--once", action="store_true",
                        help="Query once only, no continuous monitoring")
    parser.add_argument("--reset", action="store_true",
                        help="Reset monitoring state")
    args = parser.parse_args()
    
    # Determine player list: CLI > Config > Error
    players = args.players if args.players else DEFAULT_PLAYERS

    if args.reset:
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
            print("✅ Monitoring state reset")
        else:
            print("ℹ️  No state to reset")
        return

    if args.once:
        asyncio.run(run_once(players))
    else:
        asyncio.run(run_monitor(players, args.interval))


if __name__ == "__main__":
    main()
