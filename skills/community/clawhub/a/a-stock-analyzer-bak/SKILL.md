---
name: a-stock-analyzer
version: "2.1.0"
description: "A股智能分析交易助手（专业版）。基于马克·米勒维尼趋势模板和7大严格财务条件筛选优质个股，适用于追求高基本面标准的价值趋势投资者。"
compatibility:
  requires:
    - Python 3.9+
    - akshare (pip install akshare)
    - pandas
    - numpy
    - requests
  os:
    - darwin
    - linux
    - win32
---

# A股智能分析交易助手（专业版）

## 概述

本技能采用**7大严格选股条件**，结合技术面和基本面，筛选A股市场中最优质的个股。

## 7大选股条件

| 条件 | 说明 |
|------|------|
| 1 | 剔除ST股票和上市不满1年的次新股 |
| 2 | 最近一季度营业收入同比增长率 > 25% |
| 3 | 最近一季度净利润同比增长率 > 30% 且环比增长为正 |
| 4 | 股价处于30日均线上方或接近均线（5%以内） |
| 5 | 最近10个交易日平均成交量 > 120日均量（放量） |
| 6 | 净资产收益率（ROE）> 15% |
| 7 | 最近三年净利润复合增长率 > 20% |

## 核心功能

### 1. 大盘分析
- 上证指数、深证成指、创业板指、科创板指
- 实时涨跌幅

### 2. 专业选股
- 从热门股票池筛选
- 逐个检查7大条件
- 获取K线数据计算技术指标
- 获取财务数据分析基本面

### 3. 买卖建议
- 买入区间（现价±2%）
- 目标价（+15%）
- 止损价（-5%）
- 仓位配置（60%/20%/20%）

## 使用方式

### 手动触发
```bash
# 完整分析（大盘+选股）
python3 scripts/analyze.py --full

# 只看大盘
python3 scripts/analyze.py --market

# 只选股
python3 scripts/analyze.py --stocks
```

### 自动推送
配置 cron 定时任务：
```bash
# 每天早上8点分析
0 8 * * 1-5 cd /path/to/a-stock-analyzer && python3 scripts/analyze.py --full
```

## 配置文件 (config.json)

```json
{
  "push": {
    "enabled": true,
    "times": ["08:00", "14:00"],
    "channels": ["dingtalk"]
  },
  "stock": {
    "max_holdings": 3,
    "recommend_count": 3,
    "position_ratio": [0.6, 0.2, 0.2]
  },
  "risk": {
    "stop_loss_pct": 5,
    "stop_profit_pct": 15,
    "max_position_pct": 60
  }
}
```

## 技术指标

| 指标 | 说明 |
|------|------|
| MA30 | 30日均线，价格支撑/压力位 |
| MA60 | 60日均线，中期趋势 |
| MA120 | 120日均线，长期趋势 |
| VOL_MA10 | 10日均量，短期成交量 |
| VOL_MA120 | 120日均量，长期均量 |

## 财务指标

| 指标 | 说明 | 筛选标准 |
|------|------|----------|
| 营收同比 | 营业收入增长速率 | > 25% |
| 净利润同比 | 净利润增长速率 | > 30% |
| 净利润环比 | 净利润环比增长 | > 0% |
| ROE | 净资产收益率 | > 15% |
| 三年复合增长率 | 净利润3年CAGR | > 20% |

## 输出文件

- `reports/report_YYYYMMDD_HHMMSS.md` - 每日分析报告

## 风险提示

⚠️ 
- 本技能仅供参考，不构成投资建议
- 股市有风险，入市需谨慎
- 请根据自身风险承受能力使用
- 严格执行止损纪律

## 依赖安装

```bash
pip install akshare pandas numpy requests
```

## 更新日志

- v2.0.0: 专业版，支持7大严格选股条件，马克·米勒维尼趋势模板
- v1.0.0: 初始版本，基础选股功能
