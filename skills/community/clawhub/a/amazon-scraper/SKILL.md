---
name: amazon-scraper
description: >
  Containerized Amazon.com scraper (Docker + Playwright) for BSR/new-releases/movers rankings,
  keyword search results, and product detail pages. Requires a paid ISP/residential proxy.

  Use when the request is specifically about Amazon product or marketplace data:
  亚马逊/Amazon, ASIN, BSR, Best Sellers, 畅销榜, 新品榜, 飙升榜,
  选品, 竞品分析, 类目分析, listing 分析, 月销量 (bought in past month),
  评分分布, 评论分析, Amazon 关键词搜索结果, Amazon 产品详情.

  Do NOT use for general-purpose web scraping just because the user said
  爬取/抓取/采集/scrape/crawl. Every run spends metered proxy bandwidth, and the
  generic mode exists only as a fallback for pages related to an Amazon task.
  For unrelated sites prefer web_search/web_fetch, or ask first.
metadata:
  openclaw:
    requires:
      bins:
        - docker
---

# Amazon Scraper

Docker 容器化爬虫，Playwright Chromium。不使用 stealth 插件。支持亚马逊榜单/搜索/详情及通用动态页。

## 第 0 步（开跑前必须先做，不过就停）

先确认出口，再碰亚马逊：

```bash
export AMAZON_PROXIES="http://USER:PASS@HOST:PORT"   # 从密码管理器取，不要贴进对话
curl -s -x "$AMAZON_PROXIES" http://api.ipify.org
```

返回的纯文本必须等于你配置的代理 host。不是这个 IP、超时、407、403，都停，不要开爬，也不要重建后直接跑。

- **凭证不进仓库、不进镜像、不进命令回显。** 用 `-e AMAZON_PROXIES`（值从环境取，不要写在命令行里）或挂载 `config/proxies.json`。该文件已在 `.gitignore` / `.dockerignore` 里。
- 这一步只证明代理层通。裸 curl 打亚马逊拿到 500/202，不算第 0 步失败。
- 第 0 步过了，才允许 `docker run amazon-scraper`。

## 系统要求

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
| `/dp/` 或 `/gp/product/` | 产品详情 | title, asin, price, rating, reviews, brand, bsr, **boughtPastMonth**, **seller**, dateFirstAvailable, category, bullets, details |

**⚠️ 重要规则:**
- **Best Sellers 页面没有月销量(boughtPastMonth)数据** — 亚马逊不在榜单页显示此信息
- **要获取月销量，必须用搜索页(`/s?k=关键词`)或产品详情页(`/dp/ASIN`)**
- 如果用户同时需要排名+月销量，建议：先爬 Best Sellers 拿排名，再用搜索页补月销
- **BSR URL 必须使用 `/gp/bestsellers/`**，`/zgbs/` 会返回 Page Not Found
- **BSR 单 URL 只能拿 60 个产品**（2 页限制）。拿 Top 100 用搜索页 `--pages 5` 或多子类目 BSR 合并。详见 `references/bsr-top100-strategy.md`
- **评论（rating/title/body/date/helpful/verified）不在这张表里**：需要登录态 + CDP，走 `scripts/scrape_reviews.py`（`/portal/customer-reviews/ASIN` 瀑布流）。先读 `references/reviews-strategy.md` 顶部的账号/合规代价说明
- 视觉化选品 fallback：把 `image` URL 喂给 `vision_analyze`，让它"看图识物"。参考 `references/product-form-fusion.md`

```bash
# 畅销榜（有排名，无月销，最多 60 个）
docker run --rm amazon-scraper node assets/amazon_handler.js "https://www.amazon.com/gp/bestsellers/electronics"

# 搜索结果（有月销，多页可达 100+）
docker run --rm amazon-scraper node assets/amazon_handler.js "https://www.amazon.com/s?k=feather+duster"

# 产品详情（最全字段：BSR、品牌、卖点、月销）
docker run --rm amazon-scraper node assets/amazon_handler.js "https://www.amazon.com/dp/B001TQ6IHS"

# 多页爬取（搜索页建议 5 页拿 Top 100）
docker run --rm amazon-scraper node assets/amazon_handler.js "URL" --pages 2

# 保存结果到文件（必须挂载 /data 才能在主机读到）
docker run --rm -v ~/scrapes:/data amazon-scraper node assets/amazon_handler.js "URL" --output result.json

# 用自己的代理覆盖内置配置
docker run --rm -e AMAZON_PROXIES="http://user:***@host:8001,..." amazon-scraper node assets/amazon_handler.js "URL"
```

