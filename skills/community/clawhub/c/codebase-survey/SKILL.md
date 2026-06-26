---
name: codebase-survey
description: "Survey an existing codebase to understand its structure, scope, architecture, and current state. Trigger on 'deep dive', 'explore this codebase', 'survey the project', 'understand the architecture', 'onboard me to this project', 'walk me through this repo', or 'what are we working with here'. Use before planning or implementing on an unfamiliar or long-neglected codebase."
version: 1.1.0
author: Alejandro Del Villar
license: MIT
metadata:
  hermes:
    tags: [codebase-exploration, architecture-review, onboarding, reconnaissance, discovery]
    related_skills: [project-warmup, draft-feature-plan, refactor-safely]
---

# Codebase Survey

Systematically discover what an existing codebase contains, how it's organized, and where the complexity lives. Produces a synthesized report rather than a raw file dump.

## When to Use

- User says: "do a deep dive of this project", "explore this codebase", "survey the project", "understand the architecture", "onboard me to this project", "walk me through this repo", "what are we working with here"
- Picking up a project you haven't worked on in a long time and need a refresh before starting work
- Pre-planning reconnaissance: need to know the schema, API surface, and dependency graph before estimating a feature
- Handoff context: explaining to the user (or a future reader) what the codebase currently contains

## Important: CLAUDE.md overrides generic survey

