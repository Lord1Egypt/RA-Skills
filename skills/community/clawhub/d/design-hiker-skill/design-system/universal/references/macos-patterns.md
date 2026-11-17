# macOS Native UI Patterns — Reference Specifications

Canonical specs for macOS applications. These are the "ground truth" for what macOS
native design looks and feels like. Reference these before generating any macOS desktop design.

Sources: Apple HIG, macOS Sonoma/Ventura measurements, high-quality third-party apps
(Linear, Notion, Bear, Things, Fantastical).

---

## Window Chrome

```
Titlebar:        height 28–36px (most apps: 36px, toolbar-integrated: 52px)
Traffic lights:  12px diameter, 6px gap, 14px from left edge
Window title:    12.5–13px, semibold, centred, var(--color-text-tertiary)
Window border:   1px solid rgba(0,0,0,0.18) + 1px inset rgba(255,255,255,0.06)
Window radius:   10–12px
Window shadow:   layered: 0 0 0 1px rgba(0,0,0,0.18), 0 2px 6px rgba(0,0,0,0.12),
                          0 16px 48px rgba(0,0,0,0.22)
```

**Do:** match the compact 36px titlebar for utility/tool apps
**Do NOT:** use a 52px titlebar unless it contains a search bar (like Finder)

---

## Toolbar

```
Height:          48–52px (standard), 38px (compact, single-row controls)
Button height:   26–28px (standard), 22px (compact)
Button padding:  0 10px
Button radius:   5–6px
Segmented ctrl:  same 26px height, 2px inner padding, 1px outer border
Divider:         1px | rgba(0,0,0,0.12) between button groups
Search field:    height 26px, radius 6px (pill only in Spotlight-style)
```

**Typography in toolbar:**
- Section title: 15px / bold / –0.2px tracking
- Subtitle/count: 12px / regular / tertiary color

**Do:** toolbar buttons have subtle bg on hover (`rgba(0,0,0,0.06)`)
**Do NOT:** use 40px+ buttons in toolbars (mobile size)

---

## Sidebar Navigation

```
Sidebar width:   200–240px (standard), 180px (compact)
Section label:   10–11px / bold / uppercase / 0.06em tracking / tertiary
Nav item height: 26–30px
Nav item padding: 5–7px vertical, 12–16px horizontal
Nav item radius: 5–6px
Nav item font:   13px / medium (default), semibold (selected)
Icon size:       14–16px / currentColor (follows text color)
Gap between sections: 8px
```

**Selected state:**
- Background: `rgba(0,102,255,0.08)` to `rgba(0,102,255,0.12)`
- Text + icon: `var(--color-primary)`
- No border or shadow — background alone is enough

**Badge in nav:**
- Unselected: gray pill, same treatment for all badge types
- Selected: white/inverted, subordinate to selection bg
- Size: 17×17px for single digit, pill for 2+ digits (NOT oval)

---

## List / Table View

```
List border:     0.5px / var(--color-border) — not 1px
Row height:      34–40px (compact), 44px (comfortable)
Row separator:   0.5px / rgba(0,0,0,0.07) — nearly invisible
Row hover:       rgba(0,0,0,0.04) background change
Row padding:     0 16px horizontal
Header row:      28px height, 10.5px uppercase labels, surface-2 bg
Header separator: 0.5px / rgba(0,0,0,0.12) (slightly stronger than row separator)
```

**Key macOS list feel:**
- Separators should DISAPPEAR — 0.5px rgba, not 1px solid
- Row hover is subtle — barely changes, but felt
- No rounded corners on rows — only on the table container

---

## Cards

```
Card border:     0.5px / var(--color-border)  ← NOT 1px
Card radius:     8–12px (app-dependent, pick one and be consistent)
Card shadow:     0 1px 2px rgba(0,0,0,0.04) — almost nothing
Card bg:         var(--color-surface) — pure white/dark
Card padding:    12–16px
Card hover:      border darkens slightly + subtle shadow increase
                 NO transform translateY (web pattern, not native)
```

**macOS card feel:** cards don't "lift up" on hover — they just subtly emphasize.
Hover transform (`translateY(-1px)`) is a web/Material pattern, NOT macOS.

---

