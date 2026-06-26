# DESIGN.md — Vercel-Inspired Minimal

**Style:** Minimal / Developer-focused / Editorial
**Use for:** SaaS dashboards, developer tools, landing pages

## Colors
```css
--color-bg: #000000;
--color-surface: #111111;
--color-border: #222222;
--color-text: #ffffff;
--color-muted: #666666;
--color-accent: #ffffff;  /* white on black is the accent */
--color-accent-subtle: #333333;
```

## Typography
```css
--font-sans: 'Geist', 'Inter', system-ui, sans-serif;
--font-mono: 'GeistMono', 'JetBrains Mono', monospace;
--text-xs: 12px; --text-sm: 14px; --text-base: 16px;
--text-lg: 18px; --text-xl: 24px; --text-2xl: 32px;
--text-3xl: 48px; --text-4xl: 64px;
```

## Spacing
8px grid — `--space-1` (4px) through `--space-24` (96px)

## Key Rules
- Dark backgrounds with white text throughout
- Mono font for labels, metadata, code
- Sans for headings and body
- Minimal border-radius (2-4px max)
- No decorative gradients — pure flat design
- Generous whitespace, tight typographic control
