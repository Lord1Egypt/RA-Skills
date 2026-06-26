#!/usr/bin/env python3
"""
Dota 2 Stats Query Tool - Based on OpenDota API (Full Coverage)

Player Commands:
    python scripts/dota2_query.py search <player_name>           Search players by name
    python scripts/dota2_query.py player <account_id>            Player profile & win rate
    python scripts/dota2_query.py wl <account_id> [filters]      Win/Loss stats
    python scripts/dota2_query.py recent <account_id>            Recent ~20 matches
    python scripts/dota2_query.py matches <account_id> [filters] Full match history
    python scripts/dota2_query.py heroes <account_id> [--limit]  Hero usage stats
    python scripts/dota2_query.py peers <account_id> [--limit]   Frequent teammates
    python scripts/dota2_query.py totals <account_id> [filters]  Lifetime totals (kills, assists, etc.)
    python scripts/dota2_query.py counts <account_id>            Counts by category
    python scripts/dota2_query.py rankings <account_id>          Player hero rankings
    python scripts/dota2_query.py ratings <account_id>           Rank tier history
    python scripts/dota2_query.py refresh <account_id>           Refresh player data

Match Commands:
    python scripts/dota2_query.py match <match_id>               Single match detail

Hero Commands:
    python scripts/dota2_query.py hero_list                      All heroes
    python scripts/dota2_query.py hero_stats                     Global hero statistics
    python scripts/dota2_query.py hero_matchups <hero_id>        Hero matchup win rates
    python scripts/dota2_query.py hero_rankings <hero_id>        Top players for a hero
    python scripts/dota2_query.py benchmarks <hero_id>           Hero benchmarks

Global Commands:
    python scripts/dota2_query.py pro_players                    Pro player list
    python scripts/dota2_query.py pro_matches [--limit N]        Recent pro matches
    python scripts/dota2_query.py public_matches [--min_rank N]  Recent public matches
    python scripts/dota2_query.py live                           Live games
    python scripts/dota2_query.py teams [--limit N]              Team list
    python scripts/dota2_query.py team <team_id>                 Team detail & matches
    python scripts/dota2_query.py leagues                        League list
    python scripts/dota2_query.py constants <resource>           Game constants (heroes, items, etc.)
    python scripts/dota2_query.py find_matches [--teamA ids] [--teamB ids]  Find by hero combo

Filters (for wl/matches/totals/counts):
    --days N          Last N days
    --hero_id N       Specific hero
    --lobby_type N    Lobby type (7=Ranked)
    --game_mode N     Game mode
    --limit N         Limit results

Global:
    --lang zh|en      Output language (default: zh)
"""

import sys
import json
import os
import urllib.request
import urllib.parse
import urllib.error
import time
from datetime import datetime, timezone, timedelta

BASE_URL = "https://api.opendota.com/api"

# HTTP headers to avoid 403
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json; charset=utf-8"
}

# ──────────────────────────────────────────────
#  Load translation and hero data from JSON files
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


T = _load_json("translations.json")
C = _load_json("dota_constants.json")
HERO_ZH_NAMES = {int(k): v for k, v in _load_json("hero_zh_names.json").items()}

# Global language, set during startup
LANG = "zh"


def t(key, **kwargs):
    """Look up a translated string by key, with optional format args."""
    s = T[LANG].get(key, T["zh"].get(key, key))
    if kwargs:
        return s.format(**kwargs)
    return s


def get_rank_name(tier):
    """Get localized rank tier name."""
    name_key = f"rank_{tier}"
    if name_key in C[LANG]:
        return C[LANG][name_key]
    s = C[LANG].get("rank_unknown", C["zh"].get("rank_unknown", "Unknown({tier})"))
    return s.format(tier=tier)


def get_mode_name(mode_id):
    """Get localized game mode name. Falls back to zh if not found in current lang."""
    key = f"mode_{mode_id}"
    translated = C[LANG].get(key, C["zh"].get(key, key))
    return translated if translated != key else str(mode_id)


def get_lobby_name(lobby_id):
    """Get localized lobby type name. Falls back to zh if not found in current lang."""
    key = f"lobby_{lobby_id}"
    translated = C[LANG].get(key, C["zh"].get(key, key))
    return translated if translated != key else str(lobby_id)


def get_attr_name(attr):
    """Get localized attribute name. Falls back to zh if not found in current lang."""
    key = f"attr_{attr}"
    translated = C[LANG].get(key, C["zh"].get(key, key))
    return translated if translated != key else attr


def get_atk_name(atk_type):
    """Get localized attack type name."""
    if atk_type == "Melee":
        return C[LANG].get("atk_melee", C["zh"].get("atk_melee", "Melee"))
    return C[LANG].get("atk_ranged", C["zh"].get("atk_ranged", "Ranged"))


# ──────────────────────────────────────────────
#  API helpers
# ──────────────────────────────────────────────

_hero_cache = None


