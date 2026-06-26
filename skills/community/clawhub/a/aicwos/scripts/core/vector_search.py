"""
向量检索

基于numpy余弦相似度，向量存储在SQLite BLOB字段中。
支持单条检索和混合检索（向量+FTS5）。
"""

import sys
from pathlib import Path
from typing import List, Optional

_SKILL_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)

from scripts.core.semantic_model import deserialize_vector, cosine_similarity, EMBEDDING_DIM
from scripts.core.db_manager import DatabaseManager


class VectorSearch:
    """向量检索引擎"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def insert_vector(self, doc_id: str, chunk_index: int, vector: list):
        """插入向量到knowledge_chunks"""
        from scripts.core.semantic_model import serialize_vector
        blob = serialize_vector(vector) if vector else b""
        self.db.execute(
            "UPDATE knowledge_chunks SET vector_blob=? WHERE doc_id=? AND chunk_index=?",
            (blob, doc_id, chunk_index),
        )
        self.db.commit()

    def search(self, query_vector: list, top_k: int = 10, category: str = None,
               product: str = None) -> list:
        """
        向量相似度检索

        Args:
            query_vector: 查询向量
            top_k: 返回前K条
            category: 可选，限制分类
            product: 可选，限制产品

        Returns:
            [{doc_id, chunk_index, content, similarity}, ...]
        """
        conditions = ["vector_blob IS NOT NULL", "length(vector_blob) > 0"]
        params = []

        if category:
            conditions.append("kc.doc_id IN (SELECT doc_id FROM knowledge_docs WHERE category=?)")
            params.append(category)
        if product:
            conditions.append("kc.doc_id IN (SELECT doc_id FROM knowledge_docs WHERE product=?)")
            params.append(product)

        where = " AND ".join(conditions)
        rows = self.db.query_all(
            f"SELECT kc.doc_id, kc.chunk_index, kc.content, kc.vector_blob, "
            f"kd.category, kd.product "
            f"FROM knowledge_chunks kc "
            f"LEFT JOIN knowledge_docs kd ON kc.doc_id = kd.doc_id "
            f"WHERE {where}",
            tuple(params),
        )

        # 计算相似度
        results = []
        for row in rows:
            vec = deserialize_vector(row["vector_blob"])
            sim = cosine_similarity(query_vector, vec)
            results.append({
                "doc_id": row["doc_id"],
                "chunk_index": row["chunk_index"],
                "content": row["content"],
                "similarity": round(sim, 4),
                "category": row["category"],
                "product": row["product"],
            })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def search_with_fts(self, query_text: str, query_vector: list = None,
                        top_k: int = 10, category: str = None) -> list:
        """
        混合检索：FTS5关键词 + 向量语义

        有向量时：向量结果和FTS5结果合并去重，按综合分排序
        无向量时：纯FTS5关键词检索
        """
        from scripts.core.fts_search import FtsSearch
        fts = FtsSearch(self.db)

        # FTS5检索
        fts_results = fts.search(query_text, top_k=top_k * 2, category=category)

        if not query_vector:
            return fts_results[:top_k]

        # 向量检索
        vec_results = self.search(query_vector, top_k=top_k * 2, category=category)

        # 合并去重，综合评分
        merged = {}
        for r in fts_results:
            key = f"{r['doc_id']}_{r.get('chunk_index', 0)}"
            merged[key] = {**r, "fts_score": r.get("rank", 0), "vec_score": 0}
        for r in vec_results:
            key = f"{r['doc_id']}_{r['chunk_index']}"
            if key in merged:
                merged[key]["vec_score"] = r["similarity"]
            else:
                merged[key] = {**r, "fts_score": 0, "vec_score": r["similarity"]}

        # 综合分：0.4*FTS + 0.6*向量（向量权重更高因为语义更准）
        for item in merged.values():
            fts_norm = min(item.get("fts_score", 0) / 10, 1.0) if item.get("fts_score", 0) > 0 else 0
            item["combined_score"] = 0.4 * fts_norm + 0.6 * item.get("vec_score", 0)

        results = sorted(merged.values(), key=lambda x: x["combined_score"], reverse=True)
        return results[:top_k]
