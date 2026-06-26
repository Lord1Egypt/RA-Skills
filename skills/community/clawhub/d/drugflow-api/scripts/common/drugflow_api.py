#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Dict, Optional

import requests


def normalize_base_url(base_url: str) -> str:
    value = (base_url or "").strip()
    if not value:
        raise ValueError("base_url cannot be empty")
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value.rstrip("/")


def _safe_json(resp: requests.Response) -> Any:
    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text}


def _flatten_payload(payload: Any) -> str:
    if isinstance(payload, dict):
        return " ".join(_flatten_payload(v) for v in payload.values())
    if isinstance(payload, list):
        return " ".join(_flatten_payload(v) for v in payload)
    return str(payload)


class DrugFlowAPIClient:
    def __init__(self, base_url: str, session: Optional[requests.Session] = None, timeout: int = 60):
        self.base_url = normalize_base_url(base_url)
        self.session = session or requests.Session()
        self.timeout = timeout

    def build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def request_or_raise(self, method: str, path: str, timeout: Optional[int] = None, **kwargs: Any) -> Any:
        url = self.build_url(path)
        resp = self.session.request(method=method, url=url, timeout=timeout or self.timeout, **kwargs)
        payload = _safe_json(resp)
        if resp.status_code >= 400:
            raise RuntimeError(f"{method} {url} failed ({resp.status_code}): {payload}")
        return payload

    def signin(self, email: str, password: str, phone: Optional[str] = None) -> Dict[str, Any]:
        payload_data: Dict[str, str] = {
            "email": email,
            "password": password,
            # Some deployments keep LoginUserForm.phone as required even for email login.
            "phone": phone or "0",
        }
        payload = self.request_or_raise(
            "POST",
            "/signin",
            data=payload_data,
        )
        if payload.get("detail") != "ok":
            raise RuntimeError(f"signin did not return detail=ok: {payload}")
        return payload

    def signup(
        self,
        email: str,
        password: str,
        name: str = "codex-user",
        organization: str = "codex",
        allow_exists: bool = False,
    ) -> Dict[str, Any]:
        url = self.build_url("/signup")
        resp = self.session.request(
            method="POST",
            url=url,
            timeout=self.timeout,
            data={
                "email": email,
                "name": name,
                "organization": organization,
                "password1": password,
                "password2": password,
            },
        )
        payload = _safe_json(resp)
        if resp.status_code >= 400:
            if allow_exists and "exist" in _flatten_payload(payload).lower():
                return payload
            raise RuntimeError(f"POST {url} failed ({resp.status_code}): {payload}")
        return payload

    def list_workspaces(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        payload = self.request_or_raise(
            "GET",
            "/api/workspace/list",
            params={"page": page, "page_size": page_size},
        )
        if not isinstance(payload, dict):
            raise RuntimeError(f"unexpected workspace list payload: {payload}")
        return payload

    def create_workspace(self, ws_name: str, is_default: bool = True) -> Dict[str, Any]:
        payload = self.request_or_raise(
            "POST",
            "/api/workspace/create",
            json={"ws_name": ws_name, "is_default": is_default},
        )
        if not isinstance(payload, dict):
            raise RuntimeError(f"unexpected workspace create payload: {payload}")
        return payload

    def ensure_workspace(self, ws_id: Optional[str], ws_name: str) -> str:
        if ws_id:
            return ws_id

        listing = self.list_workspaces(page=1, page_size=20)
        results = listing.get("results", [])
        if results:
            default_ws = next((x for x in results if x.get("status") == 1), None)
            picked = default_ws or results[0]
            picked_ws_id = picked.get("ws_id")
            if not isinstance(picked_ws_id, str):
                raise RuntimeError(f"workspace list item missing ws_id: {picked}")
            return picked_ws_id

        created = self.create_workspace(ws_name=ws_name, is_default=True)
        if created.get("status") != "ok":
            raise RuntimeError(f"workspace create failed: {created}")
        picked_ws_id = created.get("ws_id")
        if not isinstance(picked_ws_id, str):
            raise RuntimeError(f"workspace create missing ws_id: {created}")
        return picked_ws_id

    def get_balance(self, account: str = "person") -> int:
        payload = self.request_or_raise(
            "GET",
            "/api/token/balance",
            params={"account": account},
        )
        tokens = payload.get("tokens")
        if not isinstance(tokens, int):
            raise RuntimeError(f"unexpected balance payload: {payload}")
        return tokens

    def list_jobs(self, ws_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        params = {"ws_id": ws_id, "page": page, "page_size": page_size}
        try:
            payload = self.request_or_raise("GET", "/api/jobs", params=params)
        except RuntimeError:
            remapped_ws_id = self._resolve_numeric_workspace_id(ws_id)
            if remapped_ws_id is None or str(remapped_ws_id) == str(ws_id):
                raise
            payload = self.request_or_raise(
                "GET",
                "/api/jobs",
                params={"ws_id": remapped_ws_id, "page": page, "page_size": page_size},
            )
        if not isinstance(payload, dict):
            raise RuntimeError(f"unexpected jobs list payload: {payload}")
        return payload

    def _resolve_numeric_workspace_id(self, ws_id: str) -> Optional[int]:
        listing = self.list_workspaces(page=1, page_size=200)
        for item in listing.get("results", []):
            if item.get("ws_id") == ws_id and isinstance(item.get("id"), int):
                return item["id"]
        return None
