# Templates — cargo-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市发货？" (Priority 1)
Missing destination → "运到哪个城市？" (Priority 2)
Both missing → "请告诉我出发城市和目的地城市？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Ask: "哪天发货？"
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: none (show all)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about cargo weight/dimensions — CLI does not support it
- ✅ Always remind user: "实际空运需联系航空公司货运部或货代"
- ✅ Emphasize flight timing for cargo planning: "建议选择早班或夜班航班，货运处理更高效"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "cargo-flight",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "sort_type": "2",
    "journey_type": ""
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Air Cargo Routes: {origin} → {destination}

**Best cargo-compatible flight: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

📦 **Cargo Note:** Results shown are passenger flights. Actual air cargo booking requires contacting the airline cargo department or a freight forwarder.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Air Cargo Routes: {origin} → {destination}

No flights found for this route on the selected date.

**Suggestions:**
1. Try nearby dates
2. Consider connecting flights via major hub
3. Contact freight forwarder for charter cargo options
```

### 3.3 CLI Failed

```markdown
## ✈️ Air Cargo Routes: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`

Real-time data requires a working flyai-cli.
```
