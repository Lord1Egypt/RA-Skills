from __future__ import annotations

from typing import Any

from lark_oapi.api.wiki.v2 import (
    CreateSpaceRequest,
    GetNodeSpaceRequest,
    ListSpaceNodeRequest,
    ListSpaceRequest,
    Space,
)

from ..client import create_client
from .base import BaseService


class WikiService(BaseService):
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or create_client()

    def list_spaces(self, *, page_size: int = 50) -> list[dict[str, Any]]:
        request = ListSpaceRequest.builder().page_size(page_size).build()
        response = self.client.wiki.v2.space.list(request)
        self._raise_for_response(response, "list_spaces")
        items = getattr(response.data, "items", None) or []
        return [
            {"space_id": getattr(item, "space_id", None), "name": getattr(item, "name", None), "raw": item}
            for item in items
        ]

    def create_space(self, name: str, *, description: str = "") -> dict[str, Any]:
        request = CreateSpaceRequest.builder().request_body(
            Space.builder().name(name).description(description).build()
        ).build()
        response = self.client.wiki.v2.space.create(request)
        self._raise_for_response(response, "create_space")
        space = getattr(response.data, "space", None)
        return {"space_id": getattr(space, "space_id", None), "name": getattr(space, "name", None), "raw": response.raw}

    def list_nodes(self, space_id: str, *, parent_node_token: str = "", page_size: int = 200) -> list[dict[str, Any]]:
        builder = ListSpaceNodeRequest.builder().space_id(space_id).page_size(page_size)
        if parent_node_token:
            builder = builder.parent_node_token(parent_node_token)
        response = self.client.wiki.v2.space_node.list(builder.build())
        self._raise_for_response(response, "list_nodes")
        items = getattr(response.data, "items", None) or []
        return [
            {
                "node_token": getattr(item, "node_token", None),
                "title": getattr(item, "title", None),
                "obj_type": getattr(item, "obj_type", None),
                "obj_token": getattr(item, "obj_token", None),
                "raw": item,
            }
            for item in items
        ]

    def get_node_info(self, token: str, *, obj_type: str = "docx") -> dict[str, Any]:
        request = GetNodeSpaceRequest.builder().token(token).obj_type(obj_type).build()
        response = self.client.wiki.v2.space.get_node(request)
        self._raise_for_response(response, "get_node_info")
        node = getattr(response.data, "node", None)
        return {
            "space_id": getattr(node, "space_id", None),
            "node_token": getattr(node, "node_token", None),
            "obj_type": getattr(node, "obj_type", None),
            "obj_token": getattr(node, "obj_token", None),
            "raw": response.raw,
        }
