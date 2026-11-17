from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import ConfigError, load_config
from .output import ResultWriter, setup_logging
from .scanner import ScanRunner
from .tdx_client import TdxClient
from .trading_time import is_trading_time
from .universe import build_universe

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Intraday volume breakout scanner.")
    parser.add_argument("--config", default=None, help="Path to config.toml.")
    parser.add_argument("--once", action="store_true", help="Run one scan round and exit.")
    args = parser.parse_args(argv)

    try:
        config = load_config(resolve_config_path(args.config))
    except ConfigError as exc:
        print(exc)
        return 2

    log_path = setup_logging(config.output)
    logger.info("Break Watch started. config=%s log=%s", config.path, log_path)

    client = TdxClient(config.tdx)
    try:
        stocks = build_universe(config.scan, client)
        if not stocks:
            logger.error("No stocks to scan.")
            print("No stocks to scan. Check config.toml.")
            return 1

        logger.info("Stock universe size: %s", len(stocks))
        print(f"Stock universe size: {len(stocks)}")

        writer = ResultWriter(config.output)
        runner = ScanRunner(config=config, client=client, sink=writer)
        baselines = runner.build_baselines(stocks)
        scan_stocks = [stock for stock in stocks if stock.key in baselines]

        if not scan_stocks:
            logger.error("No stocks have enough history bars.")
            print("No stocks have enough history bars.")
            return 1

        logger.info("Scannable stocks with history baseline: %s", len(scan_stocks))
        print(f"Scannable stocks: {len(scan_stocks)}")

        if args.once:
            if config.scan.market_hours_only and not is_trading_time(runner.now()):
                logger.info("Skipping one-shot scan because current time is outside market hours.")
                print("Outside market hours. Set market_hours_only=false to scan anyway.")
                return 0
            signals = runner.scan_once(scan_stocks, baselines)
            print(f"Signals: {len(signals)}")
            return 0

        runner.run_forever(scan_stocks, baselines)
        return 0
    except KeyboardInterrupt:
        logger.info("Break Watch interrupted by user.")
        print("Stopped.")
        return 0
    except Exception:
        logger.exception("Break Watch failed.")
        print("Break Watch failed. See log for details.")
        return 1
    finally:
        client.close()


def resolve_config_path(config_arg: str | None) -> Path:
    if config_arg:
        return Path(config_arg)

    candidates = [
        Path.cwd() / "config.toml",
        runtime_dir() / "config.toml",
        source_project_root() / "config.toml",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def runtime_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd().resolve()


def source_project_root() -> Path:
    return Path(__file__).resolve().parents[2]
