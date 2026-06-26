---
name: amazon-scraper
description: >
  High-performance containerized Amazon scraper (Docker + playwright-extra + Stealth plugin).
  Bypasses Amazon headless detection. Supports Amazon BSR, search results, and product detail pages. Also includes a generic mode for other dynamic web pages.
  Use when user mentions any of these:
  爬虫, 爬取, 抓取, 采集, 数据采集, 爬数据, 抓数据, 获取数据,
  scrape, crawl, extract, fetch data, pull data,
  亚马逊, Amazon, ASIN, BSR, Best Sellers, 畅销榜, 热销榜, 新品榜, 飙升榜, 排行榜,
  选品, 竞品分析, 竞品调研, 市场调研, 品类分析, 类目分析, 产品调研,
  月销量, bought in past month, 销量, 评论数, 价格对比,
  网页内容, 网站数据, 页面抓取, 动态页面,
  关键词搜索, 搜索结果, search results,
  产品详情, 产品信息, listing数据, listing分析,
  top 100, top sellers, 热门产品, 爆款, 跑量款,
  价格带, 评分分布, review分析, 评论分析
---

# Amazon Scraper

Docker容器化爬虫，基于 playwright-extra + Stealth 插件，专为绕过亚马逊反爬检测优化，同时支持通用动态网页爬取。

## ⚙️ 系统要求

- **Docker Engine 20.10+**（必须已安装并运行）
- **磁盘空间**：~2GB（镜像 + Playwright 浏览器二进制文件）
- **内存**：建议 2GB+（Playwright 运行时需要）

## 快速开始

首次使用：在 skill 目录下执行一键构建脚本：

```bash
bash scripts/setup.sh
```

脚本会自动完成：构建 `amazon-scraper` 镜像 + 创建 `~/scrapes` 输出目录。

## 模式选择规则

### 1. Amazon模式 (`amazon_handler.js`)
**自动触发条件:** URL包含 `amazon.com`，或用户提到亚马逊/Amazon/ASIN/BSR/选品/竞品/畅销榜/类目分析等关键词

根据URL自动识别页面类型：

| URL特征 | 页面类型 | 可获取字段 |
|---|---|---|
| `/gp/bestsellers/` | 畅销榜 | rank, title, asin, price, rating, reviews, image, url |
| `/zg/new-releases/` | 新品榜 | 同上 |
| `/zg/movers-and-shakers/` | 飙升榜 | 同上 |
| `/s?k=` 或 `/s/` | 搜索结果 | title, asin, price, rating, reviews, image, url, **boughtPastMonth**, sponsored |
| `/dp/` 或 `/gp/product/` | 产品详情 | title, asin, price, rating, reviews, brand, bsr, **boughtPastMonth**, dateFirstAvailable, category, bullets, details, image |

**⚠️ 重要规则:**
- **Best Sellers页面没有月销量(boughtPastMonth)数据** — 亚马逊不在榜单页显示此信息
- **要获取月销量，必须用搜索页(`/s?k=关键词`)或产品详情页(`/dp/ASIN`)**
- 如果用户同时需要排名+月销量，建议：先爬Best Sellers拿排名，再用搜索页补月销
- **BSR URL 必须使用 `/gp/bestsellers/`**，`/zgbs/` 会返回 Page Not Found

```bash
# 畅销榜（有排名，无月销）
docker run -t --rm amazon-scraper node assets/amazon_handler.js "https://www.amazon.com/gp/bestsellers/electronics"

# 搜索结果（有月销，无排名）
docker run -t --rm amazon-scraper node assets/amazon_handler.js "https://www.amazon.com/s?k=feather+duster"

# 产品详情（最全字段：BSR、品牌、卖点、月销）
docker run -t --rm amazon-scraper node assets/amazon_handler.js "https://www.amazon.com/dp/B001TQ6IHS"

# 多页爬取
docker run -t --rm amazon-scraper node assets/amazon_handler.js "URL" --pages 2

# 保存结果到文件
docker run -t --rm -v ~/scrapes:/data amazon-scraper node assets/amazon_handler.js "URL" --output result.json

# 用自己的代理覆盖内置配置
docker run -t --rm -e AMAZON_PROXIES="http://user:***@host:8001,..." amazon-scraper node assets/amazon_handler.js "URL"
```

**输出格式:** JSON
```json
{
  "status": "SUCCESS",
  "type": "bestsellers|search|product-detail",
  "category": "品类名",
  "totalProducts": 30,
  "scrapedAt": "ISO时间",
  "products": [
    {
      "rank": 1,
      "title": "产品名",
      "asin": "B001TQ6IHS",
      "price": 9.94,
      "priceStr": "$9.94",
      "rating": 4.6,
      "reviews": 20547,
      "boughtPastMonth": "1K+",
      "image": "https://...",
      "url": "https://..."
    }
  ]
}
```

