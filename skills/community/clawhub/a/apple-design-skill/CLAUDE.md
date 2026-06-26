# Apple Design Skill — CLAUDE.md

> **Self-contained skill file for Claude Code.** This file includes all design tokens, typography rules, copywriting patterns, image curation strategies, and layout templates needed to generate Apple-style frontend UI code. No external file references required.

---

## Identity & Purpose

You are an AI assistant enhanced with the **Apple Design Skill**. Generate frontend UI code that faithfully reproduces the design aesthetic of apple.com — generous whitespace, typographic precision, restrained color palettes, and relentless clarity.

**Language support:** English (en), Simplified Chinese (zh-CN), Traditional Chinese (zh-TW), Japanese (ja), Korean (ko). Detect the user's language and apply the corresponding font stack and copywriting rules automatically.

---

## Core Design Principles

1. **Simplicity over decoration.** Remove every element that does not serve a clear purpose.
2. **Whitespace is a feature.** 80–120px between sections gives content room to breathe.
3. **Typography-first hierarchy.** Large bold headlines (48–80px) anchor each section; subheadings and body step down in size and weight.
4. **Restrained color palette.** #FFFFFF, #F5F5F7, #1D1D1F for backgrounds. Accent blue (#0066CC) sparingly for interactive elements.
5. **Precision in detail.** Rounded corners (12–20px), multi-layer shadows, smooth transitions.
6. **Content-centered layout.** Constrain content to 980–1200px, centered. Full-bleed imagery may extend beyond.
7. **Responsive by default.** Three breakpoints: 734px, 1068px, 1440px.

---

## Design Tokens

All visual variables as CSS custom properties. Copy the `:root` blocks into your `<style>` tag. Never hard-code raw values.

### Colors

```css
:root {
  --apple-bg-white: #FFFFFF;
  --apple-bg-dark: #1D1D1F;
  --apple-bg-light-gray: #F5F5F7;
  --apple-bg-elevated: #FBFBFD;

  --apple-text-primary: #1D1D1F;
  --apple-text-secondary: #6E6E73;
  --apple-text-tertiary: #86868B;
  --apple-text-on-dark: #F5F5F7;
  --apple-text-white: #FFFFFF;

  --apple-link-blue: #0066CC;
  --apple-link-blue-hover: #0077ED;
  --apple-accent-green: #2D8C3C;
  --apple-accent-orange: #E85D04;
  --apple-accent-red: #E30000;
}
```

### Spacing

```css
:root {
  --apple-section-gap: 100px;
  --apple-section-gap-sm: 80px;
  --apple-section-gap-lg: 120px;

  --apple-component-gap-sm: 16px;
  --apple-component-gap-md: 32px;
  --apple-component-gap-lg: 48px;

  --apple-card-padding: 32px;
  --apple-card-padding-sm: 24px;
  --apple-card-padding-lg: 40px;

  --apple-content-max-width: 980px;
  --apple-content-max-width-lg: 1200px;
}
```

### Font Weights

```css
:root {
  --apple-weight-title: 600;
  --apple-weight-title-bold: 700;
  --apple-weight-body: 400;
  --apple-weight-body-medium: 500;
}
```

### Border Radius

```css
:root {
  --apple-radius-card: 18px;
  --apple-radius-card-sm: 12px;
  --apple-radius-card-lg: 20px;
  --apple-radius-button: 980px;
  --apple-radius-badge: 8px;
}
```

### Shadows

```css
:root {
  --apple-shadow-card: 0 2px 8px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.08);
  --apple-shadow-hover: 0 4px 12px rgba(0,0,0,0.06), 0 12px 32px rgba(0,0,0,0.12);
  --apple-shadow-sm: 0 1px 4px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.06);
  --apple-shadow-modal: 0 8px 20px rgba(0,0,0,0.08), 0 20px 60px rgba(0,0,0,0.16);
}
```

### Gradients

```css
:root {
  --apple-gradient-text-purple: linear-gradient(90deg, #7B2FBE, #E040A0);
  --apple-gradient-text-blue: linear-gradient(90deg, #2997FF, #5AC8FA);
  --apple-gradient-text-warm: linear-gradient(90deg, #E8590C, #D63384);
  --apple-gradient-text-green: linear-gradient(90deg, #30D158, #00C7BE);
  --apple-gradient-bg-light: linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%);
  --apple-gradient-bg-dark: linear-gradient(180deg, #1D1D1F 0%, #000000 100%);
}
```

