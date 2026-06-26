# Buttons

> 来源：Apple HIG - Buttons (2026)
> https://developer.apple.com/design/human-interface-guidelines/buttons

## 按钮类型

### 1. Filled Button（填充按钮）
- **Primary Button** — 品牌强调色背景，白色文字，用于主要操作
- 背景色清晰，视觉权重高
- 通常每屏只使用一个

### 2. Tinted Button（着色按钮）
- 次要强调色背景（低饱和度），文字用强调色
- 用于次要操作，视觉权重低于填充按钮

### 3. Gray Button（灰色按钮）
- 中性灰色背景
- 用于不重要的操作

### 4. Destructive Button（危险操作按钮）
- 红色背景或文字
- 用于删除、清除等不可逆操作

### 5. Borderless Button（无边框按钮）
- 仅文字，无背景
- 常用于 Navigation Bar 或 Toolbar 内
- 按下时有高亮背景

### 6. Link Button（链接按钮）
- 链接样式文字
- 用于内联次要操作

---

## 设计原则

### 尺寸与间距
- 按钮高度：iOS 标准为 **44pt**（触摸目标最小）
- 水平内边距：至少 16pt
- 按钮之间间距：至少 8pt
- 按钮内图标与文字间距：8pt

### 文字
- 使用动词或动词短语（"Save", "Delete", "Share"）
- 首字母大写（iOS 风格）或全大写（macOS）
- 避免超过 3 个词
- 不要用标题式大写

### 图标
- SF Symbols 是首选
- 图标与文字结合时，图标在左
- 确认图标清晰可辨

---

## 状态

| 状态 | 视觉表现 |
|------|---------|
| Default | 正常显示 |
| Pressed | 降低透明度或加深背景 |
| Disabled | 灰色文字，无交互响应 |
| Loading | 显示 spinner，文字变 disabled |

---

## 按钮变体风格

### iOS / iPadOS
- Filled → Tinted → Gray 递减强调
- destructive 用红色区分

### macOS
- Push button（默认）
- Secondary button（略微扁平）
- Bordered button（带边框）
- Borderless button（无边框，toolbar 内常用）

### visionOS
- 使用 **毛玻璃材质（Liquid Glass）**
- 支持背景色（彩色玻璃效果）
- 强调操作用渐变和深度效果

### watchOS
- 多用 Circular Button（圆形按钮）
- 支持侧边按钮（Digital Crown 辅助）

---

## Special Button Types

### Menu Button（下拉菜单按钮）
点击后显示 Menu（Action sheet / Dropdown）。
- 文字 + 下拉箭头
- macOS 的 Toolbar 和 View 内常用

### Segmented Control（分段控件）
一组互斥选项，属于同一操作的不同模式。
- 视觉上统一为一个控件
- 两端有圆角边框
- 选中项有填充背景

### Sheet（弹出面板）
不是按钮，但触发方式为按钮操作。

---

## Accessibility

- 保证按钮触摸目标 ≥ 44×44pt
- VoiceOver 播报按钮文字（如"Delete, button"）
- 必要时提供 `.accessibilityHint()`
- 确认所有状态（default/pressed/disabled）在 VoiceOver 下正常

---

## 代码示例

### SwiftUI

```swift
// 填充按钮（主要操作）
Button(action: {
    // 操作
}) {
    Text("保存")
        .font(.headline)
}
.buttonStyle(.borderedProminent)
.tint(.blue)  // 系统蓝

// 着色按钮（次要操作）
Button("取消", role: .cancel) { }
.buttonStyle(.bordered)

// 危险操作按钮
Button("删除", role: .destructive) {
    // 删除操作
}
.buttonStyle(.bordered)

// 无边框按钮（Toolbar 用）
Button(action: {}) {
    Image(systemName: "square.and.arrow.up")
}
.buttonStyle(.borderless)

// 链接样式
Button("了解更多") { }
.buttonStyle(.plain)

// 带图标
Button(action: {}) {
    Label("分享", systemImage: "square.and.arrow.up")
}
.buttonStyle(.borderedProminent)

// 禁用状态
Button("提交") { }
.disabled(true)  // 或 .buttonStyle(.borderedProminent).disabled(true)

// 加载状态
Button(action: {}) {
    HStack {
        ProgressView()
        Text("加载中...")
    }
}
.disabled(true)
```

### UIKit

```swift
import UIKit

// 系统按钮
let button = UIButton(type: .system)
button.setTitle("提交", for: .normal)
button.titleLabel?.font = .preferredFont(forTextStyle: .headline)
button.backgroundColor = .systemBlue  // #007AFF
button.setTitleColor(.white, for: .normal)
button.layer.cornerRadius = 10
button.contentEdgeInsets = UIEdgeInsets(top: 12, left: 20, bottom: 12, right: 20)

// 添加点击
button.addTarget(self, action: #selector(buttonTapped), for: .touchUpInside)

// 触摸目标 ≥ 44pt
button.frame = CGRect(x: 0, y: 0, width: 120, height: 44)

// 危险操作
let destructiveButton = UIButton(type: .system)
destructiveButton.setTitle("删除", for: .normal)
destructiveButton.setTitleColor(.systemRed, for: .normal)

// 禁用
button.isEnabled = false
button.alpha = 0.5
```

### 按钮尺寸规范

| 平台 | 最小高度 | 内边距 | 圆角 |
|------|---------|-------|------|
| iOS | 44pt | 16pt | 10pt |
| macOS | 22pt | 12pt | 4pt |
| tvOS | 56pt | 20pt | 8pt |
| watchOS | 44pt | 12pt | 22pt |
