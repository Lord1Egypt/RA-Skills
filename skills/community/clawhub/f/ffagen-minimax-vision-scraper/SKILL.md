---
name: ffagen__minimax-vision-scraper
description: Playwright截图 + MiniMax图像理解的高级网页抓取skill。绕过反爬虫，直接用AI理解截图内容。
version: 1.0.0
author: ffagen
credits: |
  技术参考：
  - playwright-scraper-skill by Simon Chan (https://clawhub.ai/skills/scraper) - 反爬虫技术
  - minimax-coding-plan-mcp by MiniMax - 图像理解API
---

# MiniMax Vision Scraper

Playwright 截图 + MiniMax 图像理解，绕过反爬虫，直接用 AI 提取页面内容。

---

## 核心优势

| 对比项 | 传统抓取 | Vision Scraper |
|--------|----------|----------------|
| 反爬虫 | ❌ 易被屏蔽 | ✅ 截图绕过检测 |
| JS渲染 | ⚠️ 复杂 | ✅ 截图即完整 |
| 内容理解 | ❌ 需解析HTML | ✅ AI直接理解 |
| 动态内容 | ❌ 难抓 | ✅ 截图即所见 |

---

## 工作流程

```
URL → Playwright截图(Chrome) → MiniMax VLM图像理解 → AI分析结果
```

---

## 安装

```bash
cd ~/.openclaw/workspace/skills/ffagen__minimax-vision-scraper
npm install playwright
# 无需安装 chromium，直接使用系统已装的 Google Chrome
```

---

## 使用方式

### 直接调用
```bash
node scripts/screenshot.js <URL> [prompt]

# 示例
node scripts/screenshot.js "https://news.sina.com.cn" "提取今日头条新闻"
node scripts/screenshot.js "https://finance.sina.com.cn" "提取股票行情数据"
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| WAIT_TIME | 5000 | 等待时间(ms) |
| HEADLESS | true | 是否无头模式 |
| SCREENSHOT_PATH | /tmp/screenshot-*.png | 截图保存路径 |
| MINIMAX_API_KEY | (内置) | MiniMax API Key |
| MINIMAX_API_HOST | api.minimaxi.com | API地址 |

### 在OpenClaw中调用

```
用 ffagen__minimax-vision-scraper 抓取 https://example.com，分析页面内容
```

---

## 反爬虫技术（致敬 playwright-scraper-skill）

✅ 隐藏 `navigator.webdriver`  
✅ 真实 iPhone User-Agent  
✅ 移动端视口 (375x812)  
✅ 隐藏 Chrome 自动化特征  
✅ 模拟 permissions.query  
✅ Cloudflare 检测 + 额外等待  

---

## 示例

**抓取财经新闻：**
```bash
node scripts/screenshot.js "https://finance.sina.com.cn" "提取所有财经新闻标题和摘要"
```

**抓取股票数据：**
```bash
node scripts/screenshot.js "https://stock.finance.sina.com.cn" "提取大盘指数和涨跌数据"
```

**抓取商品信息：**
```bash
node scripts/screenshot.js "https://item.jd.com/100000.html" "提取商品名称、价格、评价"
```

---

## 技术说明

- **截图引擎**：使用系统已装的 Google Chrome（无需额外下载）
- **图像理解**：MiniMax VLM API (`/v1/coding_plan/vlm`)
- **反爬策略**：Playwright Stealth 模式，隐藏自动化特征
