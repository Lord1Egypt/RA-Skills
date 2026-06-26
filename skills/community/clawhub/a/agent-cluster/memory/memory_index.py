"""
memory_index.py - 记忆全文检索索引

提供语义化的记忆检索能力：
- 关键词 + 标签 + 时间范围组合检索
- 重要性加权排序
- 相似记忆发现
- 热门标签统计
"""

from __future__ import annotations

import logging
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Optional

from .memory_core import (
    MemoryEntry,
    MemoryQuery,
    MemoryResult,
    MemoryScope,
)
from .persistent_store import PersistentStore, get_cursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryIndex:
    """
    记忆索引与检索引擎
    
    在 PersistentStore 的 FTS5 基础上，提供：
    - 多维度组合检索
    - 检索结果加权重排（重要性 + 时效性）
    - 相似记忆聚类
    - 检索建议生成
    """
    
    def __init__(self, store: Optional[PersistentStore] = None):
        self.store = store or PersistentStore()
    
    # -------------------------------------------------------------------------
    # 检索方法
    # -------------------------------------------------------------------------
    
    def search(
        self,
        query_text: str = "",
        agent_id: str = "",
        scopes: list[MemoryScope] | None = None,
        memory_types: list[str] | None = None,
        tags: list[str] | None = None,
        min_importance: int = 1,
        since_hours: int | None = None,
        caller_agent_id: str = "",
        limit: int = 20,
    ) -> MemoryResult:
        """
        组合检索
        
        支持多条件组合，返回加权排序结果
        """
        # 构建查询
        from .memory_core import MemoryQuery as MCQuery, MemoryImportance
        import typing
        types = None
        if memory_types:
            from .memory_core import MemoryType
            types = [MemoryType(t) for t in memory_types if t]
        
        scopes_enum = None
        if scopes:
            scopes_enum = [MemoryScope(s) if isinstance(s, str) else s for s in scopes]
        
        q = MCQuery(
            query_text=query_text,
            tags=tags or [],
            scopes=scopes_enum or [],
            agent_id=agent_id or None,
            memory_types=types or [],
            min_importance=MemoryImportance(min_importance),
            caller_agent_id=caller_agent_id,
            limit=limit,
        )
        
        result = self.store.query(q)
        
        # 时效性加权：如果指定了 since_hours，过滤并重排
        if since_hours:
            now = datetime.now(timezone.utc)
            cutoff = now.timestamp() - since_hours * 3600
            filtered = []
            for e in result.entries:
                try:
                    e_time = datetime.fromisoformat(e.created_at).timestamp()
                    if e_time >= cutoff:
                        filtered.append(e)
                except ValueError:
                    filtered.append(e)
            
            # 按时效性重新排序（越新越靠前）
            filtered.sort(key=lambda e: e.created_at, reverse=True)
            result.entries = filtered
            result.total = len(filtered)
        
        # 计算相关性分数并重排（可选）
        result.entries = self._rerank(query_text, result.entries)
        
        return result
    
    def _rerank(self, query_text: str, entries: list[MemoryEntry]) -> list[MemoryEntry]:
        """
        基于多信号重排检索结果
        
        评分因子：
        - 全文匹配强度（query_text 在 content/summary 中的出现次数）
        - 重要性权重（CRITICAL=5, HIGH=4, ...）
        - 时效性因子（越新越好，7天内加权）
        - 标签精确匹配（完全匹配 query 的标签越多越好）
        """
        if not entries or not query_text:
            return entries
        
        query_terms = set(query_text.lower().split())
        scored = []
        
        now = datetime.now(timezone.utc)
        seven_days_ago = (now.timestamp() - 7 * 86400)
        
        for entry in entries:
            score = 0.0
            
            # 全文匹配
            content_lower = entry.content.lower()
            summary_lower = entry.summary.lower()
            
            for term in query_terms:
                if term in content_lower:
                    score += content_lower.count(term) * 2.0
                if term in summary_lower:
                    score += summary_lower.count(term) * 3.0  # 摘要匹配权重更高
            
            # 重要性权重
            importance_weights = {5: 10.0, 4: 7.0, 3: 4.0, 2: 2.0, 1: 0.5}
            score += importance_weights.get(entry.importance.value, 1.0)
            
            # 时效性因子（7天内额外加权）
            try:
                entry_time = datetime.fromisoformat(entry.created_at).timestamp()
                if entry_time >= seven_days_ago:
                    score += 3.0
            except ValueError:
                pass
            
            # 标签精确匹配
            entry_tags_lower = [t.lower() for t in entry.tags]
            for term in query_terms:
                if term in entry_tags_lower:
                    score += 5.0  # 标签匹配加分
            
            # 置顶加分
            if entry.is_pinned:
                score += 8.0
            
            scored.append((score, entry))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored]
    
    # -------------------------------------------------------------------------
    # 相似记忆
    # -------------------------------------------------------------------------
    
    def find_similar(
        self,
        content: str,
        agent_id: str = "",
        caller_agent_id: str = "",
        scopes: list[MemoryScope] | None = None,
        limit: int = 5,
    ) -> list[MemoryEntry]:
        """
        查找与给定内容相似的已有记忆
        
        用于：
        - 记忆去重（存储前检查是否已存在类似记忆）
        - 知识补全（发现相关记忆供补充）
        """
        return self.search(
            query_text=content[:200],  # 截断避免过长
            agent_id=agent_id,
            caller_agent_id=caller_agent_id,
            scopes=scopes,
            limit=limit,
        ).entries
    
    # -------------------------------------------------------------------------
    # 热门标签
    # -------------------------------------------------------------------------
    
    def get_hot_tags(self, top_n: int = 20) -> list[tuple[str, int]]:
        """
        获取热门标签统计
        
        返回：(标签名, 使用次数) 按热度排序
        """
        with get_cursor(self.store.db_path) as cur:
            cur.execute("""
                SELECT tags FROM memory_entries
                WHERE is_deleted=0
            """)
            
            all_tags: list[str] = []
            for row in cur.fetchall():
                import json
                tags = json.loads(row["tags"])
                all_tags.extend(tags)
            
            counter = Counter(all_tags)
            
            # 过滤系统标签
            system_tags = {"session", "meta", "task", "event", "decision", 
                          "context_share", "agent_join", "session_create", "session_complete",
                          "session_knowledge", "rule_candidate", "pending_review",
                          "task_start", "task_complete", "message"}
            filtered = [(t, c) for t, c in counter.most_common(100) if t not in system_tags]
            return filtered[:top_n]
    
    # -------------------------------------------------------------------------
    # 检索建议
    # -------------------------------------------------------------------------
    
    def suggest(self, partial: str, caller_agent_id: str = "", limit: int = 5) -> list[str]:
        """
        基于已有记忆生成检索建议
        
        根据部分输入，预测可能想搜索的内容
        """
        if len(partial) < 2:
            return []
        
        hot_tags = self.get_hot_tags(top_n=50)
        partial_lower = partial.lower()
        
        suggestions = [
            tag for tag, _ in hot_tags
            if tag.startswith(partial_lower) or partial_lower in tag
        ][:limit]
        
        return suggestions
    
    # -------------------------------------------------------------------------
    # 知识图谱构建（简化版）
    # -------------------------------------------------------------------------
    
    def build_knowledge_graph(
        self,
        agent_id: str = "",
        limit: int = 200,
    ) -> dict[str, Any]:
        """
        从记忆构建简化知识图谱
        
        返回：
        - nodes: 记忆节点列表
        - edges: 关联关系列表
        """
        # 获取所有相关记忆
        q = MemoryQuery(
            scope=MemoryScope.SHARED if not agent_id else None,
            agent_id=agent_id or None,
            caller_agent_id=agent_id,
            min_importance=3,
            limit=limit,
        )
        result = self.store.query(q)
        
        nodes = []
        edges = []
        seen_edges: set[tuple] = set()
        
        for entry in result.entries:
            node_id = entry.entry_id
            
            # 节点
            nodes.append({
                "id": node_id,
                "label": entry.summary or entry.content[:50],
                "type": entry.memory_type.value,
                "scope": entry.scope.value,
                "importance": entry.importance.value,
                "tags": entry.tags[:5],
            })
            
            # 边：关联Agent
            for related_agent in entry.related_agent_ids:
                edge_key = (node_id, related_agent)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        "source": node_id,
                        "target": related_agent,
                        "type": "related_agent",
                    })
            
            # 边：关联记忆
            for related_id in entry.related_entry_ids:
                edge_key = (node_id, related_id)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        "source": node_id,
                        "target": related_id,
                        "type": "related_entry",
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges),
        }
