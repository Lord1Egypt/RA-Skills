# Design Critic Checklist

Run this checklist after L2 HTML generation, before L3 spec extraction.
This is the self-review step (L3.5). Be honest — finding issues now saves revision cycles.

For each failing item, note the specific element and the fix needed.
Do NOT proceed to L3 if critical issues (⛔) are found — fix them first.

---

## ⛔ Critical — Fix Before Proceeding

**Platform constants**
- [ ] Traffic light circles are EXACTLY 12px × 12px (not `var(--spacing-sm)`)
- [ ] Traffic light gap is EXACTLY 6px (not `var(--spacing-xs)`)
- [ ] Titlebar height is 36px or less (not 52px unless justified)
- [ ] Toolbar buttons are 26–28px height (not 44px)
- [ ] Toggle is 32×18px or smaller (not 36×22px iOS size)

**Icon format**
- [ ] Zero emoji, Unicode symbols, icon-font glyphs, rotated characters, or CSS-built shapes used as functional icons
- [ ] Every functional icon declares a trusted `data-icon-source` and canonical `data-icon-name`
- [ ] Inline SVG icons use `data-spec-source="inline-svg-icon"` and `currentColor` (not hardcoded colors)
- [ ] Every icon-only control has an accessible name and a real rendered SVG/image
- [ ] Mobile icon controls are at least 44x44px and measured icon-center offset is no more than 2px per axis
- [ ] Simulated signal, Wi-Fi, and battery icons use one coherent `platform-native` set

**CSS/JS consistency**
- [ ] Every class added via `classList.add('X')` has a matching `.X` CSS rule
- [ ] Interactive state class names in CSS match exactly what JS uses

**Token compliance**
- [ ] Zero hardcoded hex colors in `<style>` blocks
- [ ] Zero hardcoded px values for spacing (use `var(--spacing-*)`)
- [ ] All `var(--*)` names exist in tokens.css or component-tokens.css

**Component binding**
- [ ] Every visible product module has `data-component` and `data-spec-source`
- [ ] Every `data-spec-source` is listed in `component-routing.md`
- [ ] High-risk modules (`header`, `footer`, `card`, `form`, `picker`, `modal`, `alert`, `tag`, `search`, `dashboard`, `hero`) have a written rejection reason in the internal binding map
- [ ] No pseudo component source appears in final HTML (`hero-card`, `feature-tile`, `magic-panel`, `status-pill`, `decorative-card`, etc.)
- [ ] Structural wrappers use `data-spec-source="structural-container"` and do not define custom internal component styling

---

## ⚠️ Important — Fix If Found

**Visual hierarchy**
- [ ] No more than 3 items using `var(--color-primary)` as background per view
- [ ] Font size levels are decisive: max 3 distinct sizes, each clearly different
- [ ] No element is trying to be more prominent than the primary action

**Separators**
- [ ] List/table row separators use `0.5px solid var(--color-separator)`
- [ ] Card/input/modal borders use `1px solid var(--color-border)`
- [ ] No `var(--color-border)` used as row separator (too heavy)

**Consistency**
- [ ] Same component type has identical treatment across all views
  - Nav badges: same style in same state across ALL nav items
  - List separators: same weight and color on ALL lists
  - Buttons: same height and style for same function across views
- [ ] No mixed icon families or stroke weights; icon source priority follows `icon-policy.md`

**Component states**
- [ ] Every interactive element has a visible hover state
- [ ] Every input/select has focus state defined
- [ ] Toggle thumb positions are symmetric (2px from each edge)
- [ ] Badge shape: single char → circle, multi char → pill (never oval)

---

## ℹ️ Review — Evaluate and Decide

**Spacing rhythm**
- [ ] All spacing values are multiples of 4px or 8px
- [ ] Related elements are closer together than unrelated ones (Gestalt proximity)
- [ ] Section gaps are visibly larger than item gaps

**Color usage**
- [ ] Every non-neutral color can answer: "what information does this convey?"
- [ ] Neutral colors (separators, secondary text) use rgba, not hex

**Platform authenticity (macOS)**
- [ ] Typography: body/UI text is 13px, not 16px
- [ ] Cards do NOT lift on hover (no `translateY`)
- [ ] Sidebar item height is ≤ 30px, not 40–44px
- [ ] Page/section gaps feel compact, not web-generous

