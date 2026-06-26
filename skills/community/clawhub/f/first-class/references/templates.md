# Templates — first-class

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
Missing dep-date → Default: tomorrow. Tell user: "默认查明天的头等舱航班"
Missing seat-class-name → Default: first (always for this skill)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about cabin class — first-class implies seat-class-name=first

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "first-class",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "seat_class_name": "first",
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
## ✈️ First Class Flights: {origin} → {destination}

**Best first class: ¥{price} on {airline}**

| # | Flight | Departs | Arrives | Aircraft | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {aircraft} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {aircraft} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {aircraft} | ¥{price} | [Book]({detailUrl}) |

💡 **Tip:** First class includes lounge access, priority boarding, and lie-flat seats on most wide-body aircraft.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ First Class Flights: {origin} → {destination}

No first class seats found for {date}.

**Tried:**
- ✅ Searched all flights with seat-class=first → 0 results
- ✅ Checked business class availability → {count} options

**Suggestions:**
1. Try a different date
2. Consider business class on this route
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ First Class Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --seat-class-name first --sort-type 2`

Real-time data requires a working flyai-cli.
```
