# Apple Human Interface Guidelines

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

### 1.1 Clarity

- Text is legible at every size
- Icons convey meaning precisely
- Decorative elements are moderate and do not interfere with content
- Function drives design, not appearance

### 1.2 Deference

- The interface does not compete with content
- Content makes full use of screen space
- Translucency and blur suggest hierarchy
- Reduce visual weight to let content breathe

### 1.3 Depth

- Express depth through layers and motion
- Do not rely on shadows; use translucent overlays
- Touch layers are penetrable for content exploration
- Transition animations suggest spatial relationships

### 1.4 Core Design Values

| Value | Description |
|---|---|
| Aesthetic Integrity | Appearance unifies with function; do not sacrifice usability for beauty |
| Consistency | Use familiar standards and paradigms; do not reinvent the wheel |
| Direct Manipulation | Users directly interact with on-screen objects, not through indirect controls |
| Feedback | Provide immediate, perceptible feedback for every user action |
| Metaphor | Use real-world metaphors to help users understand the interface |
| User Control | Users initiate and control actions, not the system |

---

## 2. Color System

> **Note**: The following lists only the HIG default classic palette as a reference. Complete brand and theme colors are defined in the separate color specification skill.

### 2.1 System Colors

| Color Name | Light | Dark |
|---|---|---|
| systemBlue | `#007AFF` | `#0A84FF` |
| systemGreen | `#34C759` | `#30D158` |
| systemIndigo | `#5856D6` | `#5E5CE6` |
| systemOrange | `#FF9500` | `#FF9F0A` |
| systemPink | `#FF2D55` | `#FF375F` |
| systemPurple | `#AF52DE` | `#BF5AF2` |
| systemRed | `#FF3B30` | `#FF453A` |
| systemTeal | `#5AC8FA` | `#64D2FF` |
| systemYellow | `#FFCC00` | `#FFD60A` |
| systemGray | `#8E8E93` | `#8E8E93` |
| systemGray2 | `#AEAEB2` | `#636366` |
| systemGray3 | `#C7C7CC` | `#48484A` |
| systemGray4 | `#D1D1D6` | `#3A3A3C` |
| systemGray5 | `#E5E5EA` | `#2C2C2E` |
| systemGray6 | `#F2F2F7` | `#1C1C1E` |

### 2.2 Semantic Colors

Semantic colors automatically adapt to Light/Dark mode:

| Token | Light | Dark | Usage |
|---|---|---|---|
| label | `#000000` | `#FFFFFF` | Primary text |
| secondaryLabel | `#3C3C4399` | `#EBEBF599` | Secondary text |
| tertiaryLabel | `#3C3C434D` | `#EBEBF54D` | Tertiary text |
| quaternaryLabel | `#3C3C432E` | `#EBEBF53D` | Placeholder text |
| link | `#007AFF` | `#0A84FF` | Link text |
| placeholderText | `#3C3C434D` | `#EBEBF54D` | Placeholder |
| separator | `#C6C6C8` | `#38383A` | Separator |
| opaqueSeparator | `#C6C6C8` | `#38383A` | Opaque separator |

### 2.3 Background Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| systemBackground | `#FFFFFF` | `#000000` | Primary background |
| secondarySystemBackground | `#F2F2F7` | `#1C1C1E` | Secondary background |
| tertiarySystemBackground | `#FFFFFF` | `#2C2C2E` | Tertiary background |
| systemGroupedBackground | `#F2F2F7` | `#000000` | Grouped background |
| secondarySystemGroupedBackground | `#FFFFFF` | `#1C1C1E` | Secondary grouped background |
| tertiarySystemGroupedBackground | `#F2F2F7` | `#2C2C2E` | Tertiary grouped background |

### 2.4 Fill Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| systemFill | `#78788033` | `#7878805C` | Light fill |
| secondarySystemFill | `#78788028` | `#78788051` | Secondary fill |
| tertiarySystemFill | `#7676801E` | `#7676803D` | Tertiary fill |
| quaternarySystemFill | `#74748014` | `#7474802E` | Quaternary fill |

### 2.5 Dynamic Color Principles

- All semantic colors automatically respond to Light/Dark mode switching
- Use `UIColor` dynamic color API, do not hardcode
- Custom colors should provide both Light and Dark variants
- Avoid pure black `#000000` and pure white `#FFFFFF`; use system background colors

---

## 3. Typography

### 3.1 Font Family

- **Primary font**: SF Pro (San Francisco Pro)
- **Monospace font**: SF Mono
- **Serif font**: New York
- **Fallback fonts**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`

### 3.2 Font Sizes (Dynamic Type)

| Style | Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| Large Title | 34pt | Regular | 41pt | App large title |
| Title 1 | 28pt | Regular | 34pt | Page main title |
| Title 2 | 22pt | Regular | 28pt | Section title |
| Title 3 | 20pt | Regular | 25pt | Subsection title |
| Headline | 17pt | Semibold | 22pt | List title |
| Body | 17pt | Regular | 22pt | Body text |
| Callout | 16pt | Regular | 21pt | Callout text |
| Subhead | 15pt | Regular | 20pt | Subtitle |
| Footnote | 13pt | Regular | 18pt | Footnote |
| Caption 1 | 12pt | Regular | 16pt | Small label |
| Caption 2 | 11pt | Regular | 13pt | Extra small label |

### 3.3 Font Weights

| Weight | Value | Usage |
|---|---|---|
| Ultralight | 100 | Rarely used |
| Thin | 200 | Rarely used |
| Light | 300 | Light feel for large titles |
| Regular | 400 | Body text, titles |
| Medium | 500 | Emphasized text |
| Semibold | 600 | Buttons, Headline |
| Bold | 700 | Strong emphasis |
| Heavy | 800 | Rarely used |
| Black | 900 | Rarely used |

### 3.4 Typography Principles

- Minimum readable size: 11pt (Caption 2)
- Body text uses 17pt to ensure readability
- Titles use Regular or Semibold; avoid overusing Bold
- Line height at least 1.2 times font size
- Use Dynamic Type to support user font size preferences

---

## 4. Spacing and Grid

### 4.1 Base Grid

- **Base unit**: 8pt
- All spacing and sizes should be multiples of 8
- Exception: 4pt can be used for very tight spacing

### 4.2 Standard Spacing Values

| Token | Value | Usage |
|---|---|---|
| xxxSmall | 2pt | Inner icon spacing |
| xxSmall | 4pt | Tight element spacing |
| xSmall | 8pt | Default element spacing |
| small | 12pt | Small component padding |
| medium | 16pt | Standard padding |
| large | 20pt | Large component padding |
| xLarge | 24pt | Section spacing |
| xxLarge | 32pt | Large section spacing |
| xxxLarge | 48pt | Page-level spacing |
| huge | 64pt | Large page spacing |

### 4.3 Safe Area

- Content must be within the safe area
- Safe area avoids the notch, rounded corners, and Home indicator
- Use `safeAreaInsets` or CSS `env(safe-area-inset-*)`
- Background color can extend beyond the safe area; content cannot

### 4.4 Margin Specifications

| Scenario | Margin |
|---|---|
| Page horizontal margin | 16pt (iPhone) / 20pt (iPad) |
| List item padding | 16pt horizontal |
| Card padding | 16pt |
| Button padding | 16pt horizontal, 8-12pt vertical |
| Segmented control padding | 2pt |

---

## 5. Corner Radius and Shape

### 5.1 Continuous Corner Radius

HIG uses continuous curvature corner radius, not standard rounded corners:

| Token | Value | Usage |
|---|---|---|
| small | 8pt | Small buttons, input fields |
| medium | 10pt | Standard buttons |
| large | 13pt | Cards, dialogs |
| xLarge | 20pt | Large cards, Sheets |
| xxLarge | 27pt | Large containers |
| full | 9999px | Capsule buttons, avatars |

### 5.2 Corner Radius Principles

- Prefer continuous corner radius
- Larger containers use larger corner radius
- Nested element corner radius should be smaller than parent container
- Full corner radius only for capsule-shaped elements

---

## 6. Shadow and Depth

### 6.1 Depth Expression Principles

- **Minimize the use of shadows**; rely on layering and translucency to express depth
- Use background color changes to express hierarchy:
  - Primary level: `systemBackground`
  - Secondary level: `secondarySystemBackground`
  - Tertiary level: `tertiarySystemBackground`
- Modal layers use translucent black overlay: `#00000040` ~ `#00000080`

