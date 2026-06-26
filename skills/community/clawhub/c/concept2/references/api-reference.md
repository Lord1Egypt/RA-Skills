# Concept2 Logbook API Reference

Complete API endpoint reference for Concept2 Logbook.

## Base URL

```
https://log.concept2.com/api
```

## Authentication

All requests require OAuth2 Bearer token:

```
Authorization: Bearer <access_token>
```

Include API version header:

```
Accept: application/vnd.c2logbook.v1+json
```

## Endpoints

### User Endpoints

#### Get Current User
```
GET /users/me
```

Returns authenticated user profile.

**Response:**
```json
{
  "data": {
    "id": 1,
    "username": "davidh",
    "first_name": "David",
    "last_name": "Hart",
    "gender": "M",
    "dob": "1977-08-19",
    "email": "davidh@concept2.com",
    "country": "GBR",
    "profile_image": "http://...",
    "max_heart_rate": 180,
    "weight": 7500,
    "logbook_privacy": "partners"
  }
}
```

#### Get User by ID
```
GET /users/{user_id}
```

### Results (Workouts) Endpoints

#### List Results
```
GET /users/{user}/results
```

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| from | date | Start date (YYYY-MM-DD) |
| to | date | End date (YYYY-MM-DD) |
| type | string | Workout type: rower, skierg, bike, etc. |
| updated_after | datetime | Only results updated after this time |
| page | integer | Page number (1-based) |
| per_page | integer | Results per page (max 250) |

**Response:**
```json
{
  "data": [
    {
      "id": 123,
      "user_id": 1,
      "date": "2026-03-03 08:30:00",
      "distance": 5000,
      "type": "rower",
      "time": 145230,
      "time_formatted": "24:12.3",
      "stroke_rate": 28,
      "heart_rate": {"average": 145, "max": 165},
      "calories_total": 320,
      "drag_factor": 115,
      "workout_type": "JustRow"
    }
  ],
  "meta": {
    "pagination": {
      "total": 45,
      "count": 1,
      "per_page": 50,
      "current_page": 1,
      "total_pages": 1
    }
  }
}
```

#### Get Single Result
```
GET /users/{user}/results/{result_id}
```

**Query Parameters:**
- `include` - Comma-separated list: strokes, metadata, user

#### Add Result
```
POST /users/{user}/results
```

**Request Body:**
```json
{
  "type": "rower",
  "date": "2026-03-08 14:30:00",
  "timezone": "Europe/Oslo",
  "distance": 5000,
  "time": 145230,
  "weight_class": "H",
  "workout_type": "JustRow",
  "stroke_rate": 28,
  "heart_rate": {"average": 145},
  "drag_factor": 115
}
```

#### Edit Result
```
PATCH /users/{user}/results/{result_id}
```

#### Delete Result
```
DELETE /users/{user}/results/{result_id}
```

#### Bulk Add Results
```
POST /users/{user}/results/bulk
```

### Stroke Data Endpoints

#### Get Stroke Data
```
GET /users/{user}/results/{result_id}/strokes
```

Returns per-stroke data for a workout.

**Response:**
```json
{
  "data": [
    {
      "t": 23,
      "d": 155,
      "p": 971,
      "spm": 35,
      "hr": 156
    }
  ]
}
```

Fields:
- `t` - Time in tenths of seconds (incremental)
- `d` - Distance in decimeters (incremental)
- `p` - Pace in tenths of sec per 500m (rower) or 1000m (bike)
- `spm` - Strokes per minute
- `hr` - Heart rate

#### Delete Stroke Data
```
DELETE /users/{user}/results/{result_id}/strokes
```

### File Export Endpoints

#### Export Workout
```
GET /users/{user}/results/{result_id}/export/{type}
```

Export formats: `csv`, `fit`, `tcx`

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

## Time/Distance Conversions

### Time Format
- Stored in tenths of seconds
- 14523 = 1452.3 seconds = 24:12.3

### Pace Calculation
```python
pace_per_500m = (time_tenths / distance_m) * 500
```

### Distance Format
- Stored in meters
- 5000 = 5km

### Stroke Data
- Distance in decimeters (incremental)
- Time in tenths of seconds (incremental)
- Pace in tenths of sec per 500m (rower) or 1000m (bike)
