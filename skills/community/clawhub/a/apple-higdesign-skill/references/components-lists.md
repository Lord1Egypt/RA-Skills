# Lists, Tables & Collections

> 来源：Apple HIG - Tables / Lists / Collections (2026)
> https://developer.apple.com/design/human-interface-guidelines/tables
> https://developer.apple.com/design/human-interface-guidelines/lists
> https://developer.apple.com/design/human-interface-guidelines/collections

## Tables（列表视图）

用于展示有结构的数据行，支持选中、编辑、删除、分组。

### iOS Table View
- 分组列表（Inset Grouped）或普通列表
- 每行高度 ≥ 44pt（触摸目标）
- 支持 swipe actions（滑动操作）

### macOS Table
- 列可以排序、重排宽度
- 支持交替行颜色
- 支持大纲模式（层级折叠/展开）

### 设计规范
- 文字左对齐，辅助信息右对齐
- 分组头用中粗体字
- 分割线用系统 separator 颜色

---

## Lists（列表）

iOS 17+ 的新列表系统，比 Table View 更现代、更有表现力。

### 特点
- 支持 SwiftUI List DSL
- 丰富的内置样式（`.insetGrouped`, `.plain`, `.sidebar`）
- 内置 swipe actions
- 支持展开/折叠

### 列表样式

| 样式 | 场景 |
|------|------|
| `.plain` | 简单列表，无背景 |
| `.insetGrouped` | iOS 设置风格分组 |
| `.grouped` | 标准分组列表 |
| `.sidebar` | 侧边栏风格 |

---

## Collections（集合视图）

网格布局展示图片或内容卡片。

### 场景
- 相册网格
- App Store 展示卡片
- 商品列表（网格视图）

### 布局模式
- **瀑布流（Compositional Layout）** — 不同高度网格
- **均匀网格（Uniform）** — 每项大小相同
- **列表布局（List）** — 集合视图的列表模式

### 单元格
- 圆角：12-16pt
- 内边距：足够空间
- 图片比例：保持一致或有序变化

---

## Swipe Actions（滑动操作）

列表行的快捷操作。

### iOS 常见操作
| 方向 | 操作 |
|------|------|
| 左滑 | Delete（红色）/ Archive（灰色） |
| 右滑 | Pin / Mark Read |

### 设计原则
- 最多 3 个操作
- 主要操作（Delete）放最左边或用 destructive 颜色
- 图标 + 短文字标签

---

## Drag & Drop（拖放）

### 场景
- 列表重排序
- 文件在不同 App 间传递
- 文字/图片拖入编辑区

### 视觉反馈
- 拖动时原位置显示占位符
- 拖动项有阴影和缩放（1.05x）
- 有效放下区域高亮

---

## 平台差异

| 特性 | iOS | iPadOS | macOS |
|------|-----|--------|-------|
| Inset Grouped | ✅ | ✅ | ✅ |
| Swipe Actions | ✅ | ✅ | ✅ |
| Drag & Drop | ✅ | ✅ | ✅ |
| 交替行颜色 | ❌ | ❌ | ✅ |
| 列排序 | ❌ | ❌ | ✅ |
