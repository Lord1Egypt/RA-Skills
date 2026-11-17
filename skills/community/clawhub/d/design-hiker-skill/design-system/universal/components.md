# Universal Design System — Component Specs

Default specs for all common components. Every value references a token from `tokens.css`.
Use these specs exactly during L2 generation — do not invent different dimensions.

---

## Button

### Dimensions
| Variant | Height | H-Padding | Min-Width |
|---------|--------|-----------|-----------|
| Default (mobile) | `var(--btn-height-mobile)` = 44px | `var(--spacing-md)` | 80px |
| Default (desktop) | `var(--btn-height-desktop)` = 40px | `var(--spacing-md)` | 80px |
| Small | `var(--btn-height-sm)` = 32px | `var(--spacing-sm)` | 60px |

### Variants
```
primary:   bg var(--color-primary)          text var(--color-text-inverse)
           hover: bg var(--color-primary-dark)
           active: bg var(--color-primary-darker)

secondary: bg transparent                   text var(--color-primary)
           border: 1.5px solid var(--color-primary)
           hover: bg var(--color-primary-surface)

ghost:     bg transparent                   text var(--color-primary)
           hover: bg var(--color-primary-surface)

danger:    bg var(--color-danger)           text var(--color-text-inverse)
           hover: bg #CC0000

text:      bg transparent                   text var(--color-text-secondary)
           hover: text var(--color-text-primary)
```

### States
```
disabled:  opacity 0.4, cursor not-allowed, pointer-events none
loading:   show 16px spinner left of text, pointer-events none
```

### Style
```
border-radius: var(--radius-md)
font-size:     var(--font-size-body)
font-weight:   var(--font-weight-semibold)
transition:    all var(--duration-fast) var(--easing-default)
```

---

## Input / TextField

### Dimensions
| Variant | Height | H-Padding | V-Padding |
|---------|--------|-----------|-----------|
| Default (mobile) | `var(--input-height-mobile)` = 44px | `var(--spacing-md)` | 0 |
| Default (desktop) | `var(--input-height-desktop)` = 40px | `var(--spacing-md)` | 0 |

### States
```
default:  border 1px solid var(--color-border)
          bg var(--color-surface)
          text var(--color-text-primary)
          placeholder var(--color-text-disabled)

focus:    border 1.5px solid var(--color-border-focus)
          bg var(--color-surface)
          box-shadow 0 0 0 3px var(--color-primary-surface)

error:    border 1.5px solid var(--color-danger)
          box-shadow 0 0 0 3px var(--color-danger-surface)

disabled: bg var(--color-disabled-bg)
          border 1px solid var(--color-border)
          text var(--color-disabled-text), cursor not-allowed
```

### Style
```
border-radius: var(--radius-md)
font-size:     var(--font-size-body)
font-family:   var(--font-family)
transition:    border var(--duration-fast), box-shadow var(--duration-fast)
```

### Label (above input)
```
font-size:   var(--font-size-body-sm)
font-weight: var(--font-weight-medium)
color:       var(--color-text-primary)
margin-bottom: var(--spacing-xs)
```

### Helper / Error text (below input)
```
font-size:  var(--font-size-caption)
color:      var(--color-text-secondary)   [helper]
color:      var(--color-danger)           [error]
margin-top: var(--spacing-xs)
```

---

## Card

```
background:    var(--color-surface)
border:        1px solid var(--color-border)
border-radius: var(--radius-lg)
box-shadow:    var(--shadow-card)
padding:       var(--spacing-md)

hover (interactive card):
  box-shadow:    var(--shadow-md)
  border-color:  var(--color-border-strong)
  transition:    all var(--duration-fast)
```

---

## Navigation Bar (Top)

```
height:         var(--navbar-height-mobile) on mobile
                var(--navbar-height-desktop) on desktop
background:     var(--color-surface)
border-bottom:  1px solid var(--color-border)
padding:        0 var(--spacing-md)

title:
  font-size:    var(--font-size-h4)
  font-weight:  var(--font-weight-semibold)
  color:        var(--color-text-primary)

back/action icons:
  touch target: 44×44px minimum
  color:        var(--color-primary)
  font-size:    var(--font-size-h3)
```

---

## Bottom Navigation (Mobile)

```
height:       var(--bottom-nav-height) + env(safe-area-inset-bottom)
background:   var(--color-surface)
border-top:   1px solid var(--color-border)

tab item:
  min-width:  44px (touch target)
  icon:       24×24px
  label:      var(--font-size-caption) / var(--font-weight-medium)

active tab:
  icon-color:  var(--color-primary)
  label-color: var(--color-primary)

inactive tab:
  icon-color:  var(--color-text-tertiary)
  label-color: var(--color-text-tertiary)
```

---

## Tab Bar

