# Templates — anniversary

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "想去哪里庆祝纪念日？" (Priority 2)
Both missing → "请告诉我出发城市和纪念日目的地？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "纪念日是哪天？"
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: 1 (direct preferred)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest romantic destinations: "热门纪念日目的地：三亚、厦门、大理、巴厘岛"
- ✅ Offer premium option: "纪念日升级商务舱体验更佳"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "anniversary",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "journey_type": "1",
    "sort_type": "2"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Anniversary Flights: {origin} → {destination}

**Best romantic route: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

💕 **Anniversary Tip:** {romantic_suggestion}

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Anniversary Flights: {origin} → {destination}

No flights found.

**Suggestions:**
1. Try nearby dates around your anniversary
2. Consider connecting flights
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Anniversary Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
