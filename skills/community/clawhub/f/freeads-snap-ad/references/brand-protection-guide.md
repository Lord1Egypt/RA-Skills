# 品牌保护最佳实践指南

本文档提供品牌/LOGO 保护的完整技术方案，确保在 AI 图像和视频生成过程中保持品牌标识的清晰度和一致性。

## 目录

1. [品牌保护概述](#1-品牌保护概述)
2. [LOGO 收集与处理](#2-logo-收集与处理)
3. [抠图阶段品牌保护](#3-抠图阶段品牌保护)
4. [视频生成一致性保护](#4-视频生成一致性保护)
5. [常见问题与解决方案](#5-常见问题与解决方案)
6. [Prompt 模板库](#6-prompt-模板库)

---

## 1. 品牌保护概述

### 1.1 为什么需要品牌保护？

在 AI 图像和视频生成过程中，品牌元素可能出现以下问题：

| 问题类型 | 描述 | 影响 |
|---------|------|------|
| LOGO 模糊 | AI 处理后 LOGO 清晰度下降 | 品牌识别度降低 |
| LOGO 变形 | 比例、形状发生改变 | 品牌形象受损 |
| 颜色偏移 | 品牌色彩不准确 | 品牌一致性破坏 |
| 产品变形 | 视频中产品外观变化 | 用户信任度下降 |
| 场景不一致 | 多镜头间场景跳变 | 观看体验差 |

### 1.2 品牌保护三大原则

1. **清晰度优先** - LOGO 和文字必须保持清晰可读
2. **一致性保证** - 颜色、形状、比例全程一致
3. **完整性保护** - 不遮挡、不裁切、不变形

### 1.3 保护等级定义

| 等级 | 适用场景 | 保护强度 |
|-----|---------|---------|
| **高 (high)** | 品牌广告、官方宣传 | 严格保护，不允许任何变化 |
| **中 (medium)** | 社交媒体内容 | 适度保护，允许轻微艺术效果 |
| **低 (low)** | 内部测试、草稿 | 基本保护，允许创意变化 |

---

## 2. LOGO 收集与处理

### 2.1 LOGO 收集对话模板

```markdown
> 在生成广告前，我想了解一下您的品牌信息，以确保广告效果最佳：
>
> **您的产品是否有品牌 LOGO 或标识？**
>
> **选项 A：有品牌 LOGO** 
> 我可以帮您在生成过程中保护 LOGO 不走样、产品外观不变形。请提供：
> - 📷 直接粘贴 LOGO 图片（推荐 PNG 透明背景）
> - 🔗 提供 LOGO 图片链接
> - 🔍 告诉我品牌名称，我来帮您网络搜索
>
> **选项 B：没有品牌/暂时跳过**
> 直接进行广告生成，我仍会保护产品外观一致性
```

### 2.2 品牌信息数据结构

```python
brand_info = {
    # 基础信息
    "has_brand": True,                    # 是否有品牌
    "brand_name": "品牌名称",              # 品牌名称
    
    # LOGO 信息
    "logo_url": "https://...",            # LOGO 图片 URL
    "logo_format": "png",                 # 图片格式（推荐 PNG）
    "logo_resolution": "高清",            # 分辨率描述
    
    # 位置信息
    "logo_position": "产品正面中央",       # LOGO 在产品上的位置
    "logo_size": "中等",                  # LOGO 相对大小
    
    # 品牌视觉
    "brand_colors": ["#FF0000", "#FFFFFF"], # 品牌主色调
    "brand_fonts": ["Helvetica"],          # 品牌字体（如有）
    
    # 保护设置
    "protection_level": "high",           # 保护等级
    "special_requirements": ""            # 特殊要求
}
```

### 2.3 LOGO 获取方式

#### 方式一：用户直接提供图片

```python
# 1. 用户上传图片文件
logo_file_path = "/path/to/logo.png"

# 2. 上传到 Atlas Cloud
upload_response = requests.post(
    "https://api.atlascloud.ai/api/v1/model/uploadMedia",
    headers={"Authorization": f"Bearer {api_key}"},
    files={"file": open(logo_file_path, "rb")}
)
logo_url = upload_response.json().get("url")
```

#### 方式二：用户提供 URL

```python
# 直接使用用户提供的 URL
logo_url = "https://example.com/brand-logo.png"

# 验证 URL 可访问
response = requests.head(logo_url)
if response.status_code == 200:
    brand_info["logo_url"] = logo_url
else:
    raise Exception("LOGO URL 无法访问，请检查链接")
```

#### 方式三：网络搜索

使用 `search_web` 工具搜索品牌 LOGO：

```
搜索关键词建议：
- "{品牌名} logo png 透明背景"
- "{品牌名} official logo"
- "{品牌名} brand logo high resolution"
```

**搜索后验证步骤：**
1. 检查图片清晰度
2. 确认是官方 LOGO（非用户制作）
3. 询问用户确认是否正确

---

## 3. 抠图阶段品牌保护

### 3.1 标准品牌保护 Prompt

```
Remove the background COMPLETELY while applying STRICT brand protection:

=== PRODUCT INTEGRITY (CRITICAL) ===
- Maintain EXACT product shape and proportions - no distortion allowed
- Keep ALL textures and surface details crisp and sharp
- Preserve material appearance (metal, glass, plastic, fabric, etc.) perfectly
- Colors must remain accurate - no color shifting

=== BRAND LOGO PROTECTION (TOP PRIORITY) ===
- Keep ALL brand logos 100% sharp, legible, and undistorted
- The brand LOGO located at: [LOGO位置描述]
- Maintain exact logo colors without ANY shift
- Preserve logo proportions PERFECTLY - no stretching or compression
- Do NOT blur, obscure, or modify any brand text or symbols
- Brand name: [品牌名称]

=== OUTPUT REQUIREMENTS ===
- Place on pure white (#FFFFFF) background
- Add subtle professional shadow for depth
- Professional studio lighting simulation
- Ensure edges are clean and precise

The product authenticity and brand elements are the TOP PRIORITY.
```

### 3.2 不同保护等级的 Prompt

#### 高保护等级 (high)

```
CRITICAL BRAND PROTECTION - HIGHEST PRIORITY:

This is an official brand advertisement. The brand LOGO must be treated as SACRED:
- ZERO tolerance for LOGO distortion, blurring, or color shift
- Brand LOGO must remain pixel-perfect sharp
- Every character in brand text must be 100% legible
- Brand colors must match EXACTLY: [色值列表]

Product integrity is equally important:
- Product shape: EXACT preservation required
- Product colors: NO shifting allowed
- Product textures: CRISP and DETAILED

Background: Pure white (#FFFFFF)
Lighting: Professional studio, highlight brand elements
```

#### 中保护等级 (medium)

```
BRAND PROTECTION - STANDARD:

Protect brand elements while allowing subtle artistic enhancements:
- Keep LOGO clear and recognizable
- Maintain brand color accuracy (±5% tolerance)
- Product proportions should be preserved
- Light artistic shadows or highlights acceptable

Background: Clean white or subtle gradient
Lighting: Professional, can include creative lighting effects
```

#### 低保护等级 (low)

```
BASIC PRODUCT ENHANCEMENT:

Focus on visual appeal while maintaining product recognition:
- Keep product identifiable
- Brand elements should remain visible
- Creative lighting and effects allowed
- Minor stylization acceptable

Background: White or creative backgrounds
Lighting: Artistic freedom allowed
```

### 3.3 Python 实现

```python
def get_background_removal_prompt(brand_info: dict) -> str:
    """
    根据品牌信息生成抠图提示词
    
    Args:
        brand_info: 品牌信息字典
        
    Returns:
        完整的抠图提示词
    """
    protection_level = brand_info.get("protection_level", "high")
    has_brand = brand_info.get("has_brand", False)
    
    # 基础产品保护
    base_prompt = """Remove the background COMPLETELY while preserving product integrity:

PRODUCT REQUIREMENTS:
- Maintain EXACT product shape and proportions
- Keep ALL textures and surface details crisp
- Preserve material appearance perfectly
- Colors must remain accurate"""

    # 品牌保护部分
    if has_brand:
        brand_name = brand_info.get("brand_name", "N/A")
        logo_position = brand_info.get("logo_position", "on the product")
        brand_colors = brand_info.get("brand_colors", [])
        
        if protection_level == "high":
            brand_prompt = f"""

CRITICAL BRAND PROTECTION (TOP PRIORITY):
- Brand: {brand_name}
- LOGO Location: {logo_position}
- Brand Colors: {', '.join(brand_colors) if brand_colors else 'preserve original'}
- Keep ALL brand logos 100% sharp and undistorted
- ZERO tolerance for LOGO blur or color shift
- Every character must be perfectly legible
- Proportions must be EXACTLY preserved"""
        
        elif protection_level == "medium":
            brand_prompt = f"""

BRAND PROTECTION (STANDARD):
- Brand: {brand_name}
- LOGO Location: {logo_position}
- Keep brand elements clear and recognizable
- Maintain color accuracy (minor tolerance allowed)
- LOGO should remain sharp and readable"""
        
        else:  # low
            brand_prompt = f"""

BASIC BRAND AWARENESS:
- Brand: {brand_name}
- Keep brand elements visible and identifiable"""
    else:
        brand_prompt = """

DETAIL PRESERVATION:
- Keep any text or labels readable
- Preserve all product markings"""

    # 输出要求
    output_prompt = """

OUTPUT:
- Place on pure white (#FFFFFF) background
- Add subtle professional shadow for depth
- Professional studio lighting
- Clean, precise edges"""

    return base_prompt + brand_prompt + output_prompt
```

---

## 4. 视频生成一致性保护

### 4.1 视频一致性核心原则

在多帧视频生成中，必须确保：

| 维度 | 要求 | 检查点 |
|-----|------|--------|
| **产品形状** | 始终保持相同 | 开始/中间/结束帧对比 |
| **产品大小** | 不能缩放变化 | 除非镜头推拉 |
| **LOGO 清晰度** | 全程清晰可读 | 每帧检查 |
| **颜色一致** | 无色偏 | 品牌色监控 |
| **场景统一** | 背景/灯光一致 | 无突变 |

### 4.2 视频一致性 Prompt 模板

```
Cinematic product advertisement video.

[基础视频描述]

=== MANDATORY CONSISTENCY REQUIREMENTS (CRITICAL) ===

1. PRODUCT SHAPE CONSISTENCY:
   - Product MUST maintain EXACT shape throughout ALL frames
   - Size and proportions MUST NOT change at any point
   - No morphing, warping, stretching, or deformation allowed
   - Product silhouette must remain identical from start to finish

2. BRAND LOGO CONSISTENCY:
   - Brand LOGO must remain CLEARLY VISIBLE throughout
   - LOGO must stay sharp and undistorted in every frame
   - LOGO position: [位置描述]
   - Brand colors must remain CONSISTENT - no color shifting

3. SCENE CONSISTENCY:
   - Lighting must remain uniform throughout the video
   - Background must stay consistent (pure white)
   - Shadow position and intensity must be consistent
   - No sudden lighting changes or flickering

4. MOTION QUALITY:
   - Camera movement must be SMOOTH and STEADY
   - No jarring transitions or sudden movements
   - Motion should be elegant and professional

=== TECHNICAL SPECIFICATIONS ===
- Professional studio lighting with soft diffused key light
- Premium advertising aesthetic
- Clean, elegant motion
- 1080p resolution, 24fps
- Pure white or subtle gradient background

The product is the HERO - it must look IDENTICAL from first frame to last.
```

### 4.3 摄像机运动建议

不同摄像机运动对产品一致性的影响：

| 运动类型 | 一致性风险 | 推荐场景 | 品牌保护建议 |
|---------|-----------|---------|-------------|
| **静态 (static)** | 最低 | 高端品牌 | 首选，最安全 |
| **推镜 (dolly in)** | 低 | 展示细节 | 推荐，突出 LOGO |
| **环绕 (orbit)** | 中等 | 360° 展示 | 需确保 LOGO 各角度清晰 |
| **缩放 (zoom)** | 中等 | 聚焦重点 | 避免过度缩放 |
| **快速切换** | 高 | 动感广告 | 不推荐用于品牌广告 |

### 4.4 Python 实现

```python
def get_video_prompt_with_consistency(
    base_prompt: str,
    brand_info: dict,
    camera_style: str = "dolly_in"
) -> str:
    """
    生成包含一致性保护的视频提示词
    
    Args:
        base_prompt: 基础视频描述
        brand_info: 品牌信息
        camera_style: 摄像机运动风格
        
    Returns:
        完整的视频提示词
    """
    # 摄像机运动描述
    camera_movements = {
        "static": "Camera remains static with subtle product rotation, maintaining perfect clarity",
        "dolly_in": "Camera slowly dollies in, gradually revealing product details and brand elements",
        "orbit": "Camera smoothly orbits around the product at a consistent distance and speed",
        "zoom": "Gentle cinematic zoom emphasizing the product's premium quality",
        "dolly_out": "Camera slowly pulls back, revealing the complete product in context"
    }
    
    camera_desc = camera_movements.get(camera_style, camera_movements["dolly_in"])
    
    # 品牌保护指令
    brand_protection = ""
    if brand_info.get("has_brand"):
        brand_name = brand_info.get("brand_name", "")
        logo_position = brand_info.get("logo_position", "on the product")
        brand_colors = brand_info.get("brand_colors", [])
        
        brand_protection = f"""

=== BRAND PROTECTION (CRITICAL - MUST FOLLOW) ===
- Brand Name: {brand_name}
- The brand LOGO must remain CLEARLY VISIBLE throughout ALL frames
- LOGO must stay sharp, legible, and NEVER distorted or blurred
- LOGO position: {logo_position} - ensure this area is always in focus
- Brand colors {', '.join(brand_colors) if brand_colors else ''} must remain EXACTLY CONSISTENT
- Any brand text must remain readable at ALL times
- LOGO should be the focal point in at least 30% of frames"""

    # 构建完整提示词
    prompt = f"""Cinematic product advertisement video.

{base_prompt}

CAMERA MOVEMENT: {camera_desc}

=== MANDATORY CONSISTENCY REQUIREMENTS (CRITICAL) ===

1. PRODUCT CONSISTENCY:
   - Product MUST maintain EXACT shape throughout ALL frames
   - Size and proportions MUST NOT change (except natural perspective)
   - No morphing, warping, stretching, or deformation
   - Product silhouette must remain identical start to finish

2. APPEARANCE CONSISTENCY:
   - Colors must remain EXACTLY the same throughout
   - Textures and surface details must stay consistent
   - Material appearance must be uniform
   - No unexpected changes in product appearance
{brand_protection}

3. SCENE CONSISTENCY:
   - Lighting must remain uniform throughout
   - Background must stay consistent (pure white)
   - Shadow must be consistent in position and intensity
   - No sudden lighting changes or flickering

4. MOTION QUALITY:
   - Movement must be SMOOTH and STEADY
   - No jarring transitions
   - Elegant, professional motion
   - Consistent speed throughout

=== TECHNICAL SPECIFICATIONS ===
- Professional studio lighting with soft key light
- Premium advertising aesthetic
- Clean, elegant motion
- 1080p resolution, 24fps
- Pure white or subtle gradient background

The product is the HERO - it must look IDENTICAL and PERFECT from first to last frame."""

    return prompt
```

---

## 5. 常见问题与解决方案

### 5.1 LOGO 模糊问题

**症状**：抠图后 LOGO 清晰度下降

**解决方案**：
1. 确保原图中 LOGO 清晰（分辨率足够）
2. 使用高保护等级 prompt
3. 在 prompt 中明确强调 LOGO 位置
4. 尝试分两步：先抠图保留 LOGO，再优化背景

```
Enhanced prompt addition:
"Pay EXTRA attention to the brand LOGO area at [位置]. 
This area must remain PIXEL-PERFECT sharp.
Increase edge definition around text and logo elements."
```

### 5.2 颜色偏移问题

**症状**：品牌颜色在生成后发生变化

**解决方案**：
1. 在 prompt 中指定准确的色值
2. 使用"exact color match"等强调词
3. 提供品牌色板参考

```
Enhanced prompt addition:
"CRITICAL COLOR REQUIREMENTS:
- Primary brand color MUST be exactly #[色值]
- Secondary color MUST be exactly #[色值]
- Zero tolerance for color shifting or desaturation"
```

### 5.3 视频中产品变形

**症状**：视频播放过程中产品形状/大小变化

**解决方案**：
1. 使用更简单的摄像机运动（静态或推镜）
2. 增强一致性约束词
3. 降低视频时长（4秒比8秒更稳定）
4. 使用"no morphing"等明确禁止词

```
Enhanced prompt addition:
"ABSOLUTE PROHIBITION:
- NO morphing of the product shape
- NO scaling changes (except camera perspective)
- NO warping or stretching
- Product must be 100% RIGID throughout"
```

### 5.4 多镜头不连贯

**症状**：视频中不同时段场景/灯光差异明显

**解决方案**：
1. 强调"uniform lighting throughout"
2. 使用"consistent background"
3. 避免复杂的摄像机运动组合
4. 选择单一、简单的运动类型

```
Enhanced prompt addition:
"SCENE CONTINUITY:
- Lighting setup must remain EXACTLY the same from frame 1 to last frame
- Background must be UNIFORM white throughout
- NO scene transitions or lighting changes
- Create the illusion of a SINGLE continuous shot"
```

---

## 6. Prompt 模板库

### 6.1 高端品牌广告 Prompt

```
Ultra-premium product advertisement featuring [产品名] by [品牌名].

The product stands majestically on pure white background.
Professional studio lighting creates elegant highlights and subtle shadows.
Camera performs a slow, cinematic dolly-in revealing exquisite details.

BRAND REQUIREMENTS:
- The [品牌名] LOGO at [位置] must remain crystal clear throughout
- Brand colors [色值] must be perfectly preserved
- Premium, luxury aesthetic aligned with brand identity

CONSISTENCY REQUIREMENTS:
- Product shape: UNCHANGING throughout
- Product size: CONSISTENT (natural perspective only)
- LOGO clarity: SHARP in every frame
- Colors: EXACT match throughout
- Lighting: UNIFORM, professional studio

Motion: Elegant, refined, befitting a luxury brand
Quality: Cinematic, 1080p, smooth 24fps
```

### 6.2 科技产品广告 Prompt

```
Cutting-edge technology product showcase for [产品名].

The device emerges with subtle tech-inspired lighting.
Clean lines and surfaces catch professional studio lights.
Camera smoothly orbits, revealing innovative design details.

BRAND REQUIREMENTS:
- [品牌名] LOGO must be clearly visible and sharp
- Tech-forward aesthetic while protecting brand identity
- Product design integrity is paramount

CONSISTENCY REQUIREMENTS:
- Device shape: RIGID, no warping or morphing
- Display/screens: Consistent brightness and content
- Material finishes: Consistent reflections
- LOGO: Clear and legible throughout

Motion: Smooth, precise, technological
Quality: Crisp, modern, 1080p
```

### 6.3 生活美学产品 Prompt

```
Lifestyle product advertisement for [产品名] by [品牌名].

The product rests on clean white surface with warm, inviting lighting.
Soft shadows create depth and approachability.
Camera gently approaches, emphasizing natural beauty and quality.

BRAND REQUIREMENTS:
- [品牌名] branding visible and clear
- Warm, authentic aesthetic
- Product authenticity is key

CONSISTENCY REQUIREMENTS:
- Product appearance: Natural and consistent
- Colors: True to life, no artificial shifts
- Textures: Authentic material representation
- LOGO: Naturally integrated but readable

Motion: Gentle, organic, inviting
Quality: Warm, authentic, 1080p
```

---

## 附录：快速参考

### 品牌保护关键词

| 英文关键词 | 用途 |
|-----------|------|
| pixel-perfect | 像素级完美 |
| undistorted | 无变形 |
| legible | 可读的 |
| crisp | 清晰的 |
| consistent | 一致的 |
| exact match | 精确匹配 |
| no morphing | 禁止变形 |
| preserve proportions | 保持比例 |
| brand integrity | 品牌完整性 |
| color accuracy | 颜色准确度 |

### 一致性约束关键词

| 英文关键词 | 用途 |
|-----------|------|
| throughout all frames | 贯穿所有帧 |
| from first to last | 从头到尾 |
| uniform | 统一的 |
| continuous | 连续的 |
| rigid | 刚性的（不变形） |
| steady | 稳定的 |
| smooth | 平滑的 |
| identical | 完全相同的 |
