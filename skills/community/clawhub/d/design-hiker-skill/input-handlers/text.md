# Input Handler — Text Description

## Applies to
- Natural language UI descriptions
- PRD feature descriptions
- "Design a page that…" requests
- Verbal wireframe ideas

## Process

### Step 1 — Parse structural intent

Extract from the text:
- **Page purpose**: what task does this screen accomplish?
- **Sections**: hero, nav, list, form, footer, modal…
- **Components**: button, card, input, tab, chart…
- **Content types**: images, text, icons, data tables…
- **Interactions**: tap, scroll, swipe, form submit…
- **Platform signals**: "mobile app", "web dashboard", "PC" → set platform

### Step 2 — Clarify if needed

Ask (use your harness Ask-Question tool) when:
- Platform is ambiguous AND affects layout fundamentally
- No design system mentioned — confirm whether to use universal fallback
- Multiple distinct screens implied — confirm scope

Skip when: description is detailed enough, or precision is `rough`.

### Step 3 — Build component hierarchy

From the description, construct a mental tree:

```
Page: [page name]
├── [Section 1]
│   ├── [Component A]
│   └── [Component B]
└── [Section 2]
    └── [Component C]
```

Name every level semantically (`hero-section`, `product-card`), not positionally (`div-1`).

### Step 4 — Apply design system values

For every component in the tree:
- Colors → from tokens.css token names
- Typography → from font-size / font-weight tokens
- Spacing → from spacing tokens (only multiples of 4px)
- Radius → from radius tokens
- Heights → from component height tokens

For components not described explicitly, use the spec from `components.md`.

### Step 5 — Log assumptions

Text input generates the most assumptions. Log every decision:

```
[DEFAULT]    Platform: mobile 375px — not specified, assumed mobile
[DEFAULT]    Primary color: var(--color-primary) — no brand system provided
[CHOSEN]     Card layout: horizontal (image-left + text-right) — standard for product lists
[INFERRED]   Button height: var(--btn-height-mobile) — following mobile touch target standard
```

### Precision adjustments

- **rough**: hierarchy only, token names not values, "Card uses primary color"
- **standard**: token values filled in, standard spacing applied, font specs included
- **precise**: every property explicitly stated, padding/margin for every element
