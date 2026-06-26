# SwiftUI 映射：Figma → SwiftUI

> 作用：把 Figma 属性映射到 SwiftUI。  
> 含基础映射与 **线上项目** 中常见的页面级写法。

## 布局选型

| Figma 结构 | 推荐视图 |
|---|---|
| 纵向堆叠 | `VStack` |
| 横向堆叠 | `HStack` |
| 重叠 / Z 序 | `ZStack` |
| 重复相似项（≥3） | `List` / `LazyVStack` / `LazyHStack` |
| 带导航栏页面 | `NavigationStack` + `.navigationTitle` |
| 可滚动内容 | `ScrollView` |

## 自动布局映射

| Figma 属性 | SwiftUI 对应 |
|---|---|
| layoutMode: VERTICAL | `VStack` |
| layoutMode: HORIZONTAL | `HStack` |
| itemSpacing | `spacing:` 参数 |
| padding* | `.padding()` |
| primaryAxisAlignItems: CENTER | `alignment` + `Spacer()` |
| counterAxisAlignItems: CENTER | `alignment: .center` |
| layoutGrow: 1 | `.frame(maxWidth: .infinity)` 或 `Spacer()` |
| primaryAxisSizingMode: FIXED | `.frame(height/width:)` |

## 尺寸换算

- Figma px → SwiftUI pt（约 1:1）
- 字号：`.system(size:)` 用 pt

## 页面级架构

以下贴近线上 iOS **真实结构**。生成时要有 **页面级** 意识。

### 多 Tab 页
设计出现 **多个 Tab**（≥2 个文案作导航）时：

- 顶部可滑动：`TabView` + `.tabViewStyle(.page)`，或自定义 `Picker`/分段控件
- 底部 Tab：系统 `TabView` 默认样式
- **不要**用纯 `Text` 当 Tab —— 无选中态与指示器
- 每个 Tab 内容拆成独立 `View`
- 输出：主视图（Tab 容器）+ 各内容视图

```swift
// 顶部自定义下划线 Tab（示例）
struct ContentView: View {
    @State private var selectedTab = 0
    let tabs = ["关注", "推荐", "热榜"]

    var body: some View {
        VStack(spacing: 0) {
            HStack(spacing: 24) {
                ForEach(tabs.indices, id: \.self) { index in
                    VStack(spacing: 4) {
                        Text(tabs[index])
                            .font(.system(size: 16, weight: selectedTab == index ? .bold : .regular))
                            .foregroundColor(selectedTab == index ? Color(hex: "0F0F0F") : Color(hex: "858A99"))
                        Rectangle()
                            .fill(selectedTab == index ? Color(hex: "0F0F0F") : .clear)
                            .frame(height: 2)
                    }
                    .onTapGesture { selectedTab = index }
                }
            }
            .padding(.horizontal, 20)

            TabView(selection: $selectedTab) {
                FollowingView().tag(0)
                RecommendView().tag(1)
                HotListView().tag(2)
            }
            .tabViewStyle(.page(indexDisplayMode: .never))
        }
    }
}
```

### 导航栏 — 视为整体
导航栏是 **一个逻辑容器**。标准用 `NavigationStack` + `.toolbar`；自定义导航栏用单行 `HStack`，主内容放在其下并留好间距。

```swift
// 自定义导航栏
HStack {
    Button(action: { dismiss() }) {
        Image(systemName: "chevron.left")
            .frame(width: 32, height: 32)
            .background(Circle().fill(Color(hex: "000000")))
            .foregroundColor(.white)
    }
    Spacer()
    Text("设置")
        .font(.system(size: 17, weight: .bold))
    Spacer()
    Color.clear.frame(width: 32, height: 32) // 平衡占位
}
.padding(.horizontal, 20)
```

### 导航栏按钮
- 返回/关闭：`Button` + `Image`；圆底用 `.background(Circle()...)`
- 简单图标 **不要**再套多余容器

### 图标 + 文字按钮
优先 `Button` 内 `HStack { Image + Text }`；`Label` 亦可控性稍弱。

```swift
// 描边按钮 + 图标
Button(action: {}) {
    HStack(spacing: 6) {
        Image("ic_video")
            .resizable()
            .frame(width: 20, height: 20)
        Text("查看视频")
            .font(.system(size: 15, weight: .bold))
            .foregroundColor(Color(hex: "0F0F0F"))
    }
    .frame(maxWidth: .infinity)
    .frame(height: 40)
    .background(
        RoundedRectangle(cornerRadius: 12)
            .stroke(Color(hex: "DCDCDC"), lineWidth: 1)
    )
}

// 实心主按钮
Button(action: {}) {
    Text("查看报告")
        .font(.system(size: 15, weight: .bold))
        .foregroundColor(.white)
        .frame(maxWidth: .infinity)
        .frame(height: 40)
        .background(RoundedRectangle(cornerRadius: 12).fill(Color(hex: "0158FF")))
}
```

### 开关
- 标准用 `Toggle`；自定义用 `.toggleStyle`
- 着色：`.tint(Color(...))`（iOS 15+）

```swift
Toggle("通知", isOn: $isEnabled)
    .tint(Color(hex: "0158FF"))
```

### 输入框 vs 纯展示
Figma 无法区分输入与展示。

- 占位风格 + 输入态 → `TextField`
- 静态展示 → `Text`
- **不确定时问用户**

