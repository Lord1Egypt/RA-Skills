---
name: amazon-seller
description: "Amazon Seller Central listing management and optimization. Use when: user wants to create product listings, apply for GTIN exemptions, set up FBA shipments, write optimized product content, or manage Amazon inventory. Supports US, UK, EU, JP marketplaces and multiple product categories including supplements, home goods, electronics, and clothing. NOT for: other e-commerce platforms, legal/tax advice, or Amazon Advertising."
homepage: https://github.com/openclaw-skills/amazon-seller
metadata:
  openclaw:
    emoji: "📦"
    tags: ["ecommerce", "amazon", "fba", "listing", "gtin", "inventory"]
    requires:
      env: []
      tools: ["browser"]
---

# Amazon Seller Central Guide

Complete guide for creating and managing Amazon product listings across multiple marketplaces.

## When to Use

**USE this skill when:**
- Creating new product listings on Amazon Seller Central
- Applying for GTIN/UPC exemptions
- Setting up FBA (Fulfillment by Amazon) shipments
- Writing Amazon-optimized product content (titles, bullets, descriptions, search terms)
- Understanding Amazon image requirements and best practices
- Managing inventory, pricing, and product variations
- Navigating category-specific requirements and restrictions

**DON'T use this skill when:**
- Questions about other platforms (eBay, Shopify, Walmart, Etsy)
- Legal, tax, or accounting advice for Amazon selling
- Trademark registration or patent issues
- Amazon Advertising campaigns (Sponsored Products/Brands/Display)
- Account suspension appeals or reinstatement
- Wholesale/retail arbitrage strategies

## Quick Start

### 1. Choose Your Marketplace
- **US** (Amazon.com): Largest market, highest competition
- **UK** (Amazon.co.uk): English-speaking, VAT required
- **EU** (Amazon.de, .fr, .it, .es): Multi-country expansion
- **JP** (Amazon.co.jp): Unique requirements, local language needed

### 2. Determine Product Category
See [references/category-requirements.md](references/category-requirements.md) for:
- Category-specific requirements
- Approval needed categories (gated)
- Restricted products list
- Compliance documents needed

### 3. Check GTIN Requirements
- **Need UPC?** Most categories require valid UPC/EAN
- **GTIN Exemption?** See [references/gtin-exemption-guide.md](references/gtin-exemption-guide.md)
- **Brand Registry?** Required for some exemptions

### 4. Prepare Product Information
Use templates:
- [templates/product-template.txt](templates/product-template.txt) - Fill in your product details
- [templates/image-checklist.txt](templates/image-checklist.txt) - Ensure images meet requirements

### 5. Create Listing
See [references/listing-workflow.md](references/listing-workflow.md) for step-by-step instructions.

## Core Workflows

### New Product Listing
```
1. Category Selection - Check if gated/approval needed
2. Product Information - Title, bullets, description, keywords
3. Images - 7 images minimum, pure white background for main
4. Pricing & Inventory - Cost analysis, competitive pricing
5. Fulfillment - FBA vs FBM decision
6. Submit & Monitor - Wait for Amazon review
```

### GTIN Exemption Application
```
1. Verify eligibility - Private label, generic, or custom products
2. Prepare proof - Trademark, website, or product packaging
3. Apply in Seller Central - Inventory > Add Products > GTIN Exemption
4. Wait for approval - Usually 24-48 hours
5. Create listing - Use exemption to list without UPC
```
See detailed guide: [references/gtin-exemption-guide.md](references/gtin-exemption-guide.md)

### FBA Shipment Creation
```
1. Create shipping plan - Inventory > Manage FBA Inventory
2. Set quantity - Accurate count needed
3. Prep products - Labeling, packaging requirements
4. Print labels - FNSKU product labels, box labels
5. Ship to Amazon - Use partnered carrier or your own
6. Track receipt - Monitor inbound status
```
See detailed workflow: [references/fba-workflow.md](references/fba-workflow.md)

## Content Guidelines

### Title Requirements
- **Length**: Max 200 characters (varies by category)
- **Format**: [Brand] + [Product] + [Key Feature] + [Size/Quantity]
- **Avoid**: ALL CAPS, promotional phrases ("Best", "Top"), special characters (! * $)

**Example (Supplements)**:
```
Wondermed Liver Support Complex - 5-in-1 Milk Thistle Supplement with Artichoke & Dandelion - 120 Capsules - Made in USA
```

### Bullet Points (5 required)
- **Length**: Max 500 characters each
- **Format**: [ALL CAPS HEADER] + Detailed benefit
- **Content**: Focus on features, benefits, and specifications
- **Keywords**: Naturally incorporate search terms

See examples: [references/examples/](references/examples/)

### Product Description (HTML)
- **Length**: Max 2000 characters
- **Format**: Use basic HTML (<p>, <br>, <ul>, <li>, <strong>)
- **Content**: Expanded details, usage instructions, brand story
- **Mobile**: Remember most shoppers view on mobile

