# Image Curation Strategy

This module defines the criteria for selecting, recommending, and falling back on imagery in Apple-style pages. Apple's visual language extends beyond typography and color — every photograph, gradient, and placeholder reinforces the same ethos of clarity, restraint, and premium quality.

> **Usage:** When generating a page section that requires imagery, consult this module to determine the correct aspect ratio, resolution, style, and fallback strategy. If the host environment supports image search APIs (Unsplash, Pexels), use the keyword suggestions below. If not, apply the CSS gradient fallback templates.

> **Responsibility boundary:** Image selection criteria and CSS fallback strategies are implemented by this Skill. Actual image search API calls (Unsplash / Pexels) are an **optional extension** that depends on external API access and is **not included** in the core Skill. See Section 7 for details.

---

## 1. Apple-Style Image Characteristics

Every image used in an Apple-style page must pass these five visual tests. Reject any image that fails even one.

### 1.1 Visual Checklist

| # | Characteristic | Description | Why it matters |
|---|---------------|-------------|----------------|
| 1 | **Clean background** | Solid color, subtle gradient, or heavily blurred environment. No visual clutter, no busy patterns. | Keeps the viewer's focus on the subject. Apple pages never compete with their own imagery. |
| 2 | **High contrast** | Strong tonal separation between subject and background. The product or scene should "pop" without needing a border or outline. | Creates visual punch and ensures legibility when text is overlaid. |
| 3 | **Centered subject** | The primary subject sits at or near the center of the frame. Asymmetric compositions are acceptable only when intentional negative space balances the layout. | Aligns with Apple's centered, symmetrical page layouts. |
| 4 | **Natural lighting** | Soft, diffused light — studio softbox or golden-hour natural light. No harsh shadows, no visible flash artifacts, no neon color casts. | Conveys premium quality. Harsh lighting feels cheap; natural light feels aspirational. |
| 5 | **Minimal color palette** | The image's dominant colors should not exceed 3–4 hues. Muted, desaturated tones are preferred over vivid, saturated ones. | Harmonizes with Apple's restrained color tokens (#FFFFFF, #F5F5F7, #1D1D1F). |

### 1.2 Anti-Patterns — Images to Avoid

- ❌ Busy backgrounds with multiple competing elements
- ❌ Heavy filters, vignettes, or artificial color grading
- ❌ Stock-photo clichés (handshake, thumbs-up, exaggerated smiles)
- ❌ Low resolution or visibly compressed images
- ❌ Watermarked or rights-restricted images
- ❌ Images with embedded text or logos

---

## 2. Image Specifications by Section Type

Each page section has distinct image requirements. Use the table below to select the correct format.

### 2.1 Hero Section

The hero is the first thing visitors see. It must be cinematic, high-resolution, and emotionally compelling.

| Property | Value |
|----------|-------|
| Aspect ratio | **16:9** or **21:9** (ultra-wide) |
| Minimum width | **1920px** |
| Minimum height | 1080px (16:9) or 823px (21:9) |
| Background | Dark preferred (`#1D1D1F` or `#000000`) for maximum text contrast |
| Subject placement | Center or slight bottom-center to leave room for headline overlay |
| File format | WebP preferred, JPEG fallback, PNG for transparency |
| Loading | Eager (`loading="eager"`) — hero images must not lazy-load |

**Example use:** Full-bleed product shot on dark background with a large white headline overlaid.

### 2.2 Product Showcase

Product images need clinical precision — the product is the star, and nothing else should distract.

| Property | Value |
|----------|-------|
| Aspect ratio | **1:1** (square) or **4:3** |
| Background | Solid color or subtle gradient (use tokens from `design-tokens.md`) |
| Subject | Product centered, occupying 60–80% of the frame |
| Lighting | Even studio lighting, no dramatic shadows |
| File format | PNG (for transparent backgrounds) or WebP |
| Loading | Lazy (`loading="lazy"`) |

**Background recommendations:**
- White product → use `--apple-bg-light-gray` (#F5F5F7) background
- Dark product → use `--apple-bg-white` (#FFFFFF) background
- Colorful product → use `--apple-bg-dark` (#1D1D1F) background

### 2.3 Feature / Lifestyle Section

Feature images show the product in context — real people, real environments, real use cases.

| Property | Value |
|----------|-------|
| Aspect ratio | **16:9** or **4:3** |
| Style | Lifestyle / scene — product in use, environmental context |
| Lighting | Natural light, golden hour, or soft indoor ambient |
| Color tone | Warm and inviting, slightly desaturated |
| Subject | Person using the product, or a scene that implies the product's benefit |
| File format | WebP preferred, JPEG fallback |
| Loading | Lazy (`loading="lazy"`) |

**Example use:** A person working on a MacBook in a sunlit café, or AirPods on a desk next to a coffee cup.

### 2.4 Summary Table

| Section | Aspect Ratio | Min Width | Background | Style |
|---------|-------------|-----------|------------|-------|
| Hero | 16:9 / 21:9 | 1920px | Dark | Cinematic, high-impact |
| Product | 1:1 / 4:3 | 800px | Solid / gradient | Clean, centered, studio |
| Feature | 16:9 / 4:3 | 1200px | Contextual | Lifestyle, natural light |

---

## 3. Search Keyword Suggestions

When an image search API is available, use these keyword templates to find Apple-style imagery. Combine a **context keyword** with one or more **style modifiers** to narrow results.

### 3.1 Context Keywords by Section

| Section Type | Primary Keywords | Secondary Keywords |
|-------------|-----------------|-------------------|
| Hero (tech) | `technology`, `minimal workspace`, `dark background product` | `premium`, `modern`, `sleek` |
| Hero (lifestyle) | `creative workspace`, `modern lifestyle`, `minimal interior` | `bright`, `clean`, `aspirational` |
| Product (device) | `laptop minimal`, `smartphone white background`, `headphones studio` | `isolated`, `centered`, `product photography` |
| Product (accessory) | `tech accessory minimal`, `gadget white background` | `clean`, `simple`, `studio lighting` |
| Feature (work) | `person working laptop`, `creative professional`, `modern office` | `natural light`, `focused`, `candid` |
| Feature (lifestyle) | `coffee shop laptop`, `outdoor technology`, `music headphones` | `warm`, `golden hour`, `relaxed` |

### 3.2 Style Modifiers

Always append at least one style modifier to improve result quality:

| Modifier | Effect | Example query |
|----------|--------|---------------|
| `minimal` | Reduces background clutter | `laptop minimal dark background` |
| `white background` | Forces clean product shots | `smartphone white background studio` |
| `studio lighting` | Ensures even, professional light | `headphones studio lighting minimal` |
| `aerial view` | Top-down perspective for flat-lay layouts | `desk setup aerial view minimal` |
| `bokeh` | Blurred background for depth | `person laptop bokeh natural light` |
| `monochrome` | Black-and-white for dramatic hero sections | `technology monochrome minimal` |

### 3.3 Query Construction Formula

```
[context keyword] + [style modifier] + [optional: color/mood]
```

**Examples:**
- Hero: `"minimal workspace dark background premium"`
- Product: `"smartphone white background studio lighting"`
- Feature: `"creative professional laptop natural light bokeh"`

---

## 4. CSS Gradient Fallback Templates

When images are unavailable — no API access, no suitable results, or offline generation — use these CSS gradient backgrounds as high-quality substitutes. Each template is designed to evoke the same visual mood as a photograph.

### 4.1 Dark Hero Fallback

```css
.hero-fallback {
  background: linear-gradient(180deg, #1D1D1F 0%, #000000 100%);
  color: #FFFFFF;
}
```

### 4.2 Light Section Fallback

```css
.section-fallback-light {
  background: linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%);
  color: var(--apple-text-primary, #1D1D1F);
}
```

### 4.3 Product Spotlight Fallback (Radial)

```css
.product-fallback {
  background: radial-gradient(ellipse at center, #F5F5F7 0%, #E8E8ED 100%);
}
```

### 4.4 Accent Gradient Fallback (Purple-Pink)

```css
.accent-fallback-purple {
  background: linear-gradient(135deg, #7B2FBE 0%, #E040A0 100%);
  color: #FFFFFF;
}
```

### 4.5 Accent Gradient Fallback (Blue-Cyan)

```css
.accent-fallback-blue {
  background: linear-gradient(135deg, #2997FF 0%, #5AC8FA 100%);
  color: #FFFFFF;
}
```

### 4.6 Mesh Gradient Fallback (Premium Feel)

```css
.mesh-fallback {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(123, 47, 190, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(41, 151, 255, 0.15) 0%, transparent 50%),
    linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%);
}
```

### 4.7 Fallback Selection Guide

| Section | Recommended Fallback | CSS Class |
|---------|---------------------|-----------|
| Hero (dark) | Dark linear gradient | `.hero-fallback` |
| Hero (light) | Light linear gradient | `.section-fallback-light` |
| Product showcase | Radial spotlight | `.product-fallback` |
| Feature highlight | Accent gradient (match brand color) | `.accent-fallback-purple` or `.accent-fallback-blue` |
| Generic section | Light gradient or mesh | `.section-fallback-light` or `.mesh-fallback` |

---

## 5. Alt Text Writing Guidelines

Every `<img>` element must have a meaningful `alt` attribute. Apple-style alt text is concise, descriptive, and benefit-oriented — it describes what the viewer *sees and understands*, not just what the object is.

### 5.1 Rules

1. **Describe the scene, not the filename.** ❌ `alt="hero-image.jpg"` → ✅ `alt="MacBook Pro on a dark surface, screen glowing with a colorful gradient"`
2. **Include the product name** when the image shows a specific product.
3. **Mention the context** if the image is a lifestyle shot (e.g., "in a sunlit café", "on a wooden desk").
4. **Keep it under 125 characters.** Screen readers truncate longer alt text on some platforms.
5. **Skip decorative images.** If an image is purely decorative (e.g., a gradient background rendered as an image), use `alt=""` (empty alt) so screen readers skip it.
6. **Use the language of the page.** If the page is in Chinese, write alt text in Chinese.

### 5.2 Alt Text Templates

| Image Type | Template | Example |
|-----------|----------|---------|
| Product hero | `[Product name] [key visual detail] on [background description]` | `"MacBook Air in Midnight finish on a dark gradient background"` |
| Product detail | `Close-up of [product] showing [feature]` | `"Close-up of iPhone 15 Pro showing the titanium edge"` |
| Lifestyle | `[Person/scene] [action] with [product] [environment]` | `"Designer working on iPad Pro with Apple Pencil in a bright studio"` |
| Abstract / decorative | `""` (empty) | `alt=""` |

### 5.3 Chinese Alt Text Examples

| Image Type | Example |
|-----------|---------|
| Product hero | `"午夜色 MacBook Air 置于深色渐变背景上"` |
| Lifestyle | `"设计师在明亮工作室中使用 iPad Pro 和 Apple Pencil 进行创作"` |

---

## 6. Image Specifications Data Structure

The following JSON block encodes the image specifications for programmatic access and testability.

```json
{
  "imageSpecs": {
    "hero": {
      "aspectRatio": ["16:9", "21:9"],
      "minWidth": 1920,
      "minHeight": { "16:9": 1080, "21:9": 823 },
      "background": "dark",
      "style": "cinematic, high-impact, clean background, high contrast, centered subject, natural lighting",
      "loading": "eager",
      "formats": ["webp", "jpeg"]
    },
    "product": {
      "aspectRatio": ["1:1", "4:3"],
      "minWidth": 800,
      "background": "solid or gradient",
      "style": "product centered, studio lighting, clean background, 60-80% frame fill",
      "loading": "lazy",
      "formats": ["png", "webp"]
    },
    "feature": {
      "aspectRatio": ["16:9", "4:3"],
      "minWidth": 1200,
      "background": "contextual",
      "style": "lifestyle, natural light, warm tones, slightly desaturated",
      "loading": "lazy",
      "formats": ["webp", "jpeg"]
    }
  },
  "imageCharacteristics": {
    "required": [
      "clean background",
      "high contrast",
      "centered subject",
      "natural lighting",
      "minimal color palette (3-4 hues)"
    ],
    "avoid": [
      "busy backgrounds",
      "heavy filters or vignettes",
      "stock-photo clichés",
      "low resolution",
      "watermarked images",
      "embedded text or logos"
    ]
  },
  "sources": {
    "primary": ["unsplash.com", "pexels.com"],
    "note": "Image search API calls are an optional extension — not included in core Skill"
  },
  "fallback": {
    "strategy": "CSS gradient backgrounds",
    "templates": [
      {
        "name": "hero-dark",
        "css": "linear-gradient(180deg, #1D1D1F 0%, #000000 100%)"
      },
      {
        "name": "section-light",
        "css": "linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%)"
      },
      {
        "name": "product-spotlight",
        "css": "radial-gradient(ellipse at center, #F5F5F7 0%, #E8E8ED 100%)"
      },
      {
        "name": "accent-purple",
        "css": "linear-gradient(135deg, #7B2FBE 0%, #E040A0 100%)"
      },
      {
        "name": "accent-blue",
        "css": "linear-gradient(135deg, #2997FF 0%, #5AC8FA 100%)"
      }
    ]
  },
  "altText": {
    "maxLength": 125,
    "rules": [
      "Describe the scene, not the filename",
      "Include product name when visible",
      "Mention context for lifestyle shots",
      "Keep under 125 characters",
      "Use empty alt for decorative images",
      "Match the page language"
    ]
  }
}
```

---

## 7. Optional Extension: Image Search API Integration

> ⚠️ **This section describes an optional extension.** The image search API capability is **not part of the core Skill**. It requires external API access (Unsplash API, Pexels API) that may or may not be available in the host environment.

### 7.1 Capability Boundary

| Capability | Provided by | Status |
|-----------|-------------|--------|
| Image style criteria & visual checklist | **Skill** (this module) | ✅ Core — always available |
| Search keyword suggestions | **Skill** (this module) | ✅ Core — always available |
| CSS gradient fallback templates | **Skill** (this module) | ✅ Core — always available |
| Alt text writing guidelines | **Skill** (this module) | ✅ Core — always available |
| Unsplash / Pexels API calls | **Third-party / Optional extension** | ⚡ Optional — requires API key |
| Image download and optimization | **Third-party / Optional extension** | ⚡ Optional — requires API access |

### 7.2 When API Is Available

If the host environment provides image search API access:

1. Construct a search query using the keyword templates from Section 3.
2. Filter results by the aspect ratio and minimum resolution from Section 2.
3. Apply the visual checklist from Section 1 to rank results.
4. Return the top result with its direct URL and a generated alt text following Section 5.

### 7.3 When API Is Not Available — Use Curated Unsplash Direct Links

**IMPORTANT: CSS gradients alone are NOT acceptable as the primary image strategy.** Apple-style pages MUST include real photographs. When no image search API is available, use the curated Unsplash direct-link library below. These are free-to-use images via Unsplash's hotlink-friendly CDN.

#### Curated Image Library — Unsplash Direct Links

Use these URLs directly in `<img src="...">` tags. All images are high-resolution, Apple-aesthetic-compatible, and free to use.

**Hero / Dark Background / Tech:**
- `https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1920&q=80` — MacBook on dark desk, minimal
- `https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1920&q=80` — Laptop on clean workspace
- `https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1920&q=80` — Tech abstract, blue glow on dark
- `https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1920&q=80` — Retro-modern tech, neon accents
- `https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80` — Circuit board macro, tech abstract

**Product / Clean Background:**
- `https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200&q=80` — Headphones on yellow, product shot
- `https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1200&q=80` — Watch on white, minimal product
- `https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=1200&q=80` — Camera on white, clean product
- `https://images.unsplash.com/photo-1491933382434-500287f9b54b?w=1200&q=80` — iPhone on white background
- `https://images.unsplash.com/photo-1583394838336-acd977736f90?w=1200&q=80` — Headphones, studio lighting

**Lifestyle / People / Workspace:**
- `https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=80` — Team collaboration, natural light
- `https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920&q=80` — Developer at laptop, coding
- `https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1920&q=80` — Modern office, bright workspace
- `https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1920&q=80` — Business meeting, professional
- `https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1920&q=80` — Person typing on MacBook

**Abstract / Gradient / Artistic:**
- `https://images.unsplash.com/photo-1557683316-973673baf926?w=1920&q=80` — Gradient abstract, blue-purple
- `https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=80` — Colorful gradient, smooth
- `https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920&q=80` — Purple gradient, deep
- `https://images.unsplash.com/photo-1557682224-5b8590cd9ec5?w=1920&q=80` — Green-blue gradient
- `https://images.unsplash.com/photo-1557682260-96773eb01377?w=1920&q=80` — Pink-orange gradient

**Nature / Calm / Premium Feel:**
- `https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920&q=80` — Misty forest, serene
- `https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1920&q=80` — Mountain landscape, clean
- `https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80` — Beach, turquoise water
- `https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&q=80` — Starry mountain, dramatic
- `https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80` — Mountain peak, epic

#### Image Selection Rules

1. **ALWAYS include at least one real image per page.** A page with zero photographs does not feel like Apple.
2. **Hero sections MUST have a real image** — either as a background (`background-image`) or as a prominent visual element. CSS gradients may overlay the image but not replace it.
3. **Match the image category to the page content.** Tech product → use tech/product images. SaaS/business → use workspace/people images. Creative → use abstract/artistic images.
4. **Append `&w=1920&q=80` to Unsplash URLs** for hero images, `&w=1200&q=80` for product/feature images.
5. CSS gradient fallbacks from Section 4 should be used as **overlays on top of images** (using `background: linear-gradient(...), url(...)`) or as **secondary section backgrounds** — never as the sole visual for a hero section.

---

## Quick Reference

| Property | Hero | Product | Feature |
|----------|------|---------|---------|
| Aspect ratio | 16:9 / 21:9 | 1:1 / 4:3 | 16:9 / 4:3 |
| Min width | 1920px | 800px | 1200px |
| Background | Dark | Solid / gradient | Contextual |
| Style | Cinematic | Studio, centered | Lifestyle, natural light |
| Loading | Eager | Lazy | Lazy |
| Fallback | `.hero-fallback` | `.product-fallback` | `.section-fallback-light` |
