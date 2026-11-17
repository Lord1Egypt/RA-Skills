# Interaction Patterns

State flows, gesture behaviours, and feedback patterns. Each entry describes the
trigger, the state machine, and the visual treatment at each state.

Sources: Material Design 3 Motion & States, Apple HIG Gestures & Loading.

---

## Component State System

All interactive components share a consistent state layer model (MD3 spec).
State layers are applied ON TOP of the component's base style.

```
State       Trigger                         Layer opacity
─────────────────────────────────────────────────────────
enabled     default                         0%
hover       pointer over element            8%   (desktop only)
focus       keyboard nav / programmatic     12%  + focus ring
pressed     tap / click                     12%  + ripple from touch point
dragged     picked up for reorder           16%  + elevation increase
disabled    non-interactive                 content: 38% opacity
                                            container: 12% opacity
```

### Combining states
Focus + hover stack additively. A focused+hovered button shows both
the 12% focus layer and 8% hover layer simultaneously.

### Implementation
```css
/* Apply via CSS, not by changing base color */
.btn::before {
  content: '';
  position: absolute; inset: 0;
  background: currentColor;  /* uses text/icon color */
  opacity: 0;
  transition: opacity var(--duration-fast) var(--easing-default);
  border-radius: inherit;
  pointer-events: none;
}
.btn:hover::before   { opacity: 0.08; }
.btn:focus::before   { opacity: 0.12; }
.btn:active::before  { opacity: 0.12; }
```

---

## Loading States

**Rule:** show a loading indicator within 1 second of any wait. (Apple HIG)

### State machine
```
idle ──[trigger action]──► loading ──[success]──► content
                                    └─[error]───► error state
```

### Skeleton → Content (preferred for page loads)
```
Show:     immediately on navigation, before data arrives
Duration: match content layout exactly (same heights/widths as real content)
Shimmer:  left-to-right gradient sweep, 1.5s loop (see --skeleton-* tokens)
Replace:  fade content in over var(--duration-normal) once data arrives

When to use skeleton:
  ✅ First page load, tab switch, pull-to-refresh
  ❌ Actions (button press) — use spinner on the button instead
  ❌ < 300ms loads — show nothing, flash of skeleton is jarring
```

### Spinner (for actions and short waits)
```
Show:     on button press, overlay for blocking operations
Size:     16px inline (button), 24px standalone, 40px full-page overlay
Colour:   var(--color-primary) or white on coloured bg
Duration: show after 300ms delay (instant if operation is predictable)
Cancel:   always allow cancel for > 3s operations
```

### Progress bar (for known-duration operations)
```
Use:      file upload, multi-step processing with knowable progress
Prefer determinate (%) over indeterminate (spinner) when progress is measurable
Indeterminate: use when duration is unknown but bounded (< 10s typically)
```

### Full-page blocking overlay
```
Use only for: multi-step server operations that cannot be interrupted
Overlay:  var(--color-overlay) bg + centred spinner + optional label
Avoid:    for operations < 3s — prefer in-button spinner
```

---

## Pull-to-Refresh

**Platform note:** Native on iOS (UIRefreshControl). On Android and Web, build
explicitly. Only use on scrollable list/feed pages.

### State machine
```
idle ──[pull down > threshold]──► triggered ──[release]──► refreshing ──[done]──► idle
      ←─[release before threshold]──────────── cancelled
```

### Visual treatment
```
Threshold:       60–80px of overscroll
Indicator:       spinner appears at top of list, follows finger until threshold
                 colour: var(--color-primary)
Triggered state: spinner at 100% opacity, haptic feedback on iOS
Refreshing:      spinner spins, list content held down by indicator height
                 show for minimum 500ms even if data arrives faster (prevents flash)
Done:            indicator slides back up, content refreshes
                 fade-in new items from top: translateY(-20px) → 0, opacity 0 → 1
                 duration var(--duration-normal)
```

---

## Infinite Scroll / Pagination

### Infinite scroll (preferred for feeds and discovery content)
```
Trigger:     load next page when last item enters viewport
             use IntersectionObserver with 200px bottom margin
Loading:     show 3 skeleton items at bottom while fetching
Error:       show "Failed to load more" + "Retry" button at bottom
End:         show "You've reached the end" message (never just stop silently)

When NOT to use:
  ❌ Search results (users need to know total count, jump to page)
  ❌ Task lists (users need to remember where they were)
```

