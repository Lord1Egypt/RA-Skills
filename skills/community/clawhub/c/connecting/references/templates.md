# Templates — connecting

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞到哪里？" (Priority 2)
Both missing → "您从哪个城市出发，飞到哪里？"
```

### Round 2: Enhanced
```
Missing dep-date → Default: tomorrow. Tell user: "默认查明天的中转航班"
Missing transfer-city → Ask: "有没有偏好的中转城市？没有的话我按价格排序"
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Always mention: "中转航班通常比直飞便宜20-50%"

---

## 2. Internal State

```json
{
  "skill": "connecting",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "journey_type": "2",
    "sort_type": "3"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Connecting Flights: {origin} → {destination}

**Cheapest: ¥{price} via {transit_city} on {airline} — {total_duration}**

| # | Flight | Departs | Transit | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {transit} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {transit} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {transit} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

💡 **Tip:** 中转航班通常比直飞便宜20-50%，国内中转建议预留≥90分钟。

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Connecting Flights: {origin} → {destination}

No connecting flights found for {date}.

**Tried:**
- ✅ Searched with journey-type=2 → 0 results
- ✅ Removed journey-type filter → {count} flights available (may include direct)

**Suggestions:**
1. Try direct flights instead
2. Try flexible dates (±3 days)
3. Try different transit cities
```

### 3.3 CLI Failed

```markdown
## ✈️ Connecting Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --journey-type 2 --sort-type 3`

Real-time data requires a working flyai-cli.
```
