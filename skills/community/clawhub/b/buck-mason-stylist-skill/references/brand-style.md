# Buck Mason brand style guide

A snapshot of the live storefront's visual language, extracted from `buckmason.com` directly (homepage + `/collections/curved-hem-tees` + `/products/white-slub-curved-hem-tee`) on **2026-05-05**. Use this when rendering any branded surface inside the skill — the `html-cart` lookbook in particular — so the output reads as "by Buck Mason," not "AI-generated for Buck Mason."

For higher-stakes artifacts the agent can optionally re-extract live (script in the appendix). Treat this file as a fast default; trust the live site if they diverge.

## At a glance

- **One typeface family does almost everything**: Adobe **Acumin Pro** (regular + condensed). Body text is regular Acumin Pro; every label, headline, button, and nav item is **Acumin Pro Condensed, UPPERCASE, with +2% letter-spacing**. There are no serifs anywhere on the standard catalog. Don't reach for Georgia, Canela, Söhne, or any "editorial serif" instinct — that's not how Buck Mason looks.
- **The page is white.** `#FFFFFF` body, `#333333` text. Off-white `#F3F1EF` shows up only as an accent (header announcement banner). Don't paint the whole page off-white; that reads more J.Crew than Buck Mason.
- **Imagery does the heavy lifting.** Headlines are small (~20px), tightly scaled, never bigger than the body's gallery photos. The brand voice is conveyed by hero photography and copy decks, not by display typography.
- **Sharp corners.** `border-radius: 1px` (≈ 0) on CTAs, size selectors, and product tiles. Pills only on round badges (color swatches, etc., where `border-radius: 50%`).
- **3:4 portrait product crops** (`0.75` aspect). Not 4:5, not 1:1, not 16:9.

## Colors

| Role | Value | Where it shows up |
|---|---|---|
| Page background | `#FFFFFF` (rgb 255,255,255) | `<html>`, `<body>`, `<main>` |
| Primary text | `#333333` (rgb 51,51,51) | Body, headings, prices |
| Active CTA | `#000000` on white text | "Add to Bag" once a size is selected (inferred from disabled state) |
| Disabled CTA | `#AAAAAA` background, white text | "Select Size to Add to Cart" pre-size-pick |
| Accent neutral | `#F3F1EF` (warm off-white) | Header announcement banner; subtle section panels |
| Disabled-element text | `#D9D9D9` | Sold-out size selectors |
| Border / hairline (when used) | `rgba(0,0,0,0.08)`-ish | Product tiles, form fields |

The site is otherwise **chromatic only through product imagery** — no brand reds/greens/blues. Stick to the white + black + grayscale stack and let the photos carry color.

## Typography

### Stacks

```css
/* Body */
font-family: acumin-pro, Helvetica, sans-serif;

/* Headlines, labels, nav, buttons — every cap/eyebrow/CTA */
font-family: acumin-pro-condensed, Helvetica, sans-serif;
```

Acumin Pro / Acumin Pro Condensed are licensed via Adobe Fonts. If the rendered surface is a self-contained file (`html-cart`) and we deliberately don't `<link>` external font CDNs (per `references/output-formats.md`), fall back to **`Helvetica Neue Condensed`** then **`Helvetica`** for the condensed face, and **`Helvetica`** then a generic sans for the regular face. Don't substitute Inter, Söhne, IBM Plex, or any other variable sans — they'll read as "designer-default," not Buck Mason.

```css
/* Acceptable degraded stack for self-contained HTML */
--bm-cond: "Acumin Pro Condensed", "Helvetica Neue Condensed", "Helvetica Neue", Helvetica, Arial, sans-serif;
--bm-body: "Acumin Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
```

### Sizes (live values, computed)

