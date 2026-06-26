---
name: morning-brief
description: Personalized morning briefing with weather forecast, notification summary, and battery status
metadata: { "openclaw": { "emoji": "🌅" } }
---

# Morning Briefing

Generate a personalized morning briefing that aggregates weather, overnight notifications, and phone status.

## Steps

### 1. Get Current Context

Call `clawpaw_get_context` to get:
- Current time, day of week
- Current location
- Battery level and charging state
- Network status

### 2. Get Weather Forecast

Call `clawpaw_weather` (using current coordinates, forecast=true) for today's forecast.
Extract daytime/nighttime weather, temperature range, and wind.

### 3. Check Overnight Notifications

Call `clawpaw_notification_changes` (hours=12, limit=50) for overnight notification changes.
Group by app (packageName), count new notifications, and flag potentially important ones (calls, messages, work apps).

### 4. Generate Briefing

Structure the output as follows:

```
🌅 Good morning! Today is [Month] [Day], [Weekday]

🌤️ Weather
[Weather condition], [low]°C ~ [high]°C, [wind direction] [wind level]
[Clothing/umbrella advice]

📬 Notifications ([total] new)
- WeChat: X
- Email: X
- [Other app]: X
[Briefly mention any important-looking notifications]

🔋 Phone Status
Battery [XX]%, [charging/not charging]
[If <30%: "Consider charging before heading out"]

📋 Today
[Weekday: "Watch out for commute traffic"]
[Weekend: "Enjoy your day off"]
[Bad weather: "Stay safe if going out"]
```

### Clothing & Travel Advice Logic

- Temp < 5°C → "Bundle up, heavy coat recommended"
- Temp 5-15°C → "A bit chilly, bring a jacket"
- Temp 15-25°C → "Comfortable weather, light layers"
- Temp > 25°C → "Hot day, don't forget sunscreen"
- Rain → "Rain expected, bring an umbrella"
- Strong wind → "Windy today, dress accordingly"

## When to Use

- User greets in the morning ("good morning", "morning", "just woke up")
- User asks about today ("how's today looking", "what's the weather today")
- User requests a briefing ("morning brief", "daily briefing")

## When NOT to Use

- Not morning hours (afternoon/evening) — time period mismatch
- User is asking a single specific question (just weather → use the weather tool directly)
- User is asking about news or current events (this is a personal briefing, not news)
