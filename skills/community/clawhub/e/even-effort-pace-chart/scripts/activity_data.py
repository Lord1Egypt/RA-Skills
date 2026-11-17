"""Optional FIT route/activity input and Garmin Personal API adapter."""

from datetime import date, datetime
import json
import math
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

from pace_chart import InputError, number


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise InputError(f"Cannot read JSON: {path.name}") from error
    if not isinstance(value, dict):
        raise InputError(f"Expected a JSON object: {path.name}")
    return value


def decode_fit(binary: bytes) -> dict:
    try:
        from garmin_fit_sdk import Decoder, Stream
    except ImportError as error:
        raise InputError("FIT input needs garmin-fit-sdk==21.218.0; "
                         "install scripts/requirements-comparison.txt") from error
    try:
        messages, errors = Decoder(Stream.from_byte_array(bytearray(binary))).read()
    except Exception as error:
        raise InputError("Cannot decode FIT; provide an intact original FIT export") from error
    if errors:
        raise InputError("Damaged FIT: decoder reported errors; export the original again")
    return messages


def read_activity(path: Path, summary_path: Path | None = None) -> dict:
    try:
        if path.suffix.lower() == ".zip":
            with ZipFile(path) as archive:
                members = [m for m in archive.infolist()
                           if not m.is_dir() and m.filename.lower().endswith(".fit")]
                if len(members) != 1:
                    raise InputError("ZIP must contain exactly one FIT; select a single activity")
                if members[0].file_size > 250_000_000:
                    raise InputError("FIT exceeds the 250 MB input limit")
                binary = archive.read(members[0])
        elif path.suffix.lower() == ".fit":
            if path.stat().st_size > 250_000_000:
                raise InputError("FIT exceeds the 250 MB input limit")
            binary = path.read_bytes()
        else:
            raise InputError("Activity input must be a FIT file or FIT ZIP")
    except (OSError, BadZipFile, RuntimeError) as error:
        raise InputError("Cannot read activity FIT/ZIP") from error
    activity = activity_from_messages(decode_fit(binary), read_json(summary_path) if summary_path else None)
    import hashlib
    activity["source"] = {"fit_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    if summary_path:
        activity["source"]["summary_sha256"] = hashlib.sha256(summary_path.read_bytes()).hexdigest()
    return activity


def read_fit_route(path: Path) -> dict:
    activity = read_activity(path)
    records, duplicates = [], 0
    for record in activity["records"]:
        elevation = number(record.get("elevation_m"), "FIT route elevation", minimum=-math.inf)
        item = {**record, "elevation_m": elevation}
        if records and item["distance_m"] == records[-1]["distance_m"]:
            records[-1] = item
            duplicates += 1
        else:
            records.append(item)
    if len(records) < 2:
        raise InputError("FIT route needs at least two distinct recorded distances")
    if records[0]["distance_m"] != 0:
        raise InputError("FIT route GPS coverage must begin at recorded distance zero; "
                         "cannot reconstruct the missing start")
    warnings = list(activity["warnings"])
    if duplicates:
        warnings.append(f"Merged {duplicates} duplicate recorded-distance records, keeping the last point.")
    max_gap = max(b["distance_m"] - a["distance_m"] for a, b in zip(records, records[1:]))
    if max_gap > 100:
        warnings.append(f"FIT route record gap is {max_gap:.1f} m; interpolation cannot recover missing terrain.")
    if abs(records[-1]["distance_m"] - activity["totals"]["distance_m"]) > .01:
        warnings.append("FIT route ends at the last recorded distance; session total is not used to rescale it.")
    return {
        "records": records, "warnings": warnings,
        "diagnostics": {
            "distance_source": "fit_recorded", "elevation_source": "FIT enhanced_altitude / altitude",
            "fit_duplicate_distance_records": duplicates,
            "fit_skipped_records": activity["skipped_records"],
            "fit_session_distance_m": activity["totals"]["distance_m"],
        },
    }


def activity_from_messages(messages: dict, summary: dict | None = None) -> dict:
    sessions = messages.get("session_mesgs", [])
    if len(sessions) != 1:
        raise InputError("FIT must contain exactly one session; export/select a single activity")
    session = sessions[0]
    start = session.get("start_time")
    if not isinstance(start, datetime):
        raise InputError("FIT session has no valid start_time")
    fields = {"distance_m": "total_distance", "elapsed_seconds": "total_elapsed_time",
              "timer_seconds": "total_timer_time", "ascent_m": "total_ascent", "descent_m": "total_descent"}
    totals = {key: session.get(field) for key, field in fields.items()}
    platform = summary.get("summaryDTO", summary) if summary is not None else {}
    if not isinstance(platform, dict):
        raise InputError("Platform summaryDTO must be an object")
    for key, field in {"distance_m": "distance", "elapsed_seconds": "elapsedDuration",
                       "timer_seconds": "duration", "ascent_m": "elevationGain",
                       "descent_m": "elevationLoss"}.items():
        if field in platform:
            totals[key] = platform[field]
    for key, value in totals.items():
        if value is not None:
            totals[key] = number(value, key)
    for key in ("distance_m", "elapsed_seconds"):
        if totals[key] is None or totals[key] <= 0:
            raise InputError(f"Activity needs a positive {key} in session/platform summary")
    records, skipped = [], 0
    for record in messages.get("record_mesgs", []):
        if any(record.get(k) is None for k in ("timestamp", "position_lat", "position_long", "distance")):
            skipped += 1
            continue
        try:
            elapsed = (record["timestamp"] - start).total_seconds()
            lat, lon = [record[k] * 180 / 2**31 for k in ("position_lat", "position_long")]
        except (TypeError, ValueError, AttributeError) as error:
            raise InputError("Invalid FIT record timestamp or coordinates") from error
        if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in (lat, lon)):
            raise InputError("Invalid FIT record coordinates")
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise InputError("FIT record coordinates outside WGS84 bounds")
        item = {"lat": lat, "lon": lon, "distance_m": number(record["distance"], "record distance"),
                "elapsed_seconds": number(elapsed, "record elapsed")}
        item["elevation_m"] = (record["enhanced_altitude"] if record.get("enhanced_altitude") is not None
                               else record.get("altitude"))
        if records and any(item[k] < records[-1][k] for k in ("distance_m", "elapsed_seconds")):
            raise InputError("FIT record distance/time is nonmonotonic; select an intact single session")
        records.append(item)
    if len(records) < 2:
        raise InputError("FIT needs at least two timestamped GPS records with recorded distance")
    if records[-1]["elapsed_seconds"] > totals["elapsed_seconds"] + 2:
        raise InputError("FIT records extend beyond activity elapsed total; check the platform summary")
    warnings = []
    if skipped:
        warnings.append(f"Skipped {skipped} records without GPS/time/distance; gaps use linear interpolation.")
    if abs(records[-1]["distance_m"] - totals["distance_m"]) > max(100, totals["distance_m"] * .01):
        warnings.append("Last GPS record and activity distance differ substantially; check recording coverage.")
    if (records[0]["elapsed_seconds"] > 120
            or totals["elapsed_seconds"] - records[-1]["elapsed_seconds"] > 120):
        warnings.append("GPS coverage omits over 120 seconds at an activity endpoint.")
    laps = []
    cumulative = {"distance_m": 0.0, "ascent_m": 0.0, "descent_m": 0.0}
    raw_laps = messages.get("lap_mesgs", [])
    if raw_laps:
        try:
            ordered = sorted(raw_laps, key=lambda lap: lap["start_time"])
            for lap in ordered:
                length = number(lap.get("total_distance"), "lap distance", strictly_positive=True)
                cumulative["distance_m"] += length
                for key, field in (("ascent_m", "total_ascent"), ("descent_m", "total_descent")):
                    value = lap.get(field)
                    cumulative[key] = (cumulative[key] + number(value, field)
                                       if cumulative[key] is not None and value is not None else None)
                laps.append(dict(cumulative))
        except (InputError, KeyError, TypeError) as error:
            warnings.append("Incomplete/invalid lap boundaries; intermediate ascent/descent are unknown.")
            laps = []
        if laps and abs(laps[-1]["distance_m"] - totals["distance_m"]) > max(100, totals["distance_m"] * .01):
            warnings.append("Lap distance coverage differs from activity total; intermediate terrain is unknown.")
            laps = []
    if not laps:
        warnings.append("No usable FIT laps; intermediate ascent/descent are unknown.")
    else:
        for key in ("ascent_m", "descent_m"):
            if laps[-1][key] != totals[key]:
                warnings.append(f"{key}: FIT laps {laps[-1][key]}, finish {totals[key]}; no rescaling.")
    return {
        "activity_id": (summary or {}).get("activityId"),
        "activity_name": (summary or {}).get("activityName", "FIT activity"),
        "start_time": platform.get("startTimeLocal") or start.isoformat(),
        "totals_source": "Garmin platform + FIT session fallback" if summary is not None else "FIT session",
        "totals": totals, "lap_totals": dict(laps[-1]) if laps else None,
        "records": records, "laps": laps, "skipped_records": skipped, "warnings": warnings,
    }