### Pagination (for search results and structured data)
```
Show:        page count or total results ("Page 2 of 14" / "142 results")
Navigation:  Prev / Next buttons + optional page number input
Load more button: acceptable middle ground ("Load 20 more")
             clearer intent than infinite scroll, better for non-feeds
```

---

## Form Validation

### Validation timing (Apple HIG + MD3 consensus)
```
Do NOT validate on every keystroke — disruptive and premature

Validate on blur (field loses focus):
  ✅ Required field is empty
  ✅ Format clearly wrong (email missing @, phone wrong length)
  ❌ Complex rules requiring server check (username taken)

Validate on submit:
  ✅ All rules, including cross-field rules (password confirmation)
  ✅ Server-side validation errors

Validate on change (exceptions):
  ✅ Password strength meter — useful as user types
  ✅ Character counter for limited-length fields
```

### Error display
```
Position:     inline below the field, never as alert dialog
              (alert dialogs interrupt flow, users lose their form state)
Appearance:   --input-border-error (red border) + error helper text
              icon: ⚠ or ✕ before helper text
Animation:    height 0 → auto, opacity 0 → 1, var(--duration-fast)

On submit with errors:
  1. Show all field errors simultaneously
  2. Scroll to the first invalid field (smooth scroll)
  3. Focus the first invalid input
  4. Submit button remains clickable (users may want to edit)
```

### Success state
```
Field-level:  green border + ✓ icon for fields requiring confirmation
              (e.g., username availability check)
              Don't show success state on every field — visual noise
Form-level:   Toast notification ("Profile saved") + navigate away OR
              Inline success message replacing the form
              Never show a modal dialog for routine form success
```

---

## Navigation Transitions

Based on MD3 motion patterns and Apple HIG.

### Push (forward navigation — drill down)
```
Entering screen:  slides in from right → centre
                  var(--duration-normal), var(--easing-enter)
Exiting screen:   slides out to left (small distance, ~30%)
                  var(--duration-normal), var(--easing-exit)

iOS back gesture: interactive — screen follows finger,
                  cancel if < threshold, complete if > threshold
```

### Pop (back navigation)
```
Reverse of push
Entering screen:  slides in from left (small distance)
Exiting screen:   slides out to right
```

### Modal presentation (sheet / bottom sheet)
```
Enter: slides up from bottom
       var(--duration-slow), var(--easing-enter)
Exit:  slides down
       var(--duration-normal), var(--easing-exit)
Dismiss: drag down > 40% height OR tap overlay
```

### Tab switch (peer navigation — MD3 Shared Axis)
```
Switch right (to higher index tab):
  outgoing: slides left + fades, var(--duration-fast)
  incoming: slides from right + fades in

Switch left (to lower index tab):
  reverse direction
Note: don't use slide transitions for tab switches on iOS
      (reserved for push/pop), use cross-fade instead on iOS
```

### Replace / Full-screen transition (MD3 Fade Through)
```
Use for: navigating to unrelated screens, splash to main content
Outgoing: fades out + slight scale down (0.95)
Incoming: fades in + slight scale up (0.95 → 1)
Overlap:  short gap between fade-out completing and fade-in starting
Duration: var(--duration-normal)
```

---

## Swipe Actions on List Items

Common on iOS (Mail, Messages). Use for secondary actions (delete, archive, snooze).

### State machine
```
idle ──[swipe left]──► partial reveal ──[release]──► snap to action width
                    └──[swipe past threshold]──► full reveal + auto-trigger
                    └──[swipe back]──► snap back to idle
```

### Visual treatment
```
Action revealed behind item:
  background: action colour (delete: var(--color-danger), archive: var(--color-success))
  icon + label: white, centred in action zone
  action zone width: 80px per action
  max actions shown: 2 (more hides behind "More" button)

Partial reveal: item slides left, actions visible, item at rest position
Full reveal (destructive): item snaps fully off-screen, action executes
Haptic: light haptic at threshold crossing (iOS only)
```

### Rules
- Never use swipe as the ONLY way to access critical actions (accessibility)
- Always provide a visible alternative (long-press context menu or edit mode)
- Limit to secondary / optional actions — primary action is always a tap

---

## Long Press / Context Menu

```
Trigger:    500ms hold without movement (Apple HIG minimum)
Haptic:     light impact feedback on trigger (iOS)

Display:    context menu appears adjacent to touch point
            items: 3–7 actions (more = sheet)
            icons: left of labels (SF Symbols or custom)
            destructive: red text (var(--color-danger)), at bottom of list

Preview:    iOS supports content preview above the menu
            blur background behind preview

Dismiss:    tap outside, swipe away, or select action
```

