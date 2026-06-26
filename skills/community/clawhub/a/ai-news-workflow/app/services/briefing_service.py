from __future__ import annotations

from typing import Dict, List, Optional

from app.models.news_item import NewsItem


class BriefingService:
    """
    简报生成服务（Word用）：
    只输出两大部分：
    1. “一带”AI领军企业动态
    2. 全球AI产业动态

    特点：
    - 不再对传入 items 做二次有效性筛选
    - 支持 global_items_override：可传入“全球AI产业动态重点事件Top5”
    - 全球AI产业动态内部默认按 国内 -> 国际 排序
    """

    def __init__(self, max_items_per_section: int = 999999) -> None:
        self.max_items_per_section = max_items_per_section

    def build_briefing(
        self,
        items: List[NewsItem],
        run_date: str,
        time_window: str = "",
        global_items_override: Optional[List[NewsItem]] = None,
    ) -> Dict:
        valid_items = list(items)
        valid_items = self._sort_items(valid_items)

        company_items: List[NewsItem] = []
        global_items: List[NewsItem] = []

        for item in valid_items:
            level1 = (item.category_level_1 or "").strip()

            if level1 == "名单企业动态":
                company_items.append(item)
            elif level1 == "全球AI产业动态":
                global_items.append(item)
            else:
                # 兜底：按国家/地区归类，防止一级类别脏值导致 Word 漏项
                country_region = (item.country_region or "").strip()
                if country_region == "中国":
                    company_items.append(item)
                else:
                    global_items.append(item)

        # 全球AI产业动态部分：
        # 若传入重点事件覆盖列表，则只用它；否则用全部全球AI产业动态
        if global_items_override is not None:
            global_items = list(global_items_override)

        company_items = self._sort_company_items(company_items)[: self.max_items_per_section]
        global_items = self._sort_global_items(global_items)[: self.max_items_per_section]

        return {
            "title": "每日AI产业资讯简报",
            "run_date": run_date,
            "time_window": time_window,
            "company_items": self._build_items(company_items),
            "global_items": self._build_items(global_items),
        }

    def _build_items(self, items: List[NewsItem]) -> List[Dict]:
        result: List[Dict] = []

        for item in items:
            result.append({
                "title": item.title_zh or item.title or "",
                "summary": self._item_summary_text(item),
                "source_name": item.source_name or "",
                "source_url": item.source_url or "",
                "global_region_label": item.global_region_label or "",
                "global_key_event_flag": item.global_key_event_flag or "",
                "global_key_event_score": item.global_key_event_score or 0,
                "global_key_event_reason": item.global_key_event_reason or "",
            })

        return result

    @staticmethod
    def _item_summary_text(item: NewsItem) -> str:
        parts: List[str] = []

        if item.related_companies:
            parts.append(f"关联企业：{'、'.join(item.related_companies)}。")

        # 全球AI产业动态可在摘要里带上国内/国际归属，帮助阅读(不再显示)
        #if (item.category_level_1 or "").strip() == "全球AI产业动态":
        #    if (item.global_region_label or "").strip() in {"国内", "国际"}:
        #        parts.append(f"机构归属：{item.global_region_label}。")

        summary_text = (item.summary_zh or item.summary or "").strip()
        if summary_text:
            parts.append(summary_text)

#        if item.source_name:
#            parts.append(f"来源：{item.source_name}。")

        return " ".join(parts).strip()

    def _sort_company_items(self, items: List[NewsItem]) -> List[NewsItem]:
        importance_order = {"高": 0, "中": 1, "低": 2, None: 3, "": 3}

        def sort_key(x: NewsItem):
            return (
                importance_order.get(x.importance, 3),
                self._publish_sort_value(x),
                x.title_zh or x.title or "",
            )

        return sorted(items, key=sort_key)

    def _sort_global_items(self, items: List[NewsItem]) -> List[NewsItem]:
        importance_order = {"高": 0, "中": 1, "低": 2, None: 3, "": 3}

        def region_sort(x: NewsItem) -> int:
            label = (x.global_region_label or "").strip()
            if label == "国内":
                return 0
            if label == "国际":
                return 1
            return 2

        def key_event_sort(x: NewsItem) -> int:
            # 重点事件优先
            return 0 if (x.global_key_event_flag or "").strip() == "是" else 1

        def score_sort(x: NewsItem) -> int:
            # 分数高的排前面，所以这里取负值
            score = x.global_key_event_score or 0
            return -score

        def sort_key(x: NewsItem):
            return (
                region_sort(x),                     # 国内在前，国际在后
                key_event_sort(x),                  # 标记为重点事件的在前
                score_sort(x),                      # 分数高的在前
                importance_order.get(x.importance, 3),
                self._publish_sort_value(x),
                x.title_zh or x.title or "",
            )

        return sorted(items, key=sort_key)

    @staticmethod
    def _publish_sort_value(item: NewsItem):
        """
        让更早的发布时间在前（与你现在“保留最早”逻辑一致）。
        若无发布时间，则排后。
        """
        return item.publish_time or "9999-12-31 23:59:59"

    @staticmethod
    def _sort_items(items: List[NewsItem]) -> List[NewsItem]:
        """
        总体排序：
        1. 名单企业动态在前
        2. 全球AI产业动态在后
        """
        def level1_sort(x: NewsItem) -> int:
            level1 = (x.category_level_1 or "").strip()
            if level1 == "名单企业动态":
                return 0
            if level1 == "全球AI产业动态":
                return 1
            return 2

        def sort_key(x: NewsItem):
            return (
                level1_sort(x),
                x.title_zh or x.title or "",
            )

        return sorted(items, key=sort_key)