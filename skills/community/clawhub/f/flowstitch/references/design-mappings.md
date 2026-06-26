# Design Mappings & Descriptors

Use these mappings to transform vague user requests into precise, high-fidelity design instructions for Stitch.

## UI/UX Keyword Refinement

| Vague Term | Enhanced Professional Terminology |
|:---|:---|
| "menu at the top" | "sticky navigation bar with logo and list items" |
| "big photo" | "high-impact hero section with full-width imagery" |
| "list of things" | "responsive card grid with hover states and subtle elevations" |
| "button" | "primary call-to-action button with micro-interactions" |
| "form" | "clean form with labeled input fields, validation states, and submit button" |
| "picture area" | "hero section with focal-point image or video background" |
| "sidebar" | "collapsible side navigation with icon-label pairings" |
| "popup" | "modal dialog with overlay and smooth entry animation" |
| "tabs" | "tabbed navigation with active state indicator" |
| "profile" | "user profile card with avatar, name, and action buttons" |
| "search" | "search bar with placeholder text, search icon, and focus expand" |
| "table" | "data table with sortable columns, row hover states, and pagination" |
| "progress" | "step indicator with numbered steps and active state highlighting" |
| "notification" | "toast notification with icon, message, and dismiss action" |

## Atmosphere & "Vibe" Descriptors

Add these adjectives to set the mood and aesthetic philosophy:

| Basic Vibe | Enhanced Design Description |
|:---|:---|
| "Modern" | "Clean, minimal, with generous whitespace and high-contrast typography." |
| "Professional" | "Sophisticated, trustworthy, utilizing subtle shadows and a restricted, premium palette." |
| "Fun / Playful" | "Vibrant, organic, with rounded corners, bold accent colors, and bouncy micro-animations." |
| "Dark Mode" | "Electric, high-contrast accents on deep slate or near-black backgrounds." |
| "Luxury" | "Elegant, spacious, with fine lines, editorial photography, and a curated palette." |
| "Tech / Cyber" | "Futuristic, neon accents, glassmorphism effects, and monospaced typography." |
| "Warm / Cozy" | "Earthy tones, generous padding, soft corners, artisanal and inviting." |
| "Minimal / Zen" | "Ultra-clean, extreme whitespace, single accent color, typography-driven." |
| "Data / Analytics" | "Information-dense, clear hierarchy, monospace numbers, subtle grid lines." |
| "SaaS / Startup" | "Clean, confident, purple/blue accents, bold headlines, feature-forward." |

## Geometry & Shape Translation

Convert technical values into physical descriptions for Stitch prompts:

- **Pill-shaped** — Used for `rounded-full` elements (buttons, tags, badges)
- **Softly rounded** — Used for `rounded-xl` (16px) or `rounded-2xl` (20px) containers
- **Gently rounded** — Used for `rounded-lg` (12px) cards and panels
- **Slightly rounded** — Used for `rounded-md` (8px) buttons and inputs
- **Sharp/Precise** — Used for `rounded-none` or `rounded-sm` elements
- **Glassmorphism** — Semi-transparent surfaces with background blur and thin borders

## Depth & Elevation Vocabulary

- **Flat** — No shadows, focus on color blocking and borders
- **Whisper-soft** — Diffused, very light shadows for subtle lift (`0 2px 8px rgba(0,0,0,0.06)`)
- **Gentle elevation** — Soft shadow on hover for cards (`0 4px 16px rgba(0,0,0,0.08)`)
- **Floating** — High-offset, soft shadows for elements above the surface
- **Inset** — Inner shadows for pressable or nested elements
- **Dramatic** — Heavy, visible shadows for bold UI statements

## Color Description Patterns

Always write colors as: **`Descriptive Name (#hexcode) for functional role`**

Examples:
- "Racing Red (#e11d48) for CTA buttons and active states"
- "Deep Obsidian (#0f172a) for background and text containers"
- "Warm Barely-There Cream (#FCFAFA) for page background"
- "Deep Muted Teal-Navy (#294056) for primary buttons and links"
- "Charcoal Near-Black (#2C2C2C) for headlines and body text"
- "Soft Warm Gray (#6B6B6B) for secondary text and labels"

## Platform & Device Defaults

