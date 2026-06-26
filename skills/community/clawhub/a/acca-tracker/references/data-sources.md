# Data Source Strategy

Free live score sources — no API keys needed.

## PRIMARY: TheSportsDB API (use this FIRST)

TheSportsDB is the **most reliable source** for live scores. All major score sites
(Sofascore, ESPN, BBC, LiveScore, Flashscore, FotMob, SportyTrader) use JavaScript
rendering that `web_extract` cannot parse — they return empty previews without actual
scores. TheSportsDB returns structured JSON with scores and match status.

### How to use (execute_code + urllib):
```python
import json, urllib.request

headers = {"User-Agent": "Mozilla/5.0"}
today = "2026-04-15"  # format: YYYY-MM-DD

url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())
    for e in data.get("events", []):
        home = e.get("strHomeTeam", "?")
        away = e.get("strAwayTeam", "?")
        h_score = e.get("intHomeScore", "?")
        a_score = e.get("intAwayScore", "?")
        status = e.get("strStatus", "?")  # "1H", "2H", "HT", "FT", "Not Started"
        league = e.get("strLeague", "?")
        print(f"{league}: {home} {h_score}-{a_score} {away} ({status})")
```

### Status values returned by TheSportsDB:
- `"Not Started"` → match hasn't kicked off yet
- `"1H"` → first half in progress
- `"HT"` → half time
- `"2H"` → second half in progress
- `"Match Finished"` → full time
- `"Match Cancelled"` → cancelled
- `"Postponed"` → postponed

### Coverage: ALL tiers
TheSportsDB covers Champions League, League One, Regionalliga, and more. It is NOT
just for low-tier leagues. Use it as the primary source for everything.

### Limitation
May lag 2-5 minutes behind real-time. Scores might be `None` briefly during live updates.

## SECONDARY: web_search (for context, not scores)

Use web_search for:
- Pre-match context (form, H2H, injuries)
- When TheSportsDB has no data for a match
- News articles about match events

Search query patterns:
```
1. "{Team A} vs {Team B} live score"
2. "{Team A} {Team B} {league} score today"
3. "{Team A} {Team B} result {date}"
```

For German teams with special characters:
```
"FC Altona 93 vs VfB Oldenburg score"   # try without umlauts
"Schöningen vs Lohne score"             # also try with
```

Include team nicknames as fallback: "Gunners vs PSG" might catch what "Arsenal vs PSG" misses.

## Handling No Data

1. Check if kickoff has passed (if not → PENDING)
2. 30+ min past kickoff, no data → "score unavailable — match should be live"
3. 2+ hours past kickoff, no data → "unverified — likely finished, no live data"
4. NEVER guess or fabricate scores

## Lessons Learned

- **Do NOT waste calls on Sofascore/ESPN/BBC/LiveScore/FotMob for live scores** — they all require JS rendering. web_extract returns useless static HTML.
- **Sofascore API** (`api.sofascore.com/api/v1/event/{id}`) returns 404 for most events and is unreliable.
- **TheSportsDB on first attempt** saves 10+ wasted tool calls on JS-rendered sites.
- If you find team name mismatches (e.g. betslip says "Dynamo Berlin" but API says "BFC Dynamo"), note the alias and match them up.