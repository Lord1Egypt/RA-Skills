# /// script
# requires-python = ">=3.10"
# dependencies = ["garminconnect==0.3.11"]
# ///
"""Food tracking with a local-first journal, a pattern cache, and Garmin Connect
Nutrition as a sync target.

The pattern cache stores the user's food repertoire (dishes with ingredients,
packaged products from labels) so logging a meal takes one message instead of
an interrogation. The journal is the source of truth; Garmin is a sink.

Garmin food logging is a Connect+ feature. The write path uses Garmin's
private Quick Add endpoint; deletion uses DELETE /food/logs/{date} with
{"logIds": [...]} — the quickAdd action=DELETE form returns 200 and does
nothing, so it is never used here.

garminconnect is pinned to an exact version on purpose: it handles the user's
Garmin OAuth tokens, so the reviewed dependency must not drift under `uv run`
(ClawHub supply-chain check, 2026-09). Bump it deliberately: update the pin,
re-run `status`/`show`/`log --yes` against a live account, republish.
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from garminconnect import Garmin

TOKEN_DIR = Path.home() / ".garminconnect"
QUICK_ADD_PATH = "/nutrition-service/food/logs/quickAdd"
CONFIG_FILE = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "nutrition" / "config.json"

MEAL_DEFAULT_TIME = {
    "BREAKFAST": "08:00:00",
    "LUNCH": "12:00:00",
    "DINNER": "19:00:00",
    "SNACKS": "21:00:00",
}

MEAL_ALIASES = {
    "breakfast": "BREAKFAST",
    "lunch": "LUNCH",
    "dinner": "DINNER",
    "snack": "SNACKS",
    "snacks": "SNACKS",
}


# --- config / storage -------------------------------------------------------

def load_config() -> dict:
    try:
        return json.loads(CONFIG_FILE.read_text())
    except (OSError, ValueError):
        return {}


CONFIG = load_config()

DATA_DIR = Path(
    os.environ.get("NUTRITION_DATA_DIR")
    or CONFIG.get("data_dir")
    or Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share") / "nutrition"
)
PATTERNS_FILE = DATA_DIR / "patterns.json"
JOURNAL_DIR = DATA_DIR / "journal"


def load_patterns() -> dict:
    try:
        return json.loads(PATTERNS_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save_patterns(patterns: dict) -> None:
    PATTERNS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PATTERNS_FILE.write_text(json.dumps(patterns, ensure_ascii=False, indent=2) + "\n")


def food_day() -> str:
    """Today's food date: before day_cutoff, late-night food belongs to yesterday."""
    cutoff = CONFIG.get("day_cutoff", "00:00")
    now = datetime.now()
    try:
        if now.time() < time.fromisoformat(cutoff):
            return (now.date() - timedelta(days=1)).isoformat()
    except ValueError:
        pass
    return now.date().isoformat()


DAY_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def parse_day(value: str) -> str:
    """Validate a calendar date and return it as canonical YYYY-MM-DD.

    Dates become journal file names and Garmin URL path segments, so anything
    that is not a plain calendar date is rejected (no separators, no traversal).
    """
    text = str(value).strip()
    if not DAY_RE.fullmatch(text):
        raise ValueError(f"date must be YYYY-MM-DD, got {value!r}")
    return date.fromisoformat(text).isoformat()


def iso_day(value: str) -> str:
    """argparse type for --date."""
    try:
        return parse_day(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e)) from e


LOG_ID_RE = re.compile(r"[0-9A-Za-z-]{1,64}")


def log_id_arg(value: str) -> str:
    """argparse type for --log-id: Garmin log ids are opaque hex strings; nothing else is sent."""
    text = str(value).strip()
    if not LOG_ID_RE.fullmatch(text):
        raise argparse.ArgumentTypeError(f"log id must be alphanumeric, got {value!r}")
    return text


def journal_path(day: str, ext: str) -> Path:
    return JOURNAL_DIR / f"{parse_day(day)}.{ext}"


def load_day(day: str) -> dict:
    path = journal_path(day, "json")
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {"date": day, "events": []}


