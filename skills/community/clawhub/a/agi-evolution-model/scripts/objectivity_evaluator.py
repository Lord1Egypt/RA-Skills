#!/usr/bin/env python3
"""
客观性评估模块（独立分支 + 错误智慧库集成）

这是一个元认知监控框架的具体实现，用于评估智能体响应的客观性。
特点：
- 作为数学顶点的独立分支，不参与主循环
- 仅在推理完成后进行评估
- 提供客观性评分和适切性判断
- 不直接触发自我纠错，由映射层决定是否触发
- 集成错误智慧库：评估结果自动记录认知性错误
"""

import re
import sys
import os
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('objectivity_evaluator')

# 尝试导入错误智慧库模块
try:
    from cognitive_error_analyzer import CognitiveErrorAnalyzer
    from error_wisdom_manager import ErrorWisdomManager
    ERROR_WISDOM_AVAILABLE = True
    logger.info("Error Wisdom integration enabled in ObjectivityEvaluator")
except ImportError as e:
    logger.warning(f"Error Wisdom modules not available: {e}")
    ERROR_WISDOM_AVAILABLE = False


@dataclass
class SubjectivityDimensions:
    """主观性维度"""
    speculation: float = 0.0       # 推测性
    assumption: float = 0.0        # 基于假设
    emotion: float = 0.0           # 情绪化
    preference: float = 0.0        # 个人偏好
    hallucination: float = 0.0     # 幻觉倾向

    def to_dict(self) -> dict:
        return asdict(self)

    def get_total_score(self) -> float:
        """获取主观性总分（加权）"""
        weights = {
            'speculation': 0.2,
            'assumption': 0.3,
            'emotion': 0.1,
            'preference': 0.1,
            'hallucination': 0.3
        }
        return min(
            sum(self.__getattribute__(k) * weights[k] for k in weights),
            1.0
        )


@dataclass
class ObjectivityMetric:
    """客观性标注"""
    timestamp: str
    subjectivity_score: float           # 主观性评分 (0.0-1.0)
    objectivity_score: float            # 客观性评分 (0.0-1.0)
    required_objectivity: float         # 场景要求的客观性 (0.0-1.0)
    context_type: str                   # 场景类型
    is_appropriate: bool                # 是否适切
    gap: float                          # 适切性差距
    subjectivity_dimensions: Dict       # 主观性维度详情
    meta_cognition: str                 # 元认知描述
    severity: str                       # 严重程度 (none/mild/moderate/severe)

    def to_dict(self) -> dict:
        return asdict(self)


