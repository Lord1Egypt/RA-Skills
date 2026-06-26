# DOM 选择器映射表

> 选择器权威来源是 `scripts/selector_registry.py`。本表是可读参考，便于人工复核。
> 当 selector_registry.py 更新后，本表也应同步更新。

## Amazon 页面原生选择器

| 字段 | 主选择器 | 备用选择器 | 验证状态 |
|------|----------|------------|----------|
| 产品标题 | `#productTitle` | `h1.a-size-large`, `[data-feature-name='title'] h1` | ✅ |
| 当前售价 | `.a-price .a-offscreen` | `#priceblock_ourprice`, `#priceblock_dealprice`, `#priceblock_saleprice`, `.a-price-whole` | ✅ |
| 评论数量 | `#acrCustomerReviewText` | `#reviewsMedley .a-size-base` | ✅ |
| 评论星级 | `#acrPopover` | `.a-icon-star`, `[data-feature-name='averageCustomerReviews'] .a-icon-alt` | ✅ |
| 产品主图 | `#imgTagWrapperId img` | `.a-carousel .a-carousel-card img`, `#main-image` | ✅ |
| List Price | `.a-text-price` | `[aria-label*="List Price"]`, `.a-price.a-text-price` | ✅ |
| 店铺名/Sold by | `#sellerProfileTriggerId` | `[id*="soldBy"]`, `#tabular-buybox-trt-seller .tabular-buybox-text` | ✅ |
| 卖点 | `#feature-bullets` | `.a-unordered-list.a-vertical` | ✅ |
| 图片 | `#imageBlock` | `.a-carousel` | ✅ |
| A+内容 | `#aplus` | `.aplus-v2`, `[id*='aplus']` | ✅ |
| 视频 | `video` | `[data-video-url]`, `[class*='video']` | ✅ |
| Review分布 | `#histogramTable` | `#reviews-medley .a-histogram`, `[data-hook='histogram-table']` | ✅ |
| 品牌 | `#bylineInfo` | `[data-feature-name='brandName']`, `[id*='brand']`, `a#bylineInfo` | ✅ |
| 产品详情 | `#detailBulletsWrapper_feature_div` | `#detailBullets_feature_div`, `#productDetails`, `#productDetails_db_sections` | ✅ |
| 变体 | `#variation_color_name li img` | `#twister li img`, `[id*='variation'] li img`, `#twister .swatch` | ✅ |
| 活动标识 | `#dealBadge_feature_div` | `.dealBadge`, `.couponBadge`, `[class*='deal']`, `[class*='coupon']` | ✅ |

## 卖家精灵插件选择器

| 字段 | 选择器 | 提取方式 |
|------|--------|---------|
| 插件容器 | `#seller-sprite-extension-quick-view-listing` | JS innerText → Python 正则 |
| 品牌 | 同上容器 | 正则: `品牌[：:]\s*(.+)` |
| 卖家 | 同上容器 | 正则: `卖家[：:]\s*(.+)` |
| FBA 费 | 同上容器 | 正则: `FBA费用[：:]\s*\$?([\d.]+)` |
| 毛利率 | 同上容器 | 正则: `毛利率[：:]\s*([\d.]+)%?` |
| 上架时间 | 同上容器 | 正则: `上架时间[：:]\s*(\d{4}-\d{2}-\d{2})` |
| 30天销量(父) | 同上容器 | 正则: `近30天销量\(父体\)[：:]\s*([\d,]+)` |
| 30天销量(子) | 同上容器 | 正则: `近30天销量\(子体\)[：:]\s*([\d,+]+)` |
| 销售额 | 同上容器 | 正则: `销售额[：:]\s*\$?([\d,]+)` |
| 变体数 | 同上容器 | 正则: `变体数[：:]\s*(\d+)` |
| 重量 | 同上容器 | 正则: `商品重量[：:]\s*(.+)` |
| 尺寸 | 同上容器 | 正则: `商品尺寸[：:]\s*(.+)` |
| 全部流量词 | 同上容器 | 正则: `全部流量词[：:]\s*([\d,]+)` |
| 自然搜索词 | 同上容器 | 正则: `自然搜索词[：:]\s*([\d,]+)` |
| 广告流量词 | 同上容器 | 正则: `广告流量词[：:]\s*([\d,]+)` |
| BSR 排名 | 同上容器 | 正则: `#\d+ in [^\n]+` |

## SIF 插件选择器

| 字段 | 选择器 | 提取方式 |
|------|--------|---------|
| 插件容器 | `[data-sif-container]` | JS innerText → Python 正则 |
| 备用 | `.sif-extension-container`, `[class*='sif-']` | 同上 |

## 选择器变更记录

| 日期 | 字段 | 变更 | 原因 |
|------|------|------|------|
| 2026-05-26 | 全部 | 初始化 | 首次固化 |
