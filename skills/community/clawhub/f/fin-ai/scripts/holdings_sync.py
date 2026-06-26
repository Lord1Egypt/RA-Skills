#!/usr/bin/env python3
"""Phase-1 holdings sync workflow.

This script is intentionally thin:
- validate a holdings-like payload
- normalize the payload into retained V2 holdings semantics
- replace groups or overwrite the full holdings payload
- write a complete updated holdings payload back to disk
"""

from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from paths import DEFAULT_PROFILE, bootstrap_portfolio_dir, resolve_portfolio_dir


class HoldingsSyncError(Exception):
    """Raised when the incoming holdings payload is structurally invalid."""


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_current_holdings(portfolio_dir: Path, date_str: str) -> dict[str, Any]:
    holdings_path = portfolio_dir / "holdings" / f"{date_str}.json"
    if holdings_path.exists():
        return _read_json(holdings_path)
    return {"date": date_str, "updated_at": datetime.now().isoformat(), "groups": {}}


def _coerce_number(value: Any, *, field_name: str) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            raise HoldingsSyncError(f"{field_name} 不能为空字符串")
        try:
            return float(stripped)
        except ValueError as exc:
            raise HoldingsSyncError(f"{field_name} 不是合法数字: {value}") from exc
    raise HoldingsSyncError(f"{field_name} 不是合法数字: {value!r}")


def validate_holdings_payload(payload: dict[str, Any]) -> None:
    if "date" not in payload:
        raise HoldingsSyncError("缺少顶层字段 date")
    if "groups" not in payload:
        raise HoldingsSyncError("缺少顶层字段 groups")
    if not isinstance(payload["groups"], dict):
        raise HoldingsSyncError("groups 必须是对象/映射")

    for group_name, group_data in payload["groups"].items():
        if not isinstance(group_name, str) or not group_name.strip():
            raise HoldingsSyncError("group 名必须是非空字符串")
        if not isinstance(group_data, dict):
            raise HoldingsSyncError(f"group {group_name} 的值必须是对象")
        if "positions" not in group_data:
            raise HoldingsSyncError(f"group {group_name} 缺少 positions")
        if not isinstance(group_data["positions"], list):
            raise HoldingsSyncError(f"group {group_name} 的 positions 必须是列表")

        for index, position in enumerate(group_data["positions"]):
            if not isinstance(position, dict):
                raise HoldingsSyncError(f"group {group_name} 的 position[{index}] 必须是对象")
            ticker = position.get("ticker")
            if not isinstance(ticker, str) or not ticker.strip():
                raise HoldingsSyncError(f"group {group_name} 的 position[{index}] 缺少有效 ticker")
            quantity = position.get("quantity")
            if quantity is None:
                raise HoldingsSyncError(f"group {group_name} 的 position[{index}] 缺少 quantity")
            quantity_number = _coerce_number(quantity, field_name=f"{group_name}.positions[{index}].quantity")
            if quantity_number < 0:
                raise HoldingsSyncError(f"group {group_name} 的 position[{index}] quantity 不能为负数")

            if "cost_price" in position and position["cost_price"] not in (None, ""):
                _coerce_number(position["cost_price"], field_name=f"{group_name}.positions[{index}].cost_price")


def normalize_holdings_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    normalized = copy.deepcopy(payload)
    warnings: list[str] = []

    normalized["date"] = str(normalized["date"]).strip()
    normalized["updated_at"] = normalized.get("updated_at") or datetime.now().isoformat()

    groups: dict[str, Any] = {}
    for raw_group_name, raw_group in normalized["groups"].items():
        group_name = raw_group_name.strip()
        group = dict(raw_group)

        group["cash"] = _coerce_number(group.get("cash", 0), field_name=f"{group_name}.cash")
        group["fund"] = _coerce_number(group.get("fund", 0), field_name=f"{group_name}.fund")
        group["cost_basis"] = _coerce_number(group.get("cost_basis", 0), field_name=f"{group_name}.cost_basis")

        normalized_positions: list[dict[str, Any]] = []
        seen_tickers: set[str] = set()
        duplicate_tickers: set[str] = set()

        for index, raw_position in enumerate(group["positions"]):
            ticker = str(raw_position["ticker"]).strip()
            name = str(raw_position.get("name", "")).strip()
            quantity = _coerce_number(raw_position["quantity"], field_name=f"{group_name}.positions[{index}].quantity")

            cost_price_raw = raw_position.get("cost_price", 0)
            if cost_price_raw in (None, ""):
                warnings.append(f"{group_name}:{ticker} 缺少 cost_price，已回填为 0")
                cost_price = 0.0
            else:
                cost_price = _coerce_number(cost_price_raw, field_name=f"{group_name}.positions[{index}].cost_price")

            if not name:
                warnings.append(f"{group_name}:{ticker} 缺少 name，已保留为空字符串")

            if ticker in seen_tickers:
                duplicate_tickers.add(ticker)
            seen_tickers.add(ticker)

            normalized_positions.append(
                {
                    "name": name,
                    "ticker": ticker,
                    "quantity": int(quantity) if float(quantity).is_integer() else quantity,
                    "cost_price": cost_price,
                }
            )

        for ticker in sorted(duplicate_tickers):
            warnings.append(f"{group_name} 内存在重复 ticker: {ticker}（phase 1 仅告警，不自动合并）")

        group["positions"] = normalized_positions
        groups[group_name] = group

    normalized["groups"] = groups
    return normalized, warnings


