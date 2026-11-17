#!/usr/bin/env python3
"""Compare an offline recorded activity with the existing race pacing model."""

import argparse
from bisect import bisect_left
import copy
import json
import math
from pathlib import Path
import sys

from activity_data import GarminClient, api_key, lap_value, read_activity, read_json, write_private
import pace_chart as pace
from pace_chart import InputError


def clock(seconds: float) -> str:
    rounded = math.floor(abs(seconds) + .5)
    return f"{rounded // 3600:02d}:{rounded // 60 % 60:02d}:{rounded % 60:02d}"


def time_delta(seconds: float) -> str:
    return ("-" if seconds < 0 else "+" if seconds > 0 else "") + clock(seconds) if (
        math.floor(abs(seconds) + .5)) else "00:00:00"


def load_plan(path: Path, config: dict, targets: list[str] | None = None) -> tuple[dict, pace.Route]:
    config = copy.deepcopy(config)
    if targets is not None:
        config.pop("target", None)
        config["targets"] = targets
    plan = pace.build_plan(path, config, defer_water=True)
    parameters = plan["parameters"]
    route = pace.prepare_route(
        pace.load_route(path, config.get("track_index"), config.get("use_kml_altitudes", False)),
        parameters["distance_tolerance_m"], parameters["elevation_spike_m"],
    )
    return plan, route


def route_coordinate(route: pace.Route, distance: float) -> tuple[float, float]:
    distances = [s.distance_m for s in route.samples]
    right = min(len(distances) - 1, max(1, bisect_left(distances, distance)))
    left = right - 1
    width = distances[right] - distances[left]
    ratio = (distance - distances[left]) / width if width else 0
    a, b = route.points[left], route.points[right]
    return (a[0] + ratio * (b[0] - a[0]),
            (a[1] + ratio * pace.longitude_delta(a[1], b[1]) + 180) % 360 - 180)


def interpolate_record(records: list[dict], axis: list[float], value: float) -> dict:
    right = min(len(axis) - 1, max(1, bisect_left(axis, value)))
    left = right - 1
    width = axis[right] - axis[left]
    ratio = (value - axis[left]) / width if width else 0
    a, b = records[left], records[right]
    return {
        **{k: a[k] + ratio * (b[k] - a[k]) for k in ("distance_m", "elapsed_seconds", "lat")},
        "lon": (a["lon"] + ratio * pace.longitude_delta(a["lon"], b["lon"]) + 180) % 360 - 180,
        "gap_seconds": b["elapsed_seconds"] - a["elapsed_seconds"],
        "gap_m": b["distance_m"] - a["distance_m"],
    }


