# UIKit Patterns — Figma to UIKit Mapping

> Purpose: Map Figma properties to UIKit code.
> Includes both basic mapping and **production patterns** derived from real-project experience.

## Layout Selection Guide

| Figma Structure | Recommended Approach |
|---|---|
| Simple vertical/horizontal stack | UIStackView |
| Complex / relative positioning | Auto Layout (NSLayoutConstraint) |
| Repeating similar items (≥3) | UITableView / UICollectionView |
| Scrollable content | UIScrollView |
| Overlapping views | UIView hierarchy with constraints |

## Auto-layout Mapping

| Figma Property | UIKit Equivalent |
|---|---|
| layoutMode: VERTICAL | UIStackView axis=.vertical |
| layoutMode: HORIZONTAL | UIStackView axis=.horizontal |
| itemSpacing | stackView.spacing |
| padding | layoutMargins + isLayoutMarginsRelativeArrangement |
| primaryAxisAlignItems: CENTER | distribution = .equalCentering |
| counterAxisAlignItems: CENTER | alignment = .center |
| layoutGrow: 1 | setContentHuggingPriority(.defaultLow) |
| primaryAxisSizingMode: FIXED | heightAnchor/widthAnchor constraint |

## Size Conversion

- Figma px → UIKit pt (1:1)
- Font sizes: .systemFont(ofSize:) with pt values

## Page Architecture Patterns

These patterns reflect how iOS apps are **actually structured** in production.

### Multi-Tab Pages
When a design shows **multiple tabs** (≥2 text labels acting as navigation):
- Use `UITabBarController` for bottom tab bars
- For top tabs (segmented switching), use a **custom tab bar** + `UIPageViewController` or child `UIViewController` swapping
- Do NOT use plain `UILabel` views for tabs — they lack selection state, indicators, and swipe support
- Each tab’s content should be a separate `UIViewController`
- Output: main controller (with tab bar + container) + separate content view controllers

```swift
// Custom top tab bar with UIPageViewController
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

### Navigation Bar — Treat as a Single Unit
The navigation bar is **one logical container**. Content below should reference it as a whole.
- Use `UINavigationController` with `UINavigationBar` for standard nav bars
- For custom nav bars, use a `UIView` container with subviews, then constrain content below to the container’s bottomAnchor

```swift
// Custom navigation bar
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

// Content constrained to nav container bottom
contentView.topAnchor.constraint(equalTo: navContainer.bottomAnchor, constant: 12).isActive = true
```

### Navigation Bar Buttons
- **Back/close buttons**: Use `UIButton` — simple, reliable
  - Circular background: `button.layer.cornerRadius = size/2` + `clipsToBounds`
  - Icon: `setImage(UIImage(named:), for: .normal)`
  - Do NOT wrap in extra container views for simple icon buttons

### Buttons with Icon + Text
Prefer `UIStackView` with `UIImageView` + `UILabel` inside a `UIView` container, or use `UIButton.Configuration` (iOS 15+).

```swift
// UIButton.Configuration approach (iOS 15+)
var config = UIButton.Configuration.plain()
config.image = UIImage(named: "ic_video")
config.title = "查看视频"
config.imagePadding = 6
config.baseForegroundColor = UIColor(hex: "0F0F0F")
config.background.strokeColor = UIColor(hex: "DCDCDC")
config.background.strokeWidth = 1
config.background.cornerRadius = 12
let button = UIButton(configuration: config)

// StackView approach (backward compatible)
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

### Switch / Toggle
- Use `UISwitch` — standard, reliable across all iOS versions
- For custom tint: `onTintColor` property
- For fully custom appearance (non-standard shape/size), consider a custom `UIControl` subclass

```swift
let toggle = UISwitch()
toggle.onTintColor = UIColor(hex: "0158FF")
toggle.isOn = true
```

### Input Fields vs Display Fields
Figma cannot distinguish between `UITextField` and `UILabel` — both appear as RECTANGLE + TEXT.
- **Placeholder-like text** with input styling → `UITextField`
- **Static display text** → `UILabel`
- **ASK the user if unsure**

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

## Width Strategy — Fixed vs Flexible

Figma widths are **computed results**, not design intent. Infer intent to decide Auto Layout constraints.

### Rule 1: Single element spanning full width
Element width + left/right offsets ≈ screen width, with symmetric margins → pin leading + trailing to superview with margin constants.

```swift
NSLayoutConstraint.activate([
    titleLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
    titleLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20)
])
```

### Rule 2: Identify the "flexible" element in side-by-side layouts
- **Fixed**: elements with inherent size (avatars, icons, buttons). Use explicit `widthAnchor`.
- **Flexible**: text/content areas. Do NOT set `widthAnchor` — let leading+trailing constraints determine width.
- Use `contentHuggingPriority` and `contentCompressionResistancePriority` to control which view stretches.

```swift
// Avatar (fixed) + label (flexible)
NSLayoutConstraint.activate([
    avatarView.widthAnchor.constraint(equalToConstant: 56),
    avatarView.heightAnchor.constraint(equalToConstant: 56),
    avatarView.leadingAnchor.constraint(equalTo: cell.leadingAnchor, constant: 20),

    nameLabel.leadingAnchor.constraint(equalTo: avatarView.trailingAnchor, constant: 16),
    nameLabel.trailingAnchor.constraint(equalTo: cell.trailingAnchor, constant: -20),
    // nameLabel width is determined by constraints, not explicit value
])
```

