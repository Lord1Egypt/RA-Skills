---
name: diet-record
description: Diet recording skill. Log meals via text description or food photo upload, auto-recognize food items and estimate nutrition/calories. Activate when user sends a food photo, describes what they ate, asks to log a meal, or queries calorie/nutrition info. Triggers include "记录饮食", "午饭吃了", "帮我记一下", "这个多少卡", "拍了张照片", "今天吃了什么", "log my meal", "what did I eat today".
metadata: {"nanobot":{"emoji":"📸"}}
---

# Diet Logger

Record meals via photo or text, auto-recognize food items and calculate nutrition.

## Data Storage

All diet records are stored in `diet-log.jsonl` (same directory as this skill file, one JSON object per line). Create the file if it doesn't exist.

Each record schema:

```json
{
  "id": "uuid",
  "timestamp": "ISO-8601",
  "meal_type": "breakfast|lunch|dinner|snack",
  "items": [
    {
      "name": "食物名称",
      "portion_g": 150,
      "calories_kcal": 230,
      "protein_g": 12,
      "fat_g": 8,
      "carb_g": 28,
      "fiber_g": 2
    }
  ],
  "total_calories": 460,
  "notes": ""
}
```

## User Preferences

Stored in `diet-preferences.json` (same directory as this skill file). Create the file if it doesn't exist.

```json
{
  "photo_auto_log": null,
  "dietary_restrictions": [],
  "allergies": [],
  "disliked_foods": [],
  "favorite_foods": [],
  "diet_goal": null,
  "daily_calorie_target": null,
  "meal_routine": null,
  "notes": ""
}
```

Fields:

- `photo_auto_log`: `true` = auto-log on photo upload, `false` = confirm first, `null` = not yet set.
- `dietary_restrictions`: e.g. `["素食", "清真", "无麸质", "低碳水"]`
- `allergies`: e.g. `["花生", "海鲜", "乳糖不耐"]`
- `disliked_foods`: foods user explicitly dislikes
- `favorite_foods`: frequently eaten or preferred foods
- `diet_goal`: e.g. `"减脂"`, `"增肌"`, `"维持体重"`, `"均衡饮食"`
- `daily_calorie_target`: e.g. `1800` (kcal), `null` if not set
- `meal_routine`: e.g. `"一日三餐"`, `"16:8轻断食"`, `"少食多餐"`
- `notes`: any other dietary habits or notes from user

### Preference Discovery

**Photo auto-log preference**: On the first food photo upload (or when `photo_auto_log` is `null`), recognize items as usual, then ask: "以后发食物照片时，要自动帮你记录饮食吗？还是每次先确认再记录？"

**Dietary habits**: Whenever user mentions dietary preferences, restrictions, allergies, goals, or habits in conversation, extract and save to the corresponding fields. Examples:
- "我对花生过敏" → add `"花生"` to `allergies`
- "我在减脂" → set `diet_goal` to `"减脂"`
- "我不吃香菜" → add `"香菜"` to `disliked_foods`
- "我每天控制在1500卡" → set `daily_calorie_target` to `1500`
- "我在做16:8轻断食" → set `meal_routine` to `"16:8轻断食"`

Preferences are accumulated over time — update individual fields without overwriting unrelated ones. Read preferences before each interaction to provide personalized feedback (e.g. warn if a meal exceeds calorie target, flag allergens in recognized food).

## Workflow

### Photo Input

1. Receive food photo from user
2. Read `diet-preferences.json` to check `photo_auto_log`
3. Analyze the image: identify each food item, estimate portion size
4. Look up nutrition data per item (use the reference table below)
5. If `photo_auto_log` is `null`: present result, ask preference (see above), then log
6. If `photo_auto_log` is `true`: calculate totals, log directly, respond with summary
7. If `photo_auto_log` is `false`: present recognized items — ask user to confirm or correct, then log
8. Append record to `diet-log.jsonl`

### Text Input

1. Parse food description (e.g. "一碗牛肉面加个煎蛋")
2. Break into individual items with estimated portions
3. Look up nutrition and calculate totals
4. Append record

### Daily Summary

When user asks "今天吃了什么" or "daily summary":

```bash
python3 -c "
import json, datetime
today = datetime.date.today().isoformat()
with open('diet-log.jsonl') as f:
    meals = [json.loads(l) for l in f if today in l]
total = sum(m['total_calories'] for m in meals)
print(f'Today: {len(meals)} meals, {total:.0f} kcal')
for m in meals:
    items = ', '.join(i['name'] for i in m['items'])
    print(f\"  {m['meal_type']}: {m['total_calories']:.0f} kcal — {items}\")
"
```

## Nutrition Reference (per 100g)

Common foods for quick lookup (no API needed):

| Food | kcal | Protein | Fat | Carb |
|------|------|---------|-----|------|
| 白米饭 | 116 | 2.6 | 0.3 | 25.9 |
| 面条(煮) | 110 | 3.5 | 0.5 | 22 |
| 鸡胸肉 | 133 | 31 | 1.2 | 0 |
| 鸡蛋(煮) | 144 | 13 | 10 | 1.1 |
| 牛肉(瘦) | 125 | 20 | 4.2 | 0.2 |
| 三文鱼 | 208 | 20 | 13 | 0 |
| 豆腐 | 73 | 8.1 | 3.7 | 1.5 |
| 西兰花 | 34 | 2.8 | 0.4 | 5 |
| 番茄 | 18 | 0.9 | 0.2 | 3.9 |
| 苹果 | 52 | 0.3 | 0.2 | 13.8 |
| 香蕉 | 89 | 1.1 | 0.3 | 22.8 |
| 牛奶(全脂) | 61 | 3.2 | 3.3 | 4.8 |
| 酸奶(原味) | 61 | 3.5 | 3.3 | 4.7 |
| 全麦面包 | 247 | 13 | 3.4 | 41 |
| 燕麦片 | 379 | 13 | 6.5 | 67 |

For unlisted foods, estimate based on similar items or ask the user for specifics.

## Cooking Method Calorie Adjustments

- 清蒸/水煮: baseline
- 炒(少油): +10-15%
- 炒(多油): +20-30%
- 油炸: +30-50%
- 烧烤: -5% (fat drips off)

## Portion Estimation

- 一碗米饭 ≈ 200g
- 一盘菜 ≈ 200-300g
- 一个拳头 ≈ 150g (水果/肉)
- 一汤匙油 ≈ 10g (90 kcal)
- 一杯(240ml)牛奶 ≈ 245g

## Key Rules

- Present results in a clean table format
- When recognition confidence is low, ask user to confirm before logging
- Auto-detect meal_type from time: 06-10 breakfast, 11-14 lunch, 17-20 dinner, else snack
- Remind if daily protein is under 1.2g/kg body weight (when user weight is known)
- Never make moral judgments about food choices
