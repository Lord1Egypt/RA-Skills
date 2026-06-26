# AI Image To Code

**Emoji:** 🖼️→💻

**Trigger:** User pastes a UI screenshot/image and wants code (HTML/CSS or React).

## What It Does

Converts UI screenshots into working HTML/CSS or React + Tailwind components. Analyzes the layout structure, color palette, typography hierarchy, and spacing to produce faithful code reconstruction.

## Features

- Vision-powered layout extraction (header, sidebar, main content, etc.)
- Multi-format output: plain HTML/CSS (default) or React + Tailwind CSS
- Mobile-first responsive (detects mobile screenshots → max-width: 375px)
- Contextual placeholder content (e.g., "Price: $49.99" not lorem ipsum)

## Modes

| Mode | Description |
|------|-------------|
| `/ai-image-to-code` | Convert UI image to HTML/CSS |
| `/ai-image-to-code/react` | Output React functional component + Tailwind |
| `/ai-image-to-code/describe` | Text description of layout, no code |

## How To Use

```
/ai-image-to-code
```
Paste a screenshot, ask to generate HTML/CSS.

```
/ai-image-to-code/react
```
Asks for React + Tailwind output instead.

```
/ai-image-to-code/describe
```
Just describe the layout, no code generation.

## Technical Notes

- Uses MiniMax vision model to analyze screenshot
- Detects dark mode and applies appropriate color schemes
- Generates semantic HTML structure
- Tailwind classes mapped from visual analysis

---

*Last updated: 2026-05-28*