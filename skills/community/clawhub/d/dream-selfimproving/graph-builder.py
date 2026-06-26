#!/usr/bin/env python3
"""
graph-builder.py — M-FLOW 图结构构建器

从 dream skill 的日志和 topic 文件构建倒锥知识图谱：
- L4 Entity: 用户/项目/系统/技能等实体
- L3 FacetPoint: 具体属性标签（type + topic + keywords向量）
- L2 Facet: 一组相关特征
- L1 Episode: daily log / topic file

Usage:
    python graph-builder.py --build              # 全量重建
    python graph-builder.py --update             # 增量更新今日日志
    python graph-builder.py --status             # 显示图状态
"""

import json, os, re, sys, hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ========== 配置 ==========

# 自动检测workspace：优先环境变量，否则从脚本位置推断
_env = os.environ.get("OPENCLAW_WORKSPACE", "")
if _env:
    WORKSPACE = Path(_env)
else:
    # 从脚本路径推断: .../skills/dream/graph-builder.py → .../workspace
    WORKSPACE = Path(__file__).resolve().parents[2]
    # 兼容性：如果不在预期位置，尝试常见路径
    if not (WORKSPACE / "memory").exists():
        WORKSPACE = Path(os.environ.get("USERPROFILE", "/")) / ".openclaw" / "workspace"
    if not (WORKSPACE / "memory").exists():
        WORKSPACE = Path.home() / ".openclaw" / "workspace"

print(f"   [GraphBuilder] WORKSPACE: {WORKSPACE}", file=sys.stderr)

GRAPH_DIR = WORKSPACE / "memory" / "graph"
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

# 图数据文件
ENTITIES_FILE = GRAPH_DIR / "entities.json"
FACETPOINTS_FILE = GRAPH_DIR / "facetpoints.json"
FACETS_FILE = GRAPH_DIR / "facets.json"
EPISODES_FILE = GRAPH_DIR / "episodes.json"
EDGES_FILE = GRAPH_DIR / "edges.json"
INDEX_FILE = GRAPH_DIR / "index.json"

# 其他目录
LOGS_DIR = WORKSPACE / "memory" / "logs"
TOPICS_DIR = WORKSPACE / "memory" / "topics"
PATTERNS_DIR = WORKSPACE / "memory" / "patterns"
RECALL_FILE = WORKSPACE / "memory" / ".dreams" / "short-term-recall.json"


# ========== 数据结构 ==========

class GraphNode:
    """M-FLOW 图节点基类"""
    def __init__(self, id: str, label: str, layer: str):
        self.id = id
        self.label = label
        self.layer = layer  # L1/L2/L3/L4
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        node = cls(d["id"], d.get("label", ""), d.get("layer", ""))
        for k, v in d.items():
            if k not in ["id", "label", "layer"]:
                setattr(node, k, v)
        return node


class Entity(GraphNode):
    """L4 Entity — 用户/项目/系统/技能"""
    def __init__(self, id: str, name: str, entity_type: str, description: str = ""):
        super().__init__(id, name, "L4")
        self.entity_type = entity_type  # user / project / tool / skill / system
        self.description = description
        self.facetpoint_ids: list[str] = []
    @classmethod
    def from_dict(cls, d):
        node = cls(d["id"], d.get("name",""), d.get("entity_type",""), d.get("description",""))
        for k, v in d.items():
            if k not in ["id","name","entity_type","description"]:
                setattr(node, k, v)
        return node


class FacetPoint(GraphNode):
    """L3 FacetPoint — 具体属性标签"""
    def __init__(self, id: str, label: str, keywords: list[str], entity_id: str):
        super().__init__(id, label, "L3")
        self.keywords = keywords  # 向量化锚点（词袋）
        self.entity_id = entity_id
        self.facet_id: Optional[str] = None
        self.episode_ids: list[str] = []

    @classmethod
    def from_dict(cls, d):
        # FacetPoint 需要4个构造参数，覆盖父类的from_dict
        node = cls(d["id"], d.get("label",""), d.get("keywords",[]), d.get("entity_id",""))
        for k, v in d.items():
            if k not in ["id","label","keywords","entity_id"]:
                setattr(node, k, v)
        return node