---

## Toast Feedback

Use for: confirming actions the user can reverse or dismissible updates.
Do NOT use for: errors requiring action, critical information, blocking operations.

```
Trigger:    after async action completes (not on button press)
Position:   bottom-centre, 24px from safe-area-bottom
Duration:   var(--toast-auto-dismiss) = 2500ms
            longer (4000ms) if message is longer or has an action button

Enter:  translateY(100%) → 0 + opacity 0 → 1
        var(--duration-normal), var(--easing-enter)
Exit:   opacity 1 → 0 (no Y movement)
        var(--duration-normal)

With action:   "Undo" button right of message
               extend auto-dismiss to 4000ms when action is present
Stacking:      new toast replaces previous one (never stack > 1)
```

---

## Error Handling Patterns

### Levels of severity

```
Field error (lowest):
  Treatment: inline red text below field
  Dismissal: automatic when user corrects the field

Toast error:
  Treatment: Toast with ⚠ icon, slightly different bg shade
  Use for:   network blips, actions that failed but can be retried
  Dismiss:   auto after 4000ms or manual X button

Inline error in content area:
  Treatment: ErrorBlock replacing content that failed to load
             icon + message + "Try again" button
  Use for:   section that failed to load (not full-page)

Full-page error (highest):
  Treatment: empty-state-style, icon + title + description + retry CTA
  Use for:   page cannot render at all (auth error, not found, offline)
```

### Error message tone (Apple HIG)
```
✅ Explain what happened in plain language
✅ Say what the user can do next
✅ If recoverable, provide the recovery action

❌ "Error 500" or technical codes
❌ Blame the user ("You entered the wrong password" → "Incorrect password")
❌ Apologise excessively ("We're so sorry…")
❌ Explain technical cause ("The API timed out…")
```

---

## Motion Accessibility

Always respect `prefers-reduced-motion`. (MD3 + Apple HIG)

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Reduced motion substitutes:
```
Slide transitions → instant show/hide or opacity-only fade
Skeleton shimmer  → static placeholder (no animation)
Spinning loaders  → static icon or text "Loading…"
```

---

## Gesture Conflict Rules (Apple HIG)

Never override system gestures:
```
Swipe up from bottom     → Home / App Switcher (iOS)
Swipe down from top      → Notification Centre / Control Centre
Swipe from left edge     → Back navigation (iOS)
Press & hold on text     → Text selection
```

When your gesture might conflict:
- Restrict the gesture to a specific area (not full-screen)
- Use a different gesture (long-press instead of edge swipe)
- Always provide a button alternative alongside any gesture

---

## Component State Machines

Per-component state machines for L2 generation and L3 spec.json `states` fields.
Every interactive component must document all its states. Use these as the
canonical reference — do not invent states not listed here.

### State Machine Speed Reference

| Component | States | Enter animation | Exit animation |
|-----------|--------|-----------------|----------------|
| Button | 5 | — | — |
| Input | 5 | focus ring var(--duration-fast) | — |
| Card | 5 | hover lift var(--duration-fast) | — |
| List Item | 5 | — | — |
| Toggle | 4 | thumb slide var(--duration-fast) var(--easing-spring) | same |
| Modal | 3 | scale+fade var(--duration-normal) var(--easing-spring) | fade var(--duration-fast) |
| Toast | 4 | slideUp+fade var(--duration-normal) | fade var(--duration-normal) |
| Select | 5 | panel drop var(--duration-fast) | panel close var(--duration-fast) |
| Tab Bar | 3 variants | cross-fade var(--duration-fast) | — |
| Nav Drawer | 3 positions | slide var(--duration-slow) var(--easing-enter) | slide var(--duration-normal) var(--easing-exit) |
| Skeleton | 3 | — | fadeOut var(--duration-normal) |
| Search | 6 | expand var(--duration-fast) | collapse var(--duration-fast) |

---

### Button (5 states)

```
default   → hover [pointer enter]  → default [pointer leave]
default   → pressed [tap/click]    → default [release]
default   → focused [keyboard]     → default [blur]
any       → loading [async action starts]
any       → disabled [prop set]

State     Token ref                         Notes
────────────────────────────────────────────────────────────
default   --btn-primary-bg                  base appearance
hover     --btn-primary-bg-hover            desktop only; state layer 8%
pressed   --btn-primary-bg-active           state layer 12%; ripple from touch point
focused   base + focus ring                 3px solid --color-primary-surface outside border
loading   spinner 16px (white on primary)   pointer-events none; min 300ms display
disabled  opacity --btn-disabled-opacity    pointer-events none; no state layers
```

