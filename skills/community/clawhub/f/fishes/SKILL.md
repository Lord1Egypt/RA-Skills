---
name: fish
description: Search 300 Japan fish & seafood recipes from Cookpad. Use when user asks about fish recipes, seafood dishes, Japanese fish cooking, or wants to find recipes by fish type, cooking method, or ingredient.
---

# 🐟 Japan Fish Recipe Search

Search 300 community-recommended fish & seafood recipes from Cookpad Japan.

## Usage

When the user asks about fish or seafood recipes, use the search script to find matching recipes.

```bash
node SKILL_DIR/search.js <query>
```

### Examples

```bash
# Search by fish type
node SKILL_DIR/search.js salmon
node SKILL_DIR/search.js tuna
node SKILL_DIR/search.js shrimp

# Search by cooking method
node SKILL_DIR/search.js grilled
node SKILL_DIR/search.js simmered
node SKILL_DIR/search.js tempura

# Search by ingredient/flavor
node SKILL_DIR/search.js miso
node SKILL_DIR/search.js butter
node SKILL_DIR/search.js cheese

# Search by Japanese name
node SKILL_DIR/search.js サバ
node SKILL_DIR/search.js エビ

# Search by category
node SKILL_DIR/search.js easy
node SKILL_DIR/search.js bento
node SKILL_DIR/search.js salad

# Combined search (any match)
node SKILL_DIR/search.js salmon grilled
```

### Output Format

Results include recipe title (Japanese), tags, and Cookpad link.

### Data Source

- `recipes.json` — 300 recipes with Japanese titles, English tags, and URLs
- Scraped from: https://cookpad.com/jp/categories/12 (魚介のおかず)
- Date: 2026-04-01

### Search Notes

- Search is case-insensitive
- Matches against both Japanese title and English tags
- Multiple keywords narrow results (AND logic)
- If no results, suggest browsing `japan_fish_recipes.md` for the full categorized list
