#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dream Generator Tool for Active Memory Calculus
生成学习梦境摘要和知识图谱
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict

@dataclass
class DreamSummary:
    """梦境摘要结构"""
    timestamp: str
    period_start: str
    period_end: str
    key_findings: List[Dict[str, Any]]
    concept_progress: List[Dict[str, Any]]
    error_patterns_summary: List[Dict[str, Any]]
    learning_gaps: List[Dict[str, Any]]
    recommendations: List[str]
    knowledge_graph_update: Dict[str, Any]

@dataclass
class Session:
    """学习会话"""
    id: str
    timestamp: str
    transcript: str
    extracted_facts: List[Dict[str, Any]]

class DreamGenerator:
    """梦境生成器"""

    def __init__(self, memory_path: str = None):
        self.memory_path = memory_path or os.environ.get(
            "CALCULUS_MEMORY_PATH", "~/obsidian/calculus-memory")
        self.memory_path = os.path.expanduser(self.memory_path)
        self.dreams_dir = os.path.join(self.memory_path, "dreams")
        os.makedirs(self.dreams_dir, exist_ok=True)

    async def generate(self, sessions: List[Session], 
                      time_range: Tuple[datetime, datetime]) -> DreamSummary:
        """生成梦境摘要"""
        period_start, period_end = time_range

        all_facts = []
        for session in sessions:
            all_facts.extend(session.extracted_facts)

        key_findings = self._analyze_key_findings(all_facts)
        concept_progress = self._track_concept_progress(all_facts)
        error_patterns_summary = self._summarize_error_patterns(all_facts)
        learning_gaps = self._identify_learning_gaps(all_facts, concept_progress)
        recommendations = self._generate_recommendations(
            concept_progress, error_patterns_summary, learning_gaps)
        knowledge_graph_update = self._build_knowledge_graph_update(
            concept_progress, learning_gaps)

        summary = DreamSummary(
            timestamp=datetime.now().isoformat(),
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            key_findings=key_findings,
            concept_progress=concept_progress,
            error_patterns_summary=error_patterns_summary,
            learning_gaps=learning_gaps,
            recommendations=recommendations,
            knowledge_graph_update=knowledge_graph_update
        )

        await self._save_dream(summary)
        return summary

    def _analyze_key_findings(self, facts: List[Dict]) -> List[Dict[str, Any]]:
        """分析关键发现"""
        findings = []

        facts_by_type = defaultdict(list)
        for fact in facts:
            facts_by_type[fact.get("extract_type", "unknown")].append(fact)

        mastery_facts = facts_by_type.get("mastery", [])
        if mastery_facts:
            recent_proficient = [f for f in mastery_facts 
                               if f.get("content", {}).get("level") == "proficient"]
            if recent_proficient:
                concepts = list(set(f.get("content", {}).get("concept") 
                                  for f in recent_proficient))
                findings.append({
                    "type": "mastery_breakthrough",
                    "description": f"学生在以下概念上取得突破: {', '.join(concepts)}",
                    "concepts": concepts,
                    "significance": "high"
                })

        error_facts = facts_by_type.get("error", [])
        if error_facts:
            error_types = defaultdict(int)
            for fact in error_facts:
                error_type = fact.get("content", {}).get("error_type", "unknown")
                error_types[error_type] += 1

            for error_type, count in error_types.items():
                if count >= 3:
                    findings.append({
                        "type": "persistent_error",
                        "description": f"发现高频错误模式: {error_type} (出现{count}次)",
                        "error_type": error_type,
                        "frequency": count,
                        "significance": "high"
                    })

        return findings

    def _track_concept_progress(self, facts: List[Dict]) -> List[Dict[str, Any]]:
        """追踪概念掌握进展"""
        concept_stats = defaultdict(lambda: {"mentions": 0, "levels": []})

        for fact in facts:
            if fact.get("extract_type") == "mastery":
                content = fact.get("content", {})
                concept = content.get("concept")
                level = content.get("level")

                if concept and level:
                    concept_stats[concept]["mentions"] += 1
                    concept_stats[concept]["levels"].append(level)

        progress = []
        level_scores = {"struggling": 0.3, "learning": 0.6, "proficient": 0.9}

        for concept, stats in concept_stats.items():
            levels = stats["levels"]
            if levels:
                avg_score = sum(level_scores.get(l, 0.5) for l in levels) / len(levels)

                if len(levels) >= 2:
                    trend = "improving" if levels[-1] == "proficient" else "stable"
                else:
                    trend = "new"

                progress.append({
                    "concept": concept,
                    "mastery_level": round(avg_score, 2),
                    "mentions": stats["mentions"],
                    "latest_status": levels[-1],
                    "trend": trend
                })

        return sorted(progress, key=lambda x: x["mastery_level"])

    def _summarize_error_patterns(self, facts: List[Dict]) -> List[Dict[str, Any]]:
        """汇总错误模式"""
        error_stats = defaultdict(lambda: {"count": 0, "contexts": []})

        for fact in facts:
            if fact.get("extract_type") == "error":
                content = fact.get("content", {})
                error_type = content.get("error_type", "unknown")
                context = content.get("context", "")

                error_stats[error_type]["count"] += 1
                if context:
                    error_stats[error_type]["contexts"].append(context[:100])

        summary = []
        for error_type, stats in error_stats.items():
            summary.append({
                "error_type": error_type,
                "frequency": stats["count"],
                "severity": "high" if stats["count"] >= 3 else "medium",
                "sample_contexts": stats["contexts"][:3]
            })

        return sorted(summary, key=lambda x: x["frequency"], reverse=True)

    def _identify_learning_gaps(self, facts: List[Dict], 
                               concept_progress: List[Dict]) -> List[Dict[str, Any]]:
        """识别学习断层"""
        gaps = []

        dependencies = {
            "反常积分": ["极限"],
            "级数": ["极限"],
            "微分方程": ["积分", "导数"],
            "多元函数": ["导数", "极限"]
        }

        progress_dict = {p["concept"]: p for p in concept_progress}

        for concept, deps in dependencies.items():
            if concept in progress_dict:
                concept_mastery = progress_dict[concept]["mastery_level"]
                if concept_mastery < 0.5:
                    weak_prereqs = []
                    for dep in deps:
                        if dep in progress_dict:
                            dep_mastery = progress_dict[dep]["mastery_level"]
                            if dep_mastery < 0.6:
                                weak_prereqs.append({
                                    "concept": dep,
                                    "mastery": dep_mastery
                                })

                    if weak_prereqs:
                        gaps.append({
                            "concept": concept,
                            "current_mastery": concept_mastery,
                            "root_cause": "weak_prerequisites",
                            "weak_prerequisites": weak_prereqs,
                            "recommendation": f"建议先强化: {', '.join(p['concept'] for p in weak_prereqs)}"
                        })

        return gaps

    def _generate_recommendations(self, concept_progress: List[Dict],
                                 error_patterns: List[Dict],
                                 learning_gaps: List[Dict]) -> List[str]:
        """生成学习建议"""
        recommendations = []

        weak_concepts = [p for p in concept_progress if p["mastery_level"] < 0.5]
        if weak_concepts:
            concepts_str = ", ".join(c["concept"] for c in weak_concepts[:3])
            recommendations.append(f"优先强化薄弱概念: {concepts_str}")

        high_freq_errors = [e for e in error_patterns if e["frequency"] >= 3]
        for error in high_freq_errors:
            recommendations.append(f"针对高频错误'{error['error_type']}'进行专项练习")

        for gap in learning_gaps:
            recommendations.append(gap["recommendation"])

        if concept_progress:
            next_concepts = [p["concept"] for p in concept_progress 
                           if 0.4 <= p["mastery_level"] < 0.8][:2]
            if next_concepts:
                recommendations.append(f"明日推荐学习: {', '.join(next_concepts)}")

        return recommendations

    def _build_knowledge_graph_update(self, concept_progress: List[Dict],
                                     learning_gaps: List[Dict]) -> Dict[str, Any]:
        """构建知识图谱更新"""
        nodes = []
        edges = []

        for progress in concept_progress:
            nodes.append({
                "id": progress["concept"],
                "type": "concept",
                "mastery": progress["mastery_level"],
                "status": progress["latest_status"]
            })

        dependencies = {
            "反常积分": ["极限"],
            "级数": ["极限"],
            "微分方程": ["积分"]
        }

        for target, sources in dependencies.items():
            for source in sources:
                if any(n["id"] == target for n in nodes) and                    any(n["id"] == source for n in nodes):
                    edges.append({
                        "source": source,
                        "target": target,
                        "relation": "prerequisite",
                        "type": "auto_generated",
                        "strength": "strong"
                    })

        return {
            "nodes": nodes,
            "edges": edges,
            "gaps": [g["concept"] for g in learning_gaps],
            "timestamp": datetime.now().isoformat()
        }

    async def _save_dream(self, summary: DreamSummary):
        """保存梦境摘要到文件"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"DREAMS_{date_str}.md"
        filepath = os.path.join(self.dreams_dir, filename)

        md_content = self._to_markdown(summary)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

    def _to_markdown(self, summary: DreamSummary) -> str:
        """转换为 Markdown 格式"""
        lines = [
            f"# 学习梦境摘要 {summary.period_start[:10]}",
            f"",
            f"**生成时间**: {summary.timestamp}",
            f"**统计周期**: {summary.period_start} 至 {summary.period_end}",
            f"",
            f"## 关键发现",
            f""
        ]

        for finding in summary.key_findings:
            emoji = "🎯" if finding["significance"] == "high" else "💡"
            lines.append(f"{emoji} **{finding['type']}**: {finding['description']}")

        lines.extend([
            f"",
            f"## 概念掌握进展",
            f""
        ])

        for progress in summary.concept_progress:
            status_emoji = "✅" if progress["mastery_level"] > 0.7 else "⚠️" if progress["mastery_level"] > 0.4 else "❌"
            lines.append(f"{status_emoji} **{progress['concept']}**: {progress['mastery_level']:.0%} ({progress['latest_status']})")

        lines.extend([
            f"",
            f"## 错误模式分析",
            f""
        ])

        for error in summary.error_patterns_summary:
            severity_emoji = "🔴" if error["severity"] == "high" else "🟡"
            lines.append(f"{severity_emoji} **{error['error_type']}**: 出现 {error['frequency']} 次")

        lines.extend([
            f"",
            f"## 学习断层预警",
            f""
        ])

        for gap in summary.learning_gaps:
            lines.append(f"⚠️ **{gap['concept']}**: {gap['recommendation']}")

        lines.extend([
            f"",
            f"## 学习建议",
            f""
        ])

        for i, rec in enumerate(summary.recommendations, 1):
            lines.append(f"{i}. {rec}")

        lines.extend([
            f"",
            f"## 知识图谱更新",
            f"",
            f"```json",
            json.dumps(summary.knowledge_graph_update, ensure_ascii=False, indent=2),
            f"```"
        ])

        return "
".join(lines)

# CLI 接口
if __name__ == "__main__":
    import asyncio
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python dream_generator.py <sessions_json_file>")
            sys.exit(1)

        sessions_file = sys.argv[1]
        with open(sessions_file, "r", encoding="utf-8") as f:
            sessions_data = json.load(f)

        sessions = [Session(**s) for s in sessions_data]

        now = datetime.now()
        hour_ago = now - timedelta(hours=1)

        generator = DreamGenerator()
        summary = await generator.generate(sessions, (hour_ago, now))

        print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))

    asyncio.run(main())
