# Hevy Data Structures & JSON Examples

## Workout Object Structure

```json
{
  "id": "workout_id_123",
  "title": "Push Day",
  "start_time": "2026-02-14T10:00:00Z",
  "end_time": "2026-02-14T11:30:00Z",
  "exercises": [
    {
      "id": "exercise_id_456",
      "title": "Bench Press",
      "muscle_groups": ["chest", "triceps", "shoulders"],
      "exercise_template_id": "template_789",
      "sets": [
        {
          "index": 0,
          "weight_kg": 80,
          "reps": 8,
          "distance_meters": null,
          "duration_seconds": null,
          "rpe": null
        }
      ]
    }
  ],
  "notes": "Great workout today!"
}
```

## Routine Object Structure

```json
{
  "id": "routine_id_123",
  "title": "Push Pull Legs",
  "notes": "3 day split routine",
  "exercises": [
    {
      "exercise_template_id": "template_456",
      "title": "Bench Press",
      "rest_seconds": 180,
      "sets": [
        {
          "reps": 8,
          "weight_kg": 80
        }
      ]
    }
  ]
}
```

## Exercise Template Structure

```json
{
  "id": "template_123",
  "title": "Bench Press",
  "type": "weight_reps",
  "muscle_groups": ["chest", "triceps", "shoulders"],
  "is_custom": false
}
```

## Statistics Response Structure

### Summary Stats
```json
{
  "period": "month",
  "total_workouts": 12,
  "total_duration_minutes": 720,
  "average_duration_minutes": 60,
  "total_volume_kg": 15600,
  "average_volume_kg": 1300
}
```

### Progress Data
```json
{
  "exercise": "Bench Press",
  "metric": "weight",
  "data_points": [
    {
      "date": "2026-01-15",
      "value": 75,
      "volume": 600
    },
    {
      "date": "2026-01-22",
      "value": 77.5,
      "volume": 620
    }
  ]
}
```

### Personal Records
```json
{
  "records": [
    {
      "exercise": "Bench Press",
      "weight_kg": 85,
      "reps": 5,
      "date": "2026-02-10",
      "estimated_1rm_kg": 95.5
    }
  ]
}
```

## Common Query Parameters

### Date Filtering
- `--since YYYY-MM-DD`: Get data from specific date
- `--until YYYY-MM-DD`: Get data until specific date

### Output Control
- `--output json`: Structured JSON output
- `--output table`: Human-readable table
- `--output plain`: Pipe-delimited values

### Statistics Options
- `--period week|month|year`: Time period for summaries
- `--metric weight|1rm`: Progress tracking metric
- `--exercise "Exercise Name"`: Filter by exercise

## Exercise Types

### Weight & Reps
```json
{
  "type": "weight_reps",
  "sets": [
    {
      "weight_kg": 80,
      "reps": 8
    }
  ]
}
```

### Bodyweight
```json
{
  "type": "bodyweight",
  "sets": [
    {
      "reps": 15
    }
  ]
}
```

### Cardio (Time)
```json
{
  "type": "duration",
  "sets": [
    {
      "duration_seconds": 1800
    }
  ]
}
```

### Cardio (Distance)
```json
{
  "type": "distance_duration",
  "sets": [
    {
      "distance_meters": 5000,
      "duration_seconds": 1500
    }
  ]
}
```