---
name: freeads-snap-ad
description: "🎬 AI 高端广告视频生成器 - 将产品照片转化为 8 秒专业广告视频（含 BGM、Slogan、音效、丰富运镜）。使用 Atlas Cloud API 调用 Veo 3.1 生成视频。触发词：随手拍广告、生成广告视频、产品广告。核心输出：视频文件 URL。"
version: 3.7.0
author: lipeng0820
metadata:
  category: media-generation
  platforms:
    - codeflicker
    - openclaw
    - claude-code
  required-env:
    - ATLASCLOUD_API_KEY
  estimated-cost: "$0.80-1.60 per video"
---

# FreeAds 随手拍广告 🎬

> **AI 高端广告视频生成器** | 最终产出：8 秒 TVC 级 MP4 视频（含 BGM、音效、专业运镜）
> 
> 📦 安装：`clawhub install lipeng0820/freeads-snap-ad`

---

## ⚠️ 核心原则：产品外观保护（最高优先级）

**这是本 Skill 的价值核心，必须严格遵守：**

### 🛡️ 产品保真三原则

1. **外观不走样** - 产品的形状、轮廓、设计细节必须与原图完全一致
2. **材质不臆断** - 如果无法确定材质，不要描述，让 Veo 3.1 从图片推断
3. **品牌不乱改** - 如果看不清品牌标识，不要猜测或编造

### 📊 置信度判断机制

在产品识别时，模型必须对以下属性输出置信度分数（0-100）：

```json
{
  "product": {
    "type": {"value": "Air Fryer", "confidence": 95},
    "material": {"value": "matte white plastic", "confidence": 60},
    "color": {"value": "white", "confidence": 90},
    "brand": {"value": "unknown", "confidence": 20},
    "texture": {"value": "smooth finish", "confidence": 45}
  }
}
```

**规则：当 confidence < 80 时，该属性不得在 Veo 3.1 提示词中描述！**

---

## 🌐 语言处理规则

1. **与用户对话**：使用用户的语言（中文用户用中文回复）
2. **与底层模型交互**：始终使用英文
3. **翻译输出**：将模型返回的英文结果翻译成用户语言后展示

---

## 🔑 API Key 获取

当用户没有配置 `ATLASCLOUD_API_KEY` 时：

```
❌ 需要 Atlas Cloud API Key 才能生成视频 🎬

请按以下步骤获取：
1. 访问 Atlas Cloud: https://www.atlascloud.ai?ref=LJNA3T
   🎁 新用户福利：使用此链接注册，首次充值可获得 25% 奖励（最高 $100）！
2. 登录后进入 Console -> API Keys
3. 创建并复制 API Key
4. 配置环境变量：export ATLASCLOUD_API_KEY="your-api-key"
```

---

## 🚨 执行流程

### 交互式确认流程

```
Step 1: 识别产品（含置信度） → 展示结果 → 等待用户确认 ✅
Step 2: 场景设计 → 展示结果 → 等待用户确认 ✅
Step 3: 分镜脚本 → 展示结果 → 等待用户确认 ✅
Step 4: 展示 Slogan → 等待用户确认 ✅
Step 5: 展示 Veo 3.1 提示词（低置信度属性已过滤） → 等待用户确认 ✅
Step 6: 生成视频 → 同时展示 Tips → 返回视频 URL
```

---

## 🎯 产品识别 Prompt（带置信度）

```python
PRODUCT_RECOGNITION_PROMPT = """You are a product identification expert. Analyze the product image with EXTREME PRECISION.

## CRITICAL: CONFIDENCE SCORING

For EACH attribute, you MUST provide a confidence score (0-100):
- 90-100: Absolutely certain, clearly visible
- 70-89: Reasonably confident, mostly visible
- 50-69: Uncertain, partially visible or ambiguous
- 0-49: Cannot determine, guessing, or not visible

## PROTECTION RULES

1. **DO NOT GUESS** - If you cannot clearly see something, confidence should be LOW
2. **DO NOT FABRICATE** - Never make up brand names, logos, or specific details
3. **DO NOT ASSUME** - If material/texture is unclear, say "unknown" with low confidence
4. **PRESERVE ORIGINAL** - Your goal is to DESCRIBE what you SEE, not what you IMAGINE

## OUTPUT FORMAT (JSON)

{
  "product": {
    "category": {"value": "product category", "confidence": 95},
    "name": {"value": "product name", "confidence": 90},
    "shape": {"value": "shape description", "confidence": 85},
    "color": {"value": "color description", "confidence": 92},
    "material": {"value": "material or 'unknown'", "confidence": 55},
    "texture": {"value": "texture or 'unknown'", "confidence": 40},
    "brand": {"value": "brand name or 'unknown'", "confidence": 25},
    "logo_visible": {"value": true/false, "confidence": 80},
    "key_features": [
      {"value": "feature 1", "confidence": 88},
      {"value": "feature 2", "confidence": 75}
    ]
  },
  "appearance_summary": "Brief factual description of what is CLEARLY VISIBLE in the image",
  "uncertain_elements": ["list of elements that are unclear or ambiguous"],
  "overall_product_confidence": 85
}

## EXAMPLES

❌ WRONG (low confidence but detailed description):
"material": {"value": "premium brushed aluminum with anodized coating", "confidence": 45}

✅ CORRECT (low confidence = vague or unknown):
"material": {"value": "metallic surface, specific material unknown", "confidence": 45}

❌ WRONG (fabricating brand):
"brand": {"value": "Xiaomi", "confidence": 30}

✅ CORRECT (honest about uncertainty):
"brand": {"value": "unknown - no visible branding", "confidence": 10}
"""
```

