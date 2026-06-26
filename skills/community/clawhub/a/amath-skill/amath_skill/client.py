from __future__ import annotations

from typing import Any

import httpx

from .config import settings


class AmathApiError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None, payload: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class AmathApiClient:
    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._access_token: str | None = settings.access_token

    async def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=settings.api_base,
                timeout=settings.timeout_seconds,
                verify=settings.verify_ssl,
                headers={
                    "User-Agent": settings.user_agent,
                    "Accept": "application/json",
                },
            )
        return self._client

    def set_token(self, token: str | None) -> None:
        self._access_token = token or None

    def clear_token(self) -> None:
        self._access_token = None

    def get_token_preview(self) -> str | None:
        if not self._access_token:
            return None
        if len(self._access_token) <= 12:
            return self._access_token
        return f"{self._access_token[:8]}...{self._access_token[-4:]}"

    def has_token(self) -> bool:
        return bool(self._access_token)

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | list[Any] | None = None,
        form_data: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> Any:
        client = await self._http()
        headers: dict[str, str] = {}
        auth_token = token or self._access_token
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        response = await client.request(
            method=method.upper(),
            url=path,
            params=_drop_none(params),
            json=_drop_none(json_body) if isinstance(json_body, dict) else json_body,
            data=_drop_none(form_data),
            headers=headers,
        )
        return self._unwrap_response(response)

    def _unwrap_response(self, response: httpx.Response) -> Any:
        content_type = response.headers.get("content-type", "")
        payload: Any
        if "application/json" in content_type:
            payload = response.json()
        else:
            text = response.text.strip()
            payload = text if text else {"status_code": response.status_code}

        if response.is_success:
            return payload

        detail = payload
        if isinstance(payload, dict):
            detail = payload.get("detail") or payload
        raise AmathApiError(
            f"API request failed: {response.status_code} {detail}",
            status_code=response.status_code,
            payload=payload,
        )


def _drop_none(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, dict):
        return {k: _drop_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_drop_none(v) for v in value]
    return value


client = AmathApiClient()
