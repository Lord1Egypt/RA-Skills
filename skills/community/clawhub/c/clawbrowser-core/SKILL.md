---
name: clawbrowser
version: 1.0.0
description: 無頭瀏覽器自動化 CLI，ARIA ref 定位，自然語言操作，OpenClaw 集成
metadata:
  openclaw:
    requires:
      env: []
      bins: [node, npm, agent-browser]
tags:
  - browser
  - automation
  - openclaw
  - web-scraping
  - aria
---

# ClawBrowser

基於 agent-browser 的 OpenClaw 瀏覽器自動化工具，專為 AI Agent 設計。

## 核心特性

- ✅ **ARIA ref 定位** - 不用脆弱的 CSS 選擇器
- ✅ **自然語言指令** - 直接說「點擊提交按鈕」
- ✅ **無頭模式** - 只保留 DOM 渲染 + 無障礙樹快照
- ✅ **雙引擎切換** - agent-browser / traditional
- ✅ **100% 接口兼容** - 舊代碼零修改
- ✅ **網頁抓取** - extract_content/images/links

## 安裝依賴

```bash
# 安裝 agent-browser CLI
npm install -g agent-browser
agent-browser install  # 下載 Chrome
```

## 快速開始

```python
from browser_tool import BrowserTool

# 初始化
browser = BrowserTool(session_name="my_task")

# 打開網頁
browser.open("https://example.com")

# 獲取快照（包含 refs）
snapshot = browser.snapshot(interactive=True)

# 使用 ref 點擊
browser.click("@e1")

# 填寫表單
browser.fill("@e2", "test@example.com")

# 關閉
browser.close()
```

## 核心接口

### 基礎操作

| 方法 | 說明 |
|------|------|
| `open(url)` | 打開網頁 |
| `snapshot()` | 獲取無障礙樹快照 |
| `click(selector)` | 點擊元素 |
| `fill(selector, text)` | 填寫輸入框 |
| `type(selector, text)` | 輸入文本 |
| `press(key)` | 按鍵 |
| `wait(selector)` | 等待 |
| `close()` | 關閉 |

### 獲取信息

| 方法 | 說明 |
|------|------|
| `get_text(selector)` | 獲取元素文本 |
| `get_url()` | 獲取當前 URL |
| `get_title()` | 獲取頁面標題 |
| `get_attr(selector, attr)` | 獲取屬性 |

### 網頁抓取

| 方法 | 說明 |
|------|------|
| `extract_content()` | 提取頁面內容 |
| `extract_images()` | 提取圖片 |
| `extract_links()` | 提取鏈接 |

### 自然語言

```python
browser.natural_language_command("打開 github.com")
browser.natural_language_command("點擊 Sign In 按鈕")
browser.natural_language_command("填寫用戶名為 admin")
browser.natural_language_command("抓取頁面內容")
```

## 雙引擎切換

```python
# 全局切換
set_global_engine("agent-browser")  # 或 "traditional"

# 實例級切換
browser_ab = BrowserTool(engine="agent-browser")
browser_trad = BrowserTool(engine="traditional")
```

## 緩存配置

```python
from browser_tool import GLOBAL_CONFIG

# 啟用緩存
GLOBAL_CONFIG["cache_enabled"] = True

# 設置 TTL
GLOBAL_CONFIG["cache_ttl_seconds"] = 300
```

## 適用場景

- ✅ AI Agent 瀏覽器自動化
- ✅ 網頁抓取（微信文章、新聞、博客）
- ✅ 測試自動化
- ✅ 數據采集
- ✅ RPA 流程

## 限制條件

- ❌ 需要 Chrome/Chromium
- ❌ 動態內容需要重新快照
- ❌ Canvas/WebGL 不支持

## 文件結構

```
clawbrowser-skill/
├── SKILL.md              # 本文件
├── browser_tool_py36.py  # 核心工具（Python 3.6 兼容）
├── web_scraper.py        # 網頁抓取工具
└── README.md             # 補充說明
```

## 開發者

**作者**: RedOpenClaw  
**完成日期**: 2026.04.02  
**簽名**: 🦞 RedOpenClaw - 生活太快⚡️...老逼快跑💨...

## 參考資源

- agent-browser 官方文檔：https://agent-browser.dev
- OpenClaw 文檔：https://docs.openclaw.ai
- ClawHub 文檔：https://github.com/openclaw/clawhub
