# UI Design Specification Validation Checklist

## Usage

1. Select the relevant specification (HIG / Fluent / Material / All), choose the corresponding check items
2. Check each item one by one, mark as passed `[x]` or not passed `[ ]`
3. Items not passed must record the reason and modification suggestion
4. After all checks are completed, calculate the pass rate and issue distribution

---

## General Check Items

### Accessibility

- [ ] All text color contrast >= 4.5:1 (body text)
- [ ] Large text (18pt+ or 14pt+ Bold) contrast >= 3:1
- [ ] UI component border contrast >= 3:1
- [ ] All interactive elements have a clear focus state
- [ ] All interactive elements have a clear hover state (keyboard/mouse devices)
- [ ] Disabled state is visually clear and distinguishable, does not rely on color alone
- [ ] Touch targets minimum 44x44pt/px/dp
- [ ] Supports keyboard navigation (Tab order is reasonable)
- [ ] Supports screen readers (correct aria labels)
- [ ] Supports Reduced Motion preference

### Structure and Semantics

- [ ] Text has correct semantic hierarchy (title/body/supporting text)
- [ ] Uses semantic HTML tags (button instead of div)
- [ ] Form elements are associated with labels
- [ ] Icons have aria-label or aria-hidden
- [ ] Dialogs have aria-modal and focus management

### Responsive

- [ ] Supports text scaling up to 200%
- [ ] Supports different screen sizes
- [ ] Both touch and keyboard/mouse input are usable

---

## HIG Specific Check Items

### Color

- [ ] Uses SF Pro font family (or system font stack)
- [ ] Uses system colors or semantic color tokens
- [ ] Supports Light/Dark mode switching
- [ ] Custom colors provide dual-mode versions
- [ ] Avoids pure black and pure white; uses system background colors

### Shape

- [ ] Corner radius uses continuous corner radius
- [ ] Large containers use larger corner radius
- [ ] Nested element corner radius is smaller than parent container
- [ ] Capsule buttons use full corner radius

### Depth

- [ ] Relies on hierarchical background colors rather than shadows to express depth
- [ ] Minimizes shadow usage
- [ ] Modal layers use translucent overlay

### Spacing

- [ ] Follows 8pt grid system
- [ ] No content is obscured within the safe area
- [ ] Page margins 16pt (iPhone) / 20pt (iPad/macOS)

### Components

- [ ] Button minimum height 28pt, recommended 34pt
- [ ] Input field minimum height 44pt
- [ ] Switch uses system Green for on state
- [ ] List item height 44pt (single line)
- [ ] Navigation bar height 44pt (iOS) / 52pt (macOS)
- [ ] Tab bar maximum 5 tabs
- [ ] Segmented control height 32pt

### Platform

- [ ] iOS uses bottom tab bar navigation
- [ ] macOS uses sidebar + toolbar
- [ ] Supports pointer hover effects (iPadOS/macOS)
- [ ] Uses system-provided icons

---

## Fluent Specific Check Items

### Color

- [ ] Uses Segoe UI font family
- [ ] Uses theme color (Brand) to emphasize primary operations
- [ ] Uses neutral colors to build interface skeleton
- [ ] Uses semantic colors to convey status
- [ ] State fill colors use rest/hover/pressed/disabled
- [ ] Supports high contrast mode

### Shape

- [ ] Corner radius uses Fluent tokens (2-8px)
- [ ] Small elements use 2-4px corner radius
- [ ] Large containers use 6-8px corner radius
- [ ] Capsule elements use circular

### Depth

- [ ] Uses depth system (Shadow tokens)
- [ ] Static elements do not use shadows
- [ ] Elevates shadow on hover
- [ ] Modal layers use higher depth values

### Spacing

- [ ] Follows 4px grid system
- [ ] Page margins 16-32px (responsive)
- [ ] Card padding 16px

### Components

- [ ] Button minimum height 24px, recommended 32px
- [ ] Input field minimum height 32px
- [ ] Switch track 40x20px
- [ ] List item height 40px
- [ ] Navigation bar height 48px
- [ ] Menu item height 32px
- [ ] Dialog primary action on the left

