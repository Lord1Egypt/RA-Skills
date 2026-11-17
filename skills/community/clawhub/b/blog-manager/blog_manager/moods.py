"""Mood (status / 说说) management — 3 API operations.

Endpoints:
  GET    /api/moods               list_moods
  POST   /api/moods               create_mood
  DELETE /api/moods/{id}          delete_mood
"""

from __future__ import annotations

from typing import Any, Tuple

from .client import BlogClient

MOODS_PATH = "/api/moods"


def list_moods(client: BlogClient) -> Tuple[Any, str]:
    return client.get(MOODS_PATH), "moods_list"


def create_mood(
    client: BlogClient,
    content: str,
    title: str = "",
    src: str = "",
) -> Tuple[Any, str]:
    payload = {"content": content, "title": title, "src": src}
    return client.post(MOODS_PATH, json=payload), "id_response"


def delete_mood(client: BlogClient, mood_id: int) -> Tuple[Any, str]:
    return client.delete(f"{MOODS_PATH}/{mood_id}"), "message_response"
