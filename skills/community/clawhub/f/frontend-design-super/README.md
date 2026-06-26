# Frontend Design Ultimate

🎨 Create distinctive, production-grade static sites with React, Vue 3, Nuxt.js, Tailwind CSS, and shadcn/ui — no mockups needed.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-frontend--design--ultimate-purple)](https://clawhub.ai/skills/frontend-design-ultimate)
![Frameworks](https://img.shields.io/badge/Frameworks-React%20%7C%20Vue%203%20%7C%20Nuxt%203-blue)

## What is this?

An OpenClaw/Claude Code skill that generates bold, memorable web designs from plain text requirements. No Figma, no wireframes — just describe what you want.

**Now with Cross-Framework Support!** 🚀

Build your projects using:
- **React 18** (Vite or Next.js)
- **Vue 3** (Vite)
- **Nuxt 3** (SSR/SSG)

All frameworks maintain identical design quality and user experience.

## Key Features

- 🚫 **Anti-AI-slop** — Explicit guidance to avoid generic designs (no Inter, no purple gradients, no centered layouts)
- 📱 **Mobile-first patterns** — Responsive CSS that actually works
- ⚡ **Multiple frameworks** — React, Vue 3, Nuxt 3 with consistent patterns
- 🧩 **Component libraries** — shadcn/ui (React), shadcn-vue (Vue), @nuxt/ui (Nuxt)
- 🎬 **Framework-appropriate animations** — Framer Motion, @vueuse/motion
- 📦 **Single-file bundling** — Bundle entire sites to one HTML file (React/Vite only)
- 🔀 **Easy migration** — Convert between frameworks with documented patterns

## Quick Start

### Install the Skill

```bash
# OpenClaw
openclaw skill install frontend-design-ultimate

# Claude Code (copy to .claude/skills/)
git clone https://github.com/kesslerio/frontend-design-ultimate-clawhub-skill.git ~/.claude/skills/frontend-design-ultimate
```

### Use It

Just describe what you want and specify your framework:

```
Build a SaaS landing page for an AI writing tool using Vue 3. Dark theme, 
editorial typography, subtle grain texture. Pages: hero with 
animated demo, features grid, pricing table, FAQ accordion, footer.
```

The skill will:
1. Detect the requested framework (or default to React)
2. Commit to a bold aesthetic direction
3. Choose distinctive typography (no Inter!)
4. Build with the specified framework + Tailwind + component library
5. Apply mobile-first responsive patterns
6. Output production-ready code

## Framework Options

| Framework | Command | Best For | Deployment |
|-----------|---------|----------|------------|
| **React + Vite** | `bash scripts/init-vite.sh my-site` | SPAs, interactive apps | Static/CDN |
| **React + Next.js** | `bash scripts/init-nextjs.sh my-site` | SEO-critical, SSR needed | Vercel |
| **Vue 3 + Vite** | `bash scripts/init-vue-vite.sh my-site` | Progressive apps, easier learning curve | Static/CDN |
| **Nuxt 3** | `bash scripts/init-nuxt.sh my-site` | SEO-critical, full-stack Vue | Vercel/Netlify |

## What Makes This Different?

### vs. Generic AI Design
| Generic AI | This Skill |
|------------|------------|
| Inter font everywhere | Distinctive typography choices |
| Purple gradients | Context-appropriate palettes |
| Centered layouts | Intentional spatial composition |
| No animations | Orchestrated motion |
| Solid backgrounds | Atmospheric textures |

### Cross-Framework Consistency
| Feature | React | Vue 3 | Nuxt 3 |
|---------|-------|-------|--------|
| Design System | ✅ Identical | ✅ Identical | ✅ Identical |
| Responsive Patterns | ✅ Same | ✅ Same | ✅ Same |
| Animation Timing | ✅ Consistent | ✅ Consistent | ✅ Consistent |
| Component APIs | ✅ Similar | ✅ Similar | ✅ Similar |
| Performance | ✅ Optimized | ✅ Optimized | ✅ Optimized |

## Workflows

### Option A: React + Vite (Pure Static)
```bash
bash scripts/init-vite.sh my-site
cd my-site
npm run dev

# Build
npm run build

# Bundle to single HTML
bash scripts/bundle-artifact.sh
```

### Option B: React + Next.js (Vercel)
```bash
bash scripts/init-nextjs.sh my-site
cd my-site
npm run dev

# Deploy
vercel
```

### Option C: Vue 3 + Vite (Static SPA)
```bash
bash scripts/init-vue-vite.sh my-site
cd my-vue-site
npm run dev

# Build
npm run build
```

### Option D: Nuxt 3 (SSR/SSG)
```bash
bash scripts/init-nuxt.sh my-site
cd my-nuxt-site
npm run dev

# Generate static site
npm run generate

# Deploy
npx nuxi deploy
```

## Component Libraries by Framework

Each framework uses its own component library with similar APIs:

| Component | React (shadcn/ui) | Vue 3 (shadcn-vue) | Nuxt 3 (@nuxt/ui) |
|-----------|-------------------|---------------------|---------------------|
| Button | `<Button>` | `<Button />` | `<UButton />` |
| Card | `<Card>` | `<Card />` | `<UCard />` |
| Badge | `<Badge>` | `<Badge />` | `<UBadge />` |
| Accordion | `<Accordion>` | `<Accordion />` | `<UAccordion />` |
| Dialog/Modal | `<Dialog>` | `<Dialog />` | `<UModal />` |
| Navigation | `<NavigationMenu>` | `<NavigationMenu />` | `<UNavigationMenu />` |
| Tabs | `<Tabs>` | `<Tabs />` | `<UTabs />` |
| Avatar | `<Avatar>` | `<Avatar />` | `<UAvatar />` |

## Animation Libraries

| Framework | Library | Syntax |
|-----------|---------|--------|
| React | Framer Motion | `<motion.div initial={{...}} animate={{...}}>` |
| Vue 3 | @vueuse/motion | `<div v-motion :initial="{...}" :enter="{...}">` |
| Nuxt 3 | @vueuse/motion (auto-imported) | Same as Vue 3 |

## Documentation

### Core Documentation
- [SKILL.md](SKILL.md) — Main skill instructions with cross-framework support
- [references/design-philosophy.md](references/design-philosophy.md) — Anti-AI-slop manifesto
- [references/mobile-patterns.md](references/mobile-patterns.md) — Responsive CSS patterns
- [references/shadcn-components.md](references/shadcn-components.md) — Component quick reference (React-focused)
- **[references/cross-framework-guide.md](references/cross-framework-guide.md)** — 🆕 Complete cross-framework integration guide

### Templates & Configs
- [templates/site-config.ts](templates/site-config.ts) — Editable content config example

### Framework-Specific Guides
Each init script outputs detailed setup instructions:
- `scripts/init-vite.sh` → React + Vite setup guide
- `scripts/init-nextjs.sh` → React + Next.js setup guide  
- `scripts/init-vue-vite.sh` → Vue 3 + Vite setup guide
- `scripts/init-nuxt.sh` → Nuxt 3 setup guide

## Migration Guide

Converting between frameworks is well-documented:

```bash
# See the complete migration examples in:
# references/cross-framework-guide.md#migration-examples
```

**Quick Reference**:
- **React → Vue 3**: `useState` → `ref()`, JSX → templates, `onClick` → `@click`
- **Vue 3 → Nuxt 3**: Move to root level, use auto-imports, add `~/` alias
- **React → Nuxt 3**: Convert to Vue templates, use file-based routing

## Project Structure Examples

### All Frameworks Share:
- ✅ Same site config pattern (`config/site.ts`)
- ✅ Same Tailwind theme configuration
- ✅ Same CSS variables and design tokens
- ✅ Same mobile-first responsive breakpoints
- ✅ Similar component organization

### Framework-Specific Structure:
See SKILL.md for detailed project structure comparison.

## Requirements

- Node.js 18+
- npm

## What's New in v1.0.0?

### 🎉 Cross-Framework Support
- ✅ Added Vue 3 + Vite workflow
- ✅ Added Nuxt 3 workflow  
- ✅ Updated SKILL.md with comprehensive multi-framework guidance
- ✅ Created cross-framework integration guide
- ✅ Added framework selection guide and decision matrix
- ✅ Documented component library mapping across frameworks
- ✅ Provided animation library mapping and examples
- ✅ Included migration guide between frameworks
- ✅ Ensured consistency guarantees across all frameworks

### Maintained from Original
- ✅ All original anti-AI-slop design principles
- ✅ Mobile-first responsive patterns
- ✅ Typography and color guidelines
- ✅ Animation best practices
- ✅ React + Vite and React + Next.js workflows (unchanged)

## License

Apache 2.0 — See [LICENSE](LICENSE)

## Credits

Built on the shoulders of:
- [Anthropic's Claude Skills](https://github.com/anthropics/skills)
- [shadcn/ui](https://ui.shadcn.com) - React components
- [shadcn-vue](https://www.shadcn-vue.com/) - Vue 3 components
- [@nuxt/ui](https://ui.nuxt.com) - Nuxt 3 components
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [@vueuse/motion](https://motion.vueuse.org/)
- [nhatmobile1's frontend-design-v2](https://github.com/nhatmobile1/claude-skills)

---

Made with 🎨 by [lx164](https://github.com/lx164/frontend-design-super-skill)

**Now supporting React · Vue 3 · Nuxt 3** — One skill, any framework.
