#!/usr/bin/env python3
"""
Fetch encrypted Apple Health payload from Supabase using challenge signing,
then decrypt day payloads for local storage.
"""

import argparse
import json
import math
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import error, request
from config import (
    load_effective_config,
    open_relay_request,
    resolve_state_dir,
    resolve_user_paths,
    secure_private_file,
    secure_state_directory,
    write_user_config,
)
from sync_cryptography import (
    decrypt_legacy_rsa_chunked_payload,
    decrypt_v5_payload,
    load_v5_public_keys_from_config,
    public_key_base64_from_pem,
    read_legacy_rsa_block_size,
    sign_legacy_challenge,
    sign_v5_challenge,
)

MAX_VALIDATION_DEPTH = 12
MAX_VALIDATION_NODES = 20000
MAX_DICT_KEYS = 256
MAX_LIST_ITEMS = 512
MAX_HEART_RATE_SAMPLES_PER_WORKOUT = 65_536
MAX_WORKOUT_TIME_SERIES_ITEMS = 65_536
MAX_WORKOUT_EVENTS_PER_WORKOUT = 4_096
MAX_WORKOUT_ROUTE_POINTS_PER_WORKOUT = 65_536
MAX_SERIALIZED_DAY_BYTES = 4_000_000
DATE_KEY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SAFE_METRIC_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]{1,64}$")
SAFE_WORKOUT_TYPE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 &'()/+-]{0,63}$")
SAFE_UUID_PATTERN = re.compile(
    r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
)
SAFE_ISO_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
SAFE_SOURCE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .&'()/+-]{0,63}$")
SAFE_BUNDLE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]{2,127}$")
SAFE_TIMEZONE_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_./+-]{1,63}$")
SAFE_UNIT_PATTERN = re.compile(r"^[A-Za-z%°][A-Za-z0-9%°/().*+-]{0,15}$")
SAFE_SLEEP_STAGE_PATTERN = re.compile(r"^[a-z_]{1,32}$")
SAFE_DEVICE_TEXT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .:&'()/+_,-]{0,127}$")
SAFE_DEVICE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .:&'()/+_,-]{0,127}$")
WORKOUT_DEVICE_TEXT_FIELDS = {
    "name",
    "manufacturer",
    "model",
    "hardware_version",
    "firmware_version",
    "software_version",
}
WORKOUT_DEVICE_IDENTIFIER_FIELDS = {
    "local_identifier",
    "udi_device_identifier",
}
WORKOUT_EVENT_TYPES = {
    "pause",
    "resume",
    "lap",
    "marker",
    "motion_paused",
    "motion_resumed",
    "segment",
    "pause_or_resume_request",
}
WORKOUT_SPEED_SOURCES = {
    "cross_country_skiing",
    "cycling",
    "paddle_sports",
    "rowing",
    "running",
    "stair_ascent",
    "stair_descent",
    "walking",
}
WORKOUT_DISTANCE_SOURCES = {
    "cross_country_skiing",
    "cycling",
    "downhill_snow_sports",
    "paddle_sports",
    "rowing",
    "skating_sports",
    "swimming",
    "walking_running",
    "wheelchair",
}
DROP_VALUE = object()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def record_fetch_success(
    user_config: Dict[str, Any],
    attempted_at: str,
    succeeded_at: str,
    row_count: int,
    validation_metrics: Dict[str, int],
) -> None:
    user_config["last_fetch_attempt_at"] = attempted_at
    user_config["last_fetch_success_at"] = succeeded_at
    user_config["last_fetch_at"] = succeeded_at
    user_config["last_fetch_status"] = "ok"
    user_config.pop("last_fetch_error", None)
    user_config["last_fetch_row_count"] = row_count
    user_config["last_validation_raw_days"] = validation_metrics["raw_days"]
    user_config["last_validation_stored_days"] = validation_metrics["stored_days"]
    user_config["last_validation_dropped_days"] = validation_metrics["dropped_days"]


def migrate_legacy_fetch_timestamp(user_config: Dict[str, Any]) -> None:
    if "last_fetch_success_at" in user_config:
        return
    legacy_timestamp = user_config.get("last_fetch_at")
    if user_config.get("last_fetch_status") == "ok" and legacy_timestamp:
        user_config["last_fetch_success_at"] = legacy_timestamp
    else:
        user_config.pop("last_fetch_at", None)


def record_fetch_failure(user_config: Dict[str, Any], attempted_at: str, error_message: str) -> None:
    migrate_legacy_fetch_timestamp(user_config)
    user_config["last_fetch_attempt_at"] = attempted_at
    user_config["last_fetch_status"] = "error"
    user_config["last_fetch_error"] = error_message