---

## 📝 Veo 3.1 提示词构建（置信度过滤）

**关键：只有 confidence >= 80 的属性才能进入 Veo 3.1 提示词！**

```python
def build_veo_prompt(product_data, scene_data, shots_data, slogan):
    """
    构建 Veo 3.1 提示词，自动过滤低置信度属性
    """
    
    # 提取高置信度属性
    high_confidence_attrs = []
    
    for attr, data in product_data.items():
        if isinstance(data, dict) and data.get("confidence", 0) >= 80:
            high_confidence_attrs.append(f"{attr}: {data['value']}")
    
    # 如果高置信度属性很少，使用通用描述
    if len(high_confidence_attrs) < 3:
        product_description = "the product exactly as shown in the input image"
    else:
        product_description = ", ".join(high_confidence_attrs)
    
    # 构建提示词
    prompt = f"""Premium 8-second TVC commercial.

PRODUCT APPEARANCE PROTECTION (CRITICAL):
- The product MUST appear EXACTLY as shown in the input image
- DO NOT modify, enhance, or reimagine the product's appearance
- Maintain exact shape, color, proportions, and all visible details
- If there are logos or brand elements, keep them exactly as shown
- The input image is the ONLY source of truth for product appearance

PRODUCT: {product_description}

SCENE: {scene_data.get('setting_description', 'professional studio setting')}
LIGHTING: {scene_data.get('lighting', 'professional studio lighting')}
MOOD: {scene_data.get('mood', 'premium, elegant')}

SHOTS:
"""
    
    for shot in shots_data:
        prompt += f"- {shot['timing']}: {shot['description']}. Camera: {shot['camera']}\n"
    
    prompt += f"""
SLOGAN: "{slogan}" appears elegantly in the final shot.

STYLE: Premium TVC commercial, cinematic quality, Super Bowl ad level.
AUDIO: Epic background music with synchronized sound effects.

ABSOLUTE REQUIREMENT: The product's visual appearance must be IDENTICAL to the input image. 
No creative liberties with product design, color, shape, or branding."""

    return prompt
```

---

## 🎬 分镜脚本 Prompt（保护产品外观）

```python
STORYBOARD_PROMPT = """You are a TVC commercial director. Create a 3-shot storyboard for an 8-second video.

## PRODUCT APPEARANCE PROTECTION (HIGHEST PRIORITY)

⚠️ WARNING: You are NOT allowed to describe specific product details unless you are CERTAIN.

RULES:
1. Use phrases like "the product" or "the item" instead of detailed descriptions
2. Focus on CAMERA MOVEMENT, LIGHTING, and SCENE - NOT product details
3. DO NOT describe materials, textures, or brand elements unless confidence >= 80%
4. Let the input image speak for itself - Veo 3.1 will preserve the product appearance

## GOOD vs BAD EXAMPLES

❌ BAD (too specific, may cause distortion):
"The brushed stainless steel air fryer with digital LED display rotates..."

✅ GOOD (respects product appearance):
"The product rotates slowly, showcasing its design from multiple angles..."

❌ BAD (fabricating details):
"The Apple logo gleams under the studio lights..."

✅ GOOD (factual):
"Any visible branding catches the light naturally..."

## SCENE SELECTION

Based on product category, choose appropriate environment:
- Kitchen Appliance → Modern kitchen, marble countertop
- Electronics → Clean desk, tech workspace
- Fashion → Lifestyle setting, editorial style
- Beauty → Spa-like bathroom, soft lighting
- Default → Professional studio with gradient backdrop

## OUTPUT FORMAT (JSON)

{
  "scene": {
    "environment": "environment type",
    "setting_description": "scene description WITHOUT product details",
    "lighting": "lighting description",
    "mood": "emotional tone"
  },
  "slogan": "2-5 word slogan",
  "shots": [
    {
      "number": 1,
      "timing": "0-3s",
      "type": "REVEAL",
      "description": "Shot description focusing on camera and scene, NOT product details",
      "camera": "camera movement",
      "audio": "audio cue"
    },
    {
      "number": 2,
      "timing": "3-6s",
      "type": "SHOWCASE",
      "description": "Shot description - let the product's actual appearance shine",
      "camera": "camera movement",
      "audio": "audio cue"
    },
    {
      "number": 3,
      "timing": "6-8s",
      "type": "HERO",
      "description": "Final shot with slogan",
      "camera": "camera movement",
      "audio": "audio cue"
    }
  ],
  "product_appearance_note": "Brief note about what aspects of the product you're uncertain about"
}
"""
```

