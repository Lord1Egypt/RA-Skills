from __future__ import annotations

from typing import Dict, List

from app.models.news_item import NewsItem


class ClassifyService:
    """
    资讯分类服务。
    """

    def __init__(self) -> None:
        self.category_rules: Dict[str, List[str]] = {
            "融资": [
                "融资", "募资", "完成a轮", "完成b轮", "完成c轮", "天使轮", "种子轮",
                "pre-a", "series a", "series b", "series c", "funding", "raised",
                "financing", "investment round"
            ],
            "投资/并购": [
                "投资", "并购", "收购", "入股", "控股", "增资",
                "acquisition", "acquire", "investment", "invests", "merger", "m&a"
            ],
            "成立新企业": [
                "成立", "新设", "注册", "设立子公司", "成立子公司", "新公司",
                "subsidiary", "incorporated", "established", "set up"
            ],
            "产品发布": [
                "发布", "推出", "上线", "开源", "模型", "平台", "系统", "芯片",
                "launch", "launched", "unveiled", "introduced", "released", "model"
            ],
            "获得认证": [
                "认证", "批准", "获批", "通过认证", "ce", "fda", "iso", "approved",
                "certified", "approval", "clearance"
            ],
            "政策动态": [
                "政策", "法规", "监管", "法案", "战略", "指导意见", "框架",
                "policy", "regulation", "act", "framework", "guideline", "government"
            ],
            "行业大事件": [
                "行业", "大会", "峰会", "联盟", "基础设施", "算力", "数据中心",
                "industry", "summit", "alliance", "infrastructure", "datacenter"
            ],
        }

    def classify_item(self, item: NewsItem) -> NewsItem:
        """
        对单条资讯进行一级、二级分类。
        """
        text = self._build_text(item)

        level_2 = self._classify_level_2(text)
        level_1 = self._classify_level_1(item, level_2)

        item.category_level_1 = level_1
        item.category_level_2 = level_2

        return item

    def classify_items(self, items: List[NewsItem]) -> List[NewsItem]:
        """
        批量分类。
        """
        for item in items:
            self.classify_item(item)
        return items

    def _classify_level_2(self, text: str) -> str:
        """
        二级分类优先按关键词命中。
        """
        for category, keywords in self.category_rules.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return category

        return "企业重大动态"

    @staticmethod
    def _classify_level_1(item: NewsItem, level_2: str) -> str:
        """
        一级分类规则：
        1. 若 match_service 已根据企业名单国家/地区赋值，则直接保留
        2. 否则按兜底逻辑判断
        """
        if item.category_level_1:
            return item.category_level_1

        if level_2 in {"政策动态", "行业大事件"}:
            return "全球AI产业动态"

        if item.related_companies:
            return "名单企业动态"

        return "全球AI产业动态"

    @staticmethod
    def _build_text(item: NewsItem) -> str:
        parts = [
            item.title_zh or item.title or "",
            item.summary_zh or item.summary or "",
            item.cleaned_content_zh or item.cleaned_content or "",
            item.raw_content or "",
            item.source_name or "",
        ]
        return "\n".join(parts).lower()