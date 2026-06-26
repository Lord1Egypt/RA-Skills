# Data Schema Reference

This file is the authoritative storage contract for `data/`.

## Storage Layout

Hot files:

- `user_profile.json`: single object
- `current_plan.json`: single object
- `current_status.json`: single object
- `cache/progress_summary.json`: single object
- `cache/personal_bests.json`: single object

Cold files:

- `logs/food/YYYY-MM.json`
- `logs/hydration/YYYY-MM.json`
- `logs/sleep/YYYY-MM.json`
- `logs/workout/YYYY-MM.json`
- `logs/weight/YYYY-MM.json`
- `logs/watch/YYYY-MM.json`
- `logs/adjustments/YYYY-MM.json`
- `weekly_reports/week_YYYY-MM-DD.pdf`

General rules:

- Monthly log filenames use the local date at write time: `YYYY-MM.json`
- Log files are top-level JSON arrays
- Hot files and cache files are single JSON objects
- Do not introduce alternate wrapper objects such as `{days:[...]}`, `{records:[...]}`, or `{sessions:[...]}`
- The active raw-log window is the most recent `12` full months. Older monthly files are cold archive by default.
- Normal coaching commands must not read cold-archive months unless the user explicitly asks for long-term history.
- `current_status.json` and files in `data/cache/` are derived acceleration layers, not permanent history stores
- `weekly_reports/` is a human-readable archive, not a required input for daily commands

---

## user_profile.json

Single object.

```json
{
  "height_cm": 175,
  "weight_kg": 80,
  "target_weight_kg": 72,
  "age": 30,
  "gender": "male|female|other",
  "goal": "fat_loss|muscle_gain|recomposition|general_fitness|endurance",
  "timeline_months": 6,
  "experience": "beginner|intermediate|advanced",
  "training_location": "home|gym|both",
  "equipment": ["full_gym|dumbbells|resistance_bands|pull_up_bar|bench|none"],
  "days_per_week": 4,
  "session_minutes": 60,
  "city": "Shanghai",
  "diet_type": "no_restrictions|vegetarian|vegan|halal|keto|low_carb|other",
  "allergies": ["string"],
  "cooking_preference": "home|takeout|mix",
  "budget": "budget|moderate|no_concern",
  "injuries": [{"area": "string", "type": "current|past", "detail": "string"}],
  "medical_conditions": ["string"],
  "supplements": ["string"],
  "accountability_level": "standard|strict|military",
  "hydration_reminders": true,
  "checkin_time": "morning|evening|both",
  "bmr": 1800,
  "tdee": 2480,
  "calorie_target": 1980,
  "macros": {"protein_g": 160, "carbs_g": 198, "fat_g": 66},
  "water_target_ml": 3000,
  "created_at": "2026-03-30",
  "updated_at": "2026-03-30"
}
```

Required before plan generation:

- `height_cm`
- `weight_kg`
- `target_weight_kg`
- `age`
- `gender`
- `goal`
- `training_location`
- `days_per_week`
- `city`

Notes:

- `checkin_time` stores the user's preferred check-in cadence from onboarding.
- `water_target_ml` is derived from body weight and adjusted for training day, climate, diet context, and caffeine when relevant.

---

## current_plan.json

Single object.

```json
{
  "plan_id": "plan_20260330",
  "created_at": "2026-03-30",
  "plan_start_date": "2026-03-30",
  "split_type": "push_pull_legs|upper_lower|full_body|custom",
  "days": [
    {
      "day_number": 1,
      "label": "Push — Chest & Shoulders",
      "scheduled_weekday": "mon|tue|wed|thu|fri|sat|sun|null",
      "type": "training|rest|active_recovery",
      "warmup": ["band pull-aparts x15", "shoulder dislocates x10"],
      "exercises": [
        {
          "name": "Bench Press",
          "targets": ["chest", "front_delt", "triceps"],
          "sets": 4,
          "reps": "8-10",
          "rpe": 7,
          "rest_seconds": 90,
          "form_cues": ["elbows at 45 degrees", "feet flat on floor"],
          "common_mistakes": ["flaring elbows to 90 degrees"],
          "substitution": "Dumbbell Bench Press",
          "injury_note": ""
        }
      ],
      "prehab": ["external rotation x15 each side"],
      "cooldown": ["chest doorway stretch 30s", "tricep stretch 30s"],
      "duration_minutes": 55,
      "coach_note": "Focus on controlled negatives today"
    }
  ],
  "deload_every_n_weeks": 5,
  "progression_rule": "Add 2.5kg when all prescribed reps completed with RPE < 8"
}
```

