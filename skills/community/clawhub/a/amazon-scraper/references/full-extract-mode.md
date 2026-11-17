# Full Extract Mode — 43字段全量抓取

> `scripts/full_extract.js` — 独立于 `amazon_handler.js` 的全量提取脚本

## 什么时候用

- 用户说"爬取页面里所有内容"、"最大化字段"、"所有可见字段"、"完整抓取"
- 需要原来 15 个字段之外的数据：划线价、评分分布、全部图片、视频、A+内容、评论摘要、变体、优惠券、交付时间等
- 需要分析竞品 Listing 全貌（不只看价格/评分）

## 用法

```bash
docker run --rm \
  -v ~/.openclaw/skills/amazon-scraper/scripts/full_extract.js:/app/full_extract.js \
  amazon-scraper node /app/full_extract.js "https://www.amazon.com/dp/ASIN/"
```

## 抓取的 43 个字段

| 分类 | 字段 | 说明 |
|---|---|---|
| **基本信息** | title, asin, brand, brandUrl | 标题/ASIN/品牌/品牌店铺链接 |
| **价格** | prices.main, prices.listPrice, prices.dealPrice, prices.buybox, prices.allPriceElements | 主价/划线价/优惠价/buybox/所有价格元素 |
| **评分评论** | rating, ratingText, reviews, reviewsText, ratingHistogram | 评分/评分数/评分分布直方图 |
| **图片** | images[main/thumbnail/hires/aplus] | 全部图片分类标记 |
| **视频** | videos[video] | 含poster帧 |
| **五点描述** | bullets, bulletsCount | 完整五点 |
| **A+内容** | aplusContent, aplusLength | A+文本和长度 |
| **详情表** | details (20+ keys), detailsCount | 技术规格键值对 |
| **BSR** | bsr, bsrFullText | BSR数字+含分类排名全文 |
| **分类** | category, categoryFull | 面包屑/完整路径 |
| **销量** | boughtPastMonth | 月销量 |
| **日期** | dateFirstAvailable | 上架日期（常为null） |
| **卖家** | seller, shipsFrom, fulfilledBy | 卖家/发货方/FBA |
| **库存** | availability, isPrime, delivery | 库存状态/Prime标记/预计送达 |
| **促销** | coupon, subscribeAndSave | 优惠券/订阅优惠 |
| **变体** | variations (allOptions, allAsins) | 颜色/尺寸选项+变体ASIN |
| **推荐** | frequentlyBoughtTogether, carousels | FBT/关联推荐 |
| **Q&A** | customerQA | 客户问答 |
| **评论** | topReviews[8] | 顶部评论（作者/评分/标题/日期/正文/verified/有用数） |
| **安全** | safetyWarning, newerVersion | 安全警告/新版提示 |
| **元数据** | metaTags, canonicalUrl, pageUrl | 页面meta/规范URL |
| **结构化** | structuredData (JSON-LD) | 结构化数据 |
| **全文** | fullPageText | 整页纯文本（截断2万字） |

## 与 amazon_handler.js 对比

| 维度 | amazon_handler.js | full_extract.js |
|---|---|---|
| 字段数 | 15 | 43 |
| 价格 | 仅 price/priceStr | 划线价/deal价/buybox/全部价格元素 |
| 图片 | 仅1张主图 | 全部图片（main/thumb/hires/aplus分类） |
| 视频 | 无 | 有（含poster） |
| 评论 | 仅 rating + reviews 数 | 8条顶部评论（含作者/日期/正文/verified） |
| A+内容 | 无 | 有 |
| 变体 | 无 | 有（选项+变体ASIN） |
| 交付/库存 | 无 | availability/isPrime/delivery |
| 优惠券 | 无 | 有 |
| 输出大小 | ~3KB | ~85KB |

## 注意事项

1. **proxy日志混入stdout首行**：`full_extract.js` 的 stdout 第一行可能是 `Using proxy: ...`，解析JSON时从第一个 `{` 开始截取
2. **容器内代理路径**：硬编码为 `/app/config/proxies.json`，不是 `__dirname/../config/`
3. **懒加载**：需要8次滚动 + 1秒等待才能加载全部图片和A+内容
4. **偶发超时**：`waitForSelector('#productTitle, #dp', { timeout: 15000 })` 偶尔超时，重试即可（代理轮换）
5. **dateFirstAvailable 常为 null**：Amazon 新版页面不再展示此字段
6. **canonicalUrl 可能指向变体ASIN**：如 `B0F6XSV7XB` 的 canonical 指向 `B0GY92641V`（父ASIN）