### Backend Search Terms
- **Length**: Max 250 bytes (not characters)
- **Format**: Comma-separated, no repetition
- **Content**: Synonyms, alternate names, use cases
- **Avoid**: Brand names (yours or competitors'), ASINs

## Image Requirements

### Main Image (Critical)
- **Background**: Pure white (RGB 255,255,255)
- **Product**: Fill 85% or more of frame
- **Format**: JPEG, TIFF, GIF, PNG
- **Size**: Minimum 1000 x 1000 pixels (2000+ recommended)
- **No**: Text, logos, watermarks, props, multiple products

### Secondary Images (6+ recommended)
1. **Infographic** - Key features/benefits visualization
2. **Lifestyle** - Product in use, real-world context
3. **Scale/Size** - Show dimensions or compare to common objects
4. **Details** - Close-ups of important features
5. **Instructions** - How to use or assemble
6. **Package/Contents** - What's in the box
7. **Before/After** - If applicable and compliant

See full checklist: [templates/image-checklist.txt](templates/image-checklist.txt)

## Pricing Strategy

### Cost Calculation
```
Selling Price
- Amazon Referral Fee (8-15% depending on category)
- FBA Fee (if applicable)
- Storage Fee (monthly, varies by season)
- Cost of Goods
- Shipping to Amazon
- Returns/Customer Service
= Net Profit
```

### Competitive Analysis
- Check competitor prices ( Keepa, CamelCamelCamel)
- Consider Amazon fees in your pricing
- Plan for promotional pricing (Lightning Deals, Coupons)
- Factor in currency conversion for international

## Fulfillment Options

### FBA (Fulfillment by Amazon)
**Pros**:
- Prime eligibility (higher conversion)
- Amazon handles shipping, returns, customer service
- Buy Box advantage
- Multi-channel fulfillment available

**Cons**:
- FBA fees reduce margin
- Inventory storage limits
- Long-term storage fees
- Less control over packaging

### FBM (Fulfillment by Merchant)
**Pros**:
- Higher margins (no FBA fees)
- Full control over packaging/branding
- No storage limits
- Better for oversized/heavy items

**Cons**:
- No Prime badge (usually)
- Must handle shipping and returns
- Lower Buy Box share
- More operational work

### SFP (Seller Fulfilled Prime)
- Prime badge without FBA
- Strict performance requirements
- Must offer 2-day shipping
- Invitation-only program

## Category-Specific Notes

See [references/category-requirements.md](references/category-requirements.md) for details on:
- **Health & Household / Supplements**: FDA disclaimers, ingredient lists, safety warnings
- **Electronics**: Compliance certifications, safety warnings
- **Clothing/Apparel**: Size charts, material composition, care instructions
- **Home & Kitchen**: Safety warnings, assembly instructions
- **Beauty**: Ingredient transparency, expiration dates
- **Toys**: Age recommendations, safety certifications

## Common Issues & Solutions

### Listing Suppressed
- Check: Main image has pure white background
- Check: Title length within category limit
- Check: All required fields completed
- Check: No prohibited keywords

### GTIN Exemption Denied
- Provide additional brand proof
- Check if category allows exemptions
- Consider purchasing GS1 UPCs
- Ensure brand name consistency

### Buy Box Eligibility
- Maintain competitive pricing
- Use FBA for best results
- Keep inventory in stock
- Maintain account health metrics
- Get positive seller feedback

### Inventory Stranded
- Check FBA shipment status
- Verify listing is active and buyable
- Ensure correct FNSKU labeling
- Contact Seller Support if persists

## Tools & Resources

### Amazon Official
- Seller University (free training)
- Amazon Advertising Console
- Brand Analytics (for registered brands)
- Seller Forums

### Third-Party Tools
- **Research**: Helium 10, Jungle Scout, Viral Launch
- **Pricing**: Keepa, CamelCamelCamel, SellerSnap
- **Reviews**: FeedbackWhiz, Jungle Scout Alerts
- **Accounting**: QuickBooks, Fetcher, SellerBoard

### Browser Extensions
- Helium 10 Chrome Extension
- Jungle Scout Extension
- Keepa (price history)
- Amazon Seller App (mobile)

## Examples & Templates

See [references/examples/](references/examples/) for complete listing examples:
- [supplement-example.md](references/examples/supplement-example.md) - Health supplement
- [home-goods-example.md](references/examples/home-goods-example.md) - Home & Kitchen
- [electronics-example.md](references/examples/electronics-example.md) - Consumer electronics

## Updates & Version History

v1.0.0 - Initial release
- Multi-marketplace support (US, UK, EU, JP)
- Multi-category coverage
- GTIN exemption workflow
- FBA shipment guide
- Complete listing templates

---

*Note: Amazon policies change frequently. Always verify current requirements in Seller Central.*
