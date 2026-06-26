#!/usr/bin/env python3
"""
bundle-search.py — M-FLOW Bundle Search 检索实现

倒锥图路由检索算法：
1. 锥尖广撒网：查询在4层同时搜索，返回候选
2. 投影到图中：提取候选周围的子图
3. 代价传播：从锥尖向锥底传播，计算Episode得分
4. 排序返回：按最小代价排序

Usage:
    python bundle-search.py "query string" [--top-k 5]
    python bundle-search.py --interactive
"""

import json, os, re, math, sys, argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

# ========== 配置 ==========

_env = os.environ.get("OPENCLAW_WORKSPACE", "")
if _env:
    WORKSPACE = Path(_env)
else:
    WORKSPACE = Path(__file__).resolve().parents[2]
    if not (WORKSPACE / "memory").exists():
        WORKSPACE = Path.home() / ".openclaw" / "workspace"

GRAPH_DIR = WORKSPACE / "memory" / "graph"

ENTITIES_FILE = GRAPH_DIR / "entities.json"
FACETPOINTS_FILE = GRAPH_DIR / "facetpoints.json"
FACETS_FILE = GRAPH_DIR / "facets.json"
EPISODES_FILE = GRAPH_DIR / "episodes.json"
EDGES_FILE = GRAPH_DIR / "edges.json"

# Bundle Search 常数
TOP_K_PER_LAYER = 100
PENALTY_DIRECT_HIT = 0.5  # 直接命中Episode摘要的惩罚
JUMP_PENALTY = 0.1        # 每多一跳加的惩罚
EDGE_SEMANTIC_WEIGHT = 0.3  # 边描述的权重


# ========== 数据结构 ==========

class Episode:
    def __init__(self, id, title, episode_type, source_path, summary="",
                 facetpoint_ids=None, facet_ids=None, tags=None, importance=1.0):
        self.id = id
        self.title = title
        self.episode_type = episode_type
        self.source_path = source_path
        self.summary = summary
        self.facetpoint_ids = facetpoint_ids or []
        self.facet_ids = facet_ids or []
        self.tags = tags or []
        self.importance = importance
        self.direct_hit = False
        self.score = float('inf')
        self.matched_facetpoints = []

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["id"], d.get("title", ""), d.get("episode_type", ""),
            d.get("source_path", ""), d.get("summary", ""),
            d.get("facetpoint_ids", []), d.get("facet_ids", []),
            d.get("tags", []), d.get("importance", 1.0)
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "episode_type": self.episode_type,
            "source_path": self.source_path,
            "summary": self.summary,
            "tags": self.tags,
            "importance": self.importance,
            "direct_hit": self.direct_hit,
            "score": round(self.score, 4),
            "matched_facetpoints": self.matched_facetpoints
        }


class FacetPoint:
    def __init__(self, id, label, keywords, entity_id, facet_id=None,
                 episode_ids=None):
        self.id = id
        self.label = label
        self.keywords = keywords or []
        self.entity_id = entity_id
        self.facet_id = facet_id
        self.episode_ids = episode_ids or []

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["id"], d.get("label", ""), d.get("keywords", []),
            d.get("entity_id", ""), d.get("facet_id"),
            d.get("episode_ids", [])
        )


class SemanticEdge:
    def __init__(self, id, from_id, to_id, description, edge_type):
        self.id = id
        self.from_id = from_id
        self.to_id = to_id
        self.description = description
        self.edge_type = edge_type

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["id"], d.get("from_id", ""), d.get("to_id", ""),
            d.get("description", ""), d.get("edge_type", "")
        )


# ========== 简单向量相似度（无embedding模型时用词袋）========

def _tokenize_text(text: str) -> set:
    """Split text into words: jieba for Chinese, regex for English/numbers."""
    text_lower = text.lower()
    words = set()
    if JIEBA_AVAILABLE:
        words.update(jieba.lcut(text_lower))
    words.update(re.findall(r'[a-z0-9]{2,}', text_lower))
    # Chinese character level (each char is a potential word boundary)
    chinese_chars = set(re.findall(r'[\u4e00-\u9fff]', text_lower))
    words.update(chinese_chars)
    # Remove empty strings
    words = {w for w in words if w.strip()}
    return words

