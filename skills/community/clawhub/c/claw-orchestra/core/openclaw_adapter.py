"""
OpenClaw Adapter - 与 OpenClaw sessions_spawn 的集成

这个模块提供与 OpenClaw 的集成接口，让 ClawOrchestra 能够真正调用子 Agent。
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable
import json
import time

# OpenClaw sessions_spawn 工具签名（参考）
# sessions_spawn({
#     "task": "任务描述",
#     "model": "glm",  # 可选，默认用 default_model
#     "label": "标签",  # 可选，用于日志
#     "mode": "run",   # run=一次性, session=持久
#     "timeoutSeconds": 300,  # 超时
# })

from .four_tuple import AgentTuple


@dataclass
class SpawnResult:
    """sessions_spawn 执行结果"""
    success: bool
    output: str = ""
    error: str = ""
    session_key: str = ""
    duration: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "session_key": self.session_key,
            "duration": self.duration,
        }


class OpenClawAdapter:
    """
    OpenClaw 适配器
    
    将 AgentTuple 转换为 sessions_spawn 调用
    
    Example:
        >>> adapter = OpenClawAdapter()
        >>> phi = AgentTuple.researcher("搜索 LangChain")
        >>> result = adapter.spawn(phi)
        >>> print(result.output)
    """
    
    def __init__(
        self,
        default_model: str = "glm",
        timeout: int = 300,
        verbose: bool = True,
    ):
        self.default_model = default_model
        self.timeout = timeout
        self.verbose = verbose
        
        # 外部注入的 spawn 函数（由主 Agent 提供）
        self._spawn_fn: Optional[Callable] = None
    
    def set_spawn_fn(self, fn: Callable):
        """
        设置 spawn 函数
        
        在 OpenClaw 环境中，这应该是 sessions_spawn 工具
        
        Args:
            fn: 接受 dict 参数，返回 dict 结果的函数
        """
        self._spawn_fn = fn
    
    def spawn(self, phi: AgentTuple) -> SpawnResult:
        """
        执行子 Agent
        
        Args:
            phi: Agent 四元组
            
        Returns:
            SpawnResult: 执行结果
        """
        start_time = time.time()
        
        # 构建 spawn 参数
        params = self._build_spawn_params(phi)
        
        if self.verbose:
            print(f"\n🚀 Spawn 子 Agent:")
            print(f"   角色: {phi.role or '未指定'}")
            print(f"   模型: {phi.model}")
            print(f"   指令: {phi.instruction[:80]}...")
        
        try:
            if self._spawn_fn:
                # 使用注入的 spawn 函数
                result = self._spawn_fn(params)
                output = self._extract_output(result)
                session_key = result.get("sessionKey", "")
            else:
                # 模拟模式（用于测试）
                output = self._mock_spawn(phi)
                session_key = ""
            
            duration = time.time() - start_time
            
            if self.verbose:
                print(f"   ✅ 完成: {duration:.1f}s")
            
            return SpawnResult(
                success=True,
                output=output,
                session_key=session_key,
                duration=duration,
            )
        
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            
            if self.verbose:
                print(f"   ❌ 错误: {error_msg}")
            
            return SpawnResult(
                success=False,
                error=error_msg,
                duration=duration,
            )
    
    def spawn_parallel(self, phi_list: List[AgentTuple]) -> List[SpawnResult]:
        """
        并行执行多个子 Agent
        
        注意：OpenClaw 的 sessions_spawn 在同一轮调用时自动并行
        
        Args:
            phi_list: 四元组列表
            
        Returns:
            结果列表（顺序与输入一致）
        """
        if self.verbose:
            print(f"\n🚀 并行 Spawn {len(phi_list)} 个子 Agent:")
            for i, phi in enumerate(phi_list):
                print(f"   [{i+1}] {phi.role or 'Agent'} (model={phi.model})")
        
        # TODO: 在实际使用时，应该在同一轮工具调用中发起所有 spawn
        # 这里先串行模拟
        results = []
        for phi in phi_list:
            result = self.spawn(phi)
            results.append(result)
        
        return results
    
    def _build_spawn_params(self, phi: AgentTuple) -> Dict[str, Any]:
        """
        构建 sessions_spawn 参数
        
        Args:
            phi: Agent 四元组
            
        Returns:
            sessions_spawn 参数字典
        """
        # 构建任务字符串
        task_parts = []
        
        # 添加上下文（精选，不是全量历史）
        if phi.context:
            task_parts.append("[CONTEXT]")
            for ctx in phi.context:
                task_parts.append(f"- {ctx}")
            task_parts.append("")
        
        # 添加指令
        task_parts.append("[TASK]")
        task_parts.append(phi.instruction)
        
        # 添加输出限制
        task_parts.append("")
        task_parts.append(f"[OUTPUT] 返回简洁结果，控制在 {phi.max_tokens} tokens 以内")
        
        task = "\n".join(task_parts)
        
        # 构建参数
        params = {
            "task": task,
            "mode": "run",  # 一次性执行
            "timeoutSeconds": phi.timeout,
        }
        
        # 模型（使用指定的或默认的）
        model = phi.model if phi.model != "default" else self.default_model
        params["model"] = model
        
        # 标签
        if phi.role:
            params["label"] = f"{phi.role} [model: {model}]"
        
        return params
    
    def _extract_output(self, result: Dict[str, Any]) -> str:
        """
        从 sessions_spawn 结果中提取输出
        
        Args:
            result: sessions_spawn 返回的结果
            
        Returns:
            输出字符串
        """
        # sessions_spawn 返回格式：
        # {
        #   "sessionKey": "xxx",
        #   "status": "completed",
        #   "result": "输出内容" 或 {"message": "输出内容"}
        # }
        
        if isinstance(result, str):
            return result
        
        if isinstance(result, dict):
            # 尝试多种可能的输出字段
            if "result" in result:
                r = result["result"]
                if isinstance(r, str):
                    return r
                if isinstance(r, dict) and "message" in r:
                    return r["message"]
            
            if "output" in result:
                return result["output"]
            
            if "message" in result:
                return result["message"]
        
        return str(result)
    
    def _mock_spawn(self, phi: AgentTuple) -> str:
        """
        模拟 spawn（用于测试）
        
        Args:
            phi: Agent 四元组
            
        Returns:
            模拟输出
        """
        time.sleep(0.3)  # 模拟延迟
        return f"[模拟输出] 已完成: {phi.instruction[:50]}... (model={phi.model})"


# === 便捷函数 ===

def spawn_agent(
    instruction: str,
    context: List[str] = None,
    model: str = "glm",
    role: str = None,
) -> str:
    """
    快速 spawn 一个子 Agent
    
    Example:
        >>> output = spawn_agent("搜索 LangChain", model="glm")
    """
    adapter = OpenClawAdapter()
    phi = AgentTuple(
        instruction=instruction,
        context=context or [],
        model=model,
        role=role,
    )
    result = adapter.spawn(phi)
    return result.output if result.success else f"Error: {result.error}"