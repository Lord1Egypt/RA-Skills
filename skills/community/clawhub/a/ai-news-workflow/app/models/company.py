from __future__ import annotations

from typing import List, Set

from pydantic import BaseModel, Field, field_validator


class Company(BaseModel):
    """
    企业基础信息模型。
    """

    company_cn: str = Field(..., description="企业中文名")
    company_en: str = Field(default="", description="企业英文名")
    short_name: str = Field(default="", description="企业简称")
    aliases: List[str] = Field(default_factory=list, description="企业别名列表")
    parent_company: str = Field(default="", description="母公司")
    country_region: str = Field(default="", description="国家/地区")
    is_key: bool = Field(default=True, description="是否重点关注")
    remarks: str = Field(default="", description="备注")

    @field_validator("company_cn")
    @classmethod
    def validate_company_cn(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("company_cn 不能为空")
        return value

    def all_names(self) -> List[str]:
        """
        返回企业所有名称字段。
        """
        values = [
            self.company_cn,
            self.company_en,
            self.short_name,
            self.parent_company,
            *self.aliases,
        ]
        return [v.strip() for v in values if isinstance(v, str) and v.strip()]

    def keyword_set(self) -> Set[str]:
        """
        返回企业匹配检索词集合。
        """
        return set(self.all_names())