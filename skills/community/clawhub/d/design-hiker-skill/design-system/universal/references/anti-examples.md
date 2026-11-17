# Anti-Examples — What Bad Looks Like (and Why)

Documented cases of "AI design taste" problems, each with:
- What went wrong visually
- Why it happened technically
- The correct approach

---

## 1. Separator Too Heavy

**Bad:**
```css
border-bottom: 1px solid #E0E0E0;   /* used on list rows */
```
**Result:** Every row has a visible line separating it → list looks like a table grid → feels like a spreadsheet, not a native app.

**Why:** #E0E0E0 is a fully opaque medium gray. On white background it has ~1.8:1 contrast — clearly visible.

**Good:**
```css
border-bottom: 0.5px solid rgba(0,0,0,0.07);
```
**Why it works:** rgba(0,0,0,0.07) at 0.5px is barely perceptible — the eye senses structure without seeing lines.

---

## 2. Emoji as Navigation Icons

**Bad:** `<span class="nav-icon">🔍</span>` for a search navigation item

**Result:** Design immediately signals "AI-generated" — emoji are designed for communication, not UI chrome. They're disproportionately large, inconsistent in visual weight, and look out of place next to system UI.

**Good:** Inline SVG with `currentColor` and `width="14"` / `height="14"`.

**Why it happens:** Emoji are the path of least resistance for icons. The model knows "🔍 means search" so it uses it. SVG requires deliberate effort.

---

## 3. Mobile-Sized Controls in Desktop App

**Bad:**
```css
.btn { height: 44px; }       /* mobile touch target */
.toggle { width: 36px; height: 22px; }  /* iOS toggle */
```
**Result:** Everything feels chunky and sparse. The whole layout looks like a web app viewed on a large screen, not a native macOS app.

**Good:**
```css
.btn { height: 26px; }       /* macOS compact */
.toggle { width: 32px; height: 18px; }  /* macOS toggle */
```

**Why it happens:** The model learned from web/mobile design tutorials where 44px is the standard. macOS compact sizing requires explicitly overriding this.

---

## 4. Traffic Lights Tokenized

**Bad:**
```css
.tl { width: var(--spacing-sm); height: var(--spacing-sm); }
/* --spacing-sm = 8px → traffic lights become 8×8px, too small */
.traffic-lights { gap: var(--spacing-xs); }
/* --spacing-xs = 4px → gap too tight */
```
**Result:** Traffic lights appear tiny and lose the macOS feel.

**Good:**
```css
.tl { width: 12px; height: 12px; }   /* macOS spec: exactly 12px */
.traffic-lights { gap: 6px; }         /* macOS spec: exactly 6px */
```

**Rule:** Platform constants (traffic light size, system bar heights) must never be tokenized. They are fixed specifications, not design decisions.

---

## 5. Badge Shape Distorted

**Bad:**
```css
.badge { padding: 4px 5px; line-height: 16px; }
/* For "3": height = 4+16+4 = 24px, width ≈ 17px → oval (tall) */
```
**Result:** Single-character badges look like vertical ovals, not circles.

**Good:**
```css
.badge { height: 17px; min-width: 17px; line-height: 17px; padding: 0 5px; }
/* For "3": 17×17px circle; for "24": 17×24px pill — both correct */
```

**Rule:** Use fixed `height` + `line-height` (same value) + horizontal-only padding. Never use vertical padding on badges.

---

## 6. Toggle Thumb Off-Center

**Bad:**
```css
.toggle-thumb { right: 2px; top: 2px; }
.toggle.off .toggle-thumb { transform: translateX(-12px); }
/* Container 32px, thumb 14px: OFF position = 32-2-14-12 = 4px from left ≠ 2px */
```
**Result:** Thumb is slightly right of where it should be in OFF state — visible asymmetry.

**Good:**
```css
.toggle-thumb { left: 2px; top: 2px; }              /* OFF = default position */
.toggle:not(.off) .toggle-thumb { transform: translateX(14px); } /* ON = 2+14 = 16px */
```
**Rule:** Use `left`-based positioning. OFF state = `left: 2px`. ON state = `translateX(+14px)`. Math: `32 - 2 - 14 = 16px`, so `translateX(+14px)` moves from 2px to 16px. Symmetric.