### Platform

- [ ] Windows uses NavigationView
- [ ] Supports Acrylic / Mica material effects
- [ ] Touch targets >= 44px, keyboard/mouse >= 32px

---

## Material Specific Check Items

### Color

- [ ] Uses Roboto / Noto font family
- [ ] Uses Material 3 color system (primary/secondary/tertiary/surface)
- [ ] Uses on-* colors to ensure text readability
- [ ] Uses container colors (surfaceContainer) to build hierarchy
- [ ] Supports dynamic color (Android 12+)

### Shape

- [ ] Corner radius uses shape tokens
- [ ] Buttons use full corner radius (capsule shape)
- [ ] Cards use medium (12dp) corner radius
- [ ] Dialogs use extraLarge (28dp) corner radius
- [ ] Input fields use small (8dp) corner radius

### Depth

- [ ] Uses elevation system (Elevation tokens)
- [ ] Cards use 1dp shadow
- [ ] Elevates on hover
- [ ] Lowers elevation when button is pressed
- [ ] Uses Ripple effect for touch feedback

### Spacing

- [ ] Follows 8dp grid system
- [ ] Page margins 16dp
- [ ] Button padding horizontal 24dp
- [ ] List item padding horizontal 16dp

### Components

- [ ] Button minimum height 32dp, recommended 40dp
- [ ] Input field minimum height 56dp (including floating label)
- [ ] Switch track 52x32dp
- [ ] List item height 48dp (single line)
- [ ] Navigation bar height 64-152dp (depending on mode)
- [ ] Bottom navigation height 80dp
- [ ] Dialog primary action on the right

### Platform

- [ ] Android uses bottom navigation
- [ ] Supports Ripple touch feedback
- [ ] Supports dynamic color themes

---

## Component Check Items

### Button

- [ ] Component structure matches specification anatomy (Container + Label + optional Icon)
- [ ] Size is within specification range
- [ ] All states have corresponding styles (Default / Hover / Pressed / Disabled / Focused)
- [ ] Colors use correct tokens
- [ ] Spacing conforms to specification
- [ ] Corner radius conforms to specification
- [ ] Shadow/depth conforms to specification
- [ ] Touch target >= 44pt/px/dp
- [ ] Focus state is clearly visible

### TextField

- [ ] Component structure matches specification (Container + Label + Input + optional Icons)
- [ ] Minimum height conforms to specification
- [ ] All states have corresponding styles
- [ ] Error state has error text
- [ ] Label is associated with input
- [ ] Supports keyboard focus

### Checkbox / RadioButton

- [ ] Box/circle size conforms to specification
- [ ] Selected state is clearly visible
- [ ] Disabled state is clearly distinguishable
- [ ] Label spacing conforms to specification
- [ ] Supports keyboard operation (Space to toggle)

### Switch

- [ ] Track and thumb dimensions conform to specification
- [ ] On/Off state colors are correct
- [ ] Toggle animation is smooth
- [ ] Supports keyboard operation

### Slider

- [ ] Track and thumb dimensions conform to specification
- [ ] Minimum touch area >= 44pt/px/dp
- [ ] Value changes have visual feedback

### ProgressIndicator

- [ ] Size conforms to specification
- [ ] Indeterminate state has animation
- [ ] Colors use correct tokens

### Menu

- [ ] Item height conforms to specification
- [ ] Hover state is clearly visible
- [ ] Sub-menu has arrow indicator
- [ ] Dividers are used correctly

### Dialog

- [ ] Corner radius conforms to specification
- [ ] Padding conforms to specification
- [ ] Button layout conforms to specification
- [ ] Overlay is used correctly
- [ ] Focus management is correct

### Card

- [ ] Corner radius conforms to specification
- [ ] Padding conforms to specification
- [ ] Shadow/depth conforms to specification
- [ ] Hover state has feedback

### List

- [ ] Item height conforms to specification
- [ ] Dividers are used correctly
- [ ] Hover/selected states are clearly visible

