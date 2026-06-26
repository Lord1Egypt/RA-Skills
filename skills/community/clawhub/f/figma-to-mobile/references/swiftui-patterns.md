# SwiftUI Patterns — Figma to SwiftUI Mapping

> Purpose: Map Figma properties to SwiftUI code.
> Includes both basic mapping and **production patterns** derived from real-project experience.

## Layout Selection Guide

| Figma Structure | Recommended View |
|---|---|
| Vertical stack | VStack |
| Horizontal stack | HStack |
| Overlapping / z-stacking | ZStack |
| Repeating similar items (≥3) | List / LazyVStack / LazyHStack |
| Page with navigation bar | NavigationStack + .navigationTitle |
| Scrollable content | ScrollView |

## Auto-layout Mapping

| Figma Property | SwiftUI Equivalent |
|---|---|
| layoutMode: VERTICAL | VStack |
| layoutMode: HORIZONTAL | HStack |
| itemSpacing | spacing: parameter |
| padding* | .padding() modifiers |
| primaryAxisAlignItems: CENTER | alignment parameter + Spacer() |
| counterAxisAlignItems: CENTER | alignment: .center |
| layoutGrow: 1 | .frame(maxWidth: .infinity) or Spacer() |
| primaryAxisSizingMode: FIXED | .frame(height/width: X) |

## Size Conversion

- Figma px → SwiftUI pt (1:1)
- Font sizes: .system(size:) with pt values

## Page Architecture Patterns

These patterns reflect how iOS apps are **actually structured** in production.
When generating code, think about the **page-level architecture**, not just individual views.

### Multi-Tab Pages
When a design shows **multiple tabs** (≥2 text labels acting as navigation):
- Use `TabView` with `.tabViewStyle(.page)` for swipeable tabs, or custom `Picker`/segmented control for top tabs
- For bottom tab bars, use `TabView` with default style (system tab bar)
- Do NOT use plain `Text` views for tabs — they lack selection state, indicators, and swipe support
- Each tab’s content should be a separate `View` struct
- Output: main view (with TabView/segmented control) + separate content views

```swift
// Top tab bar with underline indicator (custom)
struct ContentView: View {
    @State private var selectedTab = 0
    let tabs = ["关注", "推荐", "热榜"]

    var body: some View {
        VStack(spacing: 0) {
            // Tab bar
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

            // Content
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

### Navigation Bar — Treat as a Single Unit
The navigation bar (back button + title, possibly + right action) is **one logical container**.
- Use `NavigationStack` with `.toolbar` for standard nav bars
- For custom nav bars (non-standard styling), use `HStack` as a single container, then place content below with proper spacing
- Content below should reference the navbar as one unit, not individual children within it

```swift
// Custom navigation bar
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
    Color.clear.frame(width: 32, height: 32) // Balance spacer
}
.padding(.horizontal, 20)
```

### Navigation Bar Buttons
- **Back/close buttons**: Use `Button` with `Image` content — simple, reliable
  - Circular background: `.background(Circle().fill(...))` on the Image
  - Icon: `Image(systemName:)` for SF Symbols or `Image("custom_icon")`
  - Do NOT wrap in extra containers for simple icon buttons

### Buttons with Icon + Text
Prefer `HStack` with `Image` + `Text` inside a `Button` for reliable icon+text buttons.
`Label` is an alternative but gives less layout control.

```swift
// Outlined button with icon
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

// Solid filled button
Button(action: {}) {
    Text("查看报告")
        .font(.system(size: 15, weight: .bold))
        .foregroundColor(.white)
        .frame(maxWidth: .infinity)
        .frame(height: 40)
        .background(RoundedRectangle(cornerRadius: 12).fill(Color(hex: "0158FF")))
}
```

### Switch / Toggle
- Use `Toggle` — it’s the standard SwiftUI control, reliable across all iOS versions
- For custom styling (non-standard colors/shape), use `.toggleStyle` with a custom style
- For tint color changes: `.tint(Color(...))` (iOS 15+)

```swift
Toggle("通知", isOn: $isEnabled)
    .tint(Color(hex: "0158FF"))
```

### Input Fields vs Display Fields
Figma cannot distinguish between input and display — both appear as RECTANGLE + TEXT.
- **Placeholder-like text** ("选择你的生日", "请输入姓名") with input styling → `TextField`
- **Static display text** → `Text`
- **ASK the user if unsure** — this is a functional decision

```swift
// Input field
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

## Width Strategy — Fixed vs Flexible

Figma designs are usually based on a fixed canvas (e.g. 375px or 390px). Figma widths are **computed results**, not design intent. Infer intent to decide SwiftUI sizing.

