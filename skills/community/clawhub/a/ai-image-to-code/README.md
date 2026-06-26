# AI Image To Code

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Converts UI screenshots into HTML/CSS or React components — rebuilds designs as working code

## What Problem This Solves

User has a design mockup or screenshot and needs it as actual code they can run — not a description, not a Figma export, but working HTML/CSS or a React component that looks like the original.

**When triggered:** UI screenshot/image + code/generate/rebuild intent.

## Features

- **Vision-powered layout extraction** — analyzes screenshot for structure (header, sidebar, main content), color palette, typography hierarchy, and spacing
- **Multi-format output** — plain HTML/CSS (default) or React + Tailwind CSS (for component requests)
- **Mobile-first responsive** — detects mobile screenshots and outputs `max-width: 375px` containers
- **Placeholder content** — uses contextually appropriate text ("Price: $49.99" not generic lorem ipsum)

## Quick Start

```bash
# Via ClawHub
clawhub install ai-image-to-code

# Or manually
cp -r ai-image-to-code ~/.openclaw/skills/
```

### Usage

```
/ai-image-to-code
```

Paste screenshot, ask to generate HTML/CSS.

```
/ai-image-to-code/react
```

Asks for React + Tailwind output instead of plain HTML.

```
/ai-image-to-code/describe
```

Just want a text description of the layout first — no code generation.

## Modes

| Mode | Description |
|------|-------------|
| `/ai-image-to-code` | Converts UI image to HTML/CSS |
| `/ai-image-to-code/react` | Outputs React functional component with Tailwind |
| `/ai-image-to-code/describe` | Text description of layout, no code |

## Examples

| Input | Output |
|-------|--------|
| E-commerce product card | "Price: $49.99 — Add to Cart" contextually appropriate |
| Dark mode UI screenshot | Dark background, light text, correct contrast applied |
| Mobile app screen | `max-width: 375px` container, mobile-first |
| Complex dashboard | Grid layout with sidebar, header, main panels |

## Directory Structure

```
ai-image-to-code/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Color extraction, layout patterns, Tailwind mapping
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).