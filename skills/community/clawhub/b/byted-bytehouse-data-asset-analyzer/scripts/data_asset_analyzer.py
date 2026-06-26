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
数据资产和血缘分析工具
获取数据库表结构，生成数据资产目录和血缘分析
"""

# /// script
# dependencies = [
#   "mcp>=1.0.0",
# ]
# ///

import asyncio
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _extract_engine(create_query: str) -> str:
    """从CREATE TABLE语句中提取引擎"""
    if "ENGINE = " in create_query:
        parts = create_query.split("ENGINE = ")
        if len(parts) > 1:
            engine_part = parts[1].split("\n")[0].split("(")[0].strip()
            return engine_part
    return "Unknown"


def _generate_tags(table: Dict[str, Any]) -> List[str]:
    """为表生成标签"""
    tags = []
    
    # 引擎标签
    engine = table.get("engine", "")
    if "MergeTree" in engine:
        tags.append("merge-tree")
    if "Distributed" in engine:
        tags.append("distributed")
    if "HaMergeTree" in engine or "HaUniqueMergeTree" in engine:
        tags.append("high-availability")
    
    # 表名标签
    table_name = table.get("name", "").lower()
    if "log" in table_name:
        tags.append("log-table")
    if "feedback" in table_name:
        tags.append("user-feedback")
    if "local" in table_name:
        tags.append("local-table")
    if "test" in table_name:
        tags.append("test-table")
    
    return tags


async def analyze_database(database: str, output_dir: str = None):
    """分析数据库并生成报告"""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    os.makedirs(output_dir, exist_ok=True)
    
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
    
    print(f"📊 正在分析数据库: {database}")
    print("-" * 80)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ 连接成功！")
            
            # 1. 列出所有表
            print(f"\n1️⃣  列出所有表...")
            result = await session.call_tool("list_tables", {"database": database})
            
            tables = []
            for content in result.content:
                if content.type == 'text':
                    try:
                        table_data = json.loads(content.text)
                        if isinstance(table_data, dict):
                            tables.append(table_data)
                        elif isinstance(table_data, list):
                            tables.extend(table_data)
                    except:
                        pass
            
            print(f"   找到 {len(tables)} 张表")
            
            # 2. 解析表结构
            print(f"\n2️⃣  解析表结构...")
            schema = {
                "database": database,
                "analyzed_at": datetime.now().isoformat(),
                "tables": []
            }
            
            for i, table in enumerate(tables, 1):
                table_name = table.get("name", "unknown")
                print(f"   [{i}/{len(tables)}] 处理表: {table_name}")
                
                table_info = {
                    "name": table_name,
                    "comment": table.get("comment", ""),
                    "engine": _extract_engine(table.get("create_table_query", "")),
                    "columns": [],
                    "create_table_query": table.get("create_table_query", "")
                }
                
                # 解析列信息
                columns = table.get("columns", [])
                for col in columns:
                    column_info = {
                        "name": col.get("name", ""),
                        "type": col.get("type", ""),
                        "comment": col.get("comment", ""),
                        "default_type": col.get("default_type", ""),
                        "default_expression": col.get("default_expression", ""),
                        "codec_expression": col.get("codec_expression", ""),
                        "ttl_expression": col.get("ttl_expression", "")
                    }
                    table_info["columns"].append(column_info)
                
                schema["tables"].append(table_info)
            
            # 3. 生成数据资产目录
            print(f"\n3️⃣  生成数据资产目录...")
            catalog = {
                "database": database,
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_tables": len(schema["tables"]),
                    "total_columns": sum(len(t["columns"]) for t in schema["tables"]),
                    "engines": {}
                },
                "tables": []
            }
            
            # 统计引擎分布
            for table in schema["tables"]:
                engine = table["engine"]
                catalog["summary"]["engines"][engine] = catalog["summary"]["engines"].get(engine, 0) + 1
            
            # 生成表资产信息
            for table in schema["tables"]:
                table_asset = {
                    "name": table["name"],
                    "comment": table["comment"],
                    "engine": table["engine"],
                    "column_count": len(table["columns"]),
                    "columns": [
                        {
                            "name": c["name"],
                            "type": c["type"],
                            "comment": c["comment"]
                        }
                        for c in table["columns"]
                    ],
                    "tags": _generate_tags(table)
                }
                catalog["tables"].append(table_asset)
            
            # 4. 生成血缘分析
            print(f"\n4️⃣  生成血缘分析...")
            lineage = {
                "database": database,
                "generated_at": datetime.now().isoformat(),
                "table_relationships": [],
                "column_similarities": []
            }
            
            # 分析表关系（基于表名模式）
            tables_list = schema["tables"]
            table_map = {t["name"]: t for t in tables_list}
            
            for table in tables_list:
                table_name = table["name"]
                
                # 查找相关表（基于命名模式）
                related_tables = []
                
                # Distributed表 -> Local表
                if "Distributed" in table["engine"]:
                    local_name = table_name.replace("_local", "")
                    if local_name in table_map:
                        related_tables.append({
                            "type": "distributed_to_local",
                            "target_table": local_name,
                            "description": "Distributed表指向Local表"
                        })
                
                # Local表 -> Distributed表
                if table_name.endswith("_local"):
                    distributed_name = table_name.replace("_local", "")
                    if distributed_name in table_map:
                        related_tables.append({
                            "type": "local_to_distributed",
                            "target_table": distributed_name,
                            "description": "Local表被Distributed表引用"
                        })
                
                if related_tables:
                    lineage["table_relationships"].append({
                        "source_table": table_name,
                        "relationships": related_tables
                    })
            
            # 分析列相似性
            column_map = {}
            for table in tables_list:
                for col in table["columns"]:
                    col_name = col["name"]
                    col_type = col["type"]
                    key = f"{col_name}:{col_type}"
                    if key not in column_map:
                        column_map[key] = []
                    column_map[key].append(table["name"])
            
            for key, table_list in column_map.items():
                if len(table_list) > 1:
                    col_name, col_type = key.split(":", 1)
                    lineage["column_similarities"].append({
                        "column_name": col_name,
                        "column_type": col_type,
                        "found_in_tables": table_list
                    })
            
            # 5. 保存文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            schema_file = os.path.join(output_dir, f"schema_{database}_{timestamp}.json")
            catalog_file = os.path.join(output_dir, f"catalog_{database}_{timestamp}.json")
            lineage_file = os.path.join(output_dir, f"lineage_{database}_{timestamp}.json")
            
            with open(schema_file, "w", encoding="utf-8") as f:
                json.dump(schema, f, ensure_ascii=False, indent=2)
            
            with open(catalog_file, "w", encoding="utf-8") as f:
                json.dump(catalog, f, ensure_ascii=False, indent=2)
            
            with open(lineage_file, "w", encoding="utf-8") as f:
                json.dump(lineage, f, ensure_ascii=False, indent=2)
            
            # 6. 打印摘要
            print("\n" + "=" * 80)
            print("📊 数据资产和血缘分析摘要")
            print("=" * 80)
            
            print(f"\n📁 数据库: {catalog['database']}")
            print(f"📋 总表数: {catalog['summary']['total_tables']}")
            print(f"📝 总列数: {catalog['summary']['total_columns']}")
            
            print(f"\n🔧 引擎分布:")
            for engine, count in catalog["summary"]["engines"].items():
                print(f"   - {engine}: {count} 张表")
            
            print(f"\n🔗 表关系: {len(lineage['table_relationships'])} 组")
            print(f"📊 相似列: {len(lineage['column_similarities'])} 组")
            
            print(f"\n🏷️  表标签示例:")
            tag_count = {}
            for table in catalog["tables"]:
                for tag in table["tags"]:
                    tag_count[tag] = tag_count.get(tag, 0) + 1
            
            for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {tag}: {count} 张表")
            
            print(f"\n📁 输出文件已保存到: {output_dir}")
            print(f"   - Schema: {os.path.basename(schema_file)}")
            print(f"   - 数据资产目录: {os.path.basename(catalog_file)}")
            print(f"   - 血缘分析: {os.path.basename(lineage_file)}")
            
            return {
                "schema": schema,
                "catalog": catalog,
                "lineage": lineage,
                "files": {
                    "schema": schema_file,
                    "catalog": catalog_file,
                    "lineage": lineage_file
                }
            }


async def main():
    """主函数"""
    print("=" * 80)
    print("ByteHouse 数据资产和血缘分析工具")
    print("=" * 80)
    print()
    print("⚠️  请确保已设置以下环境变量:")
    print("  - BYTEHOUSE_HOST")
    print("  - BYTEHOUSE_PORT")
    print("  - BYTEHOUSE_USER")
    print("  - BYTEHOUSE_PASSWORD")
    print()
    
    # 要分析的数据库
    database = "default"
    
    try:
        result = await analyze_database(database)
        print("\n✅ 分析完成！")
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
