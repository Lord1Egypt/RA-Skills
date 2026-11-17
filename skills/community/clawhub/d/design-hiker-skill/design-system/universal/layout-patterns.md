# Layout Patterns

Page-level skeleton templates. Start with the **Decision Tree** to pick the right
pattern, then apply the corresponding skeleton and token constraints.

Sources: Material Design 3 Canonical Layouts, Apple HIG, Nielsen Norman Group.

---

## Decision Tree

```
What does this screen primarily do?
│
├─ Shows one isolated moment (login, splash, empty, success)?
│   └─► SINGLE SCREEN
│
├─ Shows a scrollable list where each item navigates somewhere?
│   ├─ Need to show list + detail side-by-side on wider screens?
│   │   └─► MASTER-DETAIL
│   └─ Item opens a new full page?
│       └─► LIST VIEW
│
├─ Shows one item in full detail?
│   └─► DETAIL VIEW
│
├─ Collects user input (form, settings, config)?
│   └─► SETTINGS / FORM
│
├─ Aggregates metrics / content from multiple sources (home, dashboard)?
│   └─► DASHBOARD / OVERVIEW
│
├─ Organises same-level content into tabs or categories?
│   └─► TABBED CONTENT
│
└─ Guides users through a sequential process (register, checkout)?
    └─► WIZARD / STEPPER
```

---

## 1. Single Screen

**Use when:** one isolated task per screen — splash, login, onboarding step, success
confirmation, permission request, empty state.

```
┌─────────────────────────────┐
│  [Status bar]               │
│                             │
│                             │
│   [Illustration / Icon]     │  var(--icon-2xl) or full-width
│                             │
│   Headline                  │  var(--font-size-h1) / bold / centred
│   Supporting text           │  var(--font-size-body) / centred / 2 lines max
│                             │
│   [Primary CTA]             │  full-width button, var(--btn-height-mobile)
│   [Secondary link]          │  var(--font-size-body-sm) / var(--color-primary)
│                             │
│  [Home indicator]           │
└─────────────────────────────┘
```

**Token constraints**
```
Page padding:     var(--spacing-md) horizontal
Content spacing:  var(--spacing-xl) between icon and headline
                  var(--spacing-sm) between headline and body
                  var(--spacing-2xl) between body and CTA
CTA margin-bottom: var(--spacing-md) + env(safe-area-inset-bottom)
Background:       var(--color-background) or branded full-bleed bg
```

**Variants**
```
Login / Auth:   form fields replace illustration; show social login below primary CTA
Permission:     system-style icon (large, var(--icon-2xl)), concise benefit statement
Success / Done: checkmark illustration, auto-advance after 2–3s or manual dismiss
```

---

## 2. List View

**Use when:** homogeneous collection of items — product catalogue, orders, messages,
contacts, search results.

```
┌─────────────────────────────┐
│  Navbar (fixed)             │  var(--navbar-height)
│  ─────────────────────────  │
│  SearchBar (optional sticky)│
│  FilterBar / TabBar (sticky)│
│  ──────────────────────────  │  ← sticky divider / shadow
│                             │
│  Section header (sticky)    │  height 48px, bg var(--color-surface-2)
│  ListItem                   │  1-line 56px / 2-line 72px / 3-line 88px
│  ListItem                   │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  divider (optional)
│  ListItem                   │
│  ...                        │
│  Load More / Skeleton       │
│                             │
│  BottomNav (fixed)          │  var(--bottom-nav-height)
└─────────────────────────────┘
```

**Token constraints**
```
Page h-padding (card list):   var(--spacing-md)
Page h-padding (full-width):  0
Item gap (card style):        var(--spacing-sm)
Item gap (divider style):     0
Section header h-padding:     var(--spacing-md)
FloatingActionButton:         right: var(--spacing-md), bottom: var(--spacing-md)
                              + var(--bottom-nav-height) + env(safe-area-inset-bottom)
```

**List item anatomy**
```
Leading (optional): avatar var(--avatar-size-md) / icon var(--icon-lg) / thumbnail 56×56
Headline:           var(--font-size-body) / var(--font-weight-semibold)
Supporting text:    var(--font-size-body-sm) / var(--color-text-secondary)
Trailing (optional): chevron / badge / metadata text / action button
```

**Choose card vs. full-width**
```
Card (with bg + border + radius):
  ✅ Media-heavy (product images, article thumbnails)
  ✅ Content has varying heights
  ✅ Items represent distinct objects (not a continuous stream)

Full-width (divider only):
  ✅ Text-dense lists (messages, notifications, settings)
  ✅ Scannable uniform content
  ✅ High density needed
```

---

## 3. Detail View

