"""Topic 依赖图与学习路径推荐

功能：
1. 从已处理视频的 summary 中提取 Topic 标签
2. 维护 Topic 依赖关系（prerequisites → topic）
3. 基于依赖图推荐学习路径
4. 冷启动时自动 fallback 到随机选择
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class TopicNode:
    """单个 Topic 节点"""
    name: str
    depends_on: list[str] = field(default_factory=list)  # 前置 Topic
    unlocks: list[str] = field(default_factory=list)    # 可解锁的 Topic
    description: str = ""
    video_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LearningPathItem:
    """学习路径中的单个推荐"""
    bvid: str
    title: str
    topic: str
    reason: str


@dataclass
class TopicGraph:
    """Topic 依赖图"""
    topics: dict[str, TopicNode] = field(default_factory=dict)
    # video_topics: {bvid: [topic1, topic2, ...]}
    video_topics: dict[str, list[str]] = field(default_factory=dict)
    # video_metadata: {bvid: {title, processed_at, ...}}
    video_metadata: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "TopicGraph":
        """从文件加载依赖图"""
        if not path.exists():
            return cls()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                topics={
                    k: TopicNode(**v) for k, v in data.get("topics", {}).items()
                },
                video_topics=data.get("video_topics", {}),
                video_metadata=data.get("video_metadata", {}),
            )
        except (json.JSONDecodeError, TypeError):
            return cls()

    def save(self, path: Path):
        """保存依赖图到文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "topics": {k: v.to_dict() for k, v in self.topics.items()},
            "video_topics": self.video_topics,
            "video_metadata": self.video_metadata,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ── Topic 注册 ──

    def register_video(
        self, bvid: str, title: str, topics: list[str], metadata: dict | None = None
    ):
        """注册视频及其 Topic"""
        self.video_topics[bvid] = topics
        self.video_metadata[bvid] = {
            "title": title,
            "topics": topics,
            **(metadata or {}),
        }
        for topic in topics:
            if topic not in self.topics:
                self.topics[topic] = TopicNode(name=topic)
            self.topics[topic].video_count += 1

    def add_dependency(self, topic: str, depends_on: str):
        """添加 Topic 依赖关系"""
        if topic not in self.topics:
            self.topics[topic] = TopicNode(name=topic)
        if depends_on not in self.topics:
            self.topics[depends_on] = TopicNode(name=depends_on)

        if depends_on not in self.topics[topic].depends_on:
            self.topics[topic].depends_on.append(depends_on)
        if topic not in self.topics[depends_on].unlocks:
            self.topics[depends_on].unlocks.append(topic)

    def infer_dependencies_from_summary(
        self, bvid: str, prerequisites_text: str
    ):
        """
        从 prerequisites_cn 文本中推断 Topic 依赖关系
        例如 prerequisites="需要了解 Python 异步编程基础" → 依赖 "Python 异步编程"
        """
        if not prerequisites_text:
            return
        # 已知 Topic 列表用于匹配
        known_topics = list(self.topics.keys())
        if not known_topics:
            return

        # 简单关键词匹配（后续可用 LLM 增强）
        for topic in known_topics:
            if topic in prerequisites_text and bvid in self.video_topics:
                if topic not in self.video_topics[bvid]:
                    self.add_dependency(self.video_topics[bvid][0], topic)

    # ── 学习路径推荐 ──

    def get_learning_path(
        self,
        mastered_bvids: set[str],
        candidate_bvids: set[str],
        max_results: int = 5,
    ) -> list[LearningPathItem]:
        """
        基于前置知识推荐学习路径

        Args:
            mastered_bvids: 已掌握的 BV 号集合
            candidate_bvids: 候选视频 BV 号集合

        Returns:
            按推荐优先级排序的 [(bvid, title, topic, reason), ...]
        """
        if not candidate_bvids:
            return []

        # 获取已掌握的所有 Topic
        mastered_topics: set[str] = set()
        for bvid in mastered_bvids:
            mastered_topics.update(self.video_topics.get(bvid, []))

        candidates: list[tuple[str, LearningPathItem]] = []

        for bvid in candidate_bvids:
            topics = self.video_topics.get(bvid, [])
            metadata = self.video_metadata.get(bvid, {})
            title = metadata.get("title", bvid)

            if not topics:
                # 无 Topic 标签，冷启动 fallback
                candidates.append((
                    bvid,
                    LearningPathItem(bvid=bvid, title=title, topic="", reason="知识图谱尚无数据，随机推荐"),
                ))
                continue

            # 检查前置知识是否满足
            all_deps_met = True
            for topic in topics:
                node = self.topics.get(topic)
                if node and node.depends_on:
                    for dep in node.depends_on:
                        if dep not in mastered_topics:
                            all_deps_met = False
                            break
                    if not all_deps_met:
                        break

            if all_deps_met:
                reason = "前置知识已满足，可直接学习"
                candidates.append((
                    bvid,
                    LearningPathItem(bvid=bvid, title=title, topic=", ".join(topics), reason=reason),
                ))
            else:
                # 找出缺失的前置 Topic
                missing = []
                for topic in topics:
                    node = self.topics.get(topic)
                    if node:
                        for dep in node.depends_on:
                            if dep not in mastered_topics:
                                missing.append(dep)
                if missing:
                    candidates.append((
                        bvid,
                        LearningPathItem(
                            bvid=bvid,
                            title=title,
                            topic=", ".join(topics),
                            reason=f"建议先学习：{', '.join(missing)}",
                        ),
                    ))

        # 排序：前置已满足的优先，其次按 video_count（Topic 热度）
        def sort_key(item: tuple[str, LearningPathItem]) -> tuple[int, int]:
            _, lpi = item
            primary_topic = lpi.topic.split(",")[0].strip() if lpi.topic else ""
            node = self.topics.get(primary_topic)
            video_count = node.video_count if node else 0
            is_ready = 1 if "前置知识已满足" in lpi.reason else 0
            return (is_ready, video_count)

        candidates.sort(key=sort_key, reverse=True)
        return [item for _, item in candidates[:max_results]]

    def get_topic_stats(self) -> dict:
        """获取 Topic 图谱统计"""
        return {
            "total_topics": len(self.topics),
            "total_videos": len(self.video_topics),
            "topic_list": [
                {"name": name, "video_count": node.video_count, "depends_on": node.depends_on}
                for name, node in sorted(self.topics.items(), key=lambda x: -x[1].video_count)
            ],
        }


