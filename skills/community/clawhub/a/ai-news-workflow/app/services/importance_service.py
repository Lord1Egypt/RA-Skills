from __future__ import annotations

from typing import Dict, List

from app.models.news_item import NewsItem


class ImportanceService:
    """
    资讯重要性评分服务。
    """

    def __init__(self) -> None:
        self.high_keywords: List[str] = [
            "融资", "并购", "收购", "重大", "发布", "新模型", "法案", "监管", "战略",
            "funding", "raised", "acquisition", "merger", "launch", "released",
            "regulation", "policy", "approval"
        ]

        self.medium_keywords: List[str] = [
            "合作", "认证", "设立", "成立子公司", "投资", "产品", "平台",
            "partnership", "certification", "approved", "investment", "introduced"
        ]

        self.high_categories = {"融资", "投资/并购", "政策动态"}
        self.medium_categories = {"成立新企业", "产品发布", "获得认证", "企业重大动态"}

    def score_item(self, item: NewsItem) -> NewsItem:
        text = self._build_text(item)

        # 一级规则：按二级分类先给基础等级
        if item.category_level_2 in self.high_categories:
            item.importance = "高"
            return item

        if item.category_level_2 in self.medium_categories:
            item.importance = "中"
            return item

        # 二级规则：按关键词命中
        if self._contains_any(text, self.high_keywords):
            item.importance = "高"
            return item

        if self._contains_any(text, self.medium_keywords):
            item.importance = "中"
            return item

        item.importance = "低"
        return item

    def score_items(self, items: List[NewsItem]) -> List[NewsItem]:
        for item in items:
            self.score_item(item)
        return items

    @staticmethod
    def _contains_any(text: str, keywords: List[str]) -> bool:
        for keyword in keywords:
            if keyword.lower() in text:
                return True
        return False

    @staticmethod
    def _build_text(item: NewsItem) -> str:
        parts = [
            item.title or "",
            item.summary or "",
            item.cleaned_content or "",
            item.raw_content or "",
            item.category_level_1 or "",
            item.category_level_2 or "",
        ]
        return "\n".join(parts).lower()