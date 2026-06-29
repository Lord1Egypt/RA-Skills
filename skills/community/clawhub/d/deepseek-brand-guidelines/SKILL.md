---
name: brand-guidelines
description: Applies DeepSeek's official brand colors and typography to any sort of artifact that may benefit from having DeepSeek's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---

# DeepSeek Brand Styling

## Overview

To access DeepSeek's official brand identity and style resources, use this skill.

DeepSeek（深度求索）is a Chinese AI company founded in 2023. Its brand identity centers around a friendly blue whale mascot — symbolizing wisdom, depth, exploration of the unknown, and approachability. The visual identity stands out in the AI industry for its warm, human-first design philosophy.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, DeepSeek brand, visual formatting, visual design, AI branding, whale

## Brand Philosophy

DeepSeek's brand identity communicates:

- **Exploration** ("Into the unknown") — the whale represents diving deep into uncharted territory
- **Approachability** — warm, friendly, and non-intimidating AI branding
- **Intelligence without arrogance** — competent but humble
- **Openness** — open-weight models, open research philosophy

## Brand Guidelines

### Colors

**Primary Brand Color:**

| Color | Hex | RGB | Usage |
|-------|:---:|:---:|-------|
| DeepSeek Blue | `#4D6BFE` | `rgb(77, 107, 254)` | Primary brand color — homepage, brand accent, interactive elements |
| DeepSeek Blue (Chat) | `#3964FE` | `rgb(57, 100, 254)` | Chat interface primary — buttons, links, login elements |
| DeepSeek Blue (Platform) | `#3B82F6` | `rgb(59, 130, 246)` | Developer platform — API docs, platform UI |

**Neutral Palette:**

| Color | Hex | RGB | Usage |
|-------|:---:|:---:|-------|
| Dark Text | `#0F1115` | `rgb(15, 17, 21)` | Primary text and headings |
| Medium Gray | `#81858C` | `rgb(129, 133, 140)` | Secondary text, labels, captions |
| Slate Gray | `#94A3B8` | `rgb(148, 163, 184)` | Disabled state, muted elements (used on homepage) |
| Light Gray | `#E5E7EB` | `rgb(229, 231, 235)` | Navigation bars, subtle borders |
| Subtle Background | `#F9FAFB` | `rgb(249, 250, 251)` | Subtle backgrounds, card surfaces |
| White | `#FFFFFF` | `rgb(255, 255, 255)` | Primary backgrounds, content areas |

**Accent & Status Colors:**

| Color | Hex | RGB | Usage |
|-------|:---:|:---:|-------|
| Success Green | `#22C55E` | `rgb(34, 197, 94)` | Success states, positive indicators |
| Warning Orange | `#F97316` | `rgb(249, 115, 22)` | Warning states, caution indicators |
| Error Red | `#EF4444` | `rgb(239, 68, 68)` | Error states, destructive actions |

### Typography

**Primary Font Family:**

- **Headings / UI Text**: Inter (with system-ui fallback)
- **Body Text**: Inter (with system-ui fallback)
- **Monospace**: JetBrains Mono or SF Mono (code blocks)

**Font Stack (preferred):**

```
font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont,
             "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell,
             "Open Sans", "Helvetica Neue", sans-serif;
```

**CJK Text (Chinese, Japanese, Korean):**

```
font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
             "Noto Sans CJK SC", sans-serif;
```

**Logo Wordmark Style:**

- Custom geometric sans-serif typeface (similar to Prayuth / Ruberoid / Soliden)
- Lowercase with open contours and rounded edges
- Slightly detached triangular segment in the letter "K"
- Not available for public use — refer to official brand assets

**Typography Rules:**

- Maintain generous letter-spacing for headings
- Use regular weight (400) for body text, medium (500) or semibold (600) for headings
- Avoid using thin (100/200) weights for body text
- Left-align text by default for readability

### Logo

- **Emblem**: A friendly blue whale mascot — symbolizing wisdom, depth, exploration, and calm
- **Wordmark**: Lowercase "deepseek" in a rounded geometric sans-serif with open contours
- The whale complements the name's implication of "deep" exploration
- Always use the official logo assets; do not recreate, modify, or distort
- Maintain clear space around the logo equal to at least the height of the "d" in "deepseek"

## Features

### Smart Color Application

- Applies DeepSeek Blue (`#4D6BFE`) as the primary accent color
- Chat interface uses `#3964FE` for interactive elements
- Uses the neutral palette for text hierarchy — dark for primary content, medium gray for secondary
- Smart color selection based on background (white backgrounds for content, subtle backgrounds for cards)
- Maintains readability and WCAG contrast across all surfaces

### Shape and Accent Application

- Non-text shapes use DeepSeek Blue by default
- Status indicators use the appropriate accent color (green/warning/red)
- Buttons and interactive elements use DeepSeek Blue as primary
- Hover states may use a darker variant of DeepSeek Blue

### Text Styling

- Headings: Inter font, semibold weight (600), DeepSeek Dark (`#0F1115`)
- Body text: Inter font, regular weight (400), DeepSeek Dark (`#0F1115`)
- Secondary text: Inter font, regular weight (400), Medium Gray (`#81858C`)
- Preserves text hierarchy and formatting

### Font Management

- Uses Inter as the primary font, with system-ui fallback (available on most systems)
- No font installation required — works with existing system fonts
- For best results, pre-install Inter from Google Fonts or fonts.google.com
- CJK text automatically uses system Chinese/Japanese/Korean fonts

## Technical Details

### Color Application

- Uses RGB and Hex color values for precise brand matching
- Applied via standard color classes
- Maintains color fidelity across different systems

### Accessibility

- Body text on white backgrounds: high contrast ratio (≥7:1)
- Large text (18pt+ / 24px+) on white backgrounds: high contrast ratio (≥4.5:1)
- DeepSeek Blue (`#4D6BFE`) on white: passes WCAG AA for large text (`#3964FE` also passes)
- Avoid using DeepSeek Blue on light gray backgrounds for body text

## Usage Examples

### Presentation Slides

- Title slides: DeepSeek Blue (`#4D6BFE`) background with white text, or dark navy (`#0F172A`) with DeepSeek Blue accents
- Content slides: White or Subtle Background with Dark Text headings
- Accent elements: DeepSeek Blue for highlights and call-to-action elements
- Product slides (Dual-model): Gold (`#F5B800`) for flagship/Pro, DeepSeek Blue for lightweight/Flash
- Data visualizations: DeepSeek Blue as primary with accent colors for categories
- Benchmark cards: use distinct accent colors per metric (gold, blue, green, orange, purple, pink)
- **Dual color-coding system**: Gold = premium/flagship tier, Blue = lightweight/open tier

### Code Blocks

- Use a dark theme with monospace font (SF Mono / JetBrains Mono)
- DeepSeek Blue for syntax highlighting of keywords
- Light background for inline code in documentation
