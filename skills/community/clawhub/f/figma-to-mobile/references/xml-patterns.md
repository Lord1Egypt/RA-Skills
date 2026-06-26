# XML Layout Patterns — Figma to Android Mapping

> Purpose: Map Figma properties to Android XML attributes.
> This is a **mapping reference**, not an Android tutorial — the agent already knows Android conventions.
> Also includes **real-project usage patterns** — what experienced Android devs actually use in production.

## Layout Selection Guide

| Figma Structure | Recommended Layout |
|---|---|
| Complex with overlaps / relative positioning | **ConstraintLayout** (default choice) |
| Simple vertical/horizontal stack, no overlap | LinearLayout |
| Children overlapping / z-stacking | FrameLayout |
| Repeating similar items (≥3) | RecyclerView + item layout |

## Page Architecture Patterns

These patterns reflect how Android apps are **actually structured** in production.
When generating code, think about the **page-level architecture**, not just individual views.

### Multi-Tab Pages
When a design shows **multiple tabs** (≥2 text labels acting as navigation):
- **Highly likely** `TabLayout` + `ViewPager2` — this is the standard pattern for tab switching
- Do NOT use plain TextViews for tabs — they lack selection state, indicators, and swipe support
- The content area below tabs is **likely** a `ViewPager2` container, each tab's content in its own Fragment
- Output: main layout (with TabLayout + ViewPager2) + separate fragment layout(s)
- **Note**: This is a strong signal, not an absolute rule. If the design clearly shows a single static page with tab-like labels that are purely decorative, adjust accordingly. When unsure, ASK.

```xml
<!-- Standard Tab + ViewPager2 structure -->
<com.google.android.material.tabs.TabLayout
    android:id="@+id/tabLayout"
    android:layout_width="0dp"
    android:layout_height="48dp"
    app:tabIndicatorColor="#0F0F0F"
    app:tabSelectedTextColor="#0F0F0F"
    app:tabTextColor="#858A99"
    app:tabGravity="center"
    app:tabMode="fixed" />

<androidx.viewpager2.widget.ViewPager2
    android:id="@+id/viewPager"
    android:layout_width="0dp"
    android:layout_height="0dp" />
```

### Navigation Bar — Treat as a Single Unit
The navigation bar (back button + title, possibly + right action) is **one logical container**. Content below it should be constrained to the navbar's bottom, not to individual children within it.

**Implementation**: Wrap the back button and title in a single container (ConstraintLayout/Toolbar/FrameLayout), then constrain page content `layout_constraintTop_toBottomOf="@id/navbar"`. This avoids error-prone absolute margin calculations.

**Distance calculation**: When Figma shows content at y=112 and the navbar occupies y=0~100 (StatusBar 56 + NavBar 44), the real gap between navbar bottom and content top is **12dp** — not 68dp or 112dp. Always subtract the navbar extent, and remember Android StatusBar is outside the layout tree.

### Navigation Bar Buttons
- **Back/close buttons**: Use `ImageView` — simple, reliable, supports `src` + `background` combo
  - Circular background: set `android:background` to a circle shape drawable
  - Icon: set `android:src` to the arrow/close icon
  - The entire thing might also be a single combined asset — when in doubt, use one `ImageView`
- Do NOT use `FrameLayout` wrapping another view for simple icon buttons

```xml
<!-- Back button: ImageView with circle background + icon -->
<ImageView
    android:id="@+id/btnBack"
    android:layout_width="32dp"
    android:layout_height="32dp"
    android:background="@drawable/placeholder"
    android:src="@drawable/placeholder"
    android:scaleType="centerInside"
    android:contentDescription="返回" />
<!-- background = circle shape (#000000), src = white arrow icon -->
```

### Buttons with Icon + Text
`MaterialButton` with `app:icon` has known rendering issues in some configurations.
`TextView` with `drawableStart`/`drawableEnd` also has centering issues — the drawable and text are centered together as a group, but neither the icon nor the text can be independently centered, causing visual misalignment.

**Always use `LinearLayout` (horizontal) + `ImageView` + `TextView`** for icon+text buttons — this is the ONLY reliable approach:

