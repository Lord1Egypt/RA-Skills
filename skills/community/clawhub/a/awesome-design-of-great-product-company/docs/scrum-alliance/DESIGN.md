# Design System Inspiration of Scrum Alliance

## 1. Visual Theme & Atmosphere

Scrum Alliance 是全球领先的 Scrum 认证机构，品牌视觉以 **深蓝 + 中蓝为主色、浅蓝和橙色为强调色**的专业双色调体系，传达专业、权威与活力的品牌调性。

设计理念是"专业权威、清晰明亮"——深蓝色（#182340）建立权威感，中蓝色（#375EDF）传递稳重与信任，浅蓝色和橙色作为点缀增添活力。

**关键特征：**
- 品牌主色为深蓝 (`#182340`) — 主色调、主导色
- 中蓝作为第二主色 (`#375EDF`) — 次级强调
- 浅蓝作为辅助强调 (`#A4D5EB`) — 点缀、背景
- 橙色作为活力点缀 (`#FA9449`) — CTA、强调（不宜主导）
- 背景使用浅灰白色 (`#F3F3F3`) — 简洁、专业
- 按钮圆角 4px — 简洁利落
- 专业字体：Clear Sans（官方指定）+ Source Sans Pro（降级方案）

## 2. Color Palette & Roles

### 品牌主色

**Primary Colors（4色）**

| 名称 | HEX | 用途 |
|------|-----|------|
| Deep Blue | `#182340` | **主导色**，深色背景、标题、主按钮 |
| Medium Blue | `#375EDF` | **第二主色**，次级按钮、链接、强调 |
| Light Blue | `#A4D5EB` | 浅色辅助、高亮背景、图标 |
| Orange | `#FA9449` | CTA 按钮、活力强调、badge |

> **使用指南**：黑色和蓝色为主导颜色。浅蓝色和橙色更多作为点缀使用，不应成为主导。

### 品牌辅助色

**Secondary Colors（5色）**

| 名称 | HEX | 用途 |
|------|-----|------|
| Silver Grey | `#D1D3D9` | 边框、分割线 |
| Pale Blue 1 | `#D7DFF9` | 浅色背景、卡片底色 |
| Pale Blue 2 | `#DBEEF7` | 浅色提示背景 |
| Pale Orange | `#FEE4D2` | 暖色提示背景 |
| Off-White | `#F3F3F3` | 页面背景底色 |

### 中性色

| 名称 | HEX | 用途 |
|------|-----|------|
| Near Black | `#182340` | 主标题、深色文字 |
| Dark Grey | `#535353` | 正文辅助文字 |
| Mid Grey | `#A7A7A7` | 辅助说明文字 |
| Light Grey | `#D1D3D9` | 边框、分割线 |
| White | `#FFFFFF` | 卡片背景、纯白区域 |

### 品牌三色速查

| 角色 | HEX | 使用场景 |
|------|-----|----------|
| **Primary** | `#182340` | 主导色、深色背景 |
| **Secondary** | `#375EDF` | 中蓝色、链接、次级强调 |
| **Accent** | `#FA9449` | CTA、活力点缀 |
| **Light Accent** | `#A4D5EB` | 浅蓝色辅助 |

## 3. Typography Rules

### 字体家族

**主字体：** Clear Sans（官方指定）

| 字重 | 用途 |
|------|------|
| Clear Sans Regular | 正文 |
| Clear Sans Thin | 辅助文字 |
| Clear Sans Medium | 强调正文 |
| Clear Sans Bold | 标题、强调 |

**降级方案：** `'Segoe UI', 'Helvetica Neue', Arial, sans-serif`

```html
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">
```

### 标题层级

| 级别 | 字号 | 字重 | 用途 |
|------|------|------|------|
| H1 Display | 60px | 700 | 封面大标题 |
| H2 Page | 36px | 700 | 页面主标题 |
| H3 Large | 28px | 700 | 区块标题 |
| H4 Medium | 22px | 400 | 子标题 |
| H5 Small | 18px | 400 | 标签、小标题 |
| H6 All Caps Large | 18px | 400 | 大写标签，字间距 1.6px |
| H7 All Caps Small | 15px | 400 | 小写标签，字间距 2.0px |

### 正文层级

| 级别 | 字号 | 字重 | 用途 |
|------|------|------|------|
| Body Large | 20px | 400 | 强调正文 |
| Body Medium | 17px | 400 | 标准正文 |
| Body Small | 15px | 400 | 辅助正文 |
| Body XSmall | 13px | 400 | 注释、说明 |

