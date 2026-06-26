#!/usr/bin/env python3
"""
记忆存储纯Python实现

不依赖任何编译的.so文件，使用纯Python实现所有记忆存储功能。
包括：记录存储、检索、分析、反馈、模式识别、narrative.md双轨存储等。
"""

import json
import os
import time
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime


# ===== narrative.md 相关常量 =====

NARRATIVE_TEMPLATE = """# AGI自我叙事记录

本文件存储智能体的自我认知与进化轨迹，形成"我是谁"的连贯叙事。

---

## 记录态统计

## 核心洞察

## 关键突破

## 认知边界

## 进化方向

---
最后更新时间: *初始化*
"""

NARRATIVE_SECTIONS = [
    "记录态统计",
    "核心洞察",
    "关键突破",
    "认知边界",
    "进化方向"
]


@dataclass
class Record:
    """交互记录"""
    timestamp: str
    user_query: str
    intent_type: str
    reasoning_quality: float = 8.0
    solution_effectiveness: float = 8.0
    innovation_score: float = 7.0
    new_insights: List[str] = None
    feedback: Dict[str, str] = None
    overall_rating: str = "good"
    response: str = ""  # 新增：生成的响应
    objectivity_metric: Dict = None  # 新增：客观性标注
    self_correction: Dict = None  # 新增：自我纠错记录

    def __post_init__(self):
        if self.new_insights is None:
            self.new_insights = []
        if self.feedback is None:
            self.feedback = {
                "drive": "",
                "math": "",
                "iteration": ""
            }
        if self.objectivity_metric is None:
            self.objectivity_metric = {}
        if self.self_correction is None:
            self.self_correction = {}

    def to_dict(self) -> dict:
        return asdict(self)

    def get_value_weight(self) -> float:
        """计算价值权重"""
        return (
            self.reasoning_quality * 0.4 +
            self.solution_effectiveness * 0.3 +
            self.innovation_score * 0.3
        ) / 10.0


@dataclass
class AnalysisResult:
    """分析结果"""
    total_records: int
    rating_distribution: Dict[str, int]
    intent_type_distribution: Dict[str, int]
    average_scores: Dict[str, float]
    recent_insights: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


