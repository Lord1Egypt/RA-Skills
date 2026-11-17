"""User management — 2 API operations.

Endpoints:
  GET    /api/users   list_users
  POST   /api/users   create_user
"""

from __future__ import annotations

from typing import Any, Tuple

from .client import BlogClient

USERS_PATH = "/api/users"


def list_users(client: BlogClient) -> Tuple[Any, str]:
    return client.get(USERS_PATH), "users_list"


def create_user(
    client: BlogClient,
    uname: str,
    phone: str = "",
    pwd: str = "",
    email: str = "",
    img: str = "img/moren.jpg",
) -> Tuple[Any, str]:
    payload = {
        "uname": uname,
        "phone": phone,
        "pwd": pwd,
        "email": email,
        "img": img,
    }
    return client.post(USERS_PATH, json=payload), "id_response"
