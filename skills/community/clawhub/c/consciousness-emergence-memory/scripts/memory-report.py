#!/usr/bin/env python3
"""
记忆分析和报告生成模块
生成全面的分析报告，包括记忆质量、使用模式、改进建议等
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


class MemoryAnalyzer:
    """
    记忆分析器

    生成多维度的分析报告：
    1. 统计概览（数量、类型、时间分布）
    2. 质量评估（重复率、冲突率、完整度）
    3. 使用模式（访问频率、热门主题）
    4. 智能建议（优化方向、待处理事项）
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.session_state = self.workspace / "SESSION-STATE.md"
        self.memory_md = self.workspace / "MEMORY.md"
        self.memory_dir = self.workspace / "memory"

    def generate_report(self, include_recommendations: bool = True) -> Dict:
        """
        生成完整分析报告

        Args:
            include_recommendations: 是否包含改进建议

        Returns:
            分析报告
        """
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "workspace": str(self.workspace)
            },
            "statistics": self._generate_statistics(),
            "quality": self._assess_quality(),
            "usage_patterns": self._analyze_usage_patterns(),
            "health_score": 0.0
        }

        # 计算健康分数
        report["health_score"] = self._calculate_health_score(report)

        # 生成建议
        if include_recommendations:
            report["recommendations"] = self._generate_recommendations(report)

        return report

    def _generate_statistics(self) -> Dict:
        """生成统计信息"""
        stats = {
            "total_memories": 0,
            "by_type": defaultdict(int),
            "by_source": defaultdict(int),
            "by_date": defaultdict(int),
            "average_importance": 0.0,
            "importance_distribution": {"high": 0, "medium": 0, "low": 0}
        }

        # 统计所有记忆
        all_memories = self._get_all_memories()

        for mem in all_memories:
            stats["total_memories"] += 1

            mem_type = mem.get("type", "unknown")
            stats["by_type"][mem_type] += 1

            source = mem.get("source", "unknown")
            stats["by_source"][source] += 1

            # 日期分布
            if "timestamp" in mem:
                date = mem["timestamp"][:10]  # YYYY-MM-DD
                stats["by_date"][date] += 1

            # 重要性分布
            importance = mem.get("importance", 0)
            if importance >= 0.8:
                stats["importance_distribution"]["high"] += 1
            elif importance >= 0.5:
                stats["importance_distribution"]["medium"] += 1
            else:
                stats["importance_distribution"]["low"] += 1

        # 计算平均重要性
        if stats["total_memories"] > 0:
            total_importance = sum(m.get("importance", 0) for m in all_memories)
            stats["average_importance"] = total_importance / stats["total_memories"]

        return dict(stats)

    def _assess_quality(self) -> Dict:
        """评估记忆质量"""
        quality = {
            "completeness": 0.0,  # 完整度
            "consistency": 0.0,   # 一致性
            "uniqueness": 0.0,    # 唯一性
            "freshness": 0.0,     # 新鲜度
            "overall": 0.0
        }

        all_memories = self._get_all_memories()

        if not all_memories:
            return quality

        # 1. 完整度：检查是否有缺失的必要字段
        complete_count = 0
        for mem in all_memories:
            if all(k in mem for k in ["content", "type", "importance"]):
                complete_count += 1
        quality["completeness"] = complete_count / len(all_memories)

        # 2. 一致性：检查冲突和矛盾
        conflicts = self._find_conflicts(all_memories)
        quality["consistency"] = max(0.0, 1.0 - len(conflicts) / len(all_memories))

        # 3. 唯一性：检查重复
        duplicates = self._find_duplicates(all_memories)
        quality["uniqueness"] = max(0.0, 1.0 - len(duplicates) / len(all_memories))

        # 4. 新鲜度：检查记忆的平均年龄
        avg_age = self._calculate_average_age(all_memories)
        quality["freshness"] = max(0.0, 1.0 - avg_age / 180)  # 6个月为完全过期

        # 综合质量
        quality["overall"] = (
            quality["completeness"] * 0.3 +
            quality["consistency"] * 0.3 +
            quality["uniqueness"] * 0.2 +
            quality["freshness"] * 0.2
        )

        return quality

    def _analyze_usage_patterns(self) -> Dict:
        """分析使用模式"""
        patterns = {
            "access_frequency": {},
            "top_entities": [],
            "topic_clusters": [],
            "growth_trend": []
        }

        # 读取访问日志
        access_log = self.workspace / ".memory-access.log"
        if access_log.exists():
            with open(access_log, "r") as f:
                access_records = f.readlines()

            # 统计访问频率
            access_freq = defaultdict(int)
            for record in access_records:
                if "|" in record:
                    content_hash = record.split("|")[1].strip()
                    access_freq[content_hash] += 1

            patterns["access_frequency"] = dict(access_freq)

        # 提取热门实体（简化实现）
        all_memories = self._get_all_memories()
        entity_counts = defaultdict(int)

        for mem in all_memories:
            content = mem.get("content", "")
            # 简化：提取关键词
            words = content.split()
            for word in words:
                if len(word) > 3:  # 忽略短词
                    entity_counts[word] += 1

        # Top 10 实体
        top_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        patterns["top_entities"] = [{"entity": e, "count": c} for e, c in top_entities]

        # 增长趋势（按日期统计）
        date_counts = defaultdict(int)
        for mem in all_memories:
            if "timestamp" in mem:
                date = mem["timestamp"][:10]
                date_counts[date] += 1

        sorted_dates = sorted(date_counts.items())
        patterns["growth_trend"] = [{"date": d, "count": c} for d, c in sorted_dates[-7:]]  # 最近7天

        return patterns

    def _calculate_health_score(self, report: Dict) -> float:
        """计算健康分数（0-100）"""
        quality = report["quality"]["overall"]
        stats = report["statistics"]

        # 基础分：质量分数
        health = quality * 100

        # 加分项
        if stats["total_memories"] > 10:
            health += 5  # 有一定数量的记忆
        if stats["average_importance"] > 0.6:
            health += 5  # 平均重要性较高
        if stats["importance_distribution"]["high"] > 0:
            health += 5  # 有高重要性记忆

        # 减分项
        if stats["importance_distribution"]["low"] / max(stats["total_memories"], 1) > 0.5:
            health -= 10  # 低重要性记忆过多

        return round(max(0.0, min(100.0, health)), 1)

    def _generate_recommendations(self, report: Dict) -> List[Dict]:
        """生成改进建议"""
        recommendations = []

        # 基于质量分数
        quality = report["quality"]
        if quality["completeness"] < 0.8:
            recommendations.append({
                "priority": "high",
                "category": "completeness",
                "message": "部分记忆缺少必要字段，建议完善",
                "action": "review and update incomplete memories"
            })

        if quality["consistency"] < 0.7:
            recommendations.append({
                "priority": "high",
                "category": "consistency",
                "message": "发现冲突或矛盾的记忆",
                "action": "resolve conflicts and contradictions"
            })

        if quality["uniqueness"] < 0.7:
            recommendations.append({
                "priority": "medium",
                "category": "uniqueness",
                "message": "存在重复记忆",
                "action": "merge or remove duplicate memories"
            })

        if quality["freshness"] < 0.5:
            recommendations.append({
                "priority": "medium",
                "category": "freshness",
                "message": "记忆较为陈旧，建议更新",
                "action": "review and update old memories"
            })

        # 基于统计
        stats = report["statistics"]
        if stats["total_memories"] < 10:
            recommendations.append({
                "priority": "low",
                "category": "quantity",
                "message": "记忆数量较少，建议持续积累",
                "action": "actively store important information"
            })

        if stats["average_importance"] < 0.5:
            recommendations.append({
                "priority": "low",
                "category": "importance",
                "message": "平均重要性较低，建议关注高价值内容",
                "action": "focus on storing high-importance information"
            })

        # 基于使用模式
        patterns = report["usage_patterns"]
        if not patterns["top_entities"]:
            recommendations.append({
                "priority": "low",
                "category": "patterns",
                "message": "未发现明显模式",
                "action": "continue collecting memories to identify patterns"
            })

        return recommendations

    def _get_all_memories(self) -> List[Dict]:
        """获取所有记忆"""
        # 简化实现：从文件读取
        memories = []

        if self.session_state.exists():
            content = self.session_state.read_text()
            for line in content.split("\n"):
                line = line.strip("- ")
                if line and len(line) > 5:
                    memories.append({
                        "content": line,
                        "type": "context",
                        "source": "SESSION-STATE.md",
                        "importance": 0.9,
                        "timestamp": datetime.now().isoformat()
                    })

        if self.memory_md.exists():
            content = self.memory_md.read_text()
            for line in content.split("\n"):
                line = line.strip("- *")
                if line and len(line) > 5:
                    memories.append({
                        "content": line,
                        "type": "longterm",
                        "source": "MEMORY.md",
                        "importance": 0.7,
                        "timestamp": (datetime.now() - timedelta(days=30)).isoformat()
                    })

        return memories

    def _find_conflicts(self, memories: List[Dict]) -> List[Dict]:
        """查找冲突"""
        conflicts = []
        for i, mem1 in enumerate(memories):
            for j, mem2 in enumerate(memories):
                if i >= j:
                    continue
                if self._is_conflicting(mem1["content"], mem2["content"]):
                    conflicts.append({"mem1": mem1, "mem2": mem2})
        return conflicts

    def _is_conflicting(self, text1: str, text2: str) -> bool:
        """判断是否冲突"""
        conflict_indicators = ["not", "don't", "won't", "no", "never", "不", "不要"]
        text1_lower = text1.lower()
        text2_lower = text2.lower()

        for indicator in conflict_indicators:
            if indicator in text1_lower and indicator not in text2_lower:
                words1 = set(text1_lower.split())
                words2 = set(text2_lower.split())
                similarity = len(words1 & words2) / len(words1 | words2)
                if similarity > 0.5:
                    return True
        return False

    def _find_duplicates(self, memories: List[Dict]) -> List[Dict]:
        """查找重复"""
        duplicates = []
        seen = set()
        for mem in memories:
            content_hash = hash(mem["content"])
            if content_hash in seen:
                duplicates.append(mem)
            seen.add(content_hash)
        return duplicates

    def _calculate_average_age(self, memories: List[Dict]) -> float:
        """计算平均年龄（天数）"""
        ages = []
        now = datetime.now()
        for mem in memories:
            if "timestamp" in mem:
                try:
                    ts = datetime.fromisoformat(mem["timestamp"])
                    age = (now - ts).days
                    ages.append(age)
                except:
                    pass
        return sum(ages) / len(ages) if ages else 0

    def export_report(self, format: str = "markdown") -> str:
        """
        导出分析报告

        Args:
            format: 输出格式 (markdown, json)

        Returns:
            格式化报告
        """
        report = self.generate_report()

        if format == "json":
            return json.dumps(report, ensure_ascii=False, indent=2)
        elif format == "markdown":
            return self._format_as_markdown(report)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _format_as_markdown(self, report: Dict) -> str:
        """格式化为 Markdown"""
        lines = [
            "# 记忆系统分析报告",
            "",
            f"**生成时间**: {report['metadata']['generated_at']}",
            f"**健康分数**: {report['health_score']}/100",
            "",
            "## 统计概览",
            "",
            f"- **总记忆数**: {report['statistics']['total_memories']}",
            f"- **平均重要性**: {report['statistics']['average_importance']:.2f}",
            "",
            "### 按类型分布"
        ]

        for mem_type, count in report['statistics']['by_type'].items():
            lines.append(f"- {mem_type}: {count}")

        lines.extend([
            "",
            "### 重要性分布",
            f"- 高 (>0.8): {report['statistics']['importance_distribution']['high']}",
            f"- 中 (0.5-0.8): {report['statistics']['importance_distribution']['medium']}",
            f"- 低 (<0.5): {report['statistics']['importance_distribution']['low']}",
            "",
            "## 质量评估",
            "",
            f"- **完整度**: {report['quality']['completeness']:.2%}",
            f"- **一致性**: {report['quality']['consistency']:.2%}",
            f"- **唯一性**: {report['quality']['uniqueness']:.2%}",
            f"- **新鲜度**: {report['quality']['freshness']:.2%}",
            f"- **综合质量**: {report['quality']['overall']:.2%}",
            "",
            "## 改进建议"
        ])

        for rec in report.get("recommendations", []):
            priority_icon = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(rec["priority"], "")
            lines.append(f"\n{priority_icon} **{rec['message']}**")
            lines.append(f"   - 操作: {rec['action']}")

        return "\n".join(lines)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="记忆分析报告")
    parser.add_argument("--workspace", default=".", help="工作目录")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"],
                       help="输出格式")
    parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    analyzer = MemoryAnalyzer(args.workspace)
    report = analyzer.export_report(args.format)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"✓ 报告已生成: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
