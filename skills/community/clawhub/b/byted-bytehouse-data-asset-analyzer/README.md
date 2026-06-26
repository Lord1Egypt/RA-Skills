# ByteHouse 数据资产和血缘分析 Skill

## 🔵 ByteHouse 品牌标识
> 「ByteHouse」—— 火山引擎云原生数据仓库，极速、稳定、安全、易用
> 
> 本Skill基于ByteHouse MCP Server，提供完整的数据资产盘点和血缘分析能力

---

## 📁 文件说明

- **SKILL.md** - 技能主文档，包含详细使用说明
- **data_asset_analyzer.py** - 数据资产和血缘分析主程序
- **README.md** - 本文件，快速入门指南

## 🎯 功能特性

### 1. 完整Schema获取
- 获取指定数据库的所有表
- 获取每张表的所有字段
- 提取表引擎、注释等元数据
- 解析CREATE TABLE语句

### 2. 数据资产目录生成
- 表统计（总表数、总列数）
- 引擎分布统计
- 自动标签生成
- 表资产详情

### 3. 血缘分析
- 表关系识别（Distributed → Local）
- 列相似性分析
- 关系可视化

## 🚀 快速开始

### 前置条件

本skill依赖 `bytehouse-mcp` skill，确保已正确配置：

```bash
cd /root/.openclaw/workspace/skills/bytehouse-mcp
# 确认bytehouse-mcp可以正常工作
uv run test_mcp_server.py
```

### 方法1: 运行数据资产和血缘分析

```bash
cd /root/.openclaw/workspace/skills/bytehouse-data-asset-analyzer

# 先设置环境变量（复用bytehouse-mcp的配置）
export BYTEHOUSE_HOST="<ByteHouse-host>"
export BYTEHOUSE_PORT="<ByteHouse-port>"
export BYTEHOUSE_USER="<ByteHouse-user>"
export BYTEHOUSE_PASSWORD="<ByteHouse-password>"
export BYTEHOUSE_SECURE="true"
export BYTEHOUSE_VERIFY="true"

# 运行分析工具
uv run data_asset_analyzer.py
```

**输出文件（保存在 `output/` 目录）：**
1. **`schema_{database}_{timestamp}.json`** - 完整的数据库schema
2. **`catalog_{database}_{timestamp}.json`** - 数据资产目录
3. **`lineage_{database}_{timestamp}.json`** - 血缘分析报告

## 📊 输出文件说明

### 1. Schema文件
包含数据库的完整结构，所有表和字段信息。

### 2. 数据资产目录
包含数据资产的统计信息、引擎分布、自动标签等。

### 3. 血缘分析
包含表关系识别和列相似性分析。

## 🏷️ 自动标签生成

分析器会根据表名和引擎自动生成标签：
- `merge-tree` - 使用MergeTree引擎
- `distributed` - 使用Distributed引擎
- `high-availability` - 使用HaMergeTree
- `log-table` - 表名包含"log"
- `user-feedback` - 表名包含"feedback"
- `local-table` - 表名以"_local"结尾
- `test-table` - 表名包含"test"

## 📚 更多信息

详细使用说明请参考 [SKILL.md](./SKILL.md)

ByteHouse访问配置请参考 [bytehouse-mcp skill](../bytehouse-mcp/SKILL.md)

---
*最后更新: 2026-03-12*
