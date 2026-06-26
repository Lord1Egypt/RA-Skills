"""
Wiki 动态关联引擎

在 ingest 过程中自动发现新页面与已有 wiki 页面之间的关联。
支持轻量模式（单文件）和深度模式（全局批量）。

核心原则：纯代码实现关联发现，不依赖 LLM；输出结构化报告供 Agent 消费。
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .agent_logger import get_logger
from .core import WikiManager, WikiPage

LOG = get_logger("linker")


class RelationType(Enum):
    """页面间关系类型"""

    EXTENDS = "extends"  # 新页面扩展/深化已有概念
    CONTRASTS = "contrasts"  # 新页面与已有概念形成对比
    DEPENDS = "depends"  # 新页面依赖/引用已有概念
    UPDATES = "updates"  # 新页面更新/替代已有信息
    RELATED = "related"  # 一般相关


@dataclass
class PageRelation:
    """页面间关系描述"""

    source: str  # 新页面标题
    target: str  # 已有页面标题
    score: float  # 关联置信度 [0, 1]
    relation_type: RelationType  # 关系类型
    evidence: List[str] = field(default_factory=list)  # 关联证据
    suggested_action: str = ""  # 建议操作

    def to_markdown(self) -> str:
        lines = [
            f"### [[{self.target}]] — score: {self.score:.2f} | type: {self.relation_type.value.upper()}",
            f"**证据**: {', '.join(self.evidence) if self.evidence else '内容相似度'}",
        ]
        if self.suggested_action:
            lines.append(f"**建议**: {self.suggested_action}")
        return "\n".join(lines)


@dataclass
class RelationGraph:
    """关系图谱：一组新页面与 wiki 的关系网络"""

    relations: List[PageRelation] = field(default_factory=list)

    def by_source(self, source: str) -> List[PageRelation]:
        return [r for r in self.relations if r.source == source]

    def by_target(self, target: str) -> List[PageRelation]:
        return [r for r in self.relations if r.target == target]

    def top_k(self, k: int = 5) -> List[PageRelation]:
        return sorted(self.relations, key=lambda r: r.score, reverse=True)[:k]

    def to_markdown(self, title: str = "关联报告") -> str:
        lines = [f"# {title}", ""]
        if not self.relations:
            lines.append("未发现显著关联。")
            return "\n".join(lines)

        lines.append(f"## 发现关联 ({len(self.relations)})")
        lines.append("")
        for rel in sorted(self.relations, key=lambda r: r.score, reverse=True):
            lines.append(rel.to_markdown())
            lines.append("")
        return "\n".join(lines)


# 简单停用词表（中英文）
_STOP_WORDS: Set[str] = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
    "from", "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "and", "but", "or", "yet", "so", "if",
    "because", "although", "though", "while", "where", "when", "that",
    "which", "who", "whom", "whose", "what", "this", "these", "those",
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
    "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
    "会", "着", "没有", "看", "好", "自己", "这", "那", "啊",
}


def _extract_keywords(text: str) -> Set[str]:
    """从文本中提取关键词（简单启发式）"""
    # 英文单词
    words = re.findall(r"[a-zA-Z]{2,}", text.lower())
    # 中文字符：提取单个中文字符（去掉停用词）+ 2-8字连续序列
    zh_words = set()
    zh_chars = re.findall(r"[\u4e00-\u9fff]", text)
    for c in zh_chars:
        if c not in _STOP_WORDS:
            zh_words.add(c)
    zh_seqs = re.findall(r"[\u4e00-\u9fff]{2,8}", text)
    zh_words.update(zh_seqs)
    # 合并并过滤停用词
    all_words = set(words) | zh_words
    return all_words - _STOP_WORDS


def _jaccard_similarity(a: Set[str], b: Set[str]) -> float:
    """计算 Jaccard 相似度"""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _edit_distance(s1: str, s2: str) -> int:
    """计算编辑距离（Levenshtein）"""
    if len(s1) < len(s2):
        return _edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(
                min(
                    prev[j + 1] + 1,  # 删除
                    curr[j] + 1,      # 插入
                    prev[j] + (c1 != c2),  # 替换
                )
            )
        prev = curr
    return prev[-1]


def _normalize_title(title: str) -> str:
    """标准化标题用于比较"""
    return title.lower().replace("-", " ").replace("_", " ").strip()


class KnowledgeLinker:
    """知识关联引擎"""

    def __init__(self, wiki: WikiManager, index=None):
        self.wiki = wiki
        self.index = index  # Optional[EmbeddingIndex]
        self._keyword_cache: Dict[str, Set[str]] = {}

    def _get_keywords(self, page: WikiPage) -> Set[str]:
        """获取页面的关键词缓存"""
        cache_key = page.path.name
        if cache_key not in self._keyword_cache:
            text = f"{page.title} {' '.join(page.tags)} {page.content}"
            self._keyword_cache[cache_key] = _extract_keywords(text)
        return self._keyword_cache[cache_key]

    def _clear_cache(self):
        """清除关键词缓存"""
        LOG.debug("Clearing keyword cache")
        self._keyword_cache.clear()

    def find_related(
        self,
        query: str,
        query_tags: Optional[List[str]] = None,
        query_content: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.3,
        use_embedding: bool = True,
        keyword_weight: float = 0.4,
        vector_weight: float = 0.4,
        link_weight: float = 0.2,
    ) -> List[PageRelation]:
        """
        发现与 query 内容最相关的 wiki 页面。

        Args:
            query: 查询文本（通常是新页面标题）
            query_tags: 查询页面的标签
            query_content: 查询页面的完整内容（用于 keyword match 和 embedding）
            top_k: 返回的最大关联数
            min_score: 最小关联置信度
            use_embedding: 是否使用 embedding 索引
            keyword_weight: keyword match 权重
            vector_weight: vector match 权重
            link_weight: link proximity 权重

        Returns:
            按 score 降序排列的 PageRelation 列表
        """
        LOG.info("find_related: query=%s mode=kw_w=%.1f vec_w=%.1f link_w=%.1f top_k=%d min_score=%.2f",
                 query, keyword_weight, vector_weight, link_weight, top_k, min_score)
        pages = self.wiki.list_pages()
        if not pages:
            LOG.warning("Wiki has no pages")
            return []

        # 构建查询文本
        full_query = query
        if query_content:
            full_query = f"{query}\n{query_content}"
        query_tags_set = set(query_tags or [])
        query_keywords = _extract_keywords(full_query)
        LOG.debug("Query keywords extracted: %d terms", len(query_keywords))

        scores: Dict[str, float] = {}
        evidence: Dict[str, List[str]] = {}

        # 1. Keyword Match
        LOG.debug("Phase 1: keyword match (weight=%.1f)", keyword_weight)
        for page in pages:
            kw_score = 0.0
            page_evidence = []

            # 标题匹配
            norm_query = _normalize_title(query)
            norm_page = _normalize_title(page.title)
            if norm_query in norm_page or norm_page in norm_query:
                kw_score += 0.6
                page_evidence.append("标题包含")

            # 标签匹配
            page_tags = set(page.tags)
            shared_tags = query_tags_set & page_tags
            if shared_tags:
                tag_ratio = len(shared_tags) / max(len(query_tags_set), len(page_tags), 1)
                kw_score += 0.3 * tag_ratio
                page_evidence.append(f"共享标签: {', '.join(shared_tags)}")

            # 关键词重叠
            page_keywords = self._get_keywords(page)
            if page_keywords and query_keywords:
                overlap = _jaccard_similarity(page_keywords, query_keywords)
                kw_score += 0.3 * overlap
                if overlap > 0.1:
                    page_evidence.append(f"关键词重叠: {overlap:.0%}")

            # 内容包含
            query_lower = full_query.lower()
            page_lower = page.content.lower()
            if norm_page in query_lower:
                kw_score += 0.2
                page_evidence.append(f"内容引用: {page.title}")

            scores[page.title] = kw_score * keyword_weight
            evidence[page.title] = page_evidence

        # 2. Vector Match (如果 embedding 索引可用且启用)
        if (
            use_embedding
            and self.index is not None
            and vector_weight > 0
            and self.index.cache
            and self.index.cache.get("pages")
        ):
            LOG.debug("Phase 2: vector match (weight=%.1f)", vector_weight)
            try:
                vec_results = self.index.search(
                    full_query,
                    top_k=len(pages),
                    keyword_weight=0.0,
                    vector_weight=1.0,
                    link_weight=0.0,
                    enable_link_traversal=False,
                )
                LOG.debug("Vector search returned %d results", len(vec_results))
                for title, vec_score in vec_results:
                    if title in scores:
                        scores[title] = scores.get(title, 0.0) + vec_score * vector_weight
                        if vec_score > 0.5:
                            evidence.setdefault(title, []).append(f"语义相似度: {vec_score:.2f}")
            except Exception:
                LOG.warning("Vector search failed, skipping", exc_info=True)
        else:
            LOG.debug("Phase 2: vector match skipped (use_embedding=%s index=%s)",
                      use_embedding, self.index is not None)

        # 3. Link Proximity
        if link_weight > 0:
            LOG.debug("Phase 3: link proximity (weight=%.1f)", link_weight)
            # 从 query 内容中提取链接
            query_links: Set[str] = set()
            link_pattern = r"\[\[([^\]]+)\]\]"
            query_links = set(re.findall(link_pattern, full_query))
            LOG.debug("Query links found: %s", query_links)

            # 1-hop 传播
            link_boosts: Dict[str, float] = {}
            page_map = {p.title: p for p in pages}

            for link_title in query_links:
                link_page = page_map.get(link_title)
                if link_page:
                    for neighbor in link_page.links:
                        if neighbor in page_map and neighbor != query:
                            link_boosts[neighbor] = link_boosts.get(neighbor, 0.0) + link_weight * 0.5

            # 2-hop 传播
            hop1 = set(link_boosts.keys())
            for hop1_title in list(hop1):
                hop1_page = page_map.get(hop1_title)
                if hop1_page:
                    for neighbor in hop1_page.links:
                        if neighbor in page_map and neighbor != query and neighbor not in hop1:
                            link_boosts[neighbor] = link_boosts.get(neighbor, 0.0) + link_weight * 0.25

            LOG.debug("Link proximity boosts: %d pages affected", len(link_boosts))
            for title, boost in link_boosts.items():
                scores[title] = scores.get(title, 0.0) + boost
                if boost >= link_weight * 0.3:
                    evidence.setdefault(title, []).append("链接邻近")
        else:
            LOG.debug("Phase 3: link proximity skipped (weight=%.1f)", link_weight)

        # 构建 PageRelation 列表
        relations = []
        page_map = {p.title: p for p in pages}
        for title, score in scores.items():
            if score < min_score:
                continue
            if title == query:
                continue  # exclude self-relation
            page = page_map.get(title)
            if not page:
                continue

            # 关系分类
            query_page = WikiPage(
                title=query,
                content=query_content or query,
                frontmatter={"tags": list(query_tags_set)},
                path=self.wiki.wiki_dir / f"{query}.md",
            )
            rel_type = self.classify_relation(query_page, page, score)

            # 生成建议操作
            suggestion = self._suggest_action(rel_type, query, title)

            relations.append(
                PageRelation(
                    source=query,
                    target=title,
                    score=round(score, 2),
                    relation_type=rel_type,
                    evidence=evidence.get(title, []),
                    suggested_action=suggestion,
                )
            )

        # 按 score 降序，限制数量
        relations.sort(key=lambda r: r.score, reverse=True)
        LOG.info("find_related complete: %d relations above min_score (returning top %d)",
                 len(relations), top_k)
        return relations[:top_k]

    def build_relation_graph(
        self,
        new_pages: List[str],
        mode: str = "deep",
        max_depth: int = 2,
        top_k: int = 10,
        min_score: float = 0.2,
    ) -> RelationGraph:
        """
        全局深度关联：分析一组新页面与整个 wiki 的关系网络。

        Args:
            new_pages: 新页面标题列表
            mode: "light" 或 "deep"
            max_depth: 链接传播深度（暂保留接口，当前实现固定为 2）
            top_k: 每个新页面返回的最大关联数
            min_score: 最小关联置信度

        Returns:
            RelationGraph 包含所有发现的关联
        """
        LOG.info("build_relation_graph: %d new pages, mode=%s, top_k=%d", len(new_pages), mode, top_k)
        all_relations: List[PageRelation] = []

        for page_title in new_pages:
            page = self.wiki.get_page(page_title)
            if not page:
                LOG.warning("Page not found in graph build: %s", page_title)
                continue

            # 根据模式调整参数
            if mode == "light":
                rels = self.find_related(
                    query=page_title,
                    query_tags=page.tags,
                    query_content=page.content,
                    top_k=min(top_k, 5),
                    min_score=max(min_score, 0.3),
                    use_embedding=False,  # 轻量模式不用 embedding
                    keyword_weight=0.6,
                    vector_weight=0.0,
                    link_weight=0.4,
                )
            else:  # deep
                rels = self.find_related(
                    query=page_title,
                    query_tags=page.tags,
                    query_content=page.content,
                    top_k=top_k,
                    min_score=min_score,
                    use_embedding=True,
                    keyword_weight=0.4,
                    vector_weight=0.4,
                    link_weight=0.2,
                )

            all_relations.extend(rels)

        LOG.info("build_relation_graph complete: %d total relations", len(all_relations))
        return RelationGraph(relations=all_relations)

    def classify_relation(
        self,
        source: WikiPage,
        target: WikiPage,
        content_similarity: Optional[float] = None,
    ) -> RelationType:
        """
        基于启发式规则推断两个页面之间的关系类型。

        Args:
            source: 新页面
            target: 已有页面
            content_similarity: 预计算的内容相似度（可选）

        Returns:
            RelationType
        """
        s_title = _normalize_title(source.title)
        t_title = _normalize_title(target.title)

        # UPDATES: 标题高度相似（编辑距离 < 3 且标题长度 > 3）
        dist = _edit_distance(s_title, t_title)
        if dist < 3 and len(s_title) > 3 and len(t_title) > 3:
            return RelationType.UPDATES

        # CONTRASTS: 新标题包含旧标题（通常是 "X vs Y" 形式）
        if t_title in s_title and s_title != t_title:
            return RelationType.CONTRASTS

        # DEPENDS: 旧页面在 source 的 sources 中
        source_sources = source.frontmatter.get("sources", [])
        if isinstance(source_sources, list):
            for src in source_sources:
                if t_title.lower() in str(src).lower():
                    return RelationType.DEPENDS

        # EXTENDS: 标签重叠多且内容相似度高
        s_tags = set(source.tags)
        t_tags = set(target.tags)
        shared_tags = s_tags & t_tags
        if content_similarity is None:
            s_kw = _extract_keywords(source.content)
            t_kw = _extract_keywords(target.content)
            content_similarity = _jaccard_similarity(s_kw, t_kw)

        if len(shared_tags) >= 2 and content_similarity > 0.3:
            return RelationType.EXTENDS

        return RelationType.RELATED

    def _suggest_action(self, rel_type: RelationType, source: str, target: str) -> str:
        """根据关系类型生成建议操作"""
        suggestions = {
            RelationType.EXTENDS: (
                f"在 {target} 的\"相关页面\"添加 {source} 链接，"
                f"考虑在 {source} 中引用 {target} 的方法对比"
            ),
            RelationType.CONTRASTS: (
                f"在双方页面的\"相关页面\"添加互链，"
                f"考虑在 {target} 中添加\"与 {source} 的对比\"章节"
            ),
            RelationType.DEPENDS: (
                f"在 {source} 的\"来源\"中明确引用 {target}，"
                f"在 {target} 的\"相关页面\"添加 {source}"
            ),
            RelationType.UPDATES: (
                f"检查 {target} 中的信息是否需要由 {source} 更新，"
                f"在 {target} 的变更日志中记录"
            ),
            RelationType.RELATED: (
                f"在 {target} 的\"相关页面\"中添加 {source} 链接"
            ),
        }
        return suggestions.get(rel_type, "")
