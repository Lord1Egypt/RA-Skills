# Templates — economy-flights

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞到哪里？" (Priority 2)
Both missing → "您从哪个城市出发，飞到哪里？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Default: tomorrow. Tell user: "默认查明天的经济舱航班"
Missing seat-class-name → Default: economy (always for this skill)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about cabin class — economy-flights implies seat-class-name=economy

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "economy-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "seat_class_name": "economy",
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
## ✈️ Economy Flights: {origin} → {destination}

**Cheapest: ¥{price} on {airline}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

💡 **Tip:** Mid-week flights are often 20-40% cheaper than weekends.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Economy Flights: {origin} → {destination}

No economy seats found for {date}.

**Tried:**
- ✅ Searched with seat-class=economy → 0 results
- ✅ Removed seat-class filter → {count} flights available

**Suggestions:**
1. Try flexible dates (±3 days)
2. Check nearby airports
3. Consider connecting flights
```

### 3.3 CLI Failed

```markdown
## ✈️ Economy Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --seat-class-name economy --sort-type 3`

Real-time data requires a working flyai-cli.
```