### 6.2 When to Use Shadows

| Scenario | Shadow Parameters |
|---|---|
| Rarely used | Only use subtle shadows on floating elements (e.g., drag items) |
| Dialogs/Sheets | No shadow, use background overlay |
| Cards | No shadow, use background color to differentiate |

### 6.3 Shadow Specifications (if necessary)

```css
/* Subtle shadow */
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

/* Medium shadow */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
```

---

## 7. Motion Specifications

### 7.1 Animation Duration

| Type | Duration | Usage |
|---|---|---|
| Instant feedback | 100-150ms | Button press, switch toggle |
| Standard transition | 250-300ms | Page transitions, dialog appearance |
| Complex animation | 350-500ms | Large element movement, morphing |

### 7.2 Easing Functions

| Name | Curve | Usage |
|---|---|---|
| Ease In | `cubic-bezier(0.42, 0, 1, 1)` | Element exit |
| Ease Out | `cubic-bezier(0, 0, 0.58, 1)` | Element entry |
| Ease In-Out | `cubic-bezier(0.42, 0, 0.58, 1)` | Symmetrical transition |
| Spring | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Elastic effect |

### 7.3 Motion Principles

- Animations should have purpose, not decoration
- Use physical metaphors: spring, gravity, inertia
- Maintain 60fps smoothness
- Support Reduced Motion preference
- Transitions suggest spatial relationships and content hierarchy

---

## 8. Component Specifications

### 8.1 Button

**HIG Name**: Button

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
| Small | 28pt | 12pt | 8pt |
| Medium (default) | 34pt | 16pt | 10pt |
| Large | 44pt | 20pt | 10pt |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | systemBlue | white | Default state |
| Hover | systemBlue darken 10% | white | Mouse hover |
| Pressed | systemBlue darken 20% | white | Pressed |
| Disabled | systemGray5 | systemGray | Disabled |
| Focused | systemBlue + 2pt outline | white | Keyboard focus |

**Variants**:
- **Filled**: Solid background, white text
- **Tinted**: Light background (Blue 10% opacity), blue text
- **Gray**: Gray background, dark text
- **Plain**: No background, blue text

**Accessibility**:
- Minimum touch target: 44x44pt
- Color contrast ratio >= 4.5:1
- Support keyboard focus
- Disabled state clearly distinguishable

---

### 8.2 TextField

**HIG Name**: Text Field

**Anatomy**:
```
TextField
├── Background
├── Placeholder Text
├── Input Text
├── Clear Button (optional)
├── Leading Icon (optional)
└── Trailing Icon / Action (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 44pt |
| Horizontal padding | 12pt |
| Corner radius | 10pt |
| Border | 1pt solid separator |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | separator | secondarySystemBackground | Default |
| Hover | systemGray2 | secondarySystemBackground | Hover |
| Focused | systemBlue | secondarySystemBackground | Focused |
| Filled | separator | secondarySystemBackground | Has content |
| Error | systemRed | systemRed 5% opacity | Error |
| Disabled | systemGray4 | systemGray6 | Disabled |

**Accessibility**:
- Associate with label
- Error state provides aria-invalid and error text
- Support keyboard navigation

---

### 8.3 Checkbox

**HIG Name**: Checkbox (macOS) / Toggle (iOS rarely used)

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
| Box size | 18x18pt |
| Box corner radius | 4pt |
| Label spacing | 8pt |
| Checkmark line width | 2pt |

**States**:

| State | Box Background | Border | Checkmark |
|---|---|---|---|
| Unchecked | transparent | systemGray3 | None |
| Checked | systemBlue | systemBlue | white |
| Hover (unchecked) | transparent | systemGray2 | None |
| Hover (checked) | systemBlue darken | systemBlue darken | white |
| Disabled | systemGray6 | systemGray4 | systemGray |

**Accessibility**:
- Use native checkbox or role="checkbox"
- aria-checked state
- Minimum touch target 44x44pt

---

### 8.4 RadioButton

**HIG Name**: Radio Button

**Anatomy**:
```
RadioButton
├── Circle
│   └── Inner Dot (optional)
└── Label (Text)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Outer circle diameter | 20pt |
| Inner dot diameter | 8pt |
| Border width | 2pt |
| Label spacing | 8pt |

**States**:

| State | Outer Circle | Inner Dot | Description |
|---|---|---|---|
| Unselected | transparent + systemBlue border | None | Unselected |
| Selected | transparent + systemBlue border | systemBlue | Selected |
| Hover | systemBlue 10% fill | Same | Hover |
| Disabled | systemGray4 border | systemGray | Disabled |

---

### 8.5 Switch

**HIG Name**: Toggle

**Anatomy**:
```
Switch
├── Track (pill shape)
└── Thumb (circle)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Track width | 51pt |
| Track height | 31pt |
| Thumb diameter | 27pt |
| Thumb margin | 2pt |

**States**:

| State | Track | Thumb | Description |
|---|---|---|---|
| Off | systemGray4 | white | Off |
| On | systemGreen | white | On |
| Disabled (off) | systemGray6 | systemGray5 | Disabled off |
| Disabled (on) | systemGreen 40% | systemGray5 | Disabled on |

**Motion**:
- Toggle animation: 200ms ease-in-out
- Thumb movement uses spring effect

---

### 8.6 Slider

**HIG Name**: Slider

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
| Track height | 4pt |
| Track corner radius | 2pt |
| Thumb diameter | 28pt |
| Minimum touch area | 44x44pt |

**States**:

| State | Fill | Thumb | Description |
|---|---|---|---|
| Default | systemBlue | white + shadow | Default |
| Hover | systemBlue | white + 1.1x scale | Hover |
| Pressed | systemBlue darken | white + 0.9x scale | Pressed |
| Disabled | systemGray4 | systemGray5 | Disabled |

---

### 8.7 ProgressIndicator

**HIG Name**: Progress View

**Anatomy**:
```
ProgressIndicator
├── Track (background)
└── Indicator (fill / spinner)
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Linear | Height 4pt, width adapts |
| Circular | Diameter 20pt / 36pt |

**Linear Progress Bar**:
- Track: systemGray5
- Fill: systemBlue
- Corner radius: 2pt

**Circular Progress Bar**:
- Line width: 3pt (small) / 4pt (large)
- Color: systemBlue
- Rotation animation: 1s linear infinite

**Indeterminate State**:
- Linear: Loop animation, fill from 0% to 100% then reset
- Circular: Continuous rotation

---

### 8.8 Menu

**HIG Name**: Menu / Context Menu

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
| Minimum width | 200pt |
| Maximum width | 400pt |
| Item height | 44pt |
| Item padding | 16pt horizontal |
| Corner radius | 13pt |
| Shadow | Not used; use background hierarchy |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | label | Default |
| Hover | systemBlue | white | Hover |
| Pressed | systemBlue darken | white | Pressed |
| Disabled | transparent | systemGray | Disabled |

---

### 8.9 Dialog

**HIG Name**: Alert / Action Sheet / Sheet

