from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from lark_oapi.api.im.v1 import (
    CreateFileRequest,
    CreateFileRequestBody,
    CreateImageRequest,
    CreateImageRequestBody,
    CreateMessageRequest,
    CreateMessageRequestBody,
    GetMessageRequest,
    ListMessageRequest,
    ReplyMessageRequest,
    ReplyMessageRequestBody,
)

from ..client import create_client
from .base import BaseService


class IMService(BaseService):
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or create_client()

    def send_text(self, receive_id: str, text: str, *, receive_id_type: str = "open_id") -> dict[str, Any]:
        content = json.dumps({"text": text}, ensure_ascii=False)
        request = CreateMessageRequest.builder() \
            .receive_id_type(receive_id_type) \
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(receive_id)
                .msg_type("text")
                .content(content)
                .uuid(str(uuid.uuid4()))
                .build()
            ) \
            .build()
        response = self.client.im.v1.message.create(request)
        self._raise_for_response(response, "send_text")
        data = getattr(response, "data", None)
        return {
            "message_id": getattr(data, "message_id", None),
            "root_id": getattr(data, "root_id", None),
            "parent_id": getattr(data, "parent_id", None),
            "thread_id": getattr(data, "thread_id", None),
            "chat_id": getattr(data, "chat_id", None),
            "raw": response.raw,
        }

    def send_post(self, receive_id: str, title: str, lines: list[list[dict[str, str]]], *, receive_id_type: str = "open_id") -> dict[str, Any]:
        content = json.dumps({
            "zh_cn": {
                "title": title,
                "content": lines,
            }
        }, ensure_ascii=False)
        request = CreateMessageRequest.builder() \
            .receive_id_type(receive_id_type) \
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(receive_id)
                .msg_type("post")
                .content(content)
                .uuid(str(uuid.uuid4()))
                .build()
            ) \
            .build()
        response = self.client.im.v1.message.create(request)
        self._raise_for_response(response, "send_post")
        data = getattr(response, "data", None)
        return {
            "message_id": getattr(data, "message_id", None),
            "chat_id": getattr(data, "chat_id", None),
            "raw": response.raw,
        }

    def get_message(self, message_id: str) -> dict[str, Any]:
        request = GetMessageRequest.builder().message_id(message_id).build()
        response = self.client.im.v1.message.get(request)
        self._raise_for_response(response, "get_message")
        items = getattr(response.data, "items", None) or []
        message = items[0] if items else None
        return {
            "message_id": getattr(message, "message_id", None),
            "chat_id": getattr(message, "chat_id", None),
            "msg_type": getattr(message, "msg_type", None),
            "content": getattr(getattr(message, "body", None), "content", None),
            "raw": response.raw,
        }

    def list_messages(self, chat_id: str, *, start_time: str, end_time: str, page_size: int = 20) -> list[dict[str, Any]]:
        request = ListMessageRequest.builder() \
            .container_id_type("chat") \
            .container_id(chat_id) \
            .start_time(start_time) \
            .end_time(end_time) \
            .sort_type("ByCreateTimeDesc") \
            .page_size(page_size) \
            .build()
        response = self.client.im.v1.message.list(request)
        self._raise_for_response(response, "list_messages")
        items = getattr(response.data, "items", None) or []
        return [
            {
                "message_id": getattr(item, "message_id", None),
                "chat_id": getattr(item, "chat_id", None),
                "msg_type": getattr(item, "msg_type", None),
                "create_time": getattr(item, "create_time", None),
                "raw": item,
            }
            for item in items
        ]

    def reply_text(self, message_id: str, text: str, *, reply_in_thread: bool = False) -> dict[str, Any]:
        content = json.dumps({"text": text}, ensure_ascii=False)
        request = ReplyMessageRequest.builder() \
            .message_id(message_id) \
            .request_body(
                ReplyMessageRequestBody.builder()
                .msg_type("text")
                .content(content)
                .reply_in_thread(reply_in_thread)
                .uuid(str(uuid.uuid4()))
                .build()
            ) \
            .build()
        response = self.client.im.v1.message.reply(request)
        self._raise_for_response(response, "reply_text")
        data = getattr(response, "data", None)
        return {
            "message_id": getattr(data, "message_id", None),
            "root_id": getattr(data, "root_id", None),
            "parent_id": getattr(data, "parent_id", None),
            "thread_id": getattr(data, "thread_id", None),
            "chat_id": getattr(data, "chat_id", None),
            "raw": response.raw,
        }

    def upload_image(self, path: str | Path, *, image_type: str = "message") -> dict[str, Any]:
        file_path = Path(path)
        with file_path.open("rb") as f:
            request = CreateImageRequest.builder().request_body(
                CreateImageRequestBody.builder()
                .image_type(image_type)
                .image(f)
                .build()
            ).build()
            response = self.client.im.v1.image.create(request)
        self._raise_for_response(response, "upload_im_image")
        return {"image_key": getattr(response.data, "image_key", None), "raw": response.raw}

    def upload_file(self, path: str | Path, *, file_type: str = "stream") -> dict[str, Any]:
        file_path = Path(path)
        with file_path.open("rb") as f:
            request = CreateFileRequest.builder().request_body(
                CreateFileRequestBody.builder()
                .file_type(file_type)
                .file_name(file_path.name)
                .file(f)
                .build()
            ).build()
            response = self.client.im.v1.file.create(request)
        self._raise_for_response(response, "upload_im_file")
        return {"file_key": getattr(response.data, "file_key", None), "raw": response.raw}
