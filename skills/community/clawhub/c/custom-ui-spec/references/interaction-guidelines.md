# Interaction Guidelines Comparison

Comparison of user interaction behavior specifications across three major design systems.

## Table of Contents

1. [Navigation Modes](#1-navigation-modes)
2. [Gestures and Touch](#2-gestures-and-touch)
3. [Feedback Mechanisms](#3-feedback-mechanisms)
4. [Confirmation and Undo](#4-confirmation-and-undo)
5. [Selection and Operations](#5-selection-and-operations)
6. [Keyboard and Accessibility](#6-keyboard-and-accessibility)
7. [Platform Differences](#7-platform-differences)
8. [Conflict Summary](#8-conflict-summary)

---

## 1. Navigation Modes

### 1.1 Hierarchical Navigation

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Back method | Top-left back button + left swipe back gesture | Alt+Left / Back button | System back gesture + top-left back arrow |
| Deep navigation | Navigation Bar push/pop | NavigationView hierarchy | Navigation Drawer + Back stack |
| Root navigation | Tab Bar fixed at bottom | Pivot / NavigationView | Bottom Navigation / Drawer |
| Modal navigation | Sheet (slides in from bottom) | Dialog | Dialog / Bottom Sheet |
| Page transition animation | 250ms push/pop, horizontal slide | 300ms enter/exit, vertical or horizontal | 300ms parent->child, horizontal entry |
| Full-screen navigation | Tab Bar hidden + large title | Responsive expand/collapse | App Bar expand/collapse |

### 1.2 Navigation Controls

**HIG**:
- iOS uses Tab Bar (bottom) + Navigation Bar (top)
- macOS uses Sidebar + Toolbar
- Main interface uses 3-level nesting: Tab Bar to Navigation Bar to Content
- Tab Bar maximum 5 tabs, more than 5 use "More" tab
- Large title mode: Root pages use large titles, sub-pages use standard titles
- Elastic transition animation between large title and standard title

**Fluent**:
- Uses NavigationView as the primary navigation container
- Supports three navigation modes: Top (tabs), Left (sidebar), Both
- Sidebar width 260px, collapsible
- Uses Pivot (tab navigation) for switching within pages
- Breadcrumb navigation must show full path; current item not clickable
- Back stack management: push on each navigation, pop on back, keep within 5 levels

**Material**:
- Uses Bottom Navigation (3-5 items) or Navigation Drawer (5+ items)
- Top App Bar height varies by mode: small 64dp / medium 80dp / large 152dp
- Bottom navigation selected item must be visible, maximum 5 items
- Navigation drawer supports modal (overlays content) or permanent (fixed sidebar)
- Back gesture must not be hijacked by the app; system back behavior must be preserved

### 1.3 Navigation Guideline Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Primary navigation position | Bottom Tab Bar | Top/Side | Bottom/Side |
| Back method | Left swipe + button | Shortcut + button | System gesture + button |
| Breadcrumb | Not used | Required | Not used |
| Navigation depth | Shallow (2-3 levels) | Deep (multiple levels) | Medium (3-4 levels) |

---

## 2. Gestures and Touch

### 2.1 Standard Gestures

| Gesture | HIG | Fluent | Material |
|---|---|---|---|
| Tap | Select/Trigger | Select/Trigger | Select/Trigger |
| Double Tap | Zoom in/out | — | Zoom in/out |
| Long Press | Context menu / Data preview | Context menu / Rename | Context menu / Drag start |
| Swipe Left | Go back / Delete | — | Go back |
| Swipe Right | — | — | Open drawer / Go back |
| Swipe Down | Refresh / Close Sheet | — | Refresh / Close Sheet |
| Swipe Up | Control Center | — | View more |
| Pinch | Zoom in/out | Zoom in/out | Zoom in/out |
| Drag | Reposition / Reorder | Reposition / Reorder | Reposition / Reorder |
| Three-Finger Pinch | Copy | — | — |
| Three-Finger Spread | Paste | — | — |
| Three-Finger Swipe Left | Undo | — | — |
| Three-Finger Swipe Right | Redo | — | — |
| Edge Swipe | System-level back | — | System-level back |

### 2.2 List Item Gestures

| Action | HIG | Fluent | Material |
|---|---|---|---|
| Delete | Swipe left to reveal delete button | Select + Delete key | Swipe left to reveal delete |
| Multi-select | Edit mode | Checkbox column | Long press to enter selection mode |
| Reorder | Long press drag handle | Drag handle | Long press drag |
| View more | Swipe to show more actions | Right-click menu | Swipe to show actions |
| Detail preview | 3D Touch / Long press | Hover popup | Long press preview |

### 2.3 Touch Targets

| Spec | Minimum Size | Spacing | Description |
|---|---|---|---|
| HIG | 44x44pt | 8pt | All interactive elements |
| Fluent | 32x32px (keyboard/mouse) / 44x44px (touch) | 4px | Depends on input device |
| Material | 48x48dp | 8dp | All interactive elements |

### 2.4 Gesture Guideline Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Swipe left to go back | Yes (standard) | No | Yes (standard) |
| Edge gesture | System-level, app cannot intercept | Not applicable (desktop-first) | System-level, app cannot intercept |
| Undo gesture | Three-finger swipe left | Ctrl+Z | — |
| Touch target | 44pt | 32px (desktop) / 44px (touch) | 48dp |
| Context menu trigger | Long press / 3D Touch | Right click / Long press | Long press |

---

## 3. Feedback Mechanisms

### 3.1 Haptic Feedback

**HIG**:
- Uses UIFeedbackGenerator three types of feedback:
  - `UIImpactFeedbackGenerator`: Physical collision feel (light / medium / heavy)
  - `UINotificationFeedbackGenerator`: Success/Warning/Error
  - `UISelectionFeedbackGenerator`: On selection change
- Use cases: Button press, switch toggle, list selection, drag snap, error vibration
- Works with Taptic Engine for fine tactile feel

**Fluent**:
- No standardized haptic feedback API
- Relies on Windows system haptic feedback
- Primarily uses visual feedback instead of haptic

**Material**:
- Uses HapticFeedback API
- Types: `LONG_PRESS`, `TEXT_HANDLE_MOVE`, `KEYBOARD_TAP`, `CLOCK_TICK`, `CONFIRM`, `REJECT`
- Use cases: Long press confirmation, keyboard key press, drag start/end

### 3.2 Visual Feedback

| Feedback Type | HIG | Fluent | Material |
|---|---|---|---|
| Touch press | Highlight/Color darken | Background color change | Ripple effect (water ripple diffusion) |
| Hover | None (touch) / Subtle change (pointer) | Background color change + shadow change | Background color change + shadow elevate |
| Focus | Highlight outline | Brand color border + outline | Brand color outline |
| Loading | Progress View | Progress Bar / Spinner | Progress Indicator |
| Pull-to-refresh | System Pull-to-Refresh | Not commonly used | SwipeRefreshLayout |
| State change | Color + icon | Color + icon | Color + icon + animation |

### 3.3 Ripple Effect (Material Specific)

```
Touch point as center  → Ripple spreads outward  → Covers entire element  → Fades out
        0ms                   100ms                   200ms                  300ms
```

- Color: onSurface color at 10-20% opacity
- Duration: 300ms
- Types:
  - `unbounded`: Circular diffusion, not limited by boundaries (used for icon buttons)
  - `bounded`: Rectangular diffusion, clipped by element boundaries (used for buttons, list items)
- Triggers on press, stops immediately on release

### 3.4 Feedback Guideline Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Press feedback | Highlight/Darken | Background color change | Ripple diffusion |
| Haptic feedback | Three refined types | No standard | System-level |
| Hover feedback | Pointing device only | Standard behavior | Standard behavior |
| Pull-to-refresh | Standard behavior | Not recommended | Standard behavior |

---

## 4. Confirmation and Undo

### 4.1 Destructive Operations

**HIG**:
- Destructive operations must show confirmation
- Delete button uses red (`systemRed`)
- Uses Action Sheet or Alert for confirmation
- Supports undo (three-finger swipe left / Cmd+Z)
- Reversible operations may not require confirmation (e.g., mark as read)

**Fluent**:
- Destructive operations show confirmation Dialog
- Uses `error` color for emphasis
- Supports Ctrl+Z undo
- Batch operations require confirmation
- Supports operation history

**Material**:
- Recommends using Snackbar + Undo instead of confirmation Dialog
- Shows Snackbar with Undo button after deletion
- Only uses confirmation Dialog for irreversible operations
- Error/Delete operations use `error` color

### 4.2 Confirmation Dialog Use Cases

| Scenario | HIG | Fluent | Material |
|---|---|---|---|
| Delete single item | Action Sheet confirmation | Dialog confirmation | Snackbar + Undo (recommended) |
| Delete multiple items | Alert confirmation | Dialog confirmation | Dialog confirmation |
| Discard unsaved content | Alert confirmation | Dialog confirmation | Dialog confirmation |
| Submit/Send | No confirmation | No confirmation | No confirmation |
| Mark/Categorize | No confirmation | No confirmation | No confirmation |
| Irreversible operation (clear) | Alert confirmation (red button) | Dialog confirmation (red button) | Dialog confirmation (error color) |

### 4.3 Undo Mechanisms

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Gesture | Three-finger swipe left to undo / Three-finger swipe right to redo | Ctrl+Z / Ctrl+Y | Snackbar Undo button |
| Time limit | Immediate undo | No limit (history) | During Snackbar display (4-5s) |
| Scope | Text editing, delete, move | All operations | Delete, move, text editing |
| Redo | Three-finger swipe right | Ctrl+Y / Ctrl+Shift+Z | No standard |
| Multi-step undo | Supported | Supported (history panel) | Single step (Snackbar) |

### 4.4 Confirmation Guideline Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Delete confirmation method | Action Sheet confirmation | Dialog confirmation | Snackbar + Undo (recommended) |
| Undo method | Gesture | Keyboard shortcut | Snackbar button |
| Undo time limit | Immediate | No limit | 4-5s |
| Red usage | Destructive button | Error emphasis | Error/Delete |

---

## 5. Selection and Operations

### 5.1 Text Selection

**HIG**:
- Double-tap to select word, triple-tap to select paragraph
- Shows selection handles (blue dots) draggable to adjust range
- Shows contextual toolbar after selection (Cut/Copy/Paste/Define/Share)
- Supports Cmd+C / Cmd+X / Cmd+V

**Fluent**:
- Double-click to select word, triple-click to select paragraph
- Shows floating toolbar after selection (Cut/Copy/Paste)
- Supports Ctrl+C / Ctrl+X / Ctrl+V
- Supports spell check right-click menu

**Material**:
- Double-tap to select word, triple-tap to select paragraph
- Selection handles (blue circle + blue vertical line)
- Shows contextual toolbar after selection (Cut/Copy/Paste/Select All)
- Long press empty area to enter selection mode

### 5.2 Multiple Selection

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Enter selection | Tap "Edit" button or long press | Checkbox column | Long press list item |
| Selection indicator | Selected item highlight + checkmark | Checkbox check | Selected item highlight + checkmark |
| Select all | Select all button | Header checkbox | Select all button |
| Exit selection | Tap "Done" | Deselect | Tap empty area |
| Action bar | Bottom action bar | Top command bar | Top/bottom action bar |
| Shift range select | Supported (macOS) | Supported | Supported |

### 5.3 Drag and Drop

**HIG**:
- Long press to start drag
- Element is semi-transparent and follows finger during drag
- Can be dragged to target area or delete area
- Supports drag reorder (list, collection view)
- Drag snap animation

**Fluent**:
- Drag handle or long press
- Shows preview (semi-transparent) during drag
- Supports cross-app drag
- Drop area highlights
- Drag reorder list

**Material**:
- Long press to start drag
- Element elevates shadow during drag
- Drop area highlights
- Drag reorder list and grid
- Supports cross-container drag

### 5.4 Right-Click Menu

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Trigger | Long press (touch) / Right-click (macOS) | Right-click (Windows) / Long press | Long press |
| Content | Context-relevant actions | Context-relevant actions | Context-relevant actions |
| Custom | System provides standard menus | Fully customizable | Customizable |
| Position | Finger/cursor position | Cursor position | Finger/touch position |

### 5.5 Selection Guideline Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Enter multi-select | Edit button or long press | Checkbox column | Long press |
| Exit multi-select | Tap "Done" | Deselect | Tap empty area |
| Right-click menu scope | System standard + custom | Fully custom | Fully custom |
| Cross-app drag | Supported | Supported | Not supported |

---

## 6. Keyboard and Accessibility

### 6.1 Keyboard Shortcuts

**HIG (macOS)**:
- Cmd+C / Cmd+X / Cmd+V: Clipboard operations
- Cmd+Z / Cmd+Shift+Z: Undo/Redo
- Cmd+F: Find
- Cmd+A: Select All
- Cmd+S: Save
- Tab / Shift+Tab: Focus forward/backward
- Space: Preview
- Enter: Confirm
- Escape: Cancel/Close

**Fluent (Windows)**:
- Ctrl+C / Ctrl+X / Ctrl+V: Clipboard operations
- Ctrl+Z / Ctrl+Y: Undo/Redo
- Ctrl+F: Find
- Ctrl+A: Select All
- Ctrl+S: Save
- Tab / Shift+Tab: Focus forward/backward
- Alt+Left / Alt+Right: Forward/Backward navigation
- F6: Switch pane focus
- Alt+F4: Close window

**Material (ChromeOS / Android)**:
- Ctrl+C / Ctrl+X / Ctrl+V: Clipboard operations
- Ctrl+Z / Ctrl+Shift+Z: Undo/Redo
- Ctrl+F: Find
- Ctrl+A: Select All
- Ctrl+S: Save
- Tab / Shift+Tab: Focus forward/backward
- Ctrl+Shift+N: New

### 6.2 Focus Management

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| Focus indicator | System standard outline | Brand color border + outline | Brand color outline |
| Tab order | Logical order (top to bottom, left to right) | Logical order | Logical order |
| Focus capture | Modal focus restricted to dialog | Modal focus restricted | Modal focus restricted |
| Focus return | Returns to trigger element on close | Returns to trigger element on close | Returns to trigger element on close |
| No-focus mode | Touch Bar / VoiceOver | Keyboard navigation highlight | TalkBack focus |

### 6.3 Screen Readers

| Aspect | HIG | Fluent | Material |
|---|---|---|---|
| System | VoiceOver | Narrator | TalkBack |
| Label requirement | accessibilityLabel | aria-label | contentDescription |
| Hint requirement | accessibilityHint | aria-description | contentDescription |
| Group | accessibilityContainer | role="group" | focusable="false" |
| Live region | — | aria-live | accessibilityLiveRegion |
| Custom action | accessibilityCustomActions | — | accessibilityAction |

### 6.4 Keyboard Guideline Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Undo | Cmd+Z | Ctrl+Z | Ctrl+Z |
| Redo | Cmd+Shift+Z | Ctrl+Y | Ctrl+Shift+Z |
| Close | Cmd+W | Alt+F4 | — |
| Navigate back | Cmd+[ | Alt+Left | Backspace |
| Focus indicator | Standard outline | Brand color border | Brand color outline |

---

## 7. Platform Differences

### 7.1 Mobile vs Desktop

| Aspect | Mobile | Desktop |
|---|---|---|
| Navigation | Bottom tabs + back gesture | Sidebar + breadcrumb + tabs |
| Primary input | Touch | Keyboard + Mouse |
| Hover | None | Standard behavior |
| Right-click | Long press replacement | Standard right-click |
| Multi-task | System switcher | Window manager |
| Shortcuts | Very few | Rich |
| Drag | Full-screen operation | Windowed operation |

### 7.2 HIG Platform Differences

| Feature | iOS | macOS | iPadOS |
|---|---|---|---|
| Navigation | Tab Bar + Navigation Bar | Sidebar + Toolbar | Sidebar + Split View |
| Back | Left swipe gesture + button | Cmd+[ + button | Left swipe gesture + button |
| Right-click | Long press | Right-click | Long press / Right-click (pointer) |
| Selection | Touch selection | Shift+Click / Cmd+Click | Touch + Keyboard |
| Drag | Long press drag | Click drag | Long press / Click drag |
| Shortcuts | Very few | Rich | Keyboard support |
| Undo | Three-finger swipe left | Cmd+Z | Three-finger swipe left / Cmd+Z |

### 7.3 Fluent Platform Differences

| Feature | Windows | Web | Mobile |
|---|---|---|---|
| Navigation | NavigationView | Responsive | Pivot |
| Menu | Right-click + Context | Right-click + Custom | Long press |
| Selection | Ctrl+Click / Shift+Click | Same | Long press selection |
| Drag | Cross-app | In-browser | In-app |
| Shortcuts | Rich (Win key) | Partial | Very few |
| Zoom | System zoom | Browser zoom | Gesture zoom |

### 7.4 Material Platform Differences

| Feature | Android | Web | Flutter |
|---|---|---|---|
| Navigation | Bottom Nav + Drawer | Responsive | Responsive |
| Back | System gesture + button | Browser back | Platform back |
| Menu | Long press | Right-click / Long press | Long press |
| Selection | Long press | Click / Cmd+Click | Long press |
| Shortcuts | Very few | Rich | Platform-dependent |
| Haptic | HapticFeedback | None | Platform-dependent |
| Dynamic color | Android 12+ native | Needs custom | Needs custom |

---

## 8. Conflict Summary

### 8.1 Core Interaction Conflicts

| Conflict Point | HIG | Fluent | Material | Suggestion |
|---|---|---|---|---|
| Primary navigation position | Bottom | Top/Side | Bottom/Side | Mobile: HIG/Material; Desktop: Fluent |
| Delete confirmation | Action Sheet | Dialog | Snackbar + Undo | Reversible: Material; Irreversible: HIG/Fluent |
| Press feedback | Color darken | Background change | Ripple | Choose per spec |
| Touch target | 44pt | 32px(desktop)/44px(touch) | 48dp | Choose per spec |
| Hover feedback | Pointing device only | Standard | Standard | None on mobile, standard on desktop |
| Undo method | Gesture | Keyboard | Snackbar | Choose per platform |
| Right-click menu | System standard | Fully custom | Fully custom | Choose per spec |
| Focus indicator | System standard | Brand color | Brand color | Choose per spec |

### 8.2 Navigation Conflicts

| Conflict Point | HIG | Fluent | Material |
|---|---|---|---|
| Back gesture | Left swipe back | Alt+Left | System back gesture |
| Breadcrumb | Not used | Required | Not used |
| Navigation depth | 2-3 levels | Multiple levels | 3-4 levels |
| Page transition | Horizontal slide 250ms | Vertical/horizontal 300ms | Horizontal entry 300ms |

### 8.3 Gesture Conflicts

| Gesture | HIG | Fluent | Material |
|---|---|---|---|
| Swipe left | Back/Delete | — | Back/Delete |
| Long press | Context menu/Preview | Context menu/Rename | Context menu/Drag start |
| Three-finger gesture | Undo/Redo/Clipboard | — | — |
| Edge gesture | System back | — | System back |

### 8.4 Feedback Conflicts

| Feedback | HIG | Fluent | Material |
|---|---|---|---|
| Press | Highlight | Background color | Ripple |
| Haptic | Three refined types | No standard | System-level |
| Loading | Progress View | Progress Bar | Progress Indicator |
| Pull-to-refresh | Standard | Not recommended | Standard |
