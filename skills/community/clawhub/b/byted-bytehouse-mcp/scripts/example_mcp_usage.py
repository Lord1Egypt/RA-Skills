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
ByteHouse MCP Server 使用示例
演示如何调用MCP Server的tools
"""

# /// script
# dependencies = [
#   "mcp>=1.0.0",
# ]
# ///

import asyncio
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_client import ByteHouseMCPClient


async def example_list_tools():
    """示例1: 列出所有可用的tools"""
    print("=" * 80)
    print("示例1: 列出所有可用的tools")
    print("=" * 80)
    
    async with ByteHouseMCPClient() as client:
        await client.connect()
        
        tools = await client.list_tools()
        print(f"\n找到 {len(tools)} 个tools:\n")
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool['name']}")
            print(f"   描述: {tool['description']}")
            print(f"   参数: {tool['inputSchema']}")
            print()


async def example_query_databases():
    """示例2: 查询所有数据库"""
    print("=" * 80)
    print("示例2: 查询所有数据库")
    print("=" * 80)
    
    async with ByteHouseMCPClient() as client:
        await client.connect()
        
        # 注意：这里需要根据实际的tool名称来调用
        # 先列出tools看看有什么可用的
        tools = await client.list_tools()
        print("\n可用的tools:")
        for tool in tools:
            print(f"  - {tool['name']}")
        
        # 这里需要根据实际的tool名称和参数来调用
        # 由于不同的MCP Server提供的tools可能不同，这里先列出可用的tools


async def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("ByteHouse MCP Server 使用示例")
    print("=" * 80)
    print()
    print("⚠️  请确保已设置以下环境变量:")
    print("  - BYTEHOUSE_HOST")
    print("  - BYTEHOUSE_PORT")
    print("  - BYTEHOUSE_USER")
    print("  - BYTEHOUSE_PASSWORD")
    print()
    
    try:
        # 示例1: 列出所有tools
        await example_list_tools()
        
        # 示例2: 查询数据库
        # await example_query_databases()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
