# Design System Inspiration of UPerform

## 1. Visual Theme & Atmosphere

UPerform（优普丰）是一家专业Scrum/敏捷咨询公司，品牌视觉采用国际设计标准 **4 层结构**: **PRIMARY（蓝色主色）+ NEUTRALS（灰色中性）+ SECONDARY（金色辅助，可承担强调与点缀）+ ACCENT（橙色点缀，极度克制）**。各司其职——主色管品牌识别、灰色管功能支撑、金色管高级感与强调、橙色管行动信号（仅作最后手段）。

设计理念是"深邃、尊贵、活力"——深海蓝建立深邃感与权威性，灰色提供专业的文字层级支撑，尊贵金与香槟金为关键场景注入高端金属光泽并承担强调与点缀职责，活力橙与珊瑚光仅在最关键的行动信号点使用，整场不超过 1 处。**严格遵循 4 条铁律**：

1. **橙色全场 ≤ 1 处**（且尽可能不采用）
2. **金色永远搭配深色**（深海蓝 / 雾白）
3. **文字只走灰阶**（蓝/橙/金不参与正文）
4. **🆕 金色一律使用渐变，禁止纯色** —— 尊贵金 `#D4AF37` 与香槟金 `#F2D492` 是金属色，纯色使用会显得廉价（像油漆/荧光笔）。任何位置的金色（背景、底色、按钮、描边、文字）都必须用渐变呈现，否则就丢失"金属光泽"的高级感。大面积背景（卡片底色、Banner、章节页、Header）尤其禁止使用纯金色。

**关键特征：**

- **PRIMARY 主色（60-70% 视觉量）** — 海洋蓝 `#1E4976` 为主，深海蓝 `#0A2540` 为深色背景，天空蓝 `#2E6BA8` / 地平蓝 `#4A8FD8` 为辅助与点缀蓝，冰川蓝 `#E8F2FC` 为浅蓝底
- **NEUTRALS 中性色（5 档工具集）** — 碳黑 `#1A1A1A` / 石板灰 `#3D4852` / 钢铁灰 `#6B7785` / 银灰 `#A8B2BD` / 雾白 `#F5F7FA` — 只做文字层级/边框/背景，不参与品牌识别
- **SECONDARY 辅助色（高级感 + 强调点缀 ≤ 3 处）** — 尊贵金 `#D4AF37` + 香槟金 `#F2D492` 金属光泽渐变，用于 VIP 标识、奖项、关键数字；**同样可承担强调与点缀职责，是橙色的优先替代**
- **ACCENT 点缀色（行动信号 ≤ 1 处,尽可能不采用）** — 活力橙 `#FF6B35` + 珊瑚光 `#FF9B7D`，仅在最关键的 CTA 或单一增长点使用，整场不超过 1 处
- 按钮圆角 6px — 柔和但不失专业
- 专业字体：宋体 / 思源黑体（中文）+ Source Sans Pro（英文）

## 2. Color Palette & Roles

### 品牌主色：蓝色系

| 名称 | HEX | 用途 |
|------|-----|------|
| Deep Sea Blue（深海蓝） | `#0A2540` | 最深背景、深色封面、页脚、Hero 深色段 |
| Ocean Blue（海洋蓝） | `#1E4976` | **品牌主色**，主要深色区块、大标题 |
| Sky Blue（天空蓝） | `#2E6BA8` | 按钮、链接、强调边框、活跃态 |
| Horizon Blue（地平蓝） | `#4A8FD8` | **品牌次色**，次级按钮、信息卡片、进度条 |
| Glacier Blue（冰川蓝） | `#E8F2FC` | 浅色信息背景、引用块、卡片底色 |

### 中性色：灰色系

| 名称 | HEX | 用途 |
|------|-----|------|
| Carbon Black（碳黑） | `#1A1A1A` | 最深正文、富黑强调 |
| Slate Grey（石板灰） | `#3D4852` | **强文本**，标题文字 |
| Steel Grey（钢铁灰） | `#6B7785` | **正文**，段落文字 |
| Silver Grey（银灰） | `#A8B2BD` | **边框**，分隔线 |
| Mist White（雾白） | `#F5F7FA` | **背景**，次级区块底色 |
| White | `#FFFFFF` | 纯白卡片、主背景 |

### 辅助色：金色系（真正的金属感）

> 🔒 **铁律 #4（必须遵守）**：金色（尊贵金 `#D4AF37` / 香槟金 `#F2D492`）是金属色，**任何位置、任何尺寸、任何用途都必须用渐变**。纯色使用 = 廉价感 = 失去"高级感"。无论背景、底色、按钮、描边、文字——只要沾到金色，**100% 渐变**。尤其是大面积背景（卡片底色、Banner、Header、章节页），绝对禁止使用纯金色。下面的 hex 颜色值只用于**构造渐变的中间色**，而非"可直接当 background-color 用的纯色"。

| 名称 | HEX | 渐变描述 |
|------|-----|---------|
| Prestige Gold（尊贵金） | `#D4AF37` | 线性渐变 135°：`#E8C547` → `#D4AF37` → `#B8941F`，叠加白色高光 `rgba(255,255,255,0.3)`，1px 深色描边 `#9A7B1A` |
| Champagne Gold（香槟金） | `#F2D492` | 线性渐变 135°：`#FFF4D6` → `#F2D492` → `#D9BC6E`，叠加柔光 `rgba(255,248,220,0.2)`，无硬边框 |

**渐变构造公式（必须照搬，不可降级为纯色）**：

```css
/* 尊贵金渐变 —— 用于深色背景、按钮、强调条 */
background: linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%);

/* 香槟金渐变 —— 用于浅色背景、暖卡片、引用块 */
background: linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%);

/* 金色文字渐变（background-clip: text 技巧）—— 海洋蓝/深海蓝背景上专用 */
color: transparent;
background: linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%);
-webkit-background-clip: text;
background-clip: text;
-webkit-text-fill-color: transparent;
```

