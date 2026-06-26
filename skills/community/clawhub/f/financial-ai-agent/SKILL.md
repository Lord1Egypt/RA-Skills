---
name: financial-ai-agent
description: "查询金融行情数据（股票、ETF、虚拟货币等）。当用户提到查询行情、价格、股票代码时使用。例如：'查询SH600519'、'茅台今天收盘价'、'0700.HK最近10天'。"
metadata: {"openclaw": {"emoji": "📈"}}
---

# Financial AI Agent

查询金融行情数据（股票、ETF、虚拟货币等），直接调用 API 获取。

## 🚀 快速开始

### 1. 查询行情

直接告诉我股票代码或名称即可查询：

| 用户说 | 我执行 |
|--------|--------|
| 查询茅台 | `curl .../quotes/SH600519` |
| 查腾讯 | `curl .../quotes/0700.HK` |
| 英伟达最近一周 | `curl .../quotes/NVDA?days=7` |
| 上证指数 | `curl .../quotes/SH000001` |

### 2. 配置自己的 Key

> ⚠️ **提醒**：安装本 skill 后，建议配置自己的 key（默认 key 有并发限制）。
> 
> **获取 key**：访问 https://api.financialagent.cc 注册后获取

**用户只需告诉我：**
- 「我的faa的key是 `XXX`」
- 或「帮我把faa的key换成 `XXX`」

**我帮您存到 OpenClaw 配置文件中（推荐）：**

```bash
# 读取现有配置
config=$(cat ~/.openclaw/openclaw.json)

# 添加或更新 faa key（使用 jq）
jq '. + {"custom": {"financial_agent_key": "XXX"}}' ~/.openclaw/openclaw.json > temp.json && mv temp.json ~/.openclaw/openclaw.json
```

存好后，调用时读取：

```bash
# 从 OpenClaw 配置读取 key
FA_KEY=$(jq -r '.custom.financial_agent_key // "K6lncNNrMAahJccarH63P1ImRMIPCqq7"' ~/.openclaw/openclaw.json)

# 调用 API
curl -H "x-api-key: $FA_KEY" "https://api.financialagent.cc/api/v1/quotes/SH600519"
```

---

## API Key 说明

### 默认 Key

```
K6lncNNrMAahJccarH63P1ImRMIPCqq7
```

（免费体验，有并发限制）

### 自定义 Key

**获取方式：** 访问 https://api.financialagent.cc 注册后获取

配置后调用方式：

```bash
# 从 OpenClaw 配置读取 key
FA_KEY=$(jq -r '.custom.financial_agent_key // "K6lncNNrMAahJccarH63P1ImRMIPCqq7"' ~/.openclaw/openclaw.json)
curl -H "x-api-key: $FA_KEY" "https://api.financialagent.cc/api/v1/quotes/SH600519"
```

---

## 完整调用示例

### 获取日线数据（默认最近30天）

```bash
FA_KEY=$(jq -r '.custom.financial_agent_key // "K6lncNNrMAahJccarH63P1ImRMIPCqq7"' ~/.openclaw/openclaw.json)
curl -H "x-api-key: $FA_KEY" "https://api.financialagent.cc/api/v1/quotes/SH600519"
```

### 获取指定日期范围

```bash
FA_KEY=$(jq -r '.custom.financial_agent_key // "K6lncNNrMAahJccarH63P1ImRMIPCqq7"' ~/.openclaw/openclaw.json)
curl -H "x-api-key: $FA_KEY" "https://api.financialagent.cc/api/v1/quotes/0700.HK?start_date=2026-03-01&end_date=2026-03-20"
```

### 获取最近N天

```bash
FA_KEY=$(jq -r '.custom.financial_agent_key // "K6lncNNrMAahJccarH63P1ImRMIPCqq7"' ~/.openclaw/openclaw.json)
curl -H "x-api-key: $FA_KEY" "https://api.financialagent.cc/api/v1/quotes/AAPL?days=10"
```

---

## 常用股票代码

| 名称 | 代码 |
|------|------|
| 贵州茅台 | SH600519 |
| 腾讯控股 | 0700.HK |
| 阿里巴巴 | 9988.HK |
| 美团 | 3690.HK |
| 苹果 | AAPL |
| 微软 | MSFT |
| 英伟达 | NVDA |
| 特斯拉 | TSLA |
| 上证指数 | SH000001 |
| 深证成指 | SZ399001 |

---

## API 地址

```
https://api.financialagent.cc/api/v1/quotes/{symbol}
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| symbol | 股票代码 | SH600519, 0700.HK, AAPL |
| days | 最近N天 | days=10 |
| start_date | 开始日期 | start_date=2026-03-01 |
| end_date | 结束日期 | end_date=2026-03-20 |

## 返回字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| composite_score | 综合得分 (0-100)，整体评估，非单日 | 56 |
| composite_level | 评级 (S/A/B/C/D)，股票整体评级 | S |

### 评级对应关系

| 等级 | 得分范围 | 说明 |
|------|----------|------|
| S | 90-100 | 极强 |
| A | 70-89 | 强 |
| B | 50-69 | 中等 |
| C | 30-49 | 弱 |
| D | 0-29 | 极弱 |

## 返回数据解析示例

API 返回的 meta 字段包含综合评分（整体评估，非单日数据）：

```json
{
  "meta": {
    "symbol": "00700",
    "name": "腾讯控股",
    "count": 10,
    "composite_score": 49,
    "composite_level": "B"
  }
}
```

解读：
- 综合得分 49 分（整体评估）
- 评级 B（中等），说明该股票整体表现中等
