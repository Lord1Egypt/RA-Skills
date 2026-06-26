---
name: overwork-care
description: Overwork reminder with weather tips and nearby recommendations when staying at office too long
metadata: { "openclaw": { "emoji": "💤" } }
---

# Overwork Care

When the user has been at the office too long, or asks if they should leave, provide a caring reminder with weather info and nearby suggestions.

## Steps

### 1. Check Current State

Call `clawpaw_get_context` to confirm:
- Current location is tagged as COMPANY
- How long the user has been there
- Current time period

If NOT at the office, let the user know they're not in an overwork state.

### 2. Get Weather

Call `clawpaw_weather` (current coordinates, forecast=false) for real-time weather.
Use this for commute advice (umbrella, warm clothes, safety at night).

### 3. Search Nearby Relaxation Spots

Call `clawpaw_nearby` with keywords based on time:

| Time | Keywords | Rationale |
|------|----------|-----------|
| 18:00-20:00 | 餐厅 | Treat yourself to a nice meal |
| 20:00-22:00 | 咖啡厅 奶茶 | Grab a drink to unwind |
| 22:00+ | 夜宵 便利店 | Late-night fuel |

Parameters:
- `radius`: 500 (keep it close)
- `limit`: 3

### 4. Gentle Vibration

A soft nudge to get attention:
```
nodes({ action: "invoke", invokeCommand: "hardware.vibrate", invokeParamsJson: '{"pattern": [0, 200, 200, 200]}' })
```

### 5. Generate Care Message

```
💤 Overwork Reminder

You've been at the office for [X] hours and [Y] minutes. Great work today!

🌤️ Outside: [temp]°C, [weather]
[Umbrella/warmth/safety advice]

🍵 Nearby wind-down spots
1. [Name] — [X]m away, ⭐ [rating]
2. [Name] — [X]m away, ⭐ [rating]
3. [Name] — [X]m away, ⭐ [rating]

Take care of yourself — rest matters ❤️
```

### Tone by Duration

- 8-9 hours: "Nice work today, wrapping up soon?"
- 9-10 hours: "That's a solid day — don't push too hard"
- 10-12 hours: "Over [X] hours — time to call it a day!"
- 12+ hours: "You've been at it for [X] hours. Please head home and rest."

### Weather-Based Advice

- Rain: "It's raining outside, grab an umbrella"
- Cold: "It's chilly out ([X]°C), bundle up"
- Late night: "It's late — be safe on the way home"

## When to Use

- User asks "should I leave?", "am I overworking?", "how long have I been here?"
- Triggered by OVERWORK_ALERT event (stayed at COMPANY beyond threshold)
- User messages late at night while at the office

## When NOT to Use

- User is not at the office
- User explicitly says they don't want to be reminded
- Normal working hours (9:00-18:00, not considered overwork)
