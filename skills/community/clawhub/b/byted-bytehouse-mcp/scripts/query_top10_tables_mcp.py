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
使用MCP Server查询ByteHouse Top 10大表
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


async def query_top10_tables():
    """使用MCP查询Top 10大表"""
    print("=" * 80)
    print("使用MCP Server查询ByteHouse Top 10大表")
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
    
    print("\n🔌 正在连接MCP Server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ 连接成功！")
            
            # 1. 先列出所有数据库
            print("\n📊 步骤1: 列出所有数据库")
            print("-" * 80)
            result = await session.call_tool("list_databases", {})
            for content in result.content:
                if content.type == 'text':
                    print(content.text)
            
            # 2. 查询Top 10大表
            print("\n🏆 步骤2: 查询Top 10大表")
            print("-" * 80)
            sql = """
                SELECT 
                    database,
                    table,
                    sum(bytes) as total_bytes,
                    sum(rows) as total_rows
                FROM system.parts 
                WHERE active = 1
                GROUP BY database, table
                ORDER BY total_bytes DESC
                LIMIT 10
            """
            
            result = await session.call_tool("run_select_query", {"query": sql})
            
            print("\n📊 查询结果:")
            print("-" * 80)
            for content in result.content:
                if content.type == 'text':
                    print(content.text)
            
            print("\n" + "=" * 80)
            print("✅ 查询完成！")
            print("=" * 80)


if __name__ == "__main__":
    asyncio.run(query_top10_tables())
