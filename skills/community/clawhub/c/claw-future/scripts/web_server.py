"""Authenticated Web API and live event bridge for ClawTrader."""

from __future__ import annotations

import argparse
import asyncio
import os
import secrets
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, WebSocket
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from accounts import AccountRegistry, AccountRegistryError, PROJECT_ROOT
from audit import AuditLog
from demo_client import DemoAccountClient
from instance_client import AccountInstanceClient, InstanceClientError


class PrepareOrderRequest(BaseModel):
    exchange: str
    instrument: str
    direction: str
    offset: str
    volume: int = Field(ge=1)
    price_type: str = "limit"
    price: float = 0.0
    time_cond: str = "gfd"
    vol_cond: str = "any"


class SubmitOrderRequest(BaseModel):
    confirmation_token: str
    idempotency_key: str = Field(min_length=1, max_length=160)


class CancelOrderRequest(BaseModel):
    idempotency_key: str = Field(min_length=1, max_length=160)
    exchange: str = ""
    instrument: str = ""
    order_sys_id: str = ""
    order_ref: str = ""


class WriteKeyRequest(BaseModel):
    idempotency_key: str = Field(min_length=1, max_length=160)


class SubscribeRequest(WriteKeyRequest):
    instruments: str = Field(min_length=2, max_length=500)


class LoginRequest(BaseModel):
    token: str


class SessionAuth:
    def __init__(self):
        self.expected_token = os.environ.get("CLAW_WEB_TOKEN", "").strip()
        self.sessions: set[str] = set()

    @property
    def enabled(self) -> bool:
        return bool(self.expected_token)

    def login(self, supplied: str) -> Optional[str]:
        if not self.enabled or secrets.compare_digest(supplied, self.expected_token):
            session = secrets.token_urlsafe(32)
            self.sessions.add(session)
            return session
        return None

    def authenticated(self, request: Request) -> bool:
        if not self.enabled:
            return True
        bearer = request.headers.get("authorization", "")
        if bearer.startswith("Bearer ") and secrets.compare_digest(
            bearer[7:], self.expected_token
        ):
            return True
        return request.cookies.get("claw_session", "") in self.sessions

    def websocket_authenticated(self, websocket: WebSocket) -> bool:
        if not self.enabled:
            return True
        return websocket.cookies.get("claw_session", "") in self.sessions


