# Layout Patterns

This module defines reusable page-section templates that reproduce the layout patterns found on apple.com. Each template is a complete, copy-pasteable HTML + CSS block. All visual values reference tokens from `design-tokens.md`; all typographic values reference stacks and scales from `typography.md`.

> **Usage:** Choose the template that matches the section you need, paste it into your output, and replace the placeholder content. Combine multiple templates vertically to compose a full page. Always keep the token-based `var(--apple-*)` references — never hard-code raw values.

---

## 1. Content Area Width Constraints

Every section's text content must be horizontally constrained to maintain readability and match Apple's centered-content approach. Full-bleed backgrounds may extend to the viewport edge, but text and interactive elements stay within bounds.

```css
/* Base content wrapper — use inside every section */
.apple-content {
  width: 100%;
  max-width: var(--apple-content-max-width);        /* 980px from design-tokens.md */
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
  box-sizing: border-box;
}

/* Wider variant for large displays */
@media (min-width: 1440px) {
  .apple-content {
    max-width: var(--apple-content-max-width-lg);    /* 1200px from design-tokens.md */
  }
}

/* Mobile padding adjustment */
@media (max-width: 733px) {
  .apple-content {
    padding-left: 20px;
    padding-right: 20px;
  }
}
```

**Rules:**
- Default max-width: `var(--apple-content-max-width)` (980px).
- On viewports ≥ 1440px, widen to `var(--apple-content-max-width-lg)` (1200px).
- Always center with `margin: 0 auto`.
- Horizontal padding provides breathing room on smaller screens.

---

## 2. Vertical Spacing Rules

Consistent vertical rhythm is critical to the Apple aesthetic. Use section-level gaps between top-level `<section>` elements and component-level gaps within sections.

```css
/* Section-to-section spacing */
.apple-section {
  padding-top: var(--apple-section-gap);             /* 100px default from design-tokens.md */
  padding-bottom: var(--apple-section-gap);
}

/* Tighter section spacing for related blocks */
.apple-section--compact {
  padding-top: var(--apple-section-gap-sm);          /* 80px from design-tokens.md */
  padding-bottom: var(--apple-section-gap-sm);
}

/* Generous section spacing for dramatic pauses */
.apple-section--spacious {
  padding-top: var(--apple-section-gap-lg);          /* 120px from design-tokens.md */
  padding-bottom: var(--apple-section-gap-lg);
}

/* Component-level vertical gaps within a section */
.apple-stack-sm { display: flex; flex-direction: column; gap: var(--apple-component-gap-sm); }  /* 16px */
.apple-stack-md { display: flex; flex-direction: column; gap: var(--apple-component-gap-md); }  /* 32px */
.apple-stack-lg { display: flex; flex-direction: column; gap: var(--apple-component-gap-lg); }  /* 48px */
```

**Rules:**
- Between top-level sections: 80–120px (`--apple-section-gap-sm` to `--apple-section-gap-lg`).
- Between heading and subtitle: `--apple-component-gap-sm` (16px).
- Between subtitle and body/CTA: `--apple-component-gap-md` (32px).
- Between major sub-blocks within a section: `--apple-component-gap-lg` (48px).

### Responsive spacing

```css
@media (max-width: 733px) {
  .apple-section {
    padding-top: 60px;
    padding-bottom: 60px;
  }
  .apple-section--compact {
    padding-top: 48px;
    padding-bottom: 48px;
  }
}

@media (min-width: 734px) and (max-width: 1067px) {
  .apple-section {
    padding-top: var(--apple-section-gap-sm);        /* 80px */
    padding-bottom: var(--apple-section-gap-sm);
  }
}
```

---

## 3. Full-Screen Hero Section

The Hero is the first thing visitors see. Apple's hero sections feature a full-viewport dark or light background, a single oversized headline, a concise subtitle, and an optional CTA link. The image or gradient fills the entire viewport width while text stays centered within the content area.

