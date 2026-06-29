---
name: caloric-intake-tracker
description: Log and track daily calorie intake, macronutrients, body weight, and waist measurements locally in a SQLite database. Provides granular statistics, weekly averages, and future calorie budgets.
metadata: {"openclaw": {"requires": {"bins": ["python"]}}}
---

# Local Calorie Tracker Skill

Track daily calorie intake, macronutrients, body weight, and waist measurements locally using a SQLite database.

## Installation & Setup

This is a standalone, skill-first OpenClaw skill. It runs out-of-the-box using standard Python libraries.

The default SQLite database file is named `health_data.db` and is resolved relative to the current working directory (Cwd) of the running agent. To override the database path, pass the `--database PATH` option to any command.

## Operational Instructions for the Agent

1.  **No Compensatory Entries:** If a food entry was logged incorrectly (e.g. wrong calorie or protein count), do not log a new positive or negative "balancing" or "corrective" entry. Instead, identify the incorrect entry's ID using the `list` or `stats day` command, and run the `update` or `delete` command to fix it.
2.  **No Bogus Logs:** Every logged entry's description must contain only the actual name of the food or drink consumed. Do not store summaries, calorie calculations, or meta-data in the food description (e.g., do not name an entry "1875 kcal, 72g protein" to force-balance a day).
3.  **Standardized Meal Types:** Every logged food entry must have a valid `--meal` type. Allowed types are: `breakfast`, `lunch`, `dinner`, `snack`, `fika`, `drink`, `dessert`, `evening`, and `other`. Valid meal types are loaded and validated dynamically from the database.

## Day Completeness Quality Levels

When marking a day as complete using the `complete` command, use one of the following completeness quality levels:
*   `full`: Default. All meals and drinks consumed for the target day were fully tracked.
*   `partial`: Some meals are missing, or the day relies heavily on rough estimates.
*   `minimal`: Only sporadic entries were logged; most of the day's intake is unknown.

## Interpreting Weekly Averages & Budgets

When reviewing weekly averages using the `stats week` command, averages and budgets are tailored dynamically to today's completion status by default (`--include-today auto`):
*   **If Today is Incomplete:** The command excludes today's data from the active average display, showing the **Monday-to-Yesterday Average** and the **Daily Budget Starting Today** (including a dynamic helper showing remaining calories for today).
*   **If Today is Complete:** The command includes today's data, showing the **Monday-to-Today Average** and the **Daily Budget Starting Tomorrow**.
*   **Customizing Scope:** You can use the `--include-today` flag to force a specific behavior:
    - `--include-today yes`: Forces inclusion of today (shows Mon-Today average and Starting Tomorrow budget).
    - `--include-today no`: Forces exclusion of today (shows Mon-Yesterday average and Starting Today budget).
    - `--include-today both`: Shows both sets of averages and budgets.

## CLI Reference

All commands support the following global flags (which must be placed *before* the subcommand):
*   `--database PATH`: Path to SQLite database file (defaulting to `./health_data.db`).
*   `--today YYYY-MM-DD`: Simulates today's date context for the entire command run (overrides the system clock date, affecting default logging dates, lookbacks, weekly budgets, and rolling averages).

### 1. Configuration & Logging

*   **Configure Daily Goal & Height:**
    ```bash
    python scripts/tracker.py goal CALORIES [PROTEIN] [--height HEIGHT_CM]
    ```
    Sets target calories, optional protein goals (in grams), and optional height in cm (used dynamically by SQLite views to compute BMI and Waist-to-Height Ratio).
    *Example:* `python scripts/tracker.py goal 1800 120 --height 180.0`

*   **Log Food Entry:**
    ```bash
    python scripts/tracker.py add "food description" CALORIES [protein] [carbs] [fat] --meal TYPE [--date YYYY-MM-DD]
    ```
    *Example:* `python scripts/tracker.py add "Oatmeal with blueberries" 350 12 --meal breakfast`

*   **List Entries by ID:**
    ```bash
    python scripts/tracker.py list [DATE] [--no-group]
    ```
    Lists all entries for `DATE` (defaults to today). By default, entries are grouped by meal type (combining descriptions and summing calories/protein). Pass `--no-group` to disable grouping and display raw individual entries with their database IDs and timestamps (essential for updates/deletions).

*   **Update Food Entry:**
    ```bash
    python scripts/tracker.py update ID [--name NAME] [--cal CALORIES] [--p PROTEIN] [--c CARBS] [--f FAT] [--meal TYPE]
    ```
    Modifies an existing entry by ID. Only the specified flags are updated.

