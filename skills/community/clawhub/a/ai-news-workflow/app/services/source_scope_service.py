from __future__ import annotations

from typing import Dict, List, Tuple

from app.models.company import Company
from app.models.news_item import NewsItem


class SourceScopeService:
    """
    来源地区约束服务。

    规则：
    - 若来源地区 = 国内
      只保留命中“企业名单中国家/地区=中国”的企业资讯
    - 若来源地区 = 国际
      不做这个限定
    """

    def __init__(self, companies: List[Company]) -> None:
        self.company_map: Dict[str, Company] = {c.company_cn: c for c in companies}

    def filter_items(self, items: List[NewsItem]) -> Tuple[List[NewsItem], List[NewsItem]]:
        kept_items: List[NewsItem] = []
        dropped_items: List[NewsItem] = []

        for item in items:
            passed, reason = self.is_allowed(item)

            if passed:
                kept_items.append(item)
            else:
                item.entry_status = "excluded"
                item.remarks = self._append_remark(item.remarks, reason)
                dropped_items.append(item)

        return kept_items, dropped_items

    def is_allowed(self, item: NewsItem) -> Tuple[bool, str]:
        source_region = (item.source_region_scope or "").strip()

        # 国际来源：不做“中国企业限定”
        if source_region != "国内":
            return True, "国际来源不过滤"

        # 国内来源：必须命中中国企业
        if not item.related_companies:
            return False, "国内来源未命中中国企业"

        matched_companies = [
            self.company_map[name]
            for name in item.related_companies
            if name in self.company_map
        ]

        if any(self._is_china_company(c.country_region) for c in matched_companies):
            return True, "国内来源且命中中国企业"

        return False, "国内来源仅保留中国企业匹配资讯"

    @staticmethod
    def _is_china_company(country_region: str | None) -> bool:
        value = (country_region or "").strip().lower()
        return value in {"中国", "china", "cn", "中国大陆"}

    @staticmethod
    def _append_remark(existing: str | None, new_text: str) -> str:
        if not existing:
            return new_text
        return f"{existing}；{new_text}"