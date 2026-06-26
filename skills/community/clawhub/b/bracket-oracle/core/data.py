"""
Bracket Oracle — Data Ingestion

Scrapers for Bart Torvik (free), KenPom (premium), ESPN public picks.
"""

import csv
import json
import os
import re
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Optional

import requests

from .models import Team, TeamRatings, Region

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


# ─── Bart Torvik (FREE) ─────────────────────────────────────────────

TORVIK_JSON_URL = "https://barttorvik.com/{year}_team_results.json"

# Field indices in Torvik JSON arrays
TORVIK_FIELDS = {
    "rank": 0,
    "team": 1,
    "conf": 2,
    "record": 3,
    "adj_oe": 4,        # Adjusted Offensive Efficiency
    "adj_oe_rank": 5,
    "adj_de": 6,         # Adjusted Defensive Efficiency
    "adj_de_rank": 7,
    "barthag": 8,        # Win probability vs avg D1 team
    "barthag_rank": 9,
    "wab": 10,           # Wins Above Bubble
    "conf_record": 14,
    # Four Factors (offense)
    "efg_o": 15,         # Effective FG% (offense)
    "to_o": 16,          # Turnover rate (offense)
    "or_pct": 17,        # Offensive rebounding %
    "ftr_o": 18,         # Free throw rate (offense)
    # Four Factors (defense)
    "efg_d": 19,
    "to_d": 20,
    "dr_pct": 21,
    "ftr_d": 22,
    # Raw efficiencies
    "raw_oe": 23,
    "raw_de": 24,
    # Additional adjusted metrics
    "adj_oe_home": 25,
    "adj_de_home": 26,
    "adj_oe_away": 27,
    "adj_de_away": 28,
    "adj_oe_neutral": 29,
    "adj_de_neutral": 30,
    # More
    "barthag_away": 31,
    "adj_tempo": 32,
    "luck": 33,
    "sos": 41,           # Strength of schedule (via adj_em rank)
}


def fetch_torvik_ratings(year: int = 2026, force: bool = False) -> list[dict]:
    """
    Fetch team ratings from Bart Torvik T-Rank via JSON endpoint.
    Returns list of dicts with team stats.
    """
    cache_file = DATA_DIR / f"torvik_{year}.json"
    
    if cache_file.exists() and not force:
        age_hours = (datetime.now().timestamp() - cache_file.stat().st_mtime) / 3600
        if age_hours < 12:  # Cache for 12 hours
            with open(cache_file) as f:
                return json.load(f)
    
    url = TORVIK_JSON_URL.format(year=year)
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BracketOracle/1.0)",
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        
        raw = json.loads(resp.text)
        teams = _parse_torvik_json(raw)
        
        with open(cache_file, "w") as f:
            json.dump(teams, f, indent=2)
        
        return teams
    except Exception as e:
        print(f"[torvik] JSON fetch failed: {e}")
        return []


