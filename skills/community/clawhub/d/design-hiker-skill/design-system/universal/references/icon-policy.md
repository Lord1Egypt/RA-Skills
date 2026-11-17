# Icon Source and Geometry Policy

Read this file whenever a page contains functional icons or simulated platform
chrome. An icon is not accepted merely because it looks approximately correct:
its source, semantic name, rendered graphic, and placement must be verifiable.

## Source Contract

Every functional icon must declare both attributes on the rendered icon element:

```html
<svg
  data-spec-source="inline-svg-icon"
  data-icon-source="lucide"
  data-icon-name="send"
  aria-hidden="true"
  viewBox="0 0 24 24">
</svg>
```

Allowed `data-icon-source` values:

| Value | Use |
|---|---|
| `component-library` | Icon exported by the active design-system component library |
| `lucide` | Lucide icon with its canonical name and path data |
| `platform-native` | One coherent simulated platform-chrome set |
| `brand-asset` | Icon supplied by the selected brand profile |
| `provided-asset` | Icon asset supplied with the user's input |

Use this priority: active component library, Lucide, approved platform-native
set, then brand/provided asset. Do not invent a path when an approved source
contains the required icon.

## Hard Boundaries

- Do not use Unicode, emoji, icon fonts, or system-font glyphs as functional
  icons. This includes `➤`, `▲`, `‹`, `×`, and similar symbols.
- Do not rotate an arrow, triangle, or paper-plane character to imitate another
  icon.
- Do not construct battery, signal, Wi-Fi, chevron, close, or send icons from
  CSS boxes, borders, pseudo-elements, or text glyphs.
- Inline SVG must use the canonical geometry from its declared source and use
  `currentColor` for adaptable strokes/fills unless the approved asset is
  intrinsically multicolor.
- A legal outer button does not legalize an unknown icon inside it. The icon
  leaf still needs `data-icon-source` and `data-icon-name`.

## Control and Geometry Contract

- An icon-only control must have an accessible name through `aria-label` or a
  visible label association.
- Mobile icon-only controls must measure at least 44x44px. The graphic may be
  16-24px inside the target.
- Center the graphic using layout (`display:grid; place-items:center` or
  equivalent), not compensating transforms or arbitrary offsets.
- The rendered graphic center may differ from the control center by at most 2px
  on either axis. A larger offset is a P1 failure.
- The rendered control must contain an actual `svg`, `img`, or explicitly
  sourced `[data-icon-visual]`. A label alone is not a rendered icon.
- Signal, Wi-Fi, and battery in a simulated status bar must all use
  `data-icon-source="platform-native"` from one coherent set.

## Acceptance

Static QA reports unsourced icon leaves, Unicode icon controls, and CSS-built
platform icons. Browser QA blocks missing rendered graphics, untrusted source
metadata, and icon/control center offsets above 2px. Fix the icon source or
layout; do not suppress the finding with an extra wrapper.
