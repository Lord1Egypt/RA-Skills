#!/usr/bin/env python3
"""
Claude Code Enhancement Skill - Agent 增强模块
参考 Claude Code 的 Agent Tool 设计
"""

import uuid
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class AgentType(Enum):
    """Agent 类型"""
    GENERAL = "general"     # 通用
    WORKER = "worker"       # 工作 Agent
    RESEARCH = "research"   # 研究 Agent
    CODER = "coder"         # 编码 Agent
    REVIEWER = "reviewer"   # 审查 Agent


class AgentStatus(Enum):
    """Agent 状态"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class AgentInput:
    """Agent 输入"""
    description: str        # 任务描述 (3-5 词)
    prompt: str            # 详细提示
    agent_type: str = "general"
    model: str = "sonnet"
    run_in_background: bool = False
    name: Optional[str] = None
    isolation: str = "none"  # none | worktree
    cwd: Optional[str] = None


@dataclass
class AgentOutput:
    """Agent 输出"""
    status: str  # completed | async_launched | failed
    result: Optional[str] = None
    agent_id: Optional[str] = None
    output_file: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class Agent:
    """Agent 实例"""
    id: str
    name: str
    type: AgentType
    status: AgentStatus = AgentStatus.IDLE
    input: Optional[AgentInput] = None
    output: Optional[AgentOutput] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None


class EnhancedAgentTool:
    """增强版 Agent 工具 - 参考 Claude Code 的 AgentTool"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.default_type = AgentType.GENERAL
        self.isolation_mode = "none"
        self.auto_background_threshold = 120000  # 2分钟
    
    def create_agent(self, input_data: AgentInput) -> AgentOutput:
        """创建 Agent"""
        # 生成 Agent ID
        agent_id = input_data.name or f"agent_{str(uuid.uuid4())[:8]}"
        
        # 确定 Agent 类型
        try:
            agent_type = AgentType(input_data.agent_type)
        except ValueError:
            agent_type = AgentType.GENERAL
        
        # 创建 Agent 实例
        agent = Agent(
            id=agent_id,
            name=agent_id,
            type=agent_type,
            input=input_data,
            status=AgentStatus.RUNNING
        )
        
        self.agents[agent_id] = agent
        
        # 检查是否需要后台运行
        if input_data.run_in_background:
            # 异步启动
            asyncio.create_task(self._run_agent_async(agent_id))
            
            return AgentOutput(
                status="async_launched",
                agent_id=agent_id,
                output_file=f"/tmp/{agent_id}_output.txt"
            )
        
        # 同步执行（这里简化处理）
        # 实际需要调用 OpenClaw Agent
        return AgentOutput(
            status="completed",
            agent_id=agent_id,
            result=f"Agent {agent_id} 已创建\n类型: {agent_type.value}\n描述: {input_data.description}"
        )
    
    async def _run_agent_async(self, agent_id: str):
        """异步运行 Agent"""
        agent = self.agents.get(agent_id)
        if not agent:
            return
        
        try:
            # 模拟异步执行
            await asyncio.sleep(1)
            
            agent.status = AgentStatus.COMPLETED
            agent.output = AgentOutput(
                status="completed",
                result=f"Agent {agent_id} 后台任务完成"
            )
            agent.completed_at = datetime.now().isoformat()
        except Exception as e:
            agent.status = AgentStatus.FAILED
            agent.output = AgentOutput(
                status="failed",
                error=str(e)
            )
    
    def get_status(self, agent_id: str) -> str:
        """获取 Agent 状态"""
        agent = self.agents.get(agent_id)
        if not agent:
            return f"❌ Agent `{agent_id}` 不存在"
        
        emoji = {
            AgentStatus.IDLE: "💤",
            AgentStatus.RUNNING: "🔄",
            AgentStatus.COMPLETED: "✅",
            AgentStatus.FAILED: "❌",
            AgentStatus.STOPPED: "🛑"
        }.get(agent.status, "❓")
        
        lines = [
            f"🤖 Agent: **{agent.name}**",
            f"ID: `{agent.id}`",
            f"类型: {agent.type.value}",
            f"状态: {emoji} {agent.status.value}",
        ]
        
        if agent.input:
            lines.append(f"描述: {agent.input.description}")
        
        if agent.output:
            if agent.output.result:
                lines.append(f"结果: {agent.output.result[:100]}...")
            if agent.output.error:
                lines.append(f"错误: {agent.output.error}")
        
        return "\n".join(lines)
    
    def list_agents(self, status_filter: Optional[str] = None) -> str:
        """列出所有 Agent"""
        if not self.agents:
            return "📭 暂无 Agent"
        
        lines = ["**Agent 列表:**\n"]
        
        for agent in self.agents.values():
            if status_filter and agent.status.value != status_filter:
                continue
            
            emoji = {
                AgentStatus.IDLE: "💤",
                AgentStatus.RUNNING: "🔄",
                AgentStatus.COMPLETED: "✅",
                AgentStatus.FAILED: "❌",
                AgentStatus.STOPPED: "🛑"
            }.get(agent.status, "❓")
            
            lines.append(f"{emoji} `{agent.id}` - {agent.type.value}")
        
        return "\n".join(lines)
    
    def stop_agent(self, agent_id: str) -> str:
        """停止 Agent"""
        agent = self.agents.get(agent_id)
        if not agent:
            return f"❌ Agent `{agent_id}` 不存在"
        
        agent.status = AgentStatus.STOPPED
        agent.completed_at = datetime.now().isoformat()
        
        return f"🛑 Agent `{agent_id}` 已停止"
    
    def send_message(self, agent_id: str, message: str) -> str:
        """向 Agent 发送消息"""
        agent = self.agents.get(agent_id)
        if not agent:
            return f"❌ Agent `{agent_id}` 不存在"
        
        if agent.status != AgentStatus.RUNNING:
            return f"❌ Agent `{agent_id}` 当前状态: {agent.status.value}"
        
        # 这里简化处理，实际需要消息队列
        return f"📤 消息已发送到 Agent `{agent_id}`: {message}"


# 全局 Agent 工具实例
_agent_tool: Optional[EnhancedAgentTool] = None


def get_agent_tool() -> EnhancedAgentTool:
    """获取全局 Agent 工具实例"""
    global _agent_tool
    if _agent_tool is None:
        _agent_tool = EnhancedAgentTool()
    return _agent_tool


# CLI 接口
if __name__ == "__main__":
    tool = get_agent_tool()
    
    import sys
    
    if len(sys.argv) < 2:
        print("用法: agent.py <命令> [参数]")
        print("命令: create | status <id> | list | stop <id>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) > 2:
        input_data = AgentInput(
            description=sys.argv[2],
            prompt=" ".join(sys.argv[3:]) if len(sys.argv) > 3 else "请执行任务"
        )
        output = tool.create_agent(input_data)
        print(f"状态: {output.status}")
        if output.agent_id:
            print(f"Agent ID: {output.agent_id}")
    elif cmd == "status" and len(sys.argv) > 2:
        print(tool.get_status(sys.argv[2]))
    elif cmd == "list":
        print(tool.list_agents())
    elif cmd == "stop" and len(sys.argv) > 2:
        print(tool.stop_agent(sys.argv[2]))
    else:
        print(f"未知命令: {cmd}")