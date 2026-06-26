# 📡 API 与数据源清单

本技能使用的公开 API 和数据源（按优先级排序）

## 🔍 域名/官网验证类

| 服务 | URL/说明 | 用途 | 费用 |
|------|----------|------|------|
| **DomainTools WHOIS** | `https://whois.domaintools.com/` | 查询域名注册时间 | $10-20/次 |
| **Wayback Machine** | `web.archive.org/web/begin/$domain` | 官网历史快照 | 免费（限流）|
| **Who.is** | `who.is/domain.com` | WHOIS 替代方案 | 免费 |
| **DNSlytics** | `dnslytics.com/` | 域名年龄 + 流量分析 | 有免费版 |

## 📰 新闻媒体类

| 服务 | URL/说明 | 用途 | 费用 |
|------|----------|------|------|
| **Google News API** | `news.google.com` | 全球新闻搜索 | 需 API Key |
| **NewsAPI.org** | `https://newsapi.org/` | 主流媒体聚合 | $0-549/月 |
| **Tavily Web Search** | `tavily.com/search` | 智能搜索引擎 | $100=1000 次调用|
| **Reddit** | `reddit.com/search?q=` | 社区讨论热度 | 免费（限流）|

## 🛒 跨境电商平台类

| 平台 | 搜索 URL | 用途 | 费用 |
|------|----------|------|------|
| **Amazon US** | `amazon.com/gp/bestsellers` | 品牌销售排名 | 需登录/爬虫工具|
| **Amazon Global Selling** | `global.amazon.com/` | 海外站点对接 | 免费查看公开数据|
| **eBay** | `ebay.com/sch.i=http://schop.ebaysrv.com` | 多站点对比 | 需登录 |
| **AliExpress** | `aliexpress.com/wholesale=brand-name` | 品牌分销商列表 | 免费 |

## 🏪 实体店搜索类

| 服务 | URL/说明 | 用途 | 费用 |
|------|----------|------|------|
| **Google Places API** | `maps.google.com/maps?q=` | 实体店位置查询 | $120/月 (基础版)|
| **Yelp Fusion API** | `api.yelp.com/v3/businesses/search` | 北美店铺信息 | 免费 - 付费 |
| **Shopify Store Directory** | `shopify.store/` | Shopify 电商目录查询 | 免费 |

## 📱 社交媒体类

| 服务 | URL/说明 | 用途 | 费用 |
|------|----------|------|------|
| **Instagram Graph API** | `developers.facebook.com/docs/instagram-api` | Instagram 官方业务账号验证 | $10-50/月|
| **Twitter/X API v2** | `api.twitter.com/2/search` | X (Twitter) 品牌提及追踪 | $100-4000/月|
| **Facebook Graph API** | `graph.facebook.com/v18.0/` | Facebook 页面审核状态 | 免费 |

## 🌐 社交媒体热度监控（免费方案）

### 使用 Python requests + BeautifulSoup 抓取：

```python
# Reddit 搜索示例（无需 API Key）
def check_reddit_mentions(brand):
    url = f"https://www.reddit.com/search?q={brand}+official+brand"
    headers = {"User-Agent": "Mozilla/5.0 (fake-international-brand-detector)"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all("article")[:10]  # 前 10 条
    return {
        "reddit_posts": len(posts),
        "sample_urls": [p.get("href") for p in posts if p.get("href")]
    }
```

## 📊 推荐 API 账户配置

### Tavily Web Search (已在使用)
- **基础计划**: $100/月 = 1000 次调用 ✅
- **使用率**: 3%/月 (非常充裕)
- **用途**: 国际政治新闻主要来源
- **可复用**: 品牌搜索、科技新闻等场景

### Google News API (需新注册)
- **基础计划**: $5/月
- **速率**: 1000 请求/天
- **用途**: 全球新闻聚合搜索
- **配置**: 需登录 news.google.com 获取 RSS/API 权限

## 🧪 免费替代方案（测试阶段）

| 需求 | 推荐工具 | 说明 |
|------|----------|------|
| WHOIS | `whois.domaintools.com` (手动查询) | 复制粘贴到网页查询 |
| 新闻搜索 | Google Custom Search API 免费版 | 需创建自定义搜索引擎 |
| Reddit 搜索 | `reddit.com/search` (无头浏览器) | 绕过登录限制 |

## 🔐 合规性提醒

1. **遵守 robots.txt** - 各站点文件规定的爬虫规则
2. **API Key 安全** - 不要硬编码到代码中，使用环境变量
3. **速率限制** - 大多数 API 有限流机制（每分钟 1-5 次）
4. **数据保留** - 仅保存必要信息，建议不超过 7 天

## 📝 典型调用示例

```bash
# 使用 Tavily API 搜索品牌新闻
TAVILY_API_KEY=your_key python3 scripts/detect_brand.py \
    --brand "Nike" \
    --tavily-api-key "$TAVILY_API_KEY"

# 使用 Google Custom Search
GCS_API_KEY=your_key CUSTOM_SEARCH_ENGINE_ID=engine_id
python3 scripts/search_news.py \
    --url https://news.google.com/rss/search?q=$brand&ceid=US:2124 \
    --api-key $GCS_API_KEY
```

## 📊 性能基准

| API | QPS (每秒) | 平均延迟 | 成本/调用 |
|-----|------------|----------|----------|
| Tavily | ~0.1 | 2-3s | $0.001 |
| Google News API | ~0.5 | 1-2s | $0.04 |
| Reddit (无头) | ~0.2 | 3-5s | 免费（但限流）|

## 🔧 维护建议

1. **每季度审查** - 检查 API 可用性变化
2. **备用方案** - 为每个核心功能准备至少 2 个数据源
3. **监控日志** - `/home/admin/.openclaw/workspace/logs/api-errors.log`

---

*最后更新：2026-03-17*
