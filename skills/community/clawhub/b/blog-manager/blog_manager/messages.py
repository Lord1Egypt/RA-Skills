"""Message (guestbook) management — 4 API operations.

Endpoints:
  GET    /api/messages               list_messages
  POST   /api/messages               create_message
  POST   /api/messages/reply         reply_message
  DELETE /api/messages/{id}          delete_message
"""

from __future__ import annotations

from typing import Any, Tuple

from .client import BlogClient

MESSAGES_PATH = "/api/messages"


def list_messages(client: BlogClient) -> Tuple[Any, str]:
    return client.get(MESSAGES_PATH), "messages_list"


def create_message(
    client: BlogClient, uid: int, content: str
) -> Tuple[Any, str]:
    return client.post(MESSAGES_PATH, json={"uid": uid, "content": content}), "id_response"


def reply_message(
    client: BlogClient, uid: int, mid: int, content: str
) -> Tuple[Any, str]:
    payload = {"uid": uid, "mid": mid, "content": content}
    return client.post(f"{MESSAGES_PATH}/reply", json=payload), "id_response"


def delete_message(client: BlogClient, message_id: int) -> Tuple[Any, str]:
    return client.delete(f"{MESSAGES_PATH}/{message_id}"), "message_response"
