# Codebase Survey — Step-by-Step Checklist

Use this as a checklist while running a survey. Copy into scratch space and tick each box before moving on.

## Phase 1: Repository State
- [ ] `git branch -a` — active branch and topology
- [ ] `git log --oneline -20` — recent activity + commit patterns
- [ ] Note: clean working tree or uncommitted changes?

## Phase 2: Top-Level Structure
- [ ] `ls -la` — root files and config
- [ ] Directory listing of major source dirs
- [ ] Source file counts by category (app, components, lib, tests)

## Phase 3: Manifest and README
- [ ] `package.json` / equivalent → framework + dependencies
- [ ] `README.md` → purpose, setup, commands, live URL
- [ ] `.env.example` → required env vars surfaced

## Phase 4: Database Schema
- [ ] Schema definition file (Prisma, SQL, ORM model file)
- [ ] Table count + relationship summary
- [ ] Soft-delete convention noted
- [ ] Multi-tenancy or scoping fields identified

## Phase 5: Core Documentation
- [ ] `docs/technical-documentation.md` or equivalent → architecture, decisions
- [ ] `docs/functional-specifications.md` or equivalent → features, roles, rules
- [ ] `docs/implementation-plan.md` or equivalent → phases, acceptance criteria
- [ ] Active plans identified (grep `^status: active`)

## Phase 6: Access Control Model
- [ ] Auth strategy identified from types/interfaces (not credential files)
- [ ] Role model + enforcement mechanism captured from route guards/middleware
- [ ] Protected vs public route patterns documented
- [ ] **No secret files read** — credential configs, .env, and API key files explicitly skipped

## Phase 7: Key Library Files
- [ ] DB client singleton + soft-delete or transaction helpers
- [ ] Auth middleware (not config — just how auth is checked on routes)
- [ ] Cache or shared infra layer
- [ ] Feature flags / tenant scoping
- [ ] **Avoid: credential configs, API key files, env var value files**

## Phase 8: Routing Structure
- [ ] `find src/app -type d` or equivalent → route tree
- [ ] Note route groups, parallel routes, dynamic segments

## Phase 9: Component and API Inventory
- [ ] Component directory structure and counts
- [ ] API route directory structure and counts
- [ ] Representative component file(s) sampled
- [ ] Representative API route file(s) sampled

## Phase 10: Tests and Scripts
- [ ] Test files listed by framework (unit, integration, E2E)
- [ ] Test count and coverage quality noted
- [ ] Utility / migration / seed scripts listed

## Phase 11: Deployment and Environment
- [ ] Hosting platform noted
- [ ] Branch → environment mapping
- [ ] Environment variable management
- [ ] Migration / CI strategy

## Phase 12: Synthesis
- [ ] Report covers: identity, stack, scale, data model, architecture decisions
- [ ] Report covers: features complete, testing, deployment, current state, patterns
- [ ] Plain text or markdown format used (no raw file dumps unless quoting)
