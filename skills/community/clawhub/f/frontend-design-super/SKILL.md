---
name: frontend-design-ultimate
description: Create distinctive, production-grade static sites with React, Vue 3, Nuxt.js, Tailwind CSS, and shadcn/ui — no mockups needed. Generates bold, memorable designs from plain text requirements with anti-AI-slop aesthetics, mobile-first responsive patterns, and single-file bundling. Supports cross-framework development (React/Vue 3/Nuxt) with consistent design patterns. Use when building landing pages, marketing sites, portfolios, dashboards, or any static web UI.
homepage: https://github.com/kesslerio/frontend-design-ultimate-clawhub-skill
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["node", "npm"]
---

# Frontend Design Ultimate

Create distinctive, production-grade static sites from text requirements alone. No mockups, no Figma — just describe what you want and get bold, memorable designs.

**Cross-Framework Support**: React 18 | Vue 3 | Nuxt 3  
**Styling**: Tailwind CSS + shadcn/ui (or framework equivalents)  
**Output**: Vite (static HTML) or Framework-specific deployment

## Quick Start

```
"Build a SaaS landing page for an AI writing tool. Dark theme, 
editorial typography, subtle grain texture. Use Vue 3. Pages: hero with 
animated demo, features grid, pricing table, FAQ accordion, footer."
```

---

## Framework Selection Guide

Choose the right framework for your project:

| Framework | Best For | Deployment | Learning Curve |
|-----------|----------|------------|----------------|
| **React + Vite** | SPAs, interactive apps, React ecosystem | Static/CDN | Medium |
| **React + Next.js** | SEO-critical sites, SSR needed | Vercel/Node | Medium-High |
| **Vue 3 + Vite** | Progressive apps, easier learning curve | Static/CDN | Low |
| **Nuxt 3** | SEO-critical, full-stack Vue, SSR/SSG | Vercel/Netlify/Node | Low-Medium |

### Quick Commands

**TypeScript Versions (Original):**
```bash
# React + Vite (Pure Static)
bash scripts/init-vite.sh my-react-site

# React + Next.js (Vercel Deploy)
bash scripts/init-nextjs.sh my-next-site

# Vue 3 + Vite (Pure Static)
bash scripts/init-vue-vite.sh my-vue-site

# Nuxt 3 (SSR/SSG)
bash scripts/init-nuxt.sh my-nuxt-site
```

**JavaScript Versions (New - JavaScript Runtime Compatible):**
```bash
# React + Vite (Pure Static) - JavaScript
bash scripts/init-vite-js.sh my-react-site

# React + Next.js (Vercel Deploy) - JavaScript
bash scripts/init-nextjs-js.sh my-next-site

# Vue 3 + Vite (Pure Static) - JavaScript
bash scripts/init-vue-vite-js.sh my-vue-site

# Nuxt 3 (SSR/SSG) - JavaScript
bash scripts/init-nuxt-js.sh my-nuxt-site
```

> **Note**: JavaScript versions provide full compatibility with pure JavaScript runtimes while maintaining all original functionality, design patterns, and user experience.

---

## Design Thinking (Do This First)

Before writing any code, commit to a **BOLD aesthetic direction**:

### 1. Understand Context
- **Purpose**: What problem does this interface solve? Who uses it?
- **Audience**: Developer tools? Consumer app? Enterprise? Creative agency?
- **Constraints**: Performance requirements, accessibility needs, brand guidelines?

### 2. Choose an Extreme Tone
Pick ONE and commit fully — timid designs fail:

| Tone | Characteristics |
|------|-----------------|
| **Brutally Minimal** | Sparse, monochrome, massive typography, raw edges |
| **Maximalist Chaos** | Layered, dense, overlapping elements, controlled disorder |
| **Retro-Futuristic** | Neon accents, geometric shapes, CRT aesthetics |
| **Organic/Natural** | Soft curves, earth tones, hand-drawn elements |
| **Luxury/Refined** | Subtle animations, premium typography, restrained palette |
| **Editorial/Magazine** | Strong grid, dramatic headlines, whitespace as feature |
| **Brutalist/Raw** | Exposed structure, harsh contrasts, anti-design |
| **Art Deco/Geometric** | Gold accents, symmetry, ornate patterns |
| **Soft/Pastel** | Rounded corners, gentle gradients, friendly |
| **Industrial/Utilitarian** | Functional, monospace, data-dense |

