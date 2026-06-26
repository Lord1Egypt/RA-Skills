#!/usr/bin/env python3
import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path


INSTRUCTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions?", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(previous|prior)\s+instructions?", re.IGNORECASE),
    re.compile(r"(system|developer)\s+prompt", re.IGNORECASE),
    re.compile(r"you\s+are\s+now", re.IGNORECASE),
    re.compile(r"reveal\s+(the\s+)?system\s+prompt", re.IGNORECASE),
    re.compile(r"printenv|curl\s+https?://|wget\s+https?://", re.IGNORECASE),
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse CSV or JSON through a deterministic boundary and emit structured JSON."
    )
    parser.add_argument("--input", required=True, help="Path to a CSV or JSON file")
    parser.add_argument(
        "--format",
        choices=["auto", "csv", "json"],
        default="auto",
        help="Input format override",
    )
    parser.add_argument(
        "--max-preview-rows",
        type=int,
        default=25,
        help="Maximum rows/items to include in preview_rows",
    )
    parser.add_argument(
        "--max-string-length",
        type=int,
        default=160,
        help="Maximum characters to include per string value in previews",
    )
    parser.add_argument(
        "--max-input-bytes",
        type=int,
        default=25 * 1024 * 1024,
        help="Maximum input file size to parse in bytes",
    )
    return parser.parse_args()


def detect_format(path, format_hint):
    if format_hint != "auto":
        return format_hint
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".json":
        return "json"
    raise ValueError("Could not auto-detect format. Pass --format csv or --format json.")


def truncate_text(value, max_len):
    if len(value) <= max_len:
        return value, False
    return value[: max_len - 3] + "...", True


def scan_text(value):
    matches = []
    for pattern in INSTRUCTION_PATTERNS:
        if pattern.search(value):
            matches.append(pattern.pattern)
    return {
        "raw_text_present": bool(value),
        "instruction_like_text_possible": bool(matches),
        "matched_rules": matches,
    }


def make_error(message):
    return json.dumps({"error": message}, ensure_ascii=True)


def infer_scalar_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return "number"
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "string"


def try_parse_json_like_scalar(text):
    lowered = text.strip().lower()
    if lowered == "":
        return None, "empty"
    if lowered in {"true", "false"}:
        return lowered == "true", "boolean"
    if lowered == "null":
        return None, "null"
    try:
        if "." in lowered:
            return float(lowered), "number"
        return int(lowered), "integer"
    except ValueError:
        return text, "string"


def make_field_stats():
    return {
        "non_null_count": 0,
        "empty_count": 0,
        "type_counts": {},
        "max_observed_length": 0,
        "suspicious_value_count": 0,
        "sample_values": [],
    }


def update_type_counts(stats, value_type):
    stats["type_counts"][value_type] = stats["type_counts"].get(value_type, 0) + 1


def maybe_add_sample(stats, value, limit=3):
    if len(stats["sample_values"]) >= limit:
        return
    if value not in stats["sample_values"]:
        stats["sample_values"].append(value)


def build_csv_preview_row(row, max_string_length):
    preview_row = {}
    row_alerts = {}
    for key, raw_value in row.items():
        value = raw_value if raw_value is not None else ""
        truncated_value, was_truncated = truncate_text(value, max_string_length)
        text_scan = scan_text(value)
        preview_row[key] = {
            "value": truncated_value,
            "metadata": {
                "raw_text_present": text_scan["raw_text_present"],
                "instruction_like_text_possible": text_scan["instruction_like_text_possible"],
                "truncated": was_truncated,
            },
        }
        row_alerts[key] = text_scan
    return preview_row, row_alerts


def parse_csv(path, max_preview_rows, max_string_length):
    field_stats = {}
    preview_rows = []
    alerts = []
    row_count = 0
    preview_rows_truncated = False

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        dialect = csv.Sniffer().sniff(sample) if sample.strip() else csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        fieldnames = reader.fieldnames or []
        for field in fieldnames:
            field_stats[field] = make_field_stats()

        for row_index, row in enumerate(reader, start=1):
            row_count += 1
            preview_row, row_scans = build_csv_preview_row(row, max_string_length)
            if len(preview_rows) < max_preview_rows:
                preview_rows.append({"row_index": row_index, "fields": preview_row})
            else:
                preview_rows_truncated = True

            for field in fieldnames:
                raw_value = row.get(field) or ""
                parsed_value, value_type = try_parse_json_like_scalar(raw_value)
                stats = field_stats[field]
                text_scan = row_scans[field]
                if raw_value == "":
                    stats["empty_count"] += 1
                else:
                    stats["non_null_count"] += 1
                update_type_counts(stats, value_type)
                stats["max_observed_length"] = max(stats["max_observed_length"], len(raw_value))
                maybe_add_sample(stats, str(parsed_value))
                if text_scan["instruction_like_text_possible"]:
                    stats["suspicious_value_count"] += 1
                    alerts.append(
                        {
                            "kind": "instruction_like_text",
                            "location": {"row_index": row_index, "field": field},
                            "matched_rules": text_scan["matched_rules"],
                        }
                    )

    schema_fields = []
    for field, stats in field_stats.items():
        schema_fields.append(
            {
                "name": field,
                "non_null_count": stats["non_null_count"],
                "empty_count": stats["empty_count"],
                "type_counts": stats["type_counts"],
                "max_observed_length": stats["max_observed_length"],
                "raw_text_present": stats["non_null_count"] > 0,
                "instruction_like_text_possible": stats["suspicious_value_count"] > 0,
                "suspicious_value_count": stats["suspicious_value_count"],
                "sample_values": stats["sample_values"],
            }
        )

    return {
        "summary": {
            "row_count": row_count,
            "column_count": len(field_stats),
            "preview_rows_truncated": preview_rows_truncated,
        },
        "schema": {
            "kind": "table",
            "fields": schema_fields,
        },
        "alerts": alerts,
        "preview_rows": preview_rows,
    }


