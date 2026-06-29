---
name: antd-design-language
description: >-
  A design-language assistant for Ant Design (antd). Use when the user wants to learn, apply,
  critique, or theme UIs according to Ant Design's design language — its four design values
  (Natural / Certain / Meaningful / Growing), ten design principles, color/typography/layout/motion
  specs, and v5 design tokens (seed/map/alias). It also explains the underlying design-science and
  psychology (Gestalt, CRAP, UX laws, Norman's principles, cognitive load, color/contrast theory)
  behind each rule, and compares Ant Design with other design languages (Material Design, Apple HIG,
  Fluent, Carbon, and Chinese peers Arco / TDesign / Semi / Element Plus). Triggers: "Ant Design /
  antd 设计语言 / 设计规范", design-system review, "why does antd do X", "antd vs Material", theme/token
  customization, UI design critique.
---

# Ant Design — Design Language Assistant

A knowledge base + working method for **Ant Design (antd)**'s design language: not just *what* the
rules are, but *why* they exist (the design-science and psychology beneath them) and *how* they
compare to other systems. Use it to **teach**, **apply**, **critique**, or **theme** interfaces.

Ant Design is an **enterprise-grade (B-side / productivity) design system**. Its north star is
**certainty and low "collaboration entropy"** — consistent, predictable interfaces that reduce
users' cognitive and operational cost. Keep that lens when applying it: antd optimizes for
*information density, consistency, and efficiency*, not consumer flash.

## Four design values (the soul)

| Value | 中文 | Meaning | Rooted in |
| --- | --- | --- | --- |
| **Natural** | 自然 | Interactions follow human intuition & nature's order; reduce unnecessary thinking. | Mental models, affordances, Gestalt |
| **Certain** | 确定性 | Consistent rules → designers make fewer ad-hoc choices, users relearn nothing. | Jakob's Law, consistency, cognitive load |
| **Meaningful** | 意义感 | Every interface serves the user's goal and gives meaningful feedback. | Goal-gradient, feedback, peak-end |
| **Growing** | 生长性 | The system + the product evolve together; design scales as a living system. | Design tokens, modularity, systems thinking |

## Ten design principles

CRAP / Gestalt foundations → **Proximity · Alignment · Contrast · Repetition**.
Interaction principles → **Make it Direct · Stay on the Page · Keep it Lightweight · Provide an
Invitation · Use Transition · React Immediately**. Each is mapped to its psychological root in
`references/design-values-principles.md`.

## How to use this skill

Pick the mode that matches the request:

- **Learn / explain** — answer "what does antd say about X / why" using `references/`. Always pair
  the *rule* with its *reason* (the design-science/psychology), which is this skill's differentiator.
- **Apply / build** — when generating an antd UI or theme, follow `references/visual-language.md`
  (exact specs) and `references/design-tokens.md` (v5 tokens + `ConfigProvider` code). Use
  `assets/theme.example.ts` as a starting theme.
- **Critique / review** — audit a screen against `assets/review-checklist.md`; cite the violated
  principle *and* the psychological cost of violating it.
- **Compare** — position antd against other design languages with `references/comparison.md` and give
  a "which to choose" recommendation.

## Quick facts (v5)

- **Primary / brand:** `#1677FF` (Daybreak Blue). Functional: success `#52C41A`, warning `#FAAD14`,
  error `#FF4D4F`, info `#1677FF`. Palettes are 10 steps (index 1–10, primary at 6) from an algorithm.
- **Type:** base **14px / line-height 22px**; system font stack; limit to 3–5 sizes; weights 400/500
  (600 sparingly); `font-variant-numeric: tabular-nums` for figures.
- **Layout:** **8px** base grid, spacing in multiples of 8; **24-column** grid; 1440px design canvas.
- **Tokens:** Seed (`colorPrimary`, `borderRadius: 6`, `fontSize: 14`, `sizeUnit: 4`…) → Map → Alias;
  three algorithms: `defaultAlgorithm`, `darkAlgorithm`, `compactAlgorithm` (combinable).

## Files in this skill

| Path | Read it when you need… |
| --- | --- |
| `references/design-values-principles.md` | The 4 values + 10 principles in depth, each mapped to the design-science/psychology law it expresses. |
| `references/visual-language.md` | Exact visual specs: color system & palettes, typography scale, 8px layout & 24-grid, icons, motion, shadow/elevation, radius, dark mode. |
| `references/design-tokens.md` | The v5 token architecture (seed/map/alias), the three algorithms, and how to theme via `ConfigProvider` + `theme` (with code). |
| `references/psychology-design-science.md` | The "why" toolbox: Gestalt, CRAP, ~15 UX laws, Norman's principles, cognitive-load theory, color & contrast science — with how each maps to antd. |
| `references/comparison.md` | Ant Design vs Material Design, Apple HIG, Fluent, Carbon, and Chinese peers (Arco / TDesign / Semi / Element Plus) — philosophy, visuals, and a decision guide. |
| `assets/review-checklist.md` | A practical UI audit checklist: rule → principle → psychological reason, for design reviews. |
| `assets/theme.example.ts` | A ready `ConfigProvider` theme (brand color, light/dark/compact, component tokens) to copy. |

## Working rule

When you state an antd rule, **always give its reason** — the Gestalt/CRAP/UX-law/Norman/cognitive
principle behind it. "Antd uses 8px spacing" is trivia; "antd uses an 8px rhythm because consistent
spacing leverages the Gestalt law of *common region/proximity* to group related controls and lowers
extraneous cognitive load" is the assistant's value. That pairing is the whole point of this skill.
