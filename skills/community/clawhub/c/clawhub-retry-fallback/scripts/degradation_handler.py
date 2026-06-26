"""
Degradation Handler - 极端场景降级处理机制
遵循PRD 4.4节要求
"""

import time
from typing import Callable, List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field


class DegradationLevel(Enum):
    """降级等级"""
    NONE = 0           # 无降级
    LIGHT = 1          # 轻度降级 - 跳过非核心步骤
    MEDIUM = 2         # 中度降级 - 保留已完成结果
    HEAVY = 3          # 重度降级 - 输出异常分析报告


class StepPriority(Enum):
    """步骤优先级"""
    CRITICAL = 3       # 核心步骤 - 不可跳过
    IMPORTANT = 2      # 重要步骤 - 尽量保留
    OPTIONAL = 1       # 可选步骤 - 可跳过


@dataclass
class TaskStep:
    """任务步骤"""
    name: str
    func: Callable
    priority: StepPriority = StepPriority.IMPORTANT
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    result: Any = None
    executed: bool = False
    failed: bool = False
    error: Optional[str] = None


@dataclass
class DegradationResult:
    """降级执行结果"""
    success: bool
    level: DegradationLevel
    completed_steps: List[str] = field(default_factory=list)
    skipped_steps: List[str] = field(default_factory=list)
    failed_steps: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)
    report: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0


