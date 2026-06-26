# Architecture Decision Records (ADR) — For Greenfield (0-1) Projects

When building from scratch, the engineer must make and document foundational architecture decisions before producing the Implementation Plan. This template captures those decisions with rationale so the PM and future team members understand why the stack and structure were chosen.

---

## When to Use This Template

- Any project that starts from zero (no existing codebase)
- Any project that requires a major architectural shift (e.g., replatforming from monolith to microservices)
- Any time the PM asks "why this stack/approach?"

For projects that modify an existing codebase, you do not need an ADR — the architecture is inherited. Note any architecture concerns in the Software Audit instead.

## ADR Document Format

Produce one ADR per project, covering all foundational decisions:

```
# Architecture Decision Record
Project: [Project Name]
Date: [date]
Status: Proposed | Accepted by PM | Superseded by [ADR reference]
```

### ADR-001: Technology Stack

```
Decision: [What stack was chosen]

Frontend: [framework + version]
  Rationale: [why this framework — project requirements, team familiarity, ecosystem, performance]
  Alternatives Considered: [what else was evaluated and why it was rejected]

Backend: [language + framework + version]
  Rationale: [why]
  Alternatives Considered: [what else and why not]

Database: [engine + version]
  Rationale: [why — data model needs, query patterns, scaling expectations]
  Alternatives Considered: [what else and why not]

Infrastructure: [hosting, CI/CD — if determined at this stage]
  Rationale: [why]
```

### ADR-002: Application Architecture Pattern

```
Decision: [Monolith | Microservices | Serverless | Modular Monolith | etc.]

Rationale:
  - [reason 1 — e.g., project scope, team size, deployment complexity]
  - [reason 2]

Trade-offs:
  - Pros: [what this pattern gives us]
  - Cons: [what we give up or accept as risk]

Migration Path: [if starting monolith, note when/how to split if scale demands it]
```

### ADR-003: API Paradigm

```
Decision: [REST | GraphQL | gRPC | tRPC | etc.]

Default: REST unless project requirements dictate otherwise.

Rationale:
  - [why this paradigm fits the project]

Conventions:
  - URL structure: /api/v[N]/[resource]
  - Versioning strategy: [URL versioning, header versioning]
  - Pagination: [offset-based, cursor-based]
  - Filtering: [query params convention]
  - Response envelope: [if using one — e.g., { data: {}, meta: {} }]
```

### ADR-004: Data Model Approach

```
Decision: [Relational (normalized) | Document-based | Hybrid]

Default: Relational (normalized) unless project requirements dictate otherwise.

Rationale:
  - [why — data relationships, query patterns, consistency requirements]

Key Entities: [high-level list of primary entities and their relationships]
  - [Entity A] 1:N [Entity B]
  - [Entity B] N:M [Entity C] (via junction table)
```

### ADR-005: Folder Structure

```
Decision: [describe the directory layout]

Example:
  /src
    /controllers    — HTTP request handlers
    /services       — Business logic
    /models         — Data models / entities
    /middleware      — Auth, validation, error handling
    /routes         — Route definitions
    /utils          — Shared utilities
    /config         — Environment and app configuration
    /migrations     — Database migrations
    /tests          — Test files mirroring src structure

Rationale: [why this structure — separation of concerns, convention for the framework, scalability]
```

### ADR-006: Authentication Strategy

```
Decision: [JWT stateless | Session-based | OAuth2 | Auth provider (Auth0, Clerk, etc.)]

Rationale:
  - [why this approach]
  - [token storage strategy — httpOnly cookie, localStorage (with XSS caveat), etc.]
  - [refresh token strategy if applicable]

Trade-offs:
  - [what this gives us vs. what we accept]
```

## Defaults

When project requirements don't specify a preference, the engineer uses these defaults and notes them in the ADR:

- **API:** REST with JSON
- **Database:** Relational (PostgreSQL preferred)
- **Architecture:** Monolith (modular)
- **Auth:** JWT with httpOnly cookie storage
- **Folder structure:** Standard MVC / service-layer pattern for the chosen framework
- **Naming:** snake_case for DB columns, camelCase for API request/response fields, PascalCase for components

Any deviation from defaults requires explicit rationale in the ADR.

## PM Review

The ADR is submitted to the PM for review before the full Implementation Plan is produced. The PM may share the ADR with the client for awareness. Write the "Rationale" sections so a non-technical stakeholder can understand the reasoning even if they skip the technical details.

If the PM or client pushes back on a decision, the engineer addresses the concern with technical justification. If the concern is valid, update the ADR and adjust the approach. The engineer has technical authority but the PM has project authority — if there's a genuine business reason to override a technical preference, document the trade-off and proceed.
