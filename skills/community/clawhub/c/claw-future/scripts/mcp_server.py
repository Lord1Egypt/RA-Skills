"""MCP server exposing one-account-at-a-time ClawTrader tools."""

from __future__ import annotations

import argparse
import hmac
import os
from pathlib import Path
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from accounts import AccountRegistry
from instance_client import AccountInstanceClient


class _BearerMiddleware:
    """Protect the MCP HTTP route without changing stdio transport."""

    def __init__(self, app: Any, token: str):
        self.app = app
        self.token = token.encode("utf-8")

    async def __call__(self, scope: Dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") == "http" and scope.get("path") == "/mcp":
            headers = {key.lower(): value for key, value in scope.get("headers", [])}
            supplied = headers.get(b"authorization", b"")
            expected = b"Bearer " + self.token
            if not hmac.compare_digest(supplied, expected):
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [(b"content-type", b"application/json"),
                                (b"www-authenticate", b"Bearer")],
                })
                await send({
                    "type": "http.response.body",
                    "body": '{"error":"需要有效的 Bearer 令牌"}'.encode("utf-8"),
                })
                return
        await self.app(scope, receive, send)


def build_server(
    registry_file: str = "",
    *,
    host: str = "127.0.0.1",
    port: int = 17880,
) -> FastMCP:
    registry = AccountRegistry(Path(registry_file) if registry_file else None)
    client = AccountInstanceClient(registry)
    server = FastMCP(
        "ClawTrader",
        instructions=(
            "中国期货账户交易工具。每次调用只允许指定一个 account_id；"
            "多账户调度由调用 Agent 自行完成。下单先 prepare_order，再 place_order。"
        ),
        host=host,
        port=port,
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
    )

    @server.tool()
    def list_accounts() -> Dict[str, Any]:
        """列出可用账户及各自 daemon、登录和结算状态，不返回凭证。"""
        return client.list_accounts()

    @server.tool()
    def get_account_status(account_id: str) -> Dict[str, Any]:
        """查询一个账户实例的连接、认证、登录、结算和交易日状态。"""
        return client.status(account_id)

    @server.tool()
    def get_account_funds(account_id: str) -> Dict[str, Any]:
        """实时向 CTP 查询一个账户的资金、保证金和盈亏。"""
        return client.funds(account_id)

    @server.tool()
    def get_positions(account_id: str, instrument: str = "") -> Dict[str, Any]:
        """实时查询一个账户的全部持仓；instrument 可指定完整合约代码。"""
        return client.positions(account_id, instrument)

    @server.tool()
    def get_orders(account_id: str, instrument: str = "") -> Dict[str, Any]:
        """实时查询一个账户当日全部委托及状态。"""
        return client.orders(account_id, instrument)

    @server.tool()
    def get_trades(account_id: str, instrument: str = "") -> Dict[str, Any]:
        """实时查询一个账户当日成交记录。"""
        return client.trades(account_id, instrument)

    @server.tool()
    def get_quote(account_id: str, instrument: str) -> Dict[str, Any]:
        """读取一个账户实例中完整合约代码的最新行情快照。"""
        return client.quote(account_id, instrument)

    @server.tool()
    def subscribe_quote(
        account_id: str,
        instruments: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        """订阅逗号分隔的完整合约代码；写操作必须提供幂等键。"""
        if not idempotency_key.strip():
            return {"ok": False, "account_id": account_id,
                    "error": "写操作必须提供 idempotency_key"}
        return client.send(account_id, {
            "cmd": "subscribe",
            "instruments": instruments,
            "idempotency_key": idempotency_key,
        })

    @server.tool()
    def prepare_order(
        account_id: str,
        exchange: str,
        instrument: str,
        direction: str,
        offset: str,
        volume: int,
        price_type: str = "limit",
        price: float = 0.0,
        time_cond: str = "gfd",
        vol_cond: str = "any",
    ) -> Dict[str, Any]:
        """校验单账户委托并返回两分钟有效的确认令牌，不产生下单副作用。"""
        try:
            return client.prepare_order(
                account_id,
                exchange=exchange,
                instrument=instrument,
                direction=direction,
                offset=offset,
                volume=volume,
                price_type=price_type,
                price=price,
                time_cond=time_cond,
                vol_cond=vol_cond,
            )
        except Exception as exc:
            return {"ok": False, "account_id": account_id, "error": str(exc)}

    @server.tool()
    def place_order(
        account_id: str,
        confirmation_token: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        """提交 prepare_order 返回的确认令牌；只操作一个账户且幂等键必填。"""
        return client.submit_prepared_order(
            account_id, confirmation_token, idempotency_key
        )

    @server.tool()
    def cancel_order(
        account_id: str,
        idempotency_key: str,
        exchange: str = "",
        instrument: str = "",
        order_sys_id: str = "",
        order_ref: str = "",
    ) -> Dict[str, Any]:
        """撤销一个账户的一笔委托，优先使用 order_sys_id；幂等键必填。"""
        return client.cancel_order(
            account_id,
            idempotency_key=idempotency_key,
            exchange=exchange,
            instrument=instrument,
            order_sys_id=order_sys_id,
            order_ref=order_ref,
        )

    @server.tool()
    def cancel_all_orders(
        account_id: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        """撤销一个账户全部未成交委托，不影响其他账户；幂等键必填。"""
        return client.cancel_all(account_id, idempotency_key)

    return server


def main() -> None:
    parser = argparse.ArgumentParser(description="ClawTrader MCP server")
    parser.add_argument("--registry", default="")
    parser.add_argument(
        "--transport", choices=["stdio", "streamable-http"], default="stdio"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=17880)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not os.environ.get("CLAW_MCP_TOKEN"):
        raise SystemExit("非本机监听必须设置 CLAW_MCP_TOKEN，并在反向代理层校验")
    server = build_server(args.registry, host=args.host, port=args.port)
    token = os.environ.get("CLAW_MCP_TOKEN", "").strip()
    if args.transport == "streamable-http" and token:
        import uvicorn
        uvicorn.run(
            _BearerMiddleware(server.streamable_http_app(), token),
            host=args.host,
            port=args.port,
        )
        return
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
