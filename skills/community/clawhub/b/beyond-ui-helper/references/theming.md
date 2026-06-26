# Theming Beyond-UI

Beyond-UI styles every component with semantic Tailwind tokens. You can rely on the bundled default theme or override tokens to match your brand.

## Token map

| Token | Typical usage |
|-------|---------------|
| `primary` | Buttons, Sidebar active states, Dashboard header accents |
| `secondary` | Neutral surfaces, body text, card borders |
| `accent` | Supporting highlights, charts, secondary callouts |
| `danger` | Destructive actions, alert banners, critical badges |
| `success` | Confirmations, success badges, input success states |
| `warning` | Warning toasts, inline status chips |

## Using the default palette

Import `@beyondcorp/beyond-ui/dist/styles.css` and you get the fallback palette defined in `src/theme/default.ts`. This requires no Tailwind configuration.

## Overriding tokens with Tailwind

Add semantic colors to the host project's `tailwind.config.js`. Only override the keys you need; the rest continue to fall back to defaults.

```js
// tailwind.config.js
export default {
  content: [
    './src/**/*.{ts,tsx,js,jsx}',
    './node_modules/@beyondcorp/beyond-ui/dist/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f4f7ff',
          100: '#e4ebff',
          200: '#c2d0ff',
          300: '#94acff',
          400: '#5f7dff',
          500: '#3a5eff',
          600: '#1c3bec',
          700: '#132ac1',
          800: '#102394',
          900: '#0f1f6f',
          950: '#080f38',
        },
        secondary: {
          50: '#f5f6f7',
          500: '#344054',
          900: '#101828',
        },
        accent: {
          50: '#f0fdf4',
          400: '#34d399',
          700: '#047857',
        },
        danger: {
          500: '#ef4444',
          600: '#dc2626',
        },
        success: {
          500: '#22c55e',
          600: '#16a34a',
        },
        warning: {
          500: '#f59e0b',
          600: '#d97706',
        },
      },
    },
  },
};
```

After changes, restart Tailwind or the dev server. Sidebar, DashboardLayout, and all badges automatically pick up the new palette.

## Dashboard & Sidebar tips

- `DashboardLayout` composes `Sidebar` and `DashboardHeader`. Override `primary`/`secondary` tokens to recolor the shell.
- Use `sidebarMenuItems`, `activeSidebarItem`, and `onSidebarItemClick` props to manage navigation state.
- `Sidebar` exposes `className` and `headerClassName` for additional Tailwind utilities when building dark or high-contrast themes.
- Badges and status chips reflect `danger`, `success`, and `warning` tokens—update those scales for consistent feedback states.

## Gradual adoption

Teams can start with the compiled CSS only, then add Tailwind later if custom tokens or utilities are needed. Keep the CSS import in place even after bringing Tailwind into the host app so unmatched tokens continue to resolve.
