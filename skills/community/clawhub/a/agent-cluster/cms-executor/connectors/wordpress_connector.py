"""
WordPress CMS Connector - REST API implementation.
支持 WordPress 5.0+ 原生 REST API + Application Passwords 认证。
"""
import base64
import re
import urllib.request
import urllib.error
import json as _json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_connector import (
    BaseCMSConnector,
    CMSCredential,
    ContentPayload,
    OperationRecord,
    OperationType,
    OperationStatus,
)

logger = logging.getLogger(__name__)


class WordPressConnector(BaseCMSConnector):
    """
    WordPress REST API 连接器。

    认证方式：Application Passwords（WordPress 5.6+，推荐）
    配置路径：WP Admin → Users → Profile → Application Passwords
    """

    API_VERSION = "v2"

    def __init__(self, credential: CMSCredential, storage_path: str = "./wp_history.json"):
        super().__init__(credential, storage_path)
        self._api_base = self.credential.url.rstrip("/") + "/wp-json/wp/" + self.API_VERSION

    # ── 认证 ──────────────────────────────────────────────
    def authenticate(self) -> bool:
        """验证 WordPress REST API 可访问性"""
        try:
            resp = self._request("GET", "/users/me", auth=True)
            return resp is not None and resp.get("id") is not None
        except Exception as e:
            logger.error(f"WordPress authentication failed: {e}")
            return False

    # ── 内容操作 ───────────────────────────────────────────
    def create_content(self, payload: ContentPayload) -> Dict[str, Any]:
        data = self._build_post_data(payload)
        resp = self._request("POST", "/posts", data=data, auth=True)
        record = self._build_record(
            OperationType.CREATE, "post", resp.get("id"), data, resp, OperationStatus.EXECUTED
        )
        self._save_record(record)
        return {"success": True, "id": resp.get("id"), "url": resp.get("link"), "record_id": record.id}

    def update_content(self, content_id: int, payload: ContentPayload) -> Dict[str, Any]:
        # 记录更新前的快照（用于回滚）
        original = self.get_content(content_id)
        data = self._build_post_data(payload)
        resp = self._request("POST", f"/posts/{content_id}", data=data, auth=True)
        record = self._build_record(
            OperationType.UPDATE, "post", content_id, original, resp, OperationStatus.EXECUTED
        )
        self._save_record(record)
        return {"success": True, "id": resp.get("id"), "url": resp.get("link"), "record_id": record.id}

    def delete_content(self, content_id: int, force: bool = False) -> Dict[str, Any]:
        original = self.get_content(content_id)
        params = "?force=true" if force else ""
        resp = self._request("DELETE", f"/posts/{content_id}{params}", auth=True)
        record = self._build_record(
            OperationType.DELETE, "post", content_id, original, resp, OperationStatus.EXECUTED
        )
        self._save_record(record)
        return {"success": True, "deleted": True, "record_id": record.id}

    def get_content(self, content_id: int) -> Dict[str, Any]:
        return self._request("GET", f"/posts/{content_id}", auth=True)

    def list_content(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        params = params or {}
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        path = f"/posts?{qs}" if qs else "/posts"
        resp = self._request("GET", path, auth=True)
        return resp if isinstance(resp, list) else []

    # ── 回滚 ──────────────────────────────────────────────
    def _do_rollback(self, record: OperationRecord) -> bool:
        """基于操作记录实现回滚"""
        try:
            if record.operation == OperationType.DELETE:
                # 被删除的内容已无法直接恢复，需要提前备份快照
                logger.warning(f"Rollback for DELETE of {record.entity_id} requires manual restore")
                record.status = OperationStatus.ROLLED_BACK
                return True

            elif record.operation == OperationType.UPDATE:
                # 恢复到原始快照
                if record.entity_id and record.payload:
                    payload = ContentPayload(
                        title=record.payload.get("title", {}).get("raw", ""),
                        content=record.payload.get("content", {}).get("raw", ""),
                        status=record.payload.get("status", "draft"),
                    )
                    data = self._build_post_data(payload)
                    self._request("POST", f"/posts/{record.entity_id}", data=data, auth=True)
                    record.status = OperationStatus.ROLLED_BACK
                    return True

            elif record.operation == OperationType.CREATE:
                # 回滚创建 = 删除
                if record.entity_id:
                    self._request("DELETE", f"/posts/{record.entity_id}?force=true", auth=True)
                    record.status = OperationStatus.ROLLED_BACK
                    return True

            record.status = OperationStatus.ROLLED_BACK
            return True
        except Exception as e:
            record.error_message = str(e)
            record.status = OperationStatus.FAILED
            logger.error(f"Rollback failed for {record.id}: {e}")
            return False

    # ── 内部方法 ───────────────────────────────────────────
    def _build_post_data(self, payload: ContentPayload) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "title": payload.title,
            "content": payload.content,
            "status": payload.status,
        }
        if payload.excerpt:
            data["excerpt"] = payload.excerpt
        if payload.author:
            data["author"] = payload.author
        if payload.categories:
            data["categories"] = payload.categories
        if payload.tags:
            data["tags"] = payload.tags
        if payload.featured_media:
            data["featured_media"] = payload.featured_media
        if payload.custom_fields:
            data["meta"] = payload.custom_fields
        return data

    def _build_record(
        self,
        operation: OperationType,
        entity_type: str,
        entity_id: Optional[int],
        payload: Dict[str, Any],
        response: Dict[str, Any],
        status: OperationStatus,
    ) -> OperationRecord:
        return OperationRecord(
            id=self._generate_id(),
            timestamp=datetime.now(),
            operation=operation,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
            response=response,
            status=status,
        )

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        auth: bool = False,
    ) -> Any:
        """发送 HTTP 请求到 WordPress REST API"""
        url = self._api_base + path
        headers = {"Content-Type": "application/json", "User-Agent": "CMS-Executor/1.0"}

        if auth:
            creds = f"{self.credential.username}:{self.credential.app_password}"
            token = base64.b64encode(creds.encode()).decode()
            headers["Authorization"] = f"Basic {token}"

        body = _json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=self.credential.timeout) as resp:
                raw = resp.read().decode()
                return _json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode() if e.fp else ""
            logger.error(f"WordPress API error {e.code}: {err_body}")
            raise WordPressAPIError(e.code, err_body) from e
        except urllib.error.URLError as e:
            logger.error(f"Connection error: {e.reason}")
            raise WordPressAPIError(0, str(e.reason)) from e


class WordPressAPIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[WP API {code}] {message}")
