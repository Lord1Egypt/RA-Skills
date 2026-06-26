"""
Self Assessor - 元认知监控

自我评估、反思改进、置信度评估。
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class SelfAssessor:
    """自我评估器 - 元认知监控"""
    
    def __init__(self):
        self.assessment_history = []
    
    async def evaluate(self, response: Dict, context: Dict = None) -> Dict:
        """
        评估响应质量
        
        Args:
            response: 待评估的响应
            context: 上下文信息
        
        Returns:
            评估结果
        """
        print("[Meta] 开始自我评估")
        
        # 1. 评估置信度
        confidence = self._assess_confidence(response)
        
        # 2. 评估完整性
        completeness = self._assess_completeness(response)
        
        # 3. 评估准确性
        accuracy = self._assess_accuracy(response, context)
        
        # 4. 评估一致性
        consistency = self._assess_consistency(response)
        
        # 5. 综合评估
        overall_score = (confidence + completeness + accuracy + consistency) / 4
        
        # 6. 判断是否需要改进
        needs_improvement = overall_score < 0.7
        
        result = {
            "mode": "Meta-Cognition",
            "confidence": confidence,
            "completeness": completeness,
            "accuracy": accuracy,
            "consistency": consistency,
            "overall_score": overall_score,
            "needs_improvement": needs_improvement,
            "timestamp": datetime.now().isoformat()
        }
        
        if needs_improvement:
            result["improvement_suggestions"] = self._suggest_improvements(response, result)
        
        print(f"[Meta] 完成，综合评分：{overall_score:.2f}")
        
        return result
    
    async def reflect(self, response: Dict, assessment: Dict) -> Dict:
        """
        反思改进
        
        Args:
            response: 原始响应
            assessment: 评估结果
        
        Returns:
            反思结果和改进建议
        """
        print("[Meta] 开始反思")
        
        reflection = {
            "strengths": self._identify_strengths(response, assessment),
            "weaknesses": self._identify_weaknesses(response, assessment),
            "lessons_learned": self._extract_lessons(response, assessment),
            "action_items": self._generate_action_items(assessment)
        }
        
        # 记录反思历史
        self.assessment_history.append({
            "assessment": assessment,
            "reflection": reflection,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"[Meta] 反思完成，发现{len(reflection['weaknesses'])}个弱点")
        
        return reflection
    
    def _assess_confidence(self, response: Dict) -> float:
        """评估置信度"""
        score = 0.5  # 基础分
        
        # 检查是否有明确的推理过程
        if "reasoning_chain" in response:
            chain = response["reasoning_chain"]
            if len(chain) >= 3:
                score += 0.2
            if len(chain) >= 5:
                score += 0.1
        
        # 检查是否有证据支持
        if "evidence" in response or "sources" in response:
            score += 0.2
        
        # 检查是否有置信度自评
        if "confidence" in response:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _assess_completeness(self, response: Dict) -> float:
        """评估完整性"""
        score = 0.5  # 基础分
        
        # 检查是否回答了所有问题
        if "questions_answered" in response:
            answered = response.get("questions_answered", 0)
            total = response.get("total_questions", 1)
            score += 0.3 * (answered / total)
        
        # 检查是否有遗漏
        if "missing_information" not in response or not response["missing_information"]:
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _assess_accuracy(self, response: Dict, context: Dict = None) -> float:
        """评估准确性"""
        score = 0.5  # 基础分
        
        # 如果有上下文，检查一致性
        if context:
            if self._is_consistent_with_context(response, context):
                score += 0.3
        
        # 检查是否有事实错误标记
        if "factual_errors" not in response:
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _assess_consistency(self, response: Dict) -> float:
        """评估一致性"""
        score = 0.5  # 基础分
        
        # 检查内部一致性
        if "contradictions" not in response:
            score += 0.3
        
        # 检查逻辑连贯性
        if "reasoning_chain" in response:
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _is_consistent_with_context(self, response: Dict, context: Dict) -> bool:
        """检查响应与上下文的一致性"""
        # 简单实现：检查关键信息是否冲突
        # 实际实现需要更复杂的逻辑
        
        return True  # 默认一致
    
    def _suggest_improvements(self, response: Dict, assessment: Dict) -> List[str]:
        """提供改进建议"""
        suggestions = []
        
        if assessment.get("confidence", 0) < 0.6:
            suggestions.append("置信度较低，建议提供更多证据支持")
        
        if assessment.get("completeness", 0) < 0.6:
            suggestions.append("回答不完整，建议检查是否遗漏了问题")
        
        if assessment.get("accuracy", 0) < 0.6:
            suggestions.append("准确性存疑，建议核实关键信息")
        
        if assessment.get("consistency", 0) < 0.6:
            suggestions.append("存在不一致，建议检查逻辑连贯性")
        
        if "reasoning_chain" not in response:
            suggestions.append("缺少推理过程，建议展示思考步骤")
        
        return suggestions
    
    def _identify_strengths(self, response: Dict, assessment: Dict) -> List[str]:
        """识别优点"""
        strengths = []
        
        if assessment.get("confidence", 0) >= 0.8:
            strengths.append("置信度高，有充分证据支持")
        
        if assessment.get("completeness", 0) >= 0.8:
            strengths.append("回答完整，覆盖了所有问题")
        
        if "reasoning_chain" in response and len(response["reasoning_chain"]) >= 3:
            strengths.append("推理过程清晰，逻辑连贯")
        
        return strengths
    
    def _identify_weaknesses(self, response: Dict, assessment: Dict) -> List[str]:
        """识别弱点"""
        weaknesses = []
        
        if assessment.get("confidence", 0) < 0.6:
            weaknesses.append("置信度不足，需要更多证据")
        
        if assessment.get("completeness", 0) < 0.6:
            weaknesses.append("回答不完整，可能遗漏了关键问题")
        
        if "reasoning_chain" not in response:
            weaknesses.append("缺少推理过程，难以验证结论")
        
        return weaknesses
    
    def _extract_lessons(self, response: Dict, assessment: Dict) -> List[str]:
        """提取经验教训"""
        lessons = []
        
        # 从评估中提取
        if assessment.get("needs_improvement", False):
            lessons.append("需要改进：确保回答前有充分的推理和证据")
        
        # 从响应中提取
        if "lessons_learned" in response:
            lessons.extend(response["lessons_learned"])
        
        return lessons
    
    def _generate_action_items(self, assessment: Dict) -> List[str]:
        """生成行动项"""
        action_items = []
        
        if assessment.get("needs_improvement", False):
            action_items.append("重新评估响应质量")
            action_items.append("补充缺失的证据或推理")
            action_items.append("再次进行自我评估")
        
        return action_items
    
    def get_assessment_history(self, limit: int = 10) -> List[Dict]:
        """获取评估历史"""
        return self.assessment_history[-limit:]
    
    def get_improvement_trend(self) -> Dict:
        """获取改进趋势"""
        if len(self.assessment_history) < 2:
            return {"trend": "insufficient_data", "message": "数据不足，无法分析趋势"}
        
        # 计算平均分数变化
        recent_scores = [h["assessment"]["overall_score"] for h in self.assessment_history[-5:]]
        older_scores = [h["assessment"]["overall_score"] for h in self.assessment_history[-10:-5]]
        
        if not older_scores:
            return {"trend": "insufficient_data", "message": "数据不足，无法分析趋势"}
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        
        if recent_avg > older_avg + 0.1:
            trend = "improving"
            message = "质量正在提升"
        elif recent_avg < older_avg - 0.1:
            trend = "declining"
            message = "质量有所下降，需要关注"
        else:
            trend = "stable"
            message = "质量保持稳定"
        
        return {
            "trend": trend,
            "message": message,
            "recent_average": recent_avg,
            "older_average": older_avg,
            "change": recent_avg - older_avg
        }


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        assessor = SelfAssessor()
        
        # 模拟响应
        response = {
            "answer": "基于分析，主要问题是用户体验不佳",
            "reasoning_chain": [
                {"step": "收集用户反馈", "result": "100 条反馈"},
                {"step": "分类问题", "result": "5 类主要问题"},
                {"step": "优先级排序", "result": "用户体验最紧急"}
            ],
            "confidence": 0.8
        }
        
        # 评估
        assessment = await assessor.evaluate(response)
        
        print("\n=== 自我评估结果 ===")
        print(f"置信度：{assessment.get('confidence', 0):.2f}")
        print(f"完整性：{assessment.get('completeness', 0):.2f}")
        print(f"准确性：{assessment.get('accuracy', 0):.2f}")
        print(f"一致性：{assessment.get('consistency', 0):.2f}")
        print(f"综合评分：{assessment.get('overall_score', 0):.2f}")
        print(f"需要改进：{assessment.get('needs_improvement', False)}")
        
        if assessment.get("improvement_suggestions"):
            print("\n改进建议:")
            for suggestion in assessment["improvement_suggestions"]:
                print(f"  - {suggestion}")
        
        # 反思
        reflection = await assessor.reflect(response, assessment)
        
        print("\n=== 反思结果 ===")
        print(f"优点：{len(reflection.get('strengths', []))}个")
        print(f"弱点：{len(reflection.get('weaknesses', []))}个")
        print(f"经验教训：{len(reflection.get('lessons_learned', []))}个")
    
    asyncio.run(demo())
