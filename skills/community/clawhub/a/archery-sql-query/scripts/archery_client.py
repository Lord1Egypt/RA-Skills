#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests


class ArcheryError(RuntimeError):
    pass


class ArcheryClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 15,
        verify: bool = True,
        session_file: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "archery-cli/1.0"})
        self.session_file = Path(session_file).expanduser() if session_file else None

    def _url(self, path: str) -> str:
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def _cookie_dict(self) -> dict[str, str]:
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def _csrf_token(self) -> str:
        # Tolerate duplicate-named cookies (e.g. csrftoken on both / and /login/).
        # Prefer the one set on /login/ if present, otherwise pick any non-empty one.
        candidates = [c for c in self.session.cookies if c.name == "csrftoken" and c.value]
        if not candidates:
            raise ArcheryError("csrftoken not found in current session")
        # Prefer most specific path (longest path) so /login/ wins over /
        candidates.sort(key=lambda c: len(c.path or ""), reverse=True)
        return candidates[0].value

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        referer: str | None = None,
    ) -> requests.Response:
        headers = {}
        if referer:
            headers["Referer"] = referer
        if method.upper() != "GET":
            headers["X-CSRFToken"] = self._csrf_token()
            headers["X-Requested-With"] = "XMLHttpRequest"
        response = self.session.request(
            method=method.upper(),
            url=self._url(path),
            params=params,
            data=data,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise ArcheryError(
                f"{method.upper()} {path} failed: {exc}\nBody: {response.text}"
            ) from exc
        return response

    def _json(self, response: requests.Response, path: str) -> dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise ArcheryError(
                f"{path} did not return JSON:\n{response.text}"
            ) from exc

    def _unwrap(self, payload: dict[str, Any], path: str) -> Any:
        if payload.get("status") not in (0, None):
            raise ArcheryError(f"{path} failed: {payload.get('msg', payload)}")
        if "data" in payload:
            return payload["data"]
        return payload

    def bootstrap_login_page(self) -> dict[str, str]:
        response = self._request("GET", "/login/")
        # Use cookies.iterkeys() to tolerate duplicate-named cookies
        # (Archery may set csrftoken on both / and /login/).
        cookie_names = {c.name for c in self.session.cookies}
        if "csrftoken" not in cookie_names:
            raise ArcheryError("GET /login/ succeeded but csrftoken is missing")
        return self._cookie_dict()

    def login(
        self,
        username: str,
        password: str,
        *,
        otp: str | None = None,
        auth_type: str = "totp",
        phone: str = "",
        key: str = "",
    ) -> dict[str, Any]:
        referer = self._url("/login/")
        self.bootstrap_login_page()
        payload = self._json(
            self._request(
                "POST",
                "/authenticate/",
                data={"username": username, "password": password},
                referer=referer,
            ),
            "/authenticate/",
        )
        if payload.get("status") != 0:
            raise ArcheryError(payload.get("msg", "login failed"))

        if payload.get("data"):
            self.session.cookies.set("sessionid", payload["data"])
            if not otp:
                return {
                    "status": "2fa_required",
                    "cookies": self._cookie_dict(),
                    "payload": payload,
                }

            verify_payload = self._json(
                self._request(
                    "POST",
                    "/api/v1/user/2fa/verify/",
                    data={
                        "engineer": username,
                        "auth_type": auth_type,
                        "otp": otp,
                        "phone": phone,
                        "key": key,
                    },
                    referer=self._url("/login/2fa/"),
                ),
                "/api/v1/user/2fa/verify/",
            )
            if verify_payload.get("status") != 0:
                raise ArcheryError(verify_payload.get("msg", "2FA verify failed"))
            result = {"status": "ok", "cookies": self._cookie_dict(), "payload": verify_payload}
        else:
            result = {"status": "ok", "cookies": self._cookie_dict(), "payload": payload}

        if self.session_file:
            self.save_session()
        return result

    def save_session(self) -> None:
        if not self.session_file:
            raise ArcheryError("session_file is not configured")
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "base_url": self.base_url,
            "cookies": self._cookie_dict(),
        }
        self.session_file.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        )

    def load_session(self) -> bool:
        if not self.session_file or not self.session_file.exists():
            return False
        payload = json.loads(self.session_file.read_text())
        if payload.get("base_url", "").rstrip("/") != self.base_url:
            return False
        self.session.cookies = requests.utils.cookiejar_from_dict(
            payload.get("cookies", {})
        )
        return True

    def _get_cookie_value(self, name: str) -> str | None:
        """获取 cookie 值，兼容重复名称的情况"""
        candidates = [c for c in self.session.cookies if c.name == name and c.value]
        if not candidates:
            return None
        # 返回第一个非空值
        return candidates[0].value

    def ensure_session(self) -> None:
        if not self._get_cookie_value("sessionid"):
            raise ArcheryError(
                "sessionid not found. Run the login command first or provide a valid session file."
            )
        if not self._get_cookie_value("csrftoken"):
            raise ArcheryError(
                "csrftoken not found. Run the login command first or refresh the session."
            )
        # 验证 session 是否真正有效（cookie 存在但可能已过期）
        # 用轻量 API 探测，避免后续查询返回登录页 HTML
        try:
            resp = self._request("GET", "/group/user_all_instances/", referer=self._url("/sqlquery/"))
            text = resp.text.strip()
            if text.startswith("<") or text.startswith("<!DOCTYPE"):
                # 服务器返回 HTML → session 已过期，清除并重新登录
                self.session.cookies.clear()
                if self.session_file and self.session_file.exists():
                    self.session_file.unlink()
                raise ArcheryError("Session expired. Please re-login.")
        except ArcheryError:
            raise
        except Exception:
            pass  # 网络等其他错误不在此处拦截，后续查询会报出

    def list_instances(
        self,
        *,
        tag_codes: list[str] | None = None,
        type_name: str | None = None,
        db_types: list[str] | None = None,
    ) -> Any:
        self.ensure_session()
        params: list[tuple[str, str]] = []
        for tag_code in tag_codes or []:
            params.append(("tag_codes[]", tag_code))
        for db_type in db_types or []:
            params.append(("db_type[]", db_type))
        if type_name:
            params.append(("type", type_name))
        response = self._request(
            "GET",
            "/group/user_all_instances/",
            params=params or None,
            referer=self._url("/sqlquery/"),
        )
        payload = self._json(response, "/group/user_all_instances/")
        return self._unwrap(payload, "/group/user_all_instances/")

    def list_resources(
        self,
        *,
        instance_name: str,
        db_name: str = "",
        schema_name: str = "",
        tb_name: str = "",
        resource_type: str,
    ) -> Any:
        self.ensure_session()
        response = self._request(
            "GET",
            "/instance/instance_resource/",
            params={
                "instance_name": instance_name,
                "db_name": db_name,
                "schema_name": schema_name,
                "tb_name": tb_name,
                "resource_type": resource_type,
            },
            referer=self._url("/sqlquery/"),
        )
        payload = self._json(response, "/instance/instance_resource/")
        return self._unwrap(payload, "/instance/instance_resource/")

    def describe_table(
        self,
        *,
        instance_name: str,
        db_name: str,
        tb_name: str,
        schema_name: str = "",
    ) -> Any:
        self.ensure_session()
        response = self._request(
            "POST",
            "/instance/describetable/",
            data={
                "instance_name": instance_name,
                "db_name": db_name,
                "schema_name": schema_name,
                "tb_name": tb_name,
            },
            referer=self._url("/sqlquery/"),
        )
        payload = self._json(response, "/instance/describetable/")
        return self._unwrap(payload, "/instance/describetable/")

    def query(
        self,
        *,
        instance_name: str,
        db_name: str,
        sql_content: str,
        tb_name: str = "",
        schema_name: str = "",
        limit_num: int = 100,
    ) -> Any:
        self.ensure_session()
        response = self._request(
            "POST",
            "/query/",
            data={
                "instance_name": instance_name,
                "db_name": db_name,
                "schema_name": schema_name,
                "tb_name": tb_name,
                "sql_content": sql_content,
                "limit_num": str(limit_num),
            },
            referer=self._url("/sqlquery/"),
        )
        payload = self._json(response, "/query/")
        return self._unwrap(payload, "/query/")