---

## 7. CSS Class Name Drift

**Bad:**
```css
.nav-item.active { background: var(--color-selected-bg); }
```
```js
el.classList.add('on')  /* JS uses 'on', not 'active' */
```
**Result:** Selected state never applies — the CSS rule can never be triggered.

**Why it happens:** Model writes CSS in one pass, then writes JS in another pass, with different names chosen each time.

**Rule:** Define the interactive class name FIRST in CSS comments before writing the JavaScript:
```css
/* Active state class: .on (used by go() function) */
.nav-item.on { ... }
```

---

## 8. Card Hover Lift (Web Pattern)

**Bad:**
```css
.card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
```
**Result:** Cards "pop up" on hover like web cards — this is Material Design / web pattern, not macOS.

**Good:**
```css
.card:hover { border-color: var(--color-border-strong); box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
```
**macOS cards emphasize IN PLACE** — they don't move, they just get slightly more defined at the edges.

---

## 9. Primary Color Used Decoratively

**Bad:** Section titles in `var(--color-primary)` blue, colored icon backgrounds for every list item, blue text links scattered throughout interface.

**Result:** The eye doesn't know where to look. Blue has lost its signal value — it's everywhere.

**Rule:** Primary color = "I am the main action" or "I am selected." Use it max 2-3 times per screen. If everything is blue, nothing is blue.

---

## 10. Nav Badge Inconsistency Between States

**Bad:** Different nav items in the same unselected state show different badge styles:
- Item A: gray badge `rgba(0,0,0,0.06)` bg
- Item B: blue badge `rgba(0,102,255,0.12)` bg

**Result:** User thinks one of them is selected or special, when they're both in the same inactive state.

**Rule:** In the same state, same component = same visual treatment. Period.
Unselected nav badges: ALL gray. Selected nav badges: ALL white inverted. No exceptions.

## 11. Nav badge inconsistency between states

**Bad:**
Different nav items in same unselected state had different badge styles: muted=gray, accent=blue-tinted

**Why it happens:** badge-accent and badge-muted were treated independently without a unified 'same-state = same-style' rule

**Good:**
In unselected state: ALL badges use gray (badge-muted style). In selected state: ALL badges use white-inverted. Never mix badge styles within the same nav state.

---

## 12. Icon Style Inconsistency

**Bad:**
Mixing outline icons (☰ 🔍) with filled icons (📦 ⚙️) in the same navigation or toolbar.
Or mixing different icon weights: some 1px stroke, others 2px stroke.

**Result:** The UI looks assembled from different design systems — inconsistent visual weight
signals "this wasn't designed, it was assembled."

**Good:**
```html
<!-- Choose ONE style and apply it everywhere -->
<!-- Outline (recommended for macOS/web apps): -->
<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.5">...</svg>

<!-- If you use filled, ALL icons must be filled -->
<!-- Never mix stroke and filled in the same context -->
```

**Rule:** Before generating, decide: outline OR filled. Document it as a comment:
`/* Icon style: outline, 1.5px stroke, currentColor */`
Then apply consistently. Use the same style for navigation icons, action icons, and status icons.

---

## 13. Image Distortion

**Bad:**
```css
.avatar { width: 40px; height: 40px; }
/* No object-fit — image stretches to fill the fixed dimensions */
```

**Result:** Avatars become squashed ovals, product images distort, brand logos stretch.
Immediately signals "developer mindset, not designer mindset."

**Good:**
```css
/* Always pair fixed dimensions with object-fit */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  object-fit: cover;       /* fills container, crops edges */
  object-position: center; /* crop from center */
}

.logo {
  height: 24px;
  width: auto;             /* let width be automatic for logos */
  object-fit: contain;     /* show full logo, no cropping */
}
```

**Rule:** Every `<img>` with fixed `width` AND `height` must have `object-fit`.
Avatars/thumbnails → `cover`. Logos/icons → `contain`. Never leave both dimensions fixed without it.

---

## 14. Button Variant Inconsistency