**金色使用场景**：
- Prestige Gold：高级 CTA 按钮、关键徽章、奖项标识、强调条、深色背景上的金色文字
- Champagne Gold：暖色高亮卡片（**渐变背景**）、引用块背景（**渐变背景**）、轻量级强调
- 🆕 **金色文字渐变**（新）：海洋蓝/深海蓝背景上的大标题、关键数字、Hero 主视觉字——使用 `background-clip: text` 让字本身呈现金属光泽

**🆕 新增组合：海洋蓝背景 + 尊贵金字（深海奢华风）**

这是 UPerform 的标志性奢华组合——深邃的海洋蓝铺底，金属质感的金色文字浮于其上，营造"深海藏金"的视觉张力。

| 用途 | 背景 | 文字 | 适用场景 |
|------|------|------|---------|
| 海洋蓝 + 尊贵金字 | 深海蓝渐变 `linear-gradient(135deg, #0A2540 0%, #1E4976 100%)`（**优先**,大面积铺底用） | 尊贵金渐变文字（`#E8C547` → `#F2D492` → `#D4AF37`） | 高端封面、Hero 标题、奖项大数字、VIP 标识、限量版标签 |
| 深海蓝 + 香槟金字 | 深海蓝 `#0A2540` 纯色 | 香槟金渐变文字（`#FFF4D6` → `#F2D492` → `#D9BC6E`） | 章节封面、引用金句、长标题 |

> ⚠️ 关键细节：**金色文字**必须用 `background-clip: text` 渐变技术，绝对不能直接写 `color: #D4AF37`——那会让字看起来像贴上去的廉价贴纸。渐变金属字 + 深蓝底 = 高级感的灵魂。

### 点缀色：橙色系（**极度克制,作为最后手段**）

> **新规则**：橙色已不再是默认的强调色。金色系已承担强调与点缀职责。橙色仅在最关键、最不可替代的 1 处使用,默认采用金色替代。

| 名称 | HEX | 用途 |
|------|-----|------|
| Vibrant Orange（活力橙） | `#FF6B35` | **主 Accent**（仅 1 处）,最关键 CTA 按钮;**默认替换为金色** |
| Coral Light（珊瑚光） | `#FF9B7D` | **次 Accent**（极度克制）,次级高亮、暖色标签;**默认替换为金色** |

### 4 层色彩体系速查 (PRIMARY / NEUTRALS / SECONDARY / ACCENT)

按国际设计标准(Material Design / IBM Carbon / Figma 等),严格说灰色不算"颜色",是"工具集"。这套配色采用 4 层结构,**各司其职**——主色管品牌识别、灰色管功能支撑、金色管高级感与强调点缀、橙色管行动信号(仅作最后手段,≤ 1 处)。

| 层级 | 色系 | 代表色 | 视觉量 | 职责 |
|------|------|--------|--------|------|
| **PRIMARY** | 蓝色系 (5色) | 海洋蓝 `#1E4976` | 60–70% | 品牌识别 — 标题、品牌元素、关键数据 |
| **NEUTRALS** | 灰色系 (5色) | 碳黑/石板/钢铁/银/雾白 | 功能性 | 文字层级、边框、背景、阴影 |
| **SECONDARY** | 金色系 (2色) | 尊贵金 `#D4AF37` | 装饰性 / 强调性 | 高级感 + 强调点缀 — VIP 标识、奖项、关键强调、行动替代(≤ 3 处) |
| **ACCENT** | 橙色系 (2色) | 活力橙 `#FF6B35` | 行动性(极度克制) | CTA 按钮(全场 ≤ 1 处,尽可能不采用) |

## 3. Typography Rules

### 字体家族

**中文：** 宋体 / 思源黑体（Noto Sans SC）/ 微软雅黑 / 苹方
**英文：** Source Sans Pro / Open Sans / Segoe UI

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">
```

### 标题层级

| 级别 | 字号 | 字重 | 颜色 | 用途 |
|------|------|------|------|------|
| Display H1 | 48–60px | 700 | `#0A2540` 或 `#FFFFFF` | 封面大标题 |
| Page H2 | 32–36px | 700 | `#1E4976` | 页面主标题 |
| Section H3 | 24–28px | 600 | `#2E6BA8` | 区块标题 |
| Sub H4 | 20–22px | 600 | `#3D4852` | 子标题 |
| Label H5 | 16–18px | 500 | `#6B7785` | 标签、小标题 |
| Caption | 13–14px | 400 | `#6B7785` | 注释、说明 |

### 正文层级

| 级别 | 字号 | 行高 | 颜色 |
|------|------|------|------|
| Body Large | 18–20px | 1.7 | `#1A1A1A` |
| Body Base | 15–16px | 1.6 | `#1A1A1A` |
| Body Small | 13–14px | 1.5 | `#3D4852` |
| Muted | 12–13px | 1.4 | `#A8B2BD` |

### 设计原则
- **通过字重建立清晰层级**：H1/H2 使用 700（粗体），H3/H4 使用 600（次粗体），正文使用 400（常规）
- **一致的间距系统**：4/8/12/16/24/32/48/64/80/96px 间距系统
- **专业中文支持**：思源黑体提供优秀的中文字符渲染
- **按钮圆角 6px**：柔和但不失专业

## 4. Component Stylings

### 按钮

**Primary 按钮**
- Background: `#1E4976`
- Text: `#FFFFFF`
- Border: 2px solid `#1E4976`
- Padding: 10px 24px
- Radius: 6px
- Hover: Background `#2E6BA8`, border `#2E6BA8`

