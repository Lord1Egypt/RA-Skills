# Fitbit API Reference

## Authentication

Fitbit uses OAuth 2.0 for authentication.

**Authorization URL:**
```
https://www.fitbit.com/oauth2/authorize
```

**Token URL:**
```
https://api.fitbit.com/oauth2/token
```

Authentication uses HTTP Basic auth with `client_id:client_secret` as credentials.

## Scopes

This skill requires these scopes:
- `activity` - Daily activity data
- `sleep` - Sleep records and stages
- `heartrate` - Heart rate data
- `profile` - User profile
- `weight` - Weight data (optional)

## API Endpoints

### Daily Activity Summary

```
GET https://api.fitbit.com/1/user/-/activities/date/{date}.json
```

**Parameters:**
- `date` - YYYY-MM-DD format or "today"/"yesterday"

**Response fields (summary):**
| Field | Type | Description |
|-------|------|-------------|
| `steps` | int | Step count |
| `caloriesOut` | int | Total calories burned |
| `caloriesBMR` | int | Basal metabolic rate calories |
| `activityCalories` | int | Calories from activity |
| `distance` | float | Total distance (km) |
| `distances` | array | Distance breakdown by activity |
| `sedentaryMinutes` | int | Sedentary time (minutes) |
| `lightlyActiveMinutes` | int | Light activity time |
| `fairlyActiveMinutes` | int | Moderate activity time |
| `veryActiveMinutes` | int | Vigorous activity time |
| `restingHeartRate` | int | Resting heart rate (bpm) |
| `heartRateZones` | array | Time in each HR zone |

**Heart rate zones:**
| Zone | Description |
|------|-------------|
| Out of Range | Below fat burn zone |
| Fat Burn | 50-70% of max HR |
| Cardio | 70-85% of max HR |
| Peak | Above 85% of max HR |

### Sleep Records

```
GET https://api.fitbit.com/1.2/user/-/sleep/date/{date}.json
```

**Parameters:**
- `date` - YYYY-MM-DD format or "today"/"yesterday"

**Response structure:**
```json
{
  "sleep": [
    {
      "dateOfSleep": "2026-03-21",
      "duration": 29460000,        // milliseconds
      "efficiency": 89,             // percentage
      "endTime": "2026-03-21T06:29:30.000",
      "isMainSleep": true,          // false = nap
      "levels": {
        "data": [...],               // minute-by-minute stages
        "summary": {
          "deep": { "minutes": 92, "count": 3 },
          "light": { "minutes": 240, "count": 5 },
          "rem": { "minutes": 105, "count": 4 },
          "wake": { "minutes": 54, "count": 2 }
        }
      },
      "minutesAsleep": 437,
      "startTime": "2026-03-20T22:18:00.000",
      "timeInBed": 491,
      "type": "stages"              // or "classic"
    }
  ],
  "summary": {
    "totalMinutesAsleep": 437,
    "totalTimeInBed": 491,
    "totalSleepRecords": 2
  }
}
```

### Key Differences

**Main Sleep vs Naps:**
- `isMainSleep: true` - Primary sleep session (usually overnight)
- `isMainSleep: false` - Nap or short sleep

Fitbit returns records in reverse chronological order (naps first, main sleep second).

**Sleep Stages vs Classic:**
- `type: "stages"` - Uses Fitbit's Smart Wake alarm staging (recommended)
- `type: "classic"` - Traditional sleep detection

## Rate Limits

- 150 requests per hour for user-level endpoints
- 500 requests per hour for summary endpoints
- Tokens auto-refresh when expired

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Re-run OAuth login |
| 429 Too Many Requests | Rate limit exceeded | Wait and retry |
| 400 Bad Request | Invalid date format | Use YYYY-MM-DD |
