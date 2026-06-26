# Templates — charter-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞往哪个城市？" (Priority 2)
Both missing → "请告诉我出发城市和目的地城市？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "哪天出发？"
Missing journey-type → Default: 1 (direct)
Missing sort-type → Default: 2 (recommended)
Missing seat-class-name → Default: none (show all classes)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about passenger count — CLI does not support it
- ✅ Always remind user: "包机/私人飞机需直接联系航空公司或包机运营商确认"
- ✅ If user mentions return needs → add `--back-date {date}`

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "charter-flight",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "journey_type": "1",
    "sort_type": "2",
    "seat_class_name": ""
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Charter Flights: {origin} → {destination}

**Best charter-compatible option: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | Cabin | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|-------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | {cabin} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | {cabin} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | {cabin} | ¥{price} | [Book]({detailUrl}) |

📋 **Charter Note:** Results shown are scheduled flights. Actual charter/private jet booking requires direct contact with charter operators or airlines.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Charter Flights: {origin} → {destination}

No direct flights found for this route.

**Tried:**
- ✅ Direct flights → 0 results
- ✅ All flights (including connecting) → {count} flights available

**Suggestions:**
1. Try nearby airports
2. Consider connecting flights via major hub
3. Contact charter operator directly for custom routing
```

### 3.3 CLI Failed

```markdown
## ✈️ Charter Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --journey-type 1 --sort-type 2`

Real-time data requires a working flyai-cli.
```
