#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Validate an intervention packet against the bundled JSON Schema."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = SKILL_ROOT / "assets" / "intervention-packet.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate an ASI-proxy intervention packet with the bundled Draft 2020-12 "
            "schema. The validator is offline and uses only the Python standard library."
        )
    )
    parser.add_argument("packet", type=Path, help="Intervention-packet JSON file.")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Schema path (default: the bundled public schema).",
    )
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")
    return parser.parse_args()


def emit(payload: Any, *, pretty: bool = False) -> None:
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=True,
        indent=2 if pretty else None,
        sort_keys=True,
    )
    sys.stdout.write("\n")


def json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return float(left) == float(right)
    return type(left) is type(right) and left == right


def json_type_matches(instance: Any, expected: str) -> bool:
    return {
        "null": instance is None,
        "boolean": isinstance(instance, bool),
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "number": (
            isinstance(instance, (int, float))
            and not isinstance(instance, bool)
            and math.isfinite(float(instance))
        ),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
    }.get(expected, False)


def pointer(root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    value: Any = root
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise ValueError(f"unresolved schema reference: {reference}")
        value = value[token]
    if not isinstance(value, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return value


def child_path(path: str, key: str) -> str:
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
        return f"{path}.{key}"
    return f"{path}[{json.dumps(key, ensure_ascii=True)}]"


class SchemaValidator:
    """Small Draft 2020-12 subset used by the public packet schema."""

    def __init__(self, root_schema: dict[str, Any]):
        self.root = root_schema

    def validate(
        self, instance: Any, schema: dict[str, Any] | None = None, path: str = "$"
    ) -> list[str]:
        current = self.root if schema is None else schema
        errors: list[str] = []

        if "$ref" in current:
            return self.validate(instance, pointer(self.root, current["$ref"]), path)

        if "const" in current and not json_equal(instance, current["const"]):
            errors.append(f"{path}: expected constant {current['const']!r}")

        if "enum" in current and not any(
            json_equal(instance, candidate) for candidate in current["enum"]
        ):
            errors.append(f"{path}: value is not in the allowed enum")

        expected_type = current.get("type")
        if expected_type is not None:
            expected = (
                [expected_type] if isinstance(expected_type, str) else expected_type
            )
            if not isinstance(expected, list) or not all(
                isinstance(item, str) for item in expected
            ):
                raise ValueError(f"{path}: invalid schema type declaration")
            if not any(json_type_matches(instance, item) for item in expected):
                errors.append(f"{path}: expected type {' or '.join(expected)}")
                return errors

        for subschema in current.get("allOf", []):
            errors.extend(self.validate(instance, subschema, path))

        if "oneOf" in current:
            results = [
                self.validate(instance, subschema, path)
                for subschema in current["oneOf"]
            ]
            if sum(not result for result in results) != 1:
                errors.append(f"{path}: expected exactly one oneOf branch to match")

        if "anyOf" in current:
            if not any(
                not self.validate(instance, subschema, path)
                for subschema in current["anyOf"]
            ):
                errors.append(f"{path}: expected at least one anyOf branch to match")

        if "not" in current and not self.validate(instance, current["not"], path):
            errors.append(f"{path}: value matches a prohibited schema")

        if "if" in current:
            condition_matches = not self.validate(instance, current["if"], path)
            branch = current.get("then" if condition_matches else "else")
            if isinstance(branch, dict):
                errors.extend(self.validate(instance, branch, path))

        if isinstance(instance, dict):
            required = current.get("required", [])
            for key in required:
                if key not in instance:
                    errors.append(f"{child_path(path, key)}: required property is missing")
            properties = current.get("properties", {})
            for key, value in instance.items():
                if key in properties:
                    errors.extend(
                        self.validate(value, properties[key], child_path(path, key))
                    )
                elif current.get("additionalProperties") is False:
                    errors.append(f"{child_path(path, key)}: unknown property")
                elif isinstance(current.get("additionalProperties"), dict):
                    errors.extend(
                        self.validate(
                            value,
                            current["additionalProperties"],
                            child_path(path, key),
                        )
                    )

        if isinstance(instance, list):
            if len(instance) < current.get("minItems", 0):
                errors.append(
                    f"{path}: expected at least {current['minItems']} array item(s)"
                )
            if "maxItems" in current and len(instance) > current["maxItems"]:
                errors.append(
                    f"{path}: expected no more than {current['maxItems']} array item(s)"
                )
            item_schema = current.get("items")
            if isinstance(item_schema, dict):
                for index, value in enumerate(instance):
                    errors.extend(
                        self.validate(value, item_schema, f"{path}[{index}]")
                    )
            if current.get("uniqueItems"):
                for index, value in enumerate(instance):
                    if any(json_equal(value, prior) for prior in instance[:index]):
                        errors.append(f"{path}[{index}]: duplicate array item")
            if "contains" in current:
                matches = sum(
                    not self.validate(value, current["contains"], f"{path}[{index}]")
                    for index, value in enumerate(instance)
                )
                minimum = current.get("minContains", 1)
                maximum = current.get("maxContains")
                if matches < minimum or (
                    isinstance(maximum, int) and matches > maximum
                ):
                    errors.append(f"{path}: contains constraint is not satisfied")

        if isinstance(instance, str):
            if len(instance) < current.get("minLength", 0):
                errors.append(
                    f"{path}: expected at least {current['minLength']} character(s)"
                )
            if "pattern" in current and re.search(current["pattern"], instance) is None:
                errors.append(f"{path}: value does not match the required pattern")

        if (
            isinstance(instance, (int, float))
            and not isinstance(instance, bool)
            and math.isfinite(float(instance))
        ):
            if "minimum" in current and instance < current["minimum"]:
                errors.append(f"{path}: value is below minimum {current['minimum']}")
            if "maximum" in current and instance > current["maximum"]:
                errors.append(f"{path}: value is above maximum {current['maximum']}")

        return errors


def read_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} not found: {display_path(path)}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"{label} is not valid UTF-8: {display_path(path)}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{label} is invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def main() -> int:
    args = parse_args()
    try:
        schema = read_json(args.schema, "schema")
        packet = read_json(args.packet, "packet")
        if not isinstance(schema, dict):
            raise ValueError("schema root must be an object")
        errors = sorted(set(SchemaValidator(schema).validate(packet)))
    except (OSError, ValueError) as exc:
        message = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        print(f"validate_packet: {message}", file=sys.stderr)
        emit({"ok": False, "error": message}, pretty=args.pretty)
        return 2

    result = {
        "ok": not errors,
        "packet": display_path(args.packet),
        "schema": display_path(args.schema),
        "schema_version": packet.get("schema_version")
        if isinstance(packet, dict)
        else None,
        "errors": errors,
    }
    emit(result, pretty=args.pretty)
    if errors:
        print(
            f"validate_packet: rejected packet with {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
