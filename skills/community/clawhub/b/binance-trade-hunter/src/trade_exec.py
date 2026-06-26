"""
Trade Exec v1.1
One-click trading module for Binance Trade Hunter

Features:
1. Parse natural language buy/sell commands
2. Binance API with Ed25519 signing
3. Market buy/sell execution
"""

from __future__ import annotations

import re
import time
import logging
from dataclasses import dataclass
from typing import Optional

import yaml
import sys
from pathlib import Path

# Use local BinanceClient (no external dependency)
from binance_client import BinanceClient

logger = logging.getLogger("trade-exec")


# ============================================================
# 数据结构
# ============================================================
@dataclass
class TradeResult:
    success: bool
    symbol: str
    side: str
    qty: float
    price: float
    cost: float
    message: str
    raw: dict


# ============================================================
# 交易执行器
# ============================================================
class TradeExecutor:
    def __init__(self, config_path: str):
        cfg = yaml.safe_load(open(config_path, "r", encoding="utf-8"))
        api_key = cfg["binance"]["api_key"]
        private_key_path = cfg["binance"]["private_key_path"]
        self.client = BinanceClient(api_key, private_key_path)
        self._exchange_info = None

    def market_buy(self, symbol: str, usdt_amount: float) -> TradeResult:
        """市价买入"""
        # quoteOrderQty must be string (same as trade_bot.py)
        params = {
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quoteOrderQty": f"{usdt_amount:.2f}",
        }
        logger.info(f"market_buy: {symbol} amount={usdt_amount:.2f}U")
        resp = self.client._request("POST", "/api/v3/order", params=params, signed=True)
        logger.info(f"market_buy resp: {resp}")

        # check API error
        if "code" in resp and resp["code"] < 0:
            return TradeResult(False, symbol, "BUY", 0, 0, 0,
                               f"API error {resp['code']}: {resp.get('msg', '')}", resp)

        # parse fills
        fills = resp.get("fills", [])
        qty = sum(float(f.get("qty", 0)) for f in fills) if fills else 0
        cost = sum(float(f.get("qty", 0)) * float(f.get("price", 0)) for f in fills) if fills else 0
        avg_price = cost / qty if qty > 0 else 0

        success = "orderId" in resp and qty > 0
        msg = f"买入成功: {qty:.6g} {symbol.replace('USDT','')} @ ${avg_price:.4g}" if success else f"买入失败: {resp}"
        return TradeResult(success, symbol, "BUY", qty, avg_price, cost, msg, resp)

    def market_sell(self, symbol: str, qty: float) -> TradeResult:
        """市价卖出"""
        params = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": qty,
        }
        resp = self.client._request("POST", "/api/v3/order", params=params, signed=True)
        
        fills = resp.get("fills", [])
        cost = sum(float(f.get("qty", 0)) * float(f.get("price", 0)) for f in fills) if fills else 0
        avg_price = cost / qty if qty > 0 else 0

        success = "orderId" in resp
        msg = "卖出成功" if success else f"卖出失败: {resp}"
        return TradeResult(success, symbol, "SELL", qty, avg_price, cost, msg, resp)

    def _get_exchange_info(self) -> dict:
        if self._exchange_info is None:
            self._exchange_info = self.client._request("GET", "/api/v3/exchangeInfo", signed=False)
        return self._exchange_info

    def _get_step_size(self, symbol: str) -> float:
        info = self._get_exchange_info()
        for s in info.get("symbols", []):
            if s.get("symbol") == symbol:
                for f in s.get("filters", []):
                    if f.get("filterType") == "LOT_SIZE":
                        return float(f.get("stepSize", 0.0))
        return 0.0

    def _round_qty(self, qty: float, step: float) -> float:
        if step <= 0:
            return qty
        return (qty // step) * step

    def get_balance(self, asset: str = "USDT") -> float:
        return self.client.get_balance(asset)

    def get_price(self, symbol: str) -> float:
        try:
            data = self.client._request("GET", "/api/v3/ticker/price", params={"symbol": symbol}, signed=False)
            return float(data.get("price", 0))
        except Exception:
            return 0.0

    def get_positions(self, symbols: list[str]) -> list[dict]:
        positions = []
        for sym in symbols:
            base = sym.replace("USDT", "")
            qty = self.get_balance(base)
            if qty <= 0:
                continue
            price = self.get_price(sym)
            value = qty * price if price > 0 else 0.0
            positions.append({
                "symbol": sym,
                "base": base,
                "qty": qty,
                "price": price,
                "value": value,
            })
        return positions

    def market_sell_all(self, symbol: str) -> TradeResult:
        base = symbol.replace("USDT", "")
        qty = self.get_balance(base)
        step = self._get_step_size(symbol)
        qty = self._round_qty(qty, step)
        if qty <= 0:
            return TradeResult(False, symbol, "SELL", 0, 0, 0, "无可卖数量", {})
        return self.market_sell(symbol, qty)

    def market_sell_half(self, symbol: str) -> TradeResult:
        base = symbol.replace("USDT", "")
        qty = self.get_balance(base) / 2
        step = self._get_step_size(symbol)
        qty = self._round_qty(qty, step)
        if qty <= 0:
            return TradeResult(False, symbol, "SELL", 0, 0, 0, "无可卖数量", {})
        return self.market_sell(symbol, qty)


# ============================================================
# Skill 接口函数
# ============================================================
_executor: Optional[TradeExecutor] = None


def get_executor(config_path: str) -> TradeExecutor:
    global _executor
    if _executor is None:
        _executor = TradeExecutor(config_path)
    return _executor


def parse_trade_command(text: str) -> Optional[dict]:
    """
    解析自然语言交易指令
    支持：
    - "买 100U 的 BTC"
    - "卖掉 BTC"
    - "卖一半 BTC"
    """
    text = text.strip().upper()

    # 买入指令
    m = re.search(r"买\s*(\d+\.?\d*)U\s*的\s*([A-Z0-9]+)", text)
    if m:
        amount = float(m.group(1))
        base = m.group(2)
        return {"action": "BUY", "symbol": f"{base}USDT", "amount": amount}

    # 卖出全部
    m = re.search(r"卖掉\s*([A-Z0-9]+)", text)
    if m:
        base = m.group(1)
        return {"action": "SELL_ALL", "symbol": f"{base}USDT"}

    # 卖一半
    m = re.search(r"卖一半\s*([A-Z0-9]+)", text)
    if m:
        base = m.group(1)
        return {"action": "SELL_HALF", "symbol": f"{base}USDT"}

    # 查询持仓
    if re.search(r"(我的)?持仓|仓位|查看持仓", text):
        return {"action": "POSITIONS"}

    return None


# ============================================================
# 注意：实际持仓查询需配合仓位管理模块
# 这里只提供基础买卖功能接口
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("TradeExec ready")
