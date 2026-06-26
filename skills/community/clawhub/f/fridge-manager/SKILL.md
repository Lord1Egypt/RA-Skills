---
name: fridge-manager
description: "Household food inventory manager with expiry tracking. Use when: (1) adding food to fridge/freezer/pantry — 'bought milk', '买了鸡蛋', (2) removing/consuming food — 'used 3 eggs', '牛奶喝完了', '扔了过期酸奶', (3) checking inventory — 'what's in the fridge', '冰箱里有什么', (4) checking expiry — 'what's expiring soon', '什么快过期了', (5) food storage advice — 'how to store avocado', '蚝油要冷藏吗', (6) scheduled expiry reminders via cron/heartbeat. NOT for: restaurant/commercial inventory, nutrition tracking, recipe management, or meal planning."
---

# Fridge Manager

Track household food inventory via conversation. Auto-calculates expiry from built-in knowledge base, logs all changes, supports cron-based expiry alerts.

## Data

Store inventory in `family/fridge.json` (workspace-relative). Create on first use:

```json
{ "items": [], "log": [] }
```

### Item

```json
{
  "id": "a1b2c3d4",
  "name": "牛奶",
  "category": "dairy",
  "qty": "1 carton",
  "added": "2026-04-27",
  "expiry": "2026-05-04",
  "storage": "fridge",
  "notes": ""
}
```

- `id` — 8-char hex, generated via random
- `category` — `meat|seafood|dairy|vegetable|fruit|grain|condiment|leftover|drink|snack|other`
- `storage` — `fridge|freezer|pantry|counter`
- `expiry` — auto-calculated from knowledge base when omitted

### Log Entry

Append to `log[]` on every mutation:

```json
{ "action": "add|consume|discard", "id": "a1b2c3d4", "name": "牛奶", "qty": "1 carton", "reason": "", "ts": "2026-04-27T18:30:00" }
```

## Workflows

### Add (入库)

User says they bought/stored food → parse name, quantity, storage location.

1. Look up category + shelf life in knowledge base (read `references/food-knowledge-zh.md` or `references/food-knowledge-en.md` matching user language)
2. Calculate `expiry` = today + shelf life for the matching `storage` type (fridge → refrigerated life, freezer → frozen life)
3. If item not in knowledge base → estimate conservatively, flag in `notes`
4. Write to `items[]`, append `log[]`
5. Confirm: name, location, expiry date. Include one storage tip if notable (e.g., "蚝油必须冷藏")

Batch: "买了牛奶、鸡蛋和西兰花" → add all in one operation, single confirmation message.

### Remove (出库)

Three types — detect intent from phrasing:

| Intent | Trigger examples | Action |
|--------|-----------------|--------|
| **Consume** | "用完了", "喝了", "used 3 eggs" | Reduce qty or remove if zero |
| **Discard** | "扔了", "threw away", "过期了扔掉" | Remove from items |
| **Batch cook** | "做了番茄炒蛋" | Reduce/remove all ingredients mentioned |

- Fuzzy-match item names. If ambiguous (multiple matches), list and ask.
- Never silently delete — always confirm what was removed.
- Append `log[]` for each item affected.

### Query

| User says | Response |
|-----------|----------|
| "冰箱里有什么" / "what's in my fridge" | All items grouped by storage, with expiry status |
| "什么快过期" / "what's expiring" | Items within 3 days of expiry, sorted by urgency |
| "有鸡蛋吗" / "do I have eggs" | Search by name → qty + expiry |
| "冷冻室里有什么" / "what's in the freezer" | Filter by storage location |

Status indicators: 🔴 expired · 🟡 ≤3 days · 🟢 safe

### Expiry Alert (cron/heartbeat)

For scheduled invocation. Silent when nothing is urgent.

1. Read `family/fridge.json`
2. Find items where `expiry` ≤ today + 3 days
3. If found → send alert:
   ```
   🧊 Fridge Alert

   🔴 Expired:
   - 酸奶 (2 days overdue)

   🟡 Expiring soon:
   - 牛奶 (1 day left)
   - 鸡胸肉 (3 days left)

   💡 Tip: consider freezing the chicken if not cooking today
   ```
4. If nothing expiring → reply `NO_REPLY` (stay silent)

#### Cron Setup

Users create a cron via OpenClaw with this task prompt:

```
Read the fridge-manager skill, then check family/fridge.json for items expiring within 3 days. Send a reminder if any found. Otherwise reply NO_REPLY.
```

Recommended schedule: daily at 9:00 AM user's local time.

### Storage Tips

When asked "how to store X" or during add workflow, consult the knowledge base:
- Optimal storage method
- Special handling tips
- Common mistakes to avoid

## Knowledge Base

Built-in shelf life + storage tips for 60+ common foods, organized by category:

- **English**: Read `references/food-knowledge-en.md`
- **中文**: Read `references/food-knowledge-zh.md`

Use fuzzy matching: "chicken breast" → poultry row, "西红柿" → 番茄 row.

## Rules

1. Match user's language — Chinese input → Chinese response
2. Conservative expiry estimates when uncertain
3. Confirm every add/remove with a brief summary
4. Keep JSON clean — remove items at zero quantity
5. Log every mutation
