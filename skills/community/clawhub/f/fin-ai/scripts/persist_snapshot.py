#!/usr/bin/env python3
"""Phase-1 snapshot persistence workflow."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from paths import DEFAULT_PROFILE, bootstrap_portfolio_dir, resolve_portfolio_dir
CSV_HEADER = (
    "date,total_value,total_cost,total_profit,return_pct,daily_change,daily_change_pct,"
    "max_drawdown_pct,capital_change,market_daily_change,market_daily_change_pct\n"
)


class PersistSnapshotError(Exception):
    """Raised when the snapshot payload cannot be persisted as a valid artifact."""


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    required_top_level = ("date", "fx_rates", "groups", "summary")
    missing_fields = [field for field in required_top_level if field not in snapshot]
    if missing_fields:
        raise PersistSnapshotError(f"snapshot 缺少顶层字段: {', '.join(missing_fields)}")

    if not isinstance(snapshot["groups"], dict):
        raise PersistSnapshotError("snapshot.groups 必须是对象/映射")
    if not isinstance(snapshot["summary"], dict):
        raise PersistSnapshotError("snapshot.summary 必须是对象")

    required_summary_fields = (
        "total_value",
        "total_cost",
        "total_profit",
        "total_return_pct",
        "daily_change",
        "daily_change_pct",
        "max_drawdown_pct",
        "capital_change",
        "market_daily_change",
        "market_daily_change_pct",
    )
    missing_summary_fields = [field for field in required_summary_fields if field not in snapshot["summary"]]
    if missing_summary_fields:
        raise PersistSnapshotError(f"snapshot.summary 缺少字段: {', '.join(missing_summary_fields)}")


def write_snapshot(portfolio_dir: Path, snapshot: dict[str, Any]) -> Path:
    snap_dir = portfolio_dir / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    snap_path = snap_dir / f"{snapshot['date']}.json"
    snap_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return snap_path


def _snapshot_to_history_row(snapshot: dict[str, Any]) -> str:
    summary = snapshot["summary"]
    return (
        f"{snapshot['date']},{summary['total_value']},{summary['total_cost']},{summary['total_profit']},"
        f"{summary['total_return_pct']},{summary['daily_change']},{summary['daily_change_pct']},"
        f"{summary['max_drawdown_pct']},{summary['capital_change']},{summary['market_daily_change']},"
        f"{summary['market_daily_change_pct']}\n"
    )


def update_history(portfolio_dir: Path, snapshot: dict[str, Any]) -> Path:
    history_path = portfolio_dir / "history.csv"
    new_row = _snapshot_to_history_row(snapshot)
    date_str = snapshot["date"]

    if history_path.exists():
        lines = history_path.read_text(encoding="utf-8").splitlines(keepends=True)
        data_lines = [line for line in lines if not line.startswith("date,") and not line.startswith(f"{date_str},")]
        with history_path.open("w", encoding="utf-8") as f:
            f.write(CSV_HEADER)
            f.writelines(data_lines)
            f.write(new_row)
    else:
        with history_path.open("w", encoding="utf-8") as f:
            f.write(CSV_HEADER)
            f.write(new_row)

    return history_path


def persist_snapshot(
    portfolio_dir: Path,
    snapshot: dict[str, Any],
    *,
    update_history_csv: bool = True,
) -> dict[str, Any]:
    bootstrap_portfolio_dir(portfolio_dir)
    validate_snapshot(snapshot)
    snapshot_path = write_snapshot(portfolio_dir, snapshot)
    history_path = None
    warnings: list[str] = []
    if update_history_csv:
        try:
            history_path = update_history(portfolio_dir, snapshot)
        except Exception as exc:
            warnings.append(f"history.csv 更新失败，但 snapshot 已写入成功（{exc.__class__.__name__}）")
    return {
        "snapshot_path": str(snapshot_path),
        "history_path": str(history_path) if history_path else None,
        "written_at": datetime.now().isoformat(),
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Persist a snapshot-aligned JSON result to engine/portfolio.")
    parser.add_argument("--input", required=True, help="Path to the analysis_result JSON file")
    parser.add_argument(
        "--portfolio-dir",
        help="持仓数据目录；未提供时优先使用仓库内 engine/portfolio，否则使用用户 profile 目录",
    )
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="用户数据 profile 名，默认 default")
    parser.add_argument("--skip-history", action="store_true", help="Do not update history.csv")
    args = parser.parse_args()

    snapshot = _read_json(Path(args.input))
    portfolio_dir = resolve_portfolio_dir(portfolio_dir=args.portfolio_dir, profile=args.profile)
    result = persist_snapshot(portfolio_dir, snapshot, update_history_csv=not args.skip_history)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
