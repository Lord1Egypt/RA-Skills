# ESPN API Reference

ESPN provides a public REST API for football (soccer) data. No authentication or API key required. Data is accessed via `curl` or `web_fetch`.

## Base URL

```
https://site.api.espn.com/apis/site/v2/sports/soccer/{espn_league}/
```

## League Slugs

| League | ESPN Slug | Country |
|--------|-----------|---------|
| Premier League | `eng.1` | England |
| La Liga | `esp.1` | Spain |
| Bundesliga | `ger.1` | Germany |
| Serie A | `ita.1` | Italy |
| Ligue 1 | `fra.1` | France |
| Championship | `eng.2` | England |
| Eredivisie | `ned.1` | Netherlands |
| Primeira Liga | `por.1` | Portugal |
| Serie A Brazil | `bra.1` | Brazil |
| MLS | `usa.1` | USA |
| Champions League | `uefa.champions` | Europe |
| Europa League | `uefa.europa` | Europe |
| World Cup | `fifa.world` | International |

## Endpoints

### Search team — list all teams in a league
```bash
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/{espn_league}/teams" | cat
```
Response: `sports[0].leagues[0].teams[].team` — each team has:
- `id` (string): ESPN team ID (e.g., `"359"` for Arsenal)
- `displayName` (string): Full team name (e.g., `"Arsenal"`)
- `shortDisplayName` (string): Short name (e.g., `"Arsenal"`)
- `abbreviation` (string): 3-letter code (e.g., `"ARS"`)
- `logos[0].href` (string): Crest URL (e.g., `"https://a.espncdn.com/i/teamlogos/soccer/500/359.png"`)

### Get team profile
```bash
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/{espn_league}/teams/{team_id}" | cat
```
Response: `team` object — **note: different structure from teams list** (no `sports[]` wrapper):
- `team.id` (string): ESPN team ID
- `team.displayName` (string): Full team name
- `team.location` (string): City name (e.g., `"Barcelona"`)
- `team.logos[0].href` (string): Crest URL
- `team.color` (string): Primary color hex (e.g., `"990000"`)
- `team.alternateColor` (string): Secondary color hex

⚠️ **This endpoint does NOT return venue/stadium info.** To get the stadium name and city, use the schedule endpoint below — venue info is in `events[].competitions[].venue`.

### Get team schedule (past results)
```bash
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/{espn_league}/teams/{team_id}/schedule" | cat
```
Response: top-level keys are `timestamp`, `status`, `season`, `team`, `events`, `requestedSeason`. The `events[]` array contains:
- `id` (string): Event ID
- `date` (string): ISO 8601 datetime (e.g., `"2026-04-17T19:00Z"`)
- `competitions[0].competitors[]`: Array with home and away teams
  - `homeAway` (string): `"home"` or `"away"`
  - `team.id`, `team.displayName`, `team.abbreviation`
  - `score` (string): Goals scored
- `competitions[0].status.type.name` (string): `"STATUS_SCHEDULED"`, `"STATUS_FINAL"`, etc.
- `competitions[0].venue.fullName` (string): Stadium name (e.g., `"Spotify Camp Nou"`)
- `competitions[0].venue.address.city` (string): City (e.g., `"Barcelona"`)

### Get team schedule (upcoming fixtures)
```bash
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/{espn_league}/teams/{team_id}/schedule?fixture=true" | cat
```
Same response format as above, but returns future matches.

## Finding a Team

To find a team's ESPN ID and league slug:
1. If you know the league, fetch the teams list for that league and match by name
2. If you don't know the league, try the most likely leagues (e.g., for "AC Milan" try `ita.1`)
3. Use fuzzy name matching — ESPN uses English names (e.g., `"AC Milan"`, `"Bayern Munich"`) — always use the English name, not the localized name

## Common Team IDs

| Team | ESPN ID | League Slug |
|------|---------|-------------|
| Arsenal | 359 | eng.1 |
| Liverpool | 364 | eng.1 |
| Man Utd | 360 | eng.1 |
| Chelsea | 363 | eng.1 |
| Man City | 382 | eng.1 |
| Real Madrid | 86 | esp.1 |
| Barcelona | 83 | esp.1 |
| Atletico Madrid | 1068 | esp.1 |
| Bayern Munich | 132 | ger.1 |
| Dortmund | 131 | ger.1 |
| AC Milan | 103 | ita.1 |
| Inter Milan | 110 | ita.1 |
| Juventus | 111 | ita.1 |
| PSG | 160 | fra.1 |
