---
name: earnings-tracker
description: 追踪科技/AI公司财报，自动获取财报日历、预警提醒、生成摘要报告。使用场景：(1) 用户想了解某公司财报时间 (2) 用户需要财报摘要分析 (3) 用户想追踪多家公司的财报动态
---

# AI Earnings Tracker 🦞

追踪科技和AI公司的财报动态，提供：

- 📅 财报日历查询
- 📰 财报新闻获取
- 📊 财报摘要生成
- 🔔 财报预警提醒（Cron定时任务）
- 📈 多公司批量追踪
- 🌐 自动中文翻译

## 快速开始

### 环境配置

需要配置以下环境变量：

```bash
# Tavily API Key（必需）- 用于搜索财报新闻
export TAVILY_API_KEY="tvly-xxxxx"

# GLM API Key（可选）- 用于中文翻译
export ZAI_API_KEY="your-glm-api-key"
```

或配置到 `~/.openclaw/.env` 文件：

```
TAVILY_API_KEY=tvly-xxxxx
ZAI_API_KEY=your-glm-api-key
```

### 基本命令

```bash
# 显示帮助
node fetch-earnings.js help

# 查看追踪公司列表
node fetch-earnings.js list

# 获取财报日历
node fetch-earnings.js calendar

# 获取单个公司财报新闻
node fetch-earnings.js news NVDA

# 生成财报摘要
node fetch-earnings.js summary NVDA

# 追踪新公司（支持多个）
node fetch-earnings.js track NVDA,AAPL,MSFT

# 检查所有追踪公司财报动态
node fetch-earnings.js check

# 不翻译（保持英文）
node fetch-earnings.js check --no-translate
```

## 功能详解

### 1. 📋 公司追踪列表

默认追踪 10 家科技/AI 公司：

| 序号 | 股票代码 | 公司名称 | 行业 |
|------|---------|---------|------|
| 1 | NVDA | NVIDIA | AI/GPU |
| 2 | AAPL | Apple | Consumer Tech |
| 3 | MSFT | Microsoft | Cloud/AI |
| 4 | GOOGL | Google | AI/Search |
| 5 | AMZN | Amazon | Cloud/E-commerce |
| 6 | META | Meta | Social/AI |
| 7 | TSLA | Tesla | EV/AI |
| 8 | AMD | AMD | AI/GPU |
| 9 | PLTR | Palantir | AI/Data |
| 10 | CRM | Salesforce | Enterprise AI |

### 2. 📰 财报新闻获取

```bash
node fetch-earnings.js news NVDA
```

输出示例：

```
📋 NVDA 财报新闻:

🤖 AI 摘要:
英伟达将于 2026 年 2 月 25 日发布 Q1 和 Q2 财季财报。分析师预计调整后每股收益为 1.52 美元...

1. 英伟达股票投资者迎来 Palantir 和 Teradyne 的好消息 (相关度: 86%)
   英伟达将于 2 月 25 日发布季度财报，目前所有迹象都指向一个出色的季度...
```

### 3. 📊 财报摘要生成

```bash
node fetch-earnings.js summary NVDA
```

输出示例：

```
# NVDA 财报摘要

## 🤖 AI 摘要
英伟达预计将于 2026 年 2 月 25 日发布财报...

## 📈 核心数据
- 营收: $39.3B
- 净利润: $22.1B
- EPS: $0.89
- 同比增长: 78%

## 📰 相关新闻
1. 英伟达Q4财报超预期，营收$39.3B
   英伟达公布2026财年Q4财报，营收同比增长78%...
```

### 4. 🔔 财报预警（Cron定时任务）

在 OpenClaw 中配置定时提醒：

```json
{
  "jobs": [
    {
      "name": "earnings-morning-check",
      "schedule": { "kind": "cron", "expr": "0 9 * * 1-5" },
      "payload": {
        "kind": "agentTurn",
        "message": "运行 earnings-tracker check 命令，检查追踪公司的财报动态，如有重要新闻请提醒用户"
      },
      "sessionTarget": "isolated"
    }
  ]
}
```

### 5. 📈 批量检查

```bash
node fetch-earnings.js check
```

自动检查所有追踪公司的财报动态，显示进度：

```
🔍 检查 10 家追踪公司的财报动态...
进度: [10/10] 检查 CRM...

📊 追踪公司财报动态:

【NVDA - NVIDIA】
  1. 英伟达股票投资者迎来利好消息 (相关度: 86%)
     英伟达将于 2 月 25 日发布季度财报...

【TSLA - Tesla】
  1. 特斯拉 Q4 2025 财报预览 (相关度: 61%)
     特斯拉将迎来又一个销量下滑的年份...
```

## 数据来源

1. **财报搜索**: Tavily AI Search API
2. **中文翻译**: GLM-4-flash API

## 使用场景

### 场景1: 日常检查

```
用户: 帮我检查一下追踪的公司有什么财报新闻
Agent: 运行 node fetch-earnings.js check
```

### 场景2: 单独查询

```
用户: NVIDIA最新财报怎么样？
Agent: 运行 node fetch-earnings.js summary NVDA
```

### 场景3: 添加新公司

```
用户: 帮我追踪 Snowflake 的财报
Agent: 运行 node fetch-earnings.js track SNOW
```

## 注意事项

1. **API 限制**: Tavily 免费额度每月 1000 次
2. **时区**: 所有时间为北京时间 (GMT+8)
3. **翻译**: 需要配置 GLM API Key，否则输出英文
4. **合规**: 不提供投资建议，仅供参考

## 配置文件

- `.tracked-companies.json` - 追踪公司列表（自动生成）

## 更新日志

### v2.3 (2026-02-22)
- ✅ 新增自动中文翻译功能
- ✅ 使用 GLM-4-flash 进行翻译
- ✅ 翻译缓存优化
- ✅ `--no-translate` 选项

### v2.2 (2026-02-22)
- ✅ 数据源切换为 Tavily AI Search
- ✅ 移除 Playwright 依赖，纯 API 调用
- ✅ 速度大幅提升
- ✅ AI 摘要功能

### v2.0 (2026-02-19)
- ✅ 优化超时处理
- ✅ 添加进度条显示
- ✅ 支持批量检查

### v1.0 (2026-02-18)
- 🎉 初始版本

---

*Built for OpenClaw | 数据来源: Tavily AI Search | 翻译: GLM-4*
