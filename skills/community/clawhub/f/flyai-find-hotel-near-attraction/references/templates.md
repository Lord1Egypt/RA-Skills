# Templates — flyai-find-hotel-near-attraction

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required
```
Missing POI → "Which attraction do you want to stay near?"
Missing city (POI ambiguous) → "Which city's {POI}? (e.g., Hangzhou West Lake or Yangzhou?)"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dates → Default: tonight in, tomorrow out. Tell user.
Missing stars/budget → Don't ask. Show all, sorted by distance.
```

### Rules
- ❌ Never ask "hotel or homestay?" (show all types)
- ❌ Never ask room type (distance is the priority, not room config)

---

## 2. Internal State

```json
{
  "skill": "flyai-find-hotel-near-attraction",
  "params": {
    "city": "",
    "poi_name": "",
    "check_in_date": "",
    "check_out_date": "",
    "sort": "distance_asc",
    "hotel_stars": null,
    "max_price": null,
    "hotel_types": null
  },
  "poi_context": {
    "official_name": "",
    "category": "",
    "ticket_price": null,
    "detail_url": ""
  },
  "state": "collecting | verifying_poi | searching_hotels | formatting | validating"
}
```

---

## 3. Output Templates

### 3.1 Standard Result (POI + Hotels)

```markdown
## 🏨 Hotels Near {poi_name}

📍 **{poi_official_name}** ({category}) · {city}
🎫 Tickets: ¥{price} · [Buy]({poi_detailUrl})

Closest hotel: **{hotel_name}** ({distance}), ¥{price}/night.

| # | Hotel | ⭐ Stars | 📏 Distance | 💰 Price/Night | 📊 Rating | 📎 Book |
|---|-------|---------|-------------|---------------|----------|---------|
| 1 | {name} | ⭐⭐⭐⭐⭐ | 5 min walk | ¥{price} | {rating} | [Book]({detailUrl}) |
| 2 | {name} | ⭐⭐⭐⭐ | 12 min walk | ¥{price} | {rating} | [Book]({detailUrl}) |
| 3 | {name} | ⭐⭐⭐ | 8 min drive | ¥{price} | {rating} | [Book]({detailUrl}) |

💡 **Tip:** {context_tip_by_poi_type}

---
🏨 Powered by flyai · Real-time pricing, click to book
```

### 3.2 POI Not Found

```markdown
## 🏨 Hotel Search

Could not find "{poi_name}". Did you mean:
1. **{similar_1}** ({city_1})
2. **{similar_2}** ({city_2})

Tell me which one, and I'll find nearby hotels.
```

### 3.3 Few Hotels Near POI

```markdown
## 🏨 Hotels Near {poi_name}

Only {count} hotel(s) found near {poi_name}. 

**Near {poi_name} ({count}):**
| ... |

**Expanded to {city} city center ({count2} more):**
| ... |

💡 Limited lodging near this area. City center is ~{time} drive away.
```