**Accent / CTA 按钮（活力橙）**
- Background: `#FF6B35`
- Text: `#FFFFFF`
- Border: 2px solid `#FF6B35`
- Padding: 10px 24px
- Radius: 6px
- Hover: Background `#E55A2B`, border `#E55A2B`

**Premium 按钮（尊贵金渐变）**
- Background: `linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)`
- Text: `#FFFFFF`
- Border: 1px solid `#9A7B1A`
- Padding: 10px 24px
- Radius: 6px
- 叠加白色高光：`box-shadow: inset 0 1px 0 rgba(255,255,255,0.3)`
- Hover: 加深渐变 + 轻微上浮

**Secondary 按钮（描边）**
- Background: transparent
- Text: `#4A8FD8`
- Border: 2px solid `#4A8FD8`
- Padding: 10px 24px
- Radius: 6px
- Hover: Background `#4A8FD8`, text `#FFFFFF`

**Ghost 按钮（深色背景上）**
- Background: transparent
- Text: `#FFFFFF`
- Border: 2px solid `rgba(255,255,255,0.6)`
- Padding: 10px 24px
- Radius: 6px
- Hover: Background `rgba(255,255,255,0.15)`, border `#FFFFFF`

### 卡片

**标准卡片**
- Background: `#FFFFFF`
- Border: 1px solid `#A8B2BD`
- Radius: 8px
- Padding: 24px
- Shadow: `0 2px 8px rgba(10, 37, 64, 0.08)`

**深色卡片（深海蓝背景）**
- Background: `#0A2540`
- Color: `#FFFFFF`
- Radius: 8px
- Padding: 24px

**金色暖卡片（用于亮点、引用）**
- Background: `linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%)`（**渐变，绝不纯色**）
- Border-left: 4px solid `#D4AF37`（**渐变描边**：`linear-gradient(180deg, #E8C547 0%, #B8941F 100%)`）
- Radius: 0 8px 8px 0
- Padding: 16px 20px
- 叠加柔光：`box-shadow: inset 0 0 0 1px rgba(255,248,220,0.4)`

**🆕 海洋蓝 + 尊贵金字卡片（深海奢华，标志性组合）**
- Background: **深海蓝渐变 `linear-gradient(135deg, #0A2540 0%, #1E4976 100%)`**（**必须渐变,禁用纯色,深色底让金字发光**;若面积很小可酌情用海洋蓝 `#1E4976`,但大面积场景一律用渐变）
- Title 颜色：**金色文字渐变**（`background-clip: text`）：
  ```css
  background: linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  ```
- Body 颜色：`#E8F2FC`（冰川蓝）或 `#FFFFFF`（仅在标题金重时）
- Border-left: 4px（**金色渐变描边**）：`linear-gradient(180deg, #E8C547 0%, #B8941F 100%)`
- Radius: 0 8px 8px 0
- Padding: 16px 20px
- 阴影：`box-shadow: 0 4px 16px rgba(10, 37, 64, 0.3)`（深色卡片需要更深的阴影）
- 适用：高端引用、VIP 标识、奖项展示、关键数据高亮

**信息卡片（冰川蓝背景）**
- Background: `#E8F2FC`
- Border-left: 4px solid `#4A8FD8`
- Radius: 0 8px 8px 0
- Padding: 16px 20px

**暖色卡片（橙色，用于重点提示）**
- Background: `#FFF0E8`（活力橙 8% 透明叠白）
- Border-left: 4px solid `#FF6B35`
- Radius: 0 8px 8px 0
- Padding: 16px 20px

### Header / Banner

**深色 Header（深海蓝渐变）**
- Background: `linear-gradient(135deg, #0A2540 0%, #1E4976 60%, #2E6BA8 100%)`
- Color: `#FFFFFF`
- Padding: 48px 64px

**章节 Banner**
- Background: `#1E4976`
- Color: `#FFFFFF`
- Padding: 32px 48px
- Border-left: 6px solid `#FF6B35`

**金色 Banner（高级封面）**
- Background: `linear-gradient(135deg, #0A2540 0%, #1E4976 50%, #D4AF37 100%)`
- Color: `#FFFFFF`
- Padding: 64px
- 叠加金属光泽

### 标签 / Badge

```css
.up-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.up-badge-primary  { background: #1E4976; color: #FFFFFF; }
.up-badge-accent   { background: #FF6B35; color: #FFFFFF; }
.up-badge-sky      { background: #4A8FD8; color: #FFFFFF; }
.up-badge-coral    { background: #FF9B7D; color: #FFFFFF; }
.up-badge-gold     { background: linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%); color: #FFFFFF; border: 1px solid #9A7B1A; }

/* 🆕 海洋蓝 + 金字渐变 badge —— 标志性奢华组合 */
.up-badge-ocean-gold {
  background: #1E4976;                                                          /* 海洋蓝底 */
  border: 1px solid transparent;
  background-image: linear-gradient(#1E4976, #1E4976),                          /* 底层海洋蓝 */
                    linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%); /* 上层金色渐变 */
  background-origin: border-box;
  background-clip: padding-box, border-box;
  position: relative;
}
.up-badge-ocean-gold span {
  background: linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%);  /* 金字渐变 */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  letter-spacing: 1px;
}

/* 🆕 深海蓝 + 香槟金字渐变 badge —— 更深邃的版本 */
.up-badge-deep-gold {
  background: linear-gradient(135deg, #0A2540 0%, #1E4976 100%);                /* 深海蓝渐变底 */
  border: 1px solid rgba(212, 175, 55, 0.4);                                   /* 1px 半透明金描边 */
  box-shadow: inset 0 1px 0 rgba(255, 215, 100, 0.15);                         /* 顶部金色微高光 */
}
.up-badge-deep-gold span {
  background: linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%);  /* 香槟金字渐变 */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
  letter-spacing: 1px;
}
```

