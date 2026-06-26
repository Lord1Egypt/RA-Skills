# Design Tokens — Base System

## Color Palette

### Brand Neutral (Dark)
| Token | Hex | Use |
|---|---|---|
| `--color-bg` | `#0F0F0F` | Page background |
| `--color-surface` | `#1A1A1A` | Card / panel surface |
| `--color-border` | `#2A2A2A` | Borders, dividers |
| `--color-text` | `#F5F5F5` | Primary text |
| `--color-muted` | `#888888` | Secondary text, labels |
| `--color-accent` | `#6366F1` | Links, focus states, CTAs |

### Light Mode Override
| Token | Hex | Use |
|---|---|---|
| `--color-bg` | `#FAFAFA` | Page background |
| `--color-surface` | `#FFFFFF` | Card surface |
| `--color-border` | `#E5E5E5` | Borders |
| `--color-text` | `#111111` | Primary text |
| `--color-muted` | `#666666` | Secondary text |

### Semantic Colors
| Token | Hex | Use |
|---|---|---|
| `--color-success` | `#22C55E` | Success states |
| `--color-warning` | `#F59E0B` | Warning states |
| `--color-error` | `#EF4444` | Error states |
| `--color-info` | `#3B82F6` | Info / links |

## Typography

### Type Scale (ratio: 1.25 — Major Third)
| Step | Size | Use |
|---|---|---|
| `--text-xs` | 12px / 0.75rem | Labels, captions |
| `--text-sm` | 14px / 0.875rem | Secondary text, metadata |
| `--text-base` | 16px / 1rem | Body copy |
| `--text-lg` | 20px / 1.25rem | Lead text |
| `--text-xl` | 24px / 1.5rem | H4, card titles |
| `--text-2xl` | 30px / 1.875rem | H3 |
| `--text-3xl` | 38px / 2.375rem | H2 |
| `--text-4xl` | 48px / 3rem | H1, display |

### Font Families
```css
--font-sans: 'Inter', system-ui, -apple-system, sans-serif;
--font-serif: 'Georgia', 'Times New Roman', serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
--font-display: 'Inter', var(--font-sans);  /* override per project */
```

### Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Line Height
```css
--leading-tight: 1.25;   /* headings */
--leading-normal: 1.5;  /* body */
--leading-relaxed: 1.75; /* longform / newsletter */
```

## Spacing (8px Grid)

```css
--space-1:  4px;
--space-2:  8px;
--space-3:  12px;
--space-4:  16px;
--space-5:  20px;
--space-6:  24px;
--space-8:  32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
```

## Border Radius

```css
--radius-sm:  4px;   /* buttons, inputs */
--radius-md:  8px;   /* cards, panels */
--radius-lg:  12px;  /* modals, overlays */
--radius-xl:  16px;  /* large containers */
--radius-full: 9999px; /* pills, avatars */
```

## Shadows

```css
--shadow-sm:  0 1px 2px rgba(0,0,0,0.05);
--shadow-md:  0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05);
--shadow-lg:  0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
--shadow-xl:  0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04);
```

## Animation

```css
--duration-fast:   100ms;  /* micro-interactions, toggles */
--duration-base:   200ms;  /* buttons, hovers, standard transitions */
--duration-slow:    400ms;  /* modals, panels, reveals */
--ease-default:    cubic-bezier(0.4, 0, 0.2, 1);
--ease-in:          cubic-bezier(0.4, 0, 1, 1);
--ease-out:         cubic-bezier(0, 0, 0.2, 1);
--ease-bounce:      cubic-bezier(0.34, 1.56, 0.64, 1);
```

## Breakpoints

```css
--bp-sm:  640px;
--bp-md:  768px;
--bp-lg:  1024px;
--bp-xl:  1280px;
--bp-2xl: 1536px;
```

## Component Tokens

### Button
```css
--btn-height:     40px;
--btn-padding-x:  16px;
--btn-radius:     var(--radius-sm);
--btn-font-size:  var(--text-sm);
--btn-font-weight: var(--font-medium);
```

### Input
```css
--input-height:   40px;
--input-padding:  12px;
--input-radius:   var(--radius-sm);
--input-border:   1px solid var(--color-border);
--input-focus:    2px solid var(--color-accent);
```

### Card
```css
--card-padding:   var(--space-6);
--card-radius:    var(--radius-md);
--card-bg:        var(--color-surface);
--card-shadow:    var(--shadow-sm);
```

## Z-Index Scale

```css
--z-base:    0;
--z-dropdown: 100;
--z-sticky:   200;
--z-overlay:  300;
--z-modal:    400;
--z-toast:    500;
```
