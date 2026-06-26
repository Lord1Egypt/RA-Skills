---
name: aura-xhs-images
version: 1.3.2
description: Xiaohongshu infographic card style presets and prompt templates for astrology, tarot, and lifestyle content. Provides 8 visual styles × 8 layouts with ready-to-use prompt templates. Use when user mentions '小红书卡片', '小红书图片', 'XHS cards', '信息图卡片', '星宿卡片', '塔罗卡片', or wants to create visual card series for Xiaohongshu posts. This skill assembles prompts and provides style guidance — actual image generation requires external AI image tools (Midjourney/SD/DALL-E/通义万象等). ⚠️ Upgraded: Use `aura-image-gen` for multi-platform support (Pinterest, Instagram, YouTube, etc.).
---

# Aura XHS Images (小红书卡片生成)

Generate eye-catching Xiaohongshu card series. Style × Layout two-dimensional system.

## Two Dimensions

| Dimension | Controls | Options |
|-----------|----------|---------|
| **Style** | Visual aesthetics | mystic, cute, notion, bold, retro, ink-wash, tarot, minimal |
| **Layout** | Information structure | sparse, balanced, dense, list, comparison, flow, card, spread |

## Style Gallery

| Style | Description | Best For |
|-------|-------------|----------|
| `mystic` (Default for astrology) | 深色星空+金色点缀，神秘玄学感 | 星宿合盘、塔罗解读 |
| `cute` | 甜系粉嫩，经典小红书风 | 星座日常、轻松科普 |
| `notion` | 极简线条手绘，知识感 | 关系对照表、知识卡片 |
| `bold` | 高对比强冲击，大字报 | 避坑指南、排行榜 |
| `retro` | 复古怀旧，做旧质感 | 传统文化、国风内容 |
| `ink-wash` | 水墨国风，中式美学 | 星宿神兽、传统占卜 |
| `tarot` | 塔罗牌艺术风，新艺术运动边框 | 塔罗解读、牌面赏析 |
| `minimal` | 极简高端，大量留白 | 金句、单牌解读 |

### Style: Mystic (详细定义)

```yaml
canvas:
  ratio: portrait-3-4
  grid: single | dual

colors:
  primary: ["#0A0E2A", "#1A1040"]  # 深夜蓝/深紫
  accent: ["#C9A96E", "#D4AF37"]   # 古铜金/正金
  text: ["#E8D5B7", "#FFFFFF"]     # 暖白/纯白
  glow: ["#6B5CE7", "#A78BFA"]     # 紫色光晕

elements:
  background: starfield | nebula-gradient
  decorations: [constellation-lines, star-sparkles, moon-phases]
  frames: gold-border | arch-frame | none
  emphasis: glow-highlight | gold-underline

typography:
  title: serif-elegant | brush-calligraphy
  body: clean-sans | handwritten
  numbers: display-large
```

### Style: Tarot (详细定义)

```yaml
canvas:
  ratio: portrait-3-4
  grid: single

colors:
  primary: ["#1B0A2E", "#2D1B4E"]  # 深紫
  accent: ["#D4AF37", "#B8860B"]    # 金
  highlight: ["#8B0000", "#4A0080"] # 深红/紫
  text: ["#F5E6CC", "#FFFFFF"]

elements:
  background: velvet-dark | ornate-pattern
  decorations: [art-nouveau-border, celestial-symbols, card-frame]
  frames: tarot-border | ornate-gold
  emphasis: gold-foil | emboss

typography:
  title: art-nouveau | display-serif
  body: elegant-serif
  card-name: all-caps-spaced
```

### Style: Ink-wash (详细定义)

```yaml
canvas:
  ratio: portrait-3-4

colors:
  primary: ["#1A1A1A", "#4A4A4A"]  # 墨色
  accent: ["#8B0000", "#C41E3A"]    # 朱红
  background: ["#F5F0E8", "#E8DCC8"] # 宣纸色
  text: ["#2C2C2C", "#8B0000"]

elements:
  background: rice-paper-texture | ink-splash
  decorations: [brush-strokes, seal-stamp, ink-dots]
  frames: scroll-border | none
  emphasis: red-seal | brush-circle

typography:
  title: brush-calligraphy
  body: kai-style
```

## Layout Gallery

