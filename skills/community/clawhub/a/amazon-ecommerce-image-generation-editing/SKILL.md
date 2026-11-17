---
name: amazon-ecommerce-image-generation-editing
description: "Create and edit Amazon catalog images, PDP galleries, A+ Content modules, Brand Store heroes, variant sets and advertising creative bases. Use this skill for Amazon商品图、亚马逊Listing、A+页面、品牌旗舰店、主图、信息图、包装清单、尺寸比例、Sponsored Ads素材和多站点本地化；supports AI Hive reference generation."
---

# Amazon Ecommerce Image Generation and Editing

Build a complete Amazon seller image architecture beyond a single listing hero. The catalog layer locks ASIN/SKU, variant, package and claims; PDP, A+ Content, Brand Store and ad placements then reuse that truth for different shopper questions.

## Seller source sheet

Collect ASIN/internal SKU, exact variant, product and retail package, included items, dimensions, materials, approved benefits, target marketplace, units, warnings, brand assets and copy rights. Reviews, ratings, badges, certifications and competitive comparisons cannot be invented.

## Scenarios and commands

### 1. Catalog primary image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Amazon catalog primary image for the supplied SKU. Preserve exact product shape, variant, packaging, logo and included components. Complete product large on a clean background with accurate edges and shadow. No price, rating, badge, certification, lifestyle prop or unprovided text.' \
  --image /path/to/product-front.png \
  --image /path/to/package.png
```

### 2. PDP gallery questions

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a 5-image Amazon PDP gallery: product overview, in-hand scale, material detail, correct use, package contents. Keep exact SKU and brand system across all images; reserve clean areas for approved copy and measurements. Do not generate dimensions, claims, reviews or badges.' \
  --image /path/to/product.png \
  --batch 5
```

### 3. A+ Content module base

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Wide Amazon A+ Content module base: accurate product used in a credible home context, one visible feature detail, calm right-side copy region and responsive crop tolerance. Preserve product and packaging; no comparison chart data, certification, warranty or competitor reference.' \
  --image /path/to/product.png
```

### 4. Brand Store hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Amazon Brand Store hero connecting three approved products through one coherent brand use case. Keep each SKU visually distinct and accurate, use supplied brand palette, reserve headline and navigation space, and avoid price, sale event, bestseller badge or platform UI.' \
  --image /path/to/brand-products.png
```

### 5. Marketplace localization base

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Adapt the US lifestyle image into a German-market base while preserving product, package, usage and commercial facts. Change environment and caption layout only. Remove old copy and leave units, warranty, certification and claims blank for approved German localization.' \
  --image /path/to/us-lifestyle.jpg
```

## Amazon QA

- ASIN/SKU, variant, package and included items match the seller record.
- PDP images answer different questions; A+ and Brand Store support brand navigation.
- Measurements, units and localized copy use approved data.
- No generated rating, review, bestseller badge, certification, price or competitor claim.
- Source assets and brand marks have appropriate rights.
- Verify current Amazon image, A+ Content, Store and advertising requirements per marketplace.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name amazon-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Fixed model: `public_model_nano_banana_pro`. Use multiple references, batch, live parameters, routing, output directory and submit-only mode as needed.
