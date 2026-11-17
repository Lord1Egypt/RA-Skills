# App 设计规范 — {{项目名称}}

> 版本：v1.0 | 更新日期：{{日期}} | 设计：{{设计师}}

---

## 1. 项目概述

| 项目 | 内容 |
|------|------|
| 项目名称 | {{项目名称}} |
| 业务领域 | {{业务领域}} |
| 设计风格 | {{风格方向}} |
| 目标平台 | iOS / Android |
| 设计稿基准 | 375×812pt (iPhone X) / 360×640dp (Android) |

### 设计原则

{{根据业务领域生成 3-5 条设计原则}}

---

## 2. 色彩系统

### 2.1 品牌色

| 令牌 | 色值 | 用途 | 说明 |
|------|------|------|------|
| color-primary-500 | #{{主色}} | 主操作、选中态、品牌色 | 遵循 WCAG AA 对比度 |
| color-primary-600 | #{{主色深}} | 按压态、重要强调 | 主色加深 10% |
| color-primary-700 | #{{主色更深}} | 深色模式强调 | 主色加深 20% |
| color-primary-100 | #{{主色浅}} | 浅色背景、选中背景 | 主色 10% 透明度底 |
| color-primary-050 | #{{主色极浅}} | hover 态背景 | 主色 5% 透明度底 |

### 2.2 辅助色

| 令牌 | 色值 | 用途 |
|------|------|------|
| color-secondary-500 | # | 次级操作、链接 |
| color-secondary-100 | # | 浅色辅助底 |

### 2.3 中性色

| 令牌 | 色值 | 用途 |
|------|------|------|
| color-neutral-900 | #1A1A1A | 主文字 |
| color-neutral-800 | #333333 | 标题 |
| color-neutral-600 | #666666 | 次级文字 |
| color-neutral-400 | #999999 | 辅助/占位文字 |
| color-neutral-200 | #EEEEEE | 分割线、描边 |
| color-neutral-100 | #F7F7F7 | 背景 |
| color-neutral-000 | #FFFFFF | 纯白（浅色模式）|
| color-neutral-950 | #0D0D0D | 深色模式背景 |

### 2.4 语义色

| 类型 | 令牌 | 色值 | 用途 |
|------|------|------|------|
| 成功 | color-semantic-success | #34C759 | 成功状态、已完成 |
| 警告 | color-semantic-warning | #FF9500 | 警告提示 |
| 错误 | color-semantic-error | #FF3B30 | 错误、删除、禁用 |
| 信息 | color-semantic-info | #007AFF | 信息提示 |

> iOS HIG 原生语义色作为参考值，如品牌有主色可调整。

---

## 3. 字体系统

> iOS: SF Pro / PingFang SC | Android: Roboto / 思源黑体 (Noto Sans SC)

| 令牌 | 字号(pt) | 行高 | 字重 | 用途 |
|------|----------|------|------|------|
| font-size-display | 34 | 1.2 | Bold | 页面大标题 |
| font-size-title | 28 | 1.3 | Bold/Semibold | 板块标题 |
| font-size-headline | 22 | 1.3 | Semibold | 卡片标题 |
| font-size-body | 17 | 1.4 | Regular | 正文 |
| font-size-callout | 16 | 1.4 | Regular | 次级正文 |
| font-size-subheadline | 15 | 1.4 | Regular | 列表行文字 |
| font-size-footnote | 13 | 1.4 | Regular | 辅助文字 |
| font-size-caption | 11 | 1.4 | Regular | 标签、徽标 |

**数字字体**：SF Mono / Roboto Mono / DIN（数据展示场景）

---

## 4. 间距与栅格

### 4.1 间距系统（4pt × 倍数 — 8pt 网格）

| 令牌 | 值(pt) | 用途 |
|------|--------|------|
| spacing-0.5 | 2 | 微间距 |
| spacing-1 | 4 | 紧凑间距 |
| spacing-2 | 8 | 常用内边距 |
| spacing-3 | 12 | 组件内边距 |
| spacing-4 | 16 | 卡片内边距 |
| spacing-5 | 24 | 区块间距 |
| spacing-6 | 32 | 页面边距 |
| spacing-8 | 48 | 大区块间距 |

### 4.2 栅格与页面边距

| 设备 | 页面水平安全边距 |
|------|------------------|
| iPhone | 16pt |
| Android | 16dp |

- 卡片间距：12-16pt
- 栅格系统：可选 4 列（手机）/ 8 列（平板）

---

## 5. 圆角与阴影

### 5.1 圆角

| 令牌 | 值(pt) | 用途 |
|------|--------|------|
| radius-sm | 6 | 标签、小元素 |
| radius-md | 10 | 输入框、按钮、图标容器 |
| radius-lg | 16 | 卡片 |
| radius-xl | 24 | 弹窗、大卡片 |
| radius-full | 999 | 圆形元素、胶囊按钮 |

### 5.2 阴影

| 层级 | 值 | 用途 |
|------|-----|------|
| shadow-1 | 0 1pt 2pt rgba(0,0,0,0.06) | 悬浮元素 |
| shadow-2 | 0 4pt 8pt rgba(0,0,0,0.08) | 弹窗、浮层 |
| shadow-3 | 0 8pt 24pt rgba(0,0,0,0.12) | 固定导航、底部抽屉 |

