# CDP Controller 使用示例 (Puppeteer)

## 快速开始

获取 WebSocket URL:
```bash
curl -s http://localhost:9222/json/version | grep -o '"webSocketDebuggerUrl":"[^"]*"' | cut -d'"' -f4
```

或访问: http://localhost:9222/json/version

## 示例 1: 淘宝搜索商品价格

**taobao-search.json:**
```json
[
  {
    "type": "navigate",
    "url": "https://www.taobao.com"
  },
  {
    "type": "wait",
    "seconds": 2
  },
  {
    "type": "fill",
    "selector": "#q",
    "text": "iPhone"
  },
  {
    "type": "press",
    "key": "Enter"
  },
  {
    "type": "wait",
    "seconds": 5
  },
  {
    "type": "evaluate",
    "script": "Array.from(document.querySelectorAll('.item, [class*=\"Item\"]')).slice(0, 10).map(item => ({ title: item.querySelector('.title, [class*=\"title\"]')?.textContent.trim().substring(0, 80), price: item.querySelector('.price, [class*=\"price\"]')?.textContent.trim() }))"
  }
]
```

执行:
```bash
WS_URL="ws://127.0.0.1:9222/devtools/browser/YOUR-BROWSER-ID"
node scripts/cdp_controller.js --ws "$WS_URL" --commands taobao-search.json
```

## 示例 2: ChatGPT 提问

```json
[
  {
    "type": "navigate",
    "url": "https://chat.openai.com"
  },
  {
    "type": "wait_for_selector",
    "selector": "textarea",
    "timeout": 10000
  },
  {
    "type": "type",
    "selector": "textarea",
    "text": "什么是人工智能?"
  },
  {
    "type": "press",
    "key": "Enter"
  },
  {
    "type": "wait",
    "seconds": 5
  },
  {
    "type": "get_text",
    "selector": "[data-message-author-role='assistant']:last-of-type"
  }
]
```

## 常用选择器

### 淘宝
- 搜索框: `#q`
- 商品列表: `.item`
- 商品标题: `.title`
- 商品价格: `.price`

### ChatGPT
- 输入框: `textarea[placeholder*="Message"]` 或 `textarea`
- 最新回复: `[data-message-author-role='assistant']:last-of-type`
- 所有对话: `.group`

### 通用技巧
- 使用浏览器开发者工具(F12)检查元素
- 优先使用 id 选择器(`#id`)
- 其次使用 class 选择器(`.class`)
- 必要时使用属性选择器(`[attr='value']`)

## 网络拦截

拦截特定 API 响应:

```json
{
  "type": "start_intercept",
  "url_pattern": "*graphql*"
}
```

获取拦截的数据:

```json
{
  "type": "get_intercepted"
}
```

## 截图

```json
{
  "type": "screenshot",
  "path": "/path/to/screenshot.png",
  "full_page": true
}
```

## JavaScript 执行

获取页面信息:

```json
{
  "type": "evaluate",
  "script": "document.title"
}
```

提取数据:

```json
{
  "type": "evaluate",
  "script": "Array.from(document.querySelectorAll('.item')).map(el => el.textContent)"
}
```
