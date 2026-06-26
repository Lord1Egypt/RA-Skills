---
name: cn-online-shopping
description: China E-Commerce Shopping Guide - Focused on recommending mainstream Chinese e-commerce platforms such as Taobao, Tmall, JD.com, and Pinduoduo. Based on product category, price budget, and logistics needs, recommend the most suitable domestic shopping platform for users. Provide platform feature comparisons, shopping timing advice, and pitfalls to avoid.
---

⚠️ **Disclaimer**: This skill's platform recommendations are for reference only and do not constitute purchase advice. When shopping, please verify platform information, seller credibility, and product details yourself. We are not responsible for any purchasing decisions.

# China E-Commerce Shopping Guide

## Overview

This skill helps users intelligently recommend the most suitable Chinese e-commerce platforms based on product category, budget, and logistics needs.

## Supported Platforms

- **Taobao** - C2C platform, widest product range, flexible pricing
- **Tmall** - B2C platform, authentic brands, many flagship stores
- **JD.com** - Fast self-logistics, authentic guarantee, good after-sales
- **Pinduoduo** - Extremely low prices, billions in subsidies, direct agricultural shipping
- **Douyin Mall** - Live streaming sales, short video product recommendations
- **Xiaohongshu** - Product review community, authentic reviews, quality精选
- **Suning** - Home appliances specialty, in-store pickup
- **Vipshop** - Brand flash sales, strong discounts

## Triggers

- "I want to buy something on Taobao"
- "JD.com vs Taobao, which is better"
- "Is Pinduoduo reliable"
- "Which platform for home appliances"
- "Which platform is better for buying..."
- "Recommend a website for buying..."
- "Compare...platforms"
- "China e-commerce platform recommendations"

## Workflow

1. **Identify user's shopping needs** (product category, budget, time requirements, etc.)
2. **Call cn-online-shopping.py** to get platform recommendations or comparisons
3. **Present recommendation results**, including recommendation reasons, best choices, and precautions
4. **For detailed guidance**, reference documents under references/

## Usage

```bash
# Recommend platform based on product
python3 cn-online-shopping.py recommend <product name/category>

# List supported categories
python3 cn-online-shopping.py categories

# Compare two platforms
python3 cn-online-shopping.py compare <platform1> <platform2>
```

## Data Files

- `data/platforms.json` - Platform information (features, applicable regions, advantage categories)
- `data/categories.json` - Product category mapping
- `data/regions.json` - Regional recommendation configuration

## References

- `references/platform-guide.md` - Detailed platform guide
- `references/shopping-tips.md` - Shopping tips and precautions

## Limitations

- Only provides platform recommendation information, no real-time price queries
- Does not access real-time data from any shopping platform
- Recommendations based on preset rules and static data
- Platform policies and fees may change at any time; please refer to official information