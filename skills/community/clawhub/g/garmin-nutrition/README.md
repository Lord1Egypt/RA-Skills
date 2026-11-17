# Garmin Nutrition — OpenClaw Skill

Low-friction food tracking for an AI agent: a **pattern cache** of the user's usual meals, a **local-first journal**, and Garmin Connect Nutrition as a sync target.

People eat a limited repertoire. Cache a dish once (ingredients + amounts) or photograph a product label once (per-100g + package size), and from then on "ate my usual salad, double oil" logs a meal with real numbers — the agent translates words into deltas, the script does the arithmetic deterministically:

```bash
uv run scripts/garmin_nutrition.py log салат --mult масло=2 --meal dinner --yes
uv run scripts/garmin_nutrition.py log лейз --qty пачка --meal snack --yes
```

Corrections go through `--supersede`: the old journal event is kept as history and its Garmin entry is deleted automatically. Day summaries (`day`) come from the local journal, no network.

Companion to [garmin-pulse](https://github.com/weirdei/garmin-pulse), which syncs the full daily health picture into markdown. The Garmin sink needs a **Connect+** subscription; the cache and journal work without it (`--no-garmin`).

Data lives outside the skill install dir (`~/.local/share/nutrition/` by default; `~/.config/nutrition/config.json` can set `data_dir` and a late-night `day_cutoff`). See SKILL.md for the pattern schema, the delta language, and the agent behavior rules (zero-or-one question per food event).

## Direct Garmin commands

```bash
# Subscription status, calorie/macro goals, meal slots
uv run scripts/garmin_nutrition.py status [--date YYYY-MM-DD]

# Day's totals, percent of goal, entries with macros and logId
uv run scripts/garmin_nutrition.py show [--date YYYY-MM-DD]

# Add an entry (dry-run without --yes)
uv run scripts/garmin_nutrition.py add \
  --name "Chicken and rice" --kcal 620 --protein 48 --fat 14 --carbs 70 \
  --meal lunch [--date YYYY-MM-DD] [--yes]

# Delete an entry (dry-run without --yes)
uv run scripts/garmin_nutrition.py delete --name "Chicken and rice" [--yes]
uv run scripts/garmin_nutrition.py delete --log-id <logId> --yes
```

All output is JSON. `status` and `show` are read-only; **writes are dry-run by default** and require `--yes`.

**Privacy:** meals logged without `--no-garmin` are uploaded to your Garmin Connect account (Garmin's cloud). The journal and pattern cache stay local either way.

## Setup

- Python 3.10+ and [uv](https://docs.astral.sh/uv/)
- Garmin OAuth tokens in `~/.garminconnect/`
- `garminconnect` is pinned to an exact version in the script header (it handles the OAuth tokens); bump it deliberately and re-test against a live account

Tokens are shared with any `python-garminconnect` tool. If you don't have them, run the one-time setup from [garmin-pulse](https://github.com/weirdei/garmin-pulse):

```bash
uv run scripts/sync_garmin.py --setup --email you@example.com
```

## API notes

The nutrition endpoints are private and undocumented. What this skill uses, verified against a live Connect+ account (August 2026):

| Operation | Call |
|---|---|
| Read day | `GET /nutrition-service/food/logs/{date}` (via `get_nutrition_daily_food_log`) |
| Settings | `GET /nutrition-service/settings/{date}` |
| Add | `PUT /nutrition-service/food/logs/quickAdd`, body `{mealDate, quickAddItems:[…]}` |
| Delete | `DELETE /nutrition-service/food/logs/{date}`, body `{"logIds": [id]}` → 204 |

Two things worth knowing if you build on this:

- **Delete takes the date in the path and the ids in the body.** Passing a `logId` in the path returns 404, which makes it look unsupported.
- **`quickAdd` with `action: "DELETE"` returns HTTP 200 and does nothing.** The success response is meaningless; always re-read the log to confirm what happened. This skill does that after every write.
- There is no update operation. Correcting an entry means delete + add.

Meal slots (`BREAKFAST`, `LUNCH`, `DINNER`) have time windows and reject entries timestamped outside them with HTTP 400; `SNACKS` is unbounded. The skill picks the slot from `--meal` and snaps the timestamp into that slot's window, so backfilling a previous day works.

## License

MIT