def merge_or_replace_groups(
    current_holdings: dict[str, Any],
    incoming_holdings: dict[str, Any],
    *,
    mode: str,
) -> dict[str, Any]:
    if mode not in {"replace_groups", "overwrite_all"}:
        raise HoldingsSyncError(f"不支持的 holdings sync 模式: {mode}")

    merged = copy.deepcopy(current_holdings)
    merged["date"] = incoming_holdings["date"]
    merged["updated_at"] = datetime.now().isoformat()

    if mode == "overwrite_all":
        merged["groups"] = dict(incoming_holdings["groups"])
    else:
        current_groups = dict(merged.get("groups", {}))
        for group_name, group_data in incoming_holdings["groups"].items():
            current_groups[group_name] = group_data
        merged["groups"] = current_groups

    return merged


def build_sync_result(
    current_holdings: dict[str, Any],
    updated_holdings: dict[str, Any],
    incoming_group_names: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    current_group_names = set(current_holdings.get("groups", {}).keys())
    changed_groups = sorted(incoming_group_names)
    new_groups = sorted(set(incoming_group_names) - current_group_names)
    changed_positions = {
        group_name: len(group_data.get("positions", []))
        for group_name, group_data in updated_holdings.get("groups", {}).items()
        if group_name in incoming_group_names
    }

    return {
        "changed_groups": changed_groups,
        "new_groups": new_groups,
        "changed_positions": changed_positions,
        "warnings": warnings,
        "source_date": updated_holdings.get("date"),
    }


def write_holdings(portfolio_dir: Path, holdings_payload: dict[str, Any]) -> Path:
    holdings_path = portfolio_dir / "holdings" / f"{holdings_payload['date']}.json"
    _write_json(holdings_path, holdings_payload)
    return holdings_path


def sync_holdings(
    portfolio_dir: Path,
    source_payload: dict[str, Any],
    *,
    mode: str = "replace_groups",
) -> dict[str, Any]:
    bootstrap_portfolio_dir(portfolio_dir)
    validate_holdings_payload(source_payload)
    normalized_payload, warnings = normalize_holdings_payload(source_payload)
    current_holdings = load_current_holdings(portfolio_dir, normalized_payload["date"])
    updated_holdings = merge_or_replace_groups(current_holdings, normalized_payload, mode=mode)
    holdings_path = write_holdings(portfolio_dir, updated_holdings)
    sync_result = build_sync_result(
        current_holdings,
        updated_holdings,
        list(normalized_payload["groups"].keys()),
        warnings,
    )
    sync_result["mode"] = mode
    return {
        "updated_holdings": updated_holdings,
        "updated_lot_ledger": None,
        "sync_result": sync_result,
        "written_path": str(holdings_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="校验、规范化并写入 holdings-like 持仓数据。")
    parser.add_argument("--input", required=True, help="Path to incoming holdings-like JSON payload")
    parser.add_argument(
        "--portfolio-dir",
        help="持仓数据目录；未提供时优先使用仓库内 engine/portfolio，否则使用用户 profile 目录",
    )
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="用户数据 profile 名，默认 default")
    parser.add_argument(
        "--mode",
        choices=["replace_groups", "overwrite_all"],
        default="replace_groups",
        help="replace_groups=只替换输入里出现的账户组；overwrite_all=用输入整份覆盖当天 holdings",
    )
    parser.add_argument("--output", help="Optional path to write the sync result JSON")
    args = parser.parse_args()

    source_payload = _read_json(Path(args.input))
    portfolio_dir = resolve_portfolio_dir(portfolio_dir=args.portfolio_dir, profile=args.profile)
    result = sync_holdings(portfolio_dir, source_payload, mode=args.mode)

    if args.output:
        output_path = Path(args.output)
        _write_json(output_path, result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
