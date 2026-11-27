# color-system-design

[简体中文](./README.md) | English

When building websites, apps, or doing Vibe Coding, colors easily drift into a messy, clashing palette.

This project glues together well-established open-source standards and tools—**GitHub Primer** semantic roles, **Adobe Leonardo** contrast math, **W3C DTCG / Style Dictionary**, and **APCA** perceptual contrast—to produce a **rock-solid color matrix that needs almost zero manual tweaking**.

**You only provide 1 primary brand hex color.** It automatically computes a complete, balanced color matrix—including backgrounds, text, borders, interactive states, non-clashing status colors, and separate light/dark themes.

It outputs two core deliverables:
1. **A human-readable HTML report** (`dist/color-report.html`): preview real web & mobile app mockups, toggle light/dark mode, check role rules, and click to copy variables.
2. **Constraint tooling for AI & code**: ready-to-use CSS variables, Tailwind v4 `@theme` / v3 presets, W3C DTCG tokens, and a linter to stop AI or teammates from hardcoding random hex values later.

---

## Quick Start

```bash
# 1. Install dependencies
pnpm install

# 2. Provide 1 primary hex color (e.g. #2563eb)
pnpm generate -- --seed "#2563eb"
```

Check `dist/` for the generated files:
- **For humans**: open `dist/color-report.html` in any browser
- **For code**: import `dist/tokens.css` (CSS variables), `dist/tailwind.theme.css` (Tailwind v4 `@theme`), or `dist/tailwind.preset.cjs` (Tailwind v3)

Common options:
- `--tint subtle|pure|warm|cool`: adjust neutral gray tinting (default `subtle`)
- `--no-semantic`: generate core `danger` only, skipping `success/warning/info`
- `--out ./my-theme`: custom output directory

---

## How It Works

Given a single hex seed, the pipeline runs 5 deterministic steps:

1. **Lock paper & neutral grays (OKLCH)**: takes the seed's hue with ultra-low chroma (`C ≤ 0.012`) and binary-searches lightness to hit target contrast ratios for both light and dark surfaces.
2. **Solve interactive accent scales (Adobe Leonardo)**: feeds the locked paper colors as backgrounds into Leonardo to solve accent text & hover steps. Dark mode uses an independent bright seed of the same hue instead of naive inversion.
3. **Generate non-clashing status colors**: creates `danger`, `success`, `warning`, and `info` tokens; if your brand color is close to a status hue (`< 35°`), the status hue automatically shifts away.
4. **Map to semantic roles & verify (Primer + WCAG/APCA)**: assigns colors to `fgColor` / `bgColor` / `borderColor` / `focus` roles and checks every pair against both WCAG 2.1 and APCA (`apca-w3`).
5. **Bundle outputs**: writes the standalone `dist/color-report.html` alongside CSS, Tailwind, and DTCG JSON files.

---

## Constraint Checks for AI / CI

```bash
# Rebuild CSS from tokens/
pnpm tokens:build

# Run topology, contrast, and optional literal-scan checks (--scan ./src)
pnpm tokens:check
```

---

## Repository Layout

- `scripts/generate-color-system.mjs`: main generator (1 hex -> full deliverables)
- `scripts/build-color-tokens.mjs` & `check-color-tokens.mjs`: DTCG compiler & math linter
- `color-roles.md`: semantic role responsibilities & prohibitions
- `SKILL.md`: AI Agent Skill specification
