---
name: crawl-pro
version: 1.0.0
description: 爬虫专项工作流 - 基于 Scrapling 框架的生产级采集。自适应元素定位、反爬绕过、并发规模爬取、代理轮换。
keywords: [爬虫,抓取,Scraping,crawl,采集,Scrapling,反爬]
---

# Crawl Pro - 爬虫专项工作流
基于 Scrapling 框架的生产级采集

---

## 核心思想

** Scrapling 核心能力：**
1. 自适应元素定位 — 网站改版无需改代码
2. 反爬绕过 — Cloudflare 等自动绕过
3. 并发规模 — 断点续爬、代理轮换
4. MCP 集成 — AI 辅助智能抓取

---

## 触发词

`爬虫模式` / `crawl pro` / `抓取` / `采集中`

---

## 工作流阶段

### 1️⃣ 环境与请求方式选择

```
## 🌍 环境选择

### 目标网站分析
- 反爬级别：[低/中/高/Cloudflare]
- 动态内容：[是/否]

### Fetcher 选择
| 场景 | Fetcher | 说明 |
|------|---------|------|
| 静态页面 | Fetcher | 轻量，高并发 |
| 反爬站点 | StealthyFetcher | 指纹伪装 |
| JS动态渲染 | DynamicFetcher | Playwright |

### 安装
pip install scrapling
```

---

### 2️⃣ 基础请求与解析

```
## 📡 请求示例

### 基础请求
```python
from scrapling import Fetcher
fetcher = Fetcher()
response = fetcher.get('https://www.example.com')
```

### 元素提取
```python
# CSS 选择器
products = response.css('.product')

# 开启自适应（网站改版自动重定位）
products = response.css('.product', adaptive=True)

# 首次存入 SQLite，后续自动重定位
products = response.css('.product', auto_save=True)
```

### XPath 也支持
```python
items = response.xpath('//div[@class="product"]')
```
```

---

### 3️⃣ 自适应元素定位（核心）

```
## 🎯 自适应定位

### 原理
- 框架通过相似度算法（Levenshtein 距离）自动匹配
- 0.3 秒内完成重定位
- 无需修改代码

### 使用
```python
# 首次爬取
products = response.css('.product', auto_save=True)

# 网站改版后
products = response.css('.product', adaptive=True)
# 自动找到新位置的元素！
```
```

---

### 4️⃣ 并发规模爬取

```
## ⚡ 并发爬取

### 定义 Spider
```python
from scrapling import Spider

class MySpider(Spider):
    start_urls = ['https://example.com/page1', 'https://example.com/page2']
    
    async def parse(self, response):
        products = response.css('.product', adaptive=True)
        for product in products:
            yield {
                'name': product.css('.name').text(),
                'price': product.css('.price').text()
            }
```

### 配置并发
```python
spider.run(
    concurrent_requests=8,  # 并发数
    download_delay=3,           # 请求延迟（秒）
    auto_save=True,            # 断点续爬
    export='jsonl'            # 导出格式
)
```

### 断点续爬
- 按 Ctrl+C 中断自动保存 Checkpoint
- 重启后从上次位置继续
```
```

---

### 5️⃣ 反爬与代理轮换

```
## 🛡️ 反爬策略

### 代理轮换
```python
# 循环轮换代理
spider = MySpider(proxy_rotator='cyclic')

# 或内置代理池
```

### 反爬配置
| 参数 | 说明 |
|------|------|
| headless=False | 可见浏览器 |
| network_idle=True | 等待网络空闲 |
| retry=3 | 重试次数 |

### StealthyFetcher（深度伪装）
```python
from scrapling import StealthyFetcher
fetcher = StealthyFetcher.adaptive = True
response = fetcher.fetch('https://cloudflare-site.com', headless=True)
```
```

---

### 6️⃣ 数据输出

```
## 💾 数据输出

### 实时流式输���
```python
async for item in spider.stream():
    print(item)  # 实时处理
```

### 导出格式
```python
spider.run(export='jsonl')   # JSONL
spider.run(export='json')    # JSON
spider.run(export='csv')     # CSV
```

### 自定义 Pipeline
```python
class MyPipeline:
    async def process(self, item):
        # 自定义处理
        await save_to_db(item)
```
```

---

### 7️⃣ AI 集成（MCP）

```
## 🤖 AI 集成

### MCP Server
```python
from scrapling import MCP_SERVER
MCP_SERVER.start()
```

### AI 智能抓取
- 先用 MCP 提取数据
- 再调用 AI 分析
- 降低 Token 消耗
```

---

## 性能调优

| 网站类型 | 并发数 | 请求延迟 |
|----------|--------|----------|
| 普通网站 | 5-10 | 2-5秒 |
| 反爬站点 | 2-3 | 5-10秒 |
| 动态网站 | 1-2 | 10秒+ |

---

## 快速指令表

| 需求 | 命令 |
|------|------|
| 分析目标站 | `分析网站[URL]的反爬级别` |
| 写爬虫 | `写一个爬虫：抓取[URL]的[内容]` |
| 自适应 | `用adaptive模式抓取` |
| 大规模 | `并发爬取[URL]，8并发` |

---

## 输出规范

### 完整爬虫模板
```python
# 导入
from scrapling import Spider, Fetcher

# 定义
class ProductSpider(Spider):
    start_urls = ['https://example.com']
    
    async def parse(self, response):
        items = response.css('.item', adaptive=True)
        for item in items:
            yield {'title': item.css('h2').text()}

# 运行
if __name__ == '__main__':
    fetcher = Fetcher()
    spider = ProductSpider(fetcher=fetcher)
    spider.run(concurrent_requests=5, export='jsonl')
```

---

*Crawl Pro | 基于 Scrapling 的生产级爬虫工作流*