Required exercise fields:

- `name`
- `sets`
- `reps`
- `rest_seconds`

Notes:

- `plan_start_date` anchors week counting for deload timing, scheduled reviews, and progress summaries.
- `deload_every_n_weeks` is a cadence field, not a calendar date or next scheduled week number.
- `scheduled_weekday` is optional but recommended when the user follows a stable weekly rhythm. It helps `/fitness-coach checkin` determine whether today should be a training day or rest day.

---

## current_status.json

Single object. This is the day-to-day hot snapshot used to avoid rereading raw history.

```json
{
  "updated_at": "2026-03-30T20:15:00+08:00",
  "today_date": "2026-03-30",
  "latest_weight": {"date": "2026-03-30", "weight_kg": 79.2},
  "today_food": {"date": "2026-03-30", "calories": 1250, "protein_g": 95, "carbs_g": 110, "fat_g": 36},
  "today_hydration": {"date": "2026-03-30", "total_ml": 1600, "target_ml": 3000},
  "last_sleep": {"date": "2026-03-30", "hours": 7.5, "quality": 8},
  "last_workout": {"date": "2026-03-29", "plan_day": 2, "plan_label": "Pull — Back", "completion": "full"},
  "last_watch_session": {"date": "2026-03-29", "session_type": "strength", "training_load": "productive"},
  "next_session": {"day_number": 3, "label": "Legs", "scheduled_weekday": "wed"},
  "streaks": {"training_days": 3, "logging_days": 5},
  "next_actions": ["/fitness-coach checkin", "/fitness-coach water"]
}
```

Rules:

- Refresh this file after writes to food, hydration, sleep, workout, weight, watch, plan, or adjustment data.
- Prefer reading this file before opening raw monthly logs for `/`, `/checkin`, and other day-to-day commands.
- Keep `next_actions` as a short list of `1-3` context-aware command suggestions derived from the latest status snapshot.

---

## cache/progress_summary.json

Single object. This is the medium-term summary cache for `/progress` and weekly report preparation.

```json
{
  "updated_at": "2026-03-30T20:20:00+08:00",
  "section_updated_at": {
    "weight": "2026-03-30T20:20:00+08:00",
    "training": "2026-03-30T20:20:00+08:00",
    "nutrition": "2026-03-30T20:20:00+08:00",
    "hydration": "2026-03-30T20:20:00+08:00",
    "sleep": "2026-03-30T20:20:00+08:00",
    "recovery": "2026-03-30T20:20:00+08:00",
    "flags": "2026-03-30T20:20:00+08:00"
  },
  "source_windows": {
    "weight_days": 30,
    "training_days": 30,
    "nutrition_days": 30,
    "hydration_days": 14,
    "sleep_days": 14,
    "recovery_days": 14
  },
  "weight": {"latest_kg": 79.2, "change_7d": -0.4, "change_30d": -1.8, "toward_target_pct": 45},
  "training": {"planned_sessions_30d": 16, "completed_sessions_30d": 13, "completion_rate_30d": 81},
  "nutrition": {"avg_calories_7d": 1900, "protein_target_hit_days_7d": 5},
  "hydration": {"avg_ml_7d": 2800, "target_hit_days_7d": 4},
  "sleep": {"avg_hours_7d": 7.1, "under_6h_days_14d": 2},
  "recovery": {"resting_hr_trend": "up", "hrv_trend": "down", "status": "moderate"},
  "flags": ["possible_plateau"]
}
```

Rules:

- Update only the affected sections after writes:
  - food write -> `nutrition`
  - hydration write -> `hydration`
  - sleep write -> `sleep`, and `recovery` only if the saved recovery status explicitly depends on sleep
  - workout write -> `training`
  - body-weight write -> `weight`
  - watch write -> `recovery`
  - adjustment or plan change -> only the sections whose targets, baselines, or interpretations changed
- Recompute `flags` only when one of its dependent sections changed or when `/progress`, `/adjust`, or `/report` explicitly needs fresh flags.
- `updated_at` is the latest time any section was refreshed. `section_updated_at` is the source of truth for section-level staleness.
- `updated_at` reflects the latest `section_updated_at` value and should be updated whenever any section is refreshed.
- `source_windows` should mirror section names using the `<section>_days` pattern. For example, the `recovery` section uses `recovery_days` even when it is derived partly from watch data.
- A single write must not trigger a full cache rebuild unless the cache file is missing, corrupt, or the user explicitly asked for a broader historical recompute.
- Read this file first for `/progress`.
- If missing or stale, regenerate only the stale sections from the smallest recent windows needed instead of reading all historical logs.