**输出状态（必须检查，不要只看 products 长度）**

| `status` | 退出码 | 含义 | 该怎么办 |
|---|---|---|---|
| `SUCCESS` | 0 | 所有页都抓到了 | 正常使用数据 |
| `PARTIAL` | 3 | 部分页被拦/超时，`failures[]` 列出来了 | 可以用已拿到的，但**不要**把缺的那部分当成"不存在" |
| `ERROR` | 2 / 1 | 全部失败 | 丢弃结果。先查第 0 步出口，再看是不是被软拦截 |

软拦截的典型表现是 HTTP 200 + 整页没渲染，于是所有字段都是 null。现在详情页遇到这种情况会算失败并换代理重试，不会再以 `SUCCESS` 混进结果。**写入数据库/生成报表前先判 `status`** —— 把软拦截当成"价格没变"比没有数据更糟。

**输出格式:** JSON
```json
{
  "status": "SUCCESS",
  "failedJobs": [],
  "failures": [],
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
      "url": "https://...",
      "sponsored": false
    }
  ]
}
```

### 2. 通用模式 (`main_handler.js`)
**触发条件:** 非Amazon的URL，或用户提到爬取/抓取任意网页内容

- 和 Amazon 模式同一套 Playwright（无 stealth）
- 内置代理已预配置，无需额外设置
- 支持 `--output` 文件保存
- 可通过环境变量覆盖内置代理
- Playwright打开页面，等待JS加载完成
- 提取 `document.body.innerText`（纯文本，去广告噪音）
- 输出上限10000字符
- 输出: `{status:"SUCCESS", type:"GENERIC", title, data}`

```bash
# 通用爬取（代理已内置）
docker run --rm amazon-scraper node assets/main_handler.js "https://任意网址"

# 保存文件
docker run --rm -v ~/scrapes:/data \
  amazon-scraper node assets/main_handler.js "https://任意网址" --output page.json
```

## Agent调用决策树

```
用户给了URL?
├─ 包含 amazon.com → 用 amazon_handler.js
│   ├─ 需要月销量? → 建议用搜索URL(/s?k=) 或详情页(/dp/)
│   ├─ 需要排名? → 用畅销榜URL(/gp/bestsellers/)
│   └─ 需要 Top 100? → 搜索页 --pages 5 (或看 references/bsr-top100-strategy.md)
└─ 其他网站 → 用 main_handler.js (通用模式)

用户没给URL，只说了需求?
├─ "爬亚马逊XX品类Top" / "XX类目排行" / "XX畅销榜" → 构造 https://www.amazon.com/gp/bestsellers/品类
├─ "搜亚马逊XX" / "XX关键词搜索" / "找XX产品" → 构造 https://www.amazon.com/s?k=关键词
├─ "分析某个ASIN" / "看看这个产品" / "XX的详情" → 构造 https://www.amazon.com/dp/ASIN
├─ "XX的月销量" / "XX卖了多少" / "XX销量怎么样" → 用搜索页或详情页（有boughtPastMonth）
├─ "竞品分析" / "竞品调研" / "对手在卖什么" → 先搜索再逐个爬详情
├─ "选品" / "什么好卖" / "品类机会" / "市场调研" → Best Sellers + 搜索结合
├─ "Top 100" / "Top 200" / "拿 100 个产品" → /s?k=关键词 --pages 5 (一次拿 100+)
├─ "抓评论" / "获取评价" / "reviews" → 需登录态 Chrome + CDP，用 scripts/scrape_reviews.py（瀑布流模式）
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
| "帮我看看top 100" / "热门产品" | **/s?k=关键词 --pages 5**（BSR 单 URL 只到 60） |
| "新品有哪些" / "最近上了什么新品" | /zg/new-releases/ |
| "什么产品涨得快" / "飙升榜" | /zg/movers-and-shakers/ |
| "抓评论" / "获取评价" / "XX的评论" | **scripts/scrape_reviews.py**（需已登录 Chrome + CDP，瀑布流模式） |

## 代理配置

代理配置存放于 `config/proxies.json`，格式为 JSON 数组：

```json
{
  "proxies": [
    "http://user-XXX:password@ENTRY_POINT:PORT",
    "http://user-XXX:password@ENTRY_POINT:PORT"
  ]
}
```

优先级（`assets/proxy.js`，环境变量优先）：
1. `AMAZON_PROXIES`（逗号分隔多条）
2. `AMAZON_PROXY`（单条）
3. `AMAZON_PROXY_FILE` 指向的文件，否则 `config/proxies.json`

一条都没配就**直接报错退出**，不会悄悄用宿主机 IP 去爬（真要这么做得显式 `AMAZON_ALLOW_DIRECT=1`）。日志只打 `host:port`，不打凭证。

凭证**不再烘进镜像**（`Dockerfile` 不 `COPY config/`）。运行时二选一：

```bash
docker run --rm -e AMAZON_PROXIES amazon-scraper node assets/amazon_handler.js "URL"
docker run --rm -v "$PWD/config/proxies.json:/app/config/proxies.json:ro" amazon-scraper node assets/amazon_handler.js "URL"
```

改凭证不需要重 build，只有改 `assets/` 才需要。协议只接受 `http://` / `https://`，`socks5://` 会在启动时报错。

