from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class NewsItem(BaseModel):
    """
    表示一条经过抓取、清洗、翻译、筛选后的资讯记录。
    """

    # 基础标识
    item_id: Optional[str] = Field(default=None, description="资讯唯一ID，可由程序生成")
    run_date: Optional[str] = Field(default=None, description="本次任务执行日期，格式 YYYY-MM-DD")

    # 时间字段
    event_date: Optional[str] = Field(default=None, description="资讯归属日期，格式 YYYY-MM-DD")
    publish_time: Optional[datetime] = Field(default=None, description="来源页面发布时间")
    crawl_time: Optional[datetime] = Field(default=None, description="程序抓取时间")

    # 时间窗口记录
    window_start: Optional[datetime] = Field(default=None, description="统计窗口起始时间")
    window_end: Optional[datetime] = Field(default=None, description="统计窗口结束时间")

    # 分类字段
    category_level_1: Optional[str] = Field(default=None, description="一级类别")
    category_level_2: Optional[str] = Field(default=None, description="二级类别")
    global_region_label: Optional[str] = Field(default=None, description="全球AI产业动态机构归属:国内/国际/不适用")
    global_key_event_flag: Optional[str] = Field(default=None, description="全球AI产业动态是否为重点事件：是/否/不适用")
    global_key_event_score: Optional[int] = Field(default=None, description="全球AI产业动态重点事件评分，0-100")
    global_key_event_reason: Optional[str] = Field(default=None, description="全球AI产业动态重点事件判断理由")
    
    # 关联信息
    related_companies: List[str] = Field(default_factory=list, description="关联企业列表")
    country_region: Optional[str] = Field(default=None, description="国家或地区")

    # 主内容字段（当前主流程默认使用中文字段覆盖写入）
    title: str = Field(..., description="当前主标题（建议为中文）")
    summary: Optional[str] = Field(default=None, description="当前主摘要（建议为中文）")
    key_points: Optional[str] = Field(default=None, description="事件要点")
    raw_content: Optional[str] = Field(default=None, description="原始正文")
    cleaned_content: Optional[str] = Field(default=None, description="清洗后的正文（建议为中文）")

    # 原文字段
    original_title: Optional[str] = Field(default=None, description="原始标题")
    original_summary: Optional[str] = Field(default=None, description="原始摘要")
    original_cleaned_content: Optional[str] = Field(default=None, description="原始清洗后正文")
    original_language: Optional[str] = Field(default=None, description="原始语言，如 zh/en")

    # 中文标准字段
    title_zh: Optional[str] = Field(default=None, description="中文标题")
    summary_zh: Optional[str] = Field(default=None, description="中文摘要")
    cleaned_content_zh: Optional[str] = Field(default=None, description="中文正文")

    # 翻译标记
    is_machine_translated: bool = Field(default=False, description="是否机器翻译")
    translation_backend: Optional[str] = Field(default=None, description="翻译后端标识")

    # 来源字段
    source_name: str = Field(..., description="来源名称")
    source_url: str = Field(..., description="来源链接")
    source_type: Optional[str] = Field(default=None, description="来源类型，如 official/media/government")
    source_region_scope: Optional[str] = Field(default=None, description="来源地区范围，如 国内/国际")
    is_official: bool = Field(default=False, description="是否官方来源")

    # 处理标记
    importance: Optional[str] = Field(default=None, description="重要性等级：高/中/低")
    dedup_status: Optional[str] = Field(default="unique", description="去重状态")
    entry_status: Optional[str] = Field(default="pending", description="入表状态：pending/included/manual_review/excluded")
    language: Optional[str] = Field(default=None, description="兼容旧字段")
    remarks: Optional[str] = Field(default=None, description="备注")

    # 技术字段
    normalized_title: Optional[str] = Field(default=None, description="规范化标题（建议为中文）")
    content_hash: Optional[str] = Field(default=None, description="正文哈希（建议基于中文字段）")
    matched_keywords: List[str] = Field(default_factory=list, description="命中的关键词")
    extra_data: dict = Field(default_factory=dict, description="扩展字段")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title 不能为空")
        return value

    @field_validator("source_name")
    @classmethod
    def validate_source_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("source_name 不能为空")
        return value

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("source_url 不能为空")
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("source_url 必须以 http:// 或 https:// 开头")
        return value

    @field_validator("importance")
    @classmethod
    def validate_importance(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"高", "中", "低"}
        if value not in allowed:
            raise ValueError(f"importance 必须属于 {allowed}")
        return value

    @field_validator("entry_status")
    @classmethod
    def validate_entry_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"pending", "included", "manual_review", "excluded"}
        if value not in allowed:
            raise ValueError(f"entry_status 必须属于 {allowed}")
        return value

    def to_excel_row(self) -> dict:
        """
        转换为 Excel 输出所需的一行字典。
        默认优先展示中文字段。
        """
        display_title = self.title_zh or self.title or ""
        display_summary = self.summary_zh or self.summary or ""
        display_content = self.cleaned_content_zh or self.cleaned_content or ""
        display_key_points = self.key_points or display_summary

        return {
            "资讯日期": self.event_date or "",
            "抓取日期": self.run_date or "",
            "时间窗口": self.get_window_text(),
            "一级类别": self.category_level_1 or "",
            "二级类别": self.category_level_2 or "",
            "关联企业": "；".join(self.related_companies) if self.related_companies else "",
            "国家/地区": self.country_region or "",
            "标题": display_title,
            "摘要": display_summary,
            "事件要点": display_key_points,
            "来源名称": self.source_name,
            "来源链接": self.source_url,
            "发布时间": self.format_dt(self.publish_time),
            "抓取时间": self.format_dt(self.crawl_time),
            "是否官方来源": "是" if self.is_official else "否",
            "重要性等级": self.importance or "",
            "去重标记": self.dedup_status or "",
            "入表状态": self.entry_status or "",
            "备注": self.remarks or "",
            "原始语言": self.original_language or "",
            "原始标题": self.original_title or "",
            "中文标题": self.title_zh or "",
            "中文摘要": self.summary_zh or "",
            "是否机器翻译": "是" if self.is_machine_translated else "否",
            "翻译后端": self.translation_backend or "",
        }

    def get_window_text(self) -> str:
        start_text = self.format_dt(self.window_start)
        end_text = self.format_dt(self.window_end)
        if start_text and end_text:
            return f"{start_text} ~ {end_text}"
        return ""

    @staticmethod
    def format_dt(value: Optional[datetime]) -> str:
        if value is None:
            return ""
        return value.strftime("%Y-%m-%d %H:%M:%S")