**Use when:** full content of one item — article, product, profile, order detail.

```
┌─────────────────────────────┐
│  Navbar (back + title + ⋯) │
│  ─────────────────────────  │
│  Hero image (full-bleed)    │  aspect 16:9 or 4:3, no h-padding
│  ─────────────────────────  │
│  Title block                │  padding: var(--spacing-md)
│    Headline (h1)            │
│    Meta (author / date)     │  var(--font-size-body-sm) / var(--color-text-secondary)
│    Tags                     │
│  ─────────────────────────  │
│  Content sections           │  var(--spacing-xl) between sections
│    Text, images, cards…     │  h-padding: var(--spacing-md)
│  ─────────────────────────  │
│  Related items (optional)   │
│                             │
│  BottomActionBar (sticky)   │  height 64px, see below
└─────────────────────────────┘
```

**Token constraints**
```
Content h-padding:     var(--spacing-md)
Section gap:           var(--spacing-xl)
Hero: full-bleed — 0 horizontal padding, aspect-ratio: 16/9

Bottom action bar (buy / book / submit):
  height:              64px
  padding:             0 var(--spacing-md)
  padding-bottom:      calc(var(--spacing-md) + env(safe-area-inset-bottom))
  bg:                  var(--color-surface)
  border-top:          1px solid var(--color-border)
  z-index:             var(--z-sticky)
```

**Primary action placement decision**
```
Sticky bottom bar → purchase, booking, irreversible submit (always visible)
Inline in content → contextual action (follow, react, share)
Navbar right icon → global page action (edit, share, more)
```

---

## 4. Master-Detail

**Use when:** users need to browse a list AND view detail simultaneously — email, chat,
file manager, settings with sub-pages. Primarily desktop / tablet (≥ 768px).

```
Mobile (< 768px):         Desktop (≥ 768px):
┌─────────────┐           ┌──────────┬──────────────────────┐
│  List View  │           │  Master  │  Detail Panel        │
│  (full     │           │  Panel   │                      │
│   screen)   │           │  ←scroll │  (content here)      │
│             │  ──tap──► │          │                      │
│  ─────────► │           │  item    │                      │
│  Detail     │           │  list    │  Primary action      │
│  (full     │           │          │  bar (bottom)        │
│   screen)   │           │          │                      │
└─────────────┘           └──────────┴──────────────────────┘
```

**Token constraints**
```
Master panel width (desktop): min 280px, max 360px, flex-shrink 0
Detail panel: flex 1, min-width 0
Divider: 1px solid var(--color-border)
Mobile: full-screen push navigation (no split)

Breakpoint switch: --breakpoint-md (768px)
  < 768px → stack (master then detail as separate screens)
  ≥ 768px → side-by-side split
```

**Selection state in master**
```
Selected item bg:   var(--color-selected-bg)
Selected item text: var(--color-primary)
Selected indicator: 3px left border, var(--color-primary)
Empty detail state: centred Empty State component
```

---

## 5. Settings / Form

**Use when:** collecting user input or configuring preferences.

```
┌─────────────────────────────┐
│  Navbar (title + Cancel/Save│
│  ─────────────────────────  │
│                             │
│  Section label (optional)   │  var(--font-size-body-sm) / uppercase
│  ┌─────────────────────┐    │
│  │ Label               │    │
│  │ [Input field]       │    │
│  │ Helper text         │    │
│  └─────────────────────┘    │
│                             │
│  ─ ─ ─ ─ Section gap ─ ─ ─  │  var(--spacing-lg) or divider
│                             │
│  ┌─────────────────────┐    │
│  │ Toggle row          │ ◉ │
│  │ Select row          │ › │
│  └─────────────────────┘    │
│  ...                        │
│                             │
│  ──── sticky bottom ─────── │
│  [Submit / Save button]     │  full-width, var(--btn-height-mobile)
└─────────────────────────────┘
```

**Token constraints**
```
Page h-padding:   var(--spacing-md)
Label → input:    var(--spacing-xs)
Input → helper:   var(--spacing-xs)
Field → field:    var(--spacing-md)
Section gap:      var(--spacing-lg)

Submit area:
  padding:        var(--spacing-md)
  padding-bottom: calc(var(--spacing-md) + env(safe-area-inset-bottom))
  bg:             var(--color-surface)
  border-top:     1px solid var(--color-border)
```

**Validation rules (from Apple HIG)**
```
Validate on:   field blur (not keystroke) + form submit
Error display: inline below field, never alert dialog
On submit:     scroll to first error, focus it
Required mark: asterisk after label, footnote at bottom
```

