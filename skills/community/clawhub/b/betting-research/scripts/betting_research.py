#!/usr/bin/env python3
"""
Betting Research Skill - Multi-source data aggregator for sports predictions.
"""

import json
import requests
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Config paths
APIFOOTBALL_KEY = os.getenv('APIFOOTBALL_KEY', '')
ODDS_API_KEY = os.getenv('ODDS_API_KEY', '')

THE_SPORTS_DB_BASE = "https://www.thesportsdb.com/api/v1/json/3"
APIFOOTBALL_BASE = "https://v3.football.api-sports.io"

def load_config():
    """Load API keys from config files."""
    config = {}
    
    # Try to load API-Football key
    api_fb_config = Path.home() / ".config" / "api-football" / "config.json"
    if api_fb_config.exists():
        with open(api_fb_config) as f:
            data = json.load(f)
            config['api_football_key'] = data.get('api_key', '')
    else:
        config['api_football_key'] = APIFOOTBALL_KEY
    
    # Try to load Odds API key
    odds_config = Path.home() / ".config" / "the-odds-api" / "key"
    if odds_config.exists():
        with open(odds_config) as f:
            config['odds_api_key'] = f.read().strip()
    else:
        config['odds_api_key'] = ODDS_API_KEY
    
    return config

def search_team(team_name):
    """Search for team in TheSportsDB."""
    # Try exact search first
    url = f"{THE_SPORTS_DB_BASE}/searchteams.php?t={team_name.replace(' ', '%20')}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        teams = data.get('teams', [])
        if teams:
            return teams[0]
    
    # Try broader search with just first word
    first_word = team_name.split()[0]
    url = f"{THE_SPORTS_DB_BASE}/searchteams.php?t={first_word}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        teams = data.get('teams', [])
        if teams:
            # Find best match
            for team in teams:
                if first_word.lower() in team.get('strTeam', '').lower():
                    return team
            return teams[0]
    return None

def get_next_fixtures(team_id, count=5):
    """Get upcoming fixtures for a team."""
    url = f"{THE_SPORTS_DB_BASE}/eventsnext.php?id={team_id}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        events = data.get('events', [])
        return events[:count] if events else []
    return []

def get_last_results(team_id, count=5):
    """Get past results for a team."""
    url = f"{THE_SPORTS_DB_BASE}/eventslast.php?id={team_id}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        results = data.get('results', [])
        return results[:count] if results else []
    return []

def get_head_to_head(team1, team2):
    """Get head-to-head history."""
    url = f"{THE_SPORTS_DB_BASE}/searchevents.php?e={team1}_vs_{team2}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        return data.get('event', [])[:5]  # Last 5 meetings
    return []

def get_odds(sport, league, home_team, away_team, config):
    """Get current odds from The Odds API."""
    if not config.get('odds_api_key'):
        return None
    
    # Map to odds-api format
    sport_key = sport.lower().replace(' ', '_')
    
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    params = {
        'apiKey': config['odds_api_key'],
        'regions': 'uk',
        'markets': 'h2h',
        'oddsFormat': 'decimal'
    }
    
    resp = requests.get(url, params=params, timeout=15)
    if resp.status_code == 200:
        events = resp.json()
        for event in events:
            if (home_team.lower() in event['home_team'].lower() and 
                away_team.lower() in event['away_team'].lower()):
                return event
    return None

def get_weather(lat, lon, match_date):
    """Get weather forecast for match location."""
    try:
        match_dt = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
        date_str = match_dt.strftime('%Y-%m-%d')
    except:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': 'precipitation_sum,windspeed_10m_max',
        'start': date_str,
        'end': date_str,
        'timezone': 'auto'
    }
    
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        daily = data.get('daily', {})
        return {
            'precipitation': daily.get('precipitation_sum', [0])[0],
            'wind_speed': daily.get('windspeed_10m_max', [0])[0]
        }
    return None

