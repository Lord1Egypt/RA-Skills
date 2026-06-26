---
name: cookbook
description: >
  Recipe search skill. Searches a curated recipe database scraped from
  101 Cookbooks (vegetarian) and Omnivore's Cookbook (Chinese how-tos & recipes).
  Use when the user asks to find a recipe, search for dishes by ingredient or
  cuisine, or browse cooking techniques and how-to guides.
---

# Cookbook Skill — Recipe Search

## Overview

This skill searches a Markdown recipe database (`recipes.md`) built from two sources:

| Source | Focus |
|--------|-------|
| [101 Cookbooks](https://www.101cookbooks.com/vegetarian_recipes) | Vegetarian recipes (soups, salads, pasta, mains, burgers, snacks) |
| [Omnivore's Cookbook](https://omnivorescookbook.com/category/how-tos/) | Chinese how-to guides, stir-fries, noodles, rice, soups, sauces |

## Database File

Location (relative to this skill):
```
recipes.md
```


## Search Procedure

### Step 1 — Read the Database

Read `recipes.md` with the `read` tool:

```
file_path: .openclaw\workspace\skills\cookbook\recipes.md
```

### Step 2 — Parse & Match

Search the loaded content for recipes matching the user's query. Match against:
- **Title** — exact and partial keyword matches
- **Brief** — ingredient and technique mentions
- **Source** — filter to 101cookbooks or omnivorescookbook if user specifies
- **Category** — soups, salads, pasta, mains, burgers, stir-fry, noodles, rice, how-tos, sauces, etc.

### Step 3 — Present Results

Return matched recipes as a formatted list:

```
### [Recipe Title](URL)
> Brief description of the recipe.
```

If more than 8 matches: show the top 8 most relevant, offer to show more.
If no matches: say so clearly and suggest related categories.

## Example Queries & Behavior

| User says | Action |
|-----------|--------|
| "find a chickpea recipe" | Search briefs & titles for "chickpea" |
| "vegetarian soup ideas" | Filter 101cookbooks section, category Soups |
| "how do I make dumplings" | Match how-to guides for "dumpling" |
| "stir fry vegetables" | Return stir-fry category from Omnivore's |
| "quick 20-minute dinner" | Match briefs mentioning "quick", "20-minute", "fast" |
| "noodle recipes" | Return all noodle & pasta entries |
| "Chinese cooking basics" | Return all Omnivore's how-to guides |

## Formatting Rules

- Always include clickable URL links
- Show source site in parentheses: *(101 Cookbooks)* or *(Omnivore's Cookbook)*
- Group results by category when multiple categories match
- For how-to guides, label them with 📖 Guide badge
- For recipes, use 🍽️ Recipe badge

## Updating the Database

To add new recipes, append entries to `recipes.md` following the existing table format:

```markdown
| Title | Brief description of the recipe. | https://url-to-recipe |
```

To add a new source section, create a new `## Source:` heading with category subsections.
