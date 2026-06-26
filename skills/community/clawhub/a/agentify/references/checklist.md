# Agent-Friendliness Checklist

Severity: **[C]** Critical · **[M]** Major · **[m]** Minor

## Table of Contents
- [1. Semantic HTML](#1-semantic-html-15-pts)
- [2. ARIA & Accessibility](#2-aria--accessibility-15-pts)
- [3. Structured Data](#3-structured-data-15-pts)
- [4. Form Readability](#4-form-readability-10-pts)
- [5. Navigation Clarity](#5-navigation-clarity-10-pts)
- [6. Automation Attributes](#6-automation-attributes-10-pts)
- [7. CSS Selector Stability](#7-css-selector-stability-5-pts)
- [8. API Discoverability](#8-api-discoverability-10-pts)
- [9. Meta & Machine Signals](#9-meta--machine-signals-10-pts)

---

## 1. Semantic HTML (15 pts)

**Structure:**
- [C] Exactly one `<h1>` per page
- [C] No heading level skips (h1→h3 without h2)
- [M] `<main>` present (exactly one)
- [M] `<header>`, `<footer>` present
- [M] `<nav>` for navigation (not divs)
- [m] `<aside>` for sidebar content

**Content elements:**
- [C] Interactive elements use `<button>` or `<a>`, not `<div onclick>`
- [M] Lists use `<ul>`, `<ol>`, `<dl>`
- [M] Tables use `<table>` with `<thead>`, `<th>`
- [M] `<article>` wraps standalone content
- [m] `<time datetime>` for dates
- [m] `<data value>` for machine-readable values

**Anti-patterns:**
- [C] >50% structural divs have semantic alternatives → div soup
- [M] `<a>` without href used as buttons

---

## 2. ARIA & Accessibility (15 pts)

**Accessible names:**
- [C] All `<button>` have text or `aria-label`
- [C] All `<a>` have descriptive text
- [C] All `<input>` have associated labels
- [C] All `<img>` have `alt` (empty for decorative)
- [M] Icon-only buttons have `aria-label`
- [M] `<svg>` have `<title>` or `aria-label`

**Roles/states:**
- [M] Custom widgets have appropriate `role`
- [M] Expandable elements use `aria-expanded`
- [M] Tabs use `role="tablist"`, `role="tab"`, `role="tabpanel"`
- [m] Loading states use `aria-busy`

**Live regions:**
- [M] Dynamic updates use `aria-live`
- [M] Error messages use `role="alert"`

**Anti-patterns:**
- [C] No `role` where native HTML suffices
- [M] `aria-hidden="true"` not on interactive elements

---

## 3. Structured Data (15 pts)

- [C] At least one JSON-LD block on content pages
- [M] Correct `@context` and `@type`
- [M] Required properties present for schema type
- [M] Dates in ISO 8601
- [M] `BreadcrumbList` on hierarchical pages
- [m] `WebSite` + `SearchAction` on homepage
- [m] Valid JSON, no undefined properties

---

## 4. Form Readability (10 pts)

- [C] Every input has `<label>` via for/id or wrapping
- [C] Labels are descriptive (not placeholder-only)
- [M] Related fields in `<fieldset>` + `<legend>`
- [M] `name` attributes are semantic
- [M] `type` matches content (email, tel, url)
- [M] `autocomplete` on standard fields
- [M] Errors associated via `aria-describedby`
- [m] `required` or `aria-required` on mandatory fields

**N/A handling:** If no forms, redistribute 10 pts: +4 Semantic HTML, +3 ARIA, +3 Structured Data.

---

## 5. Navigation Clarity (10 pts)

- [C] Primary navigation uses `<nav>`
- [M] Nav has `aria-label`
- [M] Current page: `aria-current="page"`
- [M] Breadcrumbs present on hierarchical pages
- [C] Links have descriptive text
- [m] Skip link as first focusable element
- [m] `/sitemap.xml` exists and valid

---

## 6. Automation Attributes (10 pts)

- [M] Interactive elements have `data-testid`
- [M] Key content containers have `data-testid`
- [M] `data-testid` values: kebab-case, descriptive
- [m] Entity tagging: `data-entity-type`, `data-entity-id`
- [m] State reflection: `data-state`
- [M] Consistent naming convention across site

---

## 7. CSS Selector Stability (5 pts)

- [M] Meaningful class names (not auto-generated hashes)
- [M] Consistent naming convention (BEM or similar)
- [M] No critical functionality depends on `:nth-child`

---

## 8. API Discoverability (10 pts)

- [M] `<link rel="canonical">` present
- [m] `<link rel="next/prev">` for pagination
- [m] `<link rel="alternate">` for representations
- [m] Consistent URL patterns
- [m] API docs available (OpenAPI/Swagger)

---

## 9. Meta & Machine Signals (10 pts)

- [C] `<meta charset="utf-8">`
- [M] `<meta name="description">` with content
- [M] `<meta name="viewport">`
- [M] `og:title`, `og:description` present
- [m] `og:image`, `og:url`, `og:type`
- [m] `<html lang="...">` set
- [m] `robots.txt` allows content pages
