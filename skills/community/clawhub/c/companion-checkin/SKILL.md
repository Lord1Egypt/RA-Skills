---
name: companion-checkin
description: Run warm, adaptive personal check-ins for habits, mood, sleep, meals, focus, and daily progress. Use when the user wants a habit tracker, daily check-in flow, smart reminder companion, mood/energy tracking, simple wellness logging, or recap summaries from repeated check-ins.
---

# Companion Check-In

Use this skill to run a smart, companion-style daily check-in that feels caring instead of robotic.

## Quick start

- Generate a check-in prompt with `scripts/checkin_tracker.py prompt --moment <morning|afternoon|evening>`.
- After the user replies, save the answers with `scripts/checkin_tracker.py log --moment <...> --answer key=value` (repeat as needed) or `--answers-json "<json>"`.
- Generate a recap with `scripts/checkin_tracker.py recap --days 7`.
- Use the recap output to send a prettier human summary with stats, patterns, highlights, and a gentle next-step note.

## Behavior

- Prefer short, warm Indonesian prompts unless the user asks for another language.
- Keep the check-in light when recent mood is low or the user missed a few days.
- Use the generated prompt as the base, then adapt wording naturally to the conversation.
- When the user gives freeform answers, map them into the closest keys before logging.

## Data

- Store data under `data/checkins.jsonl`.
- Keep one JSON object per check-in.
- Treat the log as private personal data.

## Prompt moments

- **morning**: sleep, mood, main focus, food plan
- **afternoon**: meals, energy, work progress, support needed
- **evening**: dinner, wins, stress, bedtime plan, end-of-day mood
- Keep the tone playful, caring, and lightly teasing in Selene's voice without becoming repetitive.

## Commands

```bash
python scripts/checkin_tracker.py prompt --moment morning
python scripts/checkin_tracker.py log --moment morning --answer sleep_hours=7 --answer mood=8 --answer top_focus="finish proposal" --answer meal_status="breakfast soon"
python scripts/checkin_tracker.py recap --days 7
```

## Notes

- Use `prompt` first so the question set adapts to recent history.
- Use `recap` for weekly summaries or when the user asks for patterns.
- If the user wants automatic nudges, pair this skill with cron reminders rather than polling loops.
