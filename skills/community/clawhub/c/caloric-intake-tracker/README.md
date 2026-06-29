# Calorie Tracker OpenClaw Skill

A skill-first OpenClaw skill to track daily calorie intake, macronutrients, body weight, and waist measurements locally in a SQLite database. 

## Features

- **No Packaging Overheads:** Zero setup or pip installs required. Runs immediately using Python's standard libraries.
- **Dynamic Meal Types:** Allowed meal types are configured and validated directly in the SQLite database.
- **Granular Analytics:** Subcommands for daily, weekly, trend-based, and body measurement reports.
- **Intelligent Budgets:** Computes future daily budgets and historical averages (excluding incomplete days) to aid health coaching and planning.

## CLI Usage

The core script is located at `scripts/tracker.py`. 

### Global Options

The script supports two global options that must be placed *before* the subcommand:
- `--database PATH`: Specifying a path to the database (defaults to `health_data.db` in current directory).
- `--today YYYY-MM-DD`: Time-travel option to simulate the system date for all operations (logs, lists, budgets, averages).

### Core Commands

- **Config Goal:** `python scripts/tracker.py goal CALORIES [PROTEIN]`
- **Log Food:** `python scripts/tracker.py add "description" CALORIES [protein] [carbs] [fat] --meal TYPE`
- **List Food:** `python scripts/tracker.py list [DATE] [--no-group]` (groups by meal type by default)
- **Update Entry:** `python scripts/tracker.py update ID [--name NAME] [--cal CALORIES] ...`
- **Delete Entry:** `python scripts/tracker.py delete ID`
- **Mark Complete:** `python scripts/tracker.py complete DATE [--completeness QUALITY]`
- **Check Complete:** `python scripts/tracker.py check-complete [DATE]`
- **Log Weight/Waist/Measurement:** `python scripts/tracker.py weight KG` / `python scripts/tracker.py waist CM` / `python scripts/tracker.py measure TYPE VALUE`
  *(Note: Default types `waist`, `hips`, and `neck` are pre-seeded automatically. The key `waist` is specifically used to compute Waist-to-Height Ratio (WHtR) and power the legacy shortcut.)*

### Reports & Statistics

- **Daily Stats:** `python scripts/tracker.py stats day [DATE] [--no-group]` (groups by meal type by default)
- **Weekly Stats:** `python scripts/tracker.py stats week [DATE] [--weeks N] [--compact] [--include-today {auto,yes,no,both}]`
- **Rolling Trends:** `python scripts/tracker.py stats trend [--days N]`
- **Weight History:** `python scripts/tracker.py stats weight [-N ENTRIES] [--days DAYS]` (defaults to `-N 5`)
- **Waist/Measurement History:** `python scripts/tracker.py stats waist` / `python scripts/tracker.py stats measure TYPE [-N ENTRIES] [--days DAYS]`

For detailed operational rules and specifications, see [SKILL.md](SKILL.md).