### 设计原则
- **通过字重和字间距建立层级**：Display/Page 使用 Bold，Large 以上使用 Bold
- **一致的间距系统**：6/8/16/24/36/60/80px 间距系统
- **正文颜色 #535353**：确保与浅色背景的高对比度
- **标题颜色 #182340**：深蓝色标题传达权威感

## 4. Component Stylings

### 按钮

**Primary 按钮（深蓝背景）**
- Background: `#182340`
- Text: `#FFFFFF`
- Border: 1px solid `#182340`
- Padding: 0.375rem 0.75rem
- Radius: 0.25rem (4px)
- Hover: Background `#2a3a5f`

**Primary 按钮（浅色背景）**
- Background: `#375EDF`
- Text: `#FFFFFF`
- Border: 1px solid `#375EDF`
- Padding: 0.375rem 0.75rem
- Radius: 0.25rem (4px)
- Hover: Background `#4a6fe8`

**Accent / CTA 按钮（橙色）**
- Background: `#FA9449`
- Text: `#FFFFFF`
- Border: 1px solid `#FA9449`
- Padding: 0.375rem 0.75rem
- Radius: 0.25rem (4px)
- Hover: Background `#e88530`

**Secondary 按钮**
- Background: `#FFFFFF`
- Text: `#182340`
- Border: 1px solid `#182340`
- Padding: 0.375rem 0.75rem
- Radius: 0.25rem (4px)
- Hover: Background `#182340`, text `#FFFFFF`

### 链接

**主链接**
- Color: `#375EDF`
- Font-weight: 600
- Text-decoration: none
- Hover: `#182340`

**次链接**
- Color: `#182340`
- Font-weight: 600
- Text-decoration: none
- Hover: `#375EDF`

### 卡片

**标准卡片**
- Background: `#FFFFFF`
- Border: 1px solid `#D1D3D9`
- Radius: 4px
- Padding: 24px

**浅色卡片**
- Background: `#F3F3F3`
- Border: 1px solid `#D1D3D9`
- Radius: 4px
- Padding: 24px

**蓝色卡片**
- Background: `#DBEEF7`
- Border: 1px solid `#A4D5EB`
- Radius: 4px
- Padding: 24px

**卡片标题**
- Color: `#182340`
- Font-size: 22px
- Font-weight: 700
- Margin-bottom: 16px

### 标签 / Badge

```css
.sa-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.sa-badge-primary  { background: #182340; color: #FFFFFF; }
.sa-badge-blue     { background: #375EDF; color: #FFFFFF; }
.sa-badge-light   { background: #A4D5EB; color: #182340; }
.sa-badge-orange  { background: #FA9449; color: #FFFFFF; }
```

### 分隔线

```css
.sa-divider         { border: none; border-top: 1px solid #D1D3D9; margin: 24px 0; }
.sa-divider-accent  { border: none; border-top: 3px solid #375EDF; margin: 24px 0; }
```

## 5. Layout Principles

### 间距系统

```
6px | 8px | 16px | 24px | 36px | 60px | 80px
```

### 典型配色方案

**方案 A：深蓝专业（推荐用于商务报告、课程封面）**
- 背景：`#182340`
- 主文字：`#FFFFFF`
- 强调：`#FA9449`（橙色）
- 次级文字：`#A4D5EB`

**方案 B：白底专业（推荐用于内容页、讲义）**
- 背景：`#FFFFFF`
- 主标题：`#182340`
- 正文：`#535353`
- 强调色块：`#375EDF` 或 `#FA9449`
- 边框/分割：`#D1D3D9`

**方案 C：蓝色系（推荐用于数据可视化、图表）**
- 主色：`#182340`
- 辅助色1：`#375EDF`
- 辅助色2：`#A4D5EB`
- 辅助色3：`#FA9449`
- 中性背景：`#F3F3F3`

### 幻灯片 / 培训材料设计规则

| 幻灯片类型 | 背景 | 标题 | 正文 | 强调 |
|-----------|------|------|------|------|
| 封面页 | `#182340` 深蓝 | `#FFFFFF` | `#A4D5EB` | `#FA9449` |
| 章节分隔页 | `#375EDF` 中蓝 | `#FFFFFF` | 无 | `#FFFFFF` 竖线装饰 |
| 内容页 | `#FFFFFF` | `#182340` | `#535353` | `#375EDF` 下划线 |
| 引用/金句页 | `#F3F3F3` | `#182340` | `#535353` | `#375EDF` 左边框 |
| 数据/图表页 | `#FFFFFF` | `#182340` | `#535353` | 蓝橙双色系 |
| 结尾/CTA 页 | `#182340` | `#FFFFFF` | `#A4D5EB` | `#FA9449` 按钮 |