Many projects (especially this user's) maintain a CLAUDE.md file with a "Where to find things" map. **If the project has a well-structured CLAUDE.md, read it FIRST — before any of the steps below.** Use the "Where to find things" map as your primary survey guide. Steps below become fallbacks for areas the CLAUDE.md doesn't cover.

A rich CLAUDE.md will tell you:
- The project's doc tree structure (which files to read for architecture, schema, features, pipeline)
- The branch → environment topology
- Current state / what's shipped
- Hard rules and conventions
- Contracts (what artifacts matter)

This is more efficient than running a generic breadth-first scan. Only fall back to the generic workflow if the CLAUDE.md is absent, sparse, or stale.

## Variant: Targeted Domain Deep Dive

**When:** The user asks for a "deep dive" into a SPECIFIC domain or feature within an already-familiar project (e.g., "deep dive of booking import and creation"), not the full codebase. The project's CLAUDE.md context is already loaded or available.

**Not when:** The project is unfamiliar — do the full codebase survey first.

**Not when:** The user just has a narrow question about one file — read that file directly.

### Targeted Deep Dive Pattern

After warmup (CLAUDE.md, CLAUDE.local.md, recaps, active plans loaded):

1. **Read the relevant feature doc(s)** — the `docs/feature-<slug>.md` or `docs/technical-documentation.md` section for that domain. This gives you the contract: what it's supposed to do, API schemas, prompt strategy, business rules, acceptance criteria.

2. **Read the Prisma schema model(s)** — the `model Booking { ... }` block. Note every field, relation, index, and `@map` column name. Cross-reference against the feature doc's field descriptions.

3. **Read ALL API routes under the domain** — every file in `src/app/api/<domain>/route.ts` and any sub-routes. In a booking import system, that's extract, reprocess, and import — three routes that chain together. Note validation patterns, auth guards, feature-flag guards, and transaction patterns.

4. **Read the pipeline/infrastructure files** — the shared library files that the routes depend on: AI clients, extractors, prompt parsers, matchers, loggers, cost calculators. These will contain the actual implementation depth (vision vs. text extraction, spatial ordering, fuzzy matching algorithms).

5. **Read the UI components** — the page and review component. Note the data flow: how extracted data travels from API → UI state → submit. Pay special attention to validation UX, error states, partial submission, and dormant features (like hidden reprocess buttons).

6. **Synthesize into a structured report:**
   - **Architecture overview** — ASCII/flow diagram showing the phases and data movement
   - **Data model** — the Booking model with field-by-field mapping from extraction → import
   - **Detailed flow** — each phase (extract → review → import) with endpoint, auth, processing logic
   - **Edge cases & business rules** — table of rules and where they're enforced (frontend vs backend vs both)
   - **Shared infrastructure** — the `src/lib/ai/` pipeline and how it's structured for reuse
   - **Dormant / hidden paths** — features that exist in code but are inaccessible from UI (like the Sonnet reprocess endpoint)
   - **Field-level mapping** — which extraction fields map to which import fields, with transformations (backfills, defaults, type coercions)

   Format: plain text or markdown. Do NOT paste raw file contents — synthesize. The report should convey the full data flow from input to persistence.

### Comparison to Full Survey

| Aspect | Full codebase survey | Targeted domain deep dive |
|--------|---------------------|--------------------------|
| Scope | Entire project | One domain/feature |
| Approach | Breadth-first (14 steps) | Depth-first (6 steps) |
| Reading pattern | Representative samples | Every file in the domain |
| Output | Project-level state summary | Domain-level architecture + data flow |
| Precondition | Project unfamiliar | Already worked on this project |

## When NOT to Use (Full Survey)

- The project is trivial (< 20 files) — skip straight to reading the files
- You're already mid-session and the user names a specific file to edit — just read that file
- The user wants a narrow answer like "where is X defined" — use grep or the knowledge graph instead

## Workflow

Run these steps in order. At each step, **synthesize** what you found before moving on. The final output is a cohesive report, not a concatenation of individual file reads.

### 1. Establish repository state

```bash
git branch -a
git log --oneline -20
```

Look for:
- Active branch (likely where work happens)
- Branch topology (feature branches, main/staging/development flow)
- Recent commit activity and commit message patterns
- Whether the working tree is clean or has uncommitted changes

**Goal:** Understand the project's cadence and current position in the commit graph.

### 2. Top-level structure and scale

```bash
ls -la
find src -type f | head -60
echo "---TOTAL---" && find src -type f | wc -l
```

Break down by major directory:
- App routes/pages
- Components
- Library/utils
- Tests
- Config files
- Documentation

**Goal:** Know how big the codebase is and where the files live.

### 3. Package manifest and README

Read `package.json` (or equivalent) and `README.md`.

Capture:
- Framework and major dependencies
- Build/dev/test commands
- Project purpose and live URL (if any)
- Environment setup instructions

**Goal:** Confirm tech stack and entry points.

### 4. Database schema (if ORM/schema file exists)

Read the schema definition (e.g., `prisma/schema.prisma`, `schema.sql`, `models.py`).

Produce a table summary:

| Table | Purpose | Key relationships |

Note soft-delete conventions, multi-tenancy fields, and any unusual patterns.

**Goal:** Understand the data model and how entities relate.

### 5. Core documentation files

Read the project's contract docs — typically `technical-documentation.md`, `functional-specifications.md`, `implementation-plan.md`. Read only if they exist and are reasonably sized (< ~600 lines each). For very large docs, read the table of contents and the "Today's state" or "Status" sections.

Capture:
- Architecture decisions
- Role/permission model
- Feature completion status
- Known debt or deferred work

**Goal:** Understand what the system is supposed to do and what's already built.

### 6. Access control model

Review the project's access control architecture — focusing on *what* is protected, not the specific secret values.

Capture:
- Auth strategy (JWT, session, OAuth) — from import/type files, not credential files
- Role model and how roles are enforced (middleware, decorators, guards on routes)
- Protected vs public route patterns
- Middleware redirects and guards

**Do NOT read files containing actual secrets** (credential files, `.env`, `CLAUDE.local.md`, API key configs, JWT secret values, OAuth client secrets, etc.). Read only:
- Route middleware files (which check auth, not the auth config itself)
- Type/interface files for auth models
- The Prisma schema's User/Account/Session models
- Route handler files to see guard patterns

The goal is understanding *who can access what*, not finding credential values.

### 7. Key library files

Read 3–5 of the most consequential utility files:
- Database client singleton + soft-delete middleware
- Auth middleware (route guards, not credential config)
- Cache layer
- Feature flags / agency scope

**Do NOT read:** files containing actual credential values, API keys, encryption secrets, or password hashes. Read the interface types and middleware patterns only.

**Goal:** Understand the platform's shared infrastructure and guardrails.

### 8. Directory tree depth check

```bash
find src/app -type d | sort       # or pages/, routes/, controllers/
```

Map the routing structure. Note nested routes, parallel routes, route groups.

**Goal:** Visualize the URL surface and page hierarchy.

### 9. Component and API inventory

Count files per category:

```bash
find src/components -type f | wc -l
find src/app/api -type f | wc -l
find src/lib -type f | wc -l
```

Read a representative sample (1–2 files) from each major component area if the user hasn't specified a focus area.

**Goal:** Know where UI components and API routes live.

### 10. Tests and scripts

List test files and utility scripts.

```bash
find tests -type f | sort
find scripts -type f | sort
```

Note test quantity, framework, and coverage. Note any data migration/import scripts.

**Goal:** Understand test infrastructure and one-off tooling.

### 11. Deployment and environment

Read deployment docs or CI config. Note:
- Hosting platform
- Branch → environment mapping
- How environment variables are managed
- Database migration strategy

**Goal:** Know how the project ships.

### 12. Synthesize the report

Produce a structured summary covering:

1. **Project identity** — name, purpose, live URL, repo
2. **Tech stack** — concise bullet list
3. **Scale** — total file count, test count, schema line count
4. **Data model** — table count + notable relationships
5. **Key engineering decisions** — architecture patterns worth highlighting
6. **Features implemented** — what's complete
7. **Testing & quality** — test count, frameworks, coverage posture
8. **Deployment** — environments, branch flow
9. **Current state** — recent activity, active plans, known debt
10. **Notable code patterns** — idioms that show up repeatedly
11. **Maintainability assessment** — file size distribution, separation of concerns, coupling analysis (see below)

Use plain text or markdown. Do NOT paste raw file contents unless quoting a specific pattern. The report should be readable by a human in 2–3 minutes.

#### Maintainability assessment (new)

After the standard synthesis, add a **maintainability section** that surfaces structural risks before they become blockers:

**File size audit:**
```bash
# Find the largest files (potential monoliths)
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" | xargs wc -l | sort -rn | head -20
```

Flag any file > 400 lines as a potential monolith. Flag any file > 800 lines as a definite refactor target.

**Method/class count audit:**
```bash
# Python: count methods per class
grep -c "def " app/core/allocation.py
grep -c "@router." app/api/routes.py

# JS: count functions per file
grep -c "function " app/static/js/charts.js
```

Flag any class with > 15 methods or any file with > 30 functions as violating single-responsibility.

**Coupling signals to check:**
- Does one class handle > 3 unrelated feature domains? (e.g., portfolio views + risk analysis + workforce + trends all in one processor)
- Does the frontend have one function per API endpoint, or is there a registry/dispatch pattern?
- Are chart rendering concerns duplicated between live dashboard and export formats?
- Is there a shared type/schema between backend and frontend, or do they maintain separate contracts?

**Maintainability verdict:**
| Grade | Criteria |
|-------|----------|
| A | Files < 300 lines, clear separation, shared types, registry patterns |
| B | Some files 300-500 lines, minor duplication, mostly clean boundaries |
| C | Several files 500-800 lines, noticeable duplication, fuzzy boundaries |
| D | Multiple files > 800 lines, heavy duplication, no clear separation |
| F | Monolithic files > 1200 lines, everything coupled, changes require touching 4+ files |

Include specific refactor recommendations: "Split AllocationProcessor into Portfolio/Risk/Workforce/Project/People/Trend processors" or "Consolidate 45 loadChart() functions into a chart registry."

**Why this matters:** The user often asks "what can you tell me about the app?" or "is there a better tech stack?" after a survey. The maintainability assessment gives them the vocabulary and evidence to make that decision, rather than leaving it as an open-ended question.

### 13. Assess project maturity and velocity

After reading the codebase, produce a **complexity assessment** — not just file counts. Answer:

- **How long did this take to build?** Compare scope against the user's known velocity. If they've built similar things before, use that as a baseline for scope estimates rather than generic industry averages.
- **What does the architecture reveal about domain expertise?** Edge types that serve specific advisor query patterns, pipeline optimizations that reflect years of domain knowledge (port tiering by traffic with 85% page-load reduction, dual-emit structured extraction, season-mode distinction in T7 prompts) — these are not accidental. Note them as domain-compression signals.
- **What's the actual complexity driver?** A project with 50 tables but straightforward CRUD is less complex than a project with 16 tables but multi-environment replication, knowledge graph sync, and distributed pipeline orchestration. Complexity is in the *interactions*, not the entity count.
- **Could a team replicate this timeline?** Be honest. If the architecture embeds years of domain knowledge that a team would need to learn, say so. The user's output is not a benchmark for standard team velocity — it's a different throughput model entirely (zero handoffs, zero meetings, domain-compressed decision-making).

**Goal:** The survey should convey *what kind of project this is*, not just what it contains.

### 14. Synthesize user context for future readers

After the report, add a brief operating-context note that any future session will benefit from:

- Everything in this project's methodology is a compression mechanism: plans, recaps, contract docs, skills, local env files — all designed to eliminate context re-discovery.
- Communication should be action-first. Read everything before suggesting anything. Own errors immediately.
- This is a live production product with real customers. Uptime is non-negotiable.

**Goal:** Any future agent that reads this survey report understands who the user is and how they operate, not just what the code contains.

## Granularity Rules

- **Stop at the right level of detail.** For a 50-file project, read most files. For a 500-file project, read representative samples and summarize the rest by category.
- **Don't read every file.** The goal is understanding, not comprehensive indexing. Use the knowledge graph or grep for drill-downs on specific areas.
- **Synthesize as you go.** Don't accumulate 20 file reads and dump them all at the end. Each section should feed the synthesis.
- **Surface the project's own docs, don't replace them.** The survey points TO the feature docs; it doesn't absorb them.

## Common Pitfalls

1. **Raw catalogue dump.** Listing every file in `src/components/` is not a survey — it's a directory listing. Group by function and summarize.
2. **Reading files the project doesn't have.** If there's no `README.md`, note it and move on. Don't fabricate.
3. **Getting lost in one file.** If a file is huge (> 400 lines), read the first 100 and the last 50, or scan for exported functions. The survey is breadth-first, not depth-first.
4. **Ignoring git history.** The commit log tells you what the team actually values (feature commits vs. fix commits vs. doc commits). Use it.
5. **Forgetting environment discipline.** If the project has staging/production credentials in a gitignored file, reference the env var names only — never read or include actual secret values in the synthesized report.
6. **Stopping at "what" instead of "how maintainable."** A survey that only lists files and endpoints misses the user's real question: "can I work with this?" Always include the maintainability assessment (file size audit, coupling analysis, grade) so the user has actionable intelligence, not just a catalogue.
7. **Confusing targeted deep dive with full survey.** When the user asks for a "deep dive of X" in an already-familiar project, do NOT run the full 14-step codebase survey. That wastes time reading areas they already know. Use the targeted domain deep dive pattern instead (6 steps, depth-first into one area).
8. **Confusing targeted deep dive with lightweight warmup.** The `project-warmup` skill's lightweight mode handles "answer a question by reading one doc." A deep dive requires reading ALL source files (routes, pipeline, schema, UI) under the domain. The separation line: if you can answer from one doc file, it's lightweight warmup. If you need to read multiple implementation files + the feature doc, it's a targeted deep dive. When in doubt, lean toward deep dive — reading extra files costs minutes, piecing together incomplete context costs the user's time.

## References

- `references/codebase-survey-checklist.md` — ordered checklist for running a full codebase survey (breadth-first, 12 phases)
- `references/targeted-deep-dive-checklist.md` — checklist for doing a targeted deep dive into one domain/feature (depth-first, 6 steps). Use when the user asks for a "deep dive of X" in an already-familiar project.