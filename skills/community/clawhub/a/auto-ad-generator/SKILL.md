---
name: auto-ad-generator
description: Generate professional advertisement posters for multiple industries including automotive, cultural tourism, fragrance, tea, and more. Create commercial layouts with AI-generated backgrounds using PIL (local/free) or Dreamina/即梦 (high-quality AI), composite product images with typography, and export to multiple platform formats (WeChat, Xiaohongshu, airport displays). Use when the user wants to create ads, marketing posters, commercial photography layouts, brand promotional materials, or replicate advertisement styles with product replacement. Trigger on phrases like "generate ad", "make poster", "create advertisement", "like Li Auto style", "product poster", "marketing material", or when the user uploads product images and asks for marketing layouts.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - dreamina
      env:
        - DREAMINA_API_KEY
        - REMOVE_BG_API_KEY
---

# Auto Ad Generator

Generate professional advertisement posters with AI-powered backgrounds and product compositing.

## 依赖声明 (Dependencies)

本 Skill 需要以下外部服务和工具：

### 必需的二进制文件
- `python3` - Python 3.8+
- `dreamina` - Dreamina CLI (通过 `curl -s https://jimeng.jianying.com/cli | bash` 安装)

### 必需的环境变量
- `DREAMINA_API_KEY` - Dreamina API 密钥
- `REMOVE_BG_API_KEY` - remove.bg API 密钥（可选，用于背景移除）

### 可选 API 服务
- DALL-E / Midjourney / Stability AI - 用于 AI 图像生成
- Dreamina/即梦 - 主要 AI 生成后端
- remove.bg - 产品图背景移除

---

## Overview

This skill supports multiple industries and platforms:
- **Industries**: Automotive, cultural tourism, fragrance/beauty, tea, recruitment, public welfare
- **Platforms**: WeChat official accounts (21:9), Xiaohongshu (3:4), airport displays (16:9/9:16), lightboxes
- **Backends**: PIL (local/free) or Dreamina/即梦 CLI (AI-powered, high quality)

## Quick Start

### Generate an Ad

```python
# Using Dreamina AI backend
python main.py --backend dreamina \
  --car ./product.jpg \
  --brand "Brand Name" \
  --subtitle "Product Tagline" \
  --slogan "Marketing Slogan" \
  --platform xiaohongshu \
  --style premium \
  --output ./output

# Using PIL (local, free)
python main.py --backend pil \
  --car ./product.jpg \
  --brand "Brand Name" \
  --output ad.jpg
```

### Interactive Mode

```bash
python main.py
# Follow prompts to select backend, platform, and style
```

## Core Workflow

### 1. Analyze Input
When user provides car images and requests:
- **Identify car type**: sedan, SUV, MPV, etc.
- **Extract key features**: color, design highlights, target audience
- **Determine ad style**: luxury, sporty, family-friendly, tech-focused

### 2. Gather Requirements

Ask the user (unless provided):
```
1. Brand name and model?
2. Main headline/slogan?
3. Subtitle/description?
4. Target audience? (young professionals, families, etc.)
5. Celebrity endorser image? (optional)
6. Preferred color scheme? (or auto-detect from brand)
```

### 3. Generate Ad Components

#### Background Generation
Use image generation to create gradient background:
```
Prompt template:
"Premium gradient background for car advertisement, 
{primary_color} to {secondary_color} smooth gradient, 
subtle light rays, luxury automotive aesthetic, 
minimalist, high-end commercial photography style, 
no text, no car, clean background only"
```

#### Car Subject Enhancement
- Clean up the car image (remove background if needed)
- Enhance lighting and reflections
- Position car at 3/4 front angle or side profile

#### Typography Layout
```
Layout Structure (1080x1920 vertical):
┌─────────────────┐
│   HEADLINE      │ ← 40-60px, bold, white or contrast color
│   subtitle      │ ← 20-28px, lighter weight
│                 │
│   [CAR IMAGE]   │ ← Main visual, 60% of frame
│   [Celebrity]   │ ← Optional, overlapping or beside
│                 │
│   Slogan        │ ← Bottom area
│   Logo          │ ← Corner placement
└─────────────────┘
```

### 4. Style Reference: Li Auto Aesthetic

