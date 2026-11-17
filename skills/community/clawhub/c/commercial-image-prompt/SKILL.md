---
name: commercial-image-prompt
version: "0.1.0"
license: Apache-2.0
description: "Commercial and e-commerce image generation methodology — three-layer prompt engineering framework (subject-scene / style-texture / technical-constraints) covering both global cross-border platforms (Amazon, Shopify, SHEIN, TikTok, Instagram) and domestic Asian markets (Taobao, JD, Xiaohongshu, WeChat). Includes multi-platform templates and iterative optimization strategies. Use when: generating product photos, marketing posters, e-commerce covers, or commercial AI visuals. Keywords: e-commerce image, product photography, commercial prompts, SHEIN, Amazon, Shopify, 淘宝主图, 营销海报, 小红书封面, 生图提示词."
metadata:
  openclaw:
    emoji: 🖼️
---

# Commercial Image Prompt — Three-Layer Prompting Methodology

A battle-tested prompt engineering methodology designed for both **global cross-border e-commerce & social media** (Amazon, Shopify, SHEIN, TikTok, Instagram) and **Asian domestic markets** (Taobao, JD, Xiaohongshu, WeChat).

> [!TIP]
> **System Collaboration Guidelines**:
> - **Upstream Research**: If the visual style or brand aesthetic is not yet established, use `design-deep-research` first to analyze trends and compile reference moodboards.
> - **Downstream Execution**: This skill specializes in turning approved visual directions into high-precision, production-grade prompts using the Three-Layer Framework with strict negative constraints and text-safe zones.

---

## Core Methodology: Three-Layer Prompting (三层描述法)

### Layer 1: Subject & Scene Setting (主体与场景设定)
A single focused sentence describing the core visual subject, setting, environmental lighting, and primary commercial selling point.

- **Pattern**: `Generate a commercial product photograph of [product] in [scene], lit by [lighting type], emphasizing [key selling feature].`

### Layer 2: Style & Texture Enhancement (风格与质感强化)
2-3 specific aesthetic keywords, material qualities, and artistic/brand references.

- **Global Commercial Styles**: Studio minimalism, Scandinavian lifestyle, Editorial luxury, Cinematic backlight, Cyberpunk neon, High-fashion dynamic lighting.
- **Asian & Cultural Aesthetic Tags (东方美学标签)**: Neo-Chinese (新中式), China-Chic / Guochao (国潮风), Hong Kong Retro (复古港风), Ink-Wash Zen (水墨意境), Minimalist White-Space (极简留白).

### Layer 3: Technical Constraints & Negative Prompts (技术参数与避让约束)
Platform-specific aspect ratios, product framing proportions, text overlay reserve zones, and explicit negative prompts.

- **Pattern**: `Ratio [W:H]. [Color] background. Product occupies [X]% of frame center. Clean negative space reserved for typography. NO text, NO watermarks, NO distorted hands, NO silhouettes.`

---

## Scenario-Based Prompt Templates

### Category A: Global & Cross-Border Platforms (全球跨境电商与社媒)

#### Template 1: Amazon Product Hero (Pure White Background / Studio Lighting)
```
Layer 1: Commercial studio photograph of [product name, e.g. wireless noise-canceling headphones] placed on a subtle matte reflective surface, illuminated by three-point studio softbox lighting highlighting [key detail, e.g. premium metallic hinge and leather earcups].
Layer 2: Style: Ultra-clean industrial commercial product photography, Apple/Sony aesthetic, sharp focal depth, realistic material texture (brushed aluminum, textured leather).
Layer 3: Aspect ratio 1:1. Pure clean white background (#FFFFFF). Product perfectly centered, occupying 85% of frame. Crisp natural drop shadow beneath. NO text, NO watermarks, NO badges, NO packaging clutter.
```

#### Template 2: Shopify DTC Brand Lifestyle Hero Banner
```
Layer 1: Wide-angle lifestyle editorial scene showcasing [product, e.g. organic skincare serum bottle] resting on a sun-drenched travertine stone beside a delicate linen cloth and soft water ripples, warm golden hour sunlight casting soft architectural shadows.
Layer 2: Style: Kinfolk editorial minimalism, warm organic tones, Aesop aesthetic, natural film grain, premium tactile textures.
Layer 3: Aspect ratio 16:9 (horizontal banner). Product placed in right third of the frame. Left 50% reserved with clean negative space for headline text overlay. Soft focus background bokeh. NO text, NO logos.
```

#### Template 3: SHEIN / Fast-Fashion & Apparel Lookbook Shot
```
Layer 1: Full-body / three-quarter dynamic fashion model lookbook shot featuring [garment description, e.g. oversized relaxed-fit linen blazer in sage green], shot on a sunlit European terracotta street corner or minimal concrete studio backdrop.
Layer 2: Style: Zara / SHEIN Premium campaign aesthetic, editorial high-street fashion, natural dynamic pose, fabric weave and drape clearly visible, natural skin tones.
Layer 3: Aspect ratio 3:4 (vertical). Model centered with ample headroom and foot clearance. Vibrant, high-contrast, clean commercial color grading. NO text, NO artificial distortions, normal anatomical proportions.
```

