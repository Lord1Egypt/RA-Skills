from __future__ import annotations

from typing import Any

from lark_oapi.api.drive.v1 import ListFileRequest

from ..client import create_client
from .base import BaseService


class DriveService(BaseService):
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or create_client()

    def list_files(self, *, page_size: int = 50) -> list[dict[str, Any]]:
        request = ListFileRequest.builder().page_size(page_size).build()
        response = self.client.drive.v1.file.list(request)
        self._raise_for_response(response, "list_files")
        items = getattr(response.data, "files", None) or []
        return [
            {
                "token": getattr(item, "token", None),
                "name": getattr(item, "name", None),
                "type": getattr(item, "type", None),
                "url": getattr(item, "url", None),
                "raw": item,
            }
            for item in items
        ]

    def find_file_by_token(self, token: str, *, page_size: int = 200) -> dict[str, Any] | None:
        items = self.list_files(page_size=page_size)
        for item in items:
            if item.get("token") == token:
                return item
        return None
