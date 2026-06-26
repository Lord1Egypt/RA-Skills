# Color System

> 来源：Apple HIG - Color (2026)
> https://developer.apple.com/design/human-interface-guidelines/color

## 设计原则

- **避免用同一颜色表达不同含义** — 颜色含义要全局一致
- **为所有 appearance 模式测试** — light / dark / increased contrast
- **测试不同光照环境** — 户外阳光 vs 室内暗光下颜色表现不同
- **不要硬编码系统颜色值** — 系统颜色值会随版本浮动

## 系统颜色（Dynamic Colors）

### iOS/iPadOS 背景色

两组动态背景色：`system` 和 `system grouped`：

| 层级 | system | system grouped | 用途 |
|------|--------|--------------|------|
| Primary | systemBackground | systemGroupedBackground | 主视图背景 |
| Secondary | secondarySystemBackground | secondarySystemGroupedBackground | 分组内内容 |
| Tertiary | tertiarySystemBackground | tertiarySystemGroupedBackground | 更深层分组 |

### iOS/iPadOS 前景色（Label Colors）

| 用途 | SwiftUI | UIKit |
|------|---------|-------|
| 主要内容标签 | `.label` | `UIColor.label` |
| 次要内容标签 | `.secondary` | `UIColor.secondaryLabel` |
| 第三级内容标签 | `.tertiary` | `UIColor.tertiaryLabel` |
| 第四级内容标签 | `.quaternary` | `UIColor.quaternaryLabel` |
| 占位符文字 | `.placeholder` | `UIColor.placeholderText` |
| 分割线 | `.separator` | `UIColor.separator` |
| 不透明分割线 | `.opaqueSeparator` | `UIColor.opaqueSeparator` |
| 链接 | `.link` | `UIColor.link` |

### macOS 系统颜色

| 用途 | AppKit API |
|------|-----------|
| 选中控件上的文字 | `alternateSelectedControlTextColor` |
| 交替行背景 | `alternatingContentBackgroundColors` |
| 控件强调色 | `controlAccentColor` |
| 控件背景 | `controlBackgroundColor` |
| 控件表面 | `controlColor` |
| 可用控件文字 | `controlTextColor` |
| 不可用控件文字 | `disabledControlTextColor` |
| 查找高亮 | `findHighlightColor` |

### 语义颜色（Semantic Colors）

| 颜色 | 含义 |
|------|------|
| Blue `#007AFF` | 链接、操作、交互元素 |
| Green `#34C759` | 成功、正向趋势（中文语境可能相反） |
| Red `#FF3B30` | 错误、危险、删除、负向趋势 |
| Orange `#FF9500` | 警告、注意 |
| Yellow `#FFCC00` | 强调、提示 |
| Purple `#AF52DE` | 特殊功能、创意内容 |
| Pink `#FF2D55` | 促销、热情 |
| Teal `#5AC8FA` | 信息、辅助 |
| Gray `#8E8E93` | 次要、禁用状态 |

---

## Dark Mode

### 概述
Dark Mode 让用户在弱光环境下更舒适地使用设备，同时节省 OLED 屏幕电量。

支持的平台：iOS 13+ / iPadOS 13+ / macOS 10.14+ / tvOS 13+ / watchOS 6+

### 核心原则
- 系统颜色自动适配 light/dark
- 自定义颜色需要提供 light 和 dark 两个变体
- 增加对比度模式下，颜色差异更明显
- **不要用纯黑或纯白** — 用系统提供的背景色

### 设计要求
1. **文字与背景对比度** — 确保 4.5:1（普通文字）或 3:1（大字）对比度
2. **不要用纯黑或纯白** — 用系统提供的背景色（如 `#1C1C1E` 而非 `#000000`）
3. **毛玻璃效果** — iOS 的 blur/material 自动适配深色模式

### Dark Mode 色彩规范

#### 文字颜色层级

| 用途 | Light | Dark |
|------|-------|------|
| 主要文字 | #000000 (87%) | #FFFFFF (100%) |
| 次要文字 | #000000 (60%) | #FFFFFF (60%) |
| 第三文字 | #000000 (30%) | #FFFFFF (30%) |
| 占位符 | #000000 (10%) | #FFFFFF (10%) |

#### 背景层级

| 用途 | Light | Dark |
|------|-------|------|
| 主背景 | #FFFFFF | #1C1C1E |
| 分组背景 | #F2F2F7 | #000000 |
| 次背景 | #FFFFFF | #2C2C2E |
| 卡片 | #FFFFFF | #3A3A3C |

### 毛玻璃（Vibrancy / Blur）

Dark Mode 下毛玻璃效果更丰富：

| 样式 | Light | Dark |
|------|-------|------|
| `.systemMaterial` | 白色 70% | 黑色 60% + blur |
| `.systemUltraThinMaterial` | 极淡白色 | 极淡黑色 |
| `.systemChromeMaterial` | 不透明 | 极淡灰色 |

### 平台注意事项