**Badge 使用指南（6 种组合）**：

| Badge | 底色 | 文字 | 适用场景 |
|-------|------|------|---------|
| `up-badge-primary` | 海洋蓝纯色 `#1E4976` | 白色 | 普通标签 |
| `up-badge-sky` | 地平蓝纯色 `#4A8FD8` | 白色 | 信息标签 |
| `up-badge-gold` | 尊贵金渐变 | 白色 | VIP / 奖项 |
| `up-badge-warm` | 香槟金渐变 | 深海蓝 | 暖色标签 |
| 🆕 `up-badge-ocean-gold` | 海洋蓝底 + 金色渐变描边 | 尊贵金字渐变 | 高端强调、限量版 |
| 🆕 `up-badge-deep-gold` | 深海蓝渐变底 + 半透明金描边 | 香槟金字渐变 | 顶级荣誉、品牌周年 |

### 分隔线

```css
.up-divider         { border: none; border-top: 1px solid #A8B2BD; margin: 24px 0; }
.up-divider-accent  { border: none; border-top: 3px solid #FF6B35; margin: 24px 0; }
.up-divider-primary { border: none; border-top: 3px solid #1E4976; margin: 24px 0; }
.up-divider-gold    { border: none; border-top: 3px solid; background: linear-gradient(90deg, transparent 0%, #D4AF37 50%, transparent 100%); height: 3px; margin: 24px 0; }
```

## 5. Layout Principles

### 间距系统

```
4px | 8px | 12px | 16px | 24px | 32px | 48px | 64px | 80px | 96px
```

### 典型配色方案 (6 种场景)

> **新规则**：橙色已极度克制(全场 ≤ 1 处),下方场景表中的"活力橙"**优先替换为金色**;若某场景必须保留橙色,整场只保留 1 处。
> **🆕 金色铁律**：下方所有标"金色"的位置,**100% 使用渐变**（背景、按钮、描边、文字均不例外）。纯金色出现 = 廉价感。

| 场景 | 主色 (PRIMARY) | 辅助 (SECONDARY) | 点缀 (ACCENT) | 文字/底色 |
|------|---------------|----------------|--------------|----------|
| **A. 商务场景** | 深海蓝 `#0A2540` | 尊贵金渐变 `#E8C547`→`#D4AF37`→`#B8941F` | 尊贵金(优先,渐变) / 活力橙(≤1处) | 白色字 + 🆕 尊贵金字渐变 + 金底白字按钮 |
| **B. 数字产品** | 雾白 `#F5F7FA` | 香槟金渐变 `#FFF4D6`→`#F2D492`→`#D9BC6E` | 海洋蓝 `#1E4976` | 金字渐变 + 海洋蓝底白字按钮 |
| **C. 营销物料** | 天空蓝 `#2E6BA8` | 尊贵金渐变 | 尊贵金渐变(强调) | 白色字 + 🆕 尊贵金字渐变 |
| **D. 年轻场景** | Sky Blue 天空蓝 | 香槟金渐变 | 香槟金渐变(强调)/活力橙(极克制) | 现代亲和 + 🆕 香槟金字渐变 |
| **E. 专业场景** | Ocean Blue 海洋蓝 | Silver 银灰 | Coral Glow 珊瑚光(轻量) / 海洋蓝(强调) | 严谨专业 |
| **F. 🆕 商务场景 2（海洋蓝+金字，标志性奢华）** | 海洋蓝 `#1E4976` 或 深海蓝渐变 `#0A2540`→`#1E4976` | 尊贵金渐变 | 尊贵金渐变(强调)/活力橙(≤1处) | 🆕 **金字渐变**（`background-clip: text`）+ 白色 + 金边 |

### 幻灯片 / 培训材料设计规则 (三明治结构)

> **新规则**：下方表格中的"活力橙"**优先替换为金色**。一整套幻灯片里橙色元素**全场 ≤ 1 处**(例如:结尾 CTA 按钮);其余强调全部交给金色。
> **🆕 金色铁律**：所有标"金色"的位置,100% 渐变;标题用了"尊贵金"或"香槟金"作为文字色,必须用 `background-clip: text` 渐变技术,绝不能 `color: #D4AF37` 或 `color: #F2D492` 写死。

| 幻灯片类型 | 背景 (PRIMARY) | 标题色 | 正文色 (NEUTRALS) | 可用点缀 (SECONDARY + ACCENT) |
|-----------|----------------|--------|-------------------|----------------------------|
| 封面页 | 深海蓝 `#0A2540` | 🆕 尊贵金字渐变 | 冰川蓝 `#E8F2FC` | 尊贵金渐变 (品牌标识) + 海洋蓝 (辅助文字) |
| 章节分隔页 | 深海蓝 `#0A2540` | 🆕 尊贵金字渐变 | 冰川蓝 `#E8F2FC` | 尊贵金渐变 (竖线装饰) + 尊贵金 (Logo) |
| 内容页 | 雾白 `#F5F7FA` 或 冰川蓝 `#E8F2FC` | 海洋蓝 `#1E4976` | 钢铁灰 `#6B7785` | 尊贵金渐变 (强调) + 天空蓝 (图表) |
| 🆕 引用/金句页（深蓝版） | 海洋蓝 `#1E4976` 或 深海蓝渐变 | 🆕 尊贵金字渐变 | 冰川蓝 `#E8F2FC` | 尊贵金渐变 (左边框装饰) |
| 引用/金句页（暖金版） | 香槟金渐变 `#FFF4D6`→`#F2D492`→`#D9BC6E` | 碳黑 `#1A1A1A` | 石板灰 `#3D4852` | 尊贵金渐变 (左边框装饰) |
| 数据/成果页 | 雾白 `#F5F7FA` | 碳黑 `#1A1A1A` | 石板灰 `#3D4852` | 🆕 尊贵金字渐变 (关键大数字 + 增长率) |
| 结尾/CTA 页 | 深海蓝 `#0A2540` | 🆕 尊贵金字渐变 | 冰川蓝 `#E8F2FC` | 活力橙 (按钮,仅此处可保留 1 处) / 尊贵金渐变按钮(优先) + 尊贵金渐变 (品牌收尾) |

