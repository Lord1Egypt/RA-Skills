# Output Schema

## Normalized Daily Output

`fitbit_normalize_daily.py` transforms raw Fitbit API responses into a clean, consistent format.

### Complete Schema

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "Europe/London",
  "generated_at": "2026-03-21T10:30:00.000Z",

  "sleep": {
    "duration_minutes": 437,
    "efficiency": 89,
    "time_in_bed_minutes": 491,
    "sleep_score": 85,
    "deep_minutes": 92,
    "light_minutes": 240,
    "rem_minutes": 105,
    "wake_minutes": 54,
    "nap_minutes": 66,
    "source": "fitbit"
  },

  "activity": {
    "steps": 8234,
    "distance_km": 6.2,
    "calories_out": 1892,
    "calories_bmr": 1048,
    "activity_calories": 298,
    "sedentary_minutes": 492,
    "lightly_active_minutes": 84,
    "fairly_active_minutes": 23,
    "very_active_minutes": 45,
    "resting_heart_rate": 58,
    "heart_rate_zones": [
      {
        "name": "Out of Range",
        "minutes": 720,
        "calories": 1200,
        "min_hr": 60,
        "max_hr": 100
      },
      {
        "name": "Fat Burn",
        "minutes": 90,
        "calories": 350,
        "min_hr": 100,
        "max_hr": 140
      },
      {
        "name": "Cardio",
        "minutes": 32,
        "calories": 200,
        "min_hr": 140,
        "max_hr": 170
      },
      {
        "name": "Peak",
        "minutes": 8,
        "calories": 50,
        "min_hr": 170,
        "max_hr": 220
      }
    ],
    "source": "fitbit"
  },

  "sources_present": ["fitbit"],
  "source": {
    "raw_files": ["/tmp/fitbit_raw_2026-03-21.json"]
  }
}
```

## Field Descriptions

### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date in YYYY-MM-DD format |
| `timezone` | string | IANA timezone (e.g., Europe/London) |
| `generated_at` | string | ISO-8601 timestamp when generated |

### Sleep Object

| Field | Type | Description |
|-------|------|-------------|
| `duration_minutes` | int\|null | Actual sleep time (excludes awake periods) |
| `efficiency` | int\|null | Sleep efficiency percentage |
| `time_in_bed_minutes` | int\|null | Total time spent in bed |
| `sleep_score` | int\|null | Overall sleep score (not always available) |
| `deep_minutes` | int\|null | Deep sleep stage minutes |
| `light_minutes` | int\|null | Light sleep stage minutes |
| `rem_minutes` | int\|null | REM sleep stage minutes |
| `wake_minutes` | int\|null | Wake/awake minutes during night |
| `nap_minutes` | int\|null | Nap duration (if daytime sleep detected) |
| `source` | string | Always "fitbit" |

### Activity Object

| Field | Type | Description |
|-------|------|-------------|
| `steps` | int\|null | Daily step count |
| `distance_km` | float\|null | Total distance in kilometers |
| `calories_out` | int\|null | Total calories burned |
| `calories_bmr` | int\|null | Basal metabolic rate calories |
| `activity_calories` | int\|null | Calories from activity (excludes BMR) |
| `sedentary_minutes` | int\|null | Minutes in sedentary state |
| `lightly_active_minutes` | int\|null | Light activity minutes |
| `fairly_active_minutes` | int\|null | Moderate activity minutes |
| `very_active_minutes` | int\|null | Vigorous activity minutes |
| `resting_heart_rate` | int\|null | Resting heart rate in BPM |
| `heart_rate_zones` | array | Time in each heart rate zone |
| `source` | string | Always "fitbit" |

### Heart Rate Zone Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Zone name (Out of Range, Fat Burn, Cardio, Peak) |
| `minutes` | int | Minutes spent in this zone |
| `calories` | int | Calories burned in this zone |
| `min_hr` | int | Minimum heart rate for this zone |
| `max_hr` | int | Maximum heart rate for this zone |

## Notes

- All `null` fields indicate data not available from Fitbit API
- `nap_minutes` is extracted separately from main sleep records
- Heart rate zones are only included when there is time spent in them
- `activity_calories` = `calories_out` - `calories_bmr`
