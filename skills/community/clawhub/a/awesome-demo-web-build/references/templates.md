# Project Blueprint System

> These blueprints are **conversation guides** for understanding user needs.
> NOT pre-generated templates to output directly.
>
> Use the Pages/Components lists to **ask questions** and confirm preferences.
> Then use **scaffolding commands** to bootstrap the project, inject DESIGN.md, and add components.

---

## Scaffolding Commands

### Framework
| Framework | Command |
|-----------|---------|
| Next.js | `npx create-next-app@latest` |
| Astro | `npm create astro@latest` |
| Vite | `npm create vite@latest` |

### UI Component Library
| UI Library | Command |
|-------------|---------|
| shadcn/ui (recommended) | `npx shadcn@latest init` |
| Chakra UI | `npm i @chakra-ui/react @emotion/react` |
| Mantine | `npm i @mantine/core @mantine/hooks` |
| Ant Design | `npm i antd` |

### Icon Library
| Icon Library | Command / Usage |
|-------------|-----------------|
| **Lucide React** (recommended) | `npm install lucide-react` (built into shadcn) |
| **Iconfont** | `npm install @iconfont/react` + create project at iconfont.cn to get symbol URL |
| **Heroicons** | `npm install @heroicons/react` |
| **Phosphor Icons** | `npm install @phosphor-icons/react` |
| **Font Awesome** | `npm install @fortawesome/react-fontawesome` |

### Iconfont Usage