*   **Delete Food Entry:**
    ```bash
    python scripts/tracker.py delete ID
    ```
    Permanently deletes a specific entry.

*   **Mark Day as Complete:**
    ```bash
    python scripts/tracker.py complete DATE [--completeness QUALITY] [--notes NOTES]
    ```
    Sets the completeness status (`full` (default), `partial`, or `minimal`) and marks `completed=1` in the database.

*   **Check Day Completion:**
    ```bash
    python scripts/tracker.py check-complete [DATE]
    ```
    Exits with code `0` if the date is fully completed (`completeness == 'full'` and `completed == 1`), otherwise exits with `1`.

*   **Log Body Weight:**
    ```bash
    python scripts/tracker.py weight KG [DATE]
    ```
    Logs weight for the specified date (defaults to today).

*   **Log Waist Circumference (Shortcut):**
    ```bash
    python scripts/tracker.py waist CM [DATE] [--notes NOTES]
    ```
    Logs waist circumference with optional notes (delegates to `measure waist`).

*   **Log Custom Body Measurement:**
    ```bash
    python scripts/tracker.py measure TYPE VALUE [DATE] [--notes NOTES]
    ```
    Logs a measurement value for a defined measurement type (e.g. waist, hips, neck, or custom defined types) with optional notes.
    *(Note: Default types `waist`, `hips`, and `neck` are pre-seeded automatically. The key `waist` is specifically used to compute Waist-to-Height Ratio (WHtR) and power the `waist` shortcut.)*
    *Example:* `python scripts/tracker.py measure hip_upper 92.5 --notes "Upper hip line, morning"`

*   **Define Custom Measurement Type:**
    ```bash
    python scripts/tracker.py measure-type define KEY DISPLAY_NAME UNIT [--desc DESCRIPTION]
    ```
    Defines a custom measurement point with display name, unit, and optional description.
    *Example:* `python scripts/tracker.py measure-type define hip_upper "Hip (Upper)" cm --desc "Upper hip line"`

*   **List Defined Measurement Types:**
    ```bash
    python scripts/tracker.py measure-type list
    ```
    Lists all defined measurement types, units, and descriptions.

*   **Delete Custom Measurement Type:**
    ```bash
    python scripts/tracker.py measure-type delete KEY
    ```
    Deletes the type definition and all associated logs. Default types (`waist`, `hips`, `neck`) cannot be deleted.

### 2. Statistics & Reports

*   **Show Daily Breakdown:**
    ```bash
    python scripts/tracker.py stats day [DATE] [--no-group]
    ```
    Prints the chronological list of entries, meal-type breakdowns, and progress compared to daily goals. Defaults to today's date (or simulated `--today` date) if `DATE` is omitted. By default, the daily breakdown list is grouped by meal type (combining descriptions and summing calories/protein). Pass `--no-group` to disable grouping and display raw individual entries with their database IDs and timestamps.

*   **Show Weekly Summary:**
    ```bash
    python scripts/tracker.py stats week [DATE] [--weeks N] [--compact] [--include-today {auto,yes,no,both}]
    ```
    Summarizes the Mon-Sun week containing `DATE` (or N preceding weeks). Defaults to today's date (or simulated `--today` date) if `DATE` is omitted. If `--compact` is passed, it outputs a single-line summary of metrics for each week. Displays weekly averages and future daily budgets tailored dynamically to today's completion status (customizable via `--include-today`), along with a daily breakdown table.

*   **Show Macronutrient Trends:**
    ```bash
    python scripts/tracker.py stats trend [--days N]
    ```
    Displays 7-day, 30-day, and 90-day rolling averages of calorie and protein intake (resolved dynamically from rolling trends view) up to today.

*   **Show Weight logs:**
    ```bash
    python scripts/tracker.py stats weight [-N ENTRIES] [--days DAYS]
    ```
    Displays logged weights, BMI, and weight changes up to today. Defaults to showing the last 5 entries (`-N 5`). Supports a positive integer or `"all"` for `-N`, and an integer number of days for `--days`.

*   **Show Waist logs (Shortcut):**
    ```bash
    python scripts/tracker.py stats waist [-N ENTRIES] [--days DAYS]
    ```
    Displays logged waist measurements, WHtR, and waist changes. Defaults to showing the last 5 entries (`-N 5`).

*   **Show Custom Measurement logs:**
    ```bash
    python scripts/tracker.py stats measure TYPE [-N ENTRIES] [--days DAYS]
    ```
    Displays logs, unit, and calculated changes for any defined measurement type. If `TYPE` is `waist`, also prints WHtR.
    *Example:* `python scripts/tracker.py stats measure chest -N 10`
