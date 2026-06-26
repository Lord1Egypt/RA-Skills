---
name: cook-like-hoc
description: >
  Search and display recipes from the open-source Gar-b-age/CookLikeHOC repository. 
  Use when the user asks to "cook like hoc", "像老乡鸡那样做饭", "老乡鸡菜谱", "做菜", or wants to find a specific recipe from the CookLikeHOC database.
---

# CookLikeHOC Skill

This skill allows you to retrieve recipe instructions from the [CookLikeHOC](https://github.com/Gar-b-age/CookLikeHOC) repository. It contains recipes from the "老乡鸡菜品溯源报告".

## Prerequisites

- Python 3 installed
- Built-in `urllib` and `json` modules (no external libraries required)

## Workflows

### 1. Searching for a Recipe

When the user asks for a recipe or wants to know how to cook a dish from the CookLikeHOC database, run the `search_recipe.py` script.

**Command:**
```bash
python ~/.agents/skills/cook-like-hoc/scripts/search_recipe.py "<Recipe Name>"
```

*Example:*
```bash
python ~/.agents/skills/cook-like-hoc/scripts/search_recipe.py "肥肠鸡"
```

## How to handle the output
- The Python script performs fuzzy matching. It will return the markdown recipe for the exact or closest match.
- Output the recipe to the user, formatting it cleanly as markdown.
- If it says `Could not find any recipe matching`, inform the user that the recipe isn't in the database and perhaps suggest one from the provided examples.

## Supported categories & recipes
The repository has categories like 主食 (Staple Food), 炒菜 (Stir-fried), 汤 (Soup), 炖菜 (Stew), 炸品 (Fried), 烤类 (Roasted), 烫菜 (Blanched), 煮锅 (Boiled Pots), 砂锅菜 (Casserole), 蒸菜 (Steamed), 配料 (Ingredients), and 饮品 (Drinks). The script searches across all markdown files in these categories automatically.
