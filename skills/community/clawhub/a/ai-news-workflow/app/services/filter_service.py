from __future__ import annotations

from typing import List, Tuple

from app.core.time_window import TimeWindow, get_event_date, normalize_to_shanghai
from app.models.news_item import NewsItem


class FilterService:
    """
    资讯过滤服务。
    """

    def __init__(self, min_title_length: int = 8, require_source_url: bool = True) -> None:
        self.min_title_length = min_title_length
        self.require_source_url = require_source_url

    def filter_items(
        self, items: List[NewsItem], window: TimeWindow
    ) -> Tuple[List[NewsItem], List[NewsItem]]:
        """
        返回：
        - valid_items: 通过过滤的资讯
        - invalid_items: 未通过过滤的资讯
        """
        valid_items: List[NewsItem] = []
        invalid_items: List[NewsItem] = []
        item.publish_time = normalize_to_shanghai(item.publish_time) if item.publish_time else item.publish_time
        for item in items:
            passed, reason = self.is_valid(item, window)

            item.window_start = window.start_time
            item.window_end = window.end_time

            if item.publish_time:
                item.publish_time = normalize_to_shanghai(item.publish_time)
                item.event_date = get_event_date(item.publish_time)

            if passed:
                item.entry_status = "included"
                if not item.remarks:
                    item.remarks = ""
                valid_items.append(item)
            else:
                item.entry_status = "excluded"
                item.remarks = reason
                invalid_items.append(item)

        return valid_items, invalid_items

    def is_valid(self, item: NewsItem, window: TimeWindow) -> Tuple[bool, str]:
        """
        判断单条资讯是否有效。
        """
        if not item.title or len(item.title.strip()) < self.min_title_length:
            return False, "标题过短或为空"

        if self.require_source_url and not item.source_url:
            return False, "缺少来源链接"

        if not item.publish_time:
            return False, "缺少发布时间"

        publish_time = normalize_to_shanghai(item.publish_time)
        if publish_time is None:
            return False, "发布时间无法解析"

        if not window.contains(publish_time):
            return False, "发布时间不在统计窗口内"

        return True, "有效"