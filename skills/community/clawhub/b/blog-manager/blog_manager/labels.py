"""Label (tag) management — 2 API operations.

Endpoints:
  GET    /api/lables   list_labels
  POST   /api/lables   create_label
"""

from __future__ import annotations

from typing import Any, Tuple

from .client import BlogClient

LABELS_PATH = "/api/lables"


def list_labels(client: BlogClient) -> Tuple[Any, str]:
    return client.get(LABELS_PATH), "labels_list"


def create_label(client: BlogClient, lname: str) -> Tuple[Any, str]:
    return client.post(LABELS_PATH, json={"lname": lname}), "label_create"
