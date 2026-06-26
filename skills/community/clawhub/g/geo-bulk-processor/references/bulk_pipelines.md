# GEO Bulk Pipelines Reference

This document provides reference patterns and terminology for the
`geo-bulk-processor` skill. It is meant to help you design GEO bulk
pipelines that are **scalable, repeatable, and easy to operationalize**
across large websites and content libraries.

You do not need to follow these patterns rigidly. Instead, use them as
default building blocks and adapt them to the user’s actual systems,
constraints, and goals.

---

## 1. Core concepts

- **Content item**  
  A single page or document (e.g., one URL, one CMS entry, one file).

- **Cluster**  
  A group of content items that share similar purpose, structure, and
  GEO opportunities (for example, all /blog/ posts, all product detail
  pages, or all city-based location pages).

- **Page type / template**  
  A reusable structure for a set of pages. One cluster may map to a
  single page type or a small number of closely related page types.

- **Pipeline**  
  A sequence of steps that transform inputs (existing content, metadata,
  analytics) into outputs (GEO-optimized content, structured data,
  import files for CMS, etc.).

---

## 2. Typical pipeline phases

Most GEO bulk pipelines can be expressed using four high-level phases:

1. **Inventory and normalization**
2. **Content and metadata enrichment**
3. **Schema and technical enhancements**
4. **Export, rollout, and monitoring**

You can design one pipeline per cluster or page type, using these phases
as anchors.

### 2.1 Inventory and normalization

Objectives:
- Build a reliable, structured view of the content corpus.
- Normalize disparate sources into a single schema.

Common steps:
- Ingest sitemap(s) and URL lists.
- Join analytics or search data (visits, conversions, queries).
- Add CMS or product catalog data where available.
- Normalize into a table or record schema with fields such as:
  - `id`
  - `url`
  - `path`
  - `content_type`
  - `language`
  - `cluster`
  - `priority`

### 2.2 Content and metadata enrichment

Objectives:
- Strengthen content quality and structure for GEO.
- Ensure key elements are present and consistently formatted.

Common steps:
- Generate or refine titles, intros, and key sections using GEO-focused
  templates.
- Add or improve FAQ blocks aligned with target queries.
- Standardize internal linking patterns (e.g., to categories or hubs).
- Add or normalize metadata (e.g., canonical tags, language tags).

This is where other `geo-*` skills (for example, content optimizers)
integrate most heavily.

### 2.3 Schema and technical enhancements

Objectives:
- Make content machine-readable for AI and search engines.
- Align schema with content types and business goals.

Common steps:
- For products: Product, Offer, Review, FAQ schema.
- For locations: LocalBusiness, Organization, BreadcrumbList.
- For articles: Article, BlogPosting, FAQPage.
- For documentation: TechArticle, FAQPage, BreadcrumbList.

This phase is a natural integration point with skills like
`geo-schema-gen`.

### 2.4 Export, rollout, and monitoring

Objectives:
- Deliver outputs in formats that implementation teams can use.
- Phase changes to manage risk and measure impact.

Common steps:
- Export CSV/JSON for CMS or deployment pipelines.
- Generate implementation guides or mapping tables.
- Define rollout phases (pilot → expansion → full roll-out).
- Design monitoring dashboards and GEO metrics tracking.

---

## 3. Example cluster patterns

Below are some common cluster patterns. Adapt and extend them based on
the user’s site and goals.

### 3.1 Blog / editorial content

- **Cluster definition**: URLs under `/blog/` or `/insights/`.
- **Goals**:
  - Improve coverage for topic + intent queries.
  - Standardize structure (intro, key takeaways, FAQs).
  - Strengthen internal linking to product/docs.
- **Key pipeline elements**:
  - Content enrichment with GEO-aware headings and summaries.
  - FAQ extraction or generation.
  - Article/BlogPosting + FAQPage schema where appropriate.

### 3.2 Product detail pages (PDPs)

- **Cluster definition**: URLs under `/products/` or by template ID.
- **Goals**:
  - Make product attributes and benefits machine-readable.
  - Improve comparability and clarity for AI answers.
  - Increase long-tail and “best for X” coverage.
- **Key pipeline elements**:
  - Normalize product attributes and features.
  - Add FAQ sections targeting common objections and use cases.
  - Apply Product, Offer, Review, and FAQ schema.

### 3.3 Location / store pages

- **Cluster definition**: URLs under `/locations/`, `/stores/`, or
  derived from location database.
- **Goals**:
  - Improve “near me” and city + service queries.
  - Provide consistent NAP (Name, Address, Phone) and opening hours.
  - Highlight services, insurance, or specialties by location.
- **Key pipeline elements**:
  - Ensure consistent location data and contact information.
  - Add localized copy and FAQs (parking, insurance, booking).
  - Apply LocalBusiness and related schema.

---

## 4. Rollout and QA patterns

### 4.1 Phased rollout

Always prefer **phased rollout** over all-at-once changes:
- **Pilot phase**: small sample of high-traffic or representative pages.
- **Expansion phase**: additional clusters or segments based on pilot
  results.
- **Full rollout**: broad application once patterns are stable.

### 4.2 QA checklists

For each cluster, define a simple QA checklist, for example:
- Content sections present and ordered correctly.
- Key fields populated (titles, intros, FAQs, CTAs).
- Schema validates and matches visible content.
- No critical regressions (links, tracking, forms).

---

## 5. Using these patterns with the skill

When using `geo-bulk-processor`:
- Reuse these patterns as **defaults** for inventory, clustering,
  pipeline design, and rollout.
- Reference them explicitly when explaining plans to the user’s team
  (“this follows the standard 4-phase pipeline with a phased rollout”).
- Adapt terminology and structures to match the user’s internal systems
  (field names, template IDs, existing workflows).

The goal is to turn large, messy content universes into **organized,
actionable GEO programs** that can be executed and iterated on over
time.