### NavigationBar

- [ ] Height conforms to specification
- [ ] Background material conforms to specification
- [ ] Title font conforms to specification

### TabBar

- [ ] Item height conforms to specification
- [ ] Selected indicator is clearly visible
- [ ] Unselected state is not obtrusive

### Tooltip

- [ ] Maximum width conforms to specification
- [ ] Padding conforms to specification
- [ ] Show/hide timing is correct
- [ ] Arrow points to target element

### Badge

- [ ] Dot size conforms to specification
- [ ] Number badge size is correct
- [ ] Colors use correct tokens

### Chip / Tag

- [ ] Height conforms to specification
- [ ] Corner radius conforms to specification
- [ ] Removable state has close button

### DatePicker

- [ ] Cell size conforms to specification
- [ ] Selected state is clearly visible
- [ ] Today marker is correct

### Table

- [ ] Row height conforms to specification
- [ ] Header style is correct
- [ ] Hover/selected states are clearly visible
- [ ] Dividers are used correctly

### Breadcrumb

- [ ] Separators are used correctly
- [ ] Current item and clickable items are clearly distinguishable

### Select

- [ ] Trigger structure matches specification (Trigger + Value + Chevron icon)
- [ ] Dropdown panel size and maximum height conform to specification; scrollable when too long
- [ ] Options have Default / Hover / Selected / Disabled states
- [ ] Selected state has clear visual indicator (highlight/checkmark)
- [ ] Colors use correct tokens, corner radius and spacing conform to specification
- [ ] Supports keyboard operation (up/down selection, Enter to confirm, Esc to close)

### Autocomplete

- [ ] Structure matches specification (Input + suggestion list panel)
- [ ] Real-time filtering on input, matching text can be highlighted
- [ ] Suggestion item Hover / Active / Selected states are clear
- [ ] No match result has an empty state prompt
- [ ] Supports keyboard up/down navigation and Enter to select
- [ ] aria-autocomplete / aria-expanded annotations are correct

### Textarea

- [ ] Structure matches specification (Container + Label + multi-line Input)
- [ ] Minimum height and resizable size conform to specification
- [ ] All states have corresponding styles; error state has error text
- [ ] Character counter (if present) position and style are correct
- [ ] Label is associated with input; supports keyboard focus
- [ ] Color tokens and corner radius conform to specification

### NumberInput

- [ ] Structure matches specification (Input + increment/decrement stepper buttons)
- [ ] Stepper button size and touch target conform to specification
- [ ] Out-of-bounds (min/max) handling is correct; buttons disabled at boundaries
- [ ] All states have corresponding styles
- [ ] Supports keyboard up/down arrow keys to adjust value
- [ ] Color tokens and corner radius conform to specification

### Upload

- [ ] Structure matches specification (drop zone + file list + progress feedback)
- [ ] Drag hover state has clear visual feedback
- [ ] Upload progress / success / failure states are all present
- [ ] File items can be removed; delete button is present
- [ ] Error messages (type/size exceeded) are clear
- [ ] Supports keyboard trigger to select files; aria annotations are correct

### Toast

- [ ] Structure matches specification (Container + icon + text + optional action)
- [ ] Position conforms to specification (top/bottom/corner)
- [ ] Auto-dismiss duration is reasonable; can be manually closed
- [ ] Different semantic types (success/warning/error/info) use correct color tokens
- [ ] Entry/exit animations are smooth; respects Reduced Motion
- [ ] Uses aria-live to notify screen readers

### Notification

- [ ] Structure matches specification (title + description + icon + action + close)
- [ ] Stacking/grouping display logic is correct
- [ ] Each semantic type uses correct color tokens
- [ ] Can be manually closed; auto-dismiss duration is configurable
- [ ] Corner radius, spacing, shadow conform to specification
- [ ] Uses aria-live for accessibility notifications

### Alert / Banner

- [ ] Structure matches specification (icon + text + optional action/close)
- [ ] Different semantic types (info/success/warning/error) use correct color tokens
- [ ] Dismissible scenarios have a close button
- [ ] Padding and corner radius conform to specification
- [ ] Uses role="alert" / aria-live annotations
- [ ] Text contrast meets accessibility requirements

