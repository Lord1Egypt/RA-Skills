"""易企秀作品页：可编辑文本、正文配图查询与换图。"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import requests

from .errors import EqxiuAigcApiError


class H5SceneApiMixin:
    """
    依赖宿主类提供：base_url, timeout, _session、以及宿主实现的 _unwrap(resp)。
    """

    base_url: str
    timeout: float
    _session: requests.Session

    def get_editable_text(self, scene_id: int) -> Any:
        r = self._session.get(
            f"{self.base_url}/iaigc/h5_scene/get_editable_text",
            params={"id": scene_id},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return self._unwrap(r)

    def update_editable_text(
        self,
        scene_id: int,
        page_id: int,
        element_id: int,
        content: str,
        *,
        css: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"element_id": element_id, "content": content}
        if css is not None:
            body["css"] = css
        params: Dict[str, Any] = {"id": scene_id, "page_id": page_id}
        r = self._session.post(
            f"{self.base_url}/iaigc/h5_scene/update_editable_text",
            params=params,
            json=body,
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = self._unwrap(r)
        if not isinstance(data, dict):
            raise EqxiuAigcApiError("update_editable_text 返回的 data 不是对象", raw=data)
        return data

    def get_body_images(self, scene_id: int, *, page_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"id": scene_id}
        if page_id is not None:
            params["page_id"] = page_id
        r = self._session.get(
            f"{self.base_url}/iaigc/h5_scene/get_body_images",
            params=params,
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = self._unwrap(r)
        if not isinstance(data, list):
            raise EqxiuAigcApiError("get_body_images 返回的 data 不是数组", raw=data)
        return data

    def replace_body_image(
        self,
        scene_id: int,
        page_id: int,
        element_id: Union[int, str],
        src: str,
        *,
        source_id: Any = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"element_id": element_id, "src": src.strip()}
        if source_id is not None:
            body["sourceId"] = source_id
        r = self._session.post(
            f"{self.base_url}/iaigc/h5_scene/replace_body_image",
            params={"id": scene_id, "page_id": page_id},
            json=body,
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = self._unwrap(r)
        if not isinstance(data, dict):
            raise EqxiuAigcApiError("replace_body_image 返回的 data 不是对象", raw=data)
        return data