```
height:        var(--tab-bar-height)
border-bottom: 1px solid var(--color-border)

tab item:
  padding:     0 var(--spacing-md)
  font-size:   var(--font-size-body-sm)
  font-weight: var(--font-weight-medium)
  color:       var(--color-text-secondary)
  min-width:   44px

active tab:
  color:            var(--color-primary)
  border-bottom:    2px solid var(--color-primary)
  font-weight:      var(--font-weight-semibold)
```

---

## Badge / Tag

```
height:        20px
padding:       0 var(--spacing-xs)
border-radius: var(--radius-sm)
font-size:     var(--font-size-caption)
font-weight:   var(--font-weight-medium)
line-height:   20px

primary:  bg var(--color-primary)         text white
success:  bg var(--color-success-surface) text var(--color-success)
warning:  bg var(--color-warning-surface) text var(--color-warning)
danger:   bg var(--color-danger-surface)  text var(--color-danger)
neutral:  bg var(--color-surface-3)       text var(--color-text-secondary)
outline:  bg transparent, border 1px solid var(--color-border)
          text var(--color-text-secondary)
```

---

## Toggle / Switch

```
width:         36px
height:        22px
border-radius: var(--radius-full)

on:   bg var(--color-success)
off:  bg var(--color-border-strong)

thumb:
  size:        18×18px
  bg:          white
  border-radius: 50%
  shadow:      0 1px 3px rgba(0,0,0,0.25)
  transition:  transform var(--duration-fast) var(--easing-spring)

on position:  thumb right (translateX 14px)
off position: thumb left
```

---

## Checkbox

```
size:          18×18px
border-radius: var(--radius-sm)
border:        2px solid var(--color-border-strong)

checked:
  bg:    var(--color-primary)
  border: none
  checkmark: white, 8×5px, 2px stroke

indeterminate:
  bg:    var(--color-primary)
  dash:  white horizontal line

disabled:
  bg:    var(--color-disabled-bg)
  opacity: 0.5
```

---

## Modal / Dialog

```
overlay:
  bg:     var(--color-overlay)
  z-index: var(--z-modal)

container:
  background:    var(--color-surface)
  border-radius: var(--radius-xl)
  box-shadow:    var(--shadow-modal)
  padding:       var(--spacing-lg)
  max-width:     480px (desktop) / 90vw (mobile)
  animation:     scale(0.95)→scale(1) var(--duration-normal) var(--easing-spring)

title:
  font-size:   var(--font-size-h3)
  font-weight: var(--font-weight-bold)
  margin-bottom: var(--spacing-sm)

body:
  font-size:  var(--font-size-body)
  color:      var(--color-text-secondary)
  line-height: var(--line-height-relaxed)

actions:
  margin-top: var(--spacing-lg)
  gap:        var(--spacing-sm)
  justify:    flex-end
```

---

## Toast / Snackbar

```
position:      fixed, bottom 24px, centered
max-width:     min(400px, 90vw)
padding:       var(--spacing-sm) var(--spacing-md)
border-radius: var(--radius-lg)
background:    rgba(28,28,30,0.90)  [light mode]
               rgba(58,58,60,0.95)  [dark mode]
backdrop-filter: blur(20px)
color:         white
font-size:     var(--font-size-body-sm)
font-weight:   var(--font-weight-medium)
box-shadow:    var(--shadow-lg)
z-index:       var(--z-toast)

animation in:  translateY(10px)→0, opacity 0→1
duration:      var(--duration-normal)
auto-dismiss:  2.5–3s
```

---

## List Item

```
padding:        var(--spacing-sm) var(--spacing-md)
min-height:     var(--btn-height-mobile)  [44px, touch target]
border-bottom:  1px solid var(--color-border)
background:     var(--color-surface)

hover:          bg var(--color-hover-bg)
active:         bg var(--color-active-bg)

primary text:
  font-size:   var(--font-size-body)
  color:       var(--color-text-primary)

secondary text:
  font-size:   var(--font-size-body-sm)
  color:       var(--color-text-secondary)
```

---

## Section Header / Page Layout

```
Mobile (375px):
  horizontal padding:  var(--spacing-md)  [16px each side]
  max content width:   343px
  section vertical gap: var(--spacing-xl)  [32px]
  component gap:       var(--spacing-md)   [16px]

Desktop (1440px):
  page max-width:      1200px, centered
  horizontal padding:  var(--spacing-xl)   [32px each side]
  section vertical gap: var(--spacing-2xl) [48px]
  component gap:       var(--spacing-lg)   [24px]
```

---

## Select / Dropdown

