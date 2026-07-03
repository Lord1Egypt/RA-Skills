#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: agent.core
# 说明: Agent核心循环实现
# 修改建议: 如需扩展，继承AgentCore类或注册Hook
# ============================================
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from ..llm.factory import create_llm_client
from ..llm.client import Message, LLMResponse
from ..tools.registry import ToolRegistry
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class AgentState:
    """Agent状态"""
    messages: List[Message] = field(default_factory=list)
    turn_count: int = 0
    max_turns: int = 50
    stopped: bool = False


class AgentCore:
    """Agent核心实现"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        """
        初始化Agent
        
        Args:
            llm_config: LLM配置
        """
        self.llm_client = create_llm_client(llm_config)
        self.model = llm_config.get("model", "default")
        self.tools = ToolRegistry()
        self.state = AgentState()
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        from ..tools.file_tools import FileTools
        from ..tools.network_tools import NetworkTools
        
        file_tools = FileTools()
        network_tools = NetworkTools()
        
        # 注册文件工具
        self.tools.register("read_file", "读取文件内容", file_tools.read_file_schema, file_tools.read_file)
        self.tools.register("write_file", "写入文件内容", file_tools.write_file_schema, file_tools.write_file)
        self.tools.register("list_files", "列出文件", file_tools.list_files_schema, file_tools.list_files)
        
        # 注册网络工具
        self.tools.register("web_fetch", "获取网页内容", network_tools.web_fetch_schema, network_tools.web_fetch)
        self.tools.register("http_request", "发送HTTP请求", network_tools.http_request_schema, network_tools.http_request)
    
    async def run(self, user_input: str) -> str:
        """
        运行Agent
        
        Args:
            user_input: 用户输入
            
        Returns:
            Agent响应
        """
        # 添加用户消息
        self.state.messages.append(Message(role="user", content=user_input))
        self.state.turn_count += 1
        
        # 检查轮次限制
        if self.state.turn_count > self.state.max_turns:
            return "Error: Maximum turns reached"
        
        # 调用LLM
        try:
            response = await self.llm_client.chat(
                messages=self.state.messages,
                tools=self.tools.get_definitions()
            )
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return f"Error: {e}"
        
        # 处理响应
        if response.tool_calls:
            # 执行工具
            tool_results = []
            for tool_call in response.tool_calls:
                try:
                    result = self.tools.execute(tool_call.name, tool_call.arguments)
                    tool_results.append({
                        "tool_use_id": tool_call.id,
                        "content": str(result)
                    })
                except Exception as e:
                    tool_results.append({
                        "tool_use_id": tool_call.id,
                        "content": f"Error: {e}",
                        "is_error": True
                    })
            
            # 添加工具结果到消息
            self.state.messages.append(Message(
                role="user",
                content=json.dumps(tool_results)
            ))
            
            # 继续循环（简化版，实际应递归调用）
            return f"Tool results: {json.dumps(tool_results)}"
        
        # 返回文本响应
        return response.content
    
    def reset(self):
        """重置Agent状态"""
        self.state = AgentState()
        logger.info("Agent state reset")
