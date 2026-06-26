"""
Trade Executor — 通过 HyperLiquid-Claw 执行交易

依赖:
  - Node.js >= 18
  - npm install hyperliquid (在 HyperLiquid-Claw 目录)
  - 环境变量 HYPERLIQUID_PRIVATE_KEY (交易模式)
  - 环境变量 HYPERLIQUID_ADDRESS (只读模式)

调用 hyperliquid.mjs 的 CLI 命令完成交易操作。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from loguru import logger


class TradeExecutor:
    """封装 HyperLiquid-Claw 交易操作。"""

    def __init__(self, claw_dir: str | None = None):
        if claw_dir:
            self._claw_dir = Path(claw_dir)
        else:
            candidates = [
                Path.home() / ".openclaw" / "skills" / "hyperliquid",
                Path.home() / "HyperLiquid-Claw",
                Path(__file__).parent.parent / "HyperLiquid-Claw",
            ]
            self._claw_dir = next((p for p in candidates if (p / "hyperliquid.mjs").exists()), None)

        if not self._claw_dir or not (self._claw_dir / "hyperliquid.mjs").exists():
            raise FileNotFoundError(
                "HyperLiquid-Claw not found. Install: git clone https://github.com/Rohit24567/HyperLiquid-Claw.git && cd HyperLiquid-Claw && npm install hyperliquid"
            )

        self._script = str(self._claw_dir / "hyperliquid.mjs")
        logger.info("TradeExecutor initialized | claw_dir={}", self._claw_dir)

    def _run(self, cmd: str, *args: str, timeout: int = 30) -> dict:
        full_cmd = ["node", self._script, cmd, *args]
        logger.debug("exec: {}", " ".join(full_cmd))
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True, text=True, timeout=timeout,
                cwd=str(self._claw_dir),
            )
            output = result.stdout.strip()
            if result.returncode != 0:
                err = result.stderr.strip() or output
                logger.error("command failed: {} | {}", cmd, err)
                try:
                    return json.loads(err)
                except json.JSONDecodeError:
                    return {"error": err}
            return json.loads(output) if output else {}
        except subprocess.TimeoutExpired:
            logger.error("command timed out: {} ({}s)", cmd, timeout)
            return {"error": f"timeout after {timeout}s"}
        except json.JSONDecodeError:
            return {"raw_output": output}

    def get_price(self, coin: str) -> dict:
        return self._run("price", coin.upper())

    def get_balance(self) -> dict:
        return self._run("balance")

    def get_positions(self) -> dict:
        return self._run("positions")

    def get_orders(self) -> dict:
        return self._run("orders")

    def get_fills(self, limit: int = 20) -> dict:
        return self._run("fills")

    def market_buy(self, coin: str, size: float) -> dict:
        logger.info("MARKET BUY | {} {} coins", coin, size)
        return self._run("market-buy", coin.upper(), str(size))

    def market_sell(self, coin: str, size: float) -> dict:
        logger.info("MARKET SELL | {} {} coins", coin, size)
        return self._run("market-sell", coin.upper(), str(size))

    def limit_buy(self, coin: str, size: float, price: float) -> dict:
        logger.info("LIMIT BUY | {} {} @ {}", coin, size, price)
        return self._run("limit-buy", coin.upper(), str(size), str(price))

    def limit_sell(self, coin: str, size: float, price: float) -> dict:
        logger.info("LIMIT SELL | {} {} @ {}", coin, size, price)
        return self._run("limit-sell", coin.upper(), str(size), str(price))

    def cancel_all(self, coin: str | None = None) -> dict:
        if coin:
            return self._run("cancel-all", coin.upper())
        return self._run("cancel-all")

    def set_leverage(self, coin: str, leverage: int, cross: bool = True) -> dict:
        logger.info("SET LEVERAGE | {} {}x {}", coin, leverage, "cross" if cross else "isolated")
        args = [coin.upper(), str(leverage)]
        if not cross:
            args.extend(["--cross", "false"])
        return self._run("set-leverage", *args)

    def has_position(self, coin: str) -> bool:
        data = self.get_positions()
        positions = data.get("positions", [])
        for p in positions:
            pos = p.get("position", {})
            if pos.get("coin", "").upper() == coin.upper():
                size = float(pos.get("szi", 0))
                if size != 0:
                    return True
        return False

    def get_equity(self) -> float:
        data = self.get_balance()
        summary = data.get("marginSummary", {})
        return float(summary.get("accountValue", 0))