def create_app(registry_file: str = "", demo: bool = False) -> FastAPI:
    registry = AccountRegistry(Path(registry_file) if registry_file else None)
    client: Any = DemoAccountClient() if demo else AccountInstanceClient(registry)
    audit = AuditLog(PROJECT_ROOT / ".audit" / "management.db")
    auth = SessionAuth()
    frontend_dir = PROJECT_ROOT / "web" / "dist"

    app = FastAPI(
        title="ClawTrader Web",
        version="1.1.0",
        docs_url=None,
        redoc_url=None,
    )
    app.state.client = client
    app.state.demo = demo

    @app.exception_handler(AccountRegistryError)
    async def account_error(_: Request, exc: AccountRegistryError):
        return JSONResponse(status_code=404, content={"ok": False, "error": str(exc)})

    @app.exception_handler(InstanceClientError)
    async def client_error(_: Request, exc: InstanceClientError):
        return JSONResponse(status_code=400, content={"ok": False, "error": str(exc)})

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cache-Control"] = "no-store"
        return response

    def require_auth(request: Request) -> str:
        if not auth.authenticated(request):
            raise HTTPException(status_code=401, detail="需要登录")
        return "web-user"

    def require_write(
        request: Request,
        actor: str = Depends(require_auth),
        requested_with: str = Header(default="", alias="X-Claw-Request"),
    ) -> str:
        if requested_with != "web":
            raise HTTPException(status_code=403, detail="写请求缺少来源校验")
        return actor

    @app.get("/api/health")
    def health() -> Dict[str, Any]:
        return {"ok": True, "demo": demo, "time": time.time()}

    @app.get("/api/auth/status")
    def auth_status(request: Request) -> Dict[str, Any]:
        return {"ok": True, "required": auth.enabled,
                "authenticated": auth.authenticated(request)}

    @app.post("/api/auth/login")
    def login(body: LoginRequest, request: Request, response: Response) -> Dict[str, Any]:
        session = auth.login(body.token)
        if not session:
            raise HTTPException(status_code=401, detail="访问令牌无效")
        response.set_cookie(
            "claw_session", session, httponly=True,
            secure=request.url.scheme == "https",
            samesite="strict", max_age=12 * 60 * 60,
        )
        return {"ok": True}

    @app.get("/api/meta")
    def meta(_: str = Depends(require_auth)) -> Dict[str, Any]:
        return {"ok": True, "demo": demo, "product": "ClawTrader",
                "server_time": time.time()}

    @app.get("/api/accounts")
    def accounts(_: str = Depends(require_auth)) -> Dict[str, Any]:
        return client.list_accounts()

    @app.get("/api/accounts/{account_id}/status")
    def account_status(account_id: str, _: str = Depends(require_auth)):
        return client.status(account_id)

    @app.get("/api/accounts/{account_id}/funds")
    def account_funds(account_id: str, _: str = Depends(require_auth)):
        return client.funds(account_id)

    @app.get("/api/accounts/{account_id}/positions")
    def positions(account_id: str, instrument: str = "", _: str = Depends(require_auth)):
        return client.positions(account_id, instrument)

    @app.get("/api/accounts/{account_id}/orders")
    def orders(account_id: str, instrument: str = "", _: str = Depends(require_auth)):
        return client.orders(account_id, instrument)

    @app.get("/api/accounts/{account_id}/trades")
    def trades(account_id: str, instrument: str = "", _: str = Depends(require_auth)):
        return client.trades(account_id, instrument)

    @app.get("/api/accounts/{account_id}/quote")
    def quote(account_id: str, instrument: str, _: str = Depends(require_auth)):
        return client.quote(account_id, instrument)

    @app.get("/api/accounts/{account_id}/events")
    def events(
        account_id: str, after_seq: int = 0, limit: int = 500,
        _: str = Depends(require_auth),
    ):
        return client.events(account_id, after_seq, limit)

    @app.post("/api/accounts/{account_id}/subscribe")
    def subscribe(
        account_id: str, body: SubscribeRequest,
        actor: str = Depends(require_write),
    ):
        result = client.send(account_id, {
            "cmd": "subscribe", "instruments": body.instruments,
            "idempotency_key": body.idempotency_key,
        })
        audit.record(actor=actor, channel="web", account_id=account_id,
                     action="subscribe", request_key=body.idempotency_key,
                     request=body.model_dump(), response=result)
        return result

    @app.post("/api/accounts/{account_id}/orders/prepare")
    def prepare_order(
        account_id: str, body: PrepareOrderRequest,
        _: str = Depends(require_write),
    ):
        try:
            return client.prepare_order(account_id, **body.model_dump())
        except Exception as exc:
            return {"ok": False, "account_id": account_id, "error": str(exc)}

    @app.post("/api/accounts/{account_id}/orders")
    def submit_order(
        account_id: str, body: SubmitOrderRequest,
        actor: str = Depends(require_write),
    ):
        result = client.submit_prepared_order(
            account_id, body.confirmation_token, body.idempotency_key
        )
        audit.record(actor=actor, channel="web", account_id=account_id,
                     action="place_order", request_key=body.idempotency_key,
                     request=body.model_dump(), response=result)
        return result

    @app.post("/api/accounts/{account_id}/orders/cancel")
    def cancel_order(
        account_id: str, body: CancelOrderRequest,
        actor: str = Depends(require_write),
    ):
        result = client.cancel_order(account_id, **body.model_dump())
        audit.record(actor=actor, channel="web", account_id=account_id,
                     action="cancel_order", request_key=body.idempotency_key,
                     request=body.model_dump(), response=result)
        return result

    @app.post("/api/accounts/{account_id}/orders/cancel-all")
    def cancel_all(
        account_id: str, body: WriteKeyRequest,
        actor: str = Depends(require_write),
    ):
        result = client.cancel_all(account_id, body.idempotency_key)
        audit.record(actor=actor, channel="web", account_id=account_id,
                     action="cancel_all", request_key=body.idempotency_key,
                     request=body.model_dump(), response=result)
        return result

    @app.websocket("/ws/accounts/{account_id}")
    async def account_stream(websocket: WebSocket, account_id: str):
        if not auth.websocket_authenticated(websocket):
            await websocket.close(code=4401)
            return
        await websocket.accept()
        after_seq = int(websocket.query_params.get("after_seq", "0") or "0")
        try:
            while True:
                result = await asyncio.to_thread(
                    client.events, account_id, after_seq, 250
                )
                if result.get("ok"):
                    after_seq = int(result.get("next_seq", after_seq))
                await websocket.send_json(result)
                await asyncio.sleep(0.35)
        except Exception:
            try:
                await websocket.close()
            except Exception:
                pass

    if frontend_dir.exists():
        # The checked-in distribution keeps the small static bundle directly
        # under web/dist; expose it through the stable /assets URL.
        app.mount("/assets", StaticFiles(directory=frontend_dir), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def frontend(path: str):
            candidate = frontend_dir / path
            if path and candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(frontend_dir / "index.html")

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="ClawTrader Web server")
    parser.add_argument("--registry", default="")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=17890)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not os.environ.get("CLAW_WEB_TOKEN"):
        raise SystemExit("非本机监听必须设置 CLAW_WEB_TOKEN")
    import uvicorn
    uvicorn.run(create_app(args.registry, args.demo), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
