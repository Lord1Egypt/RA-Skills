---
name: food-travel
description: Plan food-driven travel experiences — recommend best cities for a dish or cuisine, generate city food maps with meal-by-meal restaurant routes, and build complete food-centric itineraries with flights, hotels, and dining schedules. Use when the user asks about food travel, food trips, eating tours, food guides, must-eat dishes, restaurant recommendations for travel, or phrases like "我想吃烤鸭去哪", "成都美食攻略", "3天吃遍西安", "周末广州美食游", "为了吃去旅行", "plan a food trip".
---

# food-travel — Eat-First Travel Planner

> **One-liner**: Input a dish, a craving, or a city — get a complete travel plan built around eating.

This skill solves the full "eat → where → go → stay → route" chain for food lovers.

## Scenario Detection

Identify which scenario the user wants, then follow the corresponding workflow:

| Trigger pattern | Scenario | Example |
|----------------|----------|---------|
| A dish/cuisine + no city | **A: Pick a destination** | "我想吃烤鸭" "想吃海鲜去哪" |
| A city + food intent | **B: City food map** | "成都有什么好吃的" "杭州美食攻略" |
| A city + duration + food intent | **C: Full itinerary** | "3天吃遍西安" "周末广州美食游" |

If unclear, ask the user to clarify.

---

## Scenario A: Pick a Destination for Food

**Input**: a dish, cuisine, or flavor preference
**Output**: best city recommendation + food list + travel logistics

### Steps

1. **Web search**: `"{dish/cuisine} 最正宗 去哪个城市吃"` to identify the top 2-3 cities.
2. **For each city, web search**: `"{city} 必吃 {dish} 餐厅推荐"` to get restaurant data.
3. **Search flights** (if user provides origin):
   ```bash
   flyai search-flight --origin "{origin}" --destination "{city}" --dep-date {date}
   ```
4. **Search hotels**:
   ```bash
   flyai search-hotel --dest-name "{city}" --check-in-date {date} --check-out-date {date}
   ```

### Output format

```
# 为了{dish}，去{city}！

## 为什么选{city}
（One-paragraph reason）

## 必吃清单

| 餐厅 | 招牌菜 | 人均 | 地址 | 推荐理由 |
|------|--------|------|------|----------|
| ...  | ...    | ...  | ...  | ...      |

## 怎么去
（Flight options table with booking links）

## 住哪里
（Hotel options near food districts, with booking links）
```

---

## Scenario B: City Food Map

**Input**: a city name
**Output**: meal-by-meal restaurant map organized by time of day

### Steps

1. **Web search**: `"{city} 必吃餐厅推荐"` + `"{city} 特色小吃 推荐"` + `"{city} 夜宵 推荐"`.
2. **Organize** results into 4 time slots: 早餐, 午餐, 晚餐, 夜宵/下午茶.
3. **keyword-search supplement**:
   ```bash
   flyai keyword-search --query "{city} 美食券 餐厅"
   ```
   Filter for food-related items only.

### Output format

```
# {city}美食地图

## 🌅 早餐
| 餐厅 | 推荐 | 人均 | 地址 |
|------|------|------|------|

## ☀️ 午餐
...

## 🌆 晚餐
...

## 🌙 夜宵
...

## 可预订美食产品
（Filtered keyword-search results with images and booking links）

> 餐厅数据来自网络搜索，美食券来自 fly.ai 实时结果。
```

---

## Scenario C: Full Food-Driven Itinerary

**Input**: city + duration (e.g. "3天吃遍西安")
**Output**: day-by-day schedule with every meal planned + attractions between meals + transport + hotel

### Steps

1. **Web search**: `"{city} {N}天美食攻略"` + `"{city} 必吃餐厅推荐"`.
2. **Search hotels**:
   ```bash
   flyai search-hotel --dest-name "{city}" --check-in-date {date} --check-out-date {date}
   ```
3. **Search flights** (if origin provided):
   ```bash
   flyai search-flight --origin "{origin}" --destination "{city}" --dep-date {date}
   ```
4. **Search attractions** to fill between-meal time:
   ```bash
   flyai search-poi --city-name "{city}"
   ```
5. **Organize** into a day-by-day plan where every meal is the anchor.

### Output format

```
# {N}天吃遍{city}

## Day 1
### 🌅 早餐 — {restaurant}
- 推荐：{dishes}｜人均：{price}｜地址：{addr}

### ☀️ 上午 — {attraction}（吃完溜达消食）
（POI info with booking link）

### 🍜 午餐 — {restaurant}
- 推荐：{dishes}｜人均：{price}｜地址：{addr}

### 🌆 下午 — {attraction/activity}

### 🔥 晚餐 — {restaurant}
- 推荐：{dishes}｜人均：{price}｜地址：{addr}

### 🌙 夜宵 — {restaurant}
- 推荐：{dishes}

## Day 2
...

## 交通
（Flight options with booking links）

## 住宿
（Hotel options with booking links, prefer hotels near Day 1 dinner area）

## 预算估算
| 项目 | 预估费用 |
|------|----------|
| 机票 | ¥xxx |
| 住宿 | ¥xxx |
| 餐饮 | ¥xxx |
| 门票 | ¥xxx |
| **合计** | **¥xxx** |

> 餐厅数据来自网络搜索，机票酒店来自 fly.ai 实时结果。
```

---

## General Rules

- **Food comes first** — every itinerary section starts with a meal, attractions fill the gaps.
- **Web search for restaurants** — flyai has no restaurant database; always use web search for dining data.
- **flyai for logistics** — use `search-flight`, `search-hotel`, `search-poi`, `keyword-search` for transport, accommodation, attractions, and bookable dining products.
- **Always include booking links** — for every flight, hotel, and POI result, show `[Click to book]({url})`.
- **Always include images** — show `![]({picUrl})` or `![]({mainPic})` when available.
- **Practical details** — include price, address, opening hours when available.
- **Source attribution** — "餐厅数据来自网络搜索，机票酒店来自 fly.ai 实时结果。"
