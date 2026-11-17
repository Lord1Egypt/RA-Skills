# Reference: `01-requirements.md`

Style: SRS (Software Requirements Specification) — the "what" document. Structure inspired by ISO/IEC/IEEE 29148:2018 (successor to IEEE 830), simplified and right-sized to the actual scope. This is what a developer reads to know what the system must do.

## Standard this follows

- Numbered, uniquely-identified requirements (`FR-n`, `NFR-n`) so other documents (especially the traceability matrix) can reference them precisely
- Clear separation of functional vs. non-functional requirements
- "shall" for firm, committed requirements; "should" for softer/desired ones — verb strength must match how confidently the source stated it, never upgraded for polish
- Each functional requirement carries acceptance criteria so "done" is testable

## Required sections, in order

### 1. Purpose & Scope
One paragraph. What this document specifies and its boundaries. Reference `00-product-overview.md` for business context rather than repeating it.

### 2. Glossary / Terminology
A short table of domain terms, entity names, and acronyms, each with a one-line definition. This is especially important for projects assembled from multiple sources (e.g. ChatGPT-authored requirements + Claude design work), where the same concept may have been named two different ways — pick one canonical term, define it, and note the alias. If a term's meaning was never pinned down, say so here and cross-list it in Open Questions.

Format:
```
| Term | Definition | Also called |
|------|------------|-------------|
| Household | A physical residence and its occupants, distinct from the billing Customer | "Property" (in early notes) |
```

### 3. Actors / Entities
Every role or entity type that interacts with the system, pulled directly from source material. For each: name, one-line description, and relationships to other entities if discussed. Do not invent entities not present in source material — flag suspected gaps in Open Questions. Keep consistent with the data model in `02-design.md` and the audience list in `00-product-overview.md`.

### 4. Functional Requirements
Numbered `FR-1`, `FR-2`, ... — one atomic behavior each (no compound "and" bundles). Group under subheadings by feature area or actor when there are more than ~10. Each requirement includes acceptance criteria in Given/When/Then form where the behavior supports it.

Format:
```
**FR-3** — The system shall allow a CSR to look up a customer by phone number.
- *Source:* CSR workflow discussion, 2026-06-19
- *Acceptance:* Given a valid phone number on file, when the CSR submits it, then the matching customer record is displayed. Given a number not on file, then a "no match" state is shown.
- *Origin:* imported requirement | derived from built interface `customer-lookup.html` | discussed in project
```

The `Origin` tag is required when the project mixes imported (e.g. ChatGPT) requirements with project-native ones — it makes the reconciliation visible. Requirements captured from a built interface that had no matching original requirement must be tagged *derived from built interface*.

### 5. Non-Functional Requirements
Numbered `NFR-1`, ... Group by category, and include only categories actually discussed:
- **Performance** (response time, concurrency, scale)
- **Security** (auth model, data protection, access control)
- **Compliance** (regulatory/industry standards — SOC 2, HIPAA, GDPR if mentioned)
- **Integration** (external systems it must connect to)
- **Reliability / Availability**
- **Accessibility** (if UI standards were discussed)

Do not invent NFRs in undiscussed categories. A project with no stated performance targets should not have fabricated numbers — omit the category or note it as unspecified in Open Questions.

### 6. Constraints
Technical, regulatory, or business constraints shaping what can be built: existing tech stack it must integrate with, timeline/budget limits if mentioned, third-party dependencies.

### 7. Open Questions & Assumptions
Every ambiguity, unresolved debate, gap, and — critically — every imported-vs-built discrepancy found during reconciliation. The most important section in this document. Should never be empty unless the source was a fully resolved, unambiguous spec. Each item states the specific gap and, if known, who/what must resolve it.

## Format

- Markdown; requirements numbered and ID'd as above so the traceability matrix can cite them
- Verb discipline: "shall" only for confident/settled requirements; "should" for soft/aspirational/debated
- Length scales with real scope — never pad with generic requirements to look thorough