def keyword_match_score(query: str, text: str) -> float:
    """
    查询与文本的匹配得分（支持中文分词）
    """
    query_words = query.lower().split()
    if not query_words:
        return 0.0
    text_words = _tokenize_text(text)

    # 精确匹配词
    exact = sum(1 for q in query_words if q in text_words)
    exact_score = exact / len(query_words)

    # 子串匹配（查询词出现在文本中）
    substr = sum(1 for q in query_words if q in text.lower())
    substr_score = substr / len(query_words)

    return max(exact_score, substr_score * 0.5)


def simple_vector_similarity(query: str, keywords: list[str]) -> float:
    """
    简化的向量相似度（词袋模型，支持中文）
    query和keywords的交集/并集
    """
    if not keywords:
        return 0.0
    query_words = set(query.lower().split())
    keyword_tokens = set()
    for k in keywords:
        keyword_tokens.update(_tokenize_text(k))
    intersection = query_words & keyword_tokens
    # Add substring matches: if query word appears in any keyword text
    for q in query_words:
        for kw in keywords:
            if q in kw.lower():
                intersection.add(q)
                break
    union = query_words | keyword_tokens
    # Also add query words that appear as substring in any keyword text
    for q in query_words:
        for kw in keywords:
            if q in kw.lower():
                union.add(q)
    if not union:
        return 0.0
    return len(intersection) / len(union)


# ========== Bundle Search ==========

