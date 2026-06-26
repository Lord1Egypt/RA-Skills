---
name: apple-higDesign-skill
description: >
  Apple 平台设计系统技能。覆盖 Apple Human Interface Guidelines (HIG)，包括设计原则
  （Hierarchy/Harmony/Consistency）、Typography（San Francisco/Dynamic Type）、
  Color System（系统色/Liquid Glass）、SF Symbols（图标库/动画）、Components
  （Button/Navigation/Tab Bar/Alert/List/TextField/SearchBar/Toggle/DatePicker）、
  Accessibility、Dark Mode、Animation、空间布局（visionOS）、Branding。
  当用户提到 Apple 设计、iOS UI 规范、Apple HIG、iOS 设计语言、SF Symbols、
  Dark Mode 设计、visionOS 空间 UI 时触发。
trigger: Apple 设计|iOS UI|iOS 设计规范|Apple HIG|人机界面指南|SF Symbol|Dark Mode|visionOS 空间设计|苹果设计系统|San Francisco|Dynamic Type|苹果设计风格|Apple Design|Apple平台|macOS设计|watchOS|tvOS|苹果设计规范
tags:
  - apple
  - ios-design
  - ui-design
  - human-interface-guidelines
  - sf-symbols
  - dark-mode
  - accessibility
  - visionos
  - apple-platform
hermes:
  tags: [apple, ios-design, ui-design, human-interface-guidelines, sf-symbols, dark-mode, accessibility, visionos, apple-platform]
  related_skills: [ios-dev, harmonyos-dev, frontend-design]
  version: "3.0.0"
  last_updated: "2026-04-23"
  source: |
    https://developer.apple.com/design/human-interface-guidelines/
    https://developer.apple.com/design/human-interface-guidelines/typography
    https://developer.apple.com/design/human-interface-guidelines/color
    https://developer.apple.com/design/human-interface-guidelines/sf-symbols
    https://developer.apple.com/design/human-interface-guidelines/dark-mode
    https://developer.apple.com/design/human-interface-guidelines/accessibility
    https://developer.apple.com/design/human-interface-guidelines/components
license: MIT
---

# Apple Design System Skill

基于 Apple Human Interface Guidelines (2026)，覆盖所有 Apple 平台的设计规范。

# 设计原则

# 视觉基础

# 图标与品牌

# 组件设计规范

### 输入组件

### 容器组件

# 体验设计

---

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

### iOS 触摸目标
最小 **44×44pt**（Apple HIG 规定）

### 按钮样式优先级
Filled Button → Tinted Button → Gray Button → Borderless Button

### Dark Mode 背景色
`#1C1C1E`（不是纯黑 #000000）

### SF Symbols 渲染模式
Monochrome → Hierarchical → Palette → Multicolor

### 布局规范
| 元素 | 边距/间距 | 备注 |
|------|---------|------|
| 屏幕边缘 | 16pt | iOS 标准 |
| 组件间距 | 8pt | 8pt 网格 |
| 列表 Cell 高度 | 44pt | 触摸目标 |
| 导航栏高度 | 44pt | 标准 |
| TabBar 高度 | 49pt | iPhone |

---

## 避坑指南

### 常见错误

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ Dark Mode 用纯黑 `#000000` | ✅ 用 `#1C1C1E`（Apple HIG 规定） |
| ❌ macOS 使用 Dynamic Type | ✅ macOS 不支持，仅 iOS/iPadOS 支持 |
| ❌ 用红绿组合传达信息 | ✅ 用蓝色+图标辅助，色盲友好 |
| ❌ visionOS 使用 3D 文字 | ✅ 用 billboarding + 2D 文字 |
| ❌ 触摸目标小于 44×44pt | ✅ 最小 44×44pt |
| ❌ 超链接用绿/蓝色组合 | ✅ 用统一蓝色 `#007AFF` |
| ❌ SearchBar 不提供清除按钮 | ✅ 右滑显示 Clear 按钮 |
| ❌ Toggle 标签用 On/Off | ✅ 用描述性标签如"深色模式" |

### 版本陷阱

- ⚠️ **Liquid Glass** — 仅限 visionOS，iOS/macOS 不支持
- ⚠️ **SF Symbols 渐变** — 仅 SF Symbols 7+ 支持，低版本设备 fallback
- ⚠️ **SF Symbols 动画** — Variable Color 不适合表达深度感，应用 Hierarchical
- ⚠️ **Dynamic Type** — 大字号时布局可能截断，需测试所有尺寸