**Bad:**
```html
<!-- Three different "secondary" button styles in the same interface -->
<button style="background:#eee; border-radius:4px">Cancel</button>
<button style="border:1px solid #ccc; background:white">Go Back</button>
<button style="background:transparent; color:blue; text-decoration:underline">Skip</button>
```

**Result:** User can't build a mental model of what secondary/tertiary actions look like.
Each button feels like a one-off decision, not a system.

**Good:**
```css
/* Define exactly 4 variants, use them exclusively */
.btn-primary   { bg: var(--color-primary); color: white; }       /* ONE per view */
.btn-secondary { bg: var(--color-surface); border: 0.5px solid var(--color-border); }
.btn-ghost     { bg: transparent; color: var(--color-primary); }  /* low emphasis */
.btn-danger    { bg: var(--color-danger-surface); color: var(--color-danger); }
```

**Rule:** Define the button type hierarchy BEFORE generating any buttons.
Then apply: one `btn-primary` per view maximum, consistent `btn-secondary` everywhere.
Never invent a new button style mid-design.

---

## 15. Text on Image — Contrast Failure

**Bad:**
```html
<div style="background-image: url(hero.jpg)">
  <h1 style="color: white;">Welcome</h1> <!-- white text on unknown image content -->
</div>
```

**Result:** On bright/light images the white text becomes invisible. Contrast is
unpredictable and depends entirely on the specific image content.

**Good:**
```css
/* Option A: gradient overlay (most common) */
.hero {
  position: relative;
  background-image: url(hero.jpg);
  background-size: cover;
}
.hero::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0) 60%);
}
.hero-text {
  position: relative; z-index: 1;
  color: white; text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

/* Option B: frosted glass card over image */
.hero-card {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(12px);
  color: var(--color-text-primary); /* dark text, guaranteed contrast */
}
```

**Rule:** Never place text directly on a photo background without a contrast layer.
WCAG AA: text-on-background contrast ≥ 4.5:1. Photo backgrounds cannot guarantee this.

---

## 16. Loading State — "Loading..." Text Only

**Bad:**
```html
<div>Loading...</div>  <!-- or spinner with no context -->
```

**Result:** Layout shift when content loads. User has no sense of what's coming.
Signals unfinished product.

**Good:**
```html
<!-- Skeleton screen: matches the real layout -->
<div class="skeleton-card">
  <div class="skeleton-avatar"></div>
  <div class="skeleton-lines">
    <div class="skeleton-line" style="width:60%"></div>
    <div class="skeleton-line" style="width:40%"></div>
  </div>
</div>
```
```css
.skeleton-line, .skeleton-avatar {
  background: var(--color-surface-3);
  border-radius: var(--radius-sm);
  animation: shimmer 1.5s ease-in-out infinite;
}
.skeleton-avatar { width: 40px; height: 40px; border-radius: var(--radius-full); }
.skeleton-line   { height: 14px; margin-bottom: var(--spacing-xs); }

@keyframes shimmer {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
```

**Rule:** Skeleton screens match the real layout's shape. Never show "Loading…" alone.
Show for ≥ 300ms even if data arrives faster (avoids flash of skeleton).

---

## 17. Missing Interaction States

**Bad:**
```css
.button { background: var(--color-primary); color: white; }
/* Only default state — hover/focus/active/disabled not defined */
```

**Result:** Buttons feel unresponsive. Users lose confidence ("did my click register?").
Disabled elements look identical to enabled ones.

**Good:**
```css
.button {
  background: var(--btn-primary-bg);
  color: var(--btn-primary-color);
  transition: all var(--duration-fast) var(--easing-default);
  cursor: pointer;
}
.button:hover   { background: var(--btn-primary-bg-hover); }
.button:active  { background: var(--btn-primary-bg-active); transform: scale(0.98); }
.button:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
}
.button:disabled {
  opacity: var(--btn-disabled-opacity);  /* 0.4 */
  cursor: not-allowed;
  pointer-events: none;
}
```

**Rule:** Every interactive element needs ALL of: default / hover / active / focus / disabled.
Missing any one of these is an incomplete implementation, not a design choice.

---
## ── 以下来自 taste-skill Section 9（内容/文案/信息层）──

## 18. Generic Content — "Jane Doe" Effect

