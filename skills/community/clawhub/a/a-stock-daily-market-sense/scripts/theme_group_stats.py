#!/usr/bin/env python3
"""Aggregate deterministic statistics for model-defined market themes.

The model owns theme and subline grouping.  This script only validates that
the mapping refers to records in module3_money_effect.json and calculates
amount/return/volume statistics for those groups.  It intentionally emits no
theme rating, industry judgment, catalyst conclusion, or trading advice.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import median
from typing import Any, Iterable


NUMERIC_FIELDS = (
    "amount_100m_yuan",
    "pct_chg",
    "ret_5d",
    "rel_ret_5d",
    "sustained_volume_days_5",
)


class ValidationError(ValueError):
    """Raised when a context or mapping payload violates the input contract."""


def _load_json(path: Path, label: str) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ValidationError(f"{label} 文件不存在: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"{label} 不是合法 JSON: {path}（第 {exc.lineno} 行，第 {exc.colno} 列）"
        ) from exc


def _require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{path} 必须是 JSON object")
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{path} 必须是 JSON array")
    return value


def _require_name(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} 必须是非空字符串")
    return value.strip()


def _optional_number(value: Any, path: str) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValidationError(f"{path} 必须是数值或 null，不能是布尔值")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{path} 必须是数值或 null，实际为 {value!r}") from exc
    if not math.isfinite(number):
        raise ValidationError(f"{path} 必须是有限数值或 null，实际为 {value!r}")
    return number


def _round_optional(value: float | None) -> float | None:
    return None if value is None else round(value, 2)


def _median(records: Iterable[dict[str, Any]], field: str) -> float | None:
    values = [record[field] for record in records if record[field] is not None]
    return _round_optional(float(median(values))) if values else None


def _parse_records(context: Any) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    root = _require_object(context, "context")
    money_effect = _require_object(root.get("money_effect"), "context.money_effect")
    grouping = _require_object(
        money_effect.get("theme_grouping_aid"),
        "context.money_effect.theme_grouping_aid",
    )
    raw_records = _require_list(
        grouping.get("records"),
        "context.money_effect.theme_grouping_aid.records",
    )

    records: list[dict[str, Any]] = []
    by_code: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_records):
        path = f"context.money_effect.theme_grouping_aid.records[{index}]"
        item = _require_object(raw, path)
        code = _require_name(item.get("ts_code"), f"{path}.ts_code")
        if code in by_code:
            raise ValidationError(f"{path}.ts_code 重复: {code}")

        record: dict[str, Any] = {
            "ts_code": code,
            "name": item.get("name") if isinstance(item.get("name"), str) else None,
        }
        for field in NUMERIC_FIELDS:
            record[field] = _optional_number(item.get(field), f"{path}.{field}")
        if record["amount_100m_yuan"] is not None and record["amount_100m_yuan"] < 0:
            raise ValidationError(f"{path}.amount_100m_yuan 不能为负数")
        records.append(record)
        by_code[code] = record
    return records, by_code


def _parse_members(value: Any, path: str, known_codes: set[str]) -> list[str]:
    raw_members = _require_list(value, path)
    members: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_members):
        code = _require_name(raw, f"{path}[{index}]")
        if code in seen:
            raise ValidationError(f"{path}[{index}] 重复成员: {code}")
        if code not in known_codes:
            raise ValidationError(f"{path}[{index}] 引用了强势池中不存在的代码: {code}")
        seen.add(code)
        members.append(code)
    return members


def _parse_mapping(mapping: Any, known_codes: set[str]) -> list[dict[str, Any]]:
    root = _require_object(mapping, "mapping")
    raw_themes = _require_list(root.get("themes"), "mapping.themes")
    themes: list[dict[str, Any]] = []
    theme_names: set[str] = set()
    member_owner: dict[str, str] = {}

    for theme_index, raw_theme in enumerate(raw_themes):
        path = f"mapping.themes[{theme_index}]"
        item = _require_object(raw_theme, path)
        name = _require_name(item.get("name"), f"{path}.name")
        if name in theme_names:
            raise ValidationError(f"{path}.name 重复: {name}")
        theme_names.add(name)
        members = _parse_members(item.get("members"), f"{path}.members", known_codes)
        for code in members:
            previous_owner = member_owner.get(code)
            if previous_owner is not None:
                raise ValidationError(
                    f"{path}.members 中的 {code} 已归入父主题 {previous_owner!r}；"
                    "同一成员不得跨父主题重复归类"
                )
            member_owner[code] = name
        member_set = set(members)

        raw_sublines = _require_list(item.get("sublines"), f"{path}.sublines")
        sublines: list[dict[str, Any]] = []
        subline_names: set[str] = set()
        for subline_index, raw_subline in enumerate(raw_sublines):
            subpath = f"{path}.sublines[{subline_index}]"
            subitem = _require_object(raw_subline, subpath)
            subname = _require_name(subitem.get("name"), f"{subpath}.name")
            if subname in subline_names:
                raise ValidationError(f"{subpath}.name 重复: {subname}")
            subline_names.add(subname)
            submembers = _parse_members(
                subitem.get("members"),
                f"{subpath}.members",
                known_codes,
            )
            outside_parent = [code for code in submembers if code not in member_set]
            if outside_parent:
                raise ValidationError(
                    f"{subpath}.members 必须是父主题 {name!r} 的子集；越界代码: "
                    + ", ".join(outside_parent)
                )
            sublines.append({"name": subname, "members": submembers})

        themes.append({"name": name, "members": members, "sublines": sublines})
    return themes


def _leaders(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        records,
        key=lambda record: (
            record["amount_100m_yuan"] is None,
            -(record["amount_100m_yuan"] or 0.0),
            record["ts_code"],
        ),
    )
    return [
        {
            "ts_code": record["ts_code"],
            "name": record["name"],
            "amount_100m_yuan": _round_optional(record["amount_100m_yuan"]),
        }
        for record in ordered[:3]
    ]


def _stats(
    member_codes: list[str],
    by_code: dict[str, dict[str, Any]],
    money_pool_amount: float,
    parent_amount: float | None,
) -> dict[str, Any]:
    records = [by_code[code] for code in member_codes]
    total_amount = sum(record["amount_100m_yuan"] or 0.0 for record in records)
    share_of_pool = total_amount / money_pool_amount * 100 if money_pool_amount > 0 else 0.0
    if parent_amount is None:
        share_of_parent = 100.0 if total_amount > 0 else 0.0
    else:
        share_of_parent = total_amount / parent_amount * 100 if parent_amount > 0 else 0.0

    return {
        "member_count": len(member_codes),
        "total_amount_100m_yuan": round(total_amount, 2),
        "share_of_money_pool_pct": round(share_of_pool, 2),
        "share_of_parent_theme_pct": round(share_of_parent, 2),
        "median_pct_chg": _median(records, "pct_chg"),
        "median_ret_5d": _median(records, "ret_5d"),
        "median_rel_ret_5d": _median(records, "rel_ret_5d"),
        "median_sustained_volume_days_5": _median(records, "sustained_volume_days_5"),
        "leaders": _leaders(records),
    }


def build_theme_group_stats(context: Any, mapping: Any) -> dict[str, Any]:
    """Validate model grouping and return deterministic aggregate statistics."""

    records, by_code = _parse_records(context)
    themes = _parse_mapping(mapping, set(by_code))
    money_pool_amount = sum(record["amount_100m_yuan"] or 0.0 for record in records)

    output_themes: list[dict[str, Any]] = []
    for theme in themes:
        theme_stats = _stats(theme["members"], by_code, money_pool_amount, None)
        parent_amount = theme_stats["total_amount_100m_yuan"]
        output_sublines = []
        for subline in theme["sublines"]:
            output_sublines.append(
                {
                    "name": subline["name"],
                    "members": subline["members"],
                    **_stats(subline["members"], by_code, money_pool_amount, parent_amount),
                }
            )
        output_themes.append(
            {
                "name": theme["name"],
                "members": theme["members"],
                **theme_stats,
                "sublines": output_sublines,
            }
        )

    return {
        "money_pool": {
            "member_count": len(records),
            "total_amount_100m_yuan": round(money_pool_amount, 2),
        },
        "themes": output_themes,
        "calculation_note": (
            "仅按模型提供的成员映射做确定性统计；空数值不参与中位数，缺失成交额按 0 计入合计。"
            "本文件不包含任何模型判断、评级或投资建议。"
        ),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="校验模块 3 主题成员映射并计算确定性成交额/收益/放量统计。"
    )
    parser.add_argument("--context", required=True, type=Path, help="module3_money_effect.json")
    parser.add_argument("--mapping", required=True, type=Path, help="module3_theme_map.json")
    parser.add_argument("--output", required=True, type=Path, help="module3_theme_stats.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        context = _load_json(args.context, "context")
        mapping = _load_json(args.mapping, "mapping")
        payload = build_theme_group_stats(context, mapping)
        _write_json(args.output, payload)
    except ValidationError as exc:
        raise SystemExit(f"theme_group_stats 输入错误: {exc}") from exc
    print(f"已写入主题确定性统计: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