**Row types for Settings pages**
```
Toggle row:  label + sublabel (optional) + Toggle (right) — no chevron
Select row:  label + current value (right, secondary) + chevron
Info row:    label + value — not tappable, no chevron
Action row:  label + chevron — navigates to sub-page
Danger row:  label in var(--color-danger) — confirms before acting
```

---

## 6. Dashboard / Overview

**Use when:** heterogeneous content sections — home feed, analytics, profile overview.

```
┌─────────────────────────────┐
│  Custom header (branded)    │  often not a standard Navbar
│  ─────────────────────────  │
│  ┌─ Banner / Status ──────┐ │  full-bleed, branded bg (optional)
│  └────────────────────────┘ │
│                             │
│  Quick actions (2×2 grid)   │  max 4 on mobile, 6 on desktop
│                             │
│  Section title   See all >  │  var(--font-size-h4) / left + right link
│  ┌──Card──┐ ┌──Card──┐     │  horizontal scroll carousel
│  │        │ │        │     │  card width: 70-80% viewport
│  └────────┘ └────────┘     │  gap: var(--spacing-sm)
│                             │
│  Section title   See all >  │
│  Full-width card list       │
│  ...                        │
│                             │
│  BottomNav (fixed)          │
└─────────────────────────────┘
```

**Token constraints**
```
Section gap:       var(--spacing-xl)
Section header:    padding: var(--spacing-md) h / var(--spacing-sm) v
Carousel:          padding-left: var(--spacing-md) (aligns to page edge)
                   peek next card as affordance (show 10-15% of next)
Max sections:      4–5 (more hurts engagement)
```

---

## 7. Tabbed Content

**Use when:** same-level content organised into named categories — explore/follows/nearby,
product description/reviews/specs.

```
┌─────────────────────────────┐
│  Navbar                     │
│  ─────────────────────────  │
│  [Tab] [Tab] [Tab] [Tab]    │  TabBar, sticky, var(--tab-bar-height)
│  ─ ─ ─ active underline ─ ─ │  2px, var(--color-primary)
│                             │
│  Scrollable content         │  per-tab content below
│  for active tab             │
│  ...                        │
│                             │
│  BottomNav (fixed)          │
└─────────────────────────────┘
```

**Token constraints**
```
TabBar:        height var(--tab-bar-height), sticky below navbar
Tab count:     3–5 recommended; scroll if > 5 (do not wrap)
Active state:  var(--tab-active-color), var(--tab-active-border)
               font-weight var(--tab-active-weight)
Inactive:      var(--tab-inactive-color), var(--tab-inactive-weight)
Tab transition: cross-fade, var(--duration-fast) (no slide on iOS — reserved for push)
```

---

## 8. Wizard / Stepper

**Use when:** guided sequential process — registration, checkout, onboarding, order flow.

```
┌─────────────────────────────┐
│  [Back] Step 2 of 4  [Skip] │  Navbar or custom header
│  ━━━━━━━━━━━░░░░░░░░░░░░░░  │  progress bar (determinate)
│  ─────────────────────────  │
│                             │
│  Step title                 │  var(--font-size-h2) / bold
│  Step description           │  var(--font-size-body) / var(--color-text-secondary)
│                             │
│  Step content               │  form fields / choices / info
│  (varies per step)          │
│                             │
│  ──── sticky bottom ─────── │
│  [Back]        [Continue]   │  ghost + primary, or primary full-width
└─────────────────────────────┘
```

**Token constraints**
```
Progress bar:  height 4px, var(--progress-track-bg) / var(--color-primary) fill
               top: 0 below navbar, full-width
Step count:    max 4–5 steps; more → progressive disclosure post-signup
Back button:   ghost style; visible from step 2 onwards
Skip link:     var(--font-size-body-sm) / var(--color-text-tertiary); only if truly optional
Last step CTA: "Get started" / "Done" — not "Continue"
```

**Step content types**
```
Input step:    form fields (follow Settings/Form token rules)
Choice step:   radio group or card-select (visual radio with icon)
Info step:     illustration + headline + body (follow Single Screen rules)
Permission:    system permission UI — do not replicate native dialogs
```

---

## Responsive Breakpoints

```
< 640px  (var(--breakpoint-sm))  — Mobile
  Single column, bottom nav, stack master-detail
  h-padding: var(--spacing-md)

640–1024px  (var(--breakpoint-md) to --breakpoint-lg))  — Tablet
  2-col card grid optional
  Side nav optional (≥ 5 top-level sections)
  Master-detail split enabled
  h-padding: var(--spacing-lg)

> 1024px  (var(--breakpoint-lg))  — Desktop
  Persistent side nav replaces bottom nav
  2-col form layout for related fields
  List-detail split layout for detail pages
  h-padding: var(--spacing-xl), max-width 1200px centred
```
