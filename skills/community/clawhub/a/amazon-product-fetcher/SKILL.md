---
name: amazon-product-fetcher
description: Fetch complete Amazon product data including title, current price, currency, star rating, review count, availability, main image, and product URL. Works from an Amazon URL or ASIN. No API key required. Trigger when asked to "get Amazon product info", "fetch Amazon price", "look up product on Amazon", "what does X cost on Amazon".
version: 1.0.0
license: MIT
metadata: {"openclaw": {"emoji": "🛒", "requires": {"bins": []}}}
---

# Amazon Product Fetcher 🛒

从 Amazon 公开商品页面抓取完整商品数据，**无需任何 API Key**，纯 Python 标准库。

## When to Use

- "Get the details for this Amazon product: [URL]"
- "What's the price of ASIN B0XXXXXXXX on Amazon?"
- "Fetch product info from amazon.com/dp/B0XXXXXXXX"
- "Look up [product] on Amazon and tell me the price"

## Quick Start

```bash
# 通过 URL
python scripts/fetch.py --url "https://www.amazon.com/dp/B0CX44VMKZ"

# 通过 ASIN
python scripts/fetch.py --asin B0CX44VMKZ

# JSON 格式输出
python scripts/fetch.py --asin B0CX44VMKZ --json
```

## Output Fields

| 字段 | 说明 |
|------|------|
| `asin` | Amazon 商品编号 |
| `title` | 商品标题 |
| `price` | 当前价格数字 |
| `currency` | 货币符号（如 `$`、`€`） |
| `rating` | 星级评分（如 `4.5`） |
| `reviews` | 评论数量 |
| `availability` | 库存状态 |
| `image_url` | 主图 URL |
| `product_url` | Amazon 商品链接 |

## No API Key Needed

直接解析 Amazon 公开商品页面 HTML。使用真实浏览器 User-Agent 避免被屏蔽。

> **提示：** Amazon 偶尔会返回 CAPTCHA 页面。若出现此情况，稍后重试即可。大批量抓取请使用 `skill-amazon-spapi`（需要卖家凭证）。

## Configuration (openclaw.json)

无需配置 API Key。可选配置：

```json
{
  "skills": {
    "entries": {
      "amazon-product-fetcher": {
        "enabled": true
      }
    }
  }
}
```

## Troubleshooting

| 问题 | 解决方案 |
|------|----------|
| 价格为空 | Amazon 可能使用了不同的价格 widget；重试一次 |
| CAPTCHA / 503 | 等待 30 秒后重试 |
| 无法从 URL 提取 ASIN | 改用 `--asin` 直接传入 |