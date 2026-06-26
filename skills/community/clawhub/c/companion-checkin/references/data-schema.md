# Companion Check-In Data Schema

Each line in `data/checkins.jsonl` is a single JSON object:

```json
{
  "timestamp": "2026-04-24T21:50:00+07:00",
  "moment": "morning",
  "answers": {
    "sleep_hours": 7,
    "mood": 8,
    "top_focus": "finish proposal",
    "meal_status": "already had toast"
  }
}
```

Common answer keys:

- `sleep_hours`
- `mood`
- `top_focus`
- `meal_status`
- `energy`
- `work_progress`
- `support_needed`
- `wins`
- `stressors`
- `bedtime_plan`
- `rest_support`
- `comeback_note`
