#!/usr/bin/env python3
"""
记忆知识图谱构建模块
分析记忆之间的关联关系，构建知识图谱，支持推理和发现
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque


class KnowledgeGraph:
    """
    记忆知识图谱

    功能：
    1. 提取实体和关系
    2. 构建图谱结构
    3. 关联推理
    4. 模式发现
    5. 路径查询
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.graph = defaultdict(set)  # adjacency list: entity -> related entities
        self.entity_types = {}  # entity -> type
        self.relationships = []  # list of (entity1, relation, entity2)
        self.memory_index = {}  # entity -> list of memory IDs

    def build_from_memories(self, memories: List[Dict]) -> Dict:
        """
        从记忆列表构建知识图谱

        Args:
            memories: 记忆列表

        Returns:
            图谱统计信息
        """
        stats = {
            "entities": 0,
            "relationships": 0,
            "clusters": 0
        }

        for memory in memories:
            content = memory.get("content", "")
            memory_id = memory.get("id", str(len(self.relationships)))

            # 提取实体
            entities = self._extract_entities(content)

            # 记录实体类型
            for entity in entities:
                entity_type = self._infer_entity_type(entity, content)
                self.entity_types[entity] = entity_type

                # 建立索引
                if entity not in self.memory_index:
                    self.memory_index[entity] = []
                self.memory_index[entity].append(memory_id)

                stats["entities"] += 1

            # 提取关系
            relations = self._extract_relationships(content, entities)
            for rel in relations:
                entity1, relation_type, entity2 = rel
                self.graph[entity1].add((entity2, relation_type))
                self.graph[entity2].add((entity1, relation_type))
                self.relationships.append((entity1, relation_type, entity2))
                stats["relationships"] += 1

        # 计算聚类
        stats["clusters"] = self._count_clusters()

        return stats

    def find_related_memories(self, entity: str, max_depth: int = 2) -> List[Dict]:
        """
        查找与实体相关的记忆（多跳查询）

        Args:
            entity: 起始实体
            max_depth: 最大跳数

        Returns:
            相关记忆列表
        """
        related_entities = set()
        visited = set()
        queue = deque([(entity, 0)])

        while queue:
            current_entity, depth = queue.popleft()

            if depth > max_depth:
                continue

            if current_entity in visited:
                continue

            visited.add(current_entity)
            related_entities.add(current_entity)

            # 遍历邻居
            for neighbor, _ in self.graph.get(current_entity, set()):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

        # 收集相关记忆
        related_memories = []
        for related_entity in related_entities:
            if related_entity in self.memory_index:
                for memory_id in self.memory_index[related_entity]:
                    related_memories.append({
                        "entity": related_entity,
                        "memory_id": memory_id
                    })

        return related_memories

    def find_shortest_path(self, entity1: str, entity2: str) -> List[str]:
        """
        查找两个实体之间的最短路径

        Args:
            entity1: 起始实体
            entity2: 目标实体

        Returns:
            路径上的实体列表
        """
        if entity1 not in self.graph or entity2 not in self.graph:
            return []

        # BFS
        visited = set()
        queue = deque([(entity1, [entity1])])
        visited.add(entity1)

        while queue:
            current, path = queue.popleft()

            if current == entity2:
                return path

            for neighbor, _ in self.graph.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def discover_patterns(self) -> List[Dict]:
        """
        发现记忆中的模式

        包括：
        1. 频繁出现的实体组合
        2. 常见关系链
        3. 孤立实体（可能需要关注的）
        4. 中心节点（关键实体）
        """
        patterns = []

        # 1. 发现中心节点（连接最多的实体）
        centrality = {}
        for entity, neighbors in self.graph.items():
            centrality[entity] = len(neighbors)

        top_entities = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        patterns.append({
            "type": "central_entities",
            "description": "连接最多的实体（关键节点）",
            "entities": [{"entity": e, "connections": c} for e, c in top_entities]
        })

        # 2. 发现孤立实体
        isolated = [e for e, neighbors in self.graph.items() if len(neighbors) == 0]
        if isolated:
            patterns.append({
                "type": "isolated_entities",
                "description": "孤立实体（可能需要关注）",
                "entities": isolated
            })

        # 3. 发现三角形关系（三元组）
        triangles = self._find_triangles()
        if triangles:
            patterns.append({
                "type": "triangular_relationships",
                "description": "三角形关系（强关联）",
                "triangles": triangles[:5]  # 只显示前 5 个
            })

        # 4. 发现频繁关系
        relation_freq = defaultdict(int)
        for _, relation, _ in self.relationships:
            relation_freq[relation] += 1

        top_relations = sorted(relation_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        patterns.append({
            "type": "frequent_relations",
            "description": "最常见的关系",
            "relations": [{"relation": r, "count": c} for r, c in top_relations]
        })

        return patterns

    def cluster_entities(self) -> List[List[str]]:
        """
        聚类实体（基于连接密度）

        Returns:
            实体聚类列表
        """
        visited = set()
        clusters = []

        for entity in self.graph:
            if entity in visited:
                continue

            # DFS 找到连通分量
            cluster = []
            stack = [entity]

            while stack:
                current = stack.pop()
                if current in visited:
                    continue

                visited.add(current)
                cluster.append(current)

                for neighbor, _ in self.graph.get(current, set()):
                    if neighbor not in visited:
                        stack.append(neighbor)

            if len(cluster) > 1:
                clusters.append(cluster)

        return clusters

    def infer_knowledge(self, entity: str) -> List[Dict]:
        """
        基于图谱推断知识

        通过分析实体的关联关系，推断隐含知识

        Args:
            entity: 目标实体

        Returns:
            推断的知识列表
        """
        inferred = []

        # 获取相关实体
        related = self.graph.get(entity, set())

        for neighbor, relation in related:
            # 推断 1: 如果 A 与 B 有关系 R，且 B 与 C 有关系 R，则 A 可能与 C 有关系 R
            for neighbor2, relation2 in self.graph.get(neighbor, set()):
                if relation == relation2 and neighbor2 != entity:
                    inferred.append({
                        "type": "transitive_inference",
                        "reasoning": f"{entity} {relation} {neighbor}, {neighbor} {relation} {neighbor2} -> {entity} 可能 {relation} {neighbor2}",
                        "confidence": 0.6
                    })

        return inferred

    def _extract_entities(self, text: str) -> List[str]:
        """
        提取实体

        简化实现：提取名词短语和专有名词
        """
        entities = []

        # 提取大写单词（可能是专有名词）
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(proper_nouns)

        # 提取引号内的内容（可能是术语）
        quoted = re.findall(r'"([^"]+)"', text)
        entities.extend(quoted)

        # 提取常见关键词
        keywords = ["React", "Vue", "Angular", "Node", "Python", "TypeScript",
                   "JavaScript", "CSS", "HTML", "Docker", "Kubernetes", "AWS"]
        for kw in keywords:
            if kw.lower() in text.lower():
                entities.append(kw)

        # 去重
        return list(set(entities))

    def _infer_entity_type(self, entity: str, context: str) -> str:
        """
        推断实体类型

        Args:
            entity: 实体名称
            context: 上下文

        Returns:
            实体类型
        """
        context_lower = context.lower()

        # 技术栈
        tech_keywords = ["framework", "library", "language", "tool", "technology"]
        if any(kw in context_lower for kw in tech_keywords):
            return "technology"

        # 项目
        if "project" in context_lower or "项目" in context_lower:
            return "project"

        # 人
        if any(indicator in context_lower for indicator in ["said", "stated", "stated that", "用户", "developer"]):
            return "person"

        # 默认
        return "unknown"

    def _extract_relationships(self, text: str, entities: List[str]) -> List[Tuple[str, str, str]]:
        """
        提取实体间关系

        简化实现：基于关键词匹配
        """
        relations = []

        relation_patterns = {
            "uses": ["uses", "used", "using", "使用"],
            "prefers": ["prefers", "prefers to", "prefers", "偏好"],
            "decided": ["decided to", "decided on", "decided", "决定"],
            "related to": ["related to", "associated with", "related", "related to"],
            "better than": ["better than", "superior to", "优于"],
            "worse than": ["worse than", "inferior to", "劣于"]
        }

        text_lower = text.lower()

        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # 检查是否存在关系
                for relation_type, keywords in relation_patterns.items():
                    for kw in keywords:
                        if kw in text_lower:
                            # 简化：假设顺序代表方向
                            idx1 = text_lower.find(entity1.lower())
                            idx2 = text_lower.find(entity2.lower())

                            if idx1 < idx2:
                                relations.append((entity1, relation_type, entity2))
                            else:
                                relations.append((entity2, relation_type, entity1))

        return relations

    def _count_clusters(self) -> int:
        """计算聚类数量"""
        return len(self.cluster_entities())

    def _find_triangles(self) -> List[List[str]]:
        """查找三角形关系（三元组）"""
        triangles = []

        for entity in self.graph:
            neighbors = list(self.graph[entity])
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    n1_entity, _ = n1
                    n2_entity, _ = n2

                    # 检查 n1 和 n2 是否直接相连
                    for neighbor, _ in self.graph.get(n1_entity, set()):
                        if neighbor == n2_entity:
                            triangles.append([entity, n1_entity, n2_entity])

        return triangles

    def visualize(self, max_nodes: int = 20) -> str:
        """
        生成可视化图谱（DOT 格式）

        Args:
            max_nodes: 最大显示节点数

        Returns:
            DOT 格式字符串
        """
        # 选择度数最高的节点
        degrees = {entity: len(neighbors) for entity, neighbors in self.graph.items()}
        top_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
        selected_entities = set(e for e, _ in top_entities)

        # 生成 DOT
        lines = ["digraph MemoryGraph {"]
        lines.append("  rankdir=LR;")
        lines.append("  node [shape=circle];")
        lines.append("")

        # 添加节点
        for entity in selected_entities:
            entity_type = self.entity_types.get(entity, "unknown")
            color = self._get_color_by_type(entity_type)
            lines.append(f'  "{entity}" [color="{color}"];')

        lines.append("")

        # 添加边
        for entity in selected_entities:
            for neighbor, relation in self.graph.get(entity, set()):
                if neighbor in selected_entities:
                    lines.append(f'  "{entity}" -> "{neighbor}" [label="{relation}"];')

        lines.append("}")

        return "\n".join(lines)

    def _get_color_by_type(self, entity_type: str) -> str:
        """根据类型获取颜色"""
        colors = {
            "technology": "#4CAF50",
            "project": "#2196F3",
            "person": "#FF9800",
            "unknown": "#9E9E9E"
        }
        return colors.get(entity_type, "#9E9E9E")


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="记忆知识图谱")
    parser.add_argument("--workspace", default=".", help="工作目录")
    parser.add_argument("action", choices=["build", "patterns", "related", "path", "visualize"])
    parser.add_argument("--entity", help="实体名称")
    parser.add_argument("--entity2", help="第二个实体名称")

    args = parser.parse_args()

    # 读取记忆文件
    memories = []
    session_state = Path(args.workspace) / "SESSION-STATE.md"
    memory_md = Path(args.workspace) / "MEMORY.md"

    if session_state.exists():
        content = session_state.read_text()
        for line in content.split("\n"):
            line = line.strip("- ")
            if line and len(line) > 5:
                memories.append({
                    "content": line,
                    "type": "context",
                    "source": "SESSION-STATE.md"
                })

    if memory_md.exists():
        content = memory_md.read_text()
        for line in content.split("\n"):
            line = line.strip("- *")
            if line and len(line) > 5:
                memories.append({
                    "content": line,
                    "type": "longterm",
                    "source": "MEMORY.md"
                })

    # 构建图谱
    kg = KnowledgeGraph(args.workspace)
    kg.build_from_memories(memories)

    if args.action == "build":
        stats = kg.build_from_memories(memories)
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif args.action == "patterns":
        patterns = kg.discover_patterns()
        print(json.dumps(patterns, ensure_ascii=False, indent=2))

    elif args.action == "related":
        if not args.entity:
            print("错误: 需要指定 --entity")
            return

        related = kg.find_related_memories(args.entity)
        print(json.dumps(related, ensure_ascii=False, indent=2))

    elif args.action == "path":
        if not args.entity or not args.entity2:
            print("错误: 需要指定 --entity 和 --entity2")
            return

        path = kg.find_shortest_path(args.entity, args.entity2)
        print(" -> ".join(path))

    elif args.action == "visualize":
        dot = kg.visualize()
        print(dot)
        print("\n提示: 将上面的 DOT 代码保存为 .dot 文件，使用 Graphviz 可视化")


if __name__ == "__main__":
    main()
