# Review Type Bundles

Pre-configured reviewer combinations by document type. Look up the document type, spawn the listed reviewers.

---

## Architecture / Strategy

**Use for:** System design docs, technical strategy, multi-component architecture decisions

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Theory & Data Modeling | T |
| B | Implementation & Systems | I |

**Additional focus for prompts:**
- Ask Reviewer A to specifically challenge "independence" claims between components
- Ask Reviewer B to focus on what the design assumes about infrastructure that may not hold

**Expected output:** Minimum 2 CRITICAL issues on any architecture doc of real complexity. Zero CRITICALs is a red flag.

---

## Pipeline / Workflow

**Use for:** Data pipelines, enrichment flows, multi-step automation, event-driven systems

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Pipeline & Sequencing | P |
| B | Implementation & Systems | I |

**Additional focus for prompts:**
- Ask Reviewer A to specifically trace every failure mode for every step
- Ask Reviewer B to focus on state machine completeness and partial failure recovery

---

## Schema / Migration

**Use for:** Database schema designs, migration SQL, index strategies

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Implementation & Systems | I |
| B | Performance & Indexes | X |

**Additional focus for prompts:**
- Ask Reviewer A to test every `ADD COLUMN IF NOT EXISTS` for idempotency traps
- Ask Reviewer B to trace every query pattern against the index types created

**Common catches:** GIN vs B-tree mismatches, inline CHECK constraint bypass, wrong data types, JSONB vs column selection errors.

---

## Security Design

**Use for:** Access control systems, authentication flows, data permission models

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Security & Access | S |
| B | Theory & Data Modeling | T |

**Additional focus for prompts:**
- Ask Reviewer A to assume an adversarial agent is trying to bypass every gate
- Ask Reviewer B to check whether the access model has contradictory defaults

---

## Marketing / Positioning

**Use for:** Positioning statements, GTM strategy, competitive narratives, product copy

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Positioning & Message | M |
| B | Theory & Data Modeling | T |

**Additional focus for prompts:**
- Ask Reviewer A to check every claim that could be challenged by a prospect
- Ask Reviewer B to check internal consistency and whether the positioning is actually differentiated

---

## API / Interface Design

**Use for:** REST/GraphQL API specs, SDK interfaces, event schemas

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Implementation & Systems | I |
| B | Theory & Data Modeling | T |

**Additional focus for prompts:**
- Ask Reviewer A to check for breaking changes and versioning gaps
- Ask Reviewer B to check naming consistency and abstraction correctness

---

## Complex / High-Stakes (3 Reviewers)

**Use for:** Major architectural decisions, anything with significant irreversible consequences

| Reviewer | Persona | Tag |
|----------|---------|-----|
| A | Theory & Data Modeling | T |
| B | Implementation & Systems | I |
| C | Pipeline & Sequencing | P |

Spawn all three simultaneously. Synthesis will take longer but the coverage is meaningfully broader.

---

## Choosing Custom Reviewers

If none of the above bundles fit exactly:

1. Read `reviewer-personas.md` and identify the two personas whose focus areas best match the document's risk areas
2. Ask: "Where would this document most likely fail?" — pick the reviewers who cover those failure modes
3. Optionally add domain-specific focus points to the prompt to sharpen the review
