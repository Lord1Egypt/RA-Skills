#!/usr/bin/env python3
"""FinXData A 股与港股模拟交易 Trading Key 客户端和命令行工具。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

DEFAULT_BASE_URL = "https://api.finxdata.ai"
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_USER_AGENT = "FinXData-SimTrading-Agent/1.1"


class FinXDataClientError(RuntimeError):
    """Base client error safe to render as JSON."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "CLIENT_ERROR",
        status_code: int | None = None,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.status_code is not None:
            payload["status_code"] = self.status_code
        if self.details is not None:
            payload["details"] = self.details
        return payload


class FinXDataSimTradingClient:
    """Small standard-library client for `/api/sim-trading/v1`."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        trading_key: str | None = None,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        self.base_url = (
            base_url
            or os.environ.get("FINXDATA_BASE_URL")
            or os.environ.get("FINDATA_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        self.trading_key = (
            trading_key
            or os.environ.get("FINXDATA_TRADING_KEY")
            or os.environ.get("FINDATA_TRADING_KEY")
        )
        self.timeout = timeout
        self._open = opener or urllib.request.urlopen

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        if not self.trading_key:
            raise FinXDataClientError(
                "缺少模拟交易 Key，请设置 FINXDATA_TRADING_KEY",
                code="MISSING_TRADING_KEY",
            )
        params = {
            key: _query_value(value)
            for key, value in (query or {}).items()
            if value is not None
        }
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        data = None
        headers = {
            "Accept": "application/json",
            "User-Agent": DEFAULT_USER_AGENT,
            "X-FINXDATA-TRADING-KEY": self.trading_key,
        }
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            response = self._open(request, timeout=self.timeout)
            with response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            payload = _decode_json(raw)
            raise FinXDataClientError(
                _error_message(payload, exc.reason),
                code=_error_code(payload, exc.code),
                status_code=exc.code,
                details=payload.get("details") if isinstance(payload, dict) else None,
            ) from None
        except urllib.error.URLError as exc:
            raise FinXDataClientError(
                f"无法连接 FinXData：{exc.reason}", code="CONNECTION_ERROR"
            ) from None
        if not raw:
            return None
        payload = _decode_json(raw)
        if payload is None:
            raise FinXDataClientError(
                "FinXData 返回了非 JSON 响应", code="INVALID_RESPONSE"
            )
        return payload

    def list_watchlist(self) -> dict[str, Any]:
        return self._request("GET", "/api/sim-trading/v1/watchlist")

    def add_watchlist(
        self, stock_code: str, *, note: str | None = None, sort_order: int = 0
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            "/api/sim-trading/v1/watchlist",
            body={"stock_code": stock_code, "note": note, "sort_order": sort_order},
        )

    def remove_watchlist(self, stock_code: str) -> dict[str, Any]:
        code = _path_segment(stock_code)
        return self._request("DELETE", f"/api/sim-trading/v1/watchlist/{code}")

    def list_accounts(
        self,
        *,
        status: str = "active",
        market: str | None = None,
        cursor: int | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/api/sim-trading/v1/accounts",
            query={
                "status": status,
                "market": market,
                "cursor": cursor,
                "limit": limit,
            },
        )

    def create_account(
        self,
        *,
        name: str,
        initial_cash: str,
        market: str = "CN",
        trading_rule_mode: str = "relaxed",
        settlement_mode: str | None = None,
    ) -> dict[str, Any]:
        body = {
            "name": name,
            "initial_cash": initial_cash,
            "market": market,
            "trading_rule_mode": trading_rule_mode,
        }
        if settlement_mode is not None:
            body["settlement_mode"] = settlement_mode
        return self._request(
            "POST",
            "/api/sim-trading/v1/accounts",
            body=body,
        )

    def get_account(self, account_id: int) -> dict[str, Any]:
        return self._request("GET", f"/api/sim-trading/v1/accounts/{account_id}")

    def reset_account(self, account_id: int, *, confirmation: str) -> dict[str, Any]:
        if confirmation != "RESET":
            raise FinXDataClientError(
                "重置账户必须显式传入 confirmation='RESET'",
                code="RESET_CONFIRMATION_REQUIRED",
            )
        return self._request(
            "POST",
            f"/api/sim-trading/v1/accounts/{account_id}/reset",
            body={"confirmation": confirmation},
        )

    def place_order(
        self,
        *,
        account_id: int,
        stock_code: str,
        side: str,
        order_type: str,
        quantity: int,
        client_order_id: str,
        limit_price: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "client_order_id": client_order_id,
            "stock_code": stock_code,
            "side": side,
            "order_type": order_type,
            "quantity": quantity,
        }
        if limit_price is not None:
            body["limit_price"] = limit_price
        return self._request(
            "POST",
            f"/api/sim-trading/v1/accounts/{account_id}/orders",
            body=body,
        )

    def list_orders(
        self,
        account_id: int,
        *,
        status: str | None = None,
        side: str | None = None,
        stock_code: str | None = None,
        started_at: str | None = None,
        ended_at: str | None = None,
        cursor: int | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/api/sim-trading/v1/accounts/{account_id}/orders",
            query={
                "status": status,
                "side": side,
                "stock_code": stock_code,
                "started_at": started_at,
                "ended_at": ended_at,
                "cursor": cursor,
                "limit": limit,
            },
        )

    def get_order(self, account_id: int, order_id: int) -> dict[str, Any]:
        return self._request(
            "GET", f"/api/sim-trading/v1/accounts/{account_id}/orders/{order_id}"
        )

    def cancel_order(self, account_id: int, order_id: int) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/api/sim-trading/v1/accounts/{account_id}/orders/{order_id}/cancel",
        )

    def list_positions(self, account_id: int) -> dict[str, Any]:
        return self._request(
            "GET", f"/api/sim-trading/v1/accounts/{account_id}/positions"
        )

    def get_position(self, account_id: int, stock_code: str) -> dict[str, Any]:
        code = _path_segment(stock_code)
        return self._request(
            "GET", f"/api/sim-trading/v1/accounts/{account_id}/positions/{code}"
        )

    def list_trades(
        self, account_id: int, *, cursor: int | None = None, limit: int = 50
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/api/sim-trading/v1/accounts/{account_id}/trades",
            query={"cursor": cursor, "limit": limit},
        )

    def list_cash_ledgers(
        self, account_id: int, *, cursor: int | None = None, limit: int = 50
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/api/sim-trading/v1/accounts/{account_id}/cash-ledgers",
            query={"cursor": cursor, "limit": limit},
        )

    def get_assets(self, account_id: int) -> dict[str, Any]:
        return self._request("GET", f"/api/sim-trading/v1/accounts/{account_id}/assets")

    def get_performance(
        self, account_id: int, *, period: str = "1m", interval: str = "day"
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/api/sim-trading/v1/accounts/{account_id}/performance",
            query={"period": period, "interval": interval},
        )


def _path_segment(value: str) -> str:
    return urllib.parse.quote(value.strip().upper(), safe="")


def _query_value(value: Any) -> str | int:
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


def _decode_json(raw: bytes) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _error_message(payload: Any, fallback: Any) -> str:
    if isinstance(payload, dict) and payload.get("message"):
        return str(payload["message"])
    return str(fallback or "FinXData 请求失败")


def _error_code(payload: Any, status_code: int) -> str:
    if isinstance(payload, dict) and payload.get("code") is not None:
        return str(payload["code"])
    return f"HTTP_{status_code}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    groups = parser.add_subparsers(dest="group", required=True)

    watchlist = groups.add_parser("watchlist").add_subparsers(
        dest="action", required=True
    )
    watchlist.add_parser("list")
    add = watchlist.add_parser("add")
    add.add_argument("--code", required=True)
    add.add_argument("--note")
    add.add_argument("--sort-order", type=int, default=0)
    remove = watchlist.add_parser("remove")
    remove.add_argument("--code", required=True)

    accounts = groups.add_parser("accounts").add_subparsers(
        dest="action", required=True
    )
    account_list = accounts.add_parser("list")
    account_list.add_argument(
        "--status",
        choices=["active", "archived", "disabled", "all"],
        default="active",
    )
    account_list.add_argument("--market", choices=["CN", "HK"])
    _add_page_args(account_list)
    create = accounts.add_parser("create")
    create.add_argument("--name", default="我的模拟账户")
    create.add_argument("--initial-cash", required=True)
    create.add_argument("--market", choices=["CN", "HK"], default="CN")
    create.add_argument("--trading-rule-mode", default="relaxed")
    create.add_argument("--settlement-mode", choices=["t_plus_1", "t_plus_0"])
    account_get = accounts.add_parser("get")
    account_get.add_argument("--account-id", type=int, required=True)
    reset = accounts.add_parser("reset")
    reset.add_argument("--account-id", type=int, required=True)
    reset.add_argument("--confirm", choices=["RESET"], required=True)

    orders = groups.add_parser("orders").add_subparsers(dest="action", required=True)
    place = orders.add_parser("place")
    _add_account_arg(place)
    place.add_argument("--client-order-id", required=True)
    place.add_argument("--code", required=True)
    place.add_argument("--side", choices=["buy", "sell"], required=True)
    place.add_argument("--order-type", choices=["market", "limit"], required=True)
    place.add_argument("--quantity", type=int, required=True)
    place.add_argument("--limit-price")
    order_list = orders.add_parser("list")
    _add_account_arg(order_list)
    order_list.add_argument("--status")
    order_list.add_argument("--side", choices=["buy", "sell"])
    order_list.add_argument("--code")
    order_list.add_argument("--started-at")
    order_list.add_argument("--ended-at")
    _add_page_args(order_list)
    order_get = orders.add_parser("get")
    _add_account_arg(order_get)
    order_get.add_argument("--order-id", type=int, required=True)
    cancel = orders.add_parser("cancel")
    _add_account_arg(cancel)
    cancel.add_argument("--order-id", type=int, required=True)

    positions = groups.add_parser("positions").add_subparsers(
        dest="action", required=True
    )
    position_list = positions.add_parser("list")
    _add_account_arg(position_list)
    position_get = positions.add_parser("get")
    _add_account_arg(position_get)
    position_get.add_argument("--code", required=True)

    for group_name in ("trades", "ledgers"):
        actions = groups.add_parser(group_name).add_subparsers(
            dest="action", required=True
        )
        item_list = actions.add_parser("list")
        _add_account_arg(item_list)
        _add_page_args(item_list)

    assets = groups.add_parser("assets").add_subparsers(dest="action", required=True)
    asset_get = assets.add_parser("get")
    _add_account_arg(asset_get)

    performance = groups.add_parser("performance").add_subparsers(
        dest="action", required=True
    )
    performance_get = performance.add_parser("get")
    _add_account_arg(performance_get)
    performance_get.add_argument(
        "--period", choices=["1m", "3m", "6m", "1y", "all"], default="1m"
    )
    performance_get.add_argument("--interval", choices=["day"], default="day")
    return parser


def _add_account_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--account-id", type=int, required=True)


def _add_page_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--cursor", type=int)
    parser.add_argument("--limit", type=int, default=50)


def execute(client: FinXDataSimTradingClient, args: argparse.Namespace) -> Any:
    key = (args.group, args.action)
    if key == ("watchlist", "list"):
        return client.list_watchlist()
    if key == ("watchlist", "add"):
        return client.add_watchlist(
            args.code, note=args.note, sort_order=args.sort_order
        )
    if key == ("watchlist", "remove"):
        return client.remove_watchlist(args.code)
    if key == ("accounts", "list"):
        return client.list_accounts(
            status=args.status,
            market=args.market,
            cursor=args.cursor,
            limit=args.limit,
        )
    if key == ("accounts", "create"):
        return client.create_account(
            name=args.name,
            initial_cash=args.initial_cash,
            market=args.market,
            trading_rule_mode=args.trading_rule_mode,
            settlement_mode=args.settlement_mode,
        )
    if key == ("accounts", "get"):
        return client.get_account(args.account_id)
    if key == ("accounts", "reset"):
        return client.reset_account(args.account_id, confirmation=args.confirm)
    if key == ("orders", "place"):
        return client.place_order(
            account_id=args.account_id,
            client_order_id=args.client_order_id,
            stock_code=args.code,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            limit_price=args.limit_price,
        )
    if key == ("orders", "list"):
        return client.list_orders(
            args.account_id,
            status=args.status,
            side=args.side,
            stock_code=args.code,
            started_at=args.started_at,
            ended_at=args.ended_at,
            cursor=args.cursor,
            limit=args.limit,
        )
    if key == ("orders", "get"):
        return client.get_order(args.account_id, args.order_id)
    if key == ("orders", "cancel"):
        return client.cancel_order(args.account_id, args.order_id)
    if key == ("positions", "list"):
        return client.list_positions(args.account_id)
    if key == ("positions", "get"):
        return client.get_position(args.account_id, args.code)
    if key == ("trades", "list"):
        return client.list_trades(args.account_id, cursor=args.cursor, limit=args.limit)
    if key == ("ledgers", "list"):
        return client.list_cash_ledgers(
            args.account_id, cursor=args.cursor, limit=args.limit
        )
    if key == ("assets", "get"):
        return client.get_assets(args.account_id)
    if key == ("performance", "get"):
        return client.get_performance(
            args.account_id, period=args.period, interval=args.interval
        )
    raise FinXDataClientError("不支持的命令", code="UNSUPPORTED_COMMAND")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    client = FinXDataSimTradingClient(
        base_url=args.base_url,
        timeout=args.timeout,
    )
    try:
        result = execute(client, args)
    except FinXDataClientError as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