| Element | Family | Weight | Size | Line-height | Letter-spacing | Transform |
|---|---|---|---|---|---|---|
| Body | acumin-pro | 400 | 13px | 18.2px (1.4) | normal | none |
| Nav link | acumin-pro-condensed | 400 | 16.4px | — | 0.33px (≈2%) | UPPERCASE |
| Hero CTA label | acumin-pro-condensed | 600 | 18.2px | — | 0.36px (≈2%) | UPPERCASE |
| PLP h1 (collection name) | acumin-pro-condensed | 400 | 20.15px | 20.15px (1.0) | 0.40px (≈2%) | UPPERCASE |
| PLP h2 (collection blurb) | acumin-pro-condensed | 700 | 19.5px | 27.3px | 0.39px (≈2%) | UPPERCASE |
| PDP h1 (product title) | acumin-pro-condensed | 600 | 20px | 20px (1.0) | 0.40px (≈2%) | UPPERCASE |
| PDP price | acumin-pro | 400 | 14px | — | normal | none |
| Add-to-Bag (disabled) | acumin-pro-condensed | 700 | 14.3px | — | 0.29px (≈2%) | UPPERCASE |
| Sold-out size button | sans-serif | 400 | 11.7px | — | normal | none |

### The 2% letter-spacing rule

Almost every condensed-uppercase element on the site has letter-spacing of approximately `0.02em` (= 2% of font size). Apply this to every uppercase label, eyebrow, button, and nav item. The exact value matters: `0.18em` is too loose (reads as "design-systemy," not Buck Mason), `0` is too tight (reads as a tee-shirt logo).

```css
.bm-label { font-family: var(--bm-cond); text-transform: uppercase; letter-spacing: 0.02em; }
```

### Headlines stay small

This is counterintuitive coming from most agencies' "editorial" defaults. Buck Mason's largest h1 on a typical page is **20px**. The brand's display moment is the photography, not 72px serif type. Don't render a `<h1>` at 48px even on a "cover" — keep the title compact and let the lookbook image tile carry the space.

### Custom fonts present but unused on standard catalog

The site loads `@font-face` rules for `MasonGothic` (300/400/700) and `PonomarUnicode`. Neither was in use on the homepage, mens collection, or a representative PDP at extraction time. They likely render on marketing/editorial pages or the Mason Made sub-brand. **Don't substitute either into our HTML output** — match the live storefront's standard-catalog look, which is Acumin-only.

## Buttons & form controls

### Primary CTA ("Add to Bag", "Send to my stylist", etc.)

```css
.bm-cta {
  font-family: var(--bm-cond);
  font-weight: 700;
  font-size: 14px;            /* 14–18px range; 14 for inline, 18 for hero overlays */
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: #ffffff;
  background: #000000;        /* solid black when active */
  border: 0;
  border-radius: 1px;          /* essentially square; never 4px+ pills */
  padding: 16px 22px;
  width: 100%;                 /* full-width on PDP-style pages */
  cursor: pointer;
}
.bm-cta[disabled] { background: #aaaaaa; cursor: not-allowed; }
```

### Secondary / outlined CTA

Pattern observed: black 1px border, transparent or white background, black text, otherwise identical typography. Use for "Cancel" / "Back" / lower-priority actions.

```css
.bm-cta-secondary {
  border: 1px solid #1a1a1a;
  background: transparent;
  color: #1a1a1a;
  /* same typography as .bm-cta */
}
```

### Size selector (rectangular, NOT pill)

```css
.bm-size {
  width: 58px; height: 41px;   /* slightly wider than tall */
  border: 1px solid #1a1a1a;
  background: #ffffff;
  font-family: sans-serif;     /* Buck Mason uses generic sans here, deliberately plain */
  font-size: 12px;
  border-radius: 1px;
  cursor: pointer;
}
.bm-size[aria-selected="true"] { background: #1a1a1a; color: #ffffff; }
.bm-size[aria-disabled="true"] { color: #d9d9d9; cursor: not-allowed; }
```

### Checkbox (interactive lookbook handoff)

The storefront doesn't expose a custom checkbox we can mirror directly, but the same minimal black/white logic applies: 16×16px, 1px black border, black fill on `:checked`, no rounded corners. Already in the `html-cart` skeleton in `references/output-formats.md`.

## Images

