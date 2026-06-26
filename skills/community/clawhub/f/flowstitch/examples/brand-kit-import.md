# Example: Brand Kit Import

This example shows §B running from a minimal brand brief — just a logo and one hex code — to a fully populated DESIGN.md.

---

## Input

**User:** "My startup is called Driftwood. We help remote teams build culture. Here's our logo [attaches image] and our brand color is #2D6A4F (a forest green). We want to feel warm and grounded, not corporate."

---

## Step 1 — Logo Analysis

```
Analyzing logo with vision model...

Extracted:
- Primary brand color: Forest Green (#2D6A4F) — confirmed, matches user input
- Secondary color detected: Warm Sand (#D4A574) — in the logomark's accent
- Background: Transparent
- Logo style: Organic letterform, slightly rounded, not geometric — humanist feel
- Personality adjectives: "grounded," "natural," "approachable," "earthy"
```

---

## Step 2 — Color System Derivation

Starting from `#2D6A4F` (Forest Green) + `#D4A574` (Warm Sand):

| Role | Color | Derivation |
|:---|:---|:---|
| Primary Accent | `#2D6A4F` Forest Green | Direct from brand |
| Secondary Accent | `#D4A574` Warm Sand | Extracted from logo |
| Background (light) | `#FAFAF8` Warm Off-White | Near-white with warmth, not clinical |
| Surface | `#F0ECE7` Parchment | Slightly darker warm white for cards |
| Text Primary | `#1C2B22` Deep Forest | Very dark green — richer than pure black |
| Text Secondary | `#6B7C74` Sage Mist | Muted green-gray for body copy |
| Border | `#DDD9D4` Linen | Barely visible warm divider |

**Contrast check:**
- Deep Forest (#1C2B22) on Warm Off-White (#FAFAF8): ratio 17.2:1 ✅ AAA
- Sage Mist (#6B7C74) on Warm Off-White: ratio 5.1:1 ✅ AA

---

## Step 3 — Typography Selection

Brand feel: warm, grounded, approachable — not corporate or technical.

**Recommendation:**
- **Display / Headlines:** `Fraunces` — humanist serif with warmth and personality, evokes craftsmanship
- **Body:** `DM Sans` — geometric sans, friendly and clean, pairs well with Fraunces
- **Fallback:** `Georgia` / `system-ui`

This combination signals quality without coldness. The serif headline says "we care about craft" and the sans body says "we're still approachable."

---

## Step 4 — User Confirmation

```
🎨 Brand kit imported for Driftwood. Here's what I built:

Primary: Forest Green (#2D6A4F) — your signature color, CTAs and accents
Secondary: Warm Sand (#D4A574) — extracted from your logo, highlights and warmth  
Background: Warm Off-White (#FAFAF8) — clean but not clinical
Surface: Parchment (#F0ECE7) — cards and panels
Text: Deep Forest (#1C2B22) — rich dark green instead of flat black

Fonts: Fraunces (headlines) + DM Sans (body) — warm craft meets modern clarity

Overall vibe: "Remote team culture tool that actually gives a damn. Natural,
warm, grounded — the opposite of Microsoft Teams."

Does this feel like Driftwood? Say "looks good" to continue building,
or tell me what to adjust.
```

**User:** "Love it. The sand accent is perfect. Let's build."

---

## Generated `.stitch/DESIGN.md`

```markdown
# Design System: Driftwood
**Project ID:** [generated on first Stitch call]

## 1. Visual Theme & Atmosphere
Driftwood embodies **warm, grounded humanity**. The antidote to cold corporate SaaS.
Natural materials and generous whitespace create the feeling of a well-lit co-working 
space — purposeful but never sterile. The palette says "we grow things together," 
not "we process tickets." Everything is soft, approachable, and intentional.

## 2. Color Palette & Roles
- **Forest Green** (#2D6A4F) — Primary CTAs, active states, brand anchor
- **Warm Sand** (#D4A574) — Secondary highlights, hover states, warmth accents
- **Warm Off-White** (#FAFAF8) — Primary page background
- **Parchment** (#F0ECE7) — Card and panel surfaces
- **Deep Forest** (#1C2B22) — Headlines and primary body text
- **Sage Mist** (#6B7C74) — Secondary text, labels, metadata
- **Linen** (#DDD9D4) — Borders and dividers (barely visible)

## 3. Typography Rules
- **Display/Headlines:** Fraunces — humanist serif, warmth and craft
  - Weight: 600–700, letter-spacing: normal (no tight tracking — warmth over precision)
  - Sizes: 3rem (H1), 2rem (H2), 1.5rem (H3)
- **Body:** DM Sans — friendly geometric sans
  - Weight: 400 regular, 500 medium for emphasis
  - Line-height: 1.7 — generous, readable, unhurried
- **Labels/Meta:** DM Sans regular, 0.875rem, Sage Mist color

## 4. Component Stylings
* **Buttons:** Softly rounded (10px) — more approachable than sharp, less juvenile than pill
  Forest Green fill, Cloud White text. Hover: slightly deeper forest tone.
  Secondary: Parchment background, Forest Green text, Linen border.
* **Cards:** Parchment (#F0ECE7) background. Softly rounded (12px).
  Gentle shadow on hover: `0 4px 16px rgba(45,106,79,0.08)` — green-tinted warmth.
* **Navigation:** Clean horizontal. Logo left. Nav items in Deep Forest, Sage Mist on hover.
  Active page: Forest Green underline (2px). CTA: Forest Green pill button, right-aligned.
* **Inputs:** Linen border default, Forest Green ring on focus. Parchment background.
  Placeholder text in Sage Mist.
* **Tags:** Pill-shaped. Forest Green background at 15% opacity, Forest Green text.

## 5. Layout Principles
- Max-width: 1200px — slightly narrower than typical SaaS, creates cozier feel
- Section padding: 80px vertical — generous but not austere
- Grid: 12-column, generous 32px gutters
- Whitespace philosophy: "breathing room is respect for the reader"
- Mobile: true mobile-first — remote teams use phones

## 6. Design System Notes for Stitch Generation
**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first with true mobile responsiveness
- Theme: Light, warm, natural — organic and human
- Background: Warm Off-White (#FAFAF8) — primary canvas
- Surface: Parchment (#F0ECE7) — cards and panels
- Primary Accent: Forest Green (#2D6A4F) — CTAs and active elements
- Secondary Accent: Warm Sand (#D4A574) — highlights and warmth
- Text Primary: Deep Forest (#1C2B22) — rich dark green for headlines
- Text Secondary: Sage Mist (#6B7C74) — body copy and labels
- Font: Fraunces (headlines, weight 600) + DM Sans (body, weight 400)
- Buttons: Softly rounded (10px), Forest Green fill, 500ms gentle transitions
- Cards: Parchment background, 12px corners, green-tinted shadow on hover
- Layout: 1200px max-width, 80px section padding, generous whitespace
- Mood: Warm, grounded, approachable — not corporate, not clinical
```
