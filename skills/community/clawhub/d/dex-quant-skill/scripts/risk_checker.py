"""
Risk Checker — 交易前风控检查

规则:
  1. 单笔仓位不超过总权益的 max_position_pct
  2. 同时最多 max_concurrent 个仓位
  3. 连续亏损 max_consecutive_losses 次后暂停
  4. 两次交易之间至少间隔 cooldown_minutes 分钟
  5. 信号置信度必须 >= min_confidence
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from loguru import logger


class RiskChecker:
    """交易前风控检查器。"""

    DEFAULT_RULES = {
        "max_position_pct": 10.0,
        "max_concurrent": 3,
        "max_consecutive_losses": 3,
        "cooldown_minutes": 30,
        "min_confidence": 0.6,
        "max_leverage": 10,
    }

    def __init__(self, rules: dict | None = None, state_file: str | None = None):
        self.rules = {**self.DEFAULT_RULES, **(rules or {})}
        self._state_file = Path(state_file or Path.home() / ".dex-quant" / "risk_state.json")
        self._state = self._load_state()

    def _load_state(self) -> dict:
        if self._state_file.exists():
            try:
                return json.loads(self._state_file.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        return {"consecutive_losses": 0, "last_trade_ts": 0, "trade_log": []}

    def _save_state(self):
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(json.dumps(self._state, indent=2))

    def check(self, signal: dict, equity: float, open_positions: int) -> tuple[bool, str]:
        """
        检查信号是否通过风控。

        返回 (passed, reason)。
        """
        confidence = signal.get("confidence", 0)
        if confidence < self.rules["min_confidence"]:
            return False, f"confidence {confidence:.2f} < {self.rules['min_confidence']}"

        if open_positions >= self.rules["max_concurrent"]:
            return False, f"already {open_positions} positions (max {self.rules['max_concurrent']})"

        if self._state["consecutive_losses"] >= self.rules["max_consecutive_losses"]:
            return False, f"consecutive losses {self._state['consecutive_losses']} >= {self.rules['max_consecutive_losses']}"

        elapsed = time.time() - self._state.get("last_trade_ts", 0)
        cooldown_sec = self.rules["cooldown_minutes"] * 60
        if elapsed < cooldown_sec:
            remaining = int(cooldown_sec - elapsed)
            return False, f"cooldown: {remaining}s remaining"

        return True, "passed"

    def calculate_position_size(self, equity: float, price: float) -> float:
        """根据权益和风控规则计算仓位大小（币数量）。"""
        max_usd = equity * (self.rules["max_position_pct"] / 100.0)
        if price <= 0:
            return 0.0
        return max_usd / price

    def record_trade(self, signal: dict, result: dict):
        """记录交易结果，更新连续亏损计数。"""
        is_loss = result.get("pnl", 0) < 0 or result.get("error")

        if is_loss:
            self._state["consecutive_losses"] += 1
        else:
            self._state["consecutive_losses"] = 0

        self._state["last_trade_ts"] = time.time()
        self._state["trade_log"].append({
            "ts": time.time(),
            "signal": {
                "symbol": signal.get("symbol"),
                "action": signal.get("action"),
                "direction": signal.get("direction"),
                "price": signal.get("price_at_signal"),
            },
            "is_loss": is_loss,
        })

        if len(self._state["trade_log"]) > 100:
            self._state["trade_log"] = self._state["trade_log"][-100:]

        self._save_state()

    def reset_losses(self):
        """重置连续亏损计数。"""
        self._state["consecutive_losses"] = 0
        self._save_state()
        logger.info("risk: consecutive losses reset to 0")

    def summary(self) -> dict:
        return {
            "rules": self.rules,
            "consecutive_losses": self._state["consecutive_losses"],
            "last_trade_ts": self._state.get("last_trade_ts", 0),
            "total_trades": len(self._state.get("trade_log", [])),
        }
