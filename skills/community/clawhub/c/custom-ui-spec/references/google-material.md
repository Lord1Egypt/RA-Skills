# Google Material Design 3

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Spacing and Grid](#4-spacing-and-grid)
5. [Corner Radius and Shape](#5-corner-radius-and-shape)
6. [Shadow and Elevation](#6-shadow-and-elevation)
7. [Motion Specifications](#7-motion-specifications)
8. [Component Specifications](#8-component-specifications)
9. [Platform Differences](#9-platform-differences)
10. [Token Reference Table](#10-token-reference-table)

---

## 1. Design Principles

### 1.1 Material is the Metaphor

- Interface elements behave like physical materials
- Materials have thickness, shadows, and layers
- Materials can move, transform, and merge
- Materials do not penetrate each other; they stack in layers

### 1.2 Bold, Graphic, Intentional

- Use bold typography and color
- Graphic elements are clear and unambiguous
- Every design decision has a purpose
- Avoid decorative elements

### 1.3 Motion Provides Meaning

- Motion helps users understand interface changes
- Feedback is immediate and perceptible
- Transitions suggest spatial relationships
- Motion guides user attention

### 1.4 Core Design Values

| Value | Description |
|---|---|
| Adaptability | Design adapts to different screens, platforms, and input methods |
| Consistency | Use a unified design language and components |
| Hierarchy | Establish clear hierarchy through elevation, color, and motion |
| Feedback | Provide immediate feedback for every user action |
| Personalization | Support dynamic color and theme customization |

---

## 2. Color System

> **Note**: The following lists only the Material 3 default classic palette as a reference. Complete brand and theme colors are defined in the separate color specification skill.

### 2.1 Primary / Secondary / Tertiary Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| primary | `#6750A4` | `#D0BCFF` | Primary color |
| onPrimary | `#FFFFFF` | `#381E72` | Text on primary |
| primaryContainer | `#EADDFF` | `#4F378B` | Primary container |
| onPrimaryContainer | `#21005D` | `#EADDFF` | Text on primary container |
| secondary | `#625B71` | `#CCC2DC` | Secondary color |
| onSecondary | `#FFFFFF` | `#332D41` | Text on secondary |
| secondaryContainer | `#E8DEF8` | `#4A4458` | Secondary container |
| onSecondaryContainer | `#1D192B` | `#E8DEF8` | Text on secondary container |
| tertiary | `#7D5260` | `#EFB8C8` | Tertiary color |
| onTertiary | `#FFFFFF` | `#492532` | Text on tertiary |
| tertiaryContainer | `#FFD8E4` | `#633B48` | Tertiary container |
| onTertiaryContainer | `#31111D` | `#FFD8E4` | Text on tertiary container |

### 2.2 Surface Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| surface | `#FFFBFE` | `#1C1B1F` | Primary surface |
| onSurface | `#1C1B1F` | `#E6E1E5` | Text on surface |
| surfaceVariant | `#E7E0EC` | `#49454F` | Surface variant |
| onSurfaceVariant | `#49454F` | `#CAC4D0` | Text on surface variant |
| surfaceDim | `#DED8E1` | `#141218` | Dim surface |
| surfaceBright | `#F7F2FA` | `#3B383E` | Bright surface |
| inverseSurface | `#322F35` | `#E6E1E5` | Inverse surface |
| inverseOnSurface | `#F5EFF7` | `#322F35` | Text on inverse surface |

### 2.3 Background and Error Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| background | `#FFFBFE` | `#1C1B1F` | Background |
| onBackground | `#1C1B1F` | `#E6E1E5` | Text on background |
| error | `#B3261E` | `#F2B8B5` | Error |
| onError | `#FFFFFF` | `#601410` | Text on error |
| errorContainer | `#F9DEDC` | `#8C1D18` | Error container |
| onErrorContainer | `#410E0B` | `#F9DEDC` | Text on error container |

### 2.4 Outline Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| outline | `#79747E` | `#938F99` | Outline |
| outlineVariant | `#CAC4D0` | `#49454F` | Outline variant |

### 2.5 Surface Container Colors

| Token | Light | Dark | Usage |
|---|---|---|---|
| surfaceContainerLowest | `#FFFFFF` | `#0F0D13` | Lowest container |
| surfaceContainerLow | `#F7F2FA` | `#1D1B20` | Low container |
| surfaceContainer | `#F3EDF7` | `#211F26` | Standard container |
| surfaceContainerHigh | `#ECE6F0` | `#2B2930` | High container |
| surfaceContainerHighest | `#E6E0E9` | `#36343B` | Highest container |

### 2.6 Color Usage Principles

- Use surface colors to build interface hierarchy
- Use primary/secondary/tertiary to emphasize interactive elements
- Use on-* colors to ensure text readability
- Container colors are used for cards, dialogs, etc.
- Support dynamic color (Android 12+ extracts from wallpaper)

---

## 3. Typography

### 3.1 Font Family

- **Primary font**: Roboto (Android/Web) / Noto Sans (Chinese)
- **Monospace font**: Roboto Mono
- **Fallback fonts**: `Roboto, "Noto Sans", -apple-system, BlinkMacSystemFont, sans-serif`

### 3.2 Type Scale (Font Ramp)

| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|---|---|---|---|---|---|
| displayLarge | 57pt | Regular | 64pt | -0.25pt | Largest display |
| displayMedium | 45pt | Regular | 52pt | 0pt | Large display |
| displaySmall | 36pt | Regular | 44pt | 0pt | Small display |
| headlineLarge | 32pt | Regular | 40pt | 0pt | Large headline |
| headlineMedium | 28pt | Regular | 36pt | 0pt | Medium headline |
| headlineSmall | 24pt | Regular | 32pt | 0pt | Small headline |
| titleLarge | 22pt | Regular | 28pt | 0pt | Large title |
| titleMedium | 16pt | Medium | 24pt | 0.15pt | Medium title |
| titleSmall | 14pt | Medium | 20pt | 0.1pt | Small title |
| bodyLarge | 16pt | Regular | 24pt | 0.5pt | Large body |
| bodyMedium | 14pt | Regular | 20pt | 0.25pt | Medium body |
| bodySmall | 12pt | Regular | 16pt | 0.4pt | Small body |
| labelLarge | 14pt | Medium | 20pt | 0.1pt | Large label |
| labelMedium | 12pt | Medium | 16pt | 0.5pt | Medium label |
| labelSmall | 11pt | Medium | 16pt | 0.5pt | Small label |

### 3.3 Font Weights

| Weight | Value | Usage |
|---|---|---|
| Regular | 400 | Body text, titles |
| Medium | 500 | Buttons, labels, small titles |
| Bold | 700 | Rarely used |

### 3.4 Typography Principles

- Body text uses bodyLarge (16pt) or bodyMedium (14pt)
- Titles use Regular weight, not Bold
- Buttons and labels use Medium weight
- Letter spacing adjusts based on font size
- Supports text scaling

---

## 4. Spacing and Grid

### 4.1 Base Grid

- **Base unit**: 8dp
- All spacing and sizes should be multiples of 8
- Exception: 4dp can be used for very tight spacing

### 4.2 Standard Spacing Values

| Token | Value | Usage |
|---|---|---|
| none | 0dp | No spacing |
| extraSmall | 4dp | Very tight |
| small | 8dp | Default element spacing |
| medium | 16dp | Standard padding |
| large | 24dp | Component spacing |
| extraLarge | 32dp | Section spacing |
| extraExtraLarge | 48dp | Large section spacing |
| extraExtraExtraLarge | 64dp | Page spacing |

### 4.3 Layout Grid

| Breakpoint | Width | Columns | Spacing |
|---|---|---|---|
| Compact | < 600dp | 4 | 16dp |
| Medium | 600-840dp | 8 | 24dp |
| Expanded | 840-1200dp | 12 | 24dp |
| Large | 1200-1600dp | 12 | 24dp |
| ExtraLarge | > 1600dp | 12 | 24dp |

### 4.4 Margin Specifications

| Scenario | Margin |
|---|---|
| Page horizontal margin | 16dp |
| Card padding | 16dp |
| Button padding | 24dp horizontal, 8dp vertical |
| List item padding | 16dp horizontal, 12dp vertical |
| Form field spacing | 16dp |
| Icon to text spacing | 8dp |

---

## 5. Corner Radius and Shape

### 5.1 Shape Tokens

| Token | Value | Usage |
|---|---|---|
| none | 0dp | Right angle |
| extraSmall | 4dp | Small elements |
| small | 8dp | Buttons, input fields |
| medium | 12dp | Cards |
| large | 16dp | Large cards |
| extraLarge | 28dp | Dialogs, bottom Sheet |
| full | 9999dp | Capsule buttons, avatars |

### 5.2 Component-Specific Corner Radius

| Component | Corner Radius | Description |
|---|---|---|
| Button | full | Capsule shape |
| Card | medium (12dp) | Standard card |
| Dialog | extraLarge (28dp) | Dialog |
| Input | small (8dp) | Input field |
| Menu | medium (12dp) | Menu |
| Chip | full | Capsule shape |
| Avatar | full | Circle |
| FAB | full | Circle |

### 5.3 Corner Radius Principles

- Buttons use full corner radius (capsule shape)
- Cards use medium corner radius
- Dialogs use extraLarge corner radius
- Nested element corner radius should be smaller than parent container

---

## 6. Shadow and Elevation

### 6.1 Elevation System

Material uses an elevation system to express hierarchical relationships:

| Token | Value | Usage |
|---|---|---|
| level0 | 0dp | Ground level |
| level1 | 1dp | Card static state |
| level2 | 3dp | Card hover state |
| level3 | 6dp | Button pressed, Menu |
| level4 | 8dp | Bottom navigation, FAB |
| level5 | 12dp | Dialog, Drawer |

### 6.2 Shadow Specifications

| Elevation | Shadow Parameters |
|---|---|
| 0dp | No shadow |
| 1dp | `0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.14)` |
| 2dp | `0 2px 4px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.14)` |
| 3dp | `0 3px 6px rgba(0,0,0,0.12), 0 2px 4px rgba(0,0,0,0.14)` |
| 4dp | `0 4px 8px rgba(0,0,0,0.12), 0 2px 4px rgba(0,0,0,0.14)` |
| 6dp | `0 6px 12px rgba(0,0,0,0.12), 0 3px 6px rgba(0,0,0,0.14)` |
| 8dp | `0 8px 16px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.14)` |
| 12dp | `0 12px 24px rgba(0,0,0,0.12), 0 6px 12px rgba(0,0,0,0.14)` |
| 16dp | `0 16px 32px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.14)` |
| 24dp | `0 24px 48px rgba(0,0,0,0.12), 0 12px 24px rgba(0,0,0,0.14)` |

### 6.3 Elevation Principles

- Static elements use 0dp or 1dp
- Elevate on hover
- Lower elevation when pressed
- Modal layers use the highest elevation
- Use elevation changes to express interaction states

---

## 7. Motion Specifications

### 7.1 Animation Duration

| Type | Duration | Usage |
|---|---|---|
| Instant feedback | 50-100ms | Button press, switch toggle |
| Fast transition | 150-200ms | Color change, state switch |
| Standard transition | 250-300ms | Element show/hide |
| Complex animation | 350-500ms | Page switch, dialog |
| Large movement | 500-700ms | Large element movement |

### 7.2 Easing Functions

| Name | Curve | Usage |
|---|---|---|
| Standard | `cubic-bezier(0.2, 0, 0, 1)` | Standard transition |
| Decelerate | `cubic-bezier(0, 0, 0.2, 1)` | Element entry |
| Accelerate | `cubic-bezier(0.4, 0, 1, 1)` | Element exit |
| Emphasized | `cubic-bezier(0.2, 0, 0, 1)` | Emphasized animation |

### 7.3 Motion Principles

- Motion should have purpose, helping users understand changes
- Use physical metaphors
- Maintain 60fps
- Support reduced motion preference
- Use Ripple effect for touch feedback

### 7.4 Ripple Effect

- Originates from touch point and spreads outward
- Color: onSurface color at 10-20% opacity
- Duration: 300ms
- Fades out after reaching element boundaries

---

## 8. Component Specifications

### 8.1 Button

**Material Name**: Button

**Anatomy**:
```
Button
├── Container
├── Label (Text)
└── Icon (optional)
```

**Size Specifications**:

| Variant | Height | Horizontal Padding | Corner Radius |
|---|---|---|---|
| Small | 32dp | 16dp | full |
| Medium (default) | 40dp | 24dp | full |
| Large | 48dp | 32dp | full |

**States**:

| State | Container | Text | Description |
|---|---|---|---|
| Default | primaryContainer | onPrimaryContainer | Default |
| Hover | primaryContainer + 8% onPrimary | onPrimaryContainer | Hover |
| Pressed | primaryContainer + 12% onPrimary | onPrimaryContainer | Pressed |
| Focused | primaryContainer + onPrimary outline | onPrimaryContainer | Focused |
| Disabled | onSurface 12% opacity | onSurface 38% opacity | Disabled |

**Variants**:
- **Elevated**: With shadow (1dp), surface color background
- **Filled**: primaryContainer background (default)
- **Tonal**: secondaryContainer background
- **Outlined**: Transparent background, outline border
- **Text**: Transparent background, no border

**Accessibility**:
- Minimum touch target: 48x48dp
- Color contrast ratio >= 4.5:1
- Support keyboard focus
- Focus indicator clearly visible

---

### 8.2 TextField

**Material Name**: Text Field

**Anatomy**:
```
TextField
├── Container
├── Label (floating)
├── Placeholder Text
├── Input Text
├── Leading Icon (optional)
├── Trailing Icon / Action (optional)
└── Supporting Text (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 56dp |
| Horizontal padding | 16dp |
| Corner radius | small (8dp) |
| Border | 1dp solid outline |

**States**:

| State | Border | Container | Label | Description |
|---|---|---|---|---|
| Default | outline | transparent | onSurfaceVariant | Default |
| Hover | onSurface | transparent | onSurfaceVariant | Hover |
| Focused | primary | transparent | primary | Focused |
| Filled | outline | transparent | onSurfaceVariant | Has content |
| Error | error | transparent | error | Error |
| Disabled | onSurface 38% | onSurface 12% | onSurface 38% | Disabled |

**Accessibility**:
- Floating label associated with input
- Error state provides error text
- Support keyboard navigation

---

### 8.3 Checkbox

**Material Name**: Checkbox

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
| Box size | 18x18dp |
| Box corner radius | 2dp |
| Label spacing | 16dp |
| Checkmark line width | 2dp |

**States**:

| State | Box Background | Border | Checkmark | Description |
|---|---|---|---|---|
| Unchecked | transparent | outline | None | Unselected |
| Checked | primary | primary | onPrimary | Selected |
| Indeterminate | primary | primary | onPrimary line | Mixed |
| Hover (unchecked) | onSurface 8% | outline | None | Hover |
| Hover (checked) | primary + 8% onPrimary | primary | onPrimary | Hover checked |
| Disabled | onSurface 12% | onSurface 38% | onSurface 38% | Disabled |

---

### 8.4 RadioButton

**Material Name**: Radio Button

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
| Outer circle diameter | 20dp |
| Inner dot diameter | 10dp |
| Border width | 2dp |
| Label spacing | 16dp |

**States**:

| State | Outer Circle | Inner Dot | Description |
|---|---|---|---|
| Unselected | transparent + outline | None | Unselected |
| Selected | transparent + primary | primary | Selected |
| Hover | onSurface 8% | Same | Hover |
| Disabled | onSurface 38% | onSurface 38% | Disabled |

---

### 8.5 Switch

**Material Name**: Switch

**Anatomy**:
```
Switch
├── Track (pill shape)
└── Handle (circle with icon)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Track width | 52dp |
| Track height | 32dp |
| Thumb diameter | 24dp |
| Thumb margin | 4dp |

**States**:

| State | Track | Thumb | Description |
|---|---|---|---|
| Off | outline | surface + shadow1 | Off |
| On | primary | onPrimary + shadow1 | On |
| Hover (off) | onSurface 8% | surface + shadow2 | Hover off |
| Hover (on) | primary + 8% onPrimary | onPrimary + shadow2 | Hover on |
| Disabled (off) | onSurface 12% | surface | Disabled off |
| Disabled (on) | onSurface 12% | onSurface | Disabled on |

**Motion**:
- Toggle animation: 150ms standard easing
- Thumb movement uses spring effect

---

### 8.6 Slider

**Material Name**: Slider

**Anatomy**:
```
Slider
├── Track (background)
├── Active Track (value)
└── Thumb (handle)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Track height | 4dp |
| Track corner radius | 2dp |
| Thumb diameter | 20dp |
| Minimum touch area | 48x48dp |

**States**:

| State | Active Track | Thumb | Description |
|---|---|---|---|
| Default | primary | surface + shadow1 | Default |
| Hover | primary | surface + shadow2 | Hover |
| Pressed | primary | surface + shadow1 + enlarge | Pressed |
| Disabled | onSurface 38% | onSurface 38% | Disabled |

---

### 8.7 ProgressIndicator

**Material Name**: Progress Indicator

**Anatomy**:
```
ProgressIndicator
├── Track (background)
└── Indicator (fill / spinner)
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Linear | Height 4dp, width adapts |
| Circular | Diameter 24dp / 40dp / 48dp |

**Linear Progress Bar**:
- Track: surfaceVariant
- Fill: primary
- Corner radius: 2dp

**Circular Progress Bar**:
- Line width: 4dp
- Color: primary
- Rotation animation: 1.4s linear infinite

**Indeterminate State**:
- Linear: Loop animation
- Circular: Continuous rotation

---

### 8.8 Menu

**Material Name**: Menu

**Anatomy**:
```
Menu
├── Menu Item
│   ├── Icon (optional)
│   ├── Label
│   ├── Shortcut (optional)
│   └── Trailing Icon (optional)
├── Divider
└── Menu Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 180dp |
| Maximum width | 320dp |
| Item height | 48dp |
| Item padding | 16dp horizontal |
| Corner radius | medium (12dp) |
| Shadow | 3dp |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | onSurface | Default |
| Hover | onSurface 8% | onSurface | Hover |
| Pressed | onSurface 12% | onSurface | Pressed |
| Focused | onSurface 8% + primary outline | onSurface | Focused |
| Disabled | transparent | onSurface 38% | Disabled |

---

### 8.9 Dialog

**Material Name**: Dialog

**Anatomy**:
```
Dialog
├── Container
├── Icon (optional)
├── Headline
├── Supporting Text
├── TextField (optional)
└── Actions
    ├── Primary Action
    └── Secondary Action
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 280dp |
| Maximum width | 560dp |
| Corner radius | extraLarge (28dp) |
| Padding | 24dp |
| Title to content spacing | 16dp |
| Content to button spacing | 24dp |

**Background**:
- Dialog background: surfaceContainerHigh
- Overlay: scrim (onSurface 32% opacity)

**Button Layout**:
- Primary action on the right
- Secondary action on the left
- 3+ buttons vertically arranged

---

### 8.10 Card

**Material Name**: Card

**Anatomy**:
```
Card
├── Container
├── Media (optional)
├── Header (optional)
├── Content
├── Actions (optional)
└── Divider (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Corner radius | medium (12dp) |
| Padding | 16dp |
| Background | surfaceContainerLow |
| Border | None |
| Shadow | 1dp (static) |

**States**:

| State | Background | Shadow | Description |
|---|---|---|---|
| Default | surfaceContainerLow | 1dp | Default |
| Hover | surfaceContainerLow | 3dp | Hover |
| Pressed | surfaceContainer | 1dp | Pressed |
| Dragged | surfaceContainer | 4dp | Drag |

---

### 8.11 List

**Material Name**: List

**Anatomy**:
```
List
├── List Item
│   ├── Leading Element (icon / avatar / checkbox)
│   ├── Content
│   │   ├── Headline
│   │   └── Supporting Text (optional)
│   ├── Trailing Element (icon / text / switch)
│   └── Divider
└── List Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Single line height | 48dp |
| Double line height | 64dp |
| Triple line height | 88dp |
| Item padding | 16dp horizontal |
| Separator | 1dp, inset 16dp or 56dp |

**States**:

| State | Background | Description |
|---|---|---|
| Default | transparent | Default |
| Hover | onSurface 8% | Hover |
| Selected | onSurface 12% | Selected |
| Pressed | onSurface 12% | Pressed |

---

### 8.12 NavigationBar

**Material Name**: Bottom App Bar / Top App Bar

**Anatomy**:
```
TopAppBar
├── Leading Icon (menu / back)
├── Headline
└── Trailing Icons (actions)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 64dp (small) / 80dp (medium) / 152dp (large) |
| Background | surface |
| Title font | titleLarge 22pt |
| Large title font | displaySmall 36pt |

**Bottom Navigation**:
- Height: 80dp
- Icon size: 24x24dp
- Label font: labelMedium 12pt
- Selected: primary color
- Unselected: onSurfaceVariant

---

### 8.13 TabBar

**Material Name**: Tabs

**Anatomy**:
```
Tabs
├── Tab List
│   └── Tab Item
└── Tab Panel
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item height | 48dp |
| Item padding | 16dp horizontal |
| Selected indicator | Bottom 3dp primary bar |
| Unselected indicator | Bottom 1dp outline bar |

**States**:

| State | Text | Indicator | Description |
|---|---|---|---|
| Selected | primary | primary 3dp | Selected |
| Unselected | onSurfaceVariant | transparent | Unselected |
| Hover | onSurface | onSurface 1dp | Hover |

---

### 8.14 SegmentedControl

**Material Name**: No direct equivalent; use Tabs or Toggle Button as substitute

---

### 8.15 Tooltip

**Material Name**: Tooltip

**Anatomy**:
```
Tooltip
├── Container
├── Label
└── Arrow
```

**Size Specifications**:

| Property | Value |
|---|---|
| Maximum width | 200dp |
| Padding | 8dp 12dp |
| Corner radius | small (8dp) |
| Font | bodySmall 12pt |
| Background | inverseSurface |
| Text | inverseOnSurface |

**Behavior**:
- Shows after 500ms hover
- Shows after 500ms long press (mobile)
- Hides 0ms after leaving target

---

### 8.16 Badge

**Material Name**: Badge

**Anatomy**:
```
Badge
├── Background
└── Label (number / dot)
```

**Size Specifications**:

| Variant | Size |
|---|---|
| Small | 6x6dp |
| Large | Height 16dp, width adapts |

**Number Badge**:
- Height: 16dp
- Minimum width: 16dp
- Padding: 4dp horizontal
- Corner radius: full
- Background: error
- Text: onError, labelSmall 11pt

---

### 8.17 Chip

**Material Name**: Chip

**Anatomy**:
```
Chip
├── Container
├── Leading Icon (optional)
├── Label
└── Trailing Icon (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 32dp |
| Horizontal padding | 12dp |
| Corner radius | full |
| Background | surfaceContainerLow |

**Variants**:
- **Assist**: Auxiliary action, surfaceContainerLow
- **Filter**: Filtering, selectable
- **Input**: Input tag, removable
- **Suggestion**: Suggestion, surfaceContainerLow

**States**:

| State | Background | Description |
|---|---|---|
| Default | surfaceContainerLow | Default |
| Selected | secondaryContainer | Selected |
| Hover | onSurface 8% | Hover |

---

### 8.18 DatePicker

**Material Name**: Date Picker

**Anatomy**:
```
DatePicker
├── Header (month / year selector)
├── Weekday Labels
└── Day Grid
    └── Day Cell
```

**Size Specifications**:

| Property | Value |
|---|---|
| Cell size | 40x40dp |
| Cell spacing | 0dp |
| Selected background | primary circle |
| Today marker | primary border circle |
| Corner radius | extraLarge (28dp) |

---

### 8.19 Table

**Material Name**: Data Table

**Anatomy**:
```
DataTable
├── Table Header
│   └── Column Header
├── Table Row
│   └── Cell
└── Table Footer (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Row height | 52dp |
| Header height | 56dp |
| Cell padding | 16dp horizontal |
| Separator | 1dp, full width |

**Table Header**:
- Font: titleSmall 14pt Medium
- Color: onSurface
- Background: surface

**Row States**:

| State | Background | Description |
|---|---|---|
| Default | transparent | Default |
| Hover | onSurface 8% | Hover |
| Selected | onSurface 12% | Selected |
| Pressed | onSurface 12% | Pressed |

---

### 8.20 Breadcrumb

**Material Name**: No direct equivalent

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
| Item font | bodyMedium 14pt |
| Separator | "/" |
| Separator color | outline |
| Current item | onSurface |
| Clickable item | primary |

---

### 8.21 Select

**Material Name**: Exposed Dropdown Menu / Select

**Anatomy**:
```
Select
├── Anchor (Text Field style)
│   ├── Label (floating)
│   ├── Selected Value
│   └── Trailing Icon (arrow down)
└── Menu (when expanded)
    └── Menu Item
        ├── Leading Icon (optional)
        ├── Label
        └── Trailing Check (selected)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Anchor minimum height | 56dp |
| Horizontal padding | 16dp |
| Anchor corner radius | small (8dp) |
| Menu corner radius | medium (12dp) |
| Menu item height | 48dp |
| Menu shadow | 3dp |

**States**:

| State | Border | Container | Label | Description |
|---|---|---|---|---|
| Default | outline | transparent | onSurfaceVariant | Default |
| Hover | onSurface | transparent | onSurfaceVariant | Hover |
| Focused / Open | primary | transparent | primary | Focused/Expanded |
| Filled | outline | transparent | onSurfaceVariant | Has selected value |
| Error | error | transparent | error | Error |
| Disabled | onSurface 38% | onSurface 12% | onSurface 38% | Disabled |

**Variants**:
- **Filled**: surfaceContainerHighest background, bottom 1dp indicator line
- **Outlined**: Transparent background, outline border (default)

**Accessibility**:
- Touch target >= 48x48dp
- Expanded menu supports keyboard up/down navigation
- Selected item provides visual marker, role association

---

### 8.22 Autocomplete

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (auto-complete based on Menu + Text Field)

**Anatomy**:
```
Autocomplete
├── Text Field
│   ├── Label (floating)
│   ├── Input Text
│   ├── Leading Icon (search, optional)
│   └── Trailing Icon (clear, optional)
└── Suggestion Menu (on input)
    └── Menu Item
        ├── Label (match highlight)
        └── Supporting Text (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Input field minimum height | 56dp |
| Horizontal padding | 16dp |
| Input corner radius | small (8dp) |
| Suggestion menu corner radius | medium (12dp) |
| Suggestion item height | 48dp |
| Suggestion menu background | surfaceContainer |
| Suggestion menu shadow | 3dp |

**States**:

| State | Border | Container | Description |
|---|---|---|---|
| Default | outline | transparent | Default |
| Hover | onSurface | transparent | Hover |
| Focused | primary | transparent | Focused (show suggestions) |
| Error | error | transparent | Error |
| Disabled | onSurface 38% | onSurface 12% | Disabled |

**Suggestion Item States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | onSurface | Default |
| Hover | onSurface 8% | onSurface | Hover |
| Active (keyboard) | onSurface 12% | onSurface | Keyboard selected |

**Accessibility**:
- Touch target >= 48x48dp
- Input updates suggestion list in real-time
- Keyboard up/down to select, Enter to confirm, Esc to close
- Matching text visually highlighted for easy identification

---

### 8.23 Textarea

**Material Name**: Text Field (multiline)

**Anatomy**:
```
Textarea
├── Container
├── Label (floating)
├── Input Text (multiline)
├── Supporting Text (optional)
└── Character Counter (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 56dp (single line start) |
| Horizontal padding | 16dp |
| Vertical padding | 16dp |
| Corner radius | small (8dp) |
| Border | 1dp solid outline |
| Line height | bodyLarge 24pt |

**States**:

| State | Border | Container | Label | Description |
|---|---|---|---|---|
| Default | outline | transparent | onSurfaceVariant | Default |
| Hover | onSurface | transparent | onSurfaceVariant | Hover |
| Focused | primary | transparent | primary | Focused |
| Filled | outline | transparent | onSurfaceVariant | Has content |
| Error | error | transparent | error | Error |
| Disabled | onSurface 38% | onSurface 12% | onSurface 38% | Disabled |

**Variants**:
- **Filled**: surfaceContainerHighest background, bottom indicator line
- **Outlined**: Transparent background, outline border (default)
- **Auto-grow**: Auto-increases height with content
- **Fixed**: Fixed height, scroll when overflow

**Accessibility**:
- Floating label associated with input area
- Character counter assists with limit indication
- Support keyboard navigation and text scaling

---

### 8.24 NumberInput

**Material Name**: No native spinner component; the following is a reasonable implementation derived from Material 3 design language (Text Field + stepper buttons)

**Anatomy**:
```
NumberInput
├── Text Field
│   ├── Label (floating)
│   └── Input Text (numeric)
└── Stepper
    ├── Increment Button (+)
    └── Decrement Button (-)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 56dp |
| Horizontal padding | 16dp |
| Corner radius | small (8dp) |
| Stepper button width | 48dp |
| Stepper button touch area | 48x48dp |
| Stepper icon | 24x24dp |

**States**:

| State | Border | Container | Stepper Button | Description |
|---|---|---|---|---|
| Default | outline | transparent | onSurfaceVariant | Default |
| Hover | onSurface | transparent | onSurface | Hover |
| Focused | primary | transparent | primary | Focused |
| Error | error | transparent | error | Out of bounds/Error |
| Disabled | onSurface 38% | onSurface 12% | onSurface 38% | Disabled |

**Stepper Button States**:

| State | State Layer | Description |
|---|---|---|
| Hover | onSurface 8% | Hover |
| Pressed | onSurface 12% | Pressed (with Ripple) |
| At Limit | onSurface 38% | Reached upper/lower limit disabled |

**Accessibility**:
- Stepper button touch target >= 48x48dp
- Support keyboard up/down to increment/decrement
- Out-of-bounds values enter Error state with prompt

---

### 8.25 Upload

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (based on Button + List)

**Anatomy**:
```
Upload
├── Trigger
│   ├── Button (select file) / Drop Zone
│   └── Helper Text
└── File List
    └── File Item
        ├── Leading Icon (file type)
        ├── File Name
        ├── Progress Indicator (uploading)
        └── Trailing Action (remove / status)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Button height | 40dp |
| Drop zone height | >= 120dp |
| Drop zone corner radius | medium (12dp) |
| Drop zone border | 1dp dashed outline |
| File item height | 56dp |
| File item padding | 16dp horizontal |
| File item background | surfaceContainerLow |

**States**:

| State | Drop Zone Border | Background | Description |
|---|---|---|---|
| Default | outline (dashed) | surface | Default |
| Hover / Drag Over | primary (dashed) | primaryContainer | Drag active |
| Uploading | primary | surface | Uploading (progress bar) |
| Success | outline | surfaceContainerLow | Complete |
| Error | error | errorContainer | Failed |
| Disabled | onSurface 38% | onSurface 12% | Disabled |

**File Item States**:

| State | Icon/Text | Description |
|---|---|---|
| Uploading | primary linear progress | In progress |
| Success | primary check | Success |
| Error | error icon | Failed |

**Accessibility**:
- Button touch target >= 48x48dp
- Drop zone also supports click to select
- Upload progress and status text prompts
- Delete operation keyboard accessible

---

### 8.26 Toast

**Material Name**: Snackbar

**Anatomy**:
```
Snackbar
├── Container
├── Supporting Text
└── Action (optional)
    └── Label Button
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 48dp |
| Minimum width | 344dp |
| Maximum width | 600dp |
| Horizontal padding | 16dp |
| Corner radius | extraSmall (4dp) |
| Background | inverseSurface |
| Text | inverseOnSurface, bodyMedium 14pt |
| Action text | inversePrimary, labelLarge 14pt |
| Shadow | 3dp |

**States**:

| State | Background | Description |
|---|---|---|
| Visible | inverseSurface | Showing |
| Action Hover | inverseSurface + 8% state layer | Action hover |
| Dismissing | inverseSurface | Fading out |

**Variants**:
- **Single-line**: Single line text, with/without action
- **Two-line**: Two lines of text
- **With Action**: Includes action button, right-aligned

**Motion**:
- Entry: 250ms decelerate, slides up from bottom
- Exit: 200ms accelerate
- Default duration: 4-10s auto-dismiss

**Accessibility**:
- Action button touch target >= 48x48dp
- Does not interrupt current user operation
- Can be manually operated before auto-dismiss

---

### 8.27 Notification

**Material Name**: No independent component; the following is a reasonable implementation derived from Material 3 design language (in-app notification)

**Anatomy**:
```
Notification
├── Container
├── Leading Icon / Avatar
├── Content
│   ├── Title (headline)
│   ├── Supporting Text
│   └── Timestamp
├── Actions (optional)
└── Close Button (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 344dp |
| Maximum width | 416dp |
| Padding | 16dp |
| Corner radius | medium (12dp) |
| Background | surfaceContainerHigh |
| Title font | titleMedium 16pt |
| Body font | bodyMedium 14pt |
| Timestamp font | bodySmall 12pt, onSurfaceVariant |
| Shadow | 3dp |

**States**:

| State | Background | Description |
|---|---|---|
| Default | surfaceContainerHigh | Default |
| Unread | surfaceContainerHigh + primary marker | Unread |
| Hover | surfaceContainerHigh + onSurface 8% | Hover |
| Read | surfaceContainer | Read |

**Variants**:
- **Info**: Default, primary icon
- **Success**: tertiary icon
- **Warning**: tertiaryContainer background
- **Error**: errorContainer background, error icon

**Accessibility**:
- Close/action button touch target >= 48x48dp
- Unread state visual marker
- Real-time notifications announced via role region

---

### 8.28 Alert / Banner

**Material Name**: Banner (inline embeddable prompt)

**Anatomy**:
```
Banner
├── Container
├── Leading Icon (optional)
├── Supporting Text
└── Actions
    ├── Primary Action
    └── Secondary Action (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum height | 54dp |
| Padding | 16dp horizontal, 16dp vertical |
| Corner radius | 0dp (flush) / medium (12dp) (card style) |
| Background | surfaceContainerLow |
| Text | onSurface, bodyMedium 14pt |
| Icon | 24x24dp |
| Bottom divider | 1dp outlineVariant |

**State/Type**:

| Type | Background | Icon Color | Description |
|---|---|---|---|
| Info | surfaceContainerLow | primary | Information prompt |
| Success | surfaceContainerLow | tertiary | Success |
| Warning | tertiaryContainer | onTertiaryContainer | Warning |
| Error | errorContainer | error | Error |

**Variants**:
- **Single-line**: Single line, action right-aligned
- **Multi-line**: Multiple lines, action below
- **Dismissible**: Includes dismiss action

**Accessibility**:
- Action button touch target >= 48x48dp
- Color contrast ratio >= 4.5:1
- Important prompts announced via role region

---

### 8.29 Skeleton

**Material Name**: No independent component; the following is a reasonable implementation derived from Material 3 design language (Loading placeholder)

**Anatomy**:
```
Skeleton
├── Placeholder Block (text / circle / rect)
└── Shimmer Overlay (animation)
```

**Size Specifications**:

| Variant | Size | Corner Radius |
|---|---|---|
| Text Line | Height 16dp, width adapts | extraSmall (4dp) |
| Title Line | Height 24dp | extraSmall (4dp) |
| Circle (avatar) | 40x40dp | full |
| Rectangle (media) | Adapts | medium (12dp) |
| Button | Height 40dp | full |

**States**:

| State | Background | Shimmer | Description |
|---|---|---|---|
| Loading | surfaceVariant | surfaceContainerHighest sweep | Loading placeholder |
| Loaded | — | — | Content replaces placeholder |

**Motion**:
- Shimmer sweep: 1.5s linear infinite
- Shimmer direction: Left to right
- Shimmer color: surfaceContainerHighest (light-dark gradient)
- Support reduced motion preference (degrade to static pulse)

**Accessibility**:
- Placeholder area marked as busy state
- Focus handed over to real content after loading
- Does not convey semantic content, only visual placeholder

---

### 8.30 Drawer / Sidebar

**Material Name**: Navigation Drawer

**Anatomy**:
```
NavigationDrawer
├── Container
├── Header (optional)
├── Section
│   ├── Section Label
│   └── Drawer Item
│       ├── Leading Icon
│       ├── Label
│       └── Trailing Badge (optional)
└── Divider
```

**Size Specifications**:

| Property | Value |
|---|---|
| Standard width | 360dp |
| Maximum width | 80% of screen |
| Item height | 56dp |
| Item padding | 16dp horizontal, 12dp vertical |
| Item corner radius | full |
| Background | surfaceContainerLow |
| Padding | 12dp |
| Shadow (modal) | 12dp (level5) |

**States**:

| State | Background | Text/Icon | Description |
|---|---|---|---|
| Default | transparent | onSurfaceVariant | Default |
| Hover | onSurface 8% | onSurfaceVariant | Hover |
| Active (selected) | secondaryContainer | onSecondaryContainer | Current item |
| Pressed | onSurface 12% | onSurfaceVariant | Pressed |
| Disabled | transparent | onSurface 38% | Disabled |

**Variants**:
- **Standard**: Persistent sidebar, side-by-side with content
- **Modal**: Overlays content, with overlay (scrim onSurface 32%)
- **Bottom**: Slides up from bottom on mobile

**Accessibility**:
- Item touch target >= 48x48dp
- Modal drawer supports Esc close, focus trap
- Current item visual and semantic marker

---

### 8.31 Pagination

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (paginator)

**Anatomy**:
```
Pagination
├── Previous Button
├── Page Items
│   ├── Page Number
│   └── Ellipsis (...)
├── Next Button
└── Page Size Selector (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Page item size | 40x40dp |
| Page item touch area | 48x48dp |
| Page item corner radius | full |
| Page item spacing | 4dp |
| Font | labelLarge 14pt |
| Arrow icon | 24x24dp |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | onSurface | Default page item |
| Hover | onSurface 8% | onSurface | Hover |
| Current | primary | onPrimary | Current page |
| Pressed | onSurface 12% | onSurface | Pressed |
| Disabled | transparent | onSurface 38% | First/last page arrow |

**Variants**:
- **Numbered**: Shows page numbers (default)
- **Simple**: Previous/Next only
- **With Page Size**: Includes items per page selector

**Accessibility**:
- Touch target >= 48x48dp
- Current page semantic marker
- Arrows keyboard accessible, disabled state not focusable

---

### 8.32 Stepper

**Material Name**: Stepper (process steps)

**Anatomy**:
```
Stepper
├── Step
│   ├── Indicator (circle: number / check / icon)
│   ├── Label
│   │   ├── Title
│   │   └── Supporting Text (optional)
│   └── Connector (line)
└── Step...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Indicator diameter | 24dp |
| Indicator font | labelMedium 12pt |
| Connector line width | 1dp |
| Step spacing | 16dp |
| Title font | titleSmall 14pt |
| Supporting text | bodySmall 12pt |

**States**:

| State | Indicator | Text | Connector | Description |
|---|---|---|---|---|
| Inactive | onSurface 38% | onSurfaceVariant | outlineVariant | Not reached |
| Active | primary | onSurface | outlineVariant | Current step |
| Completed | primary (check) | onSurface | primary | Completed |
| Error | error | error | error | Step error |
| Disabled | onSurface 12% | onSurface 38% | outlineVariant | Disabled |

**Variants**:
- **Horizontal**: Horizontal layout, horizontal connector lines
- **Vertical**: Vertical layout, vertical connector lines, includes expandable content
- **Mobile**: Dot indicator + progress text

**Accessibility**:
- Clickable step touch target >= 48x48dp
- Current/complete/error state semantic markers
- Keyboard navigation between steps

---

### 8.33 Sheet / ActionSheet

**Material Name**: Bottom Sheet

**Anatomy**:
```
BottomSheet
├── Scrim (modal only)
├── Container
├── Drag Handle
├── Header (optional)
└── Content
    └── Action Item / Custom Content
```

**Size Specifications**:

| Property | Value |
|---|---|
| Maximum width | 640dp |
| Top corner radius | extraLarge (28dp) |
| Drag handle | 32x4dp, corner radius full |
| Handle color | onSurfaceVariant |
| Padding | 16dp |
| Background | surfaceContainerLow |
| Action item height | 56dp |
| Shadow | 12dp (level5) |

**States**:

| State | Background | Description |
|---|---|---|
| Collapsed | surfaceContainerLow | Collapsed (peek height) |
| Expanded | surfaceContainerLow | Expanded |
| Item Hover | onSurface 8% | Action item hover |
| Item Pressed | onSurface 12% | Action item pressed |

**Variants**:
- **Standard**: Coexists with content, can interact with main content
- **Modal**: With overlay (scrim onSurface 32%), blocks background
- **Action Sheet**: Action list, each item with icon + label

**Motion**:
- Entry: 300ms decelerate, slides up from bottom
- Exit: 250ms accelerate
- Supports drag handle gesture for height adjustment

**Accessibility**:
- Action item touch target >= 48x48dp
- Modal supports Esc close, focus trap
- Drag handle provides visual grab cue

---

### 8.34 Avatar

**Material Name**: Avatar

**Anatomy**:
```
Avatar
├── Container (circle)
└── Content (image / initials / icon)
```

**Size Specifications**:

| Variant | Size | Font |
|---|---|---|
| Small | 24x24dp | labelSmall 11pt |
| Medium | 40x40dp | titleMedium 16pt |
| Large | 56x56dp | titleLarge 22pt |
| ExtraLarge | 72x72dp | headlineSmall 24pt |

**General Specifications**:

| Property | Value |
|---|---|
| Corner radius | full |
| Text background | primaryContainer |
| Text color | onPrimaryContainer |
| Icon background | surfaceVariant |
| Icon color | onSurfaceVariant |
| Border (optional) | 1dp outlineVariant |

**States**:

| State | Description |
|---|---|
| Image | Displays user image |
| Initials | Displays initials (primaryContainer background) |
| Icon | Displays placeholder icon (surfaceVariant background) |
| With Badge | Badge overlaid at top-right (online status/count) |

**Variants**:
- **Image**: Picture avatar
- **Initials**: Initials avatar
- **Icon**: Icon placeholder avatar
- **Group**: Multiple avatars overlapping (overlap -8dp)

**Accessibility**:
- Image provides alt text
- Initials/icon avatars provide readable name
- When clickable, touch target >= 48x48dp

---

### 8.35 Accordion

**Material Name**: No independent component; the following is a reasonable implementation derived from Material 3 design language (expand/collapse based on List)

**Anatomy**:
```
Accordion
├── Accordion Item
│   ├── Header
│   │   ├── Leading Icon (optional)
│   │   ├── Title
│   │   └── Expand Icon (chevron)
│   └── Panel (expandable content)
└── Divider
```

**Size Specifications**:

| Property | Value |
|---|---|
| Header height | 56dp |
| Header padding | 16dp horizontal |
| Title font | titleMedium 16pt |
| Expand icon | 24x24dp |
| Panel padding | 16dp |
| Divider | 1dp outlineVariant |
| Item corner radius | medium (12dp) (card style) |
| Background | surfaceContainerLow |

**States**:

| State | Header Background | Icon Direction | Description |
|---|---|---|---|
| Collapsed | transparent | chevron down | Collapsed |
| Expanded | transparent | chevron up | Expanded |
| Hover | onSurface 8% | — | Hover |
| Pressed | onSurface 12% | — | Pressed (with Ripple) |
| Disabled | transparent | onSurface 38% | Disabled |

**Variants**:
- **Single**: Only one item expanded at a time
- **Multiple**: Multiple items expanded simultaneously
- **Flush**: No card border, only dividers

**Motion**:
- Expand/Collapse: 250ms standard easing
- Icon rotation: 250ms synchronized

**Accessibility**:
- Header touch target >= 48x48dp
- Expand state semantic marker, panel association
- Keyboard Enter/Space to toggle

---

### 8.36 Carousel

**Material Name**: Carousel

**Anatomy**:
```
Carousel
├── Item Container
│   └── Carousel Item (image / card)
├── Navigation (arrows, optional)
└── Indicators (dots, optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Item corner radius | large (16dp) |
| Item spacing | 8dp |
| Large item width | Adapts (hero) |
| Small item width | 40-56dp (collapsed preview) |
| Indicator dot diameter | 8dp |
| Indicator dot spacing | 8dp |
| Navigation button touch area | 48x48dp |

**States**:

| State | Item | Indicator Dot | Description |
|---|---|---|---|
| Active | Fully expanded | primary | Current item |
| Adjacent | Partially visible | onSurfaceVariant | Adjacent item |
| Collapsed | Minimum width preview | outlineVariant | Collapsed item |
| Hover | + onSurface 8% | — | Hover |

**Variants**:
- **Multi-browse**: Multiple items of different sizes side-by-side (hero + collapsed preview)
- **Uncontained**: Items extend beyond screen edge
- **Hero**: Single large item + one preview item
- **Full-screen**: Vertical full-screen swipe

**Motion**:
- Transition: 350ms emphasized easing
- Item size transition smoothly deforms

**Accessibility**:
- Navigation button touch target >= 48x48dp
- Supports swipe gesture and keyboard left/right
- Current item semantic marker, indicators clickable

---

### 8.37 Timeline

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (timeline)

**Anatomy**:
```
Timeline
├── Timeline Item
│   ├── Indicator (node: dot / icon)
│   ├── Connector (line)
│   └── Content
│       ├── Timestamp
│       ├── Title
│       └── Supporting Text
└── Timeline Item...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Node diameter | 12dp |
| Node icon container | 24dp |
| Connector line width | 2dp |
| Node to content spacing | 16dp |
| Item vertical spacing | 24dp |
| Title font | titleSmall 14pt |
| Timestamp font | bodySmall 12pt, onSurfaceVariant |
| Body font | bodyMedium 14pt |

**States**:

| State | Node | Connector | Description |
|---|---|---|---|
| Default | outline | outlineVariant | Normal node |
| Active | primary | outlineVariant | Current/in-progress |
| Completed | primary (filled) | primary | Completed |
| Error | error | error | Error node |

**Variants**:
- **Left-aligned**: Node left, content right (default)
- **Alternate**: Content alternates left/right
- **With Icon**: Node displays status icon

**Accessibility**:
- Chronological order expressed through structure
- Node status color contrast >= 4.5:1
- Clickable node touch target >= 48x48dp

---

### 8.38 Tree

**Material Name**: No independent native component; the following is a reasonable implementation derived from Material 3 design language (tree list)

**Anatomy**:
```
Tree
├── Tree Node
│   ├── Expand Toggle (chevron, optional)
│   ├── Leading Icon (optional)
│   ├── Label
│   └── Trailing Element (optional)
└── Children (indented nesting)
    └── Tree Node...
```

**Size Specifications**:

| Property | Value |
|---|---|
| Node height | 48dp |
| Node padding | 16dp horizontal |
| Indent per level | 24dp |
| Expand icon | 24x24dp |
| Label font | bodyLarge 16pt |
| Node corner radius | full (selected state) |

**States**:

| State | Background | Icon Direction | Description |
|---|---|---|---|
| Collapsed | transparent | chevron right | Collapsed |
| Expanded | transparent | chevron down | Expanded |
| Hover | onSurface 8% | — | Hover |
| Selected | secondaryContainer | — | Selected |
| Pressed | onSurface 12% | — | Pressed |
| Disabled | transparent | onSurface 38% | Disabled |

**Variants**:
- **Single Select**: Single node selection
- **Multi Select**: With Checkbox multi-selection
- **With Lines**: Shows hierarchy guide lines (outlineVariant)

**Accessibility**:
- Node touch target >= 48x48dp
- Expand/collapse and hierarchy semantic markers
- Keyboard up/down navigation, left/right collapse/expand

---

### 8.39 Divider

**Material Name**: Divider

**Anatomy**:
```
Divider
└── Line (horizontal / vertical)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Line width | 1dp |
| Color | outlineVariant |
| Full width | No indent |
| Inset indent | Left 16dp |
| Middle inset | Left and right 16dp each |
| Vertical divider height | Adapts to content |

**Variants**:

| Variant | Description |
|---|---|
| Full-width | Spans entire container width |
| Inset | Left inset 16dp (aligns with text) |
| Middle Inset | Left and right inset, centered |
| Vertical | Vertical direction separator |
| With Text | Contains centered text (line segments on both sides) |

**With Text Specifications**:
- Text font: bodySmall 12pt
- Text color: onSurfaceVariant
- Text spacing on both sides: 16dp

**Accessibility**:
- Only serves as visual separator, marked as decorative
- Does not receive focus, does not convey semantic content
- Color is non-interactive low contrast, suitable for separation

---

### 8.40 Grid / Layout

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (responsive grid based on section 4 layout grid breakpoints)

**Anatomy**:
```
Grid
├── Container (max-width constraint)
├── Margin (side margins)
└── Columns
    ├── Column (content)
    └── Gutter (column spacing)
```

**Size Specifications (Responsive Breakpoints)**:

| Breakpoint | Width | Columns | Gutter | Margin |
|---|---|---|---|---|
| Compact | < 600dp | 4 | 16dp | 16dp |
| Medium | 600-840dp | 8 | 24dp | 24dp |
| Expanded | 840-1200dp | 12 | 24dp | 24dp |
| Large | 1200-1600dp | 12 | 24dp | 24dp |
| ExtraLarge | > 1600dp | 12 | 24dp | 24dp |

**General Specifications**:

| Property | Value |
|---|---|
| Base unit | 8dp grid |
| Column width | (Container width - margin - spacing) / column count |
| Column span | 1 to column count |

**Variants**:
- **Fixed**: Fixed column count, column width adapts
- **Fluid**: Flowing, scales with container
- **Auto-fit**: Content auto-wraps to fill

**Accessibility**:
- Layout structure only, does not affect DOM reading order
- Responsive breakpoints ensure small screen readability
- Grid adapts and reflows during content scaling

---

### 8.41 Space / Stack

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (spacing layout container)

**Anatomy**:
```
Stack
├── Child
├── Gap (spacing)
├── Child
└── Child...
```

**Size Specifications (Spacing values, following 8dp grid)**:

| Token | Value | Usage |
|---|---|---|
| none | 0dp | No spacing |
| extraSmall | 4dp | Very tight |
| small | 8dp | Default element spacing |
| medium | 16dp | Standard padding |
| large | 24dp | Component spacing |
| extraLarge | 32dp | Section spacing |

**Properties**:

| Property | Options | Description |
|---|---|---|
| Direction | horizontal / vertical | Layout direction |
| Spacing | Tokens from table above | Gap between children |
| Alignment | start / center / end / stretch | Cross-axis alignment |
| Justify | start / center / between / around | Main-axis distribution |
| Wrap | wrap / nowrap | Whether to wrap |

**Variants**:
- **Horizontal**: Horizontal layout
- **Vertical**: Vertical layout
- **Wrap**: Auto-wrap when overflow (spacing applies to both rows and columns)

**Accessibility**:
- Layout container only, does not convey semantics
- Maintain DOM reading order consistent with visual order
- Spacing follows 8dp grid to ensure rhythm

---

### 8.42 AspectRatio

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (aspect ratio container)

**Anatomy**:
```
AspectRatio
├── Container (fixed ratio)
└── Content (image / video / media, fill)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Width | 100% (adapts to parent container) |
| Height | Automatically calculated from ratio |
| Corner radius | medium (12dp) (media card default) |
| Content clipping | cover (fill and clip) |
| Background (loading) | surfaceVariant |

**Common Ratios**:

| Ratio | Usage |
|---|---|
| 1:1 | Avatar, square media |
| 4:3 | Standard image |
| 16:9 | Video, wide media |
| 3:2 | Photo |
| 21:9 | Ultra-wide banner |

**States**:

| State | Background | Description |
|---|---|---|
| Loading | surfaceVariant | Media loading placeholder |
| Loaded | Content | Media displayed |
| Error | surfaceVariant + icon | Loading failed |

**Accessibility**:
- Container only maintains ratio, does not convey semantics
- Contained media provides alt text
- Maintaining ratio prevents content scaling jumps

---

### 8.43 Popover

**Material Name**: No independent component; the following is a reasonable implementation derived from Material 3 design language (floating panel based on Menu/surface)

**Anatomy**:
```
Popover
├── Trigger (anchor)
└── Surface (floating panel)
    ├── Arrow (optional)
    ├── Header (optional)
    ├── Content
    └── Actions (optional)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Minimum width | 112dp |
| Maximum width | 320dp |
| Padding | 16dp |
| Corner radius | medium (12dp) |
| Background | surfaceContainer |
| Shadow | 3dp (level3) |
| Anchor spacing | 8dp |

**States**:

| State | Background | Description |
|---|---|---|
| Hidden | — | Hidden |
| Visible | surfaceContainer | Visible |
| Closing | surfaceContainer | Fading out |

**Variants**:
- **Menu Popover**: Content as action list
- **Rich Popover**: Includes title, body, and actions
- **With Arrow**: Arrow pointing to anchor

**Motion**:
- Entry: 150ms decelerate, scale expand from anchor
- Exit: 100ms accelerate

**Accessibility**:
- Trigger touch target >= 48x48dp
- Supports Esc close, click outside to close
- Focus moves into floating panel, returns to trigger on close

---

### 8.44 Modal

**Material Name**: Full-screen Dialog (full screen, distinct from 8.9 regular Dialog)

**Anatomy**:
```
FullScreenDialog
├── Top App Bar
│   ├── Close Button (X)
│   ├── Title
│   └── Confirm Action (text button)
└── Content (full-screen scroll)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Width | 100% (full screen) |
| Height | 100% (full screen) |
| Top bar height | 64dp |
| Corner radius | 0dp (full screen) |
| Background | surface |
| Content padding | 24dp |
| Title font | titleLarge 22pt |
| Top bar shadow | 3dp when scrolled |

**States**:

| State | Description |
|---|---|
| Open | Full screen cover, enters from bottom |
| Scrolled | Top bar shadow 3dp |
| Closing | Exit animation |

**Variants**:
- **Full-screen**: Full screen on mobile (default)
- **Centered (large screen)**: Degrades to centered large Dialog on large screen, corner radius extraLarge (28dp)

**Motion**:
- Entry: 300ms decelerate, slides up from bottom
- Exit: 250ms accelerate

**Accessibility**:
- Close/confirm button touch target >= 48x48dp
- Focus trap, Esc close
- Focus moves to first interactive element on open

---

### 8.45 FAB

**Material Name**: FAB (Floating Action Button, native component)

**Anatomy**:
```
FAB
├── Container (circle / capsule)
├── Icon
└── Label (Extended variant)
```

**Size Specifications**:

| Variant | Size | Icon | Corner Radius |
|---|---|---|---|
| Small | 40x40dp | 24x24dp | medium (12dp) |
| Standard | 56x56dp | 24x24dp | large (16dp) |
| Large | 96x96dp | 36x36dp | extraLarge (28dp) |
| Extended | Height 56dp, horizontal padding 16dp | 24x24dp | large (16dp) |

**General Specifications**:

| Property | Value |
|---|---|
| Background | primaryContainer |
| Icon/Text | onPrimaryContainer |
| Label font | labelLarge 14pt (Extended) |
| Shadow | 6dp (level3) |

**States**:

| State | Container | Shadow | Description |
|---|---|---|---|
| Default | primaryContainer | 6dp | Default |
| Hover | primaryContainer + 8% onPrimaryContainer | 8dp | Hover |
| Pressed | primaryContainer + 12% onPrimaryContainer | 6dp | Pressed (Ripple) |
| Focused | primaryContainer + 12% state layer | 6dp | Focused |
| Disabled | onSurface 12% | 0dp | onSurface 38% icon |

**Variants**:
- **Small**: Compact scenario
- **Standard**: Default primary action
- **Large**: Emphasized primary action
- **Extended**: Includes text label, more explicit
- **Color variants**: Surface / Secondary / Tertiary container colors

**Accessibility**:
- Touch target >= 48x48dp (Small needs expanded touch area)
- Primary action semantic marker, provides readable label
- Extended text improves identifiability

---

### 8.46 SearchBar

**Material Name**: Search Bar

**Anatomy**:
```
SearchBar
├── Container
├── Leading Icon (menu / back)
├── Input / Placeholder
├── Trailing Icon (avatar / mic / clear)
└── Search View (expanded)
    └── Suggestion List
```

**Size Specifications**:

| Property | Value |
|---|---|
| Height | 56dp |
| Minimum width | 360dp |
| Maximum width | 720dp |
| Horizontal padding | 16dp |
| Corner radius | full |
| Background | surfaceContainerHigh |
| Text font | bodyLarge 16pt |
| Icon | 24x24dp |
| Shadow | Static 0dp, expanded 3dp |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | surfaceContainerHigh | onSurfaceVariant (placeholder) | Default |
| Hover | surfaceContainerHigh + onSurface 8% | onSurfaceVariant | Hover |
| Focused / Active | surfaceContainerHigh | onSurface | Focused (expand suggestion view) |
| Filled | surfaceContainerHigh | onSurface | Has input |
| Disabled | onSurface 12% | onSurface 38% | Disabled |

**Variants**:
- **Search Bar**: Persistent search bar (default)
- **Search View**: Full-screen/expanded suggestion view when focused
- **Docked**: Fixed attached to top

**Accessibility**:
- Touch target >= 48x48dp
- Icon buttons provide readable labels
- Suggestion list keyboard navigable, Esc to dismiss

---

### 8.47 Rating

**Material Name**: No independent native component; the following is a reasonable implementation derived from Material 3 design language (star rating)

**Anatomy**:
```
Rating
├── Star Item (filled / half / empty)
├── Star Item...
└── Label (optional, value/count)
```

**Size Specifications**:

| Variant | Star Icon | Touch Area |
|---|---|---|
| Small | 18x18dp | 24x24dp |
| Medium | 24x24dp | 48x48dp |
| Large | 36x36dp | 48x48dp |

**General Specifications**:

| Property | Value |
|---|---|
| Star spacing | 4dp |
| Selected color | primary |
| Unselected color | outlineVariant |
| Label font | bodyMedium 14pt, onSurfaceVariant |

**States**:

| State | Star Color | Description |
|---|---|---|
| Filled | primary | Rated |
| Half | primary half fill | Half star |
| Empty | outlineVariant | Not rated |
| Hover | primary (preview) | Hover preview |
| Disabled | onSurface 38% | Read-only/Disabled |

**Variants**:
- **Interactive**: Clickable rating
- **Read-only**: Display only (includes half stars)
- **With Count**: Includes rating value or review count

**Accessibility**:
- Interactive touch target >= 48x48dp
- Current rating expressed through semantic value
- Keyboard left/right adjustment of rating

---

### 8.48 ColorPicker

**Material Name**: No native component; the following is a reasonable implementation derived from Material 3 design language (color picker)

**Anatomy**:
```
ColorPicker
├── Trigger (Swatch + Value)
└── Panel (expanded)
    ├── Saturation/Brightness Area
    ├── Hue Slider
    ├── Alpha Slider (optional)
    ├── Preset Swatches
    └── Value Input (HEX/RGB)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Swatch size | 40x40dp |
| Swatch corner radius | small (8dp) |
| Panel width | 280dp |
| Panel corner radius | medium (12dp) |
| Panel background | surfaceContainerHigh |
| Panel shadow | 3dp |
| Slider height | 24dp |
| Preset swatch | 32x32dp, corner radius full |
| Input field | Text Field, height 56dp |

**States**:

| State | Border/State Layer | Description |
|---|---|---|
| Default | outline | Default swatch |
| Hover | onSurface 8% | Hover |
| Selected (preset) | primary 2dp border | Selected color |
| Focused | primary border | Focused |
| Disabled | onSurface 38% | Disabled |

**Variants**:
- **Swatch**: Swatch trigger only
- **Inline Panel**: Directly inline panel
- **With Alpha**: Includes opacity slider

**Accessibility**:
- Swatch/slider touch target >= 48x48dp
- Provides HEX/RGB text input fallback (not reliant on visual selection)
- Current color value expressed in text, keyboard adjustable

---

### 8.49 Calendar

**Material Name**: Date Calendar / Docked DatePicker calendar view (distinct from 8.18 DatePicker)

**Anatomy**:
```
Calendar
├── Header
│   ├── Previous Month
│   ├── Month / Year Label
│   └── Next Month
├── Weekday Labels
└── Day Grid
    └── Day Cell (includes today / selected / range indicators)
```

**Size Specifications**:

| Property | Value |
|---|---|
| Cell size | 48x48dp |
| Cell touch area | 48x48dp |
| Cell corner radius | full |
| Weekday label font | bodySmall 12pt, onSurfaceVariant |
| Date font | bodyLarge 16pt |
| Month title font | titleSmall 14pt |
| Navigation icon | 24x24dp |
| Background | surfaceContainerLow |
| Container corner radius | large (16dp) |

**States**:

| State | Background | Text | Description |
|---|---|---|---|
| Default | transparent | onSurface | Normal date |
| Hover | onSurface 8% | onSurface | Hover |
| Today | transparent + primary border | primary | Today |
| Selected | primary | onPrimary | Selected date |
| In Range | primaryContainer | onPrimaryContainer | Within range |
| Range End | primary | onPrimary | Range endpoint |
| Disabled | transparent | onSurface 38% | Not selectable |

**Variants**:
- **Single**: Single date selection
- **Range**: Date range selection (start/end + interval highlight)
- **Multi-month**: Side-by-side multi-month view

**Accessibility**:
- Cell touch target >= 48x48dp
- Today/selected/range state semantic markers
- Keyboard arrow key navigation, PageUp/Down to switch months

---

## 9. Platform Differences

### 9.1 Android vs Web

| Feature | Android | Web |
|---|---|---|
| Navigation | Bottom Navigation / Navigation Drawer | Custom |
| Back | System back gesture | Browser back |
| Context menu | Long press | Right click |
| Scroll indicator | Edge glow | Scrollbar |
| Font | Roboto | Roboto / System font |
| Dynamic color | Supported (Android 12+) | Optional support |

### 9.2 Touch vs Keyboard/Mouse

| Input Method | Touch | Keyboard/Mouse |
|---|---|---|
| Minimum target | 48x48dp | 32x32dp |
| Hover effect | None | Available |
| Ripple | Available | Optional |
| Context menu | Long press | Right click |

---

## 10. Token Reference Table

### 10.1 Color Tokens

| Token | Light | Dark |
|---|---|---|
| primary | `#6750A4` | `#D0BCFF` |
| onPrimary | `#FFFFFF` | `#381E72` |
| primaryContainer | `#EADDFF` | `#4F378B` |
| secondary | `#625B71` | `#CCC2DC` |
| secondaryContainer | `#E8DEF8` | `#4A4458` |
| tertiary | `#7D5260` | `#EFB8C8` |
| surface | `#FFFBFE` | `#1C1B1F` |
| onSurface | `#1C1B1F` | `#E6E1E5` |
| surfaceVariant | `#E7E0EC` | `#49454F` |
| onSurfaceVariant | `#49454F` | `#CAC4D0` |
| background | `#FFFBFE` | `#1C1B1F` |
| error | `#B3261E` | `#F2B8B5` |
| onError | `#FFFFFF` | `#601410` |
| outline | `#79747E` | `#938F99` |
| outlineVariant | `#CAC4D0` | `#49454F` |
| surfaceContainerLow | `#F7F2FA` | `#1D1B20` |
| surfaceContainer | `#F3EDF7` | `#211F26` |
| surfaceContainerHigh | `#ECE6F0` | `#2B2930` |

### 10.2 Font Tokens

| Token | Size | Weight | Line Height |
|---|---|---|---|
| displayLarge | 57pt | Regular | 64pt |
| displayMedium | 45pt | Regular | 52pt |
| displaySmall | 36pt | Regular | 44pt |
| headlineLarge | 32pt | Regular | 40pt |
| headlineMedium | 28pt | Regular | 36pt |
| headlineSmall | 24pt | Regular | 32pt |
| titleLarge | 22pt | Regular | 28pt |
| titleMedium | 16pt | Medium | 24pt |
| titleSmall | 14pt | Medium | 20pt |
| bodyLarge | 16pt | Regular | 24pt |
| bodyMedium | 14pt | Regular | 20pt |
| bodySmall | 12pt | Regular | 16pt |
| labelLarge | 14pt | Medium | 20pt |
| labelMedium | 12pt | Medium | 16pt |
| labelSmall | 11pt | Medium | 16pt |

### 10.3 Spacing Tokens

| Token | Value |
|---|---|
| none | 0dp |
| extraSmall | 4dp |
| small | 8dp |
| medium | 16dp |
| large | 24dp |
| extraLarge | 32dp |
| extraExtraLarge | 48dp |
| extraExtraExtraLarge | 64dp |

### 10.4 Corner Radius Tokens

| Token | Value |
|---|---|
| none | 0dp |
| extraSmall | 4dp |
| small | 8dp |
| medium | 12dp |
| large | 16dp |
| extraLarge | 28dp |
| full | 9999dp |

### 10.5 Elevation Tokens

| Token | Value |
|---|---|
| level0 | 0dp |
| level1 | 1dp |
| level2 | 3dp |
| level3 | 6dp |
| level4 | 8dp |
| level5 | 12dp |
