---
name: stealth-scraper
description: 基于 Playwright 的反爬虫网页抓取技能。支持普通模式、隐身模式和批量模式。内置反检测技术（隐藏 webdriver、随机 UA、Canvas/WebGL 指纹防护）绕过常见反爬虫机制。使用场景：抓取网页内容、反爬虫抓取、批量采集、截图保存。触发关键词：scrape, 抓取, 爬虫, 反爬, stealth scrape, 采集网页, 批量抓取。
bins:
  - node
---

# Stealth Scraper

> 基于 Playwright 的反爬虫网页抓取技能，支持普通模式、隐身模式和批量模式。

## Description

强大的网页抓取工具，内置反检测技术，绕过常见反爬虫机制。纯手写反检测代码，不依赖任何第三方 stealth 插件。

**核心能力：**
- 🕵️ 隐身模式：隐藏 webdriver 指纹、随机 UA、随机延迟、禁用指纹追踪
- 📄 普通模式：快速抓取页面内容
- 📦 批量模式：并发抓取多个 URL，自动限速
- 🎯 精确提取：CSS 选择器定向抓取
- 📸 截图 & HTML 保存

## Configuration

```yaml
bins: ["node"]
```

## Setup

首次使用前需要安装依赖：

```bash
cd ~/.openclaw/workspace/skills/stealth-scraper
npm install
```

如果 Chromium 未自动安装，运行：

```bash
node scripts/setup.js
```

## Usage

### 普通模式（快速抓取）

```bash
node scripts/scraper-simple.js <URL> [options]
```

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--wait <ms>` | 页面加载后等待时间（毫秒） | 2000 |
| `--selector <css>` | CSS 选择器，只提取匹配元素的内容 | 无（提取全部） |

**示例：**
```bash
# 基本抓取
node scripts/scraper-simple.js https://example.com

# 等待 5 秒后提取
node scripts/scraper-simple.js https://example.com --wait 5000

# 只提取文章正文
node scripts/scraper-simple.js https://example.com --selector "article.content"
```

### 隐身模式（反爬虫）

```bash
node scripts/scraper-stealth.js <URL> [options]
```

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--wait <ms>` | 页面加载后等待时间（毫秒） | 2000 |
| `--selector <css>` | CSS 选择器精确提取 | 无 |
| `--proxy <url>` | 代理服务器地址 | 无 |
| `--screenshot <path>` | 保存截图到指定路径 | 无 |
| `--html <path>` | 保存完整 HTML 到指定路径 | 无 |
| `--cookie <json>` | 自定义 cookie（JSON 格式） | 无 |
| `--scroll` | 自动滚动页面加载懒加载内容 | false |

**示例：**
```bash
# 隐身抓取
node scripts/scraper-stealth.js https://example.com

# 使用代理 + 截图
node scripts/scraper-stealth.js https://example.com --proxy http://127.0.0.1:7890 --screenshot ./shot.png

# 自动滚动 + 保存 HTML
node scripts/scraper-stealth.js https://example.com --scroll --html ./page.html

# 带 cookie 访问
node scripts/scraper-stealth.js https://example.com --cookie '[{"name":"token","value":"abc123","domain":".example.com"}]'

# 精确提取 + 等待
node scripts/scraper-stealth.js https://example.com --selector "div.main" --wait 5000
```

### 批量模式

```bash
node scripts/scraper-batch.js [options] <URL1> <URL2> ...
# 或
node scripts/scraper-batch.js --file urls.txt [options]
```

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--file <path>` | URL 列表文件（每行一个 URL） | 无 |
| `--concurrency <n>` | 并发数 | 3 |
| `--stealth` | 使用隐身模式 | false |
| `--wait <ms>` | 每个页面的等待时间 | 2000 |
| `--selector <css>` | CSS 选择器 | 无 |
| `--output <path>` | 输出 JSON 文件路径 | stdout |

**示例：**
```bash
# 批量抓取多个 URL
node scripts/scraper-batch.js https://a.com https://b.com https://c.com

# 从文件读取 URL 列表，隐身模式
node scripts/scraper-batch.js --file urls.txt --stealth --concurrency 2

# 输出到文件
node scripts/scraper-batch.js --file urls.txt --output results.json
```

## Output Format

所有模式输出统一的 JSON 结构：

```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Example Domain",
  "content": "页面文本内容...",
  "links": [{"text": "More info", "href": "https://..."}],
  "images": [{"alt": "Logo", "src": "https://..."}],
  "metadata": {
    "description": "...",
    "keywords": "...",
    "author": "..."
  },
  "elapsedSeconds": 2.35
}
```

## Anti-Detection Features

| 技术 | 说明 |
|------|------|
| navigator.webdriver 隐藏 | 删除 webdriver 属性，伪装为真实浏览器 |
| User-Agent 轮换 | 10+ 真实 UA，涵盖 Chrome/Safari/Firefox，桌面+移动端 |
| 随机延迟 | 1-3 秒随机等待，模拟人类浏览行为 |
| 随机视口 | 随机分辨率，避免固定窗口指纹 |
| WebGL 指纹防护 | 注入噪声干扰 WebGL 指纹采集 |
| Canvas 指纹防护 | 对 Canvas 数据添加微小噪声 |
| 插件伪装 | 伪造 navigator.plugins 数组 |
| 语言伪装 | 伪造 navigator.languages |
| 硬件并发伪装 | 随机化 navigator.hardwareConcurrency |

## Notes

- 纯手写反检测代码，不使用任何第三方 stealth 插件（如 puppeteer-extra-plugin-stealth），避免被反检测系统识别
- 使用 Playwright 而非 Puppeteer，因为 Playwright 的反检测基础更好
- 所有反检测代码通过 `addInitScript` 在页面加载前注入
- 请遵守目标网站的 robots.txt 和服务条款