### Template

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
/* Hero section — full-screen dark variant */
.hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--apple-gradient-bg-dark);         /* gradient from design-tokens.md */
  color: var(--apple-text-white);
  text-align: center;
  overflow: hidden;
}

.hero__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--apple-component-gap-sm);                /* 16px */
  padding-top: var(--apple-section-gap);
  padding-bottom: var(--apple-section-gap);
}

.hero__headline {
  font-family: var(--apple-font-display);            /* from typography.md */
  font-size: var(--apple-font-size-hero-min);        /* 48px mobile */
  font-weight: var(--apple-weight-title-bold);       /* 700 from design-tokens.md */
  line-height: var(--apple-leading-title);           /* 1.1 from design-tokens.md */
  letter-spacing: var(--apple-tracking-en-title);    /* -0.015em from design-tokens.md */
  margin: 0;
}

.hero__subtitle {
  font-family: var(--apple-font-text);               /* from typography.md */
  font-size: var(--apple-font-size-subtitle);        /* 28px from typography.md */
  font-weight: var(--apple-weight-body);             /* 400 from design-tokens.md */
  line-height: var(--apple-leading-body);            /* 1.53 from design-tokens.md */
  color: var(--apple-text-tertiary);
  margin: 0;
}

.hero__cta {
  display: flex;
  gap: var(--apple-component-gap-md);                /* 32px */
  margin-top: var(--apple-component-gap-sm);         /* 16px */
}

.hero__link {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body);            /* 17px from typography.md */
  text-decoration: none;
}

.hero__link--primary {
  color: var(--apple-link-blue);                     /* from design-tokens.md */
}

.hero__link--primary:hover {
  color: var(--apple-link-blue-hover);
  text-decoration: underline;
}

.hero__link--secondary {
  color: var(--apple-link-blue);
}

/* Responsive hero headline scaling */
@media (min-width: 734px) {
  .hero__headline {
    font-size: var(--apple-font-size-hero);          /* 56px */
  }
}

@media (min-width: 1068px) {
  .hero__headline {
    font-size: var(--apple-font-size-hero-max);      /* 80px */
  }
}
```

### Light variant

Replace the background and text colors for a light hero:

```css
.hero--light {
  background: var(--apple-bg-white);
  color: var(--apple-text-primary);
}

