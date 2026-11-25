---
name: color-palette-advisor
description: "Generate complete, professional color palettes for UI/UX and brand design. Use when user needs a color scheme, palette, brand colors, or color system for mini-program, App, Web, or large-screen interfaces. Do NOT use for image generation, data visualization color scales, or printing/CMYK color management."
version: 1.1.0
category: design
tags: [color-palette, ui-ux, design-system, accessibility, wcag, oklch, brand-colors]
allowed_tools: [exec, read, write]
allowed-tools: [exec, read, write]
metadata:
  openclaw:
    requires:
      bins: [python3]
    os: ["darwin", "linux", "win32"]
---

# Color Palette Advisor

Generates complete, cohesive color palettes for UI/UX design (mini-program, App, Web, large-screen) and brand design. Produces harmonious color systems with exact HEX values, usage guidelines, and accessibility-checked contrast ratios.

## When to Use

- User needs a color scheme / palette (配色方案 / 配色 / 色板)
- User needs brand colors (品牌色)
- User needs a color system for a UI project (色彩系统 / 色系设计)
- User mentions a specific hue or has a brand color and needs a full palette
- User asks for color suggestions for a certain industry or style

## 何时不使用 (Do NOT use)

- 需要生成/编辑图片（位图、插画、照片调色）— 本 skill 只输出色值与 token，不画图
- 数据可视化色标（charts heatmap/sequential scale 专用配色）— 用专业图表库方案
- 印刷 CMYK 色彩管理与专色 — 本 skill 基于 sRGB/OKLCH，不处理色域转换到印刷色
- 仅询问单个颜色换算（HEX/RGB/HSL 互转）— 直接回答即可，无需完整流程

## 使用描述

**一句话：** 输入品牌色（或行业），自动生成一套完整的、带无障碍校验的 UI 配色系统，支持小程序 / App / Web / 大屏，直接给开发用。

**适用场景：**
- 新项目启动，需要从零搭建配色体系
- 已有品牌色，需要扩展出完整色阶（050-900）
- 需要同时支持浅色模式和深色模式
- 需要确保配色符合 WCAG 无障碍标准（文字可读性）
- 需要给开发直接可用的 CSS 变量 / Figma Tokens

**核心特点：**
- **OKLCH 感知均匀色阶** — 比 HSL 混合更自然，深浅过渡均匀
- **语义色双版本** — 每个语义色给 base（图标/按钮）+ text（小字安全）两版，避免文字对比度不达标
- **对比度脚本实测** — 所有组合对比度由脚本计算，不靠目测
- **输出三件套** — 聊天色板表格 + HTML 可视化预览 + CSS/Figma token 文件
- **行业参考** — 内置电商/教育/金融/医疗/科技/政务/旅游/餐饮/美妆等行业的推荐色相

**输入：** 品牌色 HEX（或行业/风格描述）
**输出：** 完整色板（HEX + 对比度实测值）+ HTML 预览 + 开发 token 文件

---

## Inputs Needed

Gather (or ask if missing):

1. **品牌色 / 主色调** — A hex value, a color name, or a hue direction (optional, can derive from industry)
2. **行业 / 领域** — e.g. 电商、教育、金融、医疗、科技、政务、旅游、美妆、餐饮 (helps pick appropriate hue)
3. **目标平台** — 小程序 / App / Web / 大屏 / 品牌 (affects contrast and usage guidance)
4. **风格方向** (optional) — 简约、时尚、沉稳、科技感、活泼、高端、国风、清新
5. **深色模式** (optional) — Whether dark mode support is needed

If user gives minimal info, pick a reasonable hue from the industry and state the assumption.

## Workflow

1. **确认输入** — If industry and platform are missing, ask. Otherwise proceed.
2. **选择基色** — Use the provided brand color, or derive an industry-appropriate base hue (见 references/industry-palettes.md)。
3. **构建色板** — Generate a full system:
   - **主色 (Primary)**: Base hue + 10-shade scale (050-900), OKLCH 算法
   - **辅助色 (Secondary)**: 按色相偏移规则（见下）
   - **中性色 (Neutral)**: 带主色微弱色相的灰阶
   - **语义色 (Semantic)**: base + text 双版本
   - **强调色 (Accent, optional)**: For highlights, promotions, badges
