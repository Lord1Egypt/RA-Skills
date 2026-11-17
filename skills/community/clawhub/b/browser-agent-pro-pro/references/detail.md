# 详细参考 - browser-agent-pro-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (text)

```text
┌─────────────────────────────────────────────────────────────────┐
│             浏览器代理专业版 (BROWSER AGENT PRO)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  反检测引擎   │  │  多标签管理   │  │  代理与网络   │           │
│  │  Anti-Detect │  │  Multi-Tab   │  │  Proxy & Net │           │
│  │  ✅ 专业版    │  │  ✅ 专业版    │  │  ✅ 专业版    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  动态抓取     │  ← 分页/无限滚动/SPA            │
│                  │  Dynamic     │    ✅ 专业版                    │
│                  └──────────────┘                                │
│                          │                                       │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  登录态管理   │  ← Cookie/Session持久化         │
│                  │  Auth State  │    ✅ 专业版                    │
│                  └──────────────┘                                │
│                          │                                       │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  UI测试框架   │  ← 回归测试/截图对比            │
│                  │  Test Suite  │    ✅ 专业版                    │
│                  └──────────────┘                                │
│                          │                                       │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  性能监控     │  ← 瓶颈分析/瀑布图              │
│                  │  Perf Monitor│    ✅ 专业版                    │
│                  └──────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 代码示例 (json)

```json
// ~/workspace/browser/config.json
{
  "edition": "pro",
  "anti_detect": {
    "enabled": true,
    "user_agents": ["UA1", "UA2", "UA3", "UA4", "UA5"],
    "mouse_simulation": true,
    "request_delay_range": [2, 5],
    "fingerprint_randomization": true
  },
  "proxy": {
    "enabled": false,
    "type": "http",
    "host": "127.0.0.1",
    "port": 7890
  },
  "auth": {
    "session_persistence": true,
    "cookie_storage": "~/workspace/browser/cookies/"
  },
  "scraping": {
    "pagination_support": true,
    "infinite_scroll": true,
    "dynamic_content_wait": 3,
    "max_records": 10000
  }
}
```

## 代码示例 (json)

```json
{
  "anti_detect": {
    "user_agent_rotation": {
      "enabled": true,
      "pool": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36..."
      ],
      "rotate_per_request": true
    },
    "fingerprint": {
      "canvas_noise": true,
      "webgl_randomization": true,
      "audio_context_spoofing": true,
      "font_fingerprint_masking": true
    },
    "behavior": {
      "mouse_trajectory": "human_like",
      "typing_speed_range": [50, 150],
      "scroll_speed_range": [200, 800],
      "random_delay_range": [1, 4]
    },
    "stealth_plugins": ["stealth.min.js"]
  }
}
```

## 代码示例 (json)

```json
{
  "proxy": {
    "type": "http|https|socks5",
    "host": "proxy.example.com",
    "port": 8080,
    "username": "env:PROXY_USER",
    "password": "env:PROXY_PASS",
    "rotation": {
      "enabled": true,
      "pool": [
        {"host": "proxy1.example.com", "port": 8080},
        {"host": "proxy2.example.com", "port": 8080}
      ],
      "rotate_per_n_requests": 10
    }
  },
  "network": {
    "geolocation": "us",
    "timezone": "America/New_York",
    "locale": "en-US",
    "bandwidth_throttling": "3g"
  }
}
```

## 代码示例 (json)

```json
// ~/workspace/browser/tests/homepage.json
{
  "name": "首页回归测试",
  "url": "https://example.com",
  "steps": [
    {"action": "open", "url": "https://example.com"},
    {"action": "wait", "selector": "#hero"},
    {"action": "screenshot", "name": "baseline"},
    {"action": "click", "selector": "#nav-products"},
    {"action": "wait", "selector": ".product-list"},
    {"action": "screenshot", "name": "products_page"}
  ],
  "assertions": [
    {"type": "visual_diff", "threshold": 0.05},
    {"type": "element_exists", "selector": "#hero"},
    {"type": "response_time", "max_ms": 3000}
  ]
}
```

## 代码示例 (json)

```json
{
  "performance_metrics": {
    "page_load_time_ms": 2340,
    "dom_content_loaded_ms": 1200,
    "first_contentful_paint_ms": 800,
    "largest_contentful_paint_ms": 1800,
    "cumulative_layout_shift": 0.02,
    "total_blocking_time_ms": 150,
    "network_requests": 45,
    "total_transfer_size_kb": 1234,
    "bottlenecks": [
      {"url": "large-image.jpg", "type": "image", "size_kb": 500, "suggestion": "压缩图片"},
      {"url": "analytics.js", "type": "script", "load_ms": 800, "suggestion": "延迟加载"}
    ]
  }
}
```

## 架构总览
```text
┌─────────────────────────────────────────────────────────────────┐
│             浏览器代理专业版 (BROWSER AGENT PRO)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  反检测引擎   │  │  多标签管理   │  │  代理与网络   │           │
│  │  Anti-Detect │  │  Multi-Tab   │  │  Proxy & Net │           │
│  │  ✅ 专业版    │  │  ✅ 专业版    │  │  ✅ 专业版    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  动态抓取     │  ← 分页/无限滚动/SPA            │
│                  │  Dynamic     │    ✅ 专业版                    │
│                  └──────────────┘                                │
│                          │                                       │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  登录态管理   │  ← Cookie/Session持久化         │
│                  │  Auth State  │    ✅ 专业版                    │
│                  └──────────────┘                                │
│                          │                                       │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  UI测试框架   │  ← 回归测试/截图对比            │
│                  │  Test Suite  │    ✅ 专业版                    │
│                  └──────────────┘                                │
│                          │                                       │
│                          ▼                                       │
│                  ┌──────────────┐                                │
│                  │  性能监控     │  ← 瓶颈分析/瀑布图              │
│                  │  Perf Monitor│    ✅ 专业版                    │
│                  └──────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```



### 功能七：UI回归测试框架
```json
// ~/workspace/browser/tests/homepage.json
{
  "name": "首页回归测试",
  "url": "https://example.com",
  "steps": [
    {"action": "open", "url": "https://example.com"},
    {"action": "wait", "selector": "#hero"},
    {"action": "screenshot", "name": "baseline"},
    {"action": "click", "selector": "#nav-products"},
    {"action": "wait", "selector": ".product-list"},
    {"action": "screenshot", "name": "products_page"}
  ],
  "assertions": [
    {"type": "visual_diff", "threshold": 0.05},
    {"type": "element_exists", "selector": "#hero"},
    {"type": "response_time", "max_ms": 3000}
  ]
}
```

```bash
agent browser test run --suite homepage.json

agent browser test report --last

agent browser test baseline --update homepage.json
```



### 功能八：性能监控
```json
{
  "performance_metrics": {
    "page_load_time_ms": 2340,
    "dom_content_loaded_ms": 1200,
    "first_contentful_paint_ms": 800,
    "largest_contentful_paint_ms": 1800,
    "cumulative_layout_shift": 0.02,
    "total_blocking_time_ms": 150,
    "network_requests": 45,
    "total_transfer_size_kb": 1234,
    "bottlenecks": [
      {"url": "large-image.jpg", "type": "image", "size_kb": 500, "suggestion": "压缩图片"},
      {"url": "analytics.js", "type": "script", "load_ms": 800, "suggestion": "延迟加载"}
    ]
  }
}
```



