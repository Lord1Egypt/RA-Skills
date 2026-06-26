# fitbuddy 🏋️

**Your AI-powered fitness buddy** — diet logging, weight tracking, exercise recording, hydration monitoring, smart diet strategies, and more.

**你的 AI 健身伙伴** — 饮食记录、体重追踪、运动记录、饮水监控、智能饮食策略等。

---

## ✨ Features / 功能亮点

- 📊 **Food Database** — Log meals by food name + grams, auto-calculate macros from built-in database (35+ foods)
- ⚖️ **Weight Tracking** — Daily weight logging with trend analysis
- 🏃 **Exercise Logging** — Strength training & cardio with calorie estimation
- 💧 **Hydration Tracking** — Water intake with daily target
- 🔄 **Smart Diet Strategies** — Carb cycling, calorie cycling, fixed calories (auto-suggest strategy switches)
- 🧠 **Smart Reminders** — Cron-based reminders that **skip if already logged** (no annoying duplicate pings)
- 🌐 **i18n** — Built-in Chinese/English templates, switchable via profile
- 📈 **Charts & Reports** — Nutrition pie charts, calorie balance, weekly/monthly reports
- 💪 **Motivation** — Emotional support, milestone celebrations, data-driven encouragement
- 🛡️ **Safety Guardrails** — Never recommends extreme diets, caps calorie deficit at 20% TDEE
- 🍔 **McDonald's Integration** — Optional MCP integration for precise nutrition data, smart recommendations, and restaurant diet plans

---

## 🚀 Quick Start / 快速开始

### 1. Installation / 安装

```bash
clawhub install fitbuddy
```

### 2. Initialization / 初始化

Tell your AI assistant anything fitness-related, and it will guide you through setup:

> "帮我初始化 fitbuddy" / "init fitbuddy"

You'll be asked for:
- Height, weight, age, gender
- Goal (cut / maintain / bulk)
- Activity level
- Training schedule
- Diet preferences & budget

### 3. Daily Usage / 日常使用

**Log meals / 记录饮食:**
```
"午餐吃了 鸡胸肉200g+米饭150g"
"Lunch: chicken breast 200g + rice 150g"
```

**Log weight / 记录体重:**
```
"记录体重72.5"
"Logged weight 72.5kg"
```

**Log exercise / 记录运动:**
```
"今天练了 深蹲4×12×60kg 跑步30分钟"
"Did squats 4×12×60kg + running 30min"
```

**Log water / 记录饮水:**
```
"喝了500ml"
"Drank 500ml"
```

**Check progress / 查看进度:**
```
"看看今天的进度"
"Show today's progress"
```

---

## 📁 Directory Structure / 目录结构

```
fitbuddy/
├── SKILL.md              # Skill instructions (for AI agent)
├── scripts/
│   ├── record.py         # Diet/weight/exercise/water recording
│   ├── calc.py           # BMR/TDEE/macro calculations
│   ├── chart.py          # Chart generation (matplotlib)
│   └── init_profile.py   # Profile initialization
├── references/
│   ├── init-guide.md     # Initialization walkthrough
│   ├── nutrition.md      # Nutrition formulas & references
│   ├── nutrition-guide.md # Food estimation guide
│   ├── exercise.md       # Exercise database
│   ├── training-plan.md  # Training plan templates
│   ├── budget-meals.md   # Budget-friendly meal plans
│   ├── channels.md       # Reminder channel config
│   └── reports.md        # Report generation guide
└── fitbuddy-data/
    ├── food-db.json      # Food database (nutrition per 100g)
    ├── i18n.json         # Chinese/English templates
    ├── changelog.json    # Change log
    ├── profile.json      # User profile (auto-generated)
    ├── records/          # Daily records (auto-generated)
    └── charts/           # Generated charts (auto-generated)
```

---

## ⚙️ Configuration / 配置

### Language / 语言

Edit `fitbuddy-data/profile.json`:
```json
{ "language": "zh" }   // Chinese (default)
{ "language": "en" }   // English
```

### Diet Strategies / 饮食策略

| Strategy | Description |
|----------|-------------|
| `carb_cycling` | High carb on training days, low carb on rest days |
| `calorie_cycling` | Alternating high/low calorie days |
| `fixed` | Fixed daily calorie target |

### Smart Reminders / 智能提醒

Reminders are created via OpenClaw cron during initialization:
- ⏰ Weight reminder — daily morning
- 🍳 Meal reminders — before each meal
- 💧 Water reminders — every few hours
- 🏋️ Pre-workout reminder — 1 hour before training

**Smart skip:** If you've already logged a meal, the reminder is automatically skipped. No spam!

**智能跳过：** 如果你已经记录了某餐，对应的提醒会自动跳过，不打扰！

---

## 🛡️ Safety / 安全红线

- Never recommends extreme diets (<1200 kcal for women, <1500 for men)
- Calorie deficit capped at 20% of TDEE
- Fat loss rate ≤ 1kg/week
- All three macronutrients are required
- Conservative advice for medical conditions

---

## 🍔 McDonald's Integration / 麦当劳集成 (Optional)

fitbuddy can integrate with the [McDonald's MCP server](https://open.mcd.cn/mcp) for precise nutrition data.

### Setup / 配置

1. Get your token at 👉 <https://open.mcd.cn/mcp>
2. Configure with mcporter:
```bash
npm install -g mcporter
mcporter config add mcd-mcp "https://mcp.mcd.cn" --header "Authorization=Bearer YOUR_TOKEN"
```
Or manually create `config/mcporter.json`:
```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": { "Authorization": "Bearer YOUR_TOKEN" }
    }
  }
}
```
3. Tell your AI assistant: "启用麦当劳集成"

### Features / 功能
- 📊 Precise nutrition logging — auto-fetch exact macros for McDonald's meals
- 🍽️ Smart recommendations — restaurant options ranked equally with other foods
- 📋 Restaurant diet plans — create McDonald's diet plans aligned with your goals
- 🎫 Promo notifications — opt-in only, defaults OFF

> Full details → [references/mcd-integration.md](references/mcd-integration.md)

---

## 📋 Requirements / 依赖

- **Python 3.8+**
- **matplotlib** — for chart generation (`pip install matplotlib`)
- **OpenClaw** — for cron-based reminders

---

## 📄 License

MIT

---

Made with 💪 by the fitbuddy community
