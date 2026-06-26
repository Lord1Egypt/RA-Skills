# UIKit 映射：Figma → UIKit

> 作用：把 Figma 属性映射到 UIKit。  
> 含基础映射与 **线上项目** 中常见的页面级写法。

## 布局选型

| Figma 结构 | 推荐做法 |
|---|---|
| 简单纵/横排 | `UIStackView` |
| 复杂相对关系 | Auto Layout（`NSLayoutConstraint`） |
| 重复相似项（≥3） | `UITableView` / `UICollectionView` |
| 可滚动内容 | `UIScrollView` |
| 视图重叠 | 约束驱动的 `UIView` 层级 |

## 自动布局映射

| Figma 属性 | UIKit 对应 |
|---|---|
| layoutMode: VERTICAL | `UIStackView` `axis = .vertical` |
| layoutMode: HORIZONTAL | `UIStackView` `axis = .horizontal` |
| itemSpacing | `stackView.spacing` |
| padding | `layoutMargins` + `isLayoutMarginsRelativeArrangement` |
| primaryAxisAlignItems: CENTER | `distribution = .equalCentering` 等 |
| counterAxisAlignItems: CENTER | `alignment = .center` |
| layoutGrow: 1 | `setContentHuggingPriority(.defaultLow)` 等 |
| primaryAxisSizingMode: FIXED | `heightAnchor` / `widthAnchor` |

## 尺寸换算

- Figma px → UIKit pt（约 1:1）
- 字号：`.systemFont(ofSize:)` 用 pt

## 页面级架构

以下贴近线上 iOS **真实结构**。

### 多 Tab 页
设计出现 **多个 Tab**（≥2 个文案作导航）时：

- 底部 Tab：`UITabBarController`
- 顶部分段切换：**自定义 Tab 条** + `UIPageViewController` 或子 VC 切换
- **不要**用纯 `UILabel` 当 Tab
- 每个 Tab 内容独立 `UIViewController`
- 输出：主控制器（Tab + 容器）+ 各内容 VC

```swift
// 顶部自定义 Tab + UIPageViewController（骨架示例）
class TabContainerViewController: UIViewController {
    private let tabBar = UIStackView()
    private let pageVC = UIPageViewController(transitionStyle: .scroll, navigationOrientation: .horizontal)
    private var tabs: [UIButton] = []
    private var viewControllers: [UIViewController] = []
    private var selectedIndex = 0

    private func setupTabBar() {
        tabBar.axis = .horizontal
        tabBar.spacing = 24
        tabBar.alignment = .center

        let titles = ["关注", "推荐", "热榜"]
        for (index, title) in titles.enumerated() {
            let button = UIButton(type: .system)
            button.setTitle(title, for: .normal)
            button.titleLabel?.font = .systemFont(ofSize: 16, weight: index == 0 ? .bold : .regular)
            button.setTitleColor(index == 0 ? UIColor(hex: "0F0F0F") : UIColor(hex: "858A99"), for: .normal)
            button.tag = index
            button.addTarget(self, action: #selector(tabTapped(_:)), for: .touchUpInside)
            tabs.append(button)
            tabBar.addArrangedSubview(button)
        }
    }

    @objc private func tabTapped(_ sender: UIButton) {
        selectTab(at: sender.tag)
    }
}
```

### 导航栏 — 视为整体
导航栏是 **一个逻辑容器**。标准用 `UINavigationController`；自定义用 `UIView` 容器，主内容约束到容器 `bottomAnchor`。

```swift
// 自定义导航栏
let navContainer = UIView()
navContainer.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(navContainer)

let backButton = UIButton(type: .system)
backButton.setImage(UIImage(named: "ic_back"), for: .normal)
backButton.backgroundColor = UIColor(hex: "000000")
backButton.layer.cornerRadius = 16
backButton.translatesAutoresizingMaskIntoConstraints = false

let titleLabel = UILabel()
titleLabel.text = "设置"
titleLabel.font = .systemFont(ofSize: 17, weight: .bold)
titleLabel.translatesAutoresizingMaskIntoConstraints = false

navContainer.addSubview(backButton)
navContainer.addSubview(titleLabel)

// 主内容顶对齐到导航容器底
contentView.topAnchor.constraint(equalTo: navContainer.bottomAnchor, constant: 12).isActive = true
```

### 导航栏按钮
- 返回/关闭：`UIButton`；圆底用 `layer.cornerRadius` + `clipsToBounds`
- 简单图标 **不要**再套多余容器