def summarize_json_value(value, max_string_length):
    if isinstance(value, dict):
        return {
            "kind": "object",
            "keys": list(value.keys()),
            "field_count": len(value),
        }
    if isinstance(value, list):
        return {
            "kind": "array",
            "length": len(value),
        }
    if isinstance(value, str):
        truncated_value, was_truncated = truncate_text(value, max_string_length)
        text_scan = scan_text(value)
        return {
            "kind": "string",
            "value": truncated_value,
            "raw_text_present": text_scan["raw_text_present"],
            "instruction_like_text_possible": text_scan["instruction_like_text_possible"],
            "matched_rules": text_scan["matched_rules"],
            "truncated": was_truncated,
        }
    return {
        "kind": infer_scalar_type(value),
        "value": value,
    }


def collect_json_schema(value, path="$", alerts=None):
    if alerts is None:
        alerts = []

    value_type = infer_scalar_type(value)
    node = {"path": path, "type": value_type}

    if isinstance(value, dict):
        properties = []
        for key, child in value.items():
            properties.append(collect_json_schema(child, f"{path}.{key}", alerts))
        node["properties"] = properties
        return node

    if isinstance(value, list):
        node["length"] = len(value)
        if value:
            sample_children = value[:5]
            node["items"] = [
                collect_json_schema(child, f"{path}[{index}]", alerts)
                for index, child in enumerate(sample_children)
            ]
        else:
            node["items"] = []
        return node

    if isinstance(value, str):
        text_scan = scan_text(value)
        node["raw_text_present"] = text_scan["raw_text_present"]
        node["instruction_like_text_possible"] = text_scan["instruction_like_text_possible"]
        node["matched_rules"] = text_scan["matched_rules"]
        if text_scan["instruction_like_text_possible"]:
            alerts.append(
                {
                    "kind": "instruction_like_text",
                    "location": {"json_path": path},
                    "matched_rules": text_scan["matched_rules"],
                }
            )
    return node


def build_json_preview(value, max_preview_rows, max_string_length):
    if isinstance(value, list):
        preview = []
        preview_truncated = len(value) > max_preview_rows
        for index, item in enumerate(value[:max_preview_rows]):
            preview.append({"index": index, "value": summarize_json_value(item, max_string_length)})
        return preview, preview_truncated

    if isinstance(value, dict):
        preview = []
        items = list(value.items())
        preview_truncated = len(items) > max_preview_rows
        for key, item_value in items[:max_preview_rows]:
            preview.append({"key": key, "value": summarize_json_value(item_value, max_string_length)})
        return preview, preview_truncated

    return [summarize_json_value(value, max_string_length)], False


def parse_json(path, max_preview_rows, max_string_length):
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)

    alerts = []
    schema = collect_json_schema(value, alerts=alerts)
    preview_rows, preview_rows_truncated = build_json_preview(
        value, max_preview_rows, max_string_length
    )

    summary = {
        "top_level_type": infer_scalar_type(value),
        "preview_rows_truncated": preview_rows_truncated,
    }
    if isinstance(value, dict):
        summary["top_level_key_count"] = len(value)
    elif isinstance(value, list):
        summary["top_level_item_count"] = len(value)

    return {
        "summary": summary,
        "schema": schema,
        "alerts": alerts,
        "preview_rows": preview_rows,
    }


def main():
    args = parse_args()
    path = Path(args.input).resolve()
    if not path.exists():
        print(make_error(f"Input file not found: {path}"), file=sys.stderr)
        return 1
    if not path.is_file():
        print(make_error(f"Input path is not a file: {path}"), file=sys.stderr)
        return 1
    input_size = path.stat().st_size
    if input_size > args.max_input_bytes:
        print(
            make_error(
                f"Input file is too large: {input_size} bytes exceeds limit {args.max_input_bytes}. "
                "Raise --max-input-bytes explicitly if you want to parse a larger file."
            ),
            file=sys.stderr,
        )
        return 1

    try:
        detected_format = detect_format(path, args.format)
        if detected_format == "csv":
            parsed = parse_csv(path, args.max_preview_rows, args.max_string_length)
        else:
            parsed = parse_json(path, args.max_preview_rows, args.max_string_length)
    except Exception as exc:
        print(make_error(str(exc)), file=sys.stderr)
        return 1

    result = {
        "source": {
            "path": str(path),
            "format": detected_format,
            "parser": "datagate/ingest_data.py",
            "limits": {
                "max_preview_rows": args.max_preview_rows,
                "max_string_length": args.max_string_length,
                "max_input_bytes": args.max_input_bytes,
            },
        }
    }
    result.update(parsed)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
