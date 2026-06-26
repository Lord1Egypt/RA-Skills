---
name: daily-recipe
description: "Daily recipe recommendation — Chinese, Western, and fusion cuisines on rotation. Full ingredients, step-by-step instructions, 30–60 min home-cook meals."
keywords:
  - 今日食谱
  - 今天吃什么
  - 做什么菜
  - 食谱推荐
  - 每日菜谱
  - 晚餐吃什么
  - 家常菜
  - 菜谱
  - 烹饪
  - 午餐
  - 早餐
  - daily recipe
  - what to cook
  - recipe of the day
  - dinner ideas
  - lunch recipe
  - cooking
  - meal idea
  - home cooking
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Recipe / 今日食谱

Generate a beautiful daily recipe card with bilingual content and step-by-step cooking instructions.

## Workflow

1. **Get today's date** — Use day of week and season to determine cuisine:
   - Mon: Chinese home cooking (家常菜)
   - Tue: Japanese/Korean
   - Wed: Italian/Mediterranean
   - Thu: Southeast Asian (Thai/Vietnamese)
   - Fri: American/Mexican
   - Sat: French/European fine dining (simplified)
   - Sun: Brunch/Baking special
   - Season affects ingredients: light/cold dishes in summer, warm/hearty in winter.
2. **Select a dish** — Use `web_search` to find a specific recipe that fits today's theme. Query: `"easy [cuisine] recipe [season]"`. Pick something achievable in 30-60 min.
3. **Format the recipe** — Ingredients list, step-by-step instructions, cooking tips. All bilingual.
4. **Generate the visual** — Create a single-file HTML artifact.

## Visual Design Requirements

Create a food-magazine quality recipe page:

- **Layout**: Full-page editorial style. Hero section with dish name and description, then ingredients sidebar + steps main column.
- **Typography**: Warm, editorial fonts (e.g., Playfair Display for titles, Nunito for body). Food should feel inviting.
- **Color scheme**: Warm, appetizing palette — terracotta, olive, cream, warm brown. Or fresh palette for salads/light dishes — mint, white, light yellow. Rotate based on dish type.
- **Recipe header**: Dish name (EN + CN, large), cuisine tag, prep time, cook time, servings, difficulty (1-3 🔥).
- **Ingredients**: Clean list with checkboxes (interactive — click to mark as gathered). Quantities in both metric and imperial.
- **Steps**: Numbered steps with clear formatting. Key actions bolded. Timer suggestions noted.
- **Tips section**: Chef's tips, substitution suggestions, storage advice.
- **Nutrition estimate**: Approximate calories, protein, carbs, fat per serving in a small info box.
- **Ad-ready zone**: `<div id="ad-slot-sidebar">` in the ingredients column area. `<div id="ad-slot-bottom">` after the recipe.
- **Footer**: "Powered by ClawCode"

## Content Guidelines

- Recipes should be achievable by home cooks (not restaurant-level complexity)
- Always include vegetarian substitution where possible
- Chinese dishes should include authentic ingredients with common substitutes noted
- Keep ingredient lists under 15 items
- Steps should be clear and numbered (8-12 steps max)

## Output

Save as `/mnt/user-data/outputs/daily-recipe.html` and present to user.

---

## 推送管理

```bash
# 开启每日推送（早晚各一次）
node scripts/push-toggle.js on <userId>

# 自定义时间和渠道
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 20:00 --channel feishu

# 关闭推送
node scripts/push-toggle.js off <userId>

# 查看推送状态
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`
