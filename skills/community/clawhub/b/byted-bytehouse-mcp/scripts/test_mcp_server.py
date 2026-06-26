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
测试ByteHouse MCP Server
直接通过stdio与MCP Server通信
"""

# /// script
# dependencies = [
#   "mcp>=1.0.0",
# ]
# ///

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """测试MCP Server"""
    print("=" * 80)
    print("测试ByteHouse MCP Server")
    print("=" * 80)
    print()
    print("⚠️  请确保已设置以下环境变量:")
    print("  - BYTEHOUSE_HOST")
    print("  - BYTEHOUSE_PORT")
    print("  - BYTEHOUSE_USER")
    print("  - BYTEHOUSE_PASSWORD")
    print()
    
    # 从环境变量获取配置
    env = os.environ.copy()
    
    # MCP Server参数
    server_params = StdioServerParameters(
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
    
    print("\n📦 正在安装和启动MCP Server...")
    print("   这可能需要几分钟时间...")
    print()
    
    try:
        # 启动stdio客户端
        async with stdio_client(server_params) as (read, write):
            # 创建会话
            async with ClientSession(read, write) as session:
                # 初始化会话
                print("🔌 正在初始化MCP会话...")
                await session.initialize()
                print("✅ 会话初始化成功！")
                print()
                
                # 列出可用的tools
                print("📋 正在获取可用的tools...")
                result = await session.list_tools()
                
                print(f"\n✅ 找到 {len(result.tools)} 个tools:\n")
                for i, tool in enumerate(result.tools, 1):
                    print(f"{i}. {tool.name}")
                    print(f"   描述: {tool.description}")
                    print(f"   参数: {tool.inputSchema}")
                    print()
                
                # 如果有tools，尝试调用第一个
                if result.tools:
                    first_tool = result.tools[0]
                    print(f"🚀 尝试调用第一个tool: {first_tool.name}")
                    print()
                    
                    try:
                        # 尝试调用tool（使用空参数）
                        call_result = await session.call_tool(first_tool.name, {})
                        
                        print("📊 调用结果:")
                        print("-" * 80)
                        for content in call_result.content:
                            if content.type == 'text':
                                print(content.text)
                            elif content.type == 'image':
                                print(f"[Image data: {len(content.data)} bytes]")
                        print("-" * 80)
                        
                    except Exception as e:
                        print(f"⚠️  调用tool失败 (可能需要特定参数): {e}")
                        print("   但这不影响MCP Server的正常工作")
                
                print("\n" + "=" * 80)
                print("🎉 MCP Server测试成功！")
                print("=" * 80)
                print()
                print("💡 下一步:")
                print("  1. 启动常驻服务: ./start_mcp_service.sh")
                print("  2. 查看状态: ./status_mcp_service.sh")
                print("  3. 停止服务: ./stop_mcp_service.sh")
                print()
                
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(test_mcp_server()))
