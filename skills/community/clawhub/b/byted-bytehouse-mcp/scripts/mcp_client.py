#!/usr/bin/env python3
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
MCP Client - 用于与MCP Server通信的客户端
"""

# /// script
# dependencies = [
#   "mcp>=1.0.0",
# ]
# ///

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ByteHouseMCPClient:
    """ByteHouse MCP客户端"""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self._exit_stack = AsyncExitStack()
        self.server_params = None
        
    async def __aenter__(self):
        await self._exit_stack.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)
        
    async def connect(self):
        """连接到ByteHouse MCP Server"""
        
        # 从环境变量获取配置
        env = os.environ.copy()
        
        # MCP Server参数
        self.server_params = StdioServerParameters(
            command='/root/.local/bin/uvx',
            args=[
                '--from',
                'git+https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse',
                'mcp_bytehouse',
                '-t',
                'stdio'
            ],
            env=env
        )
        
        print("🔌 正在连接到ByteHouse MCP Server...")
        
        # 启动stdio客户端
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        
        # 创建会话
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(stdio_transport[0], stdio_transport[1])
        )
        
        # 初始化会话
        await self.session.initialize()
        
        print("✅ 连接成功！")
        return self
        
    async def list_tools(self) -> List[Dict]:
        """列出所有可用的tools"""
        if not self.session:
            raise RuntimeError("Not connected")
            
        result = await self.session.list_tools()
        tools = []
        for tool in result.tools:
            tools.append({
                'name': tool.name,
                'description': tool.description,
                'inputSchema': tool.inputSchema
            })
        return tools
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """调用tool"""
        if not self.session:
            raise RuntimeError("Not connected")
            
        result = await self.session.call_tool(tool_name, arguments)
        
        # 处理结果
        outputs = []
        for content in result.content:
            if content.type == 'text':
                outputs.append(content.text)
            elif content.type == 'image':
                outputs.append(f"[Image: {content.data[:50]}...]")
                
        return outputs


# 便捷函数
async def run_mcp_tool(tool_name: str, arguments: Dict[str, Any] = None):
    """运行单个MCP tool"""
    if arguments is None:
        arguments = {}
        
    async with ByteHouseMCPClient() as client:
        await client.connect()
        
        # 先列出tools
        print("\n📋 可用的Tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
            
        print(f"\n🚀 调用Tool: {tool_name}")
        print(f"   参数: {json.dumps(arguments, ensure_ascii=False)}")
        
        # 调用tool
        result = await client.call_tool(tool_name, arguments)
        
        print("\n📊 结果:")
        for output in result:
            print(output)
            
        return result


if __name__ == "__main__":
    # 测试：列出所有tools
    async def main():
        async with ByteHouseMCPClient() as client:
            await client.connect()
            
            print("\n📋 可用的Tools:")
            tools = await client.list_tools()
            for tool in tools:
                print(f"\n  {tool['name']}")
                print(f"    描述: {tool['description']}")
                print(f"    参数: {json.dumps(tool['inputSchema'], ensure_ascii=False, indent=6)}")
    
    asyncio.run(main())