def normalize_public_key_base64(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def http_post_json(url: str, payload: Dict[str, Any], timeout: int, apikey: str, region: str) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-region": region,
            "apikey": apikey,
        },
        method="POST",
    )
    try:
        with open_relay_request(req, timeout=timeout) as response:
            raw = response.read()
            return json.loads(raw.decode("utf-8"))
    except error.HTTPError as http_error:
        detail = http_error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {http_error.code} from function: {detail}") from http_error
    except error.URLError as url_error:
        raise RuntimeError(f"Cannot reach function: {url_error}") from url_error


def merge_day_payload(base: Any, overlay: Any) -> Any:
    """Merge complete day snapshots with the newer scope winning per category."""
    if not isinstance(base, dict) or not isinstance(overlay, dict):
        return overlay
    merged = dict(base)
    merged.update(overlay)
    return merged


def merge_scope_payloads(
    legacy_payload: Dict[str, Any],
    history_payload: Dict[str, Any],
    recent_payload: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(legacy_payload)
    for scope_payload in (history_payload, recent_payload):
        for date_key, day_payload in scope_payload.items():
            if date_key in merged:
                merged[date_key] = merge_day_payload(merged[date_key], day_payload)
            else:
                merged[date_key] = day_payload
    return merged

def decrypt_rows(
    rows: List[Dict[str, Any]],
    protocol_version: int,
    legacy_private_key_path: Optional[Path],
    v5_encryption_private_key_path: Optional[Path],
    v5_encryption_public_key_base64: str,
    v5_recent_max_ciphertext_bytes: int,
    v5_recent_max_plaintext_bytes: int,
    v5_history_max_ciphertext_bytes: int,
    v5_history_max_plaintext_bytes: int,
) -> Dict[str, Any]:
    legacy_decrypted: Dict[str, Any] = {}
    scoped_decrypted: Dict[str, Dict[str, Any]] = {
        "history": {},
        "recent": {},
    }
    rsa_block_size = (
        read_legacy_rsa_block_size(legacy_private_key_path)
        if legacy_private_key_path and legacy_private_key_path.exists()
        else 0
    )

    for row in rows:
        scope = row.get("scope")
        ciphertext = row.get("ciphertext")
        if isinstance(scope, str) and isinstance(ciphertext, str):
            if scope == "recent":
                max_ciphertext_bytes = v5_recent_max_ciphertext_bytes
                max_plaintext_bytes = v5_recent_max_plaintext_bytes
            elif scope == "history":
                max_ciphertext_bytes = v5_history_max_ciphertext_bytes
                max_plaintext_bytes = v5_history_max_plaintext_bytes
            else:
                raise RuntimeError(f"Unsupported v5 scope: {scope}")
            if not v5_encryption_private_key_path or not v5_encryption_private_key_path.exists():
                raise RuntimeError("Missing v5 encryption private key required to decrypt v5 rows.")
            plaintext, aad = decrypt_v5_payload(
                row,
                v5_encryption_private_key_path,
                v5_encryption_public_key_base64,
                str(row.get("user_id", "")),
                scope,
                max_ciphertext_bytes,
                max_plaintext_bytes,
            )
            if aad.get("user_id") != row.get("user_id") or aad.get("scope") != scope:
                raise RuntimeError("V5 payload AAD does not match row metadata.")
            scope_payload = json.loads(plaintext.decode("utf-8"))
            if not isinstance(scope_payload, dict):
                raise RuntimeError("Invalid decrypted v5 scope payload.")
            for date_key, day_payload in scope_payload.items():
                if not isinstance(date_key, str):
                    continue
                scoped_decrypted[scope][date_key] = day_payload
            continue

        date = row.get("date")
        encrypted_data = row.get("data")
        if not isinstance(date, str) or not isinstance(encrypted_data, str):
            continue

        if protocol_version == 5 and not legacy_private_key_path:
            raise RuntimeError("Encountered legacy RSA row but no legacy RSA private key is configured.")
        if not legacy_private_key_path or not legacy_private_key_path.exists():
            raise RuntimeError("Missing RSA private key required to decrypt legacy rows.")

        plaintext = decrypt_legacy_rsa_chunked_payload(legacy_private_key_path, encrypted_data, rsa_block_size)
        legacy_decrypted[date] = json.loads(plaintext.decode("utf-8"))

    return merge_scope_payloads(
        legacy_decrypted,
        scoped_decrypted["history"],
        scoped_decrypted["recent"],
    )


def path_matches(path: Tuple[str, ...], pattern: Tuple[str, ...]) -> bool:
    return len(path) == len(pattern) and all(
        expected == "*" or actual == expected
        for actual, expected in zip(path, pattern)
    )


def path_has_prefix(path: Tuple[str, ...], prefix: Tuple[str, ...]) -> bool:
    return len(path) >= len(prefix) and all(
        expected == "*" or actual == expected
        for actual, expected in zip(path[:len(prefix)], prefix)
    )


def should_keep_string(path: Tuple[str, ...], value: str) -> bool:
    if len(value.encode("utf-8")) > 128:
        return False

    if path == ("workouts", "*", "type"):
        return bool(SAFE_WORKOUT_TYPE_PATTERN.fullmatch(value))
    if path == ("workouts", "*", "id"):
        return bool(SAFE_UUID_PATTERN.fullmatch(value))
    if path in {("workouts", "*", "start"), ("workouts", "*", "end")}:
        return bool(SAFE_ISO_TIMESTAMP_PATTERN.fullmatch(value))
    if path == ("workouts", "*", "source"):
        return bool(SAFE_SOURCE_PATTERN.fullmatch(value))
    if path == ("workouts", "*", "source_bundle_id"):
        return bool(SAFE_BUNDLE_ID_PATTERN.fullmatch(value))
    if path == ("workouts", "*", "timezone"):
        return bool(SAFE_TIMEZONE_PATTERN.fullmatch(value))
    if path in {
        ("sleep", "sessions", "*", "start"),
        ("sleep", "sessions", "*", "end"),
        ("sleep", "first_sleep_start"),
        ("sleep", "last_sleep_end"),
    }:
        return bool(SAFE_ISO_TIMESTAMP_PATTERN.fullmatch(value))
    if path == ("sleep", "sessions", "*", "stage"):
        return bool(SAFE_SLEEP_STAGE_PATTERN.fullmatch(value))
    if path == ("sleep", "sessions", "*", "timezone"):
        return bool(SAFE_TIMEZONE_PATTERN.fullmatch(value))
    if len(path) == 3 and path[0] in {"body", "heart"} and path[2] == "unit":
        return bool(SAFE_UNIT_PATTERN.fullmatch(value))
    if len(path) == 4 and path_matches(path, ("workouts", "*", "device", path[3])):
        if path[3] in WORKOUT_DEVICE_TEXT_FIELDS:
            return bool(SAFE_DEVICE_TEXT_PATTERN.fullmatch(value))
        if path[3] in WORKOUT_DEVICE_IDENTIFIER_FIELDS:
            return bool(SAFE_DEVICE_IDENTIFIER_PATTERN.fullmatch(value))
        return False
    if path_has_prefix(path, ("workouts", "*", "metadata")):
        return bool(
            SAFE_UUID_PATTERN.fullmatch(value)
            or SAFE_ISO_TIMESTAMP_PATTERN.fullmatch(value)
            or SAFE_TIMEZONE_PATTERN.fullmatch(value)
            or SAFE_BUNDLE_ID_PATTERN.fullmatch(value)
            or SAFE_SOURCE_PATTERN.fullmatch(value)
        )
    return False


def sanitize_workout_heart_rate_samples(value: Any) -> Any:
    if not isinstance(value, list) or len(value) > MAX_HEART_RATE_SAMPLES_PER_WORKOUT:
        return DROP_VALUE

    required_keys = {"start_offset_ms", "end_offset_ms", "bpm"}
    sanitized_samples: List[Dict[str, Any]] = []
    for sample in value:
        if not isinstance(sample, dict) or set(sample.keys()) != required_keys:
            return DROP_VALUE

        start_offset = sample.get("start_offset_ms")
        end_offset = sample.get("end_offset_ms")
        bpm = sample.get("bpm")
        if (
            isinstance(start_offset, bool)
            or not isinstance(start_offset, int)
            or isinstance(end_offset, bool)
            or not isinstance(end_offset, int)
            or end_offset < start_offset
            or isinstance(bpm, bool)
            or not isinstance(bpm, (int, float))
            or not math.isfinite(float(bpm))
            or float(bpm) <= 0
        ):
            return DROP_VALUE

        sanitized_samples.append(
            {
                "start_offset_ms": start_offset,
                "end_offset_ms": end_offset,
                "bpm": bpm,
            }
        )
    return sanitized_samples


def is_exact_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def has_valid_offset_range(item: Dict[str, Any]) -> bool:
    start_offset = item.get("start_offset_ms")
    end_offset = item.get("end_offset_ms")
    return (
        is_exact_int(start_offset)
        and is_exact_int(end_offset)
        and end_offset >= start_offset
    )


def sanitize_workout_timing(value: Any) -> Any:
    required_keys = {
        "elapsed_duration_ms",
        "active_duration_ms",
        "paused_duration_ms",
    }
    if not isinstance(value, dict) or set(value.keys()) != required_keys:
        return DROP_VALUE
    if any(not is_exact_int(value[key]) or value[key] < 0 for key in required_keys):
        return DROP_VALUE
    if value["active_duration_ms"] + value["paused_duration_ms"] != value["elapsed_duration_ms"]:
        return DROP_VALUE
    return {key: value[key] for key in required_keys}


def sanitize_workout_events(value: Any) -> Any:
    if not isinstance(value, list) or len(value) > MAX_WORKOUT_EVENTS_PER_WORKOUT:
        return DROP_VALUE

    required_keys = {"type", "start_offset_ms", "end_offset_ms"}
    sanitized: List[Dict[str, Any]] = []
    for event in value:
        if (
            not isinstance(event, dict)
            or set(event.keys()) != required_keys
            or event.get("type") not in WORKOUT_EVENT_TYPES
            or not has_valid_offset_range(event)
        ):
            return DROP_VALUE
        sanitized.append({key: event[key] for key in required_keys})
    return sanitized


def sanitize_workout_speed_samples(value: Any) -> Any:
    if not isinstance(value, list) or len(value) > MAX_WORKOUT_TIME_SERIES_ITEMS:
        return DROP_VALUE

    required_keys = {
        "source",
        "start_offset_ms",
        "end_offset_ms",
        "speed_meters_per_second",
        "pace_seconds_per_kilometer",
    }
    sanitized: List[Dict[str, Any]] = []
    for sample in value:
        if (
            not isinstance(sample, dict)
            or set(sample.keys()) != required_keys
            or sample.get("source") not in WORKOUT_SPEED_SOURCES
            or not has_valid_offset_range(sample)
            or not is_finite_number(sample.get("speed_meters_per_second"))
            or float(sample["speed_meters_per_second"]) <= 0
            or not is_finite_number(sample.get("pace_seconds_per_kilometer"))
            or float(sample["pace_seconds_per_kilometer"]) <= 0
        ):
            return DROP_VALUE
        sanitized.append({key: sample[key] for key in required_keys})
    return sanitized


def sanitize_workout_distance_intervals(value: Any) -> Any:
    if not isinstance(value, list) or len(value) > MAX_WORKOUT_TIME_SERIES_ITEMS:
        return DROP_VALUE

    required_keys = {
        "source",
        "start_offset_ms",
        "end_offset_ms",
        "duration_ms",
        "distance_meters",
    }
    derived_keys = {"speed_meters_per_second", "pace_seconds_per_kilometer"}
    allowed_keys = required_keys | derived_keys
    sanitized: List[Dict[str, Any]] = []
    for interval in value:
        if not isinstance(interval, dict):
            return DROP_VALUE
        keys = set(interval.keys())
        has_all_derived_values = derived_keys.issubset(keys)
        if (
            not required_keys.issubset(keys)
            or not keys.issubset(allowed_keys)
            or bool(keys & derived_keys) != has_all_derived_values
            or interval.get("source") not in WORKOUT_DISTANCE_SOURCES
            or not has_valid_offset_range(interval)
            or not is_exact_int(interval.get("duration_ms"))
            or interval["duration_ms"] < 0
            or not is_finite_number(interval.get("distance_meters"))
            or float(interval["distance_meters"]) < 0
        ):
            return DROP_VALUE
        if has_all_derived_values and (
            not is_finite_number(interval.get("speed_meters_per_second"))
            or float(interval["speed_meters_per_second"]) <= 0
            or not is_finite_number(interval.get("pace_seconds_per_kilometer"))
            or float(interval["pace_seconds_per_kilometer"]) <= 0
        ):
            return DROP_VALUE
        sanitized.append({key: interval[key] for key in keys})
    return sanitized


def sanitize_workout_route_points(value: Any) -> Any:
    if not isinstance(value, list) or len(value) > MAX_WORKOUT_ROUTE_POINTS_PER_WORKOUT:
        return DROP_VALUE

    required_keys = {"timestamp_offset_ms", "latitude", "longitude"}
    optional_keys = {
        "altitude_meters",
        "horizontal_accuracy_meters",
        "vertical_accuracy_meters",
        "speed_meters_per_second",
        "speed_accuracy_meters_per_second",
        "course_degrees",
        "course_accuracy_degrees",
    }
    nonnegative_keys = {
        "horizontal_accuracy_meters",
        "vertical_accuracy_meters",
        "speed_meters_per_second",
        "speed_accuracy_meters_per_second",
        "course_accuracy_degrees",
    }
    sanitized: List[Dict[str, Any]] = []
    for point in value:
        if not isinstance(point, dict):
            return DROP_VALUE
        keys = set(point.keys())
        if (
            not required_keys.issubset(keys)
            or not keys.issubset(required_keys | optional_keys)
            or not is_exact_int(point.get("timestamp_offset_ms"))
            or not is_finite_number(point.get("latitude"))
            or not -90 <= float(point["latitude"]) <= 90
            or not is_finite_number(point.get("longitude"))
            or not -180 <= float(point["longitude"]) <= 180
        ):
            return DROP_VALUE
        for key in keys & optional_keys:
            if not is_finite_number(point[key]):
                return DROP_VALUE
            if key in nonnegative_keys and float(point[key]) < 0:
                return DROP_VALUE
        if "course_degrees" in point and not 0 <= float(point["course_degrees"]) <= 360:
            return DROP_VALUE
        sanitized.append({key: point[key] for key in keys})
    return sanitized


def sanitize_value(value: Any, depth: int, counter: List[int], path: Tuple[str, ...] = ()) -> Any:
    if depth > MAX_VALIDATION_DEPTH:
        return DROP_VALUE

    if path_matches(path, ("workouts", "*", "heart_rate_samples")):
        return sanitize_workout_heart_rate_samples(value)
    if path_matches(path, ("workouts", "*", "workout_timing")):
        return sanitize_workout_timing(value)
    if path_matches(path, ("workouts", "*", "workout_events")):
        return sanitize_workout_events(value)
    if path_matches(path, ("workouts", "*", "workout_activities")):
        return DROP_VALUE
    if path_matches(path, ("workouts", "*", "speed_samples")):
        return sanitize_workout_speed_samples(value)
    if path_matches(path, ("workouts", "*", "distance_intervals")):
        return sanitize_workout_distance_intervals(value)
    if path_matches(path, ("workouts", "*", "route_points")):
        return sanitize_workout_route_points(value)

    counter[0] += 1
    if counter[0] > MAX_VALIDATION_NODES:
        return DROP_VALUE

    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            return DROP_VALUE
        return value
    if isinstance(value, str):
        # Keep only tightly constrained string fields that are useful for analysis.
        if should_keep_string(path, value):
            return value
        return DROP_VALUE
    if isinstance(value, list):
        sanitized_items: List[Any] = []
        for item in value[:MAX_LIST_ITEMS]:
            sanitized = sanitize_value(item, depth + 1, counter, path + ("*",))
            if sanitized is DROP_VALUE:
                continue
            sanitized_items.append(sanitized)
        return sanitized_items
    if isinstance(value, dict):
        sanitized_dict: Dict[str, Any] = {}
        item_count = 0
        for key, child in value.items():
            if item_count >= MAX_DICT_KEYS:
                break
            if not isinstance(key, str):
                continue
            key_clean = key.strip()
            if not SAFE_METRIC_KEY_PATTERN.fullmatch(key_clean):
                continue
            sanitized = sanitize_value(child, depth + 1, counter, path + (key_clean,))
            if sanitized is DROP_VALUE:
                continue
            sanitized_dict[key_clean] = sanitized
            item_count += 1
        return sanitized_dict
    return DROP_VALUE


def sanitize_decrypted_payload(raw_payload: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, int]]:
    sanitized_payload: Dict[str, Any] = {}
    metrics = {
        "raw_days": 0,
        "stored_days": 0,
        "dropped_days": 0,
    }

    for date_key, payload in raw_payload.items():
        metrics["raw_days"] += 1
        if not isinstance(date_key, str) or not DATE_KEY_PATTERN.fullmatch(date_key):
            metrics["dropped_days"] += 1
            continue

        # Apply traversal limits per day so large historical payloads do not
        # exhaust the validator budget cumulatively across unrelated dates.
        counter = [0]
        sanitized = sanitize_value(payload, depth=0, counter=counter, path=())
        if sanitized is DROP_VALUE:
            metrics["dropped_days"] += 1
            continue
        if isinstance(sanitized, (dict, list)) and not sanitized:
            metrics["dropped_days"] += 1
            continue

        serialized = json.dumps(sanitized, separators=(",", ":"))
        if len(serialized.encode("utf-8")) > MAX_SERIALIZED_DAY_BYTES:
            metrics["dropped_days"] += 1
            continue

        sanitized_payload[date_key] = sanitized
        metrics["stored_days"] += 1

    return sanitized_payload, metrics


