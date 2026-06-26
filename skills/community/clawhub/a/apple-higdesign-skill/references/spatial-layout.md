# Spatial Layout

> 来源：Apple HIG - Spatial Layout / visionOS (2026)
> https://developer.apple.com/design/human-interface-guidelines/spatial-layout

## 空间设计原则

visionOS 是 Apple 的空间计算平台，界面在用户周围的三维空间中呈现。

### 核心概念
- **Window（窗口）** — App 内容所在的 3D 容器
- **Volume（容器）** — 封闭的 3D 空间，可从各角度观看
- **Space（空间）** — visionOS 中 App 运行的混合/全空间
- **Immersive Space（沉浸空间）** — 覆盖真实世界的全虚拟环境

---

## 布局维度

### 距离与深度
- UI 元素默认放在 1 米外的"舒适区"
- 近距离（< 1m）用于需要专注的内容
- 远距离（> 1m）用于背景信息或装饰

### 焦点与注意力
- 用户注视的方向是主要输入
- 眼睛注视 → 焦点元素高亮 → 手指捏合确认
- UI 应将重要元素放在用户自然注视区

### Z 轴布局
- 内容沿 Z 轴前后排列
- 通过透明度、阴影、模糊区分层级
- 前层元素遮挡后层（符合物理规律）

---

## 毛玻璃材质（Liquid Glass）

visionOS 的标志性材质：
- 默认透明，透出背景
- 支持背景色（彩色玻璃效果）
- 前景/背景分离，内容层清晰

### 使用场景
| 元素 | 材质效果 |
|------|---------|
| Sidebar | 高不透明度毛玻璃 |
| Tab Bar | 低不透明度毛玻璃 |
| Toolbar | 中等不透明度 |
| Floating 控件 | 可变不透明度 |
| Content Area | 背景内容层 |

---

## Typography in visionOS

### 文字处理
- 优先使用 **2D 文字**（3D 文字可读性差）
- 需要空间定位的文字（如 3D 物体标签）使用 **billboarding**（永远朝向用户）
- 标题样式比 iOS 更粗更大

### Extra Large Title
visionOS 特有的超大标题样式，用于编辑风格布局。

---

## 窗口设计

### 可调整大小的 Window
- 窗口可由用户拖动调整
- 内容自适应窗口尺寸
- 断点：紧凑 / 中等 / 扩展

### 多窗口
- App 可创建多个 Window
- 每个 Window 是独立的 Navigation Context
- 窗口可并排显示（Split View）

---

## 交互方式

| 交互 | 输入 |
|------|------|
| 注视 + 捏合 | 主要选择操作 |
| 手指悬停 | 焦点高亮（hover state） |
| 手势拖动 | 移动/缩放窗口 |
| 眼动 + 手势 | 精确指向 |

---

## 设计检查

- [ ] 文字在空间中有足够的可读性（避免过小）
- [ ] 重要内容在舒适距离（~1m）
- [ ] 使用 billboarding 固定面向用户的标签
- [ ] 测试不同大小窗口的布局适配
- [ ] 减少不必要的 3D 文字
- [ ] 背景内容层与前景 UI 有足够区分度