---

## cache/personal_bests.json

Single object used for PR detection without rescanning all workout history.

```json
{
  "updated_at": "2026-03-30T20:18:00+08:00",
  "exercises": {
    "Bench Press": {
      "best_weight_kg": 80,
      "best_weight_reps": 5,
      "best_estimated_1rm": 93.3,
      "last_pr_date": "2026-03-30"
    }
  }
}
```

Rules:

- Update this cache whenever a workout log creates a new PR.
- Use this cache first for PR detection in `/fitness-coach log`.

---

## logs/workout/YYYY-MM.json

Top-level array of workout session objects.

```json
[
  {
    "date": "2026-03-30",
    "plan_day": 1,
    "plan_label": "Push — Chest & Shoulders",
    "completion": "full|partial|skipped",
    "notes": "Felt good, could increase weight",
    "energy_level": 8,
    "pain_reported": false,
    "pain_detail": "",
    "exercises": [
      {
        "name": "Bench Press",
        "is_pr": true,
        "sets": [
          {"weight_kg": 60, "reps": 10},
          {"weight_kg": 62.5, "reps": 8}
        ]
      }
    ]
  }
]
```

Required fields:

- `date`
- `completion`

Recommended when available:

- `plan_day`
- `plan_label`
- `energy_level`
- `exercises`

---

## logs/weight/YYYY-MM.json

Top-level array.

```json
[
  {
    "date": "2026-03-30",
    "weight_kg": 79.2,
    "body_fat_pct": null,
    "waist_cm": null,
    "notes": ""
  }
]
```

Required fields:

- `date`
- `weight_kg`

---

## logs/food/YYYY-MM.json

Top-level array. One object per date.

```json
[
  {
    "date": "2026-03-30",
    "meals": [
      {
        "meal_type": "breakfast|lunch|dinner|snack",
        "time": "08:00",
        "description": "2 eggs scrambled, whole wheat toast, black coffee",
        "input_method": "text|photo|shorthand",
        "confidence": "high|medium|low|null",
        "estimated_calories": 350,
        "protein_g": 22,
        "carbs_g": 30,
        "fat_g": 18,
        "verdict": "on_point|acceptable|off_track|red_flag",
        "coach_note": ""
      }
    ],
    "daily_total": {"calories": 1980, "protein_g": 160, "carbs_g": 198, "fat_g": 66},
    "daily_target": {"calories": 1980, "protein_g": 160, "carbs_g": 198, "fat_g": 66},
    "target_met": true
  }
]
```

Rules:

- Update the existing entry for the day if `date` already exists.
- Required meal fields: `meal_type`, `description`, `estimated_calories`.
- Use `confidence: null` for text-only entries if confidence is not meaningful.
- `time` uses local 24-hour format `HH:MM`. If the user does not provide a time, use the current local time.

---

## logs/hydration/YYYY-MM.json

Top-level array. One object per date.

```json
[
  {
    "date": "2026-03-30",
    "target_ml": 3000,
    "entries": [
      {"time": "07:30", "amount_ml": 300},
      {"time": "09:15", "amount_ml": 500}
    ],
    "total_ml": 800,
    "target_met": false
  }
]
```

Rules:

- Update the existing entry for the day if present.
- Required fields: `date`, `target_ml`.
- Each `entries[].time` value should use local 24-hour format `HH:MM`.
- `total_ml` must always be derived by summing `entries[].amount_ml`. Do not accept `total_ml` as direct user input.

---

## logs/sleep/YYYY-MM.json

Top-level array.

```json
[
  {
    "date": "2026-03-30",
    "hours": 7.5,
    "quality": 8,
    "notes": ""
  }
]
```

Required fields:

- `date`
- `hours`

Optional:

- `quality`
- `notes`

Rules:

- If the user corrects or re-logs the same night's sleep for the same `date`, update the existing entry instead of appending a duplicate.

---

## logs/watch/YYYY-MM.json

Top-level array.

```json
[
  {
    "date": "2026-03-30",
    "device": "Apple Watch",
    "session_type": "strength|cardio|hiit|running|cycling|swimming|other",
    "duration_min": 58,
    "avg_hr": 132,
    "max_hr": 168,
    "resting_hr": 62,
    "hrv_ms": 45,
    "calories_active": 420,
    "hr_zones": {
      "zone1_min": 5,
      "zone2_min": 15,
      "zone3_min": 22,
      "zone4_min": 14,
      "zone5_min": 2
    },
    "sleep_hours": 7.2,
    "training_load": "low|productive|overreaching",
    "vo2_max": 42.5,
    "notes": ""
  }
]
```

