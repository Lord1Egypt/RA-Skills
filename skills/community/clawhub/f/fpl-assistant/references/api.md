# FPL Public API Reference

Base URL: `https://fantasy.premierleague.com/api/`

No authentication required for public endpoints. Rate limit is generous but avoid excessive calls.

## Key Endpoints

### 1. Bootstrap Static (Master Data)

```
GET /bootstrap-static/
```

Returns ALL static data. Cache this — it's large (~2MB) but contains everything:

**Top-level keys:**
- `events` — Gameweeks (deadlines, status, chip plays)
- `teams` — 20 PL clubs (id, name, short_name, strength ratings)
- `element_types` — Position types (1=GKP, 2=DEF, 3=MID, 4=FWD)
- `elements` — All players (see below)
- `game_settings` — Scoring rules
- `chips` — Chip availability windows

**Key fields in `elements[]` (players):**
```
id                    — Player unique ID
web_name              — Short display name
element_type          — Position (1-4)
team                  — Team ID
now_cost              — Current price (×10, e.g. 75 = £7.5m)
selected_by_percent   — Ownership %
form                  — Average points last 30 days (string)
total_points          — Season total
event_points          — Last GW points
points_per_game       — Season average
minutes               — Total minutes played
goals_scored, assists — Season totals
clean_sheets          — Season total
yellow_cards, red_cards
bonus                 — Total bonus points
bps                   — Total BPS
influence, creativity, threat — ICT index values
transfers_in_event    — Transfers in this GW
transfers_out_event   — Transfers out this GW
status                — Availability: a=available, d=doubtful, i=injured, s=suspended, u=unavailable
news                  — Injury/availability news
chance_of_playing_this_round  — % or null
chance_of_playing_next_round  — % or null
```

### 2. Fixtures

```
GET /fixtures/
GET /fixtures/?event={gw}     — Specific gameweek
```

**Fields per fixture:**
```
event                    — GW number
kickoff_time             — ISO datetime
team_h, team_a           — Home/away team IDs
team_h_score, team_a_score
team_h_difficulty        — FDR for home team (1-5)
team_a_difficulty        — FDR for away team (1-5)
stats[]                  — Goals, assists, cards, bonus etc.
finished, started        — Match status
minutes                  — Minutes played
```

### 3. Element Summary (Player Detail)

```
GET /element-summary/{player_id}/
```

Returns:
- `history[]` — All past GW performances (opponent, points, minutes, goals, assists, etc.)
- `fixtures[]` — Upcoming fixtures (team, difficulty, home/away)

### 4. Manager / Entry Endpoints

```
GET /entry/{manager_id}/                — Manager profile
GET /entry/{manager_id}/event/{gw}/picks/  — Manager's team for a GW
GET /entry/{manager_id}/history/        — Season history
```

### 5. Live Data

```
GET /event/{gw}/live/                   — Live points for all players in a GW
```

Returns `elements[]` with `stats` for each player (points, minutes, goals, etc.)

### 6. Dream Team

```
GET /dream-team/{gw}/                   — Best XI for a GW
```

## Python Snippets

### Get all players as a usable dict

```python
import json, urllib.request

data = json.loads(urllib.request.urlopen(
    'https://fantasy.premierleague.com/api/bootstrap-static/'
).read())

teams = {t['id']: t for t in data['teams']}
positions = {t['id']: t['singular_name_short'] for t in data['element_types']}

players = []
for e in data['elements']:
    players.append({
        'id': e['id'],
        'name': e['web_name'],
        'team': teams[e['team']]['short_name'],
        'pos': positions[e['element_type']],
        'price': e['now_cost'] / 10,
        'form': float(e['form']),
        'pts': e['total_points'],
        'selected': float(e['selected_by_percent']),
        'goals': e['goals_scored'],
        'assists': e['assists'],
        'status': e['status'],
    })
```

### Get GW fixtures with team names

```python
fixtures = json.loads(urllib.request.urlopen(
    'https://fantasy.premierleague.com/api/fixtures/?event=32'
).read())

for f in fixtures:
    home = teams[f['team_h']]['short_name']
    away = teams[f['team_a']]['short_name']
    print(f"{home} vs {away} | FDR: {f['team_h_difficulty']}/{f['team_a_difficulty']}")
```

### Get player's recent GW history

```python
summary = json.loads(urllib.request.urlopen(
    f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
).read())

for h in summary['history'][-5:]:  # last 5 GWs
    print(f"GW{h['round']}: {h['total_points']}pts ({h['minutes']}min, {h['goals_scored']}G, {h['assists']}A)")
```

## Tips

- Call `/bootstrap-static/` once and cache; use `elements` array for all player queries
- Team IDs are stable within a season; map once from `teams[]`
- `now_cost` is in tenths — divide by 10 for display price
- `form` field is already a rolling average, useful for quick comparison
- `status` field: only `a` means fully fit; treat `d`/`i`/`s` with caution