def lap_value(laps: list[dict], distance: float, key: str) -> float | None:
    previous_distance, previous_value = 0.0, 0.0
    for lap in laps:
        if distance <= lap["distance_m"]:
            if previous_value is None or lap[key] is None:
                return None
            return previous_value + (lap[key] - previous_value) * (
                distance - previous_distance) / (lap["distance_m"] - previous_distance)
        previous_distance, previous_value = lap["distance_m"], lap[key]
    return None


def api_key(env_file: Path | None = None, environ=None) -> str:
    environ = os.environ if environ is None else environ
    key = environ.get("GARMIN_PERSONAL_API_KEY")
    if key is None and env_file is not None:
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if re.match(r"^\s*(?:export\s+)?GARMIN_PERSONAL_API_KEY\s*=", line):
                    key = line.split("=", 1)[1].strip()
                    if len(key) >= 2 and key[0] == key[-1] and key[0] in "'\"":
                        key = key[1:-1]
                    break
        except OSError as error:
            raise InputError("Cannot read the explicitly selected environment file") from error
    if not key or not re.fullmatch(r"[A-Za-z0-9_.-]+", key):
        raise InputError("Set GARMIN_PERSONAL_API_KEY in the environment or explicit --env-file; "
                         "only a literal key is accepted")
    return key


