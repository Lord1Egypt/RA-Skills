# Templates — border-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞往哪个国家/城市？" (Priority 2)
Both missing → "请告诉我出发城市和目的地国家？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "哪天出发？"
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: none (show all)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Remind about visa: "出境请确认目的地签证要求"
- ✅ Suggest international hubs: "国际出发主要口岸：北京、上海、广州、深圳"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "border-flight",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
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
## ✈️ International Flights: {origin} → {destination}

**Best international route: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | Type | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | Direct | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | Connect | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | Direct | ¥{price} | [Book]({detailUrl}) |

🛂 **Visa Reminder:** Please verify visa requirements for {destination_country} before booking.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ International Flights: {origin} → {destination}

No international flights found.

**Suggestions:**
1. Try connecting flights via major international hub
2. Check nearby departure airports
3. Expand date range
```

### 3.3 CLI Failed

```markdown
## ✈️ International Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
