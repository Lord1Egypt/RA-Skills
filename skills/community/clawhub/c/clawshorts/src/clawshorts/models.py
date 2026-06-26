"""Pydantic Device model for ClawShorts."""
from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator, model_validator

__all__ = ["Device"]


class Device(BaseModel):
    """Fire TV device configuration."""

    ip: str
    name: str | None = Field(default=None)
    limit: int = Field(default=300, ge=0)
    enabled: bool = True

    model_config = {"frozen": False, "extra": "ignore"}

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        if not re.match(r"^(\d{1,3}\.){3}\d{1,3}$", v):
            raise ValueError(f"Invalid IP format: {v}")
        if any(int(o) > 255 for o in v.split(".")):
            raise ValueError(f"Invalid IP (octet > 255): {v}")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is None:
            return v
        sanitized = re.sub(r"[^a-zA-Z0-9\-_]", "", v)
        if not sanitized:
            raise ValueError("Name cannot be only special characters")
        return sanitized[:50]

    @model_validator(mode="after")
    def auto_name(self) -> "Device":
        if not self.name:
            self.name = f"tv-{self.ip.replace('.', '-')}"
        return self

    def __str__(self) -> str:
        s = "on" if self.enabled else "off"
        return f"{self.name} ({self.ip}) {self.limit}/day [{s}]"
