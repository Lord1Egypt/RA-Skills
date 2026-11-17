"""Clearly labelled in-memory data source for UI development only."""

from __future__ import annotations

import base64
import json
import threading
import time
from typing import Any, Dict


class DemoAccountClient:
    def __init__(self):
        self._lock = threading.RLock()
        self._orders = [
            {
                "order_ref": "000000000218", "order_sys_id": "4582190",
                "instrument": "al2610", "exchange": "SHFE",
                "direction": "0", "offset": "0", "limit_price": 20840,
                "volume_total": 3, "volume_traded": 1,
                "order_status": "1", "status_msg": "部分成交",
                "insert_time": "10:14:28", "trading_day": "20260902",
            },
            {
                "order_ref": "000000000217", "order_sys_id": "4582012",
                "instrument": "rb2701", "exchange": "SHFE",
                "direction": "1", "offset": "1", "limit_price": 3268,
                "volume_total": 2, "volume_traded": 2,
                "order_status": "0", "status_msg": "全部成交",
                "insert_time": "09:52:06", "trading_day": "20260902",
            },
        ]
        self._seq = 12
        self._submitted_keys: dict[tuple[str, str], Dict[str, Any]] = {}

    def list_accounts(self) -> Dict[str, Any]:
        return {"ok": True, "accounts": [
            {
                "account_id": name, "display_name": f"账户 {name}",
                "enabled": True, "configured": True, "running": True,
                "port": 17771 + index,
                "status": self.status(name),
            }
            for index, name in enumerate("ABCDE")
        ]}

    def status(self, account_id: str) -> Dict[str, Any]:
        return {
            "ok": True, "account_id": account_id, "trading_day": "20260902",
            "connected": True, "authenticated": True, "logged_in": True,
            "settled": True, "md_connected": True, "md_logged_in": True,
        }

    def funds(self, account_id: str) -> Dict[str, Any]:
        delta = ord(account_id[0]) - ord("A") if account_id else 0
        return {"ok": True, "account_id": account_id, "account": {
            "account_id": f"SIM-{account_id}", "balance": 1268400 + delta * 48200,
            "available": 842650 + delta * 29700, "margin": 319480,
            "frozen_margin": 41720, "commission": 386.4,
            "position_profit": 18360 - delta * 900, "close_profit": 7420,
        }}

    def positions(self, account_id: str, instrument: str = "") -> Dict[str, Any]:
        rows = [
            {"instrument": "al2610", "exchange": "SHFE", "direction": "2",
             "position": 5, "today_position": 2, "yd_position": 3,
             "position_cost": 103500, "use_margin": 124600,
             "position_profit": 9260},
            {"instrument": "rb2701", "exchange": "SHFE", "direction": "3",
             "position": 2, "today_position": 0, "yd_position": 2,
             "position_cost": 65620, "use_margin": 28600,
             "position_profit": -1240},
        ]
        if instrument:
            rows = [row for row in rows if row["instrument"] == instrument]
        return {"ok": True, "account_id": account_id, "positions": rows}

    def orders(self, account_id: str, instrument: str = "") -> Dict[str, Any]:
        with self._lock:
            rows = [dict(row) for row in self._orders]
        if instrument:
            rows = [row for row in rows if row["instrument"] == instrument]
        return {"ok": True, "account_id": account_id, "orders": rows}

    def trades(self, account_id: str, instrument: str = "") -> Dict[str, Any]:
        rows = [
            {"trade_id": "9018821", "order_ref": "000000000218",
             "order_sys_id": "4582190", "instrument": "al2610",
             "exchange": "SHFE", "direction": "0", "offset": "0",
             "price": 20835, "volume": 1, "trade_time": "10:14:29",
             "trading_day": "20260902"},
            {"trade_id": "9017640", "order_ref": "000000000217",
             "order_sys_id": "4582012", "instrument": "rb2701",
             "exchange": "SHFE", "direction": "1", "offset": "1",
             "price": 3266, "volume": 2, "trade_time": "09:52:07",
             "trading_day": "20260902"},
        ]
        if instrument:
            rows = [row for row in rows if row["instrument"] == instrument]
        return {"ok": True, "account_id": account_id, "trades": rows}

    def quote(self, account_id: str, instrument: str) -> Dict[str, Any]:
        prices = {"al2610": 20845.0, "rb2701": 3271.0, "au2612": 812.36}
        last = prices.get(instrument, 1000.0)
        return {"ok": True, "account_id": account_id, "tick": {
            "instrument": instrument, "trading_day": "20260902",
            "update_time": time.strftime("%H:%M:%S"), "update_ms": 260,
            "last": last, "pre_close": last * 0.997, "open": last * 0.998,
            "high": last * 1.008, "low": last * 0.992,
            "upper_limit": last * 1.08, "lower_limit": last * 0.92,
            "bid1": last - 5 if last > 10000 else last - 1,
            "bid1_vol": 18, "ask1": last + 5 if last > 10000 else last + 1,
            "ask1_vol": 11, "vol": 128496, "open_interest": 238910,
        }}

    def events(self, account_id: str, after_seq: int = 0, limit: int = 500) -> Dict[str, Any]:
        self._seq += 1
        quote = self.quote(account_id, "al2610")["tick"]
        event = {"type": "tick", "tick": quote, "seq": self._seq,
                 "account_id": account_id, "emitted_at": time.time()}
        return {"ok": True, "account_id": account_id, "events": [event],
                "next_seq": self._seq, "oldest_seq": 1, "cursor_expired": False}

    def prepare_order(self, account_id: str, **order: Any) -> Dict[str, Any]:
        payload = {"account_id": account_id, "order": order,
                   "expires_at": int(time.time()) + 120}
        token = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(",", ":")).encode()
        ).decode()
        return {"ok": True, "account_id": account_id, "order": order,
                "quote": self.quote(account_id, order["instrument"])["tick"],
                "confirmation_token": token, "expires_at": payload["expires_at"]}

    def submit_prepared_order(self, account_id: str, token: str, key: str) -> Dict[str, Any]:
        try:
            payload = json.loads(base64.urlsafe_b64decode(token.encode()))
        except Exception:
            return {"ok": False, "account_id": account_id, "error": "演示确认令牌无效"}
        if payload.get("account_id") != account_id:
            return {"ok": False, "account_id": account_id, "error": "确认令牌属于另一个账户"}
        if int(payload.get("expires_at", 0)) < int(time.time()):
            return {"ok": False, "account_id": account_id, "error": "演示确认令牌已过期"}
        request_key = (account_id, str(key))
        with self._lock:
            previous = self._submitted_keys.get(request_key)
            if previous is not None:
                return {**previous, "idempotent_replay": True}
            ref = str(219 + len(self._orders)).zfill(12)
            order = payload["order"]
            response = {
                "ok": True, "account_id": account_id, "order_ref": ref,
                "ret": 0, "idempotency_key": f"explicit:{key}", "demo": True,
            }
            self._orders.insert(0, {
                "order_ref": ref, "order_sys_id": "", "instrument": order["instrument"],
                "exchange": order["exchange"],
                "direction": "0" if order["direction"] == "buy" else "1",
                "offset": "0" if order["offset"] == "open" else "1",
                "limit_price": order["price"], "volume_total": order["volume"],
                "volume_traded": 0, "order_status": "3", "status_msg": "未成交",
                "insert_time": time.strftime("%H:%M:%S"), "trading_day": "20260902",
            })
            self._submitted_keys[request_key] = response
        return response

    def cancel_order(self, account_id: str, **request: Any) -> Dict[str, Any]:
        target = request.get("order_ref")
        with self._lock:
            for order in self._orders:
                if order["order_ref"] == target:
                    order.update({"order_status": "5", "status_msg": "已撤单"})
        return {"ok": True, "account_id": account_id, "ret": 0, "demo": True,
                "idempotency_key": f"explicit:{request.get('idempotency_key', '')}"}

    def cancel_all(self, account_id: str, idempotency_key: str) -> Dict[str, Any]:
        count = 0
        with self._lock:
            for order in self._orders:
                if order["order_status"] not in {"0", "5"}:
                    order.update({"order_status": "5", "status_msg": "已撤单"})
                    count += 1
        return {"ok": True, "account_id": account_id, "cancelled": count,
                "failed": 0, "demo": True,
                "idempotency_key": f"explicit:{idempotency_key}"}

    def send(self, account_id: str, command: Dict[str, Any], **_: Any) -> Dict[str, Any]:
        if command.get("cmd") == "subscribe":
            return {"ok": True, "account_id": account_id, "ret": 0,
                    "idempotency_key": "explicit:" + command["idempotency_key"],
                    "demo": True}
        return {"ok": False, "account_id": account_id, "error": "演示命令不支持"}
