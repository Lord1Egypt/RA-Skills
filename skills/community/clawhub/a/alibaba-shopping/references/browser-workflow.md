# Browser Workflow for Alibaba Shopping

This document describes the browser automation workflow for Taobao, Tmall, and 1688 shopping.

## Overview

The browser workflow enables agent-assisted shopping on Alibaba ecosystem platforms while maintaining strict boundaries around user-controlled actions.

## Authentication Levels

### Level 1: Public Pages (No Login Required)
- Product search
- Product detail pages
- Public reviews
- Price comparison
- Store information

### Level 2: User Pages (Login Required)
- Shopping cart operations
- Coupon application
- Address selection
- Order generation
- Personal recommendations

### Level 3: Blocked (User Only)
- Payment execution
- Final order submission
- Password/CAPTCHA entry

## Workflow Phases

### Phase 1: Discovery
**Purpose**: Find and compare products without authentication

**Steps**:
1. Navigate to platform (taobao.com, tmall.com, 1688.com)
2. Enter search query
3. Apply filters (price, rating, sales)
4. Extract top results
5. Compare options

**Key Data Points**:
- Product title
- Current price / original price
- Monthly sales volume
- Store type badge
- Store rating
- Review count
- Main image URL

**Example**:
```
openclaw browser goto https://s.taobao.com/search?q=iPhone+16
openclaw browser snapshot
# Extract: title, price, sales, shop_name, shop_type, rating
```

### Phase 2: Selection
**Purpose**: Deep dive into chosen product

**Steps**:
1. Open product detail page
2. Extract full specifications
3. Read sample reviews
4. Check available variants
5. Calculate final price

**Key Data Points**:
- Full product description
- All available SKUs/variants
- Variant-specific pricing
- Coupon availability
- Shipping cost
- Delivery estimate
- Review highlights
- Buyer photos

**Example**:
```
openclaw browser goto [product_url]
openclaw browser snapshot
# Extract: specs, variants, coupons, shipping
```

### Phase 3: Cart & Pre-Order
**Purpose**: Prepare order (requires login)

**Steps**:
1. Confirm login status
2. Add item to cart
3. View cart contents
4. Apply available coupons
5. Select delivery address
6. Calculate final total
7. Generate order preview

**Key Data Points**:
- Cart subtotal
- Applied discounts
- Shipping cost
- Final total
- Delivery address
- Available payment methods

**Login Check**:
```
openclaw browser goto https://cart.taobao.com/cart.htm
# Check if redirected to login page
# If yes: prompt user to login first
# If no: proceed with cart operations
```

### Phase 4: Handoff
**Purpose**: Transfer control to user for payment

**Steps**:
1. Present complete order summary
2. Confirm all details with user
3. Provide manual payment instructions
4. Wait for user confirmation

**Order Summary Template**:
```
📋 订单预览
━━━━━━━━━━━━━━━━━━━━
商品: [Product Name]
规格: [Variant]
数量: [Quantity]

价格明细:
  商品金额: ¥[Amount]
  运费: ¥[Shipping]
  优惠券: -¥[Discount]
  ─────────────────
  应付总额: ¥[Total]

收货地址: [Address]
配送方式: [Shipping Method]
━━━━━━━━━━━━━━━━━━━━

👉 请手动完成支付：
1. 打开淘宝/天猫 App
2. 进入购物车
3. 点击结算
4. 确认订单信息
5. 选择支付方式并完成付款
```

## Platform-Specific Notes

### Taobao (淘宝)
- URL: taobao.com
- Search: s.taobao.com
- Cart: cart.taobao.com
- Login often required for price details
- Mobile site may have different structure

### Tmall (天猫)
- URL: tmall.com
- Search: list.tmall.com
- Cart: Shared with Taobao
- More structured product pages
- Better API-like data in HTML

### 1688
- URL: 1688.com
- Search: s.1688.com
- MOQ information critical
- Wholesale pricing tiers
- Different review system
- Often requires contact for shipping quotes

## Data Extraction Priority

When extracting product information, prioritize in this order:

1. **Identity**: Title, product ID, store name
2. **Pricing**: Current price, original price, unit price
3. **Trust**: Store type, rating, sales volume, review count
4. **Logistics**: Shipping cost, origin, delivery estimate
5. **Promotions**: Coupons, discounts, bulk pricing
6. **Variants**: Available options, variant pricing
7. **Reviews**: Rating distribution, recent comments, photos

## Error Handling

### Login Required
```
If page redirects to login:
  → Ask user to login first
  → Provide manual instructions
  → Resume after confirmation
```

### CAPTCHA
```
If CAPTCHA appears:
  → Stop automation
  → Hand to user
  → Resume after solved
```

### Price Mismatch
```
If extracted price differs significantly from expected:
  → Flag for verification
  → Re-extract with fresh snapshot
  → Confirm with user before proceeding
```

### Out of Stock
```
If variant unavailable:
  → Check alternative variants
  → Notify user
  → Get confirmation before proceeding
```

## Safety Checklist

Before any action:
- [ ] Confirm user intent
- [ ] Verify current page state
- [ ] Check for required login
- [ ] Announce action to user

After any action:
- [ ] Confirm action completed
- [ ] Snapshot result
- [ ] Extract key data
- [ ] Present summary to user

Before handoff:
- [ ] Complete order preview generated
- [ ] All prices verified
- [ ] No payment actions taken
- [ ] Clear instructions provided