class DegradationHandler:
    """
    极端场景降级处理机制
    
    Features:
    - 三级降级策略（轻度/中度/重度）
    - 智能区分核心/非核心步骤
    - 保留所有中间结果
    - 生成详细降级报告
    """
    
    def __init__(self, enable_degradation: bool = True):
        """
        初始化降级处理器
        
        Args:
            enable_degradation: 是否启用降级处理
        """
        self.enable_degradation = enable_degradation
        self._step_registry: Dict[str, TaskStep] = {}
    
    def mark_critical(self, func: Callable) -> Callable:
        """装饰器：标记为核心步骤（不可跳过）"""
        func._step_priority = StepPriority.CRITICAL
        return func
    
    def mark_optional(self, func: Callable) -> Callable:
        """装饰器：标记为可选步骤（可跳过）"""
        func._step_priority = StepPriority.OPTIONAL
        return func
    
    def execute_with_degradation(
        self,
        steps: List[TaskStep],
        on_skip: Optional[Callable] = None,
        on_degradation: Optional[Callable] = None
    ) -> DegradationResult:
        """
        执行任务链，失败时执行降级处理
        
        Args:
            steps: 任务步骤列表
            on_skip: 步骤被跳过时的回调
            on_degradation: 发生降级时的回调
            
        Returns:
            DegradationResult: 降级执行结果
        """
        if not self.enable_degradation:
            # 降级关闭时，严格模式执行
            return self._strict_execute(steps)
        
        start_time = time.time()
        completed_steps = []
        skipped_steps = []
        failed_steps = []
        results = {}
        
        current_level = DegradationLevel.NONE
        
        for i, step in enumerate(steps):
            try:
                # 执行步骤
                result = step.func(*step.args, **step.kwargs)
                
                step.result = result
                step.executed = True
                completed_steps.append(step.name)
                results[step.name] = result
                
            except Exception as e:
                step.failed = True
                step.error = str(e)
                
                # 根据步骤优先级和当前降级等级决定处理方式
                if step.priority == StepPriority.CRITICAL:
                    # 核心步骤失败
                    if current_level == DegradationLevel.NONE:
                        # 尝试中度降级
                        current_level = DegradationLevel.MEDIUM
                        failed_steps.append(step.name)
                        
                        if on_degradation:
                            on_degradation(current_level, step.name, str(e))
                        
                        # 中度降级：保留已完成结果，终止后续执行
                        break
                    else:
                        # 已经是中度或重度，进入重度降级
                        current_level = DegradationLevel.HEAVY
                        failed_steps.append(step.name)
                        break
                        
                elif step.priority == StepPriority.IMPORTANT:
                    # 重要步骤失败
                    if current_level == DegradationLevel.NONE:
                        # 轻度降级：跳过当前步骤，继续执行
                        current_level = DegradationLevel.LIGHT
                        skipped_steps.append(step.name)
                        
                        if on_skip:
                            on_skip(step.name, str(e))
                        if on_degradation:
                            on_degradation(current_level, step.name, str(e))
                    else:
                        # 已经是中度，进入重度
                        current_level = DegradationLevel.HEAVY
                        failed_steps.append(step.name)
                        break
                        
                else:  # OPTIONAL
                    # 可选步骤失败，直接跳过
                    if current_level == DegradationLevel.NONE:
                        current_level = DegradationLevel.LIGHT
                    skipped_steps.append(step.name)
                    
                    if on_skip:
                        on_skip(step.name, str(e))
        
        duration = time.time() - start_time
        
        # 生成降级报告
        report = self._generate_report(
            steps=steps,
            completed_steps=completed_steps,
            skipped_steps=skipped_steps,
            failed_steps=failed_steps,
            level=current_level,
            duration=duration
        )
        
        # 判断最终成功状态
        success = len(failed_steps) == 0 or current_level != DegradationLevel.HEAVY
        
        return DegradationResult(
            success=success,
            level=current_level,
            completed_steps=completed_steps,
            skipped_steps=skipped_steps,
            failed_steps=failed_steps,
            results=results,
            report=report,
            duration=duration
        )
    
    def _strict_execute(self, steps: List[TaskStep]) -> DegradationResult:
        """严格模式执行（无降级）"""
        start_time = time.time()
        completed_steps = []
        results = {}
        
        for step in steps:
            try:
                result = step.func(*step.args, **step.kwargs)
                step.result = result
                step.executed = True
                completed_steps.append(step.name)
                results[step.name] = result
            except Exception as e:
                step.failed = True
                step.error = str(e)
                
                return DegradationResult(
                    success=False,
                    level=DegradationLevel.HEAVY,
                    completed_steps=completed_steps,
                    failed_steps=[step.name],
                    results=results,
                    report=self._generate_report(
                        steps=steps,
                        completed_steps=completed_steps,
                        skipped_steps=[],
                        failed_steps=[step.name],
                        level=DegradationLevel.HEAVY,
                        duration=time.time() - start_time
                    ),
                    duration=time.time() - start_time
                )
        
        return DegradationResult(
            success=True,
            level=DegradationLevel.NONE,
            completed_steps=completed_steps,
            results=results,
            duration=time.time() - start_time
        )
    
    def _generate_report(
        self,
        steps: List[TaskStep],
        completed_steps: List[str],
        skipped_steps: List[str],
        failed_steps: List[str],
        level: DegradationLevel,
        duration: float
    ) -> Dict[str, Any]:
        """生成降级报告"""
        report = {
            'execution_summary': {
                'total_steps': len(steps),
                'completed': len(completed_steps),
                'skipped': len(skipped_steps),
                'failed': len(failed_steps),
                'success_rate': len(completed_steps) / len(steps) if steps else 0,
                'duration_seconds': duration
            },
            'degradation_info': {
                'level': level.name,
                'description': self._get_level_description(level),
                'enabled': self.enable_degradation
            },
            'step_details': []
        }
        
        for step in steps:
            detail = {
                'name': step.name,
                'priority': step.priority.name,
                'status': 'completed' if step.name in completed_steps else 
                         'skipped' if step.name in skipped_steps else
                         'failed' if step.name in failed_steps else 'pending',
                'executed': step.executed,
                'has_result': step.result is not None
            }
            if step.error:
                detail['error'] = step.error
            report['step_details'].append(detail)
        
        # 重度降级时添加根因分析
        if level == DegradationLevel.HEAVY and failed_steps:
            report['root_cause_analysis'] = {
                'primary_failure': failed_steps[0] if failed_steps else None,
                'failure_chain': failed_steps,
                'recommendations': self._generate_recommendations(steps, failed_steps)
            }
        
        return report
    
    def _get_level_description(self, level: DegradationLevel) -> str:
        """获取降级等级描述"""
        descriptions = {
            DegradationLevel.NONE: "正常执行，无降级",
            DegradationLevel.LIGHT: "轻度降级：跳过非核心步骤，继续执行后续流程",
            DegradationLevel.MEDIUM: "中度降级：保留已完成结果，输出核心内容",
            DegradationLevel.HEAVY: "重度降级：核心步骤失败，输出完整异常分析报告"
        }
        return descriptions.get(level, "未知")
    
    def _generate_recommendations(
        self,
        steps: List[TaskStep],
        failed_steps: List[str]
    ) -> List[str]:
        """生成处理建议"""
        recommendations = []
        
        for failed_name in failed_steps:
            step = next((s for s in steps if s.name == failed_name), None)
            if step:
                if step.priority == StepPriority.CRITICAL:
                    recommendations.append(
                        f"核心步骤 '{failed_name}' 失败，建议检查依赖服务状态或重试任务"
                    )
                else:
                    recommendations.append(
                        f"步骤 '{failed_name}' 失败，可尝试单独重试该步骤"
                    )
        
        return recommendations