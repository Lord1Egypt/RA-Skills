"""Comment management — 3 API operations.

Endpoints:
  POST   /api/comments            create_comment
  GET    /api/comments/{aid}      list_comments
  DELETE /api/comments/{id}       delete_comment
"""

from __future__ import annotations

from typing import Any, Tuple

from .client import BlogClient

COMMENTS_PATH = "/api/comments"


def create_comment(
    client: BlogClient, uid: int, aid: int, content: str
) -> Tuple[Any, str]:
    payload = {"uid": uid, "aid": aid, "content": content}
    return client.post(COMMENTS_PATH, json=payload), "id_response"


def list_comments(client: BlogClient, aid: int) -> Tuple[Any, str]:
    return client.get(f"{COMMENTS_PATH}/{aid}"), "comments_list"


def delete_comment(client: BlogClient, comment_id: int) -> Tuple[Any, str]:
    return client.delete(f"{COMMENTS_PATH}/{comment_id}"), "message_response"
