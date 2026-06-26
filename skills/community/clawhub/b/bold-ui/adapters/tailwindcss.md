# Tailwind CSS Adapter

Transform bold-ui design tokens into Tailwind CSS configuration and component code.

## Detection

You're in a Tailwind project if:
- `tailwind.config.js` or `tailwind.config.ts` exists
- `postcss.config.js` references `tailwindcss`
- `package.json` has `tailwindcss` as a dependency
- `globals.css` or `app.css` contains `@tailwind` directives

## Token Translation

### Colors

Map design token colors to Tailwind config `theme.extend.colors`:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Map from template tokens.colors
        // primary.base → primary
        // primary.light → primary-light
        // background.page → background
        // text.muted → text-muted
        primary: {
          DEFAULT: '#6366F1',
          light: '#818CF8',
          dark: '#4F46E5',
        },
        surface: '#FFFFFF',
        'text-muted': '#94A3B8',
        // ... etc for all color tokens
      }
    }
  }
}
```

**Naming convention**: Use kebab-case matching the token path. `tokens.colors.primary.base` → `colors.primary.DEFAULT`. `tokens.colors.text.muted` → `colors.text-muted`.

### Typography

Map font families and sizes:

```js
theme: {
  extend: {
    fontFamily: {
      // heading_font → sans (Tailwind uses sans as default)
      sans: ['Inter', 'SF Pro Display', '-apple-system', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },
    fontSize: {
      // Map token scale directly
      'xs': ['0.75rem', { lineHeight: '1rem' }],
      'sm': ['0.875rem', { lineHeight: '1.25rem' }],
      'base': ['1rem', { lineHeight: '1.5rem' }],
      'lg': ['1.125rem', { lineHeight: '1.75rem' }],
      // ...
    },
  }
}
```

### Border Radius

```js
theme: {
  extend: {
    borderRadius: {
      'sm': '0.25rem',
      'md': '0.5rem',
      'lg': '0.75rem',
      'xl': '1rem',
    }
  }
}
```

### Shadows

```js
theme: {
  extend: {
    boxShadow: {
      'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      'md': '0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
      'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04)',
      'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
    }
  }
}
```

### Animation

```js
theme: {
  extend: {
    transitionDuration: {
      'fast': '150ms',
      'normal': '200ms',
      'slow': '300ms',
      'gradual': '500ms',
    },
    transitionTimingFunction: {
      'in': 'cubic-bezier(0.4, 0, 1, 1)',
      'out': 'cubic-bezier(0, 0, 0.2, 1)',
      'spring': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    }
  }
}
```

## Component Generation

### Level 1: Theme Only

Generate only the `tailwind.config.js` extensions. If the project already has a Tailwind config, extend it rather than replacing:

```js
// Read existing config, add theme.extend with new tokens
// Preserve all existing config values
// Only add what the template brings new
```

### Level 2: Base Components

Generate a set of commonly used components. Place them in a sensible directory:
- Next.js/React: `src/components/ui/`
- Vue/Nuxt: `src/components/ui/`
- Others: `components/ui/`

Components to generate (use the template tokens + Tailwind classes):

**Button**
```tsx
// Use: primary.DEFAULT for bg, rounded-md (8px), shadow-sm
// Hover: translate-y-[-1px], shadow-md, primary.dark for bg
// Transition: duration-fast ease-out
// Focus: ring-2 ring-primary/40 ring-offset-2
```

**Card**
```tsx
// Use: surface for bg, rounded-lg (12px), shadow-sm
// Hover: shadow-md, translate-y-[-2px]
// Padding: p-6 (or p-4 for compact)
```

**Input**
```tsx
// Use: surface for bg, border-default for border
// Focus: border-primary, ring-2 ring-primary/40
// Rounded: rounded-md
// Text: text-primary for value, text-muted for placeholder
```

**Badge**
```tsx
// Use: rounded-full, text-xs font-medium px-2.5 py-0.5
// Variants: success/warning/error/info using functional colors
```

**Modal/Dialog**
```tsx
// Use: surface for bg, rounded-xl, shadow-xl
// Overlay: bg-black/50, backdrop-blur-sm
// Transition: scale-95 → scale-100, opacity 0 → 100
```

### Level 3: Page Layouts

Generate layout components:
- **Navbar**: Fixed top, surface bg with border-b, max-w-7xl centered
- **Hero**: Gradient bg, centered content, large heading (text-4xl), subtext
- **Footer**: surface bg with border-t, links in muted text

## Integration Notes

- **Don't overwrite**: If `tailwind.config.js` already exists, use the Edit tool to add only the `extend` section. Preserve everything else.
- **Check for conflicts**: If the project already defines `colors.primary`, rename the template's colors to `colors.bui-primary` or ask the user.
- **Use `@apply` sparingly**: Prefer inline utility classes. Only use `@apply` for truly repeated patterns (3+ identical element sets).
- **Responsive**: Apply responsive variants based on template spacing scale. Typically: `px-4 md:px-6 lg:px-8`.

## Icon Integration with Tailwind

Fetch icons from **Iconify** (free, no API key needed). Map the template's icon source to the corresponding Iconify prefix:

| Template source | Iconify prefix | Example URL |
|----------------|---------------|-------------|
| lucide         | `lucide`       | `https://api.iconify.design/lucide/search.svg` |
| phosphor       | `ph`           | `https://api.iconify.design/ph/magnifying-glass.svg` |
| heroicons      | `heroicons-outline` / `heroicons-solid` | `https://api.iconify.design/heroicons-outline/search.svg` |
| feather        | `feather`      | `https://api.iconify.design/feather/search.svg` |
| tabler         | `tabler`       | `https://api.iconify.design/tabler/search.svg` |

```
# Fetch icon SVG from Iconify (returns raw SVG, ready to inline)
curl -s "https://api.iconify.design/lucide/search.svg?height=24"
```

Style the SVG icon with Tailwind utility classes:

```tsx
// Inline SVG from API response, styled with Tailwind
<svg
  className="w-5 h-5 text-text-muted hover:text-primary transition-colors duration-fast"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  strokeWidth={2}
  strokeLinecap="round"
  strokeLinejoin="round"
>
  <path d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z M21 21l-4.35-4.35" />
</svg>
```

Icon sizing follows the template's `icon_preferences.size` (typically 20px = `w-5 h-5`). Stroke width comes from the template's `icon_preferences.stroke_width`.

If the Iconify API is unreachable, fall back to `data/icon-fallback.json` for SVG path data.