### 设计红线

- ❌ 不要硬编码系统颜色值（系统颜色值随版本浮动）
- ❌ 不要仅靠颜色传达信息（配合文字标签/图标）
- ❌ 不要忽略 Reduce Motion 设置（动画需考虑无障碍）
- ❌ 不要在 App Icon 用纯白背景（iOS 10+ 支持圆角裁切）

---

## 设计原则详解

### 3 大核心原则

#### 1. UIKit一致性（UIKit Consistency）
- 使用平台原生组件和行为
- 遵循系统交互模式
- 支持系统级无障碍和暗模式

#### 2. 清晰性（Clarity）
- 内容优先，信息层次分明
- 文字清晰可读，图标语义明确
- 动态字体支持（Dynamic Type）

#### 3. 深度（Depth）
- 利用视觉层次和真实动效传达关系
- 导航层级清晰
- 毛玻璃和阴影表达空间感

### 平台哲学差异

| 平台 | 主要模式 |
|------|---------|
| iOS | 多任务 + 手势导航 |
| macOS | 多窗口 + 菜单栏 |
| tvOS | 焦点驱动 + 远程 |
| watchOS | 表盘 + 复杂功能 |
| visionOS | 空间计算 + 手眼协作 |

---

## Typography 详解

### 字体家族

| 用途 | iOS/macOS | tvOS | watchOS |
|------|-----------|------|---------|
| 正文 | SF Pro | SF Pro | SF Pro |
| 标题 | SF Pro Display | SF Pro Display | SF Pro Rounded |
| 手写 | SF Pro Text | — | SF Pro Rounded |
| 等宽 | SF Mono | SF Mono | SF Mono |

### Dynamic Type 级别

| 级别 | 中文基准 | 英文基准 | 应用 |
|------|---------|---------|------|
| xSmall | 13pt | 13pt | 辅助文字 |
| Small | 15pt | 15pt | 次要信息 |
| Body | 17pt | 17pt | 正文 |
| Lead | 22pt | 20pt | 副标题 |
| Title | 28pt | 22pt | 标题 |
| xTitle | 34pt | 28pt | 大标题 |
| xxTitle | 40pt | 34pt | 超大标题 |

### 字号层级示例

```
主标题 (Title)  —————————  28pt Bold
副标题 (Headline)  —————  17pt Semibold
正文 (Body)  ———————————  17pt Regular
说明 (Caption)  ————————  12pt Regular
辅助 (Footnote)  ———————  13pt Regular
```

---

## Color System 详解

### 系统色彩语义