并发被代理条数卡死：`concurrency = min(请求值, 任务数, proxies.length)`。只有 1 条时 `--concurrency 5` 实际是 1，并且现在会打一行 WARNING 说明被降到了几。不要开 5 个容器打同一个 IP。

### 入口域名速查（Oxylabs 各产品）

| 产品 | 入口域名 | Amazon 适用? |
|---|---|---|
| Datacenter / DDC | `ddc.oxylabs.io` | ❌（被 Amazon ASN 黑名单） |
| **ISP Proxies** ⭐ | `isn.oxylabs.io` 或 `pr.oxylabs.io` | ✅ **推荐** |
| Residential | `pr.oxylabs.io` | ✅ |
| Mobile | `mob.oxylabs.io` | ✅（最严目标） |

> 📖 **完整产品矩阵 / 凭证格式 / 怎么从 dashboard 拿入口域名**：[references/oxylabs-product-matrix.md](references/oxylabs-product-matrix.md)
> 📖 **DDC 故障排查 / response code 速查**：[references/oxylabs-ddc-format.md](references/oxylabs-ddc-format.md)
> 📖 **Oxylabs Response Code + 怎么判断"代理层通 vs 目标站拦"**：[references/oxylabs-proxy-format.md](references/oxylabs-proxy-format.md)

### ⚠️ 代理配置陷阱（来自真实踩坑）

1. **不要把 dashboard 上的 "Assigned IP" 当入口**：那是出口 IP，不是入口。直接打 `45.x.x.x:8001` 在 VPS 上会 `No route to host`。**必须用 `ddc.oxylabs.io` 域名 + 端口**。详见 `references/oxylabs-ddc-format.md`。

2. **DDC / Datacenter 代理对 Amazon 不可用**：Amazon 把整个 datacenter ASN 段都标为高风险，配置 100% 正确也会拿到 "Sorry! Something went wrong!" 软拦截页。**Amazon 爬取用 ISP Proxies**，不要用 DDC。详见 `references/oxylabs-product-matrix.md`。

3. **凭证不区分协议前缀**：`proxies.json` 里 `http://` 和 `https://` 都能用（爬虫内部走 HTTP CONNECT）。别误用 `socks5://`。

4. **凭证过期/被封 = 静默 0 results**：如果 Amazon 返回 `totalProducts: 0` 且无明显错误，第一反应是代理被 Amazon 软拦截（datacenter）或凭证挂了。先单独跑 `curl -x ddc.oxylabs.io:PORT -U user:pass http://ip.oxylabs.io/location` 验证代理层通不通。

