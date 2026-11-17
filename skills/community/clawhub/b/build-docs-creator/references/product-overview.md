# Reference: `00-product-overview.md`

Style: BRD (Business Requirements Document) — the "why" document. Written for anyone who needs context before touching the requirements or design docs: a new developer, a stakeholder, a PM. Should be readable by a non-technical person.

## Standard this follows

Loosely modeled on standard BRD practice (business case, scope, stakeholders, objectives) — not a rigid numbered standard, since BRDs vary more by organization than SRS/DD do. Goal: clarity and completeness of business context, not conformance to a specific standard.

## Required sections, in order

### 1. Product Summary
2–4 sentences. What this is, in plain language. No jargon, no feature list — what it is and who it's for.

### 2. Business Case / Problem Statement
What problem this solves and why it's worth building. Pull directly from source material — if the "why" was never explicitly stated, say so in Open Questions rather than inventing a business rationale.

### 3. Target Audience / Users
Who uses this. If multiple user types exist, list each with a one-line description of their relationship to the product. Keep consistent with the Actors/Entities section of `01-requirements.md` — the two lists should describe the same people, not diverge.

### 4. Core Use Cases
How this actually gets used day to day, in prose or a short list — not formal use-case diagrams. 3–6 concrete scenarios is typical; don't pad if the source only supports 2.

### 5. Intended Outcomes / Success Criteria
What success looks like, if discussed — metrics, goals, or qualitative outcomes stakeholders care about. If never discussed, state plainly "Not yet defined in source material" — do not invent KPIs.

### 6. Out of Scope
Anything explicitly discussed as *not* part of this product/feature. Omit the section entirely if scope boundaries were never discussed — don't force a placeholder.

### 7. Open Questions & Assumptions
Any gap in business rationale, audience, or scope the source didn't resolve. Should exist even if short — an empty section implies false completeness.

## Format

- Markdown, clean headers matching the section list
- No filler ("In today's fast-paced world...") — get to the point
- Length scales with source material: a small feature might be one page; a full product two to three. Never pad to a length target.
- Reads as clean prose, not a citation-heavy paper — but every factual claim must be traceable to source material internally