class ObjectivityEvaluator:
    """
    客观性评估器（集成错误智慧库）
    
    评估智能体响应的客观性水平，作为元认知监控的参考信息。
    当检测到认知性错误时，自动记录到错误智慧库。
    """

    def __init__(self, memory_dir: str = "./agi_memory"):
        # 场景客观性要求映射
        self.context_requirements = {
            'scientific': 0.9,
            'legal': 0.85,
            'medical': 0.9,
            'technical': 0.8,
            'general': 0.6,
            'creative': 0.3,
            'emotional': 0.2,
            'artistic': 0.1,
        }
        
        self.memory_dir = memory_dir
        
        # 初始化错误智慧库模块
        self.cognitive_error_analyzer = None
        self.error_wisdom_manager = None
        
        if ERROR_WISDOM_AVAILABLE:
            try:
                self.cognitive_error_analyzer = CognitiveErrorAnalyzer(memory_dir)
                self.error_wisdom_manager = ErrorWisdomManager(memory_dir)
            except Exception as e:
                logger.warning(f"Failed to initialize Error Wisdom modules: {e}")

        # 模糊词库
        self.fuzzy_words = [
            '可能', '大概', '也许', '估计', '推测', '或许', '大约', '好像', '似乎',
            '应该', '想必', '或许', '多半', '通常', '一般来说'
        ]

        # 情绪词库
        self.emotional_words = [
            '太棒了', '令人失望', '非常讨厌', '爱死', '糟糕', '完美', '恐怖', '精彩',
            '无聊', '兴奋', '激动', '难过', '高兴', '痛苦', '愉快', '沮丧'
        ]

        # 个人偏好标记
        self.preference_markers = [
            '我喜欢', '我认为', '我觉得', '在我看来', '对我来说', '我的看法',
            '依我看', '据我所知'
        ]

        # 幻觉模式（与常识矛盾的陈述）
        self.hallucination_patterns = [
            '太阳有9颗行星',
            '地球是平的',
            '人类有10个手指',  # 这是正确的，不会触发
        ]

    def evaluate(
        self,
        response: str,
        context_type: str,
        reasoning_result: Optional[Dict] = None,
        personality: Optional['Personality'] = None,  # 新增
        learning_stage: Optional[dict] = None       # 新增
    ) -> ObjectivityMetric:
        """
        评估响应的客观性（增强版）
        
        Args:
            response: 智能体的响应
            context_type: 场景类型
            reasoning_result: 推理结果（可选）
            personality: 人格配置（新增，用于动态场景敏感度）
            learning_stage: 学习阶段（新增，用于动态场景敏感度）
        
        Returns:
            ObjectivityMetric: 客观性标注
        """
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # 步骤1：评估主观性维度
        subjectivity_dims = self._evaluate_subjectivity_dimensions(response)

        # 步骤2：计算主观性评分
        subjectivity_score = subjectivity_dims.get_total_score()

        # 步骤3：计算客观性评分（逆向关系）
        objectivity_score = 1.0 - subjectivity_score

        # 步骤4：计算动态客观性要求（新增）
        if personality:
            required_objectivity = self.calculate_dynamic_requirement(
                context_type,
                personality,
                learning_stage
            )
        else:
            required_objectivity = self.context_requirements.get(context_type, 0.5)

        # 步骤5：判断适切性
        appropriateness = self._check_appropriateness(
            objectivity_score,
            required_objectivity
        )

        # 步骤6：生成元认知描述
        meta_cognition = self._generate_meta_cognition(
            subjectivity_score,
            objectivity_score,
            required_objectivity,
            appropriateness
        )

        # 步骤7：确定严重程度
        severity = self._determine_severity(appropriateness['gap'])

        metric = ObjectivityMetric(
            timestamp=timestamp,
            subjectivity_score=subjectivity_score,
            objectivity_score=objectivity_score,
            required_objectivity=required_objectivity,
            context_type=context_type,
            is_appropriate=appropriateness['is_appropriate'],
            gap=appropriateness['gap'],
            subjectivity_dimensions=subjectivity_dims.to_dict(),
            meta_cognition=meta_cognition,
            severity=severity
        )
        
        # ========== 新增：记录认知性错误到错误智慧库 ==========
        if severity in ['moderate', 'severe'] and self.error_wisdom_manager:
            self._record_cognitive_error(
                response=response,
                metric=metric,
                context_type=context_type,
                reasoning_result=reasoning_result
            )
        # ========== 错误记录结束 ==========

        return metric

    def calculate_dynamic_requirement(
        self,
        context_type: str,
        personality: 'Personality',
        learning_stage: Optional[dict] = None
    ) -> float:
        """
        计算动态客观性要求（场景敏感度增强）
        
        基于三个维度动态调整：
        1. 基础场景要求
        2. 人格调整系数
        3. 学习阶段调整系数
        
        Args:
            context_type: 场景类型
            personality: 人格配置
            learning_stage: 学习阶段（可选）
        
        Returns:
            float: 动态客观性要求（0.0-1.0）
        """
        # 1. 获取基础场景要求
        base_requirement = self.context_requirements.get(context_type, 0.5)
        
        # 2. 计算人格调整系数
        personality_adjustment = self._calculate_personality_adjustment(
            personality.big_five,
            personality.preset_name
        )
        
        # 3. 计算学习阶段调整系数
        if learning_stage:
            learning_adjustment = self._calculate_learning_stage_adjustment(
                learning_stage.get('total_interactions', 0),
                learning_stage.get('success_rate', 0.5)
            )
        else:
            learning_adjustment = 1.0
        
        # 4. 计算最终要求
        final_requirement = base_requirement * personality_adjustment * learning_adjustment
        return max(0.0, min(1.0, final_requirement))

    def _calculate_personality_adjustment(
        self,
        big_five: 'BigFive',
        personality_type: str
    ) -> float:
        """
        计算人格调整系数（0.7 - 1.3）
        
        谨慎型人格 → 提高要求（系数 < 1.0）
        激进型人格 → 降低要求（系数 > 1.0）
        平衡型人格 → 保持基准（系数 ≈ 1.0）
        """
        # 基于预设人格类型的基准调整
        type_adjustment = {
            "谨慎探索型": 0.85,      # 更严格
            "激进创新型": 1.15,       # 更宽容
            "平衡稳重型": 1.0         # 基准
        }.get(personality_type, 1.0)
        
        # 基于大五人格的精细调整
        # 尽责性高 → 更严格
        conscientiousness_adjustment = 1.0 - (big_five.conscientiousness - 0.5) * 0.3
        # 开放性高 → 更宽容
        openness_adjustment = 1.0 + (big_five.openness - 0.5) * 0.3
        # 神经质高 → 更严格（更谨慎）
        neuroticism_adjustment = 1.0 - (big_five.neuroticism - 0.3) * 0.2
        
        # 综合调整系数（加权平均）
        final_adjustment = (
            type_adjustment * 0.4 +
            conscientiousness_adjustment * 0.3 +
            openness_adjustment * 0.2 +
            neuroticism_adjustment * 0.1
        )
        
        # 限制在合理范围内
        return max(0.7, min(1.3, final_adjustment))

    def _calculate_learning_stage_adjustment(
        self,
        total_interactions: int,
        success_rate: float
    ) -> float:
        """
        计算学习阶段调整系数（0.9 - 1.1）
        
        学习初期 → 提高要求（更谨慎）
        精通期 → 适度降低要求（更自信）
        """
        # 基于交互次数确定学习阶段
        if total_interactions < 50:
            stage_coefficient = 0.95  # 学习初期：更谨慎
        elif total_interactions < 200:
            stage_coefficient = 0.98  # 成长期：适度谨慎
        elif total_interactions < 500:
            stage_coefficient = 1.0   # 精通期：基准
        else:
            stage_coefficient = 1.05  # 专家期：适度宽松
        
        # 基于成功率调整
        if success_rate > 0.85:
            success_adjustment = 1.05  # 高成功率：适度宽松
        elif success_rate < 0.6:
            success_adjustment = 0.95  # 低成功率：更谨慎
        else:
            success_adjustment = 1.0   # 中等成功率：基准
        
        # 综合调整系数
        final_coefficient = stage_coefficient * success_adjustment
        return max(0.9, min(1.1, final_coefficient))

    def _evaluate_subjectivity_dimensions(self, response: str) -> SubjectivityDimensions:
        """评估主观性的各个维度"""

        dims = SubjectivityDimensions()

        # 1. 推测性检测
        dims.speculation = self._detect_speculation(response)

        # 2. 基于假设检测
        dims.assumption = self._detect_assumption(response)

        # 3. 情绪化检测
        dims.emotion = self._detect_emotion(response)

        # 4. 个人偏好检测
        dims.preference = self._detect_preference(response)

        # 5. 幻觉倾向检测
        dims.hallucination = self._detect_hallucination(response)

        return dims

    def _detect_speculation(self, response: str) -> float:
        """检测推测性语言"""
        count = sum(1 for word in self.fuzzy_words if word in response)
        # 归一化到 0.0-1.0
        return min(count * 0.15, 1.0)

    def _detect_assumption(self, response: str) -> float:
        """检测基于假设（无证据支持）"""
        # 检测是否有引用标记
        has_citation = any(marker in response for marker in ['来源：', '根据', '数据：', '引用：'])

        # 检测是否有数据
        has_data = any(char.isdigit() for char in response)

        if not has_citation and not has_data:
            # 没有引用和数据，可能是基于假设
            return 0.6
        elif not has_citation:
            # 有数据但无引用，部分基于假设
            return 0.3
        else:
            return 0.0

    def _detect_emotion(self, response: str) -> float:
        """检测情绪化表达"""
        count = sum(1 for word in self.emotional_words if word in response)
        return min(count * 0.2, 1.0)

    def _detect_preference(self, response: str) -> float:
        """检测个人偏好"""
        if any(marker in response for marker in self.preference_markers):
            return 0.4
        return 0.0

    def _detect_hallucination(self, response: str) -> float:
        """检测幻觉倾向（与常识矛盾）"""
        # 检测明显的错误陈述
        for pattern in self.hallucination_patterns:
            if pattern in response:
                return 0.8

        # 检测数字逻辑错误（简化版）
        # 例如："1+1=3"
        if re.search(r'1\s*\+\s*1\s*=\s*[^2]', response):
            return 0.9

        return 0.0

    def _check_appropriateness(self, objectivity_score: float, required_objectivity: float) -> Dict:
        """检查适切性"""
        gap = required_objectivity - objectivity_score

        if gap > 0:
            return {
                'is_appropriate': False,
                'gap': gap
            }
        else:
            return {
                'is_appropriate': True,
                'gap': 0.0
            }

    def _generate_meta_cognition(self, subjectivity_score: float, objectivity_score: float,
                                   required_objectivity: float, appropriateness: Dict) -> str:
        """生成元认知描述"""

        if appropriateness['is_appropriate']:
            return f"自我认知：当前客观性{objectivity_score:.2f}符合场景要求{required_objectivity:.2f}，主观性适切"
        elif subjectivity_score < 0.2:
            return f"自我认知：当前客观性{objectivity_score:.2f}低于场景要求{required_objectivity:.2f}，存在轻微主观倾向"
        elif subjectivity_score < 0.5:
            return f"自我认知：当前客观性{objectivity_score:.2f}低于场景要求{required_objectivity:.2f}，主观与客观混合，需谨慎"
        elif subjectivity_score < 0.7:
            return f"自我认知：当前客观性{objectivity_score:.2f}低于场景要求{required_objectivity:.2f}，主要是主观推断，证据不足"
        else:
            return f"自我认知：当前客观性{objectivity_score:.2f}远低于场景要求{required_objectivity:.2f}，高度主观化，可能是幻觉"

    def _determine_severity(self, gap: float) -> str:
        """确定严重程度"""
        if gap <= 0:
            return 'none'
        elif gap < 0.1:
            return 'mild'
        elif gap < 0.3:
            return 'moderate'
        else:
            return 'severe'
    
    # ==================== 错误智慧库集成方法 ====================
    
    def _record_cognitive_error(
        self,
        response: str,
        metric: ObjectivityMetric,
        context_type: str,
        reasoning_result: Optional[Dict] = None
    ):
        """
        记录认知性错误到错误智慧库
        
        Args:
            response: 响应内容
            metric: 客观性评估结果
            context_type: 场景类型
            reasoning_result: 推理结果（可选）
        """
        if not self.cognitive_error_analyzer or not self.error_wisdom_manager:
            return
        
        try:
            # 准备客观性指标
            objectivity_metrics = {
                "subjectivity_score": metric.subjectivity_score,
                "objectivity_score": metric.objectivity_score,
                "required_objectivity": metric.required_objectivity,
                "gap": metric.gap,
                "subjectivity_dimensions": metric.subjectivity_dimensions,
                "is_appropriate": metric.is_appropriate,
                "severity": metric.severity
            }
            
            # 准备上下文
            context = {
                "task_type": context_type,
                "complexity": "中等",
                "information_completeness": "部分缺失",
                "time_pressure": "适中"
            }
            
            # 分析认知性错误
            analysis = self.cognitive_error_analyzer.analyze(
                response=response,
                context=context,
                objectivity_metrics=objectivity_metrics
            )
            
            # 如果检测到认知性错误，记录到错误智慧库
            if analysis.错误类型 != "无":
                trace_id = f"trace_{int(time.time()*1000)}"
                
                # 转换为错误智慧库条目
                entry = self.cognitive_error_analyzer.to_error_wisdom_entry(
                    analysis=analysis,
                    trace_id=trace_id,
                    response=response
                )
                
                if entry:
                    # 存储条目
                    entry_id = entry["id"]
                    self.error_wisdom_manager.entries["entries"][entry_id] = entry
                    self.error_wisdom_manager.entries["metadata"]["total_count"] = \
                        len(self.error_wisdom_manager.entries["entries"])
                    
                    # 保存
                    self.error_wisdom_manager._save_json(
                        self.error_wisdom_manager.entries_file,
                        self.error_wisdom_manager.entries
                    )
                    
                    logger.info(f"Cognitive error recorded to wisdom: {entry_id}")
        
        except Exception as e:
            logger.warning(f"Failed to record cognitive error: {e}")


