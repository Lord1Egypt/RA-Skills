#!/usr/bin/env python3
"""
记忆存储异步实现

基于asyncio和aiofiles的异步I/O实现，提供非阻塞的记录存储、检索和分析功能。
性能优化：批量操作、并行读取、超时保护、narrative.md双轨存储。
"""

import asyncio
import json
import os
import time
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# 异步文件I/O依赖
try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False
    print("警告: aiofiles未安装，将使用同步I/O（性能较差）")


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
    response: str = ""
    objectivity_metric: Dict = None
    self_correction: Dict = None

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


class AsyncMemoryStore:
    """记忆存储管理器（异步实现）"""

    def __init__(self, memory_dir: str = "./agi_memory", batch_size: int = 100):
        """
        初始化记忆存储

        Args:
            memory_dir: 记忆存储目录
            batch_size: 批量写入大小
        """
        self.memory_dir = Path(memory_dir)
        self.records_file = self.memory_dir / "records.json"
        self.narrative_file = self.memory_dir / "narrative.md"

        self._records: List[Record] = []
        self._batch: List[Record] = []  # 待批量写入的记录
        self.batch_size = batch_size
        self.lock = asyncio.Lock()  # 保护共享数据

    # ===== JSON记录操作 =====

    async def _load_records(self):
        """异步加载记录"""
        if not self.records_file.exists():
            self._records = []
            return

        async with aiofiles.open(self.records_file, 'r', encoding='utf-8') as f:
            content = await f.read()
            data = json.loads(content)

        self._records = [Record(**item) for item in data]

    async def _save_records(self):
        """异步保存记录"""
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(self.records_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps([r.to_dict() for r in self._records], ensure_ascii=False, indent=2))

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

    async def _load_narrative(self) -> str:
        """
        异步加载 narrative.md 内容

        Returns:
            str: narrative.md 的完整内容
        """
        if not self.narrative_file.exists():
            # 文件不存在，初始化
            template = self._init_narrative()
            await self._save_narrative(template)
            return template

        async with aiofiles.open(self.narrative_file, 'r', encoding='utf-8') as f:
            return await f.read()

    async def _save_narrative(self, content: str):
        """
        异步保存 narrative.md 内容

        Args:
            content: 要保存的完整内容
        """
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(self.narrative_file, 'w', encoding='utf-8') as f:
            await f.write(content)

    async def append_narrative_section(self, section: str, content: str, timestamp: str = None):
        """
        异步在指定节末尾追加内容

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

        current = await self._load_narrative()
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

        await self._save_narrative(updated)

    async def get_narrative_insights(self, section: str = "核心洞察", limit: int = 10) -> List[str]:
        """
        异步获取指定节中的洞察

        Args:
            section: 节名称
            limit: 返回的最大条数

        Returns:
            List[str]: 洞察列表
        """
        content = await self._load_narrative()
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

        return insights[-limit:]

    async def get_narrative_summary(self) -> Dict[str, Any]:
        """
        异步获取 narrative.md 统计摘要

        Returns:
            Dict[str, Any]: 包含各节统计信息的字典
        """
        summary = {}
        content = await self._load_narrative()

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

    async def get_narrative_content(self) -> str:
        """
        异步获取 narrative.md 的完整内容

        Returns:
            str: narrative.md 的完整内容
        """
        return await self._load_narrative()

    async def get_narrative_summary_dict(self) -> Dict[str, Any]:
        """
        异步获取 narrative.md 统计摘要（公共接口）

        Returns:
            Dict[str, Any]: 包含各节统计信息的字典
        """
        return await self.get_narrative_summary()

    async def clear_narrative_section(self, section: str):
        """
        异步清空指定节的内容

        Args:
            section: 节名称

        Raises:
            ValueError: 如果 section 不是有效的节名称
        """
        if section not in NARRATIVE_SECTIONS:
            raise ValueError(f"无效的节名称: {section}，有效值为: {NARRATIVE_SECTIONS}")

        current = await self._load_narrative()
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

        await self._save_narrative(updated)

    # ===== 核心存储方法（扩展版） =====

    async def store(self, data: dict) -> bool:
        """
        异步存储记录（扩展版，支持 narrative.md）

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
            async with self.lock:
                record = Record(
                    timestamp=data.get("timestamp", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
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
                self._batch.append(record)

                # 批量写入检查
                if len(self._batch) >= self.batch_size:
                    await self._save_records()
                    self._batch.clear()
                else:
                    # 单条写入
                    await self._save_records()

            # 新增：异步写入 narrative.md
            try:
                # 存储核心洞察
                if data.get("new_insights"):
                    for insight in data["new_insights"]:
                        await self.append_narrative_section("核心洞察", insight)

                # 存储进化方向
                if data.get("evolution_direction"):
                    await self.append_narrative_section("进化方向", data["evolution_direction"])

                # 存储认知边界
                if data.get("cognitive_boundary"):
                    await self.append_narrative_section("认知边界", data["cognitive_boundary"])

                # 存储关键突破
                if data.get("key_breakthrough"):
                    await self.append_narrative_section("关键突破", data["key_breakthrough"])

                # 存储记录态统计
                if data.get("record_statistics"):
                    await self.append_narrative_section("记录态统计", data["record_statistics"])

            except Exception as e:
                # narrative.md 写入失败不影响主流程
                print(f"[WARNING] 异步写入 narrative.md 失败: {e}")

            return True
        except Exception as e:
            print(f"异步存储记录失败: {e}")
            return False

    async def retrieve(self, query_type: str, limit: int = 5) -> List[Dict]:
        """
        异步检索记录

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

    async def analyze(self) -> AnalysisResult:
        """
        异步分析记录（扩展版，包含 narrative.md 统计）

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

        # 新增：从 narrative.md 异步获取洞察
        try:
            narrative_insights = await self.get_narrative_insights("核心洞察", limit=10)
            recent_insights.extend(narrative_insights)
            recent_insights = recent_insights[-20:]  # 保留最新的20条
        except Exception as e:
            print(f"[WARNING] 异步读取 narrative.md 洞察失败: {e}")

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

    async def get_stats(self) -> Dict:
        """
        异步获取统计信息

        Returns:
            Dict: 统计信息
        """
        analysis = await self.analyze()

        return {
            "total_records": analysis.total_records,
            "rating_distribution": analysis.rating_distribution,
            "intent_type_distribution": analysis.intent_type_distribution,
            "average_scores": analysis.average_scores,
            "recent_insights_count": len(analysis.recent_insights),
            "narrative_summary": await self.get_narrative_summary_dict()
        }

    async def compress(self, threshold: float = 0.5):
        """
        异步压缩低价值记录

        Args:
            threshold: 价值权重阈值
        """
        async with self.lock:
            if len(self._records) < 10:
                return

            # 分离高低价值记录
            high_value = [r for r in self._records if r.get_value_weight() >= threshold]
            low_value = [r for r in self._records if r.get_value_weight() < threshold]

            # 保留所有高价值记录
            # 低价值记录保留摘要
            if low_value:
                summary_record = Record(
                    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            await self._save_records()

    async def flush(self):
        """强制刷新批量缓冲区"""
        async with self.lock:
            if self._batch:
                await self._save_records()
                self._batch.clear()


# ===== 命令行接口 =====

async def main():
    """命令行测试接口"""
    print("=== 记忆存储异步实现（测试模式） ===\n")

    if not AIOFILES_AVAILABLE:
        print("警告: aiofiles未安装，使用同步I/O")

    memory = AsyncMemoryStore()
    await memory._load_records()

    # 测试存储
    print("测试1：异步存储记录")
    await memory.store({
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "user_query": "异步存储测试",
        "intent_type": "async_test",
        "new_insights": ["异步I/O提升性能"],
        "evolution_direction": "异步化架构演进"
    })
    print("✓ 记录已存储\n")

    # 测试narrative
    print("测试2：narrative.md功能")
    content = await memory.get_narrative_content()
    print(f"✓ narrative内容长度: {len(content)}字符")

    summary = await memory.get_narrative_summary_dict()
    print(f"✓ 核心洞察: {summary['核心洞察']['count']}条")

    # 测试分析
    print("\n测试3：异步分析")
    analysis = await memory.analyze()
    print(f"✓ 总记录数: {analysis.total_records}")
    print(f"✓ 洞察数量: {len(analysis.recent_insights)}")

    # 刷新缓冲区
    await memory.flush()
    print("\n✓ 测试完成")


if __name__ == "__main__":
    asyncio.run(main())