- **Aspect ratio for product imagery: 3:4 portrait** (`width / height = 0.75`). Native files are 1350×1800; displayed around 900×1200. Use this ratio for both gallery hero images and lookbook try-on images. **Do not use 4:5, 1:1, or 16:9** — they read as Instagram, not Buck Mason.
- **No filter, no overlay, no faux-vintage.** Photography is direct, well-lit, naturally toned. Try-on images generated by gpt-image-2 should be passed through with no post-effect.
- **Hover swap** is the standard product-tile interaction (front view → back/detail view). Optional in the lookbook; don't bother for v1.
- **CDN host is `cdn.shopify.com`** — already declared in `clawhub.json#permissions.network`.

### Social-preview hero (`og.jpg`)

Different format, same brand rules. When the lookbook is hosted (`html`/`html-cart`), the agent ships a **1200×630 JPEG** alongside the page so iMessage / Slack / Discord / Twitter unfurl with a hero tile. Two rules:

- **Letterbox the 3:4 hero on a white (`#FFFFFF`) background.** Don't crop the model out of frame to fit 1.91:1 — crop loses the outfit; letterbox preserves it. Buck Mason's white page background absorbs the letterbox naturally.
- **No type overlay on the OG image.** The chat client renders the page title separately; doubling up reads as cluttered. The image itself is just the look.

Pillow recipe lives in `references/hosting-options.md` § "The og.jpg artifact." Shopify-CDN fallback for when local generation isn't possible is in the same section.

## Layout

- **Generous whitespace.** Section padding is large; 48–96px vertical between page sections is typical.
- **No visible dividers.** No `<hr>` elements rendered on the PDP. Sections separate via whitespace + image/text alternation. **Don't add hairline rules** to the lookbook between sections — a 64px gap and a section-eyebrow label does the job.
- **Eyebrow labels** carry section identity instead of dividers: small uppercase Acumin Pro Condensed in `#666` or `#888`, ~11px, +2% letter-spacing. ("LOOK 01", "ABOUT THE PIECE", "STORES NEAR YOU".)
- **Mobile-first column collapse.** Two-column product layouts collapse to single-column under ~700px. Already in the `html-cart` skeleton.

## Voice / copy hints (not visual, but useful when generating labels)

- Sentence-case and Title Case both appear; UPPERCASE for labels/buttons/nav only.
- Product titles are descriptive and lowercase-friendly: "Slub Curved Hem Tee," "White Field Spec Boyfriend Crop Tee." Use the exact `product.name` from the MCP — don't embellish.
- Section eyebrows are short and direct: "ABOUT THE COLLECTION," "TEES MADE HERE," "STORES NEAR YOU." Two-to-four words, uppercase.
- Avoid AI-tropey phrases: "Discover…", "Step into…", "Embrace…", "Curated for you," "Your perfect…". They read as catalog-template; the real brand voice is plainer.

## What NOT to do

- ❌ Serif headlines (Georgia, Canela, Playfair, Söhne, etc.). Brand is condensed sans only.
- ❌ Off-white page backgrounds (`#FAF8F4`, `#F5F1EA`). White only. Off-white is a banner accent.
- ❌ Pill buttons (`border-radius: 999px` or even `8px`). Sharp corners only.
- ❌ Heavy section dividers, decorative rules, or borders around content blocks.
- ❌ Display-size headlines (40px+). Buck Mason's biggest h1 is 20px; let the photography fill the space.
- ❌ Square (1:1) or landscape (4:5, 16:9) product crops. 3:4 portrait.
- ❌ External font `<link>` tags or webfont CDN URLs in self-contained outputs (`html-cart` must work offline).
- ❌ Color accents from outside the product photography (no brand red/blue/green).
- ❌ "Curated for you" / "Discover your style" copy patterns. Plain noun-phrase eyebrows only.

## Re-verifying against the live site

When rendering a high-stakes artifact, the agent can re-extract these facts in ~5 seconds. The single-batch script (Chrome MCP):

```
1. Open a tab on https://www.buckmason.com/products/white-slub-curved-hem-tee
2. Run this JS:

const s = (el, props) => { if (!el) return null; const cs = getComputedStyle(el); const o = {}; props.forEach(p => o[p] = cs.getPropertyValue(p).trim()); return o; };
const out = {};
out.body = s(document.body, ['font-family','font-size','color','background-color']);
out.h1   = s(document.querySelector('h1'), ['font-family','font-weight','font-size','letter-spacing','text-transform']);
out.cta  = s(document.querySelector('button[class*=cta_btn]'), ['font-family','font-weight','font-size','letter-spacing','color','background-color','border-radius']);
const img = document.querySelector('img[src*="cdn.shopify"]');
out.imgRatio = img ? (img.naturalWidth / img.naturalHeight).toFixed(3) : null;
JSON.stringify(out, null, 2);
```

