# Agent-Friendly Web Reference

Shared knowledge base for all Agentify capabilities.

## Table of Contents
- [1. Semantic HTML](#1-semantic-html)
- [2. ARIA](#2-aria)
- [3. Structured Data](#3-structured-data)
- [4. Data Attributes](#4-data-attributes)
- [5. Forms](#5-forms)
- [6. Navigation](#6-navigation)
- [7. API Discoverability](#7-api-discoverability)
- [8. Meta & Machine Signals](#8-meta--machine-signals)
- [9. CSS Selector Stability](#9-css-selector-stability)
- [10. Agent Interaction Patterns](#10-agent-interaction-patterns)

---

## 1. Semantic HTML

Agents parse DOM trees to understand page structure. Semantic elements provide meaning without heuristics.

| Instead of | Use | Why |
|-----------|-----|-----|
| `<div>` for sections | `<header>`, `<main>`, `<footer>`, `<aside>`, `<nav>` | Landmark navigation |
| `<div>` for content | `<article>`, `<section>`, `<figure>`, `<details>` | Content boundaries |
| `<span>` for emphasis | `<strong>`, `<em>`, `<mark>`, `<time>` | Semantic meaning |
| `<div>` for lists | `<ul>`, `<ol>`, `<dl>` | List recognition |
| `<div>` for tables | `<table>` with `<thead>`, `<tbody>`, `<th>` | Tabular data parsing |
| `<div onclick>` | `<button>`, `<a>` | Actionable element identification |

Heading rules:
- One `<h1>` per page
- Never skip levels (h1 → h3 without h2)

---

## 2. ARIA

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `role` | Define element purpose | `role="search"`, `role="tablist"` |
| `aria-label` | Name for elements without visible text | `aria-label="Close dialog"` |
| `aria-labelledby` | Reference another element as label | `aria-labelledby="section-title"` |
| `aria-describedby` | Reference descriptive text | `aria-describedby="password-hint"` |
| `aria-expanded` | Expandable state | `aria-expanded="false"` |
| `aria-hidden` | Hide from agents | `aria-hidden="true"` |
| `aria-live` | Dynamic content changes | `aria-live="polite"` |
| `aria-required` | Required fields | `aria-required="true"` |
| `aria-invalid` | Validation errors | `aria-invalid="true"` |
| `aria-current` | Current item in nav | `aria-current="page"` |

Rules:
- Don't use ARIA when native HTML provides same semantics
- Every interactive element must have an accessible name
- Keep ARIA states in sync with visual state

---

## 3. Structured Data

JSON-LD provides explicit, machine-parseable metadata about page content.

| Page type | Schema type | Key properties |
|-----------|-------------|----------------|
| Article/Blog | `Article`, `BlogPosting` | headline, author, datePublished |
| Product | `Product` | name, price, availability, review |
| Organization | `Organization` | name, url, logo, contactPoint |
| Event | `Event` | name, startDate, location |
| FAQ | `FAQPage` | mainEntity (Question + Answer) |
| How-to | `HowTo` | step, tool, supply |
| Breadcrumb | `BreadcrumbList` | itemListElement |
| Search | `WebSite` + `SearchAction` | potentialAction.query-input |

Placement:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "author": { "@type": "Person", "name": "..." },
  "datePublished": "2025-01-15"
}
</script>
```

Best practices:
- Place in `<head>` or early in `<body>`
- Use `@id` for cross-referencing entities
- Include `BreadcrumbList` on hierarchical pages

---

## 4. Data Attributes

### data-testid (de facto standard for stable element targeting)
```html
<button data-testid="submit-order">Place Order</button>
```

Naming: kebab-case, descriptive, component-scoped for large apps.

Apply to: interactive elements, content containers, key text nodes, form fields.

### Other data attributes
| Attribute | Purpose |
|-----------|---------|
| `data-action` | Describe element action |
| `data-entity-type` | Content entity type |
| `data-entity-id` | Unique entity identifier |
| `data-state` | Current component state |
| `data-section` | Label page sections |

---

## 5. Forms

```html
<label for="email">Email address</label>
<input id="email" type="email" name="email" autocomplete="email" required>

<fieldset>
  <legend>Shipping Address</legend>
  <label for="street">Street</label>
  <input id="street" name="street" autocomplete="street-address">
</fieldset>

<input id="name" aria-describedby="name-error" aria-invalid="true">
<span id="name-error" role="alert">Name is required</span>
```

Checklist:
- Every `<input>` has associated `<label>` (via for/id or wrapping)
- Use `name` attributes that describe the field
- Use `autocomplete` for standard fields
- Group related fields with `<fieldset>` + `<legend>`
- Use appropriate `type` (email, tel, url, date, number)
- Mark required fields with `required` or `aria-required`
- Associate errors with `aria-describedby`

---

## 6. Navigation

- Use `<nav>` with `aria-label` for all navigation regions
- Include skip link as first focusable element
- Provide breadcrumbs with `BreadcrumbList` structured data
- Use `aria-current="page"` for current page
- Use descriptive link text (not "click here")
- Provide `/sitemap.xml` with `lastmod` dates

---

## 7. API Discoverability

```html
<link rel="canonical" href="https://example.com/page">
<link rel="next" href="/articles?page=2">
<link rel="prev" href="/articles?page=1">
<link rel="alternate" type="application/rss+xml" href="/feed.xml">
<link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml">
```

REST: consistent URL patterns, OpenAPI specs, content negotiation, Link headers for pagination.

---

## 8. Meta & Machine Signals

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Clear page description">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://example.com/page">
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
```

- Set `<html lang="...">`
- Don't block agent-relevant content in robots.txt
- Provide sitemap.xml
- Use `<link rel="alternate">` for multi-language

---

## 9. CSS Selector Stability

- Use semantic class names: `.product-card`, `.nav-primary`
- If using CSS-in-JS, add `data-testid` as stable anchors
- Prefer BEM or consistent naming convention
- Never rely on `:nth-child` for critical targeting

---

## 10. Agent Interaction Patterns

### Actions
- Buttons and links: clear, descriptive text
- Group related actions within `<nav>`, `<menu>`, `<fieldset>`
- Label destructive actions clearly ("Delete account" not "Remove")

### State
- Use `aria-expanded`, `aria-selected`, `aria-checked`
- Use `aria-busy="true"` for loading
- Keep DOM state in sync with visual state

### Content extraction
- Wrap standalone content in `<article>`
- Use `<time datetime="...">` for dates
- Use `<data value="...">` for machine-readable values
- Use `<abbr title="...">` for abbreviations