def _send_request(req, timeout=15):
    """Internal function to send request with retry logic for 429."""
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                time.sleep(2)
                continue
            print(f"{t('api_fail')} {e.code}", file=sys.stderr)
            if e.code == 404:
                print(f"   {t('not_found')}", file=sys.stderr)
            elif e.code == 429:
                print(f"   {t('rate_limit')}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"{t('network_error')} {e.reason}", file=sys.stderr)
            sys.exit(1)
        except TimeoutError as e:
            print(f"{t('timeout_error')} ({e})", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"{t('json_error')}: {e}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"{t('network_error')} {e}", file=sys.stderr)
            sys.exit(1)


def api_get(endpoint, params=None, timeout=15):
    """Send GET request to OpenDota API."""
    url = f"{BASE_URL}{endpoint}"
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url += "?" + urllib.parse.urlencode(filtered)

    req = urllib.request.Request(url, headers=REQUEST_HEADERS)
    return _send_request(req, timeout)


def api_post(endpoint):
    """Send POST request to OpenDota API."""
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method="POST", headers=REQUEST_HEADERS)
    return _send_request(req, 15)


def get_hero_map():
    """Get hero ID → name mapping (cached). Chinese names from HERO_ZH_NAMES, English from API/cache."""
    global _hero_cache
    if _hero_cache is not None:
        return _hero_cache

    cache_file = os.path.join(DATA_DIR, "hero_en_names.json")
    heroes_en = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                heroes_en = json.load(f)
        except Exception:
            pass

    if not heroes_en:
        heroes = api_get("/heroes")
        heroes_en = {str(h["id"]): h["localized_name"] for h in heroes}
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(heroes_en, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    if LANG == "zh":
        _hero_cache = {int(k): HERO_ZH_NAMES.get(int(k), v) for k, v in heroes_en.items()}
    else:
        _hero_cache = {int(k): v for k, v in heroes_en.items()}

    return _hero_cache


def format_duration(seconds):
    """Convert seconds to m:ss format."""
    return f"{seconds // 60}:{seconds % 60:02d}"


def format_time(unix_ts):
    """Convert Unix timestamp to readable date string (Local timezone)."""
    if not unix_ts:
        return t("unknown")
    dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc).astimezone()
    return dt.strftime("%Y-%m-%d %H:%M")


def format_time_ago(unix_ts):
    """Convert Unix timestamp to relative time string."""
    if not unix_ts:
        return t("unknown")
    now = time.time()
    diff = now - unix_ts
    if diff < 3600:
        return t("minutes_ago", n=int(diff / 60))
    elif diff < 86400:
        return t("hours_ago", n=int(diff / 3600))
    elif diff < 2592000:
        return t("days_ago", n=int(diff / 86400))
    elif diff < 31536000:
        return t("months_ago", n=int(diff / 2592000))
    else:
        return t("years_ago", n=int(diff / 31536000))


def is_win(player_slot, radiant_win):
    """Determine if the player won based on slot and radiant_win."""
    is_radiant = player_slot < 128
    return (is_radiant and radiant_win) or (not is_radiant and not radiant_win)


def decode_rank_tier(rank_tier):
    """Decode rank_tier integer to human-readable string with stars."""
    if not rank_tier:
        return t("uncalibrated")
    tier = rank_tier // 10
    stars = rank_tier % 10
    name = get_rank_name(tier)
    if tier == 8:
        return name
    return f"{name} {'*' * stars}" if stars else name


# ──────────────────────────────────────────────
#  Command handlers
# ──────────────────────────────────────────────

def cmd_search(args):
    """Search for players by name."""
    if not args:
        print(t("usage_search"))
        sys.exit(1)

    query = " ".join(args)
    print(t("search_waiting"))
    sys.stdout.flush()
    results = api_get("/search", {"q": query}, timeout=120)

    if not results:
        print(t("search_no_result", query=query))
        return

    print(f"\n{t('search_header', query=query, count=len(results))}\n")
    print(f"{t('search_col_id'):<15} {t('search_col_name'):<25} {t('search_col_last'):<20} {t('search_col_sim')}")
    print("-" * 75)
    for p in results[:15]:
        last_match = p.get("last_match_time", t("unknown"))
        if last_match and last_match != t("unknown"):
            last_match = last_match[:10]
        sim = f"{p.get('similarity', 0):.2f}"
        print(f"{p['account_id']:<15} {p.get('personaname', t('unknown')):<25} {last_match:<20} {sim}")


def cmd_player(args):
    """Get player profile info."""
    if not args:
        print(t("usage_player"))
        sys.exit(1)

    account_id = args[0]
    data = api_get(f"/players/{account_id}")
    wl = api_get(f"/players/{account_id}/wl")

    profile = data.get("profile", {})
    rank_tier = data.get("rank_tier")
    leaderboard_rank = data.get("leaderboard_rank")
    mmr = data.get("computed_mmr")

    total = wl["win"] + wl["lose"]
    winrate = (wl["win"] / total * 100) if total > 0 else 0

    print(f"\n{'='*50}")
    print(f"  {t('player_header')}")
    print(f"{'='*50}")
    print(f"  {t('player_name'):<12} {profile.get('personaname', t('unknown'))}")
    print(f"  {t('player_account_id'):<12} {profile.get('account_id', account_id)}")
    print(f"  {t('player_steam_id'):<12} {profile.get('steamid', t('unknown'))}")
    print(f"  {t('player_rank'):<12} {decode_rank_tier(rank_tier)}")
    if leaderboard_rank:
        print(f"  {t('player_leaderboard'):<12} #{leaderboard_rank}")
    if mmr:
        print(f"  {t('player_mmr'):<12} {mmr}")
    print(f"  {t('player_games'):<12} {total}")
    print(f"  {t('player_wl'):<12} {wl['win']}{t('win')} / {wl['lose']}{t('lose')}")
    print(f"  {t('player_winrate'):<12} {winrate:.1f}%")
    print(f"  {t('player_steam_url'):<12} {profile.get('profileurl', '-')}")
    print(f"{'='*50}")


def cmd_wl(args):
    """Get win/loss stats."""
    if not args:
        print(t("usage_wl"))
        sys.exit(1)

    account_id = args[0]
    params = parse_filters(args[1:])
    params["significant"] = "0"
    wl = api_get(f"/players/{account_id}/wl", params)
    total = wl["win"] + wl["lose"]
    winrate = (wl["win"] / total * 100) if total > 0 else 0

    filters = []
    if "date" in params:
        filters.append(t("wl_filter_days", days=params["date"]))
    if "hero_id" in params:
        hero_map = get_hero_map()
        hero_name = hero_map.get(int(params["hero_id"]), f"ID:{params['hero_id']}")
        filters.append(t("wl_filter_hero", hero=hero_name))
    if "lobby_type" in params:
        lt = get_lobby_name(int(params["lobby_type"]))
        filters.append(t("wl_filter_lobby", lobby=lt))

    filter_str = f"（{', '.join(filters)}）" if filters else ""

    print(f"\n  {t('wl_header')}{filter_str}")
    print(f"  {t('wl_wins')} {wl['win']}")
    print(f"  {t('wl_losses')} {wl['lose']}")
    print(f"  {t('wl_total')} {total}")
    print(f"  {t('wl_winrate')} {winrate:.1f}%")


def cmd_recent(args):
    """Get recent matches."""
    if not args:
        print(t("usage_recent"))
        sys.exit(1)

    account_id = args[0]
    hero_map = get_hero_map()
    matches = api_get(f"/players/{account_id}/recentMatches")

    if not matches:
        print(t("no_recent"))
        return

    print(f"\n  {t('recent_header', count=len(matches))}\n")
    print(f"  {t('matches_col_id'):<12} {t('recent_col_hero'):<14} {t('match_mode'):<10} {t('recent_col_result'):<6} {'K/D/A':<10} {t('recent_col_gpm'):<6} {t('recent_col_xpm'):<6} {t('recent_col_duration'):<8} {t('recent_col_date')}")
    print("  " + "-" * 98)

    wins = 0
    for m in matches:
        hero = hero_map.get(m.get("hero_id", 0), t("unknown"))
        won = is_win(m.get("player_slot", 0), m.get("radiant_win"))
        if won:
            wins += 1
        result = t("result_win") if won else t("result_lose")
        mid = str(m.get("match_id", ""))
        mode = get_mode_name(m.get("game_mode", 0))
        kda = f"{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}"
        gpm = str(m.get("gold_per_min", 0))
        xpm = str(m.get("xp_per_min", 0))
        duration = format_duration(m.get("duration", 0))
        date = format_time(m.get("start_time"))

        print(f"  {mid:<12} {hero:<14} {mode:<10} {result:<6} {kda:<10} {gpm:<6} {xpm:<6} {duration:<8} {date}")

    total = len(matches)
    print(f"\n  {t('recent_summary', total=total, wins=wins, losses=total - wins, wr=wins/total*100)}")


def cmd_matches(args):
    """Get match history with pagination and filters."""
    if not args:
        print(t("usage_matches"))
        sys.exit(1)

    account_id = args[0]
    params = parse_filters(args[1:])

    if "limit" not in params:
        params["limit"] = "20"

    params["significant"] = "0"
    hero_map = get_hero_map()
    matches = api_get(f"/players/{account_id}/matches", params)

    if not matches:
        print(t("no_matches"))
        return

    print(f"\n  {t('matches_header', count=len(matches))}\n")
    print(f"  {t('matches_col_id'):<12} {t('recent_col_hero'):<14} {t('match_mode'):<10} {t('recent_col_result'):<6} {'K/D/A':<10} {t('recent_col_duration'):<8} {t('recent_col_date')}")
    print("  " + "-" * 88)

    wins = 0
    for m in matches:
        hero = hero_map.get(m.get("hero_id", 0), t("unknown"))
        won = is_win(m.get("player_slot", 0), m.get("radiant_win"))
        if won:
            wins += 1
        result = t("result_win") if won else t("result_lose")
        mode = get_mode_name(m.get("game_mode", 0))
        kda = f"{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}"
        duration = format_duration(m.get("duration", 0))
        date = format_time(m.get("start_time"))

        print(f"  {str(m.get('match_id', '')):<12} {hero:<14} {mode:<10} {result:<6} {kda:<10} {duration:<8} {date}")

    total = len(matches)
    print(f"\n  {t('matches_summary', total=total, wins=wins, losses=total - wins, wr=wins/total*100)}")


def cmd_heroes(args):
    """Get hero usage stats for a player."""
    if not args:
        print(t("usage_heroes"))
        sys.exit(1)

    account_id = args[0]
    limit = 20

    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1

    hero_map = get_hero_map()
    hero_stats = api_get(f"/players/{account_id}/heroes", {"significant": "0"})

    hero_stats = [h for h in hero_stats if h.get("games", 0) > 0]
    hero_stats.sort(key=lambda x: x.get("games", 0), reverse=True)
    hero_stats = hero_stats[:limit]

    if not hero_stats:
        print(t("no_heroes"))
        return

    print(f"\n  {t('heroes_header', limit=min(limit, len(hero_stats)))}\n")
    print(f"  {t('heroes_col_hero'):<18} {t('heroes_col_games'):<8} {t('heroes_col_wins'):<8} {t('heroes_col_winrate'):<10} {t('heroes_col_last')}")
    print("  " + "-" * 65)

    for h in hero_stats:
        hero = hero_map.get(h.get("hero_id", 0), f"ID:{h.get('hero_id', '?')}")
        games = h.get("games", 0)
        win = h.get("win", 0)
        winrate = f"{win / games * 100:.1f}%" if games > 0 else t("n_a")
        last_played = format_time_ago(h.get("last_played"))

        print(f"  {hero:<18} {games:<8} {win:<8} {winrate:<10} {last_played}")


def cmd_match(args):
    """Get single match details."""
    if not args:
        print(t("usage_match"))
        sys.exit(1)

    match_id = args[0]
    hero_map = get_hero_map()
    data = api_get(f"/matches/{match_id}")

    radiant_win = data.get("radiant_win")
    duration = format_duration(data.get("duration", 0))
    start_time = format_time(data.get("start_time"))
    game_mode = get_mode_name(data.get("game_mode", 0))
    r_score = data.get("radiant_score", 0)
    d_score = data.get("dire_score", 0)

    print(f"\n{'='*80}")
    print(f"  {t('match_header')} {match_id}")
    print(f"{'='*80}")
    print(f"  {t('match_mode')}: {game_mode}   |   {t('match_duration')}: {duration}   |   {t('match_date')}: {start_time}")
    print(f"  {t('match_score')}: {t('match_team_radiant')} {r_score} - {d_score} {t('match_team_dire')}   |   {t('match_result_radiant') if radiant_win else t('match_result_dire')}")
    print()

    players = data.get("players", [])
    radiant = [p for p in players if p.get("player_slot", 128) < 128]
    dire = [p for p in players if p.get("player_slot", 0) >= 128]

    def print_team(team_name, team_players):
        print(f"  {'─'*38} {team_name} {'─'*38}")
        print(f"  {t('match_col_player'):<18} {t('heroes_col_hero'):<16} {'K/D/A':<10} {t('recent_col_gpm'):<6} {t('recent_col_xpm'):<6} {t('match_col_damage'):<8} {t('match_col_lh'):<6} {t('match_col_level')}")
        print(f"  {'-'*76}")
        for p in team_players:
            name = p.get("personaname") or t("match_anonymous")
            if len(name) > 15:
                name = name[:14] + "…"
            hero = hero_map.get(p.get("hero_id", 0), t("unknown"))
            kda = f"{p.get('kills', 0)}/{p.get('deaths', 0)}/{p.get('assists', 0)}"
            gpm = str(p.get("gold_per_min", 0))
            xpm = str(p.get("xp_per_min", 0))
            dmg = str(p.get("hero_damage", 0))
            lh = str(p.get("last_hits", 0))
            lvl = str(p.get("level", 0))
            print(f"  {name:<18} {hero:<16} {kda:<10} {gpm:<6} {xpm:<6} {dmg:<8} {lh:<6} {lvl}")
        print()

    print_team(t("match_team_radiant"), radiant)
    print_team(t("match_team_dire"), dire)


def cmd_peers(args):
    """Get frequent teammates."""
    if not args:
        print(t("usage_peers"))
        sys.exit(1)

    account_id = args[0]
    limit = 15

    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1

    peers = api_get(f"/players/{account_id}/peers", {"significant": "0"})
    peers = peers[:limit]

    if not peers:
        print(t("no_peers"))
        return

    print(f"\n  {t('peers_header', limit=min(limit, len(peers)))}\n")
    print(f"  {t('peers_col_name'):<20} {t('peers_col_games'):<10} {t('peers_col_wins'):<10} {t('peers_col_winrate'):<10} {t('peers_col_last')}")
    print("  " + "-" * 70)

    for p in peers:
        name = p.get("personaname") or t("match_anonymous")
        if len(name) > 17:
            name = name[:16] + "…"
        games = p.get("with_games", 0)
        win = p.get("with_win", 0)
        winrate = f"{win / games * 100:.1f}%" if games > 0 else t("n_a")
        last = format_time_ago(p.get("last_played"))

        print(f"  {name:<20} {games:<10} {win:<10} {winrate:<10} {last}")


def cmd_hero_list(args):
    """Get full hero list."""
    heroes = api_get("/heroes")
    heroes.sort(key=lambda x: x["id"])

    print(f"\n{t('herolist_header', count=len(heroes))}\n")
    print(f"  {t('herolist_col_id'):<6} {t('herolist_col_name'):<28} {t('herolist_col_attr'):<8} {t('herolist_col_atk'):<8} {t('herolist_col_roles')}")
    print("  " + "-" * 80)

    for h in heroes:
        roles = ", ".join(h.get("roles", []))
        attr = get_attr_name(h.get("primary_attr", ""))
        atk = get_atk_name(h.get("attack_type", ""))
        if LANG == "zh":
            name = HERO_ZH_NAMES.get(h["id"], h["localized_name"])
        else:
            name = h["localized_name"]
        print(f"  {h['id']:<6} {name:<28} {attr:<8} {atk:<8} {roles}")


def cmd_hero_stats(args):
    """Get global hero statistics."""
    heroes = api_get("/heroStats")
    heroes.sort(key=lambda x: x.get("id", 0))

    print(f"\n{t('herostats_header')}\n")
    print(f"  {t('herostats_col_id'):<5} {t('herostats_col_hero'):<24} {t('herostats_col_turbo_picks'):<12} {t('herostats_col_turbo_wins'):<12} {t('herostats_col_turbo_wr')}")
    print("  " + "-" * 65)

    for h in heroes:
        hid = h.get("id", 0)
        tp = h.get("turbo_picks", 0)
        tw = h.get("turbo_wins", 0)
        wr = f"{tw / tp * 100:.1f}%" if tp > 0 else t("n_a")
        if LANG == "zh":
            name = HERO_ZH_NAMES.get(hid, h.get("localized_name", t("unknown")))
        else:
            name = h.get("localized_name", t("unknown"))
        print(f"  {hid:<5} {name:<24} {tp:<12} {tw:<12} {wr}")


def cmd_refresh(args):
    """Refresh player match data."""
    if not args:
        print(t("usage_refresh"))
        sys.exit(1)

    account_id = args[0]
    result = api_post(f"/players/{account_id}/refresh")
    print(f"  {t('refresh_ok', aid=account_id)}")
    print(f"  {t('refresh_resp')} {json.dumps(result, ensure_ascii=False)}")


# ──────────────────────────────────────────────
#  New API endpoint commands
# ──────────────────────────────────────────────

def parse_filters(args):
    """Parse common filter args: --days, --hero_id, --lobby_type, --game_mode, --limit, --offset."""
    params = {}
    i = 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            params["date"] = args[i + 1]; i += 2
        elif args[i] == "--hero_id" and i + 1 < len(args):
            params["hero_id"] = args[i + 1]; i += 2
        elif args[i] == "--lobby_type" and i + 1 < len(args):
            params["lobby_type"] = args[i + 1]; i += 2
        elif args[i] == "--game_mode" and i + 1 < len(args):
            params["game_mode"] = args[i + 1]; i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            params["limit"] = args[i + 1]; i += 2
        elif args[i] == "--offset" and i + 1 < len(args):
            params["offset"] = args[i + 1]; i += 2
        elif args[i] == "--min_rank" and i + 1 < len(args):
            params["min_rank"] = args[i + 1]; i += 2
        elif args[i] == "--max_rank" and i + 1 < len(args):
            params["max_rank"] = args[i + 1]; i += 2
        elif args[i] == "--teamA" and i + 1 < len(args):
            params["teamA"] = args[i + 1]; i += 2
        elif args[i] == "--teamB" and i + 1 < len(args):
            params["teamB"] = args[i + 1]; i += 2
        else:
            i += 1
    return params


def cmd_totals(args):
    """GET /players/{account_id}/totals - Lifetime totals."""
    if not args:
        print(t("usage_totals")); sys.exit(1)
    account_id = args[0]
    params = parse_filters(args[1:])
    params["significant"] = "0"
    data = api_get(f"/players/{account_id}/totals", params)
    if not data:
        print(t("no_totals")); return
    print(f"\n  {t('totals_header', aid=account_id)}\n")
    print(f"  {t('col_field'):<20} {t('col_total'):<15} {t('col_games'):<10} {t('col_average')}")
    print("  " + "-" * 60)
    for item in data:
        field = item.get("field", "?")
        n = item.get("n", 0)
        s = item.get("sum", 0)
        avg = f"{s/n:.1f}" if n > 0 else t("n_a")
        print(f"  {field:<20} {s:<15.0f} {n:<10} {avg}")


def cmd_counts(args):
    """GET /players/{account_id}/counts - Counts by category."""
    if not args:
        print(t("usage_counts")); sys.exit(1)
    account_id = args[0]
    params = parse_filters(args[1:])
    params["significant"] = "0"
    data = api_get(f"/players/{account_id}/counts", params)
    if not data:
        print(t("no_counts")); return
    print(f"\n  {t('counts_header', aid=account_id)}\n")
    for category, values in data.items():
        print(f"  [{category}]")
        if isinstance(values, dict):
            for k, v in values.items():
                games = v.get("games", 0)
                win = v.get("win", 0)
                wr = f"{win/games*100:.1f}%" if games > 0 else "N/A"
                print(f"    {k}: {games} games, {win} wins ({wr})")
        print()


def cmd_rankings_player(args):
    """GET /players/{account_id}/rankings - Player hero rankings."""
    if not args:
        print(t("usage_rankings")); sys.exit(1)
    account_id = args[0]
    hero_map = get_hero_map()
    data = api_get(f"/players/{account_id}/rankings")
    if not data:
        print(t("no_rankings_data")); return
    data.sort(key=lambda x: x.get("percent_rank", 0), reverse=True)
    print(f"\n  {t('rankings_header', aid=account_id)}\n")
    print(f"  {t('heroes_col_hero'):<20} {t('col_percentile'):<15} {t('col_card')}")
    print("  " + "-" * 50)
    for item in data[:30]:
        hero = hero_map.get(item.get("hero_id", 0), "?")
        pct = f"{item.get('percent_rank', 0)*100:.1f}%"
        card = item.get("card", t("n_a"))
        print(f"  {hero:<20} {pct:<15} {card}")


def cmd_ratings(args):
    """GET /players/{account_id}/ratings - Rank tier history."""
    if not args:
        print(t("usage_ratings")); sys.exit(1)
    account_id = args[0]
    data = api_get(f"/players/{account_id}/ratings")
    if not data:
        print(t("no_ratings")); return
    print(f"\n  {t('ratings_header', aid=account_id)}\n")
    print(f"  {t('col_date'):<20} {t('col_rank_tier'):<15} {t('matches_col_id')}")
    print("  " + "-" * 55)
    for item in data[-20:]:
        date = format_time(item.get("time"))
        rank = decode_rank_tier(item.get("rank_tier"))
        mid = item.get("match_id", t("n_a"))
        print(f"  {date:<20} {rank:<15} {mid}")


def cmd_pro_players(args):
    """GET /proPlayers - List of pro players."""
    data = api_get("/proPlayers")
    if not data:
        print(t("no_pro_players")); return
    limit = 30
    p = parse_filters(args)
    if "limit" in p:
        limit = int(p["limit"])
    print(f"\n  {t('pro_players_header', n=min(limit, len(data)), total=len(data))}\n")
    print(f"  {t('col_name'):<20} {t('col_team'):<18} {t('col_country'):<8} {t('search_col_id')}")
    print("  " + "-" * 60)
    for player in data[:limit]:
        name = player.get("name") or player.get("personaname") or "?"
        team = player.get("team_name") or "-"
        country = player.get("country_code") or "?"
        aid = player.get("account_id", "?")
        print(f"  {name:<20} {team:<18} {country:<8} {aid}")


def cmd_pro_matches(args):
    """GET /proMatches - Recent pro matches."""
    params = parse_filters(args)
    # /proMatches only supports less_than_match_id according to api.json
    api_params = {k: v for k, v in params.items() if k in ["less_than_match_id"]}
    data = api_get("/proMatches", api_params)
    if not data:
        print(t("no_pro_matches")); return
    limit = int(params.get("limit", 20))
    print(f"\n  {t('pro_matches_header')}:\n")
    print(f"  {t('matches_col_id'):<14} {t('match_team_radiant'):<18} {t('match_team_dire'):<18} {t('col_score'):<10} {t('col_duration'):<10} {t('col_league')}")
    print("  " + "-" * 90)
    for m in data[:limit]:
        mid = m.get("match_id", "?")
        rname = (m.get("radiant_name") or "?")[:16]
        dname = (m.get("dire_name") or "?")[:16]
        score = f"{m.get('radiant_score',0)}-{m.get('dire_score',0)}"
        dur = format_duration(m.get("duration", 0))
        league = (m.get("league_name") or "?")[:20]
        print(f"  {mid:<14} {rname:<18} {dname:<18} {score:<10} {dur:<10} {league}")


def cmd_public_matches(args):
    """GET /publicMatches - Recent public matches."""
    params = parse_filters(args)
    # /publicMatches only supports less_than_match_id, min_rank, max_rank
    api_params = {k: v for k, v in params.items() if k in ["less_than_match_id", "min_rank", "max_rank"]}
    data = api_get("/publicMatches", api_params)
    if not data:
        print(t("no_public_matches")); return
    hero_map = get_hero_map()
    print(f"\n  {t('public_matches_header', n=len(data))}\n")
    print(f"  {t('matches_col_id'):<14} {t('col_avg_rank'):<10} {t('col_duration'):<10} {t('col_radiant_heroes')}")
    print("  " + "-" * 80)
    for m in data[:20]:
        mid = m.get("match_id", "?")
        rank = m.get("avg_rank_tier") or "?"
        dur = format_duration(m.get("duration", 0))
        r_heroes = ", ".join(hero_map.get(h, str(h)) for h in (m.get("radiant_team") or [])[:3])
        print(f"  {mid:<14} {str(rank):<10} {dur:<10} {r_heroes}")


def cmd_live(args):
    """GET /live - Currently ongoing live games."""
    data = api_get("/live")
    if not data:
        print(t("no_live")); return
    hero_map = get_hero_map()
    print(f"\n  {t('live_header', n=len(data))}\n")
    for i, game in enumerate(data[:15]):
        players = game.get("players", [])
        avg_mmr = game.get("average_mmr", "?")
        spectators = game.get("spectators", 0)
        gtime = max(0, game.get("game_time", 0))
        r_score = game.get("radiant_score", 0)
        d_score = game.get("dire_score", 0)
        r_team = game.get("team_name_radiant") or t("match_team_radiant")
        d_team = game.get("team_name_dire") or t("match_team_dire")
        print(f"  {t('live_game_line', n=i+1, mmr=avg_mmr, time=format_duration(gtime), r_score=r_score, d_score=d_score, spec=spectators)}")
        radiant = [p for p in players if p.get("team", 0) == 0]
        dire = [p for p in players if p.get("team", 0) == 1]
        r_heroes = ", ".join(hero_map.get(p.get("hero_id", 0), "?") for p in radiant[:5])
        d_heroes = ", ".join(hero_map.get(p.get("hero_id", 0), "?") for p in dire[:5])
        print(f"    {r_team}: {r_heroes}")
        print(f"    {d_team}: {d_heroes}")
        print()


def cmd_teams(args):
    """GET /teams - Team list."""
    params = parse_filters(args)
    # /teams only supports page according to api.json
    api_params = {k: v for k, v in params.items() if k in ["page"]}
    data = api_get("/teams", api_params)
    if not data:
        print(t("no_teams")); return
    limit = int(params.get("limit", 25))
    print(f"\n  {t('teams_header', n=limit)}\n")
    print(f"  {'ID':<10} {t('col_name'):<22} {t('col_tag'):<8} {t('col_rating'):<10} {t('win'):<6} {t('lose'):<6} {t('col_last_match')}")
    print("  " + "-" * 75)
    for team in data[:limit]:
        tid = team.get("team_id", "?")
        name = (team.get("name") or "?")[:20]
        tag = (team.get("tag") or "-")[:6]
        rating = f"{team.get('rating', 0):.0f}"
        wins = team.get("wins", 0)
        losses = team.get("losses", 0)
        last = format_time_ago(team.get("last_match_time"))
        print(f"  {tid:<10} {name:<22} {tag:<8} {rating:<10} {wins:<6} {losses:<6} {last}")


def cmd_team(args):
    """GET /teams/{team_id} + /teams/{team_id}/matches + /teams/{team_id}/players."""
    if not args:
        print(t("usage_team")); sys.exit(1)
    team_id = args[0]
    info = api_get(f"/teams/{team_id}")
    if not info:
        print(t("no_team")); return
    print(f"\n  {t('team_info', name=info.get('name', '?'), tag=info.get('tag', '?'))}")
    print(f"  {t('team_rating_wl', rating=info.get('rating', 0), wins=info.get('wins', 0), losses=info.get('losses', 0))}")
    # Players
    players = api_get(f"/teams/{team_id}/players")
    if players:
        player_list = players if isinstance(players, list) else [players] if isinstance(players, dict) else []
        current = [p for p in player_list if isinstance(p, dict) and p.get("is_current_team_member")]
        if current:
            print(f"\n  {t('team_roster')}:")
            for p in current:
                name = p.get("name") or "?"
                games = p.get("games_played", 0)
                wins = p.get("wins", 0)
                print(f"    {t('team_player_stats', name=name, games=games, wins=wins)}")
    # Recent matches
    matches = api_get(f"/teams/{team_id}/matches")
    if matches:
        print(f"\n  {t('team_recent_matches')}:")
        print(f"  {t('matches_col_id'):<14} {t('col_opponent'):<20} {t('col_result'):<8} {t('col_score'):<10} {t('col_duration')}")
        print("  " + "-" * 65)
        match_list = matches if isinstance(matches, list) else [matches] if isinstance(matches, dict) else []
        for m in match_list[:10]:
            if not isinstance(m, dict):
                continue
            mid = m.get("match_id", "?")
            opp = (m.get("opposing_team_name") or "?")[:18]
            is_rad = m.get("radiant")
            rw = m.get("radiant_win")
            won = (is_rad and rw) or (not is_rad and not rw) if rw is not None else None
            result = "✅ W" if won else ("❌ L" if won is not None else "?")
            score = f"{m.get('radiant_score',0)}-{m.get('dire_score',0)}"
            dur = format_duration(m.get("duration", 0))
            print(f"  {mid:<14} {opp:<20} {result:<8} {score:<10} {dur}")


def cmd_leagues(args):
    """GET /leagues - League list."""
    params = parse_filters(args)
    limit = int(params.get("limit", 30))
    data = api_get("/leagues")
    if not data:
        print(t("no_leagues")); return
    data.sort(key=lambda x: x.get("leagueid", 0), reverse=True)
    print(f"\n  {t('leagues_header', n=min(limit, len(data)), total=len(data))}\n")
    print(f"  {'ID':<10} {t('col_name'):<40} {t('col_tier')}")
    print("  " + "-" * 60)
    for lg in data[:limit]:
        lid = lg.get("leagueid", "?")
        name = (lg.get("name") or "?")[:38]
        tier = lg.get("tier") or "?"
        print(f"  {lid:<10} {name:<40} {tier}")


def cmd_hero_matchups(args):
    """GET /heroes/{hero_id}/matchups - Win rates against other heroes."""
    if not args:
        print(t("usage_hero_matchups")); sys.exit(1)
    hero_id = args[0]
    hero_map = get_hero_map()
    data = api_get(f"/heroes/{hero_id}/matchups")
    if not data:
        print(t("no_hero_matchups")); return
    hero_name = hero_map.get(int(hero_id), f"Hero {hero_id}")
    data.sort(key=lambda x: x.get("games_played", 0), reverse=True)
    print(f"\n  {t('hero_matchups_header', hero=hero_name)}\n")
    print(f"  {t('col_opponent'):<20} {t('col_games'):<10} {t('heroes_col_wins'):<10} {t('heroes_col_winrate')}")
    print("  " + "-" * 55)
    for m in data[:30]:
        opp = hero_map.get(m.get("hero_id", 0), "?")
        games = m.get("games_played", 0)
        wins = m.get("wins", 0)
        wr = f"{wins/games*100:.1f}%" if games > 0 else t("n_a")
        print(f"  {opp:<20} {games:<10} {wins:<10} {wr}")


def cmd_hero_rankings(args):
    """GET /rankings?hero_id={} - Top players for a hero."""
    if not args:
        print(t("usage_hero_rankings")); sys.exit(1)
    hero_id = args[0]
    hero_map = get_hero_map()
    data = api_get("/rankings", {"hero_id": hero_id})
    if not data:
        print(t("no_hero_rankings")); return
    hero_name = hero_map.get(int(hero_id), f"Hero {hero_id}")
    rankings = data.get("rankings", [])
    print(f"\n  {t('hero_rankings_header', hero=hero_name, n=min(20, len(rankings)))}\n")
    print(f"  {'#':<5} {t('col_player'):<25} {'Score':<12} {t('col_rank_tier')}")
    print("  " + "-" * 50)
    for i, r in enumerate(rankings[:20], 1):
        name = r.get("personaname") or "?"
        score = f"{r.get('score', 0):.2f}"
        rank = decode_rank_tier(r.get("rank_tier"))
        print(f"  {i:<5} {name[:23]:<25} {score:<12} {rank}")


def cmd_benchmarks(args):
    """GET /benchmarks?hero_id={} - Hero benchmarks."""
    if not args:
        print(t("usage_benchmarks")); sys.exit(1)
    hero_id = args[0]
    hero_map = get_hero_map()
    data = api_get("/benchmarks", {"hero_id": hero_id})
    if not data:
        print(t("no_benchmarks")); return
    hero_name = hero_map.get(int(hero_id), f"Hero {hero_id}")
    print(f"\n  {t('benchmarks_header', hero=hero_name)}\n")
    result = data.get("result", {})
    for stat_name, values in result.items():
        print(f"  [{stat_name}]")
        if isinstance(values, list):
            for v in values:
                pct = v.get("percentile", 0)
                val = v.get("value", 0)
                print(f"    {pct*100:5.0f}%ile: {val:.1f}")
        print()


def cmd_constants(args):
    """GET /constants/{resource} - Game constants."""
    if not args:
        print(t("usage_constants"))
        print(t("constants_usage_extra"))
        print(t("constants_usage_link"))
        sys.exit(1)
    resource = args[0]
    data = api_get(f"/constants/{resource}")
    if not data:
        print(t("no_constants", resource=resource)); return
    raw = json.dumps(data, indent=2, ensure_ascii=False)
    print(raw[:5000])
    if len(raw) > 5000:
        print(f"\n  ... {t('constants_truncated', n=len(raw))}")


def cmd_find_matches(args):
    """GET /findMatches - Find matches by hero combo."""
    params = parse_filters(args)
    qp = {}
    if "teamA" in params:
        qp["teamA"] = params["teamA"]
    if "teamB" in params:
        qp["teamB"] = params["teamB"]
    if not qp:
        print(t("usage_find_matches"))
        print("  Hero IDs separated by commas. Example: --teamA 11,74 --teamB 1,44")
        sys.exit(1)
    try:
        data = api_get("/findMatches", qp)
    except SystemExit:
        print(f"  {t('find_matches_note')}")
        return
    if not data:
        print(t("no_find_matches")); return
    print(f"\n  {t('find_matches_header', n=len(data))}\n")
    print(f"  {t('matches_col_id'):<14} {t('col_duration'):<10} {t('col_date')}")
    print("  " + "-" * 45)
    for m in data[:15]:
        mid = m.get("match_id", "?")
        dur = format_duration(m.get("duration", 0)) if m.get("duration") else "?"
        start = format_time(m.get("start_time")) if m.get("start_time") else "?"
        print(f"  {mid:<14} {dur:<10} {start}")


# ──────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────

def main():
    global LANG

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Extract --lang from anywhere in args
    raw_args = sys.argv[1:]
    filtered_args = []
    i = 0
    while i < len(raw_args):
        a = raw_args[i]
        if a in ("--lang", "-l"):
            i += 1
            if i < len(raw_args):
                LANG = raw_args[i] if raw_args[i] in ("zh", "en") else "zh"
            i += 1
            continue
        if a.startswith("--lang="):
            val = a.split("=", 1)[1]
            LANG = val if val in ("zh", "en") else "zh"
            i += 1
            continue
        if a.startswith("-l="):
            val = a.split("=", 1)[1]
            LANG = val if val in ("zh", "en") else "zh"
            i += 1
            continue
        filtered_args.append(a)
        i += 1

    if not filtered_args:
        print(__doc__)
        sys.exit(1)

    command = filtered_args[0]
    cmd_args = filtered_args[1:]

    # Auto-convert Steam64 ID to 32-bit Account ID
    if cmd_args:
        try:
            val = int(cmd_args[0])
            if val > 76561197960265728:
                cmd_args[0] = str(val - 76561197960265728)
        except ValueError:
            pass

    commands = {
        "search": cmd_search,
        "player": cmd_player,
        "wl": cmd_wl,
        "recent": cmd_recent,
        "matches": cmd_matches,
        "heroes": cmd_heroes,
        "match": cmd_match,
        "peers": cmd_peers,
        "hero_list": cmd_hero_list,
        "hero_stats": cmd_hero_stats,
        "refresh": cmd_refresh,
        # New commands
        "totals": cmd_totals,
        "counts": cmd_counts,
        "rankings": cmd_rankings_player,
        "ratings": cmd_ratings,
        "pro_players": cmd_pro_players,
        "pro_matches": cmd_pro_matches,
        "public_matches": cmd_public_matches,
        "live": cmd_live,
        "teams": cmd_teams,
        "team": cmd_team,
        "leagues": cmd_leagues,
        "hero_matchups": cmd_hero_matchups,
        "hero_rankings": cmd_hero_rankings,
        "benchmarks": cmd_benchmarks,
        "constants": cmd_constants,
        "find_matches": cmd_find_matches,
    }

    if command in ("--help", "-h", "help"):
        print(__doc__)
        sys.exit(0)

    if command not in commands:
        print(f"{t('unknown_cmd')} {command}")
        print(f"{t('available_cmds')} {', '.join(commands.keys())}")
        sys.exit(1)

    commands[command](cmd_args)


if __name__ == "__main__":
    main()
