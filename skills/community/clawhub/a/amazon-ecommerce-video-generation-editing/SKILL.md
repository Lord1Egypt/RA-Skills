---
name: amazon-ecommerce-video-generation-editing
description: "Create and edit Amazon product videos, listing demos, storefront brand clips and advertising video assets. Use this skill for Amazon商品视频、Listing Video、Product Detail Page video、Sponsored Brands Video、Amazon Store、开箱、安装演示、功能说明和跨境本地化；supports text/image/reference-to-video, editing, extension and AI Hive delivery."
---

# Amazon Ecommerce Video Generation and Editing

Create product-first videos that reduce purchase uncertainty on Amazon. Every shot must help a shopper identify the item, understand setup, verify a feature or judge fit. Never generate an unsupported claim, certification, review, ranking, discount or comparison.

## Source-of-truth sheet

Collect the ASIN or internal SKU, exact variant, packaging, included components, dimensions, materials, supported features, setup instructions, warnings, target marketplace, approved copy and footage rights. If information is missing, omit it rather than asking the model to infer it.

## Choose the video job

- **Listing demo:** identify, operate and show the result.
- **Installation guide:** present steps in the correct order.
- **Feature proof:** show one feature with visible evidence.
- **Storefront story:** connect several products through a brand use case.
- **Ad variant:** open with a shopper problem and one supported benefit.
- **Localization:** adapt language and context without changing facts.

## Scenarios and commands

### 1. Product listing demonstration

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt 'Amazon listing product video for the US marketplace. Preserve exact shape, color, packaging, logo and included parts. Start with a complete product view, demonstrate one correct setup, show two material or control details, then show the product in its intended context. Clean informative pacing; no price, badge, review, ranking, certification or unsupported performance claim.'
```

### 2. Assembly or installation sequence

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Amazon product setup video based only on the merchant-approved instructions: lay out the supplied parts, show step 1, step 2 and step 3 in order with clear hand placement, then show the correctly assembled result. Do not skip safety steps, invent a component or display unprovided measurements.'
```

### 3. Feature-proof close-up

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/shot-style.mp4 \
  --image /path/to/product-detail.png \
  --prompt 'Use the reference video only for camera pace and macro transition. Create an original Amazon feature-proof clip for the supplied product: show the control action, the relevant mechanism and the visible outcome in one continuous sequence. Preserve product accuracy and do not copy reference branding, dialogue or claims.'
```

### 4. Recut supplier footage for a listing

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/supplier-master.mp4 \
  --prompt 'Re-edit the supplier footage into a clear Amazon product video. Keep all real product and setup information; remove unrelated watermarks, repetitive beauty shots and unsupported promotional text. Order the footage as full product, included items, setup, feature proof and final use case. Do not alter product specifications.'
```

### 5. Marketplace localization

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/us-listing-video.mp4 \
  --prompt 'Localize this product video for the German marketplace: preserve the product, actions, specifications and commercial meaning; adapt visible lifestyle context and reserve clean areas for approved German captions. Do not translate certification, warranty or compatibility claims unless merchant-approved localized text is provided.'
```

## QA before upload

- Variant, packaging, components, controls and setup match the source sheet.
- Claims are supported by visible evidence or approved merchant copy.
- Text and units match the target marketplace and are manually proofread.
- No generated star rating, bestseller badge, review, price, certification or competitor mark.
- Music, models, supplier footage and reference assets have usage rights.
- Verify the current Amazon listing and advertising requirements for the marketplace and category.

## Runtime

The CLI maps `t2v`, `i2v`, `r2v`, `edit` and `extend` to Seedance 2.5 generation and editing endpoints.

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name amazon-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use the media arguments, `--param key=value`, `--routing`, `--output-dir` and `--no-download` as needed. Confirm live parameters and pricing before batch production. Query an existing `taskId` after timeout.
