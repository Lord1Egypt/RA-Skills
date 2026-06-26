# 🍽️ diet-log — OpenClaw Diet Logging & Nutrition Analysis Skill

> Real food nutrition data-powered OpenClaw assistant for logging meals and analyzing 30+ nutrients.

[English](README_EN.md) | [简体中文](README.md)

---

## ✨ Features

- **🔍 Real Nutrition Data**: Built-in database of 1,643 foods across 16 categories
- **📊 Full Nutrient Analysis**: Calories, protein, fat, carbs, fiber, 7 fatty acids, 10 minerals, 13 vitamins
- **🧠 Smart Matching**: Three-level strategy — exact match → similar-type reference → ask for clarification
- **📅 Periodic Statistics**: Daily / weekly / monthly reports with daily breakdowns and reference comparisons
- **💾 Local Storage**: All records saved locally in JSON, privacy-safe, no internet required

---

## 📦 Installation

### Via ClawHub (Recommended)

```bash
clawhub install diet-log
```

### Manual Installation

1. Download or clone this repo
2. Place the `diet-log` folder into your OpenClaw workspace skills directory:
   ```
   ~/.openclaw/workspace/skills/diet-log/
   ```
3. Restart OpenClaw

---

## 🚀 Quick Start

After installation, just chat with OpenClaw:

### Log a Meal

```
I had noodles, an egg, and some greens for breakfast
```

OpenClaw will automatically:
1. Identify food items and query nutrition data
2. Calculate full nutrient breakdown
3. Output a complete nutrition report
4. Save the record locally

### Periodic Statistics

```
Stats for the last 7 days
```

Returns daily breakdowns, period totals, daily averages, and comparison against reference standards.

---

## 📂 Data Files

| File | Description |
| :--- | :--- |
| `references/food_data.json` | Food nutrition database (1,643 items, source: LuckyHookin/foodwake) |
| `references/meal_log.json` | Meal log storage (auto-created on first use) |

---

## 📚 Data Source & License

Food nutrition data from [LuckyHookin/foodwake](https://github.com/LuckyHookin/foodwake) ([Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)).

> ⚠️ Data is a 2020 snapshot from foodwake.com. Values may differ from the latest Chinese food composition tables. This tool is for general nutritional reference only, not for medical diagnosis.

---

## 🤝 Contributing

Issues and Pull Requests are welcome! If you have better food data sources or feature suggestions, feel free to reach out.

---

## 📄 License

Skill code (`SKILL.md`, `scripts/`): [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).

Food nutrition data: [LuckyHookin/foodwake](https://github.com/LuckyHookin/foodwake), licensed under Apache-2.0.
