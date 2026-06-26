# Apple Design System Skill

基于 Apple Human Interface Guidelines (2026)，覆盖所有 Apple 平台的设计规范。

## 概述

本 skill 覆盖 Apple 全平台设计知识体系，包括：

- **设计原则** — Hierarchy / Harmony / Consistency + 平台哲学
- **Typography** — San Francisco / New York / Dynamic Type / 字号层级
- **Color System** — 系统色 / Dark Mode / Liquid Glass / 宽色域 P3 / 无障碍色彩
- **SF Symbols** — 6000+ 图标库 / 渲染模式 / 动画 / 自定义符号
- **Components** — Button / Navigation / Tab Bar / Alert / List / TextField / SearchBar / Toggle / DatePicker
- **Accessibility** — VoiceOver / Dynamic Type / 对比度 / Reduce Motion / 肢体无障碍
- **Animation** — 动画原则 / 手势驱动 / SF Symbols 动画 / 性能
- **Spatial Layout** — visionOS 空间布局 / Liquid Glass / Billboarding / 3D 界面
- **Branding** — App Icon / 品牌色 / 启动画面 / Apple 品牌规范

## 核心章节

### 设计基础

| 章节 | 内容 |
|------|------|
| [设计原则](SKILL.md#设计原则) | Hierarchy / Harmony / Consistency + 平台哲学 |
| [Typography 详解](SKILL.md#Typography-详解) | San Francisco / New York / Dynamic Type / 字号层级 |
| [Color System 详解](SKILL.md#Color-System-详解) | 系统色 / Dark Mode / Liquid Glass / 宽色域 P3 |
| [SF Symbols 详解](SKILL.md#SF-Symbols-详解) | 渲染模式 / 动画 / Variable Color / 自定义符号 |

### 组件设计

| 章节 | 内容 |
|------|------|
| [组件详解](SKILL.md#组件详解) | Button / Toggle / Slider / Segmented Control / DatePicker |
| [Navigation Bar](references/components-navigation.md) | 导航栏 / Tab Bar / Toolbar / Sheet / Sidebar |
| [Lists](references/components-lists.md) | Table / List / Collection / Swipe Actions / Drag & Drop |
| [TextField & SearchBar](references/components-textfield.md) | 输入框 / 搜索栏 / TextEditor |
| [Containers](references/components-containers.md) | Alert / Action Sheet / Modal / Popover / Menu |
| [Buttons](references/components-buttons.md) | 填充按钮 / Tinted / Gray / Destructive / Borderless |

### 平台差异化

| 章节 | 内容 |
|------|------|
| [平台差异化设计](SKILL.md#平台差异化设计) | iOS / iPadOS / macOS / tvOS / watchOS / visionOS |
| [watchOS HIG](references/watchos-hig.md) | 表盘 / 导航 / 通知 / Health / 手势 / Haptic |

### 体验设计

| 章节 | 内容 |
|------|------|
| [Accessibility 无障碍](SKILL.md#Accessibility-无障碍) | VoiceOver / Dynamic Type / 对比度 / Reduce Motion |
| [Animation 动效设计](SKILL.md#Animation-动效设计) | 动画原则 / 手势驱动 / SF Symbols 动画 / 性能 |
| [Spatial Layout 空间布局](SKILL.md#Spatial-Layout-空间布局) | visionOS / Liquid Glass / Billboarding / 3D 界面 |
| [品牌与图标](SKILL.md#品牌与图标) | App Icon / 品牌色 / 启动画面 / Apple 品牌规范 |

## 快速参考

### Apple 平台默认字号

| 平台 | 默认 | 最小 |
|------|------|------|
| iOS/iPadOS | 17pt | 11pt |
| macOS | 13pt | 10pt |
| tvOS | 29pt | 23pt |
| visionOS | 17pt | 12pt |

### 系统强调色

`#007AFF` (Blue) — iOS/macOS 默认强调色

### 最小触摸目标

**44 × 44 pt**（Apple HIG 规定）

### 按钮样式优先级

`Filled Button → Tinted Button → Gray Button → Borderless Button`

### Dark Mode 背景色

`#1C1C1E`（不是纯黑 `#000000`）

### SF Symbols 渲染模式

`Monochrome → Hierarchical → Palette → Multicolor`

### 布局规范

| 元素 | 边距/间距 | 备注 |
|------|---------|------|
| 屏幕边缘 | 16pt | iOS 标准 |
| 组件间距 | 8pt | 8pt 网格 |
| 列表 Cell 高度 | 44pt | 触摸目标 |
| 导航栏高度 | 44pt | 标准 |
| TabBar 高度 | 49pt | iPhone |
| 大标题导航栏 | 96pt | iOS 11+ |

### 平台组件层级

```
iOS/macOS:
Window → ViewController → View → Subviews
NavigationController → ViewController → TableView → Cell
TabBarController → ViewController × N → NavigationController

visionOS:
Space → Window → Volume → 3D Content
WindowGroup → Content → SwiftUI Views
```

### iOS vs macOS vs watchOS vs tvOS vs visionOS

| 维度 | iOS/iPadOS | macOS | watchOS | tvOS | visionOS |
|------|-----------|-------|---------|------|---------|
| 导航 | Nav Bar + Tab Bar | Toolbar + Sidebar | Tab Bar + page | Tab Bar | Tab Nav |
| 输入 | 触摸 + Keyboard | Keyboard + Mouse | Digital Crown + Gesture | Remote | Eye + Hand |
| 字号最小 | 11pt | 10pt | 10pt | 23pt | 12pt |
| 强调色 | #007AFF | #007AFF | #007AFF | #007AFF | #007AFF |

## 避坑指南

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ Dark Mode 用纯黑 `#000000` | ✅ 用 `#1C1C1E`（Apple HIG 规定） |
| ❌ macOS 使用 Dynamic Type | ✅ macOS 不支持，仅 iOS/iPadOS 支持 |
| ❌ 用红绿组合传达信息 | ✅ 用蓝色+图标辅助，色盲友好 |
| ❌ visionOS 使用 3D 文字 | ✅ 用 billboarding + 2D 文字 |
| ❌ 触摸目标小于 44×44pt | ✅ 最小 44×44pt |
| ❌ 超链接用绿/蓝色组合 | ✅ 用统一蓝色 `#007AFF` |
| ❌ SearchBar 不提供清除按钮 | ✅ 右滑显示 Clear 按钮 |
| ❌ 硬编码系统颜色值 | ✅ 使用语义化颜色（.primary / .secondary） |
| ❌ 仅靠颜色传达信息 | ✅ 配合文字标签/图标 |
| ❌ 忽略 Reduce Motion 设置 | ✅ 动画需考虑无障碍 |

### 版本陷阱

- ⚠️ **Liquid Glass** — 仅限 visionOS，iOS/macOS 不支持
- ⚠️ **SF Symbols 渐变** — 仅 SF Symbols 7+ 支持，低版本设备 fallback
- ⚠️ **SF Symbols 动画** — Variable Color 不适合表达深度感，应用 Hierarchical
- ⚠️ **watchOS** — 使用 SF Compact（更窄），不是 SF Pro
- ⚠️ **Dynamic Type** — 大字号时布局可能截断，需测试所有尺寸

## 参考文档

| 文件 | 行数 | 内容 |
|------|------|------|
| watchos-hig.md | 332 | watchOS HIG：表盘/导航/通知/Health/手势/Haptic |
| color.md | 270 | 色彩系统：系统色/Dark Mode/Liquid Glass/P3 |
| components-containers.md | 269 | 容器组件：Alert/ActionSheet/Modal/Popover/Menu |
| components-controls.md | 247 | 控件组件：Toggle/Slider/SegmentedControl/DatePicker |
| components-textfield.md | 175 | 文本组件：TextField/SearchBar/TextEditor |
| components-buttons.md | 210 | 按钮组件：Filled/Tinted/Gray/Destructive/Borderless |
| components-navigation.md | 136 | 导航组件：NavBar/TabBar/Toolbar/Sheet/Sidebar |
| sf-symbols.md | 136 | SF Symbols：图标库/渲染模式/动画/Variable |
| accessibility.md | 125 | 无障碍：VoiceOver/Dynamic Type/对比度/ReduceMotion |
| typography.md | 118 | 字体：San Francisco/New York/Dynamic Type |
| components-lists.md | 110 | 列表组件：Table/List/Collection/Swipe |
| spatial-layout.md | 99 | 空间布局：visionOS/Liquid Glass/Billboarding |
| animation.md | 97 | 动画：原则/手势/SF Symbols动画/性能 |
| branding.md | 86 | 品牌：App Icon/品牌色/启动画面 |
| design-principles.md | 74 | 设计原则：Hierarchy/Harmony/Consistency |

## 来源

> Apple Human Interface Guidelines（2026-04-23 访问）
> - 主页：https://developer.apple.com/design/human-interface-guidelines/
> - Typography：https://developer.apple.com/design/human-interface-guidelines/typography
> - Color：https://developer.apple.com/design/human-interface-guidelines/color
> - SF Symbols：https://developer.apple.com/design/human-interface-guidelines/sf-symbols
> - Dark Mode：https://developer.apple.com/design/human-interface-guidelines/dark-mode
> - Accessibility：https://developer.apple.com/design/human-interface-guidelines/accessibility
> - Components：https://developer.apple.com/design/human-interface-guidelines/components
>
> 版本：HIG 2026（基于 iOS 18 / macOS 15 / watchOS 11 / tvOS 18 / visionOS 2）
