# Templates — business-flights

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
Missing dep-date → Default: tomorrow. Tell user: "默认查明天的商务舱航班"
Missing seat-class-name → Default: business (always for this skill)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about cabin class — business-flights implies seat-class-name=business

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "business-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "seat_class_name": "business",
    "sort_type": "4"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Business Class Flights: {origin} → {destination}

**Fastest business class: ¥{price} on {airline}, {duration}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

💡 **Tip:** Business class includes priority boarding, extra legroom, and often lounge access.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Business Class Flights: {origin} → {destination}

No business class seats found for {date}.

**Tried:**
- ✅ Searched all flights with seat-class=business → 0 results
- ✅ Checked economy availability → {count} options

**Suggestions:**
1. Try a different date
2. Consider economy class on this route
3. Check first class availability
```

### 3.3 CLI Failed

```markdown
## ✈️ Business Class Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --seat-class-name business --sort-type 4`

Real-time data requires a working flyai-cli.
```