**Bad:**
Names: "John Smith", "Sarah Chen", avatars with SVG egg silhouettes, numbers: `99.99%`, `50%`, `1,234,567`, brand names: "Acme", "Nexus", "SmartFlow", "Cloudly".

**Why:** Generic placeholder content is immediately recognizable as AI-generated. Real products have specific, slightly imperfect data.

**Good:**
Names: contextual and locale-appropriate. Numbers: organic (`47.2%`, `+1 (312) 847-1928`). Brand names: invented but plausible for the industry.

---

## 19. Filler Verbs in Copy

**Bad:**
"Elevate your workflow", "Seamlessly integrates", "Unleash the power of", "Next-Gen solution", "Revolutionize your business".

**Why:** These words signal AI-generated copy. They are meaningless, interchangeable across any product, and trained readers skip them.

**Good:**
Concrete verbs that describe what the product actually does: "Import CSV in one click", "Sync across devices automatically", "Review in 30 seconds".

---

## 20. Em-dash as Design Element

**Bad:**
Using `—` anywhere: headlines ("Built for teams — not solo"), eyebrows ("Trusted — worldwide"), quote attribution ("— John Smith, CEO"), body copy ("We ship daily — no exceptions").

**Why:** The em-dash is the single most-tested AI Tell in production. Every LLM defaults to it. Zero-tolerance rule.

**Good:**
- Headlines: use a comma or period
- Attribution: regular hyphen with spaces (` - `) or line break
- Body copy: restructure into two sentences, or use a comma, colon, or parentheses
- Date/number ranges: regular hyphen (`2018-2026`, `€40-80k`)

**Rule:** If `—` or `–` appears anywhere visible, the output is not done.

---

## 21. Section-Number Eyebrows

**Bad:**
`00 / INDEX`, `001 · Capabilities`, `06 · how it works`, `02 · Featured Work`, `Scroll · 001 Capabilities`.

**Why:** Section numbering is an agency-portfolio cliché that signals "AI tried to look designed." Users can count sections; they don't need labels.

**Good:**
Name the section in plain language: "How it works", "Capabilities", "Featured Work". If numbering is needed, embed it in the content, not as a label above the heading.

---

## 22. Version Labels and Status Stamps

**Bad:**
`V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA` as hero eyebrows. Footer strings like `v1.4.2`, `Build 0048`, `last sync 4s ago · main` on marketing or design pages.

**Why:** Version stamps are CLI/devtool fixtures. On a design or marketing page they serve no user, they just signal "AI added this to look authentic."

**Good:**
No version label unless the brief is explicitly about a product launch or technical status page. Footers: copyright, links, contact — not build metadata.

---

## 23. "Quietly Trusted By" Copy

**Bad:**
"Quietly in use at 500+ companies", "Quietly trusted by", "Quietly powering teams at".

**Why:** This phrasing is so common in AI-generated social proof that it has become a recognized Tell.

**Good:**
"Trusted by", "Used at", "Customers include" — or skip the heading entirely and let the logos speak.

---

## 24. Middle-Dot Overuse

**Bad:**
Using `·` as the default separator for everything: `DESIGN · BUILD · SHIP`, `foo · bar · baz · qux · quux`, `Lisbon · 2024 · Studio`.

**Why:** The middle-dot as universal separator is an over-used design-aesthetic shorthand. Maximum 1 per line in a metadata strip.

**Good:**
For multiple items: use line breaks, columns, hairlines, or commas. Reserve `·` for genuine paired metadata where the relationship matters.

---

## 25. Generic Step Labels

**Bad:**
"Stage 1 / Stage 2 / Stage 3", "Step 1 / Step 2 / Step 3", "Phase 01 / Phase 02 / Phase 03", "Pass One / Pass Two".

**Why:** Numbering the steps instead of naming them forces users to read both the number AND the content. The content already implies sequence.

**Good:**
Use the verb-noun directly as the label: "Install", "Configure", "Deploy" — or "Discover → Build → Launch". The number is implicit from the ordering.

---

## 26. Decorative Status Dots on Every Row

