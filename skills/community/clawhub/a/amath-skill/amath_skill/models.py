from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ApiEnvelope(BaseModel):
    ok: bool = True
    endpoint: str
    data: Any


class AuthResult(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    persisted: bool = False


class SessionTokenState(BaseModel):
    has_token: bool
    token_preview: str | None = None
