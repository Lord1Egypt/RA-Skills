#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print a pre-call parameter confirmation table for a Dataify Google skill."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


EMPTY_DEFAULTS = {
    "",
    "-",
    "none",
    "`none`",
    "no default",
    "no documented default",
    "无",
    "空",
    "无默认值",
    "none.",
    "unset",
    "`unset`",
    "unset, meaning global",
    "unset, meaning web search",
}


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def strip_cell(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^`(.+)`$", r"\1", value)
    value = value.replace("<br>", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def split_row(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    inner = line.strip("|")
    placeholder = "\uE000"
    inner = inner.replace("\\|", placeholder)
    return [strip_cell(part.replace(placeholder, "|")) for part in inner.split("|")]


def normalize_name(value: str) -> str:
    value = strip_cell(value)
    value = value.lstrip("»").strip()
    value = re.sub(r"^\*+|\*+$", "", value).strip()
    return value


def normalize_header(value: str) -> str:
    return re.sub(r"\s+", "", strip_cell(value).lower())


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def default_from_text(field: str, text: str, skill_name: str) -> str:
    lowered = text.lower()
    if field != "engine" and (
        "no documented default" in lowered
        or "no default" in lowered
        or "no explicit default" in lowered
        or "文档未给出" in text
        or "无默认" in text
    ):
        return ""
    if "example" in lowered or "例如" in lowered or "e.g." in lowered:
        no_example_text = re.split(r"example|例如|e\.g\.", text, maxsplit=1, flags=re.IGNORECASE)[0]
    else:
        no_example_text = text

    if field == "engine":
        match = re.search(r"`(google(?:_[a-z0-9]+)+|google)`|\b(google(?:_[a-z0-9]+)+|google)\b", no_example_text)
        if match:
            return next(group for group in match.groups() if group)
        suffix = skill_name.removeprefix("dataify-google-").replace("-", "_")
        return "google" if suffix == "search" else f"google_{suffix}"

    always_match = re.search(r"Always\s+`?([A-Za-z0-9_.+-]+)`?", no_example_text, flags=re.IGNORECASE)
    if always_match:
        return always_match.group(1).strip("`'\"。.,，")

    fixed_match = re.search(r"Fixed(?: value)?\s*`?([A-Za-z0-9_.+-]+)`?", no_example_text, flags=re.IGNORECASE)
    if fixed_match:
        return fixed_match.group(1).strip("`'\"。.,，")

    default_match = re.search(
        r"(?:default(?:s| value)?|默认(?:值)?|默认为|固定值|fixed(?: value)?)"
        r"(?:\s*(?:is|为|=|:|：|to)\s*|\s*[`'\"])([A-Za-z0-9_.+-]+)",
        no_example_text,
        flags=re.IGNORECASE,
    )
    if default_match:
        candidate = default_match.group(1).strip().strip("`'\"。.,，")
        if candidate.lower() not in {"is", "value", "为", "example"}:
            return candidate

    if field == "json" and re.search(r"default\s*`?1`?|默认(?:值)?\s*`?1`?|默认为\s*JSON", no_example_text, re.I):
        return "1"
    if field == "no_cache" and re.search(r"default.*false|false.*default|默认.*false|false.*默认", no_example_text, re.I):
        return "false"
    if field == "google_domain" and re.search(r"default.*google\.com|默认.*google\.com", no_example_text, re.I):
        return "google.com"
    return ""


def normalize_default(value: str, field: str, combined_text: str, skill_name: str) -> str:
    value = strip_cell(value).strip("`")
    lowered = value.lower().strip()
    if (
        lowered in EMPTY_DEFAULTS
        or "no default" in lowered
        or "无默认" in value
        or lowered.startswith("depends on")
        or lowered.startswith("omit")
    ):
        return ""
    if lowered.startswith("fixed "):
        value = value[6:].strip("` ")
    if lowered.startswith("always "):
        inferred = default_from_text(field, value, skill_name)
        if inferred:
            return inferred
    if value.startswith("固定"):
        fixed = default_from_text(field, value, skill_name)
        if fixed:
            return fixed
    if "example" in lowered or "例如" in value or "e.g." in lowered:
        inferred = default_from_text(field, combined_text, skill_name)
        return inferred
    inferred = default_from_text(field, value, skill_name)
    if inferred:
        return inferred
    return value


def parse_markdown_tables(markdown: str, skill_name: str) -> list[dict[str, str]]:
    fields: list[dict[str, str]] = []
    seen: set[str] = set()
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|") or index + 1 >= len(lines) or not is_separator(lines[index + 1]):
            index += 1
            continue

        headers = split_row(lines[index])
        normalized_headers = [normalize_header(header) for header in headers]
        field_idx = next(
            (
                i
                for i, header in enumerate(normalized_headers)
                if header in {"field", "parameter", "参数名", "名称"}
                or "field" == header
                or "parameter" == header
            ),
            None,
        )
        if field_idx is None:
            index += 1
            continue

        pure_default_headers = {"default", "defaultvalue", "documenteddefault", "默认", "默认值", "默认值来源"}
        default_idx = next((i for i, header in enumerate(normalized_headers) if header in pure_default_headers), None)
        default_hint_idx = next(
            (i for i, header in enumerate(normalized_headers) if ("default" in header or "默认" in header) and header not in pure_default_headers),
            None,
        )
        desc_idx = next(
            (
                i
                for i, header in enumerate(normalized_headers)
                if "description" in header
                or "meaning" in header
                or "说明" in header
                or "valueorrule" in header
                or "valueordefault" in header
                or "acceptedvalues" in header
                or "acceptedvaluesorformat" in header
                or "value" == header
            ),
            None,
        )

        row_index = index + 2
        while row_index < len(lines) and lines[row_index].lstrip().startswith("|"):
            row = split_row(lines[row_index])
            if len(row) < len(headers):
                row += [""] * (len(headers) - len(row))
            name = normalize_name(row[field_idx])
            if not name or name.lower() == "authorization":
                row_index += 1
                continue
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
                row_index += 1
                continue
            if name in seen:
                row_index += 1
                continue

            combined = " ".join(cell for i, cell in enumerate(row) if i != field_idx)
            if default_idx is not None:
                default = normalize_default(row[default_idx], name, combined, skill_name)
            elif default_hint_idx is not None:
                default = default_from_text(name, row[default_hint_idx], skill_name)
            else:
                default = default_from_text(name, combined, skill_name)
            if desc_idx is not None:
                description = row[desc_idx]
            else:
                description = combined
            if not description:
                description = combined
            fields.append({"name": name, "default": default, "description": description})
            seen.add(name)
            row_index += 1
        index = row_index
    return fields


def parse_script_fields(skill_dir: Path) -> list[str]:
    scripts = [path for path in (skill_dir / "scripts").glob("*.py") if path.name != "preview_params.py"]
    if not scripts:
        return []
    raw = scripts[0].read_text(encoding="utf-8", errors="ignore")
    for constant in ("REQUEST_FIELDS", "TABLE_FIELDS", "DISPLAY_FIELDS", "PARAMETER_ORDER", "FIELDS"):
        match = re.search(rf"(?s){constant}\s*=\s*(\([^\)]*\))", raw)
        if not match:
            continue
        try:
            value = ast.literal_eval(match.group(1))
        except Exception:
            continue
        fields = [str(item) for item in value]
        if constant == "FIELDS":
            fields = ["engine"] + fields
        return [field for field in fields if field != "Authorization"]
    return []


def merge_with_script_fields(parsed: list[dict[str, str]], script_fields: list[str], skill_name: str) -> list[dict[str, str]]:
    by_name = {item["name"]: item for item in parsed}
    ordered: list[dict[str, str]] = []
    for field in script_fields:
        if field.lower() == "authorization":
            continue
        if field in by_name:
            ordered.append(by_name[field])
        else:
            default = default_from_text(field, "", skill_name) if field == "engine" else ""
            ordered.append({"name": field, "default": default, "description": ""})
    for item in parsed:
        if item["name"] not in {existing["name"] for existing in ordered}:
            ordered.append(item)
    return ordered


def parse_params_json(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--params-json 不是有效 JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("--params-json 必须是 JSON object")
    return {str(key): "" if val is None else str(val) for key, val in parsed.items()}


def parse_unknown_args(tokens: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if not token.startswith("--"):
            index += 1
            continue
        key_value = token[2:]
        if "=" in key_value:
            key, value = key_value.split("=", 1)
            params[key] = value
            index += 1
            continue
        key = key_value
        if index + 1 < len(tokens) and not tokens[index + 1].startswith("--"):
            params[key] = tokens[index + 1]
            index += 2
        else:
            params[key] = "true"
            index += 1
    return params


def main() -> int:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Preview Dataify request parameters.")
    parser.add_argument("--params-json", help="Current request parameters as a JSON object.")
    args, unknown = parser.parse_known_args()

    skill_dir = Path(__file__).resolve().parents[1]
    skill_name = skill_dir.name
    refs = sorted((skill_dir / "references").glob("*api.md"))
    if not refs:
        raise SystemExit("未找到 references/*api.md")

    markdown = refs[0].read_text(encoding="utf-8", errors="ignore")
    parsed = parse_markdown_tables(markdown, skill_name)
    fields = merge_with_script_fields(parsed, parse_script_fields(skill_dir), skill_name)
    current_values = parse_params_json(args.params_json)
    current_values.update(parse_unknown_args(unknown))

    print("| 参数名 | 当前值 | 默认值 | 说明 |")
    print("| --- | --- | --- | --- |")
    for item in fields:
        name = item["name"]
        default = item["default"]
        current = current_values.get(name, default)
        print(
            "| "
            + " | ".join(
                (
                    markdown_escape(name),
                    markdown_escape(current),
                    markdown_escape(default),
                    markdown_escape(item["description"]),
                )
            )
            + " |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
