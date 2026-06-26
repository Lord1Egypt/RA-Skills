---
name: awesome-demo-web-build
description: AI-native web demo project generator using Project Blueprint system. Use when user wants to "build a demo", "create a web project", "generate a landing page", "make an AI tool UI", or similar requests.
---

# AI Web Demo Builder

## Interaction Style

**Must use selection + free-input for all questions.**

- Show **selectable options** first
- Always allow **custom input** as alternative
- Ask **one question at a time**
- Use **numbered choices** for easy selection

---

## Phase 1: Project Type

**Please select a project type:**

| # | Type | Description |
|---|------|-------------|
| 1 | AI Tool | ChatGPT, Claude, AI assistant |
| 2 | Dashboard | Analytics, admin panel |
| 3 | Landing Page | Product homepage, landing page |
| 4 | SaaS App | Notion, Linear multi-module app |
| 5 | Content Site | Blog, documentation site |
| 6 | Tool | JSON formatter, image processor |
| 7 | E-commerce | Online shop, shopping cart |
| 8 | Community | Forum, social community |
| 9 | Marketplace | Two-sided marketplace |

Enter a number or describe your requirements:

---

## Phase 2: Pages

**Please select pages (multiple choice, comma-separated):**

Display corresponding pages list based on `type`:

**AI Tool:** `/chat`, `/history`, `/settings`, `/new`
**Dashboard:** `/dashboard`, `/analytics`, `/reports`, `/[table]`
**SaaS App:** `/dashboard`, `/[module]`, `/settings`, `/profile`
**Landing Page:** `/` (single page)
**Content Site:** `/`, `/blog`, `/blog/[slug]`, `/docs`, `/search`

Enter numbers, multiple selections, or describe:

---

## Phase 3: Components

**Please select core components (multiple choice):**

Display corresponding components list based on `type`:

Example - AI Tool:
| # | Component | Description |
|---|-----------|-------------|
| 1 | ChatInput | AI input box |
| 2 | ChatMessage | Message bubble |
| 3 | ChatStream | Streaming output |
| 4 | ConversationList | History list |
| 5 | ModelSelector | Model selector |

Enter a number or describe the components you need:

---

## Phase 4: UI Library

**Please select a UI component library:**

| # | UI Library | Description |
|---|------------|-------------|
| 0 | Use recommended | shadcn/ui + Tailwind (default) |
| 1 | shadcn/ui | Highly customizable, Radix-based |
| 2 | Chakra UI | Fast prototyping, theme system |
| 3 | Mantine | Full-featured, modern feel |
| 4 | Ant Design | Enterprise admin, strict规范 |

Enter a number or specify another:

---

## Phase 5: Design Style

**Please select a design style:**

**Method 1: Choose from 57 presets**

| # | Design | Description |
|---|--------|-------------|
| 1 | claude | Claude AI style |
| 2 | linear | Linear dark & minimal |
| 3 | stripe | Stripe light & business |
| 4 | openai | OpenAI style |
| 5 | vercel | Vercel minimalist |
| ... | [Others 52](references/design-catalog.md) | Full list |

**Method 2: Provide a reference URL/screenshot**

Paste a URL or upload a screenshot, I will analyze and match the closest design style.

**Method 3: Custom description**

Describe the visual style you want, I will generate a DESIGN.md based on your description.

Enter a number, URL, or describe:

---

## Phase 6: Icon Library

**Please select an icon library (optional):**

| # | Icon Library | Description |
|---|--------------|-------------|
| 0 | Use recommended | Lucide React (default) |
| 1 | Lucide React | Modern & minimal, default option |
| 2 | Iconfont | Alibaba icon set, custom icons |
| 3 | Heroicons | Tailwind official icons |
| 4 | Phosphor Icons | Rich & diverse |
| 5 | No icons needed | - |

Enter a number or specify another:

---

## Project Summary (Confirmation)

```
Project Type: [type]
Pages: [pages]
Components: [components]
UI Library: [ui-library]
Design Style: [design]
Icon Library: [icon-library]

Scaffolding Command:
[command]

Is this correct? Enter "confirm" to start generating, or tell me what needs to be modified.
```

---

## Phase 7: Generate Project

After confirmation, execute:

**Step 1: Scaffolding**
```bash
npx create-next-app@latest my-project --typescript --tailwind --app --src-dir
cd my-project
npx shadcn@latest init
npx shadcn@latest add [components]
npm install [dependencies]
```

**Step 2: Inject DESIGN.md**
- WebFetch to get URL from design-catalog.md
- Write DESIGN.md to project root directory

**Step 3: Generate Code**
- Generate components based on blueprint
- Follow best-practices.md

---

## Output Structure

```
/project-name
├── app/                    # Next.js pages
├── components/
│   └── ui/                 # shadcn components
├── lib/                    # utils
├── DESIGN.md               # ← Injected design spec
├── tailwind.config.ts      # ← Applied design tokens
└── package.json
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/templates.md` | Blueprint definition (pages, components, scaffolding) |
| `references/design-catalog.md` | 57 design style URL mappings |
| `references/best-practices.md` | Tech stack best practices |
| `references/tech-catalog.md` | Tech documentation URL mappings |

---

## Key Principles

- **Selection + Free-input** — Options first, but allow custom input
- **One question at a time** — Only ask one dimension at a time
- **Confirmation before generate** — Generate only after confirmation
- **DESIGN.md lives in project** — Read design specs during AI coding
- **Use scaffolding CLI** — Don't generate from scratch
