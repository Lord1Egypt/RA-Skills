# Fleece — Design Notes

Design decisions, rationale, and reference for `docs/index.html`.

---

## Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--yellow` | `#FFD100` | Primary accent — buttons, badges, logo, highlights |
| `--black` | `#111111` | Hero background, nav, footer, dark sections |
| `--white` | `#FFFFFF` | Primary page background, cards |
| `--gray` | `#F5F5F3` | Alternate section background (About, Workflows) |
| `--mid` | `#555555` | Secondary text, descriptions |
| `--border` | `#E0E0E0` | Card borders, dividers |

### Spirit Airlines tribute

The yellow (`#FFD100`) and black (`#111111`) palette is used **in honor of Spirit Airlines**, whose signature colors and ultra-low-cost spirit directly inspired this project. Spirit's wind-down page (`spiritrestructuring.com`) was also the primary design reference for the layout's restraint and whitespace philosophy.

---

## Typography

| Role | Font | Weight |
|---|---|---|
| Headings, labels, badges | [Oswald](https://fonts.google.com/specimen/Oswald) | 400 / 600 / 700 |
| Body, descriptions, nav | [Source Sans 3](https://fonts.google.com/specimen/Source+Sans+3) | 400 / 600 |
| Code, CLI examples | `'Courier New', monospace` | — |

Oswald and Source Sans 3 are the same font pairing used by Spirit Airlines (Oswald for bold headings, Source Sans for body). Loaded via Google Fonts with `preconnect` for performance.

---

## Design Philosophy

Inspired by two references:

### Spirit Airlines (`spiritrestructuring.com`)
- **White as the dominant background** — yellow is an accent, not wallpaper
- **Extreme restraint** — few sections, generous whitespace, one idea per block
- **Dark hero** — black/dark top section contrasts with white content beneath
- **Pill buttons with chevron arrows** — matching Spirit's "Learn More →" style
- **Minimal footer** — logo, copyright, one link

### OpenClaw (`openclaw.ai`)
- **Workflow-first content** — show real end-to-end examples, not just feature lists
- **Code blocks as CTAs** — install commands and CLI examples front and center
- **Stats strip** — quick-scan numbers for credibility at a glance
- **Community signals** — open issue CTA, GitHub link, open-source emphasis
- **Agent integration section** — explicit cards for each platform

---

## Page Structure

```
NAV           dark bg, yellow logo, pill GitHub CTA
HERO          dark bg, #1 badges, h1, install box with version chips
FEATURE CARDS white bg, 3 columns (Chatbot / CLI Research / Redemption)
STATS STRIP   dark bg, 4 numbers (13 commands, 981 MCCs, 0 keys, MIT)
WORKFLOWS     gray bg, 4 end-to-end code examples
ABOUT         gray bg, two paragraphs, dual CTA buttons
AGENT INT.    white bg, 3 cards (Claude Code / OpenClaw / ClawHub)
COMMANDS      white bg, split layout — links left, command list right
FOOTNOTE      dark bg, † ranking source + Spirit tribute
FOOTER        dark bg, logo, copyright, MIT license link
```

---

## Key Components

### `#1` Ranking Badges
Yellow Oswald-font pills above the hero h1. Reference source: ClawHub vector search registry, `fleece@1.5.0`, May 2026. The `†` superscript links to the footnote explaining the source so the claim is transparent.

### Hero Install Box
Dark card (`#1a1a1a`) on the dark hero background — a subtle card-within-card pattern. Contains the `pip install fleece-cli` command, version/Python/license chips, and the BRAVE_API_KEY optionality note.

### Workflow Cards
Each has a label pill (yellow on black), a plain-English question, and a two-step CLI code block showing the actual commands and output. Inspired by OpenClaw's "What People Are Building" section.

### Command List
Two-column: links (install, skills, contact) on the left; command rows on the right. Highlighted commands (yellow `cmd-name`) indicate no API key required.

### Footnote
Single dark-gray line below the footer. Contains:
1. `†` ranking attribution (ClawHub, version, date)
2. Spirit Airlines color tribute

---

## Responsive Breakpoint

`@media (max-width: 768px)` — hero, feature cards, agent cards, and contact section all collapse to single column.

---

## SEO

- Title: "Fleece — Credit Card Research CLI & Rewards Optimizer"
- Meta description: 155 chars, includes `pip install fleece-cli` CTA
- Canonical: `https://getfleece.io/`
- JSON-LD: `SoftwareApplication` schema
- Open Graph + Twitter Card
- Google Search Console verified
- Sitemap: `sitemap.xml`
- Full SEO change log: `docs/SEO.md`