```swift
TextField("请输入昵称", text: $nickname)
    .font(.system(size: 15))
    .foregroundColor(Color(hex: "0F0F0F"))
    .padding(.horizontal, 12)
    .frame(width: 295, height: 48)
    .background(
        RoundedRectangle(cornerRadius: 8)
            .stroke(Color(hex: "E5E5E5"), lineWidth: 1)
    )
```

## 宽度策略：固定 vs 弹性

Figma 多为固定画布（375/390）。宽度是 **计算结果**，需推断意图。

核心问题：宽度是 **固定** 还是 **填满剩余**？

### 规则 1：单元素撑满宽
宽 + 左右边距 ≈ 屏宽 → `.frame(maxWidth: .infinity)` + `.padding(.horizontal, X)`

```swift
Text("标题")
    .frame(maxWidth: .infinity, alignment: .leading)
    .padding(.horizontal, 20)
```

### 规则 2：并排时识别「弹性」方
- **固定**：头像、图标、按钮等，用明确 `.frame(width:)`
- **弹性**：正文区用 `Spacer()` 或让布局自然扩展

```swift
// 固定头像 + 弹性文字
HStack(spacing: 16) {
    Image("avatar")
        .resizable()
        .frame(width: 56, height: 56)
        .clipShape(Circle())
    VStack(alignment: .leading, spacing: 4) {
        Text("用户名").font(.system(size: 16, weight: .bold))
        Text("描述文字").font(.system(size: 14)).foregroundColor(.gray)
    }
    Spacer()
}
.padding(.horizontal, 20)
```

### 规则 3：固定宽 + 居中
明显窄于屏且居中 → 显式 `.frame(width:)` + 父级居中

```swift
TextField("请输入昵称", text: $nickname)
    .frame(width: 295, height: 48)
```

### 列表项宽度
- Item 用 `.frame(maxWidth: .infinity)`；`List`/`LazyVStack` 控制整体宽度

## 多状态视图

同一视图有多套外观（选中/未选、可用/禁用）时：

### 选中 / 未选中
用条件修饰符驱动状态：

```swift
struct GenderCard: View {
    let title: String
    let icon: String
    let isSelected: Bool

    var body: some View {
        VStack(spacing: 8) {
            Image(icon)
                .resizable()
                .frame(width: 48, height: 48)
            Text(title)
                .font(.system(size: 15, weight: .medium))
        }
        .frame(width: 140, height: 120)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(isSelected ? Color(hex: "E8F0FF") : Color(hex: "F5F5F5"))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(isSelected ? Color(hex: "0158FF") : .clear, lineWidth: 2)
        )
    }
}
```

### 禁用 / 可用（透明度）
`.opacity()` + `.disabled()`，不要为每状态各做一个 View。

```swift
Button(action: { submit() }) {
    Text("提交")
        .frame(maxWidth: .infinity)
        .frame(height: 48)
        .background(RoundedRectangle(cornerRadius: 12).fill(Color(hex: "0158FF")))
        .foregroundColor(.white)
}
.opacity(isValid ? 1.0 : 0.3)
.disabled(!isValid)
```

### 叠放卡片
结构相似、位置偏移的叠卡 → 可能是切卡交互。**不要**只生成静态多层 `View`。  
应问用户交互方式；可选 `TabView(.page)`、`DragGesture` 或第三方栈。

## 视觉属性

### Color hex 扩展（生成代码中可含一次）

```swift
extension Color {
    init(hex: String) {
        let scanner = Scanner(string: hex)
        var rgb: UInt64 = 0
        scanner.scanHexInt64(&rgb)
        self.init(
            red: Double((rgb >> 16) & 0xFF) / 255.0,
            green: Double((rgb >> 8) & 0xFF) / 255.0,
            blue: Double(rgb & 0xFF) / 255.0
        )
    }
}
```

### 阴影

```swift
.shadow(color: Color(hex: "000000").opacity(0.1), radius: 4, x: 0, y: 2)
```

### 渐变

```swift
LinearGradient(
    colors: [Color(hex: "FF6B6B"), Color(hex: "4ECDC4")],
    startPoint: .top,
    endPoint: .bottom
)
```

### 分角圆角（iOS 16+）

```swift
.clipShape(UnevenRoundedRectangle(
    topLeadingRadius: 12,
    topTrailingRadius: 12,
    bottomLeadingRadius: 0,
    bottomTrailingRadius: 0
))
```

### 复杂插画 — 导出位图
渐变 + 布尔运算 + 多层重叠 → **不要**在 SwiftUI 里硬画，应 **PNG/WebP**（2x/3x）+ `Image` + `.resizable()`。

## 深色模式

```swift
// ✅ Asset 中 light/dark 变体
Color("primaryText")

// ✅ Environment
@Environment(\.colorScheme) var colorScheme
let textColor = colorScheme == .dark ? Color(hex: "F0F0F0") : Color(hex: "0F0F0F")

// ✅ 动态 UIColor 桥接
Color(UIColor.dynamic(light: UIColor(hex: "0F0F0F"), dark: UIColor(hex: "F0F0F0")))
```

## Figma 节点解读（SwiftUI 补充）

通用规则见 `figma-interpretation.md` 与 SKILL。SwiftUI 侧重：

- **容器 + 小图标 = 单个 `Image`**：FRAME 包 VECTOR/INSTANCE → `Image` + `.background`，勿多层嵌套
- **RECTANGLE 作背景**：GROUP 首子同尺寸 RECTANGLE → 父级 `.background`
- **GROUP vs FRAME**：有 `layoutMode` → `VStack`/`HStack`；无 → `ZStack` + `.offset`/`.position`
- **取整**：pt 约整数，字号约 0.5
