# DuckDuckGo Search & Fetch

使用 DuckDuckGo 进行网页搜索和内容抓取，无需 API Key，完全免费。

## 功能特性

- 🔍 **网页搜索** - 支持文本搜索，返回标题、URL 和摘要
- 📄 **网页抓取** - 提取网页可读内容，支持 Markdown/Text 格式
- 🔐 **无需 API Key** - 直接使用 DuckDuckGo 服务
- ⚡ **轻量级** - 纯 Python 实现，依赖少

## 安装

### 1. 安装依赖

```bash
pip3 install duckduckgo-search
```

### 2. 在 OpenClaw 中使用

```
可通过 OpenClaw skills 或直接调用脚本使用
```

## 使用方法

### 命令行

#### 搜索

```bash
python3 scripts/ddg_search.py "搜索关键词" [--max-results 10]
```

**参数说明：**
- `query` - 搜索关键词
- `--max-results` - 最大结果数（默认 10）

**示例：**
```bash
python3 scripts/ddg_search.py "OpenClaw AI agent"
python3 scripts/ddg_search.py "Python tips" --max-results 15
```

#### 抓取网页

```bash
python3 scripts/ddg_fetch.py "https://example.com" [--timeout 30] [--format markdown]
```

**参数说明：**
- `url` - 要抓取的网页 URL
- `--timeout` - 超时时间（秒，默认 30）
- `--format` - 输出格式（markdown/text，默认 markdown）

**示例：**
```bash
python3 scripts/ddg_fetch.py "https://openclaw.ai"
python3 scripts/ddg_fetch.py "https://example.com" --timeout 15 --format text
```

## 输出格式

### 搜索结果 (JSON)

```json
{
  "query": "search query",
  "count": 10,
  "results": [
    {
      "title": "Result title",
      "url": "https://example.com",
      "snippet": "Description snippet"
    }
  ]
}
```

### 抓取结果 (JSON)

```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "text": "Extracted readable content...",
  "description": "Meta description",
  "status_code": 200,
  "error": null
}
```

## OpenClaw 集成

### 作为 Skill 使用

在 OpenClaw 中可通过 skill 触发词使用：
- "search for xxx"
- "look up xxx"
- "find information about xxx"
- "fetch url xxx"
- "get page content xxx"

### 编程调用

```python
import json
import subprocess

# 搜索
result = subprocess.run(
    ["python3", "scripts/ddg_search.py", "your query"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

# 抓取网页
result = subprocess.run(
    ["python3", "scripts/ddg_fetch.py", "https://example.com"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
```

## 许可证

MIT License
