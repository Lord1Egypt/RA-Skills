#!/usr/bin/env python3
"""GPX/KML/FIT pace charts; optional weather forecasts and FIT dependency."""

from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
import csv
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
import hashlib
from html import escape
import io
import json
import math
from pathlib import Path
import re
import shutil
from statistics import median
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ARTICLE_URL = "https://mp.weixin.qq.com/s/spYCP-upbqAZN0kzUm-0ng"
ARTICLE_TITLE = "耐力科学|体感一致配速表全面指南"
DEFAULTS = {
    "sample_m": 5.0,
    "smoothing_m": 20.0,
    "ascent_smoothing_m": 0.0,
    "ascent_threshold_m": 10.0,
    "elevation_spike_m": 30.0,
    "distance_tolerance_m": 0.0,
    "ascent_km_per_100m": 1.0,
    "fatigue_rate": 0.08,
    "water_ml_per_10km": 700.0,
    "target_step_minutes": 30.0,
}
CONFIG_KEYS = set(DEFAULTS) | {
    "name", "target", "targets", "track_index", "checkpoints", "cp_selection",
    "checkpoint_overrides", "distance_alignment", "start_time", "pace_basis", "secondary_display",
    "use_kml_altitudes", "output_formats", "ascent_method",
    "water_mode", "water_target", "water_ml_per_hour", "water_buffer_minutes",
    "water_rate_overrides", "water_timezone", "water_weather",
}
CP_KEYS = {"name", "distance_km", "rest_minutes", "cutoff"}
OVERRIDE_KEYS = CP_KEYS | {"allow_off_route"}
CP_PATTERN = re.compile(
    r"(?<![A-Za-z])(?:CP|SP)\s*[-_#]?\s*\d*(?![A-Za-z])"
    r"|\b(?:checkpoint|aid\s*station|water\s*station|start|finish)\b"
    r"|补给|補給|检查点|檢查點|水站|起点|起點|终点|終點|起终点|起終點",
    re.IGNORECASE,
)


class InputError(ValueError):
    def __init__(self, message: str, details=None):
        super().__init__(message)
        self.details = details


@dataclass(frozen=True)
class Sample:
    distance_m: float
    elevation_m: float


@dataclass
class Route:
    points: list[tuple[float, float, float]]
    samples: list[Sample]
    candidates: list[dict]
    warnings: list[str] | None = None
    diagnostics: dict | None = None

    @property
    def total_m(self) -> float:
        return self.samples[-1].distance_m


