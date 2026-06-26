---
name: food-channel
version: 1.0.1
description: Handle messages in a food-tracking channel by routing food intake events through a deterministic food tracker. Use when working in a dedicated food channel, especially for barcode lookups, photo estimates, and daily summaries.
env:
  WORKSPACE:
    description: OpenClaw workspace root path
    required: false
  FOOD_LOG:
    description: Override path for food log CSV
    required: false
  FOOD_CHANNEL_ID:
    description: Channel ID for food tracking
    required: true
  FOOD_PROFILE_PATH:
    description: Path to user profile JSON with daily limits
    required: false
---

# Food Channel Skill

Handle messages in a food-tracking channel by logging food intake events.

## Configuration

Set the following environment variables or replace placeholders before use:
- `FOOD_CHANNEL_ID` — Channel ID for food tracking (env var)
- `FOOD_PROFILE_PATH` — Path to user profile JSON (default: `$WORKSPACE/data/food_profile.json`)
- Tracker script is at `scripts/tracker.py` (included in bundle)

## Message Types

### 1. Barcode Lookup
User sends a barcode (numeric string, 8-14 digits). Optional servings specified as "2x", "2 servings", "x2", etc. Defaults to 1.

**Flow:**
1. Parse the barcode and optional servings from the message
2. Run: `python3 scripts/tracker.py lookup <barcode> [servings]`
3. If successful, reply with a formatted summary of the food item and nutrition logged
4. If failed, reply with the error

### 2. Photo Estimate
User sends an image attachment.

**Flow:**
1. Copy the image to the workspace data dir
2. Resize it to max 1024px on longest side: `convert src.jpg -resize '1024x1024>' -quality 80 dst.jpg` (or use `python3 -c "from PIL import Image; ..."` if imagemagick unavailable)
3. Use the `image` tool on the resized image with a prompt asking to estimate: food items, portion sizes, and approximate nutrition per serving
4. Parse the vision response into structured nutrition data
5. Run: `echo '<json>' | python3 scripts/tracker.py estimate`
6. Reply with formatted summary noting it's an **estimate** (≈)

### 3. Summary Request
User asks for today's summary or a daily summary.

**Flow:**
1. Run: `python3 scripts/tracker.py summary [YYYY-MM-DD]`
2. Reply with formatted daily totals

### 4. Post-Log Check (after every barcode or estimate log)
After logging an entry, check running daily totals against limits:

1. Run: `python3 scripts/tracker.py summary`
2. Load profile from `FOOD_PROFILE_PATH` (default: `data/food_profile.json`)
3. Compare totals against `daily_limits`. Flag any that are over (or under for fiber_g_min):
   - **calories** > limit → `⚠️ Over calorie budget ({total}/{limit} kcal)`
   - **sodium_mg** > limit → `⚠️ High sodium ({total}/{limit} mg)`
   - **sugar_g** > limit → `⚠️ Over sugar limit ({total}/{limit} g)`
   - **fiber_g** < limit → `ℹ️ Low fiber ({total}/{limit} g)`
4. Append any warnings to the log reply. If nothing is over, skip the check section entirely.

## Reply Format

For logged items, use this format:
```
📝 **Item Name** (Brand)
Source: barcode | Servings: 2
Per serving: 150g
---
🔥 300 kcal | 🥩 12g protein | 🍞 45g carbs | 🧈 8g fat
🥬 3g fiber | 🍬 18g sugar | 🧂 420mg sodium
[Vitamins/minerals if present]
```

For photo estimates, prefix with: `📸 Estimate —`

## Parsing Servings

From message text, look for patterns like:
- `2x`, `x2`, `×2`
- `2 servings`, `2 serving`
- `two`, `three` (common number words)
- If none found, default to 1

## Data Access

This skill reads and writes persistent files in the workspace:
- **Writes** `$WORKSPACE/data/food_log.csv` — one row per food entry (item, nutrition, timestamps)
- **Writes** resized images to `$WORKSPACE/data/` during photo estimates (cleaned up after processing)
- **Reads** `$WORKSPACE/data/food_profile.json` (or `FOOD_PROFILE_PATH`) — daily nutritional limits
- **Network** barcode lookups hit `https://world.openfoodfacts.org/api/v2/` (public API, no key needed)
- **External API** photo estimates use the platform `image` tool which may send images to a remote vision model

## Required Files

- `scripts/tracker.py` — the food tracker script (included in bundle)
- `data/food_profile.json` — user profile with daily limits (user-created, not included)
