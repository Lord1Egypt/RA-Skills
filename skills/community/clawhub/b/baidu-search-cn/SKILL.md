---
name: 百度搜索
version: 1.0.1
description: 通过百度 AI 搜索 API 进行网页搜索，获取实时信息和搜索结果。
homepage: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/2m0u2qdmd
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      bins:
        - uv
      env:
        - BAIDU_API_KEY
    primaryEnv: BAIDU_API_KEY
    install:
      - id: brew
        kind: brew
        formula: uv
        bins:
          - uv
        label: Install uv via Homebrew
---

# 🔍 百度搜索

*Search the web with Baidu AI*

通过百度 AI 搜索 API 进行网页搜索，获取中文互联网的实时信息。

## Setup

```bash
cd {baseDir}
echo "BAIDU_API_KEY=your-api-key" > .env
uv venv && uv pip install -e ".[dev]"
uv run --env-file .env uvicorn baidu_search.main:app --host 127.0.0.1 --port 8001
```

需要在 `.env` 或环境变量中设置 `BAIDU_API_KEY`。

## 获取 API Key

1. 访问 [百度智能云控制台](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
2. 创建应用获取 API Key

## Quick Start

1. **检查服务:** `curl http://127.0.0.1:8001/ping`

2. **搜索网页:**
```bash
curl -X POST http://127.0.0.1:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "北京有哪些旅游景区",
    "top_k": 10
  }'
```

3. **带时间过滤的搜索:**
```bash
curl -X POST http://127.0.0.1:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "最新科技新闻",
    "top_k": 5,
    "recency_filter": "week"
  }'
```

4. **限定网站搜索:**
```bash
curl -X POST http://127.0.0.1:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "天气预报",
    "top_k": 5,
    "site_filter": ["www.weather.com.cn"]
  }'
```

## API 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | string | 必填 | 搜索关键词 |
| `top_k` | int | 10 | 返回结果数量 (1-20) |
| `recency_filter` | string | null | 时间过滤: `day`, `week`, `month`, `year` |
| `site_filter` | list | null | 限定搜索的网站列表 |

## Response Format

```json
{
  "results": [
    {
      "title": "北京十大必去景点",
      "url": "https://example.com/beijing-attractions",
      "snippet": "北京作为中国的首都，拥有众多著名景点...",
      "site_name": "旅游网"
    }
  ],
  "total": 10
}
```

## Conversation Flow

1. 用户提问需要搜索的内容
2. 判断是否需要时间过滤（如"最新"、"今天"等）
3. 调用搜索 API 获取结果
4. 整理并展示相关信息
5. 可根据需要深入查看某个结果

## 使用场景

- 查询实时信息（新闻、天气、股票等）
- 搜索中文互联网内容
- 获取特定网站的信息
- 时效性要求高的查询