### 3. Define the Unforgettable Element
What's the ONE thing someone will remember? A hero animation? Typography treatment? Color combination? Unusual layout?

---

## Aesthetics Guidelines (Framework-Agnostic)

These principles apply to ALL frameworks:

### Typography — NEVER Generic

**BANNED**: Inter, Roboto, Arial, system fonts, Open Sans

**DO**: Distinctive, characterful choices that elevate the design.

| Use Case | Approach |
|----------|----------|
| Display/Headlines | Bold personality — Clash, Cabinet Grotesk, Satoshi, Space Grotesk (sparingly), Playfair Display |
| Body Text | Refined readability — Instrument Sans, General Sans, Plus Jakarta Sans |
| Monospace/Code | DM Mono, JetBrains Mono, IBM Plex Mono |
| Pairing Strategy | Contrast weights (thin display + bold body), contrast styles (serif + geometric sans) |

**Size Progression**: Use 3x+ jumps, not timid 1.5x increments.

### Color & Theme

**BANNED**: Purple gradients on white, evenly-distributed 5-color palettes

**DO**:
- **Dominant + Sharp Accent**: 70-20-10 rule (primary-secondary-accent)
- **CSS Variables**: `--primary`, `--accent`, `--surface`, `--text`
- **Commit to dark OR light**: Don't hedge with gray middle-grounds
- **High contrast CTAs**: Buttons should pop dramatically

```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #141414;
  --text-primary: #fafafa;
  --text-secondary: #a1a1a1;
  --accent: #ff6b35;
  --accent-hover: #ff8555;
}
```

### Motion & Animation

**Priority**: One orchestrated page load > scattered micro-interactions

**High-Impact Moments**:
- Staggered hero reveals (`animation-delay`)
- Scroll-triggered section entrances
- Hover states that surprise (scale, color shift, shadow depth)
- Smooth page transitions

**Implementation by Framework**:
- **React**: Framer Motion (`motion.div`, `AnimatePresence`)
- **Vue 3**: @vueuse/motion (`v-motion`, `useMotion`)
- **Nuxt 3**: @vueuse/motion (auto-imported) or @nuxt/animations

**Keep durations 200-400ms** (snappy, not sluggish)

### Spatial Composition

**BANNED**: Centered, symmetrical, predictable layouts

**DO**:
- Asymmetry with purpose
- Overlapping elements
- Diagonal flow / grid-breaking
- Generous negative space OR controlled density (pick one)
- Off-grid hero sections

### Backgrounds & Atmosphere

**BANNED**: Solid white/gray backgrounds

**DO**:
- Gradient meshes (subtle, not garish)
- Noise/grain textures (SVG filter or CSS)
- Geometric patterns (dots, lines, shapes)
- Layered transparencies
- Dramatic shadows for depth
- Blur effects for glassmorphism

```css
/* Subtle grain overlay */
.grain::before {
  content: '';
  position: fixed;
  inset: 0;
  background: url("data:image/svg+xml,...") repeat;
  opacity: 0.03;
  pointer-events: none;
}
```

---

## Mobile-First Patterns (Framework-Agnostic)

See **[references/mobile-patterns.md](references/mobile-patterns.md)** for detailed CSS.

### Critical Rules

| Pattern | Desktop | Mobile Fix |
|---------|---------|------------|
| Hero with hidden visual | 2-column grid | Switch to `display: flex` (not grid) |
| Large selection lists | Horizontal scroll | Accordion with category headers |
| Multi-column forms | Side-by-side | Stack vertically |
| Status/alert cards | Inline | `align-items: center` + `text-align: center` |
| Feature grids | 3-4 columns | Single column |

### Breakpoints

```css
/* Tablet - stack sidebars */
@media (max-width: 1200px) { }

/* Mobile - full single column */
@media (max-width: 768px) { }

/* Small mobile - compact spacing */
@media (max-width: 480px) { }
```

### Font Scaling

```css
@media (max-width: 768px) {
  .hero-title { font-size: 32px; }      /* from ~48px */
  .section-title { font-size: 24px; }   /* from ~32px */
  .section-subtitle { font-size: 14px; } /* from ~16px */
}
```

