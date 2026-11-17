# Canonical guideline template

Use the relevant sections. Omit empty ceremony, but keep status, decisions, tokens, states, accessibility, and governance explicit.

## 1. Header

- name
- status: `candidate`, `approved`, or `implemented`
- version and date
- owners or decision authority when known
- supported products, themes, surfaces, and languages

## 2. Brand foundation

- one-sentence visual thesis
- three to five operating principles
- intended impression and anti-goals
- inherited, observed, proposed, and verified decisions

## 3. Research ledger

| Source | Observed method | Decision it informs | Authority |
| --- | --- | --- | --- |
| Direct link | Concise finding | Concrete project rule | Standard / system / brand / inspiration |

## 4. Foundations

Document only what the product needs:

- layout grid, container widths, spacing rhythm, and breakpoints
- typography roles, family, weight, size, line height, and maximum measure
- radius, border, elevation, blur, texture, and gradient policy
- image, screenshot, diagram, and evidence treatment
- motion durations, easing, density, entry behavior, and reduced motion
- voice and labeling rules

Each section should include `use`, `avoid`, and at least one representative example.

## 5. Color primitives

| Primitive | OKLCH authoring value | sRGB fallback | Intended range | Avoid |
| --- | --- | --- | --- | --- |
| `neutral-*` | value | hex | surfaces/text | direct component use |
| `brand-*` | value | hex | signal family | semantic status |

Do not create scale steps without a known job.

## 6. Semantic theme map

Include only supported themes; adapt the columns for single-theme or fixed-theme products.

| Role | Light value | Dark value | Contract |
| --- | --- | --- | --- |
| `canvas` | token | token | page background |
| `surface-raised` | token | token | raised content layer |
| `text-primary` | token | token | primary reading text |
| `text-secondary` | token | token | supporting text |
| `border-subtle` | token | token | nonessential separation |
| `brand-field` | token | token | signature filled moment |
| `on-brand` | token | token | content on brand field |
| `focus-ring` | token | token | keyboard focus |

Add status roles only when the product uses them. Components consume semantic roles, never primitive hex values.

## 7. Verified and forbidden pairs

| Foreground | Background | Ratio | Allowed use | Evidence |
| --- | --- | ---: | --- | --- |
| token and resolved value | token and resolved value | full measurement | normal / large / essential UI | method, surface, state, date |

List known forbidden pairs directly. For alpha colors, record the background and composited result that was tested.

Evaluate thresholds using the full ratio. A rounded display value is presentation, and verification is separate from approval or implementation.

## 8. Interaction state matrix

Include rows only for supported themes and states.

| Family and theme | Rest | Hover | Active/selected | Focus-visible | Disabled |
| --- | --- | --- | --- | --- | --- |
| Primary / light | fg + bg + border | pair | pair | ring + adjacent bg | pair |
| Primary / dark | fg + bg + border | pair | pair | ring + adjacent bg | pair |

Repeat for links, controls, cards, navigation, and inputs only when they exist. “Uses the accent color” is not a complete definition.

## 9. Responsive and motion behavior

- per-section responsive treatment: preserve, recompose, collapse, or defer; keep essential information and actions available
- wrapping and truncation rules
- touch target and focus behavior
- entry and continuous motion limits
- `prefers-reduced-motion` behavior

## 10. Adoption and governance

- migration order: foundations → representative components → broad adoption
- exception process and expiry when needed
- canonical file or page
- change authority, version policy, and review cadence
- unresolved decisions and next validation step

## Release checklist

- representative pages in supported light, dark, or fixed themes
- narrowest supported viewport and typical wide viewport; web reflow at 320 CSS px where applicable
- hover, keyboard focus, active/selected, disabled, error, and success states when present
- longest realistic text and URLs in the supported languages, including non-Latin wrapping when relevant
- keyboard use, zoom, overflow, focus obscuration, and target behavior
- reduced motion
- print/PDF/social/export surfaces when present
- contrast measurement and rendered visual inspection
- build and static checks proportional to risk
- guideline status matches reality, with unrendered or unmeasured proposals explicitly unverified
