"""
Signal Runtime — 策略定时执行调度器

功能:
  1. 按指定间隔运行策略脚本的 generate_signals(mode='live')
  2. 新信号经过风控检查
  3. 通过风控后调用 TradeExecutor 自动下单
  4. 所有操作写入日志 + 状态文件
  5. 支持 Ctrl+C 优雅停止

用法:
  python signal_runtime.py --strategy strategies/sol_kdj_swing.py --interval 14400

  interval 单位为秒（4h = 14400）
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import signal as _signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

from risk_checker import RiskChecker
from trade_executor import TradeExecutor


logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}",
    level="INFO",
)
LOG_DIR = Path.home() / ".dex-quant" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    str(LOG_DIR / "runtime_{time:YYYY-MM-DD}.log"),
    rotation="1 day", retention="7 days", level="DEBUG",
)


_running = True


def _stop(signum, frame):
    global _running
    logger.info("received stop signal, shutting down...")
    _running = False


_signal.signal(_signal.SIGINT, _stop)
_signal.signal(_signal.SIGTERM, _stop)


def load_strategy(path: str):
    """动态加载策略模块。"""
    spec = importlib.util.spec_from_file_location("strategy", path)
    if not spec or not spec.loader:
        raise ImportError(f"cannot load strategy: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "generate_signals"):
        raise AttributeError(f"strategy missing generate_signals(): {path}")
    return module


def extract_actionable_signals(signals: list[dict], min_confidence: float = 0.6) -> list[dict]:
    """过滤出可执行的信号（buy/sell，confidence 足够）。"""
    actionable = []
    for s in signals:
        action = s.get("action", "").lower()
        if action not in ("buy", "sell"):
            continue
        if s.get("confidence", 0) < min_confidence:
            continue
        actionable.append(s)
    return actionable


def map_signal_to_trade(signal: dict, position_size: float) -> dict:
    """将策略信号映射为交易指令。"""
    symbol = signal.get("symbol", "BTCUSDT")
    coin = symbol.replace("USDT", "").replace("PERP", "")
    action = signal["action"].lower()
    direction = signal.get("direction", "long").lower()

    if action == "buy" and direction == "long":
        return {"type": "market_buy", "coin": coin, "size": position_size}
    elif action == "sell" and direction == "long":
        return {"type": "market_sell", "coin": coin, "size": position_size}
    elif action == "sell" and direction == "short":
        return {"type": "market_sell", "coin": coin, "size": position_size}
    elif action == "buy" and direction == "short":
        return {"type": "market_buy", "coin": coin, "size": position_size}
    return {"type": "unknown"}


def execute_trade(executor: TradeExecutor, trade: dict) -> dict:
    """执行单笔交易。"""
    if trade["type"] == "market_buy":
        return executor.market_buy(trade["coin"], trade["size"])
    elif trade["type"] == "market_sell":
        return executor.market_sell(trade["coin"], trade["size"])
    else:
        return {"error": f"unknown trade type: {trade['type']}"}


def save_state(state_file: Path, state: dict):
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2, default=str))


def run_loop(
    strategy_path: str,
    interval: int = 14400,
    claw_dir: str | None = None,
    risk_rules: dict | None = None,
    dry_run: bool = False,
):
    """主循环：定时执行策略 → 风控 → 下单。"""

    strategy = load_strategy(strategy_path)
    strategy_name = getattr(strategy, "PARAMS", {}).get("strategy_name", Path(strategy_path).stem)

    executor = None
    if not dry_run:
        try:
            executor = TradeExecutor(claw_dir)
        except FileNotFoundError as e:
            logger.error("TradeExecutor init failed: {}", e)
            logger.info("switching to dry_run mode")
            dry_run = True

    risk = RiskChecker(rules=risk_rules)
    state_file = Path.home() / ".dex-quant" / "runtime_state.json"

    logger.info("=" * 60)
    logger.info("Signal Runtime Started")
    logger.info("  Strategy: {}", strategy_path)
    logger.info("  Interval: {}s ({}h)", interval, interval / 3600)
    logger.info("  Dry run: {}", dry_run)
    logger.info("  Risk rules: {}", risk.rules)
    logger.info("=" * 60)

    cycle = 0
    while _running:
        cycle += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("── Cycle {} | {} ──", cycle, now)

        try:
            result = strategy.generate_signals(mode="live")
            signals = result.get("signals", [])
            logger.info("strategy returned {} signals", len(signals))
        except Exception as e:
            logger.error("strategy execution failed: {}", e)
            _wait(interval)
            continue

        actionable = extract_actionable_signals(signals, risk.rules.get("min_confidence", 0.6))
        if not actionable:
            logger.info("no actionable signals, sleeping...")
            _wait(interval)
            continue

        logger.info("{} actionable signals found", len(actionable))

        equity = 0.0
        open_positions = 0
        if executor and not dry_run:
            try:
                equity = executor.get_equity()
                pos_data = executor.get_positions()
                open_positions = len(pos_data.get("positions", []))
            except Exception as e:
                logger.error("failed to get account state: {}", e)
                _wait(interval)
                continue

        for sig in actionable:
            logger.info("signal: {} {} {} @ {:.2f} | confidence={:.2f} | {}",
                        sig["action"], sig.get("direction", ""), sig.get("symbol", ""),
                        sig.get("price_at_signal", 0), sig.get("confidence", 0),
                        sig.get("reason", ""))

            passed, reason = risk.check(sig, equity, open_positions)
            if not passed:
                logger.warning("BLOCKED by risk: {}", reason)
                continue

            price = sig.get("price_at_signal", 0)
            position_size = risk.calculate_position_size(equity, price) if equity > 0 else 0

            trade = map_signal_to_trade(sig, position_size)
            logger.info("trade: {} {} {:.6f}", trade["type"], trade.get("coin", ""), trade.get("size", 0))

            if dry_run:
                logger.info("[DRY RUN] would execute: {}", trade)
                risk.record_trade(sig, {"status": "dry_run"})
            else:
                try:
                    result = execute_trade(executor, trade)
                    if "error" in result:
                        logger.error("trade failed: {}", result["error"])
                        risk.record_trade(sig, result)
                    else:
                        logger.info("trade executed: {}", result)
                        risk.record_trade(sig, result)
                        open_positions += 1
                except Exception as e:
                    logger.error("trade execution error: {}", e)
                    risk.record_trade(sig, {"error": str(e)})

        state = {
            "cycle": cycle,
            "last_run": now,
            "strategy": strategy_path,
            "signals_count": len(signals),
            "actionable_count": len(actionable),
            "risk_summary": risk.summary(),
        }
        save_state(state_file, state)

        _wait(interval)

    logger.info("Signal Runtime stopped.")


def _wait(seconds: int):
    """可中断的等待。"""
    end = time.time() + seconds
    while _running and time.time() < end:
        time.sleep(min(5, end - time.time()))


def main():
    parser = argparse.ArgumentParser(description="Signal Runtime — 策略定时执行")
    parser.add_argument("--strategy", required=True, help="策略脚本路径")
    parser.add_argument("--interval", type=int, default=14400, help="执行间隔（秒），默认 4h=14400")
    parser.add_argument("--claw-dir", default=None, help="HyperLiquid-Claw 安装目录")
    parser.add_argument("--dry-run", action="store_true", help="模拟模式，不实际下单")
    parser.add_argument("--max-position-pct", type=float, default=10.0, help="单笔最大仓位占比")
    parser.add_argument("--max-concurrent", type=int, default=3, help="最大同时持仓数")
    parser.add_argument("--cooldown", type=int, default=30, help="交易冷却时间（分钟）")
    args = parser.parse_args()

    risk_rules = {
        "max_position_pct": args.max_position_pct,
        "max_concurrent": args.max_concurrent,
        "cooldown_minutes": args.cooldown,
    }

    run_loop(
        strategy_path=args.strategy,
        interval=args.interval,
        claw_dir=args.claw_dir,
        risk_rules=risk_rules,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