---

### Input / TextField (5 states)

```
default → focused [click/tap]  → filled [user types]
filled  → error   [validation fails]
filled  → default [cleared]
any     → disabled [prop set]

State     Visual                                        Token ref
──────────────────────────────────────────────────────────────────────
default   border --input-border                         1px solid --color-border
focused   border --input-border-focus (1.5px)           + shadow --input-shadow-focus
filled    border --input-border                         text --color-text-primary
error     border --input-border-error (1.5px)           + shadow --input-shadow-error
          helper text: --color-danger; icon ⚠ before text
disabled  bg --input-bg-disabled; text --input-color-disabled; cursor not-allowed
```

---

### Card (5 states)

```
default → hover [pointer enter]    → default [leave]
default → pressed [tap]            → navigates or selects
default → selected [selection mode]
any     → disabled [prop set]

State     Visual                              Token ref
────────────────────────────────────────────────────────────
default   shadow --card-shadow; border --card-border
hover     shadow --card-shadow-hover; border --card-border-hover
          transform translateY(-1px)
pressed   shadow --card-shadow; transform none; state layer 12%
selected  border 2px solid --color-primary; bg --color-selected-bg
disabled  opacity 0.5; pointer-events none
```

---

### List Item (5 states)

```
default → hover [pointer enter]
default → pressed [tap]          → navigates or executes action
default → selected [tap in selection mode]
any     → disabled

State     Visual                     Token ref
──────────────────────────────────────────────────
default   bg --list-item-bg
hover     bg --list-item-bg-hover
pressed   bg --list-item-bg-active   + ripple from touch point
selected  bg --color-selected-bg; leading checkbox checked
disabled  opacity 38%; pointer-events none
```

---

### Toggle / Switch (4 states)

```
off → on   [tap]  — thumb slides right, bg changes
on  → off  [tap]  — thumb slides left, bg changes
any → disabled

State     Visual                       Animation
────────────────────────────────────────────────────────────
off       bg --toggle-off-bg; thumb left (translateX 0)
on        bg --toggle-on-bg; thumb right (translateX 14px)
          transition: transform var(--toggle-thumb-transition)
                      background var(--toggle-transition)
focused   on/off + focus ring (3px solid --color-primary-surface outside)
disabled  opacity 0.5; pointer-events none
```

---

### Modal / Dialog (3 states)

```
hidden → entering [open triggered] → visible → exiting [dismiss] → hidden

State       Visual                            Token ref
──────────────────────────────────────────────────────────────────────
entering    overlay fades in (opacity 0→1)    var(--duration-normal)
            modal: scale(0.95)→scale(1)       var(--easing-spring)
            + opacity 0→1
visible     overlay --modal-overlay-bg        z-index --modal-z-index
            container: --modal-bg, --modal-shadow, --modal-radius
exiting     modal: opacity 1→0               var(--duration-fast)
            overlay: opacity 1→0             var(--duration-fast)

Dismiss triggers: button click, overlay tap, Escape key
```

---

### Toast / Notification (4 types)

```
hidden → visible [action completed] → auto-dismiss [timer expires] → hidden
                                    → manual dismiss [tap ×] → hidden

Type       Icon   Background                 Auto-dismiss
──────────────────────────────────────────────────────────
default    none   --toast-bg                 --toast-auto-dismiss (2500ms)
success    ✓      tinted --color-success     2500ms
warning    ⚠      tinted --color-warning     4000ms (needs more time to read)
error      ✗      tinted --color-danger      0ms (manual dismiss only)

Enter: translateY(100%)→0 + opacity 0→1, var(--duration-normal) var(--easing-enter)
Exit:  opacity 1→0, var(--duration-normal)
Stacking: new toast replaces current (never stack)
With action: extend dismiss to 4000ms; "Undo" button right-aligned
```

---

### Select / Dropdown (5 states)

