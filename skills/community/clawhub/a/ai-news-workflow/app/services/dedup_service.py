from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

from rapidfuzz import fuzz

from app.models.news_item import NewsItem
from app.utils.text_utils import (
    contains_financing_signal,
    contains_policy_signal,
    contains_product_signal,
    jaccard_similarity,
    normalize_title,
    tokenize_text,
)
from app.utils.url_utils import normalize_url


class DedupService:
    """
    资讯去重服务（保留最早发布时间版）。
    去重顺序：
    1. URL
    2. 内容哈希
    3. 标题相似度
    4. 事件相似度

    规则：
    - 若两条重复，保留 publish_time 更早的那条
    """

    def __init__(
        self,
        title_similarity_threshold: int = 90,
        event_similarity_threshold: float = 0.72,
    ) -> None:
        self.title_similarity_threshold = title_similarity_threshold
        self.event_similarity_threshold = event_similarity_threshold

    def dedup_items(self, items: List[NewsItem]) -> Tuple[List[NewsItem], List[NewsItem]]:
        if not items:
            return [], []

        # 先统一标题
        for item in items:
            item.normalized_title = normalize_title(item.title)

        # 先按发布时间升序，尽量让最早的先进入
        items_sorted = sorted(items, key=self._sort_key_by_time)

        unique_items: List[NewsItem] = []
        duplicate_items: List[NewsItem] = []

        kept_items: List[NewsItem] = []
        url_map: Dict[str, NewsItem] = {}
        hash_map: Dict[str, NewsItem] = {}
        title_map: Dict[str, NewsItem] = {}

        for item in items_sorted:
            replaced = False

            # 1) URL 去重
            url = normalize_url(item.source_url)
            if url:
                kept = url_map.get(url)
                if kept:
                    winner, loser = self._pick_earlier_item(kept, item)
                    if winner is item:
                        self._replace_kept_item(kept_items, kept, item)
                        url_map[url] = item
                        self._mark_duplicate(loser, "duplicate_url", f"URL重复，保留更早发布时间：{item.title[:80]}")
                        duplicate_items.append(loser)
                    else:
                        self._mark_duplicate(item, "duplicate_url", f"URL重复，保留更早发布时间：{kept.title[:80]}")
                        duplicate_items.append(item)
                    continue

            # 2) 内容哈希去重
            if item.content_hash:
                kept = hash_map.get(item.content_hash)
                if kept:
                    winner, loser = self._pick_earlier_item(kept, item)
                    if winner is item:
                        self._replace_kept_item(kept_items, kept, item)
                        hash_map[item.content_hash] = item
                        self._mark_duplicate(loser, "duplicate_hash", f"内容哈希重复，保留更早发布时间：{item.title[:80]}")
                        duplicate_items.append(loser)
                    else:
                        self._mark_duplicate(item, "duplicate_hash", f"内容哈希重复，保留更早发布时间：{kept.title[:80]}")
                        duplicate_items.append(item)
                    continue

            # 3) 标题相似度去重
            dup_title = self._find_similar_title(item, title_map)
            if dup_title is not None:
                winner, loser = self._pick_earlier_item(dup_title, item)
                if winner is item:
                    self._replace_kept_item(kept_items, dup_title, item)
                    # title_map 里把旧标题删掉，再写新标题
                    old_key = dup_title.normalized_title or ""
                    if old_key in title_map:
                        del title_map[old_key]
                    title_map[item.normalized_title or ""] = item
                    self._mark_duplicate(loser, "duplicate_title", f"标题相似重复，保留更早发布时间：{item.title[:80]}")
                    duplicate_items.append(loser)
                else:
                    self._mark_duplicate(item, "duplicate_title", f"标题相似重复，保留更早发布时间：{dup_title.title[:80]}")
                    duplicate_items.append(item)
                continue

            # 4) 事件相似度去重
            dup_event = self._find_similar_event(item, kept_items)
            if dup_event is not None:
                winner, loser = self._pick_earlier_item(dup_event, item)
                if winner is item:
                    self._replace_kept_item(kept_items, dup_event, item)
                    # 可能需要同步更新 url/hash/title map
                    self._rebuild_maps(kept_items, url_map, hash_map, title_map)
                    self._mark_duplicate(loser, "duplicate_event", f"疑似同事件重复，保留更早发布时间：{item.title[:80]}")
                    duplicate_items.append(loser)
                else:
                    self._mark_duplicate(item, "duplicate_event", f"疑似同事件重复，保留更早发布时间：{dup_event.title[:80]}")
                    duplicate_items.append(item)
                continue

            # 保留
            item.dedup_status = "unique"
            unique_items.append(item)
            kept_items.append(item)

            if url:
                url_map[url] = item
            if item.content_hash:
                hash_map[item.content_hash] = item
            if item.normalized_title:
                title_map[item.normalized_title] = item

        # unique_items 重新对齐 kept_items
        unique_items = kept_items
        return unique_items, duplicate_items

    def _find_similar_title(self, item: NewsItem, title_map: Dict[str, NewsItem]) -> Optional[NewsItem]:
        current_title = item.normalized_title or ""
        if not current_title:
            return None

        for kept_title, kept_item in title_map.items():
            if not kept_title:
                continue

            score = fuzz.ratio(current_title, kept_title)
            if score >= self.title_similarity_threshold:
                return kept_item

        return None

    def _find_similar_event(self, item: NewsItem, kept_items: List[NewsItem]) -> Optional[NewsItem]:
        current_text = self._build_event_text(item)
        current_tokens = tokenize_text(current_text)

        if not current_tokens:
            return None

        for kept_item in kept_items:
            company_overlap = self._has_company_overlap(item, kept_item)
            same_category = (
                (item.category_level_2 or "") == (kept_item.category_level_2 or "")
                and bool(item.category_level_2)
            )

            kept_text = self._build_event_text(kept_item)
            kept_tokens = tokenize_text(kept_text)
            sim = jaccard_similarity(current_tokens, kept_tokens)

            if company_overlap and same_category and sim >= self.event_similarity_threshold:
                return kept_item

            if company_overlap and self._both_financing(item, kept_item) and sim >= 0.55:
                return kept_item

            if company_overlap and self._both_product(item, kept_item) and sim >= 0.58:
                return kept_item

            if self._both_policy(item, kept_item) and sim >= 0.68:
                return kept_item

        return None

    @staticmethod
    def _build_event_text(item: NewsItem) -> str:
        parts = [
            item.title or "",
            item.summary or "",
            item.category_level_2 or "",
            " ".join(item.related_companies) if item.related_companies else "",
        ]
        return " ".join(parts)

    @staticmethod
    def _has_company_overlap(a: NewsItem, b: NewsItem) -> bool:
        set_a = set(a.related_companies or [])
        set_b = set(b.related_companies or [])
        if not set_a or not set_b:
            return False
        return bool(set_a & set_b)

    @staticmethod
    def _both_financing(a: NewsItem, b: NewsItem) -> bool:
        ta = f"{a.title or ''} {a.summary or ''}"
        tb = f"{b.title or ''} {b.summary or ''}"
        return contains_financing_signal(ta) and contains_financing_signal(tb)

    @staticmethod
    def _both_product(a: NewsItem, b: NewsItem) -> bool:
        ta = f"{a.title or ''} {a.summary or ''}"
        tb = f"{b.title or ''} {b.summary or ''}"
        return contains_product_signal(ta) and contains_product_signal(tb)

    @staticmethod
    def _both_policy(a: NewsItem, b: NewsItem) -> bool:
        ta = f"{a.title or ''} {a.summary or ''}"
        tb = f"{b.title or ''} {b.summary or ''}"
        return contains_policy_signal(ta) and contains_policy_signal(tb)

    @staticmethod
    def _sort_key_by_time(item: NewsItem):
        dt = item.publish_time
        if dt is None:
            return (1, datetime.max.replace(year=2099))
        return (0, dt)

    @staticmethod
    def _pick_earlier_item(a: NewsItem, b: NewsItem) -> Tuple[NewsItem, NewsItem]:
        a_time = a.publish_time
        b_time = b.publish_time

        if a_time and b_time:
            return (a, b) if a_time <= b_time else (b, a)

        if a_time and not b_time:
            return a, b

        if b_time and not a_time:
            return b, a

        # 都没有发布时间，则保留原来的 a
        return a, b

    @staticmethod
    def _replace_kept_item(kept_items: List[NewsItem], old_item: NewsItem, new_item: NewsItem) -> None:
        for idx, item in enumerate(kept_items):
            if item is old_item:
                kept_items[idx] = new_item
                return

    @staticmethod
    def _mark_duplicate(item: NewsItem, status: str, remark: str) -> None:
        item.dedup_status = status
        item.entry_status = "excluded"
        item.remarks = remark

    @staticmethod
    def _rebuild_maps(
        kept_items: List[NewsItem],
        url_map: Dict[str, NewsItem],
        hash_map: Dict[str, NewsItem],
        title_map: Dict[str, NewsItem],
    ) -> None:
        url_map.clear()
        hash_map.clear()
        title_map.clear()

        for item in kept_items:
            url = normalize_url(item.source_url)
            if url:
                url_map[url] = item
            if item.content_hash:
                hash_map[item.content_hash] = item
            if item.normalized_title:
                title_map[item.normalized_title] = item