# Data Coverage

## Data Sources

| Source | What it provides | Scope |
|--------|-----------------|-------|
| ESPN API (teams list) | Team ID, team name, **team crest URL**, league | All ESPN-covered leagues |
| ESPN API (team profile) | Stadium name, city, venue info, **team crest URL** | All ESPN-covered leagues |
| ESPN API (team schedule) | **Match schedule during trip dates** (past + upcoming) | All ESPN-covered leagues |
| Web Search — Spot Info | Stadium tours, museums, fan pubs, landmarks, shops | Any city worldwide |
| Web Search — Spot Stories | Historical backstories, legends, anecdotes for each spot | Any team/city |
| Web Search — On This Day | Historic football events on specific dates | Any team/date |
| flyai (`search-flight`, `search-hotels`) | Flights and hotels | Domestic & international |

## Coverage by Command

| Command | ESPN API | Web Search (spots) | Web Search (stories) | Web Search (On This Day) | flyai |
|---------|:-:|:-:|:-:|:-:|:-:|
| `generate_pilgrimage` | x (team info + matches) | x | x | optional | optional |
| `get_stadium_info` | x (team info) | x | x | | |
| `get_pilgrimage_spots` | x (team info) | x | x | | |
| `get_on_this_day` | x (team info) | | | x | |
| `get_trip_matches` | x (team info + schedule) | | | | |
| `get_travel_plan` | x (team info) | | | | x |

## Emotional Arc Phases

| Phase | Content | Data Needed |
|-------|---------|-------------|
| Pre-departure — The Call | Team crest, history, legends, motto, On This Day, **trip match alert** | ESPN API (team info + crest + matches), Web Search (On This Day) |
| Arrival Day — First Sight | City landmarks + backstories, statues, plazas, On This Day | Web Search (spots + stories + On This Day) |
| Stadium Day — The Temple | Stadium tour + construction story, museum + crown jewels, pubs + history, On This Day, **match day itinerary** | Web Search (spots + stories + On This Day), **ESPN API (matches)** |
| Deep Experience — Immersion | Training ground + naming origin, hidden gems + special significance | Web Search (spots + stories) |
| Departure — The Farewell | Souvenirs + collectible value, one last drink | Web Search (spots) |
| Travel & Stay (optional) | Flights, hotels | flyai |

## Team Crest (Logo) Coverage

| Source | How to get | Format |
|--------|-----------|--------|
| ESPN API (teams list) | `team.logos[0].href` from teams list response | URL (PNG) |
| ESPN API (team profile) | `team.logos[0].href` from team profile response | URL (PNG) |
| Direct construction | `https://a.espncdn.com/i/teamlogos/soccer/500/{team_id}.png` | URL (PNG) |
| Web Search (fallback) | Search `"{team_name} official logo png"` | Any image URL |

The crest URL follows a predictable pattern: `https://a.espncdn.com/i/teamlogos/soccer/500/{team_id}.png`. No API call needed if team_id is known.
