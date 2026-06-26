"""
Self Reflection Engine - Post-task reflection with 3 questions
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import json


class ReflectionQuestion(Enum):
    """Reflection questions"""
    WHAT_HAPPENED = "what_happened"           # What happened?
    WHAT_WENT_WELL = "what_went_well"         # What went well?
    WHAT_COULD_BE_BETTER = "what_could_be_better"  # What could be better?
    WHAT_LEARNED = "what_learned"             # What did you learn?
    WHAT_WILL_CHANGE = "what_will_change"      # What will you change?


@dataclass
class ReflectionResult:
    """Reflection result data structure"""
    task_id: str
    questions: Dict[ReflectionQuestion, str]  # Question → Answer
    overall_score: float                      # 0-10
    key_insights: List[str]
    improvement_actions: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'task_id': self.task_id,
            'questions': {q.value: a for q, a in self.questions.items()},
            'overall_score': self.overall_score,
            'key_insights': self.key_insights,
            'improvement_actions': self.improvement_actions,
            'created_at': self.created_at.isoformat()
        }


class SelfReflectionEngine:
    """
    Self Reflection Engine
    
    Automatically performs post-task reflection with standardized questions.
    """
    
    # Standard reflection questions (3 questions)
    STANDARD_QUESTIONS = [
        ReflectionQuestion.WHAT_HAPPENED,
        ReflectionQuestion.WHAT_WENT_WELL,
        ReflectionQuestion.WHAT_COULD_BE_BETTER,
    ]
    
    # Deep reflection questions (5 questions)
    DEEP_QUESTIONS = [
        ReflectionQuestion.WHAT_HAPPENED,
        ReflectionQuestion.WHAT_WENT_WELL,
        ReflectionQuestion.WHAT_COULD_BE_BETTER,
        ReflectionQuestion.WHAT_LEARNED,
        ReflectionQuestion.WHAT_WILL_CHANGE,
    ]
    
    # Question templates
    QUESTION_TEMPLATES = {
        ReflectionQuestion.WHAT_HAPPENED: "描述任务执行过程：\n- 任务类型：{task_type}\n- 执行步骤：{steps}\n- 结果：{outcome}",
        ReflectionQuestion.WHAT_WENT_WELL: "列出任务中做得好的 3 个方面：\n1. \n2. \n3. ",
        ReflectionQuestion.WHAT_COULD_BE_BETTER: "列出任务中需要改进的 3 个方面：\n1. \n2. \n3. ",
        ReflectionQuestion.WHAT_LEARNED: "从这次任务中学到了什么？\n- \n- \n- ",
        ReflectionQuestion.WHAT_WILL_CHANGE: "基于这次经验，你将做出什么改变？\n1. \n2. \n3. ",
    }
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize Self Reflection Engine
        
        Args:
            storage_path: Path to store reflections (default: ~/.anima/data/reflections/)
        """
        self.storage_path = Path(storage_path) if storage_path else Path("~/.anima/data/reflections").expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.reflection_history: List[ReflectionResult] = []
        
        # Load existing reflections
        self._load_reflections()
    
    def _load_reflections(self):
        """Load existing reflections from storage"""
        reflections_file = self.storage_path / "reflections.json"
        
        if reflections_file.exists():
            try:
                with open(reflections_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    item['created_at'] = datetime.fromisoformat(item['created_at'])
                    item['questions'] = {
                        ReflectionQuestion(k): v for k, v in item['questions'].items()
                    }
                    result = ReflectionResult(**item)
                    self.reflection_history.append(result)
            except Exception:
                pass
    
    def _save_reflections(self):
        """Save reflections to storage"""
        reflections_file = self.storage_path / "reflections.json"
        
        data = [r.to_dict() for r in self.reflection_history]
        
        with open(reflections_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def reflect(
        self,
        task_id: str,
        task_context: Dict,
        task_result: Dict,
        questions: Optional[List[ReflectionQuestion]] = None
    ) -> ReflectionResult:
        """
        Perform self-reflection
        
        Args:
            task_id: Task ID
            task_context: Task context containing:
                - task_type: Type of task
                - steps: Execution steps
                - outcome: Task outcome
            task_result: Task result containing:
                - success: Whether task succeeded
                - error: Error message if any
                - efficiency: Efficiency score (0-1)
                - patterns_detected: Patterns found
                - missing_knowledge: Knowledge gaps found
            questions: Custom question list (default: STANDARD_QUESTIONS)
            
        Returns:
            Reflection result
        """
        questions = questions or self.STANDARD_QUESTIONS
        
        # Validate inputs
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("task_id must be a non-empty string")
        
        if not isinstance(task_context, dict):
            raise ValueError("task_context must be a dictionary")
        
        if not isinstance(task_result, dict):
            raise ValueError("task_result must be a dictionary")
        
        # Validate task_result keys
        if 'success' not in task_result:
            raise ValueError("task_result must contain 'success' key")
        
        if not isinstance(task_result.get('success'), bool):
            raise ValueError("task_result['success'] must be a boolean")
        
        efficiency = task_result.get('efficiency', 1.0)
        if not isinstance(efficiency, (int, float)) or not (0 <= efficiency <= 1):
            raise ValueError(f"task_result['efficiency'] must be between 0 and 1, got {efficiency}")
        
        # Generate question prompts
        question_answers = self._generate_questions(questions, task_context, task_result)
        
        # Calculate overall score
        overall_score = self._calculate_score(task_result)
        
        # Extract key insights
        key_insights = self._extract_insights(task_context, task_result)
        
        # Extract improvement actions
        improvement_actions = self._extract_actions(task_result)
        
        result = ReflectionResult(
            task_id=task_id,
            questions=question_answers,
            overall_score=overall_score,
            key_insights=key_insights,
            improvement_actions=improvement_actions
        )
        
        # Save to history
        self.reflection_history.append(result)
        self._save_reflections()
        
        return result
    
    def _generate_questions(
        self,
        questions: List[ReflectionQuestion],
        task_context: Dict,
        task_result: Dict
    ) -> Dict[ReflectionQuestion, str]:
        """Generate question prompts"""
        answers = {}
        
        for question in questions:
            template = self.QUESTION_TEMPLATES.get(question, "")
            
            # Format template with context
            try:
                formatted = template.format(
                    task_type=task_context.get("task_type", "unknown"),
                    steps=task_context.get("steps", "N/A"),
                    outcome=task_context.get("outcome", "N/A")
                )
            except KeyError:
                formatted = template
            
            answers[question] = formatted
        
        return answers
    
    def _calculate_score(self, task_result: Dict) -> float:
        """Calculate overall reflection score (0-10)"""
        success = task_result.get("success", True)
        error = task_result.get("error", None)
        efficiency = task_result.get("efficiency", 1.0)
        
        if not success:
            return 3.0
        
        # Base score for success
        base_score = 7.0
        
        # Efficiency bonus/penalty
        if efficiency >= 0.9:
            efficiency_bonus = 2.0
        elif efficiency >= 0.7:
            efficiency_bonus = 1.0
        elif efficiency >= 0.5:
            efficiency_bonus = 0.0
        else:
            efficiency_bonus = -1.0
        
        # Error penalty
        error_penalty = 0.0
        if error:
            error_penalty = 2.0
        
        # Calculate final score
        final_score = base_score + efficiency_bonus - error_penalty
        
        return min(10.0, max(0.0, final_score))
    
    def _extract_insights(self, context: Dict, result: Dict) -> List[str]:
        """Extract key insights from task"""
        insights = []
        
        # From context
        if context.get("complexity") == "high":
            insights.append("高复杂度任务需要更多推理步骤")
        
        if context.get("domain"):
            insights.append(f"领域 {context['domain']} 有特定的最佳实践")
        
        if context.get("task_type"):
            insights.append(f"{context['task_type']} 任务的标准流程")
        
        # From result
        if result.get("patterns_detected"):
            insights.extend(result["patterns_detected"][:2])
        
        if result.get("efficiency", 0) > 0.9:
            insights.append("高效的执行策略")
        
        if result.get("novel_approach"):
            insights.append(f"创新的方法: {result['novel_approach']}")
        
        return insights[:5]  # Max 5 insights
    
    def _extract_actions(self, result: Dict) -> List[str]:
        """Extract improvement actions from result"""
        actions = []
        
        # Error-based actions
        if not result.get("success", True):
            actions.append("分析失败原因并记录到学习日志")
            if result.get("error"):
                actions.append(f"修复错误: {result['error'][:50]}")
        
        # Inefficiency actions
        if result.get("efficiency", 1.0) < 0.7:
            actions.append("优化执行效率")
        
        # Knowledge gap actions
        if result.get("missing_knowledge"):
            for gap in result["missing_knowledge"][:2]:
                actions.append(f"补充知识: {gap[:50]}")
        
        # Pattern-based actions
        if result.get("patterns_to_apply"):
            for pattern in result["patterns_to_apply"][:2]:
                actions.append(f"应用模式: {pattern}")
        
        return actions[:3]  # Max 3 actions
    
    def get_recent_reflections(self, limit: int = 10) -> List[ReflectionResult]:
        """Get recent reflection results"""
        return sorted(
            self.reflection_history,
            key=lambda r: r.created_at,
            reverse=True
        )[:limit]
    
    def get_improvement_trends(self) -> Dict:
        """Get improvement trends"""
        if not self.reflection_history:
            return {"trend": "no_data", "average_score": 0.0}
        
        # Get recent reflections (last 10)
        recent = self.reflection_history[-10:]
        
        scores = [r.overall_score for r in recent]
        avg_score = sum(scores) / len(scores)
        
        # Determine trend
        if len(scores) >= 3:
            if scores[-1] > scores[-3]:
                trend = "improving"
            elif scores[-1] < scores[-3]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Calculate common insights
        all_insights = []
        for r in recent:
            all_insights.extend(r.key_insights)
        
        common_insights = []
        insight_counts = {}
        for insight in all_insights:
            insight_counts[insight] = insight_counts.get(insight, 0) + 1
        
        for insight, count in insight_counts.items():
            if count >= 2:
                common_insights.append(insight)
        
        return {
            "trend": trend,
            "average_score": avg_score,
            "recent_scores": scores,
            "common_insights": common_insights[:5],
            "total_reflections": len(self.reflection_history)
        }
    
    def get_action_items(self) -> List[Dict]:
        """Get pending action items from reflections"""
        action_items = []
        
        for reflection in self.reflection_history[-5:]:
            for action in reflection.improvement_actions:
                action_items.append({
                    "action": action,
                    "from_task": reflection.task_id,
                    "score": reflection.overall_score
                })
        
        return action_items
    
    def clear_old_reflections(self, keep_count: int = 50) -> int:
        """Clear old reflections, keeping most recent"""
        before_count = len(self.reflection_history)
        
        if len(self.reflection_history) > keep_count:
            self.reflection_history = self.reflection_history[-keep_count:]
            self._save_reflections()
        
        return before_count - len(self.reflection_history)