```
closed → open [trigger tap]   → option-hover [pointer moves]
                               → selected [option tap] → closed
closed → disabled

State           Visual                                Token ref
────────────────────────────────────────────────────────────────────
closed/default  border --select-border                1px solid --color-border
closed/focused  border --select-border-open           + shadow --select-shadow-open
open            panel visible below trigger           --select-panel-shadow
                arrow icon rotates 180°; transition var(--duration-fast)
option:hover    bg --select-option-bg-hover
option:selected bg --select-option-bg-selected; text --select-option-color-selected
                checkmark icon (var(--icon-sm)) trailing right
disabled        bg --color-disabled-bg; text --color-disabled-text; cursor not-allowed

Panel animation:
  enter: scaleY(0.9)→1 + opacity 0→1, origin top, var(--duration-fast) var(--easing-enter)
  exit:  opacity 1→0, var(--duration-fast)
```

---

### Tab Bar (3 variants)

```
Variant 1 — Underline (default)
  active: 2px bottom border var(--tab-active-border); text --tab-active-color
  inactive: text --tab-inactive-color
  transition: border-color + color, var(--duration-fast)
  sliding indicator: transform translateX() on the underline bar

Variant 2 — Pill
  active: bg --color-primary-surface; text --tab-active-color; border-radius --radius-full
  inactive: transparent bg
  transition: background, var(--duration-fast)

Variant 3 — Dot indicator
  active: filled dot below icon, var(--color-primary)
  inactive: no dot
  use for: bottom navigation bar icons

Tab switch animation: cross-fade content (opacity), var(--duration-fast)
  NOTE: no slide on iOS tab bar — slide is reserved for push navigation
```

---

### Navigation Drawer (3 positions)

```
Position — Left (standard)     Position — Right        Position — Bottom Sheet
hidden → visible [open]         same as left             same as bottom sheet pattern
  overlay fades in              (RTL mirrored)           see "Bottom Sheet" component spec
  drawer slides from left
  duration: var(--duration-slow) var(--easing-enter)

visible → hidden [dismiss]
  drawer slides out left
  overlay fades out
  duration: var(--duration-normal) var(--easing-exit)
  dismiss: tap overlay, swipe drawer back, close button

Drawer width:   min 240px, max 360px, never > 70% viewport width
Overlay:        bg --modal-overlay-bg; z-index below drawer
Drawer z-index: var(--z-modal)
```

---

### Skeleton / Loading (3 states)

```
loading → error   [fetch fails]    → retry [tap retry] → loading
loading → content [data arrives]

State     Visual                        Token ref
──────────────────────────────────────────────────────────────
loading   shimmer animation             --skeleton-bg + --skeleton-shimmer-mid
          bg gradient sweeps left→right, --skeleton-duration (1.5s)
          matches real content layout exactly (same dimensions)

error     ErrorBlock replaces skeleton  icon + message + "Retry" button
          icon: var(--icon-xl); message: var(--color-text-secondary)
          button: ghost style

content   skeleton fades out            opacity 1→0, var(--duration-fast)
          real content fades in         opacity 0→1, var(--duration-normal)
          stagger children: 50ms delay per item (top to bottom)

Shimmer animation:
  background: linear-gradient(90deg,
    --skeleton-bg 25%, --skeleton-shimmer-mid 50%, --skeleton-bg 75%)
  background-size: 200% 100%
  animation: shimmer 1.5s ease-in-out infinite
  @keyframes shimmer { from { background-position: 200% 0 } to { 0% 0 } }
```

---

### Search / Autocomplete (6 states)

```
idle → focused [tap field]  → typing [keystroke]  → results [submit / debounce]
                                                   → empty   [no results]
                            → cleared [tap ×]     → focused
any → loading [fetch in progress]

State     Visual                                   Notes
──────────────────────────────────────────────────────────────
idle      bg --search-bg; placeholder visible      full width, pill shape
focused   bg --search-bg-focused                   border --search-border-focused
          border + shadow --search-shadow-focused   "Cancel" button slides in (mobile)
typing    clear × button appears (right)            debounce autocomplete 200–300ms
          autocomplete dropdown opens               --select-panel-shadow, z: --z-dropdown
loading   spinner in field (right, replaces ×)      16px, --color-primary
results   autocomplete closes                        results list replaces skeleton
empty     empty state inside dropdown               "No results for 'xyz'"
          suggest: "Clear search" or rephrase hint

Cancel animation (mobile): button slides in from right, var(--duration-fast)
Autocomplete panel: same tokens as Select panel (--select-panel-* tokens)
```

---

## Emotional State Templates

Ready-to-use CSS patterns for the four key emotional states.
Copy these into generated HTML and adjust content. Do not leave these states undesigned.

---

### Empty State

