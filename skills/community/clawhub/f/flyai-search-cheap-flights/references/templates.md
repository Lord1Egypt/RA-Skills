# Templates — flyai-search-cheap-flights

> Follow the user's language. Templates below are in English; output in Chinese if the user writes in Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "Where are you flying from?"
Missing destination → "Where to?"
Both missing → "From where to where?"
```

### Round 2: Enhanced (use defaults if user doesn't state)
```
Missing date → Default: search next 7 days for lowest. Tell user:
  "I'll search the next 7 days for the lowest price. You can also give me a specific date."
Missing budget → Don't ask. Show all results, note "Tell me your budget to filter."
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about cabin class (this skill = cheapest = economy)
- ❌ Never ask about luggage preference

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "flyai-search-cheap-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "dep_date_start": "",
    "dep_date_end": "",
    "max_price": null,
    "sort_type": 3,
    "journey_type": null
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ {origin} → {destination} Cheap Flights

**Lowest ¥{min_price}** ({airline} {flight_no}), highest ¥{max_price}, spread ¥{diff}.

| # | Airline | Flight | Departure→Arrival | Duration | Type | 💰 Price | 📎 Book |
|---|---------|--------|-------------------|----------|------|----------|---------|
| 1 | {airline} | {no} | {dep}→{arr} | {dur} | ✈️ Direct | ¥{price} | [Book]({detailUrl}) |
| 2 | {airline} | {no} | {dep}→{arr} | {dur} | 🔄 via {city}({wait}) | ¥{price} | [Book]({detailUrl}) |
| 3 | {airline} | {no} | {dep}→{arr} | {dur} | ✈️ Direct | ¥{price} | [Book]({detailUrl}) |

💡 **Savings tip:** {tip}

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 Flexible Date Comparison (Step 4 output)

```markdown
### 📅 Price by Date (±3 days)

| Date | Day | Lowest | Airline | vs Original |
|------|-----|--------|---------|-------------|
| {date} | Mon | ¥{price} | {airline} | ¥{diff} cheaper ↓ |
| {date} | Fri | ¥{price} | {airline} | ¥{diff} more ↑ |

💡 **{day} is cheapest**, {percent}% less than {expensive_day}.
```

### 3.3 No Results

```markdown
## ✈️ {origin} → {destination}

No flights found for {date}.

**Tried:**
- ✅ Expanded to ±3 days → {result}
- ✅ Included connecting flights → {result}

**Suggestions:**
1. Try departing from {nearby_city}
2. Consider {alt_date}

Want me to search alternatives?
```