| 平台 | 注意事项 |
|------|---------|
| iOS/iPadOS | UISwitch 的 onTint 自动适配，Navigation/Tab Bar 自动毛玻璃 |
| macOS | 支持自动跟随系统 appearance，Menu Bar 自动变深色 |
| tvOS | 主要深色界面 + 浅色文字，焦点指示器更明显 |
| watchOS | Always-On 显示屏需考虑深色省电 |
| visionOS | 不支持 Dark Mode，使用 Liquid Glass 材质 |

### 品牌色与 Dark Mode
- 保持品牌主色在 Dark Mode 下可用
- 测试品牌色在不同背景上的对比度
- 考虑降低饱和度或亮度以适应深色环境

---

## Liquid Glass（visionOS）

visionOS 的标志性材质效果：
- 默认透明，透出后方内容颜色
- 可对背景施加颜色（类似彩色玻璃）
- 可对文字/图标施加颜色

**使用原则：**
- 背景优先 — 强调主操作时对背景着色，而非文字
- 谨慎使用 — 颜色应保留给真正需要强调的元素
- 大元素（Sidebar）更不透明，小元素更透明

---

## 宽色域（Wide Color）

- 支持 P3 色域，比 sRGB 更丰富
- 照片、视频、游戏视觉更真实
- 使用 Display P3 色彩描述文件，16 bits/pixel，导出 PNG 格式
- 需要用 P3 显示器来设计和选择颜色

### 颜色管理
- **Color Space** = 色域（如 sRGB、Display P3）
- **Color Profile** = 描述颜色如何映射到数值
- 图片必须嵌入颜色配置文件才能正确显示

---

## 无障碍色彩

- **不要仅靠颜色传达信息** — 配合文字标签、形状、图标
- **检查对比度** — 文字与背景至少 4.5:1
- **色盲友好** — 避免红绿组合（考虑用蓝色+图标）
- **文化差异** — 红色在西方是危险，在中国是正向

---

## 平台考虑

| 平台 | 强调色 |
|------|--------|
| iOS/iPadOS | `UIUserInterfaceStyle` 自动适配 |
| macOS | 用户在系统设置中选择 accent color |
| tvOS | 支持自动深色/浅色切换 |
| visionOS | 强调色融入毛玻璃材质 |
| watchOS | 支持多种外观（多个表盘主题） |

---

## 代码示例

### SwiftUI

```swift
import SwiftUI

// 系统颜色（自动适配 Dark Mode）
Text("Hello")
    .foregroundColor(.label)      // 主文字
    .foregroundColor(.secondary)  // 次要文字

// 语义颜色
Color.blue          // #007AFF
Color.green         // #34C759
Color.red           // #FF3B30
Color.orange        // #FF9500

// 强调色
Label("Settings", systemImage: "gear")
    .tint(.blue)  // 全局强调色

// 自定义颜色（需适配 Dark Mode）
extension Color {
    static let brandBlue = Color("BrandBlue")  // Asset Catalog 中的颜色集
}

// 使用 Color Set 适配 Dark Mode
// 在 Assets.xcassets 创建 "BrandBlue" 颜色集
// 添加 Light 和 Dark 两个变体

// 背景色
ZStack {
    Color.systemBackground      // 自动适配
    Color.systemGroupedBackground
}
```

### UIKit

```swift
import UIKit

// 系统颜色（自动适配 Dark Mode）
label.textColor = .label
label.textColor = .secondaryLabel

// 语义颜色
view.backgroundColor = .systemBackground
view.backgroundColor = .secondarySystemBackground

// 强调色
button.tintColor = .systemBlue  // #007AFF

// 危险色
destructiveButton.tintColor = .systemRed  // #FF3B30

// 创建适配 Dark Mode 的颜色
let brandColor = UIColor { traits in
    traits.userInterfaceStyle == .dark
        ? UIColor(red: 0.2, green: 0.6, blue: 1.0, alpha: 1.0)  // 深色
        : UIColor(red: 0.0, green: 0.48, blue: 1.0, alpha: 1.0)  // 浅色
}

// 从 Asset Catalog 加载颜色
let customColor = UIColor(named: "BrandBlue")

// Hex 转 UIColor
extension UIColor {
    convenience init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let r, g, b, a = UInt64.extract(hex: int)
        self.init(red: CGFloat(r) / 255, green: CGFloat(g) / 255, blue: CGFloat(b) / 255, alpha: CGFloat(a) / 255)
    }
}
```

### 对比度检查

| 文字色 | 背景色 | 对比度 | 适用场景 |
|--------|--------|--------|---------|
| #000000 | #FFFFFF | 21:1 | 标题/正文 |
| #333333 | #FFFFFF | 12.6:1 | 正文 |
| #666666 | #FFFFFF | 5.7:1 | 辅助文字（最小4.5:1） |
| #FFFFFF | #000000 | 21:1 | 深色模式 |
| #AAAAAA | #000000 | 4.5:1 | 深色模式辅助文字 |

> ⚠️ Apple HIG 要求普通文字至少 4.5:1，大字（18pt+ 或 14pt bold+）至少 3:1