---

## 📊 用户确认界面（显示置信度）

### 产品识别结果

```markdown
## 🎯 产品识别结果

| 属性 | 识别结果 | 置信度 | 是否用于视频描述 |
|------|----------|--------|------------------|
| **类型** | 厨房电器 | 🟢 95% | ✅ 是 |
| **名称** | 空气炸锅 | 🟢 92% | ✅ 是 |
| **颜色** | 白色 | 🟢 90% | ✅ 是 |
| **形状** | 方形立式 | 🟢 88% | ✅ 是 |
| **材质** | 未知（看起来像塑料） | 🟡 55% | ❌ 否（交由 Veo 判断） |
| **品牌** | 未识别 | 🔴 20% | ❌ 否（保持原样） |
| **纹理** | 未知 | 🔴 40% | ❌ 否（保持原样） |

### 🛡️ 产品保护说明

> 为保护产品外观不走样，以下属性将**不会**在视频提示词中详细描述，而是让 Veo 3.1 直接参考原图：
> - 材质（置信度 55% < 80%）
> - 品牌（置信度 20% < 80%）
> - 纹理（置信度 40% < 80%）
>
> 这确保视频中的产品外观与您提供的原图保持一致。

---
👆 以上识别结果是否准确？低置信度属性将保持原样不做描述。
- 回复「确认」继续
- 回复「修改」并告诉我需要调整的内容
```

---

## 🎥 Veo 3.1 最终提示词模板

**注意：低置信度属性使用通用表述**

```
Premium 8-second TVC commercial.

PRODUCT APPEARANCE PROTECTION (CRITICAL):
- The product MUST appear EXACTLY as shown in the input image
- DO NOT modify, enhance, or reimagine the product's appearance
- Maintain exact shape, color, proportions, and all visible details
- If there are logos or brand elements, keep them exactly as shown
- The input image is the ONLY source of truth for product appearance

PRODUCT: [仅包含高置信度属性，如 "white kitchen appliance with digital display"]
         [低置信度属性省略，由 Veo 从图片判断]

SCENE: Modern minimalist kitchen with marble countertop
LIGHTING: Soft natural morning light
MOOD: Fresh, clean, inviting

SHOTS:
- 0-3s: The product is revealed in its natural kitchen setting. Camera: Slow dolly in
- 3-6s: Smooth orbital rotation showcasing the product from multiple angles. Camera: 60-degree arc
- 6-8s: Hero shot with product centered, slogan fades in. Camera: Static with subtle drift

SLOGAN: "Crisp Perfection"

ABSOLUTE REQUIREMENT: The product's visual appearance must be IDENTICAL to the input image.
No creative liberties with product design, color, shape, or branding.
```

---

## 💡 Tips 生成（视频等待期间）

```python
TIPS_PROMPT = """基于产品类型：{product_type}

生成 5 条关于如何保护产品外观、写出更好广告提示词的技巧。

重点强调：
1. 如何避免产品外观走样
2. 哪些细节不应该过度描述
3. 如何让视频保持产品原始形态
4. 场景选择的技巧
5. 运镜设计的建议

用中文输出。"""
```

---

## 模型配置

| 功能 | 模型 ID |
|------|---------|
| 产品识别（带置信度） | `moonshotai/kimi-k2.5` |
| 分镜脚本 | `moonshotai/kimi-k2.5` |
| Tips 生成 | `moonshotai/kimi-k2.5` |
| **视频生成** | `google/veo3.1/image-to-video` |

---

## 版本历史

- **v3.7.0** - 🛡️ 核心升级：引入置信度判断机制，低于 80% 的属性不进入提示词；强化产品外观保护
- **v3.6.0** - 新增交互式确认流程；Tips 贴士；多语言支持
- **v3.5.x** - 优化分镜结构；智能场景选择
