from __future__ import annotations

from typing import List

from app.models.news_item import NewsItem


class GlobalKeyEventService:
    """
    从全球AI产业动态中筛选重点事件 Top N。
    """

    def __init__(self, top_n: int = 5) -> None:
        self.top_n = top_n

    def select_top_events(self, items: List[NewsItem]) -> List[NewsItem]:
        global_items = [
            x for x in items
            if (x.category_level_1 or "").strip() == "全球AI产业动态"
        ]

        if not global_items:
            return []

        def sort_key(x: NewsItem):
            flag = (x.global_key_event_flag or "").strip()
            score = x.global_key_event_score or 0
            # 先按“是/否”，再按分数降序，再按发布时间升序（更早优先）
            flag_sort = 0 if flag == "是" else 1
            publish_time = x.publish_time
            return (flag_sort, -score, publish_time or 0)

        selected = sorted(global_items, key=sort_key)

        # 如果模型标“是”的不足5条，仍按分数补足到5条
        return selected[: self.top_n]