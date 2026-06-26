"""
Action Space - 编排器动作空间

AOrchestra 的核心洞察：编排器只需要两个动作
- Delegate(Φ): 创建子 Agent 并委派任务
- Finish(y): 终止并输出最终答案

这种极简动作空间使编排器专注于"做什么"而非"怎么做"
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from enum import Enum

from .four_tuple import AgentTuple


class ActionType(Enum):
    """动作类型枚举"""
    DELEGATE = "delegate"
    FINISH = "finish"


@dataclass
class Delegate:
    """
    Delegate 动作 - 委托子任务给动态创建的 Sub-Agent
    
    编排器通过四元组 Φ = (I, C, T, M) 完整定义一个子任务：
    - I: 要做什么（指令）
    - C: 基于什么信息做（精选上下文）
    - T: 能用什么工具（工具子集）
    - M: 用什么模型（成本-性能权衡）
    
    Example:
        >>> action = Delegate(
        ...     phi=AgentTuple(
        ...         instruction="搜索 LangChain 的最新版本",
        ...         context=["用户在做框架对比研究"],
        ...         tools=["web_search", "web_fetch"],
        ...         model="glm"
        ...     ),
        ...     reasoning="需要先收集 LangChain 的信息"
        ... )
    """
    
    phi: AgentTuple                       # 四元组定义
    reasoning: str = ""                   # 编排器的推理过程（用于可解释性）
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.DELEGATE
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": "delegate",
            "reasoning": self.reasoning,
            "params": {
                "instruction": self.phi.instruction,
                "context": self.phi.context,
                "tools": self.phi.tools,
                "model": self.phi.model,
                "role": self.phi.role,
            }
        }
    
    def __repr__(self) -> str:
        return f"Delegate({self.phi.role or 'agent'}, model={self.phi.model})"


@dataclass
class Finish:
    """
    Finish 动作 - 终止交互并输出最终答案
    
    当编排器认为任务已完成时，调用 Finish 输出答案。
    
    Example:
        >>> action = Finish(
        ...     answer="LangChain 0.1.0 发布于 2024年1月",
        ...     reasoning="所有子任务都已完成，答案已确定"
        ... )
    """
    
    answer: str                            # 最终答案
    reasoning: str = ""                    # 编排器的推理过程
    confidence: float = 1.0                # 置信度 (0-1)
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.FINISH
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": "finish",
            "reasoning": self.reasoning,
            "params": {
                "answer": self.answer,
                "confidence": self.confidence,
            }
        }
    
    def __repr__(self) -> str:
        preview = self.answer[:50] + "..." if len(self.answer) > 50 else self.answer
        return f"Finish(answer='{preview}')"


# === 动作解析 ===

def parse_action(data: Dict[str, Any]) -> Union[Delegate, Finish]:
    """
    从 LLM 输出解析动作
    
    Args:
        data: LLM 返回的 JSON 对象
        
    Returns:
        Delegate 或 Finish 动作对象
        
    Raises:
        ValueError: 无法解析的动作
    """
    action = data.get("action", "").lower()
    
    if action == "delegate":
        params = data.get("params", {})
        phi = AgentTuple(
            instruction=params.get("instruction", ""),
            context=params.get("context", []),
            tools=params.get("tools", []),
            model=params.get("model", "default"),
            role=params.get("role"),
        )
        return Delegate(
            phi=phi,
            reasoning=data.get("reasoning", ""),
        )
    
    elif action == "finish":
        params = data.get("params", {})
        return Finish(
            answer=params.get("answer", ""),
            reasoning=data.get("reasoning", ""),
            confidence=params.get("confidence", 1.0),
        )
    
    else:
        raise ValueError(f"未知动作: {action}")


# === 动作验证 ===

def validate_delegate(action: Delegate, available_models: List[str]) -> List[str]:
    """
    验证 Delegate 动作的有效性
    
    Args:
        action: Delegate 动作
        available_models: 可用模型列表
        
    Returns:
        错误消息列表（空列表表示有效）
    """
    errors = []
    
    # 检查 instruction
    if not action.phi.instruction or not action.phi.instruction.strip():
        errors.append("instruction 不能为空")
    
    # 检查 model
    if action.phi.model not in available_models and action.phi.model != "default":
        errors.append(f"模型 '{action.phi.model}' 不在可用列表中: {available_models}")
    
    return errors


def validate_finish(action: Finish) -> List[str]:
    """
    验证 Finish 动作的有效性
    
    Args:
        action: Finish 动作
        
    Returns:
        错误消息列表（空列表表示有效）
    """
    errors = []
    
    if not action.answer or not action.answer.strip():
        errors.append("answer 不能为空")
    
    if not 0 <= action.confidence <= 1:
        errors.append(f"confidence 必须在 [0, 1] 范围内，当前: {action.confidence}")
    
    return errors