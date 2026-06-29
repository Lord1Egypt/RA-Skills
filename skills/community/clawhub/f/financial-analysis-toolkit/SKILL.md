---
name: financial-analysis-toolkit
version: 1.0.0
description: 实用金融分析工具包 — 基于 OpenClaw 内置工具 + AKShare + pywencai 实现金融数据获取和分析，参考 Anthropic financial-services 技能包的方法论。
source: anthropol/financial-services (方法论) + AKShare/pywencai/web_search (数据源)
---

# 金融分析工具包 v1.0

> 替代 MCP 数据源（CapIQ、FactSet 等），用 OpenClaw 现有工具实现金融分析。

## 数据源架构

| 数据需求 | 数据源 | 工具 |
|---------|--------|------|
| 全球/中国新闻 | 权威媒体 | `web_search(freshness=oneDay)` |
| A 股行情 | AKShare | `ak.stock_zh_a_hist()` |
| 指数行情 | AKShare | `ak.stock_zh_index_daily()` |
| 财务报表 | AKShare | `ak.stock_yjbb_em()` |
| 自然语言选股 | pywencai | `pywencai.get()` |
| 宏观数据 | AKShare/web_search | `ak.macro_china_*()` |
| 个股估值 | AKShare | `ak.stock_value_em()` |

## 可用分析

### 1. 个股基本面分析
- PE/PB/ROE/毛利率/净利率
- 营收/利润增长趋势
- 市值与行业对比

### 2. 技术面分析
- 日 K 线数据获取
- 均线系统（MA5/10/20/60）
- MACD/KDJ/RSI 指标计算

### 3. 行业分析
- 行业资金流向（pywencai）
- 板块涨跌幅排行
- 行业估值对比

### 4. 宏观分析
- LPR/利率数据
- CPI/PPI
- PMI 数据

### 5. 市场概览
- 沪深两市成交额
- 北向资金流向
- 涨跌家数比

## 使用方法

用户说"查一下 XX 股票"、"分析 XX 行业"、"大盘怎么样"时，按以下流程执行：

1. **识别意图** → 个股/行业/宏观/市场概览
2. **获取数据** → 调用 AKShare/pywencai/web_search
3. **分析方法** → 参考 financial-financial-analysis 等已安装技能包中的方法论
4. **生成报告** → 结构化输出

## 参考技能包

以下技能包已安装，提供建模方法论：

| 技能包 | 路径 | 用途 |
|--------|------|------|
| financial-financial-analysis | `skills/financial-financial-analysis/` | DCF/LBO/Comps 建模 |
| financial-equity-research | `skills/financial-equity-research/` | 研报框架 |
| financial-investment-banking | `skills/financial-investment-banking/` | 投行分析 |
| financial-private-equity | `skills/financial-private-equity/` | PE 尽调 |
| financial-wealth-management | `skills/financial-wealth-management/` | 财富管理 |
| financial-fund-admin | `skills/financial-fund-admin/` | 基金运营 |
| financial-operations | `skills/financial-operations/` | 运营合规 |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-05-21 | 初始版本，整合 AKShare/pywencai/web_search |
