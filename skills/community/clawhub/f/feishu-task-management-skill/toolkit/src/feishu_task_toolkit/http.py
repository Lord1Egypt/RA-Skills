from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib import parse, request
from urllib.error import HTTPError

from .config import AppConfig


class ApiError(RuntimeError):
    def __init__(self, status: int, code: int | None, message: str, payload: Any | None = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.payload = payload


@dataclass
class FeishuHttpClient:
    config: AppConfig
    _tenant_token: str | None = None

    def get_tenant_access_token(self) -> str:
        if self._tenant_token:
            return self._tenant_token
        payload = {"app_id": self.config.app_id, "app_secret": self.config.app_secret}
        response = self.request(
            "POST",
            "/auth/v3/tenant_access_token/internal",
            body=payload,
            use_auth=False,
        )
        token = response.get("tenant_access_token")
        if not token:
            raise ApiError(status=200, code=response.get("code"), message="missing tenant_access_token", payload=response)
        self._tenant_token = token
        return token

    def get_auth_token_for_path(self, path: str) -> str:
        if path.startswith("/task/") and self.config.user_access_token:
            return self.config.user_access_token
        return self.get_tenant_access_token()

    def exchange_authorization_code(
        self,
        code: str,
        redirect_uri: str | None = None,
        code_verifier: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.config.app_id,
            "client_secret": self.config.app_secret,
            "code": code,
        }
        if redirect_uri:
            body["redirect_uri"] = redirect_uri
        if code_verifier:
            body["code_verifier"] = code_verifier
        return self.request("POST", "/authen/v2/oauth/token", body=body, use_auth=False)

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        use_auth: bool = True,
    ) -> dict[str, Any]:
        url = f"{self.config.base_url}{path}"
        if params:
            query = parse.urlencode({key: value for key, value in params.items() if value is not None})
            if query:
                url = f"{url}?{query}"

        headers = {"Content-Type": "application/json; charset=utf-8"}
        if use_auth:
            headers["Authorization"] = f"Bearer {self.get_auth_token_for_path(path)}"

        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")

        req = request.Request(url=url, data=data, method=method.upper(), headers=headers)
        try:
            with request.urlopen(req) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {"code": None, "msg": raw}
            raise ApiError(status=exc.code, code=payload.get("code"), message=payload.get("msg", "http error"), payload=payload) from exc

        if payload.get("code") not in (None, 0):
            raise ApiError(status=200, code=payload.get("code"), message=payload.get("msg", "api error"), payload=payload)
        return payload.get("data", payload)