```xml
<!-- Outlined button with icon -->
<LinearLayout
    android:id="@+id/btnVideo"
    android:layout_width="0dp"
    android:layout_height="40dp"
    android:orientation="horizontal"
    android:gravity="center"
    android:background="@drawable/placeholder"
    android:clickable="true"
    android:focusable="true">
    <!-- background = rounded rect shape with stroke #DCDCDC, cornerRadius=12dp, solid #FFFFFF -->

    <ImageView
        android:layout_width="20dp"
        android:layout_height="20dp"
        android:src="@drawable/placeholder" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginStart="6dp"
        android:text="查看视频"
        android:textSize="15sp"
        android:textColor="#0F0F0F"
        android:textStyle="bold" />
</LinearLayout>

<!-- Solid filled button (no icon, or icon optional) -->
<TextView
    android:id="@+id/btnReport"
    android:layout_width="0dp"
    android:layout_height="40dp"
    android:gravity="center"
    android:text="查看报告"
    android:textSize="15sp"
    android:textColor="#FFFFFF"
    android:textStyle="bold"
    android:background="@drawable/placeholder" />
<!-- background = rounded rect shape, solid #0158FF, cornerRadius=12dp -->
```

### Text-Only Buttons (No Icon)
For buttons with **only text** (no icon), use a plain `TextView` with background — do NOT use `MaterialButton` or `LinearLayout`:

```xml
<TextView
    android:id="@+id/btnSubmit"
    android:layout_width="0dp"
    android:layout_height="48dp"
    android:gravity="center"
    android:text="提交"
    android:textSize="16sp"
    android:textColor="#FFFFFF"
    android:textStyle="bold"
    android:background="@drawable/placeholder"
    android:clickable="true"
    android:focusable="true" />
<!-- background = rounded rect shape, solid #0158FF, cornerRadius=12dp -->
```

**Summary:**
| Button Type | Correct Approach | Never Use |
|---|---|---|
| Icon + Text | `LinearLayout` + `ImageView` + `TextView` | `MaterialButton` with `app:icon`, `TextView` with `drawableStart` |
| Text Only | `TextView` with `background` + `gravity="center"` | `MaterialButton` (unless default Material styling is explicitly desired) |

### Switch / Toggle
- **Prefer `SwitchCompat`** (`androidx.appcompat.widget.SwitchCompat`) over `MaterialSwitch` — more reliable rendering across API levels and themes
- `MaterialSwitch` (`com.google.android.material.materialswitch.MaterialSwitch`) can have display issues depending on Material theme configuration
- If the design shows a custom-styled toggle (non-standard colors/shape), `SwitchCompat` with custom `thumb` and `track` drawables is easier to control

### Multi-State Views — Use Selector Drawables
When the same View has two or more visual states (selected/unselected, enabled/disabled, pressed/normal):
- **Use `selector` drawable** to combine states into one resource, NOT separate drawables toggled in code
- Parent View state propagates to children via `android:duplicateParentState="true"` — set state on parent, children auto-switch
- Common state attributes: `state_selected`, `state_activated`, `state_pressed`, `state_enabled`

```xml
<!-- drawable/bg_gender_card_selector.xml -->
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true" android:drawable="@drawable/bg_gender_card_selected" />
    <item android:drawable="@drawable/bg_gender_card_unselected" />
</selector>

<!-- drawable/ic_check_selector.xml (controls visibility via alpha) -->
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true" android:drawable="@drawable/ic_check_selected" />
    <item android:drawable="@android:color/transparent" />
</selector>
```

In code, just call `cardFemale.setSelected(true)` and all children with `duplicateParentState` follow.

### Card/Container Internals — Prefer ConstraintLayout over FrameLayout
When a card or container has multiple children that need positioning (icon at top-right, image centered, text at bottom):
- Use `ConstraintLayout` as the card root — flatter, more efficient, more precise
- `FrameLayout` is only appropriate when children truly just stack/overlap without relative positioning

### Input Fields vs Display Fields
Figma cannot distinguish between an `EditText` and a `TextView` — both appear as RECTANGLE + TEXT in the design data.
- **If the text content looks like a placeholder** ("选择你的生日", "请输入姓名", etc.) and the design shows a text input style (border + single line + hint-colored text), it's likely an **EditText**
- **ASK the user if unsure** — this is a functional decision that cannot be reliably determined from design data alone
- When generating EditText: use `android:hint` instead of `android:text`, set `android:inputType` appropriately

```xml
<!-- Input field example -->
<EditText
    android:id="@+id/etNickname"
    android:layout_width="295dp"
    android:layout_height="48dp"
    android:background="@drawable/bg_input"
    android:paddingStart="12dp"
    android:hint="请输入昵称"
    android:textColorHint="#B8B8B8"
    android:textSize="15sp"
    android:textColor="#0F0F0F"
    android:inputType="text"
    android:maxLines="1" />
```

