#!/usr/bin/env python3
"""
认知性错误集成模块（Cognitive Error Integration）

功能：
- 将认知性错误检测结果集成到错误智慧库
- 自动生成错误智慧条目
- 与五维智力模型联动
- 支持认知性错误的时效性管理

使用方式：
    # 基础使用
    integrator = CognitiveErrorIntegrator(memory_dir="./agi_memory")
    integrator.integrate(detection_result, trace_id="trace_001")

    # 测试模式
    python3 scripts/cognitive_error_integration.py --test
"""
__version__ = "1.0.0"


import os
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime
from dataclasses import asdict

# 导入认知性错误检测器
import sys
sys.path.insert(0, os.path.dirname(__file__))
from cognitive_error_detector import (
    CognitiveErrorDetector,
    DetectionResult,
    ErrorType,
    Severity
)

# 导入错误智慧库管理器
from error_wisdom_manager import (
    ErrorWisdomManager,
    ErrorWisdomEntry,
    ErrorDiscovery,
    RootCauseAnalysis,
    Solution,
    PreventionKnowledge,
    PreventionRule,
    ErrorWisdomMetadata
)

# 导入时效性管理器
from error_wisdom_timeliness import TimelinessManager

# 导入规则生成管理器
from error_wisdom_rule_generator import RuleGenerationManager
from interfaces import TraceContext, TraceContext, create_trace_context

