"""HTTP transport layer for the Dida365 OpenAPI CLI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .errors import ApiError, UserFacingError

UNSET = object()


@dataclass
class HttpResponse:
    status_code: int
    headers: dict[str, str]
    data: Any
    text: str


class HttpTransport:
    """Thin urllib wrapper with structured JSON decoding."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        json_body: Any = UNSET,
        form_body: Optional[Mapping[str, str]] = None,
        timeout: float = 30.0,
    ) -> HttpResponse:
        request_headers = dict(headers or {})
        body: Optional[bytes] = None

        if json_body is not UNSET:
            body = json.dumps(json_body).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        elif form_body is not None:
            body = urlencode(form_body).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

        request = Request(url=url, data=body, headers=request_headers, method=method.upper())

        try:
            with urlopen(request, timeout=timeout) as response:
                raw = response.read()
                return self._decode_response(response.status, response.headers, raw)
        except HTTPError as exc:
            raw = exc.read()
            decoded = self._decode_response(exc.code, exc.headers, raw)
            raise ApiError(
                f"HTTP {exc.code} returned by Dida365",
                status_code=exc.code,
                method=method.upper(),
                url=url,
                response_body=decoded.data if decoded.data is not None else decoded.text,
            ) from exc
        except URLError as exc:
            raise UserFacingError(
                "Unable to reach Dida365",
                details={"reason": str(exc.reason), "url": url},
                exit_code=1,
            ) from exc

    def _decode_response(self, status_code: int, headers: Mapping[str, str], raw: bytes) -> HttpResponse:
        text = raw.decode("utf-8", errors="replace") if raw else ""
        data: Any = None
        content_type = headers.get("Content-Type", "")
        if text:
            if "application/json" in content_type:
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    data = None
            else:
                stripped = text.lstrip()
                if stripped.startswith("{") or stripped.startswith("["):
                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError:
                        data = None
        return HttpResponse(
            status_code=status_code,
            headers={key: headers.get(key, "") for key in headers.keys()},
            data=data,
            text=text,
        )