Core question: **Is this element’s width "fixed" or "fill remaining space"?**

### Rule 1: Single element spanning full width
Element width + left/right offsets ≈ screen width, with symmetric margins → `.frame(maxWidth: .infinity)` + `.padding(.horizontal, X)`

```swift
Text("标题")
    .frame(maxWidth: .infinity, alignment: .leading)
    .padding(.horizontal, 20)
```

### Rule 2: Identify the "flexible" element in side-by-side layouts
Multiple elements arranged horizontally — determine which is **fixed** and which is **flexible**:
- **Fixed**: elements with inherent size — avatars, icons, buttons. Use explicit `.frame(width:)`
- **Flexible**: text/content areas that fill remaining space. Use `Spacer()` or let natural layout expand

```swift
// Avatar (fixed) + text (flexible)
HStack(spacing: 16) {
    Image("avatar")
        .resizable()
        .frame(width: 56, height: 56)
        .clipShape(Circle())
    VStack(alignment: .leading, spacing: 4) {
        Text("用户名").font(.system(size: 16, weight: .bold))
        Text("描述文字").font(.system(size: 14)).foregroundColor(.gray)
    }
    Spacer() // text side is flexible
}
.padding(.horizontal, 20)
```

### Rule 3: Fixed width + centered
Element clearly narrower than screen, centered → explicit `.frame(width:)` with centered parent

```swift
TextField("请输入昵称", text: $nickname)
    .frame(width: 295, height: 48)
```

### List Item Width
- Item views should use `.frame(maxWidth: .infinity)` — List/LazyVStack controls the width
- The List itself follows the above rules for its own sizing

## Multi-State Views

When the same View has two or more visual states (selected/unselected, enabled/disabled):

### Selected/Unselected State
Use conditional modifiers based on state:

```swift
// Gender selection card
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

### Disabled/Enabled State via Opacity
When a View appears in two states where one has reduced opacity:
- Use `.opacity()` + `.disabled()` modifiers
- Do NOT create separate views for each state

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

### Stacked/Overlapping Cards
Stacked cards with similar structure (same shape, offset position) → likely a card-switching interaction.
Do NOT generate as separate static Views. Ask the user about the interaction pattern.
- SwiftUI options: `TabView(.page)`, custom `DragGesture` + offset, or third-party card stack library

## Visual Properties

### Color Hex Extension (include once in generated code)

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

### Shadow Mapping

```swift
.shadow(color: Color(hex: "000000").opacity(0.1), radius: 4, x: 0, y: 2)
```

### Gradient Mapping

```swift
LinearGradient(
    colors: [Color(hex: "FF6B6B"), Color(hex: "4ECDC4")],
    startPoint: .top,
    endPoint: .bottom
)
```

### Per-corner Radius (iOS 16+)

```swift
.clipShape(UnevenRoundedRectangle(
    topLeadingRadius: 12,
    topTrailingRadius: 12,
    bottomLeadingRadius: 0,
    bottomTrailingRadius: 0
))
```

### Complex Illustrations — Export as Bitmap
When a Figma node contains gradients + boolean operations + multiple overlapping shapes:
- Do NOT attempt to recreate in SwiftUI code
- Export from Figma API as PNG/WebP at 2x/3x
- Use `Image("illustration")` with `.resizable()` and `.aspectRatio(contentMode: .fit)`

## Dark Mode Patterns

```swift
// ✅ Using Color asset with light/dark variants
Color("primaryText") // defined in Assets.xcassets with Appearances

// ✅ Using Environment
@Environment(\.colorScheme) var colorScheme
let textColor = colorScheme == .dark ? Color(hex: "F0F0F0") : Color(hex: "0F0F0F")

// ✅ Dynamic UIColor bridge
Color(UIColor.dynamic(light: UIColor(hex: "0F0F0F"), dark: UIColor(hex: "F0F0F0")))
```

## Figma Node Interpretation (SwiftUI-specific notes)

The general Figma node interpretation rules in SKILL.md apply to all platforms.
Here are SwiftUI-specific mappings:

- **Container + icon = single Image**: FRAME(background + cornerRadius) wrapping VECTOR/INSTANCE → one `Image` with `.background(Circle/RoundedRectangle)`, not nested views
- **RECTANGLE as background**: GROUP’s first child RECTANGLE matching parent size → `.background()` modifier on the container
- **GROUP vs FRAME**: FRAME with `layoutMode` → VStack/HStack; GROUP without `layoutMode` → ZStack with explicit `.offset()` or `.position()`
- **Rounding**: Round pt to nearest integer, sp to nearest 0.5