---
name: fund-flow
description: |
  资金流向分析工具 v1.1.0。分析股票/板块的主力资金净流入排行、
  散户资金对比、净额排序。支持资金趋势检测(3/5/10日)、
  板块聚合分析、多时间维度(日/周/月)、与指数对比、强度评分。

  Use when: 需要分析资金流向趋势、
  查看主力资金动向、板块资金对比、资金强度评分。

  🎉 v1.1.0 新增:
  - --trend: 资金趋势检测(3/5/10日方向 + 持续性)
  - --sector: 板块聚合分析(按板块汇总资金)
  - --timeframe: 多时间维度(day/week/month/year)
  - --compare: 与指数/大盘对比(跑赢/跑输)
  - 资金强度评分(主力占比、持续性、背离度)
  - --chart: ASCII趋势图
  - 主力流入占比指标

  触发关键词：资金流向、主力资金、板块排行、股票分析、资金趋势
  适用范围：CSV 资金流向数据(日频)
  运行模式：纯本地
---

# 💹 Fund Flow

## Overview
分析A股市场的资金流向数据，通过主力(超大单+大单)和散户(小单)的净流入对比，识别资金趋势。支持趋势检测、板块聚合、多时间维度分析。

## Usage
```bash
# 基本排行
python3 scripts/fund_flow.py --file fundflow.csv

# 资金趋势检测
python3 scripts/fund_flow.py --file fundflow.csv --trend

# 板块聚合分析
python3 scripts/fund_flow.py --file fundflow.csv --sector --sector-col 板块

# 周度分析
python3 scripts/fund_flow.py --file fundflow.csv --timeframe week

# 与指数对比
python3 scripts/fund_flow.py --file fundflow.csv --compare --index-name 沪深300

# ASCII趋势图
python3 scripts/fund_flow.py --file fundflow.csv --chart

# 输出JSON
python3 scripts/fund_flow.py --file fundflow.csv --output ranking.json
```

## 输出示例
```
💰 资金流向分析
    ==================================================================
    识别列: 代码=name, 主力=mainForce, 散户=retail
    总标的: 45
    主力总流入: +12,450,000,000
    散户总流入: -3,200,000,000
    净总额: +9,250,000,000
    ==================================================================
    排名  代码           记录   主力净流入        散户净流入           净额        占比
    ---------------------------------------------------------------------------
       1 比亚迪            22   +852,000,000    -124,000,000   +728,000,000↑  87%
       2 宁德时代          20   +645,000,000     -98,000,000   +547,000,000↑  87%
       3 茅台              18   +423,000,000     -45,000,000   +378,000,000↑  90%
       4 东方财富          20   -120,000,000    +230,000,000   -350,000,000↓  34%
```

## 命令详解
| 命令 | 说明 |
|------|------|
| (默认) | 资金流向排行分析 |
| --trend | 资金趋势检测(3/5/10日方向+持续性) |
| --sector | 板块聚合分析 |
| --timeframe | 多时间维度分析 |
| --compare | 与指数对比 |
| --chart | ASCII趋势图 |

## 资金强度评分
综合以下因素：
- **主力流入方向**: 正/负流入 ±15分
- **主力占比**: >60% +10分, >40% +5分
- **持续性**: 连续流入3天+ +10分
- **背离信号**: 主力流入+散户流出 +10分

## CSV列自动识别
| 角色 | 候选列名 |
|------|---------|
| 代码 | name, 代码, stock, 板块, sector |
| 主力净流入 | main_force, mainForce, netamount, 主力净流入 |
| 散户净流入 | retail, retailForce, 小单净流入 |
| 日期 | date, 日期, trade_date |
| 板块 | sector, 板块, industry, 行业 |

## Security
- ✅ 纯本地运行，无网络请求
- ✅ 只读CSV数据文件
- ❌ 无任意代码执行