### Skeleton

- [ ] Placeholder shapes are consistent with actual content layout
- [ ] Dimensions (line height/circle/rectangle) conform to content specification
- [ ] Loading animation (shimmer/pulse) is smooth
- [ ] Respects Reduced Motion preference; can degrade to static
- [ ] Colors use neutral placeholder tokens
- [ ] Loading state marked with aria-busy / aria-hidden

### Drawer / Sidebar

- [ ] Structure matches specification (container + navigation items + optional header/footer)
- [ ] Expand/collapse width and animation conform to specification
- [ ] Navigation item Hover / Active / Selected states are all present
- [ ] Modal drawer has overlay; Esc can close
- [ ] Focus management is correct (focus enters on open, returns on close)
- [ ] Color tokens, spacing, corner radius conform to specification

### Pagination

- [ ] Structure matches specification (page numbers + previous/next + optional jump)
- [ ] Current page highlight is clearly distinguishable
- [ ] First/last page boundary buttons are correctly disabled
- [ ] Page item size and touch target conform to specification
- [ ] Supports keyboard navigation and focus state
- [ ] Color tokens and corner radius conform to specification

### Stepper

- [ ] Structure matches specification (step nodes + connector lines + labels)
- [ ] Completed/Current/Incomplete states are visually distinct
- [ ] Node size and connector line style conform to specification
- [ ] Current step has clear marking
- [ ] Colors use correct tokens
- [ ] Step labels are readable by screen readers; current step marked with aria-current

### Sheet / ActionSheet

- [ ] Structure matches specification (container + drag handle + action items)
- [ ] Slide-in animation from bottom is smooth
- [ ] Action item grouping and destructive action styles are correct
- [ ] Has overlay; tap overlay or swipe down can dismiss
- [ ] Corner radius (top) and spacing conform to specification
- [ ] Focus management and Esc close are correct

### Avatar

- [ ] Size tiers conform to specification (e.g., xs/sm/md/lg/xl)
- [ ] Shape (circle/rounded square) conforms to specification
- [ ] Without image, fallback shows initials or placeholder icon
- [ ] Status badge (online/offline) position is correct
- [ ] Color tokens and border conform to specification
- [ ] Image has alt text; decorative ones use aria-hidden

### Accordion

- [ ] Structure matches specification (Header + expand icon + Content)
- [ ] Expand/collapse animation is smooth
- [ ] Expand icon direction changes with state
- [ ] Single/multi-open mode logic is correct
- [ ] Spacing and dividers conform to specification
- [ ] Supports keyboard operation; aria-expanded is annotated

### Carousel

- [ ] Structure matches specification (carousel container + indicator dots + optional arrows)
- [ ] Current page indicator dot is clearly highlighted
- [ ] Transition animation is smooth; supports auto-play with pause
- [ ] Arrow/indicator touch targets conform to specification
- [ ] Respects Reduced Motion; can disable auto-play
- [ ] Supports keyboard left/right navigation; aria annotations are correct

### Timeline

- [ ] Structure matches specification (nodes + connector lines + content)
- [ ] Node size and connector line style conform to specification
- [ ] Different state node colors use correct tokens
- [ ] Time/content text semantic hierarchy is correct
- [ ] Spacing conforms to specification
- [ ] List semantics are readable by screen readers

### Tree

- [ ] Structure matches specification (nodes + expand icon + indentation levels)
- [ ] Expand/collapse state and icon are correct
- [ ] Selected/hover states are clearly visible
- [ ] Indentation and node height conform to specification
- [ ] Supports keyboard up/down navigation and expand/collapse
- [ ] Annotated with role="tree" / aria-expanded / aria-selected

### Divider

- [ ] Supports horizontal/vertical directions
- [ ] Line width and color use correct neutral tokens
- [ ] Text divider text centering/alignment is correct
- [ ] Spacing conforms to specification
- [ ] Decorative dividers annotated with aria-hidden or role="separator"

