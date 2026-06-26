from __future__ import annotations

from typing import List, Tuple

from app.models.news_item import NewsItem


class RelevanceService:
    """
    相关性筛选服务：
    过滤掉中文综合媒体中的无关资讯。
    """

    def __init__(self) -> None:
        self.ai_keywords = {
            "人工智能", "ai", "大模型", "生成式ai", "生成式人工智能", "机器学习", "深度学习",
            "多模态", "智能体", "算力", "智算", "模型训练", "ai芯片", "智能驾驶",
            "llm", "foundation model", "model", "agent"
        }

        self.event_keywords = {
            "融资", "募资", "天使轮", "种子轮", "a轮", "b轮", "c轮",
            "投资", "并购", "收购", "入股", "增资",
            "成立", "新设", "注册", "子公司", "设立",
            "发布", "推出", "上线", "开源", "模型", "平台", "系统", "芯片",
            "认证", "获批", "批准", "通过认证", "ce", "fda", "iso",
            "政策", "法规", "监管", "法案", "战略", "框架", "guideline",
            "funding", "raised", "investment", "acquisition", "launch",
            "released", "approved", "policy", "regulation"
        }

        self.important_ai_companies = {
            "openai", "anthropic", "英伟达", "nvidia", "google", "deepmind",
            "meta", "xai", "mistral", "cohere", "microsoft", "微软",
            "亚马逊", "amazon", "oracle", "amd", "intel"
        }

    def filter_items(self, items: List[NewsItem]) -> Tuple[List[NewsItem], List[NewsItem]]:
        relevant_items = []
        irrelevant_items = []

        for item in items:
            passed, reason = self.is_relevant(item)
            if passed:
                relevant_items.append(item)
            else:
                item.entry_status = "excluded"
                item.remarks = self._append_remark(item.remarks, reason)
                irrelevant_items.append(item)

        return relevant_items, irrelevant_items

    def is_relevant(self, item: NewsItem) -> Tuple[bool, str]:
        text = self._build_text(item)

        has_ai_signal = self._contains_any(text, self.ai_keywords)
        has_event_signal = self._contains_any(text, self.event_keywords)
        has_target_company = bool(item.related_companies)
        has_important_ai_company = self._contains_any(text, self.important_ai_companies)

        # 规则1：名单企业 + 事件
        if has_target_company and has_event_signal:
            return True, "名单企业相关"

        # 规则2：AI主题 + 事件
        if has_ai_signal and has_event_signal:
            return True, "AI主题相关"

        # 规则3：重点AI公司 + 事件
        if has_important_ai_company and has_event_signal:
            return True, "重点AI企业相关"

        # 规则4：政策动态直接放行（前提是分类已判定）
        if item.category_level_2 == "政策动态":
            return True, "政策动态"

        # 规则5：行业大事件直接放行（前提是分类已判定）
        if item.category_level_2 == "行业大事件":
            return True, "行业大事件"

        return False, "与AI关注范围不匹配"

    @staticmethod
    def _build_text(item: NewsItem) -> str:
        parts = [
            item.title_zh or item.title or "",
            item.summary_zh or item.summary or "",
            item.cleaned_content_zh or item.cleaned_content or "",
            item.category_level_1 or "",
            item.category_level_2 or "",
            " ".join(item.related_companies) if item.related_companies else "",
        ]
        return "\n".join(parts).lower()

    @staticmethod
    def _contains_any(text: str, keywords: set[str]) -> bool:
        for kw in keywords:
            if kw.lower() in text:
                return True
        return False

    @staticmethod
    def _append_remark(existing: str | None, new_text: str) -> str:
        if not existing:
            return new_text
        return f"{existing}；{new_text}"