# 五维智力集成：升维建议持久化到 agi_memory/elevation_history
from elevation_advisor import save_elevation_suggestion

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CognitiveErrorIntegrator:
    """认知性错误集成器"""

    def __init__(
        self,
        memory_dir: str = "./agi_memory",
        error_wisdom_dir: Optional[str] = None
    ):
        """
        初始化集成器

        Args:
            memory_dir: 记忆存储目录
            error_wisdom_dir: 错误智慧库目录（默认使用memory_dir/error_wisdom）
        """
        # 将相对 memory_dir 解析到脚本所在目录（scripts/）下，避免依赖当前工作目录
        # 导致错误智慧库与升维建议写进不同的幽灵目录
        _scripts_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.isabs(memory_dir):
            self.memory_dir = memory_dir
        else:
            self.memory_dir = os.path.abspath(os.path.join(_scripts_dir, memory_dir))
        self.error_wisdom_dir = error_wisdom_dir or os.path.join(self.memory_dir, "error_wisdom")

        # 初始化错误智慧库管理器（统一使用已解析的 self.memory_dir，避免与升维建议写进不同目录）
        self.error_manager = ErrorWisdomManager(memory_dir=self.memory_dir)

        # 初始化时效性管理器（传入error_wisdom_dir，避免路径问题）
        self.timeliness_manager = TimelinessManager(memory_dir=self.error_wisdom_dir)

        # 初始化规则生成管理器
        self.rule_generator = RuleGenerationManager(memory_dir=self.error_wisdom_dir)

        # 五维智力集成：通过 elevation_advisor.save_elevation_suggestion 持久化升维建议

        logger.info(f"认知性错误集成器初始化完成，记忆目录：{memory_dir}")

    def integrate(
        self,
        detection_result: DetectionResult,
        trace_id: str,
        conversation_context: Optional[Dict] = None
    ) -> str:
        """
        集成认知性错误检测结果

        Args:
            detection_result: 认知性错误检测结果
            trace_id: 追踪ID
            conversation_context: 对话上下文

        Returns:
            str: 错误智慧条目ID
        """
        logger.info(f"开始集成认知性错误：{detection_result.error_type.value}")

        # 使用record_error方法直接记录
        entry_id = self.error_manager.record_error(
            error_type="认知性错误",
            error_subtype=detection_result.error_type.value,
            error_code=f"COG_{detection_result.error_type.value.upper()}",
            error_description=self._generate_error_description(detection_result),
            root_cause=detection_result.root_cause.primary_cause,
            solution=detection_result.prevention_suggestion.immediate_action,
            prevention_strategy=detection_result.prevention_suggestion.long_term_improvement,
            trace_id=trace_id,
            severity=self._map_severity(detection_result.severity),
            trigger_scenario=self._extract_trigger_scenario(detection_result.context),
            metadata={
                "confidence": detection_result.confidence,
                "detected_patterns": [asdict(p) for p in detection_result.detected_patterns],
                "root_cause_detail": asdict(detection_result.root_cause),
                "prevention_suggestion": asdict(detection_result.prevention_suggestion),
                "elevation_impact": asdict(detection_result.elevation_impact) if detection_result.elevation_impact else None,
                "timestamp": detection_result.timestamp
            }
        )

        logger.info(f"认知性错误已集成到错误智慧库，条目ID：{entry_id}")

        # 初始化时效性数据（Phase 3）
        self._initialize_timeliness(entry_id, detection_result.confidence)

        # 触发规则生成检查（Phase 3）
        self._check_and_generate_rules(detection_result.error_type)

        # 集成到五维智力模型
        self._integrate_to_dimension(detection_result, entry_id)

        return entry_id

    def _map_severity(self, severity: Severity) -> str:
        """映射严重程度"""
        mapping = {
            Severity.LOW: "mild",
            Severity.MEDIUM: "moderate",
            Severity.HIGH: "severe"
        }
        return mapping.get(severity, "mild")

    def _generate_error_description(self, detection_result: DetectionResult) -> str:
        """生成错误描述"""
        patterns_desc = "；".join([p.evidence for p in detection_result.detected_patterns])
        return f"检测到{detection_result.error_type.value}，置信度{detection_result.confidence:.2f}。检测模式：{patterns_desc}"

    def _extract_trigger_scenario(self, context: Dict) -> str:
        """提取触发场景"""
        user_query = context.get("user_query", "")
        return user_query[:100] if user_query else "未知场景"

    def _integrate_to_dimension(
        self,
        detection_result: DetectionResult,
        entry_id: str
    ):
        """将认知错误的升维影响集成到五维智力存储（agi_memory/elevation_history）。"""
        impact = detection_result.elevation_impact
        if not impact:
            return

        logger.info(f"记录升维影响：{impact.affected_dimensions}")
        logger.info(f"升维建议：{impact.suggestion}")
        try:
            suggestion = {
                "should_elevate": True,
                "reason": f"检测到认知性错误（{detection_result.error_type.value}），"
                          f"需强化相关维度以避免重复犯错",
                "suggested_action": "add_dimensions",
                "suggested_dimensions": list(impact.affected_dimensions),
                "expected_effect": impact.suggestion,
                "confidence": detection_result.confidence,
            }
            ok = save_elevation_suggestion(entry_id, suggestion, memory_dir=self.memory_dir)
            if ok:
                logger.info(f"升维建议已写入五维存储：条目={entry_id}，维度={impact.affected_dimensions}")
            else:
                logger.warning(f"升维建议写入失败：条目={entry_id}")
        except Exception as e:
            logger.warning(f"集成到五维智力存储失败：{e}")

    def _initialize_timeliness(
        self,
        entry_id: str,
        base_confidence: float
    ):
        """初始化时效性数据（Phase 3）"""
        try:
            # 初始化时效性数据
            self.timeliness_manager._initialize_entry(entry_id, base_confidence=base_confidence)
            logger.info(f"时效性数据已初始化，条目ID：{entry_id}")
        except Exception as e:
            logger.warning(f"初始化时效性数据失败：{e}")

    def _check_and_generate_rules(
        self,
        error_type: ErrorType
    ):
        """检查并生成预防规则（Phase 3）"""
        try:
            # 检查是否需要生成规则（相似错误≥3个）
            error_subtype = error_type.value
            self.error_manager._check_and_generate_rule(
                error_type="认知性错误",
                error_subtype=error_subtype
            )
            logger.info(f"规则生成检查已执行，错误类型：{error_subtype}")
        except Exception as e:
            logger.warning(f"规则生成检查失败：{e}")

    def query_prevention_knowledge(
        self,
        error_type: ErrorType,
        max_results: int = 5
    ) -> List[Dict]:
        """
        查询预防知识

        Args:
            error_type: 错误类型
            max_results: 最大结果数

        Returns:
            List[Dict]: 预防知识列表
        """
        error_type_mapping = {
            ErrorType.HALLUCINATION: "hallucination",
            ErrorType.REASONING_GAP: "reasoning_gap",
            ErrorType.KNOWLEDGE_GAP: "knowledge_gap",
            ErrorType.BIAS: "bias"
        }

        target_subtype = error_type_mapping.get(error_type)

        # 从所有错误中筛选认知性错误
        results = []
        for entry_id in self.error_manager.entries.get("entries", []):
            entry = self.error_manager.entries["entries"][entry_id]
            if (
                entry.get("错误发现", {}).get("错误类型") == "认知性错误"
                and target_subtype in entry.get("错误发现", {}).get("错误码", "")
            ):
                # 提取预防知识
                prevention = entry.get("预防知识", {})
                results.append({
                    "entry_id": entry_id,
                    "预防策略": prevention.get("预防策略", ""),
                    "解决方案": entry.get("解决方案", {}).get("即时纠错", ""),
                    "置信度": entry.get("元数据", {}).get("置信度", 0)
                })

        # 按置信度排序
        results.sort(key=lambda x: x["置信度"], reverse=True)

        return results[:max_results]

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        stats = self.error_manager.get_statistics()

        # 添加认知性错误特定统计
        cognitive_stats = {
            "total_cognitive_errors": 0,
            "by_type": {
                "hallucination": 0,
                "reasoning_gap": 0,
                "knowledge_gap": 0,
                "bias": 0
            },
            "by_severity": {
                "low": 0,
                "medium": 0,
                "high": 0
            }
        }

        # 统计认知性错误
        for entry_id in self.error_manager.entries.get("entries", {}):
            entry = self.error_manager.entries["entries"][entry_id]
            if entry.get("错误发现", {}).get("错误类型") == "认知性错误":
                cognitive_stats["total_cognitive_errors"] += 1

                # 按类型统计
                error_code = entry.get("错误发现", {}).get("错误码", "")
                if "HALLUCINATION" in error_code:
                    cognitive_stats["by_type"]["hallucination"] += 1
                elif "REASONING" in error_code:
                    cognitive_stats["by_type"]["reasoning_gap"] += 1
                elif "KNOWLEDGE" in error_code:
                    cognitive_stats["by_type"]["knowledge_gap"] += 1
                elif "BIAS" in error_code:
                    cognitive_stats["by_type"]["bias"] += 1

                # 按严重程度统计
                severity = entry.get("错误发现", {}).get("严重程度", "mild")
                if severity in cognitive_stats["by_severity"]:
                    cognitive_stats["by_severity"][severity] += 1

        stats["cognitive_errors"] = cognitive_stats

        return stats


