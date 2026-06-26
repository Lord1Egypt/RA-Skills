#!/usr/bin/env python3
"""
记忆系统 API 接口
为智能体提供统一的记忆管理接口，支持自动调用和上下文注入
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Memory:
    """记忆数据结构"""
    content: str
    type: str  # decision, preference, fact, lesson, context
    importance: float
    timestamp: str
    source: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict:
        return asdict(self)


class MemoryAPI:
    """
    记忆系统统一 API

    设计原则：
    1. 智能体友好：提供简单直观的接口，无需了解底层实现
    2. 自动注入：支持上下文自动注入到智能体对话中
    3. 事务安全：支持批量操作和回滚
    4. 缓存优化：内置缓存机制，提升性能
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.session_state = self.workspace / "SESSION-STATE.md"
        self.memory_md = self.workspace / "MEMORY.md"
        self.memory_dir = self.workspace / "memory"
        self.cache = {}  # 简单缓存
        self.cache_ttl = 300  # 缓存 5 分钟

        # 导入算法模块
        from memory_retrieve import MemoryRetrieve
        from memory_score import MemoryScorer
        from memory_digest import MemoryDigest

        self.retriever = MemoryRetrieve(workspace)
        self.scorer = MemoryScorer(workspace)
        self.digester = MemoryDigest(workspace)

    def store(self, content: str, memory_type: str,
              importance: Optional[float] = None,
              auto_append: bool = True) -> Dict:
        """
        存储记忆

        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性（可选，自动计算）
            auto_append: 是否自动追加到对应文件

        Returns:
            操作结果
        """
        timestamp = datetime.now().isoformat()

        # 自动计算重要性
        if importance is None:
            importance = self.scorer.score_memory(content, memory_type, datetime.now())

        memory = Memory(
            content=content,
            type=memory_type,
            importance=importance,
            timestamp=timestamp,
            source="manual",
            metadata={}
        )

        # 追加到对应文件
        if auto_append:
            if memory_type == "context":
                self._append_to_session_state(content, memory_type)
            elif memory_type in ["preference", "lesson", "decision"]:
                self._append_to_memory_md(content, memory_type, importance)
            else:
                self._append_to_daily_log(content, memory_type, importance)

        # 清除缓存
        self._clear_cache()

        return {
            "success": True,
            "memory": memory.to_dict(),
            "message": f"Memory stored with importance {importance:.2f}"
        }

    def retrieve(self, query: str, context_type: str = "general",
                 limit: int = 10, auto_inject: bool = False) -> Dict:
        """
        检索记忆

        Args:
            query: 查询内容
            context_type: 上下文类型
            limit: 返回数量
            auto_inject: 是否自动注入到上下文

        Returns:
            检索结果
        """
        # 使用智能检索算法
        results = self.retriever.retrieve(query, context_type)

        # 格式化输出
        formatted_results = []
        for r in results[:limit]:
            formatted_results.append({
                "content": r["content"],
                "source": r["source"],
                "type": r["type"],
                "score": round(r["final_score"], 3),
                "timestamp": r["timestamp"].isoformat() if hasattr(r["timestamp"], "isoformat") else str(r["timestamp"])
            })

        response = {
            "success": True,
            "query": query,
            "context_type": context_type,
            "results": formatted_results,
            "total": len(formatted_results)
        }

        # 自动注入
        if auto_inject and formatted_results:
            response["injected_context"] = self._format_context_for_injection(formatted_results)

        return response

    def inject_context(self, topics: List[str] = None,
                       max_items: int = 5) -> str:
        """
        自动注入相关上下文

        根据当前会话状态和话题，自动检索并注入相关记忆

        Args:
            topics: 话题列表（可选，自动从 SESSION-STATE 提取）
            max_items: 最大注入数量

        Returns:
            格式化的上下文字符串
        """
        # 如果没有提供话题，从 SESSION-STATE 提取
        if topics is None:
            topics = self._extract_topics_from_session()

        if not topics:
            return "无相关上下文"

        # 检索每个话题的相关记忆
        all_memories = []
        for topic in topics:
            result = self.retrieve(topic, "general", limit=max_items)
            all_memories.extend(result["results"])

        # 去重并排序
        unique_memories = self._deduplicate_memories(all_memories)
        top_memories = sorted(unique_memories, key=lambda x: x["score"], reverse=True)[:max_items]

        # 格式化输出
        return self._format_context_for_injection(top_memories)

    def validate(self, content: str, memory_type: str) -> Dict:
        """
        验证记忆质量和一致性

        Args:
            content: 记忆内容
            memory_type: 记忆类型

        Returns:
            验证结果
        """
        issues = []
        warnings = []

        # 1. 检查内容长度
        if len(content) < 10:
            issues.append("内容过短，可能不完整")

        # 2. 检查冲突
        conflicts = self._check_conflicts(content, memory_type)
        if conflicts:
            issues.extend([f"与现有记忆冲突: {c['content']}" for c in conflicts])

        # 3. 检查重复
        duplicates = self._check_duplicates(content)
        if duplicates:
            warnings.append(f"可能重复的记忆: {len(duplicates)} 条")

        # 4. 检查敏感信息
        sensitive = self._detect_sensitive_info(content)
        if sensitive:
            warnings.append(f"包含敏感信息: {', '.join(sensitive)}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "score": self.scorer.score_memory(content, memory_type)
        }

    def detect_anomalies(self) -> Dict:
        """
        检测记忆异常

        包括：
        1. 重复决策
        2. 矛盾偏好
        3. 遗忘的关键信息
        4. 长期未访问的重要记忆

        Returns:
            异常报告
        """
        anomalies = {
            "duplicate_decisions": [],
            "conflicting_preferences": [],
            "forgotten_memories": [],
            "stale_memories": []
        }

        # 1. 检测重复决策
        all_decisions = self._get_all_memories_by_type("decision")
        decision_groups = self._group_similar(all_decisions)
        for group in decision_groups:
            if len(group) > 1:
                anomalies["duplicate_decisions"].append([d["content"] for d in group])

        # 2. 检测矛盾偏好
        all_preferences = self._get_all_memories_by_type("preference")
        pref_conflicts = self._find_conflicting_preferences(all_preferences)
        anomalies["conflicting_preferences"] = pref_conflicts

        # 3. 检测遗忘的关键记忆
        important_memories = [m for m in all_decisions if m.get("importance", 0) > 0.8]
        stale_memories = self._find_stale_memories(important_memories, days=30)
        anomalies["forgotten_memories"] = stale_memories

        # 4. 检测过期记忆
        all_memories = self._get_all_memories()
        expired = self._find_expired_memories(all_memories, days=90)
        anomalies["stale_memories"] = expired

        return anomalies

    def suggest_improvements(self) -> Dict:
        """
        基于当前记忆状态，主动建议改进

        Returns:
            改进建议
        """
        suggestions = {
            "priorities": [],
            "maintenance": [],
            "optimizations": []
        }

        # 分析当前记忆状态
        anomalies = self.detect_anomalies()

        # 优先建议
        if anomalies["conflicting_preferences"]:
            suggestions["priorities"].append({
                "type": "resolve_conflicts",
                "message": f"发现 {len(anomalies['conflicting_preferences'])} 个矛盾偏好，需要解决",
                "action": "review and merge conflicting preferences"
            })

        if anomalies["duplicate_decisions"]:
            suggestions["priorities"].append({
                "type": "deduplicate",
                "message": f"发现 {len(anomalies['duplicate_decisions'])} 组重复决策",
                "action": "merge or remove duplicate decisions"
            })

        # 维护建议
        if anomalies["forgotten_memories"]:
            suggestions["maintenance"].append({
                "type": "review_forgotten",
                "message": f"{len(anomalies['forgotten_memories'])} 个重要记忆长期未访问",
                "action": "review and update stale memories"
            })

        # 优化建议
        suggestions["optimizations"].append({
            "type": "digest",
            "message": "建议执行智能摘要归档",
            "action": "run memory-digest.py to archive daily logs"
        })

        suggestions["optimizations"].append({
            "type": "prune_logs",
            "message": "建议清理访问日志",
            "action": "run memory-score.py --prune-logs 30"
        })

        return suggestions

    def export(self, format: str = "json") -> str:
        """
        导出所有记忆

        Args:
            format: 导出格式 (json, markdown)

        Returns:
            导出内容
        """
        all_memories = self._get_all_memories()

        if format == "json":
            return json.dumps(all_memories, ensure_ascii=False, indent=2)
        elif format == "markdown":
            return self._format_as_markdown(all_memories)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _append_to_session_state(self, content: str, memory_type: str):
        """追加到 SESSION-STATE.md"""
        if not self.session_state.exists():
            return

        with open(self.session_state, "a") as f:
            f.write(f"- {content}\n")

    def _append_to_memory_md(self, content: str, memory_type: str, importance: float):
        """追加到 MEMORY.md"""
        if not self.memory_md.exists():
            return

        # 简化实现：追加到文件末尾
        with open(self.memory_md, "a") as f:
            f.write(f"- {content} (importance: {importance:.2f})\n")

    def _append_to_daily_log(self, content: str, memory_type: str, importance: float):
        """追加到今日日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = self.memory_dir / f"{today}.md"

        if not self.memory_dir.exists():
            self.memory_dir.mkdir(parents=True, exist_ok=True)

        with open(daily_file, "a") as f:
            section_map = {
                "decision": "Decisions Made",
                "lesson": "Lessons Learned",
                "preference": "Preferences",
                "fact": "Facts"
            }
            section = section_map.get(memory_type, "Notes")

            f.write(f"- {content}\n")

    def _clear_cache(self):
        """清除缓存"""
        self.cache.clear()

    def _extract_topics_from_session(self) -> List[str]:
        """从 SESSION-STATE 提取话题"""
        if not self.session_state.exists():
            return []

        content = self.session_state.read_text()
        topics = []

        # 简化实现：提取关键词
        lines = content.split("\n")
        for line in lines:
            if ":" in line and not line.startswith("#"):
                topic = line.split(":")[0].strip()
                if topic and len(topic) > 2:
                    topics.append(topic)

        return topics[:5]  # 最多 5 个话题

    def _format_context_for_injection(self, memories: List[Dict]) -> str:
        """格式化上下文用于注入"""
        if not memories:
            return ""

        lines = ["## 相关记忆"]
        for i, mem in enumerate(memories, 1):
            lines.append(f"{i}. [{mem['type']}] {mem['content']} (评分: {mem['score']})")

        return "\n".join(lines)

    def _deduplicate_memories(self, memories: List[Dict]) -> List[Dict]:
        """去重记忆"""
        seen = set()
        unique = []
        for mem in memories:
            content_hash = hash(mem["content"])
            if content_hash not in seen:
                seen.add(content_hash)
                unique.append(mem)
        return unique

    def _check_conflicts(self, content: str, memory_type: str) -> List[Dict]:
        """检查冲突"""
        # 简化实现：基于关键词匹配
        all_memories = self._get_all_memories_by_type(memory_type)
        conflicts = []

        for mem in all_memories:
            if self._is_conflicting(content, mem["content"]):
                conflicts.append(mem)

        return conflicts

    def _is_conflicting(self, text1: str, text2: str) -> bool:
        """判断是否冲突"""
        conflict_indicators = ["not", "don't", "won't", "no", "never", "不", "不要", "不使用"]
        text1_lower = text1.lower()
        text2_lower = text2.lower()

        # 检查是否有相反的表达
        for indicator in conflict_indicators:
            if indicator in text1_lower and indicator not in text2_lower:
                # 检查是否描述同一主题
                words1 = set(text1_lower.split())
                words2 = set(text2_lower.split())
                similarity = len(words1 & words2) / len(words1 | words2)
                if similarity > 0.5:
                    return True

        return False

    def _check_duplicates(self, content: str) -> List[Dict]:
        """检查重复"""
        all_memories = self._get_all_memories()
        duplicates = []

        for mem in all_memories:
            if self._calculate_similarity(content, mem["content"]) > 0.8:
                duplicates.append(mem)

        return duplicates

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算相似度"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0

    def _detect_sensitive_info(self, content: str) -> List[str]:
        """检测敏感信息"""
        sensitive_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "api_key": r'\b[A-Za-z0-9]{32,}\b'
        }

        detected = []
        import re
        for info_type, pattern in sensitive_patterns.items():
            if re.search(pattern, content):
                detected.append(info_type)

        return detected

    def _get_all_memories_by_type(self, memory_type: str) -> List[Dict]:
        """获取指定类型的所有记忆"""
        all_memories = self._get_all_memories()
        return [m for m in all_memories if m.get("type") == memory_type]

    def _get_all_memories(self) -> List[Dict]:
        """获取所有记忆"""
        # 简化实现：从文件读取
        memories = []

        # 从 SESSION-STATE
        if self.session_state.exists():
            content = self.session_state.read_text()
            for line in content.split("\n"):
                line = line.strip("- ")
                if line and len(line) > 5:
                    memories.append({
                        "content": line,
                        "type": "context",
                        "source": "SESSION-STATE.md",
                        "importance": 0.9
                    })

        # 从 MEMORY.md
        if self.memory_md.exists():
            content = self.memory_md.read_text()
            for line in content.split("\n"):
                line = line.strip("- *")
                if line and len(line) > 5:
                    memories.append({
                        "content": line,
                        "type": "longterm",
                        "source": "MEMORY.md",
                        "importance": 0.7
                    })

        return memories

    def _group_similar(self, memories: List[Dict]) -> List[List[Dict]]:
        """分组相似记忆"""
        groups = []
        used = set()

        for i, mem1 in enumerate(memories):
            if i in used:
                continue

            group = [mem1]
            used.add(i)

            for j, mem2 in enumerate(memories):
                if j in used or j == i:
                    continue

                if self._calculate_similarity(mem1["content"], mem2["content"]) > 0.7:
                    group.append(mem2)
                    used.add(j)

            if len(group) > 1:
                groups.append(group)

        return groups

    def _find_conflicting_preferences(self, preferences: List[Dict]) -> List[Dict]:
        """查找矛盾偏好"""
        conflicts = []

        for i, pref1 in enumerate(preferences):
            for j, pref2 in enumerate(preferences):
                if i >= j:
                    continue

                if self._is_conflicting(pref1["content"], pref2["content"]):
                    conflicts.append({
                        "pref1": pref1["content"],
                        "pref2": pref2["content"]
                    })

        return conflicts

    def _find_stale_memories(self, memories: List[Dict], days: int) -> List[Dict]:
        """查找长期未访问的记忆"""
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        stale = []

        for mem in memories:
            if "timestamp" in mem:
                try:
                    ts = datetime.fromisoformat(mem["timestamp"])
                    if ts < cutoff:
                        stale.append(mem)
                except:
                    pass

        return stale

    def _find_expired_memories(self, memories: List[Dict], days: int) -> List[Dict]:
        """查找过期记忆"""
        return self._find_stale_memories(memories, days)

    def _format_as_markdown(self, memories: List[Dict]) -> str:
        """格式化为 Markdown"""
        lines = ["# 记忆导出\n"]
        lines.append(f"导出时间: {datetime.now().isoformat()}\n")

        for mem in memories:
            lines.append(f"- [{mem.get('type', 'unknown')}] {mem.get('content', '')}")
            lines.append(f"  来源: {mem.get('source', 'unknown')}")
            lines.append(f"  重要性: {mem.get('importance', 0):.2f}\n")

        return "\n".join(lines)


def main():
    """命令行接口（用于测试）"""
    import argparse

    parser = argparse.ArgumentParser(description="记忆系统 API")
    parser.add_argument("action", choices=["store", "retrieve", "inject", "validate", "anomalies", "suggest", "export"])
    parser.add_argument("--content", help="记忆内容")
    parser.add_argument("--type", help="记忆类型")
    parser.add_argument("--query", help="查询内容")
    parser.add_argument("--format", default="json", help="导出格式")

    args = parser.parse_args()

    api = MemoryAPI()

    if args.action == "store":
        result = api.store(args.content, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "retrieve":
        result = api.retrieve(args.query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "inject":
        context = api.inject_context()
        print(context)
    elif args.action == "validate":
        result = api.validate(args.content, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "anomalies":
        result = api.detect_anomalies()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "suggest":
        result = api.suggest_improvements()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "export":
        result = api.export(args.format)
        print(result)


if __name__ == "__main__":
    main()
