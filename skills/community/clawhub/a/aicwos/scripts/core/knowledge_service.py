"""
知识库服务

CRUD + 检索（FTS5 + 向量）+ Write-Through 双写。

架构原则：每次数据变更同时更新 DB 和文件系统，无需手动同步。
- DB：查询层（检索、FTS5、向量搜索）
- 文件系统：来源层（用户编辑、云端同步）
- 知识文档的数据流方向：文件系统 → DB（单向），删除时反向清理

核心优化：
- 添加文档时自动切分段落、生成摘要、计算向量
- 检索时返回精确段落而非整个文件
- 语义搜索+关键词搜索混合
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from scripts.core.db_manager import DatabaseManager
from scripts.core.fts_search import FtsSearch
from scripts.core.vector_search import VectorSearch
from scripts.core.text2vec_embedder import Text2VecEmbedder
from scripts.core.text_utils import generate_summary, chunk_text, extract_keywords


class KnowledgeService:
    """知识库服务（Write-Through：删除时同步清理文件）"""

    CHUNK_SIZE = 300  # 段落切分字数

    def __init__(self, db: DatabaseManager, data_dir: str = None):
        self.db = db
        self.data_dir = Path(data_dir) if data_dir else None
        self.fts = FtsSearch(db)
        self.vec_search = VectorSearch(db)
        self.embedder = Text2VecEmbedder.get_instance()

    def add_doc(self, category: str, filename: str, content: str,
                product: str = None, layer: str = "公共") -> dict:
        """
        添加知识文档

        自动：生成摘要 → 提取关键词 → 切分段落 → 计算向量 → 入库
        注：知识文档来源于文件系统（用户编辑/云端同步），此方法只做索引，不反向写文件。
        """
        doc_id = f"{category}/{product}/{filename}" if product else f"{category}/{filename}"
        now = datetime.now().isoformat(timespec="seconds")
        summary = generate_summary(content)
        keywords = extract_keywords(content)

        # 写入主表
        self.db.execute(
            "INSERT OR REPLACE INTO knowledge_docs "
            "(doc_id, category, product, filename, layer, content, summary, keywords, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (doc_id, category, product, filename, layer, content, summary,
             json.dumps(keywords, ensure_ascii=False), now),
        )

        # 切分段落
        chunks = chunk_text(content, self.CHUNK_SIZE)
        for i, chunk in enumerate(chunks):
            self.db.execute(
                "INSERT OR REPLACE INTO knowledge_chunks (doc_id, chunk_index, content) "
                "VALUES (?, ?, ?)",
                (doc_id, i, chunk),
            )
            # 计算向量
            vec = self.embedder.encode(chunk)
            if vec:
                from scripts.core.semantic_model import serialize_vector
                self.db.execute(
                    "UPDATE knowledge_chunks SET vector_blob=? WHERE doc_id=? AND chunk_index=?",
                    (serialize_vector(vec), doc_id, i),
                )

        # FTS5索引
        self.fts.insert_doc(doc_id, category, product, content, summary)
        self.db.commit()

        return {
            "status": "ok",
            "doc_id": doc_id,
            "category": category,
            "product": product,
            "summary": summary,
            "keywords": keywords,
            "chunks": len(chunks),
            "vectorized": self.embedder.is_available,
        }

    def delete_doc(self, doc_id: str) -> dict:
        """删除知识文档（Write-Through: DB + 私有层源文件清理）"""
        # 检查存在
        row = self.db.query_one("SELECT doc_id FROM knowledge_docs WHERE doc_id=?", (doc_id,))
        if not row:
            return {"status": "not_found", "doc_id": doc_id}

        self.db.execute("DELETE FROM knowledge_chunks WHERE doc_id=?", (doc_id,))
        self.db.execute("DELETE FROM knowledge_docs WHERE doc_id=?", (doc_id,))
        self.fts.delete_doc(doc_id)
        self.db.commit()

        # Write-Through: 删除私有层源文件（公共层不动，由云端管理）
        self._delete_source_file(doc_id)

        return {"status": "ok", "doc_id": doc_id, "action": "deleted"}

    def get_doc(self, doc_id: str) -> Optional[dict]:
        """获取文档完整信息"""
        row = self.db.query_one("SELECT * FROM knowledge_docs WHERE doc_id=?", (doc_id,))
        if not row:
            return None
        return dict(row)

    def search(self, query: str, top_k: int = 5, category: str = None,
               product: str = None) -> list:
        """
        混合检索知识库

        优先向量语义检索，辅以FTS5关键词检索。
        返回精确段落，非整个文件。
        """
        query_vec = self.embedder.encode(query)

        if query_vec:
            return self.vec_search.search_with_fts(
                query_text=query, query_vector=query_vec,
                top_k=top_k, category=category,
            )
        else:
            # 无向量时纯FTS5
            return self.fts.search(query, top_k=top_k, category=category)

    def list_categories(self) -> list:
        """列出所有分类及其文档数"""
        rows = self.db.query_all(
            "SELECT category, COUNT(*) as cnt FROM knowledge_docs GROUP BY category"
        )
        return [{"category": r["category"], "count": r["cnt"]} for r in rows]

    def list_docs_by_category(self, category: str) -> list:
        """列出某分类下所有文档"""
        rows = self.db.query_all(
            "SELECT doc_id, product, filename, summary FROM knowledge_docs WHERE category=?",
            (category,),
        )
        return [dict(r) for r in rows]

    def get_relevant_context(self, query: str, max_tokens: int = 1500) -> str:
        """
        获取与查询最相关的知识上下文（token预算内）

        核心优化：只返回相关段落，不读整个文件
        """
        results = self.search(query, top_k=10)
        # 估算token（中文1token≈1.7字符）
        budget = max_tokens * 1.7
        context_parts = []
        used = 0
        for r in results:
            content = r.get("content", r.get("snippet", ""))
            # 清理FTS5高亮标记和预处理插入的多余空格
            import re
            content = re.sub(r'>>>(.*?)<<<', r'\1', content)
            # 移除中文字符/中文标点之间的空格（保留中英文间的空格）
            content = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', content)
            if used + len(content) > budget:
                break
            source = r.get("doc_id", "")
            context_parts.append(f"[{source}]\n{content}")
            used += len(content)
        return "\n\n".join(context_parts)

    # ── 私有方法：文件系统清理 ──────────────────────────────

    def _delete_source_file(self, doc_id: str):
        """删除私有层知识源文件（公共层不动，由云端管理）"""
        if not self.data_dir:
            return
        # doc_id 格式: "产品目录/产品A/产品属性.txt" 或 "分类/文件.txt"
        parts = doc_id.split("/")
        private_base = self.data_dir / "知识库集" / "私有"
        # 尝试多种路径匹配
        candidates = [
            private_base / Path(*parts),                   # 精确路径
            private_base / parts[-1],                      # 仅文件名
        ]
        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                candidate.unlink()
                return