```
trigger（触发器，外观同 Input）:
  height:        var(--input-height-mobile) / var(--input-height-desktop)
  padding:       0 var(--spacing-md)
  border:        1px solid var(--color-border)
  border-radius: var(--radius-md)
  background:    var(--color-surface)
  text:          var(--font-size-body) / var(--color-text-primary)
  arrow icon:    var(--icon-sm) / var(--color-text-tertiary)
                 rotate 180° when open

  states:
    default:     border var(--color-border)
    open:        border 1.5px solid var(--color-border-focus)
                 box-shadow 0 0 0 3px var(--color-primary-surface)
    disabled:    bg var(--color-disabled-bg), text var(--color-disabled-text)

dropdown panel:
  background:    var(--color-surface)
  border:        1px solid var(--color-border)
  border-radius: var(--radius-md)
  box-shadow:    var(--shadow-popover)
  z-index:       var(--z-dropdown)
  max-height:    240px, overflow-y scroll
  padding:       var(--spacing-xs) 0

option item:
  height:        var(--btn-height-mobile) = 44px  [touch target]
  padding:       0 var(--spacing-md)
  font-size:     var(--font-size-body)
  color:         var(--color-text-primary)

  hover:         bg var(--color-hover-bg)
  selected:      bg var(--color-selected-bg)
                 text var(--color-primary)
                 checkmark icon (right, var(--icon-sm))
  disabled:      text var(--color-disabled-text), cursor not-allowed
```

---

## Radio Button

```
radio circle:
  size:          18×18px
  border:        2px solid var(--color-border-strong)
  border-radius: var(--radius-full)

  selected:
    border:      2px solid var(--color-primary)
    inner dot:   8×8px circle, bg var(--color-primary), centered

  disabled:
    border:      2px solid var(--color-border)
    bg:          var(--color-disabled-bg)
    cursor:      not-allowed

label:
  font-size:     var(--font-size-body)
  color:         var(--color-text-primary)
  margin-left:   var(--spacing-sm)

radio group item (touch target):
  min-height:    var(--btn-height-mobile) = 44px
  display:       flex, align-items center
  gap:           var(--spacing-sm)

group gap:       var(--spacing-sm) between items (vertical)
                 var(--spacing-md) between items (horizontal inline)
```

---

## Search Bar

```
container:
  height:        40px (mobile) / 36px (desktop)
  background:    var(--color-surface-2)
  border:        1px solid transparent
  border-radius: var(--radius-full)  [pill shape]
  padding:       0 var(--spacing-sm) 0 var(--spacing-md)
  display:       flex, align-items center, gap var(--spacing-xs)

search icon (left):
  size:          var(--icon-md) = 20px
  color:         var(--color-text-tertiary)

input:
  font-size:     var(--font-size-body-sm)
  color:         var(--color-text-primary)
  placeholder:   var(--color-text-disabled)
  border:        none, background none, flex 1

clear button (right, shows when value non-empty):
  size:          var(--icon-sm) = 16px
  color:         var(--color-text-tertiary)
  touch target:  28×28px

states:
  default:   bg var(--color-surface-2), border transparent
  focused:   bg var(--color-surface), border 1px solid var(--color-border-focus)
             box-shadow 0 0 0 3px var(--color-primary-surface)

cancel button (appears on focus, mobile):
  font-size:   var(--font-size-body-sm)
  color:       var(--color-primary)
  margin-left: var(--spacing-sm)
  touch target: 44px height
```

---

## Avatar

```
shape:         circle (border-radius: var(--radius-full))

sizes:
  xs:   24×24px   font-size var(--font-size-caption)    [comment count]
  sm:   32×32px   font-size var(--font-size-body-sm)    [list item]
  md:   40×40px   font-size var(--font-size-body)       [default]
  lg:   48×48px   font-size var(--font-size-h4)         [profile header]
  xl:   64×64px   font-size var(--font-size-h2)         [profile page]
  2xl:  80×80px   font-size var(--font-size-h1)         [detail page hero]

fallback (no image):
  bg:            var(--color-primary-surface)
  text:          var(--color-primary) / initials (1–2 chars)

image:
  object-fit:    cover
  border-radius: inherit

border (optional):
  border:        2px solid var(--color-surface)  [on colored bg]

badge (status indicator, bottom-right):
  size:          10×10px (sm/md), 12×12px (lg+)
  border-radius: var(--radius-full)
  border:        2px solid var(--color-surface)
  online:        bg var(--color-success)
  offline:       bg var(--color-text-tertiary)
  busy:          bg var(--color-warning)

group (stacked avatars):
  overlap:       -8px margin-left (md size)
  max show:      4–5, remainder shown as "+N" avatar
```

---

## Progress Bar

### Linear Progress Bar
```
track:
  height:        4px (default) / 8px (thick)
  background:    var(--color-surface-3)
  border-radius: var(--radius-full)

fill:
  background:    var(--color-primary)
  border-radius: var(--radius-full)
  transition:    width var(--duration-normal) var(--easing-default)

variants:
  success:   fill bg var(--color-success)
  warning:   fill bg var(--color-warning)
  danger:    fill bg var(--color-danger)

label (optional, right of bar):
  font-size:   var(--font-size-caption)
  color:       var(--color-text-secondary)
  font-family: var(--font-family-mono)
```

