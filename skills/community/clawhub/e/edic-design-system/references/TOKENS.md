# EDIC Complete Token Reference
# 完整令牌实际值速查

> Loaded on demand when spacing, radius, shadow, or motion token values are needed.
> Ground truth is `styles.css`. This reference is a compact quick index; always verify exact values against `styles.css` and `tokens.json` before release.

---

## Spacing (`--ds-space-*`)

4px base ratio. Use these instead of hard-coded pixel or rem values.

| Token | rem | px equivalent |
|-------|-----|---------------|
| `--ds-space-0` | 0 | 0 |
| `--ds-space-0-25` | 0.0625rem | 1px |
| `--ds-space-0-5` | 0.125rem | 2px |
| `--ds-space-0-75` | 0.1875rem | 3px |
| `--ds-space-1` | 0.25rem | **4px** |
| `--ds-space-2` | 0.5rem | **8px** |
| `--ds-space-3` | 0.75rem | **12px** |
| `--ds-space-4` | 1rem | **16px** |
| `--ds-space-5` | 1.25rem | 20px |
| `--ds-space-6` | 1.5rem | **24px** |
| `--ds-space-7` | 1.75rem | 28px |
| `--ds-space-8` | 2rem | **32px** |
| `--ds-space-9` | 2.25rem | 36px |
| `--ds-space-10` | 2.5rem | 40px |
| `--ds-space-12` | 3rem | 48px |
| `--ds-space-14` | 3.5rem | 56px |
| `--ds-space-16` | 4rem | 64px |
| `--ds-space-20` | 5rem | 80px |
| `--ds-space-24` | 6rem | 96px |
| `--ds-space-32` | 8rem | 128px |

**Common mappings** (use these, not magic numbers):
- `4px` → `--ds-space-1`
- `8px` → `--ds-space-2`
- `12px` → `--ds-space-3`
- `16px` → `--ds-space-4`
- `24px` → `--ds-space-6`
- `32px` → `--ds-space-8`

---

## Border Radius (`--ds-radius-*`)

| Token | Value | Use case |
|-------|-------|----------|
| `--ds-radius-none` | 0 | Sharp edges |
| `--ds-radius-sm` | 2px | Subtle rounding (badges, chips) |
| `--ds-radius-md` | **4px** | Default — buttons, inputs |
| `--ds-radius-lg` | **8px** | Cards, dropdowns, accordions |
| `--ds-radius-xl` | **12px** | Modals, glass cards, toast |
| `--ds-radius-2xl` | **16px** | Large decorative surfaces |
| `--ds-radius-full` | 9999px | Pills, circular avatars |

---

## Shadow (`--ds-shadow-*`)

All shadows use OKLch black with opacity — they adapt naturally to dark mode.

| Token | Value |
|-------|-------|
| `--ds-shadow-xs` | `0 1px 2px oklch(0% 0 0 / 4%)` |
| `--ds-shadow-sm` | `0 1px 3px oklch(0% 0 0 / 6%), 0 1px 2px oklch(0% 0 0 / 4%)` |
| `--ds-shadow-md` | `0 4px 6px oklch(0% 0 0 / 6%), 0 2px 4px oklch(0% 0 0 / 4%)` |
| `--ds-shadow-lg` | `0 10px 15px oklch(0% 0 0 / 8%), 0 4px 6px oklch(0% 0 0 / 4%)` |
| `--ds-shadow-xl` | `0 20px 25px oklch(0% 0 0 / 10%), 0 8px 10px oklch(0% 0 0 / 6%)` |
| `--ds-shadow-2xl` | `0 25px 50px oklch(0% 0 0 / 12%)` |
| `--ds-shadow-inner` | `inset 0 2px 4px oklch(0% 0 0 / 4%)` |
| `--ds-shadow-btn` | `0 1px 2px oklch(0% 0 0 / 6%)` |
| `--ds-shadow-btn-hover` | `0 4px 12px oklch(0% 0 0 / 10%), 0 2px 4px oklch(0% 0 0 / 6%)` |

Dark mode overrides (in `[data-theme="dark"]`):
- `--ds-shadow-xs` → `0 1px 2px oklch(0% 0 0 / 30%)`
- `--ds-shadow-sm` → `0 1px 3px oklch(0% 0 0 / 35%), 0 1px 2px oklch(0% 0 0 / 25%)`

---

