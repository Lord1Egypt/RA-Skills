# 设计系统：Intercom

## 1. 视觉主题与氛围

Intercom 的网站是一个温暖、自信的客户服务平台，通过简洁的编辑式设计语言传达"AI-first helpdesk"的理念。页面以温暖的米白色画布（`#faf9f6`）为基底，配合深黑色（`#111111`）文字，营造出亲密的杂志式阅读体验。标志性的 Fin Orange（`#ff5600`）——以 Intercom 的 AI agent 命名——作为温暖中性色调中唯一的鲜艳点缀色。

排版使用 Saans——一款定制的几何无衬线字体，采用激进的负字间距（80px 时为 -2.4px，24px 时为 -0.48px），并在所有标题尺寸上保持一致的 1.00 行高。这创造了超压缩的、广告牌式的标题，给人以工程化和精确的感觉。Serrif 作为编辑时刻的衬线字体伴侣，SaansMono 处理代码和大写技术标签。MediumLL 和 LLMedium 用于特定的 UI 场景，形成了丰富的五字体生态系统。

Intercom 的显著特点是其极其锐利的几何感——按钮使用 4px 圆角，创造出近乎矩形的交互元素，给人以工业化和精确的感觉，与温暖的表面颜色形成对比。按钮悬停状态使用 `scale(1.1)` 放大效果，创造出物理上的"生长"交互。边框系统使用温暖的燕麦色调（`#dedbd6`）和基于 oklab 的透明度值，实现精细的颜色管理。

**核心特征：**
- 温暖的米白色画布（`#faf9f6`）配合燕麦色调边框（`#dedbd6`）
- Saans 字体，极端负字间距（80px 时为 -2.4px）和 1.00 行高
- Fin Orange（`#ff5600`）作为唯一的品牌强调色
- 锐利的 4px 圆角——近乎矩形的按钮和元素
- Scale(1.1) 悬停效果配合 scale(0.85) 按下效果——物理按钮交互
- SaansMono 大写标签，宽字间距（0.6px–1.2px）
- 丰富的多彩报告调色板（blue、green、red、pink、lime、orange）
- oklab 颜色值用于精细的透明度管理

## 2. 调色板与角色

### 主色
- **Off Black**（`#111111`）：`--color-off-black`，主要文字、按钮背景
- **Pure White**（`#ffffff`）：`--wsc-color-content-primary`，主要表面
- **Warm Cream**（`#faf9f6`）：按钮背景、卡片表面
- **Fin Orange**（`#ff5600`）：`--color-fin`，主要品牌强调色
- **Report Orange**（`#fe4c02`）：`--color-report-orange`，数据可视化

### 报告调色板
- **Report Blue**（`#65b5ff`）：`--color-report-blue`
- **Report Green**（`#0bdf50`）：`--color-report-green`
- **Report Red**（`#c41c1c`）：`--color-report-red`
- **Report Pink**（`#ff2067`）：`--color-report-pink`
- **Report Lime**（`#b3e01c`）：`--color-report-lime-300`
- **Green**（`#00da00`）：`--color-green`
- **Deep Blue**（`#0007cb`）：深蓝色强调色

### 中性色阶（暖色）
- **Black 80**（`#313130`）：`--wsc-color-black-80`，深色中性色
- **Black 60**（`#626260`）：`--wsc-color-black-60`，中等中性色
- **Black 50**（`#7b7b78`）：`--wsc-color-black-50`，柔和文字
- **Content Tertiary**（`#9c9fa5`）：`--wsc-color-content-tertiary`
- **Oat Border**（`#dedbd6`）：温暖边框颜色
- **Warm Sand**（`#d3cec6`）：浅色温暖中性色

## 3. 排版规则

### 字体家族
- **主字体**：`Saans`，备选：`Saans Fallback, ui-sans-serif, system-ui`
- **衬线体**：`Serrif`，备选：`Serrif Fallback, ui-serif, Georgia`
- **等宽字体**：`SaansMono`，备选：`SaansMono Fallback, ui-monospace`
- **UI 字体**：`MediumLL` / `LLMedium`，备选：`system-ui, -apple-system`