.hero--light .hero__subtitle {
  color: var(--apple-text-secondary);
}
```

### Gradient headline variant

Apply a text gradient to the hero headline for dramatic effect (use sparingly — one per page):

```css
.hero__headline--gradient {
  background: var(--apple-gradient-text-purple);     /* from design-tokens.md */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## 4. Product Showcase Grid

A responsive grid for displaying product cards. Apple typically uses 2–3 columns on desktop, collapsing to a single column on mobile. Each card features an image area, a product name, a tagline, and a link.

### Template

```html
<section class="apple-section product-grid-section">
  <div class="apple-content">
    <h2 class="product-grid__heading">Explore the lineup.</h2>
    <div class="product-grid">
      <!-- Card 1 -->
      <article class="product-card">
        <div class="product-card__image">
          <img src="product-1.jpg" alt="MacBook Air — thin and light laptop" loading="lazy">
        </div>
        <h3 class="product-card__name">MacBook Air</h3>
        <p class="product-card__tagline">Strikingly thin. Impressively big.</p>
        <a href="#" class="product-card__link">Learn more ›</a>
      </article>
      <!-- Card 2 -->
      <article class="product-card">
        <div class="product-card__image">
          <img src="product-2.jpg" alt="MacBook Pro — professional laptop" loading="lazy">
        </div>
        <h3 class="product-card__name">MacBook Pro</h3>
        <p class="product-card__tagline">The most advanced Mac laptops.</p>
        <a href="#" class="product-card__link">Learn more ›</a>
      </article>
      <!-- Card 3 -->
      <article class="product-card">
        <div class="product-card__image">
          <img src="product-3.jpg" alt="iMac — all-in-one desktop" loading="lazy">
        </div>
        <h3 class="product-card__name">iMac</h3>
        <p class="product-card__tagline">Say hello to the new iMac.</p>
        <a href="#" class="product-card__link">Learn more ›</a>
      </article>
    </div>
  </div>
</section>
```

```css
/* Product showcase grid */
.product-grid-section {
  background: var(--apple-bg-light-gray);            /* from design-tokens.md */
}

.product-grid__heading {
  font-family: var(--apple-font-display);            /* from typography.md */
  font-size: var(--apple-font-size-subtitle-max);    /* 32px from typography.md */
  font-weight: var(--apple-weight-title);            /* 600 from design-tokens.md */
  line-height: var(--apple-leading-title);           /* 1.1 */
  letter-spacing: var(--apple-tracking-en-title);
  text-align: center;
  color: var(--apple-text-primary);
  margin: 0 0 var(--apple-component-gap-lg) 0;      /* 48px bottom gap */
}

.product-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--apple-component-gap-md);                /* 32px */
}

/* Tablet: 2 columns */
@media (min-width: 734px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 3 columns */
@media (min-width: 1068px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Individual product card */
.product-card {
  background: var(--apple-bg-white);
  border-radius: var(--apple-radius-card);           /* 18px from design-tokens.md */
  padding: var(--apple-card-padding);                /* 32px from design-tokens.md */
  box-shadow: var(--apple-shadow-card);              /* from design-tokens.md */
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--apple-component-gap-sm);                /* 16px */
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.product-card:hover {
  box-shadow: var(--apple-shadow-hover);             /* from design-tokens.md */
  transform: translateY(-4px);
}

.product-card__image {
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  border-radius: var(--apple-radius-card-sm);        /* 12px */
}

.product-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-card__name {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-subtitle-min);    /* 24px from typography.md */
  font-weight: var(--apple-weight-title);            /* 600 */
  line-height: var(--apple-leading-title);
  color: var(--apple-text-primary);
  margin: 0;
}

.product-card__tagline {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body);            /* 17px from typography.md */
  font-weight: var(--apple-weight-body);             /* 400 */
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

.product-card__link:hover {
  color: var(--apple-link-blue-hover);
  text-decoration: underline;
}
```

### Two-column variant

For a two-column layout on desktop (e.g., two featured products side by side):

```css
.product-grid--two-col {
  grid-template-columns: 1fr;
}

@media (min-width: 734px) {
  .product-grid--two-col {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## 5. Feature Comparison Cards

Feature cards present product capabilities in a structured, scannable format. Each card highlights a feature icon or image, a title, and a short description. Apple uses these in rows or grids to compare features across products.

### Template

```html
<section class="apple-section feature-cards-section">
  <div class="apple-content">
    <h2 class="feature-cards__heading">Why Mac.</h2>
    <p class="feature-cards__subheading">There are so many reasons to love a Mac.</p>
    <div class="feature-cards">
      <!-- Card 1 -->
      <article class="feature-card">
        <div class="feature-card__icon">
          <img src="icon-performance.svg" alt="" aria-hidden="true" width="48" height="48">
        </div>
        <h3 class="feature-card__title">Performance</h3>
        <p class="feature-card__description">Apple silicon delivers incredible speed and power efficiency, so everything you do feels fast and responsive.</p>
      </article>
      <!-- Card 2 -->
      <article class="feature-card">
        <div class="feature-card__icon">
          <img src="icon-battery.svg" alt="" aria-hidden="true" width="48" height="48">
        </div>
        <h3 class="feature-card__title">Battery Life</h3>
        <p class="feature-card__description">Up to 18 hours of battery life. Work all day without searching for an outlet.</p>
      </article>
      <!-- Card 3 -->
      <article class="feature-card">
        <div class="feature-card__icon">
          <img src="icon-display.svg" alt="" aria-hidden="true" width="48" height="48">
        </div>
        <h3 class="feature-card__title">Display</h3>
        <p class="feature-card__description">Liquid Retina display with 500 nits of brightness. Every detail is vivid and true to life.</p>
      </article>
      <!-- Card 4 -->
      <article class="feature-card">
        <div class="feature-card__icon">
          <img src="icon-security.svg" alt="" aria-hidden="true" width="48" height="48">
        </div>
        <h3 class="feature-card__title">Security</h3>
        <p class="feature-card__description">Built-in protections keep your data safe. Touch ID makes unlocking instant and secure.</p>
      </article>
    </div>
  </div>
</section>
```

```css
/* Feature comparison cards section */
.feature-cards-section {
  background: var(--apple-bg-white);
}

.feature-cards__heading {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-hero-min);        /* 48px */
  font-weight: var(--apple-weight-title-bold);       /* 700 */
  line-height: var(--apple-leading-title);
  letter-spacing: var(--apple-tracking-en-title);
  text-align: center;
  color: var(--apple-text-primary);
  margin: 0;
}