| Context | Prompt addition |
|:---|:---|
| Web landing page | "Platform: Web, Desktop-first" |
| Mobile app (iOS) | "Platform: Mobile, iOS-first" |
| Mobile app (Android) | "Platform: Mobile, Android-first" |
| Dashboard | "Platform: Web, Desktop-first, data-dense" |
| Admin panel | "Platform: Web, Desktop-first, utilitarian" |
| Marketing site | "Platform: Web, Desktop-first, visual-heavy" |
| PWA | "Platform: Web, Mobile-first, app-like" |

---

## Admin Dashboard Design Vocabulary

| Vague | Dashboard-Specific Professional Term |
|:---|:---|
| "numbers at the top" | "KPI cards row with metric value, label, and trend indicator" |
| "the list of data" | "sortable data table with fixed header, striped rows, and pagination" |
| "menu on the left" | "collapsible sidebar navigation: 240px expanded / 60px icon-only" |
| "filter stuff" | "filter bar with search input, dropdown filters, and active filter chips" |
| "charts" | "chart section with bar/line chart, time range selector, and legend" |
| "small badges" | "semantic status badges: green/active, red/error, amber/warning, gray/inactive" |

### Dashboard Color Philosophy
- **Muted base palette** — avoid saturated colors as backgrounds; they fatigue for long sessions
- **Accent for KPIs** — primary accent color used on metric values and active navigation item
- **Semantic colors for data** — consistent green=positive, red=negative, amber=neutral throughout
- **Surface elevation** — panel background slightly lighter/different than page background
- **Dark dashboards** — #0D1117 (canvas) → #161B27 (panels) → #1E293B (borders) — three-tier elevation

---

## Mobile App Design Vocabulary

| Vague | Mobile-Specific Professional Term |
|:---|:---|
| "menu at the bottom" | "bottom tab bar with 5 icon+label tabs, 49px height, active = accent color" |
| "popup from bottom" | "bottom sheet with drag handle, rounded top corners (20px), modal overlay" |
| "swipeable list" | "card list with swipe-to-reveal actions (delete/archive on left swipe)" |
| "main action button" | "floating action button (FAB), 56px, bottom-right, 16px margin above tab bar" |
| "the screen title" | "navigation bar with back chevron (left), title (center), action icon (right)" |
| "smaller than normal text" | "minimum 16px body text — never smaller (system renders crisp at this size)" |

---

## Design Anti-Patterns (AI-Generated Look — Avoid These)

These patterns make output feel AI-generated / template-based:

| Anti-Pattern | Why It Looks AI | Fix |
|:---|:---|:---|
| Generic blue (#2563eb) for everything | Default Tailwind/Bootstrap color | Use a derived accent with personality |
| Pure white (#ffffff) background | No warmth or character | Near-white with temperature (#FAFAF9 warm, #F8FAFC cool) |
| Uniform 8px border-radius everywhere | Tailwind default | Mix radii: 4px for inputs, 12px for cards, 24px for FABs |
| All-caps "LEARN MORE" buttons | Generic CTA pattern | Action-specific text ("Start Building", "View Dashboard") |
| Gray gradient hero backgrounds | Default hero template | Solid color + object, pattern, or photography |
| Stock illustration style | Unify/other tool defaults | Commission or use abstract/geometric illustrations |
| Same font weight for all text | Missing hierarchy | 3+ distinct weights (400/500/600 minimum) |

---

## Brutalist & Editorial Design Vocabulary

| Style | Description |
|:---|:---|
| Brutalist | Raw, intentional, oversized typography, stark contrast, no decorative shadows, grid-breaking elements |
| Editorial | Magazine-quality, photography-first, generous whitespace, serif + sans pairings, story-driven layout |
| Neobrutalist | Brutalist structure with vibrant color, thick black borders, offset box shadows |
| Swiss/Grid | Rigid modular grid, typographic hierarchy as design element, minimal ornamentation |

---

## Gradient Usage Guidelines

| Use Case | Guidance |
|:---|:---|
| Hero backgrounds | ✅ Use — subtle gradient (10–15% opacity range) adds depth |
| Button fills | ❌ Avoid — solid colors read more confidently for CTAs |
| Card backgrounds | ⚠️ Sparingly — only for premium/marketing context |
| Text | ⚠️ Sparingly — gradient text works for display headlines only |
| Full-page backgrounds | ❌ Avoid for app/dashboard — causes eye fatigue |
| Decorative blobs | ✅ Acceptable for landing pages — keep subtle, 30%+ blur radius |
