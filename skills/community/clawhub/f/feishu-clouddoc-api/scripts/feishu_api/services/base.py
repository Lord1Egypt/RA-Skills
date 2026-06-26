from __future__ import annotations

from typing import Any

from ..errors import FeishuRequestError


class BaseService:
    def _raise_for_response(self, response: Any, action: str) -> None:
        if getattr(response, "success", lambda: False)():
            return

        code = getattr(response, "code", None)
        msg = getattr(response, "msg", None) or f"Feishu API {action} failed"
        request_id = None
        try:
            request_id = response.get_log_id()
        except Exception:
            request_id = None

        raise FeishuRequestError(
            message=msg,
            code=code,
            request_id=request_id,
            details=response,
        )
