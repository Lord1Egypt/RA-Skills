# Code Analysis Reference

Framework for auditing existing codebases and producing technical assessments. Used in Phase 1 (Software Audit) and Phase 2 (Technical Assessment).

## Software Audit Output Format

When the PM sends a Software Audit Request, return this structure:

### 1. Architecture Summary

Describe the overall system architecture in plain language:
- What framework/stack is in use
- How the application is structured (monolith, microservices, serverless, etc.)
- Key folders and their responsibilities
- How data flows from the user interface through to the database
- Any third-party integrations or external dependencies

Write this so the PM can share it with a non-technical client and they'd understand the system at a high level.

### 2. Module Breakdown

For each module/area the PM flagged:

```
Module: [module name / path]
Purpose: [what this module does in plain language]
Key Files: [list of primary files with one-line descriptions]
Current State: [healthy / needs attention / fragile]
Notes: [anything the PM or client should know]
```

### 3. Technical Debt Register

Identify and catalog technical debt:

```
TD-001: [Short description]
Location: [file(s) or module]
Severity: Low | Medium | High | Critical
Impact: [what breaks or degrades if this isn't addressed]
Recommendation: [fix now, fix during this project, defer]
```

Severity guide:
- **Critical:** Actively causing bugs or data issues. Must address before new development.
- **High:** Will cause problems when the affected area is modified. Address during this project.
- **Medium:** Code smell or suboptimal pattern. Address opportunistically.
- **Low:** Cosmetic or preference-level. Note but don't prioritize.

### 4. Security Observations

Flag anything that stands out:
- Hardcoded secrets or credentials
- Missing input validation
- Authentication/authorization gaps
- Outdated dependencies with known vulnerabilities
- Exposed debug endpoints or verbose error messages

### 5. Refactor Opportunities

Areas where restructuring would reduce complexity or risk for the upcoming work:

```
Refactor: [what to refactor]
Current: [how it works now]
Proposed: [how it should work]
Benefit: [why this matters for the project]
Effort: [rough hours]
```

### 6. Plain-Language Summary

A 3-5 paragraph summary written for the PM to share with the client. Cover: what the system does well, what needs attention, what risks exist for the planned work, and any recommendations.

---

## Technical Assessment Output Format

When the PM sends confirmed requirements for assessment, evaluate each requirement against the codebase (or against a greenfield architecture) and return:

### Per-Requirement Assessment

```
Requirement: [SRS ID] — [title]
Feasibility: Feasible | Feasible with caveats | Not feasible as written
Approach: [1-3 sentence technical approach]
Components Affected:
  - [file/module]: [what changes]
  - [file/module]: [what changes]
Effort:
  - FE: [story points] ([hours] hours)
  - BE: [story points] ([hours] hours)
  - DB: [story points] ([hours] hours)
  - QA: [story points] ([hours] hours)
Risk: Low | Medium | High
Risk Notes: [what could go wrong, what depends on external factors]
Dependencies: [other requirement IDs that must complete first]
Blockers: [anything that prevents starting this work]
```

### Story Point Scale

Use this consistent scale:
- **1 point (1-2 hours):** Trivial change. Single file, clear path, no ambiguity.
- **2 points (2-4 hours):** Small change. A few files, straightforward logic.
- **3 points (4-8 hours):** Medium change. Multiple files, some complexity, testing needed.
- **5 points (1-2 days):** Significant change. Cross-cutting, new patterns, integration work.
- **8 points (2-4 days):** Large change. New subsystem, complex business logic, multiple integration points.
- **13 points (4+ days):** Very large. Should be broken down further if possible.

If an individual requirement scores 13+, recommend to the PM that it be split into sub-requirements.

### Assessment Summary

After all per-requirement assessments, provide:
- Total effort by role (FE, BE, DB, QA) in hours and story points
- Critical path (the sequence of requirements that determines minimum timeline)
- Top 3 technical risks across all requirements
- Recommended approach order (what to build first, what can parallel)