class Facet(GraphNode):
    """L2 Facet — 一组相关特征"""
    def __init__(self, id: str, label: str, facet_type: str):
        super().__init__(id, label, "L2")
        self.facet_type = facet_type  # correction / error / project / preference
        self.facetpoint_ids: list[str] = []
        self.episode_ids: list[str] = []
    @classmethod
    def from_dict(cls, d):
        node = cls(d["id"], d.get("label",""), d.get("facet_type",""))
        for k, v in d.items():
            if k not in ["id","label","facet_type"]:
                setattr(node, k, v)
        return node


class Episode(GraphNode):
    """L1 Episode — 最终知识单元（daily log / topic file）"""
    def __init__(self, id: str, title: str, episode_type: str, source_path: str):
        super().__init__(id, title, "L1")
        self.episode_type = episode_type  # daily_log / topic / pattern
        self.source_path = source_path
        self.title: str = title  # 显式保存到实例，避免父类init丢失
        self.summary: str = ""
        self.facetpoint_ids: list[str] = []
        self.facet_ids: list[str] = []
        self.tags: list[str] = []
        self.importance: float = 1.0
        self.direct_hit: bool = False  # 是否被直接命中（用于惩罚）
    @classmethod
    def from_dict(cls, d):
        node = cls(d["id"], d.get("title",""), d.get("episode_type",""), d.get("source_path",""))
        for k, v in d.items():
            if k not in ["id","title","episode_type","source_path"]:
                setattr(node, k, v)
        return node


class SemanticEdge:
    """语义边 — 带描述的边"""
    def __init__(self, id: str, from_id: str, to_id: str, description: str, edge_type: str):
        self.id = id
        self.from_id = from_id  # L3/L2 → L1
        self.to_id = to_id
        self.description = description  # 语义描述（参与向量检索）
        self.edge_type = edge_type  # belongs_to / relates_to / part_of
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        edge = cls(d["id"], d.get("from_id", ""), d.get("to_id", ""),
                   d.get("description", ""), d.get("edge_type", ""))
        for k, v in d.items():
            if k not in ["id", "from_id", "to_id", "description", "edge_type"]:
                setattr(edge, k, v)
        return edge


# ========== 图构建器 ==========

