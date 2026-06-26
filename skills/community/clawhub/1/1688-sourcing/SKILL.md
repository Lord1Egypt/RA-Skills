# 1688 Sourcing Assistant

Find suppliers on 1688.com, calculate profit margins, and generate multi-platform product listings for e-commerce sellers. Use when: (1) User wants to source products from China, (2) User wants to calculate profit margins, (3) User wants to find 1688 suppliers for a product, (4) User wants to generate listing content for Take.app / Shopify / IG / TikTok / XiaoHongShu.

Trigger on: "find supplier", "source product", "1688", "profit margin", "calculate profit", "sourcing", "wholesale price", "dropship", "listing content", "product research", "找貨源", "毛利", "1688搜尋", "上架".

## Overview

This skill helps e-commerce sellers and dropshippers source products from China wholesale platform 1688.com, calculate accurate profit margins, and generate ready-to-publish product listings across multiple platforms.

Designed for: solo sellers, micro e-commerce operators, dropshippers, and anyone selling products sourced from 1688 or Chinese wholesale suppliers.

## Step 1: Product Research and 1688 Supplier Search

When the user provides a product name, keyword, or URL from XiaoHongShu/TikTok/Instagram:

Extract key product info:
- Product name and category
- Key selling points and features
- Target audience
- Approximate retail price in target market

Generate 1688 search strategy:

SEARCH KEYWORDS - provide 3 variations:
- Chinese keyword 1: most accurate translation
- Chinese keyword 2: alternative keyword
- Chinese keyword 3: category plus descriptor

DIRECT 1688 SEARCH LINKS:
- https://s.1688.com/selloffer/offerlist.htm?keywords=KEYWORD_1
- https://s.1688.com/selloffer/offerlist.htm?keywords=KEYWORD_2

IMAGE SEARCH: Go to https://www.1688.com and use the camera icon to upload a product photo for visual search.

RECOMMENDED FILTERS ON 1688:
- 实力商家 (Verified suppliers)
- 货期 3-7天 (3-7 day lead time)
- Check MOQ carefully before contacting

Supplier evaluation checklist:
- Shop rating above 4.5/5
- Transaction volume over 100 orders
- Response rate above 90%
- Photos show real product not stock images
- Offers sample orders
- Has export and shipping experience

## Step 2: Profit Margin Calculator

When user provides pricing data, calculate full profit breakdown.

Input required:
- PRODUCT COST from 1688 in CNY
- SHIPPING TO WAREHOUSE per unit in CNY
- IMPORT / CUSTOMS DUTY percentage
- PLATFORM FEE percentage
- PAYMENT PROCESSING FEE default 2.5%
- SELLING PRICE
- CURRENCY: HKD / MOP / USD / SGD

Profit calculation:

Total Cost per Unit equals Product Cost converted to local currency plus Shipping Cost per Unit plus Import Duty plus Platform Fee plus Payment Processing Fee plus Packaging if applicable.

Gross Profit equals Selling Price minus Total Cost per Unit.
Gross Margin percent equals Gross Profit divided by Selling Price times 100.

MARGIN HEALTH CHECK:
- Margin above 50% = Excellent
- Margin 35-50% = Good
- Margin 20-35% = Acceptable, monitor costs
- Margin below 20% = Risky, reconsider pricing

Always output a clean breakdown table showing each cost line item, total cost, selling price, gross profit, and gross margin percentage.

CURRENCY REFERENCE (approximate):
- CNY 1 = HKD 1.10
- CNY 1 = MOP 1.13
- CNY 1 = USD 0.14
- CNY 1 = SGD 0.18
- Check live rates at https://www.xe.com/currencyconverter/

## Step 3: Reorder and Replenishment Planning

Reorder point formula:
Reorder Point = (Average Daily Sales x Lead Time Days) + Safety Stock

Example: Selling 5 units per day, lead time 14 days, safety stock 15 units. Reorder Point = (5 x 14) + 15 = 85 units remaining means place order now.

Supplier WhatsApp/WeChat message template in English:

Hi [Supplier], I would like to reorder: Product: [Name], 1688 Link: [URL], Quantity: [X] units, Shipping: [Express/Sea], Destination: [City, Country]. Please confirm: 1. Stock availability, 2. Unit price for this quantity, 3. Estimated ship date, 4. Total cost including shipping. Thank you!

Supplier message template in Chinese:

你好！我想再订购以下产品：产品：[名称]，链接：[1688链接]，数量：[X]件，发货方式：[快递/海运]，目的地：[城市]。请确认：1. 现货情况，2. 该数量单价，3. 预计发货日期，4. 含运费总价。谢谢！

## Step 4: Multi-Platform Listing Generator

Generate ready-to-publish content from a single product brief.

Take.app and Shopify Product Description format:
TITLE: [Product Name] - [Key Benefit]
DESCRIPTION: 2-3 sentences covering what it is, who it is for, and key benefit.
List 4 key features.
Include shipping info and WhatsApp/Contact CTA.
PRICE: [Currency][Price]

Instagram and Threads Caption in English:
Start with a hook - bold statement or question.
2-3 lines of product description.
Price and DM to order or link in bio.
5-8 relevant hashtags.

XiaoHongShu Caption in Chinese:
标题：带emoji，吸引眼球
种草文：2-3段，口语化，描述使用场景
列出3个卖点
售价和购买方式
5个相关话题标签

TikTok and Reels 30-second Script:
0-3s HOOK: Attention-grabbing opening line
3-8s PROBLEM: Most people struggle with [problem]
8-18s SOLUTION: That is why [product] - [key benefit]
18-25s FEATURES: Quick showcase of 2-3 features
25-30s CTA: Link in bio or comment keyword to order

## Step 5: Common Sourcing Mistakes to Avoid

- Ordering too much on first order. Always test with minimum 30-50 units first.
- Ignoring shipping costs. 1688 prices look cheap but China shipping can double your landed cost. Always calculate DDP Delivered Duty Paid.
- Not requesting samples. Order 1-2 samples before bulk order to verify quality.
- Choosing by price alone. Balance price with supplier rating and transaction history.
- Single supplier dependency. Always identify 2-3 backup suppliers for best-sellers.
- No quality inspection. For orders over 200 units consider a third-party QC service.

## Platform Tips

Take.app tips:
- Product titles under 60 characters
- Square images 1:1 ratio for best display
- Enable WhatsApp checkout for frictionless orders
- Add LOW STOCK tag when under 5 units remain

Testing demand before ordering:
- Post product on Instagram Stories with a poll asking Would you buy this
- Count DMs and interest before committing to stock
- Set up a pre-order first then place the 1688 order