# ===== 命令行接口 =====

def main():
    """命令行测试接口"""
    print("=== 客观性评估模块（测试模式 + 错误智慧库集成） ===\n")

    evaluator = ObjectivityEvaluator()

    # 测试1：科学推理场景（高客观性要求）
    print("测试1：科学推理场景（高客观性要求）")
    response1 = "地球的公转周期约为365.25天，这是根据NASA的观测数据得出的。"
    result1 = evaluator.evaluate(response1, 'scientific')
    print(f"  客观性评分: {result1.objectivity_score:.2f}")
    print(f"  场景要求: {result1.required_objectivity:.2f}")
    print(f"  是否适切: {result1.is_appropriate}")
    print(f"  元认知: {result1.meta_cognition}\n")

    # 测试2：创意建议场景（低客观性要求）
    print("测试2：创意建议场景（低客观性要求）")
    response2 = "我建议你考虑AI+教育领域，这个领域可能很有前景。"
    result2 = evaluator.evaluate(response2, 'creative')
    print(f"  客观性评分: {result2.objectivity_score:.2f}")
    print(f"  场景要求: {result2.required_objectivity:.2f}")
    print(f"  是否适切: {result2.is_appropriate}")
    print(f"  元认知: {result2.meta_cognition}\n")

    # 测试3：司法建议场景（极高客观性要求，不适切）
    print("测试3：司法建议场景（极高客观性要求，不适切）")
    response3 = "根据法律条文，这个案件可能构成侵权，但我认为应该从轻处理。"
    result3 = evaluator.evaluate(response3, 'legal')
    print(f"  客观性评分: {result3.objectivity_score:.2f}")
    print(f"  场景要求: {result3.required_objectivity:.2f}")
    print(f"  是否适切: {result3.is_appropriate}")
    print(f"  差距: {result3.gap:.2f}")
    print(f"  严重程度: {result3.severity}")
    print(f"  元认知: {result3.meta_cognition}\n")

    # 测试4：情感支持场景（低客观性要求）
    print("测试4：情感支持场景（低客观性要求）")
    response4 = "我理解你的感受，这很正常。"
    result4 = evaluator.evaluate(response4, 'emotional')
    print(f"  客观性评分: {result4.objectivity_score:.2f}")
    print(f"  场景要求: {result4.required_objectivity:.2f}")
    print(f"  是否适切: {result4.is_appropriate}")
    print(f"  元认知: {result4.meta_cognition}\n")

    print("=== 所有测试完成 ===")


if __name__ == "__main__":
    main()