## 6. Depth & Elevation

| 层级 | 处理方式 | 用途 |
|------|---------|------|
| Base | 无阴影，纯色背景 | 标准内容区块 |
| Card Elevation | `0 2px 8px rgba(10, 37, 64, 0.08)` | 浅色背景上的标准卡片 |
| Header Elevation | 渐变背景 `#0A2540` → `#1E4976` → `#2E6BA8` | 英雄头部、章节横幅 |
| Premium Header | 蓝金渐变 `#0A2540` → `#1E4976` → `#D4AF37` | 高级封面、奖项页 |
| 🆕 Ocean-Gold Card | 海洋蓝底 `#1E4976` + 🆕 金字渐变 + `0 4px 16px rgba(10,37,64,0.3)` | 高端引用、VIP 标识、关键数据高亮 |
| 🆕 Deep-Gold Badge | 深海蓝渐变底 `#0A2540`→`#1E4976` + 🆕 香槟金字渐变 + 1px 半透明金描边 | 顶级荣誉、品牌周年、限量版标签 |

**阴影理念**：UPerform 使用细腻、专业的阴影。主卡片阴影 (`0 2px 8px rgba(10, 37, 64, 0.08)`) 柔和且扩散，创造温和的抬升感而不戏剧化。深色背景上的金色文字卡片使用更深的阴影 (`0 4px 16px rgba(10, 37, 64, 0.3)`) 让卡片从深色背景中"浮起"。头部区域使用渐变背景而非阴影来创造深度感。金色元素叠加柔光层 (`rgba(255, 248, 220, 0.2)`) 营造金属光泽。**金色永远是渐变,不是阴影或纯色**——这是金属感的灵魂。

## 7. Do's and Don'ts

### Do

**4 层体系使用规范**
- **PRIMARY 主色** 使用 `#1E4976`（海洋蓝），占 60-70% 视觉量
- **NEUTRALS 中性色** 只做功能支撑（文字/边/底），不参与品牌识别
- **SECONDARY 辅助色** 使用尊贵金渐变做高级感点缀；**同样承担强调与点缀职责，是橙色的优先替代**
- **ACCENT 点缀色** 使用 `#FF6B35`（活力橙）做 CTA 按钮；**全场 ≤ 1 处，尽可能不采用**

**金色使用规范 DO'S**
- ✅ **金色必须用渐变**——`linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)`（尊贵金）或 `linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%)`（香槟金）
- ✅ 高端元素、VIP 标识
- ✅ 奖项证书、荣誉展示
- ✅ 重要 CTA 按钮强调（**优先使用，替代橙色**,渐变背景）
- ✅ 品牌周年庆典素材
- ✅ 限量版产品标识
- ✅ 关键数字、Logo 旁点缀、签名
- ✅ **强调与点缀** — 关键标签、活跃高亮、数据亮点（承担原橙色职责）
- ✅ 🆕 **海洋蓝背景 + 尊贵金字渐变**（标志性奢华组合，用于高端封面、Hero、奖项、VIP 标识）——金字用 `background-clip: text` 渐变技术

**排版与组件规范**
- 深色背景上的文字使用白色或 `#A8B2BD`
- 浅色信息块使用 `#E8F2FC`（冰川蓝）或 `#F5F7FA`（雾白）
- 按钮圆角使用 `6px`
- 间距使用官方间距系统（4/8/12/16/24/32/48/64/80/96px）
- 封面/Banner 使用深海蓝渐变 + **尊贵金渐变强调**（**优先**,活力橙仅在万不得已的 1 处使用）
- 高级场景使用蓝金渐变 + 香槟金渐变高光

### Don't

**金色使用规范 DON'TS（铁律 #4 严格执行）**
- ❌ **使用纯色金色**（`background: #D4AF37` / `background: #F2D492` / `color: #D4AF37`）——任何位置、任何尺寸、任何用途一律禁止
- ❌ 大面积背景色（即使是渐变,金色作为主背景超过 30% 视觉量也会显廉价）
- ❌ 正文字颜色（金色文字只用于标题、关键数字、Hero 字,不用于正文段落）
- ❌ 低对比度组合
- ❌ 过度使用（全场不超过 3 处金色元素）
- ❌ 与竞品金色混淆
- ❌ **把金色文字当纯色用**（如 `color: #D4AF37`）——必须 `background-clip: text` 渐变,否则字会"贴不住"深色背景

**4 层体系反模式**
- ❌ 不使用品牌色系以外的颜色（如大红色、紫色）
- ❌ 不在深色背景上使用纯黑 `#000000`
- ❌ 不在冰川蓝上使用金色（会糊）
- ❌ 不让蓝/橙/金参与正文（正文只走灰色）
- ❌ 不把灰色升格为 "secondary" 抢蓝色品牌位
- ❌ 不在普通内容页强行使用金色渐变
- ❌ 不在浅色背景上使用金色文字（对比度不足,看不见）

### 四条使用铁律 (CRITICAL RULES)

1. **橙色是"放大镜"，不是"油漆"**
   整场不超过 **1 处**橙色元素，且**尽可能不采用**。金色系**同样可以用于强调和点缀的作用**，作为橙色的优先替代——能用金色就用金色，橙色是最后手段，不到万不得已不使用。

