#!/usr/bin/env python3
"""Thin phase-1 end-to-end runner for the portfolio workflows.

This script intentionally adds no new business logic. It only orchestrates:
1. holdings_sync (optional when an input payload is provided)
2. portfolio_analysis
3. persist_snapshot

For user safety, writes are previewed in a temporary working copy by default.
Only explicit confirmation enables persistent writes to the target directory.
"""

from __future__ import annotations

import argparse
import glob
import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

import holdings_sync
import init_portfolio
import persist_snapshot
import portfolio_analysis
from paths import DEFAULT_PROFILE, REPO_PORTFOLIO_DIR, bootstrap_portfolio_dir, resolve_portfolio_dir


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _prepare_working_portfolio_dir(
    portfolio_dir: Path,
    *,
    confirm_write: bool,
) -> tuple[Path, bool]:
    resolved_portfolio_dir = portfolio_dir.resolve()
    if confirm_write:
        return resolved_portfolio_dir, False

    temp_parent = Path(tempfile.mkdtemp(prefix="portfolio-workflows-safe-run-"))
    working_dir = temp_parent / "portfolio"
    shutil.copytree(resolved_portfolio_dir, working_dir)
    return working_dir, True


def build_user_summary(result: dict[str, Any]) -> dict[str, Any]:
    analysis_result = result["analysis_result"]
    summary = analysis_result["summary"]
    group_summaries = []

    for group_name, group_data in analysis_result["groups"].items():
        group_summaries.append(
            {
                "group": group_name,
                "total_value": group_data["total_value"],
                "profit": group_data["profit"],
                "return_pct": group_data["return_pct"],
                "positions": len(group_data.get("positions", [])),
            }
        )

    return {
        "date": result["date"],
        "mode": result["mode"],
        "requires_confirmation": result["requires_confirmation"],
        "data_directory": result["target_portfolio_dir"],
        "effective_run_directory": result["working_portfolio_dir"],
        "used_safe_mode": result["safe_mode"],
        "updated_holdings": bool(result.get("holdings_sync")),
        "will_write_real_data": result["confirm_write"],
        "summary": {
            "total_value": summary["total_value"],
            "total_cost": summary["total_cost"],
            "total_profit": summary["total_profit"],
            "total_return_pct": summary["total_return_pct"],
            "daily_change": summary["daily_change"],
            "daily_change_pct": summary["daily_change_pct"],
            "month_return_pct": summary["month_return_pct"],
            "max_drawdown_pct": summary["max_drawdown_pct"],
        },
        "groups": group_summaries,
        "snapshot_written_to": result["persist_result"]["snapshot_path"],
        "history_written_to": result["persist_result"]["history_path"],
        "confirmation_message": result.get("confirmation_message"),
        "warnings_count": len(result.get("warnings", [])),
        "warnings_preview": result.get("warnings", [])[:10],
    }


