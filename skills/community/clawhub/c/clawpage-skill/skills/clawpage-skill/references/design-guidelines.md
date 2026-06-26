# Clawpage Design Guidelines

Use this file as the shared design-quality reference when generating or updating page UI.
Inspired by production-grade frontend-design practices; adapted for the Clawpage context.

---

## 1. Design Thinking (Pre-Code Phase)

Before writing ANY HTML/CSS/JS, answer these four questions:

1. **Purpose** — What problem does this page solve? Who is the audience?
2. **Tone** — Pick a bold aesthetic direction. Examples (non-exhaustive):
   - brutally minimal · maximalist chaos · retro-futuristic · organic/natural
   - luxury/refined · playful/toy-like · editorial/magazine · brutalist/raw
   - art deco/geometric · soft/pastel · industrial/utilitarian · tech-dashboard
3. **Constraints** — Technical requirements (mobile-first? accessibility? performance budget?)
4. **Differentiation** — What single detail will make this page _unforgettable_?

> **Rule:** A clear conceptual direction executed with precision always wins. Bold maximalism and refined minimalism both work — the key is _intentionality_, not intensity.

---

## 2. Typography

- **Choose distinctive fonts** that match the page's tone. Browse Google Fonts for characterful choices — pair a display font with a refined body font.
- Use CSS variables `--font-display` and `--font-body` so the template stays flexible.
- Update the `<link>` in `index.html` to load the chosen fonts.

### ❌ NEVER default to

Inter · Roboto · Arial · system-ui · Space Grotesk (unless deliberately chosen for a specific reason)

### ✅ Examples of distinctive font pairings

| Tone | Display | Body |
|------|---------|------|
| Editorial | Playfair Display | Source Serif 4 |
| Tech/Dashboard | JetBrains Mono | DM Sans |
| Playful | Baloo 2 | Nunito |
| Luxury | Cormorant Garamond | Lato |
| Brutalist | Anton | IBM Plex Mono |
| Retro-future | Orbitron | Exo 2 |
| Soft/Organic | Quicksand | Karla |

These are starting points — explore and surprise. **No two pages should use the same fonts by default.**

---

## 3. Color & Theme

- Build a cohesive palette using CSS variables (`:root { --primary: …; --accent: …; }`).
- **Dominant + accent** palettes outperform timid, evenly-distributed schemes.
- Allow light _or_ dark themes — but ensure WCAG AA contrast minimums.
- Avoid cliché AI palettes: generic purple gradients on white, pure blue-on-white cards, plain red/green/blue.

### Palette construction tips

1. Pick 1 dominant hue → derive 3–5 tints/shades via HSL shifts.
2. Choose 1 contrasting accent for callouts/CTAs.
3. Define neutral grays with a warm/cool tint matching the dominant hue.
4. Test light text on dark AND dark text on light — both must be legible.

> **Light-theme warning (from base template):** The default template assumes a light background. If you keep it, avoid dark utility classes (`bg-gray-800`, `bg-slate-900`) that destroy text contrast. If you switch to dark, update body/panel backgrounds _and_ text colors together.

---

## 4. Motion & Micro-interactions

Prioritize **high-impact moments** over scattered micro-interactions:

| Priority | Technique | Example |
|----------|-----------|---------|
| 🥇 High | Page-load stagger reveal | Cards fade-in sequentially with `animation-delay` |
| 🥇 High | Scroll-triggered entrance | Sections slide up on first scroll into view |
| 🥈 Medium | Hover state surprises | Cards lift (`translateY(-4px)`) + shadow expands |
| 🥈 Medium | Interactive transitions | Tab content cross-fades; accordion slides open |
| 🥉 Low | Decorative loops | Pulsing dots, spinning icons (use sparingly) |

### Rules

- Prefer **CSS-only** solutions (`@keyframes`, `transition`, `animation`).
- One well-orchestrated page-load stagger creates more delight than many small uncoordinated effects.
- Add `prefers-reduced-motion` media query to disable animations for accessibility.

---

## 5. Spatial Composition

Go beyond predictable grids:

- **Asymmetric layouts** — vary column widths, offset cards.
- **Overlap** — elements breaking panel boundaries (images, badges).
- **Diagonal/angular flow** — slashed dividers, rotated accents.
- **Generous negative space** OR controlled density — both work if intentional.
- **Grid-breaking hero** — full-bleed hero section contrasting with contained content below.

> Match complexity to vision: maximalist designs need elaborate layout code; minimal designs need precise spacing and typography.

---

## 6. Backgrounds & Visual Texture

Create atmosphere and depth — don't default to flat solid colors:

| Technique | When to use |
|-----------|------------|
| Gradient mesh | Rich, organic feel |
| Noise / grain overlay | Vintage, editorial, brutalist |
| Geometric pattern (SVG) | Tech, dashboard, data-heavy |
| Layered transparency / glassmorphism | Modern, floating-card UI |
| Dramatic shadows | Luxury, depth-focused |
| Decorative borders / dividers | Editorial, art deco |
| Subtle dot/grid background | Clean, techy |

- Combine 1–2 techniques maximum per page for coherence.
- Keep backgrounds non-distracting to content readability.

---

## 7. Anti-Pattern Checklist (NEVER do these)

- ❌ Reuse the same font _every_ page (e.g., always Space Grotesk)
- ❌ Default to purple-on-white or blue-on-white card grids
- ❌ Cookie-cutter layout identical across all pages
- ❌ Plain `<p>` and `<ul>` without any styling or component structure
- ❌ Uncoordinated micro-animations with no unified timing
- ❌ Flat solid-color backgrounds with no depth or texture
- ❌ Dark background classes on a light-themed template (or vice versa) without updating text colors
- ❌ Placeholders left in final output (`Lorem ipsum`, `TODO`, `[PLACEHOLDER]`)

---

## 8. Creative Variation Principle

> **每个页面都应该有独特的设计个性。**

- Vary between light and dark themes across different pages.
- Rotate font pairings — never converge on a single "default" choice.
- Alternate layout strategies (hero-centric, card grid, editorial, dashboard, single-scroll).
- Match the aesthetic to the content's subject matter and audience.
- Take creative risks — the AI is capable of extraordinary design; don't hold back.

---

## Quick Reference for Sub-Skills

| Sub-skill | Required action |
|-----------|----------------|
| `create-page` | Run full Design Thinking phase → choose fonts/palette/layout → generate UI |
| `update-page` | Maintain existing design language unless user requests style change |
| `create-management-page` | Use professional/dashboard tone; data-focused layout |
| `create-template` | Provide CSS-variable slots for fonts, colors; don't hardcode single style |
| `update-template` | Preserve CSS-variable structure; enhance visual system |