### 图标 + 文字按钮
优先 `UIStackView` + `UIImageView` + `UILabel` 放在容器里；或 iOS 15+ `UIButton.Configuration`。

```swift
// UIButton.Configuration（iOS 15+）
var config = UIButton.Configuration.plain()
config.image = UIImage(named: "ic_video")
config.title = "查看视频"
config.imagePadding = 6
config.baseForegroundColor = UIColor(hex: "0F0F0F")
config.background.strokeColor = UIColor(hex: "DCDCDC")
config.background.strokeWidth = 1
config.background.cornerRadius = 12
let button = UIButton(configuration: config)

// StackView（兼容旧系统）
let container = UIView()
container.layer.cornerRadius = 12
container.layer.borderWidth = 1
container.layer.borderColor = UIColor(hex: "DCDCDC").cgColor

let stack = UIStackView()
stack.axis = .horizontal
stack.spacing = 6
stack.alignment = .center

let iconView = UIImageView(image: UIImage(named: "ic_video"))
iconView.widthAnchor.constraint(equalToConstant: 20).isActive = true
iconView.heightAnchor.constraint(equalToConstant: 20).isActive = true

let label = UILabel()
label.text = "查看视频"
label.font = .systemFont(ofSize: 15, weight: .bold)
label.textColor = UIColor(hex: "0F0F0F")

stack.addArrangedSubview(iconView)
stack.addArrangedSubview(label)
container.addSubview(stack)
```

### 开关
- 标准用 `UISwitch`；着色 `onTintColor`
- 完全自定义外观可考虑子类化 `UIControl`

```swift
let toggle = UISwitch()
toggle.onTintColor = UIColor(hex: "0158FF")
toggle.isOn = true
```

### 输入框 vs 纯展示
Figma 无法区分 `UITextField` 与 `UILabel`。

- 占位风格 + 输入态 → `UITextField`
- 静态展示 → `UILabel`
- **不确定时问用户**

```swift
let textField = UITextField()
textField.placeholder = "请输入昵称"
textField.font = .systemFont(ofSize: 15)
textField.textColor = UIColor(hex: "0F0F0F")
textField.layer.cornerRadius = 8
textField.layer.borderWidth = 1
textField.layer.borderColor = UIColor(hex: "E5E5E5").cgColor
textField.leftView = UIView(frame: CGRect(x: 0, y: 0, width: 12, height: 0))
textField.leftViewMode = .always
```

## 宽度策略：固定 vs 弹性

Figma 宽度多为 **计算结果**，需推断意图再建约束。

### 规则 1：单元素撑满宽
左右边距对称、近似撑满屏 → `leading`/`trailing` 钉父视图并带常数。

```swift
NSLayoutConstraint.activate([
    titleLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
    titleLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20)
])
```

### 规则 2：并排时识别「弹性」方
- **固定**：头像、图标、按钮等，显式 `widthAnchor`
- **弹性**：正文区不设死 `width`，由 leading/trailing 决定
- 用 `contentHuggingPriority` / `contentCompressionResistancePriority` 控制伸缩

```swift
// 固定头像 + 弹性标签
NSLayoutConstraint.activate([
    avatarView.widthAnchor.constraint(equalToConstant: 56),
    avatarView.heightAnchor.constraint(equalToConstant: 56),
    avatarView.leadingAnchor.constraint(equalTo: cell.leadingAnchor, constant: 20),

    nameLabel.leadingAnchor.constraint(equalTo: avatarView.trailingAnchor, constant: 16),
    nameLabel.trailingAnchor.constraint(equalTo: cell.trailingAnchor, constant: -20),
])
```

### 规则 3：固定宽 + 居中
明显窄于屏且居中 → `widthAnchor` + `centerXAnchor`。

```swift
NSLayoutConstraint.activate([
    textField.widthAnchor.constraint(equalToConstant: 295),
    textField.heightAnchor.constraint(equalToConstant: 48),
    textField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
])
```

### Table/Collection Cell
- 内容相对 `contentView` 做 leading/trailing
- **不要**写死 cell 宽度，由列表控制

## 多状态视图

### 选中 / 未选中
可用 `isSelected` + 自绘，或 `UIButton` 各状态标题色。

```swift
class GenderCardView: UIControl {
    override var isSelected: Bool {
        didSet { updateAppearance() }
    }

    private func updateAppearance() {
        backgroundColor = isSelected ? UIColor(hex: "E8F0FF") : UIColor(hex: "F5F5F5")
        layer.borderColor = isSelected ? UIColor(hex: "0158FF").cgColor : UIColor.clear.cgColor
        layer.borderWidth = isSelected ? 2 : 0
    }
}
```

