---
name: firecrawl-local-search
description: 抓取网站数据的本地 Firecrawl 服务。使用本地 API (http://192.168.1.2:3002/) 进行网页抓取、数据提取和站内搜索。
---

# Firecrawl 本地搜索技能

## 快速开始

使用本地 Firecrawl 服务抓取网站数据。

### API 配置

- **基础 URL**: `http://192.168.1.2:3002/`
- **协议**: HTTP (本地服务)
- **超时**: 30 秒

## 主要功能

### 1. 网页抓取 (Scrape)

```bash
curl -X POST "http://192.168.1.2:3002/v1/scrape" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

### 2. 网站地图 (Map)

```bash
curl -X POST "http://192.168.1.2:3002/v1/map" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 3. 内容搜索 (Search)

```bash
python3 scripts/firecrawl_search.py "关键词" --site https://example.com
```

## 使用脚本

- `scripts/firecrawl_scrape.py` - 网页抓取（无需外部依赖）
- `scripts/firecrawl_map.py` - 网站地图
- `scripts/firecrawl_search.py` - 内容搜索

## 依赖说明

✅ **无需安装任何依赖** - 使用 Python 标准库 `urllib.request`

## 注意事项

1. **本地服务**: API 运行在本地网络，确保网络连接正常
2. **超时设置**: 默认 30 秒超时
3. **速率限制**: 根据服务器配置调整请求频率
4. **网络要求**: 需要访问 `http://192.168.1.2:3002/`