# ──────────────────────────────────────────────
# LLM Topic 提取（可选功能）
# ──────────────────────────────────────────────

TOPIC_EXTRACT_PROMPT = """从以下视频信息中提取 3-5 个核心 topic 标签。

标题：{title}
总结：{summary}
前置知识：{prerequisites}

要求：
- 使用标准化的 topic 名称（如"Python异步编程"、"Docker容器化"、"考研政治"）
- 只返回 topic 名称，每行一个，不要其他说明

返回格式（JSON数组）：
["topic1", "topic2", "topic3"]
"""


def extract_topics_from_summary(
    title: str,
    summary: str,
    prerequisites: str,
    llm_caller=None,
) -> list[str]:
    """从总结中提取 Topic（需 LLM）"""
    if not llm_caller:
        return []

    prompt = TOPIC_EXTRACT_PROMPT.format(
        title=title,
        summary=summary[:500],
        prerequisites=prerequisites or "无",
    )

    try:
        response = llm_caller(prompt).strip()
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        data = json.loads(response)
        return [t.strip() for t in data if t.strip()]
    except Exception:
        return []


def load_or_build_graph(data_dir: Path) -> TopicGraph:
    """加载或新建 Topic 依赖图"""
    graph_path = data_dir / "topic_graph.json"
    return TopicGraph.load(graph_path)