---

## 6. 图标规范

| 参数 | 规范 |
|------|------|
| 标准尺寸 | 24pt |
| 次级尺寸 | 16 / 20 / 28 / 32pt |
| 线条粗细 | 2pt（标准）/ 1.5pt（精细） |
| 风格 | 线性为主，圆角端点，NFG/SF Symbols 风格 |
| 色彩 | 默认 color-neutral-800，选中 color-primary-500 |
| 最小点击区域 | 44×44pt（iOS）/ 48×48dp（Android） |

---

## 7. 组件规范

### 7.1 按钮

| 类型 | 高度(pt) | 圆角 | 字号 | 场景 |
|------|----------|------|------|------|
| 主按钮 | 50 | 25 | 17 | 主要操作，品牌色填充 |
| 次级按钮 | 50 | 25 | 17 | 次级操作，线框/浅底 |
| 文字按钮 | 44 | - | 17 | 轻量操作 |
| 小按钮 | 32 | 16 | 14 | 列表内操作 |
| 图标按钮 | 44×44 | radius-md | - | 工具栏操作 |

- 主按钮最小宽度：112pt
- 禁用：color-neutral-200 背景 + color-neutral-400 文字
- iOS 建议使用全圆角。

### 7.2 输入框

| 参数 | 规范 |
|------|------|
| 高度 | 44pt（iOS）/ 48dp（Android） |
| 内边距 | 左右 16pt |
| 圆角 | radius-md（10pt） |
| 背景 | color-neutral-100 |
| 聚焦边框 | 1.5pt color-primary-500 |
| 错误边框 | 1.5pt color-semantic-error |
| 占位文字 | color-neutral-400 |

### 7.3 列表

| 参数 | 规范 |
|------|------|
| 行高 | 44pt 最小（iOS） |
| 内边距 | 左右 16pt |
| 分割线 | 0.5pt color-neutral-200，左侧 16pt inset |
| 左图标 | 24pt color-neutral-800 |
| 右侧箭头 | 12pt color-neutral-400 |

### 7.4 卡片

| 参数 | 规范 |
|------|------|
| 内边距 | 16pt |
| 圆角 | radius-lg（16pt） |
| 背景 | color-neutral-000 / 深色模式 color-neutral-900 |
| 卡片间距 | 12-16pt |
| 可选阴影 | shadow-1 |

### 7.5 导航

| 类型 | 规范 |
|------|------|
| NavigationBar | 44pt 高（iOS）+ 状态栏，背景与页面一致或毛玻璃 |
| TabBar | 49pt 高（iOS）+ 安全区，图标 24pt + 10pt 文字 |
| ToolBar | 44pt 高 |
| 搜索栏 | 36pt 圆角 10pt |

### 7.6 反馈

| 组件 | 规范 |
|------|------|
| Toast | 暗色圆角矩形 rgba(0,0,0,0.75)，16pt 圆角，居中 |
| Dialog | 宽度 270pt，圆角 14pt（iOS）or radius-lg |
| ActionSheet | 底部拉起，圆角 14pt（iOS） |
| Snackbar（Android） | 底部 6dp 高度，圆角 4dp |

---

## 8. 平台规范

### 8.1 iOS 特有

| 项 | 值 |
|-----|-----|
| 状态栏 | 44pt（刘海屏） |
| 底部安全区 | 34pt（Home Indicator） |
| 导航栏 | 44pt，毛玻璃效果 |
| TabBar | 49pt |
| 圆角按钮 | 建议全圆角 |
| 字体 | SF Pro / PingFang SC |
| 动效 | 300ms 标准曲线，支持 Haptics |

### 8.2 Android 特有

| 项 | 值 |
|-----|-----|
| 状态栏 | 24dp |
| 导航栏（底部） | 48dp 或手势条 |
| 顶部栏 | 56dp |
| TabBar | 56dp |
| 点击波纹 | 使用 Material ripple 效果 |
| 字体 | Roboto / 思源黑体 |
| 动效 | 200-300ms，标准曲线 |

### 8.3 深色模式

| 元素 | 浅色 | 深色 |
|------|------|------|
| 背景 | #FFFFFF | #0D0D0D |
| 卡片 | #FFFFFF | #1C1C1E |
| 主文字 | #1A1A1A | #FFFFFF |
| 次级文字 | #666666 | #AEAEB2 |
| 分割线 | #EEEEEE | #38383A |
| 阴影 | 有 | 弱化/无 |

---

## 9. 交付说明

### 9.1 切图规范

| 资源 | 规格 | 格式 |
|------|------|------|
| 图标 | 1x/2x/3x 三套（iOS），mdpi-xxxhdpi（Android） | PNG/JPG |
| 图片素材 | 按实际尺寸 ×2/×3 | WebP/JPG |
| 动效 | Lottie | JSON |

### 9.2 命名规范

```text
模块_组件_状态_尺寸_平台
示例：home_button_primary_normal_44x44_ios.png
```

### 9.3 标注

- 使用 Figma Auto Layout / 蓝湖
- 标注需包含：间距、字号、色值、圆角、阴影、安全区

---

*本文档由设计规范生成器生成，请根据实际项目调整。*