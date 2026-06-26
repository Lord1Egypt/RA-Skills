#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from daily_strava_roast.context_builder import build_roast_context
from daily_strava_roast.prompt_builder import build_roast_prompt
from daily_strava_roast.strava_config import config_status, load_strava_app_config, missing_config_requirements
from daily_strava_roast.writer import write_roast_preview

DEFAULT_STATE_FILE = Path.home() / ".openclaw" / "workspace" / "daily-strava-roast" / "state" / "recent_roasts.json"
DEFAULT_REAUTH_SCRIPT = Path.home() / ".openclaw" / "workspace" / "agents" / "tars-fit" / "strava_auth.py"


class StravaAuthError(RuntimeError):
    pass


class StravaDataUnavailableError(RuntimeError):
    pass


class StravaInitialSetupRequiredError(StravaAuthError):
    pass


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a daily Strava roast from recent activity.")
    p.add_argument("command", choices=["summary", "roast", "context", "prompt", "preview", "auth-url"], nargs="?", default="roast")
    p.add_argument("--config-file", default=None, help="Path to secure Strava app config JSON")
    p.add_argument("--days", type=int, default=2, help="Look back N days for recent activity")
    p.add_argument("--limit", type=int, default=6, help="Max activities to fetch")
    p.add_argument("--tone", choices=["dry", "playful", "savage", "coach"], default="playful")
    p.add_argument("--spice", type=int, choices=[0, 1, 2, 3], default=3, help="Roast intensity from 0 (gentle) to 3 (scorched)")
    p.add_argument("--state-file", default=str(DEFAULT_STATE_FILE), help="Path to roast memory state file")
    p.add_argument("--target-date", default=None, help="Local date to roast in YYYY-MM-DD format (defaults to today in Australia/Sydney)")
    p.add_argument("--reauth-script", default=str(DEFAULT_REAUTH_SCRIPT), help="Path to Strava reauth helper script")
    p.add_argument("--json", action="store_true")
    p.add_argument("--pretty", action="store_true")
    return p