.feature-cards__subheading {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-subtitle);        /* 28px */
  font-weight: var(--apple-weight-body);             /* 400 */
  line-height: var(--apple-leading-body);
  text-align: center;
  color: var(--apple-text-secondary);
  margin: var(--apple-component-gap-sm) 0 var(--apple-component-gap-lg) 0;
}

.feature-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--apple-component-gap-md);                /* 32px */
}

@media (min-width: 734px) {
  .feature-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1068px) {
  .feature-cards {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Individual feature card */
.feature-card {
  background: var(--apple-bg-light-gray);
  border-radius: var(--apple-radius-card);           /* 18px */
  padding: var(--apple-card-padding);                /* 32px */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--apple-component-gap-sm);                /* 16px */
}

.feature-card__icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.feature-card__icon img {
  width: 100%;
  height: 100%;
}

.feature-card__title {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-subtitle-min);    /* 24px */
  font-weight: var(--apple-weight-title);            /* 600 */
  line-height: var(--apple-leading-title);
  color: var(--apple-text-primary);
  margin: 0;
}

.feature-card__description {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body);            /* 17px */
  font-weight: var(--apple-weight-body);             /* 400 */
  line-height: var(--apple-leading-body);            /* 1.53 */
  color: var(--apple-text-secondary);
  margin: 0;
}
```

### Dark variant

```css
.feature-cards-section--dark {
  background: var(--apple-bg-dark);
}

.feature-cards-section--dark .feature-cards__heading {
  color: var(--apple-text-white);
}

.feature-cards-section--dark .feature-cards__subheading {
  color: var(--apple-text-tertiary);
}

.feature-cards-section--dark .feature-card {
  background: rgba(255, 255, 255, 0.06);
}

.feature-cards-section--dark .feature-card__title {
  color: var(--apple-text-on-dark);
}

.feature-cards-section--dark .feature-card__description {
  color: var(--apple-text-tertiary);
}
```

---


## 6. Scroll-Animated Section

Apple frequently uses scroll-triggered animations to reveal content as the user scrolls down the page. Elements fade in, slide up, or scale into view. This template uses the IntersectionObserver API for broad browser support, with a CSS-only `@keyframes` approach as the animation engine.

### Template

```html
<section class="apple-section scroll-section">
  <div class="apple-content">
    <div class="scroll-reveal">
      <h2 class="scroll-section__headline">A magical new way to interact with Mac.</h2>
    </div>
    <div class="scroll-reveal scroll-reveal--delay-1">
      <p class="scroll-section__body">Apple Intelligence helps you write, express yourself, and get things done effortlessly. It draws on your personal context while setting a brand-new standard for privacy in AI.</p>
    </div>
    <div class="scroll-reveal scroll-reveal--delay-2">
      <div class="scroll-section__media">
        <img src="feature-image.jpg" alt="Mac showing Apple Intelligence features" loading="lazy">
      </div>
    </div>
  </div>