def number(value, name: str, minimum=0.0, strictly_positive=False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{name} must be a finite number")
    try:
        value = float(value)
    except OverflowError as error:
        raise InputError(f"{name} must be a finite number") from error
    if not math.isfinite(value) or value < minimum or (strictly_positive and value <= 0):
        raise InputError(f"{name} must be finite and {'positive' if strictly_positive else f'>= {minimum}'}")
    return value


def keys(obj, allowed, context):
    if not isinstance(obj, dict):
        raise InputError(f"{context} must be an object")
    unknown = set(obj) - allowed
    if unknown:
        raise InputError(f"Unknown {context} fields: {', '.join(sorted(unknown))}")


def duration(value, name="duration") -> float:
    if not isinstance(value, str) or not re.fullmatch(r"\d{1,4}:[0-5]\d(?::[0-5]\d)?", value):
        raise InputError(f"{name} must be H:MM or H:MM:SS (hours may exceed 24)")
    parts = [int(part) for part in value.split(":")]
    if len(parts) == 2:
        parts.append(0)
    return float(parts[0] * 3600 + parts[1] * 60 + parts[2])


def format_duration(seconds: float) -> str:
    total = math.floor(seconds + 0.5)
    hours, remainder = divmod(total, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def format_pace(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    minutes, seconds = divmod(math.floor(seconds + 0.5), 60)
    return f"{minutes}:{seconds:02}"


def tag(element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def children(element, name):
    return [child for child in element if tag(child) == name]


def child_text(element, name) -> str:
    return next(((child.text or "").strip() for child in element if tag(child) == name), "")


def coordinates(element, require_elevation=True) -> tuple[float, float, float]:
    try:
        lat, lon = float(element.attrib["lat"]), float(element.attrib["lon"])
        ele_text = child_text(element, "ele")
        ele = float(ele_text) if ele_text else (None if require_elevation else 0.0)
    except (KeyError, TypeError, ValueError) as error:
        raise InputError("Invalid GPX coordinates or elevation") from error
    if not math.isfinite(lat) or not -90 <= lat <= 90 or not math.isfinite(lon) or not -180 <= lon <= 180:
        raise InputError("Invalid GPX latitude/longitude")
    if ele is None or not math.isfinite(ele):
        raise InputError("Missing or non-finite GPX elevation; supply a complete elevation profile")
    return lat, lon, ele


def longitude_delta(a: float, b: float) -> float:
    return (b - a + 180) % 360 - 180


def haversine(a, b) -> float:
    lat1, lat2 = math.radians(a[0]), math.radians(b[0])
    dlat = lat2 - lat1
    dlon = math.radians(longitude_delta(a[1], b[1]))
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371008.8 * 2 * math.asin(math.sqrt(min(1.0, max(0.0, h))))


def kml_coordinate(text: str, gx=False, require_elevation=True) -> tuple[float, float, float]:
    values = text.split() if gx else text.split(",")
    if len(values) not in (2, 3) or (require_elevation and len(values) != 3):
        raise InputError("KML coordinates require longitude,latitude,altitude; supply a complete elevation profile")
    try:
        lon, lat = float(values[0]), float(values[1])
        elevation = float(values[2]) if len(values) == 3 else 0.0
    except ValueError as error:
        raise InputError("Invalid KML coordinates or altitude") from error
    if not math.isfinite(lat) or not -90 <= lat <= 90 or not math.isfinite(lon) or not -180 <= lon <= 180:
        raise InputError("Invalid KML latitude/longitude")
    if not math.isfinite(elevation):
        raise InputError("Non-finite KML altitude; supply a complete elevation profile")
    return lat, lon, elevation


def kml_geometries(element, altitude_mode=""):
    for child in element:
        kind = tag(child)
        mode = child_text(child, "altitudeMode") or altitude_mode
        if kind in ("Point", "LineString", "Track"):
            yield child, mode
        elif kind in ("MultiGeometry", "MultiTrack"):
            yield from kml_geometries(child, mode)


def load_kml_route(root, track_index: int | None, use_kml_altitudes: bool) -> Route:
    alternatives, candidates = [], []
    for index, placemark in enumerate((e for e in root.iter() if tag(e) == "Placemark"), 1):
        name = child_text(placemark, "name")
        point_index = 0
        for geometry, mode in kml_geometries(placemark):
            if tag(geometry) != "Point":
                alternatives.append((name, geometry, mode))
                continue
            point_index += 1
            if not name:
                continue
            positions = child_text(geometry, "coordinates").split()
            if len(positions) != 1:
                raise InputError("KML Point needs exactly one coordinate tuple")
            lat, lon, _ = kml_coordinate(positions[0], require_elevation=False)
            candidates.append({
                "id": f"placemark:{index}:point:{point_index}", "name": name, "type": "",
                "lat": lat, "lon": lon, "recognized": bool(CP_PATTERN.search(name)),
            })
    if not alternatives:
        raise InputError("No KML LineString or gx:Track found; supply a local KML route, not a NetworkLink or KMZ")
    if track_index is None:
        if len(alternatives) != 1:
            raise InputError("Multiple KML routes; set track_index (1-based)", [
                {"track_index": i, "name": name, "geometry": tag(geometry)}
                for i, (name, geometry, _) in enumerate(alternatives, 1)
            ])
        track_index = 1
    if isinstance(track_index, bool) or not isinstance(track_index, int) or not 1 <= track_index <= len(alternatives):
        raise InputError("track_index is outside the available routes")
    _, geometry, mode = alternatives[track_index - 1]
    warnings = []
    if mode != "absolute":
        if mode not in ("", "clampToGround"):
            raise InputError(f"Unsupported KML altitude mode {mode!r}; export absolute elevations above sea level")
        if not use_kml_altitudes:
            raise InputError("KML altitude mode is not absolute; confirm coordinate heights with "
                             "use_kml_altitudes=true (inspect: --use-kml-altitudes), or export absolute elevations")
        warnings.append("KML altitude mode is omitted or clampToGround; explicitly using coordinate altitudes "
                        "as the elevation profile. No terrain or vertical-datum correction was applied.")
    gx = tag(geometry) == "Track"
    positions = [(e.text or "").strip() for e in children(geometry, "coord")] if gx else (
        child_text(geometry, "coordinates").split()
    )
    points = []
    for position in positions:
        point = kml_coordinate(position, gx=gx)
        if not points or haversine(points[-1], point) >= 0.001:
            points.append(point)
    if len(points) < 2:
        raise InputError("KML needs at least two distinct positions")
    samples = [Sample(0.0, points[0][2])]
    for previous, point in zip(points, points[1:]):
        samples.append(Sample(samples[-1].distance_m + haversine(previous, point), point[2]))
    max_gap = max(b.distance_m - a.distance_m for a, b in zip(samples, samples[1:]))
    if max_gap > 100:
        warnings.append(f"Sparse KML: maximum original point spacing is {max_gap:.1f} m; interpolation adds no measurement detail.")
    return Route(points, samples, candidates, warnings, {"source_points": len(positions)})


def load_route(path: Path, track_index: int | None = None, use_kml_altitudes=False) -> Route:
    if not isinstance(use_kml_altitudes, bool):
        raise InputError("use_kml_altitudes must be boolean")
    if Path(path).suffix.lower() in (".fit", ".zip"):
        if track_index is not None and (
                isinstance(track_index, bool) or not isinstance(track_index, int) or track_index != 1):
            raise InputError("FIT input supports a single session; track_index must be 1 or omitted")
        if use_kml_altitudes:
            raise InputError("use_kml_altitudes does not apply to FIT input")
        from activity_data import InputError as FitInputError, read_fit_route
        try:
            data = read_fit_route(path)
        except FitInputError as error:
            # The adapter imports the module's exception even when this CLI runs as __main__.
            raise InputError(str(error), error.details) from error
        points = [(r["lat"], r["lon"], r["elevation_m"]) for r in data["records"]]
        samples = [Sample(r["distance_m"], r["elevation_m"]) for r in data["records"]]
        return Route(points, samples, [], data["warnings"], data["diagnostics"])
    raw = Path(path).read_bytes()
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)", raw, flags=re.IGNORECASE):
        raise InputError("Route XML DTD/entity declarations are not supported")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as error:
        raise InputError(f"Invalid route XML: {error}") from error
    if tag(root) == "kml":
        return load_kml_route(root, track_index, use_kml_altitudes)
    if tag(root) != "gpx":
        raise InputError("Expected a GPX or KML root element")
    tracks = children(root, "trk")
    routes = children(root, "rte")
    alternatives = tracks or routes
    if not alternatives:
        raise InputError("No GPX track or route points found")
    if track_index is None:
        if len(alternatives) != 1:
            raise InputError("Multiple GPX routes; set track_index (1-based)", [
                {"track_index": i, "name": child_text(item, "name")}
                for i, item in enumerate(alternatives, 1)
            ])
        track_index = 1
    if isinstance(track_index, bool) or not isinstance(track_index, int) or not 1 <= track_index <= len(alternatives):
        raise InputError("track_index is outside the available routes")
    selected = alternatives[track_index - 1]
    segments = [children(segment, "trkpt") for segment in children(selected, "trkseg")] if tracks else [
        children(selected, "rtept")
    ]
    points = []
    for segment in segments:
        if not segment:
            continue
        current = [coordinates(point) for point in segment]
        if points and haversine(points[-1], current[0]) > 1:
            raise InputError("Disconnected GPX segment; select or repair a continuous route")
        for point in current:
            if points and haversine(points[-1], point) < 0.001:
                continue
            points.append(point)
    if len(points) < 2:
        raise InputError("GPX needs at least two distinct positions")
    samples = [Sample(0.0, points[0][2])]
    for previous, point in zip(points, points[1:]):
        samples.append(Sample(samples[-1].distance_m + haversine(previous, point), point[2]))
    candidates = []
    # A separate route often contains checkpoints beside a densely sampled track.
    sources = [("wpt", children(root, "wpt"))]
    if tracks:
        sources.extend((f"rte{index}:rtept", children(route, "rtept")) for index, route in enumerate(routes, 1))
    else:
        sources.append(("rtept", children(selected, "rtept")))
    for prefix, elements in sources:
        for index, element in enumerate(elements, 1):
            name, kind = child_text(element, "name"), child_text(element, "type")
            if not name and not kind:
                continue
            lat, lon, _ = coordinates(element, require_elevation=False)
            candidates.append({
                "id": f"{prefix}:{index}", "name": name or kind, "type": kind,
                "lat": lat, "lon": lon, "recognized": bool(CP_PATTERN.search(f"{name} {kind}")),
            })
    warnings = []
    max_gap = max(b.distance_m - a.distance_m for a, b in zip(samples, samples[1:]))
    if max_gap > 100:
        warnings.append(f"Sparse GPX: maximum original point spacing is {max_gap:.1f} m; interpolation adds no measurement detail.")
    if tracks and len(routes) > 1:
        warnings.append("Multiple auxiliary GPX routes supplied CP candidates; confirm their relevance in inspect output.")
    nodes = [point for segment in segments for point in segment]
    quality = {"source_points": len(nodes), "quality_flagged_points": 0,
               "quality_metadata_points": 0, "invalid_quality_fields": 0}
    for node in nodes:
        flagged, present = False, False
        for field, limit in (("hdop", 10), ("vdop", 20)):
            text = child_text(node, field)
            if text:
                present = True
                try:
                    value = float(text)
                    if not math.isfinite(value) or value < 0:
                        raise ValueError
                    flagged |= value > limit
                except ValueError:
                    quality["invalid_quality_fields"] += 1
        fix = child_text(node, "fix").lower()
        present |= bool(fix)
        flagged |= fix in ("none", "unknown")
        quality["quality_metadata_points"] += int(present)
        quality["quality_flagged_points"] += int(flagged)
    return Route(points, samples, candidates, warnings, quality)


def geometry_anchors(route: Route, tolerance: float) -> list[int]:
    """Bounded RDP simplification; retain loops, endpoints and large reversals."""
    boundaries = [0]
    for index, sample in enumerate(route.samples[1:-1], 1):
        if sample.distance_m - route.samples[boundaries[-1]].distance_m >= 250:
            boundaries.append(index)
    boundaries.append(len(route.points) - 1)
    keep = set(boundaries)
    stack = list(zip(boundaries, boundaries[1:]))
    while stack:
        left, right = stack.pop()
        if right <= left + 1:
            continue
        a, b = route.points[left], route.points[right]
        cosine = math.cos(math.radians(a[0]))
        scale = math.pi / 180 * 6371008.8
        bx, by = longitude_delta(a[1], b[1]) * cosine * scale, (b[0] - a[0]) * scale
        length_sq = bx * bx + by * by
        farthest, error, reversal, previous_ratio = left, -1.0, None, 0.0
        for index in range(left + 1, right + 1):
            p = route.points[index]
            px, py = longitude_delta(a[1], p[1]) * cosine * scale, (p[0] - a[0]) * scale
            projection = (px * bx + py * by) / length_sq if length_sq else 0
            if length_sq and reversal is None and projection <= previous_ratio:
                reversal = max(left + 1, index - 1)
            previous_ratio = projection
            ratio = max(0.0, min(1.0, projection))
            deviation = math.hypot(px - ratio * bx, py - ratio * by)
            if index < right and deviation > error:
                farthest, error = index, deviation
        # A zero-length chord must never collapse a closed loop.
        if reversal is not None:
            farthest = reversal
        if reversal is not None or error > tolerance or length_sq < 1e-6:
            keep.add(farthest)
            stack.extend(((left, farthest), (farthest, right)))
    return sorted(keep)


def prepare_route(route: Route, distance_tolerance_m=DEFAULTS["distance_tolerance_m"],
                  elevation_spike_m=DEFAULTS["elevation_spike_m"]) -> Route:
    tolerance = number(distance_tolerance_m, "distance_tolerance_m")
    fit_distance = (route.diagnostics or {}).get("distance_source") == "fit_recorded"
    if fit_distance and tolerance:
        raise InputError("FIT recorded distance requires distance_tolerance_m=0; "
                         "geometry simplification would replace the device distance")
    spike = number(elevation_spike_m, "elevation_spike_m")
    warnings = list(route.warnings or [])
    samples = list(route.samples)
    corrected = []
    if spike:
        for index in range(1, len(samples) - 1):
            a, p, b = route.samples[index - 1:index + 2]
            left, right = p.distance_m - a.distance_m, b.distance_m - p.distance_m
            estimate = a.elevation_m + (b.elevation_m - a.elevation_m) * left / (left + right)
            up, down = p.elevation_m - a.elevation_m, p.elevation_m - b.elevation_m
            if (left + right <= 50 and up * down > 0
                    and abs(p.elevation_m - estimate) >= spike
                    and abs(up) / left > 2 and abs(down) / right > 2
                    and abs(a.elevation_m - b.elevation_m) < spike / 2):
                corrected.append((index, estimate))
        # Adjacent flagged points are ambiguous terrain or multi-point corruption.
        indices = {index for index, _ in corrected}
        corrected = [(i, z) for i, z in corrected if i - 1 not in indices and i + 1 not in indices]
        for index, elevation in corrected:
            samples[index] = Sample(samples[index].distance_m, elevation)
    gaps = [b.distance_m - a.distance_m for a, b in zip(route.samples, route.samples[1:])]
    trial_tolerance = tolerance or 5.0
    anchors = geometry_anchors(route, trial_tolerance)
    trial_distance = sum(haversine(route.points[a], route.points[b]) for a, b in zip(anchors, anchors[1:]))
    points = [(p[0], p[1], s.elevation_m) for p, s in zip(route.points, samples)]
    if tolerance:
        distances = [0.0] * len(samples)
        for left, right in zip(anchors, anchors[1:]):
            a, b = points[left], points[right]
            length = haversine(a, b)
            cosine = math.cos(math.radians(a[0]))
            bx, by = longitude_delta(a[1], b[1]) * cosine, b[0] - a[0]
            length_sq = bx * bx + by * by
            for index in range(left + 1, right + 1):
                p = route.points[index]
                px, py = longitude_delta(a[1], p[1]) * cosine, p[0] - a[0]
                ratio = 1.0 if index == right else (px * bx + py * by) / length_sq
                distances[index] = distances[left] + length * ratio
                if index != right:
                    points[index] = (
                        a[0] + (b[0] - a[0]) * ratio,
                        (a[1] + longitude_delta(a[1], b[1]) * ratio + 180) % 360 - 180,
                        samples[index].elevation_m,
                    )
        samples = [Sample(x, s.elevation_m) for x, s in zip(distances, samples)]
        warnings.append(f"Distance simplification applied ({tolerance:g} m tolerance): "
                        f"{route.total_m:.1f} -> {samples[-1].distance_m:.1f} m; review small switchbacks and CP positions.")
    elif not fit_distance and route.total_m - trial_distance > max(10, route.total_m * 0.01):
        warnings.append(f"Distance sensitivity: 5 m simplification would reduce {route.total_m:.1f} "
                        f"to {trial_distance:.1f} m. This may be drift OR real turns; distance is unchanged.")
    if corrected:
        warnings.append(f"Corrected {len(corrected)} isolated elevation spike(s); inspect diagnostics before use.")
    diagnostics = {
        "quality_flagged_points": 0, "quality_metadata_points": 0, "invalid_quality_fields": 0,
        **(route.diagnostics or {}),
        "original_distance_m": route.total_m,
        "processed_distance_m": samples[-1].distance_m,
        "distance_removed_m": route.total_m - samples[-1].distance_m,
        "spacing_min_m": min(gaps), "spacing_median_m": median(gaps), "spacing_max_m": max(gaps),
        "distance_trial_tolerance_m": trial_tolerance, "distance_trial_m": trial_distance,
        "geometry_vertices": len(anchors) if tolerance else len(points),
        "elevation_spikes_corrected": len(corrected),
        "elevation_spike_indices": [index for index, _ in corrected],
        "original_ascent_m": sum(max(0, b.elevation_m - a.elevation_m)
                                 for a, b in zip(route.samples, route.samples[1:])),
        "cleaned_ascent_m": sum(max(0, b.elevation_m - a.elevation_m)
                                for a, b in zip(samples, samples[1:])),
    }
    if diagnostics.get("quality_flagged_points") or diagnostics.get("invalid_quality_fields"):
        warnings.append("GPX contains low-quality or invalid positioning metadata; points were not automatically removed.")
    return Route(points, samples, route.candidates, warnings, diagnostics)


def interpolate(samples: list[Sample], distance: float) -> float:
    index = bisect_right(samples, distance, key=lambda p: p.distance_m) - 1
    index = max(0, min(index, len(samples) - 2))
    a, b = samples[index:index + 2]
    ratio = (distance - a.distance_m) / (b.distance_m - a.distance_m)
    return a.elevation_m + ratio * (b.elevation_m - a.elevation_m)


def smooth_profile(route: Route, sample_m=DEFAULTS["sample_m"],
                   smoothing_m=DEFAULTS["smoothing_m"]) -> list[Sample]:
    step = number(sample_m, "sample_m", strictly_positive=True)
    window = number(smoothing_m, "smoothing_m")
    if step < route.total_m / 2_000_000:
        raise InputError("Sampling would exceed 2,000,000 points; increase sample_m")
    count = math.ceil(route.total_m / step)
    if 0 < window < 16 * math.ulp(route.total_m):
        raise InputError("smoothing window is too small for this route's numeric precision; "
                         "increase smoothing_m/ascent_smoothing_m or use 0 to disable smoothing")
    distances = [index * step for index in range(count)] + [route.total_m]
    resampled = [Sample(x, interpolate(route.samples, x)) for x in distances]
    if window == 0:
        return resampled
    areas = [0.0]
    source = route.samples
    for a, b in zip(source, source[1:]):
        areas.append(areas[-1] + (b.distance_m - a.distance_m) * (a.elevation_m + b.elevation_m) / 2)

    def average(left, right):
        first = max(0, min(bisect_right(source, left, key=lambda p: p.distance_m) - 1, len(source) - 2))
        last = max(0, min(bisect_right(source, right, key=lambda p: p.distance_m) - 1, len(source) - 2))
        start, end = interpolate(source, left), interpolate(source, right)
        if first == last:
            return (start + end) / 2
        # Integrate boundary pieces locally to avoid cancellation in tiny final windows.
        a, b = source[first + 1], source[last]
        area = math.fsum(((a.distance_m - left) * (start + a.elevation_m) / 2,
                          areas[last] - areas[first + 1],
                          (right - b.distance_m) * (b.elevation_m + end) / 2))
        return area / (right - left)

    result = []
    for x in distances:
        radius = min(window / 2, x, route.total_m - x)
        left, right = x - radius, x + radius
        elevation = interpolate(source, x) if radius <= 16 * math.ulp(route.total_m) else average(left, right)
        result.append(Sample(x, elevation))
    return result


def ascent_profile(route: Route, sample_m=DEFAULTS["sample_m"],
                   smoothing_m=DEFAULTS["ascent_smoothing_m"], method="hysteresis",
                   threshold_m=DEFAULTS["ascent_threshold_m"]) -> list[Sample]:
    if method not in ("hysteresis", "window"):
        raise InputError("ascent_method must be hysteresis or window")
    threshold = number(threshold_m, "ascent_threshold_m")
    window = number(smoothing_m, "ascent_smoothing_m")
    smoothed = smooth_profile(route, sample_m, window)
    if method == "window":
        return smoothed
    # Keep source vertices when unblurred: the display grid must not erase short hills.
    source = smoothed if window else route.samples
    if threshold == 0:
        return list(source)
    anchors = [0]
    low = high = extreme = 0
    direction = 0
    for index, sample in enumerate(source[1:], 1):
        z = sample.elevation_m
        if not direction:
            if z < source[low].elevation_m:
                low = index
            if z > source[high].elevation_m:
                high = index
            if source[high].elevation_m - source[low].elevation_m >= threshold:
                direction = 1 if high > low else -1
                first = low if direction == 1 else high
                if first:
                    anchors.append(first)
                extreme = high if direction == 1 else low
        elif direction * (z - source[extreme].elevation_m) >= 0:
            extreme = index
        elif direction * (source[extreme].elevation_m - z) >= threshold:
            anchors.append(extreme)
            direction = -direction
            extreme = index
    if direction and extreme > anchors[-1]:
        anchors.append(extreme)
    if anchors[-1] != len(source) - 1:
        anchors.append(len(source) - 1)
    result = [source[0]]
    for left, right in zip(anchors, anchors[1:]):
        start, end = source[left].elevation_m, source[right].elevation_m
        previous = start
        for index in range(left + 1, right + 1):
            z = source[index].elevation_m
            previous = min(end, max(previous, z)) if end >= start else max(end, min(previous, z))
            result.append(Sample(source[index].distance_m, previous))
    return result


def projection_options(route: Route, candidate: dict) -> list[dict]:
    lat, lon = candidate["lat"], candidate["lon"]
    cosine = math.cos(math.radians(lat))
    projections = []
    for index, (a, b) in enumerate(zip(route.points, route.points[1:])):
        ax, ay = math.radians(longitude_delta(lon, a[1])) * cosine * 6371008.8, math.radians(a[0] - lat) * 6371008.8
        bx, by = math.radians(longitude_delta(lon, b[1])) * cosine * 6371008.8, math.radians(b[0] - lat) * 6371008.8
        dx, dy = bx - ax, by - ay
        length_sq = dx * dx + dy * dy
        ratio = max(0.0, min(1.0, -(ax * dx + ay * dy) / length_sq)) if length_sq else 0.0
        distance = route.samples[index].distance_m + ratio * (
            route.samples[index + 1].distance_m - route.samples[index].distance_m
        )
        projections.append({"distance_m": distance, "offset_m": math.hypot(ax + ratio * dx, ay + ratio * dy)})
    nearest = min(item["offset_m"] for item in projections)
    nearby = sorted((p for p in projections if p["offset_m"] <= nearest + 20), key=lambda p: p["distance_m"])
    groups = [[nearby[0]]]
    for item in nearby[1:]:
        if item["distance_m"] - groups[-1][-1]["distance_m"] > 50:
            groups.append([])
        groups[-1].append(item)
    choices = [min(group, key=lambda p: p["offset_m"]) for group in groups]
    best = min(choices, key=lambda p: p["offset_m"])
    return [choice for choice in choices if abs(choice["distance_m"] - best["distance_m"]) > 100 or choice is best]


def station_fields(item: dict) -> dict:
    name = item.get("name")
    if not isinstance(name, str) or not name.strip():
        raise InputError("Every checkpoint needs a non-empty name")
    rest = number(item.get("rest_minutes", 0), "rest_minutes") * 60
    cutoff = duration(item["cutoff"], "cutoff") if item.get("cutoff") is not None else None
    return {"name": name.strip(), "rest_seconds": rest, "cutoff_seconds": cutoff}


def resolve_checkpoints(route: Route, config: dict) -> tuple[list[dict], float, list[str]]:
    warnings = []
    fit_distance = (route.diagnostics or {}).get("distance_source") == "fit_recorded"
    if "checkpoints" in config:
        items = config["checkpoints"]
        if not isinstance(items, list) or not items:
            raise InputError("checkpoints must contain CPs and an explicit final finish distance")
        if "cp_selection" in config or "checkpoint_overrides" in config:
            raise InputError("Use fields on manual checkpoints instead of CP selection/overrides")
        cps = []
        previous = -1.0
        for index, item in enumerate(items):
            keys(item, CP_KEYS, "checkpoint")
            distance = number(item.get("distance_km"), "distance_km") * 1000
            if distance <= previous:
                raise InputError("Checkpoint distances must be strictly increasing")
            previous = distance
            cps.append({"id": f"manual:{index + 1}", "distance_m": distance,
                        "official_distance_km": None if fit_distance else distance / 1000,
                        **station_fields(item)})
        official_total = cps[-1]["distance_m"]
        if official_total <= 0:
            raise InputError("Finish distance must be positive")
        tolerance = max(100, route.total_m * 0.005)
        alignment = config.get("distance_alignment", "confirm")
        if alignment not in ("confirm", "scale"):
            raise InputError("distance_alignment must be confirm or scale")
        if abs(official_total - route.total_m) > tolerance and alignment != "scale":
            raise InputError("Official/route distance mismatch; confirm then set distance_alignment=scale",
                             {"official_m": official_total, "gpx_m": route.total_m,
                              "scale": route.total_m / official_total})
        scale = route.total_m / official_total if alignment == "scale" else 1.0
        for cp in cps:
            cp["distance_m"] *= scale
        cps[-1]["distance_m"] = route.total_m
        if len(cps) > 1 and cps[-2]["distance_m"] >= route.total_m:
            raise InputError("An intermediate checkpoint falls beyond the route finish")
        if alignment == "scale":
            warnings.append(f"Confirmed official-distance mapping: {scale:.8f} route metres per official metre.")
    else:
        scale = 1.0
        candidates = route.candidates
        if "cp_selection" in config:
            ids = config["cp_selection"]
            if not isinstance(ids, list) or not ids or not all(isinstance(i, str) for i in ids) or len(ids) != len(set(ids)):
                raise InputError("cp_selection must be a non-empty list of unique candidate IDs")
            available = {p["id"]: p for p in candidates}
            if not set(ids) <= set(available):
                raise InputError("Unknown cp_selection IDs", list(available))
            selected = [available[i] for i in ids]
        else:
            selected = [p for p in candidates if p["recognized"]]
        if not selected:
            if candidates:
                raise InputError("Named route waypoints need confirmation via cp_selection, or supply checkpoints", candidates)
            raise InputError("No embedded CPs found; provide checkpoints with names and cumulative kilometres")
        overrides = config.get("checkpoint_overrides", {})
        if not isinstance(overrides, dict) or not set(overrides) <= {p["id"] for p in selected}:
            raise InputError("checkpoint_overrides must reference selected CP IDs")
        cps = []
        for candidate in selected:
            override = overrides.get(candidate["id"], {})
            keys(override, OVERRIDE_KEYS, "checkpoint override")
            item = {**candidate, **override}
            if "allow_off_route" in override and not isinstance(override["allow_off_route"], bool):
                raise InputError("allow_off_route must be boolean")
            endpoint = f'{candidate["name"]} {candidate["type"]}'
            combined = bool(re.search(r"起终点|起終點", endpoint)) or (
                bool(re.search(r"\bstart\b", endpoint, re.IGNORECASE))
                and bool(re.search(r"\bfinish\b", endpoint, re.IGNORECASE))
            )
            if combined and "distance_km" not in override:
                if any(haversine((item["lat"], item["lon"]), point) > 100
                       for point in (route.points[0], route.points[-1])):
                    raise InputError("Named combined start/finish must be within 100 m of both route endpoints; "
                                     "provide separate checkpoints or a distance_km override")
                fields = station_fields(item)
                # A shared venue is two route occurrences; its cutoff applies only at the finish.
                for suffix, position, label in (("start", 0.0, "起点"), ("finish", route.total_m, "终点")):
                    cps.append({
                        **fields, "id": f'{candidate["id"]}:{suffix}', "distance_m": position,
                        "name": f'{fields["name"]}（{label}）', "official_distance_km": None,
                        "cutoff_seconds": fields["cutoff_seconds"] if suffix == "finish" else None,
                    })
                continue
            if "distance_km" in override:
                position = number(override["distance_km"], "distance_km") * 1000
                if position > route.total_m:
                    raise InputError("CP distance override is beyond the route finish")
                # A distance override explicitly selects a route occurrence and position.
                warnings.append(f'{candidate["id"]}: confirmed position override at {position / 1000:.3f} route km.')
            elif re.search(r"\bstart\b|起点|起點", endpoint, re.IGNORECASE):
                position = 0.0
                if haversine((item["lat"], item["lon"]), route.points[0]) > 100:
                    raise InputError("Named start is over 100 m from route start; provide distance_km override")
            elif re.search(r"\bfinish\b|终点|終點", endpoint, re.IGNORECASE):
                position = route.total_m
                if haversine((item["lat"], item["lon"]), route.points[-1]) > 100:
                    raise InputError("Named finish is over 100 m from route finish; provide distance_km override")
            else:
                options = projection_options(route, candidate)
                if len(options) > 1:
                    raise InputError(f'{candidate["id"]}: ambiguous CP route occurrence; set distance_km override', options)
                nearest = options[0]
                if nearest["offset_m"] > 100:
                    if not override.get("allow_off_route", False):
                        raise InputError(f'{candidate["id"]}: CP is over 100 m off-route; confirm before allow_off_route', nearest)
                    warnings.append(f'{candidate["id"]}: confirmed off-route CP ({nearest["offset_m"]:.1f} m).')
                position = nearest["distance_m"]
            cps.append({"id": candidate["id"], "distance_m": position,
                        "official_distance_km": None, **station_fields(item)})
        cps.sort(key=lambda cp: cp["distance_m"])
    if cps[0]["distance_m"] > 0.001:
        cps.insert(0, {"id": "start", "name": "起点", "distance_m": 0.0,
                       "official_distance_km": 0.0 if "checkpoints" in config and not fit_distance else None,
                       "rest_seconds": 0.0, "cutoff_seconds": None})
    if route.total_m - cps[-1]["distance_m"] > 0.001:
        cps.append({"id": "finish", "name": "终点", "distance_m": route.total_m,
                    "official_distance_km": None, "rest_seconds": 0.0, "cutoff_seconds": None})
    if any(b["distance_m"] - a["distance_m"] < 0.001 for a, b in zip(cps, cps[1:])):
        raise InputError("Multiple CPs occupy the same route position; deduplicate or disambiguate them")
    if cps[0]["rest_seconds"] or cps[-1]["rest_seconds"]:
        raise InputError("Start/finish rest_minutes must be zero; no departure rest is counted there")
    return cps, scale, warnings


def grade_bin(grade_percent: float) -> int:
    if grade_percent <= -15:
        return 0
    if grade_percent <= -10:
        return 1
    if grade_percent <= -5:
        return 2
    if grade_percent < 5:
        return 3
    if grade_percent < 10:
        return 4
    if grade_percent < 15:
        return 5
    return 6


def profile_section(profile: list[Sample], left: float, right: float) -> list[Sample]:
    if right == left:
        return [Sample(left, interpolate(profile, left))]
    start = bisect_right(profile, left, key=lambda p: p.distance_m)
    end = bisect_left(profile, right, key=lambda p: p.distance_m)
    return [Sample(left, interpolate(profile, left)), *profile[start:end],
            Sample(right, interpolate(profile, right))]


def section_stats(profile: list[Sample], left: float, right: float, factor: float, water: float,
                  gain_profile: list[Sample] | None = None) -> dict:
    segment = profile_section(profile, left, right)
    gain_segment = segment if gain_profile is None else profile_section(gain_profile, left, right)
    ascent = sum(max(0, b.elevation_m - a.elevation_m) for a, b in zip(gain_segment, gain_segment[1:]))
    descent = sum(max(0, a.elevation_m - b.elevation_m) for a, b in zip(gain_segment, gain_segment[1:]))
    bins = [0.0] * 7
    for a, b in zip(segment, segment[1:]):
        dz, dx = b.elevation_m - a.elevation_m, b.distance_m - a.distance_m
        bins[grade_bin(100 * dz / dx)] += dx
    distance = right - left
    eq = distance / 1000 + ascent / 100 * factor
    return {
        "segment_distance_m": distance, "ascent_m": ascent, "descent_m": descent,
        "eq_distance_km": eq, "segment_water_ml": eq / 10 * water,
        "grade_fractions": [b / distance if distance else 0.0 for b in bins],
        "profile": [[p.distance_m, p.elevation_m] for p in segment],
    }


def fatigue_exponent(rate: float) -> float:
    return 1 + math.log2(1 + rate)


def target_times(config: dict, step: float) -> list[float]:
    if "targets" in config:
        values = config["targets"]
        if not isinstance(values, list) or not values:
            raise InputError("targets must be a non-empty list of H:MM durations")
        times = [duration(value, "target") for value in values]
    else:
        center = duration(config.get("target"), "target")
        times = [center + offset * step * 60 for offset in (-2, -1, 0, 1, 2)]
    if any(value <= 0 for value in times) or len(set(times)) != len(times):
        raise InputError("Target durations must be positive and unique; supply an explicit targets list")
    return sorted(times)


def water_options(plan: dict, config: dict, require_rate=True) -> tuple[dict, float | None, float, dict]:
    targets = plan["targets_seconds"]
    if "water_target" in config:
        selected = duration(config["water_target"], "water_target")
        if selected not in targets:
            raise InputError("water_target must match a displayed target")
    elif len(targets) == 1:
        selected = targets[0]
    else:
        raise InputError("water_target is required when there are multiple targets")
    schedule = next(item for item in plan["schedules"] if item["target_seconds"] == selected)
    if "water_ml_per_hour" in config:
        rate = number(config["water_ml_per_hour"], "water_ml_per_hour", strictly_positive=True)
    elif require_rate:
        raise InputError("water_ml_per_hour is required for time-based water")
    else:
        rate = None
    buffer_minutes = number(config.get("water_buffer_minutes", 0), "water_buffer_minutes")
    overrides = config.get("water_rate_overrides", {})
    allowed = {cp["id"] for cp in plan["checkpoints"][:-1]}
    if not isinstance(overrides, dict) or not set(overrides) <= allowed:
        raise InputError("water_rate_overrides must reference departure checkpoint IDs")
    rates = {key: number(value, "water_rate_overrides", strictly_positive=True)
             for key, value in overrides.items()}
    return schedule, rate, buffer_minutes, rates


def water_midpoint(route: Route, distance: float) -> tuple[float, float]:
    index = max(0, min(bisect_right(route.samples, distance, key=lambda item: item.distance_m) - 1,
                       len(route.samples) - 2))
    left, right = route.samples[index:index + 2]
    ratio = (distance - left.distance_m) / (right.distance_m - left.distance_m)
    first, second = route.points[index:index + 2]
    latitude = first[0] + (second[0] - first[0]) * ratio
    longitude = (first[1] + longitude_delta(first[1], second[1]) * ratio + 180) % 360 - 180
    return round(latitude, 4), round(longitude, 4)


def water_forecast_context(plan: dict, route: Route, config: dict) -> tuple[dict, str]:
    schedule, _, _, _ = water_options(plan, config, require_rate=False)
    start_text = plan["parameters"]["start_time"]
    if not re.fullmatch(r"\d{4}-\d\d-\d\d[ T]\d\d:\d\d", start_text):
        raise InputError("start_time must include the race date for weather; use manual water_weather otherwise")
    zone_name = config.get("water_timezone")
    if not isinstance(zone_name, str) or not zone_name:
        raise InputError("water_timezone must be an IANA timezone for weather; use manual water_weather otherwise")
    try:
        zone = ZoneInfo(zone_name)
    except (ZoneInfoNotFoundError, ValueError):
        raise InputError("water_timezone must be a valid IANA timezone; use manual water_weather otherwise") from None
    local_start = datetime.fromisoformat(start_text)
    possibilities = {}
    for fold in (0, 1):
        candidate = local_start.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
        if candidate.astimezone(zone).replace(tzinfo=None) == local_start:
            possibilities[candidate.timestamp()] = candidate
    if len(possibilities) != 1:
        raise InputError("start_time is ambiguous or nonexistent in water_timezone; use manual water_weather")
    start_utc = next(iter(possibilities.values()))
    segments = []
    checkpoints = plan["checkpoints"]
    timings = schedule["checkpoints"]
    try:
        for index, (departure, arrival) in enumerate(zip(checkpoints, checkpoints[1:])):
            latitude, longitude = water_midpoint(route, (departure["distance_m"] + arrival["distance_m"]) / 2)
            start = start_utc + timedelta(seconds=timings[index]["departure_seconds"])
            end = start_utc + timedelta(seconds=timings[index + 1]["arrival_seconds"])
            segments.append({
                "from_id": departure["id"], "from_name": departure["name"],
                "to_id": arrival["id"], "to_name": arrival["name"],
                "latitude": latitude, "longitude": longitude,
                "start_time": start.isoformat(), "end_time": end.isoformat(),
            })
    except (OverflowError, ValueError):
        raise InputError("water forecast dates are outside the supported range; use manual water_weather") from None
    context = {
        "route_sha256": plan["source"]["sha256"], "target_seconds": schedule["target_seconds"],
        "start_time": start_text, "timezone": zone_name, "segments": segments,
    }
    encoded = json.dumps(context, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return context, hashlib.sha256(encoded.encode("utf-8")).hexdigest()


WEATHER_FIELDS = ("temperature_2m", "relative_humidity_2m", "wind_speed_10m", "precipitation_probability")


def weather_hours(segment: dict) -> range:
    start = datetime.fromisoformat(segment["start_time"]).timestamp()
    end = datetime.fromisoformat(segment["end_time"]).timestamp()
    first = math.floor(start / 3600) * 3600
    last = (math.ceil(end / 3600) - 1) * 3600
    if last < first or last - first > 16 * 24 * 3600:
        raise ValueError("invalid forecast interval")
    return range(first, last + 1, 3600)


def weather_values(item: dict) -> dict:
    values = {
        "temperature_2m": number(item["temperature_2m"], "weather temperature_2m", minimum=-273.15),
        "relative_humidity_2m": number(item["relative_humidity_2m"], "weather relative_humidity_2m"),
        "wind_speed_10m": number(item["wind_speed_10m"], "weather wind_speed_10m"),
        "precipitation_probability": number(item["precipitation_probability"], "weather precipitation_probability"),
    }
    if values["relative_humidity_2m"] > 100 or values["precipitation_probability"] > 100:
        raise ValueError("invalid weather percentage")
    return values


def fetch_water_forecast(context: dict, context_sha256: str) -> dict:
    segments = []
    for segment in context["segments"]:
        query = urlencode({
            "latitude": segment["latitude"], "longitude": segment["longitude"],
            "hourly": ",".join(WEATHER_FIELDS), "forecast_days": 16,
            "timezone": "GMT", "timeformat": "unixtime",
        })
        request = Request("https://api.open-meteo.com/v1/forecast?" + query,
                          headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=10) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError, UnicodeError, json.JSONDecodeError):
            raise InputError("Weather forecast unavailable; retry or provide manual water_weather") from None
        try:
            hourly = payload["hourly"]
            times = hourly["time"]
            if (not isinstance(times, list) or not times
                    or any(isinstance(value, bool) or not isinstance(value, (int, float))
                           or not math.isfinite(value) for value in times)
                    or any(not isinstance(hourly[field], list) or len(hourly[field]) != len(times)
                           for field in WEATHER_FIELDS)):
                raise ValueError
            by_time = {int(value): index for index, value in enumerate(times)}
            if len(by_time) != len(times):
                raise ValueError
            selected = []
            for stamp in weather_hours(segment):
                index = by_time[stamp]
                values = weather_values({field: hourly[field][index] for field in WEATHER_FIELDS})
                selected.append({"time": datetime.fromtimestamp(stamp, timezone.utc).isoformat(), **values})
            segments.append({**segment, "hourly": selected})
        except (KeyError, TypeError, ValueError, OverflowError, OSError, InputError):
            raise InputError("Weather forecast incomplete or outside its range; provide manual water_weather") from None
    return {
        "source": "open-meteo", "confirmed": False,
        "context_sha256": context_sha256,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "timezone": context["timezone"], "target_seconds": context["target_seconds"],
        "segments": segments,
    }


def validate_water_weather(plan: dict, route: Route, config: dict) -> dict:
    weather = config.get("water_weather")
    if not isinstance(weather, dict):
        raise InputError("water_weather must contain confirmed forecast or manual information")
    if weather.get("confirmed") is not True:
        raise InputError("water_weather must be explicitly confirmed")
    source = weather.get("source")
    if source == "manual":
        if not isinstance(weather.get("description"), str) or not weather["description"].strip():
            raise InputError("manual water_weather requires a non-empty description")
    elif source == "open-meteo":
        context, fingerprint = water_forecast_context(plan, route, config)
        if weather.get("context_sha256") != fingerprint:
            raise InputError("water_weather no longer matches this route, target or start time")
        try:
            retrieved = datetime.fromisoformat(weather["retrieved_at"])
            segments = weather["segments"]
            if (retrieved.tzinfo is None or retrieved.utcoffset() is None
                    or weather["timezone"] != context["timezone"]
                    or weather["target_seconds"] != context["target_seconds"]
                    or not isinstance(segments, list) or len(segments) != len(context["segments"])):
                raise ValueError
            for item, expected in zip(segments, context["segments"]):
                if not isinstance(item, dict) or any(item.get(key) != expected[key] for key in expected):
                    raise ValueError
                hourly = item["hourly"]
                stamps = list(weather_hours(expected))
                if not isinstance(hourly, list) or len(hourly) != len(stamps):
                    raise ValueError
                for entry, stamp in zip(hourly, stamps):
                    if not isinstance(entry, dict) or entry.get("time") != datetime.fromtimestamp(
                        stamp, timezone.utc
                    ).isoformat():
                        raise ValueError
                    weather_values(entry)
        except (KeyError, TypeError, ValueError, OverflowError, OSError, InputError):
            raise InputError("water_weather forecast is incomplete; request a fresh forecast")
    else:
        raise InputError("water_weather source must be open-meteo or manual")
    return weather


def apply_time_water(plan: dict, route: Route, config: dict) -> None:
    schedule, rate, buffer_minutes, overrides = water_options(plan, config)
    weather = validate_water_weather(plan, route, config)
    checkpoints = plan["checkpoints"]
    for cp in checkpoints:
        cp["water_ml"] = 0.0
        cp["segment_water_ml"] = 0.0
        cp["water_rate_ml_per_hour"] = None
    for index, cp in enumerate(checkpoints[:-1]):
        outgoing_rate = overrides.get(cp["id"], rate)
        hours = schedule["checkpoints"][index + 1]["moving_seconds"] / 3600 + buffer_minutes / 60
        amount = hours * outgoing_rate
        if not math.isfinite(amount):
            raise InputError("time-based water amount must be finite")
        cp["water_ml"] = amount
        cp["water_rate_ml_per_hour"] = outgoing_rate
        checkpoints[index + 1]["segment_water_ml"] = amount
    plan["parameters"].update({
        "water_mode": "time", "water_target_seconds": schedule["target_seconds"],
        "water_ml_per_hour": rate, "water_buffer_minutes": buffer_minutes,
        "water_rate_overrides": overrides, "water_weather_source": weather["source"],
        "water_weather_retrieved_at": weather.get("retrieved_at"),
    })
    plan["water_weather"] = weather
    plan["warnings"] = [
        warning for warning in plan["warnings"] if warning != "水量仅供比较赛段差异，并非个人饮水建议。"
    ]
    plan["warnings"].append("水量按确认的速率和目标时间估算；请核实个人需要与下一站补水条件。")
    if weather["source"] == "open-meteo":
        plan["warnings"].append("天气为赛段中点预报，可能无法反映整段地形或实际天气；请赛前更新。")


def build_plan(path: Path, config: dict, *, defer_water=False) -> dict:
    keys(config, CONFIG_KEYS, "configuration")
    water_mode = config.get("water_mode", "distance")
    if water_mode not in ("distance", "time"):
        raise InputError("water_mode must be distance or time")
    time_options = {"water_target", "water_ml_per_hour", "water_buffer_minutes",
                    "water_rate_overrides", "water_timezone", "water_weather"}
    if water_mode != "time" and time_options.intersection(config):
        raise InputError("water_mode must be time when time-based water options are supplied")
    output_formats = config.get("output_formats", ["svg"])
    if (not isinstance(output_formats, list) or not output_formats
            or any(fmt not in ("svg", "html", "csv", "json") for fmt in output_formats)
            or len(set(output_formats)) != len(output_formats)):
        raise InputError("output_formats must be a non-empty list of unique formats: svg, html, csv, json")
    parameters = {
        key: number(config.get(key, value), key,
                    strictly_positive=key in ("sample_m", "target_step_minutes"))
        for key, value in DEFAULTS.items()
    }
    parameters["output_formats"] = list(output_formats)
    parameters["ascent_method"] = config.get("ascent_method", "hysteresis")
    if parameters["ascent_method"] not in ("hysteresis", "window"):
        raise InputError("ascent_method must be hysteresis or window")
    if parameters["fatigue_rate"] > 1:
        raise InputError("fatigue_rate must be between 0 and 1")
    pace_basis = config.get("pace_basis", "distance")
    if pace_basis not in ("distance", "equivalent"):
        raise InputError("pace_basis must be distance or equivalent")
    secondary_display = config.get(
        "secondary_display", "equivalent_pace" if pace_basis == "equivalent" else "pace"
    )
    if secondary_display not in ("pace", "equivalent_pace", "arrival_time"):
        raise InputError("secondary_display must be pace, equivalent_pace, or arrival_time")
    if secondary_display != "arrival_time":
        pace_basis = "equivalent" if secondary_display == "equivalent_pace" else "distance"
    parameters["pace_basis"] = pace_basis
    parameters["secondary_display"] = secondary_display
    if config.get("distance_alignment", "confirm") not in ("confirm", "scale"):
        raise InputError("distance_alignment must be confirm or scale")
    if "name" in config and (not isinstance(config["name"], str) or not config["name"].strip()):
        raise InputError("name must be a non-empty string")
    start_time = config.get("start_time", "06:00")
    if not isinstance(start_time, str) or not re.fullmatch(r"(?:\d{4}-\d\d-\d\d[ T])?\d\d:\d\d", start_time):
        raise InputError("start_time must be HH:MM or YYYY-MM-DD HH:MM (local race time)")
    try:
        time(int(start_time[-5:-3]), int(start_time[-2:]))
        if len(start_time) > 5:
            datetime.fromisoformat(start_time)
    except ValueError as error:
        raise InputError("Invalid start_time date or time") from error
    parameters["start_time"] = start_time
    route = load_route(path, config.get("track_index"), config.get("use_kml_altitudes", False))
    route = prepare_route(route, parameters["distance_tolerance_m"], parameters["elevation_spike_m"])
    profile = smooth_profile(route, parameters["sample_m"], parameters["smoothing_m"])
    gain_profile = ascent_profile(route, parameters["sample_m"], parameters["ascent_smoothing_m"],
                                  parameters["ascent_method"], parameters["ascent_threshold_m"])
    cps, scale, cp_warnings = resolve_checkpoints(route, config)
    cumulative_eq = 0.0
    for index, cp in enumerate(cps):
        left = cps[index - 1]["distance_m"] if index else 0.0
        cp.update(section_stats(profile, left, cp["distance_m"],
                                parameters["ascent_km_per_100m"], parameters["water_ml_per_10km"], gain_profile))
        cumulative_eq += cp["eq_distance_km"]
        cp["cumulative_eq_distance_km"] = cumulative_eq
    for index, cp in enumerate(cps):
        # Supplies at a station are for the next leg; terrain statistics describe the incoming leg.
        cp["water_ml"] = cps[index + 1]["segment_water_ml"] if index + 1 < len(cps) else 0.0
    targets = target_times(config, parameters["target_step_minutes"])
    rest_total = sum(cp["rest_seconds"] for cp in cps)
    exponent = fatigue_exponent(parameters["fatigue_rate"])
    schedules = []
    for target in targets:
        if target <= rest_total:
            raise InputError("Target duration must exceed total station rest time")
        moving_target = target - rest_total
        prior_moving, prior_rest = 0.0, 0.0
        times = []
        for index, cp in enumerate(cps):
            cumulative_moving = moving_target * (cp["cumulative_eq_distance_km"] / cumulative_eq) ** exponent
            moving = cumulative_moving - prior_moving
            arrival = cumulative_moving + prior_rest
            departure = arrival + cp["rest_seconds"]
            cutoff = cp["cutoff_seconds"]
            status = "not_checked" if cutoff is None else (
                "arrival_late" if arrival > cutoff + 1e-7 else (
                    "departure_late" if departure > cutoff + 1e-7 else "on_time"
                )
            )
            times.append({
                "arrival_seconds": arrival, "departure_seconds": departure,
                "moving_seconds": moving,
                "eq_pace_seconds_per_km": moving / cp["eq_distance_km"] if index else None,
                "distance_pace_seconds_per_km": moving / (cp["segment_distance_m"] / 1000) if index else None,
                "pace_seconds_per_km": moving / (
                    cp["eq_distance_km"] if pace_basis == "equivalent" else cp["segment_distance_m"] / 1000
                ) if index else None,
                "cutoff_status": status,
            })
            prior_moving = cumulative_moving
            prior_rest += cp["rest_seconds"]
        schedules.append({"target_seconds": target, "checkpoints": times})
    route_stats = section_stats(profile, 0, route.total_m, parameters["ascent_km_per_100m"],
                                parameters["water_ml_per_10km"], gain_profile)
    warnings = list(route.warnings or []) + cp_warnings
    if "target" in config and "targets" in config:
        warnings.append("同时提供 target 和 targets：使用 targets，忽略 target；如需中央目标，请移除 targets。")
    if any(cp["cutoff_seconds"] is None for cp in cps[1:]):
        warnings.append("部分或全部站点未提供关门时间，未校核这些站点。")
    warnings.extend([
        "模型未计入技术路面、陡下坡额外负担、天气和个人肌力差异；请结合赛事规程判断。",
        "水量仅供比较赛段差异，并非个人饮水建议。",
        "插值不增加原始测量精度；爬升统计依赖海拔数据、过滤方法与阈值。",
    ])
    plan = {
        "schema_version": 2,
        "name": config.get("name", Path(path).stem),
        "source": {"filename": Path(path).name, "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()},
        "article": {"title": ARTICLE_TITLE, "author": "耐力学社 / Pili（表哥）", "url": ARTICLE_URL},
        "configuration": config,
        "parameters": {**parameters, "fatigue_exponent": exponent, "rest_total_seconds": rest_total},
        "route": {"distance_m": route.total_m, "distance_scale": scale,
                  "ascent_m": route_stats["ascent_m"], "descent_m": route_stats["descent_m"],
                  "eq_distance_km": cumulative_eq,
                  "original_points": len(route.points), "sampled_points": len(profile),
                  "diagnostics": route.diagnostics,
                  "grade_fractions": route_stats["grade_fractions"]},
        "checkpoints": cps, "targets_seconds": targets, "schedules": schedules, "warnings": warnings,
    }
    if water_mode == "time" and not defer_water:
        apply_time_water(plan, route, config)
    return plan


def inspect_route(path: Path, track_index=None, sample_m=DEFAULTS["sample_m"],
                  smoothing_m=DEFAULTS["smoothing_m"], ascent_smoothing_m=DEFAULTS["ascent_smoothing_m"],
                  use_kml_altitudes=False, ascent_method="hysteresis",
                  ascent_threshold_m=DEFAULTS["ascent_threshold_m"],
                  elevation_spike_m=DEFAULTS["elevation_spike_m"],
                  distance_tolerance_m=DEFAULTS["distance_tolerance_m"]) -> dict:
    route = load_route(path, track_index, use_kml_altitudes)
    route = prepare_route(route, distance_tolerance_m, elevation_spike_m)
    profile = smooth_profile(route, sample_m, smoothing_m)
    gain_profile = ascent_profile(route, sample_m, ascent_smoothing_m, ascent_method, ascent_threshold_m)
    stats = section_stats(profile, 0, route.total_m, DEFAULTS["ascent_km_per_100m"],
                          DEFAULTS["water_ml_per_10km"], gain_profile)
    candidates = []
    for candidate in route.candidates:
        candidates.append({**candidate, "projection_options": projection_options(route, candidate)})
    return {
        "distance_m": route.total_m, "ascent_m": stats["ascent_m"], "descent_m": stats["descent_m"],
        "sample_m": sample_m, "smoothing_m": smoothing_m, "ascent_smoothing_m": ascent_smoothing_m,
        "ascent_method": ascent_method, "ascent_threshold_m": ascent_threshold_m,
        "elevation_spike_m": elevation_spike_m, "distance_tolerance_m": distance_tolerance_m,
        "diagnostics": route.diagnostics,
        "cp_candidates": candidates, "warnings": route.warnings or [],
    }


STATUS_LABELS = {
    "not_checked": "未校核", "on_time": "关门内",
    "arrival_late": "到站超时", "departure_late": "出站超时",
}
BASE_COLUMNS = [
    ("累积\n距离", 110), ("坡度\n分布", 120), ("肖像图", 130), ("距离", 78),
    ("爬升", 78), ("下降", 78), ("水", 88), ("位置", 240),
]


def wrap_text(text: str, units: int) -> list[str]:
    result, line, used = [], "", 0
    for char in text:
        size = 2 if ord(char) > 255 else 1
        if char == "\n" or (line and used + size > units):
            result.append(line)
            line, used = "", 0
        if char != "\n":
            line += char
            used += size
    if line or not result:
        result.append(line)
    return result


def svg_text(x, y, lines, size=12, color="#111111", anchor="start", family="sans-serif", underline=False) -> str:
    spans = "".join(
        f'<tspan x="{x:.2f}" dy="{0 if i == 0 else size * 1.45:.2f}">{escape(str(line))}</tspan>'
        for i, line in enumerate(lines)
    )
    decoration = ' text-decoration="underline"' if underline else ""
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-size="{size}" '
        f'text-anchor="{anchor}" font-family="{family}"{decoration}>{spans}</text>'
    )


def graphic_frame(content, x, y, width, height, label, as_group) -> str:
    if as_group:
        return f'<g transform="translate({x} {y})" role="img"><title>{label}</title>{content}</g>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{label}">{content}</svg>'
    )


def histogram_svg(fractions, x=0, y=0, width=90, height=42, as_group=False) -> str:
    bars = []
    labels = ("≤-15%", "-15~-10%", "-10~-5%", "-5~5%", "5~10%", "10~15%", "≥15%")
    for index, fraction in enumerate(fractions):
        bar_height = fraction * (height - 5)
        fill = "#ffffff" if index == 3 else "#111111"
        bars.append(
            f'<rect x="{index * width / 7 + 1:.2f}" y="{height - bar_height:.2f}" '
            f'width="{width / 7 - 2:.2f}" height="{bar_height:.2f}" fill="{fill}">'
            f'<title>{labels[index]}: {fraction:.1%}</title></rect>'
        )
    return graphic_frame("".join(bars), x, y, width, height, "坡度按距离加权的七档分布", as_group)


def profile_svg(profile, x=0, y=0, width=125, height=42, as_group=False) -> str:
    points = f"3,{height - 5} {width - 3},{height - 5}"
    if len(profile) > 1:
        left, right = profile[0][0], profile[-1][0]
        low, high = min(p[1] for p in profile), max(p[1] for p in profile)
        points = " ".join(
            f"{3 + (distance - left) / (right - left) * (width - 6):.2f},"
            f"{height - 4 - (elevation - low) / max(high - low, 1) * (height - 8):.2f}"
            for distance, elevation in profile
        )
    content = (
        f'<polyline points="{points}" fill="none" stroke="#111111" stroke-width="1.6"/>'
    )
    return graphic_frame(content, x, y, width, height, "分段海拔肖像，各段独立缩放", as_group)


def numeric_cells(cp) -> dict[int, str]:
    return {
        0: f'{cp["distance_m"] / 1000:.2f}' if cp["distance_m"] else "0",
        3: f'{cp["segment_distance_m"] / 1000:.1f}',
        4: f'{cp["ascent_m"]:.0f}', 5: f'{cp["descent_m"]:.0f}',
        6: f'{cp["water_ml"]:.0f}',
    }


def format_chart_time(seconds: float) -> str:
    hours, minutes = divmod(math.floor(seconds / 60 + 1e-9), 60)
    return f"{hours:02}:{minutes:02}"


def format_chart_pace(seconds: float) -> str:
    minutes, seconds = divmod(math.floor(seconds + 0.5), 60)
    return f"{minutes:02}:{seconds:02}"


def target_header(target: float) -> list[str]:
    label = f"{target / 3600:.1f} Hr" if target % 1800 == 0 else format_duration(target)
    return ["Target", label]


def format_arrival_time(start_time: str, seconds: float) -> str:
    start = time.fromisoformat(start_time[-5:])
    minutes = start.hour * 60 + start.minute + math.floor(seconds / 60 + 1e-9)
    days, minutes = divmod(minutes, 24 * 60)
    hours, minutes = divmod(minutes, 60)
    prefix = "次日 " if days == 1 else f"+{days}天 " if days else ""
    return f"{prefix}{hours:02}:{minutes:02}"


def table_metadata(plan) -> str:
    start = plan["parameters"]["start_time"]
    prefix = f'发枪：{start.replace("T", " ")}　'
    label = {"pace": "区间配速", "equivalent_pace": "区间等强配速", "arrival_time": "到达时间"}
    metadata = prefix + "括号内：" + label[plan["parameters"]["secondary_display"]]
    if (plan["route"].get("diagnostics") or {}).get("distance_source") == "fit_recorded":
        metadata += "　基于实际 FIT 路线"
    if plan["parameters"].get("water_mode") == "time":
        target = plan["parameters"]["water_target_seconds"]
        label = format_chart_time(target) if target % 60 == 0 else format_duration(target)
        metadata += f"　水量目标：{label}"
    return metadata


def water_metadata(plan) -> str:
    parameters = plan["parameters"]
    if parameters.get("water_mode") != "time":
        rate = str(parameters["water_ml_per_10km"]).removesuffix(".0")
        return (f"水量（ml）：{rate} ml/10 等效公里，"
                "仅供赛段比较，非个人饮水建议")
    override = "（含分段覆盖）" if parameters["water_rate_overrides"] else ""
    weather = "Open-Meteo" if parameters["water_weather_source"] == "open-meteo" else "手动"
    return (f'饮水率：{parameters["water_ml_per_hour"]:g} ml/h{override}'
            f'　余量：{parameters["water_buffer_minutes"]:g} min　天气：{weather}')


def display_station_name(cp) -> str:
    name = cp["name"]
    for label in ("起点", "终点"):
        if name.endswith(f"（{label}）"):
            name = re.sub(r"起终点|起終點", label, name[:-4])
            break
    return name


HEAT_COLUMNS = {
    3: ("distance", "segment_distance_m", "#ffdb63"),
    4: ("ascent", "ascent_m", "#ef6262"),
    5: ("descent", "descent_m", "#52bda5"),
    6: ("water", "water_ml", "#4777c5"),
}


def heat_limits(plan) -> dict[str, float]:
    return {field: max(cp[field] for cp in plan["checkpoints"])
            for _, field, _ in HEAT_COLUMNS.values()}


def cell_fill(cp, column, limits) -> str:
    if column not in HEAT_COLUMNS:
        return "#ffffff"
    _, field, color = HEAT_COLUMNS[column]
    if cp[field] == 0:
        return "#ffffff"
    strength = 0.18 + 0.72 * cp[field] / limits[field]
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(255 + (channel - 255) * strength):02x}" for channel in rgb)


def cp_details(cp) -> list[str]:
    lines = [display_station_name(cp)]
    if cp["official_distance_km"] is not None:
        lines.append(f'官方 {cp["official_distance_km"]:.2f} km')
    if cp["rest_seconds"]:
        lines.append(f'停留 {cp["rest_seconds"] / 60:g} min')
    if cp["cutoff_seconds"] is not None:
        lines.append(f'关门 {format_duration(cp["cutoff_seconds"])}')
    return lines


def timing_lines(plan, cp, timing) -> list[str]:
    lines = [format_chart_time(timing["departure_seconds"])]
    arrival_clock = plan["parameters"]["secondary_display"] == "arrival_time"
    if arrival_clock:
        value = format_arrival_time(plan["parameters"]["start_time"], timing["arrival_seconds"])
        lines.append(f"({value})")
    elif timing["pace_seconds_per_km"] is not None:
        lines.append(f'({format_chart_pace(timing["pace_seconds_per_km"])})')
    if cp["rest_seconds"] and not arrival_clock:
        lines.append(f'到 {format_chart_time(timing["arrival_seconds"])}')
    if timing["cutoff_status"] in ("arrival_late", "departure_late"):
        lines.append(STATUS_LABELS[timing["cutoff_status"]])
    return lines


def render_svg(plan: dict) -> str:
    target_width = 168 if plan["parameters"]["secondary_display"] == "arrival_time" else 116
    widths = [width for _, width in BASE_COLUMNS] + [target_width] * len(plan["schedules"])
    width, margin = sum(widths) + 2, 1
    parts = [f'<rect width="{width}" height="100%" fill="#ffffff"/>']
    metadata = [table_metadata(plan), water_metadata(plan)]
    parts.append(svg_text(6, 30, metadata, size=23))
    y = 50 + (34 if len(metadata) > 1 else 0)
    headers = [name.split("\n") for name, _ in BASE_COLUMNS]
    headers += [target_header(t) for t in plan["targets_seconds"]]
    x = margin
    for header, cell_width in zip(headers, widths):
        parts.append(f'<rect x="{x}" y="{y}" width="{cell_width}" height="84" '
                     'fill="#ffffff" stroke="#bbbbbb" stroke-width="1"/>')
        parts.append(svg_text(x + cell_width / 2, y + (29 if len(header) > 1 else 48),
                              header, size=24, anchor="middle"))
        x += cell_width
    y += 84
    limits = heat_limits(plan)
    for index, cp in enumerate(plan["checkpoints"]):
        details = cp_details(cp)
        names = wrap_text(details[0], 20)
        timings = [timing_lines(plan, cp, schedule["checkpoints"][index]) for schedule in plan["schedules"]]
        name_line_height = 22 * 1.45
        name_height = len(names) * name_line_height + (len(details) - 1) * 18
        row_height = max(94, name_height + 26, max(len(lines) for lines in timings) * 28 + 20)
        x = margin
        for column, cell_width in enumerate(widths):
            color = cell_fill(cp, column, limits)
            column_id = HEAT_COLUMNS[column][0] if column in HEAT_COLUMNS else f"column-{column}"
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_width}" height="{row_height}" '
                f'fill="{color}" stroke="#bbbbbb" stroke-width="1" data-column="{column_id}"/>'
            )
            if column in numeric_cells(cp):
                rate = cp.get("water_rate_ml_per_hour") if column == 6 else None
                text_y = y + row_height / 2 + (8 if rate is None else -4)
                parts.append(svg_text(x + cell_width / 2, text_y,
                                      [numeric_cells(cp)[column]], size=24, anchor="middle"))
                if rate is not None:
                    parts.append(svg_text(x + cell_width / 2, text_y + 25,
                                          [f"{rate:g} ml/h"], size=15, anchor="middle"))
            elif column == 1:
                parts.append(histogram_svg(cp["grade_fractions"], x + 10, y + row_height / 2 - 15,
                                            width=100, height=48, as_group=True))
            elif column == 2:
                parts.append(profile_svg(cp["profile"], x + 8, y + row_height / 2 - 31,
                                         width=114, height=62, as_group=True))
            elif column == 7:
                name_y = y + (row_height - name_height) / 2 + 23
                parts.append(svg_text(x + 12, name_y, names, size=22, color="#00008b", underline=True))
                detail_y = name_y + (len(names) - 1) * name_line_height + 28
                for detail in details[1:]:
                    parts.append(svg_text(x + 12, detail_y, [detail], size=12, color="#666666"))
                    detail_y += 18
            else:
                timing = plan["schedules"][column - 8]["checkpoints"][index]
                lines = timings[column - 8]
                color = "#b82020" if timing["cutoff_status"].endswith("_late") else "#111111"
                parts.append(svg_text(x + cell_width / 2,
                                      y + (row_height - len(lines) * 32) / 2 + 25, lines,
                                      size=23, color=color, anchor="middle"))
            x += cell_width
        y += row_height
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{y + 1:.0f}" '
        f'viewBox="0 0 {width} {y + 1:.0f}" role="img">'
        f'<title>{escape(plan["name"])} 体感一致配速表</title>'
        f'<desc>{escape("；".join(metadata))}；累计出站时间，图示和文字均在此文件内。</desc>'
        f'<metadata>{escape(json.dumps(plan["article"], ensure_ascii=False))}</metadata>'
        + "".join(parts) + "</svg>\n"
    )


