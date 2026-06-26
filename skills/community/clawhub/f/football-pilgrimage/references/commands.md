# Commands Reference

## Valid Commands

- `generate_pilgrimage`
- `get_stadium_info`
- `get_pilgrimage_spots`
- `get_on_this_day`
- `get_trip_matches`
- `get_travel_plan`

## Commands That DO NOT Exist

- ~~`get_pilgrimage_guide`~~ — the correct command is `generate_pilgrimage`
- ~~`get_stadium_tour`~~ — use `get_stadium_info` which includes tour details
- ~~`search_pilgrimage`~~ — use `get_pilgrimage_spots` with optional `spot_type` filter
- ~~`get_flight_info`~~ — use `get_travel_plan` which calls flyai internally
- ~~`get_history`~~ — use `get_on_this_day` for historic events on a specific date
- ~~`get_team_logo`~~ — team crest is included in `get_team_profile` from football-data (`data.team.crest`)
- ~~`get_match_schedule`~~ — use `get_trip_matches` to check for matches during trip dates
- ~~`check_fixtures`~~ — use `get_trip_matches` which filters by trip date range

## Command Parameter Reference

### generate_pilgrimage
- `team` (str, required): Team name
- `departure_city` (str, optional): Departure city for travel planning
- `departure_date` (str, optional): Travel date (YYYY-MM-DD) — also used for On This Day matching
- `duration` (str, optional): Trip duration in days (default: 3)

### get_stadium_info
- `team` (str, required): Team name

### get_pilgrimage_spots
- `team` (str, required): Team name
- `spot_type` (str, optional): "museum", "pub", "landmark", "shop", "all"

### get_on_this_day
- `team` (str, required): Team name
- `departure_date` (str, required): Trip start date (YYYY-MM-DD)
- `duration` (int, optional): Trip duration in days (default: 3) — searches every day from departure_date to departure_date + duration - 1

### get_trip_matches
- `team` (str, required): Team name
- `departure_date` (str, required): Trip start date (YYYY-MM-DD)
- `duration` (int, optional): Trip duration in days (default: 3)

### get_travel_plan
- `team` (str, required): Team name
- `departure_city` (str, required): Departure city
- `departure_date` (str, required): Travel date (YYYY-MM-DD)
- `nights` (int, optional): Number of nights (default: 3)