---

## Framework-Specific Workflows

### Option A: React + Vite (Pure Static)

```bash
# 1. Initialize
bash scripts/init-vite.sh my-site
cd my-site

# 2. Develop
npm run dev

# 3. Build static files
npm run build
# Output: dist/

# 4. Bundle to single HTML (optional)
bash scripts/bundle-artifact.sh
# Output: bundle.html
```

**Key Libraries**:
- `framer-motion` for animations
- `@radix-ui/react-*` for accessible components
- `lucide-react` for icons

**Component Pattern** (React):
```tsx
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'

export function Hero() {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Button size="lg">Get Started</Button>
    </motion.section>
  )
}
```

### Option B: React + Next.js (Vercel Deploy)

```bash
# 1. Initialize
bash scripts/init-nextjs.sh my-site
cd my-site

# 2. Develop
npm run dev

# 3. Deploy to Vercel
vercel
```

**Next.js-Specific Features**:
- App Router (`app/` directory)
- Server Components (use `'use client'` for interactive parts)
- Image optimization (`next/image`)
- Metadata API for SEO

**Component Pattern** (Next.js):
```tsx
'use client'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'

export default function Hero() {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Button size="lg">Get Started</Button>
    </motion.section>
  )
}
```

### Option C: Vue 3 + Vite (Pure Static)

```bash
# 1. Initialize
bash scripts/init-vue-vite.sh my-site
cd my-site

# 2. Develop
npm run dev

# 3. Build static files
npm run build
# Output: dist/
```

**Key Libraries**:
- `@vueuse/motion` for animations
- `radix-vue` for accessible components
- `lucide-vue-next` for icons
- `shadcn-vue` for UI components

**Component Pattern** (Vue 3):
```vue
<script setup lang="ts">
import { Motion } from '@vueuse/motion'
import Button from '@/components/ui/Button.vue'
</script>

<template>
  <section
    v-motion
    :initial="{ opacity: 0, y: 20 }"
    :enter="{ opacity: 1, y: 0 }"
    :duration="500"
  >
    <Button size="lg">Get Started</Button>
  </section>
</template>
```

### Option D: Nuxt 3 (SSR/SSG)

```bash
# 1. Initialize
bash scripts/init-nuxt.sh my-site
cd my-site

# 2. Develop
npm run dev

# 3. Generate static site
npm run generate
# Output: .output/public/

# 4. Deploy
npx nuxi deploy
```

**Nuxt-Specific Features**:
- File-based routing (`pages/`)
- Auto-imports (components, composables, utils)
- `@nuxt/ui` component library (UButton, UCard, etc.)
- Built-in SEO with `useHead()` and `useSeoMeta()`

**Component Pattern** (Nuxt 3):
```vue
<script setup lang="ts">
import { siteConfig } from '~/config/site'

useHead({
  title: `${siteConfig.name} - ${siteConfig.tagline}`
})
</script>

<template>
  <section
    v-motion
    :initial="{ opacity: 0, y: 20 }"
    :enter="{ opacity: 1, y: 0 }"
  >
    <UButton size="xl" :to="/signup">Get Started</UButton>
  </section>
</template>
```

---

## Project Structures

### React + Vite
```
my-site/
├── src/
│   ├── components/     # React components (.tsx)
│   ├── lib/           # Utilities, cn()
│   ├── styles/        # Global CSS
│   ├── config/
│   │   └── site.ts    # Editable content config
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── tailwind.config.ts
└── package.json
```

### React + Next.js
```
my-site/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── privacy/page.tsx
├── components/
├── lib/
├── config/
│   └── site.ts
└── tailwind.config.ts
```

### Vue 3 + Vite
```
my-site/
├── src/
│   ├── components/     # Vue components (.vue)
│   │   └── ui/        # shadcn-vue components
│   ├── lib/           # Utilities, cn()
│   ├── assets/        # CSS, images
│   ├── plugins/       # Vue plugins
│   ├── config/
│   │   └── site.ts    # Editable content config
│   ├── App.vue
│   └── main.ts
├── index.html
├── tailwind.config.ts
└── package.json
```