def ensure_sqlite_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        create table if not exists health_data (
          id integer primary key autoincrement,
          user_id text not null,
          date text not null,
          data text not null,
          created_at text not null,
          updated_at text not null
        );
        """
    )
    conn.execute(
        "create unique index if not exists health_data_user_date_idx "
        "on health_data (user_id, date);"
    )
    migrate_legacy_health_samples(conn)
    conn.commit()


def migrate_legacy_health_samples(conn: sqlite3.Connection) -> None:
    table_exists = conn.execute(
        "select 1 from sqlite_master where type='table' and name='health_samples' limit 1"
    ).fetchone()
    if not table_exists:
        return

    legacy_rows = conn.execute(
        "select record_id, fetched_at, payload_json from health_samples"
    ).fetchall()
    for user_id, fetched_at, payload_json in legacy_rows:
        try:
            payload = json.loads(payload_json)
            if not isinstance(payload, dict):
                continue
            for date_key, day_payload in payload.items():
                if not isinstance(date_key, str):
                    continue
                serialized = json.dumps(day_payload, separators=(",", ":"))
                conn.execute(
                    """
                    insert into health_data(user_id, date, data, created_at, updated_at)
                    values (?, ?, ?, ?, ?)
                    on conflict(user_id, date) do update
                      set data=excluded.data,
                          updated_at=excluded.updated_at
                    """,
                    (user_id, date_key, serialized, fetched_at, fetched_at),
                )
        except Exception:
            continue


def write_sqlite(sqlite_path: Path, user_id: str, fetched_at: str, data: Dict[str, Any]) -> None:
    sqlite_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if sqlite_path.exists() or sqlite_path.is_symlink():
        secure_private_file(sqlite_path)
    conn = sqlite3.connect(sqlite_path)
    try:
        ensure_sqlite_schema(conn)
        for date_key, day_payload in data.items():
            if not isinstance(date_key, str):
                continue
            serialized = json.dumps(day_payload, separators=(",", ":"))
            conn.execute(
                """
                insert into health_data(user_id, date, data, created_at, updated_at)
                values (?, ?, ?, ?, ?)
                on conflict(user_id, date) do update
                  set data=excluded.data,
                      updated_at=excluded.updated_at
                """,
                (user_id, date_key, serialized, fetched_at, fetched_at),
            )
        conn.commit()
    finally:
        conn.close()
    secure_private_file(sqlite_path)


def write_ndjson(json_path: Path, envelope: Dict[str, Any]) -> None:
    json_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if json_path.exists() or json_path.is_symlink():
        secure_private_file(json_path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    file_descriptor = os.open(json_path, flags, 0o600)
    os.fchmod(file_descriptor, 0o600)
    with os.fdopen(file_descriptor, "a", encoding="utf-8") as file_handle:
        file_handle.write(json.dumps(envelope, separators=(",", ":")) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch and store Apple Health data from Supabase.")
    parser.add_argument(
        "--state-dir",
        default="",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--apikey",
        default="",
        help="Supabase publishable key for Edge Function header validation.",
    )
    parser.add_argument("--user-id", default="")
    parser.add_argument("--record-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--private-key-path", default="")
    parser.add_argument("--public-key", default="")
    parser.add_argument(
        "--storage",
        choices=("auto", "sqlite", "json"),
        default="auto",
    )
    parser.add_argument("--sqlite-path", default="")
    parser.add_argument("--json-path", default="")
    parser.add_argument("--timeout-seconds", type=int, default=20)
    return parser.parse_args()


def resolve_runtime(
    args: argparse.Namespace,
    config: Dict[str, Any],
    paths: Dict[str, Path],
) -> Dict[str, Any]:
    function_url = str(config.get("supabase_get_data_url", "")).strip()
    user_id = args.user_id or args.record_id or config.get("user_id", "") or config.get("record_id", "")
    protocol_version = int(config.get("protocol_version", 4) or 4)
    legacy_private_key_path = Path(
        config.get("private_key_path", paths["secrets_dir"] / "private_key.pem")
    ).expanduser()
    legacy_public_key_base64 = normalize_public_key_base64(config.get("public_key_base64", ""))
    active_private_key_path = Path(args.private_key_path).expanduser() if args.private_key_path else None
    request_public_key = normalize_public_key_base64(args.public_key)
    signing_public_key_base64 = ""
    signing_private_key_path = active_private_key_path
    v5_encryption_private_key_path: Optional[Path] = None
    v5_encryption_public_key_base64 = ""
    if protocol_version == 5:
        signing_public_key_base64 = normalize_public_key_base64(
            request_public_key or config.get("signing_public_key_base64", "")
        )
        if not signing_public_key_base64:
            signing_public_key_base64, v5_encryption_public_key_base64 = load_v5_public_keys_from_config(config)
        else:
            _, v5_encryption_public_key_base64 = load_v5_public_keys_from_config(config)
        if signing_private_key_path is None:
            signing_private_key_path = Path(
                config.get("signing_private_key_path", paths["secrets_dir"] / "signing_private_key_v5.pem")
            ).expanduser()
        v5_encryption_private_key_path = Path(
            config.get("encryption_private_key_path", paths["secrets_dir"] / "encryption_private_key_v5.pem")
        ).expanduser()
    else:
        signing_public_key_base64 = normalize_public_key_base64(request_public_key or legacy_public_key_base64)
        if not signing_public_key_base64:
            public_key_path = Path(config.get("public_key_path", paths["config_dir"] / "public_key.pem")).expanduser()
            if public_key_path.exists():
                signing_public_key_base64 = public_key_base64_from_pem(public_key_path.read_text(encoding="utf-8"))
            else:
                raise RuntimeError(
                    "Missing public key. Set --public-key or config.public_key_base64/public_key_path."
                )
        if signing_private_key_path is None:
            signing_private_key_path = Path(
                config.get("private_key_path", paths["secrets_dir"] / "private_key.pem")
            ).expanduser()

    if not user_id:
        raise RuntimeError("Missing user ID. Set --user-id or config.user_id.")
    if not function_url:
        raise RuntimeError("Missing app-owned get-data URL in scripts/config.py.")
    if not signing_private_key_path or not signing_private_key_path.exists():
        raise RuntimeError(f"Missing signing private key file: {signing_private_key_path}")
    v5_recent_max_ciphertext_bytes = int(config.get("v5_recent_max_ciphertext_bytes", 4_194_304) or 4_194_304)
    v5_recent_max_plaintext_bytes = int(config.get("v5_recent_max_plaintext_bytes", 4_194_304) or 4_194_304)
    v5_history_max_ciphertext_bytes = int(config.get("v5_history_max_ciphertext_bytes", 16_777_216) or 16_777_216)
    v5_history_max_plaintext_bytes = int(config.get("v5_history_max_plaintext_bytes", 16_777_216) or 16_777_216)
    if (
        v5_recent_max_ciphertext_bytes <= 0
        or v5_recent_max_plaintext_bytes <= 0
        or v5_history_max_ciphertext_bytes <= 0
        or v5_history_max_plaintext_bytes <= 0
    ):
        raise RuntimeError("Configured v5 size limits must be positive integers.")
    return {
        "function_url": function_url,
        "user_id": user_id,
        "protocol_version": protocol_version,
        "signing_private_key_path": signing_private_key_path,
        "signing_public_key_base64": signing_public_key_base64,
        "legacy_private_key_path": legacy_private_key_path if legacy_private_key_path.exists() else None,
        "v5_encryption_private_key_path": v5_encryption_private_key_path
        if v5_encryption_private_key_path and v5_encryption_private_key_path.exists()
        else None,
        "v5_encryption_public_key_base64": v5_encryption_public_key_base64,
        "v5_recent_max_ciphertext_bytes": v5_recent_max_ciphertext_bytes,
        "v5_recent_max_plaintext_bytes": v5_recent_max_plaintext_bytes,
        "v5_history_max_ciphertext_bytes": v5_history_max_ciphertext_bytes,
        "v5_history_max_plaintext_bytes": v5_history_max_plaintext_bytes,
        "algorithm": str(config.get("algorithm", "RSA-2048")),
    }


def main() -> int:
    os.umask(0o077)
    args = parse_args()
    state_dir = resolve_state_dir(args.state_dir)
    paths = resolve_user_paths(state_dir)
    for private_dir in (state_dir, paths["config_dir"], paths["secrets_dir"]):
        if private_dir.exists():
            secure_state_directory(private_dir)
    user_config: Dict[str, Any] = {}
    config: Dict[str, Any] = {}
    fetch_attempted_at = ""

    try:
        user_config, config = load_effective_config(state_dir)
        fetch_attempted_at = now_iso()
        runtime = resolve_runtime(args, config, paths)
        publishable_key = args.apikey or str(config.get("supabase_publishable_key", "")).strip()
        region = str(config.get("supabase_region", "")).strip()
        if not publishable_key:
            raise RuntimeError("Missing app-owned publishable key in scripts/config.py or --apikey.")
        if not region:
            raise RuntimeError("Missing app-owned Supabase region in scripts/config.py.")
        challenge_response = http_post_json(
            str(runtime["function_url"]),
            {
                "action": "issue_challenge",
                "id": runtime["user_id"],
                "protocol_version": runtime["protocol_version"],
            },
            args.timeout_seconds,
            publishable_key,
            region,
        )

        challenge = challenge_response["challenge"]
        challenge_id = challenge_response["challengeId"]
        if int(runtime["protocol_version"]) == 5:
            signature = sign_v5_challenge(Path(runtime["signing_private_key_path"]), challenge)
        else:
            signature = sign_legacy_challenge(
                Path(runtime["signing_private_key_path"]),
                challenge,
                str(runtime["algorithm"]),
            )

        get_data_payload: Dict[str, Any] = {
            "action": "get_data",
            "id": runtime["user_id"],
            "challengeId": challenge_id,
            "signature": signature,
        }
        if int(runtime["protocol_version"]) == 5:
            get_data_payload["protocol_version"] = 5
            get_data_payload["signing_public_key"] = runtime["signing_public_key_base64"]
        else:
            get_data_payload["public_key"] = runtime["signing_public_key_base64"]

        data_response = http_post_json(
            str(runtime["function_url"]),
            get_data_payload,
            args.timeout_seconds,
            publishable_key,
            region,
        )

        encrypted_rows = data_response.get("data", [])
        if not isinstance(encrypted_rows, list):
            raise RuntimeError("Invalid get_data response format (data must be list).")

        decrypted_payload = decrypt_rows(
            encrypted_rows,
            int(runtime["protocol_version"]),
            runtime["legacy_private_key_path"],
            runtime["v5_encryption_private_key_path"],
            str(runtime["v5_encryption_public_key_base64"]),
            int(runtime["v5_recent_max_ciphertext_bytes"]),
            int(runtime["v5_recent_max_plaintext_bytes"]),
            int(runtime["v5_history_max_ciphertext_bytes"]),
            int(runtime["v5_history_max_plaintext_bytes"]),
        )
        sanitized_payload, validation_metrics = sanitize_decrypted_payload(decrypted_payload)
        fetched_at = now_iso()
        envelope = {
            "user_id": runtime["user_id"],
            "fetched_at": fetched_at,
            "payload": sanitized_payload,
            "row_count": len(encrypted_rows),
            "validation": validation_metrics,
        }

        if validation_metrics["raw_days"] > 0 and validation_metrics["stored_days"] == 0:
            raise RuntimeError("Validation rejected all decrypted rows; nothing stored.")

        storage = args.storage
        if storage == "auto":
            storage = config.get("storage", "sqlite")

        if storage == "sqlite":
            sqlite_path = Path(args.sqlite_path or config.get("sqlite_path", state_dir / "health_data.db"))
            write_sqlite(sqlite_path.expanduser(), str(runtime["user_id"]), fetched_at, sanitized_payload)
        elif storage == "json":
            json_path = Path(args.json_path or config.get("json_path", paths["config_dir"] / "health_data.ndjson"))
            write_ndjson(json_path.expanduser(), envelope)
        else:
            raise RuntimeError(f"Unsupported storage backend: {storage}")

        record_fetch_success(
            user_config,
            fetch_attempted_at,
            fetched_at,
            len(encrypted_rows),
            validation_metrics,
        )
        write_user_config(user_config, state_dir)

        print(
            f"Fetch successful: user_id={runtime['user_id']}, protocol=v{runtime['protocol_version']}, storage={storage}, "
            f"rows={len(encrypted_rows)}, stored_days={validation_metrics['stored_days']}, "
            f"dropped_days={validation_metrics['dropped_days']}, fetched_at={fetched_at}"
        )
        return 0
    except Exception as runtime_error:
        print(f"Error: {runtime_error}", file=sys.stderr)
        try:
            if user_config:
                record_fetch_failure(
                    user_config,
                    fetch_attempted_at or now_iso(),
                    str(runtime_error),
                )
                write_user_config(user_config, state_dir)
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