1. Create a project at [iconfont.cn](https://iconfont.cn) to get Symbol URL
2. Add to `app/layout.tsx` or `index.html`:

```html
<script src="https:////at.alicdn.com/t/font_xxx.js"></script>
```

3. Use the component:

```tsx
// React
<svg className="icon" aria-hidden="true">
  <use href="#icon-xxx" />
</svg>

// Or use @iconfont/react
import { Icon } from '@iconfont/react'
<Icon type="xxx" />
```

4. Add to tailwind.config.ts:

```js
theme: {
  extend: {
    width: {
      'icon': '1em',
      'icon-sm': '0.75em',
      'icon-lg': '1.25em',
    },
    height: {
      'icon': '1em',
      'icon-sm': '0.75em',
      'icon-lg': '1.25em',
    },
  },
}
```

### Default Stack Strategy
- **Next.js** → shadcn/ui + Tailwind CSS + Lucide React
- **Astro** → Minimal shadcn islands or pure Tailwind + Lucide React
- **Chinese icons needed** → Iconfont (Alibaba)

---

## Project Generation Workflow

```
1. Clarify requirements (type, pages, components, design)
2. Run scaffolding command (framework + UI library)
3. Inject DESIGN.md into project root
4. Install project-specific dependencies
5. Add shadcn/ui components: button, input, card, etc.
6. Generate blueprint components
7. Apply design tokens to tailwind.config.ts
```

---

## 1. ai-tool

**Typical products:** ChatGPT, Claude, Midjourney, AI writing assistant

### Scaffolding
```bash
# 1. Create project
npx create-next-app@latest my-ai-tool --typescript --tailwind --app --src-dir

# 2. Initialize shadcn/ui
cd my-ai-tool
npx shadcn@latest init

# 3. Add base components
npx shadcn@latest add button input card scroll-area

# 4. Install AI-related dependencies
npm install ai @ai-sdk/react zustand
```

### Pages
```
/chat          # Main chat page
/history       # Chat history
/settings      # Settings page
/new           # New chat
```

### Core Components
| Component | Description |
|-----------|-------------|
| `ChatInput` | AI input box, multiline support |
| `ChatMessage` | Message bubble, user/assistant distinction |
| `ChatStream` | Streaming output rendering |
| `ConversationList` | Sidebar history list |
| `ModelSelector` | Model dropdown selector |

### Design Priority
- **Input first** — Chat area takes the main space
- **Streaming feedback** — Typing effect
- **Dark theme** — Most AI tools prefer dark mode

---

## 2. dashboard

**Typical products:** GA Analytics, Admin panel, Data dashboard

### Scaffolding
```bash
# 1. Create project
npx create-next-app@latest my-dashboard --typescript --tailwind --app --src-dir

# 2. Initialize shadcn/ui
cd my-dashboard
npx shadcn@latest init

# 3. Add data-related components
npx shadcn@latest add button input card table dropdown-menu chart

# 4. Install data visualization
npm install recharts @tanstack/react-table zustand
```

### Pages
```
/dashboard      # Overview page (KPI cards)
/analytics      # Data analysis (charts)
/reports        # Reports (tables)
/[table]        # Data table (CRUD)
```

### Core Components
| Component | Description |
|-----------|-------------|
| `StatsCard` | KPI value card |
| `DataTable` | Table (filter/pagination/sort) |
| `Chart` | Chart (line/bar/pie) |
| `FilterBar` | Filter bar (date range) |
| `Sidebar` | Side navigation |

### Design Priority
- **Data density** — Compact information
- **Table first** — Core interaction is table
- **Chart-driven** — Explainable

---

## 3. landing-page

**Typical products:** Product homepage, campaign page, portfolio

### Scaffolding
```bash
# 1. Create project
npm create astro@latest my-landing --template minimal
cd my-landing
npx astro add tailwind

# 2. Pure Tailwind or minimal islands
npm install framer-motion clsx tailwind-merge
```

### Pages
```
/               # Single page (multiple sections)
```

### Sections
```
Hero → Features → SocialProof → Pricing → FAQ → CTA → Footer
```

### Core Components
| Component | Description |
|-----------|-------------|
| `Hero` | Large title + subtitle + CTA |
| `FeatureCard` | Feature card |
| `PricingTable` | Pricing table |
| `Testimonial` | User testimonial |
| `FAQ` | Accordion Q&A |

### Design Priority
- **Visual impact** — Above-fold decides conversion
- **Clear CTA** — Call to action in every section
- **Scroll narrative** — Single page scroll guide

---

## 4. saas-app

**Typical products:** Notion, Linear, Stripe, Slack

### Scaffolding
```bash
# 1. Create project
npx create-next-app@latest my-saas --typescript --tailwind --app --src-dir

# 2. Initialize shadcn/ui
cd my-saas
npx shadcn@latest init

# 3. Add common SaaS components
npx shadcn@latest add button input card dialog dropdown-menu tabs avatar badge separator command

# 4. Install auth and state
npm install @clerk/nextjs zustand @supabase/supabase-js
```

### Pages
```
/dashboard       # Workspace home
/[module]        # Module page (dynamic route)
/settings        # Settings
/settings/billing
/settings/team
/profile         # Profile
```

### Core Components
| Component | Description |
|-----------|-------------|
| `AppShell` | Overall layout (Sidebar + Header) |
| `Sidebar` | Navigation sidebar |
| `Header` | Top bar (breadcrumb, search) |
| `ModuleView` | Module main view |
| `CommandPalette` | Cmd+K command palette |

### Design Priority
- **Consistency** — Cross-module UI unified
- **Efficiency first** — Shortcuts, command palette
- **Information architecture** — Clear module division

---

## 5. content-site

**Typical products:** Blog, documentation site, knowledge base

### Scaffolding
```bash
# 1. Create project
npx create-next-app@latest my-blog --typescript --tailwind --app --src-dir

# 2. Initialize shadcn/ui
cd my-blog
npx shadcn@latest init

# 3. Add content-related components
npx shadcn@latest add button card badge separator scroll-area

# 4. Install content processing
npm install next-mdx-remote gray-matter fuse.js date-fns
```

### Pages
```
/                # Home (article list)
/blog            # Blog list
/blog/[slug]     # Article detail
/docs            # Docs list
/docs/[slug]      # Doc page
/search          # Search
/category/[cat]   # Category page
```

### Core Components
| Component | Description |
|-----------|-------------|
| `PostCard` | Article card |
| `MdxContent` | Markdown rendering |
| `TableOfContents` | Article TOC |
| `SearchBar` | Search box |
| `TagList` | Tag list |
| `Pagination` | Paginator |

### Design Priority
- **Readability** — Comfortable line height, clear typography
- **Navigation** — Breadcrumb, sidebar TOC
- **SEO** — meta, sitemap

---

## 6. tool

**Typical products:** JSON formatter, image compressor, code highlighter

### Scaffolding
```bash
# 1. Create project
npx create-next-app@latest my-tool --typescript --tailwind --app --src-dir

# 2. Initialize shadcn/ui
cd my-tool
npx shadcn@latest init

# 3. Add tool-related components
npx shadcn@latest add button input card dropdown-menu

# 4. Install tool dependencies
npm install @uiw/react-codemirror clsx tailwind-merge
```

### Pages
```
/               # Tool home page or single page
/[tool]         # Tool page (input → output)
```

### Core Components
| Component | Description |
|-----------|-------------|
| `ToolInput` | Input area (Textarea/Dropzone) |
| `ToolOutput` | Output area (result display) |
| `ToolOptions` | Options config |
| `CopyButton` | Copy to clipboard |
| `FormatSelect` | Format selection |

### Design Priority
- **Input/Output** — Left input, right output
- **Instant feedback** — Show when processing completes
- **Minimal** — No navigation needed

---

## Extended Types

### 7. e-commerce
```bash
npx create-next-app@latest my-shop --typescript --tailwind --app --src-dir
cd my-shop
npx shadcn@latest init
npx shadcn@latest add button input card badge carousel separator
npm install @stripe/stripe-js @supabase/supabase-js zustand
```

### 8. community
```bash
npx create-next-app@latest my-community --typescript --tailwind --app --src-dir
cd my-community
npx shadcn@latest init
npx shadcn@latest add button input card avatar badge comment
npm install @supabase/supabase-js date-fns
```

### 9. marketplace
```bash
npx create-next-app@latest my-market --typescript --tailwind --app --src-dir
cd my-market
npx shadcn@latest init
npx shadcn@latest add button input card avatar badge search command
npm install @supabase/supabase-js zustand fuse.js
```

---

## shadcn/ui Components Reference

| Category | Components |
|----------|------------|
| Basic | `button`, `input`, `label`, `badge` |
| Layout | `card`, `sheet`, `separator`, `scroll-area` |
| Navigation | `sidebar`, `tabs`, `menu`, `command` |
| Data | `table`, `chart`, `progress` |
| Feedback | `dialog`, `alert`, `toast`, `skeleton` |
| Form | `form`, `select`, `checkbox`, `radio-group` |
| Data Input | `textarea`, `switch`, `slider`, `date-picker` |

---

## Type → Design Priority

| Type | Design Priority |
|------|----------------|
| ai-tool | Input/Chat |
| dashboard | Data density |
| landing-page | Visual impact |
| saas-app | Consistency |
| content-site | Readability |
| tool | Minimal & efficient |

---

## Auto-Inference Examples

```
User: "Build me a ChatGPT clone"
→ Framework: Next.js
→ UI: shadcn/ui
→ Pages: /chat
→ Components: ChatInput, ChatMessage
→ Design: claude

User: "Something like Notion"
→ Framework: Next.js
→ UI: shadcn/ui
→ Pages: /dashboard, /[module], /settings
→ Components: AppShell, Sidebar
→ Design: minimal

User: "Data analytics admin panel"
→ Framework: Next.js
→ UI: shadcn/ui + Recharts
→ Pages: /dashboard, /analytics
→ Components: StatsCard, DataTable, Chart
→ Design: linear
```