def test_integration():
    """测试集成功能"""
    print("=== 测试认知性错误集成 ===\n")

    # 创建检测器
    detector = CognitiveErrorDetector(confidence_threshold=0.45)

    # 创建集成器
    integrator = CognitiveErrorIntegrator(memory_dir="./test_agi_memory")

    # 测试案例1：幻觉倾向
    print("测试案例1：幻觉倾向")
    result = detector.detect(
        user_query="2023年人工智能领域最重要的突破是什么？",
        agent_response="2023年3月15日，OpenAI发布了GPT-5，这是一个绝对革命性的模型。根据《人工智能前沿期刊》的报道，这个模型的参数量达到了100万亿。",
        conversation_context=None
    )

    if result:
        entry_id = integrator.integrate(result, trace_id="test_001")
        print(f"✓ 集成成功，条目ID：{entry_id}")
    else:
        print("✗ 未检测到错误")

    # 测试案例2：推理跳跃
    print("\n测试案例2：推理跳跃")
    result = detector.detect(
        user_query="为什么机器学习模型需要大量数据？",
        agent_response="机器学习模型需要大量数据是因为数据能够帮助模型学习规律，因此更多数据意味着更好的性能。显然，模型通过数据能够自动发现隐藏的模式。",
        conversation_context=None
    )

    if result:
        entry_id = integrator.integrate(result, trace_id="test_002")
        print(f"✓ 集成成功，条目ID：{entry_id}")
    else:
        print("✗ 未检测到错误")

    # 测试查询预防知识
    print("\n查询预防知识")
    prevention_knowledge = integrator.query_prevention_knowledge(ErrorType.HALLUCINATION)
    print(f"找到 {len(prevention_knowledge)} 条预防知识")
    for i, knowledge in enumerate(prevention_knowledge):
        print(f"  {i+1}. {knowledge.get('预防策略', 'N/A')}")

    # 测试统计信息
    print("\n统计信息")
    stats = integrator.get_statistics()
    cognitive_stats = stats.get("cognitive_errors", {})
    print(f"认知性错误总数：{cognitive_stats.get('total_cognitive_errors', 0)}")
    print(f"按类型分布：{cognitive_stats.get('by_type', {})}")
    print(f"按严重程度分布：{cognitive_stats.get('by_severity', {})}")


def main():
    """主函数"""
    print("认知性错误集成模块测试\n")

    test_integration()

    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    main()
