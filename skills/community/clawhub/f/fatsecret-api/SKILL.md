---
name: fatsecret-api
description: Search foods, look up nutrition, log meals, track weight, browse recipes, and manage exercises via the FatSecret API.
version: 1.0.1
homepage: https://github.com/ivanvmoreno/fatsecret-skill
metadata:
  clawdbot:
    requires:
      env:
        - FATSECRET_CLIENT_ID
        - FATSECRET_CLIENT_SECRET
      bins:
        - python3
    primaryEnv: FATSECRET_CLIENT_ID
    emoji: "\U0001F34E"
    files:
      - "scripts/*"
---

# FatSecret API Skill

## What it does

Use this skill when the user wants to:

- Search for foods or get nutritional information
- Look up a food by barcode
- Log food diary entries (create, edit, delete, copy)
- View daily or monthly food diary summaries
- Create and manage saved meals
- Search or browse recipes
- View or log exercises
- Track weight
- Manage a FatSecret user profile

All operations go through the FatSecret REST API via a Python helper script bundled with this skill.

## Prerequisites

1. The `pyfatsecret` Python package must be installed: `pip install pyfatsecret`
2. Environment variables must be set:
   - `FATSECRET_CLIENT_ID` — OAuth 2.0 client ID from https://platform.fatsecret.com/api/
   - `FATSECRET_CLIENT_SECRET` — OAuth 2.0 client secret

## How to run commands

Every operation is a single command:

```
python3 <skill-dir>/scripts/fs_runner.py <command> [--param value ...]
```

The script prints JSON to stdout on success and exits non-zero with an error message on failure.

## Available operations

### Food search and lookup

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `foods_search` | `--query TEXT` | `--page INT`, `--max INT`, `--region`, `--language` | Search the food database |
| `foods_autocomplete` | `--expression TEXT` | `--max INT`, `--region` | Get autocomplete suggestions |
| `food_get` | `--food_id ID` | | Get detailed nutrition for a food |
| `food_get_v2` | `--food_id ID` | `--region`, `--language` | Get detailed nutrition (v2) |
| `food_find_id_for_barcode` | `--barcode TEXT` | `--region`, `--language` | Find a food by its GTIN-13 barcode |

**Example — search foods:**

```
python3 scripts/fs_runner.py foods_search --query "chicken breast"
```

**Example — get nutrition for a specific food:**

```
python3 scripts/fs_runner.py food_get --food_id 4384
```

### Food favorites (delegated)

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `food_add_favorite` | `--food_id ID` | `--serving_id`, `--number_of_units` | Add a food to favorites |
| `food_delete_favorite` | `--food_id ID` | `--serving_id`, `--number_of_units` | Remove a food from favorites |
| `foods_get_favorites` | | | List favorite foods |
| `foods_get_most_eaten` | | `--meal` | List most eaten foods |
| `foods_get_recently_eaten` | | `--meal` | List recently eaten foods |

### Food diary (delegated)

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `food_entry_create` | `--food_id`, `--food_entry_name`, `--serving_id`, `--number_of_units`, `--meal` | `--date YYYY-MM-DD` | Log a food diary entry |
| `food_entry_edit` | `--food_entry_id` | `--food_entry_name`, `--serving_id`, `--number_of_units`, `--meal` | Edit a food diary entry |
| `food_entry_delete` | `--food_entry_id` | | Delete a food diary entry |
| `food_entries_get` | | `--food_entry_id` or `--date YYYY-MM-DD` | Get food diary entries |
| `food_entries_get_month` | | `--date YYYY-MM-DD` | Get monthly food diary summary |
| `food_entries_copy` | `--from_date YYYY-MM-DD`, `--to_date YYYY-MM-DD` | `--meal` | Copy entries between dates |
| `food_entries_copy_saved_meal` | `--saved_meal_id`, `--meal` | `--date YYYY-MM-DD` | Copy a saved meal to the diary |

**Example — log breakfast:**

```
python3 scripts/fs_runner.py food_entry_create --food_id 4384 --food_entry_name "Chicken Breast" --serving_id 25381 --number_of_units 1.0 --meal breakfast
```

### Saved meals (delegated)

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `saved_meal_create` | `--saved_meal_name` | `--saved_meal_description`, `--meals` | Create a saved meal |
| `saved_meal_delete` | `--saved_meal_id` | | Delete a saved meal |
| `saved_meal_edit` | `--saved_meal_id` | `--saved_meal_name`, `--saved_meal_description`, `--meals` | Edit a saved meal |
| `saved_meal_get` | | `--meal` | List saved meals |
| `saved_meal_item_add` | `--saved_meal_id`, `--food_id`, `--saved_meal_item_name`, `--serving_id`, `--number_of_units` | | Add item to saved meal |
| `saved_meal_item_delete` | `--saved_meal_item_id` | | Delete saved meal item |
| `saved_meal_item_edit` | `--saved_meal_item_id` | `--saved_meal_item_name`, `--number_of_units` | Edit saved meal item |
| `saved_meal_items_get` | `--saved_meal_id` | | List items in a saved meal |