</section>
```

```css
/* Scroll-animated section */
.scroll-section {
  background: var(--apple-bg-white);
  overflow: hidden;
}

.scroll-section__headline {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-hero-min);        /* 48px */
  font-weight: var(--apple-weight-title-bold);       /* 700 */
  line-height: var(--apple-leading-title);
  letter-spacing: var(--apple-tracking-en-title);
  color: var(--apple-text-primary);
  text-align: center;
  margin: 0;
}

.scroll-section__body {
  font-family: var(--apple-font-text);
  font-size: var(--apple-font-size-body-max);        /* 21px */
  font-weight: var(--apple-weight-body);             /* 400 */
  line-height: var(--apple-leading-body);
  color: var(--apple-text-secondary);
  text-align: center;
  max-width: 680px;
  margin: var(--apple-component-gap-md) auto 0;      /* 32px top gap, centered */
}

.scroll-section__media {
  margin-top: var(--apple-component-gap-lg);         /* 48px */
  border-radius: var(--apple-radius-card);           /* 18px */
  overflow: hidden;
}

.scroll-section__media img {
  width: 100%;
  height: auto;
  display: block;
}

/* Scroll reveal animation — initial hidden state */
.scroll-reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

/* Staggered delay modifiers */
.scroll-reveal--delay-1 {
  transition-delay: 0.15s;
}

.scroll-reveal--delay-2 {
  transition-delay: 0.3s;
}

.scroll-reveal--delay-3 {
  transition-delay: 0.45s;
}

/* Visible state — applied by IntersectionObserver */
.scroll-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Responsive headline scaling */
@media (min-width: 734px) {
  .scroll-section__headline {
    font-size: var(--apple-font-size-hero);          /* 56px */
  }
}

@media (min-width: 1068px) {
  .scroll-section__headline {
    font-size: var(--apple-font-size-hero-max);      /* 80px */
  }
}
```

### IntersectionObserver script

Include this script at the end of the page `<body>` to activate scroll-triggered reveals:

```html
<script>
  document.addEventListener('DOMContentLoaded', () => {
    const reveals = document.querySelectorAll('.scroll-reveal');
    if (!reveals.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);          // animate once only
        }
      });
    }, {
      threshold: 0.15,                               // trigger when 15% visible
      rootMargin: '0px 0px -60px 0px'                // slight offset from bottom
    });

    reveals.forEach((el) => observer.observe(el));
  });
