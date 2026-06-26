# Style: Minimal (极简高端风)

极简主义风格，大量留白，适合金句、单牌解读、高端品牌感。

```yaml
canvas:
  ratio: portrait-3-4 | square-1-1
  grid: single

colors:
  primary: ["#FFFFFF", "#F8F8F8"]  # 纯白/米白
  accent: ["#1A1A1A", "#4A4A4A"]   # 纯黑/深灰
  highlight: ["#C9A96E", "#B8860B"] # 金（可选点缀）
  text: ["#1A1A1A", "#2C2C2C"]

elements:
  background: solid-color | subtle-gradient | paper-texture
  decorations: []  # 无装饰
  frames: none | thin-line
  emphasis: whitespace | typography-scale

typography:
  title: elegant-sans | light-serif
  body: minimal-sans
  numbers: thin-display
```

## Visual Characteristics

- **留白**：60-80% 空白区域
- **字体**：细体、优雅、字间距宽松
- **对比**：黑白为主，偶尔金色点缀
- **构图**：中心/三分法，极度克制

## Best For

- 金句/名言
- 单张塔罗牌解读
- 高端品牌内容
- 极简生活方式
- 禅意/冥想主题

## Prompt Keywords

```
minimalist design, clean aesthetic, generous whitespace,
elegant typography, black and white palette, sophisticated,
high-end look, less is more, refined simplicity,
thin sans-serif fonts, centered composition, luxury feel
```

## Avoid

- 过多装饰元素
- 鲜艳颜色
- 复杂背景
- 拥挤的布局
- 粗体/卡通字体

## Example Compositions

### 金句卡片
- 背景：纯白或极浅灰
- 文字：居中，黑色细体
- 留白：上下各 40%
- 点缀：底部小金色图标

### 单牌解读
- 背景：浅米色纸张纹理
- 主体：塔罗牌居中
- 文字：牌名在上，关键词在下
- 框架：极细黑线边框

### 品牌宣言
- 背景：纯黑
- 文字：白色，大字号
- 布局：左对齐或居中
- 留白：至少 50%

## Typography Hierarchy

```
Title:    48-64pt, Light/Regular
Subtitle: 24-32pt, Light
Body:     14-18pt, Regular
Caption:  10-12pt, Light, 50% opacity
```

## Spacing Rules

- 行距：1.6-1.8 × 字号
- 字间距：+50-100 tracking
- 边距：≥10% 画布宽度
- 元素间距：≥2× 行距