def clone_holdings(portfolio_dir: Path, date_str: str) -> tuple[Path, bool]:
    """Copy previous day's holdings as today's baseline.

    Returns (path, is_new) — path to today's holdings, whether it was newly created.
    """
    holdings_dir = portfolio_dir / "holdings"
    today_file = holdings_dir / f"{date_str}.json"

    if today_file.exists():
        return today_file, False

    # Find previous
    files = sorted(glob.glob(str(holdings_dir / "*.json")))
    prev_file = None
    for f in reversed(files):
        if Path(f).stem < date_str:
            prev_file = Path(f)
            break

    if not prev_file:
        # No previous file, check if any file exists at all
        if files:
            prev_file = Path(files[-1])

    if not prev_file:
        return today_file, False

    with open(prev_file) as f:
        data = json.load(f)

    data["date"] = date_str
    data["updated_at"] = datetime.now().isoformat()
    data["cloned_from"] = prev_file.stem

    holdings_dir.mkdir(parents=True, exist_ok=True)
    with open(today_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return today_file, True


def refresh_portfolio(
    portfolio_dir: Path,
    *,
    date_str: str,
    source_payload: dict[str, Any] | None = None,
    update_history_csv: bool = True,
    confirm_write: bool = False,
) -> dict[str, Any]:
    pipeline_warnings: list[str] = []
    sync_result: dict[str, Any] | None = None
    effective_date = date_str
    working_portfolio_dir, safe_mode = _prepare_working_portfolio_dir(
        portfolio_dir,
        confirm_write=confirm_write,
    )
    bootstrap_portfolio_dir(working_portfolio_dir)

    if safe_mode:
        pipeline_warnings.append(f"当前为预演模式，已切换到安全副本运行：{working_portfolio_dir}")

    # Auto-clone previous day's holdings if today doesn't exist
    cloned_from_stem = None
    cloned_path, is_new = clone_holdings(working_portfolio_dir, date_str)
    if is_new:
        cloned_from_stem = cloned_path.stem if "cloned_from" not in json.load(open(cloned_path)) else None
        # re-read to get cloned_from info
        with open(cloned_path) as f:
            cloned_data = json.load(f)
        cloned_from_stem = cloned_data.get("cloned_from", "unknown")
        pipeline_warnings.append(f"今日持仓为空，已从 {cloned_from_stem} 克隆持仓")

    if source_payload is not None:
        sync_result = holdings_sync.sync_holdings(working_portfolio_dir, source_payload)
        effective_date = sync_result["updated_holdings"]["date"]
        pipeline_warnings.extend(sync_result.get("sync_result", {}).get("warnings", []))
        if date_str != effective_date:
            pipeline_warnings.append(
                f"显式传入日期 {date_str} 与输入 payload 日期 {effective_date} 不一致，已采用 payload 日期"
            )

    analysis_result = portfolio_analysis.analyze_portfolio(working_portfolio_dir, effective_date)
    pipeline_warnings.extend(analysis_result.get("warnings", []))

    persist_result = persist_snapshot.persist_snapshot(
        working_portfolio_dir,
        analysis_result,
        update_history_csv=update_history_csv,
    )
    pipeline_warnings.extend(persist_result.get("warnings", []))

    requires_confirmation = not confirm_write
    if source_payload is not None:
        if requires_confirmation:
            confirmation_message = (
                "本次已在临时副本中预演持仓同步与结果刷新。"
                "请确认识别结果、影响账户组和 warnings 后，再执行正式写入。"
            )
            mode = "preview_sync"
        else:
            confirmation_message = "已按确认结果写入真实持久目录。"
            mode = "confirmed_sync"
    else:
        if requires_confirmation:
            confirmation_message = "本次已在临时副本中预演组合刷新。确认后可正式写入 snapshot/history。"
            mode = "preview_refresh"
        else:
            confirmation_message = "已按确认结果写入真实 snapshot/history。"
            mode = "confirmed_refresh"

    return {
        "status": "ok",
        "date": effective_date,
        "mode": mode,
        "confirm_write": confirm_write,
        "requires_confirmation": requires_confirmation,
        "confirmation_message": confirmation_message,
        "safe_mode": safe_mode,
        "target_portfolio_dir": str(portfolio_dir.resolve()),
        "working_portfolio_dir": str(working_portfolio_dir),
        "holdings_sync": sync_result,
        "analysis_result": analysis_result,
        "persist_result": persist_result,
        "warnings": pipeline_warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the phase-1 holdings -> analysis -> snapshot pipeline."
    )
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Target date YYYY-MM-DD")
    parser.add_argument("--input", help="Optional holdings-like JSON payload to sync before analysis")
    parser.add_argument(
        "--portfolio-dir",
        help="持仓数据目录；未提供时优先使用仓库内 engine/portfolio，否则使用用户 profile 目录",
    )
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="用户数据 profile 名，默认 default")
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="兼容旧参数；等价于 --confirm-write，会正式写入目标持久目录",
    )
    parser.add_argument(
        "--confirm-write",
        action="store_true",
        help="确认将本次结果正式写入目标持久目录；未提供时默认只在临时副本中预演",
    )
    parser.add_argument("--skip-history", action="store_true", help="Do not update history.csv")
    parser.add_argument("--output", help="Optional path to write the pipeline result JSON")
    parser.add_argument(
        "--output-format",
        choices=["summary", "debug"],
        default="summary",
        help="summary=面向用户的摘要输出；debug=完整内部 JSON 输出",
    )
    args = parser.parse_args()

    source_payload = _read_json(Path(args.input)) if args.input else None
    portfolio_dir = resolve_portfolio_dir(portfolio_dir=args.portfolio_dir, profile=args.profile)
    if not portfolio_dir.exists():
        init_portfolio.init_portfolio(
            portfolio_dir=portfolio_dir,
            profile=args.profile,
            set_default=False,
        )
    result = refresh_portfolio(
        portfolio_dir,
        date_str=args.date,
        source_payload=source_payload,
        update_history_csv=not args.skip_history,
        confirm_write=(args.confirm_write or args.in_place),
    )
    output_payload = build_user_summary(result) if args.output_format == "summary" else result

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
