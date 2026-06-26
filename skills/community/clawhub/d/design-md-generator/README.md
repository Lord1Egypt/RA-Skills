# 🎨 Design MD Generator

> **[中文文档](README_CN.md)**

**One URL in, complete DESIGN.md out.** Extract any website's visual DNA into a structured markdown file that AI coding agents can read to build pixel-perfect matching UI.

## What is DESIGN.md?

[DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) is a concept introduced by Google Stitch — a plain-text design system document that AI agents read to generate consistent UI. Think of it as `AGENTS.md` for how to build, but `DESIGN.md` for how things should *look*.

This skill automates the creation of DESIGN.md files from any live website.

## How It Works

```
Website URL → Screenshot + CSS Extraction → Structured DESIGN.md
```

The skill:
1. **Captures** the target site via browser (screenshot + DOM snapshot)
2. **Extracts** all design tokens — colors, fonts, spacing, shadows, borders, components
3. **Generates** a complete DESIGN.md with 9 standardized sections

## Output Format

Every generated DESIGN.md follows the [Google Stitch format](https://stitch.withgoogle.com/docs/design-md/format/):

| # | Section | What it captures |
|---|---------|-----------------|
| 1 | Visual Theme & Atmosphere | Mood, density, design philosophy |
| 2 | Color Palette & Roles | Semantic color names + hex + functional roles |
| 3 | Typography Rules | Font families, full hierarchy table |
| 4 | Component Stylings | Buttons, cards, inputs with all states |
| 5 | Layout Principles | Spacing scale, grid system, whitespace |
| 6 | Depth & Elevation | Shadow system, surface hierarchy |
| 7 | Do's and Don'ts | Design guardrails and anti-patterns |
| 8 | Responsive Behavior | Breakpoints, touch targets, collapsing strategy |
| 9 | Agent Prompt Guide | Quick color reference + ready-to-use prompts |

## Usage

### With OpenClaw

```bash
clawhub install design-md-gen
```

Then tell your agent:
> "Generate a DESIGN.md from https://linear.app"

### What You Get

Drop the generated `DESIGN.md` into any project root, then tell your AI coding agent:
> "Build me a landing page following the DESIGN.md"

The agent reads the design system and produces UI that actually matches the target aesthetic.

## Examples

The skill has been used to generate DESIGN.md files for sites like:
- **Linear** — Ultra-minimal dark mode, indigo-violet accent
- **Vercel** — Black and white precision, Geist font system
- **Supabase** — Dark emerald theme, code-first aesthetic
- **Stripe** — Signature purple gradients, weight-300 elegance

## Skill Structure

```
design-md-generator/
├── SKILL.md                          # Workflow guide
├── scripts/
│   └── extract-tokens.js             # CSS token extraction (Puppeteer)
└── references/
    ├── format-spec.md                # 9-section format specification
    └── example-linear.md             # High-quality reference example
```

## Inspired By

- [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) — The original concept
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — Curated collection of 55 hand-crafted DESIGN.md files

## License

MIT