### Nuxt 3
```
my-site/
├── app.vue              # Root component
├── pages/               # File-based routing
│   └── index.vue
├── layouts/             # Layout components
│   └── default.vue
├── components/          # Auto-imported components
├── composables/         # Auto-imported composables
├── config/              # Site configuration
│   └── site.ts
├── assets/css/          # Global CSS
├── nuxt.config.ts
├── tailwind.config.ts
└── package.json
```

---

## Site Config Pattern (Universal)

Keep all editable content in one file — works across all frameworks:

```typescript
// config/site.ts (or ~/config/site.ts for Nuxt)
export const siteConfig = {
  name: "Acme AI",
  tagline: "Write better, faster",
  description: "AI-powered writing assistant",
  
  hero: {
    badge: "Now in beta",
    title: "Your words,\nsupercharged",
    subtitle: "Write 10x faster with AI that understands your style",
    cta: { text: "Get Started", href: "/signup" },
    secondaryCta: { text: "Watch Demo", href: "#demo" },
  },
  
  features: [
    { icon: "Zap", title: "Lightning Fast", description: "..." },
    // ...
  ],
  
  pricing: [
    { name: "Free", price: 0, features: [...] },
    { name: "Pro", price: 19, features: [...], popular: true },
  ],
  
  faq: [
    { q: "How does it work?", a: "..." },
  ],
  
  footer: {
    links: [...],
    social: [...],
  }
}
```

---

## Component Library Mapping

Each framework has its own component library with similar APIs:

| Component | React (shadcn/ui) | Vue 3 (shadcn-vue) | Nuxt 3 (@nuxt/ui) |
|-----------|-------------------|---------------------|---------------------|
| Button | `<Button>` | `<Button />` | `<UButton />` |
| Card | `<Card>` | `<Card />` | `<UCard />` |
| Badge | `<Badge>` | `<Badge />` | `<UBadge />` |
| Accordion | `<Accordion>` | `<Accordion />` | `<UAccordion />` |
| Dialog/Modal | `<Dialog>` | `<Dialog />` | `<UModal />` |
| Navigation | `<NavigationMenu>` | `<NavigationMenu />` | `<UNavigationMenu />` |
| Tabs | `<Tabs>` | `<Tabs />` | `<UTabs />` |
| Sheet/Drawer | `<Sheet>` | `<Sheet />` | `<USheet />` |
| Avatar | `<Avatar>` | `<Avatar />` | `<UAvatar />` |
| Alert | `<Alert>` | `<Alert />` | `<UAlert />` |

**Installation by Framework**:

```bash
# React
npx shadcn@latest add button card badge accordion dialog navigation-menu tabs sheet separator avatar alert

# Vue 3
npx shadcn-vue@latest add button card badge accordion dialog navigation-menu tabs sheet separator avatar alert

# Nuxt 3 (@nuxt/ui - auto-installed)
# All U* components are available automatically
```

---

## Animation Library Mapping

| Feature | React (Framer Motion) | Vue 3 (@vueuse/motion) | Nuxt 3 (@vueuse/motion) |
|---------|----------------------|------------------------|--------------------------|
| Basic animation | `<motion.div>` | `v-motion` directive | `v-motion` directive |
| Page transitions | `AnimatePresence` | `<Transition>` | `<Transition>` (built-in) |
| Scroll triggers | `whileInView` | `useScroll` composable | `useScroll` composable |
| Gestures | `whileHover`, `whileTap` | Event bindings | Event bindings |
| Stagger children | `staggerChildren` | Config-based | Config-based |

### Cross-Framework Animation Example

**React**:
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

**Vue 3**:
```vue
<div
  v-motion
  :initial="{ opacity: 0, y: 20 }"
  :enter="{ opacity: 1, y: 0 }"
  :duration="500"
>
  Content
</div>
```

**Nuxt 3**:
```vue
<div
  v-motion
  :initial="{ opacity: 0, y: 20 }"
  :visible="{ opacity: 1, y: 0 }"
  :duration="500"
>
  Content
</div>
```

---

## Pre-Implementation Checklist

Run this before finalizing any design:

### Design Quality (Framework-Agnostic)
- [ ] Typography is distinctive (no Inter/Roboto/Arial)
- [ ] Color palette has clear dominant + accent (not evenly distributed)
- [ ] Background has atmosphere (not solid white/gray)
- [ ] At least one memorable/unforgettable element
- [ ] Animations are orchestrated (not scattered)

