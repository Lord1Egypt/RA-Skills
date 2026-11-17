#!/usr/bin/env python3
"""Read-only third-party radar monitor. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal
import fcntl
import hashlib
import http.client
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import urllib.error
import urllib.request

CURRENT_URL = "https://codex-reset-radar.pages.dev/current.json"
CACHE_PATH = Path.home() / ".openclaw/workspace/cache/codex-radar-last.json"
REQUEST_TIMEOUT = 15
MAX_BODY = 1024 * 1024
MAX_CACHE = 256 * 1024
MAX_SEEN = 256
MAX_AGE = 24 * 60 * 60
FUTURE_SKEW = 300
PROB_THRESHOLD = Decimal("0.1")
VERSION = "1.1.0"
STATUSES = frozenset({
    "none", "unknown", "idle", "watch", "watching", "monitoring", "pending",
    "announced", "possible", "likely", "open", "active", "closed", "expired",
    "confirmed", "completed", "cooldown", "unconfirmed", "community_confirmed",
    "official_confirmed", "stationmaster_confirmed",
})
LEVELS = frozenset({"none", "unknown", "low", "medium", "high", "very_high"})
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9:._/-]{0,159}\Z")
TIME_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})\Z")
STATE_KEYS = frozenset({"window_open", "status", "current_window_state", "last_window_id",
    "opened_at", "prediction_level", "prediction_probability_24h", "prediction_updated_at"})
MESSAGES = {
    "invalid_data": "Radar data failed validation; no alert was generated.",
    "unsupported_schema": "Radar schema is unsupported; no alert was generated.",
    "stale_data": "Radar observation is stale; last good cache was preserved.",
    "future_data": "Radar timestamp is in the future; last good cache was preserved.",
    "upstream_error": "Radar reports an error; last good cache was preserved.",
    "network_error": "Radar request failed; last good cache was preserved.",
    "cache_error": "Cache could not be safely read or committed; no alert was generated.",
    "cache_busy": "Another check is running; no alert was generated.",
    "out_of_order": "Radar observation moved backwards; last good cache was preserved.",
    "inconsistent_data": "Radar changed without advancing its timestamp; cache was preserved.",
}


class RadarError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def fail(code="invalid_data"):
    raise RadarError(code)


def object_value(value):
    if not isinstance(value, dict):
        fail()
    return value


def boolean(value):
    if type(value) is not bool:
        fail()
    return value


def enum_value(value, allowed):
    if type(value) is not str or value not in allowed:
        fail()
    return value


def identifier(value):
    if type(value) is not str or not ID_RE.fullmatch(value):
        fail()
    return value


def probability(value):
    if type(value) not in (int, float) or not 0 <= value <= 1 or not math.isfinite(value):
        fail()
    return float(value)


def timestamp(value):
    if type(value) is not str or not TIME_RE.fullmatch(value):
        fail()
    # fromisoformat accepts offsets such as +00:99; RFC3339 does not.
    if value[-1] != "Z" and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
        fail()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, OverflowError):
        fail()


def iso(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def optional_time(value):
    return None if value is None else iso(timestamp(value))


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail()
            result[key] = value
        return result
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda _: fail())
    except (UnicodeError, ValueError, RecursionError, OverflowError):
        fail()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RadarError("network_error")


def fetch_json():
    """Fixed HTTPS source, no redirects, bounded bytes, verified TLS defaults."""
    req = urllib.request.Request(CURRENT_URL, headers={
        "User-Agent": "codex-radar-check/" + VERSION,
        "Accept": "application/json", "Accept-Encoding": "identity",
    })
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=REQUEST_TIMEOUT) as resp:
            if resp.status != 200 or resp.headers.get_content_type() != "application/json":
                fail("network_error")
            if resp.headers.get("Content-Encoding", "identity").lower() != "identity":
                fail("network_error")
            raw = resp.read(MAX_BODY + 1)
            if len(raw) > MAX_BODY:
                fail()
    except RadarError:
        raise
    except (OSError, ValueError, urllib.error.URLError, http.client.HTTPException):
        fail("network_error")
    return strict_json(raw)


def check_flags(data):
    for key in ("ok", "success"):
        if key in data and not boolean(data[key]):
            fail("upstream_error")
    for key in ("stale", "is_stale"):
        if key in data and boolean(data[key]):
            fail("stale_data")
    if data.get("error") not in (None, False, "") or data.get("errors") not in (None, []):
        fail("upstream_error")
    if data.get("status") in ("error", "failed", "unavailable", "degraded"):
        fail("upstream_error")
    if data.get("status") == "stale":
        fail("stale_data")


def normalize(data, now, max_age=MAX_AGE, prediction_max_age=MAX_AGE):
    """Validate every consumed field; ignore unrelated upstream sections entirely."""
    object_value(data)
    check_flags(data)
    schema = data.get("schema_version", "1.0")
    if type(schema) is not str or schema not in ("1.0", "2.0"):
        fail("unsupported_schema")
    if schema == "2.0":
        if data.get("service") != "codex-reset-radar" or data.get("type") != "public_summary":
            fail()
        observed = timestamp(data.get("monitored_at"))
        window = data.get("window")
        state_key = "status"
    else:
        if not ({"current_window", "last_window"} & data.keys()) or "window" in data:
            fail("unsupported_schema" if "schema_version" not in data else "invalid_data")
        observed = timestamp(data.get("checked_at", data.get("monitored_at")))
        window = data.get("current_window")
        state_key = "state"
    age = (now - observed).total_seconds()
    if age < -FUTURE_SKEW:
        fail("future_data")
    if age > max_age:
        fail("stale_data")
    opened = boolean(data.get("window_open"))
    status_value = enum_value(data.get("status"), STATUSES)
    if window is None:
        if opened or (schema == "2.0" and "window" not in data):
            fail()
        window = {}
        window_state = "none"
    else:
        object_value(window)
        check_flags(window)
        window_state = enum_value(window.get(state_key), STATUSES)
    if schema == "2.0" and window:
        if boolean(window.get("open")) != opened:
            fail()
    elif "open" in window and boolean(window["open"]) != opened:
        fail()
    if (opened and window_state in {"none", "closed", "expired", "completed"}) or (
        not opened and window_state in {"open", "active"}
    ):
        fail()
    opened_at = optional_time(window.get("opened_at"))
    closed_at = optional_time(window.get("closed_at"))
    window_id = ""
    for key in ("id", "event_id"):
        if window.get(key) is not None:
            candidate = identifier(window[key])
            if window_id and candidate != window_id:
                fail()
            window_id = candidate
    if schema == "1.0":
        last = data.get("last_window")
        if last is not None:
            object_value(last)
            window_id = identifier(last["id"]) if last.get("id") is not None else window_id
            if opened_at is None and opened:
                opened_at = optional_time(last.get("opened_at"))
    else:
        completion = data.get("completion_observation")
        if completion is not None:
            object_value(completion)
            completion_id = identifier(completion["event_id"]) if completion.get("event_id") is not None else ""
            if not opened and not window_id:
                window_id = completion_id
        # Do not use a previous completion or a changing confirmation URL as an active window ID.
    for value in (opened_at, closed_at):
        if value and (timestamp(value) - now).total_seconds() > FUTURE_SKEW:
            fail("future_data")
    pred = object_value(data.get("prediction"))
    check_flags(pred)
    level = enum_value(pred.get("level"), LEVELS)
    prob = probability(pred.get("probability_24h"))
    if "probability_48h" in pred:
        probability(pred["probability_48h"])
    updated = timestamp(pred["updated_at"]) if "updated_at" in pred else None
    if updated and (updated - now).total_seconds() > FUTURE_SKEW:
        fail("future_data")
    # Legacy feeds without prediction.updated_at can track windows, not fresh predictions.
    fresh_prediction = updated is not None and (now - updated).total_seconds() <= prediction_max_age
    state = {
        "window_open": opened, "status": status_value,
        "current_window_state": window_state, "last_window_id": window_id,
        "opened_at": opened_at, "prediction_level": level if fresh_prediction else None,
        "prediction_probability_24h": prob if fresh_prediction else None,
        "prediction_updated_at": iso(updated) if fresh_prediction else None,
    }
    fingerprint = digest([schema, iso(observed), opened, status_value, window_state,
                          window_id, opened_at, level, prob, iso(updated) if updated else None])
    return {"source_schema": schema, "observed_at": iso(observed), "fingerprint": fingerprint,
            "state": state, "warnings": [] if fresh_prediction else ["prediction_stale_or_undated"]}


def validate_state(state):
    object_value(state)
    if set(state) != STATE_KEYS:
        fail()
    boolean(state["window_open"])
    if (state["window_open"] and state["current_window_state"] in ("none", "closed", "expired", "completed")) or (
        not state["window_open"] and state["current_window_state"] in ("open", "active")
    ):
        fail()
    enum_value(state["status"], STATUSES)
    enum_value(state["current_window_state"], STATUSES)
    if state["last_window_id"] != "":
        identifier(state["last_window_id"])
    optional_time(state["opened_at"])
    if state["prediction_level"] is None:
        if state["prediction_probability_24h"] is not None or state["prediction_updated_at"] is not None:
            fail()
    else:
        enum_value(state["prediction_level"], LEVELS)
        probability(state["prediction_probability_24h"])
        timestamp(state["prediction_updated_at"])


def read_local(path, limit):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_nlink != 1:
            fail("cache_error")
        raw = stream.read(limit + 1)
        if len(raw) > limit:
            fail("cache_error")
    return raw


def load_cache(path):
    try:
        data = strict_json(read_local(path, MAX_CACHE))
        object_value(data)
        if "cache_version" not in data:
            # v1.0.4 flat caches cannot prove schema provenance. Validate and silently rebaseline.
            required = {"window_open", "status", "current_window_state", "last_window_id",
                        "prediction_level", "prediction_probability_24h", "last_checked"}
            if set(data) != required:
                fail()
            boolean(data["window_open"])
            enum_value(data["status"], STATUSES)
            enum_value(data["current_window_state"], STATUSES)
            if data["last_window_id"]:
                identifier(data["last_window_id"])
            elif type(data["last_window_id"]) is not str:
                fail()
            enum_value(data["prediction_level"], LEVELS)
            probability(data["prediction_probability_24h"])
            timestamp(data["last_checked"])
            return {"source_schema": "legacy"}
        if type(data["cache_version"]) is not int or data["cache_version"] != 2:
            fail()
        if set(data) != {"cache_version", "source_schema", "observed_at", "fingerprint",
                         "state", "seen_window_ids", "last_checked"}:
            fail()
        enum_value(data["source_schema"], {"1.0", "2.0"})
        timestamp(data["observed_at"])
        timestamp(data["last_checked"])
        if type(data["fingerprint"]) is not str or not re.fullmatch(r"[a-f0-9]{64}", data["fingerprint"]):
            fail()
        validate_state(data["state"])
        seen = data["seen_window_ids"]
        if type(seen) is not list or len(seen) > MAX_SEEN or any(type(x) is not str for x in seen):
            fail()
        if len(set(seen)) != len(seen):
            fail()
        for value in seen:
            identifier(value)
        if data["state"]["last_window_id"] and data["state"]["last_window_id"] not in seen:
            fail()
        return data
    except FileNotFoundError:
        if path.is_symlink():
            fail("cache_error")
        return None
    except (RadarError, OSError, KeyError, TypeError, ValueError):
        fail("cache_error")


@contextmanager
def cache_lock(path):
    fd = None
    try:
        # Check before mkdir, so a symlink cannot cause directory creation elsewhere.
        # A local account able to rename parent directories is trusted.
        for parent in (path.parent, *path.parent.parents):
            if parent.is_symlink():
                fail("cache_error")
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(str(path) + ".lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_nlink != 1:
            fail("cache_error")
        os.fchmod(fd, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            fail("cache_busy")
        yield
    except OSError:
        fail("cache_error")
    finally:
        if fd is not None:
            os.close(fd)


def save_cache(path, value):
    temp = None
    try:
        # Refuse a symlink or special destination even when creating a first baseline.
        try:
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_nlink != 1:
                fail("cache_error")
        except FileNotFoundError:
            pass
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix="." + path.name + ".", delete=False) as stream:
            temp = stream.name
            json.dump(value, stream, ensure_ascii=False, allow_nan=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        temp = None
        # Replacement is already committed. Report a durability warning, never a false rollback.
        try:
            directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        except OSError:
            return ["directory_sync_unavailable"]
        return []
    except OSError:
        fail("cache_error")
    finally:
        if temp is not None:
            try:
                os.unlink(temp)
            except FileNotFoundError:
                pass


def compare(prev, curr, seen, observed_at):
    events = []
    def event(kind, detail, **extra):
        value = {"type": kind, "detail": detail, **extra}
        value["event_id"] = digest([observed_at, value])
        events.append(value)
    if prev["window_open"] != curr["window_open"]:
        if curr["window_open"]:
            event("window_opened", "Codex 用量重置窗口已开启", opened_at=curr["opened_at"], scope="Codex 用户")
        else:
            event("window_closed", "Codex 用量重置窗口已关闭")
    for key, kind, label in (("status", "status_change", "状态"),
                             ("current_window_state", "current_window_state_change", "当前窗口状态")):
        if prev[key] != curr[key]:
            event(kind, f"{label}发生变化", **{"from": prev[key], "to": curr[key]})
    new_id = curr["last_window_id"]
    if new_id and new_id not in seen:
        event("new_window", "检测到新的重置事件", window_id=new_id, previous_window_id=prev["last_window_id"])
    # Each fresh prediction segment starts with a baseline; no stale-to-fresh jump alert.
    if prev["prediction_level"] is not None and curr["prediction_level"] is not None:
        if prev["prediction_level"] != curr["prediction_level"]:
            event("prediction_change", "预测等级发生变化", **{"from": prev["prediction_level"], "to": curr["prediction_level"]})
        old, new = prev["prediction_probability_24h"], curr["prediction_probability_24h"]
        if abs(Decimal(str(new)) - Decimal(str(old))) >= PROB_THRESHOLD:
            event("prediction_probability_change", "24h 预测概率变化至少 10 个百分点",
                  **{"from": old, "to": new, "probability_24h": new})
    return events


def render_notification(events):
    """Only local fixed labels and validated numbers/enums; never upstream prose/URLs."""
    lines = ["Codex Reset Radar："]
    for event in events:
        kind = event["type"]
        line = event["detail"]
        if kind in {"status_change", "current_window_state_change", "prediction_change"}:
            line += "（" + event["from"] + " → " + event["to"] + "）"
        elif kind == "prediction_probability_change":
            line += "（" + f'{event["from"]:.0%} → {event["to"]:.0%}' + "）"
        lines.append("- " + line)
    lines.append("数据来自 Codex 雷达 codexradar.com；社区监测不代表你的账号已重置。")
    return "\n".join(lines)


def process(data, path, now, max_age=MAX_AGE, prediction_max_age=MAX_AGE):
    curr = normalize(data, now, max_age, prediction_max_age)
    prev = load_cache(path)
    baseline = prev is None or prev["source_schema"] != curr["source_schema"]
    if prev and prev["source_schema"] != "legacy":
        old_time, new_time = timestamp(prev["observed_at"]), timestamp(curr["observed_at"])
        if new_time < old_time:
            fail("out_of_order")
        if not baseline and new_time == old_time and curr["fingerprint"] != prev["fingerprint"]:
            fail("inconsistent_data")
        if not baseline:
            old_pred, new_pred = prev["state"], curr["state"]
            old_update, new_update = old_pred["prediction_updated_at"], new_pred["prediction_updated_at"]
            if old_update and new_update:
                if timestamp(new_update) < timestamp(old_update):
                    fail("out_of_order")
                if new_update == old_update and any(old_pred[key] != new_pred[key] for key in (
                    "prediction_level", "prediction_probability_24h"
                )):
                    fail("inconsistent_data")
    seen = list(prev.get("seen_window_ids", [])) if prev else []
    events = [] if baseline else compare(prev["state"], curr["state"], seen, curr["observed_at"])
    current_id = curr["state"]["last_window_id"]
    if current_id:
        seen = [value for value in seen if value != current_id] + [current_id]
    cache = {key: curr[key] for key in ("source_schema", "observed_at", "fingerprint", "state")}
    cache.update(cache_version=2, seen_window_ids=seen[-MAX_SEEN:], last_checked=iso(now))
    warnings = curr["warnings"] + save_cache(path, cache)
    output_status = dict(curr["state"])
    output_status["probability_24h"] = output_status["prediction_probability_24h"]
    result = {"ok": True, "has_changes": bool(events), "events": events,
              "observed_at": curr["observed_at"], "current_status": output_status,
              "warnings": warnings, "notification": render_notification(events) if events else None}
    if baseline:
        result["message"] = "baseline_created" if prev is None else "baseline_migrated"
    return result


def age_argument(value):
    parsed = int(value)
    if not 60 <= parsed <= 7 * 24 * 3600:
        raise argparse.ArgumentTypeError("age must be between 60 and 604800 seconds")
    return parsed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, help="override local cache path")
    parser.add_argument("--input", type=Path, help="offline JSON file; requires an explicit --cache")
    parser.add_argument("--now", help="offline RFC3339 clock; requires --input")
    parser.add_argument("--max-age-seconds", type=age_argument, default=MAX_AGE)
    parser.add_argument("--prediction-max-age-seconds", type=age_argument, default=MAX_AGE)
    args = parser.parse_args(argv)
    if args.input and args.cache is None:
        parser.error("--input requires --cache to protect the live baseline")
    if args.now and not args.input:
        parser.error("--now requires --input")
    try:
        now = timestamp(args.now) if args.now else datetime.now(timezone.utc)
        path = (args.cache or CACHE_PATH).expanduser().absolute()
        with cache_lock(path):
            if args.input:
                try:
                    raw = read_local(args.input, MAX_BODY)
                except OSError:
                    fail()
                data = strict_json(raw)
            else:
                data = fetch_json()
            result = process(data, path, now, args.max_age_seconds, args.prediction_max_age_seconds)
        code = 0
    except RadarError as exc:
        result = {"ok": False, "has_changes": False, "events": [], "notification": None,
                  "error": {"code": exc.code, "message": MESSAGES[exc.code]}}
        code = 1
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
