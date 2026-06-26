---
name: eastmoney_tools
description: 东方财富金融数据工具集，集成选股、资讯搜索、行情财务查询三大功能。当用户查询 A股、港股、美股相关数据时使用，包括：条件选股、股票推荐、板块成分股；新闻、公告、研报、政策搜索；实时行情、财务指标、公司信息、资金流向等数据查询。
required_env_vars:
  - EASTMONEY_APIKEY
credentials:
  - type: api_key
    name: EASTMONEY_APIKEY
    description: 从东方财富技能市场获取的 API Key（支持多 key 轮换）
---

# 东方财富金融工具集 (eastmoney-tools)

统一入口，根据用户 query 自动路由到合适的 API。支持多 API Key 轮换。

## API Key 配置

### 方式 1：单 Key（环境变量）

```bash
export EASTMONEY_APIKEY="your-api-key"
```

### 方式 2：多 Key 轮换（vault）

从 vault 读取多个 key，按顺序轮换：

```bash
cat ~/.openclaw/workspace/vault/credentials/eastmoney.json
```

vault 文件格式：
```json
{
  "name": "Eastmoney API Keys",
  "keys": [
    "mkt_xxx1",
    "mkt_xxx2",
    "mkt_xxx3"
  ]
}
```

### 获取 Key

如果没有设置 `EASTMONEY_APIKEY`，从 vault 读取：
```bash
cat ~/.openclaw/workspace/vault/credentials/eastmoney.json
```

## 路由规则

根据用户意图自动判断调用哪个 API：

| 用户意图关键词 | 路由到 | API 端点 |
|---------------|--------|----------|
| 选股、推荐股票、条件筛选、符合xx的股票、成分股 | 选股 | `/finskillshub/api/claw/stock-screen` |
| 新闻、资讯、消息、公告、研报、政策、解读 | 资讯搜索 | `/finskillshub/api/claw/news-search` |
| 股价、市值、PE、市盈率、财报、盈利、利润、收入、资金流向、基本面 | 数据查询 | `/finskillshub/api/claw/query` |

## API 调用

### 公共配置

```bash
API_BASE="https://mkapi2.dfcfs.com"
```

### 多 Key 轮换逻辑

1. 优先使用环境变量 `EASTMONEY_APIKEY`
2. 如果环境变量未设置，从 vault 读取多个 key
3. 按顺序尝试每个 key
4. 如果返回 `status != 0`（限流或错误），自动切换下一个 key
5. 所有 key 都失败后返回错误

### 1. 选股 API

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/stock-screen" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"keyword": "用户查询", "pageNo": 1, "pageSize": 20}'
```

适用场景：
- 条件选股："今日涨幅2%的股票"、"市盈率低于10的银行股"
- 板块成分股："半导体板块的成分股"
- 股票推荐："低估值高分红的股票推荐"

### 2. 资讯搜索 API

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/news-search" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"query": "用户查询"}'
```

适用场景：
- 个股资讯："格力电器最新研报"
- 板块新闻："新能源政策解读"
- 宏观分析："美联储加息对A股影响"

### 3. 数据查询 API

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/query" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"toolQuery": "用户查询"}'
```

适用场景：
- 行情数据："贵州茅台最新价"
- 财务指标："宁德时代市盈率"
- 公司信息："比亚迪主营业务"

## 错误处理

- 自动重试：当某个 key 被限流（返回非 status=0），自动切换到下一个 key
- 保持返回原始 JSON 格式，不做转换