### Circular Progress Ring
```
size:          40px (default) / 24px (sm) / 64px (lg)
stroke-width:  4px (default) / 3px (sm) / 6px (lg)
track color:   var(--color-surface-3)
fill color:    var(--color-primary)
rotation:      starts at -90deg (top)

center label:
  font-size:   var(--font-size-caption) / var(--font-weight-semibold)
  color:       var(--color-text-primary)

loading spinner (indeterminate):
  animation:   rotate 1s var(--easing-default) infinite
  arc:         ~270deg visible, rest transparent
```

---

## Skeleton Loader

```
base:
  background:    var(--color-surface-3)
  border-radius: var(--radius-sm)
  animation:     shimmer 1.5s ease-in-out infinite

shimmer effect:
  background:    linear-gradient(
                   90deg,
                   var(--color-surface-3) 25%,
                   var(--color-surface-2) 50%,
                   var(--color-surface-3) 75%
                 )
  background-size: 200% 100%
  animation:     shimmer-slide 1.5s infinite

common skeleton shapes:
  text line:     height 14px, width varies (100% / 80% / 60%), radius var(--radius-sm)
  title line:    height 20px, width 60%, radius var(--radius-sm)
  avatar:        circle shape (same size as Avatar variants)
  image block:   height varies, width 100%, radius var(--radius-md)
  button:        height var(--btn-height-mobile), width 80px, radius var(--radius-md)

gap between skeleton lines: var(--spacing-sm)

dark mode:
  background:    var(--color-surface-2)
  shimmer mid:   var(--color-surface-3)
```

---

## Stepper / Steps

### Horizontal Steps (desktop / onboarding)
```
step indicator:
  size:          32×32px circle
  border-radius: var(--radius-full)
  font-size:     var(--font-size-body-sm) / var(--font-weight-semibold)

  completed:   bg var(--color-primary)      text var(--color-text-inverse)
               icon: checkmark (var(--icon-sm), white)
  current:     bg var(--color-primary)      text var(--color-text-inverse)
               ring: 3px solid var(--color-primary-surface) outside
  upcoming:    bg var(--color-surface-3)    text var(--color-text-tertiary)
  error:       bg var(--color-danger)       text var(--color-text-inverse)

connector line:
  height:        2px
  completed:     bg var(--color-primary)
  upcoming:      bg var(--color-border)
  flex: 1 (fills space between steps)

step label (below indicator):
  font-size:     var(--font-size-caption)
  completed:     color var(--color-text-secondary)
  current:       color var(--color-primary) / var(--font-weight-semibold)
  upcoming:      color var(--color-text-tertiary)
```

### Vertical Steps (mobile / process tracking)
```
indicator:       same as above, size 24×24px (compact)
connector:       width 2px, height auto (fills gap between steps)
                 left-aligned with indicator center

content area (right of indicator):
  title:         var(--font-size-body) / var(--font-weight-semibold)
  subtitle:      var(--font-size-body-sm) / var(--color-text-secondary)
  padding-left:  var(--spacing-md) from indicator
  padding-bottom: var(--spacing-lg) (gap to next step)
```

---

## Bottom Sheet

```
overlay:
  bg:            var(--color-overlay)
  z-index:       var(--z-overlay)
  tap to dismiss: yes

sheet container:
  position:      fixed, bottom 0, left 0, right 0
  background:    var(--color-surface)
  border-radius: var(--radius-xl) var(--radius-xl) 0 0  [top corners only]
  box-shadow:    var(--shadow-modal)
  z-index:       var(--z-modal)
  padding-bottom: env(safe-area-inset-bottom)

drag handle (top center):
  width:         36px, height 4px
  background:    var(--color-border-strong)
  border-radius: var(--radius-full)
  margin:        var(--spacing-sm) auto var(--spacing-md)

header (optional):
  padding:       0 var(--spacing-md) var(--spacing-md)
  title:         var(--font-size-h3) / var(--font-weight-bold)
  close button:  top-right, var(--icon-lg), var(--color-text-secondary)

content area:
  padding:       0 var(--spacing-md)
  max-height:    80vh (snap point)
  overflow-y:    auto

height variants:
  compact:   content height + safe area (no scroll, max ~40vh)
  half:      ~50vh, scrollable content
  full:      ~90vh, scrollable content, treats like modal

animation:
  enter:     translateY(100%) → translateY(0)
             duration var(--duration-slow), easing var(--easing-enter)
  exit:      translateY(0) → translateY(100%)
             duration var(--duration-normal), easing var(--easing-exit)
```
