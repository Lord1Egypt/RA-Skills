# Typography System

> 来源：Apple HIG - Typography (2026)
> https://developer.apple.com/design/human-interface-guidelines/typography

## 字体家族

### San Francisco (SF)
Apple 的默认无衬线字体家族，包含多个变体：

| 变体 | 用途 |
|------|------|
| SF Pro | iOS/macOS/tvOS/visionOS 主字体 |
| SF Compact | watchOS 专用（更窄） |
| SF Pro Rounded | 配合圆润 UI 元素 |
| SF Arabic/Hebrew/Georgian/Armenian | 多语言支持 |
| SF Mono | 等宽字体（代码/数字显示） |

### New York (NY)
Apple 的衬线字体家族，设计用于与 SF 配合或单独使用：
- 适合长篇阅读、编辑场景
- 支持多种字重和宽度

### 动态字体格式
SF 和 NY 都以**可变字体（Variable Font）**格式提供，支持：
- 连续字重插值（Ultralight → Black）
- 多种宽度（Condensed / Regular / Expanded）
- **Dynamic Optical Sizes** — 系统自动根据字号调整字形设计（Text / Display 融合为连续设计）

---

## 字号规范

### 平台默认/最小字号

| 平台 | 默认字号 | 最小字号 |
|------|---------|---------|
| iOS/iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

### iOS Dynamic Type 尺寸表（iOS/iPadOS）

| Style | Default | xLarge | xxLarge | xxxLarge |
|-------|---------|--------|---------|---------|
| Large Title | 34pt Bold | 38pt | 42pt | 46pt |
| Title 1 | 28pt Bold | 31pt | 34pt | 38pt |
| Title 2 | 22pt Bold | 25pt | 28pt | 31pt |
| Title 3 | 20pt Semibold | 23pt | 25pt | 28pt |
| Headline | 17pt Semibold | 20pt | 22pt | 24pt |
| Body | 17pt Regular | 20pt | 22pt | 24pt |
| Callout | 16pt Regular | 19pt | 21pt | 23pt |
| Subhead | 15pt Regular | 18pt | 20pt | 22pt |
| Footnote | 13pt Regular | 16pt | 18pt | 20pt |
| Caption 1 | 12pt Regular | 14pt | 16pt | 18pt |
| Caption 2 | 11pt Regular | 13pt | 15pt | 17pt |

---

## 排版层级实践

### 字体字重选择
- **推荐**：Regular, Medium, Semibold, Bold
- **避免**：Ultralight, Thin, Light（可读性差，尤其小字号）

### 字重匹配
SF Symbols 提供与 SF 字体完全对应的 9 级字重，保证图标与文字的视觉重量一致。

### 行高（Leading）
| 场景 | 推荐 |
|------|------|
| 长段落阅读 | Loose leading（更多行间距） |
| 列表行等高度受限场景 | Tight leading |
| 三行及以上 | 避免 tight leading |

### 字间距（Tracking）
- 系统字体在运行时自动调整 Tracking
- 设计稿中需手动调整以匹配系统渲染效果
- 字号越小，通常 tracking 需要略为正值

---

## Dynamic Type 支持

Dynamic Type 是 iOS/iPadOS/tvOS/visionOS/watchOS 的系统级功能，让用户调整文字大小。

### 设计要求
1. **布局自适应** — 验证设计在所有字号下都能正常显示
2. **图标同步缩放** — 使用 SF Symbols，它们随 Dynamic Type 自动缩放
3. **减少文字截断** — 尽量显示完整内容，避免截断
4. **大字号时的布局调整** — 考虑堆叠布局（文字在上，次要信息在下）
5. **保持层级一致性** — 字号增大时，主要元素仍在顶部

---

## 平台注意事项

### iOS/iPadOS
- SF Pro 是系统字体
- 支持 Dynamic Type

### macOS
- SF Pro 是系统字体
- **不支持 Dynamic Type**
- 使用 `Font(ofSize:)` 变体来匹配系统控件文字

### visionOS
- SF Pro 是系统字体
- 使用更粗的 Dynamic Type body/title 样式
- 引入了 Extra Large Title 1/2（大屏编辑风格）
- 优先使用 **2D 文字**（3D 文字可读性差）
- 涉及空间对象的文字使用 **billboarding**（永远朝向用户）

### watchOS
- SF Compact 是系统字体
- 复杂场景用 SF Compact Rounded
