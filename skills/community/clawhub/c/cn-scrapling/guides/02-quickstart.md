# 快速开始

## 适用场景

- 从静态或动态页面提取数据
- 处理需要绕过反爬保护的网站
- 使用 CSS/XPath 选择器精准提取内容
- 实现网页改版后的自适应抓取

---

## 选择正确的 Fetcher

| 场景 | Fetcher | 速度 |
|------|---------|------|
| 普通 HTTP 请求 | `Fetcher` | 最快 |
| 需要 TLS 指纹伪装 | `Fetcher(impersonate='chrome')` | 快 |
| Cloudflare / 反爬 | `StealthyFetcher` | 中 |
| 需要 JS 渲染 | `DynamicFetcher` | 慢 |

---

## 基础 HTTP 抓取

```python
from scrapling.fetchers import Fetcher

# 单次请求
page = Fetcher.get('https://quotes.toscrape.com/')

# 提取数据
quotes = page.css('.quote .text::text').getall()
authors = page.css('.quote .author::text').getall()
print(quotes[:3])

# XPath 方式
titles = page.xpath('//span[@class="text"]/text()').getall()
```

---

## Session 复用（跨请求保持状态）

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    # 使用最新版 Chrome TLS 指纹
    page1 = session.get('https://example.com/', stealthy_headers=True)
    page2 = session.get('https://example.com/products')  # 复用 cookie
    
    products = page2.css('.product h2::text').getall()
```

---

## 绕过 Cloudflare 保护

```python
from scrapling.fetchers import StealthyFetcher, StealthySession

# 单次请求（每次打开/关闭浏览器）
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    headless=True,
    solve_cloudflare=True   # 自动处理 Cloudflare Turnstile
)
data = page.css('.content').get()

# Session 模式（保持浏览器，效率更高）
with StealthySession(headless=True) as session:
    page = session.fetch('https://protected-site.com', google_search=False)
    links = page.css('a.product-link::attr(href)').getall()
```

---

## 动态页面（JS 渲染）

```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

# 等待网络空闲后抓取（确保异步数据加载完成）
page = DynamicFetcher.fetch(
    'https://spa-app.com',
    headless=True,
    network_idle=True
)
items = page.css('.item-list .item::text').getall()

# Session 模式（连续操作多个页面）
with DynamicSession(headless=True) as session:
    page = session.fetch('https://example.com/login')
    # 可以执行页面交互（通过 Playwright）
    page2 = session.fetch('https://example.com/dashboard')
    data = page2.css('.metric::text').getall()
```

---

## CSS 和 XPath 选择器

```python
page = Fetcher.get('https://quotes.toscrape.com/')

# CSS 选择器
title = page.css('h1::text').get()                    # 第一个元素
all_texts = page.css('.quote .text::text').getall()   # 全部

# XPath 选择器
author = page.xpath('//small[@class="author"]/text()').get()
hrefs = page.xpath('//a/@href').getall()

# 属性提取
link = page.css('a::attr(href)').get()
src = page.css('img::attr(src)').get()

# 正则提取
price = page.css('.price::text').re_first(r'\$[\d.]+')
numbers = page.css('p::text').re(r'\d+')
```

---

## 自适应抓取（网页改版后自动重定位）

这是 Scrapling 最独特的功能：

```python
from scrapling.fetchers import Fetcher

# 第一次抓取：保存元素快照（存入本地数据库）
page = Fetcher.get('https://example.com/products')
products = page.css('.product-card', auto_save=True)
print(f"找到 {len(products)} 个商品")
for p in products:
    print(p.css('h2::text').get(), p.css('.price::text').get())

# 网站改版后（.product-card 变成了 .item-wrapper）
# 传入 adaptive=True，自动通过历史快照重新定位
page = Fetcher.get('https://example.com/products')
products = page.css('.product-card', adaptive=True)   # 自动找到
```

仅查找相似元素：
```python
# 找到一个已知元素，然后查找页面上所有相似的元素
page = Fetcher.get('https://example.com')
first_item = page.css('.item').get()
similar = page.find_similar(first_item)  # 自动定位同类元素
```

---

## 查找相似元素

```python
page = Fetcher.get('https://news-site.com')

# 找到第一篇文章
first_article = page.css('article.news-item').get()

# 自动找到所有相似的文章（即使 HTML 结构不完全一样）
articles = page.find_similar(first_article)
for article in articles:
    print(article.css('h2::text').get())
```

---

## CLI 快速测试

```bash
# 抓取页面内容
scrapling fetch https://quotes.toscrape.com/ --css ".quote .text"

# 指定 Fetcher 类型
scrapling fetch https://protected-site.com --fetcher stealthy --headless

# 输出完整 HTML
scrapling fetch https://example.com --html
```

---

## 交互式调试 Shell

```bash
# 启动 IPython Shell（含 Scrapling 集成）
scrapling shell https://quotes.toscrape.com/

# 在 Shell 中：
>>> quotes = page.css('.quote .text::text').getall()
>>> authors = page.css('.author::text').getall()
>>> # 将 curl 命令转换为 Scrapling 代码：
>>> curl_to_scrapling('curl -H "User-Agent: Mozilla" https://example.com')
```

---

## 完成确认检查清单

- [ ] `Fetcher.get()` 成功返回 200 状态码
- [ ] CSS 选择器 `.getall()` 返回非空列表
- [ ] 选择适当的 Fetcher（普通/隐身/动态）
- [ ] `auto_save=True` 测试通过（数据保存到本地）
- [ ] `adaptive=True` 在元素改变后仍能定位（可选测试）

---

## 下一步

- [高级用法](03-advanced-usage.md) — Spider 框架、代理轮换、MCP 服务器、流式输出