</script>
```

### Scale-up variant

For elements that should scale from 95% to 100% as they enter the viewport:

```css
.scroll-reveal--scale {
  opacity: 0;
  transform: scale(0.95);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.scroll-reveal--scale.is-visible {
  opacity: 1;
  transform: scale(1);
}
```

### Dark scroll section variant

```css
.scroll-section--dark {
  background: var(--apple-gradient-bg-dark);
}

.scroll-section--dark .scroll-section__headline {
  color: var(--apple-text-white);
}

.scroll-section--dark .scroll-section__body {
  color: var(--apple-text-tertiary);
}
```

---

## 7. Composing a Full Page

Combine the templates above to build a complete Apple-style page. Follow this vertical stacking order:

```html
<!-- 1. Hero — full-screen opening statement -->
<section class="hero"> ... </section>

<!-- 2. Product grid — showcase the lineup -->
<section class="apple-section product-grid-section"> ... </section>

<!-- 3. Scroll-animated feature highlight -->
<section class="apple-section scroll-section"> ... </section>

<!-- 4. Feature comparison cards -->
<section class="apple-section feature-cards-section"> ... </section>

<!-- 5. Additional scroll sections as needed -->
<section class="apple-section scroll-section scroll-section--dark"> ... </section>
```

### Background alternation pattern

Alternate section backgrounds to create visual rhythm — this is a signature Apple technique:

| Section order | Background | Token |
|---------------|------------|-------|
| 1 (Hero) | Dark / gradient | `--apple-gradient-bg-dark` or `--apple-bg-dark` |
| 2 | Light gray | `--apple-bg-light-gray` |
| 3 | White | `--apple-bg-white` |
| 4 | Light gray | `--apple-bg-light-gray` |
| 5 | Dark | `--apple-bg-dark` |

### Required token imports

Every page that uses these layout templates must include the design token `:root` blocks from `design-tokens.md` and the font stack custom properties from `typography.md`. Minimal required setup:

```css
:root {
  /* From design-tokens.md — spacing */
  --apple-section-gap: 100px;
  --apple-section-gap-sm: 80px;
  --apple-section-gap-lg: 120px;
  --apple-component-gap-sm: 16px;
  --apple-component-gap-md: 32px;
  --apple-component-gap-lg: 48px;
  --apple-card-padding: 32px;
  --apple-content-max-width: 980px;
  --apple-content-max-width-lg: 1200px;

  /* From design-tokens.md — colors */
  --apple-bg-white: #FFFFFF;
  --apple-bg-dark: #1D1D1F;
  --apple-bg-light-gray: #F5F5F7;
  --apple-text-primary: #1D1D1F;
  --apple-text-secondary: #6E6E73;
  --apple-text-tertiary: #86868B;
  --apple-text-on-dark: #F5F5F7;
  --apple-text-white: #FFFFFF;
  --apple-link-blue: #0066CC;
  --apple-link-blue-hover: #0077ED;

  /* From design-tokens.md — radii & shadows */
  --apple-radius-card: 18px;
  --apple-radius-card-sm: 12px;
  --apple-shadow-card: 0 2px 8px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.08);
  --apple-shadow-hover: 0 4px 12px rgba(0,0,0,0.06), 0 12px 32px rgba(0,0,0,0.12);

  /* From design-tokens.md — gradients */
  --apple-gradient-bg-dark: linear-gradient(180deg, #1D1D1F 0%, #000000 100%);
  --apple-gradient-text-purple: linear-gradient(90deg, #7B2FBE, #E040A0);

  /* From design-tokens.md — typography weights & metrics */
  --apple-weight-title: 600;
  --apple-weight-title-bold: 700;
  --apple-weight-body: 400;
  --apple-leading-title: 1.1;
  --apple-leading-body: 1.53;
  --apple-tracking-en-title: -0.015em;

  /* From typography.md — font stacks (English default) */
  --apple-font-display: 'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  --apple-font-text: 'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;

  /* From typography.md — font sizes */
  --apple-font-size-hero: 56px;
  --apple-font-size-hero-min: 48px;
  --apple-font-size-hero-max: 80px;
  --apple-font-size-subtitle: 28px;
  --apple-font-size-subtitle-min: 24px;
  --apple-font-size-subtitle-max: 32px;
  --apple-font-size-body: 17px;
  --apple-font-size-body-max: 21px;
}
```

---

## Quick Reference

| Pattern | Section | Columns | Background |
|---------|---------|---------|------------|
| Hero | Full-screen opening | 1 (centered) | Dark gradient or white |
| Product Grid | Product showcase | 1 → 2 → 3 (responsive) | Light gray |
| Feature Cards | Feature comparison | 1 → 2 → 4 (responsive) | White or dark |
| Scroll Section | Animated content reveal | 1 (centered) | White or dark |

| Spacing context | Token | Value |
|----------------|-------|-------|
| Between sections | `--apple-section-gap` | 80–120px |
| Heading → subtitle | `--apple-component-gap-sm` | 16px |
| Subtitle → body/CTA | `--apple-component-gap-md` | 32px |
| Between sub-blocks | `--apple-component-gap-lg` | 48px |
| Card internal padding | `--apple-card-padding` | 24–40px |
| Content max-width | `--apple-content-max-width` | 980px |
| Content max-width (large) | `--apple-content-max-width-lg` | 1200px |