5. **改 `proxies.json` 不再需要重 build**：`Dockerfile` 已经不 `COPY config/`，凭证走 `-e AMAZON_PROXIES` 或挂载 `/app/config/proxies.json`。改 `assets/` 下的代码仍然要 `docker build -t amazon-scraper <skill 目录>`。
6. **`--output` 是容器内路径**：必须 `-v /host/path:/data` 挂载，否则文件在容器内拿不到。
7. **`Accept-Encoding: identity` 头导致详情页加载失败**：原 `createContext` 的 `extraHTTPHeaders` 和 `setExtraHTTPHeaders` 里设了 `Accept-Encoding: identity`，会导致 Amazon 新版详情页 JS 不渲染（`#productTitle` 等 selector 全部 timeout）。已移除该头和整个 `setExtraHTTPHeaders` 调用，详情页恢复正常。
8. **新版 Amazon 详情页 DOM 结构变化**（2026年7月实测）：
   - BSR 不在 `body.innerText` 正则里了，在 `#prodDetails tr` 的 `th/td` 行里（key="Best Sellers Rank", val="#84 in Electronics..."）
   - brand 从 `#bylineInfo` 拿到的是 "Brand: XXX" 或 "Visit the XXX Store"，需清理前缀和后缀
   - seller 从 `#sellerProfileTriggerId` 提取（如 "BeataTap-SKALON"），但部分 ASIN 的 `#sellerProfileTriggerId` 会抓到 Amazon 比价组件的垃圾文本（"different sellers.\nShow details..."），需在分析层过滤
   - `dateFirstAvailable` 在新版页面 **100% 缺失**（Amazon 不再展示此字段），详情页正则和 `#prodDetails tr` 都拿不到
   - 详情页需要 `waitForSelector('#productTitle, #dp', { timeout: 15000 })` + `waitForTimeout(3000)` 才能拿到完整数据
9. **datacenter 代理对 Amazon 详情页 100% 软拦截**（返回空页面），ISP 代理正常。用 `isp.oxylabs.io` 这类 ISP/住宅入口，不要用 `ddc.*` / `disp.*`。
10. **搜索页 `--pages 5` 实际只返回 ~26 个唯一 ASIN**（不是 100）：Amazon 搜索结果含大量广告/重复，拿真正 Top 100 需要更多页或关键词变体。
11. **搜索页翻页参数是 `&page=N` 不是 `&pg=N`**（2026-07-04 修复）：原代码用 `&pg=N` 翻页，Amazon 不认这个参数，每页都返回第一页数据（全是重复），所以 `--pages 10` 只拿到 29 个唯一 ASIN。改成 `&page=N` 后 10 页拿到 234 个唯一 ASIN。如果发现多页爬取结果去重后远少于预期，先检查翻页参数。
12. **批量只能按当前代理条数来**：并发被代码卡成 `min(请求值, 任务数, 代理条数)`，只有 1 条出口时开 5 个容器就是 5 个浏览器打同一个 IP。超过约 10 分钟的批量必须后台跑（前台 600s 会杀掉容器）。要并行，先加不同出口 IP，再给每个容器 `-e AMAZON_PROXIES` 指定各自的出口。合并按 `_source`，不按返回的 `asin`。
13. **CDP Fallback 补漏方案（2026-07-04 验证）**：即使安全加速模式仍有 ~25% ASIN 被软拦截返回 null。**解法**：用本地 Chrome CDP（port 9222）串行补爬失败的 ASIN，成功率 100%。脚本 `scripts/cdp_fallback_scrape.py`，详见 `references/cdp-fallback-strategy.md`。完整流程：Docker 批量（快但有失败）→ 提取失败 ASIN → CDP 串行补漏（慢但 100% 成功）→ 合并结果。

## 反爬能力
- **出口**：按配置的代理条数轮询；失败换下一条；页间隔 1.5s
- **UA**：Linux Chrome 119，对齐 Playwright 1.40 内核（不再写 Mac/Win）
- **端口绑死**：分辨率 / 时区 / 核数；cookie 落 `/data/fingerprint-state/{namespace}/{port}.json`（需 `-v ~/scrapes:/data`）。通用模式按目标域名分 namespace，不和亚马逊共用一个 cookie 罐
- ⚠️ `BY_PORT` 的指纹表只覆盖端口 8001–8005。代理端口不在这个范围时会走 host 哈希的 fallback，所谓"同端口同指纹"实际没生效 —— 换代理商后要同步更新这张表
- **先开首页再跳目标**，同一 page 带 referer
- **不授权 geolocation**
- **无 stealth 插件**（特征库公开，已关掉做 A/B）
- **WebRTC**：`--force-webrtc-ip-handling-policy=disable_non_proxied_udp`，API 在，不走宿主机 UDP
- 轻量 `mouse.move`，不是拟人鼠标库
- Docker 用完即毁；`--no-sandbox` 仍在（容器必需）