## Settings / Preferences

```
Page layout:     left nav (160–200px) | right content (flex 1)
Left nav item:   28–32px height, 13px / medium
Selected nav:    primary-surface bg + primary text (same as sidebar)
Section title:   11px / bold / uppercase / 0.06em tracking / tertiary
Row height:      36–44px (match content)
Row separator:   0.5px rgba (same as list)
Toggle size:     32×18px (NOT 36×22px which is iOS)
Toggle thumb:    14px, left:2px default (OFF), translateX(+14px) for ON
Select control:  compact, 24–28px height, native-look
```

---

## Spacing Rhythm (macOS context)

```
Within a component:  4px (xs) or 8px (sm)
Between components:  16px (md)
Between sections:    24–32px (lg/xl)
Page edge margin:    16–20px
Sidebar internal:    8px top padding, 5px side for nav items
```

**macOS density is HIGHER than mobile.** A row that would be 56px on mobile
is 36–40px on macOS. The same padding that's 16px on mobile is 12px on macOS.

---

## Typography Scale for macOS Apps

```
Window title:        13px / semibold
Toolbar section:     15–17px / bold / –0.3px tracking
Toolbar sub/count:   12px / regular / tertiary
Sidebar label (all): 11px / bold / uppercase
Sidebar item:        13px / medium → semibold (selected)
List primary:        13px / semibold
List secondary:      11–12px / regular / tertiary
Badge:               10px / bold
Caption/meta:        11px / regular / tertiary
```

**Note:** macOS uses SMALLER type than web. Body text in macOS apps is 13px, not 16px.
16px body is for long-form reading content, not compact UI.

---

## Color Usage in macOS

```
Primary accent:     used sparingly (selected state, primary action, links)
                    NOT for headings, NOT for decorative elements
Text hierarchy:     primary (#111 / #F2F2F7) → secondary (#666 / #C7C7CC) →
                    tertiary (#999 / #8E8E93) → disabled (#AAA / #636366)
Backgrounds:        window surface → sidebar surface-2 → hover surface-3
                    each step is barely different — hierarchy is felt, not seen
Separator:          rgba(0,0,0,0.07) light / rgba(0,0,0,0.12) strong
                    NEVER a hex color for separators
```

---

## Mobile Phone Standards

**Default: iPhone 16 (393 × 852pt)**

Unless the user specifies a different device, always use these exact dimensions.
Do NOT invent arbitrary heights (667, 780, 812px) — pick from the table below.

```
Device              Width   Height  Corner  Status bar  Bottom safe
─────────────────────────────────────────────────────────────────────
iPhone 16           390     844     47px    54px        34px
iPhone 16 Plus      430     932     55px    54px        34px
iPhone 16 Pro       402     874     48px    54px        34px
iPhone 16 Pro Max   440     956     55px    54px        34px
iPhone 15 / 15 Plus 393     852     47px    54px        34px  ← USE THIS AS DEFAULT
iPhone SE (3rd)     375     667     39px    20px         0px  ← compact / legacy
─────────────────────────────────────────────────────────────────────
```

**Default to iPhone 15 size (393 × 852) unless:**
- User says "iPhone SE" / "compact" → use 375 × 667
- User says "Plus/Max/Pro Max" → use the wider size
- User specifies exact dimensions

### Key measurements (iPhone 15/16 default)

```css
.phone {
  width: 393px;
  height: 852px;           /* NOT 667px, 812px, or other arbitrary values */
  border-radius: 47px;     /* matches real iPhone corner curve */
  overflow: hidden;
}

.status-bar {
  height: 54px;            /* includes Dynamic Island area */
  /* Time + icons sit at bottom of this area */
  padding: 14px 24px 0;
  display: flex; align-items: flex-end; justify-content: space-between;
}

.home-indicator-area {
  height: 34px;            /* bottom safe area */
  flex-shrink: 0;
}
```

### Dynamic Island placeholder (optional)

```css
.dynamic-island {
  width: 120px; height: 35px;
  background: #000;
  border-radius: 20px;
  position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
}
```

**Rule:** Phone dimensions are platform constants — NEVER tokenize them.
Same as traffic light dots: use exact pixel values, not `var(--spacing-*)`.
