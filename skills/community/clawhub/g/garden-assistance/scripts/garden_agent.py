#!/usr/bin/env python3
"""Deterministic engine for the garden assistance agent skill."""

from __future__ import annotations

import argparse
import calendar
import copy
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

CROP_KB_PATH = DATA_DIR / "crop_knowledge_base.json"
PLANTED_CROPS_PATH = DATA_DIR / "planted_crops.json"
GARDEN_PROFILE_PATH = DATA_DIR / "garden_profile.json"
GARDEN_STATE_PATH = DATA_DIR / "garden_state.json"
RECIPIENTS_PATH = DATA_DIR / "telegram_recipients.json"
WATERING_DETAIL_LOG_PATH = DATA_DIR / "watering_detail_log.json"

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
FORECAST_DAYS = 7
RAIN_SKIP_THRESHOLD_L_PER_M2 = 1.0
# Three watering tiers matched to root depth. A "surface watering" keeps the seedbed
# (1-3 cm layer) moist for germinating seeds; a "light watering" wets the shallow root
# zone (3-9 cm layer); a "deep watering" soaks the deeper root zone (9-27 cm layer).
# Crops progress surface -> light -> deep as their roots reach further down.
# Doses are the litres/m2 applied per session (already in post-layer-conversion units).
SURFACE_WATERING_L_PER_M2 = 2.0
LIGHT_WATERING_L_PER_M2 = 5.0
DEEP_WATERING_L_PER_M2 = 20.0
# Litres per m2 needed to raise volumetric water content by 1 m3/m3 across each layer.
# Equals layer thickness (m) * 1000. Surface 2 cm -> 20; shallow 6 cm -> 60; deep 18 cm -> 180.
SURFACE_LAYER_THICKNESS_L_PER_M2 = 20.0
SHALLOW_LAYER_THICKNESS_L_PER_M2 = 60.0
DEEP_LAYER_THICKNESS_L_PER_M2 = 180.0
REMINDER_TIMING_KEYS = {
    "weeks_after_direct_sowing",
    "weeks_after_indoor_sowing",
    "weeks_after_transplant",
}
REMINDER_MONTH_FILTER_KEYS = {
    "valid_sown_months",
    "valid_transplanted_months",
    "valid_due_months",
}
# Bare-minimum set of lifecycle anchors. Completing one of these reminders re-times every
# downstream reminder (see adjustment logic). Kept small on purpose: transplant and harvest
# start are already captured by update-transplanted and mark-harvested/log-harvest, and other
# reminders are either chores (timing is the gardener's choice) or downstream of these anchors.
REMINDER_ANCHOR_EVENTS = {
    "check_germination": "germination",
    "check_flowering": "flowering",
    "check_fruiting": "fruiting",
}
# Informational reminders announce a lifecycle stage/state but require no completable action.
# They surface as one-time notices (within NOTICE_WINDOW_DAYS of their trigger) rather than
# persistent tasks, and never need to be marked done.
INFORMATIONAL_REMINDER_TYPES = {
    "check_root_development",
    "transplant_window_start",
    "harvest_window_start",
    "stop_harvest",
    "watering_attention",
}
NOTICE_WINDOW_DAYS = 7
DERIVED_ANCHOR_EVENTS = {
    "transplanted_outdoors",
    "harvest_window_start",
    "harvest_started",
}
LIFECYCLE_ANCHOR_EVENTS = set(REMINDER_ANCHOR_EVENTS.values()) | DERIVED_ANCHOR_EVENTS
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def reminder_kind(reminder_type: str) -> str:
    """'informational' for one-time state notices, otherwise 'task' (completable)."""
    return "informational" if reminder_type in INFORMATIONAL_REMINDER_TYPES else "task"


class ValidationError(Exception):
    pass