class BundleSearch:
    """
    M-FLOW Bundle Search 检索器

    核心算法：
    1. 阶段1（锥尖广撒网）：查询向量同时在4层搜索
    2. 阶段2（投影到图）：提取候选周围的子图
    3. 阶段3（代价传播）：从锥尖向锥底传播，计算Episode得分
    """

    def __init__(self, quiet: bool = False):
        self.episodes: dict[str, Episode] = {}
        self.facetpoints: dict[str, FacetPoint] = {}
        self.edges: dict[str, SemanticEdge] = {}
        self._quiet = quiet
        self._adj: dict[str, list[str]] = {}  # 邻接表：node_id -> [neighbor_ids]
        self._edge_by_nodes: dict[tuple[str, str], SemanticEdge] = {}  # (from,to)->edge  O(1)边查找
        self._load()

    def _load(self):
        """加载图数据（统一UTF-8）"""
        def read(path):
            if not path.exists():
                return []
            try:
                return json.loads(path.read_text(encoding='utf-8'))
            except Exception:
                return []

        for d in read(EPISODES_FILE):
            ep = Episode.from_dict(d)
            self.episodes[ep.id] = ep

        for d in read(FACETPOINTS_FILE):
            fp = FacetPoint.from_dict(d)
            self.facetpoints[fp.id] = fp

        for d in read(EDGES_FILE):
            edge = SemanticEdge.from_dict(d)
            self.edges[edge.id] = edge

        # 构建邻接表（加速_get_neighbors）
        self._adj = {}
        self._edge_by_nodes = {}
        for edge in self.edges.values():
            for nid in (edge.from_id, edge.to_id):
                if nid not in self._adj:
                    self._adj[nid] = []
            if edge.to_id not in self._adj[edge.from_id]:
                self._adj[edge.from_id].append(edge.to_id)
            if edge.from_id not in self._adj[edge.to_id]:
                self._adj[edge.to_id].append(edge.from_id)
            # 双向存储(from,to) -> edge
            self._edge_by_nodes[(edge.from_id, edge.to_id)] = edge

        if not self._quiet:
            print(f"📂 Loaded: {len(self.episodes)} episodes, "
                  f"{len(self.facetpoints)} facetpoints, "
                  f"{len(self.edges)} edges")

    def _search_layer(self, query: str, top_k: int = 100) -> list[tuple[str, float, str]]:
        """
        阶段1：锥尖广撒网

        在所有层同时搜索，返回 (node_id, score, layer) 元组列表
        layer: "L4_entity" | "L3_fp" | "L2_facet" | "L1_episode"
        """
        candidates = []

        # L3 FacetPoints 搜索（最可能被精确命中）
        for fp_id, fp in self.facetpoints.items():
            score = simple_vector_similarity(query, fp.keywords)
            if score > 0:
                candidates.append((fp_id, score, "L3_fp"))

        # L4 Entities 搜索（实体名匹配）
        # entities直接通过facetpoint反查，这里跳过

        # L1 Episodes 直接搜索（会被惩罚）
        for ep_id, ep in self.episodes.items():
            # 标题匹配
            title_score = keyword_match_score(query, ep.title)
            # 摘要匹配
            summary_score = keyword_match_score(query, ep.summary) * 0.7
            # Tags匹配
            tag_score = keyword_match_score(query, " ".join(ep.tags)) * 0.8

            combined = max(title_score, summary_score, tag_score)
            if combined > 0:
                ep.direct_hit = True  # 标记直接命中，会被惩罚
                candidates.append((ep_id, combined, "L1_ep"))

        # 排序并截断
        candidates.sort(key=lambda x: -x[1])
        return candidates[:top_k]

    def _get_subgraph(self, anchor_ids: list[str], direct_hit_eps: set = None) -> tuple[set, set]:
        """
        阶段2：投影到图中

        返回 (node_ids, edge_ids) — 以锚点为中心的1跳子图
        """
        node_ids = set(anchor_ids)
        # FIX: when no anchors but have direct-hit L1 eps, use them as starting points
        if not anchor_ids and direct_hit_eps:
            node_ids.update(direct_hit_eps)
        edge_ids = set()

        for edge_id, edge in self.edges.items():
            if edge.from_id in anchor_ids or (direct_hit_eps and edge.from_id in direct_hit_eps):
                node_ids.add(edge.to_id)
                edge_ids.add(edge_id)
            if edge.to_id in anchor_ids or (direct_hit_eps and edge.to_id in direct_hit_eps):
                node_ids.add(edge.from_id)
                edge_ids.add(edge_id)

        return node_ids, edge_ids

    def _get_neighbors(self, node_id: str) -> list[str]:
        """获取节点的邻居ID（O(1)邻接表查找）"""
        return self._adj.get(node_id, [])

    def _compute_edge_cost(self, edge: SemanticEdge, query: str) -> float:
        """
        计算边的代价（语义距离）

        边代价 = 边的向量距离 + 跳跃惩罚
        如果边描述与查询相关，代价低
        """
        # 边描述与查询的匹配度
        desc_score = keyword_match_score(query, edge.description)

        # 相关则代价低，不相关则代价高
        edge_cost = (1.0 - desc_score) * 0.5 + JUMP_PENALTY

        return edge_cost

    def _propagate_cost(self, query: str, subgraph_nodes: set, subgraph_edges: set, direct_hit_eps: set = None) -> dict[str, float]:
        """
        阶段3：代价传播（Bundle Search本质）

        从锥尖（锚点）向锥底（Episode）传播代价
        Episode得分 = 所有路径中最小代价
        """
        episode_scores: dict[str, float] = {}

        # 获取所有锚点（命中的FacetPoints）
        anchor_fps = [
            (fp_id, self.facetpoints[fp_id])
            for fp_id in subgraph_nodes
            if fp_id in self.facetpoints
        ]

        # 初始化锚点代价（锥尖 = 0）
        start_cost = {fp_id: 0.0 for fp_id, _ in anchor_fps}

        # BFS传播
        visited = set()
        queue = [(fp_id, 0.0) for fp_id, _ in anchor_fps]

        # FIX: If no FP anchors but have direct_hit_eps, start BFS from them
        if not queue and direct_hit_eps:
            for ep_id in direct_hit_eps:
                if ep_id in subgraph_nodes:
                    queue.append((ep_id, 0.0))

        while queue:
            node_id, current_cost = queue.pop(0)

            if node_id in visited:
                continue
            visited.add(node_id)

            # 如果是Episode，计算代价
            if node_id in self.episodes and node_id in subgraph_nodes:
                ep = self.episodes[node_id]

                # 找从锚点到这个Episode的所有路径
                # 简化为：episode得分 = min(锚点代价 + 边代价累加)
                if node_id not in episode_scores or current_cost < episode_scores[node_id]:
                    episode_scores[node_id] = current_cost

            # 传播到邻居
            neighbors = self._get_neighbors(node_id)
            for neighbor_id in neighbors:
                if neighbor_id in visited:
                    continue

                # O(1)边代价查找（邻接表已替代全量扫描）
                edge_cost = 0.0
                edge = self._edge_by_nodes.get((node_id, neighbor_id)) or self._edge_by_nodes.get((neighbor_id, node_id))
                if edge:
                    edge_cost = self._compute_edge_cost(edge, query)

                new_cost = current_cost + edge_cost
                queue.append((neighbor_id, new_cost))

        return episode_scores

    def _calculate_final_scores(self, query: str,
                                episode_scores: dict[str, float],
                                direct_hit_eps: set) -> list[Episode]:
        """
        计算最终Episode得分，应用惩罚和boost
        """
        results = []

        for ep_id, path_cost in episode_scores.items():
            ep = self.episodes[ep_id]

            # 起始代价 = 1 - 向量相似度（0-1范围，越小越好）
            start_cost = 1.0 - keyword_match_score(query, ep.summary)

            # 总代价 = 传播代价 + 起始代价
            total_cost = path_cost + start_cost * 0.3

            # 惩罚直接命中Episode摘要（防宽泛）
            if ep_id in direct_hit_eps:
                total_cost += PENALTY_DIRECT_HIT

            # Boost：有关键词命中
            matched_kw = [kw for kw in ep.tags if kw.lower() in query.lower()]
            if matched_kw:
                total_cost *= (1.0 - 0.1 * len(matched_kw))  # 每命中一个tag减10%

            ep.score = total_cost
            ep.matched_facetpoints = matched_kw
            results.append(ep)

        return results

    def _p(self, *args, **kwargs):
        """Conditional print based on quiet mode"""
        if not getattr(self, '_quiet', False):
            print(*args, **kwargs)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Bundle Search 主入口

        Args:
            query: 查询字符串
            top_k: 返回top K结果

        Returns:
            list of Episode dicts with scores
        """
        if not query.strip():
            return []

        self._p(f"\n🔍 Bundle Search: '{query}'")

        # 阶段1：锥尖广撒网
        candidates = self._search_layer(query, TOP_K_PER_LAYER)
        self._p(f"   阶段1: {len(candidates)} 个候选命中")

        if not candidates:
            self._p("   ⚠️  无候选命中，返回空")
            return []

        # 分离直接命中的Episodes
        direct_hit_eps = {c[0] for c in candidates if c[2] == "L1_ep"}
        anchor_ids = [c[0] for c in candidates if c[2] != "L1_ep"]

        # 阶段2：投影到图
        subgraph_nodes, subgraph_edges = self._get_subgraph(anchor_ids, direct_hit_eps)
        self._p(f"   阶段2: 子图 {len(subgraph_nodes)} 节点, {len(subgraph_edges)} 边")

        # 阶段3：代价传播
        episode_scores = self._propagate_cost(query, subgraph_nodes, subgraph_edges, direct_hit_eps)
        self._p(f"   阶段3: {len(episode_scores)} 个Episode在传播范围内")

        # 计算最终得分
        results = self._calculate_final_scores(query, episode_scores, direct_hit_eps)

        # 排序
        results.sort(key=lambda e: e.score)

        # 返回top_k
        top_results = results[:top_k]

        self._p(f"\n📋 Top {len(top_results)} Results:")
        for i, ep in enumerate(top_results, 1):
            self._p(f"   {i}. [{ep.score:.3f}] {ep.title}")
            print(f"      → {ep.summary[:80]}...")
            if ep.matched_facetpoints:
                print(f"      → Tags: {', '.join(ep.matched_facetpoints)}")
            print(f"      → Source: {ep.source_path}")

        return [e.to_dict() for e in top_results]


# ========== CLI ==========

def interactive_mode():
    """交互模式"""
    print("\n🧠 M-FLOW Bundle Search — Interactive Mode")
    print("Type 'quit' or 'exit' to stop\n")

    searcher = BundleSearch()

    while True:
        try:
            query = input("\n💬 Query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋")
            break

        if query.lower() in ["quit", "exit", "q"]:
            print("👋")
            break

        if not query:
            continue

        results = searcher.search(query, top_k=5)
        if not results:
            print("   No results found.")


def main():
    parser = argparse.ArgumentParser(description="M-FLOW Bundle Search")
    parser.add_argument("query", nargs="?", help="Search query string")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress status prints")
    args = parser.parse_args()

    if args.interactive or (not args.query):
        interactive_mode()
        return

    searcher = BundleSearch(quiet=args.quiet or args.json)
    import time
    t0 = time.time()
    results = searcher.search(args.query, top_k=args.top_k)
    t_search = time.time() - t0
    if not args.quiet:
        print(f"   [BundleSearch] search took {t_search:.3f}s", file=sys.stderr)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2), flush=True)
    else:
        # 默认格式化输出
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['title']} [score={r['score']}]")
            print(f"   {r['summary'][:100]}...")
            if r['tags']:
                print(f"   Tags: {', '.join(r['tags'])}")
            if r['matched_facetpoints']:
                print(f"   Matched: {', '.join(r['matched_facetpoints'])}")
            print(f"   → {r['source_path']}")


if __name__ == "__main__":
    main()