### Grid / Layout

- [ ] Grid column count and breakpoints conform to specification
- [ ] Column spacing (gutter) conforms to specification
- [ ] Responsive adaptation to different screen sizes
- [ ] Alignment (start/center/end) is correct
- [ ] Spacing uses grid system tokens

### Space / Stack

- [ ] Spacing size tiers conform to specification grid system
- [ ] Supports horizontal/vertical directions
- [ ] Child alignment is correct
- [ ] Auto-wrap behavior is correct
- [ ] Spacing uses correct tokens

### AspectRatio

- [ ] Ratio constraints (e.g., 16:9 / 1:1) work correctly
- [ ] Content clipping/fill mode conforms to specification
- [ ] Maintains ratio on responsive layouts
- [ ] Corner radius (if present) conforms to specification

### Popover

- [ ] Structure matches specification (trigger + floating panel + optional arrow)
- [ ] Panel positioning and arrow pointing to trigger element are correct
- [ ] Padding, corner radius, shadow conform to specification
- [ ] Click outside or Esc can close
- [ ] Focus management is correct
- [ ] Color tokens are correct; aria-related attributes are annotated

### Modal

- [ ] Structure matches specification (overlay + container + title + content + actions)
- [ ] Corner radius and padding conform to specification
- [ ] Focus trap works (Tab cycles within dialog)
- [ ] Esc close, click overlay close logic is correct
- [ ] Overlay color and opacity conform to specification
- [ ] Annotated with aria-modal; focus enters on open, returns on close

### FAB

- [ ] Shape (circle/rounded) and size tiers conform to specification
- [ ] Icon is centered; touch target >= 44pt/px/dp
- [ ] Shadow/elevation conforms to specification
- [ ] Positioning (bottom-right, etc.) and safe area conform to specification
- [ ] Hover / Pressed states have feedback
- [ ] Color uses emphasis color token; has aria-label

### SearchBar

- [ ] Structure matches specification (search icon + Input + optional clear button)
- [ ] Height and corner radius conform to specification
- [ ] Clear button appears when there is content
- [ ] Focus / Active states are clear
- [ ] Supports keyboard submit and Esc clear
- [ ] Color tokens are correct; annotated with role="search"

### Rating

- [ ] Icon (star) size and count conform to specification
- [ ] Selected/unselected/half states are visually clear
- [ ] Hover preview feedback is correct
- [ ] Colors use correct tokens
- [ ] Supports keyboard left/right adjustment of rating
- [ ] Annotated with aria-label / current value is readable

### ColorPicker

- [ ] Structure matches specification (color swatch preview + color picker panel)
- [ ] Hue/saturation/brightness selection area interaction is correct
- [ ] Currently selected color has clear marking
- [ ] Input (HEX/RGB) syncs with panel
- [ ] Corner radius, spacing conform to specification
- [ ] Supports keyboard operation; color values are readable by screen readers

### Calendar

- [ ] Cell size conforms to specification
- [ ] Selected/today/range states are clearly visible
- [ ] Disabled dates are visually clear and distinguishable
- [ ] Month switching interaction is correct
- [ ] Supports keyboard arrow key navigation of dates
- [ ] Color tokens are correct; aria-related attributes are annotated

---

## Validation Report Template

```markdown
# UI Design Specification Validation Report

## Basic Information
- **Specification**: HIG / Fluent / Material / All
- **Inspection Date**: YYYY-MM-DD
- **Inspector**: Agent

## Statistics
- **Total Check Items**: XXX
- **Passed**: XXX
- **Warnings**: XXX
- **Errors**: XXX
- **Pass Rate**: XX%

## Issue List

### Errors
1. **[Component Name] - [Issue Description]**
   - Location: [File Path:Line Number]
   - Expected: [Specification Requirement]
   - Actual: [Current Implementation]
   - Suggestion: [Modification Plan]

### Warnings
1. **[Component Name] - [Issue Description]**
   - Suggestion: [Optimization Plan]

## Summary
[Overall Evaluation and Modification Suggestions]
```
