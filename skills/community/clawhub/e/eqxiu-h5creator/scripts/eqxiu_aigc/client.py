"""易企秀 /iaigc 主客户端：品类、大纲、场景模板与 H5 页能力。"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

import requests

from .constants import (
    AI_PORTAL_ORIGIN,
    BROWSER_CHROME_UA,
    CONFIG_TOKEN_KEY,
    DEFAULT_UPLOAD_TIMEOUT,
    EQXIU_MATERIAL_API_BASE,
)
from .errors import EqxiuAigcApiError
from .h5_scene_api import H5SceneApiMixin
from .upload_material import list_user_upload_materials


def preview_url_from_scene_tpl(scene_tpl_data: Any) -> Optional[str]:
    if isinstance(scene_tpl_data, dict):
        v = scene_tpl_data.get("previewUrl")
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


class EqxiuAigcClient(H5SceneApiMixin):
    """调用 /iaigc/* 接口。默认 timeout 较大。"""

    def __init__(
        self, base_url: str, timeout: float = 150.0, access_token: Optional[str] = None
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        if access_token:
            self._session.headers.update({CONFIG_TOKEN_KEY: access_token})

    def _access_token(self) -> str:
        return (self._session.headers.get(CONFIG_TOKEN_KEY) or "").strip()

    def list_user_material_uploads(
        self,
        *,
        file_type: int = 1,
        page_no: int = 1,
        page_size: int = 30,
        tag_id: int = -1,
        material_api_base: str = EQXIU_MATERIAL_API_BASE,
    ) -> Dict[str, Any]:
        """查询当前用户在素材库中的上传列表（易企秀 material-api，非 iaigc）。"""
        token = self._access_token()
        if not token:
            raise EqxiuAigcApiError("缺少 X-Openclaw-Token，无法查询素材", raw=None)
        t = min(int(self.timeout), max(DEFAULT_UPLOAD_TIMEOUT, 60))
        try:
            return list_user_upload_materials(
                token,
                file_type=file_type,
                page_no=page_no,
                page_size=page_size,
                tag_id=tag_id,
                material_api_base=material_api_base,
                timeout=t,
            )
        except RuntimeError as e:
            raise EqxiuAigcApiError(str(e), raw=None) from e

    def _unwrap(self, resp: requests.Response) -> Any:
        try:
            payload = resp.json()
        except json.JSONDecodeError as e:
            raise EqxiuAigcApiError(
                f"无效 JSON 响应: {e}", status_code=resp.status_code, raw=resp.text
            ) from e
        if not isinstance(payload, dict):
            raise EqxiuAigcApiError("响应不是 JSON 对象", status_code=resp.status_code, raw=payload)
        if payload.get("success") is False:
            raise EqxiuAigcApiError(
                str(payload.get("msg", "请求失败")),
                status_code=resp.status_code if resp.status_code >= 400 else payload.get("code"),
                raw=payload,
            )
        if "data" in payload:
            return payload["data"]
        return payload

    def create_h5_stream(
        self,
        user_prompt: str,
        *,
        product_code_sub: str,
        on_progress: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        POST /aigc/draw/ai/create/stream — SSE 流式一键生成 H5。
        on_progress(msg: str, payload: dict) 可选，用于输出进度。
        成功时返回最终 data（含 id、code、editUrl、previewUrl 等）。
        """
        prompt = (user_prompt or "").strip()
        if not prompt:
            raise EqxiuAigcApiError("userPrompt 不能为空", raw=None)
        if not self._access_token():
            raise EqxiuAigcApiError("缺少 X-Openclaw-Token", raw=None)

        headers = {
            "Content-Type": "application/json;",
            "Origin": AI_PORTAL_ORIGIN,
            "Referer": f"{AI_PORTAL_ORIGIN}/",
            "User-Agent": BROWSER_CHROME_UA,
        }
        r = self._session.post(
            f"{self.base_url}/aigc/draw/ai/create/stream",
            json={"userPrompt": prompt, "productCodeSub": product_code_sub},
            headers=headers,
            stream=True,
            timeout=self.timeout,
        )
        r.raise_for_status()

        final_data: Optional[Dict[str, Any]] = None
        last_payload: Optional[Dict[str, Any]] = None

        for payload in self._iter_sse_json(r):
            last_payload = payload
            if payload.get("success") is False or (
                payload.get("code") is not None and payload.get("code") != 200
            ):
                raise EqxiuAigcApiError(
                    str(payload.get("msg") or payload.get("codeDesc") or "生成失败"),
                    status_code=payload.get("code"),
                    raw=payload,
                )
            msg = payload.get("msg")
            if isinstance(msg, str) and msg.strip() and on_progress:
                on_progress(msg.strip(), payload)
            data = payload.get("data")
            if isinstance(data, dict) and (
                data.get("previewUrl") or data.get("editUrl") or data.get("id")
            ):
                final_data = data

        if final_data is None:
            raise EqxiuAigcApiError(
                "流式响应未包含作品结果",
                raw=last_payload,
            )
        return final_data

    @staticmethod
    def _iter_sse_json(resp: requests.Response):
        """解析 event:message / data:{json} 形式的 SSE 行。"""
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip() if isinstance(raw_line, str) else raw_line.decode("utf-8").strip()
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if not data_str:
                continue
            try:
                payload = json.loads(data_str)
            except json.JSONDecodeError as e:
                raise EqxiuAigcApiError(f"无效 SSE data JSON: {e}", raw=data_str) from e
            if isinstance(payload, dict):
                yield payload

