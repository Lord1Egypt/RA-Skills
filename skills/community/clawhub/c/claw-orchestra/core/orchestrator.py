"""
Orchestrator - 编排器主逻辑

编排器的核心职责：
1. 分析任务 → 分解子任务
2. 为每个子任务构建四元组 Φ = (I, C, T, M)
3. 调用 sessions_spawn 执行
4. 收集结果 → 决定继续或完成

设计原则（来自 AOrchestra）：
- 编排器不直接执行环境动作，只做决策
- 动作空间极简：{Delegate, Finish}
- 上下文精选：只传递任务相关的信息
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Union
import json
import time

from .four_tuple import AgentTuple
from .action_space import Delegate, Finish, ActionType, parse_action
from .openclaw_adapter import OpenClawAdapter


@dataclass
class SubTaskResult:
    """子任务执行结果"""
    phi: AgentTuple                    # 执行的四元组
    success: bool                      # 是否成功
    output: str = ""                   # 输出内容
    error: str = ""                    # 错误信息
    duration: float = 0.0              # 执行耗时（秒）
    tokens_used: int = 0               # 消耗的 token 数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "instruction": self.phi.instruction,
            "model": self.phi.model,
            "role": self.phi.role,
            "success": self.success,
            "output": self.output[:500] if self.output else "",  # 截断长输出
            "error": self.error,
            "duration": self.duration,
            "tokens_used": self.tokens_used,
        }


@dataclass
class OrchestrationState:
    """编排状态"""
    original_task: str                           # 原始任务
    attempt: int = 0                             # 当前尝试次数
    max_attempts: int = 10                       # 最大尝试次数
    subtask_history: List[SubTaskResult] = field(default_factory=list)  # 子任务历史
    context: str = ""                            # 累积上下文
    total_cost: float = 0.0                      # 总成本
    total_tokens: int = 0                        # 总 token 数
    
    def add_result(self, result: SubTaskResult):
        """添加子任务结果"""
        self.subtask_history.append(result)
        # 更新上下文
        if result.success:
            self.context += f"\n[✓] {result.phi.instruction[:100]}\n结果: {result.output[:200]}\n"
        else:
            self.context += f"\n[✗] {result.phi.instruction[:100]}\n错误: {result.error}\n"
    
    def format_history(self) -> str:
        """格式化子任务历史（用于 prompt）"""
        if not self.subtask_history:
            return "暂无子任务执行历史"
        
        lines = []
        for i, result in enumerate(self.subtask_history, 1):
            status = "✅" if result.success else "❌"
            lines.append(f"[{i}] {status} {result.phi.role or 'Agent'} (model={result.phi.model})")
            lines.append(f"    任务: {result.phi.instruction[:80]}...")
            if result.success:
                lines.append(f"    结果: {result.output[:100]}...")
            else:
                lines.append(f"    错误: {result.error}")
            lines.append(f"    耗时: {result.duration:.1f}s")
            lines.append("")
        
        # 汇总
        success_count = sum(1 for r in self.subtask_history if r.success)
        lines.append(f"---\n汇总: {success_count}/{len(self.subtask_history)} 子任务成功")
        
        return "\n".join(lines)


@dataclass
class OrchestratorConfig:
    """编排器配置"""
    main_model: str = "sonnet"                   # 编排器使用的模型
    sub_models: List[str] = field(default_factory=lambda: ["glm", "kimi", "gemini"])  # 子 Agent 可用模型
    max_attempts: int = 10                       # 最大编排轮数
    default_model: str = "glm"                   # 默认子模型
    enable_context_routing: bool = True          # 启用上下文路由
    enable_model_routing: bool = True            # 启用模型路由
    verbose: bool = True                         # 详细日志


class Orchestrator:
    """
    编排器 - AOrchestra 的核心
    
    编排器通过两个动作完成任务：
    1. Delegate(Φ): 创建子 Agent 并委派任务
    2. Finish(y): 终止并输出最终答案
    
    Example:
        >>> orchestrator = Orchestrator(
        ...     main_model="sonnet",
        ...     sub_models=["glm", "kimi", "gemini"]
        ... )
        >>> result = orchestrator.run("帮我调研三个 AI 框架的对比")
    """
    
    def __init__(
        self,
        main_model: str = "sonnet",
        sub_models: List[str] = None,
        max_attempts: int = 10,
        default_model: str = "glm",
        verbose: bool = True,
        config: OrchestratorConfig = None,
    ):
        self.config = config or OrchestratorConfig(
            main_model=main_model,
            sub_models=sub_models or ["glm", "kimi", "gemini"],
            max_attempts=max_attempts,
            default_model=default_model,
            verbose=verbose,
        )
        
        # 状态
        self.state: Optional[OrchestrationState] = None
        
        # OpenClaw 适配器
        self._adapter: Optional[OpenClawAdapter] = None
        
        # 外部依赖注入（用于测试或自定义执行）
        self._spawn_fn: Optional[Callable] = None
        self._llm_fn: Optional[Callable] = None
    
    def set_adapter(self, adapter: OpenClawAdapter):
        """设置 OpenClaw 适配器（用于真正调用 sessions_spawn）"""
        self._adapter = adapter
    
    def set_spawn_fn(self, fn: Callable):
        """设置子 Agent 执行函数（用于测试或自定义）"""
        self._spawn_fn = fn
    
    def set_llm_fn(self, fn: Callable):
        """设置编排器 LLM 调用函数（用于测试或自定义）"""
        self._llm_fn = fn
    
    def run(self, task: str) -> str:
        """
        执行编排任务
        
        Args:
            task: 任务描述
            
        Returns:
            最终答案
        """
        # 初始化状态
        self.state = OrchestrationState(
            original_task=task,
            max_attempts=self.config.max_attempts,
        )
        
        if self.config.verbose:
            print(f"\n{'='*60}")
            print(f"🎯 开始编排任务: {task[:100]}...")
            print(f"   主模型: {self.config.main_model}")
            print(f"   子模型: {self.config.sub_models}")
            print(f"   最大轮数: {self.config.max_attempts}")
            print(f"{'='*60}\n")
        
        # 编排循环
        while self.state.attempt < self.state.max_attempts:
            self.state.attempt += 1
            
            if self.config.verbose:
                print(f"\n📍 轮次 {self.state.attempt}/{self.config.max_attempts}")
            
            # 1. 决策下一步动作
            action = self._decide_action()
            
            if self.config.verbose:
                print(f"   决策: {action.action_type.value}")
            
            # 2. 执行动作
            if action.action_type == ActionType.FINISH:
                # 完成
                if self.config.verbose:
                    print(f"\n✅ 任务完成!")
                    print(f"   答案: {action.answer[:200]}...")
                    print(f"   总轮数: {self.state.attempt}")
                    print(f"   总成本: ${self.state.total_cost:.4f}")
                
                return action.answer
            
            elif action.action_type == ActionType.DELEGATE:
                # 委托子任务
                result = self._execute_delegate(action)
                self.state.add_result(result)
                
                if self.config.verbose:
                    status = "✅" if result.success else "❌"
                    print(f"   {status} 子任务完成: {result.duration:.1f}s")
                    if not result.success:
                        print(f"      错误: {result.error}")
        
        # 超过最大轮数
        if self.config.verbose:
            print(f"\n⚠️ 达到最大轮数 {self.config.max_attempts}，强制结束")
        
        return self._generate_fallback_answer()
    
    def _decide_action(self) -> Union[Delegate, Finish]:
        """
        决策下一步动作
        
        这是编排器的核心决策逻辑。
        
        Returns:
            Delegate 或 Finish 动作
        """
        # 构建决策 prompt
        prompt = self._build_decision_prompt()
        
        # 调用 LLM
        if self._llm_fn:
            response = self._llm_fn(prompt)
        else:
            # 默认：使用简单的启发式规则
            response = self._heuristic_decision()
        
        # 解析动作
        try:
            action = parse_action(response)
        except ValueError:
            # 解析失败，回退到启发式
            action = self._heuristic_decision_action()
        
        return action
    
    def _build_decision_prompt(self) -> str:
        """构建决策 prompt"""
        return f"""你是编排器（Orchestrator），负责分解任务并委派给子 Agent。