def render_html(plan: dict) -> str:
    headers = "".join("<th>" + "<br>".join(escape(line) for line in name.split("\n")) + "</th>"
                      for name, _ in BASE_COLUMNS)
    headers += "".join("<th>" + "<br>".join(target_header(t)) + "</th>" for t in plan["targets_seconds"])
    target_width = 168 if plan["parameters"]["secondary_display"] == "arrival_time" else 116
    widths = [width for _, width in BASE_COLUMNS] + [target_width] * len(plan["schedules"])
    columns = "".join(f'<col style="width:{100 * width / sum(widths):.5f}%">' for width in widths)
    limits = heat_limits(plan)
    metadata = [table_metadata(plan), water_metadata(plan)]
    metadata_html = "<br>".join(escape(line) for line in metadata)
    rows = []
    for index, cp in enumerate(plan["checkpoints"]):
        cells = ""
        for column in range(len(BASE_COLUMNS)):
            if column in numeric_cells(cp):
                content = numeric_cells(cp)[column]
                rate = cp.get("water_rate_ml_per_hour") if column == 6 else None
                if rate is not None:
                    content += f"<small>{rate:g} ml/h</small>"
            elif column == 1:
                content = histogram_svg(cp["grade_fractions"], width=100, height=48)
            elif column == 2:
                content = profile_svg(cp["profile"], width=114, height=62)
            else:
                details = cp_details(cp)
                content = f'<span class="station-name">{escape(details[0])}</span>'
                if len(details) > 1:
                    content += '<small>' + "<br>".join(escape(line) for line in details[1:]) + "</small>"
            css = ' class="cp"' if column == 7 else ""
            cells += f'<td{css} style="background:{cell_fill(cp, column, limits)}">{content}</td>'
        for schedule in plan["schedules"]:
            timing = schedule["checkpoints"][index]
            late = timing["cutoff_status"].endswith("_late")
            cells += f'<td class="{"late" if late else "timing"}">' + "<br>".join(
                escape(line) for line in timing_lines(plan, cp, timing)
            ) + "</td>"
        rows.append("<tr>" + cells + "</tr>")
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="author" content="{escape(plan["article"]["author"])}">
<meta name="source" content="{escape(plan["article"]["url"])}">
<title>{escape(plan["name"])} · 体感一致配速表</title>
<style>
:root {{ --ink:#111111; --paper:#ffffff; --rule:#bbbbbb; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; color:var(--ink); background:var(--paper); font-family:"PingFang SC","Microsoft YaHei",sans-serif; }}
main {{ padding:6px; }} header p {{ margin:0 0 12px; font-size:23px; }}
.scroll {{ overflow-x:auto; }}
table {{ width:100%; min-width:{sum(widths)}px; table-layout:fixed; border-collapse:collapse; font-size:23px; font-variant-numeric:tabular-nums; }}
th {{ height:84px; padding:8px 4px; font-weight:600; line-height:1.35; }}
th,td {{ border:1px solid var(--rule); text-align:center; }}
td {{ height:94px; padding:12px 4px; line-height:1.4; }}
.cp {{ padding-left:12px; text-align:left; overflow-wrap:anywhere; font-size:22px; }}
.station-name {{ color:#00008b; text-decoration:underline; }} small {{ display:block; margin-top:4px; font-size:12px; color:#666666; }}
.timing,.late {{ white-space:nowrap; }} .late {{ color:#b82020; font-weight:bold; }}
td svg {{ display:block; max-width:100%; margin:auto; }}
@media(max-width:600px) {{ header p {{ font-size:16px; }} }}
@page {{ size:A4 landscape; margin:8mm; }}
@media print {{
* {{ print-color-adjust:exact; -webkit-print-color-adjust:exact; }} main {{ padding:0; }}
header p {{ font-size:11px; margin-bottom:6px; }} .scroll {{ overflow:visible; }}
table {{ min-width:0; font-size:10px; }} th {{ height:31px; }} td {{ height:35px; }}
th,td {{ padding:3px 2px; }}
thead {{ display:table-header-group; }} tr {{ break-inside:avoid; page-break-inside:avoid; }}
.cp {{ padding-left:4px; font-size:10px; }} small {{ font-size:6px; margin-top:1px; }}
td svg {{ width:100%; height:28px; }} th {{ white-space:normal; }}
}}
</style></head><body><main>
<header><p>{metadata_html}</p></header>
<div class="scroll"><table aria-label="{escape(plan["name"])} 体感一致配速表"><colgroup>{columns}</colgroup>
<thead><tr>{headers}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</main></body></html>
"""


def csv_text(plan: dict) -> str:
    stream = io.StringIO(newline="")
    fields = [
        "checkpoint_id", "checkpoint_name", "gpx_distance_km", "official_distance_km",
        "segment_distance_km", "ascent_m", "descent_m", "eq_distance_km", "segment_water_ml", "water_ml",
        "rest_seconds", "cutoff_seconds", "target_seconds", "arrival_seconds",
        "departure_seconds", "moving_seconds", "eq_pace_seconds_per_km",
        "distance_pace_seconds_per_km", "pace_seconds_per_km", "cutoff_status",
        "arrival", "departure", "eq_pace", "pace",
    ]
    time_water = plan["parameters"].get("water_mode") == "time"
    if time_water:
        fields.extend([
            "water_reference_target_seconds", "water_rate_ml_per_hour", "water_buffer_minutes",
            "water_weather_source", "water_weather_retrieved_at",
        ])
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for schedule in plan["schedules"]:
        for cp, timing in zip(plan["checkpoints"], schedule["checkpoints"]):
            name = cp["name"]
            if name.lstrip().startswith(("=", "+", "-", "@")):
                name = "'" + name
            row = {
                "checkpoint_id": cp["id"], "checkpoint_name": name,
                "gpx_distance_km": cp["distance_m"] / 1000,
                "official_distance_km": cp["official_distance_km"],
                "segment_distance_km": cp["segment_distance_m"] / 1000,
                **{key: cp[key] for key in ("ascent_m", "descent_m", "eq_distance_km",
                                           "segment_water_ml", "water_ml", "rest_seconds", "cutoff_seconds")},
                "target_seconds": schedule["target_seconds"],
                **timing,
                "arrival": format_duration(timing["arrival_seconds"]),
                "departure": format_duration(timing["departure_seconds"]),
                "eq_pace": format_pace(timing["eq_pace_seconds_per_km"]),
                "pace": format_pace(timing["pace_seconds_per_km"]),
            }
            if time_water:
                row.update({
                    "water_reference_target_seconds": plan["parameters"]["water_target_seconds"],
                    "water_rate_ml_per_hour": cp["water_rate_ml_per_hour"],
                    "water_buffer_minutes": plan["parameters"]["water_buffer_minutes"],
                    "water_weather_source": plan["parameters"]["water_weather_source"],
                    "water_weather_retrieved_at": plan["parameters"]["water_weather_retrieved_at"],
                })
            writer.writerow(row)
    return stream.getvalue()


def plan_summary(plan: dict) -> dict:
    cps, schedules = plan["checkpoints"], plan["schedules"]
    close = lambda a, b: math.isclose(a, b, rel_tol=0, abs_tol=1e-7)
    return {
        "parameters": plan["parameters"],
        "target_source": "targets" if "targets" in plan["configuration"] else "target",
        "targets_seconds": plan["targets_seconds"],
        "route": plan["route"],
        "checkpoints": [
            {key: cp[key] for key in ("id", "name", "distance_m", "rest_seconds", "cutoff_seconds")}
            for cp in cps
        ],
        "verification": {
            "finish_targets_match": all(
                close(s["checkpoints"][-1]["departure_seconds"], s["target_seconds"]) for s in schedules
            ),
            "rests_match": all(
                close(t["departure_seconds"] - t["arrival_seconds"], cp["rest_seconds"])
                for s in schedules for cp, t in zip(cps, s["checkpoints"])
            ),
            "cutoff_checked_stations": sum(cp["cutoff_seconds"] is not None for cp in cps[1:]),
            "cutoff_unchecked_stations": sum(cp["cutoff_seconds"] is None for cp in cps[1:]),
            "cutoff_failures": [
                {"target_seconds": s["target_seconds"], "checkpoint_id": cp["id"], "status": t["cutoff_status"]}
                for s in schedules for cp, t in zip(cps[1:], s["checkpoints"][1:])
                if t["cutoff_status"] in ("arrival_late", "departure_late")
            ],
        },
    }


def write_outputs(plan: dict, output_dir: Path, overwrite=False) -> list[Path]:
    output_dir = Path(output_dir)
    renderers = {
        "json": lambda: json.dumps(plan, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        "csv": lambda: "\ufeff" + csv_text(plan),
        "html": lambda: render_html(plan),
        "svg": lambda: render_svg(plan),
    }
    formats = plan["parameters"]["output_formats"]
    paths = [output_dir / f"pace-chart.{fmt}" for fmt in formats]
    for path in paths:
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise InputError(f"Output must be a regular file, not a directory or symlink: {path}")
    if not overwrite and any(path.exists() for path in paths):
        raise InputError("Output files already exist; choose a new directory or use --overwrite")
    contents = [renderers[fmt]() for fmt in formats]
    output_dir.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".pace-chart-", dir=output_dir))
    backups, replaced = {}, []
    keep_backup = False
    try:
        # Stage every export and backup before replacing any user-visible output.
        for path, text in zip(paths, contents):
            with (staging / path.name).open("w", encoding="utf-8", newline="") as stream:
                stream.write(text)
            if path.exists():
                backup = staging / (path.name + ".bak")
                shutil.copy2(path, backup)
                backups[path] = backup
        try:
            for path in paths:
                (staging / path.name).replace(path)
                replaced.append(path)
        except OSError as error:
            failures = []
            for path in reversed(replaced):
                try:
                    if path in backups:
                        backups[path].replace(path)
                    else:
                        path.unlink()
                except OSError as recovery_error:
                    failures.append({"path": str(path), "error": str(recovery_error)})
            if failures:
                keep_backup = True
                raise InputError(
                    f"Export failed ({error}); rollback incomplete. Recovery files retained at {staging}",
                    {"recovery_directory": str(staging), "rollback_failures": failures},
                ) from error
            raise
    finally:
        if not keep_backup:
            shutil.rmtree(staging)
    return paths


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="Inspect geometry and embedded CP candidates")
    inspect.add_argument("route", type=Path, help="Local GPX, KML, FIT or single-FIT ZIP route")
    inspect.add_argument("--track-index", type=int)
    inspect.add_argument("--sample-m", type=float, default=DEFAULTS["sample_m"])
    inspect.add_argument("--smoothing-m", type=float, default=DEFAULTS["smoothing_m"])
    inspect.add_argument("--ascent-smoothing-m", type=float, default=DEFAULTS["ascent_smoothing_m"])
    inspect.add_argument("--ascent-method", choices=("hysteresis", "window"), default="hysteresis")
    for name in ("ascent_threshold_m", "elevation_spike_m", "distance_tolerance_m"):
        inspect.add_argument("--" + name.replace("_", "-"), type=float, default=DEFAULTS[name])
    inspect.add_argument("--use-kml-altitudes", action="store_true",
                         help="Use supplied KML coordinate heights when altitudeMode is omitted or clampToGround")
    generate = commands.add_parser("generate", help="Generate SVG by default; select exports with output_formats")
    generate.add_argument("route", type=Path, help="Local GPX, KML, FIT or single-FIT ZIP route")
    generate.add_argument("--config", type=Path, required=True)
    generate.add_argument("--output-dir", type=Path, required=True)
    generate.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_route(args.route, args.track_index, args.sample_m, args.smoothing_m,
                                   args.ascent_smoothing_m, args.use_kml_altitudes, args.ascent_method,
                                   args.ascent_threshold_m, args.elevation_spike_m, args.distance_tolerance_m)
        else:
            config = json.loads(args.config.read_text(encoding="utf-8"))
            keys(config, CONFIG_KEYS, "configuration")
            preview = None
            if config.get("water_mode") == "time":
                draft = build_plan(args.route, config, defer_water=True)
                water_options(draft, config, require_rate=False)
                weather = config.get("water_weather")
                if weather is not None and not isinstance(weather, dict):
                    raise InputError("water_weather must contain confirmed forecast or manual information")
                if weather is not None and weather.get("source") not in ("manual", "open-meteo"):
                    raise InputError("water_weather source must be open-meteo or manual")
                if weather is None or weather["source"] == "open-meteo":
                    parameters = draft["parameters"]
                    route = prepare_route(
                        load_route(args.route, config.get("track_index"), config.get("use_kml_altitudes", False)),
                        parameters["distance_tolerance_m"], parameters["elevation_spike_m"],
                    )
                    context, fingerprint = water_forecast_context(draft, route, config)
                    if weather is None or weather.get("context_sha256") != fingerprint:
                        weather = fetch_water_forecast(context, fingerprint)
                    if weather.get("confirmed") is not True:
                        check = {**config, "water_weather": {**weather, "confirmed": True}}
                        validate_water_weather(draft, route, check)
                        preview = {
                            "status": "needs_water_confirmation", "outputs": [],
                            "water_weather": weather, "summary": plan_summary(draft),
                            "warnings": ["天气为赛段中点预报，请确认后填写各段饮水速率。"],
                        }
            if preview is not None:
                result = preview
            else:
                plan = build_plan(args.route, config)
                paths = write_outputs(plan, args.output_dir, args.overwrite)
                result = {"outputs": [str(path) for path in paths], "warnings": plan["warnings"],
                          "summary": plan_summary(plan)}
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as error:
        result = {"error": str(error)}
        if isinstance(error, InputError) and error.details is not None:
            result["details"] = error.details
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
