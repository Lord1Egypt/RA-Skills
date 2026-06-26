#!/usr/bin/env python3
"""Food intake tracker — writes structured CSV logs from barcode lookups or photo estimates."""

import csv
import json
import os
import sys
from datetime import datetime, timezone

WORKSPACE = os.environ.get("WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
LOG_FILE = os.environ.get("FOOD_LOG", os.path.join(WORKSPACE, "data/food_log.csv"))

FIELDNAMES = [
    "date", "time_utc", "item", "brand", "source", "servings",
    "serving_size_g", "calories", "protein_g", "carbs_g", "fat_g",
    "fiber_g", "sugar_g", "sodium_mg", "extra_nutrients"
]

# Vitamin / mineral fields we try to pull from Open Food Facts
MICRO_KEYS = [
    "vitamins-a_100g", "vitamin-d_100g", "vitamin-e_100g",
    "vitamin-k_100g", "vitamin-c_100g", "vitamin-b1_100g",
    "vitamin-b2_100g", "vitamin-b6_100g", "vitamin-b12_100g",
    "vitamin-pp_100g", "pantothenic-acid_100g", "folates_100g",
    "biotin_100g", "calcium_100g", "iron_100g", "magnesium_100g",
    "phosphorus_100g", "potassium_100g", "zinc_100g", "copper_100g",
    "manganese_100g", "selenium_100g", "chromium_100g", "molybdenum_100g",
    "iodine_100g", "caffeine_100g", "alcohol_100g",
]

def _init_csv():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def _parse_float(v):
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

def log_entry(item, brand="", source="estimate", servings=1,
              serving_size_g=None, calories=None, protein_g=None,
              carbs_g=None, fat_g=None, fiber_g=None, sugar_g=None,
              sodium_mg=None, extra_nutrients=None, discord_msg_id=None):
    _init_csv()
    now = datetime.now(timezone.utc)
    row = {
        "date": now.strftime("%Y-%m-%d"),
        "time_utc": now.strftime("%H:%M:%S"),
        "item": item,
        "brand": brand,
        "source": source,
        "servings": servings,
        "serving_size_g": serving_size_g,
        "calories": calories,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "fiber_g": fiber_g,
        "sugar_g": sugar_g,
        "sodium_mg": sodium_mg,
        "extra_nutrients": json.dumps(extra_nutrients) if extra_nutrients else "",
    }
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
    return row

def lookup_barcode(barcode, servings=1):
    """Look up a barcode via Open Food Facts and return structured nutrition data."""
    import urllib.request
    import urllib.error

    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-FoodTracker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, f"Barcode `{barcode}` not found in Open Food Facts."
        return None, f"Barcode lookup failed (HTTP {e.code})"
    except Exception as e:
        return None, f"Barcode lookup failed: {e}"

    product = data.get("product", {})
    status = data.get("status", 0)
    if not product or status == 0:
        return None, f"Barcode `{barcode}` not found in Open Food Facts."

    nutriments = product.get("nutriments", {})

    def nf(key):
        return _parse_float(nutriments.get(key))

    serving_size = product.get("serving_quantity")
    if serving_size is None:
        serving_size = _parse_float(product.get("nutriscore_data", {}).get("serving_size_quantity"))

    # Prefer per-serving values when available, otherwise per-100g
    def prefer_serving(base_key):
        srv_val = nf(f"{base_key}_serving")
        if srv_val is not None:
            return srv_val
        return nf(f"{base_key}_100g")

    has_serving = any(nf(f"{k}_serving") is not None for k in
                     ["energy-kcal", "proteins", "carbohydrates", "fat"])

    if has_serving:
        base_cal = prefer_serving("energy-kcal")
        base_protein = prefer_serving("proteins")
        base_carbs = prefer_serving("carbohydrates")
        base_fat = prefer_serving("fat")
        base_fiber = prefer_serving("fiber")
        base_sugar = prefer_serving("sugars")
        base_sodium = prefer_serving("sodium")
    else:
        base_cal = nf("energy-kcal_100g")
        base_protein = nf("proteins_100g")
        base_carbs = nf("carbohydrates_100g")
        base_fat = nf("fat_100g")
        base_fiber = nf("fiber_100g")
        base_sugar = nf("sugars_100g")
        base_sodium = nf("sodium_100g")
        serving_size = serving_size or 100

    # Collect micros
    micros = {}
    for k in MICRO_KEYS:
        v = nf(k)
        if v is not None and v > 0:
            label = k.replace("_100g", "").replace("-", " ").title()
            micros[label] = v

    item_name = product.get("product_name") or product.get("product_name_en") or f"Product {barcode}"
    brand = product.get("brands") or ""

    # Compute totals for servings
    def mult(base):
        if base is None:
            return None
        return round(base * servings, 1)

    entry = log_entry(
        item=item_name,
        brand=brand,
        source="barcode",
        servings=servings,
        serving_size_g=serving_size,
        calories=mult(base_cal),
        protein_g=mult(base_protein),
        carbs_g=mult(base_carbs),
        fat_g=mult(base_fat),
        fiber_g=mult(base_fiber),
        sugar_g=mult(base_sugar),
        sodium_mg=mult(base_sodium),
        extra_nutrients=micros if micros else None,
    )

    return entry, None


def get_daily_summary(date_str=None):
    """Return aggregated daily totals."""
    _init_csv()
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    rows = []
    with open(LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("date") == date_str:
                rows.append(row)

    if not rows:
        return date_str, [], None

    totals = {
        "calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0,
        "fiber_g": 0, "sugar_g": 0, "sodium_mg": 0,
    }
    micro_totals = {}

    for row in rows:
        for k in totals:
            v = _parse_float(row.get(k))
            if v:
                totals[k] += v
        extra = row.get("extra_nutrients")
        if extra:
            try:
                ed = json.loads(extra)
                for mk, mv in ed.items():
                    micro_totals[mk] = micro_totals.get(mk, 0) + float(mv)
            except (json.JSONDecodeError, ValueError):
                pass

    for k in totals:
        totals[k] = round(totals[k], 1)
    for mk in micro_totals:
        micro_totals[mk] = round(micro_totals[mk], 1)

    return date_str, rows, totals, micro_totals


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: tracker.py <command> [args]")
        print("Commands: lookup <barcode> [servings], summary [date]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "lookup":
        if len(sys.argv) < 3:
            print("Usage: tracker.py lookup <barcode> [servings]")
            sys.exit(1)
        bc = sys.argv[2].strip()
        srv = float(sys.argv[3]) if len(sys.argv) > 3 else 1
        entry, err = lookup_barcode(bc, srv)
        if err:
            print(f"ERROR: {err}")
            sys.exit(1)
        print(json.dumps(entry, indent=2))
    elif cmd == "summary":
        date_s = sys.argv[2] if len(sys.argv) > 2 else None
        date_s, rows, totals, *rest = get_daily_summary(date_s)
        micro_totals = rest[0] if rest else {}
        if not rows:
            print(f"No entries for {date_s}")
        else:
            print(f"Summary for {date_s} ({len(rows)} entries):")
            print(json.dumps(totals, indent=2))
            if micro_totals:
                print("Micronutrients:")
                print(json.dumps(micro_totals, indent=2))
    elif cmd == "estimate":
        # JSON via stdin for photo estimates
        data = json.loads(sys.stdin.read())
        entry = log_entry(**data)
        print(json.dumps(entry, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