def analyze_form(results, team_name):
    """Analyze recent form."""
    if not results:
        return "No data"
    
    wins = 0
    draws = 0
    losses = 0
    goals_for = 0
    goals_against = 0
    
    for match in results:
        home_score = match.get('intHomeScore')
        away_score = match.get('intAwayScore')
        home_team = match.get('strHomeTeam', '')
        
        if home_score is None or away_score is None:
            continue
        
        try:
            home_score = int(home_score)
            away_score = int(away_score)
        except:
            continue
        
        is_home = team_name.lower() in home_team.lower()
        
        if is_home:
            goals_for += home_score
            goals_against += away_score
            if home_score > away_score:
                wins += 1
            elif home_score == away_score:
                draws += 1
            else:
                losses += 1
        else:
            goals_for += away_score
            goals_against += home_score
            if away_score > home_score:
                wins += 1
            elif away_score == home_score:
                draws += 1
            else:
                losses += 1
    
    total = wins + draws + losses
    if total == 0:
        return "No valid results"
    
    return {
        'matches': total,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'win_rate': round(wins / total * 100, 1),
        'goals_for': goals_for,
        'goals_against': goals_against,
        'form_string': ''.join(['W' if i < wins else 'D' if i < wins + draws else 'L' 
                               for i in range(min(5, total))])
    }