Required fields:

- `date`
- `session_type`

All other metrics are optional because device support varies.

Notes:

- `sleep_hours` here is device-reported and may differ from `logs/sleep/YYYY-MM.json`. Prefer the user-reported sleep log as the coaching ground truth and use watch sleep only as a supplementary cross-check.

---

## logs/adjustments/YYYY-MM.json

Top-level array.

```json
[
  {
    "date": "2026-04-15",
    "trigger": "weight_plateau|rapid_loss|low_completion|pain|poor_recovery|goal_achieved|user_request",
    "changes": {
      "calorie_target": {"from": 1980, "to": 1780},
      "macros": {
        "from": {"protein_g": 160, "carbs_g": 198, "fat_g": 66},
        "to": {"protein_g": 160, "carbs_g": 148, "fat_g": 66}
      },
      "training_notes": "Added 1 extra HIIT session per week"
    },
    "reason": "Weight stalled for 3 weeks at 77kg"
  }
]
```

Required fields:

- `date`
- `trigger`
- `reason`

---

## weekly_reports/

Directory of PDF archive files.

- filename format: `week_YYYY-MM-DD.pdf`
- date should represent the Monday of that training week
- content should follow [report-template.md](report-template.md)
- keep the saved report compact and summary-only; do not dump raw daily logs, full watch exports, or set-by-set workout transcripts into this archive
- prefer a professional one-page or two-page PDF layout with section cards, clean icons, and compact charts
- include only visuals supported by the requested week's data and hot files; omit visual blocks instead of inventing data
- allow card height or page height to expand when Chinese summary text or the coach verdict needs more room; do not clip or artificially compress those sections
- if a temporary source file is needed during PDF generation, treat it as transient and do not store it as the canonical report archive
- if the runtime does not have native PDF export, prefer a bundled script-based generator over external desktop PDF tools; a local Python runtime cache such as `.pdfgen-venv` is acceptable

---

## Data Access Rules

1. Read `current_status.json` before raw logs for startup and check-ins.
2. Read `cache/progress_summary.json` before raw logs for `/progress`.
3. Read `cache/personal_bests.json` before raw workout logs for PR checks.
4. Day-based commands should prefer the current month file and only open adjacent month files when a date range crosses a month boundary.
5. Do not scan all months unless the user explicitly asks for long-term history.
6. Refresh `current_status.json` and only the relevant cache section or cache file after writes so future reads stay cheap.
7. Do not read `weekly_reports/` for startup, check-ins, or normal day-to-day coaching.
8. Day-based commands may read at most the current month plus `1` adjacent month per domain.
9. `/progress` and `/adjust` may read at most the `3` most recent month files per domain by default.
10. `/report` may read only the month file(s) overlapping the requested report week, usually `1-2` files per domain.
11. If a command-specific access matrix in `SKILL.md` is narrower than these defaults, the narrower rule wins.

## Cache Staleness Rules

Treat hot files and cache files as valid until a concrete reason makes them stale.

`current_status.json` is stale only when:

- `today_date` is not the current local date
- a newer write to food, hydration, sleep, workout, weight, watch, plan, or adjustments occurred after `updated_at`
- the current command needs a snapshot field that is missing

an individual section in `cache/progress_summary.json` is stale only when:

- a newer write affecting that section occurred after `section_updated_at.<section>`
- the requested review period exceeds the stored `source_windows` for that section
- the required summary section is missing
- for `flags`, any dependency section it uses was refreshed after `section_updated_at.flags`

`cache/personal_bests.json` is stale only when:

- workout data changed after `updated_at`
- the exercise being checked is absent from the cache

If a file is not stale, reuse it instead of recomputing it from raw logs.
If one progress-summary section is stale, recompute only that section plus dependent `flags`.

## Data Integrity Rules

1. Append to monthly log arrays instead of overwriting prior history.
2. Only `user_profile.json`, `current_plan.json`, `current_status.json`, and files in `data/cache/` may be overwritten.
3. If a day-based log already has an entry for the same date, update that day's object instead of creating a duplicate.
4. Use the exact enum strings defined above.
5. Use `null` instead of omitting optional numeric fields when a field is known but unavailable.
6. Keep numeric units explicit in key names such as `weight_kg` and `target_ml`.
7. In log files, the calorie field is always keyed as `calories`. Use `calorie_target` only in `user_profile.json`. Never use `kcal` as a JSON key name.
