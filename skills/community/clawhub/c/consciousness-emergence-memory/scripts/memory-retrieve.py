#!/usr/bin/env python3
"""
智能记忆检索模块
根据上下文动态选择最优检索策略，实现多源记忆的智能排序和过滤
"""
import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from pathlib import Path

class MemoryRetrieve:
    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.session_state = self.workspace / "SESSION-STATE.md"
        self.memory_md = self.workspace / "MEMORY.md"
        self.memory_dir = self.workspace / "memory"

    def retrieve(self, query: str, context_type: str = "general") -> List[Dict]:
        """
        智能检索记忆，根据查询和上下文类型选择最优策略

        Args:
            query: 查询内容
            context_type: 上下文类型 (general, decision, preference, fact)

        Returns:
            排序后的记忆列表，每项包含: content, source, score, timestamp, type
        """
        memories = []

        # 1. 从 SESSION-STATE.md 获取热数据（最高优先级）
        session_memories = self._retrieve_session_state(query, context_type)
        memories.extend(session_memories)

        # 2. 从 MEMORY.md 获取长期记忆
        longterm_memories = self._retrieve_longterm(query, context_type)
        memories.extend(longterm_memories)

        # 3. 从 daily logs 获取近期记忆
        daily_memories = self._retrieve_daily(query, context_type, days=7)
        memories.extend(daily_memories)

        # 4. 多维度排序
        ranked_memories = self._rank_memories(memories, query, context_type)

        return ranked_memories

    def _retrieve_session_state(self, query: str, context_type: str) -> List[Dict]:
        """从 SESSION-STATE.md 检索，权重最高"""
        if not self.session_state.exists():
            return []

        content = self.session_state.read_text()
        memories = []

        # 提取关键信息
        if "Current Task" in content and "任务" in query:
            task_match = re.search(r"Current Task\s*\n\s*(.+)", content)
            if task_match:
                memories.append({
                    "content": task_match.group(1),
                    "source": "SESSION-STATE",
                    "score": 1.0,
                    "timestamp": datetime.now(),
                    "type": "current_task"
                })

        # 提取关键上下文
        context_section = re.search(r"## Key Context\s*\n([\s\S]*?)(?=##|$)", content)
        if context_section:
            for line in context_section.group(1).split("\n"):
                line = line.strip("- ")
                if line and self._is_relevant(line, query, context_type):
                    memories.append({
                        "content": line,
                        "source": "SESSION-STATE",
                        "score": 0.9,
                        "timestamp": datetime.now(),
                        "type": "context"
                    })

        # 提取最近决策
        decisions_section = re.search(r"## Recent Decisions\s*\n([\s\S]*?)(?=##|$)", content)
        if decisions_section and context_type in ["decision", "general"]:
            for line in decisions_section.group(1).split("\n"):
                line = line.strip("- ")
                if line and self._is_relevant(line, query, context_type):
                    memories.append({
                        "content": line,
                        "source": "SESSION-STATE",
                        "score": 0.95,
                        "timestamp": datetime.now(),
                        "type": "decision"
                    })

        return memories

    def _retrieve_longterm(self, query: str, context_type: str) -> List[Dict]:
        """从 MEMORY.md 检索长期记忆"""
        if not self.memory_md.exists():
            return []

        content = self.memory_md.read_text()
        memories = []

        # 根据上下文类型提取对应章节
        sections_map = {
            "preference": ["Preferences", "About the User"],
            "decision": ["Decisions Log"],
            "fact": ["Lessons Learned"],
            "general": ["Preferences", "Decisions Log", "Lessons Learned", "Projects"]
        }

        target_sections = sections_map.get(context_type, sections_map["general"])

        for section_name in target_sections:
            section_pattern = rf"## {section_name}\s*\n([\s\S]*?)(?=##|$)"
            section_match = re.search(section_pattern, content)

            if section_match:
                section_content = section_match.group(1)
                lines = section_content.split("\n")

                for line in lines:
                    line = line.strip("- *")
                    if line and len(line) > 10 and self._is_relevant(line, query, context_type):
                        # 计算重要性评分（基于内容长度和位置）
                        importance = self._calculate_importance(line, section_name)
                        memories.append({
                            "content": line,
                            "source": "MEMORY.md",
                            "score": 0.7 * importance,
                            "timestamp": datetime.now() - timedelta(days=30),  # 假设长期记忆
                            "type": context_type
                        })

        return memories

    def _retrieve_daily(self, query: str, context_type: str, days: int = 7) -> List[Dict]:
        """从最近 N 天的日志中检索"""
        if not self.memory_dir.exists():
            return []

        memories = []
        today = datetime.now()

        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            daily_file = self.memory_dir / f"{date_str}.md"

            if daily_file.exists():
                content = daily_file.read_text()
                file_date = date

                # 提取决策
                if context_type in ["decision", "general"]:
                    decisions_match = re.search(r"## Decisions Made\s*\n([\s\S]*?)(?=##|$)", content)
                    if decisions_match:
                        for line in decisions_match.group(1).split("\n"):
                            line = line.strip("- ")
                            if line and self._is_relevant(line, query, context_type):
                                time_decay = self._time_decay(i, days)
                                memories.append({
                                    "content": line,
                                    "source": f"daily/{date_str}",
                                    "score": 0.6 * time_decay,
                                    "timestamp": file_date,
                                    "type": "decision"
                                })

                # 提取教训
                if context_type in ["fact", "general"]:
                    lessons_match = re.search(r"## Lessons Learned\s*\n([\s\S]*?)(?=##|$)", content)
                    if lessons_match:
                        for line in lessons_match.group(1).split("\n"):
                            line = line.strip("- ")
                            if line and self._is_relevant(line, query, context_type):
                                time_decay = self._time_decay(i, days)
                                memories.append({
                                    "content": line,
                                    "source": f"daily/{date_str}",
                                    "score": 0.55 * time_decay,
                                    "timestamp": file_date,
                                    "type": "lesson"
                                })

        return memories

    def _rank_memories(self, memories: List[Dict], query: str, context_type: str) -> List[Dict]:
        """
        多维度排序：
        1. 基础评分（来源权重）
        2. 语义相关性（关键词匹配）
        3. 时间衰减
        4. 类型权重
        """
        type_weights = {
            "current_task": 1.0,
            "decision": 0.9,
            "preference": 0.85,
            "context": 0.8,
            "lesson": 0.7
        }

        for memory in memories:
            base_score = memory["score"]
            type_weight = type_weights.get(memory["type"], 0.7)

            # 语义相关性评分（关键词匹配）
            relevance = self._calculate_relevance(memory["content"], query)

            # 综合评分
            memory["final_score"] = base_score * type_weight * relevance

        # 按最终评分排序
        ranked = sorted(memories, key=lambda x: x["final_score"], reverse=True)

        # 返回 Top 10
        return ranked[:10]

    def _is_relevant(self, content: str, query: str, context_type: str) -> bool:
        """判断内容是否相关"""
        query_lower = query.lower()
        content_lower = content.lower()

        # 直接关键词匹配
        if any(word in content_lower for word in query_lower.split()):
            return True

        # 根据上下文类型的启发式规则
        if context_type == "preference":
            pref_keywords = ["prefer", "like", "want", "always", "never"]
            return any(kw in content_lower for kw in pref_keywords)
        elif context_type == "decision":
            decision_keywords = ["decided", "will", "going to", "choose"]
            return any(kw in content_lower for kw in decision_keywords)

        return False

    def _calculate_importance(self, content: str, section: str) -> float:
        """计算记忆重要性（基于内容特征）"""
        importance = 1.0

        # 较长的内容通常更重要
        if len(content) > 100:
            importance *= 1.2

        # 包含特定关键词的内容更重要
        important_keywords = ["critical", "important", "must", "never", "always"]
        if any(kw in content.lower() for kw in important_keywords):
            importance *= 1.3

        return min(importance, 2.0)

    def _time_decay(self, days_ago: int, max_days: int) -> float:
        """时间衰减函数：越近的记忆权重越高"""
        if days_ago >= max_days:
            return 0.3
        return 1.0 - (days_ago / max_days) * 0.5

    def _calculate_relevance(self, content: str, query: str) -> float:
        """计算语义相关性"""
        content_words = set(content.lower().split())
        query_words = set(query.lower().split())

        if not query_words:
            return 0.5

        # Jaccard 相似度
        intersection = len(content_words & query_words)
        union = len(content_words | query_words)

        jaccard = intersection / union if union > 0 else 0

        # 基础相关性，范围 [0.3, 1.0]
        return max(0.3, jaccard * 2)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="智能记忆检索")
    parser.add_argument("query", help="查询内容")
    parser.add_argument("--type", choices=["general", "decision", "preference", "fact"],
                       default="general", help="上下文类型")
    parser.add_argument("--workspace", default=".", help="工作目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    retriever = MemoryRetrieve(args.workspace)
    results = retriever.retrieve(args.query, args.type)

    if args.json:
        output = []
        for r in results:
            output.append({
                "content": r["content"],
                "source": r["source"],
                "score": round(r["final_score"], 3),
                "type": r["type"]
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"🧠 检索结果 (Top {len(results)})")
        print("-" * 50)
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['type']}] {r['content']}")
            print(f"   来源: {r['source']} | 评分: {r['final_score']:.3f}")
            print()


if __name__ == "__main__":
    main()