4. **对比度校验** — **必须用 `scripts/palette.py` 脚本实际计算**，不要目测估。校验清单：
   - 白字 on primary-500 / 600 / 700（≥4.5:1）
   - primary-500 做白底大字/图标（≥3:1）
   - neutral 文字各层级 on 白底 / 页面底色
   - 语义色 text 版 on 白底（≥4.5:1）
   - 深色模式：primary-300/400 on 深底（≥4.5:1）
5. **生成使用指南** — For each color group: usage scenarios, percentage guidance, pairing rules.
6. **输出三件套** —
   - ① 聊天里输出**完整色板表格**（含实测对比度数值，不写“约”写实际值）
   - ② **HTML 可视化预览**（必做）— `python3 scripts/palette.py --html` 生成，然后按 custom-app-file-sender 规则用 `MEDIA:` 发送
   - ③ **开发 token 导出** — `--export css` / `--export figma`，生成 CSS 变量或 Figma Tokens JSON 文件给开发直接用

### 辅助色色相偏移规则（明确化）

不要含糊说“互补色/类似色”，给出具体偏移角度：

| 场景 | 方法 | 色相偏移 (OKLCH H) |
|------|------|-------------------|
| 默认 / 后台 / 工具类产品 | 类似色 analogous | H + 40° ~ 60° |
| 需要强对比 / 促销 / 年轻化 | 分裂互补 split-complementary | H + 150° ~ 210° |
| 强调色 accent | 暖色对冲，与主辅都拉开 | 通常 H + 165° 附近 |

饱和度：辅助色 C = 主色 C × 0.90~1.00；强调色 C = 主色 C × 1.10~1.15。

## 执行脚本

`scripts/palette.py` 是本 skill 的**计算引擎**，所有色阶/对比度/导出都由它算，避免目测出错。仅依赖 Python 标准库，无第三方包；语法兼容 **Python 3.6+**（f-string 内不使用嵌套同引号等 3.12-only 写法）。

```bash
# 生成完整色板 + 对比度报告 (JSON)
python3 scripts/palette.py --base "#0F62FE" --name "智慧园区"

# 生成 HTML 可视化预览 (默认输出到 /tmp/openclaw/palette-preview.html)
python3 scripts/palette.py --base "#0F62FE" --name "智慧园区" --html

# 导出 CSS 变量
python3 scripts/palette.py --base "#0F62FE" --export css --out ./tokens.css

# 导出 Figma Tokens JSON
python3 scripts/palette.py --base "#0F62FE" --export figma --out ./tokens.json
```

可用参数：`--base` 基准色 · `--name` 项目名 · `--secondary-mode analogous|split` · `--dark` 输出深色模式 · `--html` · `--export css|figma|md` · `--out`


## Color Generation Rules

### Primary scale (any hue) — OKLCH 感知均匀算法

Given a base color at 500, generate 050–900 shades using **OKLCH 色彩空间**（感知均匀，比 HSL 线性混合效果自然）：

**目标明度 (OKLCH L):**
- **050**: L = 0.972 (~92% 感知亮度) — 最浅背景
- **100**: L = 0.936 — 选中背景/徽标
- **200**: L = 0.876 — 图标填充
- **300**: L = 0.786 — 链接、描边强调
- **400**: L = 0.686 — 次级按钮
- **500**: L = base L — 🔑 基准色
- **600**: L = base - 0.085 — hover/按压
- **700**: L = base - 0.155 — 重要强调
- **800**: L = base - 0.215 — 深色品牌文字
- **900**: L = base - 0.275 — 品牌深色

**饱和度缩放 (OKLCH C):**
- 050: C × 0.28 (极淡)
- 100: C × 0.42
- 200: C × 0.62
- 300: C × 0.82
- 400-600: C × 1.0 (保持基准)
- 700: C × 0.92
- 800: C × 0.88
- 900: C × 0.80

**色相 H:** 全程保持 base H（不偏移，保证统一感）

**gamut mapping:** 超出 sRGB 范围时，自动降低 C 直到回到色域内（二分法，24 次迭代足够）

**不要使用** HSL 线性混合（mix with white/black），会产生感知不均匀的色阶。

### Semantic colors — 双版本策略（必须）

每个语义色输出 **两个版本**：
- **base**: 用于图标、大按钮、标签底色（对比度 ≥3:1）
- **text**: 加深版，用于小字文字（对比度 ≥4.5:1）

