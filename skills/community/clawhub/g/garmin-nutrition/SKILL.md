---
name: garmin-nutrition
version: 1.1.3
homepage: https://github.com/weirdei/garmin-nutrition
description: Low-friction food tracking - a pattern cache of the user's usual meals, a local-first journal, and Garmin Connect Nutrition as a sync target. Log "my usual salad, double oil" in one message. Logged meals are uploaded to the user's Garmin Connect account (Garmin cloud) unless `--no-garmin`; the skill can also read and delete entries in the user's Garmin food log. Requires Garmin Connect+ for the Garmin sink.
metadata: {"openclaw":{"emoji":"🍽️","requires":{"bins":["uv"]},"install":[{"id":"uv","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv via Homebrew"}]}}
---

# Garmin Nutrition

Track what the user eats with minimal friction. The core idea: people eat a limited repertoire. Cache it once, then a short message ("ate my usual salad, double oil") is enough to log a meal with real numbers.

All data is local-first: the journal is the source of truth, Garmin Connect is a sink. The Garmin sink needs a Connect+ subscription; the cache and journal work without it (use `--no-garmin`).

**Privacy:** without `--no-garmin`, every meal you log with `--yes` (name, calories, macros, meal slot, timestamp) is uploaded to the user's Garmin Connect account, i.e. to Garmin's cloud under Garmin's privacy policy. Nutrition data is health data; make sure the user knows it leaves the machine. For a strictly local journal, use `--no-garmin` on every `log` call.

## What this skill touches

- **Local files, read/write:** the pattern cache and journal in the data dir (`~/.local/share/nutrition/` by default; see Storage). Read-only: `~/.config/nutrition/config.json`.
- **Environment:** reads `NUTRITION_DATA_DIR`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`. No secrets are read from the environment.
- **Credentials:** the user's Garmin OAuth tokens in `~/.garminconnect/`, read-only. They are created once by the user (see README, Setup); the skill never asks for or stores a password.
- **Network:** Garmin Connect only, and only for `status`, `show`, `delete`, and `log` without `--no-garmin`. `pattern *` and `day` never touch the network.
- **Input validation:** every `--date` must be a real calendar date in `YYYY-MM-DD` form; it becomes a journal file name and a Garmin URL segment, so anything else is rejected.
- **Dependency:** the Garmin client library is pinned to an exact version in the script header (it handles the OAuth tokens); it only changes with a new skill release.

## The one rule that matters

**Ask zero or one question per food event, never more.** Prefer a stated assumption over a question. Log with `--confidence low` rather than interrogate. The user correcting you afterwards is cheaper than friction before logging.

- One cached match for "чипсы" → use it silently, mention the assumption in your reply.
- Several matches → one short question: "какие — лейз (пачка 45 г) или начос?"
- No pattern and no data ("тарелка картошки с мясом") → estimate standard portions, log adhoc with low confidence, state assumptions in one line. Do NOT ask for grams.

## Storage

- Config: `~/.config/nutrition/config.json` — `{"data_dir": "...", "day_cutoff": "04:00"}` (both optional)
- Data: `$NUTRITION_DATA_DIR`, else config `data_dir`, else `~/.local/share/nutrition/`
  - `patterns.json` — the food cache
  - `journal/YYYY-MM-DD.json` + rendered `.md` — the log
- `day_cutoff`: food logged before this hour belongs to the previous day (late-night eating). Default `00:00` (calendar days).

## The pattern cache

Two kinds of entries:

**Dish** — ingredients with amounts and per-100g macros; totals are always computed, never stored. Supports deltas at log time.

**Product** — a packaged item photographed once: per-100g from the label plus named portion sizes.

```bash
uv run {baseDir}/scripts/garmin_nutrition.py pattern list
uv run {baseDir}/scripts/garmin_nutrition.py pattern show <name>
uv run {baseDir}/scripts/garmin_nutrition.py pattern add <name> --json '<entry>'
uv run {baseDir}/scripts/garmin_nutrition.py pattern set <name> --json '<entry>'   # full replace
uv run {baseDir}/scripts/garmin_nutrition.py pattern rm <name>
```

Dish entry:

```json
{"type": "dish", "aliases": ["салат"],
 "ingredients": [
   {"name": "помидоры", "qty": 150, "unit": "g",
    "per100g": {"kcal": 18, "p": 0.9, "f": 0.2, "c": 3.9},
    "source": "generic", "confidence": "medium"},
   {"name": "масло", "qty": 3, "unit": "spray", "g_per_unit": 1.66,
    "per100g": {"kcal": 900, "p": 0, "f": 100, "c": 0}}
 ],
 "notes": "frying oil would get counting: 0.5"}