def match_checkpoints(plan: dict, route: pace.Route, activity: dict, overrides: dict) -> tuple[list, list]:
    if not isinstance(overrides, dict):
        raise InputError("Passage overrides must be a JSON object: CP ID -> elapsed H:MM:SS")
    checkpoints = plan["checkpoints"]
    allowed = {cp["id"] for cp in checkpoints[1:-1]}
    if set(overrides) - allowed:
        raise InputError("Unknown or endpoint passage override IDs", {"allowed_ids": sorted(allowed)})
    records = activity["records"]
    points = [(r["lat"], r["lon"], 0) for r in records]
    distances = [0.0]
    for a, b in zip(points, points[1:]):
        distances.append(distances[-1] + pace.haversine(a, b))
    if distances[-1] <= 0:
        raise InputError("Recorded GPS track has no horizontal extent")
    recorded_route = pace.Route(points, [pace.Sample(d, 0) for d in distances], [])
    timestamps = [r["elapsed_seconds"] for r in records]
    candidates = {c["id"]: c for c in route.candidates}
    configured_positions = plan["configuration"].get("checkpoint_overrides", {})
    matched, warnings = [], []
    for index, cp in enumerate(checkpoints):
        candidate = candidates.get(cp["id"])
        if candidate and "distance_km" not in configured_positions.get(cp["id"], {}):
            coordinate = candidate["lat"], candidate["lon"]
        else:
            coordinate = route_coordinate(route, cp["distance_m"])
        if index in (0, len(checkpoints) - 1):
            start = index == 0
            offset = pace.haversine(coordinate, points[0 if start else -1])
            if offset > 100:
                raise InputError(f'{cp["id"]}: activity endpoint is over 100 m from route; '
                                 'select a matching activity/route', {"offset_m": offset})
            item = ({"distance_m": 0.0, "elapsed_seconds": 0.0, "ascent_m": 0.0, "descent_m": 0.0}
                    if start else {k: activity["totals"][k] for k in (
                        "distance_m", "elapsed_seconds", "ascent_m", "descent_m")})
            item.update(offset_m=offset, match_method="session endpoint")
        else:
            point = {"lat": coordinate[0], "lon": coordinate[1]}
            if cp["id"] in overrides:
                value = overrides[cp["id"]]
                elapsed = (pace.duration(value, "passage override") if isinstance(value, str)
                           else pace.number(value, "passage override"))
                if not timestamps[0] <= elapsed <= timestamps[-1]:
                    raise InputError(f'{cp["id"]}: override is outside GPS record coverage')
                item = interpolate_record(records, timestamps, elapsed)
                item["elapsed_seconds"] = elapsed
                item["offset_m"] = pace.haversine(coordinate, (item["lat"], item["lon"]))
                item["match_method"] = "elapsed override"
                warnings.append(f'{cp["id"]}: explicit passage override, offset {item["offset_m"]:.1f} m.')
            else:
                options = pace.projection_options(recorded_route, point)
                diagnostic = [
                    {**option, "elapsed_seconds": interpolate_record(
                        records, distances, option["distance_m"])["elapsed_seconds"]}
                    for option in options
                ]
                if len(options) != 1 or options[0]["offset_m"] > 100:
                    reason = "ambiguous activity passage" if len(options) != 1 else "over 100 m off activity track"
                    raise InputError(f'{cp["id"]}: {reason}; supply --passage-overrides with '
                                     'this CP ID and confirmed actual elapsed time', diagnostic)
                item = interpolate_record(records, distances, options[0]["distance_m"])
                item.update(offset_m=options[0]["offset_m"], match_method="track projection")
                # Geometric distance does not distinguish arrival from departure during a GPS standstill.
                close = [r for r, p in zip(records, points) if pace.haversine(coordinate, p) <= 3]
                if close and close[-1]["elapsed_seconds"] - close[0]["elapsed_seconds"] >= 120:
                    raise InputError(f'{cp["id"]}: ambiguous stationary passage; confirm elapsed time '
                                     'with --passage-overrides',
                                     {"earliest_seconds": close[0]["elapsed_seconds"],
                                      "latest_seconds": close[-1]["elapsed_seconds"]})
            for key in ("ascent_m", "descent_m"):
                item[key] = lap_value(activity["laps"], item["distance_m"], key)
            if item["gap_seconds"] > 120 or item["gap_m"] > 100:
                warnings.append(f'{cp["id"]}: passage interpolated across {item["gap_seconds"]:.0f} s / '
                                f'{item["gap_m"]:.0f} m record gap.')
        if matched and any(item[k] <= matched[-1][k] for k in ("elapsed_seconds", "distance_m")):
            raise InputError(f'{cp["id"]}: nonmonotonic CP passage order; confirm actual times '
                             'with --passage-overrides')
        for key in ("ascent_m", "descent_m"):
            if matched and item[key] is not None and matched[-1][key] is not None and item[key] < matched[-1][key]:
                raise InputError(f'{cp["id"]}: {key} decreases at finish/station; check summary and FIT laps')
        matched.append({"id": cp["id"], "name": cp["name"], **item})
    return matched, warnings


def subtract(a: float | None, b: float | None) -> float | None:
    return None if a is None or b is None else a - b


