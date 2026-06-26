"""
core/models.py — Pydantic 数据模型
"""

from pydantic import BaseModel
from typing import Optional


class CapsuleIn(BaseModel):
    memo: str
    content: str = ""
    tags: str = ""
    session_id: Optional[str] = None
    window_title: Optional[str] = None
    url: Optional[str] = None


class CapsuleUpdate(BaseModel):
    """Fields that can be updated via PATCH."""
    memo: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    category_path: Optional[str] = None


class CapsuleRecord(BaseModel):
    id: str
    memo: str
    content: str
    tags: str
    session_id: Optional[str]
    window_title: Optional[str]
    url: Optional[str]
    created_at: float
    synced: bool
    # 加密字段（元数据，非明文内容）
    has_encrypted_content: bool = False
    encrypted_len: Optional[int] = None


class FreezeResponse(BaseModel):
    session_key: Optional[str]
    prefill: str
    summary: str
    files: list[dict]
    timestamp: float
