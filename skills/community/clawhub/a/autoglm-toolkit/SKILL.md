---
name: autoglm-toolkit
version: 1.0.0
description: >
  AutoGLM AI agent toolkit powered by Zhipu AI. Includes browser automation, 
  deep research, web search, image generation, image search, and web page 
  content extraction. Perfect for Chinese internet tasks.
  Triggers: "浏览器自动化", "深度研究", "网络搜索", "AI生图", "搜图", 
  "网页抓取", "AutoGLM", "智谱".
tags: [autoglm, zhipu, browser, automation, research, search, image, chinese, ai-agent]
env:
  AUTOGLM_TOKEN: "AutoGLM API token (obtained from local service or manual config)"
---

# AutoGLM Toolkit (智谱 AI 工具箱)

A comprehensive AI agent toolkit powered by [Zhipu AI](https://zhipuai.cn). Includes 6 capabilities:

1. **🌐 Browser Automation** — Autonomous browser agent for any web task
2. **🔍 Deep Research** — Multi-round search + deep reading for structured reports
3. **🔎 Web Search** — Quick web search with concise results
4. **🎨 Image Generation** — Text-to-image generation
5. **🖼️ Image Search** — Search for stock images by keywords
6. **📄 Web Page Reader** — Extract full-text content from web pages

---

## Authentication

All API calls share the same authentication mechanism.

### Token
Obtain via local AutoGLM service or manual configuration.

### Signing Headers (required for all requests)
Every request must include these headers:

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer <token>` |
| `X-Auth-Appid` | Your app ID |
| `X-Auth-TimeStamp` | Current Unix timestamp (seconds) |
| `X-Auth-Sign` | MD5(`appid` + `"&"` + `timestamp` + `"&"` + `secret`) |

```python
import hashlib, time

def make_headers(token, app_id, secret):
    ts = str(int(time.time()))
    sign = hashlib.md5(f"{app_id}&{ts}&{secret}".encode()).hexdigest()
    return {
        'Authorization': f'Bearer {token}',
        'X-Auth-Appid': app_id,
        'X-Auth-TimeStamp': ts,
        'X-Auth-Sign': sign,
        'Content-Type': 'application/json'
    }
```

---

## 1. Browser Automation Agent

Autonomous browser automation agent that can perform any web task.

### Capabilities
- Open web pages, search engines (Baidu/Google/Bing)
- Browse social media (Weibo, Xiaohongshu, Zhihu, Douyin, Bilibili)
- Like, comment, repost, bookmark posts
- Login to websites, fill forms
- Take screenshots, scrape web content
- Online shopping comparisons
- Operate online documents (Feishu Docs, Tencent Docs)

### Usage
```bash
# Delegate entire task to autonomous browser subagent
browser_subagent(task="<task_description>", start_url="<url>")
```

### Key Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `task` | ✅ | Task description (use user's exact words) |
| `start_url` | Optional | Starting URL for the task |
| `session_id` | Optional | Resume previous browser session |
| `auto_approve` | Optional | Auto-approve sensitive operations (default: false) |

### Session Management
- Sessions persist in session pool with 12-hour TTL
- Same-site tasks reuse existing sessions
- Different-site tasks open new browser tabs
- Login/captcha always requires manual user interaction

### Important Rules
1. One task at a time (no concurrent browser tasks)
2. Always show screenshots in results
3. Default to 5 items when user doesn't specify quantity
4. Separate browser operations from non-browser operations (like saving to Excel)

---

## 2. Deep Research (深度调研)

Conduct in-depth research on any topic with structured output.

### Process
1. **Decompose**: Break topic into 1-2 key search directions
2. **Search**: 1-2 rounds of web search (controlled quantity)
3. **Deep Read**: Open 1-3 important pages for full-text analysis
4. **Report**: Generate structured research report

### API Endpoints
```python
# Web Search
POST https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search
Body: {"queries": [{"query": "<search_term>"}]}
# Returns: data.results[].webPages.value[] → name / url / snippet

# Open Link (Deep Read)
POST https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link
Body: {"url": "<page_url>"}
# Returns: data.text → full page content
```

### Execution Constraints
- `web-search` max 2 calls
- `open-link` max 3 calls
- Show intermediate results after each call
- Stop when sufficient information is gathered

### Output Format
```markdown
# [Topic] 深度调研报告

## 中间发现
## 概述
## 背景
## 现状分析
## 典型案例 / 代表性观点
## 发展趋势
## 总结
## 参考来源
```

---

## 3. Web Search (网络搜索)

Quick web search with structured results.

### API
```python
POST https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search
Body: {"queries": [{"query": "<search_term>"}]}
```

### Response
```json
{
  "code": 0,
  "data": {
    "results": [{
      "webPages": {
        "value": [
          {"name": "Page Title", "url": "URL", "snippet": "Summary"}
        ]
      }
    }]
  }
}
```

### Output Requirements
1. Summarize search results based on snippets
2. Append reference sources with links

---

## 4. Image Generation (AI 生图)

Generate images from text descriptions.

### API
```python
POST https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image
Body: {"text": "<image_description>"}
```

### Response
```json
{
  "code": 0,
  "data": {"image_url": "https://..."}
}
```

Display result as: `![Generated Image](image_url)`

---

## 5. Image Search (搜图)

Search for images by keywords.

### API
```python
POST https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/search-image
Body: {"query": "<search_keywords>"}
```

### Response
```json
{
  "code": 0,
  "data": {
    "results": [{
      "original_url": "image_url",
      "caption": "description",
      "source": "source",
      "original_width": 1267,
      "original_height": 845
    }],
    "count": 4
  }
}
```

---

## 6. Web Page Reader (网页阅读)

Extract full-text content from a web page URL.

### API
```python
POST https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link
Body: {"url": "<page_url>"}
```

### Response
```json
{
  "code": 0,
  "data": {"text": "Full page content..."}
}
```

### Output Requirements
1. Extract `data.text` as page content
2. Summarize or display based on user's goal
3. Never fabricate content on API error

---

## API Quick Reference

| Capability | Endpoint | Method |
|------------|----------|--------|
| Web Search | `/skills/web-search` | POST |
| Open Link | `/skills/open-link` | POST |
| Generate Image | `/skills/generate-image` | POST |
| Search Image | `/skills/search-image` | POST |

Base URL: `https://autoglm-api.zhipuai.cn/agentdr/v1/assistant`

---

## Notes

- All APIs use the same authentication signature mechanism
- Python 3 with standard library only (no extra dependencies)
- Particularly effective for Chinese internet content
- Browser agent requires Chromium-based browser with AutoClaw extension
