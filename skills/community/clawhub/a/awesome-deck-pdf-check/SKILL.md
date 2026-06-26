---
name: html-ppt-to-pdf
description: Turn any design style into a polished HTML slide deck and export it as a high-quality PDF. Triggers when users say things like "make me a nice PPT", "create slides based on X style", "build a deck", "generate presentation". Supports four input types: (1) Upload a .pptx template file — extract its colors, fonts and layout via python-pptx; (2) Share an image or screenshot of a design; (3) Provide a website URL to clone its visual style; (4) Describe a style in words (e.g. "Apple style", "Notion minimal", "Linear dark"). Output: pixel-sharp 1440×900 slides exported to PDF via Puppeteer, production-quality design.
---

# HTML → PDF Slide Workflow

## ‼️ STOP — Read Before Doing Anything

Before writing a single line of code or HTML, you MUST complete these two confirmation steps **in order**. Do not proceed until you receive explicit user approval for each.

### Confirmation 1 of 2: Design Style

Analyze the user's input (image / URL / keyword / .pptx), then show a design spec summary and ask:

> Here's the design style I extracted from [source]:
> - Background: `#000` dark / Accent: `#2997FF` blue
> - Font: SF Pro Display, oversized heading, minimal whitespace
> - Style: dark Keynote, glow effects
>
> **Does this match what you want? Any changes before I start?**

If the user provided a website URL and fetching fails (Fake IP, login wall, etc.):
- Say exactly why it failed
- Ask: **"Could you send a few screenshots of the site? I'll analyze the design from those."**
- Do NOT assume or default to any style

Wait for explicit approval → then move to Confirmation 2.

### Confirmation 2 of 2: Slide Content

Ask the user if they have existing materials:

> Do you have reference materials for the content?
> (existing PPT, doc, data, bullet points — anything works)
> If yes, send them over. If not, I'll draft an outline for you to review.

Once you receive a reply, prepare a numbered list: slide title + one-line summary per slide. Show it and ask:

> Here's the planned structure — does this look right? Anything to add, remove, or change?

Wait for explicit approval → **only then** begin generating HTML.

---

**If either confirmation is skipped, the workflow is broken. Start over from Confirmation 1.**

---

**`export_pdf.js` auto-detects Chrome in this order:**
1. Puppeteer bundled Chromium (`npm install puppeteer`)
2. System Chrome/Chromium (macOS: `/Applications/Google Chrome.app`, Linux: `/usr/bin/chromium`)
3. If neither found → prints a clear error with install instructions, exits

**If `npm install puppeteer` fails (sandbox/network restriction):**
```bash
# Option A: skip Chromium download, install separately
npm install puppeteer --ignore-scripts
npx puppeteer browsers install chrome

# Option B: use puppeteer-core (no bundled Chrome download)
npm install puppeteer-core
# script will auto-find system Chrome

# Option C: install system Chrome first, then run script
# macOS: brew install --cask google-chrome
# Linux: sudo apt install chromium-browser
npm install puppeteer-core
```
**Do NOT fall back to wkhtmltopdf, pdfkit, weasyprint, or any other tool.**

For full installation instructions across OpenClaw, Claude Code, Codex, and Linux/macOS setup, see `references/install.md`.

---

## Workflow Overview

```
User input (image / website URL / style keyword / .pptx file)
    ↓ Step 1: Extract design spec → ⚠️ Confirm with user
    ↓ Step 2: Outline slide content → ⚠️ Confirm with user
    ↓ Step 3: Generate HTML → 💾 Save slides.html to disk
    ↓ Step 4: Run export_pdf.js → 💾 Output slides.pdf
    
Both slides.html and slides.pdf must exist as final outputs.
```

---

## ⚠️ Two Mandatory Confirmation Gates (never skip)

### Gate 1: Design Style

After analyzing the input, show the extracted design spec summary and ask for confirmation:

> Here's what I extracted from [source]:
> - Background: `#000000` black · Accent: `#2997FF` apple blue
> - Font: SF Pro Display, oversized centered headline
> - Style: dark Keynote, glow effects
>
> Does this match the style you want? Any adjustments?

**⚠️ If website fetch fails (e.g. Fake IP / login required):**
- Tell the user clearly why it failed
- Ask for screenshots: **"Could you send a few screenshots of the site? I'll analyze the design from those."**
- **Never assume or default to any style** — wait for user confirmation before proceeding

**Website analysis priority:**
1. Puppeteer screenshot → visual analysis (most accurate)
2. `web_fetch` page content → CSS/font extraction
3. Ask user to send screenshots

### Gate 2: Slide Content

**First ask if the user has existing materials:**

> Do you have any reference materials for the content?
> e.g. existing PPT, doc, report, or a list of key points?
> Send them over and I'll structure the slides — otherwise I'll draft an outline for you to review.

After receiving a reply, prepare a one-line summary per slide and confirm before generating HTML.

---

## Step 1: Extract Design Spec → DESIGN.md

Supported inputs:

| Input | Approach |
|---|---|
| 📂 .pptx template | Parse with python-pptx: extract colors, fonts, backgrounds, placeholder layouts (most accurate) |
| 📎 Image / screenshot | Visual analysis: colors, font style, spacing, component patterns |
| 🌐 Website URL | Puppeteer screenshot + `getComputedStyle` font/color extraction |
| 💬 Style keyword | Use brand knowledge: Apple → SF Pro, Notion → Inter, Linear → Inter, Google → Google Sans |

**Extracting from .pptx:**
```python
from pptx import Presentation
prs = Presentation("template.pptx")
slide = prs.slides[0]
for shape in slide.shapes:
    if shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                print(run.font.name, run.font.size, run.font.color.rgb, run.font.bold)
```

Fill extracted values into DESIGN.md (see `references/DESIGN_TEMPLATE.md`):

- **Colors**: primary bg, secondary bg, text colors, accent, border → CSS variables
- **Fonts**: heading / body / decorative number — name, weight, size range per level
- **Layout**: padding, max-width, grid columns, gap, border-radius
- **Components**: card, badge/label, button, divider, background decoration
- **Section list**: CSS class + content theme + dark/light tone per slide

**Font extraction by input type:**

| Input | Method |
|---|---|
| `.pptx` | `run.font.name` per text run |
| Website | `getComputedStyle(el).fontFamily` via Puppeteer |
| Image / screenshot | Visual analysis — describe closest match (e.g. "geometric sans, similar to Helvetica") |
| Style keyword | Brand knowledge mapping |

Fonts go into DESIGN.md as CSS variables. Append Chinese fallbacks at the end (never hardcode them as primary):
```css
--font-heading: 'SF Pro Display', 'PingFang SC', 'Helvetica Neue', sans-serif;
--font-body:    'SF Pro Text',    'PingFang SC', 'Helvetica Neue', sans-serif;
```

---

## Step 2: Generate HTML

> ⚠️ **Save the HTML to a `.html` file first. Do not merge HTML generation and PDF export into one step.** The HTML file is a required intermediate artifact — it must exist on disk before running `export_pdf.js`.

Generate a single `.html` file and write it to disk (e.g. `slides.html`):

- Single file, all CSS inlined, zero external dependencies
- Each slide = one `<section class="...">`, fixed width **1440px**, height fits content
- Fonts from DESIGN.md — Chinese fallback appended, never hardcoded as primary
- `@media print`: `page-break-after: always` on every section

Font consistency check after saving:
```bash
grep -n "font-family" slides.html
```

Only proceed to Step 3 once the `.html` file is saved and verified.

---

## Step 3 & 4: Export PDF via Puppeteer

> ⚠️ **Only use `export_pdf.js` (Puppeteer screenshot-and-compose). Do NOT use any of these alternatives — they all produce broken output:**
> - `page.pdf()` directly → A4 portrait, white space below every slide
> - `wkhtmltopdf` → outdated WebKit engine, broken flexbox/grid/modern CSS
> - Any other HTML-to-PDF CLI (Prince, WeasyPrint, pdfkit, etc.) → layout incorrect
>
> The screenshot-and-compose approach is the only method that faithfully preserves the rendered layout.

### Environment matters

**Claude Code / Codex / OpenClaw / local agent** (can run shell commands):
- Read `scripts/export_pdf.js`, copy it to the project directory, run it:
```bash
node export_pdf.js              # reads slides.html → slides.pdf (auto-detects <section> elements)
node export_pdf.js my-deck.html # specify a different file
```

**Claude.ai chat / any chat-only interface** (cannot run shell commands):
- Your role ends at Step 3: generate the HTML and provide it to the user
- Tell the user: **"Here's your `slides.html`. To export the PDF, copy `scripts/export_pdf.js` from the skill folder to the same directory and run `node export_pdf.js`."**
- Do NOT attempt to run Puppeteer, install npm packages, or use any PDF tool in chat


```bash
node export_pdf.js              # reads slides.html → slides.pdf (auto-detects all <section> elements)
node export_pdf.js my-deck.html # specify a different HTML file
```

**Auto-detection:** The script automatically finds all `<section>` elements in DOM order — no need to manually set SELECTORS. Only configure `SELECTORS` manually if you need a custom slide order or to merge multiple elements into one slide:

```js
// Optional manual override — leave as [] for auto-detect
const SELECTORS = [
  '.cover',
  '.section-2',
  ['.chart', '.stats'],  // array = merge into one slide
];
```

See `references/export_pdf_guide.md` for details.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| PDF has white space / broken layout | Do not use `page.pdf()`, `wkhtmltopdf`, or any CLI PDF tool. Run `export_pdf.js` only — it uses Puppeteer screenshot-and-compose to preserve layout exactly |
| Chinese text renders as Song/Ming | Add `'PingFang SC'` to font stack (available on macOS by default) |
| Inconsistent fonts across slides | Run `grep -n "font-family" slides.html` and normalize |
| Wrong page count in PDF | Check that SELECTORS covers all sections |
| Detached Frame error | Use the reusable `overlayPage` pattern — never use `newPage()/close()` in a loop |
| Website URL fails to fetch | Likely Fake IP proxy — use Puppeteer screenshot instead, or ask user for screenshots |