| Layout | Density | Best For |
|--------|---------|----------|
| `sparse` | 1-2 points | 封面、金句、单牌 |
| `balanced` | 3-4 points | 标准内容、性格解读 |
| `dense` | 5-8 points | 知识卡片、对照表 |
| `list` | 4-7 items | 排行榜、清单 |
| `comparison` | 2 sides | 两人合盘、正逆位对比 |
| `flow` | 3-6 steps | 流程、时间线 |
| `card` | Single focus | 单张塔罗牌/星宿卡 |
| `spread` | Multi-position | 牌阵展示 |

## Language Support

| Language | When | Notes |
|----------|------|-------|
| 中文 | 小红书内容 | 默认，所有文字元素用中文 |
| English | Pinterest / international | 所有文字元素用英文 |
| 双语 | 用户指定 | 同一张图可以中英双语（标题中文+副标题英文） |

**Prompt language rule**: 
- AI 生图的 prompt 始终用**英文**（模型理解最好）
- 图片内的**展示文字**跟随目标平台语言
- Prompt 中用 `Text on image in Chinese: "xxx"` 或 `Text on image in English: "xxx"` 明确指定

### 星宿内容预设

| Preset | Style + Layout | Use Case |
|--------|---------------|----------|
| `xingxiu-profile` | mystic + balanced | 单宿性格解读 |
| `xingxiu-compatibility` | mystic + comparison | 两人合盘 |
| `xingxiu-ranking` | bold + list | 关系排行榜 |
| `xingxiu-lookup` | notion + dense | 查宿对照表 |
| `xingxiu-beast` | ink-wash + card | 星宿神兽卡 |

### 塔罗内容预设

| Preset | Style + Layout | Use Case |
|--------|---------------|----------|
| `tarot-single` | tarot + card | 单牌解读 |
| `tarot-spread` | tarot + spread | 牌阵解读 |
| `tarot-daily` | mystic + sparse | 每日一牌 |
| `tarot-guide` | notion + list | 新手教程 |
| `tarot-compare` | tarot + comparison | 正位vs逆位 |

### 通用预设

| Preset | Style + Layout | Use Case |
|--------|---------------|----------|
| `knowledge-card` | notion + dense | 干货知识卡 |
| `warning` | bold + list | 避坑指南 |
| `quote` | minimal + sparse | 金句封面 |

## Workflow

### Step 1: Analyze Content
- 识别内容类型（星宿/塔罗/知识/排行）
- 推荐 preset 或 style + layout 组合
- 确定图片数量（封面+内容+结尾）

### Step 2: Confirm
- 展示推荐方案
- 用户确认或调整

### Step 3: Generate Outline
每张图的：
- 位置（封面/内容/结尾）
- 文字内容
- 视觉概念
- 使用的 layout

### Step 4: Generate Images
- 为每张图组装 prompt（style + layout + content）
- 参考 `references/workflows/prompt-assembly.md` 拼装完整 prompt
- 使用任意 AI 生图工具执行（Midjourney/SD/DALL-E/通义万象等）
- 第一张作为视觉锚点，后续用第一张做参考保持风格一致
- 每张生成后报告进度

### Step 5: Output
```
Series Complete!
Topic: [topic]
Style: [style] · Layout: [layout]
Images: N total
Files: 01-cover.png, 02-content.png, ...
```

## Prompt Assembly

每张图的 prompt 结构：

```
Create a Xiaohongshu infographic card:

## Specs
- Aspect Ratio: 3:4 (1080×1440)
- Style: {from style definition}

## Visual Rules
{from style yaml: colors, elements, typography}

## Layout
{from layout definition: density, structure, whitespace}

## Content
Position: {cover/content/ending}
Text: {actual content}
Visual Concept: {description}

## Language
{Match content language}
```

## Visual Authenticity Tips

- Add slight asymmetry to compositions
- Offset text 2-3px from perfect center
- Include subtle texture noise in backgrounds
- Vary line thickness naturally
- Allow soft edges on color blocks

## References

**Presets** (style definitions — load when generating):
- `references/presets/mystic.md` — 玄学神秘风
- `references/presets/tarot.md` — 塔罗艺术风
- `references/presets/ink-wash.md` — 水墨国风
- `references/presets/cute.md` — 甜系少女风
- `references/presets/notion.md` — 极简知识风
- `references/presets/bold.md` — 高冲击力风

**Elements** (canvas specs):
- `references/elements/canvas.md` — 画布尺寸/安全区/布局网格

**Workflows** (process guides):
- `references/workflows/prompt-assembly.md` — Prompt 拼装指南
