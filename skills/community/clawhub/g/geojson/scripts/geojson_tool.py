#!/usr/bin/env python3
"""Small helper for GeoJSON summary and validation."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


GEOMETRY_TYPES = {
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
}


def load_input(file_path: str | None, json_text: str | None) -> Any:
    if bool(file_path) == bool(json_text):
        raise ValueError("Provide exactly one of --file or --json.")
    if file_path:
        return json.loads(Path(file_path).read_text(encoding="utf-8"))
    return json.loads(json_text)


def iter_geometry_objects(obj: Any) -> list[dict[str, Any]]:
    if not isinstance(obj, dict):
        return []

    obj_type = obj.get("type")
    if obj_type == "FeatureCollection":
        features = obj.get("features")
        if not isinstance(features, list):
            return []
        geometries: list[dict[str, Any]] = []
        for feature in features:
            if isinstance(feature, dict):
                geom = feature.get("geometry")
                if isinstance(geom, dict):
                    geometries.append(geom)
        return geometries
    if obj_type == "Feature":
        geom = obj.get("geometry")
        return [geom] if isinstance(geom, dict) else []
    if obj_type in GEOMETRY_TYPES:
        return [obj]
    return []


def extract_positions(geometry: dict[str, Any]) -> list[tuple[float, float]]:
    positions: list[tuple[float, float]] = []

    def walk_coordinates(node: Any) -> None:
        if isinstance(node, list):
            if len(node) >= 2 and all(isinstance(v, (int, float)) for v in node[:2]):
                positions.append((float(node[0]), float(node[1])))
                return
            for child in node:
                walk_coordinates(child)

    geom_type = geometry.get("type")
    if geom_type == "GeometryCollection":
        for child in geometry.get("geometries", []):
            if isinstance(child, dict):
                positions.extend(extract_positions(child))
        return positions

    walk_coordinates(geometry.get("coordinates"))
    return positions


def compute_bbox(positions: list[tuple[float, float]]) -> list[float] | None:
    if not positions:
        return None
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    return [min(xs), min(ys), max(xs), max(ys)]


def top_type_name(obj: Any) -> str:
    return obj.get("type") if isinstance(obj, dict) and isinstance(obj.get("type"), str) else "unknown"


def validate_geojson(obj: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["Top-level JSON value must be an object."]

    obj_type = obj.get("type")
    if not isinstance(obj_type, str):
        errors.append("Missing or invalid top-level 'type'.")
        return errors

    if obj_type == "FeatureCollection":
        features = obj.get("features")
        if not isinstance(features, list):
            errors.append("'FeatureCollection.features' must be an array.")
        else:
            for index, feature in enumerate(features):
                if not isinstance(feature, dict):
                    errors.append(f"Feature at index {index} is not an object.")
                    continue
                if feature.get("type") != "Feature":
                    errors.append(f"Feature at index {index} must have type 'Feature'.")
    elif obj_type == "Feature":
        if "geometry" not in obj:
            errors.append("Feature is missing 'geometry'.")
    elif obj_type not in GEOMETRY_TYPES:
        errors.append(f"Unsupported or unknown GeoJSON type '{obj_type}'.")

    return errors


def build_summary(obj: Any) -> dict[str, Any]:
    geometries = iter_geometry_objects(obj)
    geom_counter = Counter(
        geom.get("type", "unknown") for geom in geometries if isinstance(geom, dict)
    )
    positions: list[tuple[float, float]] = []
    for geom in geometries:
        positions.extend(extract_positions(geom))

    suspicious = []
    if positions:
        out_of_range = sum(
            1
            for lon, lat in positions
            if not (-180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0)
        )
        maybe_swapped = sum(
            1
            for lon, lat in positions
            if -90.0 <= lon <= 90.0 and not (-90.0 <= lat <= 90.0)
        )
        if out_of_range:
            suspicious.append(f"{out_of_range} coordinate pairs fall outside lon/lat range.")
        if maybe_swapped:
            suspicious.append(f"{maybe_swapped} coordinate pairs may be swapped lat/lon.")

    feature_count = None
    if isinstance(obj, dict) and obj.get("type") == "FeatureCollection" and isinstance(obj.get("features"), list):
        feature_count = len(obj["features"])

    return {
        "type": top_type_name(obj),
        "feature_count": feature_count,
        "geometry_types": dict(geom_counter),
        "bbox": compute_bbox(positions),
        "position_count": len(positions),
        "suspicious_notes": suspicious,
        "crs_note": "GeoJSON is commonly exchanged as WGS84-style lon/lat, but confirm source CRS if precision matters.",
    }


def cmd_summary(args: argparse.Namespace) -> int:
    obj = load_input(args.file, args.json)
    payload = build_summary(obj)
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    obj = load_input(args.file, args.json)
    errors = validate_geojson(obj)
    payload = {
        "type": top_type_name(obj),
        "valid": not errors,
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GeoJSON summary and validation helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    summary = sub.add_parser("summary", help="Summarize a GeoJSON file or JSON string.")
    summary.add_argument("--file")
    summary.add_argument("--json")
    summary.set_defaults(func=cmd_summary)

    validate = sub.add_parser("validate", help="Validate a GeoJSON file or JSON string.")
    validate.add_argument("--file")
    validate.add_argument("--json")
    validate.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