### List Item Height Alignment
When a list item has a **left sidebar element** and **right content area**, observe the design data to decide alignment:
- Look at **multiple items** in the design — if the left side height is consistent across items and doesn't change with right side content length, they are likely **equal height** (constrain top-to-top + bottom-to-bottom, or same fixed height)
- If the left side height clearly varies with content, use `wrap_content` independently
- **This is observation-based, not a fixed rule** — always check the actual data for each design

## Figma Node Interpretation Rules

These rules help correctly interpret Figma node structures when mapping to Android views.
They are **observation heuristics**, not absolute rules — always verify against the actual design data.

### System Components — Skip
Nodes representing **iOS system chrome** should NOT generate Android code:
- `StatusBar`, `HomeIndicator`, `NavigationBar` (by name)
- These are Figma design placeholders for the system UI — Android handles them natively
- Signal: INSTANCE nodes with names like "StatusBar", "HomeIndicator", or with well-known component IDs that appear at screen top (y≈0) or bottom (y≈screen height - small offset)
- Also skip **duplicate nodes** — if the same component appears twice at the same position, only one is real (Figma artifact)

### Invisible Nodes — Skip
Nodes that exist in the tree but render nothing should NOT generate views:
- **VECTOR with empty fills + invisible strokes**: `fills: []` and all strokes have `visible: false` → the node is effectively invisible
- **`absoluteRenderBounds: null`**: Figma returns null when the node has no rendered output — always skip
- These are often leftover elements from earlier design iterations that the designer forgot to delete
- Note: this is different from `visible: false` on the node itself (which `figma_fetch.py` already filters out)

