---
name: color-palette-advisor
description: "Generate complete, professional color palettes for UI/UX and brand design. Use when user needs a color scheme, palette, brand colors, or color system for mini-program, App, Web, or large-screen interfaces."
---

# Color Palette Advisor

Generates complete, cohesive color palettes for UI/UX design (mini-program, App, Web, large-screen) and brand design. Produces harmonious color systems with exact HEX values, usage guidelines, and accessibility-checked contrast ratios.

## When to Use

- User needs a color scheme / palette (配色方案 / 配色 / 色板)
- User needs brand colors (品牌色)
- User needs a color system for a UI project (色彩系统 / 色系设计)
- User mentions a specific hue or has a brand color and needs a full palette
- User asks for color suggestions for a certain industry or style

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
2. **选择基色** — Use the provided brand color, or derive an industry-appropriate base hue.
3. **构建色板** — Generate a full system:
   - **主色 (Primary)**: Base hue + 10-shade scale (050-900)
   - **辅助色 (Secondary)**: Complementary / analogous hue for secondary actions and links
   - **中性色 (Neutral)**: Grays — text, background, border, divider
   - **语义色 (Semantic)**: success / warning / error / info
   - **强调色 (Accent, optional)**: For highlights, promotions, badges
4. **对比度校验** — Check WCAG AA contrast for text on backgrounds. Adjust if needed.
5. **生成使用指南** — For each color group: usage scenarios, percentage guidance, pairing rules.
6. **输出** — Present full palette with HEX values and usage notes. If user wants a file, save a `.md` palette doc.

## Color Generation Rules

### Primary scale (any hue)

Given a base color at 500, generate 050–900 shades:

- **050**: Base + white (~92% light) — lightest tint for backgrounds
- **100**: ~85% light — light tint for selection bg / badges
- **200**: ~75% light
- **300**: ~60% light
- **400**: ~45% light
- **500**: 🔑 BASE COLOR
- **600**: ~10% darker — hover / pressed states
- **700**: ~20% darker — pressed / important emphasis
- **800**: ~30% darker — hero text on light bg
- **900**: ~40% darker — deep brand accent

Tints = mix with white; shades = mix with black. Keep hue steady, vary lightness.

### Semantic colors (standard, adjust for dark mode)

| Type | Light mode | Dark mode |
|------|-----------|-----------|
| Success | #22C55E | #4ADE80 |
| Warning | #F59E0B | #FBBF24 |
| Error | #EF4444 | #F87171 |
| Info | #3B82F6 | #60A5FA |

### Neutral grays (hue-tinted)

Derive neutrals with a subtle tint of the primary hue for cohesion:

| Level | Purpose |
|-------|---------|
| 900 | Main text |
| 700 | Secondary text |
| 500 | Placeholder / disabled text |
| 300 | Border / divider |
| 200 | Subtle border |
| 100 | Hover / subtle bg |
| 50 | Page background |
| 0 | Card / surface (white or near-white) |

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