### Rule 3: Fixed width + centered
Element clearly narrower than screen, centered → explicit `widthAnchor` + `centerXAnchor`.

```swift
NSLayoutConstraint.activate([
    textField.widthAnchor.constraint(equalToConstant: 295),
    textField.heightAnchor.constraint(equalToConstant: 48),
    textField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
])
```

### Table/Collection View Cell Width
- Cell content should use leading/trailing constraints to superview (the cell’s contentView)
- Never hardcode cell width — let the table/collection view control it

## Multi-State Views

### Selected/Unselected State
Use `isSelected` property with custom state rendering:

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

For simpler cases, use `UIButton` with different configurations per state:
```swift
button.setTitleColor(UIColor(hex: "0F0F0F"), for: .selected)
button.setTitleColor(UIColor(hex: "858A99"), for: .normal)
```

### Disabled/Enabled State via Opacity
- Use `alpha` + `isEnabled` / `isUserInteractionEnabled`
- Do NOT create separate views for each state

```swift
submitButton.alpha = isValid ? 1.0 : 0.3
submitButton.isEnabled = isValid
```

### Stacked/Overlapping Cards
Stacked cards with similar structure → likely a card-switching interaction.
Do NOT generate as separate static views. Ask the user about the interaction pattern.
- UIKit options: `UIPageViewController`, custom pan gesture + transform, or third-party card stack library

## Visual Properties

### Color Hex Extension (include once in generated code)

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

### Layout Approach

1. Set `translatesAutoresizingMaskIntoConstraints = false`
2. Use `NSLayoutConstraint.activate([])`
3. Prefer UIStackView for linear layouts (reduces constraint count)
4. Use direct constraints for complex/absolute positioning

### Shadow Mapping

```swift
view.layer.shadowColor = UIColor(hex: "000000").cgColor
view.layer.shadowOpacity = 0.1
view.layer.shadowRadius = 4
view.layer.shadowOffset = CGSize(width: 0, height: 2)
```

### Gradient Mapping

```swift
let gradientLayer = CAGradientLayer()
gradientLayer.colors = [UIColor(hex: "FF6B6B").cgColor, UIColor(hex: "4ECDC4").cgColor]
gradientLayer.startPoint = CGPoint(x: 0.5, y: 0)
gradientLayer.endPoint = CGPoint(x: 0.5, y: 1)
gradientLayer.frame = view.bounds
view.layer.insertSublayer(gradientLayer, at: 0)
```

### Per-corner Radius

```swift
view.layer.cornerRadius = 12
view.layer.maskedCorners = [.layerMinXMinYCorner, .layerMaxXMinYCorner]  // top only
```

### Complex Illustrations — Export as Bitmap
When a Figma node contains gradients + boolean operations + multiple overlapping shapes:
- Do NOT attempt to recreate programmatically
- Export from Figma API as PNG/WebP at 2x/3x
- Use `UIImageView` with the exported image

## Dark Mode Patterns

### UIColor.dynamic Pattern
Most iOS projects use `UIColor.dynamic(light:dark:)` or similar wrapper. When generating code:

```swift
// ✅ Correct: use dynamic color for dark mode support
let textColor = UIColor.dynamic(
    light: UIColor(hex: "0F0F0F"),
    dark: UIColor(hex: "F0F0F0")
)

// ❌ Wrong: hardcoded single color (no dark mode)
let textColor = UIColor(hex: "0F0F0F")
```

### Dynamic Color Inference
Figma designs are typically light mode only. When generating dark mode counterparts:
- **Text**: light `#0F0F0F` → dark `#F0F0F0` (invert on gray scale)
- **Background**: light `#FFFFFF` → dark `#1C1C1E` (system dark background)
- **Card/surface**: light `#F7F7F7` → dark `#2C2C2E`
- **Dividers**: light `#EEEEEE` → dark `#3A3A3C`
- **Brand colors**: keep same or slightly lighten for dark (e.g., `#2965FF` → `#4D88FF`)
- **Always check the project first** — if the project already defines light/dark color pairs, use those

### When NOT to Infer Dark Mode
- If the project has NO dynamic colors (no `UIColor.dynamic` / no colorset with Appearances) → project likely doesn't support dark mode, don't add it
- If user explicitly says "light mode only" → use plain `UIColor(hex:)`

## Figma Node Interpretation (UIKit-specific notes)

The general Figma node interpretation rules in SKILL.md apply to all platforms.
Here are UIKit-specific mappings:

- **Container + icon = single UIImageView**: FRAME(background + cornerRadius) wrapping VECTOR/INSTANCE → one `UIImageView` with `layer.cornerRadius` + `backgroundColor` + `image`
- **RECTANGLE as background**: GROUP’s first child RECTANGLE matching parent size → `backgroundColor` or a background sublayer on the container UIView
- **GROUP vs FRAME**: FRAME with `layoutMode` → UIStackView; GROUP without `layoutMode` → explicit frame/constraints based on x/y positions
- **Rounding**: Round pt to nearest integer, font size to nearest 0.5