#### Template 4: TikTok / Instagram Reels & Story Hook Cover
```
Layer 1: High-energy vertical lifestyle close-up showing [action / product in use, e.g. portable espresso maker pulling a rich crema shot], steam rising, dramatic directional side lighting.
Layer 2: Style: Viral social-first aesthetic, punchy color contrast, glossy modern feel, dynamic motion capture.
Layer 3: Aspect ratio 9:16 (vertical). Core visual action strictly positioned within the safe vertical middle third (40%-70% height). Top 25% and bottom 25% kept uncluttered for platform UI overlays. NO text, NO icons.
```

---

### Category B: Domestic Asian E-Commerce & Content Ecosystem (国内电商与内容生态)

#### Template 5: 淘宝/天猫/京东 高点击率主图 (Scene & Selling Point)
```
Layer 1: 商业产品实物精修摄影，主体为[产品名称]，放置在[场景环境，如现代极简木质茶台/大理石卫浴台面]，采用专业商业漫反射柔光，凸显[核心卖点，如磨砂磨砂金属旋钮/细腻乳液质地]。
Layer 2: 风格：新中式现代轻奢 (Neo-Chinese luxury) / 日系性冷淡生活美学，材质光影层次通透，微距景深虚化背景。
Layer 3: 比例 1:1 或 3:4。产品居中偏右下，画面顶部留出 30% 干净空间用于后期促销文案与利益点排版。严禁画面内自带任何文字、水印、天猫标或促销色块。
```

#### Template 6: 小红书 / 抖音 爆款种草博主封面图 (Xiaohongshu Native Vibe)
```
Layer 1: [内容主题] 真实生活感实拍特写镜头，第一人称视角或博主桌面摆拍，展示[核心好物/体验场景]，自然窗边侧光带来柔和高光。
Layer 2: 风格：小红书爆款网感风格，高饱和、微冷清透色调、胶片轻微颗粒、氛围感拉满。
Layer 3: 比例 3:4 (竖版)。画面中央为视觉焦点，顶部与底部各预留 15% 干净负空间供大字标题贴纸排版。色彩吸睛有视觉冲击力。画面内严禁 AI 乱码文字。
```

#### Template 7: 微信公众号 / 专栏知识头图 (WeChat Cover 2.35:1)
```
Layer 1: [文章主题] 概念插画或具象隐喻场景，视觉中心为[核心意象]，构图采用稳定对称或黄金分割。
Layer 2: 风格：商业深度思考感，低明度克制莫兰迪色系，磨砂噪点质感，沉稳内敛。
Layer 3: 比例 2.35:1 (极宽横屏)。核心主体严格居中靠下分布（下 2/3），画面上部 1/3 必须保持极简留白，专供公众号遮罩标题展示。NO text.
```

---

## Iteration & Optimization Strategies

### Micro-Adjustments (Variable Isolation)
- **Clean up background**: "Keep the subject intact, but simplify the background with a soft neutral gradient."
- **Element swap**: "Retain the core product and lighting, replace [element A] with [element B]."
- **Style transfer**: "Preserve the composition and framing, shift the aesthetic from [Scandinavian minimal] to [Industrial cyberpunk]."
- **Aspect ratio adaptation**: "Keep the exact content and subject scale, reframe composition into vertical (9:16) format with expanded headroom."
- **Detail enhancement**: "Increase definition and specular highlights on the [metal bezel / glass bottle surface]."

### The "One Variable at a Time" Rule
Never change composition, style, and lighting simultaneously in one iteration round. Isolate and test:
1. Round 1: Composition & framing only
2. Round 2: Style & material texture only
3. Round 3: Lighting & micro-details only

---

## Failure Recovery Guide

| Failure Mode | Symptom | Fix Prompt |
|-------------|---------|-----------|
| **Text artifacts** | Garbled AI pseudo-characters appear | "Strictly pure photography, absolute zero text, letters, numerals, or characters anywhere in image." |
| **Product deformation** | Warped edges, distorted geometry | "Ensure [product] maintains strict rectilinear industrial proportions and photorealistic CAD-accurate geometry." |
| **Muddy colors** | Over-saturated color bleed | "Clean color separation, increase dynamic range, neutral background tones without tint bleed." |
| **Subject crowding** | No room for post-production text | "Zoom out 15%, pull camera back, provide 30% clean negative space around the upper third of the frame." |
| **Platform UI clash** | Critical elements covered by TikTok/IG buttons | "Keep all primary visual interest inside the central 50% safe zone; top and bottom margins completely clear." |

---

## ⚠️ Hard Rules for Commercial Outputs

1. **ZERO TEXT IN IMAGES**: AI-generated text is unusable for commercial packaging or advertisements. Always enforce negative prompts for text and reserve clean negative space for graphic typography in post-production.
2. **ALL THREE LAYERS MANDATORY**: Every prompt must define Subject (Layer 1), Style (Layer 2), and Constraints (Layer 3). Missing Layer 3 will default to wrong aspect ratios and un-cropped clutter.
3. **PRECISE ASPECT RATIOS**:
   - Amazon / Standard E-commerce Hero: `1:1`
   - SHEIN / Apparel / Xiaohongshu: `3:4`
   - Shopify / Web Hero: `16:9`
   - TikTok / Instagram Reels / Mobile Hook: `9:16`
   - WeChat Article Banner: `2.35:1`
