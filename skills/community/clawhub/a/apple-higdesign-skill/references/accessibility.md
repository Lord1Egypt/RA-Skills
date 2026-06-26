# Accessibility

> 来源：Apple HIG - Accessibility / Dynamic Type (2026)
> https://developer.apple.com/design/human-interface-guidelines/accessibility
> https://developer.apple.com/design/human-interface-guidelines/dynamic-type

## 核心原则

> Accessibility is not a feature — it's a human right.
> Or more practically: accessibility is quality.

Apple 将无障碍视为**质量指标**，而非附加功能。

---

## 视觉无障碍

### VoiceOver
屏幕阅读器，帮助盲人或视力低视力用户使用设备。

**设计要求：**
- 所有交互元素必须有 `.accessibilityLabel()`
- 图片应有描述（`accessibilityLabel` = "风景照片：山间日落"）
- 装饰性图片设置 `accessibilityHidden=true`
- 表格行应描述内容和动作（如 "Delete button, row 3 of 10"）

### Dynamic Type
用户可调整全局文字大小。

**设计要求：**
- 所有文字使用 Dynamic Type text styles
- 布局自适应文字大小增长
- 避免文字截断（用多行标签）
- SF Symbols 自动随 Dynamic Type 缩放

### 颜色对比度
| 文字类型 | 最低对比度 |
|---------|-----------|
| 普通文字（< 18pt） | 4.5:1 |
| 大字（≥ 18pt / 粗体 ≥ 14pt） | 3:1 |
| UI 组件和图形对象 | 3:1 |

### 色彩
- 不要仅靠颜色传达信息
- 提供文字标签或形状差异作为替代方案
- 考虑色盲用户（避免红绿组合）

---

## 运动无障碍

### Reduce Motion
用户开启"减弱动画效果"时：
- 用渐变替代滑动
- 避免快速自动播放内容
- 避免页面自动跳转

### 优先使用静态内容表示状态变化

---

## 听力无障碍

- 视频应有**隐藏式字幕（CC）**
- 音频内容应有**文字记录**
- 重要声音提示应有视觉替代

---

## 肢体无障碍

### Switch Control
用户用有限物理开关控制设备。

**设计要求：**
- 所有操作可通过简单切换完成
- 支持焦点导航（Tab 顺序合理）
- 避免时间限制的操作

---

## Dynamic Type 支持详情

### 字号范围（iOS）

| 名称 | 放大系数 | Body 实际字号 |
|------|---------|------------|
| xSmall | 0.75x | 12.75pt |
| Small | 0.85x | 14.45pt |
| Medium | 1.0x | 17pt（基准） |
| Large（默认） | 1.15x | 19.55pt |
| xLarge | 1.3x | 22.1pt |
| xxLarge | 1.5x | 25.5pt |
| xxxLarge | 1.75x | 29.75pt |
| Accessibility sizes | 最高 3.5x | 59.5pt |

### 大字号时的布局策略

1. **堆叠布局** — 文字在上，次要信息在下
2. **单列布局** — 多列在大字号时合并为单列
3. **图标同步放大** — SF Symbols 自动放大
4. **保持层级** — 主要元素始终在顶部

---

## 开发资源

| 框架 | API |
|------|-----|
| SwiftUI | `.accessibilityLabel()`, `.accessibilityHint()` |
| UIKit | `UIAccessibility` |
| iOS SDK | `traitCollection.preferredContentSizeCategory` |
| ARKit | 3D 场景中的 VoiceOver 支持 |

---

## 检查清单

- [ ] VoiceOver 能导航所有内容
- [ ] Dynamic Type 在所有尺寸下正常显示
- [ ] 颜色对比度达标
- [ ] 不依赖颜色传达关键信息
- [ ] 动画可被关闭（Reduce Motion）
- [ ] 触摸目标 ≥ 44×44pt
- [ ] 视频有字幕
