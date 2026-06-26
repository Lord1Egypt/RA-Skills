---
name: aastock-daily
description: A股日报 + 持仓管家，自动推送盘前/收盘/夜间简报，监控持仓股动态及股吧舆情，支持周末资讯。
version: 1.1.0
author: moer
---

# A股日报 + 持仓管家 (aastock-daily)

基于东方财富 API 的 A 股市场资讯推送系统，支持每日定时推送、持仓股票追踪及股吧舆情监控。

## 功能特性

| 功能 | 说明 | 推送时间 |
|------|------|----------|
| 📰 盘前快讯 | 隔夜美股、期货、黄金原油、重要新闻 | 09:15 (周一至周五) |
| 💼 持仓追踪(早) | 持仓股行情+公告+股吧舆情 | 09:30 (周一至周五) |
| 📈 收盘简报 | 指数涨跌、板块资金、涨停统计 | 15:00 (周一至周五) |
| 💼 持仓追踪(晚) | 持仓股动态+晚间公告+股吧舆情 | 18:00 (周一至周五) |
| 🌙 夜间复盘 | 龙虎榜、游资动向、外盘夜盘 | 20:00 (周一至周五) |
| 📺 周末资讯 | 市场回顾、周报分析、持仓股公告 | 10:00 / 15:00 (周六周日) |

### 持仓追踪内容

每只持仓股包含：
- 📊 **实时行情** - 当前价格、涨跌幅、主力资金流向
- 📢 **最新公告** - 最新发布的公告或研报标题
- 💬 **股吧舆情** - 散户讨论、投资者问答、社区热点

## 目录结构

```
aastock-daily/
├── SKILL.md              # 本文档
├── config.json            # 用户配置（持仓列表、开关等）
├── config-schema.json     # 配置 JSON Schema
├── scripts/
│   ├── common.sh         # 公共函数库（API、日志、东方财富行情）
│   ├── morning.sh        # 盘前快讯
│   ├── close.sh          # 收盘简报
│   ├── night.sh          # 夜间复盘
│   ├── portfolio.sh      # 持仓追踪（含股吧舆情）
│   └── weekend.sh        # 周末资讯
└── logs/                  # 日志目录
```

## 快速开始

### 1. 配置持仓股票

编辑 `config.json` 中的 `portfolio` 列表：

```json
{
  "portfolio": [
    {"name": "中国建筑", "code": "601668"},
    {"name": "中国广核", "code": "003816"},
    {"name": "中国电信", "code": "601728"}
  ]
}
```

### 2. 手动执行脚本

```bash
# 持仓追踪（含股吧）
bash scripts/portfolio.sh

# 指定早间/晚间
bash scripts/portfolio.sh 早间
bash scripts/portfolio.sh 晚间

# 周末资讯
bash scripts/weekend.sh
```

## 配置说明

### config.json 完整配置

```json
{
  "version": "1.1.0",
  "portfolio": [
    {"name": "股票名称", "code": "股票代码"}
  ],
  "push_schedule": {
    "morning": {"enabled": true, "time": "09:15"},
    "close": {"enabled": true, "time": "15:00"},
    "night": {"enabled": true, "time": "20:00"}
  },
  "portfolio_tracking": {
    "enabled": true,
    "times": ["09:30", "18:00"]
  },
  "weekend": {
    "enabled": true,
    "times": ["10:00", "15:00"]
  }
}
```

## API 调用说明

### 数据来源

| 数据类型 | API 来源 |
|----------|----------|
| 指数/个股行情 | push2.eastmoney.com (免费实时) |
| 涨停/资金流向 | push2.eastmoney.com (免费实时) |
| 新闻/公告/研报 | mkapi2.dfcfs.com (认证API) |
| 股吧舆情 | mkapi2.dfcfs.com (认证API) |

### API 消耗估算

| 脚本 | API 调用次数 |
|------|-------------|
| morning.sh | 6 次 |
| close.sh | 8 次 |
| night.sh | 6 次 |
| portfolio.sh | 21-27 次（含9只股吧） |
| weekend.sh | 10 次 |
| **工作日总计** | ~92 次 |
| **周末总计** | ~10 次 |

## 更新日志

### v1.1.0 (2026-03-28)
- ✅ 新增：持仓股吧舆情功能
- 追踪散户讨论、投资者问答、社区热点

### v1.0.0 (2026-03-28)
- 初始版本
- 支持盘前/收盘/夜间/持仓追踪/周末资讯
