# 高级用法

## Spider 框架（大规模并发爬取）

Spider 框架提供 Scrapy 风格的 API，适合需要跨多页面爬取的任务：

```python
from scrapling.spiders import Spider, Request, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10       # 最大并发数
    download_delay = 0.5           # 请求间隔（秒）
    robots_txt_obey = True         # 遵守 robots.txt

    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
                "tags": quote.css('.tag::text').getall(),
            }
        # 翻页
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield Request(response.urljoin(next_page))

# 运行爬虫
result = QuotesSpider().start()
result.items.to_json('quotes.json')       # 导出 JSON
result.items.to_jsonl('quotes.jsonl')     # 导出 JSONL
```

---

## 暂停与恢复爬虫

```python
from scrapling.spiders import Spider

class LargeSpider(Spider):
    name = "large"
    start_urls = ["https://large-site.com/"]
    # 开启检查点持久化
    checkpoint = True

    async def parse(self, response):
        # ...爬取逻辑...
        pass

# 启动时按 Ctrl+C 优雅停止
result = LargeSpider().start()

# 下次运行时自动从上次停止的地方继续
result = LargeSpider().start()   # 无需额外配置
```

---

## 流式输出（实时处理）

```python
from scrapling.spiders import Spider
import asyncio

class StreamingSpider(Spider):
    name = "stream"
    start_urls = ["https://news-site.com/"]

    async def parse(self, response):
        for article in response.css('article'):
            yield {"title": article.css('h2::text').get()}

async def main():
    spider = StreamingSpider()
    async for item in spider.stream():
        # 实时处理每个抓取到的 item
        print(item)
        # 实时写入数据库、发送到队列等

asyncio.run(main())
```

---

## 多 Session 路由（混用 HTTP 和浏览器）

```python
from scrapling.spiders import Spider, Request, Response

class HybridSpider(Spider):
    name = "hybrid"
    start_urls = ["https://example.com/catalog"]

    async def parse(self, response: Response):
        for link in response.css('.product-link::attr(href)').getall():
            # 普通页面用 HTTP，详情页面用浏览器
            if '/protected/' in link:
                yield Request(link, session_id='stealthy')   # 使用 StealthyFetcher
            else:
                yield Request(link)                           # 使用默认 HTTP

    async def parse_product(self, response: Response):
        yield {"title": response.css('h1::text').get()}
```

---

## 代理轮换

```python
from scrapling.fetchers import Fetcher, FetcherSession, StealthyFetcher
from scrapling.proxy_rotator import ProxyRotator

# 设置代理列表
proxies = [
    "http://user:pass@proxy1.example.com:8080",
    "http://user:pass@proxy2.example.com:8080",
    "socks5://user:pass@proxy3.example.com:1080",
]

# 循环轮换
rotator = ProxyRotator(proxies, mode='cyclic')

with FetcherSession(proxy=rotator) as session:
    page = session.get('https://example.com')
    print(page.css('title::text').get())

# Spider 中使用代理
class ProxySpider(Spider):
    name = "proxy"
    start_urls = ["https://example.com/"]
    proxies = proxies   # 直接指定代理列表（自动轮换）

    async def parse(self, response):
        yield {"url": response.url}
```

---

## 防 DNS 泄露（DoH 模式）

使用代理时，防止真实 IP 通过 DNS 查询泄露：

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get(
    'https://example.com',
    doh=True   # 通过 Cloudflare DoH 路由 DNS 查询
)
```

---

## 广告拦截和域名过滤

```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

# 开启内置广告拦截（约 3500 个广告/追踪域名）
with DynamicSession(headless=True, block_ads=True) as session:
    page = session.fetch('https://news-site.com/')

# 自定义域名黑名单（拦截指定域名及其所有子域名）
with DynamicSession(
    headless=True,
    blocked_domains=['ads.example.com', 'tracker.net']
) as session:
    page = session.fetch('https://example.com/')
```

---

## MCP 服务器（AI 集成）

Scrapling 内置 MCP 服务器，让 Claude/Cursor 直接控制浏览器提取数据，在传给 AI 之前完成精准提取，大幅降低 Token 消耗：

### 启动 MCP 服务器

```bash
# 直接启动（用于手动测试）
scrapling mcp

# 在 Claude Code 中配置
claude mcp add scrapling --scope user python -m scrapling.mcp
```

### Claude Code 配置

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "python",
      "args": ["-m", "scrapling.mcp"],
      "env": {}
    }
  }
}
```

### 在 AI 对话中使用

```
请用 Scrapling 抓取 https://news.ycombinator.com/ 的所有文章标题和链接

请用隐身模式抓取 https://example.com/products 的商品列表，这个网站有 Cloudflare 保护
```

---

## 开发模式（离线调试）

```python
from scrapling.fetchers import Fetcher

# 首次运行：缓存响应到磁盘
page = Fetcher.get('https://example.com', cache=True)
products = page.css('.product', auto_save=True)

# 后续运行：从缓存读取，无需网络请求（快速迭代解析逻辑）
page = Fetcher.get('https://example.com', cache=True, dev_mode=True)
products = page.css('.product', adaptive=True)
```

---

## 异步并发抓取

```python
import asyncio
from scrapling.fetchers import AsyncFetcher

async def fetch_all(urls):
    async with AsyncFetcher() as fetcher:
        tasks = [fetcher.get(url) for url in urls]
        pages = await asyncio.gather(*tasks)
        return [page.css('title::text').get() for page in pages]

urls = [f"https://example.com/page/{i}" for i in range(1, 20)]
titles = asyncio.run(fetch_all(urls))
```

---

## 完成确认检查清单

- [ ] Spider 类成功爬取多页数据并导出 JSON
- [ ] 代理轮换配置正确（可选）
- [ ] MCP 服务器启动成功（如需 AI 集成）
- [ ] 暂停/恢复功能测试通过（长任务场景）

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [完整文档](https://scrapling.readthedocs.io/en/latest/)
- [Spider API 参考](https://scrapling.readthedocs.io/en/latest/spiders/architecture.html)
- [MCP 文档](https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html)
