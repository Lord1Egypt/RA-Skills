# Templates — birthday-trip

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "生日想去哪里？" (Priority 2)
Both missing → "请告诉我出发城市和生日目的地？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "生日是哪天？"
Missing sort-type → Default: 2 (recommended)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest popular birthday destinations: "热门生日旅行：成都、长沙、厦门、三亚"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "birthday-trip",
  "params": { "origin": "", "destination": "", "dep_date": "", "sort_type": "2" },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Birthday Trip Flights: {origin} → {destination}

**Best birthday route: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

🎂 **Birthday Tip:** {destination_suggestion}

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Birthday Trip Flights: {origin} → {destination}

No flights found.

**Suggestions:**
1. Try nearby dates around the birthday
2. Consider connecting flights
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Birthday Trip Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`
```
