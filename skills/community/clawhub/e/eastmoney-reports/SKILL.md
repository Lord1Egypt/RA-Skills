---
name: eastmoney-reports
version: 1.0.0
description: 查询和下载东方财富研报，支持行业研报、个股研报、策略报告、宏观研究、券商晨报
tags: [金融数据, 研报查询, 东方财富, 金融, 投资, MCP]
requirements:
  - python >= 3.8
  - pip packages: requests, lxml, fastmcp
---

# 东方财富研报工具

## 功能描述

这是一个命令行 + MCP Server 工具，用于从东方财富网获取研报数据：

- **查询研报**：按行业、股票、类型筛选研报列表
- **下载 PDF**：批量下载研报 PDF 文件
- **行业列表**：查看所有行业分类及代码
- **导出数据**：支持 CSV/Excel 格式导出

支持的研报类型：
- `industry` - 行业研报（分析特定行业）
- `stock` - 个股研报（分析单只股票）
- `strategy` - 策略报告（市场分析、投资策略）
- `macro` - 宏观研究（经济形势分析）
- `morning` - 券商晨报（每日资讯）

## 使用方法

### 命令行模式

```bash
# 查看所有行业
report list

# 搜索行业
report list -s 游戏

# 查询行业研报（游戏行业代码 1046）
report query -i 1046 -s 10

# 查询个股研报（贵州茅台 600519）
report query -t stock -c 600519 -s 5

# 下载研报 PDF
report download -i 1046 -o ./reports -s 3

# 导出为 CSV
report query -i 1046 --save-csv
```

### MCP Server 模式（AI 调用）

```bash
# 启动 MCP Server
python -m mcp_server_fastmcp
```

提供的 MCP 工具：
- `list_industries` - 列出行业分类
- `query_reports` - 查询研报列表
- `download_reports` - 下载研报 PDF
- `get_industry_code` - 搜索行业代码

## 配置变量

无需配置，开箱即用。

## 安装

```bash
git clone https://github.com/manymore13/eastmoney.git
cd eastmoney
pip install -r requirements.txt
```

## 示例

**用户**：帮我查一下游戏行业的最新研报

**助手**：
1. 使用 `get_industry_code` 查找"游戏"行业代码 → 1046
2. 使用 `query_reports` 查询行业研报 → 返回最新研报列表
3. 展示标题、机构、日期等信息

**用户**：下载最新的3篇策略报告

**助手**：使用 `download_reports` 工具，type="strategy", pagesize=3