def _parse_torvik_json(raw_data: list) -> list[dict]:
    """Parse Torvik JSON array format into named dicts."""
    teams = []
    
    for entry in raw_data:
        if not isinstance(entry, list) or len(entry) < 10:
            continue
        
        def safe_val(idx, default=None):
            try:
                return entry[idx] if idx < len(entry) else default
            except (IndexError, TypeError):
                return default
        
        team = {
            "rank": safe_val(TORVIK_FIELDS["rank"]),
            "team": safe_val(TORVIK_FIELDS["team"]),
            "conf": safe_val(TORVIK_FIELDS["conf"]),
            "record": safe_val(TORVIK_FIELDS["record"]),
            "adj_oe": safe_val(TORVIK_FIELDS["adj_oe"]),
            "adj_oe_rank": safe_val(TORVIK_FIELDS["adj_oe_rank"]),
            "adj_de": safe_val(TORVIK_FIELDS["adj_de"]),
            "adj_de_rank": safe_val(TORVIK_FIELDS["adj_de_rank"]),
            "barthag": safe_val(TORVIK_FIELDS["barthag"]),
            "barthag_rank": safe_val(TORVIK_FIELDS["barthag_rank"]),
            "wab": safe_val(TORVIK_FIELDS["wab"]),
            "conf_record": safe_val(TORVIK_FIELDS["conf_record"]),
            "efg_o": safe_val(TORVIK_FIELDS["efg_o"]),
            "to_o": safe_val(TORVIK_FIELDS["to_o"]),
            "or_pct": safe_val(TORVIK_FIELDS["or_pct"]),
            "ftr_o": safe_val(TORVIK_FIELDS["ftr_o"]),
            "efg_d": safe_val(TORVIK_FIELDS["efg_d"]),
            "to_d": safe_val(TORVIK_FIELDS["to_d"]),
            "dr_pct": safe_val(TORVIK_FIELDS["dr_pct"]),
            "ftr_d": safe_val(TORVIK_FIELDS["ftr_d"]),
            "adj_tempo": safe_val(TORVIK_FIELDS["adj_tempo"]),
            "luck": safe_val(TORVIK_FIELDS["luck"]),
        }
        
        # Compute adj_em from adj_oe - adj_de
        if team["adj_oe"] and team["adj_de"]:
            try:
                team["adj_em"] = float(team["adj_oe"]) - float(team["adj_de"])
            except (ValueError, TypeError):
                team["adj_em"] = 0.0
        
        teams.append(team)
    
    return teams


def torvik_to_team_ratings(torvik_data: dict) -> TeamRatings:
    """Convert a Torvik data dict to TeamRatings."""
    def safe_float(val, default=0.0):
        try:
            return float(val) if val is not None else default
        except (ValueError, TypeError):
            return default
    
    return TeamRatings(
        adj_em=safe_float(torvik_data.get("adj_em")),
        adj_o=safe_float(torvik_data.get("adj_oe")),
        adj_d=safe_float(torvik_data.get("adj_de")),
        adj_tempo=safe_float(torvik_data.get("adj_tempo")),
        sos=safe_float(torvik_data.get("wab")),  # WAB as SOS proxy
        luck=safe_float(torvik_data.get("luck")),
        source="torvik",
    )


# ─── KenPom (PREMIUM — optional) ────────────────────────────────────

def fetch_kenpom_ratings(
    email: Optional[str] = None,
    password: Optional[str] = None,
    year: int = 2026,
    force: bool = False,
) -> list[dict]:
    """
    Fetch team ratings from KenPom (requires subscription).
    
    Credentials can be passed directly or set as env vars:
        KENPOM_EMAIL, KENPOM_PASSWORD
    """
    email = email or os.environ.get("KENPOM_EMAIL")
    password = password or os.environ.get("KENPOM_PASSWORD")
    
    if not email or not password:
        print("[kenpom] No credentials. Use Torvik (free) or set KENPOM_EMAIL/KENPOM_PASSWORD.")
        return []
    
    cache_file = DATA_DIR / f"kenpom_{year}.json"
    
    if cache_file.exists() and not force:
        age_hours = (datetime.now().timestamp() - cache_file.stat().st_mtime) / 3600
        if age_hours < 12:
            with open(cache_file) as f:
                return json.load(f)
    
    try:
        from kenpompy.utils import login
        import kenpompy.summary as kp
        
        browser = login(email, password)
        df = kp.get_efficiency(browser, season=str(year))
        
        teams = df.to_dict("records")
        
        with open(cache_file, "w") as f:
            json.dump(teams, f, indent=2, default=str)
        
        return teams
    except ImportError:
        print("[kenpom] kenpompy not installed. Run: pip install kenpompy")
        return []
    except Exception as e:
        print(f"[kenpom] Fetch failed: {e}")
        return []


