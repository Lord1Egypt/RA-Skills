# Apple Design Principles

> 来源：Apple Human Interface Guidelines (2026)
> https://developer.apple.com/design/human-interface-guidelines/

## 三大核心原则

### 1. Hierarchy（层次感）
建立清晰的视觉层次，控件和界面元素要突出内容、形成区分。

> Establish a clear visual hierarchy where controls and interface elements elevate and distinguish the content beneath them.

- 内容优先于装饰
- 通过大小、颜色、对比度区分重要性
- 重要信息用更大字体或更强对比

### 2. Harmony（和谐）
与硬件和软件 concentric design（同心设计）保持一致，创造界面元素、系统体验与设备之间的和谐。

> Align with the concentric design of the hardware and software to create harmony between interface elements, system experiences, and devices.

- 界面元素与设备形态呼应（如 iPhone 的圆润边角、Vision Pro 的空间设计）
- 深色模式/浅色模式与系统外观自动适配
- UI 与触感反馈协调

### 3. Consistency（一致性）
遵循平台约定，在不同窗口大小和显示器间保持一致的设计。

> Adopt platform conventions to maintain a consistent design that continuously adapts across window sizes and displays.

- 使用系统组件（Tab Bar、Navigation Bar、Alert 等）
- 遵循平台惯例（iOS 用 Tab Bar、macOS 用 Toolbar）
- 跨尺寸保持体验一致

---

## 设计要素

### Clarity（清晰）
- 突出重要内容，弱化次要元素
- 图标和文字要具有可读性
- 留白创造呼吸感

### Deference（谦逊）
- 系统 UI 不抢占内容空间
- 控件在需要时才出现
- 内容本身是主角

### Depth（深度）
- 使用视觉层次（阴影、模糊、毛玻璃）传达空间关系
- 支持手势和转场动画增加交互深度感
- visionOS 强调空间深度（Z 轴）

---

## 平台哲学

| 平台 | 核心理念 |
|------|---------|
| **iOS/iPadOS** | 手势驱动、边缘交互、App 切换器 |
| **macOS** | 窗口管理、Menu Bar、快捷键 |
| **visionOS** | 空间计算、沉浸感、billboarding |
| **watchOS** | 紧凑信息、Glance、Digital Crown |
| **tvOS** | 远程导航、焦点驱动、大屏幕 |

---

## 设计流程建议

1. **从内容出发** — 不要从装饰出发，先确定要传达的信息
2. **用系统组件** — 优先使用系统提供的 UI 组件
3. **保持简洁** — 避免不必要的视觉元素
4. **测试真实场景** — 在真机上测试不同光照、不同字体大小
5. **无障碍优先** — 从一开始就将 VoiceOver、Dynamic Type 纳入设计
