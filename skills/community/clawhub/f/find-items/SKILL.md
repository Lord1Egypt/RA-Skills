---
name: find-items
description: Search for products on Chinese e-commerce platforms (Taobao, JD, Vipshop, PDD, Meituan, Ele.me, etc.) using web search. This skill helps users find products, compare prices, and get recommendations from major shopping platforms.
version: 1.0.2
---

# Find Items

This skill helps you search for products on major Chinese e-commerce platforms.

## Supported Platforms

| Platform | Type | Best For |
|----------|------|----------|
| 淘宝 (Taobao) | C2C/B2C | Variety, price comparison |
| 京东 (JD) | B2C | Electronics, fast delivery |
| 唯品会 (Vipshop) | B2C | Brand discounts, fashion |
| 拼多多 (PDD) | C2M | Low prices, group buying |
| 天猫 (Tmall) | B2C | Brand stores, quality |
| 苏宁易购 (Suning) | B2C | Appliances, electronics |
| 美团 (Meituan) | O2O | Local services, food delivery |
| 饿了么 (Ele.me) | O2O | Food delivery |
| 抖音商城 (Douyin) | Social commerce | Live shopping, trends |
| 小红书 (Xiaohongshu) | Social commerce | Reviews, lifestyle |

## When to Use This Skill

Use this skill when the user:

- Asks "搜索[商品]" or "找[商品]"
- Wants to compare prices across platforms
- Needs product recommendations
- Asks "哪里买[商品]便宜"
- Wants to find specific items with filters (price, brand, etc.)

## How It Works

### Step 1: Understand the Request

Identify:
1. Product name/keywords
2. Preferred platform (if specified)
3. Filters: price range, brand, specifications
4. Sort preference: price, rating, sales

### Step 2: Construct Search Query

Build a search query with platform and product:

```
{platform} {product} {filters}
```

Examples:
- "淘宝 iPhone 16 价格"
- "京东 索尼耳机 降噪"
- "唯品会 耐克运动鞋 折扣"
- "拼多多 纸巾 便宜"

### Step 3: Execute Search

Use web search to find current product information:

```bash
# Using agent-reach or similar search capability
web_search "{query}"
```

### Step 4: Parse and Present Results

Format results with:
- Product name and image
- Price (with platform comparison if multiple)
- Store/seller info
- Rating/reviews
- Direct links

## Command Usage

```bash
# Basic search
find-items search "iPhone 16" --platform taobao

# Search with filters
find-items search "运动鞋" --platform jd --max-price 500 --brand nike

# Compare across platforms
find-items compare "MacBook Pro" --platforms taobao,jd,pdd

# Get deals/discounts
find-items deals "化妆品" --platform vipshop
```

## Example Output

```
🔍 搜索结果：iPhone 16 256GB

📱 淘宝/天猫
   💰 ¥5,999 - ¥6,299
   🏪 Apple官方旗舰店
   ⭐ 4.9/5 (12,345条评价)
   🔗 https://detail.tmall.com/...

📱 京东
   💰 ¥5,899 (百亿补贴)
   🏪 京东自营
   ⭐ 4.8/5 (8,234条评价)
   🔗 https://item.jd.com/...

📱 拼多多
   💰 ¥5,699 (拼团价)
   🏪 品牌授权店
   ⭐ 4.7/5 (5,678条评价)
   🔗 https://mobile.yangkeduo.com/...

💡 价格对比：拼多多最便宜 (省¥300)
💡 物流速度：京东最快 (当日达)
💡 售后保障：天猫/京东官方店最优
```

## Platform-Specific Tips

### 淘宝/天猫
- Use "天猫" for brand stores
- Check "淘宝特价版" for lower prices
- Look for "天猫超市" for daily goods

### 京东
- "京东自营" = JD's own inventory, fastest delivery
- "京东物流" = JD delivery network
- "百亿补贴" = subsidized prices

### 拼多多
- "品牌" tag = authorized sellers
- "百亿补贴" = official subsidies
- Group buying for extra discounts

### 唯品会
- Flash sales, limited time
- Brand focus
- Check "即将售罄" for best deals

## Search Filters

| Filter | Options | Example |
|--------|---------|---------|
| --platform | taobao, jd, pdd, vipshop, tmall | --platform jd |
| --min-price | Number | --min-price 100 |
| --max-price | Number | --max-price 500 |
| --brand | Brand name | --brand nike |
| --sort | price-asc, price-desc, sales, rating | --sort price-asc |
| --condition | new, used, refurbished | --condition new |

## Implementation Notes

This skill uses web search to gather real-time product information. Results are:
- Current as of search time
- From official platform pages
- May include affiliate links
- Prices subject to change

## Security Updates

### v1.0.2
- Changed shebang from `#!/bin/bash` to `#!/bin/sh` for POSIX compliance
- Fixed `get_platform_name` to return empty string for invalid platforms instead of echoing input
- Improved `is_safe_string` validation with more dangerous characters
- Used `tr` instead of `IFS` for safer string splitting
- Removed all local variable declarations (not POSIX)
- Used underscore-prefixed variable names to avoid conflicts

### v1.0.1
- Fixed potential shell compatibility issues
- Added input validation for all parameters
- Added platform whitelist validation
- Improved dangerous character filtering
- Replaced bash-specific syntax with POSIX-compatible alternatives

## Author & License

OpenClaw Skill - MIT License
