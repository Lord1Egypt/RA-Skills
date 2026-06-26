# Templates — flyai-plan-japan-travel

> Follow user's language. All `{variables}` must be filled from CLI output, not training data.

## 1. Parameter Collection SOP

### Single-Point Query
```
→ No questions needed. Execute matching CLI command directly.
  "Flights to Tokyo" → search-flight
  "Kyoto hotels" → search-hotels
  "What to do in Osaka" → search-poi
  "Japan visa" → fliggy-fast-search
```

### Full Itinerary
```
Ask (max 3 questions, all at once):
"Let me plan your Japan trip! A few things first:
 1. Where are you departing from?
 2. When are you going, and for how many days?
 3. Any specific cities or activities you want?"

Defaults for unmentioned params:
  Budget → don't ask, search all price ranges, show prices
  Interests → search poi-level 5 (top attractions), don't guess
  City preference → ASK, do not assume a route
```

### Rules
- ❌ Never ask > 3 questions
- ❌ Never start outputting before collecting origin + dates
- ❌ Never assume a "classic route" — route must be based on CLI availability

---

## 2. Internal State

```json
{
  "skill": "flyai-plan-japan-travel",
  "query_type": "single_point | full_plan",
  "params": {
    "origin_city": "",
    "destinations": [],
    "dep_date": "",
    "trip_days": null,
    "interests": []
  },
  "execution_plan": [
    { "step": "visa", "status": "pending" },
    { "step": "flight_out", "status": "pending" },
    { "step": "flight_return", "status": "pending" },
    { "step": "hotel_city1", "status": "pending" },
    { "step": "poi_city1", "status": "pending" }
  ],
  "state": "collecting | executing | formatting | validating"
}
```

---

## 3. Output Templates

### 3.1 Full Itinerary

```markdown
## 🇯🇵 Japan {days}-Day Itinerary

**Route:** {City A} → {City B} → {City C} · Budget: ~¥{total}/person

### 📋 Preparation
| Item | Details |
|------|---------|
| ✈️ Outbound | {origin}→{dest} ¥{price} · {airline} {no} · [Book]({detailUrl}) |
| ✈️ Return | {dest}→{origin} ¥{price} · {airline} {no} · [Book]({detailUrl}) |
| 📄 Visa | {from CLI output} |
| 🚄 Transport | {enrichment: JR Pass / IC card if multi-city} |

---

### Day {N} · {City} — {Theme}

🏨 **Hotel:** {name} ⭐{stars} ¥{price}/night · [Book]({detailUrl})

| Time | Activity | Details |
|------|----------|---------|
| AM | {poi_name} | {category} · [Tickets]({detailUrl}) |
| PM | {poi_name} | {category} · [View]({detailUrl}) |
| Eve | {activity} | {enrichment tip} |

---

### 💡 Tips
1. 🌸 **Season:** {seasonal note from domain knowledge}
2. 🚄 **Transport:** {transport tip}
3. 🏛️ **Culture:** {cultural tip}

---
🇯🇵 Powered by flyai · Real-time pricing, click to book
```

### 3.2 Single-Point: Flights

```markdown
## ✈️ {origin} → {destination}

**Lowest ¥{min}** ({airline} {no})

| # | Airline | Flight | Dep→Arr | 💰 Price | 📎 Book |
|---|---------|--------|---------|----------|---------|
| 1 | {airline} | {no} | {dep}→{arr} | ¥{price} | [Book]({detailUrl}) |

---
✈️ Powered by flyai
```

### 3.3 Single-Point: Attractions

```markdown
## 🇯🇵 {city} Attractions

| # | Name | Category | 📎 Details |
|---|------|----------|-----------|
| 1 | {name} | {category} | [View]({detailUrl}) |

---
🇯🇵 Powered by flyai
```

### 3.4 CLI Failed

```markdown
## 🇯🇵 Japan Travel

⚠️ Could not retrieve real-time data: {error}

**Tried:** {fallback attempts}

**Next steps:**
- Check network connection
- Run manually: `flyai fliggy-fast-search --query "{query}"`

Real-time data and booking links require a working flyai-cli.
```
