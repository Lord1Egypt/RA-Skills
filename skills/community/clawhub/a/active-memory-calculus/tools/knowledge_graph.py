#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Graph Builder for Active Memory Calculus
构建和维护高等数学知识图谱
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class KnowledgeGraph:
    """知识图谱结构"""
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    last_updated: str

@dataclass
class Fact:
    """事实数据"""
    concept: str
    relation: str
    target: Optional[str]
    attributes: Dict[str, Any]
    timestamp: str

class KnowledgeGraphBuilder:
    """知识图谱构建器"""

    # 高等数学概念依赖关系
    CONCEPT_DEPENDENCIES = {
        "极限": [],
        "连续": ["极限"],
        "导数": ["极限", "连续"],
        "微分": ["导数"],
        "微分中值定理": ["导数", "连续"],
        "泰勒公式": ["微分中值定理", "导数"],
        "不定积分": ["导数"],
        "定积分": ["不定积分", "极限"],
        "定积分应用": ["定积分"],
        "反常积分": ["定积分", "极限"],
        "微分方程": ["不定积分", "导数"],
        "向量代数": [],
        "空间解析几何": ["向量代数"],
        "多元函数极限": ["极限", "向量代数"],
        "偏导数": ["多元函数极限", "导数"],
        "全微分": ["偏导数", "微分"],
        "重积分": ["定积分", "空间解析几何"],
        "曲线积分": ["定积分", "空间解析几何"],
        "曲面积分": ["重积分", "曲线积分"],
        "级数": ["极限"],
        "幂级数": ["级数"],
        "傅里叶级数": ["级数", "积分"]
    }

    def __init__(self, memory_path: str = None):
        self.memory_path = memory_path or os.environ.get(
            "CALCULUS_MEMORY_PATH", "~/obsidian/calculus-memory")
        self.memory_path = os.path.expanduser(self.memory_path)
        self.graph_path = os.path.join(self.memory_path, "knowledge-graph")
        os.makedirs(self.graph_path, exist_ok=True)

        self.graph_file = os.path.join(self.graph_path, "calculus_knowledge_graph.json")
        self.current_graph = self._load_existing_graph()

    def _load_existing_graph(self) -> KnowledgeGraph:
        """加载现有知识图谱"""
        if os.path.exists(self.graph_file):
            with open(self.graph_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return KnowledgeGraph(**data)

        return KnowledgeGraph(
            nodes=[],
            edges=[],
            metadata={"version": "1.0", "description": "高等数学知识图谱"},
            last_updated=datetime.now().isoformat()
        )

    async def build(self, facts: List[Fact], 
                   existing_graph: Optional[KnowledgeGraph] = None) -> KnowledgeGraph:
        """构建或更新知识图谱"""
        if existing_graph is None:
            existing_graph = self.current_graph

        graph = existing_graph

        for fact in facts:
            await self._process_fact(graph, fact)

        self._auto_build_dependencies(graph)
        self._detect_learning_paths(graph)

        graph.last_updated = datetime.now().isoformat()
        await self._save_graph(graph)

        return graph

    async def _process_fact(self, graph: KnowledgeGraph, fact: Fact):
        """处理单个事实"""
        existing_node = None
        for node in graph.nodes:
            if node["id"] == fact.concept:
                existing_node = node
                break

        if existing_node:
            if fact.attributes.get("mastery_level"):
                existing_node["mastery"] = fact.attributes["mastery_level"]
            if fact.attributes.get("status"):
                existing_node["status"] = fact.attributes["status"]
            existing_node["last_updated"] = fact.timestamp
        else:
            new_node = {
                "id": fact.concept,
                "type": "concept",
                "mastery": fact.attributes.get("mastery_level", 0.0),
                "status": fact.attributes.get("status", "unknown"),
                "created_at": fact.timestamp,
                "last_updated": fact.timestamp
            }
            graph.nodes.append(new_node)

        if fact.target and fact.relation:
            edge = {
                "source": fact.concept,
                "target": fact.target,
                "relation": fact.relation,
                "timestamp": fact.timestamp
            }
            if not any(e["source"] == edge["source"] and 
                      e["target"] == edge["target"] and
                      e["relation"] == edge["relation"] 
                      for e in graph.edges):
                graph.edges.append(edge)

    def _auto_build_dependencies(self, graph: KnowledgeGraph):
        """自动构建概念依赖关系"""
        existing_concepts = {node["id"] for node in graph.nodes}

        for concept, deps in self.CONCEPT_DEPENDENCIES.items():
            if concept not in existing_concepts:
                continue

            for dep in deps:
                if dep in existing_concepts:
                    edge_exists = any(
                        e["source"] == dep and 
                        e["target"] == concept and
                        e["relation"] == "prerequisite"
                        for e in graph.edges
                    )

                    if not edge_exists:
                        graph.edges.append({
                            "source": dep,
                            "target": concept,
                            "relation": "prerequisite",
                            "type": "auto_generated",
                            "strength": "strong"
                        })

    def _detect_learning_paths(self, graph: KnowledgeGraph):
        """检测推荐学习路径"""
        weak_concepts = [
            node for node in graph.nodes 
            if node.get("mastery", 0) < 0.5 and node.get("status") != "mastered"
        ]

        learning_paths = []

        for concept_node in weak_concepts:
            concept = concept_node["id"]

            prerequisites = [
                edge["source"] for edge in graph.edges
                if edge["target"] == concept and edge["relation"] == "prerequisite"
            ]

            weak_prereqs = []
            for prereq in prerequisites:
                prereq_node = next((n for n in graph.nodes if n["id"] == prereq), None)
                if prereq_node and prereq_node.get("mastery", 0) < 0.6:
                    weak_prereqs.append(prereq)

            if weak_prereqs:
                learning_paths.append({
                    "target": concept,
                    "weak_prerequisites": weak_prereqs,
                    "recommended_path": weak_prereqs + [concept],
                    "priority": "high" if concept_node.get("mastery", 0) < 0.3 else "medium"
                })

        graph.metadata["learning_paths"] = learning_paths
        graph.metadata["weak_concepts"] = [n["id"] for n in weak_concepts]

    async def _save_graph(self, graph: KnowledgeGraph):
        """保存知识图谱"""
        with open(self.graph_file, "w", encoding="utf-8") as f:
            json.dump(asdict(graph), f, ensure_ascii=False, indent=2)

    def get_learning_path(self, target_concept: str) -> Optional[List[str]]:
        """获取到目标概念的推荐学习路径"""
        paths = self.current_graph.metadata.get("learning_paths", [])
        for path in paths:
            if path["target"] == target_concept:
                return path["recommended_path"]

        if target_concept in self.CONCEPT_DEPENDENCIES:
            deps = self.CONCEPT_DEPENDENCIES[target_concept]
            return deps + [target_concept]

        return None

    def to_json(self, graph: KnowledgeGraph = None) -> str:
        """导出为JSON"""
        if graph is None:
            graph = self.current_graph
        return json.dumps(asdict(graph), ensure_ascii=False, indent=2)

# CLI 接口
if __name__ == "__main__":
    import asyncio
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python knowledge_graph.py <facts_json_file>")
            sys.exit(1)

        facts_file = sys.argv[1]
        with open(facts_file, "r", encoding="utf-8") as f:
            facts_data = json.load(f)

        facts = [Fact(**f) for f in facts_data]

        builder = KnowledgeGraphBuilder()
        graph = await builder.build(facts)

        print(builder.to_json(graph))

    asyncio.run(main())
