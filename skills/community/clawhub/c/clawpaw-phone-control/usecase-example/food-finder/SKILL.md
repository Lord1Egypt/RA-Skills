---
name: food-finder
description: Smart nearby food recommendations based on current location, time of day, and weather
metadata: { "openclaw": { "emoji": "🍜" } }
---

# Food Finder

Recommend nearby restaurants based on the user's current location, time of day, and weather conditions.

## Steps

### 1. Get Context

Call `clawpaw_get_context` to get:
- Current time and time period (morning/noon/afternoon/evening/late night)
- Current location coordinates

### 2. Get Weather

Call `clawpaw_weather` (using current coordinates, forecast=false) for real-time weather.
Note the weather condition and temperature for recommendation adjustments.

### 3. Choose Food Category

Select search keywords based on time of day:

| Period | Time Range | Category | Keywords |
|--------|-----------|----------|----------|
| Breakfast | 06:00-09:00 | Breakfast spots | 早餐 |
| Lunch | 11:00-13:30 | Full meals | 午餐 |
| Afternoon tea | 14:00-17:00 | Coffee, desserts | 咖啡厅 |
| Dinner | 17:30-20:00 | Full meals | 餐厅 |
| Late night | 20:00-02:00 | Late-night eats | 夜宵 |
| Other | 02:00-06:00 | 24h restaurants | 24小时餐饮 |

If the user mentions a specific cuisine (e.g. "hotpot", "coffee"), prioritize their preference over time-based defaults.

### 4. Search Nearby

Call `clawpaw_nearby` with:
- `longitude` / `latitude`: from context
- `keywords`: based on time period (or user preference)
- `poi_type`: 餐饮
- `radius`: adjust by weather
  - Rain/snow/extreme weather → 500
  - Normal weather → 1000
  - User has transport → 2000
- `limit`: 10

### 5. Output Recommendations

Pick the TOP 5 results and format:

```
🍜 Based on your location and the time of day, here are some picks:

1. **Restaurant Name** — XXm away
   ⭐ X.X | 💰 ¥XX avg | 📞 phone
   💡 [Reason tied to weather/time, e.g. "A warm bowl of soup on a rainy day"]

2. ...
```

Recommendation reasons should feel contextual:
- Rainy → "Close by, just X min walk"
- Cold → "Hot food to warm you up"
- Hot → "Air-conditioned, great for cooling off"
- Late night → "Open late, perfect for a midnight snack"

## When to Use

- User expresses hunger ("I'm hungry", "starving")
- User asks what to eat ("what should I eat", "any food nearby")
- User asks about nearby restaurants ("any good restaurants around here")
- User mentions a specific food type ("I want hotpot", "coffee shop nearby")

## When NOT to Use

- User is asking for a recipe or cooking instructions
- User specifies a different address (not their current location)
- User is discussing nutrition or dietary health topics