If any of these drift materially from the values in this doc (e.g., body font becomes "Söhne", aspect ratio becomes 0.8), update this file in the same commit + bump the lockstep version (CLAUDE.md § Versioning).

## Applying the brand style across formats

The rules above are written CSS-first because that's the easiest target, but they apply to **every rendered branded artifact** the skill produces — `html`, `html-cart`, `ppt`, and any future `pdf` output. Below is how each rule translates per builder.

### `ppt` (`python-pptx`)

| Brand rule | python-pptx mapping |
|---|---|
| Body font | `run.font.name = "Acumin Pro"` (fallback "Helvetica Neue") |
| Display / labels | `run.font.name = "Acumin Pro Condensed"` (fallback "Helvetica Neue Condensed") |
| Uppercase | Write the string already in uppercase — pptx has no `text-transform` |
| +2% letter-spacing | `run.font.spc` is the OOXML spelling; many readers ignore it. Skip if it doesn't survive a save-and-reload — the typeface choice carries 90% of the brand feel |
| 600/700 weight | `run.font.bold = True` |
| Slide background `#FFFFFF` | `slide.background.fill.solid()` → `fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)` |
| Text color `#333333` | `run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)` |
| Headline size ~20pt | `run.font.size = Pt(20)` for the slide title; **don't go to 36pt+ "presentation titles"** even though that's pptx's default — Buck Mason headlines stay small |
| Eyebrow ~11pt | `Pt(11)`, condensed, `RGBColor(0x66, 0x66, 0x66)` |
| 3:4 portrait hero | Place at `width=Inches(4.5), height=Inches(6.0)` (or any same-ratio pair). **Don't use 16:9 landscape for the hero** even though the slide itself is 16:9 — the photo stays portrait and lives on the left half |
| Sharp corners | `python-pptx`'s default `add_picture` has no rounded corners — leave defaults. Don't apply preset rounded shapes (`MSO_SHAPE.ROUNDED_RECTANGLE`) to image frames |
| No section dividers | Don't draw lines between content blocks; use blank space and a small uppercase eyebrow label instead |

Acumin Pro / Acumin Pro Condensed aren't bundled with Office or macOS; recipients without an Adobe Fonts subscription will see the system fallback. That's an acceptable degradation — the layout, color, and tone still read as Buck Mason. Don't try to embed the TTFs (license issue, file bloat). The fallback chain in the table above lands on Helvetica Neue, which is already on macOS and Office bundles.

### `pdf` (when it lands)

There's no `pdf` builder in the skill today; the cleanest implementation when it ships is to **render the existing `html` / `html-cart` template through `wkhtmltopdf` or headless Chromium** (`weasyprint`, Playwright `page.pdf()`). In that case the brand style flows through automatically — same CSS, same fonts, same crops. Don't reach for `reportlab` or `fpdf2` and re-implement; you'll fight the typography for a week and still come out worse than rasterizing the HTML.

If `OPENAI_API_KEY` is unset and the agent falls back to a flat-lay PDF (no try-on imagery), keep the brand rules: white bg, condensed sans labels, 3:4 product crops, no decorative borders.

### `html` and `html-cart`

The CSS skeleton in `references/output-formats.md` § 3 and § 4 already encodes the brand rules — fonts, color, type scale, button shape, image ratios. If you edit those skeletons, cross-check this doc.

### `images` (raw PNGs)

Skip — there's no assembly step, just the OpenAI output files. The image generation prompt itself follows different rules (see `references/image-generation.md`); brand-style.md doesn't apply.

## When to load this doc

- **Always**, before generating any `html-cart`, `html`, `ppt`, or `pdf` lookbook — anything visible and branded.
- **Skip** for non-rendered outputs: text-only chat replies, JSON handoff blocks, raw `images` lookbooks. The brand style is for assembled visible artifacts only.
