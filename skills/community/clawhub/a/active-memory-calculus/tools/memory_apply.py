#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Apply Tool for Active Memory Calculus
在生成回复前应用相关记忆数据
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class MemoryContext:
    """记忆上下文，用于指导回复生成"""
    personalization_hints: List[str]
    difficulty_adjustment: str
    warnings: List[str]
    recommended_skills: List[str]
    suggested_visualization: Optional[str]
    pace_adjustment: Optional[str]
    context_summary: str

class MemoryApplier:
    """记忆应用器"""

    def __init__(self, memory_path: str = None):
        self.memory_path = memory_path or os.environ.get(
            "CALCULUS_MEMORY_PATH", "~/obsidian/calculus-memory")
        self.memory_path = os.path.expanduser(self.memory_path)
        self.student_profile = {}
        self.session_memories = []

    async def apply(self, current_query: str, student_id: str,
                   apply_modes: List[str] = None) -> MemoryContext:
        """应用记忆到当前查询"""
        if apply_modes is None:
            apply_modes = ["personalization", "difficulty", "warning"]

        await self._load_student_profile(student_id)
        await self._load_recent_memories(student_id)

        context = MemoryContext(
            personalization_hints=[],
            difficulty_adjustment="normal",
            warnings=[],
            recommended_skills=[],
            suggested_visualization=None,
            pace_adjustment=None,
            context_summary=""
        )

        if "personalization" in apply_modes:
            self._apply_personalization(context, current_query)

        if "difficulty" in apply_modes:
            self._apply_difficulty_adjustment(context, current_query)

        if "warning" in apply_modes:
            self._apply_warnings(context, current_query)

        context.context_summary = self._generate_summary(context)
        return context

    async def _load_student_profile(self, student_id: str):
        """加载学生档案"""
        profile_file = os.path.join(self.memory_path, "profiles", f"{student_id}.json")
        if os.path.exists(profile_file):
            with open(profile_file, "r", encoding="utf-8") as f:
                self.student_profile = json.load(f)

    async def _load_recent_memories(self, student_id: str, hours: int = 24):
        """加载近期记忆"""
        memories_dir = os.path.join(self.memory_path, "memories", student_id)
        if not os.path.exists(memories_dir):
            return

        cutoff_time = datetime.now() - timedelta(hours=hours)

        for filename in os.listdir(memories_dir):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(memories_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                memory = json.load(f)
                memory_time = datetime.fromisoformat(memory.get("timestamp", ""))
                if memory_time > cutoff_time:
                    self.session_memories.append(memory)

    def _apply_personalization(self, context: MemoryContext, query: str):
        """应用个性化设置"""
        learning_style = self.student_profile.get("learning_style", {})
        style_type = learning_style.get("type")

        if style_type == "visual":
            context.personalization_hints.append("学生偏好视觉化学习，建议优先使用GeoGebra动画")
            context.suggested_visualization = "geogebra_animation"
            context.recommended_skills.append("calculus-concept-visualizer")
        elif style_type == "deductive":
            context.personalization_hints.append("学生偏好推导型学习，建议详细展示证明步骤")
            context.recommended_skills.append("derivation-animator")
        elif style_type == "practice":
            context.personalization_hints.append("学生偏好练习型学习，建议提供更多例题")
            context.recommended_skills.append("exam-problem-generator")

    def _apply_difficulty_adjustment(self, context: MemoryContext, query: str):
        """应用难度调整"""
        concept_mastery = self.student_profile.get("concept_mastery", {})

        query_lower = query.lower()
        relevant_concepts = []

        concept_keywords = {
            "极限": ["极限", "limit", "趋近"],
            "导数": ["导数", "derivative", "微分"],
            "积分": ["积分", "integral"],
            "级数": ["级数", "series"]
        }

        for concept, keywords in concept_keywords.items():
            if any(kw in query_lower for kw in keywords):
                relevant_concepts.append(concept)

        if relevant_concepts:
            mastery_levels = []
            for concept in relevant_concepts:
                level = concept_mastery.get(concept, {}).get("level", "unknown")
                mastery_levels.append(level)

            if all(l == "proficient" for l in mastery_levels):
                context.difficulty_adjustment = "advanced"
                context.personalization_hints.append("学生已熟练掌握相关概念，可提供进阶内容或技巧")
            elif any(l == "struggling" for l in mastery_levels):
                context.difficulty_adjustment = "foundational"
                context.personalization_hints.append("学生在相关概念上存在困难，建议回顾基础知识")

    def _apply_warnings(self, context: MemoryContext, query: str):
        """应用预警提示"""
        error_patterns = self.student_profile.get("error_patterns", [])

        query_lower = query.lower()

        for error in error_patterns:
            error_type = error.get("error_type", "")
            frequency = error.get("frequency", 0)

            if frequency >= 3:
                if "积分限" in query_lower and error_type == "integral_limit_transform":
                    context.warnings.append("⚠️ 注意：这是你的常见易错点——定积分换元时忘记变换积分限")
                elif "链式" in query_lower or "复合" in query_lower:
                    if error_type == "derivative_chain_rule":
                        context.warnings.append("⚠️ 注意：复合函数求导时记得应用链式法则，不要遗漏内层导数")

    def _generate_summary(self, context: MemoryContext) -> str:
        """生成上下文摘要"""
        parts = []

        if context.personalization_hints:
            parts.append("【个性化】" + "; ".join(context.personalization_hints))

        if context.warnings:
            parts.append("【预警】" + "; ".join(context.warnings))

        parts.append(f"【难度】{context.difficulty_adjustment}")

        if context.recommended_skills:
            parts.append(f"【推荐Skills】{', '.join(context.recommended_skills)}")

        return " | ".join(parts)

# CLI 接口
if __name__ == "__main__":
    import asyncio
    import sys

    async def main():
        if len(sys.argv) < 3:
            print("Usage: python memory_apply.py <query> <student_id> [apply_modes]")
            sys.exit(1)

        query = sys.argv[1]
        student_id = sys.argv[2]
        apply_modes = sys.argv[3].split(",") if len(sys.argv) > 3 else None

        applier = MemoryApplier()
        context = await applier.apply(query, student_id, apply_modes)

        print(json.dumps(asdict(context), ensure_ascii=False, indent=2))

    asyncio.run(main())
