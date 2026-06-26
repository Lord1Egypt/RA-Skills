from __future__ import annotations

import re
from typing import Dict, List, Set

from app.models.company import Company
from app.models.news_item import NewsItem


class MatchService:
    """
    企业匹配服务（增强版）。
    特点：
    1. 中文全称/英文全称优先
    2. 过滤高风险短别名
    3. 英文使用单词边界匹配，避免子串误伤
    4. 根据企业名单国家/地区，给 item 写入：
       - related_companies
       - country_region
       - category_level_1
    """

    def __init__(self, companies: List[Company]) -> None:
        self.companies = companies
        self.company_map: Dict[str, Company] = {c.company_cn: c for c in companies}

    def match_item(self, item: NewsItem) -> NewsItem:
        matched_companies = self.find_company_objects(item)
        matched_names = [c.company_cn for c in matched_companies]

        item.related_companies = matched_names

        if matched_companies:
            if any(self._is_china_company(c) for c in matched_companies):
                item.country_region = "中国"
                item.category_level_1 = "名单企业动态"
            else:
                item.country_region = "国际"
                item.category_level_1 = "全球AI产业动态"

        return item

    def match_items(self, items: List[NewsItem]) -> List[NewsItem]:
        for item in items:
            self.match_item(item)
        return items

    def find_company_objects(self, item: NewsItem) -> List[Company]:
        text_parts = [
            item.title_zh or item.title or "",
            item.summary_zh or item.summary or "",
            item.cleaned_content_zh or item.cleaned_content or "",
            item.raw_content or "",
        ]
        full_text = "\n".join(text_parts)
        full_text_lower = full_text.lower()

        matched_companies: List[Company] = []
        seen: Set[str] = set()

        for company in self.companies:
            if self._match_company(full_text, full_text_lower, company):
                if company.company_cn not in seen:
                    matched_companies.append(company)
                    seen.add(company.company_cn)

        return matched_companies

    def _match_company(self, full_text: str, full_text_lower: str, company: Company) -> bool:
        """
        匹配顺序：
        1. 中文全称
        2. 英文全称
        3. 中文简称/别名（过滤短词）
        4. 英文简称/别名（单词边界）
        """

        # 1) 中文全称：强匹配
        if company.company_cn and self._match_chinese_phrase(full_text, company.company_cn):
            return True

        # 2) 英文全称：强匹配
        if company.company_en and self._match_english_phrase(full_text_lower, company.company_en.lower()):
            return True

        # 3) 中文简称 + 中文别名：中匹配（过滤短词）
        zh_candidates = self._get_chinese_aliases(company)
        for kw in zh_candidates:
            if self._is_safe_chinese_keyword(kw) and self._match_chinese_phrase(full_text, kw):
                return True

        # 4) 英文简称 + 英文别名：中匹配（过滤短词 + 单词边界）
        en_candidates = self._get_english_aliases(company)
        for kw in en_candidates:
            kw_lower = kw.lower()
            if self._is_safe_english_keyword(kw_lower) and self._match_english_phrase(full_text_lower, kw_lower):
                return True

        return False

    @staticmethod
    def _get_chinese_aliases(company: Company) -> List[str]:
        values = [company.short_name, *company.aliases]
        result = []
        for v in values:
            v = (v or "").strip()
            if v and MatchService._contains_chinese(v):
                result.append(v)
        return list(dict.fromkeys(result))

    @staticmethod
    def _get_english_aliases(company: Company) -> List[str]:
        values = [company.short_name, *company.aliases, company.parent_company]
        result = []
        for v in values:
            v = (v or "").strip()
            if v and not MatchService._contains_chinese(v):
                result.append(v)
        return list(dict.fromkeys(result))

    @staticmethod
    def _contains_chinese(text: str) -> bool:
        return any("\u4e00" <= ch <= "\u9fff" for ch in text)

    @staticmethod
    def _is_safe_chinese_keyword(keyword: str) -> bool:
        """
        中文关键词安全阈值：
        - 长度至少 3
        - 避免单字/双字通用词误伤
        """
        keyword = keyword.strip()
        if len(keyword) < 3:
            return False
        return True

    @staticmethod
    def _is_safe_english_keyword(keyword: str) -> bool:
        """
        英文关键词安全阈值：
        - 长度至少 4
        """
        keyword = keyword.strip()
        if len(keyword) < 4:
            return False
        return True

    @staticmethod
    def _match_chinese_phrase(text: str, keyword: str) -> bool:
        """
        中文短语匹配：
        当前先做严格包含，但前提是 keyword 已通过长度过滤。
        """
        keyword = keyword.strip()
        if not keyword:
            return False
        return keyword in text

    @staticmethod
    def _match_english_phrase(text_lower: str, keyword_lower: str) -> bool:
        """
        英文短语匹配：使用单词边界，避免子串误伤
        """
        keyword_lower = keyword_lower.strip()
        if not keyword_lower:
            return False

        pattern = r"\b" + re.escape(keyword_lower) + r"\b"
        return re.search(pattern, text_lower) is not None

    @staticmethod
    def _is_china_company(company: Company) -> bool:
        value = (company.country_region or "").strip().lower()
        return value in {"中国", "china", "cn", "中国大陆"}