def search_x_for_lineups(home_team, away_team):
    """Search X/Twitter for lineup info."""
    try:
        import subprocess
        search_script = Path.home() / ".openclaw" / "workspace" / "skills" / "search-x" / "scripts" / "search.js"
        if search_script.exists():
            query = f"{home_team} vs {away_team} lineup"
            result = subprocess.run(
                ["node", str(search_script), query, "--compact"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout[:500]
    except Exception:
        pass
    return None

def search_x_for_injuries(team_name):
    """Search X/Twitter for injury news."""
    try:
        import subprocess
        search_script = Path.home() / ".openclaw" / "workspace" / "skills" / "search-x" / "scripts" / "search.js"
        if search_script.exists():
            query = f"{team_name} injury news"
            result = subprocess.run(
                ["node", str(search_script), query, "--compact"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout[:500]
    except Exception:
        pass
    return None

def get_league_table(league_id):
    """Get league standings from TheSportsDB."""
    url = f"{THE_SPORTS_DB_BASE}/lookuptable.php?l={league_id}&s=2025-2026"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        table = data.get('table', [])
        return table
    return []

def calculate_motivation(team_name, league_table, fixtures_remaining):
    """Calculate motivation index based on league position."""
    if not league_table:
        return {"score": 0, "context": "Unknown"}
    
    team_pos = None
    total_teams = len(league_table)
    
    for i, team in enumerate(league_table):
        if team_name.lower() in team.get('strTeam', '').lower():
            team_pos = i + 1
            break
    
    if team_pos is None:
        return {"score": 0, "context": "Team not found in table"}
    
    # Calculate motivation based on position
    if team_pos <= 4:
        return {"score": 90, "context": f"Top 4 chase (position {team_pos})", "type": "title_race"}
    elif team_pos >= total_teams - 3:
        return {"score": 95, "context": f"Relegation battle (position {team_pos}/{total_teams})", "type": "relegation"}
    elif team_pos <= 7:
        return {"score": 70, "context": f"European spots hunt (position {team_pos})", "type": "europe"}
    elif fixtures_remaining <= 5 and abs(team_pos - total_teams // 2) <= 3:
        return {"score": 80, "context": f"Late season pressure (position {team_pos})", "type": "late_season"}
    else:
        return {"score": 40, "context": f"Mid-table comfort (position {team_pos})", "type": "mid_table"}

def calculate_fatigue(results, team_name):
    """Calculate fatigue score based on match density."""
    if not results or len(results) < 2:
        return {"score": 50, "days_since_last": 7, "recent_games": 0}
    
    # Get dates of last matches
    dates = []
    for match in results[:5]:
        date_str = match.get('dateEvent')
        if date_str:
            try:
                dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
            except:
                pass
    
    if len(dates) < 2:
        return {"score": 50, "days_since_last": 7, "recent_games": len(dates)}
    
    dates.sort(reverse=True)
    days_since_last = (datetime.now() - dates[0]).days
    
    # Calculate average days between last 3 games
    if len(dates) >= 3:
        gaps = [(dates[i] - dates[i+1]).days for i in range(min(3, len(dates)-1))]
        avg_gap = sum(gaps) / len(gaps)
    else:
        avg_gap = 7
    
    # Fatigue score: lower gap = higher fatigue
    if avg_gap <= 3:
        fatigue_score = 85  # Very high
    elif avg_gap <= 5:
        fatigue_score = 70  # High
    elif avg_gap <= 7:
        fatigue_score = 50  # Normal
    else:
        fatigue_score = 30  # Well rested
    
    return {
        "score": fatigue_score,
        "days_since_last": days_since_last,
        "avg_days_between": round(avg_gap, 1),
        "recent_games": len(dates)
    }

def calculate_value(odds, implied_prob, true_prob):
    """Calculate if there's value in a bet."""
    edge = true_prob - implied_prob
    return {
        'has_value': edge > 0.05,  # 5% edge threshold
        'edge_percent': round(edge * 100, 1),
        'suggestion': 'Value bet' if edge > 0.05 else 'No value' if edge > -0.05 else 'Avoid'
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: betting-research.py 'Team A vs Team B'")
        print("       betting-research.py --team 'Liverpool'")
        sys.exit(1)
    
    query = sys.argv[1]
    config = load_config()
    
    # Parse match query
    if ' vs ' in query.lower():
        parts = query.lower().split(' vs ')
        team1_name = parts[0].strip().title()
        team2_name = parts[1].strip().title()
    else:
        team1_name = query.strip().title()
        team2_name = None
    
    print(f"🔍 Researching: {team1_name} {'vs ' + team2_name if team2_name else ''}\n")
    
    # Get team data
    team1 = search_team(team1_name)
    if not team1:
        print(f"❌ Team not found: {team1_name}")
        sys.exit(1)
    
    team1_id = team1.get('idTeam')
    
    print(f"✅ Found: {team1.get('strTeam')} ({team1.get('strLeague')})")
    
    # Get fixtures - filter to only show this team's matches
    fixtures = get_next_fixtures(team1_id, 5)
    if fixtures:
        team1_full_name = team1.get('strTeam', '').lower()
        # Filter fixtures to only include matches involving this team
        filtered_fixtures = []
        for fix in fixtures:
            home = fix.get('strHomeTeam', '').lower()
            away = fix.get('strAwayTeam', '').lower()
            if team1_full_name in home or team1_full_name in away:
                filtered_fixtures.append(fix)
        fixtures = filtered_fixtures[:3]  # Top 3 after filtering
    if fixtures:
        print(f"\n📅 Upcoming Matches:")
        for fix in fixtures:
            home = fix.get('strHomeTeam')
            away = fix.get('strAwayTeam')
            date = fix.get('dateEvent')
            league = fix.get('strLeague', 'Unknown')
            print(f"   {date}: {home} vs {away} ({league})")
    
    # Get recent form
    results = get_last_results(team1_id, 5)
    form = analyze_form(results, team1_name)
    
    if isinstance(form, dict):
        print(f"\n📊 Recent Form (Last {form['matches']} matches):")
        print(f"   W: {form['wins']} | D: {form['draws']} | L: {form['losses']} ({form['win_rate']}% win rate)")
        print(f"   Goals: {form['goals_for']} scored, {form['goals_against']} conceded")
        print(f"   Form: {form['form_string']}")
    
    # Fatigue analysis
    fatigue = calculate_fatigue(results, team1_name)
    print(f"\n😴 Fatigue Analysis:")
    print(f"   Days since last match: {fatigue['days_since_last']}")
    print(f"   Avg days between games: {fatigue['avg_days_between']}")
    if fatigue['score'] >= 70:
        print(f"   ⚠️  HIGH FATIGUE ({fatigue['score']}/100) - squad rotation likely")
    elif fatigue['score'] >= 50:
        print(f"   🟡 Moderate fatigue ({fatigue['score']}/100)")
    else:
        print(f"   🟢 Well rested ({fatigue['score']}/100)")
    
    # Motivation analysis (if league data available)
    league_id = team1.get('idLeague')
    if league_id:
        league_table = get_league_table(league_id)
        # Estimate fixtures remaining
        fixtures_remaining = 10  # Rough estimate
        motivation = calculate_motivation(team1_name, league_table, fixtures_remaining)
        print(f"\n🔥 Motivation Index:")
        print(f"   Score: {motivation['score']}/100")
        print(f"   Context: {motivation['context']}")
        if motivation['type'] == 'relegation':
            print(f"   🚨 DESPERATION FACTOR - must-win mentality")
        elif motivation['type'] == 'title_race':
            print(f"   🏆 TITLE PRESSURE - every point crucial")
    
    # H2H analysis
    if team2_name:
        print(f"\n⚔️ Head-to-Head:")
        h2h = get_head_to_head(team1_name, team2_name)
        if h2h:
            print(f"   Last {len(h2h)} meetings:")
            for match in h2h[:3]:
                home = match.get('strHomeTeam', '')
                away = match.get('strAwayTeam', '')
                h_score = match.get('intHomeScore', '-')
                a_score = match.get('intAwayScore', '-')
                date = match.get('dateEvent', '')
                print(f"   {date}: {home} {h_score}-{a_score} {away}")
        else:
            print(f"   No recent H2H data available")
    
    # Check for odds
    if team2_name and config.get('odds_api_key'):
        print(f"\n💰 Current Odds:")
        odds_data = get_odds('soccer', team1.get('strLeague', ''), team1_name, team2_name, config)
        if odds_data:
            bookmakers = odds_data.get('bookmakers', [])
            if bookmakers:
                bm = bookmakers[0]  # First bookmaker
                outcomes = bm.get('markets', [{}])[0].get('outcomes', [])
                for outcome in outcomes[:3]:
                    print(f"   {outcome['name']}: {outcome['price']}")
        else:
            print(f"   No odds data available")
    
    # Check for X search info (lineups, injuries)
    if team2_name:
        print(f"\n🐦 X/Twitter Intelligence:")
        
        # Lineup search
        x_lineups = search_x_for_lineups(team1_name, team2_name)
        if x_lineups:
            print(f"   📋 Lineup leaks:")
            print(f"   {x_lineups[:300]}...")
        
        # Injury search for both teams
        print(f"")
        x_injuries_1 = search_x_for_injuries(team1_name)
        if x_injuries_1:
            print(f"   🚑 {team1_name} injury news:")
            print(f"   {x_injuries_1[:250]}...")
        
        x_injuries_2 = search_x_for_injuries(team2_name)
        if x_injuries_2:
            print(f"   🚑 {team2_name} injury news:")
            print(f"   {x_injuries_2[:250]}...")
        
        if not x_lineups and not x_injuries_1 and not x_injuries_2:
            print(f"   No X data found (requires xAI API key for search-x)")
            print(f"   Manual: node ~/.openclaw/workspace/skills/search-x/scripts/search.js '{team1_name} vs {team2_name} lineup'")
    
    print(f"\n---")
    print("💡 Tip: Check X 1-2 hours before kickoff for leaked lineups and injury updates")
    print("💡 Run with '--full' for API-Football data (confirmed lineups, injuries, xG)")

if __name__ == "__main__":
    main()