def load_tokens(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise StravaInitialSetupRequiredError(
            f"Strava token file not found at {path}. Initial Strava setup is required."
        ) from exc
    except json.JSONDecodeError as exc:
        raise StravaInitialSetupRequiredError(
            f"Strava token file at {path} is invalid JSON. Re-run initial Strava setup."
        ) from exc


def save_tokens(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"recent": []}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {"recent": []}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n")


def record_roast_state(path: Path, day: dict[str, Any], tone: str, spice: int, roast: str, *, metadata: dict[str, Any] | None = None) -> None:
    state = load_state(path)
    recent = state.get("recent")
    if not isinstance(recent, list):
        recent = []

    summaries = day.get("summaries", [])
    sport_labels = [str(s.get("sport")) for s in summaries if s.get("sport")]
    activity_names = [str(s.get("name")) for s in summaries if s.get("name")]
    dominant_sport = None
    if summaries:
        first = summaries[0].get("sport")
        if isinstance(first, str):
            dominant_sport = first.lower()

    entry: dict[str, Any] = {
        "at": datetime.now(ZoneInfo("UTC")).isoformat(),
        "date": day.get("date"),
        "sports": sport_labels,
        "count": int(day.get("count", 0) or 0),
        "tone": tone,
        "spice": spice,
        "distance_km": float(day.get("total_km", 0) or 0),
        "moving_minutes": int(day.get("total_min", 0) or 0),
        "elevation_m": int(day.get("total_elev", 0) or 0),
        "kudos": int(day.get("total_kudos", 0) or 0),
        "activity_names": activity_names,
        "dominant_sport": dominant_sport,
        "roast": roast,
    }
    if metadata:
        for key, value in metadata.items():
            entry[key] = value

    recent.append(entry)
    state["recent"] = recent[-14:]
    save_state(path, state)


def reauth_available(reauth_script: Path, config: dict[str, Any]) -> bool:
    return reauth_script.exists() and not missing_config_requirements(config)


def get_reauth_url(reauth_script: Path) -> str:
    result = subprocess.run(["python3", str(reauth_script)], capture_output=True, text=True, timeout=30, check=False)
    if result.returncode != 0:
        raise StravaAuthError((result.stderr or result.stdout).strip() or "Failed to generate Strava reauth URL")
    return result.stdout.strip()


def validate_token_shape(tokens: dict[str, Any], path: Path) -> None:
    required = ["access_token", "refresh_token", "expires_at"]
    missing = [key for key in required if key not in tokens or tokens.get(key) in (None, "")]
    if missing:
        raise StravaInitialSetupRequiredError(
            f"Strava token file at {path} is missing required field(s): {', '.join(missing)}. Initial Strava setup is required."
        )


def refresh_tokens(tokens: dict[str, Any], path: Path, client_id: str, client_secret: str | None, *, force: bool = False) -> dict[str, Any]:
    validate_token_shape(tokens, path)
    if not force and tokens.get("expires_at", 0) > int(time.time()) + 300:
        return tokens
    if not client_secret:
        raise StravaAuthError("Strava client_secret is not configured")
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
    }).encode()
    req = urllib.request.Request("https://www.strava.com/oauth/token", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            fresh = json.load(r)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        raise StravaAuthError(f"Strava token refresh failed ({exc.code}): {body or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise StravaDataUnavailableError(f"Strava token refresh unavailable: {exc.reason}") from exc
    validate_token_shape(fresh, path)
    save_tokens(path, fresh)
    return fresh


def fetch_activities(tokens: dict[str, Any], days: int, limit: int) -> list[dict[str, Any]]:
    after = int(time.time()) - days * 86400
    query = urllib.parse.urlencode({"after": after, "per_page": limit, "page": 1})
    req = urllib.request.Request(
        f"https://www.strava.com/api/v3/athlete/activities?{query}",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        if exc.code == 401:
            raise StravaAuthError(f"Strava activity fetch failed with 401: {body or exc.reason}") from exc
        raise StravaDataUnavailableError(f"Strava activity fetch failed ({exc.code}): {body or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise StravaDataUnavailableError(f"Strava activity fetch unavailable: {exc.reason}") from exc


def build_recovery_payload(config: dict[str, Any], reauth_script: Path, error: Exception, *, status: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": status,
        "error": str(error),
        "config_path": config["config_path"],
        "config_present": config["config_present"],
        "config_status": config_status(config),
        "missing_requirements": missing_config_requirements(config),
        "token_file": config["token_file"],
        "reauth_script": str(reauth_script),
        "reauth_available": reauth_available(reauth_script, config),
    }
    if payload["reauth_available"]:
        payload["auth_url"] = get_reauth_url(reauth_script)
    else:
        payload["auth_url"] = None
    return payload


def fetch_activities_with_recovery(config: dict[str, Any], days: int, limit: int, reauth_script: Path) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    token_file = Path(config["token_file"]).expanduser()
    recovery: dict[str, Any] | None = None
    tokens = load_tokens(token_file)

    try:
        tokens = refresh_tokens(tokens, token_file, config["client_id"], config["client_secret"])
    except StravaInitialSetupRequiredError as exc:
        recovery = build_recovery_payload(config, reauth_script, exc, status="initial_setup_required")
        raise
    except StravaAuthError as exc:
        if missing_config_requirements(config):
            recovery = build_recovery_payload(config, reauth_script, exc, status="config_incomplete")
        raise

    try:
        return fetch_activities(tokens, days, limit), recovery
    except StravaAuthError as first_auth_error:
        try:
            refreshed = refresh_tokens(tokens, token_file, config["client_id"], config["client_secret"], force=True)
            return fetch_activities(refreshed, days, limit), recovery
        except StravaInitialSetupRequiredError as exc:
            recovery = build_recovery_payload(config, reauth_script, exc, status="initial_setup_required")
            raise
        except StravaAuthError:
            recovery = build_recovery_payload(config, reauth_script, first_auth_error, status="reauth_required")
            raise StravaAuthError(str(first_auth_error)) from first_auth_error


def km(distance_m: float | None) -> float:
    return round((distance_m or 0.0) / 1000.0, 2)


def minutes(seconds: int | None) -> int:
    return round((seconds or 0) / 60)


def summarize_activity(a: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": a.get("name") or "Unnamed suffering",
        "sport": a.get("sport_type") or a.get("type") or "Activity",
        "distance_km": km(a.get("distance")),
        "moving_min": minutes(a.get("moving_time")),
        "elapsed_min": minutes(a.get("elapsed_time")),
        "elev_m": round(a.get("total_elevation_gain") or 0),
        "kudos": a.get("kudos_count") or 0,
        "avg_hr": round(a.get("average_heartrate") or 0) or None,
        "max_hr": round(a.get("max_heartrate") or 0) or None,
        "avg_watts": round(a.get("average_watts") or 0) or None,
        "suffer": a.get("suffer_score"),
        "date_local": a.get("start_date_local"),
        "trainer": bool(a.get("trainer")),
    }


def date_key(summary: dict[str, Any]) -> str:
    return (summary.get("date_local") or "")[:10]


def aggregate_day(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "date": date_key(summaries[0]) if summaries else None,
        "count": len(summaries),
        "names": [s["name"] for s in summaries],
        "sports": [s["sport"] for s in summaries],
        "total_km": round(sum(s["distance_km"] for s in summaries), 2),
        "total_min": sum(s["moving_min"] for s in summaries),
        "total_elev": sum(s["elev_m"] for s in summaries),
        "total_kudos": sum(s["kudos"] for s in summaries),
        "indoor_count": sum(1 for s in summaries if s["trainer"]),
        "summaries": summaries,
    }


def build_daily_payload(activities: list[dict[str, Any]]) -> dict[str, Any]:
    summaries = [summarize_activity(a) for a in activities]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for summary in summaries:
        grouped[date_key(summary)].append(summary)
    days = [{"date": key, "activities": items, "rollup": aggregate_day(items)} for key, items in sorted(grouped.items(), reverse=True)]
    return {"activity_count": len(summaries), "days": days}


def resolve_target_date(target_date: str | None) -> str:
    if target_date:
        return target_date
    return datetime.now(ZoneInfo("Australia/Sydney")).date().isoformat()


def select_target_day(daily: dict[str, Any], target_date: str) -> dict[str, Any] | None:
    for day in daily.get("days", []):
        if day.get("date") == target_date:
            return day.get("rollup")
    return None


def build_empty_day(target_date: str) -> dict[str, Any]:
    return {"date": target_date, "count": 0, "names": [], "sports": [], "total_km": 0.0, "total_min": 0, "total_elev": 0, "total_kudos": 0, "indoor_count": 0, "summaries": []}


def find_last_activity(activities: list[dict[str, Any]], target_date: str) -> dict[str, Any] | None:
    summaries = [summarize_activity(a) for a in activities]
    for summary in summaries:
        if date_key(summary) < target_date:
            return summary
    return summaries[0] if summaries else None


def line_for_run(s: dict[str, Any], tone: str, spice: int) -> str:
    base = f"{s['name']}: {s['distance_km']} km in {s['moving_min']} min"
    if tone == 'coach': return base + ". Useful work. Now try to recover like someone who plans to run again this century."
    if tone == 'dry': return base + ". A concise little appointment with gravity and self-imposed inconvenience."
    if spice >= 3: return base + f" with {s['elev_m']} m climbing. Remarkable commitment to making your own life harder on purpose."
    if spice == 2: return base + ". Efficient, uncomfortable, and exactly the kind of idea your legs will remember tomorrow."
    if spice == 1: return base + f" with {s['kudos']} kudos. Cardio, but make it publicly auditable."
    return base + ". Nice work. Mildly heroic, acceptably unhinged."


def line_for_tennis(s: dict[str, Any], tone: str, spice: int) -> str:
    base = f"{s['name']}: {s['moving_min']} min of tennis"
    if spice >= 3: return base + ". Competitive cardio disguised as leisure. A classic scam."
    if spice == 2: return base + ". Just enough running to be annoying, not enough to count as honesty."
    if spice == 1: return base + f" with {s['kudos']} kudos. Elegant little sprint intervals in polite clothing."
    return base + ". Solid session. Civilized suffering with a racket."


def line_for_weights(s: dict[str, Any], tone: str, spice: int) -> str:
    base = f"{s['name']}: {s['moving_min']} min of weight training"
    if tone == 'coach': return base + ". Good. Lift the weight, keep the ego on a shorter leash."
    if spice >= 3: return base + ". Zero kilometres, maximum theatrical tension."
    if spice == 2: return base + ". Same room, same iron, same refusal to choose peace."
    if spice == 1: return base + ". Honest work. No scenery, just reps and consequences."
    return base + ". Strong, sensible, and only moderately feral."


def generic_line(s: dict[str, Any], tone: str, spice: int) -> str:
    sport = s['sport'].lower()
    base = f"{s['name']}: {s['distance_km']} km of {sport} in {s['moving_min']} min"
    if spice >= 3: return base + ". A creative new way to be tired for no financial reward."
    if spice == 2: return base + ". Public evidence that questionable judgment and endurance remain close friends."
    if spice == 1: return base + ". Respectable effort, lightly seasoned with chaos."
    return base + ". Nice little outing."


def roast_line(summary: dict[str, Any], tone: str, spice: int) -> str:
    sport = summary['sport'].lower()
    if 'run' in sport: return line_for_run(summary, tone, spice)
    if 'tennis' in sport: return line_for_tennis(summary, tone, spice)
    if 'weight' in sport or summary['trainer']: return line_for_weights(summary, tone, spice)
    return generic_line(summary, tone, spice)


def overall_line(summaries: list[dict[str, Any]], spice: int) -> str:
    total_km = round(sum(s['distance_km'] for s in summaries), 2)
    total_min = sum(s['moving_min'] for s in summaries)
    if spice >= 3: return f"Overall: {total_km} km across {len(summaries)} activities and {total_min} moving minutes. An impressive amount of voluntary wear and tear."
    if spice == 2: return f"Overall: {total_km} km across {len(summaries)} activities and {total_min} moving minutes. Productive, disciplined, and a little bit deranged."
    if spice == 1: return f"Overall: {total_km} km across {len(summaries)} activities and {total_min} moving minutes. A productive little festival of exertion."
    return f"Overall: {total_km} km across {len(summaries)} activities and {total_min} moving minutes. Nicely done."


def roast_block(activities: list[dict[str, Any]], tone: str, spice: int, *, target_date: str | None = None) -> str:
    summaries = [summarize_activity(a) for a in activities]
    if target_date:
        summaries = [s for s in summaries if date_key(s) == target_date]
    if not summaries:
        if spice >= 3: return "No Strava activity today. Elite dedication to stealth mode."
        if spice == 2: return "No Strava activity today. Either rest day, or you buried the evidence well."
        if spice == 1: return "No Strava activity today. Recovery day or suspiciously quiet behaviour."
        return "No Strava activity today. Rest counts too."
    lines = [roast_line(s, tone, spice) for s in summaries]
    if len(summaries) > 1: lines.append(overall_line(summaries, spice))
    return "\n".join(lines)


def auth_unavailable_message(error: Exception, recovery: dict[str, Any] | None = None) -> str:
    if recovery and recovery.get("status") == "initial_setup_required":
        return "Strava initial setup is missing or incomplete, so I can't verify today's activity yet. Please complete the initial Strava connection first."
    if recovery and recovery.get("status") == "config_incomplete":
        return "Strava app configuration is missing or incomplete, so automatic token refresh is unavailable. Add the Strava app client credentials first."
    if recovery and recovery.get("status") == "reauth_required":
        return "Strava authentication needs reauthorisation before I can verify today's activity. This is not a confirmed rest day."
    return f"Strava data unavailable due to authentication failure: {error}. This is not a confirmed rest day."


def data_unavailable_message(error: Exception) -> str:
    return f"Strava data is currently unavailable: {error}. This is not a confirmed rest day."


def main() -> int:
    args = build_parser().parse_args()
    config = load_strava_app_config(args.config_file)
    state_file = Path(args.state_file).expanduser()
    reauth_script = Path(args.reauth_script).expanduser()

    if args.command == "auth-url":
        available = reauth_available(reauth_script, config)
        missing = missing_config_requirements(config)
        setup_status = "ready"
        token_file = Path(config["token_file"]).expanduser()
        try:
            validate_token_shape(load_tokens(token_file), token_file)
        except StravaInitialSetupRequiredError:
            setup_status = "initial_setup_required"
        payload: Any = {
            "status": "reauth_available" if available else "reauth_unavailable",
            "setup_status": setup_status,
            "config_status": config_status(config),
            "auth_url": get_reauth_url(reauth_script) if available else None,
            "reauth_script": str(reauth_script),
            "config_path": config["config_path"],
            "config_present": config["config_present"],
            "token_file": config["token_file"],
            "missing_requirements": missing,
        }
        print(json.dumps(payload, indent=2))
        return 0

    recovery: dict[str, Any] | None = None
    try:
        activities, recovery = fetch_activities_with_recovery(config, args.days, args.limit, reauth_script)
    except (StravaInitialSetupRequiredError, StravaAuthError) as exc:
        status = recovery.get("status") if recovery else "auth_unavailable"
        payload = {
            "status": status,
            "error": str(exc),
            "reauth": recovery,
            "config_path": config["config_path"],
            "config_present": config["config_present"],
            "config_status": config_status(config),
            "missing_requirements": missing_config_requirements(config),
            "token_file": config["token_file"],
            "roast": auth_unavailable_message(exc, recovery),
        }
        if args.json: print(json.dumps(payload, indent=2 if args.pretty else None))
        else: print(payload["roast"])
        return 0
    except StravaDataUnavailableError as exc:
        payload = {"status": "data_unavailable", "error": str(exc), "roast": data_unavailable_message(exc)}
        if args.json: print(json.dumps(payload, indent=2 if args.pretty else None))
        else: print(payload["roast"])
        return 0

    daily = build_daily_payload(activities)
    target_date = resolve_target_date(args.target_date)
    target_day = select_target_day(daily, target_date)
    last_activity = find_last_activity(activities, target_date)

    if args.command == "summary":
        payload = {"status": "ok", **daily}
    elif args.command == "context":
        state = load_state(state_file)
        payload = build_roast_context(target_day or build_empty_day(target_date), args.tone, args.spice, state)
        payload["status"] = "ok"
        payload["target_date"] = target_date
        payload["has_activity_today"] = bool(target_day and target_day.get("count"))
        if last_activity and not payload["has_activity_today"]: payload["last_activity"] = last_activity
    elif args.command == "prompt":
        state = load_state(state_file)
        context = build_roast_context(target_day or build_empty_day(target_date), args.tone, args.spice, state)
        context["status"] = "ok"
        context["target_date"] = target_date
        context["has_activity_today"] = bool(target_day and target_day.get("count"))
        if last_activity and not context["has_activity_today"]: context["last_activity"] = last_activity
        payload = build_roast_prompt(context)
    elif args.command == "preview":
        state = load_state(state_file)
        context = build_roast_context(target_day or build_empty_day(target_date), args.tone, args.spice, state)
        context["status"] = "ok"
        context["target_date"] = target_date
        context["has_activity_today"] = bool(target_day and target_day.get("count"))
        if last_activity and not context["has_activity_today"]: context["last_activity"] = last_activity
        payload = write_roast_preview(context, build_roast_prompt(context))
    else:
        roast_text = roast_block(activities, args.tone, args.spice, target_date=target_date)
        payload = {"status": "ok", "activity_count": daily["activity_count"], "target_date": target_date, "has_activity_today": bool(target_day and target_day.get("count")), "tone": args.tone, "spice": args.spice, "roast": roast_text}
        if target_day:
            record_roast_state(state_file, target_day, args.tone, args.spice, roast_text)

    if args.command in {"prompt", "preview"}: print(payload)
    elif args.json or args.command in {"summary", "context", "auth-url"}: print(json.dumps(payload, indent=2 if args.pretty or args.command in {"summary", "context", "auth-url"} else None))
    else: print(payload["roast"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
