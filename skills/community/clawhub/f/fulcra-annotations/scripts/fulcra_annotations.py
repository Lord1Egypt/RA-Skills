#!/usr/bin/env python3
"""Create and record Fulcra annotations.

Generic helper for agents. It intentionally avoids printing secrets and supports
dry-runs for all write commands.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


API_BASE = os.environ.get("FULCRA_API_BASE", "https://api.fulcradynamics.com").rstrip("/")
DEFAULT_AGENT_SOURCE = os.environ.get("FULCRA_AGENT_SOURCE", "com.fulcra.agent")
PROCESS_HOME = os.environ.get("HOME") or str(Path.home())
DEFAULT_HOME = os.environ.get("FULCRA_HOME") or PROCESS_HOME

TYPE_TO_DATA_TYPE = {
    "moment": "MomentAnnotation",
    "duration": "DurationAnnotation",
    "boolean": "BooleanAnnotation",
    "numeric": "NumericAnnotation",
    "scale": "ScaleAnnotation",
}

TYPE_TO_READ_CLASS = {
    "moment": "event",
    "duration": "event",
    "boolean": "metric",
    "numeric": "metric",
    "scale": "metric",
}


def fail(message: str, code: int = 1) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


def bearer_value() -> str:
    env_token = os.environ.get("FULCRA_ACCESS_TOKEN")
    if env_token:
        return env_token.strip()

    env = os.environ.copy()
    env["HOME"] = DEFAULT_HOME
    if os.environ.get("FULCRA_HOME"):
        env.setdefault("UV_TOOL_DIR", str(Path(PROCESS_HOME) / ".local" / "share" / "uv" / "tools"))
        env.setdefault("UV_CACHE_DIR", str(Path(PROCESS_HOME) / ".cache" / "uv"))

    command = os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api")
    candidates = [[*shlex.split(command), "auth", "print-access-token"]]
    for cmd in candidates:
        try:
            token = subprocess.check_output(
                cmd,
                env=env,
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=45,
            ).strip()
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
        if token:
            return token
    fail("No Fulcra auth available. Set FULCRA_ACCESS_TOKEN or run Fulcra CLI auth login.")


def request(method: str, path: str, payload: Any | None = None) -> tuple[int, str]:
    data = None
    headers = {"Authorization": f"Bearer {bearer_value()}"}
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API_BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
            return response.status, body.decode() if body else ""
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        return exc.code, body


def parse_labels(raw: str | None, low: int = 1, high: int = 5) -> dict[str, str]:
    if not raw:
        return {str(i): str(i) for i in range(low, high + 1)}
    labels: dict[str, str] = {}
    for part in raw.split(","):
        if not part.strip():
            continue
        if "=" not in part:
            fail(f"Invalid --scale-labels item {part!r}; expected N=Label")
        key, value = part.split("=", 1)
        labels[key.strip()] = value.strip()
    return labels


def annotation_source_id(annotation: dict[str, Any]) -> str:
    ann_id = annotation["id"]
    return annotation.get("fulcra_source_id") or f"com.fulcradynamics.annotation.{ann_id}"


def is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


def get_tag_by_name(name: str) -> dict[str, Any] | None:
    path = f"/user/v1alpha1/tag/name/{urllib.parse.quote(name, safe='')}"
    status, body = request("GET", path)
    if status == 200:
        return json.loads(body)
    if status == 404:
        return None
    fail(f"Failed to look up tag {name!r}: HTTP {status}: {body[:500]}")


def create_tag(name: str) -> dict[str, Any]:
    status, body = request("POST", "/user/v1alpha1/tag", {"name": name})
    if status in {200, 201} and body:
        return json.loads(body)
    if status in {200, 201, 303}:
        tag = get_tag_by_name(name)
        if tag:
            return tag
    fail(f"Failed to create tag {name!r}: HTTP {status}: {body[:500]}")


def resolve_tags(raw_tags: list[str] | None, create_missing: bool = True) -> list[str]:
    resolved: list[str] = []
    for raw in raw_tags or []:
        tag = raw.strip()
        if not tag:
            continue
        if is_uuid(tag):
            resolved.append(str(uuid.UUID(tag)))
            continue
        found = get_tag_by_name(tag)
        if not found:
            if not create_missing:
                fail(f"No Fulcra tag named {tag!r}; create it first or allow tag creation.")
            found = create_tag(tag)
        resolved.append(found["id"])
    return resolved


def normalize_annotation(annotation: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": annotation.get("id"),
        "name": annotation.get("name"),
        "type": annotation.get("annotation_type"),
        "source_id": annotation_source_id(annotation),
        "deleted_at": annotation.get("deleted_at"),
        "tags": annotation.get("tags") or [],
    }


def list_annotations(include_deleted: bool = False) -> list[dict[str, Any]]:
    status, body = request("GET", "/user/v1alpha1/annotation")
    if status != 200:
        fail(f"Failed to list annotations: HTTP {status}: {body[:500]}")
    data = json.loads(body)
    rows = [normalize_annotation(item) for item in data]
    if not include_deleted:
        rows = [row for row in rows if not row.get("deleted_at")]
    return rows


def find_annotation(name: str | None = None, annotation_id: str | None = None) -> dict[str, Any]:
    status, body = request("GET", "/user/v1alpha1/annotation")
    if status != 200:
        fail(f"Failed to list annotations: HTTP {status}: {body[:500]}")
    data = json.loads(body)
    active = [row for row in data if not row.get("deleted_at")]
    if annotation_id:
        matches = [row for row in active if row.get("id") == annotation_id]
    else:
        target = (name or "").strip().lower()
        matches = [row for row in active if row.get("name", "").strip().lower() == target]
    if not matches:
        fail("No active annotation matched the requested name/id.")
    if len(matches) > 1:
        fail("Multiple active annotations matched; rerun with --id.")
    return matches[0]


def create_payload(args: argparse.Namespace) -> dict[str, Any]:
    tags = resolve_tags(args.tag)
    base = {
        "annotation_type": args.type,
        "name": args.name,
        "description": args.description or "",
        "tags": tags,
    }
    if args.type == "moment":
        base["measurement_spec"] = None
        base["spec"] = {"default_note": args.default_note} if args.default_note else None
    elif args.type == "boolean":
        default = True if args.default_value is None else str(args.default_value).lower() in {"1", "true", "yes", "y"}
        base["measurement_spec"] = {
            "measurement_type": "boolean",
            "value_type": "boolean",
            "unit": None,
            "boolean": {"value": default},
        }
        base["spec"] = {"default_note": args.default_note} if args.default_note else None
    elif args.type == "numeric":
        value = float(args.default_value) if args.default_value is not None else None
        measurement_type = args.measurement_type or "custom"
        base["measurement_spec"] = {
            "measurement_type": measurement_type,
            "value_type": "real",
            "unit": args.unit,
            measurement_type: {"value": value},
        }
        base["spec"] = {"default_note": args.default_note} if args.default_note else None
    elif args.type == "scale":
        low = int(args.scale_min)
        high = int(args.scale_max)
        default = int(args.default_value) if args.default_value is not None else (low + high) // 2
        base["measurement_spec"] = {
            "measurement_type": "scale",
            "value_type": "integer",
            "unit": None,
            "scale": {"min_allowed": low, "max_allowed": high, "value": default},
        }
        base["spec"] = {
            "default_note": args.default_note,
            "scale": {
                "label_mapping": {
                    "mapping_type": "string",
                    "string": {"mapping": parse_labels(args.scale_labels, low, high)},
                },
                "scale_mapping": None,
            },
        }
    else:
        fail(f"Create support for annotation type {args.type!r} is not implemented.")
    return base


def create_annotation(args: argparse.Namespace) -> dict[str, Any]:
    payload = create_payload(args)
    if args.dry_run:
        return {"ok": True, "dry_run": True, "payload": payload}
    status, body = request("POST", "/user/v1alpha1/annotation", payload)
    if status != 200:
        fail(f"Failed to create annotation: HTTP {status}: {body[:800]}")
    return {"ok": True, "annotation": normalize_annotation(json.loads(body))}


def record_payload(annotation: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    ann_type = annotation["annotation_type"]
    data_type = TYPE_TO_DATA_TYPE.get(ann_type)
    if not data_type:
        fail(f"Recording {ann_type!r} annotations is not implemented.")
    recorded_at = args.recorded_at or datetime.now(timezone.utc).isoformat()
    data: dict[str, Any] = {}
    if args.note:
        data["note"] = args.note
    if ann_type in {"boolean", "numeric", "scale"}:
        if args.value is None:
            fail(f"--value is required when recording {ann_type} annotations.")
        if ann_type == "boolean":
            data["value"] = str(args.value).lower() in {"1", "true", "yes", "y"}
        elif ann_type == "scale":
            data["value"] = int(args.value)
        else:
            data["value"] = float(args.value)

    source_id = annotation_source_id(annotation)
    tags = resolve_tags(args.tag) if args.tag is not None else (annotation.get("tags") or [])
    return {
        "specversion": 1,
        "data": json.dumps(data),
        "metadata": {
            "data_type": data_type,
            "recorded_at": recorded_at,
            "source": [args.source or DEFAULT_AGENT_SOURCE, source_id],
            "tags": tags,
            "content_type": "application/json",
        },
    }


def verify_record(annotation: dict[str, Any], recorded_at: str) -> int:
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
    status, body = request("GET", f"/data/v1alpha1/{read_class}/{data_type}?{query}")
    if status != 200:
        return 0
    source_id = annotation_source_id(annotation)
    records = json.loads(body)
    return sum(
        1
        for item in records
        if item.get("source_id") == source_id or source_id in item.get("sources", [])
    )


def record_annotation(args: argparse.Namespace) -> dict[str, Any]:
    annotation = find_annotation(name=args.name, annotation_id=args.id)
    payload = record_payload(annotation, args)
    if args.dry_run:
        return {"ok": True, "dry_run": True, "annotation": normalize_annotation(annotation), "payload": payload}
    status, body = request("POST", "/ingest/v1/record", payload)
    if status != 204:
        fail(f"Failed to record annotation: HTTP {status}: {body[:800]}")
    recorded_at = payload["metadata"]["recorded_at"]
    return {
        "ok": True,
        "annotation": normalize_annotation(annotation),
        "recorded_at": recorded_at,
        "verified_matches": verify_record(annotation, recorded_at),
    }


def recent_records(args: argparse.Namespace) -> dict[str, Any]:
    annotation = find_annotation(name=args.name, annotation_id=args.id)
    ann_type = annotation["annotation_type"]
    data_type = TYPE_TO_DATA_TYPE[ann_type]
    read_class = TYPE_TO_READ_CLASS[ann_type]
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=args.hours)
    query = urllib.parse.urlencode({"start_time": start.isoformat(), "end_time": end.isoformat()})
    status, body = request("GET", f"/data/v1alpha1/{read_class}/{data_type}?{query}")
    if status != 200:
        fail(f"Failed to read records: HTTP {status}: {body[:500]}")
    source_id = annotation_source_id(annotation)
    records = [
        item
        for item in json.loads(body)
        if item.get("source_id") == source_id or source_id in item.get("sources", [])
    ]
    return {
        "ok": True,
        "annotation": normalize_annotation(annotation),
        "count": len(records),
        "records": records[-args.limit :],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and record Fulcra annotations")
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--include-deleted", action="store_true")

    create = sub.add_parser("create")
    create.add_argument("--type", choices=["moment", "boolean", "numeric", "scale"], required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--description", default="")
    create.add_argument("--tag", action="append")
    create.add_argument("--default-note")
    create.add_argument("--default-value")
    create.add_argument("--unit")
    create.add_argument("--measurement-type", choices=["custom", "count", "mass", "distance", "percent", "temperature", "volume"])
    create.add_argument("--scale-min", default=1)
    create.add_argument("--scale-max", default=5)
    create.add_argument("--scale-labels")
    create.add_argument("--dry-run", action="store_true")

    record = sub.add_parser("record")
    record.add_argument("--name")
    record.add_argument("--id")
    record.add_argument("--value")
    record.add_argument("--note")
    record.add_argument("--recorded-at")
    record.add_argument("--source")
    record.add_argument("--tag", action="append")
    record.add_argument("--dry-run", action="store_true")

    recent = sub.add_parser("recent")
    recent.add_argument("--name")
    recent.add_argument("--id")
    recent.add_argument("--hours", type=float, default=24)
    recent.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()
    if args.command == "list":
        result = {"ok": True, "annotations": list_annotations(args.include_deleted)}
    elif args.command == "create":
        result = create_annotation(args)
    elif args.command == "record":
        if not args.name and not args.id:
            fail("record requires --name or --id")
        result = record_annotation(args)
    elif args.command == "recent":
        if not args.name and not args.id:
            fail("recent requires --name or --id")
        result = recent_records(args)
    else:
        fail("unknown command")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
