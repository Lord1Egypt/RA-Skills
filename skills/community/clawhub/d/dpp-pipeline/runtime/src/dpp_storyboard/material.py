from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MaterialConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    brand: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    image_path: str = Field(min_length=1)
    description: str = Field(min_length=1)
    details: dict[str, str] = Field(default_factory=dict)
    placement_guidance: str | None = None

    @field_validator("brand", "product_name", "image_path", "description", mode="before")
    @classmethod
    def _normalize_required_text(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("Text fields cannot be empty.")
        return normalized

    @field_validator("placement_guidance", mode="before")
    @classmethod
    def _normalize_optional_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        return normalized or None

    @field_validator("details", mode="before")
    @classmethod
    def _normalize_details(cls, value: Any) -> dict[str, str]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise TypeError("details must be an object of string values.")
        normalized: dict[str, str] = {}
        for key, item in value.items():
            if not isinstance(key, str) or not isinstance(item, str):
                raise TypeError("details must be an object of string values.")
            stripped_key = key.strip()
            stripped_value = item.strip()
            if stripped_key and stripped_value:
                normalized[stripped_key] = stripped_value
        return normalized

    def resolve_image_path(self, config_path: str | Path) -> Path:
        base_path = Path(config_path).expanduser().resolve().parent
        image_path = Path(self.image_path).expanduser()
        return image_path.resolve() if image_path.is_absolute() else (base_path / image_path).resolve()

    def to_prompt_block(self) -> str:
        lines = [
            f"品牌: {self.brand}",
            f"商品名: {self.product_name}",
            f"简介: {self.description}",
        ]
        for key, value in self.details.items():
            lines.append(f"{key}: {value}")
        if self.placement_guidance:
            lines.append(f"植入建议: {self.placement_guidance}")
        return "\n".join(lines)


def load_material_config(config_path: str | Path) -> MaterialConfig:
    path = Path(config_path).expanduser().resolve()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return MaterialConfig.model_validate(payload)
