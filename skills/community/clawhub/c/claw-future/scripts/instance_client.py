"""Shared account-instance access layer for CLI, MCP, and Web."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import socket
import time
from pathlib import Path
from typing import Any, Dict, Optional

from accounts import AccountPaths, AccountRegistry
import state


_INSTRUMENT_RE = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9& +.\-]{2,64}$")
_EXCHANGES = {"SHFE", "DCE", "CZCE", "CFFEX", "INE", "GFEX"}
_DIRECTIONS = {"buy", "sell"}
_OFFSETS = {"open", "close", "close_today", "close_yesterday"}
_PRICE_TYPES = {"limit", "market"}


class InstanceClientError(RuntimeError):
    pass


def _canonical_json(value: Dict[str, Any]) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _load_or_create_secret(path: Path) -> bytes:
    try:
        raw = path.read_bytes()
        if len(raw) >= 32:
            return raw
    except FileNotFoundError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    value = secrets.token_bytes(32)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raw = path.read_bytes()
        if len(raw) < 32:
            raise InstanceClientError("管理签名密钥损坏，拒绝生成下单确认")
        return raw
    try:
        os.write(fd, value)
        os.fsync(fd)
    finally:
        os.close(fd)
    return value


class AccountInstanceClient:
    def __init__(
        self,
        registry: Optional[AccountRegistry] = None,
        timeout: float = 10.0,
    ):
        self.registry = registry or AccountRegistry()
        self.timeout = timeout
        self._secrets: Dict[str, bytes] = {}

    def paths(self, account_id: str) -> AccountPaths:
        return self.registry.resolve(account_id)

    def _secret_for(self, account_id: str) -> bytes:
        secret = self._secrets.get(account_id)
        if secret is None:
            paths = self.paths(account_id)
            paths.ensure_layout()
            secret = _load_or_create_secret(paths.root / ".management_secret")
            self._secrets[account_id] = secret
        return secret

    def list_accounts(self) -> Dict[str, Any]:
        rows = []
        for item in self.registry.public_accounts():
            row = dict(item)
            if row["enabled"]:
                paths = self.paths(row["account_id"])
                daemon_state = state.read_path(paths.state_file)
                running = state.is_running_path(paths.state_file)
                row.update({
                    "running": running,
                    "pid": daemon_state.get("pid") if running else None,
                    "port": daemon_state.get("port") if running else paths.daemon_port,
                })
                if running:
                    ping = self.send(row["account_id"], {"cmd": "ping"}, timeout=2.0)
                    row["status"] = ping
            rows.append(row)
        return {"ok": True, "accounts": rows}

    def send(
        self,
        account_id: str,
        command: Dict[str, Any],
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        paths = self.paths(account_id)
        daemon_state = state.read_path(paths.state_file)
        port = daemon_state.get("port") if state.is_running_path(paths.state_file) else None
        if not port:
            return {
                "ok": False,
                "account_id": account_id,
                "error": "账户实例未运行",
            }
        payload = {**command, "account_id": account_id}
        wait = float(timeout if timeout is not None else self.timeout)
        try:
            with socket.create_connection(("127.0.0.1", int(port)), timeout=wait) as conn:
                conn.settimeout(wait)
                conn.sendall(_canonical_json(payload) + b"\n")
                buffer = b""
                while not buffer.endswith(b"\n"):
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    buffer += chunk
            response = json.loads(buffer.decode("utf-8"))
            if not isinstance(response, dict):
                raise ValueError("响应不是对象")
            response.setdefault("account_id", account_id)
            return response
        except Exception as exc:
            return {
                "ok": False,
                "account_id": account_id,
                "error": f"账户实例通信失败: {exc}",
            }

    def status(self, account_id: str) -> Dict[str, Any]:
        return self.send(account_id, {"cmd": "ping"}, timeout=2.0)

    def funds(self, account_id: str) -> Dict[str, Any]:
        return self.send(account_id, {"cmd": "qry_account"})

    def positions(self, account_id: str, instrument: str = "") -> Dict[str, Any]:
        return self.send(account_id, {
            "cmd": "qry_position", "instrument": instrument,
        })

    def orders(self, account_id: str, instrument: str = "") -> Dict[str, Any]:
        return self.send(account_id, {
            "cmd": "qry_orders", "instrument": instrument,
        })

    def trades(self, account_id: str, instrument: str = "") -> Dict[str, Any]:
        return self.send(account_id, {
            "cmd": "qry_trades", "instrument": instrument,
        })

    def quote(self, account_id: str, instrument: str) -> Dict[str, Any]:
        return self.send(account_id, {
            "cmd": "qry_price", "instrument": validate_instrument(instrument),
        }, timeout=2.0)

    def events(
        self, account_id: str, after_seq: int = 0, limit: int = 500
    ) -> Dict[str, Any]:
        return self.send(account_id, {
            "cmd": "poll_events", "after_seq": after_seq, "limit": limit,
        }, timeout=2.0)

    def prepare_order(
        self,
        account_id: str,
        *,
        exchange: str,
        instrument: str,
        direction: str,
        offset: str,
        volume: int,
        price_type: str = "limit",
        price: float = 0.0,
        time_cond: str = "gfd",
        vol_cond: str = "any",
        ttl_seconds: int = 120,
    ) -> Dict[str, Any]:
        order = validate_order({
            "exchange": exchange,
            "instrument": instrument,
            "direction": direction,
            "offset": offset,
            "volume": volume,
            "price_type": price_type,
            "price": price,
            "time_cond": time_cond,
            "vol_cond": vol_cond,
        })
        status = self.status(account_id)
        if not status.get("ok"):
            return status
        if not status.get("settled"):
            return {
                "ok": False,
                "account_id": account_id,
                "error": "账户尚未完成登录和结算确认",
                "status": status,
            }
        payload = {
            "version": 1,
            "account_id": account_id,
            "order": order,
            "expires_at": int(time.time()) + max(30, min(int(ttl_seconds), 300)),
            "nonce": secrets.token_hex(8),
        }
        body = base64.urlsafe_b64encode(_canonical_json(payload)).rstrip(b"=")
        secret = self._secret_for(account_id)
        signature = hmac.new(secret, body, hashlib.sha256).hexdigest().encode("ascii")
        token = body.decode("ascii") + "." + signature.decode("ascii")
        quote = self.quote(account_id, order["instrument"])
        return {
            "ok": True,
            "account_id": account_id,
            "order": order,
            "quote": quote.get("tick") if quote.get("ok") else None,
            "confirmation_token": token,
            "expires_at": payload["expires_at"],
        }

    def submit_prepared_order(
        self, account_id: str, confirmation_token: str, idempotency_key: str
    ) -> Dict[str, Any]:
        if not str(idempotency_key or "").strip():
            return {"ok": False, "account_id": account_id,
                    "error": "写操作必须提供 idempotency_key"}
        try:
            payload = self._verify_token(account_id, confirmation_token)
        except InstanceClientError as exc:
            return {"ok": False, "account_id": account_id, "error": str(exc)}
        if payload.get("account_id") != account_id:
            return {"ok": False, "account_id": account_id,
                    "error": "确认令牌属于另一个账户"}
        command = {
            "cmd": "order",
            **payload["order"],
            "idempotency_key": idempotency_key,
        }
        return self.send(account_id, command)

    def cancel_order(
        self,
        account_id: str,
        *,
        idempotency_key: str,
        exchange: str = "",
        instrument: str = "",
        order_sys_id: str = "",
        order_ref: str = "",
    ) -> Dict[str, Any]:
        if not str(idempotency_key or "").strip():
            return {"ok": False, "account_id": account_id,
                    "error": "写操作必须提供 idempotency_key"}
        if not order_sys_id and not order_ref:
            return {"ok": False, "account_id": account_id,
                    "error": "撤单必须提供 order_sys_id 或 order_ref"}
        return self.send(account_id, {
            "cmd": "cancel",
            "exchange": exchange,
            "instrument": instrument,
            "order_sys_id": order_sys_id,
            "order_ref": order_ref,
            "idempotency_key": idempotency_key,
        })

    def cancel_all(self, account_id: str, idempotency_key: str) -> Dict[str, Any]:
        if not str(idempotency_key or "").strip():
            return {"ok": False, "account_id": account_id,
                    "error": "写操作必须提供 idempotency_key"}
        return self.send(account_id, {
            "cmd": "cancel_all", "idempotency_key": idempotency_key,
        })

    def _verify_token(self, account_id: str, token: str) -> Dict[str, Any]:
        try:
            body_text, supplied_signature = str(token).split(".", 1)
            body = body_text.encode("ascii")
            expected = hmac.new(
                self._secret_for(account_id), body, hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(expected, supplied_signature):
                raise InstanceClientError("下单确认令牌签名无效")
            padding = "=" * (-len(body_text) % 4)
            payload = json.loads(base64.urlsafe_b64decode(body_text + padding))
        except InstanceClientError:
            raise
        except Exception as exc:
            raise InstanceClientError("下单确认令牌格式无效") from exc
        if int(payload.get("expires_at", 0)) < int(time.time()):
            raise InstanceClientError("下单确认令牌已过期，请重新确认")
        if not isinstance(payload.get("order"), dict):
            raise InstanceClientError("下单确认令牌缺少委托参数")
        return payload


def validate_instrument(instrument: str) -> str:
    value = str(instrument or "").strip()
    if not _INSTRUMENT_RE.fullmatch(value):
        raise InstanceClientError("请输入完整合约代码，例如 al2610，不能只填写月份")
    return value


def validate_order(order: Dict[str, Any]) -> Dict[str, Any]:
    exchange = str(order.get("exchange") or "").upper()
    if exchange not in _EXCHANGES:
        raise InstanceClientError(f"不支持的交易所: {exchange}")
    instrument = validate_instrument(str(order.get("instrument") or ""))
    direction = str(order.get("direction") or "")
    offset = str(order.get("offset") or "")
    price_type = str(order.get("price_type") or "limit")
    if direction not in _DIRECTIONS:
        raise InstanceClientError("direction 必须是 buy 或 sell")
    if offset not in _OFFSETS:
        raise InstanceClientError("offset 参数无效")
    if price_type not in _PRICE_TYPES:
        raise InstanceClientError("price_type 必须是 limit 或 market")
    try:
        volume = int(order.get("volume"))
        price = float(order.get("price", 0.0))
    except (TypeError, ValueError) as exc:
        raise InstanceClientError("价格或手数格式无效") from exc
    if not 1 <= volume <= 100000:
        raise InstanceClientError("手数必须在 1 到 100000 之间")
    if price_type == "limit" and price <= 0:
        raise InstanceClientError("限价单价格必须大于 0")
    return {
        "exchange": exchange,
        "instrument": instrument,
        "direction": direction,
        "offset": offset,
        "price_type": price_type,
        "price": 0.0 if price_type == "market" else price,
        "volume": volume,
        "time_cond": str(order.get("time_cond") or "gfd"),
        "vol_cond": str(order.get("vol_cond") or "any"),
    }
