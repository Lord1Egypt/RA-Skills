# SDLC Phases — Detailed Checklists

This file expands each SDLC phase with the concrete questions and artifacts that should exist before you move to the next one. Use it as a checklist, not a script.

## 1. Requirements Analysis

### Functional requirements
- What are the 3–7 core user-facing capabilities? Write them as user stories: "As a [role], I can [action] so that [outcome]."
- What are the explicit non-goals? Write them down — they're the first thing to cite when scope creeps.
- What's the shortest possible path to a demo? That's your MVP.

### Non-functional requirements
- **Users & load**: expected DAU/MAU, peak concurrent users, requests/sec
- **Latency**: acceptable p50, p95, p99 response times
- **Data**: record counts, growth rate, retention, PII/sensitive data flags
- **Availability**: is 99% fine, or is this a payments system that needs 99.99%?
- **Compliance**: GDPR (EU users), HIPAA (health), PCI (cards), SOC 2 (enterprise B2B)
- **Accessibility**: WCAG 2.1 AA is the default for anything public-facing
- **Browsers/devices**: modern evergreen only, or IE11, or mobile-first?

### Clarifying questions to ask when requirements are vague
- "Who is the primary user, and what's their technical comfort level?"
- "Does this need auth? If yes, public signup or invite-only?"
- "Is there existing data this needs to import from, or does it start empty?"
- "Where will this be deployed, and who's paying for hosting?"
- "What's the one thing that, if missing at launch, would make this not worth shipping?"

### Output artifact
A short `REQUIREMENTS.md` or a bulleted section in the chat with: goals, non-goals, users, key flows, constraints. 10–30 lines is usually right.

## 2. Planning

### Scope slicing
- Write an MVP list — features that MUST ship for v1 to be useful.
- Write a "v1.1" list — things you'd add immediately after.
- Write a "someday" list — everything else. This list is where good ideas go to wait.

### Milestones as vertical slices
Order milestones so each one is independently runnable. Bad: "build the whole database, then the whole API, then the whole frontend." Good: "get a single entity (User) creatable from UI → API → DB, then add the next."

### Risk register
List risks and what you'd do about each:
- **Third-party dependencies** (Stripe, OpenAI, Twilio): what if they're down or change their API?
- **Novel tech**: are you using something you've never used before? Prototype the risky bit first.
- **Unclear requirements**: call these out explicitly — "we're guessing about X, need confirmation before wiring Y"
- **Performance assumptions**: load-test the riskiest path before building around it

### Tech stack decision
Pick now. One line per choice justifying it. See the stack table in `SKILL.md`. Avoid decision paralysis — you can swap a library later; you can't swap a framework later without a rewrite. So spend time on the framework choice and move fast on everything else.

## 3. Design & Architecture

### Data model
- List entities (User, Post, Order, etc.)
- List relationships (1:1, 1:N, N:M)
- List key fields per entity with types
- Identify indexes you'll need based on query patterns
- Identify soft-delete, audit, timestamp columns — adding these later is painful

For SQL: draft `CREATE TABLE` statements.
For NoSQL: draft document shapes AND the access patterns they support (DynamoDB in particular is access-pattern-driven).

### API surface
- REST: list endpoints with method, path, request body, response body, status codes.
- GraphQL: draft the schema (types, queries, mutations).
- Identify which endpoints need auth and what roles.

### Frontend architecture
- List pages/routes.
- Identify shared components (navigation, forms, modals, tables).
- Decide state boundaries: server state (React Query/SWR), global UI state (Zustand/Redux/Context), form state (React Hook Form).
- Decide rendering strategy per page: SSR, SSG, CSR, ISR.

### Infrastructure sketch
Draw the request flow. Even ASCII is fine:

```
[Browser] --> [CDN/Vercel] --> [Next.js app]
                                    |
                                    +--> [Postgres]
                                    +--> [S3 / object storage]
                                    +--> [Stripe API]
                                    +--> [SendGrid API]
```

Identify the trust boundaries — every arrow crossing a boundary is a place that needs auth, validation, and error handling.

### Directory layout
Show the full tree before creating files. Fix it now — renaming directories later is a chore.

### Output artifact
A `DESIGN.md` or a design section with: data model, API list, component tree, infra diagram, directory tree.

## 4. Implementation

See `SKILL.md` for the vertical-slice order. Additional guidance:

### Version control hygiene
- One commit per logical change, with a clear message.
- Never commit `.env`, `node_modules`, build artifacts, or credentials.
- Add a `.gitignore` on day one.

### Code organization
- **Routes / controllers**: thin — parse input, call a service, return a response.
- **Services**: business logic. The thing you'd unit-test.
- **Repositories / models**: database access. Replaceable.
- **Utilities / lib**: pure functions shared across features.

This separation pays off around 2,000 lines, not before. Don't prematurely abstract a 200-line project.

### Config & environment
- `.env` for local secrets (git-ignored)
- `.env.example` committed, documenting every required variable
- Config validation on boot — the app should fail fast if a required env var is missing, not 20 minutes later when that code path runs

### Error handling
- At the API boundary: catch exceptions, return structured error JSON, log the full trace.
- Inside services: throw domain-specific errors. Don't swallow or rewrap unless you're adding context.
- On the frontend: one global error boundary, plus per-feature error states for network failures.

### README as you go
A `README.md` with prerequisites, `clone → install → env → migrate → run` steps. Update it every time the setup changes. A broken README wastes more time than a missing feature.

## 5. Testing

See `references/testing-strategies.md`.

## 6. Deployment & CI/CD

See `references/deployment-cicd.md`.

## 7. Maintenance

### Day-1 observability
- Structured JSON logs with request ID, user ID, timing.
- Error tracking (Sentry, Rollbar, or equivalent) in both frontend and backend.
- Uptime check on the health endpoint.
- Basic dashboard: request rate, error rate, p95 latency, DB connection count.

See `references/observability.md` for details.

### Operational runbook
A one-page doc covering:
- How to deploy
- How to roll back
- How to connect to production DB read-replica
- How to rotate a leaked secret
- Who to page and how
- Where to find logs, metrics, errors

### Security review before launch
Walk through `references/security-checklist.md`. Don't skip. The cost of an auth bug in prod dwarfs the 30 minutes of reviewing.

### Ongoing maintenance
- Dependency updates: Dependabot / Renovate on a weekly cadence, plus a quarterly major-version review.
- Backup verification: restore the backup to a staging DB at least quarterly. An untested backup may not be a backup.
- Tech debt tracking: keep a `TODO.md` or use issues. If something is a known compromise, write it down.
