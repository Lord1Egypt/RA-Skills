---
name: 短线手术刀 (ScalpelTrade)
description: "A股短线量化分析工具 — 实时行情、9因子选股、多空辩论+风控审查、推荐追踪闭环。数据源：新浪财经+东方财富（免费行情）。"
tags:
  - finance
  - china-stocks
  - a-shares
  - market-data
  - stock-screening
  - multi-agent
  - debate-analysis
version: 2.2.0
---

# 短线手术刀 (ScalpelTrade) v2.2 — A股短线多因子量化分析工具

专为A股短线交易设计的多Agent量化分析框架。四层架构（采集→分析→辩论→追踪），提供从数据采集到推荐闭环的全链路支持。

## 架构

```
         ┌──────────────────────────────────────────┐
Layer 4  │  追踪层: tracker.py                      │
         │  推荐记录 → 每日检查 → 报告生成           │
         ├──────────────────────────────────────────┤
Layer 3  │  决策层: debater.py                      │
         │  多头×空头辩论 → 风控审查 → 分歧转一致检测  │
         ├──────────────────────────────────────────┤
Layer 2  │  分析层: analyzer.py                     │
         │  多日趋势分析、假跌破检测、因子评分         │
         ├──────────────────────────────────────────┤
Layer 1  │  执行层: fetcher.py                      │
         │  实时行情(新浪) + 资金流向(东方财富) +     │
         │  9项技术因子(RSI/MACD/KDJ/布林/ICU等)     │
         └──────────────────────────────────────────┘
```

## 用法

### Layer 1: 数据层

#### 单只实时行情
```bash
python3 {baseDir}/scripts/fetcher.py
```
返回结构化数据：price、change_pct、high、low、amount_yi、volume_wan

#### 批量行情
```python
from scripts.fetcher import fetch_batch
results = fetch_batch(["000001","000002","600519"])
```

#### 技术指标计算（v2.2 — 9个因子）
```python
from scripts.fetcher import fetch_kline, calc_indicators
kline = fetch_kline("300042", "daily", 120)
indicators = calc_indicators(kline)
# 返回: ma5/10/20/60, RSI6/14, MACD+柱, KDJ, Bollinger, ICU均线(中泰2023), 鳄鱼线(招商2024), ADX, OBV
```

#### 东方财富资金流向（v2.2 新增）
```python
from scripts.fetcher import eastmoney_kline, eastmoney_sector_flow

# 个股基础数据（换手率、量比、市值）
data = eastmoney_kline("002842")

# 板块资金排行Top10
sectors = eastmoney_sector_flow(10)  # 主力净流入、涨跌幅、超大单、散户
```

### Layer 2: 分析层

#### 全市场扫描
```bash
python3 {baseDir}/scripts/analyzer.py scan
```
按板块输出涨跌幅排行（含多日趋势、假跌破检测）

#### 市场简报
```bash
python3 {baseDir}/scripts/analyzer.py report
```
生成Markdown格式日报，保存到 reports/ 目录

#### 市场状态检测
```bash
python3 {baseDir}/scripts/analyzer.py regime
```
判断当前市场处于牛市/熊市/震荡（均线偏离度法）

#### 板块资金流向采集
```python
from scripts.analyzer import collect_sector_flow
sf = collect_sector_flow(15)
```

### Layer 3: 决策层 — 多空辩论+风控审查

#### 完整五层辩论流程（TradingAgents架构）
```bash
python3 {baseDir}/scripts/debater.py 002842
```
输出：
- **多头论点**：均线、量能、RSI、MACD金叉、KDJ金叉、ICU均线、鳄鱼线、分歧转一致
- **空头论点**：超买、超涨、死叉、布林上轨、OBV流出
- **主持人裁决**：多/空/分歧
- **风控审查**：风险等级(高/中/低)、建议仓位上限、超买/波动率警报
- **分歧转一致信号**：缩量回调后放量突破、横盘启动、回踩支撑反弹

### Layer 4: 追踪层 — 推荐闭环（v2.2 新增）

#### 记录推荐
```bash
python3 {baseDir}/scripts/tracker.py record 002842 long 35.76 32.0 42.0 '钨涨价+分歧转一致'
```

#### 每日检查
```bash
python3 {baseDir}/scripts/tracker.py check
```
自动检查所有活跃推荐，含技术因子快照、止损/止盈触发、自动关闭

#### 生成报告
```bash
python3 {baseDir}/scripts/tracker.py report
```
输出Markdown格式追踪报告，显示每只推荐标的的入场价、当前收益、RSI/MACD/ICU状态

## 数据源

| 数据源 | 类型 | 数据内容 | 成本 |
|--------|------|---------|------|
| **新浪财经** (sina) | HTTP REST | 实时行情、日K/周K/分钟K线、板块涨跌排行 | 免费 |
| **东方财富** (eastmoney) | HTTP REST | 换手率、量比、总市值/流通市值、市盈率、**板块资金流向排行**(主力净流入/超大单/散户) | 免费 |

零成本，无需 API Key。

## 升级日志

| 版本 | 日期 | 内容 |
|------|------|------|
| v2.2.0 | 2026-06-11 | 短线手术刀正式更名; 新增东方财富数据源(换手率/量比/市值/板块资金排行); 新增RSI/MACD/KDJ/布林/ICU均线/鳄鱼线/ADX/OBV共9因子; 新增分歧转一致检测+风控审查(risk_audit); 新增推荐追踪引擎(tracker.py); 新增多日趋势分析+假跌破检测 |
| v2.0 | 2026-06-10 | 统一import路径、新增三层架构、新增debater.py辩论引擎、新增calc_indicators指标计算、单接口fetch_realtime独立行情获取 |

## 技术参考

- StockBench (arXiv 2025) — LLM交易代理评估框架
- TradingAgents (UCLA+MIT) — 多Agent投行模拟架构
- 中国基金报 (2026-04) — A股打板生态深度剖析
- QuantsPlaybook (hugo2046) — 券商金工因子库
- 中泰证券《ICU均线下的择时策略》(2023)
- 招商证券《基于鳄鱼线的指数择时及轮动策略》(2024)

## 依赖

- Python 3.8+
- 标准库（urllib、json、csv、re、math）

## 合规声明

仅提供市场数据整理与技术指标计算，**不构成任何投资建议**。投资有风险，决策需自主。
