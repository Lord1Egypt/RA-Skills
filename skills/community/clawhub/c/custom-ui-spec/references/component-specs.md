# Component Unified Specification and Comparison

## Table of Contents

1. [Component Mapping Overview](#1-component-mapping-overview)
2. [Detailed Component Definitions](#2-detailed-component-definitions)
3. [Cross-Specification Conflict Summary](#3-cross-specification-conflict-summary)

---

## 1. Component Mapping Overview

| Unified Name | HIG | Fluent | Material |
|---|---|---|---|
| Button | Button | Button | Button |
| TextField | Text Field | Input | Text Field |
| Checkbox | Checkbox | Checkbox | Checkbox |
| RadioButton | Radio Button | Radio | Radio Button |
| Switch | Toggle | Switch | Switch |
| Slider | Slider | Slider | Slider |
| ProgressIndicator | Progress View | Progress Bar | Progress Indicator |
| Menu | Menu | Menu | Menu |
| Dialog | Alert / Sheet | Dialog | Dialog |
| Card | — | Card | Card |
| List | List | List | List |
| NavigationBar | Navigation Bar | Navigation | Top / Bottom App Bar |
| TabBar | Tab Bar | Tab | Tabs |
| SegmentedControl | Segmented Control | — | — |
| Tooltip | Tooltip | Tooltip | Tooltip |
| Badge | Badge | Badge | Badge |
| Chip | — | Tag | Chip |
| DatePicker | Date Picker | Date Picker | Date Picker |
| Table | Table | Data Grid | Data Table |
| Breadcrumb | — | Breadcrumb | — |
| Select | Pop-up Button / Menu | Dropdown / Combobox | Exposed Dropdown Menu |
| Autocomplete | — (derived) | Combobox (editable) | — (derived) |
| Textarea | Multiline Text Field | Textarea | Text Field (multiline) |
| NumberInput | Stepper + Text Field | SpinButton | — (derived) |
| Upload | — (derived) | — (derived) | — (derived) |
| Toast | — (derived) | Toast | Snackbar |
| Notification | — (derived) | — (derived, based on MessageBar) | — (derived) |
| Alert / Banner | — (derived, inline banner) | MessageBar | Banner |
| Skeleton | — (derived) | Skeleton | — (derived) |
| Drawer / Sidebar | Sidebar | NavigationView / Drawer | Navigation Drawer |
| Pagination | — (derived) | — (derived) | — (derived) |
| Stepper | — (derived) | — (derived) | Stepper |
| Sheet / ActionSheet | Action Sheet / Sheet | — (derived, bottom Drawer) | Bottom Sheet |
| Avatar | — (derived) | Avatar / Persona | Avatar |
| Accordion | Disclosure Group | Accordion | — (derived) |
| Carousel | Page Control + horizontal scroll | Carousel | Carousel |
| Timeline | — (derived) | — (derived) | — (derived) |
| Tree | Outline View | TreeView | — (derived) |
| Divider | Separator | Divider | Divider |
| Grid / Layout | — (derived) | — (derived) | — (derived) |
| Space / Stack | — (derived) | Stack | — (derived) |
| AspectRatio | — (derived) | — (derived) | — (derived) |
| Popover | Popover | Popover | — (derived) |
| Modal | Modal Sheet / Full Screen Cover | Modal Dialog | Full-screen Dialog |
| FAB | — (derived) | — (derived) | FAB |
| SearchBar | Search Field | SearchBox | Search Bar |
| Rating | — (derived) | Rating | — (derived) |
| ColorPicker | Color Well | ColorPicker | — (derived) |
| Calendar | Calendar View | Calendar | Date Calendar |

---

## 2. Detailed Component Definitions

### 2.1 Button

**Purpose**: The primary interactive element for triggering actions or operations.

**Anatomy**:
```
Button
├── Container / Background
├── Label (Text)
└── Icon (optional, leading or trailing)
```

**Size Specification Comparison**:

| Spec | Small | Medium | Large |
|---|---|---|---|
| HIG | 28pt x 12pt padding | 34pt x 16pt padding | 44pt x 20pt padding |
| Fluent | 24px x 8px padding | 32px x 12px padding | 40px x 16px padding |
| Material | 32dp x 16dp padding | 40dp x 24dp padding | 48dp x 32dp padding |

**Corner Radius Comparison**:

| Spec | Corner Radius | Description |
|---|---|---|
| HIG | 8-10pt | Medium corner radius |
| Fluent | 4px | Small corner radius |
| Material | full (capsule shape) | Full corner radius |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | systemBlue bg, white text | neutral bg, neutral text | primaryContainer bg |
| Hover | darken 10% | neutralBackground2 | +8% overlay |
| Pressed | darken 20% | neutralBackground3 | +12% overlay |
| Disabled | systemGray5, systemGray | neutralDisabled | 12% opacity |
| Focused | systemBlue + outline | brandStroke + outline | primary + outline |

**Cross-Spec Conflict Points**:
- **Corner radius**: HIG medium vs Fluent small vs Material full
- **Height**: Material buttons tallest (40-48dp), HIG middle, Fluent shortest
- **Variant naming**: The three specs have completely different variant names

---

### 2.2 TextField

**Purpose**: Receives user text input.

**Anatomy**:
```
TextField
├── Container / Background
├── Border
├── Label (floating or static)
├── Placeholder Text
├── Input Text
├── Leading Icon (optional)
├── Trailing Icon / Action (optional)
└── Supporting Text / Error Text (optional)
```

**Size Specification Comparison**:

| Spec | Minimum Height | Horizontal Padding | Corner Radius |
|---|---|---|---|
| HIG | 44pt | 12pt | 10pt |
| Fluent | 32px | 12px | 4px |
| Material | 56dp | 16dp | 8dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | separator border | neutralStroke1 | outline border |
| Hover | systemGray2 | neutralStrokeAccessible | onSurface |
| Focused | systemBlue | brandStroke | primary |
| Error | systemRed | error | error |
| Disabled | systemGray4 | neutralDisabled | 38% opacity |

**Cross-Spec Conflict Points**:
- **Height**: Material tallest (56dp), HIG middle (44pt), Fluent shortest (32px)
- **Label position**: Material uses floating label, HIG/Fluent use static labels
- **Corner radius**: HIG largest (10pt), Material middle (8dp), Fluent smallest (4px)

---

### 2.3 Checkbox

**Purpose**: Select one or multiple options from a group.

**Anatomy**:
```
Checkbox
├── Box (square)
│   └── Checkmark / Indeterminate line
└── Label (Text)
```

**Size Specification Comparison**:

| Spec | Box Size | Corner Radius | Label Spacing |
|---|---|---|---|
| HIG | 18x18pt | 4pt | 8pt |
| Fluent | 16x16px | 2px | 8px |
| Material | 18x18dp | 2dp | 16dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Unchecked | transparent + gray border | transparent + neutral border | transparent + outline |
| Checked | systemBlue bg + white check | brand bg + white check | primary bg + onPrimary check |
| Mixed | — | brand bg + white line | primary bg + onPrimary line |
| Disabled | gray bg + gray check | neutralDisabled | 38% opacity |

**Cross-Spec Conflict Points**:
- **Label spacing**: Material largest (16dp), HIG/Fluent smaller (8pt/8px)
- **Mixed state**: HIG has no mixed state, Fluent/Material support it

---

### 2.4 RadioButton

**Purpose**: Select one option from a group of mutually exclusive options.

**Anatomy**:
```
RadioButton
├── Circle (outer)
│   └── Inner Dot (optional)
└── Label (Text)
```

**Size Specification Comparison**:

| Spec | Outer Circle Diameter | Inner Dot Diameter | Border Width |
|---|---|---|---|
| HIG | 20pt | 8pt | 2pt |
| Fluent | 16px | 8px | 1px |
| Material | 20dp | 10dp | 2dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Unselected | systemBlue border | neutral border | outline border |
| Selected | systemBlue border + dot | brand border + dot | primary border + dot |
| Disabled | systemGray4 | neutralDisabled | 38% opacity |

---

### 2.5 Switch

**Purpose**: Toggle a single setting on/off.

**Anatomy**:
```
Switch
├── Track (pill shape)
└── Thumb / Handle (circle)
```

**Size Specification Comparison**:

| Spec | Track Width | Track Height | Thumb Diameter |
|---|---|---|---|
| HIG | 51pt | 31pt | 27pt |
| Fluent | 40px | 20px | 14px |
| Material | 52dp | 32dp | 24dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Off | systemGray4 track, white thumb | neutral track, white thumb | outline track, surface thumb |
| On | systemGreen track, white thumb | brand track, white thumb | primary track, onPrimary thumb |
| Disabled | systemGray6 | neutralDisabled | 12% opacity |

**Cross-Spec Conflict Points**:
- **Size**: HIG largest (51x31pt), Material middle, Fluent smallest (40x20px)
- **On color**: HIG uses green, Fluent/Material use brand/primary color

---

### 2.6 Slider

**Purpose**: Select a value from a continuous or discrete range.

**Anatomy**:
```
Slider
├── Track (background)
├── Fill / Active Track (value)
└── Thumb (handle)
```

**Size Specification Comparison**:

| Spec | Track Height | Thumb Diameter | Touch Area |
|---|---|---|---|
| HIG | 4pt | 28pt | 44x44pt |
| Fluent | 4px | 16px | 32x32px |
| Material | 4dp | 20dp | 48x48dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | systemBlue fill | brand fill | primary fill |
| Hover | systemBlue | brand | primary |
| Pressed | systemBlue darken | brandPressed | primary |
| Disabled | systemGray4 | neutralDisabled | 38% opacity |

---

### 2.7 ProgressIndicator

**Purpose**: Display operation progress or loading state.

**Anatomy**:
```
ProgressIndicator
├── Track (background)
└── Indicator (fill / spinner)
```

**Size Specification Comparison**:

| Spec | Linear Height | Circular Diameter | Line Width |
|---|---|---|---|
| HIG | 4pt | 20/36pt | 3-4pt |
| Fluent | 2px | 16/24/32px | 2px |
| Material | 4dp | 24/40/48dp | 4dp |

**Colors**:

| Spec | Track | Fill |
|---|---|---|
| HIG | systemGray5 | systemBlue |
| Fluent | neutralBackground3 | brandBackground |
| Material | surfaceVariant | primary |

---

### 2.8 Menu

**Purpose**: Display a list of actions or options.

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

**Size Specification Comparison**:

| Spec | Minimum Width | Item Height | Corner Radius | Shadow |
|---|---|---|---|---|
| HIG | 200pt | 44pt | 13pt | None |
| Fluent | 160px | 32px | 4px | shadow8 |
| Material | 180dp | 48dp | 12dp | 3dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | transparent | transparent | transparent |
| Hover | systemBlue + white text | neutralBackground2 | onSurface 8% |
| Pressed | systemBlue darken | neutralBackground3 | onSurface 12% |
| Disabled | transparent + gray | transparent + disabled | 38% opacity |

**Cross-Spec Conflict Points**:
- **Hover style**: HIG uses brand background + white text, Fluent/Material use light background
- **Shadow**: HIG does not use shadows, Fluent/Material use shadows

---

### 2.9 Dialog

**Purpose**: Display important information that requires user attention or action.

**Anatomy**:
```
Dialog
├── Container
├── Icon (optional)
├── Title / Headline
├── Message / Supporting Text
├── TextField (optional)
└── Actions
    ├── Primary Action
    └── Secondary Action
```

**Size Specification Comparison**:

| Spec | Minimum Width | Corner Radius | Padding |
|---|---|---|---|
| HIG | 270pt | 13pt | 20pt |
| Fluent | 288px | 8px | 24px |
| Material | 280dp | 28dp | 24dp |

**Button Layout**:

| Spec | 2 Buttons | 3+ Buttons |
|---|---|---|
| HIG | Horizontal, primary on right | Vertical |
| Fluent | Horizontal, primary on left | Vertical |
| Material | Horizontal, primary on right | Vertical |

**Cross-Spec Conflict Points**:
- **Corner radius**: Material largest (28dp), HIG middle (13pt), Fluent smallest (8px)
- **Button position**: HIG/Material primary on right, Fluent primary on left

---

### 2.10 Card

**Purpose**: Group related content for display.

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

**Size Specification Comparison**:

| Spec | Corner Radius | Padding | Background | Shadow |
|---|---|---|---|---|
| HIG | 10-13pt | 16pt | secondarySystemBackground | None |
| Fluent | 4px | 16px | neutralBackground1 | None (static) |
| Material | 12dp | 16dp | surfaceContainerLow | 1dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | No shadow | No shadow | 1dp shadow |
| Hover | No change | shadow4 | 3dp shadow |
| Selected | — | brandStroke border | — |
| Pressed | — | — | 1dp shadow |

**Cross-Spec Conflict Points**:
- **Shadow**: Material always uses shadow, Fluent on hover, HIG does not use
- **Corner radius**: Material largest (12dp), HIG middle, Fluent smallest (4px)

---

### 2.11 List

**Purpose**: Display a scrollable group of related items.

**Anatomy**:
```
List
├── List Item
│   ├── Leading Element (icon / avatar / checkbox)
│   ├── Content
│   │   ├── Title / Headline
│   │   └── Subtitle / Supporting Text (optional)
│   ├── Trailing Element (icon / text / switch)
│   └── Divider
└── List Item...
```

**Size Specification Comparison**:

| Spec | Item Height | Padding | Separator |
|---|---|---|---|
| HIG | 44pt (single line) | 16pt horizontal | Inset 60pt |
| Fluent | 40px | 12px horizontal | Full width |
| Material | 48dp (single line) | 16dp horizontal | Inset 16/56dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | transparent | transparent | transparent |
| Hover | systemGray6 | neutralBackground2 | onSurface 8% |
| Selected | systemBlue | brand 10% | onSurface 12% |
| Pressed | systemGray5 | neutralBackground3 | onSurface 12% |

---

### 2.12 NavigationBar

**Purpose**: Provide primary application navigation.

**Anatomy**:
```
NavigationBar
├── Leading Item (menu / back / logo)
├── Title / Headline
└── Trailing Items (actions)
```

**Size Specification Comparison**:

| Spec | Height | Background | Title Font |
|---|---|---|---|
| HIG | 44pt (iOS) / 52pt (macOS) | systemBackground + blur | Headline 17pt |
| Fluent | 48px | neutralBackground1 / Acrylic | Body 14pt |
| Material | 64dp (small) / 80dp (medium) / 152dp (large) | surface | titleLarge 22pt |

**Cross-Spec Conflict Points**:
- **Position**: HIG top, Material top/bottom, Fluent top/side
- **Height**: Material most variable (64-152dp), HIG middle, Fluent fixed
- **Material**: Fluent uses Acrylic, HIG uses blur, Material does not use

---

### 2.13 TabBar

**Purpose**: Switch between content at the same hierarchy level.

**Anatomy**:
```
TabBar
├── Tab List
│   └── Tab Item
│       ├── Icon (optional)
│       └── Label
└── Tab Panel
```

**Size Specification Comparison**:

| Spec | Item Height | Icon Size | Selected Indicator |
|---|---|---|---|
| HIG | 49pt (iOS) | 24x24pt | Color change |
| Fluent | 36px | — | Bottom 2px brand bar |
| Material | 48dp | 24x24dp | Bottom 3dp primary bar |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Selected | systemBlue | brandForeground | primary |
| Unselected | systemGray | neutralForeground2 | onSurfaceVariant |

**Cross-Spec Conflict Points**:
- **Indicator**: Fluent/Material use bottom bar, HIG uses color change
- **Position**: HIG bottom (iOS), Fluent/Material top

---

### 2.14 SegmentedControl

**Purpose**: Switch between a set of mutually exclusive options.

**Anatomy**:
```
SegmentedControl
├── Background
├── Segment
│   └── Label
├── Segment...
└── Selected Indicator
```

**Size Specification Comparison**:

| Spec | Height | Corner Radius | Background |
|---|---|---|---|
| HIG | 32pt | 8pt | systemGray5 |
| Fluent | — | — | — |
| Material | — | — | — |

**State Definitions**:

| State | HIG |
|---|---|
| Selected | white indicator + label |
| Unselected | transparent + label |
| Disabled | white indicator + gray text |

**Cross-Spec Conflict Points**:
- **Existence**: Only HIG has native SegmentedControl; Fluent/Material use Tab/Toggle Button as substitute
- **Indicator**: HIG uses white background block

---

### 2.15 Tooltip

**Purpose**: Display additional information about an element.

**Anatomy**:
```
Tooltip
├── Container
├── Label
└── Arrow (optional)
```

**Size Specification Comparison**:

| Spec | Maximum Width | Padding | Corner Radius | Font |
|---|---|---|---|---|
| HIG | 240pt | 8pt 12pt | 8pt | Caption 1 12pt |
| Fluent | 240px | 8px 12px | 4px | Caption 12pt |
| Material | 200dp | 8dp 12dp | 8dp | bodySmall 12pt |

**Background**:

| Spec | Background | Text |
|---|---|---|
| HIG | label (dark) | white |
| Fluent | neutralBackgroundInverted | neutralForegroundInverted |
| Material | inverseSurface | inverseOnSurface |

---

### 2.16 Badge

**Purpose**: Display a count or status indicator.

**Anatomy**:
```
Badge
├── Background
└── Label (number / dot)
```

**Size Specification Comparison**:

| Spec | Dot Size | Number Height | Corner Radius |
|---|---|---|---|
| HIG | 8x8pt | 18pt | 9pt (full) |
| Fluent | 8x8px | 16px | 8px (full) |
| Material | 6x6dp | 16dp | full |

**Colors**:

| Spec | Background | Text |
|---|---|---|
| HIG | systemRed | white |
| Fluent | brandBackground | white |
| Material | error | onError |

---

### 2.17 Chip

**Purpose**: Display compact information or action.

**Anatomy**:
```
Chip
├── Container
├── Leading Icon (optional)
├── Label
└── Trailing Icon / Close (optional)
```

**Size Specification Comparison**:

| Spec | Height | Padding | Corner Radius | Background |
|---|---|---|---|---|
| HIG | 28pt | 12pt | full | systemGray5 |
| Fluent | 24px | 8px | 4px | neutralBackground2 |
| Material | 32dp | 12dp | full | surfaceContainerLow |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | systemGray5 | neutralBackground2 | surfaceContainerLow |
| Selected | systemBlue | brand 10% | secondaryContainer |
| Hover | systemGray4 | neutralBackground3 | onSurface 8% |

**Cross-Spec Conflict Points**:
- **Name**: HIG has no native Chip, Fluent calls it Tag, Material calls it Chip
- **Corner radius**: HIG/Material use full, Fluent uses 4px

---

### 2.18 DatePicker

**Purpose**: Select a date.

**Anatomy**:
```
DatePicker
├── Header (month / year)
├── Weekday Labels
└── Day Grid
    └── Day Cell
```

**Size Specification Comparison**:

| Spec | Cell Size | Cell Spacing | Selected Background | Corner Radius |
|---|---|---|---|---|
| HIG | 32x32pt | 4pt | systemBlue circle | — |
| Fluent | 32x32px | 2px | brandBackground circle | 4px |
| Material | 40x40dp | 0dp | primary circle | 28dp |

---

### 2.19 Table

**Purpose**: Display data in rows and columns.

**Anatomy**:
```
Table
├── Table Header
│   └── Column Header
├── Table Row
│   └── Cell
└── Table Footer (optional)
```

**Size Specification Comparison**:

| Spec | Row Height | Header Height | Padding |
|---|---|---|---|
| HIG | 44pt | 36pt | 16pt horizontal |
| Fluent | 40px | 32px | 12px horizontal |
| Material | 52dp | 56dp | 16dp horizontal |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | transparent | transparent | transparent |
| Hover | systemGray6 | neutralBackground2 | onSurface 8% |
| Selected | systemBlue | brand 10% | onSurface 12% |
| Alternate | — | — | — |

---

### 2.20 Breadcrumb

**Purpose**: Display the current page location within the hierarchy.

**Anatomy**:
```
Breadcrumb
├── Item
│   ├── Icon (optional)
│   └── Label
├── Separator
└── Item...
```

**Size Specification Comparison**:

| Spec | Font | Separator | Clickable Item Color |
|---|---|---|---|
| HIG | Body 17pt | "/" or ">" | systemBlue |
| Fluent | Body 14pt | "/" | brandForeground |
| Material | bodyMedium 14pt | "/" | primary |

**Cross-Spec Conflict Points**:
- **Existence**: HIG has no native Breadcrumb (macOS uses Path Control), Material has no native

---

### 2.21 Select

**Purpose**: Select a single option from a dropdown list.

**Anatomy**:
```
Select
├── Trigger / Anchor
│   ├── Label / Selected Value
│   └── Chevron (down)
└── Menu / Listbox (popup)
    └── Option
        ├── Checkmark (selected)
        └── Label
```

**Size Specification Comparison**:

| Spec | Trigger Height | Horizontal Padding | Trigger Corner Radius | Menu Corner Radius | Menu Item Height |
|---|---|---|---|---|---|
| HIG | 34pt | 12pt | 8pt | 13pt | 44pt |
| Fluent | 32px | 12px | 4px | 4px | 32px |
| Material | 56dp | 16dp | 8dp | 12dp | 48dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | tertiarySystemFill | neutralStroke1 | outline border |
| Hover | secondarySystemFill | neutralStrokeAccessible | onSurface border |
| Focused / Open | systemBlue outline | brandStroke | primary |
| Disabled | systemGray6 | neutralStrokeDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Trigger height**: Material tallest (56dp), HIG middle (34pt), Fluent shortest (32px)
- **Corner radius**: HIG trigger 8pt / menu 13pt, Fluent 4px, Material 8dp/12dp
- **Naming**: HIG=Pop-up Button, Fluent=Dropdown, Material=Exposed Dropdown Menu

---

### 2.22 Autocomplete

**Purpose**: Filter and complete suggestions while typing.

**Anatomy**:
```
Autocomplete
├── Input Field
│   ├── Leading/Search Icon (optional)
│   ├── Input Text
│   └── Clear / Chevron (optional)
└── Suggestion List (popup)
    └── Suggestion Item (matched highlight)
```

**Size Specification Comparison**:

| Spec | Input Height | Input Corner Radius | Suggestion List Corner Radius | Suggestion Item Height |
|---|---|---|---|---|
| HIG | 44pt | 10pt | 13pt | 44pt |
| Fluent | 32px | 4px | 4px | 32px |
| Material | 56dp | 8dp | 12dp | 48dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | separator | neutralStroke1 | outline |
| Focused | systemBlue | brandStroke | primary |
| Suggesting | systemBlue | brandStroke (filtering) | primary |
| Match highlight | systemBlue text | brandForeground Semibold | visual highlight |
| Disabled | systemGray4 | neutralStrokeDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG has no native component, derived implementation (Search Field + suggestion list); Material has no native component, derived implementation (Menu + Text Field); only Fluent has native Combobox editable mode
- **Height**: Material tallest (56dp), HIG middle (44pt), Fluent shortest (32px)

---

### 2.23 Textarea

**Purpose**: Receive multi-line text input.

**Anatomy**:
```
Textarea
├── Container / Background
├── Border
├── Label (Material floating)
├── Placeholder / Input Text (multiline)
└── Resize Handle / Counter (optional)
```

**Size Specification Comparison**:

| Spec | Minimum Height | Horizontal Padding | Vertical Padding | Corner Radius | Line Height |
|---|---|---|---|---|---|
| HIG | 88pt | 12pt | 12pt | 10pt | 22pt |
| Fluent | 60px | 12px | 8px | 4px | 20px |
| Material | 56dp | 16dp | 16dp | 8dp | 24pt |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | separator | neutralStroke1 | outline |
| Hover | systemGray2 | neutralStrokeAccessible | onSurface |
| Focused | systemBlue | brandStroke | primary |
| Error | systemRed | error | error |
| Disabled | systemGray4 | neutralStrokeDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Minimum height**: HIG tallest (88pt ~2 lines), Fluent 60px, Material 56dp (single line start)
- **Corner radius**: HIG largest (10pt), Material middle (8dp), Fluent smallest (4px)
- **Label position**: Material uses floating label, HIG/Fluent have no floating label

---

### 2.24 NumberInput

**Purpose**: Input numeric values and adjust via stepper buttons.

**Anatomy**:
```
NumberInput
├── Text Field
│   └── Numeric Value
└── Stepper
    ├── Increment Button (+/▲)
    └── Decrement Button (-/▼)
```

**Size Specification Comparison**:

| Spec | Overall Height | Corner Radius | Stepper Button Width | Stepper Icon/Touch |
|---|---|---|---|---|
| HIG | 44pt | 10pt | 47pt (per button) | 44x44pt |
| Fluent | 32px | 4px | 24px | 16px height (each half) |
| Material | 56dp | 8dp | 48dp | 24x24dp / 48x48dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | separator + tertiarySystemFill | neutralStroke1 | outline |
| Focused | systemBlue | brandStroke | primary |
| Pressed (button) | systemFill | neutralBackground3 | onSurface 12% (Ripple) |
| At Limit | systemGray disabled | neutralForegroundDisabled | onSurface 38% |
| Disabled | systemGray6 | neutralStrokeDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: Only Fluent has native SpinButton; Material has no native spinner, derived implementation (Text Field + stepper buttons); HIG is Stepper + Text Field combination
- **Overall height**: Material tallest (56dp), HIG middle (44pt), Fluent shortest (32px)
- **Stepper button width**: Material widest (48dp), HIG 47pt, Fluent narrowest (24px)

---

### 2.25 Upload

**Purpose**: Select or drag-and-drop upload files and display progress.

**Anatomy**:
```
Upload
├── Drop Zone / Trigger
│   ├── Icon
│   ├── Prompt Text
│   └── Browse Button
└── File List
    └── File Item
        ├── File Icon / Name / Size
        ├── Progress (uploading)
        └── Remove / Status Button
```

**Size Specification Comparison**:

| Spec | Drop Zone Minimum Height | Drop Zone Corner Radius | Drop Zone Border | File Item Height |
|---|---|---|---|---|
| HIG | 160pt | 13pt | 2pt dashed separator | 60pt |
| Fluent | 120px | 8px | 1px dashed neutralStroke1 | 48px |
| Material | 120dp | 12dp | 1dp dashed outline | 56dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | separator (dashed) | neutralStroke1 (dashed) | outline (dashed) |
| Dragover | systemBlue + 10% bg | brandStroke | primary + primaryContainer |
| Success | systemGreen check | success | primary check |
| Error | systemRed warning | error | error + errorContainer |
| Disabled | systemGray4 | neutralStrokeDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: All three specs have no native component; HIG/Fluent/Material are all derived implementations (based on Button + List)
- **Drop zone minimum height**: HIG tallest (160pt), Fluent/Material both 120
- **Corner radius**: HIG largest (13pt), Material middle (12dp), Fluent smallest (8px)

---

### 2.26 Toast

**Purpose**: Briefly display a lightweight operation feedback.

**Anatomy**:
```
Toast
├── Container / Background
├── Icon (optional)
├── Message / Title + Body
└── Action Button (optional)
```

**Size Specification Comparison**:

| Spec | Minimum Height | Maximum Width | Padding | Corner Radius | Auto-Dismiss |
|---|---|---|---|---|---|
| HIG | 50pt | Container width - 32pt | 16pt/12pt | 13pt | 3s |
| Fluent | — | 360px | 12px 16px | 6px | 4-6s |
| Material | 48dp | 600dp | 16dp | 4dp | 4-10s |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Background | secondarySystemBackground + blur | neutralBackground1 + Acrylic | inverseSurface |
| Info | systemBlue | info | — |
| Success | systemGreen | success | — |
| Warning | systemYellow | warning | — |
| Error | systemRed | error | — |
| Action color | systemBlue | — | inversePrimary |

**Cross-Spec Conflict Points**:
- **Native support**: HIG has no native lightweight notification component, derived implementation (bottom translucent overlay); Fluent=Toast, Material=Snackbar
- **Corner radius**: HIG largest (13pt), Fluent 6px, Material smallest (4dp)
- **Background**: HIG/Fluent use translucent/Acrylic light background, Material uses inverse inverseSurface
- **Semantic color variants**: HIG/Fluent provide Info/Success/Warning/Error, Material Snackbar does not differentiate semantic colors

---

### 2.27 Notification

**Purpose**: Display in-app notification messages requiring user attention.

**Anatomy**:
```
Notification
├── Container / Background
├── App Icon / Leading Icon
├── Content
│   ├── Title
│   ├── Body
│   └── Timestamp (optional)
└── Action / Dismiss Button
```

**Size Specification Comparison**:

| Spec | Minimum Height/Width | Padding | Corner Radius | Title Font |
|---|---|---|---|---|
| HIG | Height 64pt | 16pt | 20pt | Headline 17pt Semibold |
| Fluent | Width 320-400px | 12px 16px | 6px | Body 14pt Semibold |
| Material | Width 344-416dp | 16dp | 12dp | titleMedium 16pt |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | secondarySystemBackground + blur | neutralBackground1 | surfaceContainerHigh |
| Hover | tertiarySystemBackground | — | onSurface 8% |
| Unread/Read | — | — | primary marker / surfaceContainer |
| Shadow | None (blur) | shadow8 | 3dp |

**Cross-Spec Conflict Points**:
- **Native support**: All three specs have no independent native component; HIG/Material are derived implementations, Fluent based on MessageBar derived
- **Corner radius**: HIG largest (20pt), Material middle (12dp), Fluent smallest (6px)
- **Material**: HIG translucent blur, Fluent Acrylic/shadow, Material layered surface + shadow

---

### 2.28 Alert / Banner

**Purpose**: Inline embeddable status prompt bar within a page.

**Anatomy**:
```
Banner
├── Background (tinted)
├── Leading Icon (status)
├── Content (Title / Message)
├── Action (optional)
└── Dismiss Button (optional)
```

**Size Specification Comparison**:

| Spec | Minimum Height | Padding | Corner Radius | Icon Size |
|---|---|---|---|---|
| HIG | 44pt | 12pt 16pt | 10pt | 20x20pt |
| Fluent | 32px | 12px 8px | 4px | 16x16px |
| Material | 54dp | 16dp | 0dp / 12dp | 24x24dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Info | systemBlue 10% | Info Background | surfaceContainerLow + primary |
| Success | systemGreen 10% | Success Background | surfaceContainerLow + tertiary |
| Warning | systemYellow 10% | Warning Background | tertiaryContainer |
| Error | systemRed 10% | Error Background | errorContainer |

**Cross-Spec Conflict Points**:
- **Native support**: HIG has no native inline embeddable prompt bar, derived implementation (distinct from dialog-style Alert); Fluent=MessageBar, Material=Banner
- **Corner radius**: HIG largest (10pt), Fluent 4px, Material flush 0dp or card 12dp
- **Minimum height**: Material tallest (54dp), HIG middle (44pt), Fluent shortest (32px)

---

### 2.29 Skeleton

**Purpose**: Placeholder skeleton during content loading.

**Anatomy**:
```
Skeleton
├── Shape Placeholder (line / circle / rect)
└── Shimmer Overlay (animated)
```

**Size Specification Comparison**:

| Spec | Text Line Height | Text Line Corner Radius | Circle Placeholder | Block Placeholder Corner Radius |
|---|---|---|---|---|
| HIG | 12/16pt | 4pt | Matches avatar (e.g., 40pt) | 10pt |
| Fluent | 12/14/16px | 4px | 32/40px | 4px |
| Material | 16dp (title 24dp) | 4dp | 40dp | 12dp |

**State Definitions**:

| Spec | Placeholder Base | Shimmer Highlight |
|---|---|---|
| HIG | systemGray5 | systemGray6 |
| Fluent | neutralBackground3 | neutralBackground1 |
| Material | surfaceVariant | surfaceContainerHighest |

**Cross-Spec Conflict Points**:
- **Native support**: HIG/Material have no native component, both are derived implementations; only Fluent has native Skeleton
- **Block placeholder corner radius**: HIG largest (10pt), Material middle (12dp), Fluent smallest (4px)
- **Shimmer animation**: All three specs are 1.5s linear infinite left-to-right sweep

---

### 2.30 Drawer / Sidebar

**Purpose**: Slide-out or persistent side navigation panel.

**Anatomy**:
```
Drawer / Sidebar
├── Overlay / Scrim (slide-out)
└── Panel
    ├── Header (title / close)
    ├── Content / Nav Items
    └── Footer (optional)
```

**Size Specification Comparison**:

| Spec | Panel Width | Padding | Corner Radius | Nav Item Height | Overlay |
|---|---|---|---|---|---|
| HIG | 280-320pt | 16pt | 0/20pt | 44pt | black 40% |
| Fluent | 320px | 16px | 0px | — | black 40% |
| Material | 360dp | 12dp | full (item) | 56dp | onSurface 32% |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | secondarySystemBackground | neutralBackground1 + Acrylic | surfaceContainerLow |
| Item Hover | systemGray6 | — | onSurface 8% |
| Item Selected | systemBlue | — | secondaryContainer |
| Shadow | None (blur) | shadow28 | 12dp (level5) |

**Cross-Spec Conflict Points**:
- **Panel width**: Material widest (360dp), Fluent 320px, HIG 280-320pt
- **Nav item height**: Material tallest (56dp), HIG 44pt
- **Overlay opacity**: HIG/Fluent black 40%, Material onSurface 32%
- **Naming**: HIG=Sidebar, Fluent=NavigationView/Drawer, Material=Navigation Drawer

---

### 2.31 Pagination

**Purpose**: Switch between multiple pages of data.

**Anatomy**:
```
Pagination
├── Previous Button (chevron)
├── Page Item (number)
├── Ellipsis (...)
└── Next Button (chevron)
```

**Size Specification Comparison**:

| Spec | Page Item Size | Item Spacing | Corner Radius | Touch Target | Font |
|---|---|---|---|---|---|
| HIG | 32x32pt | 8pt | 8pt | 44x44pt | Subhead 15pt |
| Fluent | 32x32px | 4px | 4px | 32px/44px | Body 14pt |
| Material | 40x40dp | 4dp | full | 48x48dp | labelLarge 14pt |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | transparent | transparent | transparent |
| Hover | systemGray6 | neutralBackground2 | onSurface 8% |
| Current | systemBlue / white | brandBackground / inverted | primary / onPrimary |
| Disabled | systemGray | neutralForegroundDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: All three specs have no native component, all are derived implementations
- **Corner radius**: HIG 8pt, Fluent 4px, Material full (capsule)
- **Page item size**: Material largest (40dp), HIG/Fluent 32

---

### 2.32 Stepper

**Purpose**: Display progress of a multi-step process (wizard step bar).

**Anatomy**:
```
Stepper
├── Step
│   ├── Indicator (number / checkmark)
│   ├── Title
│   └── Subtitle (optional)
├── Connector (line)
└── Step...
```

**Size Specification Comparison**:

| Spec | Indicator Diameter | Connector Width | Step Spacing | Title Font |
|---|---|---|---|---|
| HIG | 28pt | 2pt | 8pt | Subhead 15pt |
| Fluent | 24px | 2px | 16px | Body 14pt |
| Material | 24dp | 1dp | 16dp | titleSmall 14pt |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Upcoming/Inactive | systemGray5 | neutralBackground3 | onSurface 38% |
| Current/Active | systemBlue | brandBackground | primary |
| Completed | systemBlue check | brandBackground check | primary check |
| Error | systemRed | error | error |
| Disabled | systemGray6 | neutralBackgroundDisabled | onSurface 12% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG/Fluent have no native component, both are derived implementations; only Material has native Stepper
- **Indicator diameter**: HIG largest (28pt), Fluent/Material 24
- **Connector width**: Material thinnest (1dp), HIG/Fluent 2

---

### 2.33 Sheet / ActionSheet

**Purpose**: Action list or content panel sliding up from the bottom.

**Anatomy**:
```
Sheet / ActionSheet
├── Overlay / Scrim
└── Panel (bottom)
    ├── Grabber / Drag Handle
    ├── Title / Header (optional)
    ├── Action List
    └── Cancel Action (optional)
```

**Size Specification Comparison**:

| Spec | Top Corner Radius | Padding | Handle Size | Action Item Height | Overlay |
|---|---|---|---|---|---|
| HIG | 20pt | 16pt | 36x5pt | 56pt | black 40% |
| Fluent | 8px | 16px | 32x4px | 44px | black 40% |
| Material | 28dp | 16dp | 32x4dp | 56dp | onSurface 32% |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | transparent / systemBlue | transparent | surfaceContainerLow |
| Pressed | systemGray5 | neutralBackground3 | onSurface 12% |
| Destructive | systemRed | error | — |
| Background | secondarySystemBackground + blur | neutralBackground1 + Acrylic | surfaceContainerLow |

**Cross-Spec Conflict Points**:
- **Native support**: Only HIG (Action Sheet/Sheet) and Material (Bottom Sheet) have native components; Fluent has no native bottom overlay, derived implementation (based on Dialog)
- **Top corner radius**: Material largest (28dp), HIG 20pt, Fluent smallest (8px)
- **Overlay**: HIG/Fluent black 40%, Material onSurface 32%

---

### 2.34 Avatar

**Purpose**: Display user avatar, initials, or icon.

**Anatomy**:
```
Avatar
├── Container (circle / square)
│   └── Image / Initials / Icon
├── Border (optional)
└── Status / Presence Badge (optional)
```

**Size Specification Comparison**:

| Spec | Small | Medium (default) | Large | xLarge | Corner Radius |
|---|---|---|---|---|---|
| HIG | 32pt | 40pt | 56pt | 80pt | full/13pt |
| Fluent | 24px | 32px | 40px | 48px | full/4px |
| Material | 24dp | 40dp | 56dp | 72dp | full |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Online/Available | systemGreen | success | — |
| Away | systemYellow | warning | — |
| Busy | systemRed | error | — |
| Offline | systemGray | neutralStrokeAccessible | — |
| Text bg/color | systemGray4 / white | brandBackground / inverted | primaryContainer / onPrimaryContainer |

**Cross-Spec Conflict Points**:
- **Native support**: HIG has no native component, derived implementation; Fluent=Avatar/Persona, Material=Avatar
- **Default size**: HIG 40pt / Fluent 32px / Material 40dp inconsistent
- **Square corner radius variant**: HIG 13pt, Fluent 4px, Material has no square (only full)
- **Presence status color**: HIG/Fluent provide, Material native does not include presence

---

### 2.35 Accordion

**Purpose**: Collapsible/expandable content grouping.

**Anatomy**:
```
Accordion
├── Accordion Item
│   ├── Header (Title + Chevron)
│   └── Content / Panel (collapsible)
└── Accordion Item...
```

**Size Specification Comparison**:

| Spec | Header Height | Header Padding | Title Font | Chevron | Corner Radius |
|---|---|---|---|---|---|
| HIG | 44pt | 16pt | Headline 17pt | 14pt | — |
| Fluent | 44px | 12px | Body 14pt Semibold | — | 4px |
| Material | 56dp | 16dp | titleMedium 16pt | 24dp | 12dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Collapsed | secondarySystemBackground | transparent | transparent |
| Expanded | secondarySystemBackground | neutralBackground2 | transparent |
| Hover | systemGray6 | neutralBackground2 | onSurface 8% |
| Pressed | — | — | onSurface 12% (Ripple) |
| Disabled | systemGray6 | neutralForegroundDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG=Disclosure Group, Fluent=Accordion; Material has no independent component, derived implementation (based on List)
- **Header height**: Material tallest (56dp), HIG/Fluent 44
- **Expand animation**: HIG 250ms ease-in-out, Fluent 200ms standard, Material 250ms standard

---

### 2.36 Carousel

**Purpose**: Horizontally scroll to display multiple items.

**Anatomy**:
```
Carousel
├── Slide Track / Viewport
│   └── Slide / Item
├── Page Control / Indicators (dots)
└── Navigation Arrows (optional)
```

**Size Specification Comparison**:

| Spec | Item Corner Radius | Item Spacing | Indicator Dot Diameter | Dot Spacing | Navigation Button |
|---|---|---|---|---|---|
| HIG | 13pt | 8pt | 8pt | 8pt | 44x44pt |
| Fluent | 8px | — | 8px | 8px | 32x32px |
| Material | 16dp | 8dp | 8dp | 8dp | 48x48dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Active dot | label | brandBackground | primary |
| Inactive dot | tertiaryLabel | neutralStroke1 | onSurfaceVariant |
| Arrow Default | systemBlue | neutralBackground1 + shadow8 | — |
| Arrow Disabled | systemGray | neutralBackgroundDisabled | — |

**Cross-Spec Conflict Points**:
- **Native support**: HIG is Page Control + horizontal scroll combination (derived); Fluent=Carousel, Material=Carousel
- **Item corner radius**: Material largest (16dp), HIG 13pt, Fluent smallest (8px)
- **Transition animation**: HIG 300ms ease-out, Fluent 300ms decelerate, Material 350ms emphasized

---

### 2.37 Timeline

**Purpose**: Display event nodes in chronological order.

**Anatomy**:
```
Timeline
├── Timeline Item
│   ├── Node (dot / icon)
│   ├── Connector (line)
│   └── Content (Timestamp / Title / Description)
└── Timeline Item...
```

**Size Specification Comparison**:

| Spec | Node Diameter | Connector Width | Node to Content Spacing | Item Spacing |
|---|---|---|---|---|
| HIG | 12pt | 2pt | 16pt | 20pt |
| Fluent | 12px | 2px | 12px | 16px |
| Material | 12dp | 2dp | 16dp | 24dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Completed | systemBlue filled | brandBackground | primary filled |
| Current/Active | systemBlue + halo | brandBackground + ring | primary |
| Upcoming/Default | systemGray4 | neutralBackground3 | outline |
| Error | systemRed | error | error |

**Cross-Spec Conflict Points**:
- **Native support**: All three specs have no native component, all are derived implementations
- **Item spacing**: Material largest (24dp), HIG 20pt, Fluent smallest (16px)
- **Node diameter consistent**: All three specs are 12 (pt/px/dp)

---

### 2.38 Tree

**Purpose**: Display expandable/collapsible hierarchical structure.

**Anatomy**:
```
Tree
├── Tree Node
│   ├── Disclosure Chevron (has children)
│   ├── Icon (optional)
│   ├── Label
│   └── Children (indented, collapsible)
└── Tree Node...
```

**Size Specification Comparison**:

| Spec | Row Height | Indent per Level | Chevron | Horizontal Padding | Font |
|---|---|---|---|---|---|
| HIG | 28/44pt | 16pt | 12pt | 16pt | Body 17pt |
| Fluent | 32px | 16px | 16x16px | 8px | Body 14pt |
| Material | 48dp | 24dp | 24x24dp | 16dp | bodyLarge 16pt |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | transparent | transparent | transparent |
| Hover | systemGray6 | neutralBackground2 | onSurface 8% |
| Selected | systemBlue | neutralBackground3 | secondaryContainer |
| Focused | — | brandStroke outline | — |
| Disabled | systemGray | neutralForegroundDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG=Outline View, Fluent=TreeView; Material has no independent native component, derived implementation
- **Row height**: Material tallest (48dp), HIG 28/44pt, Fluent 32px
- **Indent per level**: Material largest (24dp), HIG/Fluent 16

---

### 2.39 Divider

**Purpose**: Visually separate content sections.

**Anatomy**:
```
Divider
├── Line (horizontal / vertical)
└── Label (optional, centered)
```

**Size Specification Comparison**:

| Spec | Line Width | Color | Inset Indent | Label Font |
|---|---|---|---|---|
| HIG | 1pt | separator | 16/60pt | Footnote 13pt |
| Fluent | 1px | neutralStroke2 | Single side inset | Caption 12pt |
| Material | 1dp | outlineVariant | 16dp | bodySmall 12pt |

**State Definitions**:

| Variant | HIG | Fluent | Material |
|---|---|---|---|
| Horizontal | Default | Default | Full-width |
| Vertical | Supported | Supported | Supported |
| Inset | Inset 16/60pt | Single side inset | Left inset 16dp |
| Labeled | Center label | With Label | With Text (line segments on both sides) |

**Cross-Spec Conflict Points**:
- **Color token**: HIG=separator, Fluent=neutralStroke2, Material=outlineVariant
- **Line width consistent**: All three specs are 1 (pt/px/dp)
- **Inset**: HIG list inset 16/60pt, Material fixed 16dp, Fluent single side inset

---

### 2.40 Grid / Layout

**Purpose**: Responsive layout grid container.

**Anatomy**:
```
Grid / Layout
├── Container (max-width)
├── Margin (side margins)
└── Columns
    ├── Column (span)
    └── Gutter (column spacing)
```

**Size Specification Comparison**:

| Spec | Base Unit | Column Spacing | Maximum Columns | Page Margin |
|---|---|---|---|---|
| HIG | 8pt | 16pt (compact 8pt) | 12 | 16/20/24pt |
| Fluent | 4px | 16/24/32/48px | 12 | 16/24/32px |
| Material | 8dp | 16/24dp | 12 | 16/24dp |

**Breakpoint Comparison**:

| Spec | Breakpoint Divisions |
|---|---|
| HIG | Compact <600 / Regular 600-1024 / Wide >1024 (pt) |
| Fluent | Small <640 / Medium 640-1024 / Large 1024-1440 / XLarge >1440 (px) |
| Material | Compact <600 / Medium 600-840 / Expanded 840-1200 / Large 1200-1600 / XLarge >1600 (dp) |

**Cross-Spec Conflict Points**:
- **Native support**: All three specs have no native component, all are derived implementations
- **Base unit**: HIG/Material 8 grid, Fluent 4 grid
- **Breakpoint count**: Material/Fluent have finer divisions (5/4 tiers), HIG has 3 tiers
- **Maximum columns consistent**: All three specs are 12 columns

---

### 2.41 Space / Stack

**Purpose**: A layout container that arranges child elements with uniform spacing.

**Anatomy**:
```
Stack
├── Child
├── Spacing (gap)
└── Child...
```

**Size Specification Comparison (Spacing Tokens)**:

| Spec | Base Grid | Default Spacing | Token Range |
|---|---|---|---|
| HIG | 8pt | 8pt(xSmall) | 4/8/12/16/20/24/32pt |
| Fluent | 4px | 12px(medium) | 4/8/12/16/20/24px |
| Material | 8dp | 8dp(small) | 4/8/16/24/32dp |

**State Definitions**:

| Property | HIG | Fluent | Material |
|---|---|---|---|
| Direction | H/V/Z Stack | horizontal/vertical | horizontal/vertical |
| Alignment | leading/center/trailing | start/center/end/stretch | start/center/end/stretch |
| Justify | start/center/end/space-between | start/center/end/space-between | start/center/between/around |

**Cross-Spec Conflict Points**:
- **Native support**: HIG/Material have no native component (derived, HIG corresponds to SwiftUI Stack concept); only Fluent has native Stack
- **Base grid**: HIG/Material 8 grid, Fluent 4 grid
- **Default spacing**: HIG 8pt / Fluent 12px / Material 8dp inconsistent

---

### 2.42 AspectRatio

**Purpose**: A container that maintains a fixed aspect ratio for content.

**Anatomy**:
```
AspectRatio
├── Ratio Box (fixed aspect ratio)
│   └── Content (fit / fill)
└── Placeholder (loading, optional)
```

**Size Specification Comparison**:

| Spec | Width | Corner Radius | Placeholder Background | Content Clipping |
|---|---|---|---|---|
| HIG | Adapts to parent container | 13pt | systemGray5 | clip to corner radius |
| Fluent | 100% | 4px | — | hidden |
| Material | 100% | 12dp | surfaceVariant | cover |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Common ratios | 1:1 / 4:3 / 16:9 / 3:2 / 21:9 | Same as HIG | Same as HIG |
| Loading | aria-busy | Skeleton maintains ratio | surfaceVariant |
| Error | — | — | surfaceVariant + icon |

**Cross-Spec Conflict Points**:
- **Native support**: All three specs have no native component, all are derived implementations
- **Corner radius**: HIG largest (13pt), Material middle (12dp), Fluent smallest (4px)
- **Common ratios consistent**: All three specs support 1:1 / 4:3 / 16:9 / 3:2 / 21:9

---

### 2.43 Popover

**Purpose**: A floating information panel attached to an anchor.

**Anatomy**:
```
Popover
├── Arrow (pointer to anchor, optional)
└── Container / Surface
    ├── Header (optional)
    ├── Content
    └── Actions (optional)
```

**Size Specification Comparison**:

| Spec | Minimum Width | Maximum Width | Padding | Corner Radius | Arrow |
|---|---|---|---|---|---|
| HIG | 200pt | 400pt | 16pt | 13pt | 12pt |
| Fluent | 160px | 320px | 12px 16px | 6px | 8x8px |
| Material | 112dp | 320dp | 16dp | 12dp | optional |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Background | secondarySystemBackground + blur | neutralBackground1 + Acrylic | surfaceContainer |
| Shadow | None (blur) | shadow16 | 3dp (level3) |
| Entry animation | 250ms ease-out | 150ms decelerate | 150ms decelerate |

**Cross-Spec Conflict Points**:
- **Native support**: HIG=Popover, Fluent=Popover; Material has no independent component, derived implementation (based on Menu/surface)
- **Corner radius**: HIG largest (13pt), Material middle (12dp), Fluent smallest (6px)
- **Minimum width**: HIG widest (200pt), Fluent 160px, Material narrowest (112dp)

---

### 2.44 Modal

**Purpose**: Large/full-screen modal overlay panel (distinct from small dialog).

**Anatomy**:
```
Modal
├── Overlay / Scrim
└── Container / Surface
    ├── Header (Cancel / Title / Done)
    ├── Content (scrollable)
    └── Footer (optional)
```

**Size Specification Comparison**:

| Spec | Corner Radius | Header Height | Padding | Title Font | Overlay |
|---|---|---|---|---|---|
| HIG | 20pt / 0pt(full screen) | 56pt | 16/20pt | Headline 17pt | black 40% |
| Fluent | 8px / 0px(full screen) | — | 24px | Title 24pt | black 40% |
| Material | 0dp(full screen) / 28dp(large screen) | 64dp | 24dp | titleLarge 22pt | — |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Presented | Slide in from bottom | Fade in + move up | Enter from bottom |
| Scrolled | — | — | Top bar shadow 3dp |
| Background | systemBackground | neutralBackground1 + Acrylic | surface |
| Entry animation | 350ms ease-out | 300ms decelerate | 300ms decelerate |

**Cross-Spec Conflict Points**:
- **Naming**: HIG=Modal Sheet/Full Screen Cover, Fluent=Modal Dialog, Material=Full-screen Dialog
- **Corner radius**: Material large screen degenerate 28dp largest, HIG 20pt, Fluent 8px
- **Primary action position**: HIG/Material on right (Done), Fluent primary on left

---

### 2.45 FAB

**Purpose**: A floating circular primary action button.

**Anatomy**:
```
FAB
├── Background (circle / capsule)
├── Icon
└── Label (Extended variant)
```

**Size Specification Comparison**:

| Spec | Small | Regular/Standard | Large | Extended Corner Radius |
|---|---|---|---|---|
| HIG | 44pt | 56pt | — | 28pt |
| Fluent | 40x40px | 48x48px | — | circular |
| Material | 40x40dp | 56x56dp | 96x96dp | 16dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | systemBlue | brandBackground / shadow8 | primaryContainer / 6dp |
| Hover | systemBlue darken 10% | brandBackgroundHover / shadow16 | + 8% / 8dp |
| Pressed | systemBlue darken 20% | brandBackgroundPressed / shadow4 | + 12% (Ripple) |
| Disabled | systemGray4 | neutralBackgroundDisabled | onSurface 12% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG has no floating button convention (derived), Fluent has no floating convention (derived); only Material has native FAB
- **Size tiers**: Material has an additional Large tier (96dp) with color variants; HIG/Fluent only have two tiers
- **Icon/background color**: HIG systemBlue/white, Fluent brand/inverted, Material primaryContainer/onPrimaryContainer

---

### 2.46 SearchBar

**Purpose**: An input field for entering search keywords.

**Anatomy**:
```
SearchBar
├── Background / Container
├── Leading Search Icon
├── Placeholder / Input Text
├── Clear Button (optional)
└── Cancel / Trailing (optional)
```

**Size Specification Comparison**:

| Spec | Height | Corner Radius | Horizontal Padding | Icon | Font |
|---|---|---|---|---|---|
| HIG | 36pt | 10pt | 8pt | 16pt | Body 17pt |
| Fluent | 32px | 4px | 12px | 16x16px | Body 14pt |
| Material | 56dp | full | 16dp | 24x24dp | bodyLarge 16pt |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | tertiarySystemFill | neutralStroke1 | surfaceContainerHigh |
| Hover | — | neutralStrokeAccessible | + onSurface 8% |
| Focused | + Cancel visible | brandStroke | onSurface (expand suggestions) |
| Filled | + Clear visible | + Clear | onSurface |
| Disabled | systemGray6 | neutralStrokeDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Naming**: HIG=Search Field, Fluent=SearchBox, Material=Search Bar (all native)
- **Height**: Material tallest (56dp), HIG 36pt, Fluent shortest (32px)
- **Corner radius**: Material full (capsule), HIG 10pt, Fluent 4px

---

### 2.47 Rating

**Purpose**: Star rating display and input.

**Anatomy**:
```
Rating
├── Star Item (filled / half / empty)
├── Star Item...
└── Value Label (optional)
```

**Size Specification Comparison**:

| Spec | Small | Medium (default) | Large | Star Spacing |
|---|---|---|---|---|
| HIG | 16pt | 24pt | 32pt | 4pt |
| Fluent | 16px | 20px | 24px | 2/4px |
| Material | 18dp | 24dp | 36dp | 4dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Filled | systemYellow | warning | primary |
| Half | systemYellow half | warning half | primary half |
| Empty | systemGray4 | neutralStroke1 | outlineVariant |
| Hover | systemYellow 60% | warning preview | primary preview |
| Disabled | systemGray5 | neutralForegroundDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG/Material have no native component, both are derived implementations; only Fluent has native Rating
- **Fill color**: HIG/Fluent use yellow (systemYellow/warning), Material uses primary color
- **Default size**: HIG/Fluent/Material Medium are 24pt/20px/24dp respectively

---

### 2.48 ColorPicker

**Purpose**: Select and preview color values.

**Anatomy**:
```
ColorPicker
├── Trigger (Color Well / Swatch + Value)
└── Picker Popover / Panel
    ├── Spectrum / Saturation Area
    ├── Hue / Alpha Slider
    ├── Preset Swatches
    └── Hex / RGB Input
```

**Size Specification Comparison**:

| Spec | Swatch/Well Size | Well Corner Radius | Panel Corner Radius | Slider Height | Preset Swatch |
|---|---|---|---|---|---|
| HIG | 28pt | full | 13pt | 4pt | 24x24pt |
| Fluent | 32x32px (preview) | — | 8px | 12px | 24x24px |
| Material | 40x40dp | 8dp | 12dp | 24dp | 32x32dp |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Default | Current color swatch | Cursor + shadow4 | outline |
| Hover | systemBlue ring | — | onSurface 8% |
| Focused | systemBlue outline | brandStroke outline | primary border |
| Selected (preset) | — | brandStroke 2px | primary 2dp |
| Disabled | systemGray4 | neutralForegroundDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG=Color Well, Fluent=ColorPicker; Material has no native component, derived implementation
- **Well/swatch size**: Material largest (40dp), Fluent 32px, HIG smallest (28pt)
- **Panel corner radius**: HIG largest (13pt), Material middle (12dp), Fluent smallest (8px)

---

### 2.49 Calendar

**Purpose**: Month calendar view for date selection (distinct from compact DatePicker).

**Anatomy**:
```
Calendar
├── Header (Month / Year Title + Navigation)
├── Weekday Labels
├── Day Grid
│   └── Day Cell (Date Number + Event Indicator)
└── Footer (optional)
```

**Size Specification Comparison**:

| Spec | Cell Size | Cell Spacing | Cell Corner Radius | Date Font | Navigation Button |
|---|---|---|---|---|---|
| HIG | 44x44pt | 4pt | full(circle) | Body 17pt | 44x44pt |
| Fluent | 40x40px | 4px | 4px | Body 14pt | 32x32px |
| Material | 48x48dp | — | full | bodyLarge 16pt | 24x24dp icon |

**State Definitions**:

| State | HIG | Fluent | Material |
|---|---|---|---|
| Today | systemBlue border circle | brandStroke border / brandForeground | primary border |
| Selected | systemBlue / white | brandBackground / inverted | primary / onPrimary |
| In Range | systemBlue 15% | — | primaryContainer |
| Outside Month | tertiaryLabel | neutralForeground4 | onSurface 38% |
| Disabled | systemGray | neutralForegroundDisabled | onSurface 38% |

**Cross-Spec Conflict Points**:
- **Native support**: HIG=Calendar View, Fluent=Calendar, Material=Date Calendar (all provided)
- **Cell size**: Material largest (48dp), HIG 44pt, Fluent smallest (40px)
- **Cell corner radius**: HIG/Material use full (circle), Fluent uses 4px square
- **Range selection**: HIG systemBlue 15%, Material primaryContainer, Fluent does not support range

---

## 3. Cross-Specification Conflict Summary

### 3.1 Corner Radius Conflicts

| Component | HIG | Fluent | Material | Suggestion |
|---|---|---|---|---|
| Button | 8-10pt | 4px | full | Choose per spec |
| Card | 10-13pt | 4px | 12dp | Choose per spec |
| Dialog | 13pt | 8px | 28dp | Choose per spec |
| Input | 10pt | 4px | 8dp | Choose per spec |
| Menu | 13pt | 4px | 12dp | Choose per spec |

### 3.2 Size Conflicts

| Component | HIG | Fluent | Material | Suggestion |
|---|---|---|---|---|
| Button height | 28-44pt | 24-40px | 32-48dp | Choose per spec |
| Input height | 44pt | 32px | 56dp | Choose per spec |
| List item height | 44pt | 40px | 48dp | Choose per spec |
| Switch track | 51x31pt | 40x20px | 52x32dp | Choose per spec |

### 3.3 Shadow Conflicts

| Scenario | HIG | Fluent | Material | Suggestion |
|---|---|---|---|---|
| Card | None | On hover | Always | Choose per spec |
| Menu | None | shadow8 | 3dp | Choose per spec |
| Dialog | None | shadow16 | 6dp | Choose per spec |
| Button | None | None | 1dp | Choose per spec |

### 3.4 Button Position Conflicts

| Scenario | HIG | Fluent | Material |
|---|---|---|---|
| Dialog primary action | Right | Left | Right |
| Form submission | Bottom right | Bottom left | Bottom right |

### 3.5 Color System Conflicts

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Primary color expression | System color (Blue) | Brand color (Brand) | Primary color (Primary) |
| Semantic colors | System Red/Green | Success/Error tokens | Error/Success tokens |
| Background hierarchy | systemBackground 1/2/3 | neutralBackground 1-5 | surfaceContainer low/high |
| Disabled state | Gray | Reduced opacity | Reduced opacity |

### 3.6 Motion Conflicts

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Button press | Color darken | Background change | Ripple effect |
| Switch toggle | Spring effect | Standard transition | Spring effect |
| Page transition | 250ms | 300ms | 300ms |
| Easing function | Ease In-Out | Standard | Standard |

### 3.7 Material Conflicts

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Background effect | Translucent blur | Acrylic / Mica | None |
| Depth expression | Layered background color | Shadow system | Elevation system |
| Navigation bar | Blur background | Acrylic | Solid color |