2. **金色永远搭配深色**
   尊贵金 + 深海蓝 = 经典奢华；香槟金 + 雾白 = 轻柔优雅。
   **金色不要放在冰川蓝上（会糊）**。
   金色已承担原橙色的强调与点缀职责，使用上限 ≤ 3 处。

3. **文字层级用灰色系统，蓝/橙/金不参与正文**
   正文只走 `#1A1A1A` → `#3D4852` → `#6B7785` 的灰阶。
   蓝/金/橙都是装饰色，不是文字色——避免大段彩色文字，既疲劳又掉档次。

4. **🆕 金色一律使用渐变,禁止纯色**（新铁律）
   尊贵金 `#D4AF37` 与香槟金 `#F2D492` 是金属色,纯色使用 = 廉价感 = 油漆/荧光笔。
   **所有金色元素（背景、底色、按钮、描边、文字）100% 渐变**。
   - 渐变背景：`linear-gradient(135deg, ...)` 多色渐变
   - 渐变文字：`background-clip: text` + `-webkit-text-fill-color: transparent`
   - 渐变描边：`background-image` 双层 + `background-origin: border-box`
   - 大面积背景（卡片底色、Banner、Header、章节页）尤其禁止使用纯金色——这是高级感的灵魂。

## 8. Responsive Behavior

### 断点

| 名称 | 宽度 | 关键变化 |
|------|-------|---------|
| Mobile | <640px | 单列，减少间距 |
| Tablet | 640–1024px | 双列网格，标准间距 |
| Desktop | >1024px | 完整布局，最大间距 |

### 折叠策略
- 卡片网格：多列 → 移动端单列
- 头部：按比例减少 padding
- 字体：较小屏幕上缩小标题
- 间距：使用更小的间距档位

## 9. Agent Prompt Guide

### 4 层色彩体系速查

```
PRIMARY        NEUTRALS                    SECONDARY (渐变)          ACCENT
海洋蓝         碳黑/石板/钢铁/银/雾白     尊贵金渐变/香槟金渐变   活力橙/珊瑚光
```

- **PRIMARY**（品牌识别 60-70%）：深海蓝 `#0A2540` / 海洋蓝 `#1E4976` / 天空蓝 `#2E6BA8` / 地平蓝 `#4A8FD8` / 冰川蓝 `#E8F2FC`
- **NEUTRALS**（功能支撑）：碳黑 `#1A1A1A` / 石板灰 `#3D4852` / 钢铁灰 `#6B7785` / 银灰 `#A8B2BD` / 雾白 `#F5F7FA`
- **SECONDARY**（高级感 + 强调点缀，≤ 3 处）：**尊贵金渐变** `#E8C547`→`#D4AF37`→`#B8941F` / **香槟金渐变** `#FFF4D6`→`#F2D492`→`#D9BC6E` — **金色 100% 渐变,绝无纯色;同样可承担强调与点缀职责,是橙色的优先替代**
- **ACCENT**（行动信号，≤ 1 处,尽可能不采用）：活力橙 `#FF6B35` / 珊瑚光 `#FF9B7D` — **仅在无金色替代时使用**

### 快速颜色参考
- 品牌主色：`#1E4976`（海洋蓝）
- 文字正文：`#1A1A1A` → `#3D4852` → `#6B7785`（灰阶）
- 边框分割：`#A8B2BD`（银灰）
- 浅色背景：`#F5F7FA`（雾白）/ `#E8F2FC`（冰川蓝）
- 🆕 **高级强调 / 强调点缀**：**金色渐变**（不是 `#D4AF37`）— 背景用 `linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)`;金字用 `background-clip: text` 渐变技术
- 行动 CTA：`#FF6B35`（活力橙，全场 ≤ 1 处,尽可能不采用）

### 示例组件提示
- "创建英雄头部，渐变背景从 `#0A2540` 到 `#1E4976` 再到 `#2E6BA8`。标题 48px 思源黑体字重 700，🆕 **白色或尊贵金字渐变（`background-clip: text` 技术,不要用 `color: #D4AF37`）**。副标题 18px，颜色 `#A8B2BD`。下方添加 4px 强调条，使用**金色渐变 `linear-gradient(90deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)`**（**纯金渐变,绝不纯色**;如必须用活力橙则仅 1 处）。"
- "设计内容卡片：白色背景，1px `#A8B2BD` 边框，8px 圆角，24px padding。标题 28px `#1E4976`。正文 16px `#1A1A1A`，行高 1.6。"
- "**创建尊贵金 CTA 按钮（**优先替代活力橙**）:金属渐变 `linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)` 背景（**绝不用纯色 `background: #D4AF37`**），白色文字，6px 圆角，10px 24px padding。15px Source Sans Pro 字重 600。"
- "**创建活力橙 CTA 按钮(全场 ≤ 1 处)**:`#FF6B35` 背景，白色文字，6px 圆角，10px 24px padding。15px Source Sans Pro 字重 600。"
- "创建尊贵金 Premium 按钮：金属渐变 `linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)`（**绝不用纯色**），1px `#9A7B1A` 描边，白色文字，6px 圆角，叠加 inset 高光 `rgba(255,255,255,0.3)`。"
- "构建冰川蓝信息框：`#E8F2FC` 背景，4px 左侧边框 `#4A8FD8`，16px 20px padding，0 8px 8px 0 圆角。"
- "构建香槟金暖色框（**渐变,绝不用纯色**）:`linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%)` 背景，4px 左侧边框用渐变 `linear-gradient(180deg, #E8C547 0%, #B8941F 100%)`，叠加柔光 `inset 0 0 0 1px rgba(255,248,220,0.4)`。"
- "🆕 **构建海洋蓝+金字渐变卡片(标志性奢华组合)**:海洋蓝 `#1E4976` 纯色背景(或深海蓝渐变 `#0A2540`→`#1E4976`),4px 左侧边框用金色渐变 `linear-gradient(180deg, #E8C547 0%, #B8941F 100%)`,标题用**金字渐变**:`background: linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%); -webkit-background-clip: text; background-clip: text; color: transparent;`,正文用冰川蓝 `#E8F2FC`,阴影 `0 4px 16px rgba(10,37,64,0.3)`,0 8px 8px 0 圆角。"
- "🆕 **构建海洋蓝+金字渐变 badge**:海洋蓝 `#1E4976` 底 + 1px 金色渐变描边(双层 `background-image` + `background-origin: border-box` + `background-clip: padding-box, border-box`)+ 金字渐变(`background-clip: text`)。HTML 写法:`<span class='up-badge-ocean-gold'><span>VIP 会员</span></span>`,内层 `span` 负责金字渐变,外层 `span` 负责描边。"
- "🆕 **构建深海蓝+香槟金字渐变 badge(更深邃版本)**:深海蓝渐变底 `linear-gradient(135deg, #0A2540 0%, #1E4976 100%)` + 1px 半透明金描边 `1px solid rgba(212,175,55,0.4)` + 顶部金色微高光 `inset 0 1px 0 rgba(255,215,100,0.15)` + 香槟金字渐变 `linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%)`(`background-clip: text`)。"
- "设计章节横幅：`#1E4976` 背景，白色文字，32px 48px padding，**6px 左侧边框用金色渐变 `linear-gradient(180deg, #E8C547 0%, #B8941F 100%)`（**金色优先,渐变描边,替代原纯色活力橙**）**。"
- "设计高级封面：背景渐变 `linear-gradient(135deg, #0A2540 0%, #1E4976 50%, #D4AF37 100%)`，标题**用金字渐变**（`background-clip: text` 技术），装饰用香槟金渐变高光。**所有金色元素 100% 渐变,绝无纯色**。"