### Container + Icon = Single ImageView
When data shows a **FRAME** (with background color + cornerRadius) containing a single **INSTANCE** or **VECTOR** child that is clearly an icon:
- This is one `ImageView` in code, not a nested layout
- `android:background` = the container shape (circle, rounded rect, etc.)
- `android:src` = the icon drawable
- Typical signal: outer FRAME has cornerRadius ≥ 50% of size (circular), inner child is VECTOR/INSTANCE much smaller than container
- Example from data: FRAME(32×32, #000000, cornerRadius=100) → INSTANCE(18×18) → VECTOR = one `ImageView`

### VECTOR/ELLIPSE Compositions = Single Drawable
When a FRAME contains **multiple VECTOR and/or ELLIPSE** nodes that together form a recognizable icon shape:
- These are pieces of a single icon asset, NOT separate views
- In code: one `ImageView` with `android:src="@drawable/placeholder"`
- Signal: multiple small VECTOR/ELLIPSE siblings inside a FRAME, all with small sizes relative to parent, often overlapping
- Example: play button icon = 2 VECTORs (triangle shape) + 1 ELLIPSE (circle outline) → one icon asset

### RECTANGLE as Background
When a GROUP's **first child** is a RECTANGLE with the **same dimensions** as the GROUP:
- The RECTANGLE is a background shape, not an independent view
- Map it to `android:background` on the parent container
- Signal: RECTANGLE is first child, width≈GROUP width, height≈GROUP height
- Example: GROUP(40×152) → first child RECTANGLE(40×152, #F3F3F4, cornerRadius=30) = background shape

### GROUP vs FRAME Layout Strategy
- **FRAME with `layoutMode`**: has Auto-layout → map to LinearLayout or ConstraintLayout chain (structured flow)
- **GROUP without `layoutMode`**: no Auto-layout → children are positioned by absolute coordinates → use ConstraintLayout with constraints derived from x/y positions
- When converting GROUP children positions to constraints, calculate relative offsets from the GROUP's origin

### Tab Selected State
When multiple Text nodes in a tab bar have **different textColors** (e.g., one is #0F0F0F, others are #858A99):
- This indicates selected vs unselected state
- Map to `TabLayout` attributes: `app:tabSelectedTextColor` for the active color, `app:tabTextColor` for inactive
- Do NOT hardcode individual tab colors — the selection state is dynamic at runtime

### Figma Decimal Precision → Android Rounding
Figma values often have excessive decimal places (e.g., 127.86dp, 7.63dp):
- **Round to nearest integer dp** for layout dimensions, margins, padding
- **Round sp to nearest 0.5** for font sizes (e.g., 15.27sp → 15sp)
- Exception: if the exact value clearly maps to a standard size (e.g., 47.99 → 48dp), snap to that

### Complex Illustrations — Export as Bitmap, Not Vector
When a Figma node contains **gradients + boolean operations + multiple overlapping shapes** (e.g., character illustrations, mascots, complex logos):
- Do NOT attempt to convert to Android Vector Drawable — it will lose visual fidelity (gradients, blend modes, boolean ops are poorly supported)
- Export from Figma API as **PNG or WebP** at appropriate density (2x/3x)
- Use `ImageView` with the exported bitmap
- Signal: node tree has ELLIPSE/VECTOR with `gradient` fields, nested BOOLEAN_OPERATION, or opacity/blend effects

### Multi-State Page Analysis
When given **multiple Figma frames representing different states** of the same page:
1. First identify which nodes are **shared** (identical across states) — these are static
2. Then diff the remaining nodes to find **what changes** between states (color, text, visibility, border, opacity)
3. For each changing property, annotate in the XML with a comment describing the state transition
4. Prefer declarative state handling (selector drawables, alpha, state attributes) over imperative code (manual visibility toggles)
5. Output a **state change summary table** after the XML for the developer to implement business logic

### Disabled/Enabled State via Opacity
When a View appears in two states where one has `opacity < 1` and the other has full opacity:
- This is a **disabled/enabled** pattern
- Map to `android:alpha` (0.3 = disabled, 1.0 = enabled)
- Also set `android:clickable` and `android:enabled` accordingly
- Do NOT use a separate drawable — alpha is sufficient

## ConstraintLayout Mapping

### Child View Sizing Rules (from real-project analysis)

When generating a child View inside ConstraintLayout, choose width/height based on content type:

| Content Type | Width × Height | When |
|---|---|---|
| Text / auto-size content | `wrap_content` × `wrap_content` | Default for labels, titles |
| Text filling horizontal space | `0dp` × `wrap_content` | When constrained Start+End |
| Icon (small indicator) | `12dp` × `12dp` | Dots, status indicators |
| Icon (inline/row) | `20dp` × `20dp` | Icons next to text in rows |
| Icon (standard action) | `24dp` × `24dp` | Toolbar/action icons (Material standard) |
| Icon (medium) | `32dp` × `32dp` | Feature icons, navigation |
| Touch target / avatar | `48dp` × `48dp` | Buttons, avatars (Material min touch) |
| Divider/separator | `match_parent` × `1px` | Horizontal line between sections |
| Full-width scrollable area | `match_parent` × `0dp` | RecyclerView/ScrollView filling remaining space |
| Row container (fixed height) | `match_parent` × `44dp`~`56dp` | List items, settings rows |

**Divider pattern** — use a plain `View` with background color:
```xml
<View
    android:layout_width="match_parent"
    android:layout_height="1px"
    android:background="@color/divider"
    app:layout_constraintTop_toBottomOf="@id/prevView" />
```
Note: use `1px` not `1dp` for hairline dividers (1dp = 2-3px on high-DPI, too thick).

### ImageView Mapping

Figma icon nodes should map to a simple `ImageView` with `src`/`srcCompat`:
```xml
<ImageView
    android:layout_width="24dp"
    android:layout_height="24dp"
    app:srcCompat="@drawable/ic_arrow_right" />
```

**Default: `src` only.** In practice, most ImageViews only need `src`/`srcCompat`.

**When to use `background` + `src`:**
- Figma shows a filled circle/rectangle behind the icon → `background` (shape drawable) + `src` (icon)
- **Vector/SVG icons with dark mode support** → `background` (shape with `@color/` reference) + `src` (vector drawable) + `app:tint` (`@color/` reference). This combination is the dark mode best practice: background color, icon, and tint all follow theme via color resources, no need for separate light/dark assets
- A tappable area larger than the icon → wrap in a container or use padding

**Dark mode trend:** As more projects adopt dark mode, the `background + vector + tint` pattern will become more common. When generating code for a project that supports dark mode (detected via scan or user context), prefer this pattern over plain `src` for icon containers:
```xml
<!-- Dark mode friendly icon container -->
<ImageView
    android:layout_width="32dp"
    android:layout_height="32dp"
    android:background="@drawable/bg_icon_circle"
    app:srcCompat="@drawable/ic_settings"
    app:tint="@color/icon_primary" />
```
All three attributes reference theme-aware resources, so light/dark switching is automatic.

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="16dp">

    <TextView
        android:id="@+id/tvTitle"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="标题"
        android:textSize="17sp"
        android:textColor="#0F0F0F"
        android:textStyle="bold"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toStartOf="@id/ivArrow" />

    <ImageView
        android:id="@+id/ivArrow"
        android:layout_width="24dp"
        android:layout_height="24dp"
        android:src="@drawable/placeholder"
        app:layout_constraintTop_toTopOf="@id/tvTitle"
        app:layout_constraintBottom_toBottomOf="@id/tvTitle"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

Key constraint patterns:
- **Centering**: `constraintTop_toTopOf + constraintBottom_toBottomOf` same target
- **Chains**: horizontal/vertical chains for distributing elements
- **0dp (match_constraints)**: fill available space between constraints
- **Guidelines**: use for percentage-based positioning
- **Barrier**: align to the largest of a group

## Auto-layout Mapping

| Figma Property | XML Equivalent |
|---|---|
| layoutMode: VERTICAL | LinearLayout vertical / ConstraintLayout vertical chain |
| layoutMode: HORIZONTAL | LinearLayout horizontal / ConstraintLayout horizontal chain |
| itemSpacing | marginTop/marginStart on children |
| padding* | android:padding on parent |
| primaryAxisAlignItems: CENTER | gravity=center / chain spread_inside |
| counterAxisAlignItems: CENTER | gravity=center_vertical/horizontal |
| layoutGrow: 1 | layout_weight=1 (Linear) / 0dp + constraints (Constraint) |
| primaryAxisSizingMode: FIXED | layout_height/width = exact dp |
| counterAxisSizingMode: AUTO | layout_width/height = wrap_content |

## Size Conversion

- Figma px → Android dp (1:1)
- Figma font px → Android sp (1:1)

## Width Strategy — Fixed vs Flexible

Figma 设计稿通常基于 375px 宽画布。Figma 里的宽度值是**计算结果**，不是设计意图。需要反推意图来决定 Android 属性。

核心问题：**这个元素的宽度是"固定尺寸"还是"填满剩余空间"？**

### 规则 1：单个元素撑满屏幕宽度
元素宽度 + 左右偏移 ≈ 屏幕宽度（375），且左右边距对称或近似对称 → `match_parent` + `marginHorizontal`

- 例：宽 335 + 左 20 + 右 20 = 375 → `match_parent` + `marginHorizontal="20dp"`
- **经验阈值**：宽度占屏幕 >85% 且左右边距近似对称 → 优先 `match_parent` + margin
- 适配优势：不同屏幕宽度下自动拉伸

### 规则 2：并排元素中识别"弹性方"
多个元素横向排列时，判断每个元素是**固定方**还是**弹性方**：

- **固定方**：有明确视觉尺寸的元素——头像、图标、按钮、固定宽度标签等。用固定 dp 值。
- **弹性方**：宽度 = 屏幕宽 - 固定方宽度 - 各间距的元素——通常是文本、描述、内容区域。用 `0dp`（match_constraints）+ 约束填满剩余空间。

判断方法：计算 `固定方宽度 + 弹性方宽度 + 所有间距 ≈ 屏幕宽度` 是否成立。如果成立，弹性方不应写死宽度。

- 例：头像 56dp + 间距 16dp + 文本 263dp + 右边距 20dp + 左边距 20dp = 375
  → 头像是固定方（56dp），文本是弹性方
  → 文本：`layout_width="0dp"` + `constraintStart_toEndOf="@id/ivAvatar"` + `constraintEnd_toEndOf="parent"` + `marginStart="16dp"` + `marginEnd="20dp"`
- 例：标签 "姓名" 40dp + 间距 12dp + 输入框 283dp + 右边距 20dp + 左边距 20dp = 375
  → 标签固定，输入框弹性

### 规则 3：固定宽度 + 居中
元素明显比屏幕窄，且居中放置，不靠左右边缘 → 固定宽度 + 居中约束

- 例：宽 295 居中在 375 里 → `layout_width="295dp"` + `constraintStart/End` 居中
- 适用于输入框、小卡片等独立居中的元素

### RecyclerView item 宽度
- item 布局始终用 `match_parent`，宽度由 RecyclerView 本身控制
- RecyclerView 自身的宽度按上述规则判断

## Shadow Mapping

```xml
<!-- Use MaterialCardView for elevation shadow -->
<com.google.android.material.card.MaterialCardView
    app:cardElevation="4dp"
    app:cardCornerRadius="12dp">
```

For custom shadows (specific color/offset): use `android:elevation` + `android:outlineSpotShadowColor` (API 28+) or a drawable background with shadow layer.

## Gradient Mapping

```xml
<!-- Define in drawable XML -->
<shape>
    <gradient
        android:startColor="#FF6B6B"
        android:endColor="#4ECDC4"
        android:angle="90" />
</shape>
```
