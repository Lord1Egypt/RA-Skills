#!/usr/bin/env python
"""Break Watch intraday scanner - skill entry point.

Runs a single scan round for A-share stocks meeting
"volume breakout + rising + bullish candle" conditions.
Outputs structured JSON to stdout for the assistant to parse.

Usage:
    python scan_breakout.py [--mode all|watchlist] [--watchlist CODES]
                            [--min-rise-pct N] [--volume-ratio-threshold N]
                            [--output json|files|both]
                            [--config PATH]
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap import path so the script works from any cwd.
# ---------------------------------------------------------------------------
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "src"))

from break_watch.config import (  # noqa: E402
    AppConfig,
    DEFAULT_SERVERS,
    OutputConfig,
    ScanConfig,
    TdxConfig,
    load_config,
)
from break_watch.models import Signal  # noqa: E402
from break_watch.output import ResultWriter  # noqa: E402
from break_watch.scanner import ScanRunner  # noqa: E402
from break_watch.tdx_client import TdxClient  # noqa: E402
from break_watch.trading_time import is_trading_time, trading_progress  # noqa: E402
from break_watch.universe import build_universe  # noqa: E402


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Intraday volume breakout scanner for A-shares."
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config.toml. If omitted, uses built-in defaults.",
    )
    parser.add_argument(
        "--mode",
        choices=["all", "watchlist"],
        default=None,
        help="Scan mode: all-market or watchlist only.",
    )
    parser.add_argument(
        "--watchlist",
        default=None,
        help="Comma-separated stock codes, e.g. 600000,000001,300750.",
    )
    parser.add_argument(
        "--min-rise-pct",
        type=float,
        default=None,
        help="Minimum rise percentage threshold (default: 1.0).",
    )
    parser.add_argument(
        "--volume-ratio-threshold",
        type=float,
        default=None,
        help="Historical volume ratio threshold (default: 2.0).",
    )
    parser.add_argument(
        "--interval-spike-threshold",
        type=float,
        default=None,
        help="Intraday interval spike ratio threshold (default: 2.0).",
    )
    parser.add_argument(
        "--history-days",
        type=int,
        default=None,
        help="Number of historical trading days for baseline (default: 20).",
    )
    parser.add_argument(
        "--market-hours-only",
        action="store_true",
        default=None,
        help="Only scan during A-share trading hours.",
    )
    parser.add_argument(
        "--force-scan",
        action="store_true",
        help="Scan even outside trading hours (overrides market-hours-only).",
    )
    parser.add_argument(
        "--output",
        choices=["json", "files", "both"],
        default="json",
        help="Output format: json to stdout, files (CSV/HTML/TXT), or both.",
    )
    parser.add_argument(
        "--result-dir",
        default=None,
        help="Directory for output files when output=files or both.",
    )
    return parser


def resolve_config(args: argparse.Namespace) -> AppConfig:
    """Load config from file or build from CLI args with defaults."""

    if args.config:
        config = load_config(args.config)
    else:
        # Try config.toml in skill root, fall back to defaults.
        default_path = SKILL_ROOT / "config.toml"
        if default_path.exists():
            config = load_config(default_path)
        else:
            config = _default_config()

    # Apply CLI overrides.
    overrides: dict[str, object] = {}
    if args.mode is not None:
        overrides["mode"] = args.mode
    if args.watchlist is not None:
        codes = [c.strip() for c in args.watchlist.split(",") if c.strip()]
        overrides["watchlist"] = tuple(codes)
        if "mode" not in overrides:
            overrides["mode"] = "watchlist"
    if args.min_rise_pct is not None:
        overrides["min_rise_pct"] = args.min_rise_pct
    if args.volume_ratio_threshold is not None:
        overrides["volume_ratio_threshold"] = args.volume_ratio_threshold
    if args.interval_spike_threshold is not None:
        overrides["interval_spike_threshold"] = args.interval_spike_threshold
    if args.history_days is not None:
        overrides["history_days"] = args.history_days
    if args.market_hours_only is not None:
        overrides["market_hours_only"] = args.market_hours_only
    if args.force_scan:
        overrides["market_hours_only"] = False
    if args.result_dir is not None:
        result_dir = Path(args.result_dir)
        if not result_dir.is_absolute():
            result_dir = SKILL_ROOT / result_dir
        overrides["_result_dir"] = result_dir.resolve()

    if not overrides:
        return config

    return _apply_overrides(config, overrides)


def _default_config() -> AppConfig:
    """Build a config with sensible defaults (no file needed)."""
    root = SKILL_ROOT
    return AppConfig(
        path=root / "config.toml",
        root_dir=root,
        tdx=TdxConfig(servers=DEFAULT_SERVERS),
        scan=ScanConfig(),
        output=OutputConfig(
            log_dir=root / "logs",
            data_dir=root / "data",
            result_dir=root / "output",
        ),
    )


def _apply_overrides(config: AppConfig, overrides: dict[str, object]) -> AppConfig:
    scan_fields = {
        "mode",
        "watchlist",
        "min_rise_pct",
        "volume_ratio_threshold",
        "interval_spike_threshold",
        "history_days",
        "market_hours_only",
    }
    scan_overrides = {k: v for k, v in overrides.items() if k in scan_fields}
    result_dir = overrides.get("_result_dir")

    new_scan = config.scan
    if scan_overrides:
        new_scan = ScanConfig(
            **{
                **{
                    "mode": config.scan.mode,
                    "watchlist": config.scan.watchlist,
                    "exclude_star_market": config.scan.exclude_star_market,
                    "exclude_bse": config.scan.exclude_bse,
                    "scan_interval_seconds": config.scan.scan_interval_seconds,
                    "history_days": config.scan.history_days,
                    "volume_ratio_threshold": config.scan.volume_ratio_threshold,
                    "interval_spike_threshold": config.scan.interval_spike_threshold,
                    "interval_spike_window": config.scan.interval_spike_window,
                    "interval_spike_min_samples": config.scan.interval_spike_min_samples,
                    "min_rise_pct": config.scan.min_rise_pct,
                    "market_hours_only": config.scan.market_hours_only,
                    "repeat_alert": config.scan.repeat_alert,
                },
                **scan_overrides,
            }
        )

    new_output = config.output
    if result_dir is not None:
        new_output = OutputConfig(
            log_dir=config.output.log_dir,
            data_dir=config.output.data_dir,
            result_dir=Path(result_dir),
            csv_enabled=config.output.csv_enabled,
            html_enabled=config.output.html_enabled,
            ths_txt_enabled=config.output.ths_txt_enabled,
            ths_txt_code_format=config.output.ths_txt_code_format,
            console_enabled=config.output.console_enabled,
        )

    return AppConfig(
        path=config.path,
        root_dir=config.root_dir,
        tdx=config.tdx,
        scan=new_scan,
        output=new_output,
    )


def signal_to_dict(signal: Signal) -> dict:
    return {
        "code": signal.stock.code,
        "name": signal.stock.name or "-",
        "market": signal.stock.market_prefix,
        "timestamp": signal.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "price": round(signal.price, 4),
        "last_close": round(signal.last_close, 4),
        "open": round(signal.open, 4),
        "change_pct": round(signal.change_pct, 2),
        "current_volume": round(signal.current_volume, 2),
        "avg_volume": round(signal.avg_volume, 2),
        "expected_volume": round(signal.expected_volume, 2),
        "volume_ratio": round(signal.volume_ratio, 2),
        "interval_volume": (
            round(signal.interval_volume, 2) if signal.interval_volume is not None else None
        ),
        "interval_spike_ratio": (
            round(signal.interval_spike_ratio, 2)
            if signal.interval_spike_ratio is not None
            else None
        ),
        "server": signal.server,
    }


def run_scan(args: argparse.Namespace) -> int:
    errors: list[str] = []

    try:
        config = resolve_config(args)
    except Exception as exc:
        _emit_error(f"Config error: {exc}")
        return 2

    # Suppress console prints from the package; we control output.
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    now = datetime.now()
    trading = is_trading_time(now)
    progress = trading_progress(now)

    if config.scan.market_hours_only and not trading:
        _emit_json(
            {
                "scan_time": now.isoformat(),
                "is_trading_hours": False,
                "trading_progress": round(progress, 4),
                "universe_size": 0,
                "scannable_count": 0,
                "signal_count": 0,
                "signals": [],
                "message": (
                    "Current time is outside A-share trading hours "
                    "(09:30-11:30, 13:00-15:00). "
                    "Use --force-scan to scan anyway."
                ),
                "errors": [],
            }
        )
        return 0

    client = TdxClient(config.tdx)
    try:
        stocks = build_universe(config.scan, client)
        if not stocks:
            _emit_error("No stocks to scan. Check config or watchlist.")
            return 1

        # Build history baselines.
        runner = ScanRunner(
            config=config,
            client=client,
            sink=ResultWriter(config.output) if args.output in ("files", "both") else _NullSink(),
        )
        baselines = runner.build_baselines(stocks)
        scan_stocks = [s for s in stocks if s.key in baselines]

        if not scan_stocks:
            _emit_error("No stocks have enough history bars for baseline calculation.")
            return 1

        signals = runner.scan_once(scan_stocks, baselines)

        # Write files if requested.
        if args.output in ("files", "both") and signals:
            writer = ResultWriter(config.output)
            writer.emit(signals)

        result = {
            "scan_time": now.isoformat(),
            "server": client.current_server,
            "is_trading_hours": trading,
            "trading_progress": round(progress, 4),
            "universe_size": len(stocks),
            "scannable_count": len(scan_stocks),
            "signal_count": len(signals),
            "signals": [signal_to_dict(s) for s in signals],
            "config": {
                "mode": config.scan.mode,
                "min_rise_pct": config.scan.min_rise_pct,
                "volume_ratio_threshold": config.scan.volume_ratio_threshold,
                "interval_spike_threshold": config.scan.interval_spike_threshold,
                "history_days": config.scan.history_days,
            },
            "output_files": _output_file_paths(config) if args.output in ("files", "both") else None,
            "errors": errors,
        }
        _emit_json(result)
        return 0

    except Exception as exc:
        errors.append(str(exc))
        _emit_error(f"Scan failed: {exc}", errors=errors)
        return 1
    finally:
        client.close()


class _NullSink:
    """No-op sink for JSON-only output mode."""

    def emit(self, signals: list[Signal]) -> None:
        pass


def _output_file_paths(config: AppConfig) -> dict[str, str]:
    today = datetime.now().strftime("%Y%m%d")
    return {
        "csv": str(config.output.result_dir / f"signals_{today}.csv"),
        "html": str(config.output.result_dir / f"signals_{today}.html"),
        "ths_txt": str(config.output.result_dir / f"ths_codes_{today}.txt"),
    }


def _emit_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _emit_error(message: str, errors: list[str] | None = None) -> None:
    print(
        json.dumps(
            {
                "error": message,
                "errors": errors or [],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    return run_scan(args)


if __name__ == "__main__":
    raise SystemExit(main())
