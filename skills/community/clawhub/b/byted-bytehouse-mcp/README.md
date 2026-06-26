# ByteHouse MCP Server Skill

## 🔵 ByteHouse 品牌标识
> 「ByteHouse」—— 火山引擎云原生数据仓库，极速、稳定、安全、易用
> 
> 本Skill基于ByteHouse官方MCP Server，提供完整的ByteHouse数据访问能力

---

## 📁 文件说明

- **SKILL.md** - 技能主文档，包含详细使用说明
- **mcp_client.py** - MCP客户端模块，用于程序化调用
- **test_mcp_server.py** - MCP Server测试脚本
- **example_mcp_usage.py** - MCP使用示例
- **query_top10_tables_mcp.py** - 使用MCP查询Top 10大表
- **test_list_tables.py** - 测试list_tables tool
- **data_asset_analyzer.py** - 数据资产和血缘分析工具（新增）
- **start_mcp_service.sh** - 启动常驻MCP Server服务
- **stop_mcp_service.sh** - 停止服务
- **status_mcp_service.sh** - 查看状态
- **restart_mcp_service.sh** - 重启服务
- **README.md** - 本文件，快速入门指南

## 🎯 ByteHouse MCP Server Tools

| 序号 | Tool名称 | 功能描述 |
|------|----------|----------|
| 1 | **list_databases** | 列出所有数据库 |
| 2 | **list_tables** | 列出指定数据库中的所有表 |
| 3 | **run_select_query** | 运行SELECT查询 |
| 4 | **run_dml_ddl_query** | 运行DML/DDL查询 |
| 5 | **get_bytehouse_table_engine_doc** | 获取ByteHouse表引擎文档 |

## 🚀 快速开始

### 前置配置

在使用前，请先配置ByteHouse连接信息：

```bash
export BYTEHOUSE_HOST="<ByteHouse-host>"
export BYTEHOUSE_PORT="<ByteHouse-port>"
export BYTEHOUSE_USER="<ByteHouse-user>"
export BYTEHOUSE_PASSWORD="<ByteHouse-password>"
export BYTEHOUSE_SECURE="true"
export BYTEHOUSE_VERIFY="true"
```

### 方法1: 测试MCP Server（推荐先测试）

```bash
cd /root/.openclaw/workspace/skills/bytehouse-mcp
# 先设置环境变量，然后运行
uv run test_mcp_server.py
```

### 方法2: 列出数据库中的表

```bash
cd /root/.openclaw/workspace/skills/bytehouse-mcp
# 先设置环境变量，然后运行
uv run test_list_tables.py
```

### 方法3: 使用MCP查询Top 10大表

```bash
cd /root/.openclaw/workspace/skills/bytehouse-mcp
# 先设置环境变量，然后运行
uv run query_top10_tables_mcp.py
```

### 方法4: 生成数据资产和血缘分析（新增）

```bash
cd /root/.openclaw/workspace/skills/bytehouse-mcp
# 先设置环境变量，然后运行
uv run data_asset_analyzer.py
```

**功能说明：**
- 获取数据库完整schema（所有表和字段）
- 生成数据资产目录（表统计、引擎分布、自动标签）
- 生成血缘分析（表关系、列相似性）
- 保存JSON文件到 `output/` 目录

**输出文件：**
- `schema_{database}_{timestamp}.json` - 完整schema
- `catalog_{database}_{timestamp}.json` - 数据资产目录
- `lineage_{database}_{timestamp}.json` - 血缘分析

### 方法5: 启动常驻MCP Server服务

```bash
cd /root/.openclaw/workspace/skills/bytehouse-mcp
# 先在脚本中配置环境变量，然后运行
./start_mcp_service.sh
```

### 方法6: 查看服务状态

```bash
./status_mcp_service.sh
```

### 方法7: 查看日志

```bash
tail -f logs/mcp_server_*.log
```

### 方法8: 停止服务

```bash
./stop_mcp_service.sh
```

## 💻 使用MCP Tools示例

### 示例1: 列出所有数据库

```python
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 设置环境变量（请自行配置）
    env = os.environ.copy()
    env.update({
        'BYTEHOUSE_HOST': '<ByteHouse-host>',
        'BYTEHOUSE_PORT': '<ByteHouse-port>',
        'BYTEHOUSE_USER': '<ByteHouse-user>',
        'BYTEHOUSE_PASSWORD': '<ByteHouse-password>',
        'BYTEHOUSE_SECURE': 'true',
        'BYTEHOUSE_VERIFY': 'true',
    })
    
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
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 调用list_databases
            result = await session.call_tool("list_databases", {})
            for content in result.content:
                if content.type == 'text':
                    print(content.text)

asyncio.run(main())
```

### 示例2: 列出数据库中的表

```python
# 调用list_tables
result = await session.call_tool("list_tables", {"database": "default"})
```

### 示例3: 运行SELECT查询

```python
# 调用run_select_query
sql = "SELECT * FROM default.conversation_feedback LIMIT 10"
result = await session.call_tool("run_select_query", {"query": sql})
```

### 示例4: 查询Top 10大表

```python
# 查询Top 10大表
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
```

## 🔧 服务管理

### 启动服务
```bash
# 先配置环境变量，然后运行
./start_mcp_service.sh
```

### 查看状态
```bash
./status_mcp_service.sh
```

### 停止服务
```bash
./stop_mcp_service.sh
```

### 重启服务
```bash
./restart_mcp_service.sh
```

## 📚 更多信息

详细使用说明请参考 [SKILL.md](./SKILL.md)

---
*最后更新: 2026-03-12*