Apply a text gradient:

```css
.gradient-headline {
  background: var(--apple-gradient-text-purple);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Letter Spacing

```css
:root {
  --apple-tracking-zh-title: 0.04em;
  --apple-tracking-en-title: -0.015em;
  --apple-tracking-en-title-tight: -0.02em;
  --apple-tracking-en-title-loose: 0.01em;
  --apple-tracking-body: 0em;
}
```

Rule: `zh-CN`, `zh-TW`, `ja` → use `--apple-tracking-zh-title` for headings. `en`, `ko` → use `--apple-tracking-en-title`.

### Line Height

```css
:root {
  --apple-leading-title: 1.1;
  --apple-leading-title-tight: 1.05;
  --apple-leading-title-loose: 1.15;
  --apple-leading-body: 1.53;
  --apple-leading-body-tight: 1.5;
  --apple-leading-body-loose: 1.58;
}
```

### Responsive Breakpoints

```css
:root {
  --apple-breakpoint-sm: 734px;
  --apple-breakpoint-md: 1068px;
  --apple-breakpoint-lg: 1440px;
}
```

```css
/* Mobile-first base (< 734px) */
@media (min-width: 734px)  { /* tablet */ }
@media (min-width: 1068px) { /* desktop */ }
@media (min-width: 1440px) { /* large desktop */ }
```

---

## Typography — Multi-Language Font Stacks

### Font Stack Data

```json
{
  "fontStacks": {
    "en": {
      "display": "'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
      "text": "'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
      "fallback_google": "'Inter', sans-serif"
    },
    "zh-CN": {
      "display": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
      "text": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
      "fallback_google": "'Noto Sans SC', sans-serif"
    },
    "zh-TW": {
      "display": "'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif",
      "text": "'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif",
      "fallback_google": "'Noto Sans TC', sans-serif"
    },
    "ja": {
      "display": "'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif",
      "text": "'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif",
      "fallback_google": "'Noto Sans JP', sans-serif"
    },
    "ko": {
      "display": "'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
      "text": "'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
      "fallback_google": "'Noto Sans KR', sans-serif"
    }
  }
}
```

### Language-Specific CSS

```css
:root[lang="en"], :root:lang(en) {
  --apple-font-display: 'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  --apple-font-text: 'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
}
:root[lang="zh-CN"], :root:lang(zh-CN) {
  --apple-font-display: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  --apple-font-text: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
}
:root[lang="zh-TW"], :root:lang(zh-TW) {
  --apple-font-display: 'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif;
  --apple-font-text: 'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif;
}
:root[lang="ja"], :root:lang(ja) {
  --apple-font-display: 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif;
  --apple-font-text: 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif;
}
:root[lang="ko"], :root:lang(ko) {
  --apple-font-display: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  --apple-font-text: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
}
```

### Google Fonts Fallback

Include only the tags needed for the detected language:

```html
<!-- English --> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- zh-CN -->  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- zh-TW -->  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- ja -->     <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- ko -->     <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Font Size Scale

```css
:root {
  --apple-font-size-hero: 56px;
  --apple-font-size-hero-min: 48px;
  --apple-font-size-hero-max: 80px;
  --apple-font-size-subtitle: 28px;
  --apple-font-size-subtitle-min: 24px;
  --apple-font-size-subtitle-max: 32px;
  --apple-font-size-body: 17px;
  --apple-font-size-body-max: 21px;
  --apple-font-size-caption: 12px;
  --apple-font-size-caption-max: 14px;
}
```

Responsive headline scaling:

```css
h1, .hero-headline {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-hero-min);
  font-weight: var(--apple-weight-title-bold);
  line-height: var(--apple-leading-title);
  letter-spacing: var(--apple-tracking-en-title);
}
@media (min-width: 734px)  { h1, .hero-headline { font-size: var(--apple-font-size-hero); } }
@media (min-width: 1068px) { h1, .hero-headline { font-size: var(--apple-font-size-hero-max); } }
```

### Language Detection Logic

1. Examine the user's prompt language → use that language's font stack.
2. Check for explicit `lang` attribute requests.
3. Character-based fallback: CJK Ideographs → zh-CN/zh-TW; Hiragana/Katakana → ja; Hangul → ko; else → en.
4. Default: `en`.

---

## Copywriting Rules

### Core Principles

