# Reference: `02-design.md`

Style: DD (Design Document) — the "how" document. Structure inspired by IEEE 1016 (Software Design Descriptions), simplified to match how much design detail the source material actually contains. This is where a developer looks to understand intended architecture and technical decisions before implementing — it is not a substitute for their own detailed design work where the source never went deep.

## Standard this follows

IEEE 1016-inspired, simplified. This document must never claim more architectural rigor than was genuinely decided. A design doc that invents an architecture nobody agreed to is worse than a short, honest one. Throughout, visibly distinguish **decided** choices from **proposed/leaning** ones.

## Required sections, in order

### 1. Architecture Overview
Plain-language description of the system's major components/services and how they relate, as discussed. A component list or short prose is fine; only produce a Mermaid diagram if the source specified component boundaries clearly enough to make one accurate. If architecture was only loosely discussed, say so and describe what is known.

### 2. Technology Stack
A table of the languages, frameworks, libraries, services, and datastores named anywhere in the source, each marked **Decided** or **Proposed / under discussion**. Include what it's for. If a layer (e.g. database, hosting) was never chosen, list the layer with "not yet selected" rather than omitting it — a dev needs to see the hole.

Format:
```
| Layer | Choice | Status | Notes |
|-------|--------|--------|-------|
| Frontend | React | Decided | Interfaces already built in React |
| Auth | Cognito (Amplify stack) | Proposed | Debated vs. Google Auth — see Open Questions |
| Database | not yet selected | — | No datastore discussed |
```

### 3. Data Model
Entities and relationships as actually discussed — not a full ERD unless the source built one. A relationship list is often sufficient:
```
- Customer — has many — Jobs
- Job — belongs to — Property
- Property — may belong to — one or more Households (still under discussion — see Open Questions)
```
Keep consistent with the Actors/Entities section of `01-requirements.md`. If field-level detail exists in built interfaces, reflect it here (e.g. which fields a form captures) rather than leaving the model vaguer than the code already is.

### 4. Key Interaction Flows
For the most important 1–4 user or system flows that were actually discussed or are evident from the interfaces, describe the sequence of steps end-to-end (e.g. "user submits lookup -> system queries CRM -> match returned -> record rendered"). Prose or a numbered list; a Mermaid sequence diagram only if the source supports that precision. Skip this section entirely if no multi-step flow is discernible — don't fabricate one.

### 5. Interfaces & Integrations
What this system connects to — internal systems, third-party services, APIs — and what's known about each connection's purpose. If an integration was named without specifics ("needs to talk to the CRM"), note the connection and flag the missing contract in Open Questions rather than inventing an API shape. Keep consistent with the "Connects to" entries in `03-interfaces/interface-reference.md`.

### 6. Key Technical Decisions (Decision Log)
Each settled architecture/technology decision: the decision, and the reasoning if it was discussed. This is a log of decisions already made, not a place to introduce new ones on the author's own judgment. Format each as: decision, rationale, source. Leanings that aren't yet decisions go in Open Questions, not here.

### 7. Deployment & Operational Considerations
Only if discussed: hosting target, environments, CI/CD, scaling approach, monitoring. If none of this was discussed, state "Not addressed in source material" in one line — its absence is itself useful signal to a dev team, so don't omit the section silently.

### 8. Open Questions & Assumptions
Design-specific gaps — anything architectural/technical debated without resolution, or that a dev must resolve before building. Be specific and actionable ("auth provider not confirmed — Google Auth vs Cognito discussed, not decided" not "auth needs thought").

## Format

- Markdown; Mermaid diagrams only when the source supports enough structural detail to make them accurate
- Decided vs. Proposed must be visually unambiguous everywhere it matters (status columns, explicit labels)
- Length scales with design maturity — an early-stage project yields a short doc dominated by Open Questions, and that is the correct, honest output