class MFlowGraphBuilder:
    """M-FLOW 倒锥图构建器"""

    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.facetpoints: dict[str, FacetPoint] = {}
        self.facets: dict[str, Facet] = {}
        self.episodes: dict[str, Episode] = {}
        self.edges: dict[str, SemanticEdge] = {}
        self._load()

    def _load(self):
        """从文件加载现有图数据（兼容GBK旧文件）"""
        def read_json(path):
            if not path.exists():
                return []
            raw = path.read_bytes()
            for enc in ['utf-8', 'gbk', 'latin1']:
                try:
                    return json.loads(raw.decode(enc))
                except Exception:
                    continue
            return []

        for d in read_json(ENTITIES_FILE):
            e = Entity.from_dict(d)
            self.entities[e.id] = e
        for d in read_json(FACETPOINTS_FILE):
            fp = FacetPoint.from_dict(d)
            self.facetpoints[fp.id] = fp
        for d in read_json(FACETS_FILE):
            f = Facet.from_dict(d)
            self.facets[f.id] = f
        for d in read_json(EPISODES_FILE):
            ep = Episode.from_dict(d)
            self.episodes[ep.id] = ep
        for d in read_json(EDGES_FILE):
            edge = SemanticEdge.from_dict(d)
            self.edges[edge.id] = edge

    def _save(self):
        """持久化图数据（强制UTF-8）"""
        def w(path, data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        w(ENTITIES_FILE, [e.to_dict() for e in self.entities.values()])
        w(FACETPOINTS_FILE, [fp.to_dict() for fp in self.facetpoints.values()])
        w(FACETS_FILE, [f.to_dict() for f in self.facets.values()])
        w(EPISODES_FILE, [ep.to_dict() for ep in self.episodes.values()])
        w(EDGES_FILE, [e.to_dict() for e in self.edges.values()])

    def _make_id(self, prefix: str, name: str) -> str:
        """生成唯一ID"""
        h = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"{prefix}-{h}"

    def _read_file_content(self, path: Path) -> str:
        """读取文件内容"""
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return ""

    # ---- Episode 构建 ----

    def add_episode_from_log(self, log_path: Path) -> Episode:
        """从daily log文件构建Episode"""
        date_str = log_path.stem  # YYYY-MM-DD
        content = self._read_file_content(log_path)

        # 提取摘要（取前200字）
        summary = content[:200].strip().replace("#", "").replace("##", "")

        # 判断类型
        episode_type = "daily_log"

        # 生成tags
        tags = []
        if "correction" in content.lower():
            tags.append("correction")
        if "error" in content.lower():
            tags.append("error")
        if "decision" in content.lower():
            tags.append("decision")
        if "insight" in content.lower():
            tags.append("insight")

        episode = Episode(
            id=f"ep-log-{date_str}",
            title=f"Daily Log {date_str}",
            episode_type=episode_type,
            source_path=str(log_path)
        )
        episode.summary = summary
        episode.tags = tags

        self.episodes[episode.id] = episode
        return episode

    def add_episode_from_topic(self, topic_path: Path) -> Episode:
        """从topic文件构建Episode"""
        content = self._read_file_content(topic_path)
        name = topic_path.stem

        # 解析frontmatter
        frontmatter = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        frontmatter[k.strip()] = v.strip()

        title = frontmatter.get("title", name)
        episode_type = frontmatter.get("type", "topic")
        tags = frontmatter.get("tags", "").split(",") if frontmatter.get("tags") else []
        summary = content[:300].strip()

        episode = Episode(
            id=f"ep-topic-{name}",
            title=title,
            episode_type=episode_type,
            source_path=str(topic_path)
        )
        episode.summary = summary
        episode.tags = [t.strip() for t in tags if t.strip()]

        self.episodes[episode.id] = episode
        return episode

    # ---- FacetPoint 构建 ----

    def _extract_facetpoints_from_episode(self, episode: Episode, content: str) -> list[FacetPoint]:
        """从Episode内容提取FacetPoints"""
        fps = []
        tags = getattr(episode, "tags", [])

        # 从tags生成FacetPoints
        for tag in tags:
            if not tag:
                continue
            fp_id = self._make_id("fp", f"{episode.id}-{tag}")
            fp = FacetPoint(
                id=fp_id,
                label=tag,
                keywords=[tag],
                entity_id=""  # 待后续关联
            )
            fp.episode_ids.append(episode.id)
            episode.facetpoint_ids.append(fp_id)
            fps.append(fp)

        # 从内容提取关键词作为FacetPoints
        words = re.findall(r'\b\w{4,}\b', content.lower())
        word_freq = {}
        for w in words:
            word_freq[w] = word_freq.get(w, 0) + 1

        # 取最高频的5个词作为FacetPoints
        top_words = sorted(word_freq.items(), key=lambda x: -x[1])[:5]
        for word, freq in top_words:
            if word in ["error", "correction", "decision", "insight", "completed"]:
                continue
            fp_id = self._make_id("fp", f"{episode.id}-{word}")
            if fp_id not in self.facetpoints:
                fp = FacetPoint(
                    id=fp_id,
                    label=word,
                    keywords=[word],
                    entity_id=""
                )
                fp.episode_ids.append(episode.id)
                episode.facetpoint_ids.append(fp_id)
                fps.append(fp)

        return fps

    # ---- Facet 构建 ----

    def add_facet_for_type(self, episode: Episode, facet_type: str) -> Optional[Facet]:
        """为特定类型创建Facet"""
        facet_id = self._make_id("facet", f"{facet_type}")
        if facet_id in self.facets:
            facet = self.facets[facet_id]
        else:
            facet = Facet(id=facet_id, label=facet_type, facet_type=facet_type)
            self.facets[facet_id] = facet

        # 关联Episode
        if episode.id not in facet.episode_ids:
            facet.episode_ids.append(episode.id)
        if episode.id not in episode.facet_ids:
            episode.facet_ids.append(facet_id)

        return facet

    # ---- Entity 构建 ----

    def ensure_user_entity(self, user_name: str = "luyi") -> Entity:
        """确保用户Entity存在"""
        entity_id = f"entity-user-{user_name}"
        if entity_id in self.entities:
            return self.entities[entity_id]

        entity = Entity(
            id=entity_id,
            name=user_name,
            entity_type="user",
            description=f"用户 {user_name}"
        )
        self.entities[entity_id] = entity
        return entity

    def ensure_project_entities(self):
        """从目录结构推断项目Entity"""
        # 从topics目录推断
        if TOPICS_DIR.exists():
            for d in TOPICS_DIR.iterdir():
                if d.is_dir() or d.suffix == ".md":
                    name = d.stem
                    if name.startswith("project_"):
                        proj_name = name.replace("project_", "")
                        entity_id = self._make_id("entity", f"project-{proj_name}")
                        if entity_id not in self.entities:
                            entity = Entity(
                                id=entity_id,
                                name=proj_name,
                                entity_type="project",
                                description=f"项目: {proj_name}"
                            )
                            self.entities[entity_id] = entity

    # ---- 边构建 ----

    def add_semantic_edge(self, from_id: str, to_id: str, description: str,
                          edge_type: str = "belongs_to") -> SemanticEdge:
        """添加语义边"""
        edge_id = self._make_id("edge", f"{from_id}-{to_id}")
        if edge_id in self.edges:
            return self.edges[edge_id]

        edge = SemanticEdge(
            id=edge_id,
            from_id=from_id,
            to_id=to_id,
            description=description,
            edge_type=edge_type
        )
        self.edges[edge_id] = edge
        return edge

    def link_facetpoint_to_facet(self, fp_id: str, facet_id: str, description: str = ""):
        """连接FacetPoint到Facet"""
        if fp_id in self.facetpoints and facet_id in self.facets:
            fp = self.facetpoints[fp_id]
            if fp.facet_id is None:
                fp.facet_id = facet_id
            if fp_id not in self.facets[facet_id].facetpoint_ids:
                self.facets[facet_id].facetpoint_ids.append(fp_id)

            desc = description or f"{fp.label} 属于 {self.facets[facet_id].label}"
            self.add_semantic_edge(fp_id, facet_id, desc, "belongs_to")

    def link_facetpoint_to_episode(self, fp_id: str, episode_id: str, description: str = ""):
        """连接FacetPoint到Episode"""
        if fp_id in self.facetpoints and episode_id in self.episodes:
            fp = self.facetpoints[fp_id]
            if episode_id not in fp.episode_ids:
                fp.episode_ids.append(episode_id)
            if fp_id not in self.episodes[episode_id].facetpoint_ids:
                self.episodes[episode_id].facetpoint_ids.append(fp_id)

            desc = description or f"{fp.label} 出现在 {self.episodes[episode_id].title}"
            self.add_semantic_edge(fp_id, episode_id, desc, "appears_in")

    def link_facet_to_episode(self, facet_id: str, episode_id: str, description: str = ""):
        """连接Facet到Episode"""
        if facet_id in self.facets and episode_id in self.episodes:
            if episode_id not in self.facets[facet_id].episode_ids:
                self.facets[facet_id].episode_ids.append(episode_id)
            if facet_id not in self.episodes[episode_id].facet_ids:
                self.episodes[episode_id].facet_ids.append(facet_id)

            desc = description or f"{self.facets[facet_id].label} 相关于 {self.episodes[episode_id].title}"
            self.add_semantic_edge(facet_id, episode_id, desc, "relates_to")

    # ---- 从Recall Store富化 ----

    def enrich_from_recall(self, top_n: int = 200, min_recall: int = 0, min_score: float = 0.5):
        """
        从OpenClaw Recall Store (short-term-recall.json) 富化FacetPoints。
        conceptTags → 直接作为FacetPoint的keywords，复用已有标签系统。
        """
        if not RECALL_FILE.exists():
            print(f"   ⚠️  Recall file not found: {RECALL_FILE}")
            return

        import json
        try:
            data = json.loads(RECALL_FILE.read_text(encoding='utf-8'))
        except Exception:
            try:
                raw = RECALL_FILE.read_bytes()
                for enc in ['utf-8', 'gbk']:
                    try:
                        data = json.loads(raw.decode(enc))
                        break
                    except Exception:
                        continue
            except Exception as e:
                print(f"   ⚠️  Recall file read failed: {e}")
                return

        entries = data.get('entries', {})
        if isinstance(entries, dict):
            entries = list(entries.values())

        print(f"   📂 Recall entries: {len(entries)}")

        # 过滤+排序
        filtered = []
        for e in entries:
            if isinstance(e, dict):
                recall_count = e.get('recallCount', 0)
                total_score = e.get('totalScore', 0.0)
                concept_tags = e.get('conceptTags', [])
                if recall_count >= min_recall and total_score >= min_score and concept_tags:
                    filtered.append((total_score + recall_count * 0.1, e))


        filtered.sort(key=lambda x: x[0], reverse=True)
        filtered = filtered[:top_n]
        print(f"   🎯 Top entries: {len(filtered)}")


        # 确保user entity存在
        user_entity = self.ensure_user_entity("luyi")


        # 从每条entry构建/增强FacetPoint
        recall_fps = 0
        recall_eps = 0
        recall_keywords_merged = 0
        for score, e in filtered:
            path = e.get('path', '')
            concept_tags = e.get('conceptTags', [])
            snippet = e.get('snippet', '')[:200]

            for tag in concept_tags:
                # 跳过系统级高频标签
                if tag.lower() in ('assistant', 'user', 'untrusted', 'metadata', 'conversation', 'message-id', 'openclaw-weixin'):
                    continue

                tag_clean = re.sub(r'[^\w\u4e00-\u9fff-]', '_', tag)[:40]
                fp_id = f"fp-recall-{tag_clean}"


                # 已有FacetPoint → 补充keywords
                if fp_id in self.facetpoints:
                    fp = self.facetpoints[fp_id]
                    merged = 0
                    for kw in concept_tags:
                        if kw not in fp.keywords:
                            fp.keywords.append(kw)
                            merged += 1
                    recall_keywords_merged += merged
                    continue

                # 新建FacetPoint + Episode（同一个tag的多个conceptTags共享同一EP）
                source_short = path.split('/')[-1].replace('.md', '') if path else 'unknown'
                ep_id = f"ep-recall-{source_short}-{hash(tag) % 9999:04d}"
                title = f"Recall:{tag[:30]}"

                # Episode（如果不存在同名，先创建）
                ep_created = False
                if ep_id not in self.episodes:
                    ep = Episode(
                        id=ep_id, title=title,
                        episode_type="recall",
                        source_path=f"recall:{path}"
                    )
                    ep.summary = snippet
                    ep.tags = [t for t in concept_tags if len(t) < 30][:10]
                    ep.recallCount = e.get('recallCount', 0)
                    ep.totalScore = score
                    self.episodes[ep_id] = ep
                    ep_created = True
                else:
                    ep = self.episodes[ep_id]

                fp = FacetPoint(
                    id=fp_id, label=tag[:40],
                    keywords=list(concept_tags)[:20],
                    entity_id=user_entity.id
                )
                fp.episode_ids = [ep_id]
                self.facetpoints[fp_id] = fp

                # 链接
                self.link_facetpoint_to_episode(fp_id, ep_id)
                recall_fps += 1
                if ep_created:
                    recall_eps += 1

        print(f"   ✅ Recall: {recall_fps} FPs (+{recall_keywords_merged} kw-merged), {recall_eps} EPs")


    # ---- 全量构建 ----



    def enrich_from_errors(self):
        """从 .learnings/ERRORS.md 读取 pending 条目，生成 FacetPoints + Episodes"""
        import re
        err_file = WORKSPACE / '.learnings' / 'ERRORS.md'
        if not err_file.exists():
            print(f"   [i] .learnings/ERRORS.md not found, skipping")
            return

        content = err_file.read_text(encoding='utf-8', errors='replace')
        entries = []
        current = {}
        in_error = False

        for line in content.split('\n'):
            if line.startswith('## [ERR-'):
                if current:
                    entries.append(current)
                parts = line.strip().split('] ', 1)
                if len(parts) == 2:
                    err_id = parts[0].lstrip('## [')
                    title = parts[1]
                    current = {'id': err_id, 'title': title, 'status': 'unknown',
                               'summary': '', 'error_type': 'unknown'}
                    in_error = True
                else:
                    in_error = False
                    current = {}
            elif in_error:
                if '**Status**:' in line:
                    current['status'] = line.split('**Status**:', 1)[1].strip()
                elif '**Summary**' in line:
                    txt = line.split('**Summary**', 1)[1].lstrip(' *').strip()
                    current['summary'] = txt
                elif '**Error Type**' in line or '**Category**' in line:
                    txt = line.split('**', 1)[-1].strip()
                    current['error_type'] = txt

        if current:
            entries.append(current)

        pending = [e for e in entries if e.get('status', '').lower() == 'pending']
        print(f"   \U0001f4e6 .learnings/ERRORS.md: {len(pending)} pending errors")

        if not pending:
            return

        user_entity = self.ensure_user_entity("luyi")
        fps_created = 0
        eps_created = 0

        for err in pending:
            err_id = err.get('id', '')
            title = err.get('title', '')
            summary = (err.get('summary') or '').strip()
            err_type = err.get('error_type', 'unknown')

            keywords = []
            for word in re.findall(r'[A-Za-z_]+', title):
                if len(word) >= 2:
                    keywords.append(word.lower())
            for word in re.findall(r'[A-Za-z_]+', summary[:100]):
                if len(word) >= 3:
                    keywords.append(word.lower())
            if err_type not in ('unknown', ''):
                keywords.append(err_type.lower())

            seen = set()
            unique_keywords = []
            for kw in keywords:
                k = kw.lower()
                if k not in seen and k not in ('unknown', 'pending', ''):
                    seen.add(k)
                    unique_keywords.append(k)
            if not unique_keywords:
                unique_keywords = ['error', 'pending']

            fp_id = "fp-error-" + err_id.lower().replace('-', '_')
            ep_id = "ep-error-" + err_id.lower().replace('-', '_')
            fp_label = title[:40] if title else err_id

            ep = Episode(
                id=ep_id,
                title="Error: " + title[:50],
                episode_type="error",
                source_path="error:" + err_id
            )
            ep.summary = summary[:200] if summary else title
            ep.tags = unique_keywords[:10]
            self.episodes[ep_id] = ep
            eps_created += 1

            fp = FacetPoint(
                id=fp_id,
                label=fp_label,
                keywords=unique_keywords[:20],
                entity_id=user_entity.id
            )
            fp.episode_ids = [ep_id]
            self.facetpoints[fp_id] = fp
            fps_created += 1

            self.link_facetpoint_to_episode(fp_id, ep_id)

        print(f"   \u2705 Errors: {fps_created} FPs, {eps_created} EPs")


    def build_all(self):
        """从零构建完整图结构"""
        print("🔨 Building M-FLOW graph...")

        # 1. 构建Episodes (L1)
        print("  📄 Building Episodes...")

        # Daily logs
        if LOGS_DIR.exists():
            for ym_dir in LOGS_DIR.rglob("*"):
                if ym_dir.is_dir():
                    for log_file in ym_dir.glob("*.md"):
                        self.add_episode_from_log(log_file)

        # Topics
        if TOPICS_DIR.exists():
            for topic_file in TOPICS_DIR.glob("*.md"):
                self.add_episode_from_topic(topic_file)

        # Patterns
        if PATTERNS_DIR.exists():
            for pattern_file in PATTERNS_DIR.glob("*.md"):
                ep = self.add_episode_from_topic(pattern_file)
                ep.episode_type = "pattern"

        print(f"    → {len(self.episodes)} Episodes built")

        # 2. 构建Facets (L2)
        print("  🏷️  Building Facets...")

        type_facets = {}
        for ep in self.episodes.values():
            for tag in ep.tags:
                if tag not in type_facets:
                    facet = self.add_facet_for_type(ep, tag)
                    type_facets[tag] = facet

        print(f"    → {len(self.facets)} Facets built")

        # 3. 构建FacetPoints (L3)
        print("  🪬  Building FacetPoints...")

        fp_count = 0
        for ep in self.episodes.values():
            content = self._read_file_content(Path(ep.source_path))
            fps = self._extract_facetpoints_from_episode(ep, content)
            for fp in fps:
                if fp.id not in self.facetpoints:
                    self.facetpoints[fp.id] = fp
                    fp_count += 1

                # 链接到Episode
                self.link_facetpoint_to_episode(fp.id, ep.id)

                # 链接到Facet
                for tag in ep.tags:
                    if tag in type_facets:
                        self.link_facetpoint_to_facet(fp.id, type_facets[tag].id)

        print(f"    → {fp_count} FacetPoints built")

        # 4. 构建Entities (L4)
        print("  🎯 Building Entities...")

        self.ensure_user_entity()
        self.ensure_project_entities()

        # 为correction/error相关FacetPoints关联user entity
        if "entity-user-luyi" in self.entities:
            user_entity = self.entities["entity-user-luyi"]
            for fp in self.facetpoints.values():
                if fp.entity_id == "" and fp.label in ["correction", "error", "insight"]:
                    fp.entity_id = user_entity.id
                    if fp.id not in user_entity.facetpoint_ids:
                        user_entity.facetpoint_ids.append(fp.id)

        print(f"    → {len(self.entities)} Entities built")

        # 5. 保存
        print("  💾 Saving graph...")
        self._save()

        print(f"\n✅ Graph built: {len(self.entities)} entities, "
              f"{len(self.facetpoints)} facetpoints, "
              f"{len(self.facets)} facets, "
              f"{len(self.episodes)} episodes, "
              f"{len(self.edges)} edges")

    # ---- 增量更新 ----

    def update_today(self):
        """增量更新今日日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = LOGS_DIR / datetime.now().strftime("%Y") / datetime.now().strftime("%m") / f"{today}.md"

        if not log_path.exists():
            print(f"⚠️  No log for today: {log_path}")
            return

        episode_id = f"ep-log-{today}"
        if episode_id in self.episodes:
            print(f"ℹ️  Episode {episode_id} already exists, rebuilding...")
            del self.episodes[episode_id]

        episode = self.add_episode_from_log(log_path)
        content = self._read_file_content(log_path)
        fps = self._extract_facetpoints_from_episode(episode, content)

        for fp in fps:
            if fp.id not in self.facetpoints:
                self.facetpoints[fp.id] = fp
            self.link_facetpoint_to_episode(fp.id, episode.id)

        # 重建今日相关的边
        for tag in episode.tags:
            facet = self.add_facet_for_type(episode, tag)
            self.link_facet_to_episode(facet.id, episode.id)

        self._save()
        print(f"✅ Updated: {episode_id} with {len(fps)} FacetPoints")

    # ---- 状态显示 ----

    def status(self):
        """显示图状态"""
        print("\n📊 M-FLOW Graph Status")
        print(f"   Entities:     {len(self.entities)}")
        print(f"   FacetPoints: {len(self.facetpoints)}")
        print(f"   Facets:      {len(self.facets)}")
        print(f"   Episodes:    {len(self.episodes)}")
        print(f"   Edges:       {len(self.edges)}")

        # 计算连通性
        connected = sum(1 for e in self.episodes.values() if e.facetpoint_ids or e.facet_ids)
        print(f"   Connectivity: {connected}/{len(self.episodes)} Episodes linked")

        # 计算平均路径长度（简化估算）
        if self.edges:
            avg_edges_per_ep = sum(
                len(e.facetpoint_ids) + len(e.facet_ids)
                for e in self.episodes.values()
            ) / max(1, len(self.episodes))
            print(f"   Avg edges/Episode: {avg_edges_per_ep:.2f}")


# ========== CLI ==========

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="M-FLOW Graph Builder")
    parser.add_argument("--build", action="store_true", help="Full graph rebuild")
    parser.add_argument("--update", action="store_true", help="Incrementally update today")
    parser.add_argument("--status", action="store_true", help="Show graph status")
    parser.add_argument("--enrich-from-recall", action="store_true", help="Enrich graph from OpenClaw Recall Store")
    parser.add_argument("--recall-top", type=int, default=200, help="Max recall entries to process")
    parser.add_argument("--enrich-from-errors", action="store_true", help="Enrich graph from .learnings/ERRORS.md")
    parser.add_argument("--recall-min-score", type=float, default=0.5, help="Min recall totalScore")
    args = parser.parse_args()

    builder = MFlowGraphBuilder()

    if args.status:
        builder.status()
    elif args.update:
        builder.update_today()
    elif args.build:
        builder.build_all()
        if args.enrich_from_recall:
            print("  📦 Enriching from Recall Store...")
            builder.enrich_from_recall(top_n=args.recall_top, min_score=args.recall_min_score)
            if args.enrich_from_errors:
                print("  \U0001f4e6 Enriching from .learnings/ERRORS.md...")
                builder.enrich_from_errors()
            builder._save()
    else:
        parser.print_help()
