#!/usr/bin/env python3
"""Read morning context from Fulcra and write a subjective check-in back as annotations.

Two subcommands:

  context   Read last night's sleep summary and today's calendar event count.
  save      Write the check-in: a "Morning Check-In" moment annotation that holds
            the full structured record in its note, plus scale annotations for the
            quantifiable dimensions (energy, mood, social battery) so they become
            trackable time series alongside objective health data.

The write path mirrors the proven Fulcra ingest flow: ensure the annotation
definition exists (POST /user/v1alpha1/annotation), record the value
(POST /ingest/v1/record), then read it back to confirm it landed. A 204 from
ingest alone is NOT proof of success -- only a readback match is.

Auth: the script never handles credentials directly. It reads a bearer token from
the FULCRA_ACCESS_TOKEN env var, or by shelling out to the Fulcra CLI
(`uv tool run fulcra-api auth print-access-token`, overridable via FULCRA_CLI_COMMAND).
Stdlib only -- no third-party imports -- so it runs under any Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

API_BASE = os.environ.get("FULCRA_API_BASE", "https://api.fulcradynamics.com").rstrip("/")
AGENT_SOURCE = os.environ.get("FULCRA_AGENT_SOURCE", "com.fulcradynamics.subjective-checkin")
CLI_COMMAND = os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api")
DEFAULT_HOME = os.environ.get("FULCRA_HOME") or os.environ.get("HOME") or os.path.expanduser("~")

# overall_feeling word -> 1..5 (rough..great). Used for the "Morning Mood" scale.
FEELING_TO_SCORE = {"rough": 1, "low": 2, "okay": 3, "good": 4, "great": 5}
# social battery word -> 1..3 (low..high).
SOCIAL_TO_SCORE = {"low": 1, "medium": 2, "high": 3}

# The annotation definitions this skill manages. Created once, on demand.
DEFS: dict[str, dict[str, Any]] = {
    "checkin": {
        "name": "Morning Check-In",
        "type": "moment",
        "description": "Daily subjective morning check-in. Full structured record is stored in the note.",
        "tags": ["checkin", "subjective"],
    },
    "energy": {
        "name": "Morning Energy",
        "type": "scale",
        "description": "Self-reported morning energy level (1 = depleted, 10 = peak).",
        "scale_min": 1,
        "scale_max": 10,
        "labels": {1: "Depleted", 3: "Low", 5: "Steady", 7: "Good", 10: "Peak"},
        "tags": ["checkin", "energy"],
    },
    "mood": {
        "name": "Morning Mood",
        "type": "scale",
        "description": "Self-reported morning mood.",
        "scale_min": 1,
        "scale_max": 5,
        "labels": {1: "Rough", 2: "Low", 3: "Okay", 4: "Good", 5: "Great"},
        "tags": ["checkin", "mood"],
    },
    "social": {
        "name": "Social Battery",
        "type": "scale",
        "description": "Self-reported social battery / appetite for people today.",
        "scale_min": 1,
        "scale_max": 3,
        "labels": {1: "Low", 2: "Medium", 3: "High"},
        "tags": ["checkin", "social"],
    },
}

TYPE_TO_DATA_TYPE = {"moment": "MomentAnnotation", "scale": "ScaleAnnotation"}
TYPE_TO_READ_CLASS = {"moment": "event", "scale": "metric"}


def fail(message: str, code: int = 1) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


# --------------------------------------------------------------------------- auth + HTTP

_token_cache: str | None = None


def access_token() -> str:
    global _token_cache
    if _token_cache:
        return _token_cache
    env_token = os.environ.get("FULCRA_ACCESS_TOKEN")
    if env_token:
        _token_cache = env_token.strip()
        return _token_cache
    env = os.environ.copy()
    env["HOME"] = DEFAULT_HOME
    env.setdefault("PYTHONUTF8", "1")
    cmd = [*shlex.split(CLI_COMMAND, posix=(os.name != "nt")), "auth", "print-access-token"]
    try:
        token = subprocess.check_output(
            cmd, env=env, text=True, stderr=subprocess.DEVNULL, timeout=60
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        fail(
            "Could not get a Fulcra access token. Set FULCRA_ACCESS_TOKEN, or make the "
            f"Fulcra CLI runnable (`{CLI_COMMAND} auth login`). Underlying error: {exc}"
        )
    if not token:
        fail("Fulcra CLI returned an empty access token. Run `auth login` again.")
    _token_cache = token
    return token


def request(method: str, path: str, payload: Any | None = None) -> tuple[int, str]:
    headers = {"Authorization": f"Bearer {access_token()}"}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API_BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = resp.read()
            return resp.status, body.decode() if body else ""
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        return exc.code, body
    except urllib.error.URLError as exc:
        fail(f"Network error contacting Fulcra at {API_BASE}{path}: {exc}")


# --------------------------------------------------------------------------- tags + defs

def is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def get_tag_by_name(name: str) -> dict[str, Any] | None:
    status, body = request("GET", f"/user/v1alpha1/tag/name/{urllib.parse.quote(name, safe='')}")
    if status == 200:
        return json.loads(body)
    if status == 404:
        return None
    fail(f"Failed to look up tag {name!r}: HTTP {status}: {body[:300]}")


def create_tag(name: str) -> dict[str, Any]:
    status, body = request("POST", "/user/v1alpha1/tag", {"name": name})
    if status in {200, 201} and body:
        return json.loads(body)
    if status in {200, 201, 303}:
        tag = get_tag_by_name(name)
        if tag:
            return tag
    fail(f"Failed to create tag {name!r}: HTTP {status}: {body[:300]}")


def resolve_tags(raw_tags: list[str]) -> list[str]:
    resolved: list[str] = []
    for raw in raw_tags or []:
        tag = raw.strip()
        if not tag:
            continue
        if is_uuid(tag):
            resolved.append(str(uuid.UUID(tag)))
            continue
        found = get_tag_by_name(tag) or create_tag(tag)
        resolved.append(found["id"])
    return resolved


def list_annotations() -> list[dict[str, Any]]:
    status, body = request("GET", "/user/v1alpha1/annotation")
    if status != 200:
        fail(f"Failed to list annotations: HTTP {status}: {body[:300]}")
    return [a for a in json.loads(body) if not a.get("deleted_at")]


def source_id_of(annotation: dict[str, Any]) -> str:
    return annotation.get("fulcra_source_id") or f"com.fulcradynamics.annotation.{annotation['id']}"


def build_definition_payload(spec: dict[str, Any], tags: list[str]) -> dict[str, Any]:
    base: dict[str, Any] = {
        "annotation_type": spec["type"],
        "name": spec["name"],
        "description": spec.get("description", ""),
        "tags": tags,
    }
    if spec["type"] == "moment":
        base["measurement_spec"] = None
        base["spec"] = None
    elif spec["type"] == "scale":
        low, high = int(spec["scale_min"]), int(spec["scale_max"])
        default = (low + high) // 2
        labels = {str(k): str(v) for k, v in spec.get("labels", {}).items()}
        for i in range(low, high + 1):
            labels.setdefault(str(i), str(i))
        base["measurement_spec"] = {
            "measurement_type": "scale",
            "value_type": "integer",
            "unit": None,
            "scale": {"min_allowed": low, "max_allowed": high, "value": default},
        }
        base["spec"] = {
            "default_note": None,
            "scale": {
                "label_mapping": {"mapping_type": "string", "string": {"mapping": labels}},
                "scale_mapping": None,
            },
        }
    else:
        fail(f"Unsupported annotation type {spec['type']!r}")
    return base


def ensure_definition(spec: dict[str, Any], existing: list[dict[str, Any]], dry_run: bool) -> dict[str, Any]:
    target = spec["name"].strip().lower()
    matches = [a for a in existing if a.get("name", "").strip().lower() == target]
    if matches:
        # Deterministic pick (oldest by created_at) so repeated runs -- including
        # across multiple machines -- converge on one definition instead of each run
        # adopting a different duplicate. Mirrors fulcra-common's resolve_definition_id.
        matches.sort(key=lambda d: (d.get("created_at") is None, d.get("created_at", ""), d.get("id", "")))
        return matches[0]
    if dry_run:
        # No API calls: show raw tag names rather than resolving (which would create them).
        payload = build_definition_payload(spec, tags=list(spec.get("tags", [])))
        return {"id": "(dry-run)", "name": spec["name"], "annotation_type": spec["type"], "tags": [], "_payload": payload}
    payload = build_definition_payload(spec, tags=resolve_tags(spec.get("tags", [])))
    status, body = request("POST", "/user/v1alpha1/annotation", payload)
    if status != 200:
        fail(f"Failed to create annotation {spec['name']!r}: HTTP {status}: {body[:500]}")
    created = json.loads(body)
    existing.append(created)
    return created


# --------------------------------------------------------------------------- recording

def record(annotation: dict[str, Any], recorded_at: str, note: str | None, value: int | None, dry_run: bool) -> dict[str, Any]:
    ann_type = annotation["annotation_type"]
    data_type = TYPE_TO_DATA_TYPE[ann_type]
    data: dict[str, Any] = {}
    if note:
        data["note"] = note
    if value is not None:
        data["value"] = int(value)
    payload = {
        "specversion": 1,
        "data": json.dumps(data, sort_keys=True),
        "metadata": {
            "data_type": data_type,
            "recorded_at": recorded_at,
            "source": [AGENT_SOURCE, source_id_of(annotation)],
            "tags": annotation.get("tags") or [],
            "content_type": "application/json",
        },
    }
    if dry_run:
        return {"name": annotation["name"], "dry_run": True, "payload": payload}
    status, body = request("POST", "/ingest/v1/record", payload)
    if status != 204:
        fail(f"Failed to record {annotation['name']!r}: HTTP {status}: {body[:500]}")
    return {
        "name": annotation["name"],
        "recorded_at": recorded_at,
        "verified_matches": verify(annotation, recorded_at),
    }


def verify(annotation: dict[str, Any], recorded_at: str, attempts: int = 5, delay: float = 2.0) -> int:
    """Confirm a written record is readable. Ingest is eventually consistent: a record
    accepted by /ingest/v1/record is not queryable for a second or two, so poll with a
    short backoff rather than checking once. Returns the number of matching records."""
    ann_type = annotation["annotation_type"]
    data_type = TYPE_TO_DATA_TYPE[ann_type]
    read_class = TYPE_TO_READ_CLASS[ann_type]
    center = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
    query = urllib.parse.urlencode(
        {
            "start_time": (center - timedelta(minutes=5)).isoformat(),
            "end_time": (center + timedelta(minutes=5)).isoformat(),
        }
    )
    path = f"/data/v1alpha1/{read_class}/{data_type}?{query}"
    sid = source_id_of(annotation)
    for attempt in range(attempts):
        status, body = request("GET", path)
        if status == 200:
            try:
                records = json.loads(body)
            except json.JSONDecodeError:
                records = []
            matches = sum(
                1 for item in records
                if isinstance(item, dict)
                and (item.get("source_id") == sid or sid in (item.get("sources") or []))
            )
            if matches:
                return matches
        if attempt < attempts - 1:
            time.sleep(delay)
    return 0


# --------------------------------------------------------------------------- read context

def run_cli(args: list[str]) -> tuple[int, str]:
    env = os.environ.copy()
    env["HOME"] = DEFAULT_HOME
    env.setdefault("PYTHONUTF8", "1")
    cmd = [*shlex.split(CLI_COMMAND, posix=(os.name != "nt")), *args]
    try:
        proc = subprocess.run(cmd, env=env, text=True, capture_output=True, timeout=120)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, f"CLI invocation failed: {exc}"
    if proc.returncode != 0:
        return proc.returncode, (proc.stderr or proc.stdout or "").strip()
    return 0, proc.stdout


def parse_records(raw: str) -> list[Any]:
    """Fulcra CLI commands emit NDJSON (one JSON object per line). Tolerate a plain
    JSON array or a {"data": [...]} envelope too, so this keeps working if a command
    formats its output differently."""
    raw = (raw or "").strip()
    if not raw:
        return []
    try:
        val = json.loads(raw)
        if isinstance(val, list):
            return val
        if isinstance(val, dict):
            return val["data"] if isinstance(val.get("data"), list) else [val]
    except json.JSONDecodeError:
        pass
    rows: list[Any] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def context(args: argparse.Namespace) -> dict[str, Any]:
    now = datetime.now().astimezone()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    out: dict[str, Any] = {"ok": True, "as_of": now.isoformat(), "sleep": None, "calendar": None}

    # Sleep: read raw SleepStage samples over a wide window and summarize the most
    # recent night. A wide lookback + "pick the last session" is robust to whatever
    # time of day the check-in runs and to sync delays.
    rc, body = run_cli(["get-records", "SleepStage", (now - timedelta(hours=30)).isoformat(), now.isoformat()])
    out["sleep"] = {"available": False, "reason": body[:300]} if rc != 0 else summarize_sleep(body)

    # Calendar: count *today's* events specifically, in local time.
    rc, body = run_cli(["calendar-events", day_start.isoformat(), day_end.isoformat()])
    out["calendar"] = {"available": False, "reason": body[:300]} if rc != 0 else summarize_calendar(body)
    return out


# Authoritative SleepStage values (Fulcra catalog + fulcra-context sleep utils):
# 0 = in bed, 1 = asleep (unspecified), 2 = awake, 3 = core/light, 4 = deep, 5 = REM.
# Time asleep = stages 3 + 4 + 5; stage 2 is awake-in-bed.
SLEEP_STAGE_NAMES = {2: "awake", 3: "core", 4: "deep", 5: "rem"}


def _parse_dt(ts: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except (ValueError, AttributeError, TypeError):
        return None


def _field(sample: dict[str, Any], *names: str) -> Any:
    for n in names:
        if sample.get(n) is not None:
            return sample[n]
    return None


def summarize_sleep(raw: str) -> dict[str, Any]:
    """Summarize the most recent night from raw SleepStage samples. Mirrors the math in
    the official fulcra-context sleep utility: group samples into sessions (gaps > 60 min
    split a session), take the latest session, sum stage minutes, and derive hours asleep
    plus deep/REM percentages and a coarse quality label."""
    samples: list[tuple[datetime, datetime, int]] = []
    for r in parse_records(raw):
        if not isinstance(r, dict):
            continue
        sd = _parse_dt(_field(r, "start_date", "start_time", "start", "time"))
        ed = _parse_dt(_field(r, "end_date", "end_time", "end"))
        val = _field(r, "value", "sleep_stage")
        if sd and ed and val is not None:
            try:
                samples.append((sd, ed, int(val)))
            except (TypeError, ValueError):
                continue
    if not samples:
        return {"available": False, "reason": "No sleep stage data in the last ~30h."}

    samples.sort(key=lambda s: s[0])
    sessions: list[list[tuple[datetime, datetime, int]]] = [[samples[0]]]
    for s in samples[1:]:
        if (s[0] - sessions[-1][-1][1]).total_seconds() / 60 > 60:
            sessions.append([s])
        else:
            sessions[-1].append(s)
    session = sessions[-1]

    stage_min: dict[int, float] = {}
    s_start = s_end = None
    for sd, ed, val in session:
        if val in SLEEP_STAGE_NAMES:
            stage_min[val] = stage_min.get(val, 0.0) + (ed - sd).total_seconds() / 60
        s_start = sd if s_start is None or sd < s_start else s_start
        s_end = ed if s_end is None or ed > s_end else s_end

    asleep = stage_min.get(3, 0) + stage_min.get(4, 0) + stage_min.get(5, 0)
    awake = stage_min.get(2, 0)
    in_bed = asleep + awake
    if asleep < 30:
        return {"available": False, "reason": "Most recent sleep session too short to summarize."}
    deep_pct = round(stage_min.get(4, 0) / asleep * 100, 1)
    rem_pct = round(stage_min.get(5, 0) / asleep * 100, 1)
    if asleep < 360:
        quality = "poor"
    elif deep_pct < 10 or rem_pct < 15:
        quality = "fair"
    elif asleep >= 420 and deep_pct >= 15 and rem_pct >= 20:
        quality = "excellent"
    else:
        quality = "good"
    return {
        "available": True,
        "total_hours": round(asleep / 60, 1),
        "asleep_minutes": round(asleep),
        "stages_minutes": {SLEEP_STAGE_NAMES[k]: round(v) for k, v in stage_min.items()},
        "deep_pct": deep_pct,
        "rem_pct": rem_pct,
        "efficiency_pct": round(asleep / in_bed * 100, 1) if in_bed else None,
        "quality": quality,
        "bedtime": s_start.isoformat() if s_start else None,
        "wake": s_end.isoformat() if s_end else None,
    }


def summarize_calendar(raw: str) -> dict[str, Any]:
    rows = parse_records(raw)
    titles = []
    for e in rows:
        if isinstance(e, dict):
            titles.append(e.get("title") or e.get("summary") or e.get("name") or "(untitled)")
    return {"available": True, "event_count": len(rows), "titles": titles[:12]}


# --------------------------------------------------------------------------- save

def save(args: argparse.Namespace) -> dict[str, Any]:
    recorded_at = args.recorded_at or datetime.now(timezone.utc).isoformat()
    feeling = (args.overall_feeling or "").strip()
    social = (args.social_battery or "").strip().lower()

    full_record = {
        "timestamp": recorded_at,
        "overall_feeling": feeling or None,
        "energy_level": args.energy_level,
        "energy_words": args.energy_words or None,
        "social_battery": social or None,
        "physical_notes": args.physical_notes or None,
        "daily_intention": args.daily_intention or None,
        "sleep_score_objective": args.sleep_objective,
        "sleep_score_subjective": args.sleep_subjective or None,
    }

    try:
        existing = list_annotations()
    except SystemExit:
        if not args.dry_run:
            raise
        existing = []  # offline dry-run: pretend nothing exists so we show full payloads

    results: list[dict[str, Any]] = []

    # 1) Canonical moment annotation: full structured record in the note.
    checkin_def = ensure_definition(DEFS["checkin"], existing, args.dry_run)
    results.append(record(checkin_def, recorded_at, note=json.dumps(full_record), value=None, dry_run=args.dry_run))

    # 2) Energy scale (1-10).
    if args.energy_level is not None:
        energy_def = ensure_definition(DEFS["energy"], existing, args.dry_run)
        val = max(1, min(10, int(args.energy_level)))
        results.append(record(energy_def, recorded_at, note=args.energy_words or None, value=val, dry_run=args.dry_run))

    # 3) Mood scale (1-5) derived from overall_feeling.
    mood_score = FEELING_TO_SCORE.get(feeling.lower())
    if mood_score is not None:
        mood_def = ensure_definition(DEFS["mood"], existing, args.dry_run)
        results.append(record(mood_def, recorded_at, note=feeling, value=mood_score, dry_run=args.dry_run))

    # 4) Social battery scale (1-3).
    social_score = SOCIAL_TO_SCORE.get(social)
    if social_score is not None:
        social_def = ensure_definition(DEFS["social"], existing, args.dry_run)
        results.append(record(social_def, recorded_at, note=None, value=social_score, dry_run=args.dry_run))

    confirmed = [r for r in results if not args.dry_run and r.get("verified_matches", 0) >= 1]
    return {
        "ok": True,
        "dry_run": args.dry_run,
        "recorded_at": recorded_at,
        "record": full_record,
        "writes": results,
        "confirmed_count": len(confirmed),
        "total_writes": len(results),
    }


# --------------------------------------------------------------------------- cli

def main() -> int:
    parser = argparse.ArgumentParser(description="Fulcra subjective morning check-in")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("context", help="Read last night's sleep + today's calendar count")

    s = sub.add_parser("save", help="Write the check-in to Fulcra")
    s.add_argument("--overall-feeling", help="great|good|okay|low|rough (free text also stored)")
    s.add_argument("--energy-level", type=int, help="1-10")
    s.add_argument("--energy-words", help="A few words about energy")
    s.add_argument("--social-battery", help="high|medium|low")
    s.add_argument("--physical-notes", help="Headache, sore, coming down with something, etc.")
    s.add_argument("--daily-intention", help="Something to accomplish beyond the calendar")
    s.add_argument("--sleep-objective", type=float, help="Objective sleep number (e.g. hours asleep or device score)")
    s.add_argument("--sleep-subjective", help="How they say they actually slept")
    s.add_argument("--recorded-at", help="ISO-8601 timestamp with offset; defaults to now (UTC)")
    s.add_argument("--dry-run", action="store_true", help="Build payloads and print them without writing")

    args = parser.parse_args()
    if args.command == "context":
        result = context(args)
    elif args.command == "save":
        result = save(args)
    else:
        fail("unknown command")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