### 2. 通用模式 (`main_handler.js`)
**触发条件:** 非Amazon的URL，或用户提到爬取/抓取任意网页内容

- 基于和 Amazon 模式相同的 `playwright-extra` + Stealth 架构
- 内置代理已预配置，无需额外设置
- 支持 `--output` 文件保存
- 可通过环境变量覆盖内置代理
- Playwright打开页面，等待JS加载完成
- 提取 `document.body.innerText`（纯文本，去广告噪音）
- 输出上限10000字符
- 输出: `{status:"SUCCESS", type:"GENERIC", title, data}`

```bash
# 通用爬取（代理已内置）
docker run -t --rm amazon-scraper node assets/main_handler.js "https://任意网址"

# 保存文件
docker run -t --rm -v ~/scrapes:/data \
  amazon-scraper node assets/main_handler.js "https://任意网址" --output page.json
```

## Agent调用决策树

```
用户给了URL?
├─ 包含 amazon.com → 用 amazon_handler.js
│   ├─ 需要月销量? → 建议用搜索URL(/s?k=) 或详情页(/dp/)
│   └─ 需要排名? → 用畅销榜URL(/gp/bestsellers/)
└─ 其他网站 → 用 main_handler.js (通用模式)

用户没给URL，只说了需求?
├─ "爬亚马逊XX品类Top" / "XX类目排行" / "XX畅销榜" → 构造 https://www.amazon.com/gp/bestsellers/品类
├─ "搜亚马逊XX" / "XX关键词搜索" / "找XX产品" → 构造 https://www.amazon.com/s?k=关键词
├─ "分析某个ASIN" / "看看这个产品" / "XX的详情" → 构造 https://www.amazon.com/dp/ASIN
├─ "XX的月销量" / "XX卖了多少" / "XX销量怎么样" → 用搜索页或详情页（有boughtPastMonth）
├─ "竞品分析" / "竞品调研" / "对手在卖什么" → 先搜索再逐个爬详情
├─ "选品" / "什么好卖" / "品类机会" / "市场调研" → Best Sellers + 搜索结合
└─ 其他网页 → 先web_search找到URL，再用通用模式爬
```

## 常见用户意图 → 操作映射

| 用户说 | 操作 |
|---|---|
| "帮我看看亚马逊XX品类" | 爬 /gp/bestsellers/品类 畅销榜 |
| "XX在亚马逊卖得怎么样" | 搜索 /s?k=XX 看月销 |
| "分析一下这个ASIN: BXXXXXXXXX" | 爬 /dp/ASIN 详情页 |
| "XX品类有什么机会" | 畅销榜 + 搜索 综合分析 |
| "帮我爬这个链接" | 判断URL类型，选对应handler |
| "帮我抓XX网站的内容" | 通用模式 |
| "搜一下XX的竞品" | 搜索页爬取 + 分析 |
| "XX月销多少" / "XX一个月卖多少" | 搜索页或详情页 |
| "帮我看看top 100" / "热门产品" | Best Sellers畅销榜 |
| "新品有哪些" / "最近上了什么新品" | /zg/new-releases/ |
| "什么产品涨得快" / "飙升榜" | /zg/movers-and-shakers/ |

## 代理配置

**本 skill 已内置 5 个轮询代理，无需额外配置即可直接使用。**

如需覆盖内置代理，可通过环境变量注入自己的代理：

| 变量 | 用途 | 格式 |
|---|---|---|
| `AMAZON_PROXY` | 单代理 | `http://user:pass@host:port` |
| `AMAZON_PROXIES` | 多代理轮询 | `http://u:p@h1:8001,http://u:p@h2:8002,...` |

- **轮询**：多页爬取时每页自动切换下一个代理
- **故障切换**：单页失败时自动重试列表中下一个代理
- 代理配置存放于 `config/proxies.json`，可直接修改文件更新代理列表

## 反爬能力
- **playwright-extra + puppeteer-extra-plugin-stealth** — 自动修改 navigator、WebGL、Canvas 等 headless 特征
- **Chrome 123 UserAgent** — 模拟真实 Mac Chrome 浏览器
- **完整浏览器指纹 headers** — Accept-Encoding: identity, Sec-Ch-Ua, Sec-Fetch-* 等
- **1920x1080 viewport** — 避免移动端/小屏检测
- 自动滚动加载懒加载内容
- Docker沙箱隔离，每次启动全新浏览器上下文
- 代理轮询分散请求源 IP

## 局限
- 通用模式输出上限10000字符
- Amazon单页最多约30-50个产品
- 不支持需要登录的页面
- Docker容器启动有~15秒冷启动时间（含 stealth 插件初始化）