class GarminClient:
    """One region per client; credentials and bearer tokens stay in memory."""

    def __init__(self, key: str, region="com", timeout=45):
        if region not in ("com", "cn"):
            raise InputError("region must be com or cn")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", key):
            raise InputError("Invalid API key format")
        self.base = f"https://personal.connectapi.garmin.{region}"
        self.key, self.token = key, None
        self.timeout = number(timeout, "timeout", strictly_positive=True)

    def request(self, path: str, auth: str, method="GET") -> bytes:
        try:
            request = Request(self.base + path, method=method,
                              headers={"Authorization": auth, "Accept": "*/*"})
            with urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except HTTPError as error:
            status = error.code
            error.close()
            raise InputError(f"Garmin request failed (HTTP {status}); check region and key permissions") from None
        except (URLError, TimeoutError, OSError):
            raise InputError("Garmin connection failed or timed out; retry explicitly") from None

    def get(self, path: str) -> bytes:
        if self.token is None:
            binary = self.request("/personalapitoken-service/personal-api/personal-api-key/token",
                                  "ApiKey " + self.key, method="POST")
            try:
                self.token = binary.decode().strip()
            except UnicodeError:
                raise InputError("Invalid Garmin authentication response") from None
            if not self.token or any(c.isspace() for c in self.token):
                raise InputError("Invalid Garmin authentication response")
        return self.request(path, "Bearer " + self.token)

    def get_json(self, path: str):
        try:
            return json.loads(self.get(path))
        except (ValueError, UnicodeError):
            raise InputError("Invalid JSON returned by Garmin") from None

    def activities(self, start_date: str, end_date: str, limit=20, start=0):
        try:
            if date.fromisoformat(start_date) > date.fromisoformat(end_date):
                raise ValueError
        except (ValueError, TypeError):
            raise InputError("Use an ordered start/end date range (YYYY-MM-DD)") from None
        if not isinstance(limit, int) or not 1 <= limit <= 1000 or not isinstance(start, int) or start < 0:
            raise InputError("limit must be 1..1000 and start must be nonnegative")
        query = urlencode({"startDate": start_date, "endDate": end_date, "limit": limit, "start": start})
        result = self.get_json("/activitylist-service/activities/search/activities?" + query)
        if not isinstance(result, list):
            raise InputError("Garmin activities response must be a list")
        return result

    def fetch(self, activity_id: str, output_dir: Path, overwrite=False) -> list[Path]:
        if not re.fullmatch(r"[1-9][0-9]*", str(activity_id)):
            raise InputError("Activity ID must be a positive integer")
        paths = [output_dir / "activity-details.json", output_dir / "activity-original.zip"]
        if not overwrite and any(p.exists() for p in paths):
            raise InputError("Activity cache exists; select another directory or --overwrite")
        details = self.get_json("/activity-service/activity/" + str(activity_id))
        if not isinstance(details, dict):
            raise InputError("Garmin activity summary must be an object")
        binary = self.get("/download-service/files/activity/" + str(activity_id))
        if not binary.startswith(b"PK"):
            raise InputError("Garmin original download is not a FIT ZIP")
        output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        write_private(paths[0], json.dumps(details, ensure_ascii=False, indent=2).encode(), overwrite)
        write_private(paths[1], binary, overwrite)
        return paths


def write_private(path: Path, binary: bytes, overwrite=False):
    flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if overwrite else os.O_EXCL)
    try:
        fd = os.open(path, flags, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(binary)
        path.chmod(0o600)
    except OSError as error:
        raise InputError(f"Cannot write output: {path.name}") from error
