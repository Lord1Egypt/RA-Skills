"""
FTS5全文检索

中文适配：写入和查询时对文本做预处理（每字插空格），
使unicode61分词器能正确匹配中文字符。
"""

import re
from typing import List, Optional
from scripts.core.db_manager import DatabaseManager


def _preprocess_chinese(text: str) -> str:
    """对中文文本做预处理：每个中文字符后插空格，使FTS5能匹配单字"""
    if not text:
        return text
    # 中文字符后插空格
    result = re.sub(r'([\u4e00-\u9fff])', r'\1 ', text)
    return result


def _preprocess_query(query: str) -> str:
    """对搜索查询做预处理：每个中文字符后插空格"""
    if not query:
        return query
    chars = list(query.strip())
    processed = []
    for c in chars:
        if re.match(r'[\u4e00-\u9fff]', c):
            processed.append(f'"{c}"')
        elif c.strip():
            processed.append(f'"{c}"')
    return " OR ".join(processed)


class FtsSearch:
    """FTS5全文检索引擎"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def insert_doc(self, doc_id: str, category: str, product: str,
                   content: str, summary: str = ""):
        """插入文档到FTS5索引（中文预处理）"""
        self.db.execute(
            "INSERT OR REPLACE INTO knowledge_fts (doc_id, category, product, content, summary) "
            "VALUES (?, ?, ?, ?, ?)",
            (doc_id,
             _preprocess_chinese(category),
             _preprocess_chinese(product or ""),
             _preprocess_chinese(content),
             _preprocess_chinese(summary or "")),
        )
        self.db.commit()

    def delete_doc(self, doc_id: str):
        """从FTS5索引删除文档"""
        self.db.execute("DELETE FROM knowledge_fts WHERE doc_id=?", (doc_id,))
        self.db.commit()

    def search(self, query: str, top_k: int = 10,
               category: str = None, product: str = None) -> list:
        """
        FTS5关键词检索

        Args:
            query: 搜索关键词
            top_k: 返回条数
            category: 分类过滤
            product: 产品过滤

        Returns:
            [{doc_id, category, product, snippet, rank}, ...]
        """
        fts_query = _preprocess_query(query)
        if not fts_query:
            return []

        filter_clauses = []
        params: list = []
        if category:
            filter_clauses.append("category MATCH ?")
            params.append(_preprocess_chinese(category))
        if product:
            filter_clauses.append("product MATCH ?")
            params.append(_preprocess_chinese(product))

        filter_sql = ""
        if filter_clauses:
            filter_sql = " AND " + " AND ".join(filter_clauses)

        sql = (
            f"SELECT doc_id, category, product, "
            f"snippet(knowledge_fts, 3, '>>>', '<<<', '...', 30) as snippet, "
            f"rank "
            f"FROM knowledge_fts WHERE knowledge_fts MATCH ?{filter_sql} "
            f"ORDER BY rank LIMIT ?"
        )
        params = [fts_query] + params + [top_k]

        rows = self.db.query_all(sql, tuple(params))
        results = []
        for row in rows:
            snippet = row["snippet"] or ""
            # 清理预处理插入的空格和高亮标记
            snippet = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', snippet)
            category_clean = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', row["category"] or "")
            product_clean = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', row["product"] or "")
            results.append({
                "doc_id": row["doc_id"],
                "category": category_clean.strip() or None,
                "product": product_clean.strip() or None,
                "snippet": snippet,
                "rank": -row["rank"] if row["rank"] else 0,
            })
        return results

    def search_by_category(self, category: str) -> list:
        """按分类浏览所有文档"""
        return [
            dict(row) for row in self.db.query_all(
                "SELECT doc_id, category, product, summary FROM knowledge_fts WHERE category=?",
                (category,),
            )
        ]

    def get_all_categories(self) -> list:
        """获取所有知识分类"""
        rows = self.db.query_all(
            "SELECT DISTINCT category FROM knowledge_fts ORDER BY category"
        )
        return [row["category"] for row in rows]