1. **One idea per line.** Each headline communicates exactly one benefit.
2. **Short beats long.** Brevity signals confidence.
3. **Lead with the benefit, not the spec.** Transform technical parameters into felt experiences.
4. **Rhythm matters.** Fragments, pauses, parallel structures create intentional tempo.
5. **Surprise with simplicity.** The most memorable lines are disarmingly simple.

### Title Length Constraints

| Language | Title (H1) | Subtitle (H2) |
|----------|-----------|---------------|
| English  | ≤ 8 words | ≤ 20 words    |
| Chinese  | ≤ 12 chars | ≤ 30 chars   |

Punctuation excluded from count. Count before output; rewrite if over limit.

### English Patterns

| Pattern | Examples |
|---------|---------|
| Fragment sentences | "Chip. For dip." · "Pro. Beyond." · "Supercharged. By M2." |
| Single-word impact | "Whoa." · "Brilliant." · "Power." |
| Superlative | "The best Mac ever." · "Our thinnest design." |
| Rhyme / wordplay | "Light. Years ahead." · "Powerful. Portable. Pro." |
| Question / challenge | "Why Mac?" · "What's a computer?" |

### Chinese Patterns

| Pattern | Examples |
|---------|---------|
| 对仗 (parallel) | "强得很，轻得很" · "有颜值，有实力" |
| 四字格 (4-char idiom) | "放心比好了" · "岂止于大" · "超凡出众" |
| 反问 (rhetorical) | "还有谁？" · "谁说轻薄不能强大？" |
| 押韵 (rhyming) | "大的好，好的大" · "一身轻，万事行" |

### Spec-to-Experience Conversion

Never lead with raw specs. Convert to felt outcomes:

| Spec | Apple-style |
|------|------------|
| 18-hour battery life | "All day. And then some." |
| 48MP main camera | "Every detail. Captured beautifully." |
| M3 chip with 8-core GPU | "Blazingly fast graphics." |
| 256GB SSD | "Room for everything you love." |

Rules: Never lead with a number. Avoid jargon. Use sensory language. One spec per sentence.

### Copywriting Rules Data

```json
{
  "copywritingRules": {
    "titleRules": { "en": { "maxWords": 8 }, "zh": { "maxChars": 12 } },
    "subtitleRules": { "en": { "maxWords": 20 }, "zh": { "maxChars": 30 } },
    "patterns": {
      "en": [
        { "name": "fragment-sentences", "examples": ["Chip. For dip.", "Pro. Beyond."] },
        { "name": "single-word-impact", "examples": ["Whoa.", "Brilliant."] },
        { "name": "superlative-comparative", "examples": ["The best Mac ever."] },
        { "name": "rhyme-wordplay", "examples": ["Light. Years ahead."] },
        { "name": "question-challenge", "examples": ["Why Mac?"] }
      ],
      "zh": [
        { "name": "parallel-structure", "examples": ["强得很，轻得很", "有颜值，有实力"] },
        { "name": "four-character-idiom", "examples": ["放心比好了", "岂止于大"] },
        { "name": "rhetorical-question", "examples": ["还有谁？", "何止于快？"] },
        { "name": "rhyming", "examples": ["大的好，好的大"] }
      ]
    }
  }
}
```

---

## Image Curation

### Apple-Style Image Characteristics

Every image must pass these tests:
1. **Clean background** — solid color, subtle gradient, or heavily blurred. No clutter.
2. **High contrast** — subject "pops" without borders.
3. **Centered subject** — primary subject at or near center.
4. **Natural lighting** — soft, diffused. No harsh shadows or flash artifacts.
5. **Minimal color palette** — 3–4 hues max, muted/desaturated preferred.

Avoid: busy backgrounds, heavy filters, stock-photo clichés, low resolution, watermarks, embedded text.

### Image Specs by Section

| Section | Aspect Ratio | Min Width | Background | Style |
|---------|-------------|-----------|------------|-------|
| Hero | 16:9 / 21:9 | 1920px | Dark | Cinematic, high-impact |
| Product | 1:1 / 4:3 | 800px | Solid / gradient | Clean, centered, studio |
| Feature | 16:9 / 4:3 | 1200px | Contextual | Lifestyle, natural light |

### CSS Gradient Fallbacks

When images are unavailable, use these CSS gradients:

```css
.hero-fallback {
  background: linear-gradient(180deg, #1D1D1F 0%, #000000 100%);
  color: #FFFFFF;
}
.section-fallback-light {
  background: linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%);
  color: var(--apple-text-primary, #1D1D1F);
}
.product-fallback {
  background: radial-gradient(ellipse at center, #F5F5F7 0%, #E8E8ED 100%);
}
.accent-fallback-purple {
  background: linear-gradient(135deg, #7B2FBE 0%, #E040A0 100%);
  color: #FFFFFF;
}
.accent-fallback-blue {
  background: linear-gradient(135deg, #2997FF 0%, #5AC8FA 100%);
  color: #FFFFFF;
}
.mesh-fallback {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(123,47,190,0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(41,151,255,0.15) 0%, transparent 50%),
    linear-gradient(180deg, #FBFBFD 0%, #F5F5F7 100%);
}
```

### Alt Text Rules

- Describe the scene, not the filename.
- Include product name when visible.
- Keep under 125 characters.
- Use `alt=""` for purely decorative images.
- Match the page language.

### Image Specs Data

```json
{
  "imageSpecs": {
    "hero": {
      "aspectRatio": ["16:9", "21:9"],
      "minWidth": 1920,
      "background": "dark",
      "style": "cinematic, high-impact"
    },
    "product": {
      "aspectRatio": ["1:1", "4:3"],
      "minWidth": 800,
      "background": "solid or gradient",
      "style": "product centered, studio lighting"
    },
    "feature": {
      "aspectRatio": ["16:9", "4:3"],
      "minWidth": 1200,
      "background": "contextual",
      "style": "lifestyle, natural light"
    }
  },
  "sources": ["unsplash.com", "pexels.com"],
  "fallback": "CSS gradient backgrounds",
  "altText": { "maxLength": 125 }
}
```

> **Note:** Image search API calls (Unsplash/Pexels) are an optional extension not included in this Skill. Use keyword suggestions and CSS fallbacks when API is unavailable.

---

## Layout Patterns

### Content Area Width

```css
.apple-content {
  width: 100%;
  max-width: var(--apple-content-max-width);
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
  box-sizing: border-box;
}
@media (min-width: 1440px) {
  .apple-content { max-width: var(--apple-content-max-width-lg); }
}
@media (max-width: 733px) {
  .apple-content { padding-left: 20px; padding-right: 20px; }
}
```

### Vertical Spacing

```css
.apple-section { padding-top: var(--apple-section-gap); padding-bottom: var(--apple-section-gap); }
.apple-section--compact { padding-top: var(--apple-section-gap-sm); padding-bottom: var(--apple-section-gap-sm); }
.apple-section--spacious { padding-top: var(--apple-section-gap-lg); padding-bottom: var(--apple-section-gap-lg); }

.apple-stack-sm { display: flex; flex-direction: column; gap: var(--apple-component-gap-sm); }
.apple-stack-md { display: flex; flex-direction: column; gap: var(--apple-component-gap-md); }
.apple-stack-lg { display: flex; flex-direction: column; gap: var(--apple-component-gap-lg); }
```


### Hero Section Template

```html
<section class="hero">
  <div class="apple-content hero__content">
    <h1 class="hero__headline">iPhone 16 Pro.</h1>
    <p class="hero__subtitle">Hello, Apple Intelligence.</p>
    <div class="hero__cta">
      <a href="#learn-more" class="hero__link hero__link--primary">Learn more ›</a>
      <a href="#buy" class="hero__link hero__link--secondary">Buy ›</a>
    </div>
  </div>
</section>
```

```css
.hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--apple-gradient-bg-dark);
  color: var(--apple-text-white);
  text-align: center;
  overflow: hidden;
}
.hero__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--apple-component-gap-sm);
  padding-top: var(--apple-section-gap);
  padding-bottom: var(--apple-section-gap);
}
.hero__headline {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-hero-min);
  font-weight: var(--apple-weight-title-bold);
  line-height: var(--apple-leading-title);
  letter-spacing: var(--apple-tracking-en-title);
  margin: 0;
}
.hero__subtitle {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-subtitle);
  font-weight: var(--apple-weight-body);
  line-height: var(--apple-leading-body);
  color: var(--apple-text-tertiary);
  margin: 0;
}
.hero__cta {
  display: flex;
  gap: var(--apple-component-gap-md);
  margin-top: var(--apple-component-gap-sm);
}
.hero__link {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body);
  text-decoration: none;
}
.hero__link--primary { color: var(--apple-link-blue); }
.hero__link--primary:hover { color: var(--apple-link-blue-hover); text-decoration: underline; }
.hero__link--secondary { color: var(--apple-link-blue); }

/* Light variant */
.hero--light { background: var(--apple-bg-white); color: var(--apple-text-primary); }
.hero--light .hero__subtitle { color: var(--apple-text-secondary); }

/* Gradient headline */
.hero__headline--gradient {
  background: var(--apple-gradient-text-purple);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Responsive */
@media (min-width: 734px)  { .hero__headline { font-size: var(--apple-font-size-hero); } }
@media (min-width: 1068px) { .hero__headline { font-size: var(--apple-font-size-hero-max); } }
```

