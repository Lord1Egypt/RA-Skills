# Microsoft Fluent Design System

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Spacing and Grid](#4-spacing-and-grid)
5. [Corner Radius and Shape](#5-corner-radius-and-shape)
6. [Shadow and Depth](#6-shadow-and-depth)
7. [Motion Specifications](#7-motion-specifications)
8. [Component Specifications](#8-component-specifications)
9. [Platform Differences](#9-platform-differences)
10. [Token Reference Table](#10-token-reference-table)

---

## 1. Design Principles

### 1.1 Light

- Use light to guide attention
- Highlight important content and interactive elements
- Create depth through lighting effects
- Avoid overuse; maintain restraint

### 1.2 Depth

- Use the z-axis to create hierarchical relationships
- Foreground elements are closer to the user, background elements are farther
- Express depth through shadows and layers
- Depth changes suggest interaction and state

### 1.3 Motion

- Motion helps users understand interface changes
- Use physical metaphors (spring, inertia)
- Maintain smoothness and responsiveness
- Support reduced motion preference

### 1.4 Material

- Interface elements have physical texture
- Use Acrylic and Mica material effects
- Background blur and transparency create depth
- Material responds to lighting changes

### 1.5 Scale

- Design should adapt to different screen sizes
- From phones to large displays
- Use responsive layouts and breakpoints
- Both touch and keyboard/mouse input must be supported

---

## 2. Color System

> **Note**: The following lists only the Fluent default classic palette as a reference. Complete brand and theme colors are defined in the separate color specification skill.

### 2.1 Brand Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| brandBackground | `#0078D4` | `#0078D4` | Brand background |
| brandBackgroundHover | `#006CBE` | `#006CBE` | Brand hover |
| brandBackgroundPressed | `#005BA1` | `#005BA1` | Brand pressed |
| brandBackgroundSelected | `#0078D4` | `#0078D4` | Brand selected |
| brandForeground | `#0078D4` | `#0078D4` | Brand foreground |
| brandForegroundHover | `#006CBE` | `#006CBE` | Brand foreground hover |
| brandForegroundPressed | `#005BA1` | `#005BA1` | Brand foreground pressed |
| brandStroke | `#0078D4` | `#0078D4` | Brand stroke |

### 2.2 Neutral Foreground

| Token | Light | Dark | Usage |
|---|---|---|---|
| neutralForeground1 | `#242424` | `#FFFFFF` | Primary text |
| neutralForeground2 | `#424242` | `#D6D6D6` | Secondary text |
| neutralForeground3 | `#616161` | `#ADADAD` | Tertiary text |
| neutralForeground4 | `#707070` | `#999999` | Disabled text |
| neutralForegroundDisabled | `#BDBDBD` | `#5C5C5C` | Disabled |
| neutralForegroundInverted | `#FFFFFF` | `#242424` | Inverted text |

### 2.3 Neutral Background

| Token | Light | Dark | Usage |
|---|---|---|---|
| neutralBackground1 | `#FFFFFF` | `#292929` | Primary background |
| neutralBackground2 | `#FAFAFA` | `#1F1F1F` | Secondary background |
| neutralBackground3 | `#F5F5F5` | `#141414` | Tertiary background |
| neutralBackground4 | `#F0F0F0` | `#0A0A0A` | Quaternary background |
| neutralBackground5 | `#EBEBEB` | `#000000` | Quinary background |
| neutralBackgroundDisabled | `#F0F0F0` | `#141414` | Disabled background |
| neutralBackgroundInverted | `#292929` | `#FFFFFF` | Inverted background |

### 2.4 Neutral Stroke

| Token | Light | Dark | Usage |
|---|---|---|---|
| neutralStroke1 | `#D1D1D1` | `#666666` | Primary stroke |
| neutralStroke2 | `#E0E0E0` | `#525252` | Secondary stroke |
| neutralStroke3 | `#F5F5F5` | `#3D3D3D` | Tertiary stroke |
| neutralStrokeAccessible | `#616161` | `#ADADAD` | Accessible stroke |
| neutralStrokeDisabled | `#E0E0E0` | `#424242` | Disabled stroke |

### 2.5 Status Colors

| State | Light | Dark | Usage |
|---|---|---|---|
| Success | `#107C10` | `#54B054` | Success |
| Success Background | `#DFF6DD` | `#052505` | Success background |
| Warning | `#FFC107` | `#FDBA3B` | Warning |
| Warning Background | `#FFF4CE` | `#3B3A00` | Warning background |
| Error | `#D13438` | `#E9838A` | Error |
| Error Background | `#FDE7E9` | `#3B0505` | Error background |
| Info | `#0099BC` | `#60CDFF` | Info |
| Info Background | `#CCECF5` | `#002B3D` | Info background |

### 2.6 Fill Colors (State Layers)

| State | Light | Dark |
|---|---|---|
| rest | `#FFFFFF` | `#292929` |
| hover | `#F5F5F5` | `#3D3D3D` |
| pressed | `#E0E0E0` | `#525252` |
| selected | `#E0E0E0` | `#525252` |
| disabled | `#F0F0F0` | `#141414` |

### 2.7 Color Usage Principles

- Use neutral colors to build the interface skeleton
- Use theme colors to emphasize brand and primary operations
- Use semantic colors to convey status and feedback
- Ensure all text contrast >= 4.5:1
- Support high contrast mode

---

## 3. Typography

### 3.1 Font Family

- **Primary font**: Segoe UI
- **Monospace font**: Cascadia Code / Consolas
- **Fallback fonts**: `"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif`

### 3.2 Type Ramp

| Token | Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| Hero | 28pt | Semibold | 36pt | Page large title |
| Title | 24pt | Semibold | 32pt | Page title |
| Subtitle | 20pt | Regular | 28pt | Subtitle |
| Body | 14pt | Regular | 20pt | Body text |
| Caption | 12pt | Regular | 16pt | Description text |
| Caption2 | 10pt | Regular | 14pt | Extra small text |

### 3.3 Font Weights

| Weight | Value | Usage |
|---|---|---|
| Regular | 400 | Body text, labels |
| Semibold | 600 | Titles, buttons, emphasis |
| Bold | 700 | Strong emphasis, numbers |

### 3.4 Typography Principles

- Body text uses 14pt for readability
- Titles use Semibold, not Bold
- Line height at least 1.4 times font size
- Use font ramp for consistency
- Support text scaling up to 200%

---

## 4. Spacing and Grid

### 4.1 Base Grid

- **Base unit**: 4px
- All spacing and sizes should be multiples of 4

### 4.2 Standard Spacing Values

| Token | Value | Usage |
|---|---|---|
| none | 0px | No spacing |
| xxSmall | 2px | Very tight |
| xSmall | 4px | Internal icon spacing |
| small | 8px | Tight elements |
| medium | 12px | Default spacing |
| large | 16px | Standard padding |
| xLarge | 20px | Component spacing |
| xxLarge | 24px | Section spacing |
| xxxLarge | 32px | Large section |
| huge | 48px | Page spacing |

### 4.3 Layout Grid

| Breakpoint | Width | Columns | Spacing |
|---|---|---|---|
| Small | < 640px | 1-2 | 16px |
| Medium | 640-1024px | 2-4 | 24px |
| Large | 1024-1440px | 4-6 | 32px |
| XLarge | > 1440px | 6-12 | 48px |

### 4.4 Margin Specifications

| Scenario | Margin |
|---|---|
| Page horizontal margin | 16px (small screen) / 24px (medium screen) / 32px (large screen) |
| Card padding | 16px |
| Button padding | 12px horizontal, 6-8px vertical |
| List item padding | 12px horizontal, 8px vertical |
| Form field spacing | 16px |

---

## 5. Corner Radius and Shape

### 5.1 Corner Radius Tokens

| Token | Value | Usage |
|---|---|---|
| none | 0px | Right angle |
| small | 2px | Very small corner radius |
| medium | 4px | Small buttons, input fields |
| large | 6px | Standard buttons, cards |
| xLarge | 8px | Large cards, dialogs |
| circular | 9999px | Avatars, badges, capsule buttons |

### 5.2 Corner Radius Principles

- Small elements use small corner radius (2-4px)
- Large containers use large corner radius (6-8px)
- Capsule-shaped elements use circular
- Nested element corner radius should be smaller than parent container

---

## 6. Shadow and Depth

### 6.1 Depth System

Fluent uses a depth system to express hierarchical relationships:

| Token | Value | Usage |
|---|---|---|
| shadow2 | `0 1px 2px rgba(0,0,0,0.14)` | Slight elevation |
| shadow4 | `0 2px 4px rgba(0,0,0,0.14)` | Small card |
| shadow8 | `0 4px 8px rgba(0,0,0,0.14)` | Card |
| shadow16 | `0 8px 16px rgba(0,0,0,0.14)` | Dialog |
| shadow28 | `0 14px 28px rgba(0,0,0,0.14)` | Large dialog |
| shadow64 | `0 32px 64px rgba(0,0,0,0.14)` | Full-screen overlay |

### 6.2 Material Effects

**Acrylic**:
- Background blur + noise texture + color overlay
- Used for sidebar, navigation, dialog backgrounds
- Allows underlying content to be faintly visible

**Mica**:
- Lighter background effect
- Uses desktop wallpaper tones
- Used for window backgrounds

### 6.3 Depth Principles

- Use shadows to express the elevated feel of interactive elements
- Static elements do not use shadows
- Modal layers use higher depth values
- Depth changes suggest interaction states

---

## 7. Motion Specifications

### 7.1 Animation Duration

| Type | Duration | Usage |
|---|---|---|
| Instant feedback | 100ms | Button press, switch toggle |
| Fast transition | 150ms | Color change, state switch |
| Standard transition | 200ms | Element show/hide |
| Complex animation | 300ms | Page transition, dialog |
| Large movement | 500ms | Large element movement |

### 7.2 Easing Functions

| Name | Curve | Usage |
|---|---|---|
| Decelerate | `cubic-bezier(0, 0, 0, 1)` | Element entry |
| Accelerate | `cubic-bezier(1, 0, 1, 1)` | Element exit |
| Standard | `cubic-bezier(0.33, 0, 0.67, 1)` | Standard transition |

### 7.3 Motion Principles

- Motion should help users understand interface changes
- Use physical metaphors
- Maintain 60fps
- Support reduced motion preference
- Use clear animation for focus changes

---

## 8. Component Specifications

### 8.1 Button

**Fluent Name**: Button

**Anatomy**:
```
Button
├── Background
├── Label (Text)
└── Icon (optional)
```

**Size Specifications**:

| Variant | Height | Horizontal Padding | Corner Radius |
|---|---|---|---|
| Small | 24px | 8px | 4px |
| Medium (default) | 32px | 12px | 4px |
| Large | 40px | 16px | 4px |

**States**:

| State | Background | Text | Border | Description |
|---|---|---|---|---|
| Default | neutralBackground1 | neutralForeground1 | neutralStroke1 | Default |
| Hover | neutralBackground2 | neutralForeground1 | neutralStroke1 | Hover |
| Pressed | neutralBackground3 | neutralForeground1 | neutralStrokeAccessible | Pressed |
| Disabled | neutralBackgroundDisabled | neutralForegroundDisabled | neutralStrokeDisabled | Disabled |
| Focused | neutralBackground1 | neutralForeground1 | brandStroke + 1px outline | Focused |

**Variants**:
- **Default**: White background, gray border
- **Primary**: Brand color background, white text
- **Subtle**: Transparent background, gray background on hover
- **Transparent**: Fully transparent, text and icon only
- **Outline**: Transparent background, brand color border

**Accessibility**:
- Minimum touch target: 32x32px
- Color contrast ratio >= 4.5:1
- Support keyboard focus
- Focus indicator clearly visible

---

### 8.2 TextField

**Fluent Name**: Input

**Anatomy**:
```
Input
├── Background
├── Border
├── Placeholder Text
├── Input Text
├── Leading Icon (optional)
└── Trailing Icon / Action (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 32px |
| Horizontal padding | 12px |
| Corner radius | 4px |
| Border | 1px solid neutralStroke1 |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | neutralStroke1 | neutralBackground1 | Default |
| Hover | neutralStrokeAccessible | neutralBackground1 | Hover |
| Focused | brandStroke | neutralBackground1 | Focused |
| Filled | neutralStroke1 | neutralBackground1 | Has content |
| Error | error | neutralBackground1 | Error |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | Disabled |

**Accessibility**:
- Associate with label
- Error state provides aria-invalid
- Support keyboard navigation

---

### 8.3 Checkbox

**Fluent Name**: Checkbox

**Anatomy**:
```
Checkbox
├── Box (square)
│   └── Checkmark (optional)
└── Label (Text)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Box size | 16x16px |
| Box corner radius | 2px |
| Label spacing | 8px |
| Checkmark line width | 2px |

**States**:

| State | Box Background | Border | Checkmark | Description |
|---|---|---|---|---|
| Unchecked | transparent | neutralStrokeAccessible | None | Unselected |
| Checked | brandBackground | brandBackground | white | Selected |
| Mixed | brandBackground | brandBackground | white line | Mixed |
| Hover (unchecked) | neutralBackground2 | neutralStrokeAccessible | None | Hover |
| Hover (checked) | brandBackgroundHover | brandBackgroundHover | white | Hover checked |
| Disabled | neutralBackgroundDisabled | neutralStrokeDisabled | neutralForegroundDisabled | Disabled |

---

### 8.4 RadioButton

**Fluent Name**: Radio

**Anatomy**:
```
Radio
├── Circle
│   └── Inner Dot (optional)
└── Label (Text)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Outer circle diameter | 16px |
| Inner dot diameter | 8px |
| Border width | 1px |
| Label spacing | 8px |

**States**:

| State | Outer Circle | Inner Dot | Description |
|---|---|---|---|
| Unselected | transparent + neutralStrokeAccessible | None | Unselected |
| Selected | transparent + brandBackground | brandBackground | Selected |
| Hover | neutralBackground2 | Same | Hover |
| Disabled | neutralStrokeDisabled | neutralForegroundDisabled | Disabled |

---

### 8.5 Switch

**Fluent Name**: Switch

**Anatomy**:
```
Switch
├── Track (pill shape)
└── Thumb (circle)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Track width | 40px |
| Track height | 20px |
| Thumb diameter | 14px |
| Thumb margin | 3px |

**States**:

| State | Track | Thumb | Description |
|---|---|---|---|
| Off | neutralStrokeAccessible | neutralBackground1 | Off |
| On | brandBackground | neutralBackground1 | On |
| Hover (off) | neutralStroke1 | neutralBackground2 | Hover off |
| Hover (on) | brandBackgroundHover | neutralBackground1 | Hover on |
| Disabled (off) | neutralStrokeDisabled | neutralBackgroundDisabled | Disabled off |
| Disabled (on) | brandBackground + 40% opacity | neutralBackgroundDisabled | Disabled on |

**Motion**:
- Toggle animation: 150ms standard easing

---

### 8.6 Slider

**Fluent Name**: Slider

**Anatomy**:
```
Slider
├── Track (background)
├── Fill (value)
└── Thumb (handle)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Track height | 4px |
| Track corner radius | 2px |
| Thumb diameter | 16px |
| Minimum touch area | 32x32px |

**States**:

| State | Fill | Thumb | Description |
|---|---|---|---|
| Default | brandBackground | neutralBackground1 + shadow2 | Default |
| Hover | brandBackground | neutralBackground2 + shadow4 | Hover |
| Pressed | brandBackgroundPressed | neutralBackground3 + shadow2 | Pressed |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | Disabled |

---

### 8.7 ProgressIndicator

**Fluent Name**: Progress Bar

**Anatomy**:
```
ProgressBar
├── Track (background)
└── Indicator (fill / spinner)
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Linear | Height 2px, width adapts |
| Circular | Diameter 16px / 24px / 32px |

**Linear Progress Bar**:
- Track: neutralBackground3
- Fill: brandBackground
- Corner radius: 1px

**Circular Progress Bar**:
- Line width: 2px
- Color: brandBackground
- Rotation animation: 1.5s linear infinite

**Indeterminate State**:
- Linear: Loop animation
- Circular: Continuous rotation

---

### 8.8 Menu

**Fluent Name**: Menu

**Anatomy**:
```
Menu
├── Menu Item
│   ├── Icon (optional)
│   ├── Label
│   ├── Shortcut (optional)
│   └── Submenu Arrow (optional)
├── Divider
└── Menu Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 160px |
| Maximum width | 320px |
| Item height | 32px |
| Item padding | 12px horizontal |
| Corner radius | 4px |
| Shadow | shadow8 |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | neutralForeground1 | Default |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Pressed | neutralBackground3 | neutralForeground1 | Pressed |
| Disabled | transparent | neutralForegroundDisabled | Disabled |

---

### 8.9 Dialog

**Fluent Name**: Dialog

**Anatomy**:
```
Dialog
├── Title
├── Content
├── TextField (optional)
└── Actions
    ├── Primary Action
    └── Secondary Action
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 288px |
| Maximum width | 600px |
| Corner radius | 8px |
| Padding | 24px |
| Title to content spacing | 8px |
| Content to button spacing | 24px |

**Background**:
- Dialog background: neutralBackground1 + Acrylic effect
- Overlay: black 40% opacity

**Button Layout**:
- Primary action on the left (Fluent convention)
- Secondary action on the right
- 3+ buttons vertically arranged

---

### 8.10 Card

**Fluent Name**: Card

**Anatomy**:
```
Card
├── Background
├── Header (optional)
├── Content
├── Footer (optional)
└── Actions (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Corner radius | 4px |
| Padding | 16px |
| Background | neutralBackground1 |
| Border | 1px solid neutralStroke1 |
| Shadow | None (static) |

**Hover State**:
- Shadow: shadow4
- Background: neutralBackground2

**Selected State**:
- Border: brandStroke
- Shadow: shadow4

---

### 8.11 List

**Fluent Name**: List

**Anatomy**:
```
List
├── List Item
│   ├── Icon (optional)
│   ├── Content
│   │   ├── Title
│   │   └── Description (optional)
│   ├── Detail (optional)
│   └── Actions (optional)
└── List Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item height | 40px |
| Item padding | 12px horizontal, 8px vertical |
| Separator | 1px solid neutralStroke2 |

**States**:

| State | Background | Description |
|---|---|---|
| Default | transparent | Default |
| Hover | neutralBackground2 | Hover |
| Selected | brandBackground + 10% | Selected |
| Pressed | neutralBackground3 | Pressed |

---

### 8.12 NavigationBar

**Fluent Name**: Navigation

**Anatomy**:
```
Navigation
├── Brand / Logo (optional)
├── Navigation Items
│   └── Item
└── Actions (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 48px |
| Background | neutralBackground1 / Acrylic |
| Item font | Body 14pt |
| Item spacing | 8px |

**Vertical Navigation (Sidebar)**:
- Width: 260px
- Item height: 36px
- Item corner radius: 4px
- Selected indicator: Left 3px brand color bar

---

### 8.13 TabBar

**Fluent Name**: Tab

**Anatomy**:
```
Tab
├── Tab List
│   └── Tab Item
└── Tab Panel
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item height | 36px |
| Item padding | 12px horizontal |
| Item corner radius | 4px |
| Selected indicator | Bottom 2px brand color bar |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Selected | transparent | brandForeground | Selected |
| Unselected | transparent | neutralForeground2 | Unselected |
| Hover | neutralBackground2 | neutralForeground1 | Hover |

---

### 8.14 SegmentedControl

**Fluent Name**: No direct equivalent; use Tab or Toggle as substitute

---

### 8.15 Tooltip

**Fluent Name**: Tooltip

**Anatomy**:
```
Tooltip
├── Background
└── Label
```

**Size Specifications**:

| Property | Value |
|---|---|
| Maximum width | 240px |
| Padding | 8px 12px |
| Corner radius | 4px |
| Font | Caption 12pt |
| Background | neutralBackgroundInverted |
| Text | neutralForegroundInverted |

**Behavior**:
- Shows after 500ms hover
- Hides 0ms after leaving target
- Arrow points to target element

---

### 8.16 Badge

**Fluent Name**: Badge

**Anatomy**:
```
Badge
├── Background
└── Label (number / dot)
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Dot | 8x8px |
| Number | Height 16px, width adapts |

**Number Badge**:
- Height: 16px
- Minimum width: 16px
- Padding: 4px horizontal
- Corner radius: 8px (full)
- Background: brandBackground
- Text: white, Caption 10pt

---

### 8.17 Chip

**Fluent Name**: Tag

**Anatomy**:
```
Tag
├── Background
├── Icon (optional)
├── Label
└── Dismiss Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 24px |
| Horizontal padding | 8px |
| Corner radius | 4px |
| Background | neutralBackground2 |
| Text | neutralForeground1 |

**States**:

| State | Background | Description |
|---|---|---|
| Default | neutralBackground2 | Default |
| Selected | brandBackground + 10% | Selected |
| Hover | neutralBackground3 | Hover |

---

### 8.18 DatePicker

**Fluent Name**: Date Picker

**Anatomy**:
```
DatePicker
├── Header (month / year)
├── Weekday Labels
└── Day Grid
    └── Day Cell
```

**Size Specifications**:

| Property | Value |
|---|---|
| Cell size | 32x32px |
| Cell spacing | 2px |
| Selected background | brandBackground circle |
| Today marker | brandStroke border circle |

---

### 8.19 Table

**Fluent Name**: Data Grid

**Anatomy**:
```
DataGrid
├── Table Header
│   └── Column Header
├── Table Row
│   └── Cell
└── Table Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Row height | 40px |
| Header height | 32px |
| Cell padding | 12px horizontal |
| Separator | 1px solid neutralStroke2 |

**Table Header**:
- Font: Body 14pt Semibold
- Color: neutralForeground1
- Background: neutralBackground2

**Row States**:

| State | Background | Description |
|---|---|---|
| Default | transparent | Default |
| Hover | neutralBackground2 | Hover |
| Selected | brandBackground + 10% | Selected |
| Alternate | neutralBackground2 | Zebra striping (optional) |

---

### 8.20 Breadcrumb

**Fluent Name**: Breadcrumb

**Anatomy**:
```
Breadcrumb
├── Item
│   ├── Icon (optional)
│   └── Label
├── Separator
└── Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item font | Body 14pt |
| Separator | "/" |
| Separator color | neutralStrokeAccessible |
| Current item | neutralForeground1 |
| Clickable item | brandForeground |

---

### 8.21 Select

**Fluent Name**: Dropdown / Combobox

**Anatomy**:
```
Dropdown
├── Trigger
│   ├── Selected Value (Text)
│   └── Chevron Icon
└── Listbox (popup)
    ├── Option
    │   ├── Checkmark (optional)
    │   └── Label
    └── Option...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Trigger height | 32px |
| Horizontal padding | 12px |
| Corner radius | 4px |
| Border | 1px solid neutralStroke1 |
| List minimum width | Same as trigger |
| List maximum height | 320px |
| Option height | 32px |
| List shadow | shadow8 |

**States**:

| State | Border | Background | Text | Description |
|---|---|---|---|---|
| Default | neutralStroke1 | neutralBackground1 | neutralForeground1 | Default |
| Hover | neutralStrokeAccessible | neutralBackground1 | neutralForeground1 | Hover |
| Focused | brandStroke | neutralBackground1 | neutralForeground1 | Focused |
| Open | brandStroke | neutralBackground1 | neutralForeground1 | Expanded |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | neutralForegroundDisabled | Disabled |

**Option States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | neutralForeground1 | Default |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Selected | neutralBackground3 | neutralForeground1 | Selected (with checkmark) |

**Accessibility**:
- Associate with label, role="combobox"
- List role="listbox", options role="option"
- Support keyboard up/down navigation, Enter to select, Esc to close
- aria-expanded reflects expansion state

---

### 8.22 Autocomplete

**Fluent Name**: Combobox (editable mode)

**Anatomy**:
```
Combobox
├── Input
│   ├── Editable Text
│   └── Chevron Icon
└── Listbox (filtered popup)
    ├── Option (matched, highlight matching segment)
    └── Option...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Input height | 32px |
| Horizontal padding | 12px |
| Corner radius | 4px |
| Border | 1px solid neutralStroke1 |
| List maximum height | 320px |
| Option height | 32px |
| List shadow | shadow8 |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | neutralStroke1 | neutralBackground1 | Default |
| Hover | neutralStrokeAccessible | neutralBackground1 | Hover |
| Focused | brandStroke | neutralBackground1 | Focused (editable) |
| Filtering | brandStroke | neutralBackground1 | Filtering on input |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | Disabled |

**Match Highlight**:
- Matched segment: brandForeground, Semibold
- Remaining text: neutralForeground1

**Accessibility**:
- role="combobox", aria-autocomplete="list"
- Instant filtering on input, aria-activedescendant indicates highlighted item
- Support keyboard up/down navigation, Enter to confirm, Esc to clear

---

### 8.23 Textarea

**Fluent Name**: Textarea

**Anatomy**:
```
Textarea
├── Background
├── Border
├── Input Text (multi-line)
└── Resize Handle (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 60px |
| Horizontal padding | 12px |
| Vertical padding | 8px |
| Corner radius | 4px |
| Border | 1px solid neutralStroke1 |
| Font | Body 14pt |
| Line height | 20px |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | neutralStroke1 | neutralBackground1 | Default |
| Hover | neutralStrokeAccessible | neutralBackground1 | Hover |
| Focused | brandStroke | neutralBackground1 | Focused |
| Filled | neutralStroke1 | neutralBackground1 | Has content |
| Error | error | neutralBackground1 | Error |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | Disabled |

**Variants**:
- **Fixed**: Fixed height, internal scroll
- **Auto-grow**: Auto-increases with content
- **Resizable**: Bottom-right drag handle for manual adjustment

**Accessibility**:
- Associate with label, multi-line text support
- Error state provides aria-invalid
- Character limit indicated via aria-describedby

---

### 8.24 NumberInput

**Fluent Name**: SpinButton

**Anatomy**:
```
SpinButton
├── Background
├── Border
├── Input Text (numeric)
└── Stepper
    ├── Increment Button (▲)
    └── Decrement Button (▼)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 32px |
| Horizontal padding | 12px |
| Corner radius | 4px |
| Border | 1px solid neutralStroke1 |
| Stepper button width | 24px |
| Stepper button height | 16px (each half) |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | neutralStroke1 | neutralBackground1 | Default |
| Hover | neutralStrokeAccessible | neutralBackground1 | Hover |
| Focused | brandStroke | neutralBackground1 | Focused |
| Error | error | neutralBackground1 | Out of range |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | Disabled |

**Stepper Button States**:

| State | Background | Icon | Description |
|---|---|---|---|
| Default | transparent | neutralForeground2 | Default |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Pressed | neutralBackground3 | neutralForeground1 | Pressed |
| Disabled | transparent | neutralForegroundDisabled | Reached boundary |

**Accessibility**:
- role="spinbutton", aria-valuenow / aria-valuemin / aria-valuemax
- Support keyboard up/down arrows to step, Page Up/Down for large steps
- Minimum touch target: 32x32px

---

### 8.25 Upload

**Fluent Name**: No native component; the following is a reasonable implementation derived from Fluent design language (based on Button + List)

**Anatomy**:
```
Upload
├── Drop Zone
│   ├── Icon
│   ├── Prompt Text
│   └── Browse Button
└── File List
    └── File Item
        ├── File Icon
        ├── File Name + Size
        ├── Progress Bar
        └── Remove Button
```

**Size Specifications**:

| Property | Value |
|---|---|
| Drop zone minimum height | 120px |
| Drop zone padding | 24px |
| Drop zone corner radius | 8px |
| Drop zone border | 1px dashed neutralStroke1 |
| File item height | 48px |
| File item padding | 12px horizontal, 8px vertical |
| File item corner radius | 4px |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | neutralStroke1 (dashed) | neutralBackground2 | Default |
| Hover | neutralStrokeAccessible (dashed) | neutralBackground3 | Hover |
| Dragover | brandStroke (dashed) | neutralBackground3 | Dragging in |
| Disabled | neutralStrokeDisabled (dashed) | neutralBackgroundDisabled | Disabled |

**File Item States**:

| State | Progress Bar | Description |
|---|---|---|
| Uploading | brandBackground | Uploading |
| Success | success | Complete |
| Error | error | Failed |

**Accessibility**:
- Browse button keyboard focusable
- Drop zone provides text prompt and alternative click-to-upload
- Upload progress announced via aria-live

---

### 8.26 Toast

**Fluent Name**: Toast

**Anatomy**:
```
Toast
├── Background (Acrylic)
├── Status Icon (optional)
├── Content
│   ├── Title
│   └── Body (optional)
├── Action (optional)
└── Dismiss Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 288px |
| Maximum width | 360px |
| Padding | 12px 16px |
| Corner radius | 6px |
| Shadow | shadow16 |
| Background | neutralBackground1 + Acrylic |
| Title font | Body 14pt Semibold |
| Body font | Caption 12pt |

**Variants**:

| Variant | Status Icon Color | Description |
|---|---|---|
| Info | info | General information |
| Success | success | Success |
| Warning | warning | Warning |
| Error | error | Error |

**Behavior**:
- Default display 4-6 seconds then auto-dismiss
- Entry: Decelerate easing, 200ms
- Exit: Accelerate easing, 150ms
- Typically stacked at bottom-right of screen

**Accessibility**:
- role="status" (info/success) or role="alert" (warning/error)
- aria-live auto-announces
- Can pause auto-dismiss (on hover)

---

### 8.27 Notification

**Fluent Name**: No independent component; the following is a reasonable implementation derived from Fluent design language (notification based on MessageBar)

**Anatomy**:
```
Notification
├── Background
├── Status Icon
├── Content
│   ├── Title
│   ├── Body
│   └── Timestamp (optional)
├── Actions (optional)
└── Dismiss Button
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 320px |
| Maximum width | 400px |
| Padding | 12px 16px |
| Corner radius | 6px |
| Shadow | shadow8 |
| Background | neutralBackground1 |
| Border | 1px solid neutralStroke2 |
| Title font | Body 14pt Semibold |
| Body font | Caption 12pt |
| Timestamp font | Caption2 10pt, neutralForeground3 |

**Variants**:

| Variant | Status Icon Color | Description |
|---|---|---|
| Info | info | General notification |
| Success | success | Success notification |
| Warning | warning | Warning notification |
| Error | error | Error notification |

**Behavior**:
- Persistent display, requires manual close or action
- Multiple notifications stack vertically in notification center, 8px spacing

**Accessibility**:
- role="status", aria-live="polite"
- Close button aria-label="Close"
- Action buttons keyboard focusable

---

### 8.28 Alert / Banner

**Fluent Name**: MessageBar (inline embeddable prompt bar)

**Anatomy**:
```
MessageBar
├── Background
├── Status Icon
├── Message Text
├── Actions (optional)
└── Dismiss Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 32px |
| Horizontal padding | 12px |
| Vertical padding | 8px |
| Corner radius | 4px |
| Icon size | 16x16px |
| Icon to text spacing | 8px |
| Font | Body 14pt |

**Variants**:

| Variant | Background | Icon Color | Text | Description |
|---|---|---|---|---|
| Info | Info Background | info | neutralForeground1 | Information |
| Success | Success Background | success | neutralForeground1 | Success |
| Warning | Warning Background | warning | neutralForeground1 | Warning |
| Error | Error Background | error | neutralForeground1 | Error |

**Layout**:
- Single line: Icon + text + action horizontally arranged
- Multi-line: Text wraps, action on new line
- Width adapts to parent container

**Accessibility**:
- role="alert" (error/warning) or role="status" (info/success)
- Close button aria-label="Close"
- Color not the sole differentiator; paired with icon

---

### 8.29 Skeleton

**Fluent Name**: Skeleton

**Anatomy**:
```
Skeleton
├── Shape (rect / circle / line)
└── Shimmer Overlay
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Line (text) | Height 12px / 14px / 16px, corner radius 4px |
| Rectangle (block) | Adapts, corner radius 4px |
| Circle (avatar) | Diameter 32px / 40px, circular |

**Colors**:

| Element | Color |
|---|---|
| Base background | neutralBackground3 |
| Shimmer highlight | neutralBackground1 |

**Behavior**:
- Shimmer sweep animation: left to right, 1.5s linear infinite
- Multi-line text skeleton: line spacing 8px, last line width about 60%
- Support reduced motion preference (static background color)

**Accessibility**:
- aria-busy="true", remove after content loads
- Screen readers ignore skeleton (aria-hidden placeholder)

---

### 8.30 Drawer / Sidebar

**Fluent Name**: NavigationView / Drawer (Overlay mode)

**Anatomy**:
```
Drawer
├── Scrim (overlay backdrop)
└── Panel (Acrylic)
    ├── Header
    │   ├── Title
    │   └── Close Button
    ├── Content / Nav Items
    └── Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Panel width (side) | 320px |
| Panel height (side) | 100% |
| Padding | 16px |
| Corner radius | 0px (flush) |
| Shadow | shadow28 |
| Background | neutralBackground1 + Acrylic |
| Overlay | black 40% opacity |

**Variants**:

| Variant | Description |
|---|---|
| Overlay | Floats above content, with overlay |
| Inline | Pushes content aside, no overlay |
| Left / Right | Slides in from left or right |

**Behavior**:
- Entry: Decelerate easing, 300ms horizontal slide in
- Exit: Accelerate easing, 200ms slide out
- Click overlay or Esc to close (Overlay mode)

**Accessibility**:
- role="dialog" / aria-modal="true" (Overlay)
- Focus locked within panel
- Close button aria-label="Close"

---

### 8.31 Pagination

**Fluent Name**: No native component; the following is a reasonable implementation derived from Fluent design language

**Anatomy**:
```
Pagination
├── Previous Button (‹)
├── Page Buttons
│   ├── Page Number
│   └── Ellipsis (...)
├── Next Button (›)
└── Page Info (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Page button size | 32x32px |
| Button spacing | 4px |
| Corner radius | 4px |
| Font | Body 14pt |
| Page info font | Caption 12pt, neutralForeground3 |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | neutralForeground1 | Default |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Current | brandBackground | neutralForegroundInverted | Current page |
| Disabled | transparent | neutralForegroundDisabled | Unavailable (first/last) |

**Accessibility**:
- nav role, aria-label="Pagination"
- Current page aria-current="page"
- Previous/next button aria-label, disabled aria-disabled
- Minimum touch target: 32x32px (keyboard/mouse) / 44px (touch)

---

### 8.32 Stepper

**Fluent Name**: No native component; the following is a reasonable implementation derived from Fluent design language (wizard step bar)

**Anatomy**:
```
Stepper
├── Step
│   ├── Indicator (number / checkmark)
│   ├── Label
│   └── Description (optional)
├── Connector (line)
└── Step...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Indicator diameter | 24px |
| Indicator corner radius | circular |
| Connector line width | 2px |
| Step spacing | 16px |
| Label font | Body 14pt |
| Description font | Caption 12pt, neutralForeground3 |

**States**:

| State | Indicator Background | Indicator Content | Connector | Label | Description |
|---|---|---|---|---|---|
| Completed | brandBackground | checkmark (white) | brandBackground | neutralForeground1 | Completed |
| Current | brandBackground | number (white) | neutralStroke1 | neutralForeground1 Semibold | Current |
| Upcoming | neutralBackground3 | number (neutralForeground3) | neutralStroke1 | neutralForeground3 | Not reached |
| Error | Error Background | error icon | neutralStroke1 | error | Error |
| Disabled | neutralBackgroundDisabled | neutralForegroundDisabled | neutralStrokeDisabled | neutralForegroundDisabled | Disabled |

**Variants**:
- **Horizontal**: Steps arranged horizontally, connector lines horizontal
- **Vertical**: Steps arranged vertically, connector lines vertical

**Accessibility**:
- Current step aria-current="step"
- Step state conveyed through text and icon dual representation
- Support keyboard navigation between clickable steps

---

### 8.33 Sheet / ActionSheet

**Fluent Name**: No native bottom overlay; the following is a reasonable implementation derived from Fluent design language (bottom Drawer based on Dialog)

**Anatomy**:
```
Sheet
├── Scrim (overlay backdrop)
└── Panel (Acrylic)
    ├── Drag Handle
    ├── Header (optional)
    │   └── Title
    ├── Content / Action List
    │   └── Action Item
    └── Cancel Action (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Panel width | 100% |
| Maximum height | 90% viewport |
| Top corner radius | 8px |
| Padding | 16px |
| Shadow | shadow28 |
| Drag handle | Width 32px, height 4px, corner radius circular, neutralStroke1 |
| Action item height | 44px |
| Background | neutralBackground1 + Acrylic |
| Overlay | black 40% opacity |

**Action Item States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | neutralForeground1 | Default |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Pressed | neutralBackground3 | neutralForeground1 | Pressed |
| Destructive | transparent | error | Dangerous action |

**Behavior**:
- Entry: Decelerate easing, 300ms slide up from bottom
- Exit: Accelerate easing, 200ms slide down
- Supports drag handle downward to close, click overlay or Esc to close

**Accessibility**:
- role="dialog" / aria-modal="true"
- Focus locked within panel
- Action items keyboard focusable, minimum touch target 44px

---

### 8.34 Avatar

**Fluent Name**: Avatar / Persona

**Anatomy**:
```
Avatar
├── Container (circle / square)
│   ├── Image
│   ├── Initials (fallback)
│   └── Icon (fallback)
└── Presence Badge (optional)
```

**Size Specifications**:

| Variant | Diameter | Font |
|---|---|---|
| XSmall | 16px | Caption2 10pt |
| Small | 24px | Caption 12pt |
| Medium (default) | 32px | Body 14pt |
| Large | 40px | Subtitle 20pt |
| XLarge | 48px | Subtitle 20pt |

**Shape**:

| Shape | Corner Radius |
|---|---|
| Circular (default) | circular |
| Square | 4px |

**Presence Badge**:

| State | Color | Description |
|---|---|---|
| Available | success | Online |
| Away | warning | Away |
| Busy | error | Busy |
| Offline | neutralStrokeAccessible | Offline |

**Fallback Style**:
- Background: brandBackground
- Initials: neutralForegroundInverted

**Accessibility**:
- Image provides alt or aria-label (name)
- Presence state supplemented with text, not just color

---

### 8.35 Accordion

**Fluent Name**: Accordion

**Anatomy**:
```
Accordion
├── Item
│   ├── Header
│   │   ├── Chevron Icon
│   │   ├── Title
│   │   └── Icon (optional)
│   └── Panel (collapsible content)
└── Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Header height | 44px |
| Header padding | 12px horizontal |
| Panel padding | 12px 16px |
| Corner radius | 4px |
| Title font | Body 14pt Semibold |
| Divider | 1px solid neutralStroke2 |

**States**:

| State | Header Background | Text | Chevron | Description |
|---|---|---|---|---|
| Collapsed | transparent | neutralForeground1 | ▶ (right) | Collapsed |
| Expanded | neutralBackground2 | neutralForeground1 | ▼ (down) | Expanded |
| Hover | neutralBackground2 | neutralForeground1 | — | Hover |
| Disabled | transparent | neutralForegroundDisabled | — | Disabled |

**Behavior**:
- Expand/Collapse animation: 200ms standard easing, height transition
- Chevron rotation animation synchronized
- Supports single or multi-open modes

**Accessibility**:
- Header role="button", aria-expanded reflects state
- aria-controls associates panel
- Support keyboard Enter/Space to toggle

---

### 8.36 Carousel

**Fluent Name**: Carousel

**Anatomy**:
```
Carousel
├── Viewport
│   └── Slides Track
│       └── Slide
├── Previous Button (‹)
├── Next Button (›)
└── Indicators (dots)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Viewport width | 100% |
| Corner radius | 8px |
| Navigation button size | 32x32px |
| Navigation button corner radius | circular |
| Indicator dot diameter | 8px |
| Indicator dot spacing | 8px |

**States**:

| Element | State | Color | Description |
|---|---|---|---|
| Indicator dot | Active | brandBackground | Current page |
| Indicator dot | Inactive | neutralStroke1 | Other pages |
| Navigation button | Default | neutralBackground1 + shadow8 | Default |
| Navigation button | Hover | neutralBackground2 + shadow16 | Hover |
| Navigation button | Disabled | neutralBackgroundDisabled | Reached boundary |

**Behavior**:
- Transition animation: 300ms decelerate easing, horizontal slide
- Supports auto-rotation (pausable) and touch swipe
- Support reduced motion preference (fade in/out instead of slide)

**Accessibility**:
- role="region", aria-roledescription="carousel"
- Indicator dot aria-label="Slide N"
- Auto-rotating carousel provides pause control

---

### 8.37 Timeline

**Fluent Name**: No native component; the following is a reasonable implementation derived from Fluent design language

**Anatomy**:
```
Timeline
├── Item
│   ├── Node (dot / icon)
│   ├── Connector (line)
│   └── Content
│       ├── Title
│       ├── Description (optional)
│       └── Timestamp
└── Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Node diameter | 12px |
| Node corner radius | circular |
| Connector line width | 2px |
| Node to content spacing | 12px |
| Item spacing | 16px |
| Title font | Body 14pt Semibold |
| Description font | Body 14pt |
| Timestamp font | Caption 12pt, neutralForeground3 |

**States**:

| State | Node | Connector | Description |
|---|---|---|---|
| Completed | brandBackground | brandBackground | Occurred |
| Current | brandBackground + ring | neutralStroke1 | Current node |
| Upcoming | neutralBackground3 + neutralStroke1 border | neutralStroke1 | Future |
| Error | error | neutralStroke1 | Error node |

**Variants**:
- **Vertical** (default): Nodes arranged vertically
- **Alternate**: Content alternates left/right

**Accessibility**:
- Uses ordered list semantics (ol / li)
- Timestamp provides machine-readable datetime
- Node state supplemented with text

---

### 8.38 Tree

**Fluent Name**: TreeView

**Anatomy**:
```
TreeView
├── Tree Item
│   ├── Expand Chevron (if has children)
│   ├── Icon (optional)
│   ├── Label
│   └── Children (nested)
│       └── Tree Item...
└── Tree Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item height | 32px |
| Indent step | 16px |
| Chevron size | 16x16px |
| Item padding | 8px horizontal |
| Corner radius | 4px |
| Font | Body 14pt |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | neutralForeground1 | Default |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Selected | neutralBackground3 | neutralForeground1 | Selected |
| Focused | transparent | neutralForeground1 + brandStroke outline | Focused |
| Disabled | transparent | neutralForegroundDisabled | Disabled |

**Chevron State**:
- Collapsed: ▶ (pointing right)
- Expanded: ▼ (pointing down), rotation animation 150ms

**Accessibility**:
- role="tree", items role="treeitem"
- aria-expanded reflects expand state, aria-level reflects level
- Support keyboard up/down navigation, left/right expand/collapse

---

### 8.39 Divider

**Fluent Name**: Divider

**Anatomy**:
```
Divider
├── Line
└── Label (optional, centered/inset)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Line width | 1px |
| Color | neutralStroke2 |
| Default margin (horizontal) | 8px top and bottom |
| Default margin (vertical) | 8px left and right |
| Label font | Caption 12pt, neutralForeground3 |
| Label spacing on both sides | 12px |

**Variants**:

| Variant | Description |
|---|---|
| Horizontal (default) | Horizontal separator |
| Vertical | Vertical separator, height adapts |
| With Label | Text label embedded at center or start |
| Inset | Single side inset inset |

**Accessibility**:
- role="separator", aria-orientation reflects direction
- Purely decorative separators can use aria-hidden
- When carrying semantic grouping, associate with aria-label

---

### 8.40 Grid / Layout

**Fluent Name**: No native component; the following is a reasonable implementation derived from Fluent design language (responsive layout grid, based on section 4 layout grid breakpoints)

**Anatomy**:
```
Grid
├── Container (max-width)
└── Row
    └── Column (span)
        └── Content
```

**Breakpoints and Columns** (corresponding to section 4.3):

| Breakpoint | Width | Columns | Spacing |
|---|---|---|---|
| Small | < 640px | 1-2 | 16px |
| Medium | 640-1024px | 2-4 | 24px |
| Large | 1024-1440px | 4-6 | 32px |
| XLarge | > 1440px | 6-12 | 48px |

**Size Specifications**:

| Property | Value |
|---|---|
| Column spacing (gutter) | Varies by breakpoint 16/24/32/48px |
| Row spacing | 16px |
| Page horizontal margin | 16px (small) / 24px (medium) / 32px (large) |
| Column base | 12-column grid |

**Layout Principles**:
- All spacing is a multiple of the 4px grid
- Column width allocated by span ratio (e.g., 6/12 = half width)
- Nested grids inherit context spacing

**Accessibility**:
- Layout containers do not introduce additional semantics
- Reading order consistent with visual order
- Responsive breakpoints do not disrupt DOM order

---

### 8.41 Space / Stack

**Fluent Name**: Stack

**Anatomy**:
```
Stack
├── Child
├── Gap (spacing)
└── Child...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Spacing values | 4px grid (2/4/8/12/16/20/24/32/48) |
| Default spacing | 12px (medium) |
| Direction | horizontal / vertical |

**Spacing Token Mapping** (corresponding to section 4.2):

| Token | Value |
|---|---|
| xSmall | 4px |
| small | 8px |
| medium | 12px |
| large | 16px |
| xLarge | 20px |
| xxLarge | 24px |

**Alignment Options**:

| Property | Values |
|---|---|
| Main axis alignment | start / center / end / space-between |
| Cross axis alignment | start / center / end / stretch |
| Wrap | wrap / nowrap |

**Accessibility**:
- Purely layout container, no semantics introduced
- Child reading order consistent with DOM order

---

### 8.42 AspectRatio

**Fluent Name**: No native component; the following is a reasonable implementation derived from Fluent design language (aspect ratio container)

**Anatomy**:
```
AspectRatio
└── Container (ratio-locked)
    └── Content (image / video / embed)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Width | 100% (adapts to parent container) |
| Height | Derived from ratio |
| Corner radius | 4px (when containing media) |
| Overflow | hidden |

**Common Ratios**:

| Ratio | Usage |
|---|---|
| 1:1 | Avatar, square thumbnail |
| 4:3 | Traditional image |
| 16:9 | Video, wide image |
| 3:2 | Photo |
| 21:9 | Ultra-wide banner |

**Behavior**:
- Content fills via cover or contain
- Ratio locked, height scales proportionally when width changes

**Accessibility**:
- Container is layout only, no semantics introduced
- Internal media retain their own alt / title
- When in placeholder state, maintain ratio with Skeleton

---

### 8.43 Popover

**Fluent Name**: Popover

**Anatomy**:
```
Popover
├── Anchor (trigger)
└── Surface (Acrylic)
    ├── Arrow (optional)
    ├── Content
    └── Actions (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 160px |
| Maximum width | 320px |
| Padding | 12px 16px |
| Corner radius | 6px |
| Shadow | shadow16 |
| Background | neutralBackground1 + Acrylic |
| Arrow size | 8x8px |

**States**:

| State | Description |
|---|---|
| Closed | Hidden |
| Open | Visible, positioned at anchor |

**Behavior**:
- Entry: Decelerate easing, 150ms fade in + slight scale
- Exit: Accelerate easing, 100ms fade out
- Click outside or Esc to close, auto-flip to avoid viewport overflow

**Accessibility**:
- role="dialog", aria-modal depends on context
- Anchor aria-haspopup, aria-expanded reflects state
- Focus moves into Surface, returns to anchor on close

---

### 8.44 Modal

**Fluent Name**: Modal Dialog (large/full-screen, distinct from 8.9 regular Dialog)

**Anatomy**:
```
Modal
├── Scrim (overlay backdrop)
└── Surface (Acrylic)
    ├── Header
    │   ├── Title
    │   └── Close Button
    ├── Body (scrollable)
    └── Footer
        └── Actions
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 600px |
| Maximum width | 960px (or full screen) |
| Maximum height | 90% viewport |
| Corner radius | 8px (0px when full screen) |
| Header padding | 24px |
| Body padding | 24px |
| Footer padding | 24px |
| Shadow | shadow64 |
| Background | neutralBackground1 + Acrylic |
| Overlay | black 40% opacity |

**Layout**:
- Header and footer fixed, body area internally scrollable
- Title font: Title 24pt Semibold
- Primary action on the left (Fluent convention), secondary on the right

**Behavior**:
- Entry: Decelerate easing, 300ms fade in + move up
- Exit: Accelerate easing, 200ms fade out
- Click overlay or Esc to close (can be disabled)

**Accessibility**:
- role="dialog" / aria-modal="true"
- Focus locked within Surface, focus title on open
- aria-labelledby associates title, close button aria-label="Close"

---

### 8.45 FAB

**Fluent Name**: No floating button convention; the following is a reasonable implementation derived from Fluent design language (circular floating button based on Button)

**Anatomy**:
```
FAB
├── Background (circle)
├── Icon
└── Label (extended variant)
```

**Size Specifications**:

| Variant | Size | Corner Radius | Icon |
|---|---|---|---|
| Regular | 48x48px | circular | 24px |
| Small | 40x40px | circular | 20px |
| Extended | Height 48px, width adapts | circular | 24px + Body 14pt label |

**States**:

| State | Background | Icon | Shadow | Description |
|---|---|---|---|---|
| Default | brandBackground | neutralForegroundInverted | shadow8 | Default |
| Hover | brandBackgroundHover | neutralForegroundInverted | shadow16 | Hover |
| Pressed | brandBackgroundPressed | neutralForegroundInverted | shadow4 | Pressed |
| Disabled | neutralBackgroundDisabled | neutralForegroundDisabled | None | Disabled |

**Positioning**:
- Fixed at the bottom-right of content area, 16px from edge (small screen) / 24px (large screen)
- Always floats above content (Depth principle)

**Accessibility**:
- role="button", aria-label describes action (required for icon-only variant)
- Minimum touch target: 48x48px
- Supports keyboard focus and Enter/Space trigger

---

### 8.46 SearchBar

**Fluent Name**: SearchBox

**Anatomy**:
```
SearchBox
├── Background
├── Border
├── Search Icon (leading)
├── Input Text / Placeholder
└── Clear Button (trailing, optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 32px |
| Horizontal padding | 12px |
| Corner radius | 4px |
| Border | 1px solid neutralStroke1 |
| Icon size | 16x16px |
| Icon to text spacing | 8px |
| Font | Body 14pt |

**States**:

| State | Border | Background | Icon | Description |
|---|---|---|---|---|
| Default | neutralStroke1 | neutralBackground1 | neutralForeground3 | Default |
| Hover | neutralStrokeAccessible | neutralBackground1 | neutralForeground2 | Hover |
| Focused | brandStroke | neutralBackground1 | neutralForeground2 | Focused |
| Filled | neutralStroke1 | neutralBackground1 | neutralForeground2 | Has content (shows clear) |
| Disabled | neutralStrokeDisabled | neutralBackgroundDisabled | neutralForegroundDisabled | Disabled |

**Behavior**:
- Input triggers instant or debounced search
- Clear button appears when there is content, clears and focuses on click

**Accessibility**:
- role="searchbox", associate with label or aria-label
- Clear button aria-label="Clear"
- Search result count announced via aria-live

---

### 8.47 Rating

**Fluent Name**: Rating

**Anatomy**:
```
Rating
├── Star (filled / half / empty)
├── Star...
└── Value Text (optional)
```

**Size Specifications**:

| Variant | Star Size | Spacing |
|---|---|---|
| Small | 16px | 2px |
| Medium (default) | 20px | 4px |
| Large | 24px | 4px |

**States**:

| State | Filled | Empty | Description |
|---|---|---|---|
| Filled | warning | — | Rated (filled) |
| Half | warning (half) | neutralStroke1 | Half star |
| Empty | — | neutralStroke1 | Not rated |
| Hover | warning (preview) | neutralStroke1 | Hover preview |
| Disabled | neutralForegroundDisabled | neutralStrokeDisabled | Read-only/Disabled |

**Variants**:
- **Interactive**: Clickable/keyboard rating
- **Read-only**: Display only, interaction disabled

**Accessibility**:
- role="slider" or radiogroup, aria-valuenow / aria-valuemax
- Support keyboard left/right arrow adjustment
- Value supplemented with text (e.g., "4 / 5 stars")

---

### 8.48 ColorPicker

**Fluent Name**: ColorPicker

**Anatomy**:
```
ColorPicker
├── Saturation/Value Area
│   └── Cursor
├── Hue Slider
├── Alpha Slider (optional)
├── Preview Swatch
├── Input Fields (HEX / RGB)
└── Preset Swatches (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Color field area height | 160px |
| Slider height | 12px |
| Slider corner radius | circular |
| Cursor diameter | 16px |
| Preview swatch | 32x32px |
| Preset swatch | 24x24px |
| Input height | 32px |
| Panel corner radius | 8px |
| Panel padding | 16px |
| Panel shadow | shadow16 |

**States**:

| Element | State | Description |
|---|---|---|
| Cursor | Default | neutralBackground1 border + shadow4 |
| Cursor | Focused | brandStroke outline |
| Preset swatch | Selected | brandStroke 2px border |
| Input | Error | error border (invalid value) |
| Overall | Disabled | neutralForegroundDisabled |

**Accessibility**:
- Color field and sliders role="slider", aria-valuetext describes color value
- Support keyboard arrow key fine adjustment
- Color values provide HEX text input fallback

---

### 8.49 Calendar

**Fluent Name**: Calendar (month calendar view, distinct from 8.18 DatePicker)

**Anatomy**:
```
Calendar
├── Header
│   ├── Previous Month (‹)
│   ├── Month / Year Label
│   └── Next Month (›)
├── Weekday Labels
└── Month Grid
    └── Day Cell
        ├── Day Number
        └── Event Indicator (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Cell size | 40x40px |
| Cell spacing | 4px |
| Cell corner radius | 4px |
| Header height | 48px |
| Navigation button size | 32x32px |
| Weekday label font | Caption 12pt, neutralForeground3 |
| Date font | Body 14pt |
| Month label font | Subtitle 20pt Semibold |

**Day Cell States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | neutralForeground1 | Normal date |
| Today | transparent + brandStroke border | brandForeground | Today |
| Selected | brandBackground | neutralForegroundInverted | Selected |
| Hover | neutralBackground2 | neutralForeground1 | Hover |
| Outside | transparent | neutralForeground4 | Not this month |
| Disabled | transparent | neutralForegroundDisabled | Not selectable |

**Event Indicator**:
- Small dot below cell, brandBackground, diameter 4px

**Behavior**:
- Month transition animation: 200ms standard easing
- Supports range selection (start/end highlight, interval brandBackground + 10%)

**Accessibility**:
- role="grid", day cell role="gridcell"
- Today aria-current="date", selected aria-selected
- Support keyboard arrow key navigation, PageUp/Down to switch months

---

## 9. Platform Differences

### 9.1 Windows vs Web

| Feature | Windows | Web |
|---|---|---|
| Material | Acrylic / Mica | Simulated or simplified |
| Navigation | NavigationView | Custom |
| Title bar | Integrated into window | Browser tab |
| Context menu | Right-click | Right-click / Long press |
| Window controls | Maximize/Minimize/Close | Not applicable |

### 9.2 Touch vs Keyboard/Mouse

| Input Method | Touch | Keyboard/Mouse |
|---|---|---|
| Minimum target | 44x44px | 32x32px |
| Hover effect | None | Available |
| Context menu | Long press | Right-click |
| Scrolling | Touch swipe | Scroll wheel |

---

## 10. Token Reference Table

### 10.1 Color Tokens

| Token | Light | Dark |
|---|---|---|
| brandBackground | `#0078D4` | `#0078D4` |
| brandBackgroundHover | `#006CBE` | `#006CBE` |
| neutralForeground1 | `#242424` | `#FFFFFF` |
| neutralForeground2 | `#424242` | `#D6D6D6` |
| neutralForeground3 | `#616161` | `#ADADAD` |
| neutralBackground1 | `#FFFFFF` | `#292929` |
| neutralBackground2 | `#FAFAFA` | `#1F1F1F` |
| neutralBackground3 | `#F5F5F5` | `#141414` |
| neutralStroke1 | `#D1D1D1` | `#666666` |
| neutralStroke2 | `#E0E0E0` | `#525252` |
| neutralStrokeAccessible | `#616161` | `#ADADAD` |
| success | `#107C10` | `#54B054` |
| warning | `#FFC107` | `#FDBA3B` |
| error | `#D13438` | `#E9838A` |
| info | `#0099BC` | `#60CDFF` |

### 10.2 Font Tokens

| Token | Size | Weight | Line Height |
|---|---|---|---|
| hero | 28pt | Semibold | 36pt |
| title | 24pt | Semibold | 32pt |
| subtitle | 20pt | Regular | 28pt |
| body | 14pt | Regular | 20pt |
| caption | 12pt | Regular | 16pt |
| caption2 | 10pt | Regular | 14pt |

### 10.3 Spacing Tokens

| Token | Value |
|---|---|
| none | 0px |
| xxSmall | 2px |
| xSmall | 4px |
| small | 8px |
| medium | 12px |
| large | 16px |
| xLarge | 20px |
| xxLarge | 24px |
| xxxLarge | 32px |
| huge | 48px |

### 10.4 Corner Radius Tokens

| Token | Value |
|---|---|
| none | 0px |
| small | 2px |
| medium | 4px |
| large | 6px |
| xLarge | 8px |
| circular | 9999px |

### 10.5 Shadow Tokens

| Token | Parameters |
|---|---|
| shadow2 | `0 1px 2px rgba(0,0,0,0.14)` |
| shadow4 | `0 2px 4px rgba(0,0,0,0.14)` |
| shadow8 | `0 4px 8px rgba(0,0,0,0.14)` |
| shadow16 | `0 8px 16px rgba(0,0,0,0.14)` |
| shadow28 | `0 14px 28px rgba(0,0,0,0.14)` |
| shadow64 | `0 32px 64px rgba(0,0,0,0.14)` |
