---
name: agentify
description: Analyze, rewrite, and generate design specs to make web pages and websites more easily usable by AI agents, web scrapers, and automation tools. Use when (1) evaluating how agent-friendly, accessible (a11y), or machine-readable a web page or HTML/JSX/Vue/Svelte code is, (2) rewriting web templates to add semantic markup, ARIA, structured data (schema.org / JSON-LD), and stable selectors (data-testid) for tools like Playwright, Puppeteer, Cypress, or Selenium, (3) generating agent-friendly design specification documents for development teams covering SEO, accessibility, and GEO (Generative Engine Optimization). Triggers on phrases like "agent-friendly", "make this page work with agents", "analyze for automation", "agentify", "improve SEO", "add structured data", "add data-testid", "web scraping friendly", "machine-readable", "a11y audit", "crawler-friendly".
---

# Agentify

Make web pages and websites more easily navigable, parseable, and operable by AI agents, web scrapers, and automation tools.

## Core Capabilities

### 1. Analyze

Evaluate web pages or code for agent-friendliness. Produce a scored report (0-100) with actionable improvements.

**When to use:** The user wants to audit a page, URL, or codebase for agent accessibility.

**Workflow:**

1. Acquire the content:
   - URL → fetch and retrieve HTML
   - File path → read the file
   - Glob pattern → find matching files, analyze each
   - IDE selection → analyze selected code
2. Read the scoring reference: [references/scoring.md](references/scoring.md)
3. Read the full checklist: [references/checklist.md](references/checklist.md)
4. Evaluate across 9 categories (100 points total):

| # | Category | Pts | Focus |
|---|----------|-----|-------|
| 1 | Semantic HTML | 15 | Heading hierarchy, landmarks, semantic tags vs div soup |
| 2 | ARIA & Accessibility | 15 | Roles, labels, live regions, keyboard attributes |
| 3 | Structured Data | 15 | JSON-LD / schema.org presence, completeness |
| 4 | Form Readability | 10 | Label association, autocomplete, fieldset grouping |
| 5 | Navigation Clarity | 10 | Consistent nav, breadcrumbs, skip links, sitemap |
| 6 | Automation Attributes | 10 | data-testid coverage, data-* for key elements |
| 7 | CSS Selector Stability | 5 | Meaningful class names vs generated hashes |
| 8 | API Discoverability | 10 | Canonical URLs, link relations, OpenAPI |
| 9 | Meta & Machine Signals | 10 | robots meta, description, OG tags, sitemap |

5. Output report in this format:
   - Score: X/100 (Grade A-F)
   - Per-category score breakdown table
   - Top 5 priority improvements with before/after code
   - Detailed findings per category
   - Quick wins section (changes under 5 minutes, 5+ point gain)

### 2. Rewrite

Transform web templates to be agent-friendly while preserving all existing functionality.

**When to use:** The user wants to improve existing code for agent consumption.

**Workflow:**

1. Detect framework from file extension (.html, .jsx, .tsx, .vue, .svelte)
2. Read the patterns reference: [references/patterns.md](references/patterns.md)
3. Read framework-specific guidance: [references/frameworks.md](references/frameworks.md)
4. Read and understand the entire file before modifying
5. Apply transformations in order:
   - Replace non-semantic elements with semantic equivalents (only when intent is unambiguous)
   - Add ARIA attributes to interactive elements
   - Add `data-testid` to buttons, links, inputs, content containers (kebab-case naming)
   - Improve form labels, autocomplete, fieldset grouping
   - Insert JSON-LD structured data where content type is identifiable
   - Add meta tags for full HTML pages
   - Add skip links and nav labels
   - Fix heading hierarchy

**Safety rules (non-negotiable):**
- Never remove existing code, event handlers, or component logic
- Never change class names, IDs, or visual appearance
- Never break framework-specific syntax
- Only add attributes, never replace unless strictly better
- Match existing formatting style

6. After modification, summarize: number of changes per category, changes considered but skipped, and follow-up suggestions needing human judgment

### 3. Design Spec

Generate a comprehensive agent-friendly design specification document for development teams.

**When to use:** The user wants to establish standards for agent-friendly web development.

**Workflow:**

1. Parse arguments for project name and focus area (e-commerce, dashboard, docs, SaaS, marketing)
2. Scan the project if in a code directory:
   - Detect framework (package.json, config files)
   - Detect test framework
   - Grep for existing data-testid, aria-*, schema.org patterns
   - Read 2-3 representative components to understand code style
3. Read the spec template: [references/spec-template.md](references/spec-template.md)
4. Read the example spec: [references/spec-example.md](references/spec-example.md)
5. Generate a markdown spec to `agent-friendly-spec.md` covering:
   - Executive summary
   - Semantic HTML guidelines
   - ARIA & accessibility patterns
   - Naming conventions (data-testid, CSS classes, components)
   - Structured data (JSON-LD) per page type
   - Form design patterns
   - Navigation patterns
   - API & discoverability
   - Meta tags & machine signals
   - Component-level checklists
   - Testing for agent-friendliness
   - Migration guide (quick wins → medium → large effort)

Each section must include: priority level (P0/P1/P2), code examples for the detected framework, anti-patterns, and verification methods.

## Shared Knowledge Base

For the canonical reference on all agent-friendly web patterns (semantic HTML, ARIA, structured data, data attributes, forms, navigation, APIs, meta tags, CSS stability, interaction patterns), read: [references/knowledge-base.md](references/knowledge-base.md)