### Product Grid Template

```html
<section class="apple-section product-grid-section">
  <div class="apple-content">
    <h2 class="product-grid__heading">Explore the lineup.</h2>
    <div class="product-grid">
      <article class="product-card">
        <div class="product-card__image">
          <img src="product-1.jpg" alt="MacBook Air — thin and light laptop" loading="lazy">
        </div>
        <h3 class="product-card__name">MacBook Air</h3>
        <p class="product-card__tagline">Strikingly thin. Impressively big.</p>
        <a href="#" class="product-card__link">Learn more ›</a>
      </article>
      <!-- Repeat cards as needed -->
    </div>
  </div>
</section>
```

```css
.product-grid-section { background: var(--apple-bg-light-gray); }

.product-grid__heading {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-subtitle-max);
  font-weight: var(--apple-weight-title);
  line-height: var(--apple-leading-title);
  letter-spacing: var(--apple-tracking-en-title);
  text-align: center;
  color: var(--apple-text-primary);
  margin: 0 0 var(--apple-component-gap-lg) 0;
}

.product-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--apple-component-gap-md);
}
@media (min-width: 734px)  { .product-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1068px) { .product-grid { grid-template-columns: repeat(3, 1fr); } }

.product-card {
  background: var(--apple-bg-white);
  border-radius: var(--apple-radius-card);
  padding: var(--apple-card-padding);
  box-shadow: var(--apple-shadow-card);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--apple-component-gap-sm);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}
.product-card:hover {
  box-shadow: var(--apple-shadow-hover);
  transform: translateY(-4px);
}
.product-card__image {
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  border-radius: var(--apple-radius-card-sm);
}
.product-card__image img { width: 100%; height: 100%; object-fit: cover; }
.product-card__name {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-subtitle-min);
  font-weight: var(--apple-weight-title);
  line-height: var(--apple-leading-title);
  color: var(--apple-text-primary);
  margin: 0;
}
.product-card__tagline {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body);
  font-weight: var(--apple-weight-body);
  line-height: var(--apple-leading-body);
  color: var(--apple-text-secondary);
  margin: 0;
}
.product-card__link {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body);
  color: var(--apple-link-blue);
  text-decoration: none;
}
.product-card__link:hover { color: var(--apple-link-blue-hover); text-decoration: underline; }
```

### Composing a Full Page

Stack sections vertically and alternate backgrounds:

| Order | Section | Background |
|-------|---------|------------|
| 1 | Hero | Dark gradient or `--apple-bg-dark` |
| 2 | Product Grid | `--apple-bg-light-gray` |
| 3 | Feature Content | `--apple-bg-white` |
| 4 | Feature Cards | `--apple-bg-light-gray` |
| 5 | Dark Section | `--apple-bg-dark` |

---

## Output Rules

- Always use CSS custom properties (`var(--apple-*)`) — never hard-code raw values.
- Prefer semantic class names (`.hero`, `.product-card`) over utility-only markup.
- Include Google Fonts `<link>` tags when Apple system fonts may be unavailable.
- All `<img>` elements must have descriptive `alt` text.
- Produce valid, accessible HTML (proper heading hierarchy, ARIA labels where needed).
- Set `<html lang="detected-language">` based on user's language.

---

## Responsibility Boundaries

| Capability | Provider |
|------------|----------|
| Design tokens, typography, copywriting, layout, image rules | **This Skill** (self-contained) |
| Image search API calls (Unsplash/Pexels) | **Optional extension** (not included) |
| Skill installation & distribution | **OpenClaw Platform** |
| Version management | **OpenClaw Platform** |

This Skill is a pure instruction set — it does not make network requests, call APIs, or execute code.
