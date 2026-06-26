# Scrapling 抓取指南

## 1. CLI 命令速查

| 命令 | 用途 | 适用场景 |
|-----|------|---------|
| `get` | HTTP GET 请求 | 静态页面、博客、新闻 |
| `fetch` | 浏览器模式 | 动态内容、SPA |
| `stealthy-fetch` | 隐身浏览器 | 反爬保护、Cloudflare |

**常用参数**：
- `--timeout 60` : 超时秒数
- `--network-idle` : 等待网络空闲
- `--wait 2000` : 额外等待毫秒
- `-s ".selector"` : CSS 选择器
- `--wait-selector ".loaded"` : 等待元素出现
- `--proxy "http://host:port"` : 使用代理

## 2. CLI 抓取示例

**抓取 36氪 AI 频道**：
```bash
# 方式 1: 简单请求（适合静态页面）
scrapling extract get "https://www.36kr.com/information/AI/" /tmp/36kr-ai.md

# 方式 2: 浏览器模式（适合动态内容）
scrapling extract fetch "https://www.36kr.com/information/AI/" /tmp/36kr-ai.md --network-idle

# 方式 3: 隐身模式（适合反爬保护）
scrapling extract stealthy-fetch "https://www.36kr.com/information/AI/" /tmp/36kr-ai.md
```

**抓取虎嗅 AI 相关**：
```bash
scrapling extract get "https://www.huxiu.com/channel/106.html" /tmp/huxiu-ai.md
```

**使用 CSS 选择器提取特定内容**：
```bash
# 只提取文章列表
scrapling extract get "https://www.36kr.com/information/AI/" /tmp/articles.md -s ".article-item"
```

## 3. Python 脚本抓取 (复杂场景)

对于复杂抓取，使用 `scripts/scrape_news.py`：

```python
from scrapling.fetchers import Fetcher, StealthyFetcher

# 简单抓取
page = Fetcher.get('https://www.36kr.com/information/AI/')
titles = page.css('.article-item .title::text').getall()

# 隐身抓取（绕过反爬）
page = StealthyFetcher.fetch('https://www.36kr.com/information/AI/', headless=True)
articles = page.css('.article-item')

for article in articles:
    title = article.css('.title::text').get()
    link = article.css('a::attr(href)').get()
    print(f"{title}: {link}")
```