## Motion (`--ds-duration-*` / `--ds-ease-*`)

| Token | Value | Use case |
|-------|-------|----------|
| `--ds-duration-50` | 50ms | Micro-interactions (icon swap) |
| `--ds-duration-100` | 100ms | Button press |
| `--ds-duration-150` | **150ms** | Default hover transitions |
| `--ds-duration-200` | 200ms | Panel fade |
| `--ds-duration-300` | **300ms** | Modal open, toast slide-in |
| `--ds-duration-500` | 500ms | Page transitions, theme switch |
| `--ds-duration-700` | 700ms | Reveal animations |
| `--ds-duration-1000` | 1000ms | Slow entrance |

| Easing Token | Value | Character |
|---|---|---|
| `--ds-ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Fast start, gentle deceleration — **default** |
| `--ds-ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Slow start, fast exit (dismissals) |
| `--ds-ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Symmetric, for toggles |
| `--ds-ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Slight overshoot, playful |

Always add `@media (prefers-reduced-motion: reduce)` override when using durations > 150ms.

---

## Typography Scale (`--ds-text-*`)

| Token | rem | px | Use |
|-------|-----|----|-----|
| `--ds-text-caption` | 0.75rem | 12px | Labels, meta |
| `--ds-text-body-sm` | 0.875rem | 14px | Secondary text, UI |
| `--ds-text-body` | 1rem | 16px | **Default body** |
| `--ds-text-body-lg` | 1.125rem | 18px | Lead paragraphs |
| `--ds-text-lead` | 1.25rem | 20px | Hero subtitles |
| `--ds-text-h5` | 1.25rem | 20px | Sub-headings, navbar brand |
| `--ds-text-h4` | 1.5rem | 24px | Card headings |
| `--ds-text-h3` | 1.875rem | 30px | Sub-section |
| `--ds-text-h2` | 2.25rem | 36px | Page sections |
| `--ds-text-h1` | 3rem | 48px | Page title |
| `--ds-text-display` | 3.75rem | 60px | Feature headings |
| `--ds-text-hero` | 4.5rem | 72px | Hero |

---

## Line Height (`--ds-leading-*`)

| Token | Value | Use |
|-------|-------|-----|
| `--ds-leading-tight` | 1.1 | Display headings |
| `--ds-leading-snug` | 1.25 | Sub-headings |
| `--ds-leading-body` | **1.55** | Body text (default) |
| `--ds-leading-relaxed` | 1.7 | Long-form prose |
| `--ds-leading-loose` | 2.0 | Spacious reading |

---

## Letter Spacing (`--ds-tracking-*`)

| Token | Value | Use |
|-------|-------|-----|
| `--ds-tracking-tight` | -0.01em | Display headings |
| `--ds-tracking-normal` | 0.02em | UI text default |
| `--ds-tracking-wide` | 0.04em | Brand / navbar |
| `--ds-tracking-wider` | 0.08em | Eyebrow labels |
| `--ds-tracking-widest` | 0.12em | All-caps labels |
| `--ds-tracking-cjk-body` | 0.03em | CJK body text |
| `--ds-tracking-cjk-heading` | 0.06em | CJK headings |
| `--ds-tracking-mono` | 0 | Code |

---

## Z-Index (`--ds-z-*`)

| Token | Value | Layer |
|-------|-------|-------|
| `--ds-z-base` | 0 | Default flow |
| `--ds-z-above` | 1 | Raised elements |
| `--ds-z-dropdown` | 100 | Dropdowns |
| `--ds-z-sticky` | 200 | Sticky navbar |
| `--ds-z-overlay` | 300 | Backdrop overlays |
| `--ds-z-modal` | 400 | Modal dialogs |
| `--ds-z-toast` | 500 | Toast notifications |


---

## Blur (`--ds-blur-*`)

Used with `backdrop-filter` on glass surfaces. Always pair with a colored background parent.

| Token | Value | Use case |
|-------|-------|----------|
| `--ds-blur-sm` | 4px | Subtle frosted hint |
| `--ds-blur-md` | 12px | Frosted nav, light glass |
| `--ds-blur-lg` | **24px** | Glass cards, modal backdrops — **default** |
| `--ds-blur-xl` | 48px | Heavy frosted overlay |

> `backdrop-filter` requires the element to have a translucent background (e.g. `var(--ds-glass-bg)` at ~55% opacity). A fully opaque background makes blur invisible.
