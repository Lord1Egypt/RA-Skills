---
name: crawl4ai-docker-skill
description: "Dockerized web crawling and scraping service with REST API. Docker化网页爬虫服务 | Web crawler, web scraper, REST API service. Intelligent content extraction with LLM optimization. 智能内容提取 | Docker部署，REST API调用"
version: 1.0.0
author: OpenClaw Assistant
license: MIT-0
repository: https://github.com/unclecode/crawl4ai
homepage: https://docs.crawl4ai.com/
tags:
  - web-scraping
  - web-crawling
  - docker
  - rest-api
  - crawler
  - scraper
  - markdown
  - llm
  - content-extraction
  - 爬虫
  - 爬取
  - 网页抓取
  - docker部署
requires:
  services:
    - crawl4ai-docker
---

# Crawl4AI Docker Skill - Web Crawler & Scraper Service

**Dockerized Web Crawling 网页爬虫服务 | REST API 网页爬取 | LLM 智能提取**

基于 Docker 部署的 Crawl4AI 网页爬虫服务，提供完整的 REST API 接口，支持智能内容提取和 LLM 优化输出。

## 🚀 核心功能 | Core Features

- 🐳 **Docker 部署** - 容器化服务，端口 11235
- 🔌 **REST API** - 完整的 HTTP 接口
- 🤖 **LLM 智能提取** - 支持多种 LLM 提供商
- 📊 **实时监控** - 内置监控面板和 API
- ⚡ **高性能** - 异步处理，支持并发请求

---

## 📋 快速开始 | Quick Start

### 前提条件 | Prerequisites

确保 Docker Compose 服务正在运行：

```bash
# 检查服务状态
docker compose ps

# 健康检查
curl http://localhost:11235/health

# 访问监控面板
open http://localhost:11235/dashboard
```

---

## 🔌 REST API 使用指南

### 基础网页抓取 | Basic Web Crawling

#### 简单 Markdown 提取
```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "extraction_strategy": "markdown"
  }'
```

#### 带浏览器配置
```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "extraction_strategy": "markdown",
    "browser_config": {
      "headless": true,
      "viewport_width": 1280,
      "viewport_height": 720
    }
  }'
```

### LLM 智能提取 | LLM Smart Extraction

#### 内容总结
```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "extraction_strategy": {
      "type": "llm",
      "provider": "openrouter/free",
      "instruction": "总结网页的主要内容",
      "max_tokens": 1000
    }
  }'
```

#### 结构化数据提取
```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com/products"],
    "extraction_strategy": {
      "type": "llm",
      "provider": "openrouter/free",
      "instruction": "提取所有产品名称、价格和描述，返回 JSON 格式",
      "max_tokens": 1500,
      "temperature": 0.1
    }
  }'
```

### 高级功能 | Advanced Features

#### 网页截图
```bash
curl -X POST "http://localhost:11235/screenshot" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "full_page": true,
      "quality": 80
    }
  }'
```

#### PDF 生成
```bash
curl -X POST "http://localhost:11235/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

---

## 📊 API 端点参考 | API Endpoints Reference

### 核心端点 | Core Endpoints

| 端点 | 方法 | 用途 |
|------|------|------|
| `POST /crawl` | POST | 网页抓取和内容提取 |
| `GET /health` | GET | 服务健康检查 |
| `GET /dashboard` | GET | 监控面板 |

### 监控端点 | Monitoring Endpoints

| 端点 | 方法 | 用途 |
|------|------|------|
| `GET /monitor/health` | GET | 系统健康状态 |
| `GET /monitor/browsers` | GET | 浏览器池状态 |
| `GET /monitor/requests` | GET | 请求统计 |

### 工具端点 | Utility Endpoints

| 端点 | 方法 | 用途 |
|------|------|------|
| `POST /screenshot` | POST | 网页截图 |
| `POST /pdf` | POST | PDF 生成 |
| `POST /execute_js` | POST | JavaScript 执行 |

---

## 🎯 使用场景 | Use Cases

### 场景 1：文档网站爬取 | Documentation Site Crawling

```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://docs.openclaw.ai/zh-CN"],
    "extraction_strategy": "markdown"
  }'
```

### 场景 2：新闻文章提取 | News Article Extraction

```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://news-site.com/article"],
    "extraction_strategy": {
      "type": "llm",
      "provider": "openrouter/free",
      "instruction": "提取文章标题、作者、发布时间和主要内容",
      "max_tokens": 1500
    }
  }'
```

### 场景 3：产品信息抓取 | Product Information Scraping

```bash
curl -X POST "http://localhost:11235/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://ecommerce-site.com/products"],
    "extraction_strategy": {
      "type": "llm",
      "provider": "openrouter/free",
      "instruction": "提取所有产品的名称、价格、描述和图片链接",
      "max_tokens": 2000
    }
  }'
```

---

## ⚙️ 配置说明 | Configuration

### LLM 提供商配置 | LLM Provider Configuration

创建 `.llm.env` 文件：

```bash
# OpenRouter 配置
OPENROUTER_API_KEY=your-api-key
LLM_PROVIDER=openrouter/free
LLM_MAX_TOKENS=2000
LLM_TEMPERATURE=0.7

# 或使用其他提供商
# OPENAI_API_KEY=sk-your-key
# OPENAI_BASE_URL=https://your-custom-api.com/v1
# LLM_PROVIDER=openai/gpt-4o-mini
```

### 浏览器配置 | Browser Configuration

```json
{
  "browser_config": {
    "headless": true,
    "viewport_width": 1280,
    "viewport_height": 720,
    "user_agent": "Mozilla/5.0..."
  }
}
```

---

## 📈 响应格式 | Response Format

### 成功响应 | Success Response

```json
{
  "success": true,
  "results": [
    {
      "url": "https://example.com",
      "markdown": "# 提取的 Markdown 内容...",
      "metadata": {
        "title": "网页标题",
        "description": "网页描述",
        "url": "https://example.com"
      },
      "extracted_content": {
        "summary": "LLM 提取的内容..."
      }
    }
  ]
}
```

### 错误响应 | Error Response

```json
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE"
}
```

---

## 🔧 故障排除 | Troubleshooting

### 常见问题 | Common Issues

#### 1. 服务未启动
```bash
# 检查容器状态
docker compose ps

# 查看日志
docker compose logs crawl4ai

# 重启服务
docker compose restart crawl4ai
```

#### 2. LLM 提取失败
- 检查 `.llm.env` 配置
- 验证 API 密钥
- 测试不同的 LLM 提供商

#### 3. 网络连接问题
```bash
# 测试网络连接
curl -I https://example.com

# 检查代理配置
env | grep -i proxy
```

### 监控和调试 | Monitoring & Debugging

```bash
# 访问监控面板
open http://localhost:11235/dashboard

# 查看系统健康
curl http://localhost:11235/monitor/health

# 查看浏览器池状态
curl http://localhost:11235/monitor/browsers
```

---

## 🔗 相关链接 | Links

- 📚 [官方文档](https://docs.crawl4ai.com/)
- 💻 [GitHub 仓库](https://github.com/unclecode/crawl4ai)
- 🐳 [Docker Hub](https://hub.docker.com/r/unclecode/crawl4ai)

---

## 🎉 为什么选择 Docker 版本？

✅ **容器化部署** - 一键启动，环境隔离  
✅ **REST API** - 标准 HTTP 接口，易于集成  
✅ **实时监控** - 内置监控面板和 API  
✅ **资源管理** - 自动浏览器池管理  
✅ **生产就绪** - 企业级稳定性和性能  

**立即开始使用 Docker 化的 Crawl4AI 服务！** 🚀