**Light mode:**
| Type | base (图标/按钮) | text (小字安全) | base 对比度 | text 对比度 |
|------|----------------|----------------|-------------|-------------|
| Success | #16A34A | #00893A | 3.3:1 ❌ | 4.5:1 ✅ |
| Warning | #E08C00 | #AE6500 | 2.7:1 ❌ | 4.5:1 ✅ |
| Error | #DC2626 | #D53530 | 4.8:1 ✅ | 4.8:1 ✅ |
| Info | #0284C7 | #147DB9 | 4.1:1 ❌ | 4.5:1 ✅ |

**Dark mode (深底 #0B1118):**
| Type | base (图标/按钮) | text (小字安全) |
|------|----------------|----------------|
| Success | #4ADE80 | #22C55E |
| Warning | #FBBF24 | #F59E0B |
| Error | #F87171 | #EF4444 |
| Info | #60A5FA | #3B82F6 |

**计算 text 版本:** 保持色相 H 不变，降低 L 直到对比度 ≥4.5:1（OKLCH 二分法，最多 100 步，每步 ΔL = 0.004）

### Neutral grays (hue-tinted, OKLCH 算法)

中性色带主色的**微弱色相**，保持整体统一感。

**OKLCH 算法:**
- H = 主色 H（保持）
- C = 0.008 ~ 0.015（极低饱和度，肉眼几乎无色相但整体和谐）
- L 按层级设定（下表）

| 令牌 | L (OKLCH) | C (OKLCH) | 用途 |
|------|-----------|-----------|------|
| neutral-000 | 1.0 | 0 | 纯白（卡片/表面） |
| neutral-050 | 0.975 | 0.008 | 页面背景 |
| neutral-100 | 0.945 | 0.010 | hover/浅底 |
| neutral-200 | 0.905 | 0.012 | 细分隔线 |
| neutral-300 | 0.825 | 0.015 | 边框 |
| neutral-400 | 0.695 | 0.020 | 弱化图标 |
| neutral-500 | 0.545 | 0.025 | 占位/禁用文字 |
| neutral-600 | 0.445 | 0.030 | 弱化正文 |
| neutral-700 | 0.355 | 0.035 | 次级文字 |
| neutral-800 | 0.235 | 0.040 | 弱化标题 |
| neutral-900 | 0.165 | 0.045 | 主文字 |

## Accessibility Rules

- **Text on light bg**: text color must have ≥4.5:1 contrast (body), ≥3:1 (large text ≥18pt/24px)
- **Primary button**: white text on primary-500 must be ≥4.5:1 (if not, use 600/700)
- **State combos**: disabled must still read as text (≥3:1 on bg)
- **Dark mode**: text #E5E7EB or similar on dark bg (#111827)

If primary-500 fails contrast with white text, recommend using primary-600/700 for buttons instead.

## Palette Presentation Format

```
🎨 配色方案 — {项目/行业} · {风格}

## 主色 Primary
| 令牌 | 色值 | 明度 | 用途 |
050 | # | ~92% | 浅背景 |
100 | # | ~85% | 选中背景 |
... 
500 | # | base | 主操作/品牌 |
600 | # | darker | 按压/hover |
900 | # | darkest | 品牌强调 |

## 辅助色 Secondary
...

## 中性色 Neutral
...

## 语义色 Semantic
...

## 强调色 Accent (optional)
...

## 使用指南
- 主色占比 ~60-70%
- 辅助色 ~20%
- 中性色 ~5-10% (functional)
- 强调色 ≤5% (亮点)
- 深色模式调暗主色使用 400/300
```

## Platform-Specific Notes

| Platform | Color usage guidance |
|----------|---------------------|
| 小程序 | 主色用在按钮/选中态，注意与微信原生 UI 协调 |
| App | iOS 建议系统语义色（绿/橙/红/蓝），可覆写 |
| Web | 需 hover / focus / active 状态色 |
| 大屏 | 深色背景为主，主色做亮色强调，注意远距离对比度 |
| 品牌 | 强调独特性，考虑印刷 CMYK 转换 |

## References

- `references/industry-palettes.md` — Industry-appropriate base hues
- `references/color-harmony.md` — Color harmony rules (complementary, analogous, triadic)
- `references/accessibility-quick-check.md` — Quick contrast check values