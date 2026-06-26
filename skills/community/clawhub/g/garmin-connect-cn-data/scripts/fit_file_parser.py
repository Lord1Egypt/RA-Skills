#!/usr/bin/env python3
"""Parse FIT files with Python SDK (fitparse)."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from fitparse import FitFile
except Exception:  # pragma: no cover
    FitFile = None


def parse_fit_header(path: Path) -> Dict[str, object]:
    with path.open("rb") as f:
        raw = f.read(14)

    if len(raw) < 12:
        raise ValueError("FIT header too short (<12 bytes)")

    header_size = raw[0]
    protocol_ver = raw[1]
    profile_ver = int.from_bytes(raw[2:4], "little")
    data_size = int.from_bytes(raw[4:8], "little")
    data_type = raw[8:12].decode("ascii", errors="replace")
    header_crc = int.from_bytes(raw[12:14], "little") if header_size >= 14 and len(raw) >= 14 else None

    return {
        "header_size": header_size,
        "protocol_version_raw": protocol_ver,
        "protocol_version": f"{protocol_ver >> 4}.{protocol_ver & 0x0F}",
        "profile_version_raw": profile_ver,
        "profile_version": round(profile_ver / 100.0, 2),
        "data_size": data_size,
        "data_type": data_type,
        "header_crc": header_crc,
        "is_fit_magic_valid": data_type == ".FIT",
    }


def to_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def pick(d: Dict[str, object], *keys: str):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None


def normalize_stride(raw_stride: Optional[float]) -> Optional[float]:
    if raw_stride is None:
        return None
    # Heuristic normalization for common encodings.
    if raw_stride > 20:
        return round(raw_stride / 1000.0, 3)  # likely mm
    if raw_stride > 5:
        return round(raw_stride / 100.0, 3)  # likely cm
    return round(raw_stride, 3)  # likely meters


def parse_fit_with_sdk(path: Path, max_messages: int) -> Dict[str, object]:
    ff = FitFile(str(path))

    message_counts: Dict[str, int] = {}
    presence = {
        "heart_rate": False,
        "cadence": False,
        "stride": False,
        "distance": False,
        "time": False,
    }

    laps = []
    scanned = 0

    for msg in ff.get_messages():
        scanned += 1
        if scanned > max_messages:
            break

        msg_name = msg.name
        message_counts[msg_name] = message_counts.get(msg_name, 0) + 1

        values = {f.name: f.value for f in msg}
        keys = set(values.keys())

        if "heart_rate" in keys or "avg_heart_rate" in keys:
            presence["heart_rate"] = True
        if "cadence" in keys or "avg_cadence" in keys or "avg_running_cadence" in keys:
            presence["cadence"] = True
        if {"step_length", "stride_length", "avg_step_length", "avg_stride_length"} & keys:
            presence["stride"] = True
        if "distance" in keys or "total_distance" in keys:
            presence["distance"] = True
        if "timestamp" in keys or "total_timer_time" in keys:
            presence["time"] = True

        if msg_name == "lap":
            lap_dist = to_float(pick(values, "total_distance", "distance"))
            lap_time = to_float(pick(values, "total_timer_time", "total_elapsed_time", "timer_time"))
            lap_hr = to_float(pick(values, "avg_heart_rate", "average_heart_rate", "heart_rate"))
            lap_cad = to_float(
                pick(
                    values,
                    "avg_running_cadence",
                    "avg_cadence",
                    "cadence",
                )
            )
            lap_stride_raw = to_float(
                pick(
                    values,
                    "avg_step_length",
                    "avg_stride_length",
                    "step_length",
                    "stride_length",
                )
            )

            if lap_dist is not None and lap_dist > 0:
                laps.append(
                    {
                        "distance_m": round(lap_dist, 3),
                        "duration_sec": round(lap_time, 3) if lap_time is not None else None,
                        "avg_hr": lap_hr,
                        "cadence": lap_cad,
                        "stride_raw": lap_stride_raw,
                    }
                )

    if presence["heart_rate"]:
        hr = "direct"
    else:
        hr = "unavailable"

    if presence["cadence"]:
        cadence = "direct"
    else:
        cadence = "unavailable"

    if presence["stride"]:
        stride = "direct"
    elif presence["cadence"] and presence["distance"] and presence["time"]:
        stride = "estimated"
    else:
        stride = "unavailable"

    return {
        "messages_scanned": scanned,
        "message_counts": message_counts,
        "presence": presence,
        "metrics": {
            "hr": hr,
            "cadence": cadence,
            "stride": stride,
        },
        "laps": laps,
    }


def parse_targets(raw: str) -> List[object]:
    out: List[object] = []
    for item in raw.split(","):
        token = item.strip().lower()
        if not token:
            continue
        if token == "last":
            out.append("last")
            continue
        try:
            out.append(float(token))
        except ValueError:
            raise ValueError(f"Invalid target token: {item}")
    return out


def km_samples_from_laps(laps: List[Dict[str, object]], targets: List[object]) -> Dict[str, object]:
    if not laps:
        return {}

    rows = []
    cum_m = 0.0
    for i, lap in enumerate(laps, start=1):
        dist = to_float(lap.get("distance_m")) or 0.0
        dur = to_float(lap.get("duration_sec"))
        hr = to_float(lap.get("avg_hr"))
        cad = to_float(lap.get("cadence"))
        stride_raw = to_float(lap.get("stride_raw"))

        cum_m += dist
        stride_direct = normalize_stride(stride_raw)

        stride_estimated = None
        if stride_direct is None and cad and dur and dur > 0:
            steps = cad * (dur / 60.0)
            if steps > 0:
                stride_estimated = round(dist / steps, 3)

        if stride_direct is not None:
            stride = stride_direct
            stride_source = "direct"
        elif stride_estimated is not None:
            stride = stride_estimated
            stride_source = "estimated"
        else:
            stride = None
            stride_source = "unavailable"

        rows.append(
            {
                "lap": i,
                "cum_km": cum_m / 1000.0,
                "avg_hr": hr,
                "cadence": cad,
                "stride_m": stride,
                "stride_source": stride_source,
            }
        )

    total_km = rows[-1]["cum_km"]

    out: Dict[str, object] = {}
    for target in targets:
        if target == "last":
            target_km = total_km
            key = "km_last"
        else:
            target_km = float(target)
            key = f"km_{int(target_km) if math.isclose(target_km, int(target_km)) else target_km}"

        if target_km <= 0:
            out[key] = None
            continue

        chosen = min(rows, key=lambda r: abs(r["cum_km"] - target_km))
        out[key] = {
            "target_km": round(target_km, 3),
            "matched_lap": chosen["lap"],
            "matched_cum_km": round(chosen["cum_km"], 3),
            "avg_hr": chosen["avg_hr"],
            "cadence": chosen["cadence"],
            "stride_m": chosen["stride_m"],
            "stride_source": chosen["stride_source"],
        }

    return out


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Parse FIT file using Python SDK (fitparse)")
    p.add_argument("input_fit", help="Path to .fit file")
    p.add_argument("--targets", default="1,5,10,last", help="KM targets, e.g. 1,5,10,last")
    p.add_argument("--max-messages", type=int, default=500000, help="Safety cap for parsed FIT messages")
    p.add_argument("--output", default=None, help="Write JSON to file instead of stdout")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if hr/cadence are unavailable",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if FitFile is None:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "fitparse is not installed. Use: uv run --with fitparse python scripts/fit_file_parser.py ...",
                },
                ensure_ascii=False,
            )
        )
        return 2

    input_fit = Path(args.input_fit).expanduser().resolve()
    if not input_fit.exists():
        print(json.dumps({"status": "error", "message": f"Input not found: {input_fit}"}, ensure_ascii=False))
        return 2

    result: Dict[str, object] = {
        "status": "success",
        "input_file": str(input_fit),
    }

    try:
        result["fit_header"] = parse_fit_header(input_fit)
        parsed = parse_fit_with_sdk(input_fit, args.max_messages)
        result["parse"] = {
            "messages_scanned": parsed["messages_scanned"],
            "message_counts": parsed["message_counts"],
            "metrics": parsed["metrics"],
        }

        targets = parse_targets(args.targets)
        result["km_samples"] = km_samples_from_laps(parsed["laps"], targets)

        if args.strict:
            m = parsed["metrics"]
            if m["hr"] == "unavailable" or m["cadence"] == "unavailable":
                result["status"] = "error"
                result["message"] = "Strict mode failed: hr/cadence unavailable"

    except Exception as exc:
        result["status"] = "error"
        result["message"] = str(exc)

    payload = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + ("\n" if not payload.endswith("\n") else ""), encoding="utf-8")
    else:
        print(payload)

    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