### Recipes

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `recipes_search` | `--query TEXT` | `--recipe_type`, `--page INT`, `--max INT` | Search recipes |
| `recipe_get` | `--recipe_id ID` | | Get recipe details |
| `recipe_types_get` | | | List all recipe types |
| `recipes_add_favorite` | `--recipe_id ID` | | Add recipe to favorites |
| `recipes_delete_favorite` | `--recipe_id ID` | | Remove recipe from favorites |
| `recipes_get_favorites` | | | List favorite recipes |

**Example — search recipes:**

```
python3 scripts/fs_runner.py recipes_search --query "low carb dinner"
```

### Exercises (delegated)

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `exercises_get` | | | List all exercise types |
| `exercise_entries_get` | | `--date YYYY-MM-DD` | Get exercise entries for a day |
| `exercise_entries_get_month` | | `--date YYYY-MM-DD` | Get monthly exercise summary |
| `exercise_entries_commit_day` | | `--date YYYY-MM-DD` | Save default exercises for a day |
| `exercise_entries_save_template` | `--days BITS` | `--date YYYY-MM-DD` | Save exercise day as template |
| `exercise_entry_edit` | `--shift_to_id`, `--shift_from_id`, `--minutes` | `--date`, `--shift_to_name`, `--shift_from_name`, `--kcal` | Edit exercise entry |

### Profile (delegated)

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `profile_create` | | `--user_id` | Create a new profile |
| `profile_get_auth` | `--user_id` | | Get auth info for a user |

### Weight (delegated)

| Command | Required params | Optional params | Description |
|---|---|---|---|
| `weight_update` | `--current_weight_kg FLOAT` | `--date`, `--weight_type`, `--height_type`, `--goal_weight_kg`, `--current_height_cm`, `--comment` | Record weight |
| `weights_get_month` | | `--date YYYY-MM-DD` | Get monthly weight log |

**Example — log weight:**

```
python3 scripts/fs_runner.py weight_update --current_weight_kg 75.5
```

## Output format

- The script always prints JSON to stdout.
- Summarize the JSON for the user in a readable way (e.g. a table of foods with calories, a confirmation message for diary entries).
- When returning food nutrition, highlight: calories, fat, carbs, protein, and serving size.

## Guardrails

- Never fabricate food IDs, serving IDs, entry IDs, or nutritional values. Always look them up first.
- Before creating or deleting diary entries, confirm the action with the user.
- Before deleting saved meals or favorites, confirm with the user.
- Prefer read-only operations (search, get) unless the user explicitly asks to create, edit, or delete.
- Profile-scoped operations (diary, favorites, exercises, weight) require a profile to be created first via `profile_create`.

## Failure handling

- If the script exits non-zero, show the error message to the user.
- Common errors:
  - **Code 2**: "Requires authenticated session" — delegated credentials are missing.
  - **Code 101–108**: Parameter error — a required parameter is missing or invalid.
  - **Code 201–207**: Application error — contact FatSecret support.
- If a search returns no results, tell the user and suggest refining the query.
- If a date is required but not provided, ask the user which date they mean.

## External endpoints

| Endpoint | Method | Data sent |
|---|---|---|
| `https://platform.fatsecret.com/rest/v2/server.api` | POST | OAuth 2.0 bearer-token authorized requests: method name, search terms, food/recipe/entry IDs, dates, serving sizes, weight values. No raw user content beyond search queries. |
| `https://oauth.fatsecret.com/connect/token` | POST | OAuth 2.0 client credentials grant (client_id, client_secret) to obtain access tokens. |

No other endpoints are contacted. All network calls are made by the `pyfatsecret` Python package via the `requests` library.

## Security and privacy

- **What leaves the machine**: Search queries, food/recipe/entry IDs, serving sizes, weight values, and OAuth 2.0 credentials are sent to `platform.fatsecret.com` and `oauth.fatsecret.com` over HTTPS.
- **What stays local**: The script reads environment variables for credentials and prints JSON to stdout. No data is written to disk. No data is sent to any service other than FatSecret.
- **Credentials**: Client ID/secret are read from environment variables only. They are never logged or printed.
- **Shell safety**: The script is pure Python using the `requests` library. There is no shell expansion or interpolation of user input.

## Model invocation note

This skill may be invoked autonomously by the agent when it determines the user's request matches the skill's capabilities (food search, nutrition lookup, diary management, etc.). This is standard OpenClaw behavior. To disable autonomous invocation, configure the skill as manual-only in your OpenClaw settings.

## Trust statement

By using this skill, food-related queries and diary data are sent to the **FatSecret API** (`platform.fatsecret.com`) over HTTPS. Only install this skill if you trust the FatSecret platform with your nutritional and health data. Review the [FatSecret API Terms of Use](https://platform.fatsecret.com/api/Default.aspx?screen=rapisd) before use.
