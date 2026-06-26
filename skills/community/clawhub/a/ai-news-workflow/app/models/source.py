from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class Source(BaseModel):
    """
    资讯来源配置模型。
    """

    source_name: str = Field(..., description="来源名称")
    source_type: str = Field(default="other", description="来源类型，如 official/media/government/rss")
    url: str = Field(..., description="来源网址或入口")
    coverage: str = Field(default="", description="覆盖范围")
    priority: int = Field(default=5, description="优先级，数字越小越高")
    enabled: bool = Field(default=True, description="是否启用")
    fetch_method: str = Field(default="webpage", description="抓取方式，如 rss/webpage/api")
    region_scope: str = Field(default="", description="来源地区范围，如 国内/国际")

    @field_validator("source_name")
    @classmethod
    def validate_source_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("source_name 不能为空")
        return value

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("url 不能为空")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: int) -> int:
        if value < 1:
            return 1
        return value