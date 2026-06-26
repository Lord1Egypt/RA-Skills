# Example: Competitive Design Analysis

This example shows a full §A run against a real competitor site, producing an actionable DESIGN.md.

---

## Input

**User:** "Analyze Linear's design and help me build something better for my project management tool"

**URL analyzed:** https://linear.app

---

## Step 1 — Extracted Design Language

Scraping linear.app revealed:

**Colors (extracted from CSS):**
- `--background: #0F0F0F` — near-black primary canvas
- `--foreground: #F2F2F2` — near-white text
- `#5E6AD2` — signature indigo (primary accent throughout)
- `#1C1C1E` — elevated surface (cards, panels)
- `#2A2A2E` — border/divider color

**Typography:**
- `"Inter"` loaded via Google Fonts — primary font everywhere
- Headlines: `font-weight: 600–700`, `letter-spacing: -0.02em` (tight tracking = premium feel)
- Body: `font-weight: 400`, `line-height: 1.6`

**Layout:**
- Max-width: `max-w-7xl` (1280px)
- Section padding: 96–128px vertical
- Grid: 12-column, 24px gutters

**Components:**
- Buttons: `rounded-md` (8px), not pill-shaped — more "tool" than "consumer app"
- Cards: flat background color `#1C1C1E`, very subtle 1px border
- Nav: minimal, horizontal, logo left, CTA right, no mega-menu

---

## Step 2 — What Linear Does Well

1. **Dark + indigo is iconic** — instantly recognizable, feels premium and technical
2. **Typography tightness** — negative letter-spacing on headlines signals craft and attention
3. **Information density** — manages to feel clean despite feature richness
4. **Consistent radius** — 8px everywhere creates coherence across all components
5. **Whitespace at scale** — large section padding makes every section feel intentional

---

## Step 3 — What's Missing / Weak

1. **Zero warmth** — black/indigo is great for developers, alienating for non-technical teams
2. **Navigation feels dated by 2026** — plain horizontal nav with no depth or personality
3. **Hero is static** — video or motion would significantly increase perceived modernity
4. **No brand personality below the fold** — consistent but anonymous after the hero
5. **Mobile experience** — desktop-first design shows in mobile breakpoints

---

## Generated `.stitch/DESIGN.md` — "Better Than Linear"

```markdown
# Design System: Loopback (Better Than Linear)
*Inspired by Linear's discipline, differentiated by warmth and personality*

## 1. Visual Theme & Atmosphere
Where Linear is cold and technical, Loopback is **warm and decisive**. The same 
information density and craft — but with a color system that doesn't alienate 
non-engineering teams. "Premium dark" meets "human warmth." Think Linear if it 
had a good personality.

## 2. Color Palette & Roles
- **Midnight Ink** (#0D1117) — Primary canvas. Slightly cooler than Linear's pure black
- **Soft Slate Surface** (#161B27) — Elevated surfaces: cards, panels, modals
- **Aurora Violet** (#7C3AED) — Primary accent. Violet vs. indigo = distinguishable, ownable
- **Lavender Glow** (#A78BFA) — Links, hover states, secondary accents
- **Cloud White** (#F8FAFC) — Primary text. Slightly warm white, not harsh
- **Fog Gray** (#94A3B8) — Secondary text, labels, metadata
- **Storm Border** (#1E293B) — Borders, dividers — barely perceptible

## 3. Typography Rules
- **Font Family:** Inter — same as Linear (proven for tool UIs), owned through execution
- **Headlines:** Semibold (600), letter-spacing -0.02em (same tight tracking as Linear — keep this)
- **Subheadlines:** Medium (500), letter-spacing -0.01em
- **Body:** Regular (400), line-height 1.65, slightly relaxed vs. Linear
- **Labels/Meta:** Regular (400), uppercase, letter-spacing 0.06em — adds organization

## 4. Component Stylings
* **Buttons:** Subtly rounded (8px) — matches Linear's tool aesthetic. Aurora Violet (#7C3AED) fill.
  Hover: Lavender Glow tint. Focus: violet ring at 2px offset.
* **Cards:** Soft Slate Surface (#161B27) background. 1px Storm Border edge. 
  No shadow (flat) on default. Whisper shadow on hover: `0 4px 20px rgba(124,58,237,0.08)` — 
  violet-tinted lift, not generic gray.
* **Navigation:** Horizontal, minimal. Logo + icon left. CTA pill-shaped right (differentiated 
  from Linear's squared CTA — more inviting).
* **Inputs:** Storm Border (#1E293B) default. Aurora Violet ring on focus. 
  Soft Slate background — readable in dark context.
* **Tags/Chips:** Pill-shaped. Background: `rgba(124,58,237,0.15)`. Text: Lavender Glow.

## 5. Layout Principles
- Max-width: 1280px (matches Linear — proven)
- Section padding: 96px vertical (matches Linear — intentional breathing room)
- Grid: 12-column, 24px gutters
- Mobile-first: deliberately improve on Linear's desktop-first bias

## 6. Design System Notes for Stitch Generation
**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first
- Theme: Dark, warm-cool contrast, premium tool aesthetic
- Background: Midnight Ink (#0D1117) — primary canvas
- Surface: Soft Slate (#161B27) — cards and panels
- Primary Accent: Aurora Violet (#7C3AED) — CTAs and active states
- Secondary Accent: Lavender Glow (#A78BFA) — links and hover states
- Text Primary: Cloud White (#F8FAFC) — headlines and body
- Text Secondary: Fog Gray (#94A3B8) — labels and metadata
- Font: Inter — semibold headlines with -0.02em letter-spacing, regular body
- Buttons: Subtly rounded (8px), Aurora Violet fill, pill-shaped for primary CTA in nav
- Cards: Flat Soft Slate background, 1px subtle border, violet-tinted hover shadow
- Layout: 1280px max-width, 96px section padding, generous breathing room
```

---

## What We Changed vs. Linear

| Element | Linear | Loopback |
|:---|:---|:---|
| Accent color | Indigo (#5E6AD2) | Violet (#7C3AED) — ownable, distinguishable |
| Canvas | Pure near-black | Midnight Ink — slightly cooler, more depth |
| Nav CTA | Square button | Pill-shaped — more inviting entry point |
| Card hover | No hover effect | Violet-tinted shadow — brand personality |
| Typography mood | Technical/cold | Same discipline, slightly more human |
| Mobile | Afterthought | Mobile-first explicitly in spec |

**Positioning:** Same category, same quality signal — but for teams, not just engineers.