## 6. Depth & Elevation

| 层级 | 处理方式 | 用途 |
|------|---------|------|
| Base | 无阴影，纯色背景 | 标准内容区块 |
| Card Elevation | 1px solid `#D1D3D9` 边框 | 浅色背景上的标准卡片 |
| Header Elevation | 纯色 `#182340` 背景 | 英雄头部、章节横幅 |

**阴影理念**：Scrum Alliance 使用简洁的卡片边框而非阴影来区分层级。深色头部使用纯色背景创造深度感。

## 7. Do's and Don'ts

### Do
- 主色使用 `#182340`（深蓝），而非其他蓝色
- 第二主色使用 `#375EDF`（中蓝）
- 浅蓝色和橙色更多作为点缀使用
- 标题颜色使用 `#182340`（深蓝）
- 正文颜色使用 `#535353`（Dark Grey）
- 背景使用 `#F3F3F3`（Off-White）而非纯灰
- 按钮圆角使用 `0.25rem`（4px）
- 间距使用官方间距系统（6/8/16/24/36/60/80px）
- 封面/Banner 使用深蓝背景 + 橙色强调

### Don't
- 浅蓝色和橙色不应成为主导颜色
- 不使用品牌色系以外的颜色（如大红色、紫色）
- 不在深色背景上使用纯黑 `#000000`
- 不使用超过 3 种主色调
- 不得更改 Logo 颜色或添加视觉效果
- 不得将 Logo 放置在与品牌色冲突的背景上

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

### 快速颜色参考
- 主色：`#182340`（Deep Blue）
- 第二主色：`#375EDF`（Medium Blue）
- 浅色辅助：`#A4D5EB`（Light Blue）
- 活力强调：`#FA9449`（Orange）
- 正文色：`#535353`（Dark Grey）
- 背景色：`#F3F3F3`（Off-White）

### 示例组件提示
- "创建英雄头部，深色背景 #182340，标题 60px Clear Sans Bold 白色，副标题 20px 颜色 #A4D5EB。下方添加橙色强调条，使用 #FA9449。"
- "设计内容卡片：白色背景，1px #D1D3D9 边框，4px 圆角，24px padding。标题 22px #182340。正文 17px #535353，行高 1.6。"
- "创建 Primary CTA 按钮：#FA9449 背景，白色文字，4px 圆角，0.375rem 0.75rem padding。"
- "设计浅色 Badge：#A4D5EB 背景，#182340 文字，20px 圆角，4px 12px padding。"
- "构建引用块：#F3F3F3 背景，4px 左侧边框 #375EDF，16px 20px padding，0 4px 4px 0 圆角。"

### 迭代指南
1. 以深蓝 `#182340` 作为主色调 — 它奠定权威基调
2. 为次级元素使用中蓝 `#375EDF` — 支持视觉层级
3. 橙色 `#FA9449` 用于 CTA 和活力强调 — 点缀而非主导
4. 浅蓝 `#A4D5EB` 用于辅助高亮 — 轻盈点缀
5. 保持按钮四角利落 — 4px 圆角
6. 使用 6/8/16/24/36/60/80px 系统保持一致的间距

### CSS 变量参考

```css
:root {
  /* 主色 - 深蓝系 */
  --sa-deep-blue: #182340;
  --sa-medium-blue: #375EDF;
  --sa-light-blue: #A4D5EB;
  --sa-orange: #FA9449;

  /* 辅助色 - 浅色系 */
  --sa-silver-grey: #D1D3D9;
  --sa-pale-blue-1: #D7DFF9;
  --sa-pale-blue-2: #DBEEF7;
  --sa-pale-orange: #FEE4D2;
  --sa-off-white: #F3F3F3;

  /* 中性色 */
  --sa-dark-grey: #535353;
  --sa-mid-grey: #A7A7A7;
  --sa-white: #FFFFFF;
}
```

---

## 相关资源

- 官方品牌指南：[Scrum Alliance ZeroHeight Design System](https://zeroheight.com/70fa032c4/p/36a279-colors)
- GitHub Style Guide：[scrumalliance/Style-Guide](https://github.com/scrumalliance/Style-Guide)