### 层级

| 角色 | 字体 | 尺寸 | 字重 | 行高 | 字间距 |
|------|------|------|------|------|--------|
| Display Hero | Saans | 80px | 400 | 1.00（紧凑）| -2.4px |
| Section Heading | Saans | 54px | 400 | 1.00 | -1.6px |
| Sub-heading | Saans | 40px | 400 | 1.00 | -1.2px |
| Card Title | Saans | 32px | 400 | 1.00 | -0.96px |
| Feature Title | Saans | 24px | 400 | 1.00 | -0.48px |
| Body Emphasis | Saans | 20px | 400 | 0.95 | -0.2px |
| Nav / UI | Saans | 18px | 400 | 1.00 | normal |
| Body | Saans | 16px | 400 | 1.50 | normal |
| Body Light | Saans | 14px | 300 | 1.40 | normal |
| Button | Saans | 16px / 14px | 400 | 1.50 / 1.43 | normal |
| Button Bold | LLMedium | 16px | 700 | 1.20 | 0.16px |
| Serif Body | Serrif | 16px | 300 | 1.40 | -0.16px |
| Mono Label | SaansMono | 12px | 400–500 | 1.00–1.30 | 0.6px–1.2px 大写 |

## 4. 组件样式

### 按钮

**深色主按钮**
- 背景：`#111111`
- 文字：`#ffffff`
- 内边距：0px 14px
- 圆角：4px
- 悬停：白色背景，深色文字，scale(1.1)
- 按下：绿色背景（`#2c6415`），scale(0.85)

**描边按钮**
- 背景：透明
- 文字：`#111111`
- 边框：`1px solid #111111`
- 圆角：4px
- 相同的 scale 悬停/按下行为

**暖色卡片按钮**
- 背景：`#faf9f6`
- 文字：`#111111`
- 内边距：16px
- 边框：`1px solid oklab(... / 0.1)`

### 卡片与容器
- 背景：`#faf9f6`（Warm Cream）
- 边框：`1px solid #dedbd6`（温暖燕麦色）
- 圆角：8px
- 无可见阴影

### 导航
- 链接使用 Saans 16px
- 白色背景上的 Off Black 文字
- 小圆角 4px–6px 按钮
- AI 功能使用 Orange Fin 强调色

## 5. 布局原则

### 间距：8px, 10px, 12px, 14px, 16px, 20px, 24px, 32px, 40px, 48px, 60px, 64px, 80px, 96px
### 圆角：4px（按钮），6px（导航项），8px（卡片、容器）

## 6. 深度与层级
极简阴影。通过温暖的边框颜色和表面色调创造深度。

## 7. 最佳实践

### 应该
- 所有标题使用 Saans，行高 1.00 和负字间距
- 按钮应用 4px 圆角——锐利几何是核心识别
- 仅将 Fin Orange（#ff5600）用于 AI/品牌强调
- 按钮应用 scale(1.1) 悬停效果
- 使用温暖中性色（#faf9f6, #dedbd6）

### 不应
- 按钮圆角不要超过 4px
- 不要将 Fin Orange 用作装饰
- 不要使用冷灰色边框——始终使用温暖燕麦色调
- 标题不要省略负字间距

## 8. 响应式行为
断点：425px, 530px, 600px, 640px, 768px, 896px

## 9. Agent Prompt 指南

### 快速颜色参考
- 文字：Off Black（`#111111`）
- 背景：Warm Cream（`#faf9f6`）
- 强调色：Fin Orange（`#ff5600`）
- 边框：Oat（`#dedbd6`）
- 柔和色：`#7b7b78`

### 组件示例提示词
- "创建 hero：温暖米色（#faf9f6）背景。Saans 80px 字重 400，行高 1.00，字间距 -2.4px，#111111。深色按钮（#111111，4px 圆角）。悬停：scale(1.1)，白色背景。"