**Color Palettes**:
- Premium: Deep blue → Purple gradient (#1a237e → #7c4dff)
- Warm: Orange → Pink gradient (#ff6b35 → #f7931e)
- Cool: Teal → Cyan gradient (#00897b → #00bcd4)
- Dark: Black → Deep gray with subtle blue tint

**Typography**:
- Headline: Bold, condensed sans-serif
- Subtitle: Light weight, generous letter-spacing
- Slogan: Italic or script for emotional touch

**Lighting**:
- Soft, diffused key light
- Subtle rim light on car edges
- Gradient background with light source from top

### 5. Execution Steps

```python
# Pseudo-code for skill execution
def generate_car_ad(car_image, params):
    # Step 1: Analyze car
    car_analysis = analyze_image(car_image)
    
    # Step 2: Generate background
    background = generate_image(
        prompt=build_background_prompt(params['style']),
        size="1024x1536"
    )
    
    # Step 3: Process car image
    car_processed = remove_background(car_image)
    car_enhanced = enhance_lighting(car_processed)
    
    # Step 4: Composite
    composite = overlay_car_on_background(
        background, 
        car_enhanced,
        position="center-bottom",
        scale=0.7
    )
    
    # Step 5: Add text
    final = add_typography(
        composite,
        headline=params['headline'],
        subtitle=params['subtitle'],
        slogan=params['slogan'],
        font_style=params['style']
    )
    
    # Step 6: Add logo
    if params.get('logo'):
        final = overlay_logo(final, params['logo'])
    
    return final
```

### 6. Quality Checklist

Before presenting to user:
- [ ] Car is the clear focal point
- [ ] Text is readable against background
- [ ] Color harmony between car and background
- [ ] Professional lighting on car
- [ ] Brand/logo placement is subtle but visible
- [ ] Overall composition follows rule of thirds

## Example Outputs

### Example 1: Li Auto Style SUV Ad
**Input**: SUV image, "理想i6", "新形态纯电五座SUV"  
**Output**: Purple-blue gradient, car at 3/4 angle, large white text, celebrity placement

### Example 2: Sporty Sedan Ad
**Input**: Sports sedan, "P7", "纯粹驾驶乐趣"  
**Output**: Dark background with orange accent lighting, dynamic angle, bold typography

### Example 3: Family MPV Ad
**Input**: Minivan, "MEGA", "全家人的幸福空间"  
**Output**: Warm gradient, spacious composition, friendly tone, emphasis on interior space

## Tools & Scripts

### Required Tools
- Image generation (DALL-E, Midjourney, or local SD)
- Image editing (remove.bg API or local model)
- Text overlay (PIL/Pillow or similar)
- Image composition (layer blending)

### Bundled Scripts
- `scripts/generate_background.py` - Generate gradient backgrounds
- `scripts/composite_ad.py` - Layer car, background, text
- `scripts/typography.py` - Add professional text layout

## Guidelines

### Do
- Match background color to car's personality (sporty=warm, luxury=cool)
- Keep text minimal - one headline, one subtitle max
- Ensure car lighting matches background light source
- Use high-resolution source images (min 1024px width)

### Don't
- Overcrowd with too much text
- Use clashing colors (unless intentional for contrast)
- Place car too small in frame (should be 50-70% of composition)
- Ignore the brand's existing visual identity

### Edge Cases
- **No car image provided**: Ask user to upload, or generate concept car
- **Low resolution input**: Upscale first, or use as thumbnail/concept only
- **Multiple cars**: Focus on hero car, use others as supporting elements
- **Specific brand requirements**: Follow brand guidelines over Li Auto style

## Reference Materials

See `references/` directory for:
- `li_auto_examples.md` - Analysis of Li Auto ad patterns
- `color_palettes.json` - Pre-defined gradient combinations
- `typography_guide.md` - Font pairing recommendations
- `composition_templates/` - Layout reference images

---

## Dreamina (即梦) Integration

This skill supports Dreamina CLI for AI-powered background generation with higher quality results.

### Prerequisites
```bash
# Install Dreamina CLI
curl -s https://jimeng.jianying.com/cli | bash

# Login (required before use)
dreamina login --headless
```

### Two Backend Modes

#### Mode 1: PIL (Local, Free)
Uses Python PIL to generate simple gradient backgrounds.
- **Pros**: No API cost, instant, offline
- **Cons**: Basic quality, limited styles

```python
python main.py --backend pil --car image.jpg --brand 理想 --model i6
```

#### Mode 2: Dreamina (AI-powered)
Uses Dreamina's text2image for professional AI backgrounds.
- **Pros**: High quality, diverse styles, professional aesthetics
- **Cons**: Consumes credits (~10-50 per image)

```python
python main.py --backend dreamina --car image.jpg --brand 理想 --model i6 \
  --platform xiaohongshu --style premium
```

### Platform Presets

| Platform | Ratio | Size | Use Case |
|----------|-------|------|----------|
| `wechat` | 21:9 | ~900×383 | 公众号头图 |
| `xiaohongshu` | 3:4 | 1242×1660 | 小红书封面 |
| `airport_h` | 16:9 | 1920×1080 | 机场横屏广告 |
| `airport_v` | 9:16 | 1080×1920 | 机场竖屏广告 |
| `lightbox` | 16:9 | Custom | 灯箱广告 |

### Style Presets

| Style | Mood | Best For |
|-------|------|----------|
| `premium` | 豪华科技 | 汽车、高端产品 |
| `warm` | 运动年轻 | 年轻品牌、运动产品 |
| `cool` | 环保现代 | 新能源、科技产品 |
| `dark` | 神秘高端 | 奢侈品、夜景 |
| `cultural` | 国风山水 | 文旅、传统文化 |
| `fragrance` | 粉金轻奢 | 美妆、香化 |
| `tea` | 禅意自然 | 茶叶、健康 |

### Complete Workflow with Dreamina

```bash
# Step 1: Generate AI background
python main.py --backend dreamina \
  --car ./assets/suv.png \
  --brand 理想 \
  --model i6 \
  --subtitle "新形态纯电五座SUV" \
  --slogan "理想，就是活成自己喜欢的样子" \
  --platform xiaohongshu \
  --style premium \
  --output ./output

# Step 2: Check generation status
dreamina query_result --submit_id=<id_from_step1>

# Step 3: Download result and composite (manual or scripted)
# Step 4: Add typography using composite_ad.py
```

### Credit Management

```bash
# Check remaining credits
dreamina user_credit

# Typical consumption:
# - text2image (2k): ~10-20 credits
# - text2image (4k): ~30-50 credits
# - image_upscale: ~20-40 credits
```

### Advanced: Image-to-Image

Use existing image as base for style transfer:

```python
from scripts.dreamina_backend import image_to_image

result = image_to_image(
    prompt="luxury car advertisement style, premium gradient background",
    image_path="existing_car_shot.jpg",
    ratio="16:9"
)
```
