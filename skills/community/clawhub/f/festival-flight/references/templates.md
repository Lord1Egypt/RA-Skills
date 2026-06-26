# Templates — festival-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "节日要去哪里？" (Priority 2)
Both missing → "请告诉我出发城市和节日目的地？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Default: festival date range
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: any (1 or 2)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest popular festival destinations: "热门节日出行：春节返乡、中秋团圆、国庆出游"
- ✅ Note: "节日出行高峰，建议提前预订"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "festival-flight",
  "params": { "origin": "", "destination": "", "dep_date": "", "sort_type": "2" },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Festival Flights: {origin} → {destination}

**Recommended: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

🎉 **Festival Tip:** 节日出行高峰，建议尽早预订！

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Festival Flights: {origin} → {destination}

No flights found for selected dates.

**Suggestions:**
1. Try flexible dates around the festival
2. Consider connecting flights
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Festival Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`
```
