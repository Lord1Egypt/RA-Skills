"""Article management — 7 API operations.

Endpoints:
  GET    /api/articles                   list_articles
  POST   /api/articles                   create_article
  GET    /api/articles/{id}              get_article
  PUT    /api/articles/{id}              update_article
  DELETE /api/articles/{id}?soft=        delete_article
  POST   /api/articles/{id}/restore      restore_article
  GET    /api/articles/heat/top          top_articles
"""

from __future__ import annotations

from typing import Any, Optional, Tuple

from .client import BlogClient

ARTICLES_PATH = "/api/articles"


def list_articles(
    client: BlogClient,
    page: int = 1,
    size: int = 10,
    lid: int = 0,
    keyword: str = "",
) -> Tuple[Any, str]:
    params: dict = {"page": page, "size": size, "lid": lid}
    if keyword:
        params["keyword"] = keyword
    return client.get(ARTICLES_PATH, params=params), "articles_list"


def create_article(
    client: BlogClient,
    title: str,
    content: str,
    uid: int = 1,
    lid: int = 1,
    img: Optional[str] = None,
    heat: int = 0,
) -> Tuple[Any, str]:
    payload: dict = {
        "title": title,
        "content": content,
        "uid": uid,
        "lid": lid,
        "heat": heat,
    }
    if img is not None:
        payload["img"] = img
    return client.post(ARTICLES_PATH, json=payload), "id_response"


def get_article(client: BlogClient, article_id: int) -> Tuple[Any, str]:
    return client.get(f"{ARTICLES_PATH}/{article_id}"), "article_get"


def update_article(
    client: BlogClient,
    article_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    lid: Optional[int] = None,
    img: Optional[str] = None,
    heat: Optional[int] = None,
) -> Tuple[Any, str]:
    payload: dict = {}
    if title is not None:
        payload["title"] = title
    if content is not None:
        payload["content"] = content
    if lid is not None:
        payload["lid"] = lid
    if img is not None:
        payload["img"] = img
    if heat is not None:
        payload["heat"] = heat
    return client.put(f"{ARTICLES_PATH}/{article_id}", json=payload), "message_response"


def delete_article(
    client: BlogClient, article_id: int, soft: bool = True
) -> Tuple[Any, str]:
    soft_str = "true" if soft else "false"
    path = f"{ARTICLES_PATH}/{article_id}"
    return client.delete(path, params={"soft": soft_str}), "message_response"


def restore_article(client: BlogClient, article_id: int) -> Tuple[Any, str]:
    return client.post(f"{ARTICLES_PATH}/{article_id}/restore"), "message_response"


def top_articles(client: BlogClient, limit: int = 5) -> Tuple[Any, str]:
    return client.get(f"{ARTICLES_PATH}/heat/top", params={"limit": limit}), "articles_top"