def kenpom_to_team_ratings(kenpom_data: dict) -> TeamRatings:
    """Convert a KenPom data dict to TeamRatings."""
    def safe_float(val, default=0.0):
        try:
            return float(val) if val else default
        except (ValueError, TypeError):
            return default
    
    return TeamRatings(
        adj_em=safe_float(kenpom_data.get("AdjEM", kenpom_data.get("adj_em", 0))),
        adj_o=safe_float(kenpom_data.get("AdjO", kenpom_data.get("adj_o", 0))),
        adj_d=safe_float(kenpom_data.get("AdjD", kenpom_data.get("adj_d", 0))),
        adj_tempo=safe_float(kenpom_data.get("AdjT", kenpom_data.get("adj_tempo", 0))),
        sos=safe_float(kenpom_data.get("SOS AdjEM", None)),
        luck=safe_float(kenpom_data.get("Luck", None)),
        source="kenpom",
    )


# ─── ESPN Public Pick Percentages ────────────────────────────────────

ESPN_PICKS_URL = "https://fantasy.espn.com/tournament-challenge-bracket/2026/en/whopickedwhom"


def fetch_espn_public_picks(year: int = 2026, force: bool = False) -> dict[str, list[float]]:
    """
    Fetch ESPN 'Who Picked Whom' data.
    Returns dict of team_name -> [R1%, R2%, R3%, R4%, R5%, R6%]
    
    NOTE: This data is only available after brackets are released
    and people start filling them out (after Selection Sunday).
    """
    cache_file = DATA_DIR / f"espn_picks_{year}.json"
    
    if cache_file.exists() and not force:
        age_hours = (datetime.now().timestamp() - cache_file.stat().st_mtime) / 3600
        if age_hours < 4:  # Refresh more often during bracket filling period
            with open(cache_file) as f:
                return json.load(f)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BracketOracle/1.0)",
    }
    
    try:
        resp = requests.get(ESPN_PICKS_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        
        picks = _parse_espn_picks(resp.text)
        
        if picks:
            with open(cache_file, "w") as f:
                json.dump(picks, f, indent=2)
        
        return picks
    except Exception as e:
        print(f"[espn] Public picks fetch failed: {e}")
        return {}


def _parse_espn_picks(html: str) -> dict[str, list[float]]:
    """Parse ESPN Who Picked Whom page."""
    # ESPN renders this with JavaScript — may need browser scraping
    # For now, return empty and we'll implement with Scrapling/browser when needed
    picks = {}
    
    # Try to find JSON data embedded in the page
    json_match = re.search(r'window\.__espnfitt__\s*=\s*(\{.*?\});', html, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            # Parse the structure — ESPN changes this frequently
            # Will need to adapt when we see actual 2026 data
            return _extract_picks_from_espn_json(data)
        except json.JSONDecodeError:
            pass
    
    return picks


def _extract_picks_from_espn_json(data: dict) -> dict[str, list[float]]:
    """Extract pick percentages from ESPN JSON data."""
    picks = {}
    # Structure varies by year — implement when we see 2026 data
    return picks


# ─── Combined Data Pipeline ─────────────────────────────────────────

def get_team_ratings(
    year: int = 2026,
    source: str = "auto",
    kenpom_email: Optional[str] = None,
    kenpom_password: Optional[str] = None,
    force_refresh: bool = False,
) -> list[dict]:
    """
    Get team ratings from best available source.
    
    source:
        "auto" — Try KenPom first (if credentials), fall back to Torvik
        "torvik" — Bart Torvik only (free)
        "kenpom" — KenPom only (requires subscription)
    """
    if source == "kenpom" or (source == "auto" and (kenpom_email or os.environ.get("KENPOM_EMAIL"))):
        data = fetch_kenpom_ratings(kenpom_email, kenpom_password, year, force_refresh)
        if data:
            return data
        if source == "kenpom":
            print("[data] KenPom fetch failed, no fallback requested.")
            return []
    
    return fetch_torvik_ratings(year, force_refresh)


def build_team_lookup(ratings_data: list[dict], source: str = "torvik") -> dict[str, TeamRatings]:
    """Build a team_name -> TeamRatings lookup from raw data."""
    converter = torvik_to_team_ratings if source == "torvik" else kenpom_to_team_ratings
    lookup = {}
    
    for entry in ratings_data:
        name = entry.get("team", entry.get("Team", entry.get("TeamName", "")))
        if name:
            lookup[name] = converter(entry)
    
    return lookup