这不是红手指分控箱：没有一人一号、没有真实字体/显卡。

## 局限
- 通用模式输出上限10000字符
- Amazon BSR 单 URL 最多 60 个产品（2 页限制），拿 Top 100 用搜索页
- Amazon 单页搜索结果最多约 30-50 个产品
- 不支持需要登录的页面
- Docker 容器启动有冷启动时间（Playwright Chromium）
- Amazon 对 datacenter 代理段主动风控，**Amazon 爬取必须用 ISP / Residential / Mobile 代理**
- **评论抓取不在 Docker 内**：需已登录的 Chrome + CDP（`scripts/scrape_reviews.py`），非匿名页面，详见 `references/reviews-strategy.md`
- **ASIN 详情页返回所有字段为 null**：`status: SUCCESS` + `products[0]` 存在但 `title`/`price`/`rating` 全为 null。两种原因：(1) ASIN 已下架/不可用（换一个有效 ASIN 验证即可区分）；(2) 代理被亚马逊软拦截（503/captcha 页）。用 `curl -x <proxy> -s -o /dev/null -w "%{http_code}" "https://www.amazon.com/dp/<ASIN>"` 检查，正常应返回 200，503 = 代理被拦

## 相关 references
- `references/new-layout-fixes-2026-07.md` — Amazon 新版页面 DOM 变化 + 修复详情（seller 字段、BSR 提取、brand 清理、proxy 切换）
- `references/oxylabs-product-matrix.md` — 哪个 Oxylabs 产品对应哪个入口域名，Amazon 该买哪个
- `references/oxylabs-ddc-format.md` — DDC 故障排查、response code 速查、"代理通 vs 目标拦"判别
- `references/oxylabs-proxy-format.md` — 通用 Oxylabs 代理格式 + 验证命令
- `references/bsr-top100-strategy.md` — BSR 60 个上限 + 拿 Top 100 的三种策略
- `references/search-page-title-fix.md` — 搜索页 `title: null` 根因 + 已合入的修复 + 重 build 步骤
- `references/product-form-fusion.md` — 视觉化选品 / 产品形态融合创意（vision_analyze fallback）
- `references/sharing-checklist.md` — 打包分享前的凭证安全检查
- `references/reviews-strategy.md` — 评论页抓取策略（瀑布流模式 + CDP page WS + 选择器参考）
- `references/batch-parallel-scraping.md` — 批量详情页并行爬取模式（5 容器 × 独立代理端口 × 低并发）
- `scripts/scrape_reviews.py` — 可直接运行的评论抓取脚本（CDP + 瀑布流 + SQLite 存储）
- `scripts/asin_price_monitor.py` — 每日竞品 ASIN 价格监控脚本，用 `openclaw automations` 的 command 定时跑，不另起一轮模型。stdout 可推到 Discord/Telegram。含价格变化检测。修改 ASINS 列表增删监控目标
- `scripts/cdp_fallback_scrape.py` — CDP 补漏脚本：当 Docker 代理批量爬取被软拦截时，用本地 Chrome CDP 串行补爬失败 ASIN，成功率 100%。详见 `references/cdp-fallback-strategy.md`
- `scripts/pickleball_price_monitor.py` — 多 ASIN 价格监控模板（Docker 爬虫 + SQLite + 飞书多维表格 + Discord 推送），用 OpenClaw automation 定时跑
- `references/cron-price-monitor-pattern.md` — 价格监控定时任务：OpenClaw automations + 飞书多维表格 + Discord，含时区和 lark-base 字段类型注意事项
- `references/cdp-fallback-strategy.md` — CDP Fallback 完整策略：前置条件、使用方法、Docker+CDP 两阶段工作流