```swift
button.setTitleColor(UIColor(hex: "0F0F0F"), for: .selected)
button.setTitleColor(UIColor(hex: "858A99"), for: .normal)
```

### 禁用 / 可用（透明度）
`alpha` + `isEnabled` / `isUserInteractionEnabled`，勿为每状态各做一个 View。

```swift
submitButton.alpha = isValid ? 1.0 : 0.3
submitButton.isEnabled = isValid
```

### 叠放卡片
结构相似叠放 → 可能为切卡交互。**不要**只生成静态多层 View；问清交互；可用 `UIPageViewController`、手势或第三方。

## 视觉属性

### UIColor hex 扩展（生成代码中可含一次）

```swift
extension UIColor {
    convenience init(hex: String) {
        let scanner = Scanner(string: hex)
        var rgb: UInt64 = 0
        scanner.scanHexInt64(&rgb)
        self.init(
            red: CGFloat((rgb >> 16) & 0xFF) / 255.0,
            green: CGFloat((rgb >> 8) & 0xFF) / 255.0,
            blue: CGFloat(rgb & 0xFF) / 255.0,
            alpha: 1.0
        )
    }
}
```

### 布局习惯

1. `translatesAutoresizingMaskIntoConstraints = false`
2. `NSLayoutConstraint.activate([])`
3. 线性布局优先 `UIStackView` 减少约束数量
4. 复杂/绝对位置用直接约束

### 阴影

```swift
view.layer.shadowColor = UIColor(hex: "000000").cgColor
view.layer.shadowOpacity = 0.1
view.layer.shadowRadius = 4
view.layer.shadowOffset = CGSize(width: 0, height: 2)
```

### 渐变

```swift
let gradientLayer = CAGradientLayer()
gradientLayer.colors = [UIColor(hex: "FF6B6B").cgColor, UIColor(hex: "4ECDC4").cgColor]
gradientLayer.startPoint = CGPoint(x: 0.5, y: 0)
gradientLayer.endPoint = CGPoint(x: 0.5, y: 1)
gradientLayer.frame = view.bounds
view.layer.insertSublayer(gradientLayer, at: 0)
```

### 分角圆角

```swift
view.layer.cornerRadius = 12
view.layer.maskedCorners = [.layerMinXMinYCorner, .layerMaxXMinYCorner]  // 仅顶部
```

### 复杂插画 — 导出位图
渐变 + 布尔 + 多层重叠 → **不要**纯代码还原；**PNG/WebP**（2x/3x）+ `UIImageView`。

## 深色模式

### 动态色
工程常见 `UIColor.dynamic(light:dark:)` 或封装。生成时：

```swift
// ✅ 支持深色：动态色
let textColor = UIColor.dynamic(
    light: UIColor(hex: "0F0F0F"),
    dark: UIColor(hex: "F0F0F0")
)

// ❌ 仅浅色：单路 hex（无深色策略时）
let textColor = UIColor(hex: "0F0F0F")
```

### 深色值推断（仅供参考）
Figma 多为浅色稿。若需补深色对应：

- 正文：浅 `#0F0F0F` → 深约 `#F0F0F0`
- 背景：浅 `#FFFFFF` → 深约 `#1C1C1E`
- 卡片：浅 `#F7F7F7` → 深约 `#2C2C2E`
- 分割线：浅 `#EEEEEE` → 深约 `#3A3A3C`
- 品牌色可略提亮（如 `#2965FF` → `#4D88FF`）
- **优先以工程已有 light/dark 对为准**

### 何时不推断深色
- 工程无动态色、无 Asset Appearances → 可能不支持深色，**不要**擅自加
- 用户明确只要浅色 → 用 `UIColor(hex:)`

## Figma 节点解读（UIKit 补充）

通用规则见 SKILL 与 `figma-interpretation.md`。UIKit 侧重：

- **容器 + 小图标 = 单个 `UIImageView`**：FRAME 包 VECTOR/INSTANCE → 圆角/背景 + `image`
- **RECTANGLE 作背景**：GROUP 首子同尺寸 RECTANGLE → 容器 `backgroundColor` 或背景子层
- **GROUP vs FRAME**：有 `layoutMode` → `UIStackView`；无 → 按 x/y 建约束
- **取整**：pt 约整数，字号约 0.5
