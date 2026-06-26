# SF Symbols

> 来源：Apple HIG - SF Symbols (2026)
> https://developer.apple.com/design/human-interface-guidelines/sf-symbols

## 概述

SF Symbols 提供 6000+ 一致、高度可配置的系统图标，与 San Francisco 字体无缝对齐，自动匹配所有字重和字号。

**下载与浏览**：[SF Symbols Mac App](https://developer.apple.com/sf-symbols/)

---

## 渲染模式（Rendering Modes）

SF Symbols 将图标的路径分为多个图层（Primary / Secondary / Tertiary）。

### 1. Monochrome（单色）
所有图层应用同一颜色。路径内可填充透明或指定颜色。

### 2. Hierarchical（层级）
同一颜色不同透明度，传达视觉深度感。

### 3. Palette（调色板）
为每个图层指定不同颜色（最多支持多色）。

### 4. Multicolor（多色）
系统内置颜色（如 `leaf.fill` 用绿色，`trash.slash` 用红色表示数据丢失）。

---

## 渐变（Gradients）

SF Symbols 7+ 支持线性渐变，所有渲染模式都支持：
- 从单一源色生成平滑渐变
- 在任何尺寸都支持，但大尺寸效果最佳

---

## 可变颜色（Variable Color）

用于表达随时间变化的特性（音量、强度、容量）：
- 符号的不同图层在不同阈值下被着色
- 不适合用可变颜色表达深度感（用 Hierarchical）

---

## 字重与尺寸（Weights & Scales）

### 字重（9 级）
`ultralight` / `light` / `thin` / `regular` / `medium` / `semibold` / `bold` / `heavy` / `black`

与 SF 字体字重完全对应，保证图标与文字视觉重量一致。

### 尺寸（3 级）
| 尺寸 | 相对于 San Francisco Cap Height |
|------|------|
| Small | 0.5x |
| Medium（默认） | 1.0x |
| Large | 1.5x |

---

## 符号变体（Design Variants）

| 变体 | 说明 |
|------|------|
| `outline`（描边） | 最常见，适合 Toolbar、List |
| `fill`（填充） | 更强视觉重量，适合 Tab Bar、Swipe Actions |
| `slash`（斜杠） | 表示不可用（如 `eye.slash`） |
| `circle.fill` | 圆形包裹，适合小尺寸增强可读性 |
| `badge` | 徽章变体 |

### 变体组合
`book.fill` = 填充 + book 形状
`xmark.circle.fill` = 填充 + 圆形 + xmark

---

## 动画（Animations）

| 动画 | 效果 | 用途 |
|------|------|------|
| `Appear` | 渐现 | 元素出现 |
| `Disappear` | 渐隐 | 元素消失 |
| `Bounce` | 弹性弹跳 | 反馈操作发生 |
| `Scale` | 缩放 | 吸引注意力到选中项 |
| `Pulse` | 透明度变化 | 持续活动中 |
| `Variable Color` | 逐层变色 | 进度、播放中、连接中 |
| `Replace` | 符号替换 | 状态切换 |
| `Magic Replace` | 智能形变 | 相关形状间的智能过渡 |
| `Wiggle` | 左右/上下摆动 | 强调变化 |
| `Breathe` | 呼吸效果 | 状态变化、录制中 |
| `Rotate` | 旋转 | 活动指示 |
| `Draw On/Off` | 路径绘制 | 下载进度等 |

**使用原则：**
- 谨慎使用动画
- 确保每个动画有明确目的
- 考虑 App 整体风格和色调

---

## 自定义符号（Custom Symbols）

### 设计原则
- **Simple** — 简洁
- **Recognizable** — 易辨认
- **Inclusive** — 包容（不同文化背景都能理解）
- **Directly related** — 与所表达的动作/内容直接相关

### 创建步骤
1. 在 SF Symbols App 找到相似符号，导出其模板
2. 用矢量工具修改模板
3. 使用 **annotating** 为各图层分配颜色或层级

### 注意事项
- 不要复制 Apple 产品外观的符号
- 可为图层设置负边距以改善光学对齐
- 确保图层设计适合动画
- 为自定义符号提供替代文字标签（Accessibility）
- 避免自己绘制常见的 enclosure/badge 变体，用 App 提供的组件库

---

## 使用场景建议

| 场景 | 推荐变体 |
|------|---------|
| Toolbar | outline |
| Tab Bar（iOS） | fill |
| List 内图标 | outline |
| Swipe Actions | fill |
| 不可用状态 | slash |
| 选中状态 | fill + accent color |
| 操作反馈 | 动画（bounce/scale） |
