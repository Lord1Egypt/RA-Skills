# Multi-Platform Workflow

多平台图片适配工作流。一份内容 → 多平台输出。

## Workflow Overview

```
原始内容
    ↓
[平台分析] → 确定目标平台规格
    ↓
[风格映射] → 保持品牌一致性
    ↓
[布局调整] → 适配不同比例
    ↓
[文字重排] → 符合平台阅读习惯
    ↓
[生成 Prompt] → 各平台独立 prompt
    ↓
[批量生成] → 并行执行
```

## Step 1: Platform Analysis

### Input
- 原始内容（文字/主题）
- 目标平台列表（默认：xiaohongshu + pinterest）

### Output
| Platform | Ratio | Priority | Notes |
|----------|-------|----------|-------|
| xiaohongshu | 3:4 | 主平台 | 中文内容，封面优先 |
| pinterest | 2:3 | 次平台 | 英文翻译，SEO 优化 |

### Decision Matrix

| 内容类型 | 主平台 | 次平台 | 理由 |
|----------|--------|--------|------|
| 中文科普 | xiaohongshu | - | 语言限制 |
| 英文教程 | pinterest | instagram | SEO + 视觉 |
| 双语内容 | xiaohongshu | pinterest | 最大化覆盖 |
| 品牌形象 | 全平台 | - | 一致性优先 |

## Step 2: Style Mapping

保持跨平台视觉一致性：

```yaml
core_elements:
  - 主色调（不变）
  - 字体家族（不变）
  - 装饰元素（微调密度）
  - 品牌 Logo（位置适配）

platform_adaptations:
  xiaohongshu:
    - 增加细节密度
    - 封面冲击力优先
  pinterest:
    - 简化文字（英文更短）
    - SEO 关键词前置
  instagram:
    - 中心构图
    - 适配 Feed 美学
```

## Step 3: Layout Adaptation

### 3:4 → 2:3 (XHS → Pinterest)

```
原始 (3:4)              适配后 (2:3)
┌──────────┐           ┌──────────┐
│  标题区   │           │  标题区   │ ← 更高，容纳英文
├──────────┤           │ (expanded)│
│          │           ├──────────┤
│  内容区   │    →      │          │
│          │           │  内容区   │ ← 拉伸
│          │           │          │
├──────────┤           │          │
│  底部区   │           │  底部区   │
└──────────┘           └──────────┘
   1080×1440              1000×1500
```

**调整策略**：
1. 垂直拉伸 104% (1500/1440)
2. 标题区扩大 15-20%（英文通常更长）
3. 内容区重新分布
4. 保持视觉重心在 40-60% 高度

### 3:4 → 1:1 (XHS → IG Square)

```
原始 (3:4)              适配后 (1:1)
┌──────────┐           ┌──────────┐
│  标题区   │  [裁剪]   │  标题区   │
├──────────┤    →      │ (精简)   │
│          │           ├──────────┤
│  内容区   │           │  内容区   │
│          │           │ (压缩)   │
├──────────┤           └──────────┘
│  底部区   │  [删除]
└──────────┘
   1080×1440              1080×1080
```

**调整策略**：
1. 删除底部区（或合并到内容区）
2. 标题精简为 1 行
3. 内容区压缩 30%
4. 中心聚焦构图

### 3:4 → 16:9 (XHS → YouTube)

```
原始 (3:4)              适配后 (16:9)
┌──────────┐           ┌────────────────────┐
│  标题区   │           │  标题区 (超大字号)  │
├──────────┤    →      │                    │
│          │           │      主体图         │
│  内容区   │           │   (横向扩展)        │
│          │           │                    │
├──────────┤           └────────────────────┘
│  底部区   │
└──────────┘
   1080×1440              1280×720
```

**调整策略**：
1. 完全重构布局（纵向→横向）
2. 标题字号扩大 50%（缩略图可读性）
3. 内容简化为 1-2 个核心点
4. 高对比度（深色背景 + 亮色文字）

## Step 4: Text Adaptation

### 文字长度调整

| 平台 | 标题限制 | 正文限制 | 策略 |
|------|----------|----------|------|
| xiaohongshu | ≤20 字 | ≤800 字 | 详细解释 |
| pinterest | ≤100 字符 | ≤500 字符 | 关键词优先 |
| instagram | ≤125 字符 (caption) | 无限制 | 故事性 |
| youtube | ≤60 字符 (缩略图) | N/A | 冲击短语 |

### 语言适配

**中文 → 英文**：
```
中文：「12 星座本周运势详解」
英文：「Weekly Horoscope: All 12 Signs」

中文：「塔罗牌入门：愚人牌解读」
英文：「Tarot 101: The Fool Card Meaning」
```

**原则**：
- 英文更简洁（通常短 20-30%）
- 关键词前置（SEO）
- 避免直译，用自然地道的表达

## Step 5: Prompt Generation

为每个平台生成独立 prompt：

```yaml
xhs_prompt:
  aspect_ratio: "3:4"
  text_elements:
    - "Text on image in Chinese: '标题'"
  style: "mystic"
  layout: "balanced"

pinterest_prompt:
  aspect_ratio: "2:3"
  text_elements:
    - "Text on image in English: 'SEO Title'"
  style: "mystic"
  layout: "balanced"
  priority: "top 40 chars for search snippet"

instagram_prompt:
  aspect_ratio: "1:1"
  text_elements:
    - "Text on image in English: 'Short Title'"
  style: "mystic"
  layout: "card"
  composition: "centered"
```

## Step 6: Batch Generation

### 并行执行

```bash
# 伪代码示例
for platform in [xhs, pinterest, ig]:
    generate_image(prompt[platform])
```

### 一致性检查

生成后验证：
- [ ] 色调一致（主色相同）
- [ ] 字体一致（同一家族）
- [ ] 风格一致（同一 preset）
- [ ] 品牌元素一致（Logo/水印位置）

## Platform-Specific Checklists

### Xiaohongshu Checklist
- [ ] 封面 3 秒法则：能否一眼看懂？
- [ ] 右上角安全区：避开互动图标
- [ ] 底部安全区：避开标题栏
- [ ] 中文文字无错别字
- [ ] 标签 5-10 个

### Pinterest Checklist
- [ ] 标题前 40 字符含关键词
- [ ] 英文无语法错误
- [ ] 文字在小图下清晰可读
- [ ] 垂直构图充分利用
- [ ] Board 分类正确

### Instagram Checklist
- [ ] 中心构图
- [ ] 适配 Feed 美学
- [ ] Caption 有故事性
- [ ] Hashtags 15-30 个
- [ ] 与前后帖子协调

### YouTube Checklist
- [ ] 缩略图缩小到 10% 仍清晰
- [ ] 文字≥48pt 等效
- [ ] 高对比度
- [ ] 人脸表情夸张
- [ ] 数字/列表吸引点击

## Export & Delivery

```
Output Folder Structure:
output/
├── xiaohongshu/
│   ├── 01-cover.png
│   ├── 02-content.png
│   └── 03-ending.png
├── pinterest/
│   ├── 01-cover.png
│   └── 02-content.png
└── instagram/
    ├── 01-feed.png
    └── 02-story.png
```

### File Naming
- `{platform}/{sequence}-{type}.png`
- 序列号保持跨平台一致（便于对照）

### Metadata
- 保留平台特定的 EXIF/关键词
- 删除拍摄信息（AI 生成无需保留）