def build_comparison(plan: dict, route: pace.Route, activity: dict, overrides: dict | None = None) -> dict:
    overrides = {} if overrides is None else overrides
    actual, warnings = match_checkpoints(plan, route, activity, overrides)
    segments, terrain = [], []
    for index in range(1, len(actual)):
        prior, cp = actual[index - 1:index + 1]
        actual_seconds = cp["elapsed_seconds"] - prior["elapsed_seconds"]
        entries = []
        for schedule in plan["schedules"]:
            times = schedule["checkpoints"]
            seconds = times[index]["arrival_seconds"] - times[index - 1]["arrival_seconds"]
            entries.append({"target_seconds": schedule["target_seconds"], "seconds": seconds,
                            "delta_seconds": seconds - actual_seconds})
        segments.append({"from_id": prior["id"], "to_id": cp["id"],
                         "from_name": prior["name"], "to_name": cp["name"],
                         "actual_seconds": actual_seconds, "plans": entries})
        terrain.append({
            "id": cp["id"], "actual_distance_m": cp["distance_m"],
            "actual_ascent_m": subtract(cp["ascent_m"], prior["ascent_m"]),
            "actual_descent_m": subtract(cp["descent_m"], prior["descent_m"]),
            "planned_distance_m": plan["checkpoints"][index]["distance_m"],
            "planned_ascent_m": plan["checkpoints"][index]["ascent_m"],
            "planned_descent_m": plan["checkpoints"][index]["descent_m"],
        })
    return {
        "schema_version": 1, "plan": plan,
        "activity": {k: v for k, v in activity.items() if k not in ("records", "laps")},
        "checkpoints": actual, "segments": segments, "terrain": terrain,
        "passage_overrides": overrides,
        "warnings": list(activity["warnings"]) + warnings,
        "semantics": {"time_basis": "Elapsed including stops; projected passage, not official timing",
                      "delta": "repository minus recorded activity",
                      "terrain": "Cumulative distance; per-segment ascent/descent from adjacent lap estimates"},
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("list", "fetch"):
        sub = commands.add_parser(name)
        sub.add_argument("--region", choices=["com", "cn"], default="com")
        sub.add_argument("--env-file", type=Path)
        sub.add_argument("--timeout", type=float, default=45)
        if name == "list":
            sub.add_argument("--start-date", required=True)
            sub.add_argument("--end-date", required=True)
            sub.add_argument("--limit", type=int, default=20)
            sub.add_argument("--start", type=int, default=0)
        else:
            sub.add_argument("activity_id")
            sub.add_argument("--output-dir", type=Path)
            sub.add_argument("--overwrite", action="store_true")
    for name in ("inspect", "generate"):
        sub = commands.add_parser(name)
        sub.add_argument("route", type=Path)
        sub.add_argument("--config", required=True, type=Path)
        sub.add_argument("--fit", required=True, type=Path)
        sub.add_argument("--summary", type=Path)
        sub.add_argument("--targets", nargs="+")
        sub.add_argument("--passage-overrides", type=Path)
        if name == "generate":
            sub.add_argument("--output-dir", type=Path, default=Path("output/comparison"))
            sub.add_argument("--overwrite", action="store_true")
            sub.add_argument("--export-json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command in ("list", "fetch"):
            client = GarminClient(api_key(args.env_file), args.region, args.timeout)
            if args.command == "list":
                print(json.dumps(client.activities(args.start_date, args.end_date, args.limit, args.start),
                                 ensure_ascii=False, indent=2))
            else:
                folder = args.output_dir or Path("output/activities") / args.activity_id
                paths = client.fetch(args.activity_id, folder, args.overwrite)
                print(json.dumps({"files": [str(p) for p in paths]}, ensure_ascii=False))
            return 0
        config = read_json(args.config)
        plan, route = load_plan(args.route, config, args.targets)
        activity = read_activity(args.fit, args.summary)
        overrides = read_json(args.passage_overrides) if args.passage_overrides else {}
        comparison = build_comparison(plan, route, activity, overrides)
        # File hashes are portable provenance; local paths and raw GPS records are not exported.
        import hashlib
        comparison["config_sha256"] = hashlib.sha256(args.config.read_bytes()).hexdigest()
        if args.command == "inspect":
            print(json.dumps({k: v for k, v in comparison.items() if k != "plan"},
                             ensure_ascii=False, indent=2, allow_nan=False))
        else:
            from comparison_svg import render_svg
            outputs = {args.output_dir / "garmin-comparison.svg": render_svg(comparison).encode()}
            if args.export_json:
                outputs[args.output_dir / "garmin-comparison.json"] = json.dumps(
                    comparison, ensure_ascii=False, indent=2, allow_nan=False).encode()
            if not args.overwrite and any(p.exists() for p in outputs):
                raise InputError("Comparison output exists; choose another directory or --overwrite")
            args.output_dir.mkdir(parents=True, exist_ok=True)
            for path, binary in outputs.items():
                write_private(path, binary, args.overwrite)
            print(json.dumps({"files": [str(p) for p in outputs], "targets_seconds": plan["targets_seconds"],
                              "elapsed_seconds": activity["totals"]["elapsed_seconds"],
                              "segment_count": len(comparison["segments"]),
                              "warnings": comparison["warnings"]}, ensure_ascii=False, indent=2))
        return 0
    except (InputError, OSError) as error:
        result = {"error": str(error)}
        if isinstance(error, InputError) and error.details is not None:
            result["details"] = error.details
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