### Mobile Responsiveness (Framework-Agnostic)
- [ ] Hero centers on mobile (no empty grid space)
- [ ] All grids collapse to single column
- [ ] Forms stack vertically
- [ ] Large lists use accordion (not horizontal scroll)
- [ ] Font sizes scale down appropriately

### Form Consistency
- [ ] Input, select, textarea all styled consistently
- [ ] Radio/checkbox visible (check transparent-border styles)
- [ ] Dropdown options have readable backgrounds
- [ ] Labels use CSS variables (not hardcoded colors)

### Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Focus states visible
- [ ] Semantic HTML (nav, main, section, article)
- [ ] Alt text for images
- [ ] Keyboard navigation works

### Framework-Specific
- [ ] Using correct component imports for chosen framework
- [ ] Animations use framework-appropriate library
- [ ] Build configuration matches target framework
- [ ] TypeScript types properly configured

---

## Cross-Framework Consistency Guarantees

This skill ensures consistency across frameworks:

✅ **Design System**: Same color variables, typography scale, spacing tokens  
✅ **Responsive Patterns**: Same mobile-first breakpoints and behaviors  
✅ **Animation Timing**: Same durations (200-400ms), easing functions  
✅ **Component APIs**: Similar props and event handling patterns  
✅ **File Organization**: Logical structure adapted per framework conventions  
✅ **Performance**: Optimized bundle sizes, lazy loading strategies  

**What Adapts Per Framework**:
- Syntax (JSX vs Template)
- Import paths (@/ vs ~/ vs relative)
- Component names (PascalCase vs kebab-case)
- State management (useState vs ref/reactive)
- Lifecycle hooks (useEffect vs onMounted/watch)
- Routing (React Router vs Vue Router vs file-based)

---

## References

- **[references/design-philosophy.md](references/design-philosophy.md)** — Extended anti-AI-slop guidance
- **[references/mobile-patterns.md](references/mobile-patterns.md)** — Detailed responsive CSS
- **[references/shadcn-components.md](references/shadcn-components.md)** — Component quick reference (React-focused)
- **[templates/site-config.ts](templates/site-config.ts)** — Full siteConfig example
- **Framework Guides**:
  - React: See init-vite.sh and init-nextjs.sh output
  - Vue 3: See init-vue-vite.sh output
  - Nuxt 3: See init-nuxt.sh output

---

## Examples

### Prompt → Multi-Framework Output

**Input**:
> "Portfolio site for a photographer. Minimal, editorial feel. 
> Grid gallery with lightbox, about section, contact form."

**Design Decisions** (Same for all frameworks):
- Tone: Editorial/Magazine
- Typography: Cormorant Garamond (display) + Plus Jakarta Sans (body)
- Color: Near-black bg (#0c0c0c), warm white text (#f5f5f0), copper accent (#b87333)
- Unforgettable: Full-bleed hero image with text overlay that reveals on scroll
- Motion: Gallery images fade in staggered on scroll

**Output Options**:
- **React + Vite**: Complete Vite project with responsive gallery, lightbox component
- **React + Next.js**: Next.js App Router with image optimization
- **Vue 3 + Vite**: Vue 3 composition API with reactive gallery state
- **Nuxt 3**: Nuxt 3 with auto-imports, SEO metadata, static generation

All outputs maintain identical visual design and user experience.

---

## Migration Guide

### Converting Between Frameworks

**React → Vue 3**:
- `useState` → `ref()` or `reactive()`
- `useEffect` → `onMounted()` + `watch()`
- JSX → Vue template syntax
- `className` → `class`
- `onClick` → `@click`
- `{variable}` → `{{ variable }}`

**Vue 3 → Nuxt 3**:
- Move `src/` contents to root level
- Replace `vue-router` with `pages/` directory
- Replace manual imports with auto-imports
- Add `~/` alias for root imports
- Use `useHead()` instead of manual `<head>`

**React → Nuxt 3**:
- Convert JSX to Vue templates
- Replace React hooks with Vue composition API
- Move to file-based routing
- Use Nuxt-specific modules (@nuxt/image, etc.)

---

*Based on Anthropic's frontend-design, web-artifacts-builder, and community frontend-design-v2 skills. Enhanced with cross-framework support for modern frontend development.*