### 迭代指南 (4 层结构)

**PRIMARY 主色系（蓝色 60-70% 视觉量）**
1. 以海洋蓝 `#1E4976` 作为主色调 — 它奠定专业基调
2. 深海蓝 `#0A2540` 用于最深色块（深色 Header、页脚、封面）
3. 天空蓝 `#2E6BA8` 用于辅助蓝（二级标题、卡片顶条、hover 状态）
4. 地平蓝 `#4A8FD8` 用于点缀蓝（图标、链接、图表高亮）
5. 冰川蓝 `#E8F2FC` 用于浅蓝底（卡片底色、引用块、表格交替行）

**NEUTRALS 中性色系（灰色 5 档 — 工具集）**
6. 碳黑 `#1A1A1A` 用于极深文本（大标题）
7. 石板灰 `#3D4852` 用于强文本（小标题、关键句）
8. 钢铁灰 `#6B7785` 用于正文（不用纯黑，更柔和专业）
9. 银灰 `#A8B2BD` 用于边框/分割
10. 雾白 `#F5F7FA` 用于浅色背景（与冰川蓝二选一）

**SECONDARY 辅助色系（金色 — 高级感 + 强调点缀）**
11. 🆕 **高级场景使用金色渐变**（不是纯色）—— 尊贵金 `linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%)` + 香槟金 `linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%)`
12. **全场不超过 3 处金色元素**（VIP 标识、奖项、关键强调、强调与点缀）
13. **金色可承担强调与点缀职责，是橙色的优先替代**——关键标签、活跃高亮、数据亮点优先用金色
14. 🆕 **金字必须用渐变**：使用 `background-clip: text` 技术,`background: linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%)` + `-webkit-background-clip: text; color: transparent`,绝不写 `color: #D4AF37`
15. 🆕 **金描边必须用渐变**：使用双层 `background-image` + `background-origin: border-box` + `background-clip: padding-box, border-box`,绝不写 `border: 1px solid #D4AF37`

**ACCENT 点缀色系（橙色 — 行动信号,极度克制）**
16. 仅在无金色替代时,CTA 按钮才使用活力橙 `#FF6B35`
17. 珊瑚光 `#FF9B7D` 用于次级 CTA、暖色标签（同样极度克制）
18. **橙色全场不超过 1 处,尽可能不采用**（默认不用,使用金色替代）

**四条铁律**
- 🔴 橙色是"放大镜"不是"油漆",全场 ≤ 1 处(尽可能不采用)
- 🟡 金色永远搭配深色(深海蓝/雾白),不要放冰川蓝上;**金色已承担强调与点缀职责(≤ 3 处)**
- ⚪ 文字只走灰阶(`#1A1A1A` → `#3D4852` → `#6B7785`),蓝/橙/金不参与正文
- 🆕 🟨 **金色一律渐变,禁止纯色** —— 任何位置、任何尺寸、任何用途的金色 100% 渐变;大面积背景尤其禁止使用纯金色

**排版与组件**
- 保持所有角圆润但不过于柔软 — 按钮 6px，卡片 8px
- 使用 4/8/12/16/24/32/48/64/80/96px 系统保持一致的间距
- 🆕 金字渐变需保证对比度:深色背景用浅金(`#E8C547`→`#F2D492`→`#D4AF37`),浅色背景用深金(`#B8941F`→`#D4AF37`→`#9A7B1A`)

### CSS 变量参考 (4 层结构)

