#!/usr/bin/env python3
"""
记忆重要性评分模块
基于时间衰减、访问频率、内容特征计算记忆的重要性评分
"""
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple


class MemoryScorer:
    """
    记忆重要性评分器

    评分维度：
    1. 时间新鲜度 (Time Freshness): 越新的记忆越重要
    2. 访问频率 (Access Frequency): 频繁访问的记忆更持久
    3. 内容重要性 (Content Importance): 长度、关键词、类型
    4. 用户标记 (User Marking): 显式标记的记忆权重更高
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.session_state = self.workspace / "SESSION-STATE.md"
        self.memory_md = self.workspace / "MEMORY.md"
        self.memory_dir = self.workspace / "memory"
        self.access_log = self.workspace / ".memory-access.log"

    def score_memory(self, content: str, memory_type: str,
                    timestamp: datetime = None, source: str = "") -> float:
        """
        计算单个记忆的重要性评分

        Args:
            content: 记忆内容
            memory_type: 记忆类型 (decision, preference, fact, lesson, context)
            timestamp: 记忆时间戳
            source: 记忆来源

        Returns:
            重要性评分 [0.0, 1.0]
        """
        if timestamp is None:
            timestamp = datetime.now()

        # 1. 时间新鲜度评分 [0.2, 1.0]
        time_score = self._time_freshness_score(timestamp)

        # 2. 内容重要性评分 [0.3, 1.0]
        content_score = self._content_importance_score(content, memory_type)

        # 3. 访问频率评分 [0.5, 1.0]
        access_score = self._access_frequency_score(content, source)

        # 4. 类型权重 [0.5, 1.0]
        type_weight = self._get_type_weight(memory_type)

        # 5. 综合评分（加权平均）
        final_score = (
            time_score * 0.25 +
            content_score * 0.35 +
            access_score * 0.20 +
            type_weight * 0.20
        )

        return round(final_score, 3)

    def _time_freshness_score(self, timestamp: datetime) -> float:
        """
        时间新鲜度评分
        使用指数衰减函数：越新的记忆评分越高
        """
        now = datetime.now()
        days_old = (now - timestamp).days

        # 指数衰减：30天后评分降到 0.5
        decay_rate = 0.05  # 每天衰减 5%
        fresh_score = max(0.2, 1.0 * (2.718 ** (-decay_rate * days_old)))

        return fresh_score

    def _content_importance_score(self, content: str, memory_type: str) -> float:
        """
        内容重要性评分
        基于内容长度、关键词、结构特征
        """
        score = 0.5  # 基础分

        # 1. 长度评分（适中的长度更可能重要）
        content_len = len(content)
        if 50 <= content_len <= 200:
            score += 0.2
        elif content_len > 200:
            score += 0.3

        # 2. 关键词评分
        critical_keywords = ["critical", "important", "must", "never", "always",
                           "关键", "重要", "必须", "禁止", "永远"]
        if any(kw in content.lower() for kw in critical_keywords):
            score += 0.2

        # 3. 结构评分（包含原因、理由的内容更重要）
        if "because" in content.lower() or "因为" in content:
            score += 0.1
        if "reason" in content.lower() or "reason" in content.lower() or "原因" in content:
            score += 0.1

        # 4. 类型特定评分
        if memory_type == "decision":
            score += 0.1  # 决策通常很重要
        elif memory_type == "preference":
            score += 0.05  # 偏好中等重要
        elif memory_type == "lesson":
            score += 0.15  # 教训通常很重要

        return min(score, 1.0)

    def _access_frequency_score(self, content: str, source: str) -> float:
        """
        访问频率评分
        从访问日志中统计该记忆的访问次数
        """
        if not self.access_log.exists():
            return 0.5  # 无访问记录，给予中等分

        # 计算内容的哈希值作为唯一标识
        content_hash = hash(content + source)

        # 读取访问日志
        try:
            with open(self.access_log, "r") as f:
                log_content = f.read()
        except:
            return 0.5

        # 统计访问次数
        access_count = log_content.count(str(content_hash))

        # 访问频率评分：访问越多，评分越高
        # 0次访问 -> 0.5，10次以上 -> 1.0
        access_score = min(1.0, 0.5 + access_count * 0.05)

        return access_score

    def _get_type_weight(self, memory_type: str) -> float:
        """获取记忆类型的权重"""
        type_weights = {
            "current_task": 1.0,
            "decision": 0.9,
            "preference": 0.85,
            "lesson": 0.8,
            "fact": 0.75,
            "context": 0.7
        }
        return type_weights.get(memory_type, 0.7)

    def log_access(self, content: str, source: str):
        """
        记录记忆访问
        """
        content_hash = hash(content + source)
        timestamp = datetime.now().isoformat()

        log_entry = f"{timestamp} | {content_hash}\n"

        try:
            with open(self.access_log, "a") as f:
                f.write(log_entry)
        except:
            pass  # 忽略日志记录失败

    def prune_old_logs(self, days: int = 30):
        """
        清理旧的访问日志（保留最近 N 天）
        """
        if not self.access_log.exists():
            return

        cutoff_date = datetime.now() - timedelta(days=days)
        new_log_entries = []

        try:
            with open(self.access_log, "r") as f:
                for line in f:
                    if "|" in line:
                        timestamp_str = line.split("|")[0].strip()
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str)
                            if timestamp >= cutoff_date:
                                new_log_entries.append(line)
                        except:
                            continue

            # 重写日志
            with open(self.access_log, "w") as f:
                f.writelines(new_log_entries)

        except:
            pass

    def batch_score(self, memories: List[Dict]) -> List[Dict]:
        """
        批量评分

        Args:
            memories: 记忆列表，每项包含 content, type, timestamp, source

        Returns:
            添加了 score 字段的记忆列表
        """
        scored_memories = []

        for memory in memories:
            timestamp = memory.get("timestamp")
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)

            score = self.score_memory(
                memory["content"],
                memory["type"],
                timestamp,
                memory.get("source", "")
            )

            memory_copy = memory.copy()
            memory_copy["score"] = score
            scored_memories.append(memory_copy)

        # 按评分排序
        scored_memories.sort(key=lambda x: x["score"], reverse=True)

        return scored_memories


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="记忆重要性评分")
    parser.add_argument("content", help="记忆内容")
    parser.add_argument("--type", default="general",
                       choices=["decision", "preference", "fact", "lesson", "context"],
                       help="记忆类型")
    parser.add_argument("--workspace", default=".", help="工作目录")
    parser.add_argument("--log-access", action="store_true",
                       help="记录此次访问")
    parser.add_argument("--prune-logs", type=int, metavar="DAYS",
                       help="清理旧日志（保留最近 N 天）")

    args = parser.parse_args()

    scorer = MemoryScorer(args.workspace)

    if args.prune_logs:
        scorer.prune_old_logs(args.prune_logs)
        print(f"✓ 已清理 {args.prune_logs} 天前的访问日志")
        return

    timestamp = datetime.now()
    score = scorer.score_memory(args.content, args.type, timestamp)

    print(f"📊 记忆重要性评分")
    print(f"内容: {args.content}")
    print(f"类型: {args.type}")
    print(f"评分: {score:.3f}")
    print(f"时间: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    if args.log_access:
        scorer.log_access(args.content, "manual")
        print("✓ 已记录访问日志")


if __name__ == "__main__":
    main()
