---
name: clone-website
description: Clone, copy, rebuild, or reverse engineer any website. Use when users request to clone a website, copy a page, replicate a webpage, or recreate one from scratch.
---

# Clone Website

Use browser automation tools to perform a complete website cloning workflow: Reconnaissance → Infrastructure → Components → Assembly → QA.

## Pre-flight Checks

Before starting, confirm:
1. Browser MCP tools are available (Playwright MCP or Chrome MCP, run `npx playwright install chromium` first to ensure browser readiness)
2. Target URL is accessible
3. Project is initialized: `npx create-next-app@latest` + Tailwind + shadcn/ui
4. Create documentation directory: `mkdir -p docs/research/components`

Only proceed to Phase One after all checks are complete.

## Phase One: Reconnaissance

### 1.1 Screenshot Capture
Execute using browser tools:
- Desktop full-page screenshot (1440px viewport width)
- Mobile full-page screenshot (390px viewport width)

### 1.2 Scroll Behaviors
Scroll down the page gradually from top to bottom, record to `docs/research/BEHAVIORS.md`:
- Whether navbar style changes with scroll (fixed/sticky, background color, shadow, height)
- Entry animations (which element, trigger condition, animation effect)
- Scroll snap behavior
- Parallax or sticky elements

### 1.3 Interaction Testing
- Click all interactive elements (buttons, links, tabs, accordions), record toggle/expand/popup feedback
- Hover to test hover effects (color change, underline, scale, shadow)
- Switch viewport to 768px and 390px, record layout breakpoint changes
- Append all findings to `BEHAVIORS.md`

## Phase Two: Infrastructure

### 2.1 Fonts
```js
// Run in browser console
Array.from(document.styleSheets)
  .flatMap(s => [...s.cssRules].map(r => r.cssText))
  .filter(t => t.includes('@font-face') || t.includes('font-family'))
```
Also extract from `<link>` tags and `getComputedStyle(document.body).fontFamily`. Download fonts to `public/fonts/`.

### 2.2 Color System
```css
/* Define in globals.css using CSS variables, example structure: */
:root {
  --background: #...;
  --foreground: #...;
  --primary: #...;
  --primary-foreground: #...;
  --muted: #...;
  --muted-foreground: #...;
  --border: #...;
  --radius: 0.5rem;
}
```
Extract exact color values from key elements using computed styles, do not rely on visual guessing.

### 2.3 Asset Download
- Download all `<img>`, `<video>`, `<source>` to `public/images/` and `public/videos/`
- Extract all inline SVGs as standalone `.tsx` components into `components/icons/`
- Use `wget` or `curl -O` for batch downloads, preserve original filenames

### 2.4 Verification
Run `npm run build` to confirm the project compiles after infrastructure setup.

## Phase Three: Component Specifications

For each page block (Navigation, Hero, Features, CTA, Footer, etc.), execute the following in order:

### 3.1 Precise CSS Extraction
In browser DevTools on the target element, run:
```js
const el = document.querySelector('selector');
const style = getComputedStyle(el);
// Record all non-default values
const props = ['padding','margin','border','borderRadius','boxShadow','backgroundColor','color',
  'fontSize','fontWeight','lineHeight','letterSpacing','display','flexDirection',
  'alignItems','justifyContent','gap','width','height','maxWidth','position',
  'top','right','bottom','left','zIndex','opacity','transform','transition','animation'];
props.forEach(p => { const v = style[p]; if (v) console.log(p, ':', v); });
```

### 3.2 DOM Structure Recording
- Extract HTML structure (right-click Copy → Copy outerHTML)
- Pay attention to layering: background layer + foreground layer + overlay may be 3 separate elements
- Pay attention to pseudo-elements `::before` / `::after` when they serve as decorations, handle them separately

### 3.3 State Style Extraction
For each state (hover, active, focus, disabled, open), manually trigger and then force the state via DevTools `:hover`, then run `getComputedStyle()` again to extract differences.

### 3.4 Text Transcription
Copy real text content (do not use lorem ipsum).

### 3.5 Output
Write a specification document for each component to `docs/research/components/<component-name>.md`, containing:
- Screenshot reference
- CSS properties table
- DOM structure
- State style differences
- Real text content
- Responsive breakpoint behaviors

## Phase Four: Build

Build React components one by one according to the specification documents.

### Discipline
- **One file per component**: `components/<ComponentName>.tsx`
- **Check after each component**: `npx tsc --noEmit`
- **Complete before optimizing**: Don't refine design as you write
- Map CSS properties to Tailwind classes, use `style={{}}` for precise values when necessary
- Use previously extracted icon components, do not substitute with lucide-react

## Phase Five: Assembly & QA

### 5.1 Assembly
Assemble all components in `app/page.tsx` in the same order as the original site.

### 5.2 Build Check
```bash
npm run build
```
Fix all errors until compilation passes.

### 5.3 Comparison Verification
1. `npm run dev` to start the local version
2. Open both the original site and the cloned site simultaneously in the browser
3. Scroll section by section to compare, fix discrepancies
4. Verify responsiveness at three widths: 390px, 768px, and 1440px

## Key Principles

- **CSS must be extracted using `getComputedStyle()`** — no visual estimation, no guessing
- **Scroll before clicking** — first determine if interactions are scroll-driven or click-driven
- **Extract all states** (:hover, :active, :focus, :disabled), not just default state
- **Pay attention to layering** — a visual effect may consist of three layers: background + foreground + overlay
- **Assets must be downloaded locally** — do not link to original site resources
- **Text must be transcribed verbatim** — no placeholder text

## Constraints

- Do not use for phishing, spoofing, or fraud
- Logo and brand assets remain property of their original owners
- Only clone websites you own or have permission to use