---

## Quick Anti-Example Check

Scan the HTML and confirm NONE of these patterns are present:

```
"emoji"            ← UI icon as emoji (🔍📦⚙️ etc.)
">➤<" / ">‹<"    ← Unicode glyph used as a functional icon
class="battery"    ← CSS-built platform icon without sourced SVG
height: 44px       ← mobile touch target in desktop context
1px solid #E0E0E0  ← heavy separator on list rows
translateY(-       ← card lift on hover (web pattern)
.active {          ← check if JS uses 'active' or something else
var(--spacing-sm)  ← inside .tl CSS (traffic light tokenization)
```

---

## Output Format

After running this checklist, output:

```
CRITIC REVIEW — [component/page name]

Critical issues (must fix before L3):
  1. [specific element]: [what's wrong] → [fix]

Important issues:
  1. [specific element]: [what's wrong] → [fix]

Passed: [count] checks passed, [count] issues found
```

If zero critical issues and ≤ 2 important issues: proceed to L3.
If critical issues exist: fix them, then re-run critical checks only.

---

## ── Content & Copy Checks (from taste-skill Section 14) ──

Run these alongside the visual checks above. Content tells are harder to spot than visual tells.

### ⛔ Zero-Tolerance (fix before proceeding)

- [ ] **ZERO em-dashes (`—` or `–`)** anywhere on the page — headlines, body, captions, attribution, buttons. Search literally: `grep "—\|–"`. Must return 0.
- [ ] **No section-number eyebrows** (`00/INDEX`, `001 · Capabilities`, `06 · how it works`). Plain language only.
- [ ] **No version labels** (`V0.6`, `BETA`, `INVITE-ONLY`, `EARLY ACCESS`) unless the brief is explicitly a launch page.
- [ ] **No div-based fake product UI** — no fake terminal, task list, or dashboard built from `<div>` rectangles. Use real image, generated image, or omit.
- [ ] **Color consistency**: ONE accent color used identically across ALL sections. No warm-grey page with a blue CTA appearing only in one section.

### ⚠️ Important (fix if found)

- [ ] **No filler verbs** in copy: "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize". Replace with concrete, product-specific verbs.
- [ ] **No generic placeholder content**: "John Doe", "Sarah Chen", "Acme", "SmartFlow", "99.99%", "1,234,567". Use realistic, organic data.
- [ ] **No "Quietly trusted by" / "Quietly in use at"** social-proof phrasing. Use "Trusted by" or skip the header.
- [ ] **Middle-dot rationed**: max 1 `·` per line in metadata strips. Not used as universal separator.
- [ ] **No generic step labels**: "Stage 1", "Step 1", "Phase 01". Use verb-noun labels ("Install", "Configure", "Ship").
- [ ] **No decorative status dots** before nav items, list rows, badges unless conveying real semantic state.
- [ ] **No locale/weather strips** (`LIS 14:23 · 18°C`) unless brief explicitly requires it.
- [ ] **No scroll cues** (`Scroll`, `↓ scroll`, `Scroll to explore`) at the bottom of any section.
- [ ] **No pills/labels overlaid on images** (`Brand · 02`, `PLATE · BRAND`). Caption below image only.
- [ ] **No photo credit captions as decoration** on placeholder or stock images.
- [ ] **No version footers** (`v1.4.2`, `Build 0048`) on design/marketing pages.
- [ ] **No border-top + border-bottom on every list row**. Pick one side, apply sparsely.
- [ ] **No pure black `#000000`**. Use off-black (`#111111`, `#1a1a1a`).
- [ ] **No neon outer glows** on buttons or text. Use inner borders or subtle tinted shadows.
- [ ] **No `Fraunces` or `Instrument Serif`** as default display fonts.
- [ ] **No mixed font-family** in a single headline for emphasis. Use italic/bold of the same font.
- [ ] **One design system per project**. No mixing two component libraries in the same output.

### ℹ️ Content Density

- [ ] Quotes ≤ 3 lines of body text, attribution clean (no em-dash)
- [ ] Sub-paragraphs ≤ 25 words by default
- [ ] No two CTAs with the same intent on one page ("Get in touch" + "Let's talk" = same intent, pick one)
- [ ] CTA button text fits on ONE line — no wrapping at desktop width