**Bad:**
A colored dot before every nav item, every list row, every badge, every task: `● ONE Q4 SLOT OPEN`, `● Available`, `● Design`, `● Engineering`.

**Why:** Colored dots carry semantic meaning (server live, availability flag). When used decoratively on every item they lose meaning and add visual noise.

**Good:**
Zero decorative dots by default. Use ONLY when conveying real semantic state (server status, live availability indicator) — one per section maximum.

---

## 27. Locale / Weather / Time Strips

**Bad:**
`LIS 14:23 · 18°C` in the nav, "Lisbon, working with founders" in hero, "1200-690 Lisbon, Portugal" in footer as atmospheric decoration.

**Why:** These are agency-portfolio decoration tells — they signal "AI tried to add personality" without serving the user.

**Good:**
A functional contact address in the footer is fine. Atmospheric locale strips are banned unless the brief is explicitly about a globally-distributed team with timezone-relevant work.

---

## 28. Scroll Cues

**Bad:**
`Scroll`, `↓ scroll`, `Scroll to explore`, `Scroll to walk through it`, animated mouse-wheel icons at the bottom of the hero.

**Why:** If the user hasn't scrolled, they're looking at the hero. They know what scrolling is. The bottom of the viewport does not need a label.

**Good:**
No scroll cues. If content below the fold is important, make it visible in the viewport or use a natural affordance (partial content peeking).

---

## 29. Pills / Labels Overlaid on Images

**Bad:**
`<span>` overlays on photos: `Brand · 02`, `PLATE · BRAND`, `Field notes - journal`, `Category · Product`.

**Why:** Text overlaid on images has unpredictable contrast and reads as a workaround rather than a design decision.

**Good:**
Either let the image speak alone, or add a caption directly below (outside the image, in the document flow).

---

## 30. Photo Credit Captions as Decoration

**Bad:**
`Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm` under placeholder/stock images as style elements.

**Why:** Photo attribution is for crediting a real photographer for a real photograph. When applied to placeholders or stock, it's affectation.

**Good:**
Skip the caption entirely, or use a single functional caption ("The 6-quart Dutch oven, in Sage."). Photo credit only when there is a real photographer to credit.

---

## 31. border-top + border-bottom on Every Row

**Bad:**
```css
/* Applied to every row in a long list */
border-top: 1px solid var(--color-border);
border-bottom: 1px solid var(--color-border);
```
Every row in a 10-item list gets its own box. The list becomes a grid of bordered rectangles.

**Why:** Double-bordering creates visual doubling (shared edges appear twice as heavy) and makes a list look like a data table when it shouldn't.

**Good:**
Pick ONE: either `border-bottom` between rows only, OR `border-top` above the group header only. Apply sparsely. Use spacing to create separation before reaching for borders.

---

## 32. Div-Based Fake Screenshots

**Bad:**
Building a fake product UI (task list, terminal, dashboard) out of styled `<div>` rectangles to simulate what the product looks like.

**Why:** This is the #1 LLM-design Tell. It always looks unconvincing — the proportions are wrong, the typography is wrong, the interactions are missing. It screams "I couldn't get a real screenshot."

**Good:**
Use a real screenshot, a generated image via an image-generation tool, a real working component preview, or skip the product preview entirely. Honest emptiness beats a fake representation.

---

## 33. Neon Outer Glows

**Bad:**
```css
box-shadow: 0 0 20px rgba(0,122,255,.6);  /* outer glow on button */
text-shadow: 0 0 10px #00ff88;           /* neon text glow */
```

**Why:** Outer glows are an early-2010s web aesthetic and a default LLM decoration choice. They look cheap and draw attention without communicating anything.

**Good:**
Inner borders, subtle tinted shadows (inset), or a slight surface-tint shift. If depth is needed: `box-shadow: inset 0 0 0 1px rgba(255,255,255,.1)` on dark surfaces.

---

## 34. Pure Black

**Bad:**
`color: #000000; background: #000000;`

**Why:** Pure black creates harsh contrast and looks flat on screen. It's also a default that signals no color decision was made.

**Good:**
Off-black: `#0a0a0a`, `#111111`, `#1a1a1a` (adjust warmth/coolness to match the palette). These read as "black" but are perceptually richer.

