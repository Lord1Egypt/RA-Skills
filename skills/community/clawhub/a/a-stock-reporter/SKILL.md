---
name: a-stock-reporter
description: A股实时行情报告与定时推送。支持用户主动查询个股、生成市场简报、查询历史日报，也可由cron定时触发交易时段报告（9:30/10:30/11:30/13:30/14:30）。激活关键词：股票日报、A股简报、查股票、市场报告、每日研报、历史日报、查询过去。NOT for 美股、港股、期货、基金等非A股资产。
---

# A股行情报告系统

A股实时行情查询与自动报告生成，支持手动查询和定时推送。

## 使用场景

### 1. 用户主动查询个股
```bash
# 查询特定股票
python {baseDir}/scripts/query_stock.py 600519

# 查询多只股票
python {baseDir}/scripts/query_stock.py 600519 000858 300750
```

### 2. 生成市场简报
```bash
# 大盘概览 + 板块表现 + 热门个股
python {baseDir}/scripts/market_brief.py
```

### 3. 定时触发（由cron调用）
```bash
# 交易时段自动报告
python {baseDir}/scripts/trading_update.py --time 0930
python {baseDir}/scripts/trading_update.py --time 1030
python {baseDir}/scripts/trading_update.py --time 1130
python {baseDir}/scripts/trading_update.py --time 1330
python {baseDir}/scripts/trading_update.py --time 1430
```

### 4. 查询历史日报 ⭐ 新增
```bash
# 查询指定日期的历史报告（优先查已保存的报告）
python {baseDir}/scripts/historical_report.py --date 2025-03-05

# 仅查询已保存的报告（离线模式）
python {baseDir}/scripts/historical_report.py --date 2025-03-05 --offline

# 查询并保存到文件
python {baseDir}/scripts/historical_report.py --date 2025-03-01 --save
```

**工作原理**：
1. 首先检查是否有保存的日报文件
2. 如果没有，尝试在线获取历史数据
3. 支持离线查询已保存的历史报告

**日期格式**: `YYYY-MM-DD`，如 `2025-03-05`

## 输出格式

### 个股查询输出示例
```
📈 贵州茅台 (600519)
━━━━━━━━━━━━━━━━━━━━
最新价: ¥1,688.00
涨跌幅: +2.35% 📈
成交量: 12.5万手
成交额: 21.1亿元
振幅: 3.2%
所属板块: 白酒 ⭐核心资产
```

### 市场简报输出示例
```
📊 A股市场简报 - 09:30
━━━━━━━━━━━━━━━━━━━━
【大盘概况】
上证指数: 3,082.47 (-0.98%)
深证成指: 11,917.75 (-0.75%)
创业板指: 2,164.37 (-1.41%)

【板块表现】
🔥 领涨: 白酒 +2.1%, 新能源 +1.8%
📉 领跌: 半导体 -2.5%, 医药 -1.9%

【热门个股】
涨停: 603XXX, 002XXX
跌停: 300XXX, 688XXX

【市场立场】
震荡偏弱，建议观望或轻仓
```

### 历史日报输出示例 ⭐ 新增
```
📊 A股历史日报 - 2024-03-01 (复盘)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【大盘回顾】
上证指数: 3,027.02 (+0.39%) 📈 | 量:412亿
深证成指: 9,432.33 (+1.12%) 📈 | 量:538亿
创业板指: 1,824.44 (+1.20%) 📈 | 量:251亿

【当日特征】
上证振幅: 1.23%
成交金额: 412亿元

【市场立场（复盘）】
📈 震荡上行，适度参与

💡 提示: 历史数据仅供参考，不构成投资建议
```

## 数据参考

板块分类与股票池见 `references/` 目录：
- `sectors.json` - 板块分类及成分股
- `watchlist.json` - 重点观察名单
- `rules.md` - 策略规则说明

## 股票代码格式

- **个股**: 直接输入6位代码，如 600519
- **上证指数**: sh000001
- **深证成指**: sz399001
- **创业板指**: sz399006

## 依赖

```bash
pip install easyquotation requests akshare
```

## 定时配置示例

```cron
# A股交易日定时推送 (周一至周五, 排除节假日)
30 9 * * 1-5 python {baseDir}/scripts/trading_update.py --time 0930
30 10 * * 1-5 python {baseDir}/scripts/trading_update.py --time 1030
30 11 * * 1-5 python {baseDir}/scripts/trading_update.py --time 1130
30 13 * * 1-5 python {baseDir}/scripts/trading_update.py --time 1330
30 14 * * 1-5 python {baseDir}/scripts/trading_update.py --time 1430
```

## 数据来源

- 新浪财经实时行情（easyquotation）
- 腾讯财经大盘数据
- AKShare历史数据（日线数据）