==== 当前状态 ====
原始任务: {self.state.original_task}
当前轮次: {self.state.attempt}/{self.state.max_attempts}

==== 子任务历史 ====
{self.state.format_history()}

==== 可用模型 ====
{self._format_model_table()}

==== 输出格式 ====
返回 JSON:
- 委托子任务: {{"action": "delegate", "reasoning": "...", "params": {{"instruction": "...", "context": [...], "tools": [...], "model": "glm"}}}}
- 完成任务: {{"action": "finish", "reasoning": "...", "params": {{"answer": "..."}}}}

==== 决策 ====
分析任务和子任务历史，决定下一步动作。"""
    
    def _format_model_table(self) -> str:
        """格式化模型表格"""
        lines = ["| 模型 | 特点 | 适用场景 |"]
        lines.append("|------|------|----------|")
        
        model_info = {
            "glm": "便宜、速度快、中文好",
            "kimi": "长上下文、代码强",
            "gemini": "创意好、多模态",
            "sonnet": "均衡、推理稳",
            "opus": "最强推理",
        }
        
        for model in self.config.sub_models:
            info = model_info.get(model, "通用")
            lines.append(f"| {model} | {info} | 任务类型 |")
        
        return "\n".join(lines)
    
    def _heuristic_decision(self) -> Dict[str, Any]:
        """启发式决策（当没有 LLM 时使用）"""
        # 简单规则：
        # - 如果是第一轮，委托一个搜索任务
        # - 如果已经有结果，总结并完成
        
        if self.state.attempt == 1:
            return {
                "action": "delegate",
                "reasoning": "第一轮，开始搜索信息",
                "params": {
                    "instruction": f"搜索并收集关于 '{self.state.original_task}' 的信息",
                    "context": [],
                    "tools": ["web_search", "web_fetch"],
                    "model": self.config.default_model,
                }
            }
        else:
            # 汇总结果
            outputs = [r.output for r in self.state.subtask_history if r.success]
            answer = "\n\n".join(outputs) if outputs else "无法完成任务"
            
            return {
                "action": "finish",
                "reasoning": "已有足够信息，完成任务",
                "params": {
                    "answer": answer,
                }
            }
    
    def _heuristic_decision_action(self) -> Union[Delegate, Finish]:
        """启发式决策动作对象"""
        data = self._heuristic_decision()
        return parse_action(data)
    
    def _execute_delegate(self, action: Delegate) -> SubTaskResult:
        """
        执行 Delegate 动作
        
        Args:
            action: Delegate 动作
            
        Returns:
            子任务执行结果
        """
        start_time = time.time()
        
        try:
            # 使用 OpenClawAdapter 执行
            if self._adapter:
                result = self._adapter.spawn(action.phi)
                duration = time.time() - start_time
                
                return SubTaskResult(
                    phi=action.phi,
                    success=result.success,
                    output=result.output,
                    error=result.error,
                    duration=duration,
                )
            elif self._spawn_fn:
                # 使用注入的执行函数（向后兼容）
                output = self._spawn_fn(action.phi)
                duration = time.time() - start_time
                
                return SubTaskResult(
                    phi=action.phi,
                    success=True,
                    output=output,
                    duration=duration,
                )
            else:
                # 默认执行：打印并返回模拟结果
                output = self._default_spawn(action.phi)
                duration = time.time() - start_time
                
                return SubTaskResult(
                    phi=action.phi,
                    success=True,
                    output=output,
                    duration=duration,
                )
        
        except Exception as e:
            duration = time.time() - start_time
            return SubTaskResult(
                phi=action.phi,
                success=False,
                error=str(e),
                duration=duration,
            )
    
    def _default_spawn(self, phi: AgentTuple) -> str:
        """
        默认的子 Agent 执行（模拟）
        
        在实际使用时，应该设置 adapter 或 spawn_fn
        """
        if self.config.verbose:
            print(f"\n   🚀 派遣子 Agent:")
            print(f"      角色: {phi.role or '未指定'}")
            print(f"      模型: {phi.model}")
            print(f"      指令: {phi.instruction[:80]}...")
            print(f"      工具: {phi.tools}")
        
        # 模拟执行
        time.sleep(0.3)
        
        return f"[模拟结果] 已完成: {phi.instruction[:50]}..."
    
    def _generate_fallback_answer(self) -> str:
        """生成回退答案（当达到最大轮数时）"""
        outputs = [r.output for r in self.state.subtask_history if r.success]
        if outputs:
            return f"达到最大轮数，部分结果汇总：\n\n" + "\n\n".join(outputs)
        else:
            return "抱歉，未能完成任务。请尝试简化任务或提供更多信息。"


# === 便捷函数 ===

def orchestrate(
    task: str,
    main_model: str = "sonnet",
    sub_models: List[str] = None,
    max_attempts: int = 10,
) -> str:
    """
    快速编排任务的便捷函数
    
    Example:
        >>> result = orchestrate("帮我调研三个 AI 框架的对比")
    """
    orchestrator = Orchestrator(
        main_model=main_model,
        sub_models=sub_models,
        max_attempts=max_attempts,
    )
    return orchestrator.run(task)