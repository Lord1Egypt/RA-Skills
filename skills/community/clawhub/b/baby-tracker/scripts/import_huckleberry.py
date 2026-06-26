#!/usr/bin/env python3
"""Import Huckleberry CSV exports into baby-tracker events.csv.

Idempotent: imported rows use deterministic event_ids based on row content.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import uuid
from pathlib import Path
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import baby_tracker  # noqa: E402

NS = uuid.uuid5(uuid.NAMESPACE_URL, "openclaw:baby-tracker:huckleberry-import:v1")


def compact_row(row: dict) -> str:
    return json.dumps({k: row.get(k, "") for k in ["Type", "Start", "End", "Duration", "Start Condition", "Start Location", "End Condition", "Notes"]}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def duration_to_min(s: str | None) -> float | None:
    if not s:
        return None
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", s.strip())
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def parse_amount(s: str | None) -> tuple[float | None, str | None]:
    if not s:
        return None, None
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*(kg|g|ml|oz|cm|c|°c)\b", s.strip(), flags=re.I)
    if not m:
        return None, None
    unit = m.group(2).lower().replace("°c", "c")
    if unit == "c":
        unit = "C"
    return float(m.group(1)), unit


def side_duration(s: str | None) -> tuple[str | None, float | None, str | None]:
    if not s:
        return None, None, None
    m = re.fullmatch(r"(\d{1,2}:\d{2})([LR])", s.strip(), flags=re.I)
    if not m:
        return None, None, s
    side = "left" if m.group(2).upper() == "L" else "right"
    return side, duration_to_min(m.group(1)), None


def ts_pair(local_text: str, tz_name: str) -> tuple[str, str]:
    return baby_tracker.parse_timestamp(local_text, tz_name)


def parse_diaper_notes(notes: str) -> tuple[str, dict]:
    n = (notes or "").strip()
    low = n.lower()
    details: dict[str, str] = {}
    if "pee" in low:
        details["pee"] = "yes"
    if "poo" in low:
        details["poo"] = "yes"
    for key in ["pee", "poo"]:
        m = re.search(rf"\b{key}\s*:\s*([a-z]+)", low)
        if m:
            details[key] = m.group(1)
    if low.startswith("both") or ("pee" in details and "poo" in details):
        subtype = "both"
    elif "pee" in details:
        subtype = "wet"
    elif "poo" in details:
        subtype = "dirty"
    elif low == "both":
        subtype = "both"
    elif low:
        subtype = low.split(",", 1)[0].strip().replace(" ", "-")
    else:
        subtype = ""
    return subtype, details


def normalize(row: dict, idx: int, tz_name: str, baby_id: str) -> dict:
    source_type = (row.get("Type") or "").strip()
    typ = source_type.lower().strip().replace(" ", "-") or "unknown"
    start = (row.get("Start") or "").strip()
    if not start:
        raise ValueError("missing Start")
    local_ts, utc_ts = ts_pair(start, tz_name)
    details = {
        "import_source": "huckleberry",
        "import_row": idx,
        "source_type": source_type,
    }
    for col, key in [
        ("End", "end"), ("Duration", "duration_text"), ("Start Condition", "start_condition"),
        ("Start Location", "start_location"), ("End Condition", "end_condition"), ("Notes", "huckleberry_notes"),
    ]:
        if row.get(col):
            details[key] = row[col]
    if row.get("End"):
        try:
            end_local, end_utc = ts_pair(row["End"], tz_name)
            details["end_local"] = end_local
            details["end_utc"] = end_utc
        except Exception:
            pass
    dur_min = duration_to_min(row.get("Duration"))
    if dur_min is not None:
        details["duration_min"] = dur_min

    subtype = ""
    metric = ""
    value = ""
    unit = ""
    notes = ""

    if typ == "growth":
        amount, amt_unit = parse_amount(row.get("Start Condition"))
        if amt_unit in {"kg", "g"}:
            subtype = "weight"; metric = "weight"; value = amount; unit = amt_unit
        elif amt_unit == "cm":
            subtype = "height"; metric = "height"; value = amount; unit = amt_unit
        elif amount is not None:
            subtype = "measurement"; metric = "measurement"; value = amount; unit = amt_unit or ""
        else:
            subtype = "growth"
    elif typ == "diaper":
        # In Huckleberry exports the human diaper text usually lands in End Condition,
        # not Notes, despite being shown as notes in the app UI.
        diaper_text = row.get("Notes") or row.get("End Condition") or ""
        subtype, parsed = parse_diaper_notes(diaper_text)
        details.update(parsed)
        # Huckleberry sometimes stores colour/consistency in odd columns for diaper rows.
        if row.get("Duration") and not duration_to_min(row.get("Duration")):
            details["poo_colour"] = row["Duration"]
        if row.get("Start Condition"):
            details["poo_consistency"] = row["Start Condition"]
    elif typ == "feed":
        loc = (row.get("Start Location") or "").strip().lower()
        if loc == "bottle":
            subtype = "bottle"
            amount, amt_unit = parse_amount(" ".join([row.get("End Condition") or "", row.get("Notes") or ""]))
            metric = "volume" if amount is not None else ""
            value = amount if amount is not None else ""
            unit = amt_unit or ""
            if "breast" in (row.get("Start Condition") or "").lower():
                details["milk"] = "breast"
        elif loc == "breast":
            subtype = "breast"
            metric = "duration" if dur_min is not None else ""
            value = dur_min if dur_min is not None else ""
            unit = "min" if dur_min is not None else ""
            for field, label in [("Start Condition", "start"), ("End Condition", "end")]:
                side, mins, raw = side_duration(row.get(field))
                if side and mins is not None:
                    details[f"{side}_min"] = details.get(f"{side}_min", 0) + mins
                    details[f"{label}_side"] = side
                elif raw:
                    details[f"{label}_raw"] = raw
            if "left_min" in details and "right_min" in details:
                details["side"] = "both"
            elif "left_min" in details:
                details["side"] = "left"
            elif "right_min" in details:
                details["side"] = "right"
        else:
            subtype = loc or "feed"
    elif typ == "sleep":
        subtype = "sleep"
        metric = "duration" if dur_min is not None else ""
        value = dur_min if dur_min is not None else ""
        unit = "min" if dur_min is not None else ""
    elif typ == "pump":
        subtype = "pump"
        candidates = [row.get("End Condition"), row.get("Start Condition"), row.get("Notes")]
        amount = amt_unit = None
        for c in candidates:
            amount, amt_unit = parse_amount(c)
            if amount is not None:
                break
        metric = "volume" if amount is not None else ("duration" if dur_min is not None else "")
        value = amount if amount is not None else (dur_min if dur_min is not None else "")
        unit = amt_unit or ("min" if dur_min is not None else "")
    elif typ == "indoor-play":
        subtype = "indoor-play"
        metric = "duration" if dur_min is not None else ""
        value = dur_min if dur_min is not None else ""
        unit = "min" if dur_min is not None else ""
    else:
        subtype = typ

    event_id = str(uuid.uuid5(NS, f"{idx}|{compact_row(row)}"))
    return {
        "event_id": event_id,
        "timestamp_local": local_ts,
        "timestamp_utc": utc_ts,
        "timezone": tz_name,
        "baby_id": baby_id,
        "type": typ,
        "subtype": subtype,
        "metric": metric,
        "value": "" if value == "" or value is None else str(value),
        "unit": unit,
        "details_json": json.dumps(details, ensure_ascii=False, sort_keys=True),
        "notes": notes,
        "source_text": compact_row(row),
        "created_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Import a Huckleberry CSV into baby-tracker events.csv")
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--data-dir", type=Path, default=baby_tracker.DEFAULT_DATA_DIR)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    paths = baby_tracker.ensure_store(args.data_dir)
    meta = baby_tracker.read_json(paths["metadata"])
    tz_name = meta.get("timezone") or "Europe/London"
    baby_id = meta.get("baby_id") or "baby-1"

    existing_ids = {r.get("event_id") for r in baby_tracker.load_events(paths["events"])}
    rows_to_add = []
    skipped = 0
    errors = []
    with args.csv_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            try:
                event = normalize(row, idx, tz_name, baby_id)
                if event["event_id"] in existing_ids:
                    skipped += 1
                else:
                    rows_to_add.append(event)
            except Exception as e:
                errors.append({"row": idx, "error": str(e), "source": row})

    if not args.dry_run and rows_to_add:
        with paths["events"].open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=baby_tracker.EVENT_HEADERS)
            writer.writerows(rows_to_add)

    summary = {
        "source": str(args.csv_path),
        "data_dir": str(args.data_dir),
        "new_events": len(rows_to_add),
        "skipped_existing": skipped,
        "errors": len(errors),
        "dry_run": args.dry_run,
        "type_counts": {},
    }
    for e in rows_to_add:
        summary["type_counts"][e["type"]] = summary["type_counts"].get(e["type"], 0) + 1
    if errors:
        summary["error_samples"] = errors[:5]
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
