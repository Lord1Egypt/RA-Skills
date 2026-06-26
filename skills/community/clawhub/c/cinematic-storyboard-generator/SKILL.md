---
name: cinematic-storyboard-generator
description: Generate professional, cinema-grade storyboard prompts for AI image/video generation platforms (LibTV/LibLib, 即梦, Seedance, Kling, etc.). Use when creating shot-by-shot visual prompts for short dramas, films, promotional videos, or any cinematic content. Triggers on: 写分镜, 生成分镜, 分镜提示词, storyboard, shot list, 镜头设计, 影视级提示词, 短剧分镜, AI生图提示词, AI视频提示词. Includes: seven essential elements framework, four iron rules (asset anchoring, light logic, material consistency, spatial coherence), quality checklist, scene-type-specific guidance (ancient/fantasy, modern, overseas formats), shot type reference, and transition words. Built from professional film cinematography standards — not generic prompt templates, but cinema-level methodology.
---

# Cinematic Storyboard Generator

Generate professional, cinema-grade image prompts for AI generation platforms (LibTV/LibLib, 即梦, Seedance, etc.).

## Quick Start

**Every shot prompt must contain these 7 elements** (in order):

```
日夜景 · 主体描述 · 空间坐标 · 镜头形式 · 光影设计 · 情绪落点 · 资产锚点
```

Example:
```
夜 · 男主立于城楼最高处，深褐短发金色发带，灰色对襟长袍金色云纹刺绣，拂尘横握 · 身后城墙延展，脚下士兵阵列，前景地面 · 远景 · 低角仰拍 · 固定镜头 · 侧逆光，金色月光从左侧45度打入，硬光，冷蓝#8899BB · 肃穆 · 战意凝聚 · 参考：宿迁_霸王故居_场景图.png + 定妆照_季沧海.png
```

---

## Four Iron Rules

### Rule 1: Asset Anchoring
- Character description **MUST** reference actual costume photo (定妆照)
- Scene description **MUST** reference actual scene image file
- Never imagine what an asset looks like — if you haven't seen the photo, don't write details
- Append asset paths at end of every prompt

### Rule 2: Light Logic
- **Single main light only** — never write multiple light sources
- Direction must be specific: "侧逆光从右侧45度打入" — not "自然光"
- Contact shadows required: "投影落地面，方向与光源一致" — characters don't float
- Back/side lighting preferred — frontal soft light = AI feel = fake

### Rule 3: Material Consistency
- Skin: "真实皮肤纹理，无磨皮无柔光" — not "细腻白皙"
- Clothing: "有重力垂坠感，真实褶皱，非贴图感"
- Scene-character same rendering space: "三层可信纵深：前景地面反光 → 中景人物 → 远景建筑轮廓"

### Rule 4: Spatial Coherence
- Characters stand on ground with physically correct shadows
- Three-layer depth: near ground reflection → middle ground character → far ground scene outline
- Portal/doorway as spatial boundary — not VFX effect rings
- Scale reference: character height ~1/5 of frame in wide shots

---

## Shot Sequence Design

### Step 1: Analyze the Scene
- Read the script/description
- Confirm emotion curve (what does the audience feel at this moment?)
- Identify key action and turning point

### Step 2: Confirm Assets First
- View all relevant costume photos (定妆照)
- View all relevant scene images
- Establish main light direction based on time of day
- Mark asset paths before writing prompts

### Step 3: Build the Sequence
Write prompts one by one. Each prompt is independent and complete.

| Sequence Position | Purpose | Shot Type |
|-------------------|---------|-----------|
| Opening (1-3) | Establish atmosphere, introduce setting | Wide/establishing |
| Middle (4-N) | Develop tension, reveal details | Medium/close-up |
| Climax (N-2) | Emotional peak | Close-up/extreme close-up |
| Ending (last 1-2) | Release, transition | Wide/freeze frame |

### Step 4: Quality Check Each Prompt
Before finishing, verify:
- [ ] Day/night marked in first clause
- [ ] Character description matches costume photo
- [ ] Scene has specific asset anchor
- [ ] Light direction is specific (no "自然光")
- [ ] Character has ground shadow (not floating)
- [ ] Skin texture without retouching
- [ ] Clothing has weight/draping
- [ ] Three-layer depth is physically coherent
- [ ] Shot type matches emotion
- [ ] Asset paths annotated at end

---

## Scene Type Reference

### Ancient/Fantasy (古装/仙侠)

**Light frameworks:**
| Time | Main Light | Shadow | Texture |
|------|-----------|--------|---------|
| Morning | Side backlight, golden #D4A574 | Cool blue #4A3F6B | Dust visible in light beams |
| Dusk | Side light, orange-red, low angle | Deep orange to blue-purple | Long shadows, golden rim light |
| Night | Moonlight, cool blue #8899BB + lantern warm orange #FF6B35 | Cold-warm contrast | Volumetric light, mist |

**Common scenes:**
- Temple/mountain: Stone steps, cloud sea, ancient bells, pine trees
- Battlefield: Yellow earth, cracked, broken banners, dust, rusty metal weapons
- Interior: Wood structure, rammed earth walls, paper windows, bronze vessels

### Modern Short Drama (现代短剧)

**Light:** Natural interior light, window light with side backlight preferred. Avoid frontal soft light.

**Scenes:** Apartment, office, street, convenience store — real environments with specific details.

### Overseas Format

**Style:** Realism, natural color grading, no stylizing filters. Skin texture realistic-level.

**Frame:** 9:16 vertical (short drama format) or 16:9 horizontal (film).

---

## Shot Type Reference

| Shot | Use When | Vertical Height Ratio |
|------|-----------|----------------------|
| Extreme Wide / 全景 | Establishing shot, full scene | ~1/5 of frame |
| Wide / 远景 | Scene environment, large movement | ~1/4 of frame |
| Medium / 中景 | Narrative主体, character relationships | ~1/3 of frame |
| Close-up / 近景 | Focus on performance, expressions | Chest and above |
| Extreme Close-up / 特写 | Emotion amplification, key props | Single body part |

**Angle-Emotion mapping:**
| Angle | Emotional Effect |
|-------|-----------------|
| Low angle upward / 低角仰拍 | Power, authority,压迫感 |
| High angle downward / 高角俯拍 | Vulnerability, disadvantage |
| Eye level / 平视 | Objective, equal, confrontational |
| Profile / 侧面 | Narrative, observational |
| Back / 背面 | Mystery, leading viewer into frame |

---

## Transition Words

| Type | Usage | Example |
|------|-------|---------|
| Time | "随月光升起..." | Transition from day to night |
| Space | "画面从...过渡到..." | Scene to scene |
| Dissolve | " ↔ " | "古钟 ↔ 水面，金字浮现" |
| Hard cut | "下一秒..." | Scene switch |
| Match cut | "场景切换至..." | Cut to matching composition |

---

## Reference Files

For detailed elements checklist, see [prompt-elements.md](prompt-elements.md).
For scene-type-specific guidance (ancient/fantasy), see [scene-ancient.md](scene-ancient.md).