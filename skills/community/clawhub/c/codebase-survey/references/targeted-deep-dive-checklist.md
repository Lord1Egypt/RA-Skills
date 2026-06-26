# Targeted Domain Deep Dive — Step-by-Step Checklist

Use when the user asks for a deep dive into ONE specific domain/feature within an already-familiar project.

## Precondition
- [ ] CLAUDE.md read (project memory, hard rules, today's state)
- [ ] CLAUDE.local.md — **only read with explicit user approval in the current turn** (ask before reading)
- [ ] Latest 1-3 recaps read (last session context)
- [ ] Active plans identified and read

## Step 1: Feature Doc
- [ ] Read the relevant `docs/feature-<slug>.md` or architectural doc
- [ ] Note: API endpoint specs, prompt strategy, business rules, acceptance criteria

## Step 2: Schema
- [ ] Read the Prisma model(s) for the domain
- [ ] Note every field, relation, index, @map column name
- [ ] Cross-reference against feature doc field descriptions
- [ ] Note which fields are CREATED during import vs lifecycle-only fields

## Step 3: API Routes
- [ ] Read every file under `src/app/api/<domain>/`
- [ ] For each route, capture: auth guard, validation, feature flag check, processing logic, response schema
- [ ] Note any hidden/dormant routes (e.g., reprocess endpoints with hidden UI buttons)
- [ ] Note transaction patterns and batch processing logic

## Step 4: Pipeline / Infrastructure
- [ ] Read all shared library files the routes depend on (AI clients, extractors, matchers, loggers)
- [ ] Note the actual implementation depth (vision vs. text, fuzzy matching algorithms, spatial ordering)
- [ ] Note reusable patterns (subprocess isolation for native modules, fire-and-forget logging)

## Step 5: UI Components
- [ ] Read the page component and review/submit component
- [ ] Trace the data flow: API response → UI state → user edits → submit payload
- [ ] Note: validation UX, error states, partial submission, dormant features

## Step 6: Synthesize Report
- [ ] Architecture overview (ASCII/flow diagram showing phases)
- [ ] Data model (field-by-field mapping from extraction → import)
- [ ] Detailed flow for each phase (endpoint, auth, processing)
- [ ] Edge cases & business rules table (rule, where enforced)
- [ ] Shared infrastructure summary
- [ ] Dormant/hidden paths documented
- [ ] Field-level mapping with transformations (backfills, defaults, type coercions)

## Verification
- [ ] Report is readable in 2-3 minutes (not a raw file dump)
- [ ] Every file under the domain is accounted for (no unread routes or critical lib files)
- [ ] Contradictions between docs and implementation surfaced explicitly
