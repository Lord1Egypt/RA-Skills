---
name: concept2
description: Fetch and analyze Concept2 Logbook workout data via API with pulse zone analysis and trend tracking. Use when the user wants to retrieve rowing/skiing/biking workouts, analyze heart rate zones, track training trends over time, get workout summaries with performance insights, or evaluate training effectiveness. Features include pulse zone distribution (5-zone model), weekly trend analysis, pace consistency evaluation, improvement tracking, and personalized training recommendations. Requires Concept2 API access token.
---

# Concept2 Logbook API Skill

Fetch and analyze workout data from Concept2 Logbook with advanced pulse zone and trend analysis.

## Quick Start

Use the provided script to fetch workouts:

```bash
python3 scripts/fetch_workouts.py --token <API_TOKEN> --from-date 2026-03-01 --format table
```

## API Authentication

Requires a Concept2 API access token. Get one from:
https://log.concept2.com/developers/keys

Token must be passed with `Authorization: Bearer <token>` header.

## Main Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/users/me` | Get authenticated user info |
| `GET /api/users/me/results` | Get workouts (paginated) |
| `GET /api/users/me/results/{id}` | Get specific workout |
| `GET /api/users/me/results/{id}/strokes` | Get stroke-level data |

## Query Parameters for Results

| Param | Type | Description |
|-------|------|-------------|
| `from` | date | Start date (YYYY-MM-DD) |
| `to` | date | End date (YYYY-MM-DD) |
| `type` | string | Workout type: rower, skierg, bike, etc. |
| `per_page` | integer | Results per page (max 250) |

## Workout Types

| Type | Description |
|------|-------------|
| JustRow | Free rowing |
| FixedDistanceSplits | Fixed distance with splits |
| FixedTimeSplits | Fixed time with splits |
| FixedCalorie | Fixed calorie target |
| FixedWattMinute | Fixed watt-minute target |
| FixedTimeInterval | Time-based intervals |
| FixedDistanceInterval | Distance-based intervals |
| FixedCalorieInterval | Calorie intervals |
| FixedWattMinuteInterval | Watt-minute intervals |
| VariableInterval | Variable intervals |
| VariableIntervalUndefinedRest | Variable with undefined rest |

## Equipment Types

| Type | Description |
|------|-------------|
| rower | RowErg |
| skierg | SkiErg |
| bike | BikeErg |
| dynamic | Dynamic RowErg |
| slides | RowErg with slides |
| paddle | PaddleErg |
| water | WaterRower |
| snow | Snow (Nordic skiing) |
| rollerski | Roller skiing |
| multierg | MultiErg |

## Script Usage

### Basic Usage - Summary with Pulse Zones
```bash
# Auto-detect max HR from birthdate in profile
python3 scripts/fetch_workouts.py --token <TOKEN> --from-date 2026-03-01

# Specify max HR manually
python3 scripts/fetch_workouts.py --token <TOKEN> --max-hr 165 --from-date 2026-02-01

# Estimate max HR from age
python3 scripts/fetch_workouts.py --token <TOKEN> --age 59 --from-date 2026-02-01
```

### Trend Analysis (8 weeks)
```bash
python3 scripts/fetch_workouts.py --token <TOKEN> --trends 8 --from-date 2026-01-01
```

### Other Formats
```bash
# Simple table
python3 scripts/fetch_workouts.py --token <TOKEN> --format table

# JSON export
python3 scripts/fetch_workouts.py --token <TOKEN> --format json > workouts.json

# Filter by equipment type
python3 scripts/fetch_workouts.py --token <TOKEN> --type skierg
```

## Pulse Zone Analysis (5-Zone Model)

Zones based on percentage of maximum HR:

| Zone | Name | Range | Purpose |
|------|------|-------|---------|
| 🟢 1 | Restitusjon | 0-60% | Recovery, warmup |
| 🔵 2 | Aerob kapasitet | 60-70% | Base building |
| 🟡 3 | Aerob effekt | 70-80% | Tempo training |
| 🟠 4 | Anaerob terskel | 80-90% | Threshold/intervals |
| 🔴 5 | Maks kapasitet | 90-100% | VO2max/sprints |

### Max HR Calculation
- Manual: `--max-hr 165`
- From age: `--age 59` (uses Tanaka formula: 208 - 0.7×age)
- From profile: reads birthdate from user data

## Trend Analysis

Weekly aggregation of:
- Total distance
- Total time
- Number of workouts
- Average pace
- Improvement rate (pace change %)

## Workout Quality Metrics

### Pace Consistency
- Calculated from split data if available
- Standard deviation / average pace
- Rating: 🟢 Jevn | 🟡 OK | 🔴 Ujevn

### Stroke Rate (SPM) Assessment
- 🟢 18-22: Efficient, strong drive
- 🔵 <18: Fast recovery phase
- 🟡 24-28: Tempo pace
- 🟠 >30: High rate, check technique

## Training Recommendations

The script provides personalized tips:
- Training frequency assessment
- High intensity balance (20% rule for zones 4-5)
- Long workout suggestions
- Interval training reminders

## Common Calculations

### Calculate Pace
```python
pace_tenths = (time_tenths / distance_m) * 500
```

### Format Time
```python
total_seconds = time_tenths / 10
minutes = int(total_seconds // 60)
seconds = total_seconds % 60
formatted = f"{minutes}:{seconds:04.1f}"
```

### Distance Format
- Stored in meters
- 5000 = 5km

### Stroke Data
- Distance in decimeters (incremental)
- Time in tenths of seconds (incremental)
- Pace in tenths of sec per 500m (rower) or 1000m (bike)

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 200 | OK | Success |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Invalid or expired token |
| 403 | Forbidden | User hasn't authorized app |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate entry |
| 422 | Unprocessable | Validation error |
| 500 | Server Error | Try again later |
| 503 | Service Unavailable | API temporarily down |

## Pagination

Paginated responses include a `meta.pagination` object:

```json
{
  "meta": {
    "pagination": {
      "total": 150,
      "count": 50,
      "per_page": 50,
      "current_page": 1,
      "total_pages": 3,
      "links": {
        "next": "https://log.concept2.com/api/users/me/results?page=2"
      }
    }
  }
}
```

Default per_page is 50, maximum is 250.

## See Also

- Full API docs: https://log.concept2.com/developers/documentation/
- API keys: https://log.concept2.com/developers/keys
- Online validator: https://log.concept2.com/developers/validator