class UnknownPlantError(ValidationError):
    """Raised when a requested plant_id/name is not found in the knowledge base."""
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json_atomic(path: Path, data: Any, validator=None) -> None:
    if validator is not None:
        validator(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
        with tmp_path.open("r", encoding="utf-8") as handle:
            parsed = json.load(handle)
        if validator is not None:
            validator(parsed)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def load_crop_knowledge_base() -> dict[str, Any]:
    data = load_json(CROP_KB_PATH)
    if not data:
        data = {
            "schema_version": "1.0",
            "crop_knowledge": []
        }
    return data


def load_planted_crops() -> dict[str, Any]:
    data = load_json(PLANTED_CROPS_PATH)
    if not data:
        data = {
            "schema_version": "1.0",
            "planted_crops": []
        }
    return data


def load_garden_profile() -> dict[str, Any]:
    return load_json(GARDEN_PROFILE_PATH)


def load_garden_state() -> dict[str, Any]:
    return load_json(GARDEN_STATE_PATH)


def load_recipients() -> dict[str, Any]:
    data = load_json(RECIPIENTS_PATH)
    if not data:
        data = {
            "schema_version": "1.0",
            "recipients": []
        }
    return data


def crop_index(kb: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {plant["id"]: plant for plant in kb.get("crop_knowledge", [])}


def no_nulls(value: Any, path: str = "$", allow_null_keys: tuple[str, ...] = ()) -> None:
    if value is None:
        fail(f"{path} must not be null")
    if isinstance(value, dict):
        for key, child in value.items():
            if key in allow_null_keys and child is None:
                continue
            no_nulls(child, f"{path}.{key}", allow_null_keys)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            no_nulls(child, f"{path}[{idx}]", allow_null_keys)


def require_keys(obj: dict[str, Any], keys: list[str], path: str) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{path}.{key} is required")


def require_number(value: Any, path: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        fail(f"{path} must be numeric")


def require_positive_number(value: Any, path: str) -> None:
    require_number(value, path)
    if value <= 0:
        fail(f"{path} must be > 0")


def require_int(value: Any, path: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        fail(f"{path} must be an integer")


def validate_date_string(value: Any, path: str, allow_empty: bool = True) -> None:
    if value == "" and allow_empty:
        return
    if not isinstance(value, str) or not DATE_RE.match(value):
        fail(f"{path} must be YYYY-MM-DD or empty string")
    try:
        date.fromisoformat(value)
    except ValueError:
        fail(f"{path} is not a valid date")


def validate_months(months: Any, path: str) -> None:
    if not isinstance(months, list) or not months:
        fail(f"{path} must be a non-empty month array")
    for idx, month in enumerate(months):
        require_int(month, f"{path}[{idx}]")
        if month < 1 or month > 12:
            fail(f"{path}[{idx}] must be between 1 and 12")


def validate_week_values(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            # These watering-stage and seasonality fields are validated separately.
            if key in ("deep_watering_after_weeks", "light_watering_after_weeks", "weeks"):
                continue
            if "weeks" in key or key == "germination_weeks":
                require_int(child, child_path)
            validate_week_values(child, child_path)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            validate_week_values(child, f"{path}[{idx}]")


def validate_perennial_crop_entry(plant: dict[str, Any]) -> None:
    timing = plant.get("timing", {})
    require_keys(timing, ["harvest_month_min", "harvest_month_max"], f"{plant['id']}.timing")
    validate_months([timing["harvest_month_min"]], f"{plant['id']}.timing.harvest_month_min")
    validate_months([timing["harvest_month_max"]], f"{plant['id']}.timing.harvest_month_max")
    if timing["harvest_month_min"] > timing["harvest_month_max"]:
        fail(f"{plant['id']}.timing harvest_month_min must be <= harvest_month_max")
    reminders = plant["agent_reminders"]
    require_keys(reminders, ["perennial"], f"{plant['id']}.agent_reminders")
    perennial = reminders["perennial"]
    if not isinstance(perennial, list) or not perennial:
        fail(f"{plant['id']}.agent_reminders.perennial must be non-empty")
    for idx, reminder in enumerate(perennial):
        path = f"{plant['id']}.agent_reminders.perennial[{idx}]"
        require_keys(reminder, ["type", "text", "month_trigger", "active_months"], path)
        require_int(reminder["month_trigger"], f"{path}.month_trigger")
        validate_months([reminder["month_trigger"]], f"{path}.month_trigger")
        validate_months(reminder["active_months"], f"{path}.active_months")


def validate_crop_entry(plant: dict[str, Any]) -> None:
    require_keys(
        plant,
        ["id", "name", "harvest_pattern", "market_price_dkk_per_kg", "soil_moisture", "care", "agent_reminders"],
        "plant",
    )
    if plant["harvest_pattern"] not in {"single", "continuous"}:
        fail(f"{plant['id']}.harvest_pattern is invalid")
    require_number(plant["market_price_dkk_per_kg"], f"{plant['id']}.market_price_dkk_per_kg")
    if plant["market_price_dkk_per_kg"] < 0:
        fail(f"{plant['id']}.market_price_dkk_per_kg must be >= 0")
    moisture = plant["soil_moisture"]
    require_keys(moisture, ["min_m3_m3", "optimal_min_m3_m3", "optimal_max_m3_m3", "too_wet_m3_m3"], f"{plant['id']}.soil_moisture")
    if not (moisture["min_m3_m3"] <= moisture["optimal_min_m3_m3"] <= moisture["optimal_max_m3_m3"] <= moisture["too_wet_m3_m3"]):
        fail(f"{plant['id']}.soil_moisture values are not ordered")

    for week_field in ("deep_watering_after_weeks", "light_watering_after_weeks"):
        if week_field not in plant:
            fail(f"{plant['id']}.{week_field} is required")
        value = plant[week_field]
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            fail(f"{plant['id']}.{week_field} must be null or a non-negative integer")
    lwa = plant["light_watering_after_weeks"]
    dwa = plant["deep_watering_after_weeks"]
    # The surface stage must end no later than the deep stage begins.
    if lwa is not None and dwa is not None and dwa > 0 and lwa > dwa:
        fail(f"{plant['id']}.light_watering_after_weeks must be <= deep_watering_after_weeks")

    if plant.get("lifecycle") == "perennial":
        validate_perennial_crop_entry(plant)
        return

    require_keys(plant, ["spacing", "seasonality", "sowing", "transplanting", "timing"], "plant")
    seasonality = plant["seasonality"]
    require_keys(seasonality, ["outdoor_direct_sow_windows", "indoor_sow_windows", "transplant_outdoor_windows"], plant["id"])
    for key in ["outdoor_direct_sow_windows", "indoor_sow_windows", "transplant_outdoor_windows"]:
        windows = seasonality[key]
        if not isinstance(windows, list):
            fail(f"{plant['id']}.seasonality.{key} must be a list of window dicts")
        for idx, win in enumerate(windows):
            path = f"{plant['id']}.seasonality.{key}[{idx}]"
            require_keys(win, ["reference", "weeks"], path)
            if win["reference"] not in ["last_spring_frost", "first_autumn_frost"]:
                fail(f"{path}.reference must be last_spring_frost or first_autumn_frost")
            if not isinstance(win["weeks"], list) or len(win["weeks"]) != 2:
                fail(f"{path}.weeks must be a list of 2 integers [start_weeks, end_weeks]")
            if not isinstance(win["weeks"][0], int) or not isinstance(win["weeks"][1], int):
                fail(f"{path}.weeks must contain integers")
            if win["weeks"][0] > win["weeks"][1]:
                fail(f"{path}.weeks start_weeks must be <= end_weeks")

    sowing = plant["sowing"]
    require_keys(sowing, ["depth_cm", "outdoor_direct", "indoor"], f"{plant['id']}.sowing")
    outdoor = sowing["outdoor_direct"]
    indoor = sowing["indoor"]
    require_keys(outdoor, ["recommended", "soil_temp_min_c", "soil_temp_optimal_min_c", "soil_temp_optimal_max_c", "germination_weeks"], f"{plant['id']}.sowing.outdoor_direct")
    require_keys(indoor, ["recommended", "germination_temp_min_c", "germination_temp_optimal_min_c", "germination_temp_optimal_max_c", "germination_weeks"], f"{plant['id']}.sowing.indoor")
    if not (outdoor["soil_temp_min_c"] <= outdoor["soil_temp_optimal_min_c"] <= outdoor["soil_temp_optimal_max_c"]):
        fail(f"{plant['id']}.sowing.outdoor_direct soil temperatures are not ordered")
    if not (indoor["germination_temp_min_c"] <= indoor["germination_temp_optimal_min_c"] <= indoor["germination_temp_optimal_max_c"]):
        fail(f"{plant['id']}.sowing.indoor germination temperatures are not ordered")

    transplanting = plant["transplanting"]
    if "eligible" in transplanting:
        fail(f"{plant['id']}.transplanting.eligible must not exist")
    require_keys(transplanting, ["seedling_age_weeks_min", "seedling_age_weeks_max", "outdoor_soil_temp_min_c", "outdoor_soil_temp_optimal_min_c", "outdoor_soil_temp_optimal_max_c", "hardening_off_weeks"], f"{plant['id']}.transplanting")
    if not (transplanting["outdoor_soil_temp_min_c"] <= transplanting["outdoor_soil_temp_optimal_min_c"] <= transplanting["outdoor_soil_temp_optimal_max_c"]):
        fail(f"{plant['id']}.transplanting soil temperatures are not ordered")

    timing = plant["timing"]
    for prefix in ["harvest_from_direct_sow_weeks", "harvest_from_transplant_weeks"]:
        min_key = f"{prefix}_min"
        max_key = f"{prefix}_max"
        require_keys(timing, [min_key, max_key], f"{plant['id']}.timing")
        if timing[min_key] > timing[max_key]:
            fail(f"{plant['id']}.timing {min_key} must be <= {max_key}")

    reminders = plant["agent_reminders"]
    require_keys(reminders, ["outdoor_direct", "indoor"], f"{plant['id']}.agent_reminders")
    for method in ["outdoor_direct", "indoor"]:
        if not isinstance(reminders[method], list) or not reminders[method]:
            fail(f"{plant['id']}.agent_reminders.{method} must be non-empty")
        for idx, reminder in enumerate(reminders[method]):
            path = f"{plant['id']}.agent_reminders.{method}[{idx}]"
            require_keys(reminder, ["type", "text"], path)
            timing_keys = [key for key in REMINDER_TIMING_KEYS if key in reminder]
            if len(timing_keys) != 1:
                fail(f"{path} must have exactly one reminder timing key")
            require_int(reminder[timing_keys[0]], f"{path}.{timing_keys[0]}")
            for month_key in REMINDER_MONTH_FILTER_KEYS:
                if month_key in reminder:
                    validate_months(reminder[month_key], f"{path}.{month_key}")
    validate_week_values(plant, plant["id"])


def validate_crop_knowledge_base(data: dict[str, Any]) -> None:
    no_nulls(data, allow_null_keys=("deep_watering_after_weeks", "light_watering_after_weeks"))
    require_keys(data, ["schema_version", "crop_knowledge"], "$")
    if not isinstance(data["crop_knowledge"], list):
        fail("$.crop_knowledge must be a list")
    seen = set()
    for plant in data["crop_knowledge"]:
        validate_crop_entry(plant)
        if plant["id"] in seen:
            fail(f"duplicate plant id {plant['id']}")
        seen.add(plant["id"])


def validate_garden_profile(data: dict[str, Any]) -> None:
    if not data:
        fail("Garden profile is not configured. Please run the 'configure-profile' command first.")
    no_nulls(data)
    require_keys(data, ["schema_version", "location", "garden"], "$")
    require_keys(data["location"], ["latitude", "longitude", "timezone"], "$.location")
    data["location"].setdefault("country", "Local")
    data["location"].setdefault("region", "Local")
    require_keys(data["garden"], ["bed_width_m", "bed_length_m"], "$.garden")
    for key in ["bed_width_m", "bed_length_m"]:
        require_number(data["garden"][key], f"$.garden.{key}")
        if data["garden"][key] <= 0:
            fail(f"$.garden.{key} must be > 0")
    if "climate" in data:
        require_keys(data["climate"], ["last_spring_frost", "first_autumn_frost"], "$.climate")
        for key in ["last_spring_frost", "first_autumn_frost"]:
            val = data["climate"][key]
            parts = val.split("-")
            if len(parts) != 2:
                fail(f"$.climate.{key} must be in MM-DD format")
            try:
                m = int(parts[0])
                d = int(parts[1])
                date(2000, m, d)
            except ValueError:
                fail(f"$.climate.{key} must be a valid date in MM-DD format")


def fetch_frost_dates_from_archive(lat: float, lon: float) -> tuple[str, str]:
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date=2025-01-01&end_date=2025-12-31"
        f"&daily=temperature_2m_min"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "GardenAssistance"})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode("utf-8"))
    
    daily = res.get("daily", {})
    dates = daily.get("time", [])
    temps = daily.get("temperature_2m_min", [])
    
    is_southern = (lat < 0)
    spring_dates = []
    autumn_dates = []
    
    for d_str, temp in zip(dates, temps):
        if temp is None:
            continue
        d = date.fromisoformat(d_str)
        is_frost = (temp <= 0.0)
        
        if is_southern:
            if d.month >= 7:
                if is_frost:
                    spring_dates.append(d)
            else:
                if is_frost:
                    autumn_dates.append(d)
        else:
            if d.month <= 6:
                if is_frost:
                    spring_dates.append(d)
            else:
                if is_frost:
                    autumn_dates.append(d)
                    
    if spring_dates:
        lfd = max(spring_dates)
        last_frost_str = f"{lfd.month:02d}-{lfd.day:02d}"
    else:
        last_frost_str = "07-01" if is_southern else "01-01"
        
    if autumn_dates:
        ffd = min(autumn_dates)
        first_frost_str = f"{ffd.month:02d}-{ffd.day:02d}"
    else:
        first_frost_str = "06-30" if is_southern else "12-31"
        
    return last_frost_str, first_frost_str


def configure_profile(args: argparse.Namespace) -> dict[str, Any]:
    if not CROP_KB_PATH.exists():
        example_path = CROP_KB_PATH.parent / "crop_knowledge_base.example.json"
        if example_path.exists():
            try:
                CROP_KB_PATH.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")
            except OSError:
                pass

    profile = load_garden_profile()
    profile.setdefault("schema_version", "1.0")
    profile.setdefault("location", {})
    profile.setdefault("climate", {})
    
    profile["location"]["latitude"] = args.latitude
    profile["location"]["longitude"] = args.longitude
    profile["location"]["timezone"] = args.timezone
    
    if args.last_frost and args.first_frost:
        last_frost = args.last_frost
        first_frost = args.first_frost
    else:
        try:
            last_frost, first_frost = fetch_frost_dates_from_archive(args.latitude, args.longitude)
        except Exception as exc:
            fail(f"Failed to auto-detect frost dates via Open-Meteo Archive: {exc}. Please specify --last-frost and --first-frost manually.")
            
    profile["climate"]["last_spring_frost"] = last_frost
    profile["climate"]["first_autumn_frost"] = first_frost
    
    profile.setdefault("garden", {})
    if args.bed_width > 0:
        profile["garden"]["bed_width_m"] = args.bed_width
    elif "bed_width_m" not in profile["garden"]:
        profile["garden"]["bed_width_m"] = 1.2

    if args.bed_length > 0:
        profile["garden"]["bed_length_m"] = args.bed_length
    elif "bed_length_m" not in profile["garden"]:
        profile["garden"]["bed_length_m"] = 3.0
    
    save_json_atomic(GARDEN_PROFILE_PATH, profile, validate_garden_profile)
    return {
        "summary": f"Configured garden profile at {args.latitude}, {args.longitude} with timezone {args.timezone}. Frost dates: Last spring frost = {last_frost}, First autumn frost = {first_frost}.",
        "profile": profile
    }


def get_local_seasonality(plant: dict[str, Any], profile: dict[str, Any]) -> dict[str, list[int]]:
    if "seasonality" not in plant:
        return {
            "indoor_sow_months": [],
            "outdoor_direct_sow_months": [],
            "transplant_outdoor_months": [],
        }
        
    climate = profile.get("climate", {})
    if not climate or "last_spring_frost" not in climate or "first_autumn_frost" not in climate:
        lfd_str = "05-01"
        ffd_str = "11-01"
    else:
        lfd_str = climate["last_spring_frost"]
        ffd_str = climate["first_autumn_frost"]
        
    lfd_m, lfd_d = map(int, lfd_str.split("-"))
    ffd_m, ffd_d = map(int, ffd_str.split("-"))
    
    year = 2026
    lfd_date = date(year, lfd_m, lfd_d)
    ffd_date = date(year, ffd_m, ffd_d)
    
    def resolve_ref(ref_name: str) -> date:
        if ref_name == "first_autumn_frost":
            return ffd_date
        return lfd_date
        
    def windows_to_months(windows: list[dict[str, Any]]) -> list[int]:
        months = set()
        for win in windows:
            ref = resolve_ref(win.get("reference", "last_spring_frost"))
            start_weeks, end_weeks = win["weeks"]
            start_date = ref + timedelta(weeks=start_weeks)
            end_date = ref + timedelta(weeks=end_weeks)
            
            curr = start_date
            while curr <= end_date:
                months.add(curr.month)
                curr += timedelta(days=1)
        return sorted(list(months))
        
    season = plant["seasonality"]
    return {
        "indoor_sow_months": windows_to_months(season.get("indoor_sow_windows", [])),
        "outdoor_direct_sow_months": windows_to_months(season.get("outdoor_direct_sow_windows", [])),
        "transplant_outdoor_months": windows_to_months(season.get("transplant_outdoor_windows", [])),
    }


def bed_area_m2(profile: dict[str, Any]) -> float:
    garden = profile["garden"]
    return round(garden["bed_width_m"] * garden["bed_length_m"], 2)


def validate_garden_state(data: dict[str, Any]) -> None:
    no_nulls(data)
    require_keys(data, ["schema_version", "forecast_generated_at", "source", "location", "daily"], "$")
    if data["source"] != "open-meteo":
        fail("$.source must be open-meteo")
    require_keys(data["location"], ["latitude", "longitude", "timezone"], "$.location")
    if not isinstance(data["daily"], list):
        fail("$.daily must be a list")
    for idx, day in enumerate(data["daily"]):
        path = f"$.daily[{idx}]"
        require_keys(
            day,
            [
                "date",
                "air_temperature_c",
                "precipitation_mm",
                "et0_fao_mm",
                "soil_temperature_6cm_c",
                "soil_moisture_1_to_3cm_m3_m3",
                "soil_moisture_3_to_9cm_m3_m3",
                "soil_moisture_9_to_27cm_m3_m3",
            ],
            path,
        )
        validate_date_string(day["date"], f"{path}.date", allow_empty=False)
        for range_key in ["air_temperature_c", "soil_temperature_6cm_c", "soil_moisture_1_to_3cm_m3_m3", "soil_moisture_3_to_9cm_m3_m3", "soil_moisture_9_to_27cm_m3_m3"]:
            require_keys(day[range_key], ["min", "max"], f"{path}.{range_key}")
            require_number(day[range_key]["min"], f"{path}.{range_key}.min")
            require_number(day[range_key]["max"], f"{path}.{range_key}.max")
            if day[range_key]["min"] > day[range_key]["max"]:
                fail(f"{path}.{range_key}.min must be <= max")
        for key in ["precipitation_mm", "et0_fao_mm"]:
            require_number(day[key], f"{path}.{key}")
            if day[key] < 0:
                fail(f"{path}.{key} must be >= 0")


def validate_recipients(data: dict[str, Any]) -> None:
    no_nulls(data)
    require_keys(data, ["schema_version", "recipients"], "$")
    if not isinstance(data["recipients"], list):
        fail("$.recipients must be a list")
    seen = set()
    for idx, recipient in enumerate(data["recipients"]):
        path = f"$.recipients[{idx}]"
        require_keys(recipient, ["label", "target", "enabled"], path)
        if not isinstance(recipient["label"], str) or not recipient["label"].strip():
            fail(f"{path}.label must be a non-empty string")
        if not isinstance(recipient["target"], str) or not recipient["target"].strip():
            fail(f"{path}.target must be a non-empty string")
        if not isinstance(recipient["enabled"], bool):
            fail(f"{path}.enabled must be boolean")
        if recipient["target"] in seen:
            fail(f"duplicate recipient target {recipient['target']}")
        seen.add(recipient["target"])


def validate_harvest_entry(entry: dict[str, Any], path: str) -> None:
    require_keys(entry, ["harvest_id", "date", "weight_kg", "notes", "created_date"], path)
    if not isinstance(entry["harvest_id"], str) or not re.match(r"^harvest_\d+$", entry["harvest_id"]):
        fail(f"{path}.harvest_id is invalid")
    validate_date_string(entry["date"], f"{path}.date", allow_empty=False)
    require_positive_number(entry["weight_kg"], f"{path}.weight_kg")
    if not isinstance(entry["notes"], str):
        fail(f"{path}.notes must be a string")
    validate_date_string(entry["created_date"], f"{path}.created_date", allow_empty=False)


def validate_planted_crop_entry(crop: dict[str, Any], kb: dict[str, Any]) -> None:
    plants = crop_index(kb)
    require_keys(crop, ["id", "plant_id", "display_name", "planting_method", "dates", "status", "tracking", "agent_state", "notes"], "crop")
    if crop["plant_id"] not in plants:
        fail(f"{crop['id']}.plant_id does not exist in crop knowledge")
    if crop["planting_method"] not in {"indoor", "outdoor_direct", "perennial"}:
        fail(f"{crop['id']}.planting_method is invalid")
    dates = crop["dates"]
    require_keys(dates, ["sown_date", "transplanted_date", "harvest_started_date", "harvest_finished_date"], f"{crop['id']}.dates")
    for key, value in dates.items():
        validate_date_string(value, f"{crop['id']}.dates.{key}", allow_empty=True)
    status = crop["status"]
    require_keys(status, ["currently_active", "started_indoors", "transplanted_outdoors", "harvest_started", "harvest_finished", "harvest_completed"], f"{crop['id']}.status")
    if crop["planting_method"] == "indoor" and status["started_indoors"] is not True:
        fail(f"{crop['id']} indoor crops must have started_indoors true")
    if crop["planting_method"] == "outdoor_direct" and status["started_indoors"] is not False:
        fail(f"{crop['id']} outdoor_direct crops must have started_indoors false")
    for key, value in status.items():
        if not isinstance(value, bool):
            fail(f"{crop['id']}.status.{key} must be boolean")
    tracking = crop["tracking"]
    require_keys(tracking, ["last_watered_date", "last_fertilized_date", "last_agent_review_date"], f"{crop['id']}.tracking")
    for key, value in tracking.items():
        validate_date_string(value, f"{crop['id']}.tracking.{key}", allow_empty=True)
    agent_state = crop["agent_state"]
    require_keys(agent_state, ["active_reminder_ids", "completed_reminder_ids", "suppressed_reminder_ids"], f"{crop['id']}.agent_state")
    for key in ["active_reminder_ids", "completed_reminder_ids", "suppressed_reminder_ids"]:
        if not isinstance(agent_state[key], list) or not all(isinstance(item, str) for item in agent_state[key]):
            fail(f"{crop['id']}.agent_state.{key} must be a string list")
    if "schedule_adjustments" in agent_state:
        if not isinstance(agent_state["schedule_adjustments"], list):
            fail(f"{crop['id']}.agent_state.schedule_adjustments must be a list")
        seen_adjustments = set()
        for idx, adjustment in enumerate(agent_state["schedule_adjustments"]):
            path = f"{crop['id']}.agent_state.schedule_adjustments[{idx}]"
            require_keys(
                adjustment,
                [
                    "adjustment_id",
                    "anchor_event",
                    "nominal_anchor_date",
                    "adjusted_anchor_date_before_change",
                    "actual_anchor_date",
                    "offset_days",
                    "reason",
                    "created_date",
                ],
                path,
            )
            if adjustment["adjustment_id"] in seen_adjustments:
                fail(f"{path}.adjustment_id is duplicated")
            seen_adjustments.add(adjustment["adjustment_id"])
            if adjustment["anchor_event"] not in LIFECYCLE_ANCHOR_EVENTS:
                fail(f"{path}.anchor_event is invalid")
            if "anchor_reminder_id" in adjustment and not isinstance(adjustment["anchor_reminder_id"], str):
                fail(f"{path}.anchor_reminder_id must be a string")
            for key in ["nominal_anchor_date", "adjusted_anchor_date_before_change", "actual_anchor_date", "created_date"]:
                validate_date_string(adjustment[key], f"{path}.{key}", allow_empty=False)
            require_int(adjustment["offset_days"], f"{path}.offset_days")
            if not isinstance(adjustment["reason"], str) or not adjustment["reason"].strip():
                fail(f"{path}.reason must be a non-empty string")
    if "harvest_log" in crop:
        if not isinstance(crop["harvest_log"], list):
            fail(f"{crop['id']}.harvest_log must be a list")
        seen_harvests = set()
        for idx, entry in enumerate(crop["harvest_log"]):
            path = f"{crop['id']}.harvest_log[{idx}]"
            validate_harvest_entry(entry, path)
            if entry["harvest_id"] in seen_harvests:
                fail(f"{path}.harvest_id is duplicated")
            seen_harvests.add(entry["harvest_id"])


def validate_planted_crops(data: dict[str, Any], kb: dict[str, Any]) -> None:
    no_nulls(data)
    require_keys(data, ["schema_version", "planted_crops"], "$")
    if not isinstance(data["planted_crops"], list):
        fail("$.planted_crops must be a list")
    seen = set()
    for crop in data["planted_crops"]:
        validate_planted_crop_entry(crop, kb)
        if crop["id"] in seen:
            fail(f"duplicate planted crop id {crop['id']}")
        seen.add(crop["id"])


def validate_all() -> None:
    kb = load_crop_knowledge_base()
    validate_crop_knowledge_base(kb)
    validate_garden_profile(load_garden_profile())
    state = load_garden_state()
    if state:
        validate_garden_state(state)
    validate_recipients(load_recipients())
    validate_planted_crops(load_planted_crops(), kb)


def save_planted_crops(data: dict[str, Any]) -> None:
    kb = load_crop_knowledge_base()
    # Clean up old perennial reminder IDs
    today_year = date.today().year
    for crop in data.get("planted_crops", []):
        if crop.get("planting_method") == "perennial":
            for list_key in ("completed_reminder_ids", "suppressed_reminder_ids"):
                lst = crop["agent_state"].get(list_key, [])
                new_lst = []
                for rid in lst:
                    parts = rid.split(":")
                    if len(parts) == 4 and parts[1] == "month_trigger":
                        try:
                            y = int(parts[3])
                            if y < today_year - 1:
                                continue  # discard
                        except ValueError:
                            pass
                    new_lst.append(rid)
                crop["agent_state"][list_key] = new_lst
    save_json_atomic(PLANTED_CROPS_PATH, data, lambda candidate: validate_planted_crops(candidate, kb))


def save_garden_state(data: dict[str, Any]) -> None:
    save_json_atomic(GARDEN_STATE_PATH, data, validate_garden_state)


def save_crop_knowledge_base(data: dict[str, Any]) -> None:
    save_json_atomic(CROP_KB_PATH, data, validate_crop_knowledge_base)


def list_kb_crops(kb: dict[str, Any]) -> dict[str, Any]:
    crops = [
        {
            "plant_id": p["id"],
            "name": p["name"],
            "lifecycle": p.get("lifecycle", "annual"),
        }
        for p in kb["crop_knowledge"]
    ]
    crops.sort(key=lambda c: c["plant_id"])
    if not crops:
        instruction = (
            "The crop knowledge base is empty. Please ask the user if they "
            "already know some crops that they will plant. These should be added "
            "to the knowledge base using the add-kb-crop command."
        )
        return {
            "summary": instruction,
            "instruction": instruction,
            "crop_count": 0,
            "crops": [],
        }
    return {
        "summary": f"{len(crops)} crop(s) in knowledge base.",
        "crop_count": len(crops),
        "crops": crops,
    }


DEFAULT_ANNUAL_TEMPLATE = {
    "harvest_pattern": "single",
    "market_price_dkk_per_kg": 20,
    "light_watering_after_weeks": 2,
    "deep_watering_after_weeks": 6,
    "soil_moisture": {
        "min_m3_m3": 0.15,
        "optimal_min_m3_m3": 0.20,
        "optimal_max_m3_m3": 0.30,
        "too_wet_m3_m3": 0.40
    },
    "care": {
        "water_need": "medium",
        "drought_sensitivity": "medium",
        "heat_sensitive": False,
        "bolting_risk": "none",
        "notes": "Care guidelines placeholder."
    },
    "spacing": {
        "plant_spacing_cm": 10,
        "row_spacing_cm": 30
    },
    "seasonality": {
        "indoor_sow_windows": [
            {"reference": "last_spring_frost", "weeks": [-8, -4]}
        ],
        "outdoor_direct_sow_windows": [
            {"reference": "last_spring_frost", "weeks": [-4, 4]}
        ],
        "transplant_outdoor_windows": [
            {"reference": "last_spring_frost", "weeks": [0, 8]}
        ]
    },
    "sowing": {
        "depth_cm": 1.0,
        "indoor": {
            "recommended": False,
            "germination_temp_min_c": 10,
            "germination_temp_optimal_min_c": 15,
            "germination_temp_optimal_max_c": 22,
            "germination_weeks": 2
        },
        "outdoor_direct": {
            "recommended": True,
            "soil_temp_min_c": 8,
            "soil_temp_optimal_min_c": 12,
            "soil_temp_optimal_max_c": 20,
            "germination_weeks": 2
        }
    },
    "transplanting": {
        "seedling_age_weeks_min": 4,
        "seedling_age_weeks_max": 6,
        "hardening_off_weeks": 1,
        "outdoor_soil_temp_min_c": 10,
        "outdoor_soil_temp_optimal_min_c": 14,
        "outdoor_soil_temp_optimal_max_c": 20
    },
    "timing": {
        "harvest_from_direct_sow_weeks_min": 10,
        "harvest_from_direct_sow_weeks_max": 14,
        "harvest_from_transplant_weeks_min": 8,
        "harvest_from_transplant_weeks_max": 12,
        "harvest_duration_weeks": 4
    },
    "agent_reminders": {
        "indoor": [
            {
                "type": "check_germination",
                "text": "Check if seedlings have germinated indoors.",
                "weeks_after_indoor_sowing": 2
            }
        ],
        "outdoor_direct": [
            {
                "type": "check_germination",
                "text": "Check for outdoor seedling emergence.",
                "weeks_after_direct_sowing": 2
            }
        ]
    }
}

DEFAULT_PERENNIAL_TEMPLATE = {
    "lifecycle": "perennial",
    "harvest_pattern": "single",
    "market_price_dkk_per_kg": 40,
    "light_watering_after_weeks": 2,
    "deep_watering_after_weeks": 6,
    "soil_moisture": {
        "min_m3_m3": 0.15,
        "optimal_min_m3_m3": 0.20,
        "optimal_max_m3_m3": 0.30,
        "too_wet_m3_m3": 0.40
    },
    "care": {
        "water_need": "medium",
        "drought_sensitivity": "medium",
        "heat_sensitive": False,
        "bolting_risk": "none",
        "notes": "Care guidelines placeholder."
    },
    "timing": {
        "harvest_month_min": 5,
        "harvest_month_max": 7
    },
    "agent_reminders": {
        "perennial": [
            {
                "type": "mulch",
                "text": "Apply compost or mulch to feed the soil and protect roots.",
                "month_trigger": 3,
                "active_months": [3, 4]
            }
        ]
    }
}


def add_kb_crop(args: argparse.Namespace) -> dict[str, Any]:
    if args.from_file == "-":
        try:
            raw = json.loads(sys.stdin.read())
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON from stdin: {exc}")
    else:
        path = Path(args.from_file)
        if not path.exists():
            fail(f"File not found: {args.from_file}")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {args.from_file}: {exc}")
    validate_crop_entry(raw)
    kb = load_crop_knowledge_base()
    existing_ids = {p["id"] for p in kb["crop_knowledge"]}
    if raw["id"] in existing_ids:
        fail(f"Plant id '{raw['id']}' already exists in the knowledge base.")
    kb["crop_knowledge"].append(raw)
    save_crop_knowledge_base(kb)
    
    if args.from_file != "-":
        path = Path(args.from_file)
        if path.exists() and path.resolve().parent == DATA_DIR.resolve():
            try:
                path.unlink()
            except OSError:
                pass

    return {
        "summary": f"Added '{raw['name']}' (plant_id: {raw['id']}) to the knowledge base.",
        "plant_id": raw["id"],
        "name": raw["name"],
        "lifecycle": raw.get("lifecycle", "annual"),
    }


def delete_kb_crop(plant_id: str) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    original_len = len(kb["crop_knowledge"])
    kb["crop_knowledge"] = [p for p in kb["crop_knowledge"] if p["id"] != plant_id]
    if len(kb["crop_knowledge"]) == original_len:
        fail(f"Plant id '{plant_id}' not found in the knowledge base.")
    save_crop_knowledge_base(kb)
    return {
        "summary": f"Deleted '{plant_id}' from the knowledge base.",
        "plant_id": plant_id,
    }


def edit_kb_crop(args: argparse.Namespace) -> dict[str, Any]:
    if args.from_file == "-":
        try:
            raw = json.loads(sys.stdin.read())
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON from stdin: {exc}")
    else:
        path = Path(args.from_file)
        if not path.exists():
            fail(f"File not found: {args.from_file}")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {args.from_file}: {exc}")
    if raw.get("id") != args.plant_id:
        fail(f"Plant ID in file '{raw.get('id')}' does not match requested --plant-id '{args.plant_id}'.")
    validate_crop_entry(raw)
    kb = load_crop_knowledge_base()
    found = False
    for idx, p in enumerate(kb["crop_knowledge"]):
        if p["id"] == args.plant_id:
            kb["crop_knowledge"][idx] = raw
            found = True
            break
    if not found:
        fail(f"Plant id '{args.plant_id}' not found in the knowledge base.")
    save_crop_knowledge_base(kb)
    return {
        "summary": f"Updated '{raw['name']}' (plant_id: {raw['id']}) in the knowledge base.",
        "plant_id": raw["id"],
        "name": raw["name"],
        "lifecycle": raw.get("lifecycle", "annual"),
    }


def scaffold_kb_crop(args: argparse.Namespace) -> Any:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    
    if args.template:
        template_id = resolve_plant_id(args.template, plants)
        template_crop = copy.deepcopy(plants[template_id])
        template_crop["id"] = args.plant_id
        template_crop["name"] = args.display_name or args.plant_id.replace("_", " ").title()
        res = template_crop
    else:
        name = args.display_name or args.plant_id.replace("_", " ").title()
        if args.lifecycle == "perennial":
            res = copy.deepcopy(DEFAULT_PERENNIAL_TEMPLATE)
        else:
            res = copy.deepcopy(DEFAULT_ANNUAL_TEMPLATE)
        res["id"] = args.plant_id
        res["name"] = name
        
    if args.file:
        filename = Path(args.file).name
        path = DATA_DIR / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {
            "summary": f"Created template for '{res['name']}' at data/{filename}."
        }
    else:
        return res


def open_meteo_url(profile: dict[str, Any]) -> str:
    loc = profile["location"]
    params = {
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
        "timezone": loc["timezone"],
        "forecast_days": FORECAST_DAYS,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
        "hourly": "soil_temperature_6cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm",
    }
    return f"{OPEN_METEO_URL}?{urllib.parse.urlencode(params)}"


def fetch_json(url: str, timeout: int = 20) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "garden-assistance-agent-skill/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def aggregate_hourly_by_day(hourly: dict[str, list[Any]]) -> dict[str, dict[str, dict[str, float]]]:
    required = [
        "time", "soil_temperature_6cm",
        "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm",
    ]
    for key in required:
        if key not in hourly or not hourly[key]:
            fail(f"Open-Meteo hourly.{key} is missing or empty")
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for timestamp, temp, moisture_surface, moisture_shallow, moisture_deep in zip(
        hourly["time"],
        hourly["soil_temperature_6cm"],
        hourly["soil_moisture_1_to_3cm"],
        hourly["soil_moisture_3_to_9cm"],
        hourly["soil_moisture_9_to_27cm"],
    ):
        day = timestamp[:10]
        grouped[day]["soil_temperature_6cm"].append(float(temp))
        grouped[day]["soil_moisture_1_to_3cm"].append(float(moisture_surface))
        grouped[day]["soil_moisture_3_to_9cm"].append(float(moisture_shallow))
        grouped[day]["soil_moisture_9_to_27cm"].append(float(moisture_deep))
    result: dict[str, dict[str, dict[str, float]]] = {}
    for day, values in grouped.items():
        result[day] = {
            "soil_temperature_6cm_c": {
                "min": round(min(values["soil_temperature_6cm"]), 2),
                "max": round(max(values["soil_temperature_6cm"]), 2),
            },
            "soil_moisture_1_to_3cm_m3_m3": {
                "min": round(min(values["soil_moisture_1_to_3cm"]), 3),
                "max": round(max(values["soil_moisture_1_to_3cm"]), 3),
            },
            "soil_moisture_3_to_9cm_m3_m3": {
                "min": round(min(values["soil_moisture_3_to_9cm"]), 3),
                "max": round(max(values["soil_moisture_3_to_9cm"]), 3),
            },
            "soil_moisture_9_to_27cm_m3_m3": {
                "min": round(min(values["soil_moisture_9_to_27cm"]), 3),
                "max": round(max(values["soil_moisture_9_to_27cm"]), 3),
            },
        }
    return result


def parse_open_meteo_forecast(payload: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    daily = payload.get("daily") or {}
    hourly = payload.get("hourly") or {}
    daily_keys = ["time", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "et0_fao_evapotranspiration"]
    for key in daily_keys:
        if key not in daily or not daily[key]:
            fail(f"Open-Meteo daily.{key} is missing or empty")
    soil_by_day = aggregate_hourly_by_day(hourly)
    days = []
    for idx, day in enumerate(daily["time"]):
        if day not in soil_by_day:
            fail(f"No hourly soil data found for {day}")
        days.append(
            {
                "date": day,
                "air_temperature_c": {
                    "min": round(float(daily["temperature_2m_min"][idx]), 2),
                    "max": round(float(daily["temperature_2m_max"][idx]), 2),
                },
                "precipitation_mm": round(float(daily["precipitation_sum"][idx]), 2),
                "et0_fao_mm": round(float(daily["et0_fao_evapotranspiration"][idx]), 2),
                **soil_by_day[day],
            }
        )
    loc = profile["location"]
    state = {
        "schema_version": "1.0",
        "forecast_generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": "open-meteo",
        "location": {
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "timezone": loc["timezone"],
        },
        "daily": days,
    }
    validate_garden_state(state)
    return state


def update_weekly_forecast() -> dict[str, Any]:
    profile = load_garden_profile()
    validate_garden_profile(profile)
    payload = fetch_json(open_meteo_url(profile))
    state = parse_open_meteo_forecast(payload, profile)
    save_garden_state(state)
    return state


def clamp_score(score: int) -> int:
    return max(0, min(100, score))


def status_from_score(score: int) -> str:
    if score >= 80:
        return "ideal"
    if score >= 60:
        return "good"
    if score >= 40:
        return "acceptable"
    if score >= 20:
        return "risky"
    return "not_recommended"


def evaluate_outdoor_sowing(plant: dict[str, Any], garden_state: dict[str, Any], current_month: int) -> dict[str, Any]:
    score = 50
    reasons = []
    outdoor = plant["sowing"]["outdoor_direct"]
    profile = load_garden_profile()
    local_season = get_local_seasonality(plant, profile)
    months = local_season["outdoor_direct_sow_months"]
    if current_month in months:
        score += 20
        reasons.append("Current month is within the recommended outdoor sowing window.")
    else:
        score -= 20
        reasons.append("Current month is outside the recommended outdoor sowing window.")
    if outdoor["recommended"]:
        score += 10
    else:
        score -= 15
        reasons.append("Outdoor direct sowing is marked as less suitable for this crop.")

    if garden_state["daily"]:
        first = garden_state["daily"][0]
        soil_temp = first["soil_temperature_6cm_c"]
        soil_moisture = first["soil_moisture_3_to_9cm_m3_m3"]
        moisture = plant["soil_moisture"]
        if soil_temp["max"] < outdoor["soil_temp_min_c"]:
            score -= 25
            reasons.append("Forecast 6 cm soil temperature is below the crop minimum.")
        elif soil_temp["max"] >= outdoor["soil_temp_optimal_min_c"] and soil_temp["min"] <= outdoor["soil_temp_optimal_max_c"]:
            score += 20
            reasons.append("Forecast 6 cm soil temperature overlaps the optimal range.")
        else:
            reasons.append("Forecast 6 cm soil temperature is usable but not ideal.")
        if soil_moisture["min"] < moisture["min_m3_m3"]:
            score -= 20
            reasons.append("Forecast 3-9 cm soil moisture falls below the crop minimum.")
        elif soil_moisture["max"] > moisture["too_wet_m3_m3"]:
            score -= 20
            reasons.append("Forecast 3-9 cm soil moisture is too wet for this crop.")
        elif soil_moisture["min"] >= moisture["optimal_min_m3_m3"] and soil_moisture["max"] <= moisture["optimal_max_m3_m3"]:
            score += 10
            reasons.append("Forecast 3-9 cm soil moisture is within the optimal range.")
    else:
        reasons.append("No weekly forecast is available yet; run update-weekly-forecast for soil conditions.")

    score = clamp_score(score)
    return {"plant_id": plant["id"], "crop_name": plant["name"], "method": "outdoor_direct", "score": score, "status": status_from_score(score)}


def evaluate_indoor_sowing(plant: dict[str, Any], current_month: int) -> dict[str, Any]:
    score = 50
    reasons = []
    profile = load_garden_profile()
    local_season = get_local_seasonality(plant, profile)
    months = local_season["indoor_sow_months"]
    if current_month in months:
        score += 25
        reasons.append("Current month is within the recommended indoor sowing window.")
    else:
        score -= 20
        reasons.append("Current month is outside the recommended indoor sowing window.")
    if plant["sowing"]["indoor"]["recommended"]:
        score += 15
        reasons.append("Indoor sowing is recommended for this crop.")
    else:
        score -= 15
        reasons.append("Indoor sowing is marked as less suitable for this crop.")
    score = clamp_score(score)
    return {"plant_id": plant["id"], "crop_name": plant["name"], "method": "indoor", "score": score, "status": status_from_score(score)}


def recommend_crops(kb: dict[str, Any], garden_state: dict[str, Any], current_month: int) -> list[dict[str, Any]]:
    recommendations = []
    for plant in kb["crop_knowledge"]:
        if plant.get("lifecycle") == "perennial":
            continue
        recommendations.append(evaluate_outdoor_sowing(plant, garden_state, current_month))
        recommendations.append(evaluate_indoor_sowing(plant, current_month))
    filtered = [r for r in recommendations if r["status"] not in {"not_recommended", "risky"}]
    sorted_recs = sorted(filtered, key=lambda item: item["score"], reverse=True)
    for r in sorted_recs:
        r.pop("score", None)
    return sorted_recs


def reminder_id(reminder: dict[str, Any]) -> str:
    timing_key = next(key for key in REMINDER_TIMING_KEYS if key in reminder)
    return f"{reminder['type']}:{timing_key}:{reminder[timing_key]}"


def parse_date_or_none(value: str) -> date | None:
    return date.fromisoformat(value) if value else None


def crop_schedule_adjustments(crop: dict[str, Any]) -> list[dict[str, Any]]:
    return crop.get("agent_state", {}).get("schedule_adjustments", [])


def next_schedule_adjustment_id(crop: dict[str, Any]) -> str:
    max_num = 0
    for adjustment in crop_schedule_adjustments(crop):
        match = re.match(r"^adj_(\d+)$", adjustment.get("adjustment_id", ""))
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"adj_{max_num + 1:03d}"


def schedule_base_date(planted_crop: dict[str, Any], timing_key: str) -> date | None:
    if timing_key in {"weeks_after_direct_sowing", "weeks_after_indoor_sowing"}:
        return parse_date_or_none(planted_crop["dates"]["sown_date"])
    return parse_date_or_none(planted_crop["dates"]["transplanted_date"])


def reminder_due_date_nominal(planted_crop: dict[str, Any], reminder: dict[str, Any]) -> date | None:
    timing_key = next(key for key in REMINDER_TIMING_KEYS if key in reminder)
    base = schedule_base_date(planted_crop, timing_key)
    if base is None:
        return None
    return base + timedelta(weeks=reminder[timing_key])


def schedule_event(
    event_id: str,
    event_type: str,
    nominal_date: date,
    *,
    anchor_event: str = "",
    source: str = "derived",
    reminder_id_value: str = "",
    reminder_type: str = "",
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "anchor_event": anchor_event,
        "nominal_date": nominal_date,
        "source": source,
        "reminder_id": reminder_id_value,
        "reminder_type": reminder_type,
    }


def crop_timeline_events(planted_crop: dict[str, Any], plant: dict[str, Any]) -> list[dict[str, Any]]:
    if planted_crop["planting_method"] == "perennial":
        return []
    events: list[dict[str, Any]] = []
    method = planted_crop["planting_method"]
    for reminder in plant["agent_reminders"][method]:
        due = reminder_due_date_nominal(planted_crop, reminder)
        if due is None:
            continue
        rid = reminder_id(reminder)
        events.append(
            schedule_event(
                f"reminder:{rid}",
                reminder["type"],
                due,
                anchor_event=REMINDER_ANCHOR_EVENTS.get(reminder["type"], ""),
                source="reminder",
                reminder_id_value=rid,
                reminder_type=reminder["type"],
            )
        )

    sown = parse_date_or_none(planted_crop["dates"]["sown_date"])
    if method == "indoor" and sown is not None and "transplanting" in plant:
        transplanting = plant["transplanting"]
        events.append(
            schedule_event(
                "derived:transplanted_outdoors",
                "transplanted_outdoors",
                sown + timedelta(weeks=transplanting["seedling_age_weeks_min"]),
                anchor_event="transplanted_outdoors",
            )
        )
        events.append(
            schedule_event(
                "derived:transplant_window_end",
                "transplant_window_end",
                sown + timedelta(weeks=transplanting["seedling_age_weeks_max"]),
            )
        )

    harvest_start, harvest_end, harvest_uses_actual_transplant = (None, None, False)
    if "timing" in plant:
        harvest_start, harvest_end, harvest_uses_actual_transplant = nominal_harvest_dates(planted_crop, plant)
    if harvest_start is not None:
        events.append(
            schedule_event(
                "derived:harvest_window_start",
                "harvest_window_start",
                harvest_start,
                anchor_event="harvest_window_start",
            )
        )
        events.append(
            schedule_event(
                "derived:harvest_started",
                "harvest_started",
                harvest_start,
                anchor_event="harvest_started",
            )
        )
    if harvest_end is not None:
        events.append(
            schedule_event(
                "derived:harvest_window_end",
                "harvest_window_end",
                harvest_end,
            )
        )

    for event in events:
        event["harvest_uses_actual_transplant"] = harvest_uses_actual_transplant and event["event_id"].startswith("derived:harvest_")
    return sorted(events, key=lambda item: (item["nominal_date"], item["event_id"]))


def adjustment_applies_to_event(adjustment: dict[str, Any], event: dict[str, Any], skip_anchor_events: set[str] | None = None) -> bool:
    if skip_anchor_events and adjustment["anchor_event"] in skip_anchor_events:
        return False
    if event.get("harvest_uses_actual_transplant") and adjustment["anchor_event"] == "transplanted_outdoors":
        return False
    anchor_date = date.fromisoformat(adjustment["nominal_anchor_date"])
    return event["nominal_date"] >= anchor_date


def adjusted_event_date(
    planted_crop: dict[str, Any],
    event: dict[str, Any],
    adjustments: list[dict[str, Any]] | None = None,
    skip_anchor_events: set[str] | None = None,
) -> date:
    if adjustments is None:
        adjustments = crop_schedule_adjustments(planted_crop)
    offset_days = sum(
        adjustment["offset_days"]
        for adjustment in adjustments
        if adjustment_applies_to_event(adjustment, event, skip_anchor_events)
    )
    return event["nominal_date"] + timedelta(days=offset_days)


def adjusted_reminder_due_date(planted_crop: dict[str, Any], plant: dict[str, Any], reminder: dict[str, Any]) -> date | None:
    rid = reminder_id(reminder)
    for event in crop_timeline_events(planted_crop, plant):
        if event["reminder_id"] == rid:
            return adjusted_event_date(planted_crop, event)
    return None


def available_schedule_anchor_events(planted_crop: dict[str, Any], plant: dict[str, Any]) -> list[dict[str, Any]]:
    anchors = []
    for event in crop_timeline_events(planted_crop, plant):
        if event["anchor_event"]:
            anchors.append(
                {
                    "anchor_event": event["anchor_event"],
                    "event_id": event["event_id"],
                    "event_type": event["event_type"],
                    "nominal_date": event["nominal_date"].isoformat(),
                    "adjusted_date": adjusted_event_date(planted_crop, event).isoformat(),
                    "reminder_id": event["reminder_id"],
                    "source": event["source"],
                }
            )
    return anchors


def resolve_schedule_anchor(
    planted_crop: dict[str, Any],
    plant: dict[str, Any],
    anchor_event: str = "",
    anchor_reminder_id: str = "",
) -> dict[str, Any]:
    events = crop_timeline_events(planted_crop, plant)
    if anchor_reminder_id:
        matches = [event for event in events if event["reminder_id"] == anchor_reminder_id]
        if not matches:
            fail(f"Unknown anchor reminder id: {anchor_reminder_id}")
        event = matches[0]
        if not event["anchor_event"]:
            fail(f"{anchor_reminder_id} is not a lifecycle anchor event")
        return event

    if anchor_event not in LIFECYCLE_ANCHOR_EVENTS:
        fail(f"Unknown lifecycle anchor event: {anchor_event}")
    if anchor_event in {"harvest_window_start", "harvest_started", "transplanted_outdoors"}:
        preferred = [event for event in events if event["event_id"] == f"derived:{anchor_event}"]
        if preferred:
            return preferred[0]
    matches = [event for event in events if event["anchor_event"] == anchor_event]
    if not matches:
        fail(f"{anchor_event} is not available for this crop")
    if len(matches) > 1:
        reminder_ids = ", ".join(event["reminder_id"] or event["event_id"] for event in matches)
        fail(f"{anchor_event} is ambiguous for this crop; use --anchor-reminder-id with one of: {reminder_ids}")
    return matches[0]


def schedule_adjustment_record(
    crop: dict[str, Any],
    anchor: dict[str, Any],
    actual_date: date,
    offset_days: int,
    reason: str,
    existing_adjustments: list[dict[str, Any]],
) -> dict[str, Any]:
    adjusted_before = adjusted_event_date(crop, anchor, existing_adjustments)
    record = {
        "adjustment_id": next_schedule_adjustment_id(crop),
        "anchor_event": anchor["anchor_event"],
        "nominal_anchor_date": anchor["nominal_date"].isoformat(),
        "adjusted_anchor_date_before_change": adjusted_before.isoformat(),
        "actual_anchor_date": actual_date.isoformat(),
        "offset_days": offset_days,
        "reason": reason.strip(),
        "created_date": date.today().isoformat(),
    }
    if anchor["reminder_id"]:
        record["anchor_reminder_id"] = anchor["reminder_id"]
    return record


def add_schedule_adjustment(
    crop: dict[str, Any],
    plant: dict[str, Any],
    *,
    anchor_event: str = "",
    anchor_reminder_id: str = "",
    actual_date_value: str = "",
    offset_days_value: int | None = None,
    reason: str,
) -> dict[str, Any]:
    if bool(anchor_event) == bool(anchor_reminder_id):
        fail("Specify exactly one of --anchor-event or --anchor-reminder-id")
    if bool(actual_date_value) == (offset_days_value is not None):
        fail("Specify exactly one of --actual-date or --offset-days")
    if not reason.strip():
        fail("--reason is required")
    anchor = resolve_schedule_anchor(crop, plant, anchor_event=anchor_event, anchor_reminder_id=anchor_reminder_id)
    existing = list(crop_schedule_adjustments(crop))
    adjusted_before = adjusted_event_date(crop, anchor, existing)
    if actual_date_value:
        validate_date_string(actual_date_value, "--actual-date", allow_empty=False)
        actual = date.fromisoformat(actual_date_value)
        offset_days = (actual - adjusted_before).days
    else:
        offset_days = int(offset_days_value or 0)
        actual = adjusted_before + timedelta(days=offset_days)
    if offset_days == 0 and not (anchor["anchor_event"] == "harvest_started" and not crop["status"]["harvest_started"]):
        fail("Schedule adjustment is a no-op")
    record = schedule_adjustment_record(crop, anchor, actual, offset_days, reason, existing)
    crop["agent_state"].setdefault("schedule_adjustments", []).append(record)
    crop["tracking"]["last_agent_review_date"] = date.today().isoformat()
    if anchor["anchor_event"] == "harvest_started":
        crop["status"]["harvest_started"] = True
        crop["dates"]["harvest_started_date"] = actual.isoformat()
        crop["status"]["currently_active"] = True
    return record


def reminder_due_date(planted_crop: dict[str, Any], reminder: dict[str, Any]) -> date | None:
    kb = load_crop_knowledge_base()
    plant = crop_index(kb)[planted_crop["plant_id"]]
    return adjusted_reminder_due_date(planted_crop, plant, reminder)


def month_matches_filter(value: str, months: list[int]) -> bool:
    parsed = parse_date_or_none(value)
    return parsed is not None and parsed.month in months


def reminder_is_seasonally_valid(planted_crop: dict[str, Any], reminder: dict[str, Any], due_date: date) -> bool:
    if "valid_sown_months" in reminder and not month_matches_filter(
        planted_crop["dates"]["sown_date"], reminder["valid_sown_months"]
    ):
        return False
    if "valid_transplanted_months" in reminder and not month_matches_filter(
        planted_crop["dates"]["transplanted_date"], reminder["valid_transplanted_months"]
    ):
        return False
    if "valid_due_months" in reminder and due_date.month not in reminder["valid_due_months"]:
        return False
    return True


def get_due_perennial_reminders(planted_crop: dict[str, Any], plant: dict[str, Any], today: date) -> list[dict[str, Any]]:
    state = planted_crop["agent_state"]
    excluded = set(state["completed_reminder_ids"]) | set(state["suppressed_reminder_ids"])
    due = []
    for year in (today.year - 1, today.year):
        for reminder in plant["agent_reminders"]["perennial"]:
            month = reminder["month_trigger"]
            rid = f"{reminder['type']}:month_trigger:{month}:{year}"
            if rid in excluded or reminder["type"] in excluded:
                continue
            due_date = date(year, month, 1)
            kind = reminder_kind(reminder["type"])
            if kind == "informational":
                # Fire once near the trigger month start, not for the whole active span.
                if not ((today - timedelta(days=NOTICE_WINDOW_DAYS)) <= due_date <= today):
                    continue
            else:
                if year == today.year and today.month not in reminder["active_months"]:
                    continue
                if due_date > today:
                    continue
            due.append({
                "crop_id": planted_crop["id"],
                "crop_name": planted_crop.get("display_name", planted_crop["plant_id"]),
                "plant_id": planted_crop["plant_id"],
                "reminder_id": rid,
                "type": reminder["type"],
                "kind": kind,
                "anchor_event": REMINDER_ANCHOR_EVENTS.get(reminder["type"], ""),
                "due_date": due_date.isoformat(),
                "days_overdue": (today - due_date).days,
                "text": reminder["text"],
            })
    return due


def get_due_reminders(planted_crop: dict[str, Any], plant: dict[str, Any], today: date) -> list[dict[str, Any]]:
    if planted_crop["planting_method"] == "perennial":
        return get_due_perennial_reminders(planted_crop, plant, today)
    method = planted_crop["planting_method"]
    reminders = plant["agent_reminders"][method]
    state = planted_crop["agent_state"]
    excluded = set(state["completed_reminder_ids"]) | set(state["suppressed_reminder_ids"])
    due = []
    for reminder in reminders:
        rid = reminder_id(reminder)
        if rid in excluded or reminder["type"] in excluded:
            continue
        due_date = adjusted_reminder_due_date(planted_crop, plant, reminder)
        if due_date is None:
            continue
        if not reminder_is_seasonally_valid(planted_crop, reminder, due_date):
            continue
        kind = reminder_kind(reminder["type"])
        # Tasks stay due until completed; informational notices fire once within a short window.
        if kind == "informational":
            is_due = (today - timedelta(days=NOTICE_WINDOW_DAYS)) <= due_date <= today
        else:
            is_due = due_date <= today
        if is_due:
            due.append(
                {
                    "crop_id": planted_crop["id"],
                    "crop_name": planted_crop.get("display_name", planted_crop["plant_id"]),
                    "plant_id": planted_crop["plant_id"],
                    "reminder_id": rid,
                    "type": reminder["type"],
                    "kind": kind,
                    "anchor_event": REMINDER_ANCHOR_EVENTS.get(reminder["type"], ""),
                    "due_date": due_date.isoformat(),
                    "days_overdue": (today - due_date).days,
                    "text": reminder["text"],
                }
            )
    return due


def suppress_old_retroactive_reminders(crop: dict[str, Any], plant: dict[str, Any], today: date) -> int:
    if crop["planting_method"] == "perennial":
        return 0
    cutoff = today - timedelta(days=7)
    suppressed = crop["agent_state"]["suppressed_reminder_ids"]
    count = 0
    for reminder in plant["agent_reminders"][crop["planting_method"]]:
        due_date = adjusted_reminder_due_date(crop, plant, reminder)
        if due_date is not None and reminder_is_seasonally_valid(crop, reminder, due_date) and due_date < cutoff:
            rid = reminder_id(reminder)
            if rid not in suppressed:
                suppressed.append(rid)
                count += 1
    return count


def list_due_reminders(today: date) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    planted = load_planted_crops()
    plants = crop_index(kb)
    by_crop: dict[str, dict[str, Any]] = {}
    notices: list[dict[str, Any]] = []
    for crop in planted["planted_crops"]:
        if not crop["status"]["currently_active"]:
            continue
        for r in get_due_reminders(crop, plants[crop["plant_id"]], today):
            if r["kind"] == "informational":
                notices.append({
                    "crop_name": crop["display_name"],
                    "due_date": r["due_date"],
                    "text": r["text"],
                })
                continue
            entry = {
                "reminder_id": r["reminder_id"],
                "due_date": r["due_date"],
                "days_overdue": r["days_overdue"],
                "text": r["text"],
            }
            if r["anchor_event"]:
                # Completing this re-times downstream reminders automatically.
                entry["anchor_event"] = r["anchor_event"]
            by_crop.setdefault(crop["id"], {"crop_name": crop["display_name"], "reminders": []})
            by_crop[crop["id"]]["reminders"].append(entry)
    crops_out = sorted(by_crop.values(), key=lambda c: c["crop_name"])
    notices.sort(key=lambda n: (n["crop_name"], n["due_date"]))
    task_total = sum(len(c["reminders"]) for c in crops_out)
    summary = f"{task_total} task(s) due across {len(crops_out)} crop(s)."
    if notices:
        summary += f" {len(notices)} informational notice(s)."
    return {
        "summary": summary,
        "reminder_count": task_total,
        "crops": crops_out,
        "notice_count": len(notices),
        "notices": notices,
    }


def normalize_alias(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return re.sub(r"\s+", " ", normalized)


def singularize_alias(alias: str) -> str:
    if alias.endswith("ies"):
        return f"{alias[:-3]}y"
    if alias.endswith("oes"):
        return alias[:-2]
    if alias.endswith("s") and not alias.endswith("ss"):
        return alias[:-1]
    return alias


def add_alias(aliases: list[str], value: str) -> None:
    alias = normalize_alias(value)
    if alias and alias not in aliases:
        aliases.append(alias)
    singular = singularize_alias(alias)
    if singular and singular not in aliases:
        aliases.append(singular)


def plant_aliases(plant: dict[str, Any]) -> list[str]:
    aliases: list[str] = []
    for value in [plant["id"], plant["id"].replace("_", " "), plant["name"]]:
        add_alias(aliases, value)
    return aliases


def resolve_plant_id(requested: str, plants: dict[str, dict[str, Any]]) -> str:
    query = normalize_alias(requested)
    query_singular = singularize_alias(query)
    for plant_id, plant in plants.items():
        if query in plant_aliases(plant) or query_singular in plant_aliases(plant):
            return plant_id

    matches = []
    for plant_id, plant in plants.items():
        aliases = plant_aliases(plant)
        if any(query in alias or alias in query for alias in aliases):
            matches.append(plant_id)
    if len(matches) == 1:
        return matches[0]
    if matches:
        names = ", ".join(plants[plant_id]["name"] for plant_id in matches)
        fail(f"Plant name '{requested}' is ambiguous: {names}")
    raise UnknownPlantError(requested)


def default_crop_label(plant: dict[str, Any]) -> str:
    label = re.sub(r"\s*\([^)]*\)\s*$", "", plant["name"]).strip()
    if label:
        return label
    return plant["id"].replace("_", " ").title()


def crop_phase(crop: dict[str, Any]) -> str:
    status = crop["status"]
    if not status["currently_active"]:
        return "inactive"
    if status["harvest_finished"] or status["harvest_completed"]:
        return "harvest_finished"
    if status["harvest_started"]:
        return "harvesting"
    if crop["planting_method"] == "indoor" and not status["transplanted_outdoors"]:
        return "indoor"
    if crop["planting_method"] == "indoor" and status["transplanted_outdoors"]:
        return "transplanted_outdoors"
    return "outdoor_direct"


def crop_aliases(crop: dict[str, Any], plant: dict[str, Any]) -> list[str]:
    values = [
        crop["id"],
        crop["display_name"],
        crop["plant_id"],
        crop["plant_id"].replace("_", " "),
        plant["name"],
    ]
    aliases = []
    for value in values:
        add_alias(aliases, value)
    return aliases


def list_planted_crops(active_only: bool = False) -> list[dict[str, Any]]:
    kb = load_crop_knowledge_base()
    planted = load_planted_crops()
    plants = crop_index(kb)
    crops = []
    for crop in planted["planted_crops"]:
        if active_only and not crop["status"]["currently_active"]:
            continue
        plant = plants[crop["plant_id"]]
        non_empty_dates = {k: v for k, v in crop["dates"].items() if v}
        crops.append(
            {
                "crop_id": crop["id"],
                "display_name": crop["display_name"],
                "aliases": crop_aliases(crop, plant),
                "planting_method": crop["planting_method"],
                "phase": crop_phase(crop),
                "currently_active": crop["status"]["currently_active"],
                "dates": non_empty_dates,
            }
        )
    return crops


def crop_info(plant_id_query: str) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    plant_id = resolve_plant_id(plant_id_query, plants)
    plant = plants[plant_id]
    is_perennial = plant.get("lifecycle") == "perennial"

    timing = plant.get("timing", {})
    care = plant.get("care", {})
    moisture = plant["soil_moisture"]

    harvest: dict[str, Any] = {
        "pattern": plant["harvest_pattern"],
        "market_price_dkk_per_kg": plant["market_price_dkk_per_kg"],
    }
    if is_perennial:
        harvest["season_start_month"] = timing["harvest_month_min"]
        harvest["season_end_month"] = timing["harvest_month_max"]
    else:
        harvest["from_direct_sow_weeks_min"] = timing.get("harvest_from_direct_sow_weeks_min")
        harvest["from_direct_sow_weeks_max"] = timing.get("harvest_from_direct_sow_weeks_max")
        harvest["from_transplant_weeks_min"] = timing.get("harvest_from_transplant_weeks_min")
        harvest["from_transplant_weeks_max"] = timing.get("harvest_from_transplant_weeks_max")
        harvest["duration_weeks"] = timing.get("harvest_duration_weeks")

    result: dict[str, Any] = {
        "plant_id": plant_id,
        "name": plant["name"],
        "lifecycle": "perennial" if is_perennial else "annual",
        "harvest": harvest,
        "water": {
            "need": care.get("water_need"),
            "drought_sensitivity": care.get("drought_sensitivity"),
            "soil_moisture_optimal_min_m3_m3": moisture["optimal_min_m3_m3"],
            "soil_moisture_optimal_max_m3_m3": moisture["optimal_max_m3_m3"],
            "soil_moisture_too_wet_m3_m3": moisture["too_wet_m3_m3"],
            "light_watering_after_weeks": plant.get("light_watering_after_weeks"),
            "deep_watering_after_weeks": plant.get("deep_watering_after_weeks"),
            "watering_regime": describe_watering_regime(
                plant.get("light_watering_after_weeks"),
                plant.get("deep_watering_after_weeks"),
                is_perennial,
            ),
        },
        "care": {
            "heat_sensitive": care.get("heat_sensitive"),
            "bolting_risk": care.get("bolting_risk"),
            "notes": care.get("notes", ""),
        },
    }

    if not is_perennial:
        sowing = plant["sowing"]
        outdoor = sowing["outdoor_direct"]
        indoor = sowing["indoor"]
        result["sowing"] = {
            "depth_cm": sowing.get("depth_cm"),
            "spacing_cm": plant.get("spacing"),
            "outdoor_direct": {
                "recommended": outdoor["recommended"],
                "germination_weeks": outdoor["germination_weeks"],
                "soil_temp_min_c": outdoor["soil_temp_min_c"],
                "soil_temp_optimal_min_c": outdoor["soil_temp_optimal_min_c"],
                "soil_temp_optimal_max_c": outdoor["soil_temp_optimal_max_c"],
            },
            "indoor": {
                "recommended": indoor["recommended"],
                "germination_weeks": indoor["germination_weeks"],
                "germination_temp_min_c": indoor["germination_temp_min_c"],
                "germination_temp_optimal_min_c": indoor["germination_temp_optimal_min_c"],
                "germination_temp_optimal_max_c": indoor["germination_temp_optimal_max_c"],
            },
        }
        transplanting = plant["transplanting"]
        result["transplanting"] = {
            "seedling_age_weeks_min": transplanting["seedling_age_weeks_min"],
            "seedling_age_weeks_max": transplanting["seedling_age_weeks_max"],
            "hardening_off_weeks": transplanting["hardening_off_weeks"],
            "outdoor_soil_temp_min_c": transplanting["outdoor_soil_temp_min_c"],
            "outdoor_soil_temp_optimal_min_c": transplanting["outdoor_soil_temp_optimal_min_c"],
            "outdoor_soil_temp_optimal_max_c": transplanting["outdoor_soil_temp_optimal_max_c"],
        }
        profile = load_garden_profile()
        local_season = get_local_seasonality(plant, profile)
        result["seasonality"] = {
            "indoor_sow_months": local_season["indoor_sow_months"],
            "outdoor_direct_sow_months": local_season["outdoor_direct_sow_months"],
            "transplant_outdoor_months": local_season["transplant_outdoor_months"],
        }

    return result


def next_crop_id(planted: dict[str, Any], plant_id: str) -> str:
    """Return the next crop ID for a given plant_id, e.g. 'carrot_1', 'carrot_2'."""
    max_num = 0
    prefix = f"{plant_id}_"
    for crop in planted["planted_crops"]:
        if crop["id"].startswith(prefix):
            suffix = crop["id"][len(prefix):]
            if suffix.isdigit():
                max_num = max(max_num, int(suffix))
    return f"{plant_id}_{max_num + 1}"


def add_planted_crop(args: argparse.Namespace) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    plant_id = resolve_plant_id(args.plant_id, plants)
    is_perennial = args.method == "perennial"
    if is_perennial:
        sown_date = ""
        transplanted = ""
    else:
        validate_date_string(args.sown_date, "--sown-date", allow_empty=False)
        sown_date = args.sown_date
        transplanted = args.transplanted_date or ""
        validate_date_string(transplanted, "--transplanted-date", allow_empty=True)
    planted = load_planted_crops()
    display_name = (args.display_name or "").strip() or default_crop_label(plants[plant_id])
    crop = {
        "id": args.crop_id or next_crop_id(planted, plant_id),
        "plant_id": plant_id,
        "display_name": display_name,
        "planting_method": args.method,
        "dates": {
            "sown_date": sown_date,
            "transplanted_date": transplanted,
            "harvest_started_date": "",
            "harvest_finished_date": "",
        },
        "status": {
            "currently_active": True,
            "started_indoors": False if is_perennial else args.method == "indoor",
            "transplanted_outdoors": True if is_perennial else bool(transplanted),
            "harvest_started": False,
            "harvest_finished": False,
            "harvest_completed": False,
        },
        "tracking": {
            "last_watered_date": "",
            "last_fertilized_date": "",
            "last_agent_review_date": date.today().isoformat(),
        },
        "agent_state": {
            "active_reminder_ids": [],
            "completed_reminder_ids": [],
            "suppressed_reminder_ids": [],
            "schedule_adjustments": [],
        },
        "harvest_log": [],
        "notes": args.notes or "",
    }
    if not is_perennial:
        suppressed_count = suppress_old_retroactive_reminders(crop, plants[plant_id], date.today())
        if suppressed_count:
            note = (
                f"[{date.today().isoformat()}] Retroactive entry: suppressed {suppressed_count} reminder(s) "
                "older than one week."
            )
            crop["notes"] = f"{crop['notes']}\n{note}".strip() if crop["notes"] else note
    planted["planted_crops"].append(crop)
    save_planted_crops(planted)
    return crop


def delete_planted_crop(crop_id: str) -> dict[str, Any]:
    planted = load_planted_crops()
    original_len = len(planted["planted_crops"])
    planted["planted_crops"] = [c for c in planted["planted_crops"] if c["id"] != crop_id]
    if len(planted["planted_crops"]) == original_len:
        fail(f"Crop id '{crop_id}' not found.")
    save_planted_crops(planted)
    return {
        "summary": f"Deleted planted crop '{crop_id}'.",
        "crop_id": crop_id,
    }


def edit_planted_crop(args: argparse.Namespace) -> dict[str, Any]:
    planted = load_planted_crops()
    crop = find_crop(planted, args.crop_id)
    
    if args.display_name:
        crop["display_name"] = args.display_name.strip()
    
    if args.sown_date:
        validate_date_string(args.sown_date, "--sown-date", allow_empty=False)
        crop["dates"]["sown_date"] = args.sown_date
        
    if args.transplanted_date:
        validate_date_string(args.transplanted_date, "--transplanted-date", allow_empty=False)
        sown = parse_date_or_none(crop["dates"]["sown_date"])
        transplanted = date.fromisoformat(args.transplanted_date)
        if sown is not None and transplanted < sown:
            fail("--transplanted-date must not be before the crop's sown_date")
        crop["dates"]["transplanted_date"] = args.transplanted_date
        crop["status"]["transplanted_outdoors"] = True
        
    if args.notes:
        crop["notes"] = args.notes.strip()
        
    crop["tracking"]["last_agent_review_date"] = date.today().isoformat()
    save_planted_crops(planted)
    return crop


def update_transplanted(crop_id: str, transplanted_date: str) -> dict[str, Any]:
    validate_date_string(transplanted_date, "--transplanted-date", allow_empty=False)
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    if crop["planting_method"] != "indoor":
        fail(f"{crop_id} is not an indoor-started crop")
    sown = parse_date_or_none(crop["dates"]["sown_date"])
    transplanted = date.fromisoformat(transplanted_date)
    if sown is not None and transplanted < sown:
        fail("--transplanted-date must not be before the crop's sown_date")
    existing_date = crop["dates"]["transplanted_date"]
    crop["dates"]["transplanted_date"] = transplanted_date
    crop["status"]["transplanted_outdoors"] = True
    crop["tracking"]["last_agent_review_date"] = date.today().isoformat()
    if existing_date != transplanted_date:
        try:
            add_schedule_adjustment(
                crop,
                plants[crop["plant_id"]],
                anchor_event="transplanted_outdoors",
                actual_date_value=transplanted_date,
                reason="Actual outdoor transplant date recorded.",
            )
        except ValidationError as exc:
            if "no-op" not in str(exc):
                raise
    save_planted_crops(planted)
    return crop


def find_crop(planted: dict[str, Any], crop_id: str) -> dict[str, Any]:
    for crop in planted["planted_crops"]:
        if crop["id"] == crop_id:
            return crop
    fail(f"Unknown crop id: {crop_id}")


def mark_reminder(crop_id: str, rid: str, target: str) -> dict[str, Any]:
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    state = crop["agent_state"]
    if rid not in state[target]:
        state[target].append(rid)
    if rid in state["active_reminder_ids"]:
        state["active_reminder_ids"].remove(rid)
    save_planted_crops(planted)
    return crop


def complete_reminder(crop_id: str, rid: str, actual_date_value: str, today: date) -> dict[str, Any]:
    """Mark a reminder completed. If it is a lifecycle anchor (germination/flowering/
    fruiting), record the observed date and re-time downstream reminders automatically.
    """
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    state = crop["agent_state"]
    if rid not in state["completed_reminder_ids"]:
        state["completed_reminder_ids"].append(rid)
    if rid in state["active_reminder_ids"]:
        state["active_reminder_ids"].remove(rid)

    anchor_type = rid.split(":", 1)[0]
    anchor_event = REMINDER_ANCHOR_EVENTS.get(anchor_type, "")
    adjustment = None
    if anchor_event and crop["planting_method"] != "perennial":
        if actual_date_value:
            validate_date_string(actual_date_value, "--actual-date", allow_empty=False)
            actual = date.fromisoformat(actual_date_value)
        else:
            actual = today
        plant = plants[crop["plant_id"]]
        anchor = resolve_schedule_anchor(crop, plant, anchor_event=anchor_event)
        current = adjusted_event_date(crop, anchor)
        if actual != current:  # skip no-ops (observed on the expected date)
            adjustment = add_schedule_adjustment(
                crop,
                plant,
                anchor_event=anchor_event,
                actual_date_value=actual.isoformat(),
                reason=f"Auto-adjust: {anchor_event} observed on {actual.isoformat()}",
            )

    save_planted_crops(planted)
    result: dict[str, Any] = {"crop_id": crop["id"], "reminder_id": rid, "completed": True}
    if adjustment is not None:
        result["summary"] = (
            f"Completed {anchor_event} check for {crop['display_name']} and shifted "
            f"later reminders by {adjustment['offset_days']} day(s)."
        )
        result["schedule_adjustment"] = adjustment
    else:
        result["summary"] = f"Marked reminder completed for {crop['display_name']}."
    return result


def mark_harvested(crop_id: str, today: date) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    plant = plants[crop["plant_id"]]
    if crop["planting_method"] != "perennial":
        try:
            add_schedule_adjustment(
                crop,
                plant,
                anchor_event="harvest_started",
                actual_date_value=today.isoformat(),
                reason="Actual harvest start date recorded.",
            )
        except ValidationError as exc:
            if "no-op" not in str(exc):
                raise
    crop["status"]["harvest_started"] = True
    crop["dates"]["harvest_started_date"] = crop["dates"]["harvest_started_date"] or today.isoformat()
    crop["status"]["currently_active"] = True
    save_planted_crops(planted)
    return crop


def finish_harvest(crop_id: str, today: date) -> dict[str, Any]:
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    if crop["planting_method"] == "perennial":
        fail(f"{crop_id} is a perennial crop — use log-harvest to record harvests. Perennial crops are never deactivated by finishing a harvest.")
    crop["status"]["harvest_finished"] = True
    crop["status"]["harvest_completed"] = True
    crop["status"]["currently_active"] = False
    crop["dates"]["harvest_finished_date"] = today.isoformat()
    save_planted_crops(planted)
    return crop


def next_harvest_id(crop: dict[str, Any]) -> str:
    max_num = 0
    for entry in crop.get("harvest_log", []):
        match = re.match(r"^harvest_(\d+)$", entry.get("harvest_id", ""))
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"harvest_{max_num + 1:03d}"


def harvest_log_entry(crop: dict[str, Any], harvest_date: str, weight_kg: float, notes: str = "") -> dict[str, Any]:
    validate_date_string(harvest_date, "--date", allow_empty=False)
    require_positive_number(weight_kg, "--weight-kg")
    if not isinstance(notes, str):
        fail("--notes must be a string")
    return {
        "harvest_id": next_harvest_id(crop),
        "date": harvest_date,
        "weight_kg": round(float(weight_kg), 3),
        "notes": notes,
        "created_date": date.today().isoformat(),
    }


def mark_harvest_started_from_log(crop: dict[str, Any], plant: dict[str, Any], harvest_date: str) -> None:
    if crop["status"]["harvest_started"]:
        return
    if plant["harvest_pattern"] == "continuous" and crop["planting_method"] != "perennial":
        try:
            add_schedule_adjustment(
                crop,
                plant,
                anchor_event="harvest_started",
                actual_date_value=harvest_date,
                reason="Actual harvest start date recorded from harvest log.",
            )
        except ValidationError as exc:
            if "no-op" not in str(exc):
                raise
    crop["status"]["harvest_started"] = True
    crop["dates"]["harvest_started_date"] = harvest_date
    crop["status"]["currently_active"] = True


def append_harvest_log_entry(crop: dict[str, Any], plant: dict[str, Any], entry: dict[str, Any]) -> None:
    crop.setdefault("harvest_log", []).append(entry)
    mark_harvest_started_from_log(crop, plant, entry["date"])
    crop["tracking"]["last_agent_review_date"] = date.today().isoformat()


def log_harvest(args: argparse.Namespace) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    crop = find_crop(planted, args.crop_id)
    entry = harvest_log_entry(crop, args.date, args.weight_kg, args.notes or "")
    append_harvest_log_entry(crop, plants[crop["plant_id"]], entry)
    save_planted_crops(planted)
    return {
        "summary": f"Logged {entry['weight_kg']:g} kg harvested from {crop['display_name']}.",
        "crop_id": crop["id"],
        "display_name": crop["display_name"],
        "harvest": entry,
    }


def validate_bulk_harvest_payload(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("harvests"), list):
        fail("Bulk harvest file must contain a harvests list")
    normalized = []
    for idx, item in enumerate(payload["harvests"]):
        path = f"harvests[{idx}]"
        if not isinstance(item, dict):
            fail(f"{path} must be an object")
        require_keys(item, ["crop_id", "date", "weight_kg"], path)
        if not isinstance(item["crop_id"], str) or not item["crop_id"].strip():
            fail(f"{path}.crop_id must be a non-empty string")
        validate_date_string(item["date"], f"{path}.date", allow_empty=False)
        require_positive_number(item["weight_kg"], f"{path}.weight_kg")
        notes = item.get("notes", "")
        if not isinstance(notes, str):
            fail(f"{path}.notes must be a string")
        normalized.append(
            {
                "crop_id": item["crop_id"],
                "date": item["date"],
                "weight_kg": float(item["weight_kg"]),
                "notes": notes,
            }
        )
    return normalized


def bulk_log_harvest(file_path: str) -> dict[str, Any]:
    try:
        payload = load_json(Path(file_path))
    except OSError as exc:
        fail(f"Could not read bulk harvest file: {exc}")
    entries = validate_bulk_harvest_payload(payload)
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    candidate = copy.deepcopy(planted)
    logged = []
    for item in entries:
        crop = find_crop(candidate, item["crop_id"])
        entry = harvest_log_entry(crop, item["date"], item["weight_kg"], item["notes"])
        append_harvest_log_entry(crop, plants[crop["plant_id"]], entry)
        logged.append(
            {
                "crop_id": crop["id"],
                "display_name": crop["display_name"],
                "harvest": entry,
            }
        )
    save_planted_crops(candidate)
    total_weight = round(sum(item["harvest"]["weight_kg"] for item in logged), 3)
    return {
        "summary": f"Logged {len(logged)} harvest(s), totaling {total_weight:g} kg.",
        "harvest_count": len(logged),
        "total_weight_kg": total_weight,
        "logged_harvests": logged,
    }


def list_harvests(crop_id: str = "") -> dict[str, Any]:
    planted = load_planted_crops()
    crops = [find_crop(planted, crop_id)] if crop_id else planted["planted_crops"]
    crops_out = []
    total_count = 0
    for crop in crops:
        log = crop.get("harvest_log", [])
        if not log:
            continue
        entries = sorted(
            [{"date": e["date"], "weight_kg": e["weight_kg"]} for e in log],
            key=lambda e: e["date"],
        )
        crop_total = round(sum(e["weight_kg"] for e in entries), 3)
        total_count += len(entries)
        crops_out.append(
            {
                "crop_id": crop["id"],
                "display_name": crop["display_name"],
                "total_weight_kg": crop_total,
                "harvests": entries,
            }
        )
    crops_out.sort(key=lambda c: c["display_name"])
    total_weight = round(sum(c["total_weight_kg"] for c in crops_out), 3)
    return {
        "summary": f"Found {total_count} harvest(s) across {len(crops_out)} crop(s), totaling {total_weight:g} kg.",
        "harvest_count": total_count,
        "total_weight_kg": total_weight,
        "crops": crops_out,
    }


def harvest_savings(year: int) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    details_by_crop: dict[str, dict[str, Any]] = {}
    for crop in planted["planted_crops"]:
        plant = plants[crop["plant_id"]]
        price = float(plant["market_price_dkk_per_kg"])
        for entry in crop.get("harvest_log", []):
            if date.fromisoformat(entry["date"]).year != year:
                continue
            detail = details_by_crop.setdefault(
                crop["id"],
                {
                    "display_name": crop["display_name"],
                    "harvest_count": 0,
                    "weight_kg": 0.0,
                    "market_price_dkk_per_kg": round(price, 2),
                    "value_dkk": 0.0,
                },
            )
            detail["harvest_count"] += 1
            detail["weight_kg"] += float(entry["weight_kg"])
    for detail in details_by_crop.values():
        detail["weight_kg"] = round(detail["weight_kg"], 3)
        detail["value_dkk"] = round(detail["weight_kg"] * detail["market_price_dkk_per_kg"], 2)
    crop_details = sorted(details_by_crop.values(), key=lambda item: item["display_name"])
    total_weight = round(sum(item["weight_kg"] for item in crop_details), 3)
    total_value = round(sum(item["value_dkk"] for item in crop_details), 2)
    return {
        "summary": f"Harvest savings for {year}: {total_value:g} DKK from {total_weight:g} kg harvested.",
        "year": year,
        "currency": "DKK",
        "total_weight_kg": total_weight,
        "total_value_dkk": total_value,
        "crop_count": len(crop_details),
        "crops": crop_details,
    }


def deactivate_crop(crop_id: str, reason: str, deactivated_date: str) -> dict[str, Any]:
    validate_date_string(deactivated_date, "--date", allow_empty=False)
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    crop["status"]["currently_active"] = False
    crop["tracking"]["last_agent_review_date"] = date.today().isoformat()
    note = f"[{deactivated_date}] Deactivated"
    if reason:
        note = f"{note}: {reason}"
    crop["notes"] = f"{crop['notes']}\n{note}".strip() if crop["notes"] else note
    save_planted_crops(planted)
    return crop


def list_schedule_adjustments(crop_id: str) -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    plants = crop_index(kb)
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    return {
        "crop_id": crop["id"],
        "display_name": crop["display_name"],
        "schedule_adjustments": crop_schedule_adjustments(crop),
        "available_anchors": available_schedule_anchor_events(crop, plants[crop["plant_id"]]),
    }


def clear_schedule_adjustment(crop_id: str, adjustment_id: str) -> dict[str, Any]:
    planted = load_planted_crops()
    crop = find_crop(planted, crop_id)
    adjustments = crop["agent_state"].setdefault("schedule_adjustments", [])
    kept = [item for item in adjustments if item["adjustment_id"] != adjustment_id]
    if len(kept) == len(adjustments):
        fail(f"Unknown schedule adjustment id: {adjustment_id}")
    crop["agent_state"]["schedule_adjustments"] = kept
    crop["tracking"]["last_agent_review_date"] = date.today().isoformat()
    save_planted_crops(planted)
    return {
        "summary": f"Cleared schedule adjustment {adjustment_id} for {crop['display_name']}.",
        "crop_id": crop["id"],
        "cleared_adjustment_id": adjustment_id,
        "schedule_adjustments": kept,
    }


def nominal_harvest_dates(planted_crop: dict[str, Any], plant: dict[str, Any]) -> tuple[date | None, date | None, bool]:
    dates = planted_crop["dates"]
    timing = plant["timing"]
    uses_actual_transplant = False
    if planted_crop["planting_method"] == "outdoor_direct":
        base = parse_date_or_none(dates["sown_date"])
        min_weeks = timing["harvest_from_direct_sow_weeks_min"]
        max_weeks = timing["harvest_from_direct_sow_weeks_max"]
    else:
        base = parse_date_or_none(dates["transplanted_date"])
        if base is None:
            return None, None, False
        uses_actual_transplant = True
        min_weeks = timing["harvest_from_transplant_weeks_min"]
        max_weeks = timing["harvest_from_transplant_weeks_max"]
    if base is None:
        return None, None, uses_actual_transplant
    start = base + timedelta(weeks=min_weeks)
    end = base + timedelta(weeks=max_weeks)
    if plant["harvest_pattern"] == "continuous":
        end = end + timedelta(weeks=timing.get("harvest_duration_weeks", 0))
    return start, end, uses_actual_transplant


def estimate_harvest_window(planted_crop: dict[str, Any], plant: dict[str, Any]) -> dict[str, Any]:
    status = planted_crop["status"]
    dates = planted_crop["dates"]
    result = {"crop_name": planted_crop["display_name"], "status": "unknown"}
    if planted_crop["planting_method"] == "perennial":
        today = date.today()
        timing = plant["timing"]
        m_min, m_max = timing["harvest_month_min"], timing["harvest_month_max"]
        start = date(today.year, m_min, 1)
        end = date(today.year, m_max, calendar.monthrange(today.year, m_max)[1])
        if status["harvest_completed"]:
            result.update({"status": "complete", "harvest_finished_date": dates["harvest_finished_date"]})
        else:
            result.update({"status": "estimated", "harvest_window": {"start": start.isoformat(), "end": end.isoformat()}})
        return result
    if plant["harvest_pattern"] == "single" and status["harvest_completed"]:
        result.update({"status": "complete", "harvest_finished_date": dates["harvest_finished_date"]})
        return result
    if planted_crop["planting_method"] == "indoor" and not dates["transplanted_date"]:
        sown = parse_date_or_none(dates["sown_date"])
        if sown is None:
            result.update({"status": "waiting_for_sown_date"})
            return result
        start_event = schedule_event(
            "derived:transplanted_outdoors",
            "transplanted_outdoors",
            sown + timedelta(weeks=plant["transplanting"]["seedling_age_weeks_min"]),
            anchor_event="transplanted_outdoors",
        )
        end_event = schedule_event(
            "derived:transplant_window_end",
            "transplant_window_end",
            sown + timedelta(weeks=plant["transplanting"]["seedling_age_weeks_max"]),
        )
        result.update(
            {
                "status": "waiting_for_transplant",
                "expected_transplant_window": {
                    "start": adjusted_event_date(planted_crop, start_event).isoformat(),
                    "end": adjusted_event_date(planted_crop, end_event).isoformat(),
                },
            }
        )
        return result

    start, end, uses_actual_transplant = nominal_harvest_dates(planted_crop, plant)
    if start is None or end is None:
        result.update({"status": "waiting_for_sown_date"})
        return result
    if plant["harvest_pattern"] == "continuous" and dates["harvest_started_date"]:
        actual_start = date.fromisoformat(dates["harvest_started_date"])
        duration = timedelta(weeks=plant["timing"].get("harvest_duration_weeks", 0))
        result.update(
            {
                "status": "estimated",
                "harvest_window": {
                    "start": actual_start.isoformat(),
                    "end": (actual_start + duration).isoformat(),
                },
            }
        )
        return result
    skip = {"transplanted_outdoors"} if uses_actual_transplant else set()
    start_event = schedule_event(
        "derived:harvest_window_start",
        "harvest_window_start",
        start,
        anchor_event="harvest_window_start",
    )
    end_event = schedule_event("derived:harvest_window_end", "harvest_window_end", end)
    result.update(
        {
            "status": "estimated",
            "harvest_window": {
                "start": adjusted_event_date(planted_crop, start_event, skip_anchor_events=skip).isoformat(),
                "end": adjusted_event_date(planted_crop, end_event, skip_anchor_events=skip).isoformat(),
            },
        }
    )
    return result


def harvest_windows() -> list[dict[str, Any]]:
    kb = load_crop_knowledge_base()
    planted = load_planted_crops()
    plants = crop_index(kb)
    return [estimate_harvest_window(crop, plants[crop["plant_id"]]) for crop in planted["planted_crops"]]


def describe_watering_regime(
    light_watering_after_weeks: int | None,
    deep_watering_after_weeks: int | None,
    is_perennial: bool,
) -> str:
    """Human-readable description of a crop's surface/light/deep watering regime."""
    lwa = light_watering_after_weeks
    dwa = deep_watering_after_weeks
    if dwa is not None and dwa <= 0:
        return "Deep waterings (established deep roots)."
    anchor = "sowing"
    stages = []
    if lwa:
        stages.append(f"surface waterings for the first {lwa} week(s) after {anchor} (germinating seedbed)")
        stages.append("light waterings once seedlings establish")
    else:
        stages.append("light waterings")
    if dwa is not None:
        stages.append(f"deep waterings from {dwa} weeks after {anchor} as roots reach deeper soil")
    text = ", then ".join(stages)
    return text[0].upper() + text[1:] + "."


def resolve_watering_mode(planted_crop: dict[str, Any], plant: dict[str, Any], today: date) -> str:
    """Return 'surface', 'light', or 'deep' for a crop's current root depth.

    light_watering_after_weeks: None/0 -> no surface stage; N -> surface for the
      first N weeks after sowing (direct-sown only), then light.
    deep_watering_after_weeks: None -> never deep; 0 -> always deep (perennials);
      N -> deep from N weeks after sowing (direct) or transplanting.
    """
    dwa = plant.get("deep_watering_after_weeks")
    if dwa is not None and dwa <= 0:
        return "deep"
    method = planted_crop["planting_method"]
    if method == "perennial":
        return "deep" if dwa is not None else "light"
    if method == "outdoor_direct":
        base = parse_date_or_none(planted_crop["dates"]["sown_date"])
        has_surface_stage = True
    else:  # indoor crop, only watered once transplanted outdoors (past the seedbed stage)
        base = parse_date_or_none(planted_crop["dates"]["transplanted_date"])
        has_surface_stage = False
    if base is None:
        return "light"  # not enough info yet; light watering is the gentler default
    weeks_since = (today - base).days / 7
    lwa = plant.get("light_watering_after_weeks")
    if has_surface_stage and lwa and weeks_since < lwa:
        return "surface"
    if dwa is not None and weeks_since >= dwa:
        return "deep"
    return "light"


def watering_week() -> dict[str, Any]:
    kb = load_crop_knowledge_base()
    planted = load_planted_crops()
    state = load_garden_state()
    profile = load_garden_profile()
    area_m2 = bed_area_m2(profile)
    today = date.today()
    plants = crop_index(kb)
    active = [crop for crop in planted["planted_crops"] if crop["status"]["currently_active"]]
    outdoor_soil_crops = [
        crop
        for crop in active
        if crop["planting_method"] in {"outdoor_direct", "perennial"} or crop["status"]["transplanted_outdoors"]
    ]
    skipped_indoor = [
        {"crop_name": crop["display_name"], "reason": "Indoor crop has not been transplanted outdoors."}
        for crop in active
        if crop["planting_method"] == "indoor" and not crop["status"]["transplanted_outdoors"]
    ]
    if not active:
        return {
            "status": "no_active_crops",
            "total_waterings": 0,
            "rainy_days": [],
            "per_crop": [],
            "skipped_crops": skipped_indoor,
            "summary": "No active planted crops are being tracked.",
        }
    if not outdoor_soil_crops:
        return {
            "status": "no_outdoor_soil_crops",
            "total_waterings": 0,
            "rainy_days": [],
            "per_crop": [],
            "skipped_crops": skipped_indoor,
            "summary": "No active crops are currently in the outdoor raised bed.",
        }
    if not state["daily"]:
        return {
            "status": "missing_forecast",
            "total_waterings": 0,
            "rainy_days": [],
            "per_crop": [],
            "skipped_crops": skipped_indoor,
            "summary": "No weekly forecast is available. Run update-weekly-forecast first.",
        }

    rainy_days = [d["date"] for d in state["daily"] if d["precipitation_mm"] >= RAIN_SKIP_THRESHOLD_L_PER_M2]

    # Each watering tier reads the soil-moisture layer matching its root depth.
    mode_params = {
        "surface": (SURFACE_WATERING_L_PER_M2, SURFACE_LAYER_THICKNESS_L_PER_M2, "soil_moisture_1_to_3cm_m3_m3"),
        "light": (LIGHT_WATERING_L_PER_M2, SHALLOW_LAYER_THICKNESS_L_PER_M2, "soil_moisture_3_to_9cm_m3_m3"),
        "deep": (DEEP_WATERING_L_PER_M2, DEEP_LAYER_THICKNESS_L_PER_M2, "soil_moisture_9_to_27cm_m3_m3"),
    }

    # For each outdoor crop, find the maximum number of standard doses needed on any dry day.
    per_crop = []
    assessments = []  # written to detail log only
    for crop in outdoor_soil_crops:
        plant = plants[crop["plant_id"]]
        moisture = plant["soil_moisture"]
        is_perennial = crop["planting_method"] == "perennial"
        mode = resolve_watering_mode(crop, plant, today)
        volume, thickness, layer_key = mode_params[mode]
        max_sessions = 0
        per_day = []
        for day in state["daily"]:
            blocked = day["precipitation_mm"] >= RAIN_SKIP_THRESHOLD_L_PER_M2
            sm_min = day[layer_key]["min"]
            sm_max = day[layer_key]["max"]
            missing = max(0.0, moisture["optimal_min_m3_m3"] - sm_min) * thickness
            if not blocked and missing > 0:
                needed = math.ceil(missing / volume)
                capacity = max(0.0, moisture["optimal_max_m3_m3"] - sm_max) * thickness
                max_safe = math.floor(capacity / volume)
                sessions = max(0, min(needed, max_safe))
                max_sessions = max(max_sessions, sessions)
            else:
                sessions = 0
            per_day.append({
                "date": day["date"],
                "blocked_by_rain": blocked,
                "forecast_min_m3_m3": round(sm_min, 3),
                "missing_l_per_m2": round(missing, 2),
                "sessions": sessions,
            })
        if max_sessions > 0:
            entry = {
                "crop_name": crop["display_name"],
                "watering_type": mode,
                "waterings": max_sessions,
            }
            if is_perennial:
                entry["l_per_m2"] = round(max_sessions * volume, 2)
            else:
                entry["l_per_bed"] = round(max_sessions * volume * area_m2, 2)
            per_crop.append(entry)
        assessments.append({"crop_id": crop["id"], "plant_id": plant["id"], "watering_mode": mode, "days": per_day})

    per_crop.sort(key=lambda c: (-c["waterings"], c["crop_name"]))
    total_waterings = per_crop[0]["waterings"] if per_crop else 0

    if total_waterings == 0:
        summary = "No watering is recommended this week."
    else:
        clauses = []
        # Bed crops (annuals): report per-watering dose in L/bed, split by tier.
        for mode in ("surface", "light", "deep"):
            n = max((c["waterings"] for c in per_crop if c["watering_type"] == mode and "l_per_bed" in c), default=0)
            if n > 0:
                dose = round(mode_params[mode][0] * area_m2, 2)
                clauses.append(f"Bed {mode}: up to {n} watering(s) of {dose:g} L/bed each")
        # Perennials (single bushes): report per-watering dose in L/m2.
        for mode in ("surface", "light", "deep"):
            n = max((c["waterings"] for c in per_crop if c["watering_type"] == mode and "l_per_m2" in c), default=0)
            if n > 0:
                dose = mode_params[mode][0]
                clauses.append(f"Perennials {mode}: up to {n} watering(s) of {dose:g} L/m² each")
        rain_note = (
            f" Skip watering on rainy days: {', '.join(rainy_days)}." if rainy_days else ""
        )
        summary = ". ".join(clauses) + "." + rain_note

    # Write full detail (daily grid per crop) to log file — kept out of agent context.
    detail = {
        "generated": today.isoformat(),
        "model": "FAO-56-style soil-water balance using Open-Meteo FAO Penman-Monteith ET0; surface waterings use the 1-3 cm layer, light waterings the 3-9 cm layer, deep waterings the 9-27 cm layer.",
        "bed_area_m2": area_m2,
        "surface_watering_l_per_m2": SURFACE_WATERING_L_PER_M2,
        "light_watering_l_per_m2": LIGHT_WATERING_L_PER_M2,
        "deep_watering_l_per_m2": DEEP_WATERING_L_PER_M2,
        "rain_skip_threshold_l_per_m2": RAIN_SKIP_THRESHOLD_L_PER_M2,
        "crop_assessments": assessments,
    }
    try:
        WATERING_DETAIL_LOG_PATH.write_text(json.dumps(detail, indent=2))
    except OSError:
        pass  # Non-fatal: agent reply is not affected if log write fails.

    return {
        "status": "ok",
        "total_waterings": total_waterings,
        "rainy_days": rainy_days,
        "per_crop": per_crop,
        "skipped_crops": skipped_indoor,
        "summary": summary,
    }


def weekly_status(today: date) -> dict[str, Any]:
    crops = list_planted_crops(active_only=True)
    active_crop_names = {crop["display_name"] for crop in crops}
    watering = watering_week()
    reminders = list_due_reminders(today)
    # Only surface harvest windows that are open or starting within 14 days.
    harvest_attention = [
        {"crop_name": w["crop_name"], "status": w["status"], "window": w.get("harvest_window") or w.get("expected_transplant_window")}
        for w in harvest_windows()
        if w["crop_name"] in active_crop_names and w["status"] in {"estimated", "active", "waiting_for_transplant"}
        and (
            w.get("harvest_window", {}).get("start", "9999") <= (today + timedelta(days=14)).isoformat()
            or w.get("expected_transplant_window", {}).get("start", "9999") <= (today + timedelta(days=14)).isoformat()
        )
    ]
    watering_summary = watering.get("summary", "Watering status is unavailable.")
    reminder_count = reminders.get("reminder_count", 0)
    notice_count = reminders.get("notice_count", 0)
    summary = f"{len(crops)} active crop(s). {watering_summary} {reminder_count} task(s) due."
    if notice_count:
        summary += f" {notice_count} notice(s)."
    return {
        "date": today.isoformat(),
        "status": "ok",
        "summary": summary,
        "active_crop_count": len(crops),
        "watering": {
            "status": watering["status"],
            "summary": watering_summary,
            "total_waterings": watering.get("total_waterings", 0),
            "rainy_days": watering.get("rainy_days", []),
            "per_crop": watering.get("per_crop", []),
            "skipped_crops": watering["skipped_crops"],
        },
        "due_reminders": reminders,
        "harvest_attention": harvest_attention,
    }


def format_weekly_report(status: dict[str, Any]) -> str:
    lines = [
        f"Weekly garden update ({status['date']})",
        status["watering"]["summary"],
    ]
    reminders = status.get("due_reminders", {})
    reminder_crops = reminders.get("crops", [])
    reminder_count = reminders.get("reminder_count", 0)
    if reminder_crops:
        lines.append(f"{reminder_count} garden task(s) are due:")
        shown = 0
        for crop_block in reminder_crops:
            for reminder in crop_block["reminders"]:
                if shown >= 6:
                    break
                lines.append(f"- {crop_block['crop_name']}: {reminder['text']}")
                shown += 1
        if reminder_count > 6:
            lines.append(f"- Plus {reminder_count - 6} more.")
        lines.append("Reply when tasks are done so I can mark the reminders completed.")
    else:
        lines.append("No garden tasks are due right now.")
    notices = reminders.get("notices", [])
    if notices:
        lines.append("Heads-up:")
        for notice in notices[:6]:
            lines.append(f"- {notice['crop_name']}: {notice['text']}")
        if len(notices) > 6:
            lines.append(f"- Plus {len(notices) - 6} more.")
    return "\n".join(lines)


def weekly_report(update_forecast: bool = True) -> dict[str, Any]:
    if update_forecast:
        update_weekly_forecast()
    validate_all()
    status = weekly_status(date.today())
    return {
        "date": status["date"],
        "type": "weekly_report",
        "message": format_weekly_report(status),
        "status": status,
        "summary": status["summary"],
    }


def enabled_recipients() -> list[dict[str, Any]]:
    data = load_recipients()
    validate_recipients(data)
    return [recipient for recipient in data["recipients"] if recipient["enabled"]]


def send_weekly_report(dry_run: bool = False, update_forecast: bool = True) -> dict[str, Any]:
    report = weekly_report(update_forecast=update_forecast)
    try:
        recipients = enabled_recipients()
    except ValidationError:
        recipients = []

    if not recipients:
        return {
            "date": report["date"],
            "type": "weekly_report_delivery",
            "dry_run": dry_run,
            "recipients": [],
            "message": report["message"],
            "command_returncode": 0,
            "stdout": "",
            "stderr": "",
            "summary": "Prepared weekly report (no recipients configured).",
        }

    targets = [recipient["target"] for recipient in recipients]
    command = [
        "openclaw",
        "message",
        "broadcast",
        "--channel",
        "telegram",
        "--message",
        report["message"],
        "--targets",
        *targets,
    ]
    if dry_run:
        command.append("--dry-run")
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        return {
            "date": report["date"],
            "type": "weekly_report_delivery",
            "dry_run": dry_run,
            "recipients": recipients,
            "message": report["message"],
            "command_returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "summary": f"Prepared weekly report for {len(recipients)} recipient(s).",
        }
    except FileNotFoundError:
        return {
            "date": report["date"],
            "type": "weekly_report_delivery",
            "dry_run": dry_run,
            "recipients": recipients,
            "message": report["message"],
            "command_returncode": -1,
            "stdout": "",
            "stderr": "Delivery tool 'openclaw' is not installed or not in PATH.",
            "summary": "Prepared weekly report (delivery tool 'openclaw' not installed).",
        }


def print_result(data: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    if isinstance(data, dict) and data.get("type") in {"weekly_report", "weekly_report_delivery"}:
        print(data["message"])
        if data.get("type") == "weekly_report_delivery":
            print(data["summary"])
            if data.get("dry_run"):
                print("Dry run only; no message was sent.")
            if data.get("command_returncode", 0) != 0:
                print(f"Delivery command failed with exit code {data['command_returncode']}.", file=sys.stderr)
                if data.get("stderr"):
                    print(data["stderr"], file=sys.stderr)
        return
    if isinstance(data, list):
        for item in data:
            print(json.dumps(item, sort_keys=True))
    elif isinstance(data, dict) and "summary" in data:
        print(data["summary"])
        if data.get("scheduled_waterings"):
            for item in data["scheduled_waterings"]:
                window = item["watering_window"]
                crops = ", ".join(crop.get("crop_name", crop["crop_id"]) for crop in item.get("limiting_crops", []))
                print(f"- {window['start']} to {window['end']}: {item['water_l_per_bed']:g} L/bed for {crops}")
        if data.get("watering", {}).get("scheduled_waterings"):
            for item in data["watering"]["scheduled_waterings"]:
                window = item["watering_window"]
                crops = ", ".join(crop.get("crop_name", crop["crop_id"]) for crop in item.get("limiting_crops", []))
                print(f"- {window['start']} to {window['end']}: {item['water_l_per_bed']:g} L/bed for {crops}")
        if data.get("due_reminders"):
            print("Due reminders:")
            for reminder in data["due_reminders"]:
                print(f"- {reminder.get('crop_name', reminder['crop_id'])}: {reminder['text']}")
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Garden assistance deterministic engine")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate")
    sub.add_parser("update-weekly-forecast")

    list_kb = sub.add_parser("list-kb-crops")
    list_kb.add_argument("--json", action="store_true")

    add_kb = sub.add_parser("add-kb-crop")
    add_kb.add_argument("--from-file", required=True)
    add_kb.add_argument("--json", action="store_true")

    crop_info_cmd = sub.add_parser("crop-info")
    crop_info_cmd.add_argument("--plant-id", required=True)
    crop_info_cmd.add_argument("--json", action="store_true")

    for name in ["recommend", "watering-week", "list-reminders", "harvest-windows", "list-planted-crops", "status", "weekly-report"]:
        cmd = sub.add_parser(name)
        cmd.add_argument("--json", action="store_true")
        if name == "list-planted-crops":
            cmd.add_argument("--include-inactive", action="store_true")
        if name == "weekly-report":
            cmd.add_argument("--skip-forecast-update", action="store_true")

    send_report = sub.add_parser("send-weekly-report")
    send_report.add_argument("--dry-run", action="store_true")
    send_report.add_argument("--skip-forecast-update", action="store_true")
    send_report.add_argument("--json", action="store_true")

    add = sub.add_parser("add-planted-crop")
    add.add_argument("--crop-id")
    add.add_argument("--plant-id", required=True)
    add.add_argument("--display-name", default="")
    add.add_argument("--method", choices=["indoor", "outdoor_direct", "perennial"], required=True)
    add.add_argument("--sown-date", default="")
    add.add_argument("--transplanted-date", default="")
    add.add_argument("--notes", default="")
    add.add_argument("--json", action="store_true")

    transplant = sub.add_parser("update-transplanted")
    transplant.add_argument("--crop-id", required=True)
    transplant.add_argument("--transplanted-date", default=date.today().isoformat())
    transplant.add_argument("--json", action="store_true")

    complete = sub.add_parser("mark-reminder-completed")
    complete.add_argument("--crop-id", required=True)
    complete.add_argument("--reminder-id", required=True)
    complete.add_argument("--actual-date", default="", help="Actual date the event occurred (anchor reminders only); defaults to today.")
    complete.add_argument("--json", action="store_true")

    suppress = sub.add_parser("mark-reminder-suppressed")
    suppress.add_argument("--crop-id", required=True)
    suppress.add_argument("--reminder-id", required=True)
    suppress.add_argument("--json", action="store_true")

    harvested = sub.add_parser("mark-harvested")
    harvested.add_argument("--crop-id", required=True)
    harvested.add_argument("--date", default=date.today().isoformat())
    harvested.add_argument("--json", action="store_true")

    log_harvest_cmd = sub.add_parser("log-harvest")
    log_harvest_cmd.add_argument("--crop-id", required=True)
    log_harvest_cmd.add_argument("--weight-kg", required=True, type=float)
    log_harvest_cmd.add_argument("--date", default=date.today().isoformat())
    log_harvest_cmd.add_argument("--notes", default="")
    log_harvest_cmd.add_argument("--json", action="store_true")

    bulk_harvest = sub.add_parser("bulk-log-harvest")
    bulk_harvest.add_argument("--file", required=True)
    bulk_harvest.add_argument("--json", action="store_true")

    list_harvests_cmd = sub.add_parser("list-harvests")
    list_harvests_cmd.add_argument("--crop-id", default="")
    list_harvests_cmd.add_argument("--json", action="store_true")

    savings = sub.add_parser("harvest-savings")
    savings.add_argument("--year", type=int, default=date.today().year)
    savings.add_argument("--json", action="store_true")

    finish = sub.add_parser("finish-harvest")
    finish.add_argument("--crop-id", required=True)
    finish.add_argument("--json", action="store_true")

    deactivate = sub.add_parser("deactivate-crop")
    deactivate.add_argument("--crop-id", required=True)
    deactivate.add_argument("--reason", default="")
    deactivate.add_argument("--date", default=date.today().isoformat())
    deactivate.add_argument("--json", action="store_true")

    list_adjustments = sub.add_parser("list-schedule-adjustments")
    list_adjustments.add_argument("--crop-id", required=True)
    list_adjustments.add_argument("--json", action="store_true")

    clear_adjustment = sub.add_parser("clear-schedule-adjustment")
    clear_adjustment.add_argument("--crop-id", required=True)
    clear_adjustment.add_argument("--adjustment-id", required=True)
    clear_adjustment.add_argument("--json", action="store_true")

    delete_crop_cmd = sub.add_parser("delete-planted-crop")
    delete_crop_cmd.add_argument("--crop-id", required=True)
    delete_crop_cmd.add_argument("--json", action="store_true")

    edit_crop_cmd = sub.add_parser("edit-planted-crop")
    edit_crop_cmd.add_argument("--crop-id", required=True)
    edit_crop_cmd.add_argument("--display-name", default="")
    edit_crop_cmd.add_argument("--sown-date", default="")
    edit_crop_cmd.add_argument("--transplanted-date", default="")
    edit_crop_cmd.add_argument("--notes", default="")
    edit_crop_cmd.add_argument("--json", action="store_true")

    delete_kb_cmd = sub.add_parser("delete-kb-crop")
    delete_kb_cmd.add_argument("--plant-id", required=True)
    delete_kb_cmd.add_argument("--json", action="store_true")

    edit_kb_cmd = sub.add_parser("edit-kb-crop")
    edit_kb_cmd.add_argument("--plant-id", required=True)
    edit_kb_cmd.add_argument("--from-file", required=True)
    edit_kb_cmd.add_argument("--json", action="store_true")

    configure_profile_cmd = sub.add_parser("configure-profile")
    configure_profile_cmd.add_argument("--latitude", type=float, required=True)
    configure_profile_cmd.add_argument("--longitude", type=float, required=True)
    configure_profile_cmd.add_argument("--timezone", required=True)
    configure_profile_cmd.add_argument("--last-frost", default="")
    configure_profile_cmd.add_argument("--first-frost", default="")
    configure_profile_cmd.add_argument("--bed-width", type=float, default=0.0)
    configure_profile_cmd.add_argument("--bed-length", type=float, default=0.0)
    configure_profile_cmd.add_argument("--json", action="store_true")

    scaffold_cmd = sub.add_parser("scaffold-kb-crop")
    scaffold_cmd.add_argument("--plant-id", required=True)
    scaffold_cmd.add_argument("--display-name", default="")
    scaffold_cmd.add_argument("--lifecycle", choices=["annual", "perennial"], default="annual")
    scaffold_cmd.add_argument("--template", default="")
    scaffold_cmd.add_argument("--file", default="")
    scaffold_cmd.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            validate_all()
            print("All garden memory files are valid.")
        elif args.command == "update-weekly-forecast":
            state = update_weekly_forecast()
            print_result({"summary": f"Updated {len(state['daily'])} forecast days from Open-Meteo.", "daily": state["daily"]}, False)
        elif args.command == "recommend":
            validate_all()
            kb = load_crop_knowledge_base()
            kb_count = len(kb.get("crop_knowledge", []))
            if kb_count == 0:
                instruction = (
                    "No recommendations are available because the crop knowledge base is empty. "
                    "Please suggest some common crops to the user that they can plan to grow and add to the knowledge base."
                )
                print_result({
                    "summary": instruction,
                    "instruction": instruction,
                    "status": "empty_kb",
                    "recommendations": []
                }, args.json)
            elif kb_count < 6:
                result = recommend_crops(kb, load_garden_state(), date.today().month)
                instruction = (
                    f"There are only {kb_count} crop(s) in the knowledge base. "
                    "Please suggest some common crops to the user that they can plan to grow and add to the knowledge base."
                )
                rec_summary = "\n".join(f"- {r['crop_name']} ({r['method']}): {r['status']}" for r in result)
                summary = f"{instruction}\n\nRecommendations:\n{rec_summary}" if rec_summary else f"{instruction}\n\nNo current recommendations for the existing crops."
                print_result({
                    "summary": summary,
                    "instruction": instruction,
                    "status": "sparse_kb",
                    "recommendations": result
                }, args.json)
            else:
                result = recommend_crops(kb, load_garden_state(), date.today().month)
                print_result(result, args.json)
        elif args.command == "watering-week":
            validate_all()
            print_result(watering_week(), args.json)
        elif args.command == "list-reminders":
            validate_all()
            print_result(list_due_reminders(date.today()), args.json)
        elif args.command == "harvest-windows":
            validate_all()
            print_result(harvest_windows(), args.json)
        elif args.command == "list-planted-crops":
            validate_all()
            print_result(list_planted_crops(active_only=not args.include_inactive), args.json)
        elif args.command == "status":
            validate_all()
            print_result(weekly_status(date.today()), args.json)
        elif args.command == "weekly-report":
            print_result(weekly_report(update_forecast=not args.skip_forecast_update), args.json)
        elif args.command == "send-weekly-report":
            print_result(send_weekly_report(dry_run=args.dry_run, update_forecast=not args.skip_forecast_update), args.json)
        elif args.command == "add-planted-crop":
            try:
                crop = add_planted_crop(args)
                print_result(crop, args.json)
            except UnknownPlantError as exc:
                plant_id_req = str(exc)
                if args.json:
                    print(json.dumps({
                        "error": "unknown_plant",
                        "plant_id": plant_id_req,
                        "message": (
                            f"Plant '{plant_id_req}' is not in the knowledge base. "
                            "Use add-kb-crop --from-file <path> to add it first, then retry add-planted-crop."
                        ),
                    }))
                else:
                    print(
                        f"ERROR: Unknown plant '{plant_id_req}'. "
                        "Use add-kb-crop to add it to the knowledge base first.",
                        file=sys.stderr,
                    )
                return 1
        elif args.command == "update-transplanted":
            crop = update_transplanted(args.crop_id, args.transplanted_date)
            print_result(crop, args.json)
        elif args.command == "mark-reminder-completed":
            print_result(complete_reminder(args.crop_id, args.reminder_id, args.actual_date, date.today()), args.json)
        elif args.command == "mark-reminder-suppressed":
            crop = mark_reminder(args.crop_id, args.reminder_id, "suppressed_reminder_ids")
            print_result(crop, args.json)
        elif args.command == "mark-harvested":
            validate_date_string(args.date, "--date", allow_empty=False)
            crop = mark_harvested(args.crop_id, date.fromisoformat(args.date))
            print_result(crop, args.json)
        elif args.command == "log-harvest":
            validate_date_string(args.date, "--date", allow_empty=False)
            print_result(log_harvest(args), args.json)
        elif args.command == "bulk-log-harvest":
            print_result(bulk_log_harvest(args.file), args.json)
        elif args.command == "list-harvests":
            print_result(list_harvests(args.crop_id), args.json)
        elif args.command == "harvest-savings":
            if args.year < 1:
                fail("--year must be a positive integer")
            print_result(harvest_savings(args.year), args.json)
        elif args.command == "finish-harvest":
            crop = finish_harvest(args.crop_id, date.today())
            print_result(crop, args.json)
        elif args.command == "deactivate-crop":
            crop = deactivate_crop(args.crop_id, args.reason, args.date)
            print_result(crop, args.json)
        elif args.command == "list-schedule-adjustments":
            print_result(list_schedule_adjustments(args.crop_id), args.json)
        elif args.command == "clear-schedule-adjustment":
            print_result(clear_schedule_adjustment(args.crop_id, args.adjustment_id), args.json)
        elif args.command == "list-kb-crops":
            print_result(list_kb_crops(load_crop_knowledge_base()), args.json)
        elif args.command == "add-kb-crop":
            print_result(add_kb_crop(args), args.json)
        elif args.command == "delete-planted-crop":
            print_result(delete_planted_crop(args.crop_id), args.json)
        elif args.command == "edit-planted-crop":
            print_result(edit_planted_crop(args), args.json)
        elif args.command == "delete-kb-crop":
            print_result(delete_kb_crop(args.plant_id), args.json)
        elif args.command == "edit-kb-crop":
            print_result(edit_kb_crop(args), args.json)
        elif args.command == "configure-profile":
            print_result(configure_profile(args), args.json)
        elif args.command == "scaffold-kb-crop":
            print_result(scaffold_kb_crop(args), args.json)
        elif args.command == "crop-info":
            validate_all()
            print_result(crop_info(args.plant_id), args.json)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except urllib.error.URLError as exc:
        print(f"ERROR: forecast fetch failed: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