class MemoryStore:
    """记忆存储管理器（纯Python实现）"""

    def __init__(self, memory_dir: str = "./agi_memory"):
        """
        初始化记忆存储

        Args:
            memory_dir: 记忆存储目录
        """
        self.memory_dir = memory_dir
        self.records_file = os.path.join(memory_dir, "records.json")
        self.narrative_file = os.path.join(memory_dir, "narrative.md")
        self._records: List[Record] = []
        self._load_records()

    def _load_records(self):
        """加载记录"""
        if not os.path.exists(self.records_file):
            self._records = []
            return

        with open(self.records_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self._records = [Record(**item) for item in data]

    def _save_records(self):
        """保存记录"""
        os.makedirs(self.memory_dir, exist_ok=True)

        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self._records], f, ensure_ascii=False, indent=2)

    # ===== narrative.md 核心方法 =====

    def _init_narrative(self) -> str:
        """
        初始化 narrative.md 模板

        Returns:
            str: 初始化后的模板内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%SZ")
        template = NARRATIVE_TEMPLATE.replace("*初始化*", timestamp)
        return template

    def _load_narrative(self) -> str:
        """
        加载 narrative.md 内容

        Returns:
            str: narrative.md 的完整内容
        """
        if not os.path.exists(self.narrative_file):
            # 文件不存在，初始化
            template = self._init_narrative()
            self._save_narrative(template)
            return template

        with open(self.narrative_file, 'r', encoding='utf-8') as f:
            return f.read()

    def _save_narrative(self, content: str):
        """
        保存 narrative.md 内容

        Args:
            content: 要保存的完整内容
        """
        os.makedirs(self.memory_dir, exist_ok=True)

        with open(self.narrative_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def append_narrative_section(self, section: str, content: str, timestamp: str = None):
        """
        在指定节末尾追加内容

        Args:
            section: 节名称（必须是 NARRATIVE_SECTIONS 之一）
            content: 要追加的内容
            timestamp: 时间戳（可选，默认当前时间）

        Raises:
            ValueError: 如果 section 不是有效的节名称
        """
        if section not in NARRATIVE_SECTIONS:
            raise ValueError(f"无效的节名称: {section}，有效值为: {NARRATIVE_SECTIONS}")

        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%SZ")

        current = self._load_narrative()
        section_header = f"## {section}"

        # 查找该节的位置
        idx = current.find(section_header)
        if idx == -1:
            # 节不存在，添加新节
            new_section = f"\n## {section}\n- [{timestamp}] {content}\n"
            updated = current + new_section
        else:
            # 查找下一节的位置
            next_section_idx = current.find("\n## ", idx + len(section_header))
            if next_section_idx == -1:
                next_section_idx = len(current)

            # 在该节末尾追加
            new_entry = f"\n- [{timestamp}] {content}"
            updated = current[:next_section_idx] + new_entry + current[next_section_idx:]

        # 更新最后更新时间
        updated = updated.replace(
            "最后更新时间: *",
            f"最后更新时间: {timestamp}"
        )

        self._save_narrative(updated)

    def get_narrative_insights(self, section: str = "核心洞察", limit: int = 10) -> List[str]:
        """
        获取指定节中的洞察

        Args:
            section: 节名称
            limit: 返回的最大条数

        Returns:
            List[str]: 洞察列表
        """
        content = self._load_narrative()
        section_header = f"## {section}"

        idx = content.find(section_header)
        if idx == -1:
            return []

        # 提取该节内容
        next_section_idx = content.find("\n## ", idx + len(section_header))
        if next_section_idx == -1:
            next_section_idx = len(content)

        section_content = content[idx + len(section_header):next_section_idx]

        # 解析洞察条目
        insights = []
        for line in section_content.split('\n'):
            if line.strip().startswith('- ['):
                # 提取内容部分
                match = line[line.find(']')+1:].strip()
                if match:
                    insights.append(match)

        return insights[-limit:]  # 返回最新的 limit 条

    def get_narrative_summary(self) -> Dict[str, Any]:
        """
        获取 narrative.md 统计摘要

        Returns:
            Dict[str, Any]: 包含各节统计信息的字典
        """
        summary = {}
        content = self._load_narrative()

        for section in NARRATIVE_SECTIONS:
            section_header = f"## {section}"
            idx = content.find(section_header)
            if idx == -1:
                summary[section] = {"count": 0, "latest": None}
                continue

            # 提取该节内容
            next_section_idx = content.find("\n## ", idx + len(section_header))
            if next_section_idx == -1:
                next_section_idx = len(content)

            section_content = content[idx + len(section_header):next_section_idx]

            # 统计条目数
            count = section_content.count('\n- [')

            # 提取最新条目
            latest = None
            for line in section_content.split('\n'):
                if line.strip().startswith('- ['):
                    match = line[line.find(']')+1:].strip()
                    if match:
                        latest = match

            summary[section] = {
                "count": count,
                "latest": latest
            }

        return summary

    # ===== 公共接口 =====

    def get_narrative_content(self) -> str:
        """
        获取 narrative.md 的完整内容

        Returns:
            str: narrative.md 的完整内容
        """
        return self._load_narrative()

    def get_narrative_summary_dict(self) -> Dict[str, Any]:
        """
        获取 narrative.md 统计摘要（公共接口）

        Returns:
            Dict[str, Any]: 包含各节统计信息的字典
        """
        return self.get_narrative_summary()

    def clear_narrative_section(self, section: str):
        """
        清空指定节的内容

        Args:
            section: 节名称

        Raises:
            ValueError: 如果 section 不是有效的节名称
        """
        if section not in NARRATIVE_SECTIONS:
            raise ValueError(f"无效的节名称: {section}，有效值为: {NARRATIVE_SECTIONS}")

        current = self._load_narrative()
        section_header = f"## {section}"

        idx = current.find(section_header)
        if idx == -1:
            return  # 节不存在，无需清空

        # 查找下一节的位置
        next_section_idx = current.find("\n## ", idx + len(section_header))
        if next_section_idx == -1:
            # 没有下一节，直接删除到文件末尾
            updated = current[:idx]
        else:
            # 删除该节内容，保留节标题
            updated = current[:idx + len(section_header)] + "\n" + current[next_section_idx:]

        self._save_narrative(updated)

    # ===== 核心存储方法（扩展版） =====

    def store(self, data: dict) -> bool:
        """
        存储记录（扩展版，支持 narrative.md）

        Args:
            data: 记录数据，支持以下字段：
                - timestamp: 时间戳
                - user_query: 用户查询
                - intent_type: 意图类型
                - reasoning_quality: 推理质量
                - solution_effectiveness: 解决方案有效性
                - innovation_score: 创新分数
                - new_insights: 新洞察列表（将写入 narrative.md）
                - evolution_direction: 进化方向（将写入 narrative.md）
                - cognitive_boundary: 认知边界（将写入 narrative.md）
                - key_breakthrough: 关键突破（将写入 narrative.md）
                - record_statistics: 记录态统计（将写入 narrative.md）
                - feedback: 反馈字典
                - overall_rating: 整体评分
                - response: 生成的响应
                - objectivity_metric: 客观性标注
                - self_correction: 自我纠错记录

        Returns:
            bool: 是否成功
        """
        try:
            record = Record(
                timestamp=data.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
                user_query=data.get("user_query", ""),
                intent_type=data.get("intent_type", ""),
                reasoning_quality=data.get("reasoning_quality", 8.0),
                solution_effectiveness=data.get("solution_effectiveness", 8.0),
                innovation_score=data.get("innovation_score", 7.0),
                new_insights=data.get("new_insights", []),
                feedback=data.get("feedback", {}),
                overall_rating=data.get("overall_rating", "good"),
                response=data.get("response", ""),
                objectivity_metric=data.get("objectivity_metric", {}),
                self_correction=data.get("self_correction", {})
            )

            self._records.append(record)
            self._save_records()

            # 新增：写入 narrative.md
            try:
                # 存储核心洞察
                if data.get("new_insights"):
                    for insight in data["new_insights"]:
                        self.append_narrative_section("核心洞察", insight)

                # 存储进化方向
                if data.get("evolution_direction"):
                    self.append_narrative_section("进化方向", data["evolution_direction"])

                # 存储认知边界
                if data.get("cognitive_boundary"):
                    self.append_narrative_section("认知边界", data["cognitive_boundary"])

                # 存储关键突破
                if data.get("key_breakthrough"):
                    self.append_narrative_section("关键突破", data["key_breakthrough"])

                # 存储记录态统计
                if data.get("record_statistics"):
                    self.append_narrative_section("记录态统计", data["record_statistics"])

            except Exception as e:
                # narrative.md 写入失败不影响主流程
                print(f"[WARNING] 写入 narrative.md 失败: {e}")

            return True
        except Exception as e:
            print(f"存储记录失败: {e}")
            return False

    def retrieve(self, query_type: str, limit: int = 5) -> List[Dict]:
        """
        检索记录

        Args:
            query_type: 查询类型
            limit: 返回数量限制

        Returns:
            List[Dict]: 匹配的记录
        """
        # 简单的匹配逻辑
        matched = []

        for record in reversed(self._records):
            if query_type.lower() in record.intent_type.lower():
                matched.append(record.to_dict())
                if len(matched) >= limit:
                    break

        return matched

    def analyze(self) -> AnalysisResult:
        """
        分析记录（扩展版，包含 narrative.md 统计）

        Returns:
            AnalysisResult: 分析结果
        """
        if not self._records:
            return AnalysisResult(
                total_records=0,
                rating_distribution={},
                intent_type_distribution={},
                average_scores={},
                recent_insights=[]
            )

        total = len(self._records)

        # 评分分布
        rating_dist = {}
        for record in self._records:
            rating = record.overall_rating
            rating_dist[rating] = rating_dist.get(rating, 0) + 1

        # 意图类型分布
        intent_dist = {}
        for record in self._records:
            intent = record.intent_type
            intent_dist[intent] = intent_dist.get(intent, 0) + 1

        # 平均分
        avg_reasoning = sum(r.reasoning_quality for r in self._records) / total
        avg_effectiveness = sum(r.solution_effectiveness for r in self._records) / total
        avg_innovation = sum(r.innovation_score for r in self._records) / total

        # 收集最近的洞察
        recent_insights = []
        for record in reversed(self._records[-10:]):
            recent_insights.extend(record.new_insights)

        # 新增：从 narrative.md 获取洞察
        try:
            narrative_insights = self.get_narrative_insights("核心洞察", limit=10)
            recent_insights.extend(narrative_insights)
            recent_insights = recent_insights[-20:]  # 保留最新的20条
        except Exception as e:
            print(f"[WARNING] 读取 narrative.md 洞察失败: {e}")

        return AnalysisResult(
            total_records=total,
            rating_distribution=rating_dist,
            intent_type_distribution=intent_dist,
            average_scores={
                "reasoning_quality": round(avg_reasoning, 2),
                "solution_effectiveness": round(avg_effectiveness, 2),
                "innovation_score": round(avg_innovation, 2)
            },
            recent_insights=recent_insights
        )

    def feedback(self, vertex: str) -> Dict[str, str]:
        """
        生成反馈建议

        Args:
            vertex: 顶点名称（drive/math/iteration）

        Returns:
            Dict: 反馈建议
        """
        analysis = self.analyze()

        # 根据分析结果生成反馈
        feedback_map = {
            "drive": {
                "suggestion": "需求识别准确",
                "optimization": "继续优化优先级排序"
            },
            "math": {
                "suggestion": "推理方法有效",
                "optimization": "可增强逻辑一致性检查"
            },
            "iteration": {
                "suggestion": "进化路径平稳",
                "optimization": "尝试更多创新策略"
            }
        }

        if analysis.total_records == 0:
            return {
                "vertex": vertex,
                "suggestion": "暂无数据",
                "optimization": "需要更多交互记录"
            }

        base_feedback = feedback_map.get(vertex, {})

        # 根据评分调整
        avg_effectiveness = analysis.average_scores.get("solution_effectiveness", 8.0)

        if avg_effectiveness > 8.5:
            base_feedback["optimization"] = "当前策略优秀，继续保持"

        return base_feedback

    def patterns(self) -> List[Dict]:
        """
        识别模式

        Returns:
            List[Dict]: 识别到的模式
        """
        if len(self._records) < 5:
            return []

        patterns = []

        # 识别高频意图类型
        analysis = self.analyze()
        intent_dist = analysis.intent_type_distribution

        if intent_dist:
            most_common = max(intent_dist, key=intent_dist.get)
            if intent_dist[most_common] >= 3:
                patterns.append({
                    "type": "frequent_intent",
                    "pattern": most_common,
                    "frequency": intent_dist[most_common]
                })

        # 识别高分模式
        high_quality = [r for r in self._records if r.get_value_weight() > 0.8]
        if len(high_quality) >= 3:
            patterns.append({
                "type": "high_quality_pattern",
                "count": len(high_quality),
                "avg_score": sum(r.get_value_weight() for r in high_quality) / len(high_quality)
            })

        return patterns

    def compress(self, threshold: float = 0.5):
        """
        压缩低价值记录

        Args:
            threshold: 价值权重阈值
        """
        if len(self._records) < 10:
            return

        # 分离高低价值记录
        high_value = [r for r in self._records if r.get_value_weight() >= threshold]
        low_value = [r for r in self._records if r.get_value_weight() < threshold]

        # 保留所有高价值记录
        # 低价值记录保留摘要
        if low_value:
            summary_record = Record(
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                user_query=f"[摘要] {len(low_value)}条低价值记录",
                intent_type="summary",
                reasoning_quality=sum(r.reasoning_quality for r in low_value) / len(low_value),
                solution_effectiveness=sum(r.solution_effectiveness for r in low_value) / len(low_value),
                innovation_score=sum(r.innovation_score for r in low_value) / len(low_value),
                new_insights=[],
                feedback={},
                overall_rating="neutral"
            )
            high_value.append(summary_record)

        self._records = high_value
        self._save_records()

    def get_stats(self) -> Dict:
        """
        获取统计信息

        Returns:
            Dict: 统计信息
        """
        analysis = self.analyze()

        return {
            "total_records": analysis.total_records,
            "rating_distribution": analysis.rating_distribution,
            "intent_type_distribution": analysis.intent_type_distribution,
            "average_scores": analysis.average_scores,
            "recent_insights_count": len(analysis.recent_insights),
            "patterns_count": len(self.patterns()),
            "narrative_summary": self.get_narrative_summary_dict()
        }


# ===== 命令行接口 =====

def main():
    """命令行测试接口"""
    print("=== 记忆存储纯Python实现（测试模式） ===\n")

    memory = MemoryStore()

    # 测试存储
    print("测试1：存储记录")
    memory.store({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "user_query": "架构升级需要谨慎",
        "intent_type": "架构决策",
        "reasoning_quality": 9.0,
        "solution_effectiveness": 9.0,
        "innovation_score": 7.0,
        "new_insights": ["架构升级是相变事件", "谨慎是美德"],
        "evolution_direction": "渐进演化优于激进突变",
        "feedback": {
            "drive": "强化需求验证",
            "math": "优化推理规则",
            "iteration": "渐进演化优于激进突变"
        },
        "overall_rating": "good"
    })
    print("✓ 记录已存储\n")

    # 测试检索
    print("测试2：检索记录")
    results = memory.retrieve("架构决策", limit=5)
    print(f"✓ 找到 {len(results)} 条记录\n")

    # 测试分析
    print("测试3：分析记录")
    analysis = memory.analyze()
    print(f"✓ 总记录数: {analysis.total_records}")

    # 测试narrative
    print("\n测试4：narrative.md功能")
    print("✓ narrative内容:")
    print(memory.get_narrative_content())

    print("\n✓ narrative摘要:")
    summary = memory.get_narrative_summary_dict()
    for section, data in summary.items():
        print(f"  {section}: {data['count']}条")
        if data['latest']:
            print(f"    最新: {data['latest'][:50]}...")


if __name__ == "__main__":
    main()