```css
:root {
  /* ========== PRIMARY (品牌主色) - 蓝色系 ========== */
  --up-deep-sea:     #0A2540;   /* Deep Sea 深海蓝 - 深色背景 */
  --up-ocean:        #1E4976;   /* Ocean 海洋蓝 - 品牌主色 (60-70%) */
  --up-sky:          #2E6BA8;   /* Sky 天空蓝 - 辅助蓝/二级标题/hover */
  --up-horizon:      #4A8FD8;   /* Horizon 地平蓝 - 点缀蓝/图标/链接 */
  --up-glacier:      #E8F2FC;   /* Glacier 冰川蓝 - 浅蓝底/卡片底色 */

  /* ========== NEUTRALS (中性色) - 灰色系 ========== */
  /* 工具集:文字层级/边框/背景/阴影,不参与品牌识别 */
  --up-carbon:       #1A1A1A;   /* Carbon 碳黑 - 极深文本/大标题 */
  --up-slate:        #3D4852;   /* Slate 石板灰 - 强文本/小标题 */
  --up-steel-text:   #6B7785;   /* Steel 钢铁灰 - 正文 */
  --up-silver:       #A8B2BD;   /* Silver 银灰 - 边框/分割 */
  --up-mist:         #F5F7FA;   /* Mist 雾白 - 浅色背景 */
  --up-white:        #FFFFFF;

  /* ========== SECONDARY (辅助色) - 金色系 (基础色) ========== */
  /* ⚠️ 这些 hex 颜色只用于"构造渐变的中间色",禁止直接当 background-color 纯色使用 */
  /* 高级感 + 强调点缀:全场 ≤ 3 处,搭配深色使用 */
  /* 金色已承担原橙色的强调与点缀职责,是橙色的优先替代 */
  --up-prestige:     #D4AF37;   /* Prestige 尊贵金 - 中间色 */
  --up-prestige-hi:  #E8C547;   /* 亮金高光 */
  --up-prestige-lo:  #B8941F;   /* 深金阴影 */
  --up-prestige-edge:#9A7B1A;   /* 金色描边 */
  --up-champagne:    #F2D492;   /* Champagne 香槟金 - 中间色 */
  --up-champagne-hi: #FFF4D6;   /* 香槟金高光 */
  --up-champagne-lo: #D9BC6E;   /* 香槟金阴影 */

  /* ========== SECONDARY (辅助色) - 金色系 (渐变变量) 🆕 ========== */
  /* 这些是设计系统中"金色"的真正形态 —— 100% 渐变,绝无纯色 */
  /* 推荐直接使用这些渐变变量,不要自己再拼 linear-gradient */
  --up-gold-gradient:        linear-gradient(135deg, #E8C547 0%, #D4AF37 50%, #B8941F 100%);
  --up-gold-gradient-soft:   linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%); /* 浅金柔光,适合金字 */
  --up-gold-gradient-border: linear-gradient(135deg, #E8C547 0%, #B8941F 100%);              /* 金色描边渐变 */
  --up-gold-gradient-hover:  linear-gradient(135deg, #D4AF37 0%, #B8941F 50%, #9A7B1A 100%); /* hover 加深 */

  --up-champagne-gradient:      linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%);
  --up-champagne-gradient-soft: linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%); /* 适合金字 */
  --up-champagne-gradient-text: linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%); /* 深海蓝背景上的香槟金字 */

  /* 🆕 金字渐变工具类 (background-clip: text) */
  --up-gold-text: linear-gradient(135deg, #E8C547 0%, #F2D492 50%, #D4AF37 100%);
  --up-champagne-text: linear-gradient(135deg, #FFF4D6 0%, #F2D492 50%, #D9BC6E 100%);

  /* 🆕 海洋蓝 + 金字组合(标志性奢华) */
  --up-ocean-gold-bg:    #1E4976;          /* 海洋蓝底 */
  --up-deep-gold-bg:     linear-gradient(135deg, #0A2540 0%, #1E4976 100%); /* 深海蓝渐变底 */
  --up-ocean-gold-border: linear-gradient(135deg, #E8C547 0%, #B8941F 100%); /* 金色描边 */

  /* ========== ACCENT (点缀色) - 橙色系 ========== */
  /* 行动信号:CTA 按钮,全场 ≤ 1 处,尽可能不采用 */
  /* 默认用金色替代;仅在无金色替代的最关键场景使用 */
  --up-vibrant:      #FF6B35;   /* Vibrant 活力橙 - CTA(克制) */
  --up-vibrant-dark: #E55A2B;   /* 活力橙 hover */
  --up-coral:        #FF9B7D;   /* Coral 珊瑚光 - 柔强调/次 CTA(克制) */
}

/* ========== 🆕 金字渐变文字工具类 (background-clip: text) ========== */
/* 用法: <h1 class="up-gold-text">顶级荣誉</h1> 需放在海洋蓝/深海蓝背景上 */
.up-gold-text {
  background: var(--up-gold-text);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
.up-champagne-text {
  background: var(--up-champagne-text);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

/* ========== 🆕 金色描边工具类 (双层 background-image) ========== */
/* 用法: <div class="up-gold-border">...</div> */
.up-gold-border {
  border: 1px solid transparent;
  background-image: linear-gradient(#1E4976, #1E4976), var(--up-ocean-gold-border);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

/* ========== 🆕 海洋蓝 + 金字卡片 (标志性奢华组合) ========== */
.up-card-ocean-gold {
  background: var(--up-ocean-gold-bg);
  border: 1px solid transparent;
  background-image: linear-gradient(#1E4976, #1E4976), var(--up-ocean-gold-border);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  border-left: 4px solid transparent;
  border-radius: 0 8px 8px 0;
  padding: 16px 20px;
  box-shadow: 0 4px 16px rgba(10, 37, 64, 0.3);
}
.up-card-ocean-gold .up-title {
  background: var(--up-gold-text);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
  font-weight: 700;
}
.up-card-ocean-gold .up-body {
  color: var(--up-glacier);
}
```

---

## 相关资源

- 完整视觉规范：查看 `../uperform-visual-design/SKILL.md`
- 配色方案来源：`./优普丰品牌设计配色方案.md`
