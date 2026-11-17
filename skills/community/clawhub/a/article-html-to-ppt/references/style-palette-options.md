# Style Palette Options

Each style has 2-3 pre-defined palette options. The user picks one style and one palette at the start of a deck (see Gate 3: Visual Direction Confirmation in SKILL.md). DO NOT generate colors outside this list unless the user explicitly provides new hex values. Words like "restrained", "modern", "premium", or "tech" are NOT color instructions — always resolve to a concrete palette id below.

Token meaning:
- `primary`: dominant brand/structure color (titles, key bars, headers).
- `accent`: emphasis color (callouts, key figures, active states).
- `background`: page base color.
- `text`: primary body/text color on the background.
- `secondary`: supporting/secondary accent (dividers, tags, muted labels, chart series 2).

Write the chosen palette alias and complete design tokens into `.ppt-work/contracts/style-contract.json`.

---

## consulting-light

### palette-cl-mckinsey (麦肯锡钢青蓝)
- primary: #0A2233
- accent: #2C4A6E
- background: #FBFBF8
- text: #2A2E35
- secondary: #7C7669
- border: #E4E0D7
- surface: #F1EFEA

### palette-cl-bcg (BCG灰调橄榄绿)
- primary: #0E3D28
- accent: #3E7A55
- background: #FAF9F5
- text: #2A2E35
- secondary: #7C7669
- border: #E4E0D7

---

## product-report

### palette-pr-linear (Linear 风 — warm slate + muted lavender)
- primary: #232030
- accent: #6B5B95
- background: #F6F5F2
- text: #2A2E35
- secondary: #7A746B
- border: #E3DFD6
- surface: #EDEBE6

### palette-pr-stripe (Stripe 风 — near-black + restrained steel blue)
- primary: #14161A
- accent: #3A5A8C
- background: #FAFAF7
- text: #242526
- secondary: #79746B
- border: #E4E0D7

---

## technical-blueprint

### palette-tb-ibm-whitepaper (IBM 白皮书 — restrained engineering blue, print-friendly)
- primary: #2A5578
- accent: #2A5578
- background: #FAFAF7
- text: #2A2E35
- secondary: #3B3A34
- muted: #6E6A60
- border: #DAD5CB
- surface: #EFEDE7

Note: accent = primary here. Use neutral `#3B3A34` as second-tier emphasis for secondary nodes. Rely on weight and spatial isolation for hierarchy, not a second hue.

---

## consulting-blueprint-hybrid

### palette-cbh-deep-amber (深蓝 + 琥珀金)
- primary: #1B2A42
- accent: #C69749
- background: #FAF9F5
- text: #2D3340
- secondary: #6E6A60
- border: #E4E0D7

Use accent sparingly — a highlight rule, a number underline, a single labeled arrow. Never as a large fill.

---

## editorial-knowledge

### palette-ek-warm-paper (暖棕纸质感)
- primary: #2B2621
- accent: #C65D3B
- background: #FBF8F1
- text: #4A423A
- secondary: #857C70
- border: #E4DDCF