**Anatomy**:
```
Dialog (Alert)
├── Title
├── Message
├── TextField (optional)
└── Actions
    ├── Primary Action
    └── Secondary Action
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 270pt |
| Maximum width | 400pt |
| Corner radius | 13pt |
| Padding | 20pt |
| Title to content spacing | 8pt |
| Content to button spacing | 16pt |

**Background**:
- Dialog background: secondarySystemBackground
- Overlay: black 40% opacity

**Button Layout**:
- 2 buttons: horizontal layout
- 3+ buttons: vertical layout
- Primary action on the right (horizontal) or bottom (vertical)

**Sheet (Bottom Sheet)**:
- Slides in from the bottom
- Corner radius: 20pt (top)
- Supports drag to dismiss

---

### 8.10 Card

**HIG Name**: No direct equivalent; uses Grouped Background

**Anatomy**:
```
Card
├── Background
├── Content
│   ├── Header (optional)
│   ├── Body
│   └── Footer (optional)
└── Divider (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Corner radius | 10pt (iOS) / 13pt (macOS) |
| Padding | 16pt |
| Background | secondarySystemBackground |
| Border | None |
| Shadow | None |

**List Cards**:
- Use grouped background style
- First item: top corner radius
- Middle items: no corner radius
- Last item: bottom corner radius
- Items separated by dividers

---

### 8.11 List

**HIG Name**: List / Table

**Anatomy**:
```
List
├── List Section (optional)
│   └── Header
├── List Item
│   ├── Icon (optional)
│   ├── Content
│   │   ├── Title
│   │   └── Subtitle (optional)
│   ├── Detail (optional)
│   └── Accessory (chevron / switch / etc.)
└── List Section...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item height | 44pt (single line) / 60pt (double line) |
| Item padding | 16pt horizontal |
| Separator inset | 60pt (with icon) / 16pt (without icon) |
| Separator color | separator |

**States**:

| State | Background | Description |
|---|---|---|
| Default | transparent | Default |
| Hover | systemGray6 | Hover (macOS) |
| Selected | systemBlue | Selected |
| Pressed | systemGray5 | Pressed |

---

### 8.12 NavigationBar

**HIG Name**: Navigation Bar

**Anatomy**:
```
NavigationBar
├── Leading Item (back / menu)
├── Title
└── Trailing Items (actions)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 44pt (iOS) / 52pt (macOS) |
| Background | systemBackground + blur |
| Title font | Headline 17pt Semibold |
| Large title font | Title 1 28pt Bold |

**Large Title Mode**:
- Large title shrinks to normal title on scroll
- Transition animation: 250ms ease-in-out

---

### 8.13 TabBar

**HIG Name**: Tab Bar

**Anatomy**:
```
TabBar
├── Tab Item
│   ├── Icon
│   └── Label
├── Tab Item...
└── Background
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 49pt (iOS) |
| Background | systemBackground + blur |
| Icon size | 24x24pt |
| Label font | Caption 2 10pt |
| Label to icon spacing | 4pt |

**States**:

| State | Icon/Text | Description |
|---|---|---|
| Selected | systemBlue | Selected |
| Unselected | systemGray | Unselected |

**Limitations**:
- Maximum 5 tabs
- 5+ use "More" tab

---

### 8.14 SegmentedControl

**HIG Name**: Segmented Control

**Anatomy**:
```
SegmentedControl
├── Background
├── Segment
│   └── Label
├── Segment...
└── Selected Indicator
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 32pt |
| Corner radius | 8pt |
| Segment spacing | 2pt |
| Padding | 2pt |
| Background | systemGray5 |

**States**:

| State | Indicator | Text | Description |
|---|---|---|---|
| Selected | white | label | Selected |
| Unselected | transparent | label | Unselected |
| Disabled | white | systemGray | Disabled |

---

### 8.15 Tooltip

**HIG Name**: Tooltip

**Anatomy**:
```
Tooltip
├── Background
└── Label
```

**Size Specifications**:

| Property | Value |
|---|---|
| Maximum width | 240pt |
| Padding | 8pt 12pt |
| Corner radius | 8pt |
| Font | Caption 1 12pt |
| Background | label (dark) |
| Text | white |

**Behavior**:
- Shows after 500ms hover
- Hides 0ms after leaving target
- Arrow points to center of target element

---

### 8.16 Badge

**HIG Name**: Badge

**Anatomy**:
```
Badge
├── Background
└── Label (number / dot)
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Dot | 8x8pt |
| Number | Height 18pt, width adapts |

**Number Badge**:
- Height: 18pt
- Minimum width: 18pt
- Padding: 6pt horizontal
- Corner radius: 9pt (full)
- Background: systemRed
- Text: white, Caption 2 11pt

---

### 8.17 Chip

**HIG Name**: No direct equivalent; use Tag or Pill style

**Anatomy**:
```
Chip
├── Background
├── Icon (optional)
├── Label
└── Close Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 28pt |
| Horizontal padding | 12pt |
| Corner radius | full (capsule) |
| Background | systemGray5 |
| Text | label |

**States**:

| State | Background | Description |
|---|---|---|
| Default | systemGray5 | Default |
| Selected | systemBlue | Selected |
| Hover | systemGray4 | Hover |

---

### 8.18 DatePicker

**HIG Name**: Date Picker

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
| Cell size | 32x32pt |
| Cell spacing | 4pt |
| Selected background | systemBlue circle |
| Today marker | systemBlue border circle |

**Variants**:
- **Compact**: Input field + popup calendar
- **Inline**: Directly expanded calendar
- **Wheels**: Wheel picker (iOS traditional)

---

### 8.19 Table

**HIG Name**: Table

**Anatomy**:
```
Table
├── Table Header
│   └── Column Header
├── Table Row
│   └── Cell
└── Table Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Row height | 44pt |
| Header height | 36pt |
| Cell padding | 16pt horizontal |
| Separator | separator, full width |

**Table Header**:
- Font: Caption 1 12pt Semibold
- Color: secondaryLabel
- Background: systemGray6

**Row States**:

| State | Background | Description |
|---|---|---|
| Default | transparent | Default |
| Hover | systemGray6 | Hover |
| Selected | systemBlue | Selected |
| Alternate | systemGray6 | Zebra striping (optional) |

---

### 8.20 Breadcrumb

**HIG Name**: No direct equivalent (macOS uses Path Control)

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
| Item font | Body 17pt |
| Separator | "/" or ">" |
| Separator color | systemGray3 |
| Current item | label, no underline |
| Clickable items | systemBlue |

---

### 8.21 Select

**HIG Name**: Pop-up Button / Menu

**Anatomy**:
```
Select
├── Trigger
│   ├── Label / Selected Value
│   └── Chevron (up/down)
└── Menu (popover)
    ├── Menu Item
    │   ├── Checkmark (selected)
    │   └── Label
    └── Menu Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 34pt |
| Horizontal padding | 12pt |
| Corner radius | 8pt |
| Trigger background | tertiarySystemFill |
| Chevron color | secondaryLabel |
| Menu corner radius | 13pt |
| Menu item height | 44pt |

**States**:

| State | Trigger Background | Text | Description |
|---|---|---|---|
| Default | tertiarySystemFill | label | Default |
| Hover | secondarySystemFill | label | Hover |
| Pressed | systemFill | label | Press to expand |
| Focused | tertiarySystemFill + systemBlue 2pt outline | label | Keyboard focus |
| Disabled | systemGray6 | systemGray | Disabled |

**Variants**:
- **Inline**: Trigger shows current value + chevron
- **Menu**: Click to expand menu, selected item shows checkmark
- **Sectioned**: Menu with grouped section dividers

**Accessibility**:
- Minimum touch target 44x44pt
- Use native select or role="combobox" + aria-expanded
- Mark selected item with aria-selected
- Support keyboard up/down navigation

---

### 8.22 Autocomplete

**HIG Name**: No native combobox component; the following is a reasonable implementation derived from HIG design language (Search Field + suggestion list)

**Anatomy**:
```
Autocomplete
├── Input Field
│   ├── Leading Search Icon
│   ├── Input Text / Placeholder
│   └── Clear Button (optional)
└── Suggestion List (popover)
    ├── Suggestion Item
    │   ├── Icon (optional)
    │   └── Label (matched highlight)
    └── Suggestion Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Input height | 44pt |
| Input corner radius | 10pt |
| Input background | secondarySystemBackground |
| Suggestion list corner radius | 13pt |
| Suggestion item height | 44pt |
| Suggestion item padding | 16pt horizontal |
| List to input spacing | 4pt |
| Match highlight | systemBlue text |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | separator | secondarySystemBackground | Default |
| Focused | systemBlue | secondarySystemBackground | Focused, inputting |
| Suggesting | systemBlue | secondarySystemBackground | Suggestions expanded |
| Disabled | systemGray4 | systemGray6 | Disabled |

**Suggestion Item States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | label | Default |
| Hover | systemBlue | white | Hover |
| Active | systemBlue | white | Keyboard highlighted |

**Variants**:
- **Single-select**: Select fills and closes
- **Multi-select**: Selected items accumulate as chips
- **Free-text**: Allows free-form input beyond suggestions

**Accessibility**:
- role="combobox" + aria-autocomplete="list"
- aria-expanded marks suggestion expansion state
- aria-activedescendant marks current highlighted item
- Support Esc to close suggestions, up/down navigation

---

### 8.23 Textarea

**HIG Name**: Multiline Text Field

**Anatomy**:
```
Textarea
├── Background
├── Placeholder Text
├── Input Text (multiline)
└── Resize Handle (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 88pt (approx. 2 lines) |
| Horizontal padding | 12pt |
| Vertical padding | 12pt |
| Corner radius | 10pt |
| Border | 1pt solid separator |
| Line height | Body 22pt |
| Background | secondarySystemBackground |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | separator | secondarySystemBackground | Default |
| Hover | systemGray2 | secondarySystemBackground | Hover |
| Focused | systemBlue | secondarySystemBackground | Focused |
| Filled | separator | secondarySystemBackground | Has content |
| Error | systemRed | systemRed 5% opacity | Error |
| Disabled | systemGray4 | systemGray6 | Disabled |

**Variants**:
- **Fixed**: Fixed height, scroll when overflow
- **Auto-grow**: Auto-grows with content
- **With Counter**: Character count at bottom (caption1 12pt secondaryLabel)

**Accessibility**:
- Associate with label
- Error state provides aria-invalid and error text
- Character limit indicated via aria-describedby

---

### 8.24 NumberInput

**HIG Name**: Stepper + Text Field combination

**Anatomy**:
```
NumberInput
├── Text Field
│   └── Numeric Value
└── Stepper
    ├── Decrement Button (-)
    └── Increment Button (+)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Overall height | 44pt |
| Input corner radius | 10pt (left side) |
| Input padding | 12pt horizontal |
| Stepper width | 94pt (dual button) |
| Stepper button width | 47pt |
| Stepper background | tertiarySystemFill |
| Stepper corner radius | 8pt |
| Divider | separator 1pt (between buttons) |

**States**:

| State | Input Border | Stepper Background | Description |
|---|---|---|---|
| Default | separator | tertiarySystemFill | Default |
| Focused | systemBlue | tertiarySystemFill | Input focused |
| Pressed (button) | separator | systemFill | Button pressed |
| Min/Max boundary | separator | tertiarySystemFill | Corresponding button becomes systemGray, disabled |
| Disabled | systemGray4 | systemGray6 | Fully disabled |

**Variants**:
- **Inline Stepper**: +/- buttons attached to the right of input
- **Detached Stepper**: Standalone stepper (no input, only +/-)
- **With Unit**: Unit text after value (secondaryLabel)

**Accessibility**:
- role="spinbutton" + aria-valuenow / aria-valuemin / aria-valuemax
- Each stepper button minimum touch 44x44pt
- Support keyboard up/down stepping

---

### 8.25 Upload

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (file upload based on Button + List)

**Anatomy**:
```
Upload
├── Drop Zone
│   ├── Icon (cloud / plus)
│   ├── Prompt Text
│   └── Browse Button
└── File List
    └── File Item
        ├── File Icon
        ├── File Name / Size
        ├── Progress (uploading)
        └── Remove / Status Button
```

**Size Specifications**:

| Property | Value |
|---|---|
| Drop zone minimum height | 160pt |
| Drop zone corner radius | 13pt |
| Drop zone border | 2pt dashed separator |
| Drop zone background | secondarySystemBackground |
| File item height | 60pt |
| File item corner radius | 10pt |
| Progress bar height | 4pt |
| Progress bar fill | systemBlue |

**States**:

| State | Border | Background | Description |
|---|---|---|---|
| Default | separator (dashed) | secondarySystemBackground | Default |
| Hover | systemGray2 (dashed) | secondarySystemBackground | Hover |
| Dragover | systemBlue (dashed) | systemBlue 10% opacity | Drag hover |
| Disabled | systemGray4 (dashed) | systemGray6 | Disabled |

**File Item States**:

| State | Indicator | Color | Description |
|---|---|---|---|
| Uploading | Progress bar | systemBlue | Uploading |
| Success | Checkmark icon | systemGreen | Success |
| Error | Warning icon | systemRed | Error |

**Variants**:
- **Dropzone**: Large drag-drop area
- **Button-only**: Single browse button + file list
- **Avatar/Image**: Image preview thumbnails

**Accessibility**:
- Drop zone provides equivalent browse button (keyboard accessible)
- File status uses aria-live for upload progress
- Remove button minimum touch 44x44pt

---

### 8.26 Toast

**HIG Name**: No native lightweight notification component; the following is a bottom overlay derived from HIG Deference and translucency principles

**Anatomy**:
```
Toast
├── Background (translucent + blur)
├── Icon (optional)
├── Message
└── Action Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 50pt |
| Maximum width | Container width - 32pt margin |
| Horizontal padding | 16pt |
| Vertical padding | 12pt |
| Corner radius | 13pt |
| Background | secondarySystemBackground + blur |
| Text | label, Subhead 15pt |
| Bottom spacing | 16pt (avoid safe area) |

**States**:

| State | Icon Color | Description |
|---|---|---|
| Info | systemBlue | General information |
| Success | systemGreen | Success |
| Warning | systemYellow | Warning |
| Error | systemRed | Error |

**Behavior**:
- Fades in from bottom and slides up: 250ms ease-out
- Default 3s display then auto-fades out
- Supports swipe up gesture to dismiss early
- Multiple toasts stack vertically, 8pt spacing

**Accessibility**:
- role="status" + aria-live="polite" (use assertive for errors)
- Does not steal focus; content priority
- Allow sufficient reading time before auto-dismiss

---

### 8.27 Notification

**HIG Name**: No native in-app notification component; the following is a banner notification derived from HIG design language

**Anatomy**:
```
Notification
├── Background (translucent + blur)
├── App Icon / Leading Icon
├── Content
│   ├── Title
│   └── Body
├── Timestamp (optional)
└── Action / Dismiss Button
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 64pt |
| Padding | 16pt |
| Corner radius | 20pt |
| Background | secondarySystemBackground + blur |
| Icon size | 38x38pt |
| Icon corner radius | 8pt |
| Title font | Headline 17pt Semibold |
| Body font | Subhead 15pt secondaryLabel |
| Top spacing | 16pt (avoid safe area) |

**States**:

| State | Background | Description |
|---|---|---|
| Default | secondarySystemBackground + blur | Default banner |
| Hover | tertiarySystemBackground | Hover (macOS) |
| Pressed | systemFill | Press to expand/navigate |

**Variants**:
- **Banner**: Slides down from top, auto-dismisses
- **Persistent**: Remains until user action
- **Grouped**: Multiple related notifications collapsed together

**Behavior**:
- Slides in from top: 300ms ease-out
- Banner auto-dismisses after 5s
- Supports swipe up to dismiss, swipe down to expand

**Accessibility**:
- role="alert" (important) or role="status" (general)
- aria-live announces title and body
- Dismiss button minimum touch 44x44pt

---

### 8.28 Alert / Banner

**HIG Name**: No native inline embeddable prompt bar; the following is a reasonable implementation derived from HIG design language (inline banner, distinct from 8.9 dialog-style Alert)

**Anatomy**:
```
Inline Banner
├── Background (tinted)
├── Leading Icon (status)
├── Content
│   ├── Title (optional)
│   └── Message
├── Action Link (optional)
└── Dismiss Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 44pt |
| Padding | 12pt 16pt |
| Corner radius | 10pt |
| Icon size | 20x20pt |
| Icon to content spacing | 12pt |
| Title font | Subhead 15pt Semibold |
| Body font | Footnote 13pt |

**States (Semantic Variants)**:

| State | Background | Icon/Emphasis Color | Text |
|---|---|---|---|
| Info | systemBlue 10% opacity | systemBlue | label |
| Success | systemGreen 10% opacity | systemGreen | label |
| Warning | systemYellow 10% opacity | systemYellow | label |
| Error | systemRed 10% opacity | systemRed | label |
| Neutral | secondarySystemBackground | secondaryLabel | label |

**Variants**:
- **Compact**: Single line, icon + text only
- **Detailed**: Title + body + action link
- **Dismissible**: Close button on the right

**Accessibility**:
- role="alert" (error/warning) or role="status" (info)
- Do not rely solely on color for semantics; pair with icons
- Dismiss button minimum touch 44x44pt

---

### 8.29 Skeleton

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (loading placeholder skeleton)

**Anatomy**:
```
Skeleton
├── Shape Placeholder
│   ├── Line (text)
│   ├── Circle (avatar)
│   └── Rect (image / block)
└── Shimmer Overlay (animated)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Text line height | 12pt / 16pt (per font) |
| Text line corner radius | 4pt |
| Circle placeholder | Matches avatar size (e.g., 40pt) |
| Block placeholder corner radius | 10pt |
| Placeholder background | systemGray5 |
| Shimmer highlight | systemGray6 |
| Line spacing | 8pt |

**States**:

| State | Background | Description |
|---|---|---|
| Loading | systemGray5 + shimmer | Loading |
| Pulse | systemGray5 ↔ systemGray6 | Breathing gradient variant |

**Variants**:
- **Text**: Multi-line text placeholder, last line shorter
- **Avatar**: Circular avatar placeholder
- **Card**: Image block + multi-line text combination
- **List**: Repeated row placeholder

**Motion**:
- Shimmer: 1.5s linear infinite, left to right sweep
- Pulse: 1.2s ease-in-out, opacity 100% ↔ 40%
- Supports Reduced Motion: degrades to static placeholder

**Accessibility**:
- aria-hidden="true", hide placeholders from screen readers
- Container uses aria-busy="true" to indicate loading

---

### 8.30 Drawer / Sidebar

**HIG Name**: Sidebar (macOS) / Slide-out side panel

**Anatomy**:
```
Drawer / Sidebar
├── Overlay (scrim, slide-out)
└── Panel
    ├── Header (title / close)
    ├── Content
    │   └── Navigation List / Custom
    └── Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Width (side) | 280pt~320pt |
| Padding | 16pt |
| Background | secondarySystemBackground + blur |
| Corner radius | 0pt (flush) / 20pt (floating slide-out) |
| Overlay | black 40% opacity (slide-out) |
| Navigation item height | 44pt |
| Navigation item corner radius | 8pt |

**States**:

| State | Background | Description |
|---|---|---|
| Default | secondarySystemBackground | Default |
| Item Hover | systemGray6 | Item hover |
| Item Selected | systemBlue | Item selected |
| Collapsed | — | Icons only, width 64pt |

**Variants**:
- **Fixed Sidebar**: Persistent sidebar (macOS/iPad)
- **Overlay Drawer**: Overlay with scrim (mobile)
- **Collapsible**: Collapsible to icon bar

**Behavior**:
- Slide-out animation: 300ms ease-out
- Closes on overlay tap or left swipe
- Supports edge-swipe gesture to reveal

**Accessibility**:
- role="navigation" or role="complementary"
- When slide-out opens, focus moves to panel; returns on close
- Supports Esc to close, overlay clickable to close

---

### 8.31 Pagination

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (paginator)

**Anatomy**:
```
Pagination
├── Previous Button (chevron)
├── Page Item
│   └── Page Number
├── Ellipsis (...)
├── Page Item...
└── Next Button (chevron)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Page item size | 32x32pt |
| Page item spacing | 8pt |
| Page item corner radius | 8pt |
| Touch target | 44x44pt |
| Font | Subhead 15pt |
| Arrow color | systemBlue |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | label | Default page number |
| Hover | systemGray6 | label | Hover |
| Current | systemBlue | white | Current page |
| Disabled | transparent | systemGray | Boundary arrow disabled |

**Variants**:
- **Numbered**: Page numbers + ellipsis
- **Simple**: Previous/Next only
- **Compact**: Current page / Total pages (e.g., "3 / 12")

**Accessibility**:
- role="navigation" aria-label="Pagination"
- Mark current page aria-current="page"
- Each clickable item minimum touch 44x44pt

---

### 8.32 Stepper

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (process step indicator / wizard step bar, distinct from 8.24 NumberInput stepper)

**Anatomy**:
```
Stepper (Wizard)
├── Step
│   ├── Indicator (number / checkmark)
│   ├── Title
│   └── Subtitle (optional)
├── Connector (line)
└── Step...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Indicator diameter | 28pt |
| Indicator font | Subhead 15pt Semibold |
| Connector line width | 2pt |
| Connector line color | separator |
| Title font | Subhead 15pt |
| Subtitle font | Footnote 13pt secondaryLabel |
| Step spacing | 8pt (horizontal connector area) |

**States**:

| State | Indicator Background | Indicator Content | Text |
|---|---|---|---|
| Upcoming | systemGray5 | Gray number | secondaryLabel |
| Current | systemBlue | white number | label Semibold |
| Completed | systemBlue | white checkmark | label |
| Error | systemRed | white exclamation | systemRed |
| Disabled | systemGray6 | systemGray number | systemGray |

**Variants**:
- **Horizontal**: Horizontal step bar + connector lines
- **Vertical**: Vertical step bar, connector lines below indicators
- **Dot**: Dots only (no numbers), for simplified progress

**Accessibility**:
- Mark current step with aria-current="step"
- Completed steps use checkmark icon + aria-label dual representation
- Wrapped in role="list", each step role="listitem"

---

### 8.33 Sheet / ActionSheet

**HIG Name**: Action Sheet / Sheet

**Anatomy**:
```
Sheet / ActionSheet
├── Overlay (scrim)
└── Panel (bottom)
    ├── Grabber (drag handle)
    ├── Title / Message (optional)
    ├── Action List
    │   └── Action Item
    └── Cancel Action
```

**Size Specifications**:

| Property | Value |
|---|---|
| Top corner radius | 20pt |
| Padding | 16pt |
| Background | secondarySystemBackground + blur |
| Overlay | black 40% opacity |
| Grabber width | 36pt |
| Grabber height | 5pt |
| Grabber color | systemGray3 |
| Action item height | 56pt |
| Cancel item spacing | 8pt |

**States**:

| State | Action Item Background | Text | Description |
|---|---|---|---|
| Default | transparent | systemBlue | Default action |
| Pressed | systemGray5 | systemBlue | Pressed |
| Destructive | transparent | systemRed | Destructive action |
| Cancel | secondarySystemBackground | systemBlue Semibold | Cancel (separate group) |
| Disabled | transparent | systemGray | Disabled |

**Variants**:
- **Action Sheet**: Bottom action list + cancel
- **Sheet (Detail)**: Drag-gable content panel with multiple height detents
- **Modal Sheet**: Blocking content editing panel

**Behavior**:
- Slides in from bottom: 300ms ease-out
- Supports downward drag to dismiss (Grabber)
- Tap overlay to dismiss (non-destructive scenarios)

**Accessibility**:
- role="dialog" aria-modal="true"
- Focus moves into panel when opened
- Destructive actions not solely color-based; clear labeling required
- Each action item minimum touch 44x44pt

---

### 8.34 Avatar

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (circular avatar image)

**Anatomy**:
```
Avatar
├── Image / Initials / Icon
├── Border (optional)
├── Status Indicator (optional)
└── Badge (optional)
```

**Size Specifications**:

| Variant | Diameter |
|---|---|
| xSmall | 24pt |
| Small | 32pt |
| Medium (default) | 40pt |
| Large | 56pt |
| xLarge | 80pt |

**General Specifications**:

| Property | Value |
|---|---|
| Corner radius | full (circle) / 13pt (rounded square variant) |
| Placeholder background | systemGray4 |
| Initials text | white, font per size |
| Border | 2pt systemBackground (when stacked) |
| Status dot diameter | 30% of diameter, minimum 8pt |

**Status Indicator Colors**:

| Status | Color | Description |
|---|---|---|
| Online | systemGreen | Online |
| Busy | systemRed | Busy |
| Away | systemYellow | Away |
| Offline | systemGray | Offline |

**Variants**:
- **Image**: Picture avatar
- **Initials**: Initial placeholder
- **Icon**: Icon placeholder
- **Group**: Overlapping avatars (overlap -12pt, with systemBackground border)

**Accessibility**:
- Image provides alt description (username)
- Status indicator paired with aria-label, not color alone
- Purely decorative avatars can use aria-hidden

---

### 8.35 Accordion

**HIG Name**: Disclosure (Collapsible Group / Disclosure Group)

**Anatomy**:
```
Accordion
├── Accordion Item
│   ├── Header
│   │   ├── Title
│   │   └── Disclosure Chevron
│   └── Content (collapsible)
└── Accordion Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Header height | 44pt |
| Header padding | 16pt horizontal |
| Title font | Headline 17pt Semibold |
| Chevron size | 14pt |
| Chevron color | secondaryLabel |
| Content padding | 16pt |
| Divider | separator (between items) |
| Background | secondarySystemBackground |

**States**:

| State | Header Background | Chevron | Description |
|---|---|---|---|
| Collapsed | secondarySystemBackground | Right/Down | Collapsed |
| Expanded | secondarySystemBackground | Rotated 90 degrees (Down/Up) | Expanded |
| Hover | systemGray6 | Same | Hover |
| Disabled | systemGray6 | systemGray | Disabled |

**Variants**:
- **Single**: Only one item expanded at a time (accordion)
- **Multiple**: Allows multiple items expanded simultaneously
- **Bordered / Plain**: With or without border style

**Motion**:
- Expand/Collapse: 250ms ease-in-out
- Chevron rotation transitions synchronously

**Accessibility**:
- Header role="button" + aria-expanded
- aria-controls associates content area
- Support Enter/Space toggle, minimum touch 44x44pt

---

### 8.36 Carousel

**HIG Name**: Page Control + Horizontal Scroll

**Anatomy**:
```
Carousel
├── Slide Track (horizontal scroll)
│   └── Slide
│       └── Content
├── Page Control (dots)
└── Navigation Arrows (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Slide corner radius | 13pt |
| Slide spacing | 8pt |
| Page Control dot diameter | 8pt |
| Dot spacing | 8pt |
| Dot touch area | 44x44pt |
| Arrow button size | 44x44pt |
| Arrow background | systemBackground + blur |

**States**:

| State | Dot Color | Description |
|---|---|---|
| Active | label | Current page dot |
| Inactive | tertiaryLabel | Non-current page dot |
| Arrow Default | systemBlue | Arrow available |
| Arrow Disabled | systemGray | Boundary disabled |

**Variants**:
- **Full-width**: Single full-width slide + pagination
- **Peeking**: Shows adjacent slide edges
- **Auto-play**: Auto-rotating (supports pause)

**Motion**:
- Page transition: 300ms ease-out
- Supports inertial scrolling and snap

**Accessibility**:
- role="group" aria-roledescription="carousel"
- Provide pause control for auto-play
- Page Control marks aria-current
- Support keyboard left/right navigation

---

### 8.37 Timeline

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (timeline)

**Anatomy**:
```
Timeline
├── Timeline Item
│   ├── Node (dot / icon)
│   ├── Connector (line)
│   └── Content
│       ├── Timestamp
│       ├── Title
│       └── Description (optional)
└── Timeline Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Node diameter | 12pt |
| Node icon size | 24pt (icon variant) |
| Connector line width | 2pt |
| Connector line color | separator |
| Node to content spacing | 16pt |
| Item spacing | 20pt |
| Timestamp font | Footnote 13pt secondaryLabel |
| Title font | Subhead 15pt Semibold |
| Description font | Footnote 13pt |

**States**:

| State | Node | Connector | Description |
|---|---|---|---|
| Completed | systemBlue filled | systemBlue | Completed |
| Current | systemBlue filled + halo | systemBlue/separator | Current |
| Upcoming | systemGray4 filled | separator | Future |
| Error | systemRed filled | separator | Error node |

**Variants**:
- **Vertical**: Vertical timeline (default)
- **Alternating**: Content alternates left/right
- **With Icons**: Nodes use semantic icons instead of dots

**Accessibility**:
- role="list", each item role="listitem"
- Timestamp uses `<time>` semantic markup
- Status not solely color-based; paired with icons/text

---

### 8.38 Tree

**HIG Name**: Outline View

**Anatomy**:
```
Tree (Outline)
├── Tree Node
│   ├── Disclosure Chevron (has children)
│   ├── Icon (optional)
│   ├── Label
│   └── Accessory (optional)
│   └── Children (indented, collapsible)
└── Tree Node...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Row height | 28pt (compact) / 44pt (touch) |
| Indent per level | 16pt |
| Chevron size | 12pt |
| Chevron color | secondaryLabel |
| Icon size | 20x20pt |
| Label font | Body 17pt |
| Horizontal padding | 16pt |

**States**:

| State | Background | Chevron | Description |
|---|---|---|---|
| Default | transparent | Right | Default |
| Expanded | transparent | Down (rotated 90 degrees) | Expanded |
| Hover | systemGray6 | Same | Hover |
| Selected | systemBlue | Same | Selected |
| Disabled | transparent | systemGray | Disabled |

**Variants**:
- **Single-select**: Single selection
- **Multi-select**: Multiple selection (macOS)
- **With Checkbox**: Checkbox before node (including indeterminate parent)

**Motion**:
- Expand/Collapse: 250ms ease-in-out
- Chevron rotation synchronizes

**Accessibility**:
- role="tree", nodes role="treeitem"
- aria-expanded / aria-level / aria-selected
- Support arrow key navigation, left/right expand/collapse

---

### 8.39 Divider

**HIG Name**: Separator

**Anatomy**:
```
Divider
├── Line
└── Label (optional, centered)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Line width | 1pt (hairline) |
| Color | separator |
| Full-width indent | 0pt (full width) / 16pt (inset) |
| With label spacing | 12pt on each side of label |
| Label font | Footnote 13pt secondaryLabel |
| Vertical divider height | Inherits parent container |

**Variants**:

| Variant | Description |
|---|---|
| Horizontal | Horizontal separator (default) |
| Vertical | Vertical separator (e.g., within toolbar) |
| Inset | Inset separator (list items, indent 16pt or 60pt) |
| Labeled | With centered text label |

**Accessibility**:
- Purely visual separator uses role="separator" or `<hr>`
- Decorative separators aria-hidden="true"
- Labeled separators should not carry semantic content

---

### 8.40 Grid / Layout

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (layout grid container)

**Anatomy**:
```
Grid / Layout
├── Grid Container
│   └── Grid Item (cell)
│       └── Content
└── Gutter (column/row spacing)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Base unit | 8pt grid |
| Column spacing (gutter) | 16pt (default) / 8pt (compact) |
| Row spacing | 16pt |
| Page margin | 16pt (iPhone) / 20pt (iPad) |
| Columns (mobile) | 4 columns |
| Columns (tablet/desktop) | 8-12 columns |

**Breakpoint Specifications**:

| Breakpoint | Width | Columns | Margin |
|---|---|---|---|
| Compact | < 600pt | 4 | 16pt |
| Regular | 600-1024pt | 8 | 20pt |
| Wide | > 1024pt | 12 | 24pt |

**Variants**:
- **Fixed Columns**: Fixed number of equal-width columns
- **Auto-fit**: Automatically arranges by minimum item width
- **Masonry**: Waterfall layout (uneven height items)

**Accessibility**:
- Visual layout does not change DOM reading order
- Grid is for layout only, not table semantics (if table needed, use 8.19 Table)
- Content follows safe area

---

### 8.41 Space / Stack

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (Stack spacing layout, corresponding to SwiftUI HStack / VStack concept)

**Anatomy**:
```
Stack
├── Child
├── Spacing (gap)
├── Child
└── ...
```

**Size Specifications (Spacing Tokens, following 8pt grid)**:

| Token | Value | Usage |
|---|---|---|
| xxSmall | 4pt | Tight elements |
| xSmall | 8pt | Default spacing |
| small | 12pt | Between small components |
| medium | 16pt | Standard spacing |
| large | 20pt | Section spacing |
| xLarge | 24pt | Large section spacing |
| xxLarge | 32pt | Page-level spacing |

**Alignment Specifications**:

| Property | Values |
|---|---|
| Axis direction | Horizontal (HStack) / Vertical (VStack) / Depth (ZStack) |
| Alignment | leading / center / trailing |
| Justify | start / center / end / space-between |

**Variants**:
- **HStack**: Horizontal arrangement + spacing
- **VStack**: Vertical arrangement + spacing
- **ZStack**: Overlapping alignment (depth)
- **Spacer**: Elastic spacer to fill space

**Accessibility**:
- Purely layout container, no additional semantics
- Maintain DOM order consistent with visual order
- Spacing uses unified tokens, avoid hardcoding

---

### 8.42 AspectRatio

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (aspect ratio container)

**Anatomy**:
```
AspectRatio
├── Ratio Box (fixed aspect ratio)
│   └── Content (fit / fill)
└── Placeholder (loading, optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Corner radius | 13pt (default content clipping) |
| Placeholder background | systemGray5 |
| Content clipping | clip to corner radius |
| Width | Adapts to parent container |

**Common Ratios**:

| Ratio | Usage |
|---|---|
| 1:1 | Avatar, square cover |
| 4:3 | Standard image |
| 16:9 | Video, wide landscape |
| 3:2 | Photo |
| 21:9 | Ultra-wide banner |

**Content Fit**:

| Mode | Description |
|---|---|
| Fit | Displays fully, may leave letterbox space |
| Fill | Fills container, overflows clipped |

**Accessibility**:
- Image content provides alt description
- Loading placeholder aria-busy="true"
- Purely decorative container aria-hidden

---

### 8.43 Popover

**HIG Name**: Popover

**Anatomy**:
```
Popover
├── Arrow (pointer to anchor)
└── Container
    ├── Header (optional)
    ├── Content
    └── Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 200pt |
| Maximum width | 400pt |
| Padding | 16pt |
| Corner radius | 13pt |
| Arrow size | 12pt |
| Background | secondarySystemBackground + blur |
| Overlay | None (lightweight) / transparent clickable to close |

**States**:

| State | Description |
|---|---|
| Presented | Expands from anchor, arrow points to anchor center |
| Dismissing | Fades out and retracts |

**Arrow Direction**:
- Automatically chooses up/down/left/right based on anchor position
- Auto-flips when space is insufficient

**Variants**:
- **iPad/macOS**: Floating panel with arrow
- **iPhone**: Can degrade to Sheet (bottom popup)

**Motion**:
- Expand: 250ms ease-out, scale and fade in from anchor
- Close: 200ms ease-in

**Accessibility**:
- role="dialog", focus moves in when opened
- Click outside or Esc to close, focus returns to anchor
- Anchor button marks aria-haspopup + aria-expanded

---

### 8.44 Modal

**HIG Name**: Modal Sheet / Full Screen Cover (large/full-screen modal, distinct from 8.9 small dialog)

**Anatomy**:
```
Modal
├── Overlay (scrim)
└── Container
    ├── Header
    │   ├── Cancel / Back
    │   ├── Title
    │   └── Done / Action
    ├── Content (scrollable)
    └── Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Top corner radius | 20pt (card Sheet) / 0pt (full screen) |
| Header height | 56pt |
| Padding | 16pt (iPhone) / 20pt (iPad) |
| Background | systemBackground |
| Overlay | black 40% opacity |
| Title font | Headline 17pt Semibold |
| Card top spacing | 10pt from top (reveals underlying layer) |

**States**:

| State | Description |
|---|---|
| Presented | Slides in from bottom to cover |
| Dragging | Dragging down (card type can dismiss) |
| Dismissing | Slides out and retracts |

**Variants**:
- **Card Sheet**: Card style, reveals underlying background at top (iOS 13+ default)
- **Full Screen**: Full screen cover, no reveal
- **Form Sheet**: Centered floating panel (iPad)

**Behavior**:
- Entry animation: 350ms ease-out
- Card type supports pull-down dismiss (when not blocking editing)
- Full screen type requires explicit Cancel/Done

**Accessibility**:
- role="dialog" aria-modal="true"
- Focus moves in when opened, background content aria-hidden
- Provide explicit close/done button, minimum touch 44x44pt

---

### 8.45 FAB

**HIG Name**: No floating action button convention; the following is a reasonable implementation derived from HIG design language (circular floating button based on Button)

**Anatomy**:
```
FAB
├── Background (circle)
├── Icon
└── Label (extended variant)
```

**Size Specifications**:

| Variant | Diameter |
|---|---|
| Regular (default) | 56pt |
| Small | 44pt |
| Extended | Height 56pt, width adapts |

**General Specifications**:

| Property | Value |
|---|---|
| Corner radius | full (circle) / 28pt (Extended) |
| Icon size | 24x24pt |
| Background | systemBlue |
| Icon color | white |
| Edge margin | 16pt (avoid safe area) |
| Extended padding | 20pt horizontal |

**States**:

| State | Background | Description |
|---|---|---|
| Default | systemBlue | Default |
| Hover | systemBlue darken 10% | Hover |
| Pressed | systemBlue darken 20% | Pressed |
| Disabled | systemGray4 | Disabled |

**Variants**:
- **Regular**: Icon circular floating button
- **Extended**: Icon + text capsule
- **Speed Dial**: Click to expand multiple sub-actions

**Motion**:
- Press scale 0.95x, 100ms
- Speed Dial expand: 250ms ease-out staggered appearance

**Accessibility**:
- Minimum touch target 44x44pt
- Icon-only variant must provide aria-label
- Should not block key content; follow safe area

---

### 8.46 SearchBar

**HIG Name**: Search Field

**Anatomy**:
```
SearchBar
├── Background
├── Leading Search Icon
├── Placeholder / Input Text
├── Clear Button (optional)
└── Cancel Button (optional, when active)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 36pt |
| Corner radius | 10pt |
| Horizontal padding | 8pt |
| Background | tertiarySystemFill |
| Search icon | 16pt, secondaryLabel |
| Placeholder text | secondaryLabel, Body 17pt |
| Clear button | 16pt, systemGray |
| Cancel font | Body 17pt, systemBlue |

**States**:

| State | Background | Description |
|---|---|---|
| Default | tertiarySystemFill | Default |
| Focused | tertiarySystemFill + Cancel visible | Focused input |
| Filled | tertiarySystemFill + Clear visible | Has content |
| Disabled | systemGray6 | Disabled |

**Variants**:
- **Inline**: Search embedded in navigation bar
- **With Scope Bar**: Segmented filter below
- **Prominent / Minimized**: Expand/collapse on scroll

**Accessibility**:
- role="search", input type="search"
- Associate visible or hidden label
- Clear / Cancel minimum touch 44x44pt

---

### 8.47 Rating

**HIG Name**: No native component; the following is a reasonable implementation derived from HIG design language (star rating)

**Anatomy**:
```
Rating
├── Star Item (filled / half / empty)
├── Star Item...
└── Value Label (optional)
```

**Size Specifications**:

| Variant | Star Size | Touch Area |
|---|---|---|
| Small | 16pt | 28pt |
| Medium (default) | 24pt | 44pt |
| Large | 32pt | 44pt |

**General Specifications**:

| Property | Value |
|---|---|
| Star spacing | 4pt |
| Fill color | systemYellow |
| Empty star color | systemGray4 |
| Value label font | Subhead 15pt secondaryLabel |

**States**:

| State | Star Color | Description |
|---|---|---|
| Filled | systemYellow | Rated |
| Half | systemYellow (half) | Half star |
| Empty | systemGray4 | Not rated |
| Hover | systemYellow 60% | Hover preview (interactive) |
| Disabled | systemGray5 | Read-only/Disabled |

**Variants**:
- **Interactive**: Clickable rating
- **Read-only**: Display only (supports half stars)
- **Custom Icon**: Heart/other icons instead of stars

**Accessibility**:
- role="slider" or radiogroup + aria-valuenow / aria-valuemax
- Provide numeric text equivalent (e.g., "4.5 / 5")
- Interactive items minimum touch 44x44pt

---

### 8.48 ColorPicker

**HIG Name**: Color Well

**Anatomy**:
```
ColorPicker
├── Color Well (trigger)
│   ├── Current Color Swatch
│   └── Ring Border
└── Picker Popover
    ├── Spectrum / Grid
    ├── Sliders (RGB / HSB / Opacity)
    ├── Preset Swatches
    └── Hex Input
```

**Size Specifications**:

| Property | Value |
|---|---|
| Color Well diameter | 28pt |
| Well corner radius | full (circle) |
| Well border | 2pt systemBackground + 1pt separator |
| Popover corner radius | 13pt |
| Popover background | secondarySystemBackground + blur |
| Preset swatch size | 24x24pt |
| Preset swatch corner radius | full |
| Slider height | 4pt |

**States**:

| State | Description |
|---|---|
| Default | Displays current color swatch |
| Hover | Border highlight (systemBlue ring) |
| Focused | systemBlue 2pt outline |
| Active | Popover expanded |
| Disabled | systemGray4 swatch, reduced opacity |

**Variants**:
- **Compact Well**: Circular swatch trigger only
- **With Hex**: Popover includes hex input
- **With Opacity**: Includes opacity slider

**Accessibility**:
- Trigger role="button" aria-haspopup, minimum touch 44x44pt
- Current color provides text/Hex equivalent description
- Sliders support keyboard stepping, aria-valuenow

---

### 8.49 Calendar

**HIG Name**: Calendar View (month calendar view, distinct from 8.18 DatePicker compact picker)

**Anatomy**:
```
Calendar
├── Header
│   ├── Month / Year Title
│   └── Navigation (prev / next)
├── Weekday Labels
├── Day Grid
│   └── Day Cell
│       ├── Date Number
│       └── Event Indicator (dot, optional)
└── Footer (optional, today / actions)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Cell size | 44x44pt |
| Cell spacing | 4pt |
| Title font | Title 3 20pt Semibold |
| Weekday label font | Caption 1 12pt secondaryLabel |
| Date font | Body 17pt |
| Navigation button | 44x44pt, systemBlue |
| Event dot | 6pt, systemBlue |
| Grid background | systemBackground |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | label | Current month date |
| Today | systemBlue border circle | systemBlue | Today |
| Selected | systemBlue circle | white | Selected |
| Hover | systemGray6 circle | label | Hover |
| In Range | systemBlue 15% opacity | label | In range (range selection) |
| Outside Month | transparent | tertiaryLabel | Not current month |
| Disabled | transparent | systemGray | Not selectable |

**Variants**:
- **Month View**: Month grid (default)
- **Range Selection**: Start-end range highlighting
- **Multi-event**: Cell with multiple event dots
- **Week View**: Single week horizontal view

**Motion**:
- Month transition: 300ms ease-out horizontal slide
- Date selection: Spring scale circle background

**Accessibility**:
- role="grid", cells role="gridcell"
- Selected date marks aria-selected, today aria-current="date"
- Support arrow key navigation on date grid
- Dates use full aria-label (e.g., "June 8, 2026, Monday")
- Cell minimum touch 44x44pt

---

## 9. Platform Differences

### 9.1 iOS vs macOS

| Feature | iOS | macOS |
|---|---|---|
| Navigation | Tab Bar + Navigation Bar | Sidebar + Toolbar |
| Primary interaction | Touch | Mouse + Keyboard |
| Context menu | Long press | Right click |
| Dialogs | Sheet / Alert | Sheet / Dialog |
| List selection | Single/Multi select | Single/Multi select + drag |
| Font size | Smaller, compact | Larger, spacious |
| Margins | 16pt | 20pt |

### 9.2 iPadOS

- Supports multi-window and split view
- Uses Sidebar navigation (similar to macOS)
- Supports pointer hover effects
- Dialogs use Popover

### 9.3 watchOS

- Very small screen, minimal design
- Uses vertical scrolling lists
- Digital crown interaction
- Dark Mode enforced

### 9.4 tvOS

- Far viewing distance, large fonts
- Focus-driven navigation
- Uses Parallax effects
- Supports Dark Mode

---

## 10. Token Reference Table

### 10.1 Color Tokens

| Token | Light | Dark |
|---|---|---|
| systemBlue | `#007AFF` | `#0A84FF` |
| systemGreen | `#34C759` | `#30D158` |
| systemRed | `#FF3B30` | `#FF453A` |
| systemYellow | `#FFCC00` | `#FFD60A` |
| label | `#000000` | `#FFFFFF` |
| secondaryLabel | `#3C3C4399` | `#EBEBF599` |
| tertiaryLabel | `#3C3C434D` | `#EBEBF54D` |
| systemBackground | `#FFFFFF` | `#000000` |
| secondarySystemBackground | `#F2F2F7` | `#1C1C1E` |
| tertiarySystemBackground | `#FFFFFF` | `#2C2C2E` |
| separator | `#C6C6C8` | `#38383A` |
| systemGray5 | `#E5E5EA` | `#2C2C2E` |
| systemGray6 | `#F2F2F7` | `#1C1C1E` |

### 10.2 Font Tokens

| Token | Size | Weight | Line Height |
|---|---|---|---|
| largeTitle | 34pt | Regular | 41pt |
| title1 | 28pt | Regular | 34pt |
| title2 | 22pt | Regular | 28pt |
| title3 | 20pt | Regular | 25pt |
| headline | 17pt | Semibold | 22pt |
| body | 17pt | Regular | 22pt |
| callout | 16pt | Regular | 21pt |
| subhead | 15pt | Regular | 20pt |
| footnote | 13pt | Regular | 18pt |
| caption1 | 12pt | Regular | 16pt |
| caption2 | 11pt | Regular | 13pt |

### 10.3 Spacing Tokens

| Token | Value |
|---|---|
| xxxSmall | 2pt |
| xxSmall | 4pt |
| xSmall | 8pt |
| small | 12pt |
| medium | 16pt |
| large | 20pt |
| xLarge | 24pt |
| xxLarge | 32pt |
| xxxLarge | 48pt |
| huge | 64pt |

### 10.4 Corner Radius Tokens

| Token | Value |
|---|---|
| small | 8pt |
| medium | 10pt |
| large | 13pt |
| xLarge | 20pt |
| xxLarge | 27pt |
| full | 9999px |

### 10.5 Shadow Tokens

| Token | Parameters |
|---|---|
| shadowSmall | `0 1px 3px rgba(0,0,0,0.1)` |
| shadowMedium | `0 4px 12px rgba(0,0,0,0.15)` |
