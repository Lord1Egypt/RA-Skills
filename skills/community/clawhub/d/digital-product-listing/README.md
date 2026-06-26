# Digital Product Listing Generator — OpenClaw Skill

**Generate optimised listings for Etsy, Gumroad, and Payhip from a single product description.**

Stop writing three different listings for every product you launch. Describe it once, get three platform-ready listings back instantly.

---

## What it does

Describe your digital product. Get back:

- **Etsy listing** — SEO title (140 chars), full description (400–500 words), exactly 13 tags, pricing suggestion
- **Gumroad listing** — product name, summary, full description (250–350 words), tags, pricing suggestion
- **Payhip listing** — title, short description, full description (300–400 words), categories, pricing suggestion
- **Cross-platform summary** — recommended primary platform, pricing range, bundle opportunity

All three in one response. Copy, paste, publish.

---

## Who it's for

- Etsy sellers selling printables, templates, clip art, or digital downloads
- Creators selling on Gumroad — notion templates, presets, guides, swipe files
- Anyone running a digital product side hustle across multiple platforms
- Designers and makers launching new products regularly

---

## Installation

```bash
npx clawhub@latest install tetsuakira-vk/digital-product-listing
```

---

## Usage

```
Use digital-product-listing to generate listings for: [describe your product]
```

Example:

```
Use digital-product-listing to generate listings for: A set of 10 A4 printable weekly planner pages in a minimal black and white style. PDF format, instant download, designed for productivity enthusiasts.
```

---

## Example output

**Input:** "Watercolour floral clipart bundle, 25 PNG files with transparent backgrounds, commercial licence included"

**Output:**
- Etsy title: "Watercolour Floral Clipart Bundle, 25 PNG Transparent Background, Commercial Use Digital Download"
- Etsy description: 450 words, structured with what's included, how to use, technical specs
- 13 Etsy tags covering style, use case, format, and audience
- Gumroad listing with direct creator tone, 280-word description
- Payhip listing with feature bullets and trust signals
- Cross-platform summary recommending Etsy as primary platform with bundle suggestion

---

## Platform comparison

| Platform | Best for | Tone used |
|---|---|---|
| Etsy | Search-driven discovery, broad audience | Warm, keyword-rich |
| Gumroad | Creator audiences, social traffic | Direct, conversational |
| Payhip | Direct links, no transaction fees | Clear, professional |

---

## Features

- Handles all digital product types: printables, templates, clip art, presets, ebooks, guides, bundles
- Platform-specific tone and structure for each listing
- Exactly 13 Etsy tags generated every time (the platform maximum)
- Pricing suggestions based on product type and platform norms
- Bundle opportunity suggestions included
- Works for single products or bundles

---

## Requirements

- OpenClaw installed and running
- Any supported LLM
- A description of your digital product (the more detail the better)

No API keys or external services required.

---

## Tips

- More detail in your product description = better output. Include format, dimensions, file count, licence type, and target buyer if you have them
- Use the cross-platform summary to decide where to focus your marketing
- Run it for every new product before launch — takes 30 seconds vs 30 minutes of manual writing
- If you only sell on one platform, just say "Etsy only" or "Gumroad only" to get a single listing

---

## Licence

MIT — free to use, modify, and build on.

---

## Feedback & issues

Open an issue on GitHub. Actively maintained.
