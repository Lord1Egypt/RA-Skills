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
测试调用 list_tables tool
"""

# /// script
# dependencies = [
#   "mcp>=1.0.0",
# ]
# ///

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_list_tables():
    """测试list_tables tool"""
    print("=" * 80)
    print("测试调用 list_tables tool")
    print("=" * 80)
    
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
    
    print("\n🔌 正在连接MCP Server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ 连接成功！")
            
            # 1. 先列出所有数据库
            print("\n📊 步骤1: 列出所有数据库")
            print("-" * 80)
            result = await session.call_tool("list_databases", {})
            databases = []
            for content in result.content:
                if content.type == 'text':
                    print(content.text)
                    databases = [db.strip() for db in content.text.split('\n') if db.strip()]
            
            # 2. 列出每个数据库的表
            print(f"\n📊 步骤2: 列出每个数据库的表")
            print("-" * 80)
            
            for db in databases:
                print(f"\n📁 数据库: {db}")
                print("-" * 40)
                
                try:
                    result = await session.call_tool("list_tables", {"database": db})
                    for content in result.content:
                        if content.type == 'text':
                            tables = [t.strip() for t in content.text.split('\n') if t.strip()]
                            print(f"   找到 {len(tables)} 张表:")
                            for table in tables:
                                print(f"     - {table}")
                except Exception as e:
                    print(f"   ❌ 查询失败: {e}")
            
            print("\n" + "=" * 80)
            print("✅ 测试完成！")
            print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_list_tables())