def save_day(day_data: dict) -> None:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    day = parse_day(day_data["date"])
    journal_path(day, "json").write_text(json.dumps(day_data, ensure_ascii=False, indent=2) + "\n")
    lines = [
        f"# Nutrition — {day}",
        "",
        "| id | meal | name | kcal | P | F | C | conf | status | garmin |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for e in day_data["events"]:
        g = "✓" if (e.get("garmin") or {}).get("log_id") else ""
        lines.append(
            f"| {e['id']} | {e.get('meal','')} | {e.get('name','')} | {e.get('kcal','')} "
            f"| {e.get('p','')} | {e.get('f','')} | {e.get('c','')} "
            f"| {e.get('confidence','')} | {e.get('status','')} | {g} |"
        )
    active = [e for e in day_data["events"] if e.get("status") == "active"]
    totals = day_totals(active)
    lines += ["", f"**Total: {totals['kcal']} kcal | P {totals['p']} | F {totals['f']} | C {totals['c']}**", ""]
    journal_path(day, "md").write_text("\n".join(lines))


def next_event_id(day_data: dict) -> str:
    return f"food-{len(day_data['events']) + 1:03d}"


def day_totals(events: list[dict]) -> dict:
    out = {"kcal": 0, "p": 0.0, "f": 0.0, "c": 0.0}
    for e in events:
        out["kcal"] += int(e.get("kcal") or 0)
        for k in ("p", "f", "c"):
            out[k] += float(e.get(k) or 0)
    return {"kcal": out["kcal"], "p": round(out["p"], 1), "f": round(out["f"], 1), "c": round(out["c"], 1)}


# --- pattern math -----------------------------------------------------------

def resolve_pattern(patterns: dict, name: str) -> tuple[str, dict] | None:
    if name in patterns:
        return name, patterns[name]
    wanted = name.strip().casefold()
    for key, entry in patterns.items():
        if key.casefold() == wanted:
            return key, entry
        if any(a.casefold() == wanted for a in entry.get("aliases") or []):
            return key, entry
    return None


def ingredient_grams(ing: dict) -> float:
    qty = float(ing.get("qty") or 0)
    unit = (ing.get("unit") or "g").lower()
    if unit in ("g", "ml"):
        return qty
    per_unit = ing.get("g_per_unit")
    if per_unit is None:
        raise ValueError(f"ingredient '{ing.get('name')}': unit '{unit}' needs g_per_unit")
    return qty * float(per_unit)


def ingredient_macros(ing: dict) -> dict:
    grams = ingredient_grams(ing) * float(ing.get("counting", 1.0))
    per = ing.get("per100g") or {}
    return {
        "kcal": grams * float(per.get("kcal") or 0) / 100,
        "p": grams * float(per.get("p") or 0) / 100,
        "f": grams * float(per.get("f") or 0) / 100,
        "c": grams * float(per.get("c") or 0) / 100,
    }


def sum_macros(parts: list[dict]) -> dict:
    total = {"kcal": 0.0, "p": 0.0, "f": 0.0, "c": 0.0}
    for m in parts:
        for k in total:
            total[k] += m[k]
    return {"kcal": round(total["kcal"]), "p": round(total["p"], 1), "f": round(total["f"], 1), "c": round(total["c"], 1)}


QTY_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*([a-zA-Zа-яА-Я]*)$")


def parse_qty(text: str, default_unit: str) -> tuple[float, str]:
    m = QTY_RE.match(text.strip())
    if not m:
        raise ValueError(f"cannot parse quantity '{text}'")
    return float(m.group(1)), (m.group(2) or default_unit).lower()


def find_ingredient(ingredients: list[dict], name: str) -> dict | None:
    wanted = name.strip().casefold()
    for ing in ingredients:
        if (ing.get("name") or "").casefold() == wanted:
            return ing
    return None


def apply_deltas(entry: dict, patterns: dict, args) -> tuple[dict, list[str]]:
    """Return (totals, applied-delta descriptions) for a dish pattern."""
    ingredients = [dict(i) for i in entry.get("ingredients") or []]
    applied: list[str] = []

    for spec in args.without or []:
        ing = find_ingredient(ingredients, spec)
        if ing is None:
            raise ValueError(f"--without: no ingredient '{spec}' in pattern")
        ingredients.remove(ing)
        applied.append(f"without {spec}")

    for spec in args.mult or []:
        name, _, factor = spec.partition("=")
        ing = find_ingredient(ingredients, name)
        if ing is None:
            raise ValueError(f"--mult: no ingredient '{name}' in pattern")
        ing["qty"] = float(ing.get("qty") or 0) * float(factor)
        applied.append(f"mult {name}={factor}")

    for spec in args.set or []:
        name, _, value = spec.partition("=")
        ing = find_ingredient(ingredients, name)
        if ing is None:
            raise ValueError(f"--set: no ingredient '{name}' in pattern")
        qty, unit = parse_qty(value, ing.get("unit") or "g")
        if unit in ("g", "ml") and (ing.get("unit") or "g") not in ("g", "ml"):
            ing["unit"], ing["g_per_unit"] = unit, None
            ing["g_per_unit"] = 1.0
        ing["qty"] = qty
        applied.append(f"set {name}={value}")

    for spec in args.add or []:
        name, _, rest = spec.partition("=")
        qty_part, _, macro_part = rest.partition("@")
        qty, unit = parse_qty(qty_part, "g")
        if macro_part:
            kcal, p, f, c = (float(x) for x in macro_part.split(","))
            per100g = {"kcal": kcal, "p": p, "f": f, "c": c}
        else:
            found = resolve_pattern(patterns, name)
            if not found or found[1].get("type") != "product" or not found[1].get("per100g"):
                raise ValueError(
                    f"--add: '{name}' is not a cached product; pass macros as {name}={qty_part}@kcal,p,f,c"
                )
            per100g = found[1]["per100g"]
        ingredients.append({"name": name, "qty": qty, "unit": unit, "per100g": per100g})
        applied.append(f"add {spec}")

    if args.portion and float(args.portion) != 1.0:
        for ing in ingredients:
            ing["qty"] = float(ing.get("qty") or 0) * float(args.portion)
        applied.append(f"portion x{args.portion}")

    return sum_macros([ingredient_macros(i) for i in ingredients]), applied


def product_totals(entry: dict, qty_spec: str | None) -> tuple[dict, str]:
    per100g = entry.get("per100g") or {}
    portions = entry.get("portions") or {}
    if qty_spec:
        named = portions.get(qty_spec) or portions.get(qty_spec.casefold())
        if named is not None:
            grams, label = float(named), f"{qty_spec} ({named} g)"
        else:
            qty, unit = parse_qty(qty_spec, "g")
            if unit not in ("g", "ml"):
                raise ValueError(f"unknown portion '{qty_spec}'; defined: {', '.join(portions) or 'none'}")
            grams, label = qty, f"{qty:g} g"
    else:
        default = entry.get("default_portion")
        if default and default in portions:
            grams, label = float(portions[default]), f"{default} ({portions[default]} g)"
        elif len(portions) == 1:
            name, val = next(iter(portions.items()))
            grams, label = float(val), f"{name} ({val} g)"
        else:
            raise ValueError("product needs --qty (named portion or grams)")
    factor = grams / 100
    totals = {
        "kcal": round(factor * float(per100g.get("kcal") or 0)),
        "p": round(factor * float(per100g.get("p") or 0), 1),
        "f": round(factor * float(per100g.get("f") or 0), 1),
        "c": round(factor * float(per100g.get("c") or 0), 1),
    }
    return totals, label


def validate_pattern(entry: dict) -> str | None:
    kind = entry.get("type")
    if kind == "dish":
        if not entry.get("ingredients"):
            return "dish pattern needs a non-empty ingredients list"
        for ing in entry["ingredients"]:
            if not ing.get("name") or ing.get("qty") is None or not ing.get("per100g"):
                return f"ingredient {ing.get('name')!r} needs name, qty and per100g"
            try:
                ingredient_grams(ing)
            except ValueError as e:
                return str(e)
    elif kind == "product":
        if not entry.get("per100g"):
            return "product pattern needs per100g"
    else:
        return "pattern type must be 'dish' or 'product'"
    return None


# --- garmin -----------------------------------------------------------------

def connect() -> Garmin:
    if not TOKEN_DIR.exists() or not any(TOKEN_DIR.iterdir()):
        print(
            f"Error: No cached Garmin tokens in {TOKEN_DIR}.\n"
            "Run the setup of a Garmin auth skill first, e.g.:\n\n"
            "  uv run scripts/sync_garmin.py --setup --email you@example.com\n"
            "  (from the garmin-pulse skill)\n",
            file=sys.stderr,
        )
        sys.exit(1)
    client = Garmin()
    try:
        client.login(str(TOKEN_DIR))
    except Exception as e:
        print(f"Error: Garmin authentication failed — {e}", file=sys.stderr)
        sys.exit(1)
    return client


def garmin_session(client: Garmin):
    session = getattr(client, "garth", None) or getattr(client, "client", None)
    if session is None:
        print("Error: cannot reach the underlying Garmin HTTP session.", file=sys.stderr)
        sys.exit(1)
    return session


def fetch_log(client: Garmin, day: str) -> dict:
    try:
        return client.get_nutrition_daily_food_log(day) or {}
    except Exception as e:
        print(f"Error: could not read nutrition log for {day} — {e}", file=sys.stderr)
        sys.exit(1)


def meal_slots(log: dict) -> list[dict]:
    slots = []
    for detail in log.get("mealDetails") or []:
        meal = detail.get("meal") or {}
        if meal.get("mealId") is None:
            continue
        slots.append(
            {
                "meal_id": int(meal["mealId"]),
                "name": meal.get("mealName"),
                "start_time": meal.get("startTime"),
                "end_time": meal.get("endTime"),
            }
        )
    return slots


def logged_foods(log: dict) -> list[dict]:
    entries = []
    for detail in log.get("mealDetails") or []:
        slot_name = ((detail.get("meal") or {}).get("mealName")) or "?"
        for food in detail.get("loggedFoods") or []:
            meta = food.get("foodMetaData") or {}
            nutrition = food.get("nutritionContent") or {}
            entries.append(
                {
                    "meal": slot_name,
                    "name": meta.get("foodName"),
                    "calories": nutrition.get("calories"),
                    "protein": nutrition.get("protein"),
                    "fat": nutrition.get("fat"),
                    "carbs": nutrition.get("carbs"),
                    "log_id": food.get("logId"),
                    "meal_time": food.get("mealTime"),
                }
            )
    return entries


def pick_slot(slots: list[dict], label: str | None) -> dict:
    if label:
        wanted = MEAL_ALIASES.get(label.lower())
        if wanted is None:
            print(f"Error: unknown meal '{label}'. Use: breakfast, lunch, dinner, snack.", file=sys.stderr)
            sys.exit(1)
        for slot in slots:
            if slot["name"] == wanted:
                return slot
        print(f"Error: Garmin has no '{wanted}' slot on this date.", file=sys.stderr)
        sys.exit(1)
    for slot in slots:
        if slot["name"] == "SNACKS":
            return slot
    if slots:
        return slots[-1]
    print(
        "Error: no meal slots returned. Nutrition is a Garmin Connect+ feature —\n"
        "check that the subscription is active and food logging is enabled.",
        file=sys.stderr,
    )
    sys.exit(1)


def slot_timestamp(day: str, slot: dict) -> tuple[str, str]:
    default = MEAL_DEFAULT_TIME.get(slot["name"] or "", "21:00:00")
    start, end = slot.get("start_time"), slot.get("end_time")
    chosen = default
    if start and end:
        try:
            if not (time.fromisoformat(start) <= time.fromisoformat(default) <= time.fromisoformat(end)):
                chosen = start
        except ValueError:
            chosen = start
    local = datetime.fromisoformat(f"{day}T{chosen}")
    utc = local.astimezone(timezone.utc) if local.tzinfo else local
    return chosen, utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def garmin_push(client: Garmin, day: str, name: str, totals: dict, meal_label: str | None) -> dict:
    log = fetch_log(client, day)
    slot = pick_slot(meal_slots(log), meal_label)
    meal_time, log_timestamp = slot_timestamp(day, slot)
    payload = {
        "mealDate": day,
        "quickAddItems": [
            {
                "name": name,
                "logId": None,
                "logTimestamp": log_timestamp,
                "logSource": "GCW",
                "logCategory": "QUICK_ADD",
                "mealTime": meal_time,
                "mealId": slot["meal_id"],
                "action": "ADD",
                "calories": str(totals["kcal"]),
                "carbs": str(round(totals["c"])),
                "protein": str(round(totals["p"])),
                "fat": str(round(totals["f"])),
            }
        ],
    }
    session = garmin_session(client)
    known = {e["log_id"] for e in logged_foods(log)}
    try:
        session.put("connectapi", QUICK_ADD_PATH, json=payload)
    except Exception as e:
        return {"status": "push_failed", "error": str(e)[:200]}
    for entry in logged_foods(fetch_log(client, day)):
        if entry["log_id"] not in known and (entry.get("name") or "").strip() == name.strip():
            return {"status": "synced", "log_id": entry["log_id"], "meal": entry["meal"], "meal_time": entry["meal_time"]}
    return {"status": "unknown_after_push"}


def garmin_delete(client: Garmin, day: str, log_ids: list[str]) -> dict:
    session = garmin_session(client)
    try:
        response = session.request(
            "DELETE", "connectapi", f"/nutrition-service/food/logs/{day}", api=True, json={"logIds": log_ids}
        )
        status = getattr(response, "status_code", None)
    except Exception as e:
        return {"status": "delete_failed", "error": str(e)[:200]}
    remaining = [e for e in logged_foods(fetch_log(client, day)) if e.get("log_id") in log_ids]
    return {"status": "deleted" if not remaining else "delete_failed", "http_status": status}


# --- commands: direct Garmin ------------------------------------------------

def cmd_status(args) -> None:
    client = connect()
    log = fetch_log(client, args.date)
    try:
        settings = client.get_nutrition_daily_settings(args.date) or {}
    except Exception:
        settings = {}
    goals = log.get("dailyNutritionGoals") or {}
    print(
        json.dumps(
            {
                "date": args.date,
                "nutrition_status": settings.get("nutritionStatus"),
                "calorie_goal": goals.get("adjustedCalories") or goals.get("calories"),
                "macro_goals": {k: goals.get(k) for k in ("protein", "fat", "carbs") if goals.get(k) is not None},
                "meal_slots": meal_slots(log),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_show(args) -> None:
    client = connect()
    log = fetch_log(client, args.date)
    content = log.get("dailyNutritionContent") or {}
    goals = log.get("dailyNutritionGoals") or {}
    print(
        json.dumps(
            {
                "date": args.date,
                "totals": {
                    "calories": content.get("calories"),
                    "protein": content.get("protein"),
                    "fat": content.get("fat"),
                    "carbs": content.get("carbs"),
                    "percent_of_goal": content.get("caloriesPercentage"),
                },
                "goal_calories": goals.get("adjustedCalories") or goals.get("calories"),
                "entries": logged_foods(log),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_delete(args) -> None:
    client = connect()
    entries = logged_foods(fetch_log(client, args.date))
    if args.log_id:
        matches = [e for e in entries if e.get("log_id") == args.log_id]
    else:
        matches = [e for e in entries if (e.get("name") or "").strip() == args.name.strip()]
    if not matches:
        target = args.log_id or f"named '{args.name}'"
        print(f"Error: no entry {target} logged on {args.date}.", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1 and not args.all:
        print(
            json.dumps(
                {
                    "action": "refused_ambiguous",
                    "reason": "Several entries match. Pass --log-id, or --all to delete every match.",
                    "matches": matches,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(2)
    if not args.yes:
        print(
            json.dumps(
                {"action": "dry_run", "note": "Nothing deleted. Re-run with --yes.", "would_delete": matches},
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    result = garmin_delete(client, args.date, [e["log_id"] for e in matches])
    print(json.dumps({"action": result["status"], **result, "deleted": [e["name"] for e in matches]},
                     ensure_ascii=False, indent=2))


# --- commands: patterns -----------------------------------------------------

def pattern_baseline(entry: dict) -> dict | None:
    if entry.get("type") == "dish":
        try:
            return sum_macros([ingredient_macros(i) for i in entry.get("ingredients") or []])
        except ValueError:
            return None
    return None


def cmd_pattern(args) -> None:
    patterns = load_patterns()

    if args.pattern_command == "list":
        out = []
        for name, entry in patterns.items():
            row = {"name": name, "type": entry.get("type"), "aliases": entry.get("aliases") or []}
            baseline = pattern_baseline(entry)
            if baseline:
                row["baseline_kcal"] = baseline["kcal"]
            if entry.get("type") == "product":
                row["per100g_kcal"] = (entry.get("per100g") or {}).get("kcal")
            out.append(row)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if args.pattern_command == "show":
        found = resolve_pattern(patterns, args.name)
        if not found:
            print(f"Error: no pattern '{args.name}'.", file=sys.stderr)
            sys.exit(1)
        key, entry = found
        result = {"name": key, **entry}
        baseline = pattern_baseline(entry)
        if baseline:
            result["baseline"] = baseline
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.pattern_command in ("add", "set"):
        try:
            entry = json.loads(args.json)
        except ValueError as e:
            print(f"Error: bad JSON — {e}", file=sys.stderr)
            sys.exit(1)
        error = validate_pattern(entry)
        if error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        exists = args.name in patterns
        if args.pattern_command == "add" and exists:
            print(f"Error: pattern '{args.name}' exists; use pattern set.", file=sys.stderr)
            sys.exit(1)
        if args.pattern_command == "set" and not exists:
            print(f"Error: pattern '{args.name}' does not exist; use pattern add.", file=sys.stderr)
            sys.exit(1)
        entry["updated"] = date.today().isoformat()
        patterns[args.name] = entry
        save_patterns(patterns)
        result = {"action": args.pattern_command, "name": args.name}
        baseline = pattern_baseline(entry)
        if baseline:
            result["baseline"] = baseline
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.pattern_command == "rm":
        if args.name not in patterns:
            print(f"Error: no pattern '{args.name}'.", file=sys.stderr)
            sys.exit(1)
        del patterns[args.name]
        save_patterns(patterns)
        print(json.dumps({"action": "removed", "name": args.name}, ensure_ascii=False))


# --- commands: journal ------------------------------------------------------

def cmd_log(args) -> None:
    patterns = load_patterns()
    day = args.date or food_day()
    deltas: list[str] = []

    if args.pattern == "adhoc":
        if args.kcal is None or not args.name:
            print("Error: adhoc needs --name and --kcal (plus --p/--f/--c).", file=sys.stderr)
            sys.exit(1)
        display_name = args.name
        totals = {
            "kcal": round(args.kcal),
            "p": round(args.p or 0, 1),
            "f": round(args.f or 0, 1),
            "c": round(args.c or 0, 1),
        }
        confidence = args.confidence or "low"
        source = "adhoc"
    else:
        found = resolve_pattern(patterns, args.pattern)
        if not found:
            print(
                f"Error: no pattern '{args.pattern}'. Use `pattern list`, or log it as adhoc.",
                file=sys.stderr,
            )
            sys.exit(1)
        key, entry = found
        display_name = args.name or key
        if entry.get("type") == "dish":
            try:
                totals, deltas = apply_deltas(entry, patterns, args)
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                totals, portion_label = product_totals(entry, args.qty)
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            deltas = [f"portion {portion_label}"]
        confidence = args.confidence or "medium"
        source = f"pattern:{key}"

    day_data = load_day(day)
    superseded = None
    if args.supersede:
        superseded = next((e for e in day_data["events"] if e["id"] == args.supersede), None)
        if superseded is None:
            print(f"Error: no event '{args.supersede}' on {day}.", file=sys.stderr)
            sys.exit(1)

    plan = {
        "action": "log" if args.yes else "dry_run",
        "date": day,
        "meal": args.meal or "snack",
        "name": display_name,
        "source": source,
        "deltas": deltas,
        "totals": totals,
        "confidence": confidence,
        "garmin": "skip" if args.no_garmin else "push",
    }
    if superseded is not None:
        plan["supersedes"] = {"id": superseded["id"], "name": superseded.get("name"), "kcal": superseded.get("kcal")}
    if not args.yes:
        plan["note"] = "Nothing written. Re-run with --yes."
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    client = None if args.no_garmin and not (superseded and (superseded.get("garmin") or {}).get("log_id")) else connect()

    if superseded is not None:
        superseded["status"] = "superseded"
        old_log_id = (superseded.get("garmin") or {}).get("log_id")
        if old_log_id and client is not None:
            plan["superseded_garmin"] = garmin_delete(client, day, [old_log_id])
            if plan["superseded_garmin"]["status"] == "deleted":
                superseded["garmin"]["deleted"] = True

    event = {
        "id": next_event_id(day_data),
        "time": datetime.now().isoformat(timespec="seconds"),
        "meal": args.meal or "snack",
        "name": display_name,
        "source": source,
        "deltas": deltas,
        "kcal": totals["kcal"],
        "p": totals["p"],
        "f": totals["f"],
        "c": totals["c"],
        "confidence": confidence,
        "status": "active",
    }
    if args.note:
        event["note"] = args.note

    if not args.no_garmin:
        event["garmin"] = garmin_push(client, day, display_name, totals, args.meal)
        plan["garmin_result"] = event["garmin"]

    day_data["events"].append(event)
    save_day(day_data)

    active = [e for e in day_data["events"] if e.get("status") == "active"]
    plan["event_id"] = event["id"]
    plan["day_totals"] = day_totals(active)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if not args.no_garmin and event["garmin"]["status"] not in ("synced",):
        sys.exit(1)


def cmd_day(args) -> None:
    day = args.date or food_day()
    day_data = load_day(day)
    active = [e for e in day_data["events"] if e.get("status") == "active"]
    print(
        json.dumps(
            {"date": day, "totals": day_totals(active), "events": day_data["events"]},
            ensure_ascii=False,
            indent=2,
        )
    )


# --- main -------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Food tracking: pattern cache, local journal, Garmin sync.")
    sub = parser.add_subparsers(dest="command", required=True)
    today = date.today().isoformat()

    p_status = sub.add_parser("status", help="Garmin nutrition status, goals and meal slots")
    p_status.add_argument("--date", type=iso_day, default=today)
    p_status.set_defaults(func=cmd_status)

    p_show = sub.add_parser("show", help="Garmin food log for a day")
    p_show.add_argument("--date", type=iso_day, default=today)
    p_show.set_defaults(func=cmd_show)

    p_del = sub.add_parser("delete", help="Delete a Garmin entry (dry-run unless --yes)")
    group = p_del.add_mutually_exclusive_group(required=True)
    group.add_argument("--name")
    group.add_argument("--log-id", type=log_id_arg)
    p_del.add_argument("--date", type=iso_day, default=today)
    p_del.add_argument("--all", action="store_true")
    p_del.add_argument("--yes", action="store_true")
    p_del.set_defaults(func=cmd_delete)

    p_pat = sub.add_parser("pattern", help="Manage the food pattern cache")
    pat_sub = p_pat.add_subparsers(dest="pattern_command", required=True)
    pat_sub.add_parser("list")
    p_ps = pat_sub.add_parser("show")
    p_ps.add_argument("name")
    for verb in ("add", "set"):
        p_pa = pat_sub.add_parser(verb)
        p_pa.add_argument("name")
        p_pa.add_argument("--json", required=True, help="Pattern entry as JSON")
    p_pr = pat_sub.add_parser("rm")
    p_pr.add_argument("name")
    p_pat.set_defaults(func=cmd_pattern)

    p_log = sub.add_parser("log", help="Log food to the journal + Garmin (dry-run unless --yes)")
    p_log.add_argument("pattern", help="Pattern name/alias, or 'adhoc'")
    p_log.add_argument("--name", help="Display name (defaults to pattern name; required for adhoc)")
    p_log.add_argument("--meal", help="breakfast | lunch | dinner | snack")
    p_log.add_argument("--date", type=iso_day, help="Food date YYYY-MM-DD (default: today respecting day_cutoff)")
    p_log.add_argument("--qty", help="Product portion: named ('пачка') or grams ('40g')")
    p_log.add_argument("--mult", action="append", help="Scale ingredient: масло=2")
    p_log.add_argument("--without", action="append", help="Drop ingredient")
    p_log.add_argument("--set", action="append", help="Override amount: помидоры=200g")
    p_log.add_argument("--add", action="append", help="Extra item: фета=30g[@kcal,p,f,c]")
    p_log.add_argument("--portion", type=float, help="Scale whole dish")
    p_log.add_argument("--kcal", type=float, help="adhoc: calories")
    p_log.add_argument("--p", type=float, help="adhoc: protein g")
    p_log.add_argument("--f", type=float, help="adhoc: fat g")
    p_log.add_argument("--c", type=float, help="adhoc: carbs g")
    p_log.add_argument("--confidence", choices=["low", "medium", "high"])
    p_log.add_argument("--note")
    p_log.add_argument("--supersede", help="Mark an earlier event replaced (deletes its Garmin entry)")
    p_log.add_argument("--no-garmin", action="store_true", help="Journal only, skip Garmin")
    p_log.add_argument("--yes", action="store_true")
    p_log.set_defaults(func=cmd_log)

    p_day = sub.add_parser("day", help="Journal totals and events for a day")
    p_day.add_argument("--date", type=iso_day)
    p_day.set_defaults(func=cmd_day)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
