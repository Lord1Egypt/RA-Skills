from __future__ import annotations

from typing import List, Optional

from rapidfuzz import fuzz

from app.core.database import DatabaseManager
from app.models.news_item import NewsItem
from app.utils.text_utils import normalize_title
from app.utils.url_utils import normalize_url


class NewsRepository:
    """
    资讯历史库访问层（增强版：支持数据库级近似标题查重）。
    """

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def exists_by_url(self, source_url: str) -> bool:
        normalized_url = normalize_url(source_url)
        if not normalized_url:
            return False

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM news_history WHERE source_url = ? LIMIT 1",
                (normalized_url,),
            )
            return cursor.fetchone() is not None

    def exists_by_hash(self, content_hash: str | None) -> bool:
        if not content_hash:
            return False

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM news_history WHERE content_hash = ? LIMIT 1",
                (content_hash,),
            )
            return cursor.fetchone() is not None

    def exists_by_normalized_title(self, normalized_title: str | None) -> bool:
        if not normalized_title:
            return False

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM news_history WHERE normalized_title = ? LIMIT 1",
                (normalized_title,),
            )
            return cursor.fetchone() is not None

    def find_similar_title_in_db(
        self,
        normalized_title: str | None,
        threshold: int = 92,
        recent_days: int = 30,
        category_level_2: str | None = None,
    ) -> Optional[dict]:
        """
        在数据库中查找近似标题。
        返回匹配到的历史记录 dict；找不到则返回 None。
        """
        if not normalized_title:
            return None

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            if category_level_2:
                cursor.execute(
                    """
                    SELECT id, title, normalized_title, source_url, category_level_2, created_at
                    FROM news_history
                    WHERE created_at >= datetime('now', ?)
                      AND category_level_2 = ?
                      AND normalized_title IS NOT NULL
                      AND normalized_title != ''
                    ORDER BY created_at DESC
                    """,
                    (f"-{recent_days} days", category_level_2),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, title, normalized_title, source_url, category_level_2, created_at
                    FROM news_history
                    WHERE created_at >= datetime('now', ?)
                      AND normalized_title IS NOT NULL
                      AND normalized_title != ''
                    ORDER BY created_at DESC
                    """,
                    (f"-{recent_days} days",),
                )

            rows = cursor.fetchall()

        best_match = None
        best_score = 0

        for row in rows:
            hist_title = row["normalized_title"] or ""
            if not hist_title:
                continue

            score = fuzz.ratio(normalized_title, hist_title)
            if score >= threshold and score > best_score:
                best_score = score
                best_match = {
                    "id": row["id"],
                    "title": row["title"],
                    "normalized_title": row["normalized_title"],
                    "source_url": row["source_url"],
                    "category_level_2": row["category_level_2"],
                    "created_at": row["created_at"],
                    "score": score,
                }

        return best_match

    def save_item(self, item: NewsItem) -> None:
        normalized_url = normalize_url(item.source_url)
        normalized_title = item.normalized_title or normalize_title(item.title)

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO news_history (
                    title,
                    normalized_title,
                    source_name,
                    source_url,
                    publish_time,
                    related_companies,
                    category_level_1,
                    category_level_2,
                    content_hash,
                    importance
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.title,
                    normalized_title,
                    item.source_name,
                    normalized_url,
                    item.format_dt(item.publish_time),
                    "；".join(item.related_companies) if item.related_companies else "",
                    item.category_level_1,
                    item.category_level_2,
                    item.content_hash,
                    item.importance,
                ),
            )
            conn.commit()

    def save_items(self, items: List[NewsItem]) -> None:
        for item in items:
            self.save_item_prefer_earliest(item)

    def filter_existing(self, items: List[NewsItem]) -> List[NewsItem]:
        """
        兼容旧接口：只按 URL 过滤。
        """
        result: List[NewsItem] = []

        for item in items:
            if self.exists_by_url(item.source_url):
                item.entry_status = "excluded"
                item.dedup_status = "duplicate_url"
                item.remarks = self._append_remark(item.remarks, "数据库已存在同URL记录")
                continue
            result.append(item)

        return result

    def filter_existing_advanced(
        self,
        items: List[NewsItem],
        similar_title_threshold: int = 92,
        similar_title_recent_days: int = 30,
    ) -> List[NewsItem]:
        """
        按 URL + content_hash + normalized_title + 近似标题 多条件过滤历史重复。
        """
        result: List[NewsItem] = []

        for item in items:
            normalized_title = item.normalized_title or normalize_title(item.title)
            item.normalized_title = normalized_title

            if self.exists_by_url(item.source_url):
                item.entry_status = "excluded"
                item.dedup_status = "duplicate_db_url"
                item.remarks = self._append_remark(item.remarks, "数据库已存在同URL记录")
                continue

            if self.exists_by_hash(item.content_hash):
                item.entry_status = "excluded"
                item.dedup_status = "duplicate_db_hash"
                item.remarks = self._append_remark(item.remarks, "数据库已存在同内容哈希记录")
                continue

            if self.exists_by_normalized_title(normalized_title):
                item.entry_status = "excluded"
                item.dedup_status = "duplicate_db_title"
                item.remarks = self._append_remark(item.remarks, "数据库已存在同规范化标题记录")
                continue

            similar_record = self.find_similar_title_in_db(
                normalized_title=normalized_title,
                threshold=similar_title_threshold,
                recent_days=similar_title_recent_days,
                category_level_2=item.category_level_2,
            )
            if similar_record:
                item.entry_status = "excluded"
                item.dedup_status = "duplicate_db_similar_title"
                item.remarks = self._append_remark(
                    item.remarks,
                    f"数据库近似标题重复（相似度={similar_record['score']}，参考标题：{similar_record['title'][:80]}）"
                )
                continue

            result.append(item)

        return result

    def save_item_prefer_earliest(self, item: NewsItem) -> None:
        normalized_url = normalize_url(item.source_url)
        normalized_title = item.normalized_title or normalize_title(item.title)

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            # 优先按 source_url 查
            existing = None
            if normalized_url:
                cursor.execute(
                    """
                    SELECT id, publish_time
                    FROM news_history
                    WHERE source_url = ?
                    LIMIT 1
                    """,
                    (normalized_url,),
                )
                existing = cursor.fetchone()

            if existing:
                existing_publish_time = existing["publish_time"] or ""
                current_publish_time = item.format_dt(item.publish_time)

                # 当前更早，则更新
                if current_publish_time and (not existing_publish_time or current_publish_time < existing_publish_time):
                    cursor.execute(
                        """
                        UPDATE news_history
                        SET title = ?, normalized_title = ?, source_name = ?, source_url = ?,
                            publish_time = ?, related_companies = ?, category_level_1 = ?,
                            category_level_2 = ?, content_hash = ?, importance = ?
                        WHERE id = ?
                        """,
                        (
                            item.title,
                            normalized_title,
                            item.source_name,
                            normalized_url,
                            current_publish_time,
                            "；".join(item.related_companies) if item.related_companies else "",
                            item.category_level_1,
                            item.category_level_2,
                            item.content_hash,
                            item.importance,
                            existing["id"],
                        ),
                    )
                conn.commit()
                return

            # 不存在则插入
            cursor.execute(
                """
                INSERT INTO news_history (
                    title,
                    normalized_title,
                    source_name,
                    source_url,
                    publish_time,
                    related_companies,
                    category_level_1,
                    category_level_2,
                    content_hash,
                    importance
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.title,
                    normalized_title,
                    item.source_name,
                    normalized_url,
                    item.format_dt(item.publish_time),
                    "；".join(item.related_companies) if item.related_companies else "",
                    item.category_level_1,
                    item.category_level_2,
                    item.content_hash,
                    item.importance,
                ),
            )
            conn.commit()


    @staticmethod
    def _append_remark(existing: str | None, new_text: str) -> str:
        if not existing:
            return new_text
        return f"{existing}；{new_text}"