| 用途 | iOS | macOS |
|------|-----|-------|
| 主要文字 | label | labelColor |
| 次要文字 | secondaryLabel | secondaryLabelColor |
| 主色 | tints/tintColor | controlAccentColor |
| 背景 | systemBackground | windowBackgroundColor |
| 分组背景 | systemGroupedBackground | controlBackgroundColor |
| 强调色 | systemBlue (#007AFF) | systemBlue |

### P3 广色域
- 支持 25% 色彩空间扩展
- 设计资源用 sRGB 交付，广色域用 Display P3
- iPhone 7+ / iPad Pro / Mac 支持

---

## SF Symbols 详解

### 图标分类

| 类别 | 数量 | 示例 |
|------|------|------|
| UI 图标 | 150+ | chevron, plus, xmark |
| 多媒体 | 100+ | play, pause, speaker |
| 通信 | 80+ | message, phone, mail |
| 物体 | 200+ | book, car, house |
| 天气 | 50+ | sun, cloud, rain |

### 渲染模式

| 模式 | 效果 | 适用场景 |
|------|------|---------|
| Monochrome | 单一颜色 | 默认图标 |
| Hierarchical | 单色分层透明度 | visionOS 强调 |
| Palette | 最多 3 色 | 自定义主题 |
| Multicolor | 固有色 | 装饰性图标 |

### 常用图标速查

| 功能 | SF Symbol |
|------|-----------|
| 返回 | chevron.left |
| 关闭 | xmark |
| 菜单 | line.3.horizontal |
| 分享 | square.and.arrow.up |
| 收藏 | heart / heart.fill |
| 设置 | gear |
| 搜索 | magnifyingglass |
| 刷新 | arrow.clockwise |
| 删除 | trash |
| 编辑 | pencil |
| 添加 | plus |
| 相机 | camera |
| 照片 | photo |
| 地图 | map |
| 定位 | location |

---

## 组件详解

### Button 按钮

#### 样式优先级
1. **Filled** — 主要操作，强调色背景
2. **Tinted** — 次要操作，浅色背景+强调色文字
3. **Gray** — 第三操作，灰色背景
4. **Borderless** — 最低调，文字+图标

#### 设计要点
- 触摸目标最小 44×44pt
- 按钮内边距最小 12pt
- 同组按钮间距至少 8pt
- 危险操作用 destructive 样式

### Navigation 导航

#### iOS 导航模式
- **Navigation Bar** — 分层内容，push/pop
- **Tab Bar** — 扁平结构，切换视图
- **Toolbar** — 页面内操作
- **Segmented Control** — 同级切换

#### 规范
- Tab Bar 最多 5 个
- Navigation Bar 显示当前层级标题
- 返回按钮始终可见
- Sheet 支持 .medium / .large detents

### Lists 列表

#### 单元格结构
```
┌─────────────────────────────────┐
│  Leading    Title    Trailing   │
│  Icon    Primary   Secondary  Image │
│         Subtitle                 │
└─────────────────────────────────┘
```

#### 交互
- Swipe Actions — 左滑/右滑快捷操作
- Drag & Drop — 拖拽排序
- 附件指示器 — disclosure chevron

### Alerts 弹窗

#### 类型
| 类型 | 样式 | 用途 |
|------|------|------|
| Alert | 模态 | 重要信息/确认 |
| Action Sheet | 底部弹出 | 多选项 |
| Toast | 自动消失 | 轻量反馈 |
| Dialog | macOS | 确认/输入 |

---

## Accessibility 无障碍

### 核心要求

| 类型 | 要求 |
|------|------|
| VoiceOver | 所有元素可朗读 |
| Dynamic Type | 支持所有字体级别 |
| 对比度 | 文字 4.5:1 / 大字 3:1 |
| 触摸目标 | 最小 44×44pt |
| Reduce Motion | 尊重系统设置 |

### 实现检查清单
- [ ] 所有图片有 alt 文字
- [ ] 颜色不是唯一信息载体
- [ ] 手势有替代方案
- [ ] 音频有字幕/文字记录
- [ ] 支持 Switch Control

---

## 平台差异化设计

### iOS

#### 核心特征
- 手势驱动：Swipe Back、Pull to Refresh、3D Touch/Haptic Touch
- 独立 App 沙箱
- 通知系统：Banner、Alert、Lock Screen
- 小组件：Home Screen Widgets
- 多任务：App Switcher、Slide Over、Split View（iPad）

#### 设计要点
- 底部 Tab Bar 导航（≤5 个 Tab）
- Navigation Bar 返回上一页
- Modal Sheet 从底部滑出
- 触摸目标 ≥ 44×44pt
- Safe Area 适配（刘海、Home Indicator）

#### iOS 特有组件
- `UINavigationController` — 分层导航
- `UITabBarController` — 底部切换
- `UITableView` / `UICollectionView` — 列表/网格
- `UISegmentedControl` — 分段选择
- `UISwitch` — 开关控制
- `UIAlertController` — 警告框

### iPad

#### 核心特征
- Split View：分屏多任务
- Slide Over：悬浮面板
- 多窗口：多实例 App
- 键盘/触控板支持
- 外接显示器支持

#### 设计要点
- 侧边栏导航（Sidebar）
- Toolbar 用于页面操作
- Popover 用于上下文选项
- 拖拽跨 App 传输数据
- 支持拖拽调整大小的窗口

### macOS

#### 核心特征
- 窗口管理：最小化/最大化/关闭
- 菜单栏：App 菜单、系统菜单
- Dock：应用启动器
- 多窗口并发
- 键盘快捷键优先

#### 设计要点
- **不支持 Dynamic Type** — 仅 iOS/iPadOS 支持
- 使用原生窗口样式
- 支持拖拽调整大小
- 菜单项 Keyboard Shortcut
- Touch Bar 支持（MacBook Pro）

### tvOS

#### 核心特征
- 焦点驱动（Focus Engine）
- 远程控制/ Siri Remote
- 10-foot UI（远距离观看，屏幕距离用户 3 米）
- 屏幕大，文字需更大字号

#### 10-Foot UI 设计规范

**设计原则**

| 原则 | 说明 |
|------|------|
| 简洁性 | 一屏只做一件事 |
| 层级清晰 | 信息优先级分明 |
| 颜色鲜明 | 对比度足够 |
| 字体足够大 | 远距离可读 |

**字号层级**

| 用途 | 字号 | 说明 |
|------|------|------|
| 大标题 | 54pt | 屏幕标题 |
| 标题 | 38pt | 分类标题 |
| 副标题 | 29pt | 列表项标题 |
| 正文 | 24pt | 描述文字 |
| Caption | 19pt | 辅助说明 |

#### Focus Engine 焦点引擎

tvOS 独有的交互模型：用户用 Siri Remote 选择元素，焦点自动跟随。

**焦点状态**

| 状态 | 视觉变化 |
|------|---------|
| Unfocused | 正常大小，100% 透明度 |
| Focused | 放大 1.1x，阴影加深，透明度 100% |
| Highlighted | 按下时的反馈色 |

**焦点导航规则**
- 自动识别相邻元素
- 焦点按最近距离或阅读顺序跳转
- 水平/垂直网格自动推断

#### 布局规范

| 规范 | 值 |
|------|---|
| 屏幕分辨率 | 1920×1080 / 3840×2160 |
| 安全区域 | 上下左右各 90pt |
| 水平边距 | 96pt |
| 列表项高度 | 120pt |
| Tab Bar 高度 | 96pt |

#### 深度与阴影

焦点元素通过阴影表达深度：

```swift
// 焦点元素阴影
Text("Focused Item")
    .shadow(color: .black.opacity(0.5), radius: 20, x: 0, y: 10)

// 未聚焦元素阴影
Text("Unfocused Item")
    .shadow(color: .black.opacity(0.3), radius: 8, x: 0, y: 4)
```

#### 组件层级

| 组件 | tvOS 控件 | 说明 |
|------|-----------|------|
| 导航 | TabBar | 底部标签切换 |
| 列表 | List | 水平滚动 Banner/Collection |
| 详情 | Detail | 大图+描述+操作 |
| 菜单 | Menu | 弹出操作菜单 |

#### SwiftUI for tvOS

```swift
import SwiftUI
import TVUIKit

struct ContentView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem { Label("首页", systemImage: "house") }
            SearchView()
                .tabItem { Label("搜索", systemImage: "magnifyingglass") }
        }
    }
}

// 焦点状态
struct FocusableCard: View {
    @State private var isFocused = false

    var body: some View {
        VStack {
            Image("poster")
                .resizable()
                .aspectRatio(16/9, contentMode: .fit)
            Text("Title")
                .font(.title2)
        }
        .scaleEffect(isFocused ? 1.1 : 1.0)
        .animation(.easeInOut(duration: 0.2), value: isFocused)
        .focusable()
        .onFocusChange { focused in
            isFocused = focused
        }
    }
}
```

#### UIKit for tvOS

```swift
import UIKit
import TVUIKit

class CatalogViewController: UIViewController {
    private var collectionView: UICollectionView!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupCollectionView()
    }

    private func setupCollectionView() {
        let layout = UICollectionViewFlowLayout()
        layout.scrollDirection = .horizontal
        layout.itemSize = CGSize(width: 400, height: 225)
        layout.minimumLineSpacing = 40

        collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
        collectionView.delegate = self
        collectionView.dataSource = self
        collectionView.register(CatalogCell.self, forCellWithReuseIdentifier: "Cell")

        // 焦点行为
        collectionView.remembersFocused = true
    }
}

// UICollectionViewDelegateFocus
extension CatalogViewController: UICollectionViewDelegateFocus {
    func collectionView(_ collectionView: UICollectionView, didUpdateFocusIn context: UICollectionViewFocusUpdateContext, with coordinator: UIFocusAnimationCoordinator) {
        if let indexPath = context.nextFocusedIndexPath {
            coordinator.addCoordinatedAnimations {
                // 焦点动画
            }
        }
    }
}
```

#### 避坑指南

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 小字体 | ✅ 最小 19pt Caption |
| ❌ 密集布局 | ✅ 每屏一个主题 |
| ❌ 触摸交互 | ✅ 远程/语音/手势 |
| ❌ Hover 效果 | ✅ 焦点自动跟随 |
| ❌ 复杂导航 | ✅ 最多两层深度 |
| ❌ 窄边框 | ✅ 安全区域各 90pt |

### watchOS

#### 核心特征
- 腕上设备，屏幕极小（40-45mm Series 10）
- Digital Crown 滚动导航
- Haptic 反馈（Tap、Click、Ritual）
- 续航优先，Always-On 显示

#### 设计原则

**1. 简洁性（Reduce）**
- 每次只展示一个核心功能
- 避免长列表和复杂表单
- 单列式布局，信息垂直滚动

**2. 上下文感知（Context）**
- 基于时间和位置主动呈现信息
- Glanceable：一瞥即知
- Long-Look：通知展开显示详情

**3. 实时性（Timely）**
- 实时数据更新（心率、步数）
- 快捷操作（回复、支付）

#### Apple Watch HIG 核心规范

| 规范 | 要求 |
|------|------|
| 屏幕尺寸 | 40mm/44mm/45mm/46mm |
| 基准字号 | 14pt（Body） |
| 最小字号 | 10pt（Caption） |
| 触控目标 | 最小 44×44pt |
| 边距 | 12pt（水平） |
| Corner Radius | 约 36pt（贴合屏幕） |

#### 布局模式

```
┌─────────────────────────┐
│        Status Bar        │  18pt
├─────────────────────────┤
│                         │
│       通知内容            │  主区域
│       (Long-Look)        │
│                         │
├─────────────────────────┤
│       Quick Actions      │  56pt
└─────────────────────────┘
```

#### 颜色系统

| 类型 | 色值 | 用途 |
|------|------|------|
| 强调色 | #FF9500 | 主要操作 |
| 成功色 | #34C759 | 健康数据 |
| 警告色 | #FF3B30 | 警报 |
| 背景 | #000000 | 表盘背景 |

#### 组件层级

| 组件 | 说明 |
|------|------|
| WatchFace | 表盘（Modular/Analog/...） |
| WatchWindow | 全屏窗口 |
| Alert | 通知展开视图 |
| Menu | 快捷操作菜单 |
| Picker | 滚轮选择器 |

#### 交互模式

| 模式 | 操作 | 反馈 |
|------|------|------|
| Tap | 点击按钮 | Haptic Click |
| Swipe | 上下滑动 | Haptic Scroll |
| Long Press | 长按编辑 | Haptic Tap |
| Digital Crown | 旋转滚动 | Haptic Tick |
| Side Button | 侧边按钮 | Haptic Impact |

#### SwiftUI for watchOS

```swift
// 基础页面
struct ContentView: View {
    var body: some View {
        VStack {
            Text("心率")
                .font(.caption)
            Text("72")
                .font(.largeTitle)
                .foregroundColor(.green)
        }
    }
}

// 列表导航
struct ListView: View {
    var body: some View {
        List {
            ForEach(items) { item in
                NavigationLink(destination: DetailView(item: item)) {
                    Text(item.name)
                }
            }
        }
    }
}

// Picker 滚轮
Picker("选择", selection: $selected) {
    Text("选项1").tag(0)
    Text("选项2").tag(1)
}
.pickerStyle(.wheel)
```

#### UIKit for watchOS

```swift
import WatchKit

class InterfaceController: WKInterfaceController {
    @IBOutlet weak var label: WKInterfaceLabel!

    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        label.setText("Hello Apple Watch")
    }

    @IBAction func buttonTapped() {
        WKInterfaceDevice.current().play(.click)
    }
}
```

#### 避坑指南

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 多列布局 | ✅ 单列垂直滚动 |
| ❌ 长文本列表 | ✅ 精简内容，异步加载 |
| ❌ 复杂手势 | ✅ 点击+滚轮即可 |
| ❌ 忽略续航 | ✅ 减少后台刷新 |
| ❌ 与手机相同布局 | ✅ 专为小屏重设计 |

### visionOS

#### 核心特征
- 空间计算（Spatial Computing）
- Eye + Hand 交互
- 3D 窗口/场景
- 沉浸式体验

#### 设计规范
- **不支持 Dark Mode** — 使用 Liquid Glass
- Liquid Glass 材质（毛玻璃 + 透明度）
- Billboarding：2D 文字始终面向用户
- 深度层级：场景中的 Z 轴位置
- 焦点：眼睛注视 + 手势确认

#### 布局模式
- **Windows** — 可拖动/调整的窗口
- **Volumes** — 3D 容器
- **Spaces** — 完全沉浸空间
- **Mixed Reality** — 虚实结合

---

## Animation 动效设计

### 核心原则
1. **反馈** — 操作即时响应
2. **连续性** — 状态平滑过渡
3. **导航** — 引导用户理解层级
4. **一致性** — 同类操作使用相同动效

### 动画类型

| 类型 | 用途 | 时长 | 曲线 |
|------|------|------|------|
| 系统动画 | UI 状态变化 | 250-400ms | easeInOut |
| 导航动画 | 页面切换 | 350-500ms | spring |
| 手势动画 | 拖拽/缩放 | 实时 | 直接 |
| 载入动画 | 等待反馈 | 循环 | linear |

### SwiftUI 动画

```swift
// 隐式动画
withAnimation(.easeInOut(duration: 0.3)) {
    isExpanded.toggle()
}

// 显式动画
Button("点击") {
    withSpring {
        offset.y -= 10
    }
}

// 过渡动画
Text("Hello")
    .transition(.opacity.combined(with: .scale))
```

### UIKit 动画

```swift
// UIView.animate
UIView.animate(withDuration: 0.3, delay: 0, options: .curveEaseInOut) {
    view.transform = CGAffineTransform(scaleX: 1.1, y: 1.1)
}

// UIViewPropertyAnimator
let animator = UIViewPropertyAnimator(duration: 0.3, curve: .easeInOut) {
    view.center = newCenter
}
animator.startAnimation()
```

### 无障碍动画
- 检测 `UIAccessibility.isReduceMotionEnabled`
- 减少或禁用动画
- 提供静态替代

---

## Spatial Layout 空间布局

### 布局基础

#### 8pt 网格系统
- 所有间距是 8 的倍数
- 组件间距：8pt / 16pt / 24pt / 32pt
- 屏幕边距：16pt（iPhone）/ 20pt（iPad）

#### 间距层级

| 用途 | 间距 |
|------|------|
| 紧凑 | 4pt |
| 标准 | 8pt |
| 中等 | 16pt |
| 宽松 | 24pt |
| 超宽 | 32pt+ |

### iOS 布局规范

#### 安全区域
- 顶部：Dynamic Island / 刘海
- 底部：Home Indicator
- 左右：屏幕圆角

### visionOS 空间布局

#### 窗口尺寸
- 最小宽度：320pt
- 默认高度：600pt
- 圆角：44pt

#### 深度层级
- Near：Z = 0（主窗口）
- Mid：Z = -200（背景元素）
- Far：Z = -500（装饰元素）

---

## 品牌与图标

### App Icon

#### 尺寸要求
| 平台 | 尺寸 | 备注 |
|------|------|------|
| iPhone | 180×180 (@3x) | 60×60 (@1x) |
| iPad | 167×167 (@2x) | 83.5×83.5 (@1x) |
| App Store | 1024×1024 | 唯一尺寸 |

#### 设计规范
- 圆角：iOS 自动裁切
- 背景：避免纯白（iOS 10+ 圆角裁切）
- 内容居中，四周留白
- 测试在不同背景上的显示

### Apple 品牌规范

#### 可用
- Apple Logo（SF Symbol: `apple.logo`）
- 产品名称拼写正确（iPhone、iPad、Mac）

#### 禁止
- Apple 彩虹 logo 变体
- 产品名称翻译
- 模仿 Apple 字体

---

## 输出格式规范

当使用本技能回答用户问题时，遵循以下格式：

### 回复结构
1. **直接回答** — 一段简洁的话给出核心答案
2. **规范引用** — 补充 HIG 相关条款（如适用）
3. **设计建议** — 组件选用、视觉规范（如需）
4. **避坑提醒** — 常见错误+正确做法

### 示例回复（按钮设计）

> iOS 按钮首选 Filled 样式，背景用 `#007AFF`，文字白色，高度至少 44pt。若要次要操作，用 Tinted 按钮。macOS 避免 Dynamic Type，visionOS 用 Liquid Glass 材质。注意按钮之间至少留 8pt 间距。

### 禁用格式
- ❌ 不要显式分层（避免"第一层/第二层/框架分析"等字眼）
- ❌ 不要长篇引用原文，要内化为自己的话
- ❌ 不要包含代码实现（那是 ios-dev 技能的职责）
- ✅ 输出应是一段干净的话

---

## 来源

> 来源：Apple Human Interface Guidelines（2026-04-23 访问）
> - 主页：https://developer.apple.com/design/human-interface-guidelines/
> - Typography：https://developer.apple.com/design/human-interface-guidelines/typography
> - Color：https://developer.apple.com/design/human-interface-guidelines/color
> - SF Symbols：https://developer.apple.com/design/human-interface-guidelines/sf-symbols
> - Components：https://developer.apple.com/design/human-interface-guidelines/components
> - Accessibility：https://developer.apple.com/design/human-interface-guidelines/accessibility
>
> 更新频率：随系统版本迭代（当前基于 2026）
