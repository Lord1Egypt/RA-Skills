---
name: bing-search
description: "免费网页搜索，使用 Bing + Jina.ai 提取内容摘要。无需 API Key，直接可用。适用于快速获取搜索结果和网页内容。"
---

# Bing Search Skill

免费网页搜索方案，基于 Bing 搜索 + Jina.ai 内容提取。

## 特性

- ✅ **完全免费** — 无需 API Key
- 🌐 **Bing 搜索** — 全球搜索结果
- 📄 **内容摘要** — Jina.ai 自动提取页面核心内容
- ⚡ **快速响应** — 通常 1 秒内完成

## 使用方法

### 命令行

```bash
./scripts/bing_search.sh '<json>'
```

**示例：**
```bash
# 基本搜索
./scripts/bing_search.sh '{"query": "Python 教程"}'

# 指定结果数量
./scripts/bing_search.sh '{"query": "AI news", "max_results": 5}'

# 中文搜索
./scripts/bing_search.sh '{"query": "人工智能 最新消息", "max_results": 3}'
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | string | 必填 | 搜索关键词 |
| `max_results` | number | 5 | 返回结果数量 (1-10) |

## 输出格式

```json
{
  "query": "搜索关键词",
  "results": [
    {
      "url": "https://example.com",
      "title": "页面标题",
      "content": "页面内容摘要...",
      "score": 0.95
    }
  ],
  "response_time": 0.75
}
```

## 技术原理

1. **Bing 搜索** — 获取搜索结果列表
2. **Jina.ai 提取** — `https://r.jina.ai/http://bing.com/search?q=关键词`
3. **结果解析** — 提取标题、URL、内容摘要

## 限制

- 免费服务，有请求频率限制
- 不适合大规模自动化搜索
- 结果质量依赖 Bing 和 Jina.ai

## 故障排除

**问题：** 返回空结果
**解决：** 检查网络连接，稍后重试

**问题：** 请求频繁被拒
**解决：** 等待几秒后再试，或减少请求频率

---

**来源：** agents-skills-personal → openclaw-workspace