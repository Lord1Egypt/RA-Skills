"""
AgentTuple - 四元组抽象

将任何 Agent 形式化为 Φ = (I, C, T, M)
- I: Instruction  任务指令
- C: Context      精选上下文
- T: Tools        工具子集
- M: Model        模型选择

参考: AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json


@dataclass
class AgentTuple:
    """
    Agent 四元组抽象
    
    将 Agent 的能力划分为两个互补轴：
    - 工作记忆轴：(I, C) — 定义"Agent 要做什么、基于什么信息做"
    - 能力轴：(T, M) — 定义"Agent 能做什么、用什么模型做"
    
    Example:
        >>> phi = AgentTuple(
        ...     instruction="搜索 AOrchestra 论文的引用情况",
        ...     context=["论文标题: AOrchestra", "作者: Xu et al.", "年份: 2026"],
        ...     tools=["web_search", "web_fetch"],
        ...     model="glm"
        ... )
        >>> phi.to_spawn_params()
        {'task': '...', 'model': 'glm', ...}
    """
    
    # === 四元组核心字段 ===
    instruction: str                    # I: 任务指令（必须）
    context: List[str] = field(default_factory=list)  # C: 精选上下文（不是全量历史）
    tools: List[str] = field(default_factory=list)    # T: 工具子集（按需分配）
    model: str = "default"              # M: 模型选择
    
    # === 可选元数据 ===
    role: Optional[str] = None          # 角色标签（用于日志和显示）
    max_tokens: int = 4096              # 子 Agent 输出限制
    timeout: int = 300                  # 超时秒数
    
    def __post_init__(self):
        """验证四元组有效性"""
        if not self.instruction or not self.instruction.strip():
            raise ValueError("instruction 不能为空")
        
        # 确保列表类型
        if isinstance(self.context, str):
            self.context = [self.context]
        if isinstance(self.tools, str):
            self.tools = [self.tools]
    
    # === 属性访问器（兼容 AOrchestra 命名）===
    @property
    def I(self) -> str:
        """Instruction - 任务指令"""
        return self.instruction
    
    @property
    def C(self) -> List[str]:
        """Context - 精选上下文"""
        return self.context
    
    @property
    def T(self) -> List[str]:
        """Tools - 工具子集"""
        return self.tools
    
    @property
    def M(self) -> str:
        """Model - 模型选择"""
        return self.model
    
    # === 序列化 ===
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "instruction": self.instruction,
            "context": self.context,
            "tools": self.tools,
            "model": self.model,
            "role": self.role,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
        }
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentTuple":
        """从字典创建"""
        return cls(
            instruction=data["instruction"],
            context=data.get("context", []),
            tools=data.get("tools", []),
            model=data.get("model", "default"),
            role=data.get("role"),
            max_tokens=data.get("max_tokens", 4096),
            timeout=data.get("timeout", 300),
        )
    
    # === OpenClaw sessions_spawn 适配 ===
    
    def to_spawn_params(self, label: Optional[str] = None) -> Dict[str, Any]:
        """
        转换为 sessions_spawn 参数格式
        
        Args:
            label: 可选的标签（会显示在 OpenClaw 日志中）
        
        Returns:
            可以直接传给 sessions_spawn 的参数字典
        """
        # 构建 task 字符串
        task_parts = []
        
        # 添加上下文
        if self.context:
            task_parts.append("[CONTEXT]")
            for ctx in self.context:
                task_parts.append(f"- {ctx}")
            task_parts.append("")
        
        # 添加指令
        task_parts.append("[TASK]")
        task_parts.append(self.instruction)
        
        # 添加输出限制
        task_parts.append("")
        task_parts.append(f"[OUTPUT LIMIT] 返回结果控制在 {self.max_tokens} tokens 以内")
        
        task = "\n".join(task_parts)
        
        # 构建参数
        params = {
            "task": task,
            "model": self.model,
        }
        
        # 添加标签
        if label:
            params["label"] = label
        elif self.role:
            params["label"] = f"{self.role} [model: {self.model}]"
        
        return params
    
    # === 工厂方法 ===
    
    @classmethod
    def researcher(
        cls,
        instruction: str,
        context: List[str] = None,
        model: str = "glm"
    ) -> "AgentTuple":
        """创建研究员 Agent（搜索、信息收集）"""
        return cls(
            instruction=instruction,
            context=context or [],
            tools=["web_search", "web_fetch"],
            model=model,
            role="🔍 researcher",
        )
    
    @classmethod
    def analyst(
        cls,
        instruction: str,
        context: List[str] = None,
        model: str = "kimi"
    ) -> "AgentTuple":
        """创建分析师 Agent（深度分析、对比）"""
        return cls(
            instruction=instruction,
            context=context or [],
            tools=["web_search", "web_fetch", "read"],
            model=model,
            role="📊 analyst",
        )
    
    @classmethod
    def coder(
        cls,
        instruction: str,
        context: List[str] = None,
        model: str = "kimi"
    ) -> "AgentTuple":
        """创建程序员 Agent（代码实现）"""
        return cls(
            instruction=instruction,
            context=context or [],
            tools=["exec", "read", "write", "edit"],
            model=model,
            role="💻 coder",
        )
    
    @classmethod
    def writer(
        cls,
        instruction: str,
        context: List[str] = None,
        model: str = "gemini"
    ) -> "AgentTuple":
        """创建写作者 Agent（报告、文档）"""
        return cls(
            instruction=instruction,
            context=context or [],
            tools=["read", "write"],
            model=model,
            role="✍️ writer",
        )
    
    def __repr__(self) -> str:
        role_str = f"[{self.role}] " if self.role else ""
        return f"AgentTuple({role_str}I='{self.instruction[:50]}...', M='{self.model}', T={self.tools})"


# === 便捷函数 ===

def delegate(
    instruction: str,
    context: List[str] = None,
    tools: List[str] = None,
    model: str = "default",
    role: str = None,
) -> AgentTuple:
    """
    快速创建四元组的便捷函数
    
    Example:
        >>> phi = delegate("搜索 AOrchestra", model="glm")
        >>> phi.role = "🔍 researcher"
    """
    return AgentTuple(
        instruction=instruction,
        context=context or [],
        tools=tools or [],
        model=model,
        role=role,
    )