```html
<div class="empty-state" data-component="empty-state" data-spec-states="default">
  <div class="empty-state-icon">
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
      <!-- Replace with context-appropriate icon -->
      <rect x="8" y="12" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.5"/>
      <path d="M16 20h16M16 26h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
  </div>
  <p class="empty-state-title">Your skills will appear here</p>
  <p class="empty-state-body">Browse the marketplace to find and install skills.</p>
  <button class="btn btn-primary empty-state-action">Browse Marketplace</button>
</div>
```

```css
.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: var(--spacing-3xl) var(--spacing-xl);
  gap: var(--spacing-sm); text-align: center;
}
.empty-state-icon {
  color: var(--color-text-disabled);
  margin-bottom: var(--spacing-sm);
  opacity: 0.6;
}
.empty-state-title {
  font-size: var(--font-size-h4);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}
.empty-state-body {
  font-size: var(--font-size-body-sm);
  color: var(--color-text-secondary);
  max-width: 280px;
  line-height: var(--line-height-normal);
}
.empty-state-action { margin-top: var(--spacing-md); }
```

---

### Error State (inline content area)

```html
<div class="error-state" data-component="error-state" data-spec-states="default,retry">
  <svg class="error-state-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
    <path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  </svg>
  <div class="error-state-content">
    <p class="error-state-title">Couldn't load skills</p>
    <p class="error-state-body">Check your connection and try again.</p>
  </div>
  <button class="btn btn-secondary error-state-retry" onclick="retry()">Retry</button>
</div>
```

```css
.error-state {
  display: flex; align-items: center; gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-danger-surface);
  border: 0.5px solid rgba(255,51,51,0.2);
  border-radius: var(--radius-md);
  color: var(--color-danger);
}
.error-state-icon { flex-shrink: 0; }
.error-state-content { flex: 1; }
.error-state-title {
  font-size: var(--font-size-body-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-danger);
}
.error-state-body {
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
  margin-top: 2px;
}
```

---

### Success Toast

```html
<!-- Append to <body>, remove after 2.5s -->
<div class="toast toast-success" role="status" aria-live="polite">
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.2"/>
    <path d="M4.5 7l2 2 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <span>design-spec installed successfully</span>
</div>
```

```css
/* In addition to base .toast styles */
.toast-success {
  background: rgba(0,170,85,0.92); /* var(--color-success) with opacity */
  backdrop-filter: blur(20px);
  border: 0.5px solid rgba(255,255,255,0.15);
  display: flex; align-items: center; gap: var(--spacing-xs);
}

/* Auto-dismiss via animation — add class after inserting */
.toast.dismissing {
  animation: toastOut var(--duration-300) var(--easing-exit) forwards;
}
```

```js
function showSuccessToast(message) {
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const t = document.createElement('div');
  t.className = 'toast toast-success';
  t.innerHTML = `<svg>...</svg><span>${message}</span>`;
  document.body.appendChild(t);
  // Auto-dismiss
  setTimeout(() => {
    t.classList.add('dismissing');
    setTimeout(() => t.remove(), 300);
  }, 2500);
}
```

---

### Loading Skeleton

```html
<!-- Mirror the real layout exactly — same structure, filled with skeletons -->
<div class="skeleton-list" aria-busy="true" aria-label="Loading skills…">
  <!-- Repeat for expected number of items -->
  <div class="skeleton-row">
    <div class="skeleton skeleton-avatar"></div>
    <div class="skeleton-row-content">
      <div class="skeleton skeleton-line" style="width:45%"></div>
      <div class="skeleton skeleton-line" style="width:30%;margin-top:6px"></div>
    </div>
    <div class="skeleton skeleton-badge"></div>
  </div>
</div>
```

```css
/* Base shimmer */
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface-3) 25%,
    var(--color-surface-2) 50%,
    var(--color-surface-3) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

/* Shapes */
.skeleton-avatar   { width: 36px; height: 36px; border-radius: var(--radius-md); flex-shrink: 0; }
.skeleton-line     { height: 13px; }
.skeleton-badge    { width: 40px; height: 20px; border-radius: var(--radius-full); flex-shrink: 0; }

/* Layout */
.skeleton-row {
  display: flex; align-items: center; gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 0.5px solid var(--color-separator);
}
.skeleton-row-content { flex: 1; }

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; opacity: 0.6; }
}

/* Fade out when real content replaces skeleton */
.skeleton-list.loaded {
  animation: fadeOut var(--duration-300) var(--easing-exit) forwards;
}
```