```

Non-gram units (`spray`, `piece`, …) need `g_per_unit`. `counting` (default 1.0) is the absorbed fraction — e.g. 0.5 for frying oil that stays in the pan.

Product entry:

```json
{"type": "product", "aliases": ["lays"],
 "per100g": {"kcal": 536, "p": 6.6, "f": 34, "c": 51},
 "portions": {"пачка": 45, "маленькая": 25}, "default_portion": "пачка",
 "source": "label photo 2026-08-22"}
```

When the user photographs a label, read per-100g values and package size from it and `pattern add` a product. That is the whole point of the photo — one shot, cached forever.

### Growing the cache

- Same uncached dish logged for the second or third time (check recent journal days): offer once to save it as a pattern with the user's typical amounts.
- The user corrects your numbers ("в твороге не столько белка"): ask whether to update the pattern, then `pattern set`. **Never update baselines silently.**
- Label values the user confirmed beat generic database values; record `source` and `confidence` per ingredient.

## Logging

Everything goes through `log`. Dry-run by default; `--yes` writes journal + Garmin.

```bash
# dish by name/alias, with deltas translated from the user's words
uv run {baseDir}/scripts/garmin_nutrition.py log салат --mult масло=2 --meal dinner --yes

# "порция побольше, где-то полторы"      → --portion 1.5
# "без сыра"                             → --without сыр
# "помидоров сегодня 200 г"              → --set помидоры=200g
# "добавил фету грамм 30"                → --add фета=30g        (cached product)
#                                          --add фета=30g@264,18,21,0  (with per-100g macros)

# product: named portion or grams
uv run {baseDir}/scripts/garmin_nutrition.py log лейз --qty пачка --meal snack --yes

# no pattern: agent's estimate, stated assumptions, low confidence
uv run {baseDir}/scripts/garmin_nutrition.py log adhoc --name "картошка с мясом" \
  --kcal 700 --p 35 --f 30 --c 60 --confidence low --meal dinner --yes

# correction: replaces an earlier event AND deletes its Garmin entry
uv run {baseDir}/scripts/garmin_nutrition.py log салат --set авокадо=150g \
  --supersede food-002 --meal dinner --yes

# day summary from the journal (no network)
uv run {baseDir}/scripts/garmin_nutrition.py day [--date YYYY-MM-DD]
```

Before `--yes`, show the user one compact line: name, kcal, macros, meal. Corrections use `--supersede`, not delete+re-add: it keeps history and cleans Garmin automatically.

## Direct Garmin commands

`status` (subscription, goals, meal slots), `show` (Garmin's own log for a day), `delete` (by `--name` or `--log-id`, dry-run without `--yes`).

`status` and `show` are read-only: they use the user's own cached token and change nothing, so run them when the user's request needs the data (e.g. "what did I eat today according to Garmin"). Do not poll Garmin on your own initiative. `delete` changes the user's Garmin log: show the dry-run output and get an explicit go-ahead before adding `--yes`.

## Garmin API notes

Private, undocumented endpoints; verified August 2026. Add = `PUT /nutrition-service/food/logs/quickAdd`. Delete = `DELETE /nutrition-service/food/logs/{date}` with `{"logIds": [...]}` (date in path, ids in body — an id in the path 404s). `quickAdd` with `action: "DELETE"` returns 200 and does nothing; never use it. There is no update. After every write the script re-reads the log to confirm; `unknown_after_push` in the output means check before retrying, a retry can duplicate.

## Related

- [garmin-pulse](https://github.com/weirdei/garmin-pulse) — syncs the full daily health picture (sleep, HR, HRV, body battery, training status, activities, and nutrition totals) into markdown files. Use it for reading health history; use this skill to log food.
