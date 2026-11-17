---
name: fswe
description: Full-stack engineering skill with 24 modules covering architecture, API, performance, testing, DevOps, security, and modern TypeScript stack.
version: 2.0.0
user-invocable: true
homepage: https://clawhub.ai/khamalismadie/fswe
metadata: {"openclaw":{"emoji":"🏗️","os":["linux","darwin","win32"]}}
---

# Full-Stack Web Engineer 🏗️

24 engineering modules. TypeScript-first. Production-ready.

## Auto-Select

Route to the right module based on input:

| Input Keywords | Module |
|----------------|--------|
| api, rest, endpoint, controller | api-development |
| grpc, protobuf, rpc | http-grpc |
| docker, container, compose | docker-containers |
| ci, deploy, pipeline, github actions | ci-cd-pipelines |
| security, auth, jwt, oauth | security-auth |
| test, jest, vitest, coverage | testing-fundamentals |
| perf, cache, slow, optimize | performance |
| vue, composition, pinia | vue3-modernization |
| migrate, legacy, php, strangler | legacy-migration |
| db, sql, schema, index, migration | sql-database |
| monitor, log, alert, observability | monitoring-observability |
| graphql, gql, resolver | graphql-api |
| websocket, realtime, sse | websocket-realtime |
| state, store, pinia, vuex | state-management |
| microservice, service, boundary | system-design |
| bun, typescript, runtime | bun-typescript |
| retry, circuit breaker, fault | fault-tolerance |
| feature flag, rollout, kill switch | feature-flags |
| code review, pr, quality | code-quality |
| debug, rca, production | debugging |
| sprint, agile, scrum, story | scrum-agile |
| cross-team, stakeholder, spec | cross-functional |
| ownership, delivery, release | feature-ownership |
| async, promise, concurrency | concurrency-async |

## Parameters

| Parameter | Type | Required | Default | Options | Description |
|-----------|------|----------|---------|---------|-------------|
| module | string | yes | — | (see auto-select) | Target module name |
| language | string | no | en | en, id | Output language |
| depth | string | no | standard | quick, standard, deep | Detail level |
| stack | string | no | bun | bun, node, deno | Runtime target |
| database | string | no | postgres | postgres, mysql, sqlite, redis, mongodb | Database type |
| framework | string | no | vue3 | vue3, react, next, nuxt | Frontend framework |
| output | string | no | markdown | markdown, code, checklist, both | Output format |

## Module Index

### Architecture
- `system-design` — Monolith vs microservices, service boundaries, CQRS
- `bun-typescript` — Bun runtime, TypeScript backend, FFI

### API & Networks
- `api-development` — REST, controllers, validation, auth, error handling
- `http-grpc` — HTTP/gRPC protocols, versioning, idempotency
- `graphql-api` — Schema design, resolvers, N+1, subscriptions
- `websocket-realtime` — WebSocket, SSE, pub/sub, connection management

### Frontend
- `vue3-modernization` — Composition API, Pinia, script setup
- `state-management` — Pinia, Vuex migration, reactive patterns

### Performance & Resilience
- `performance` — Profiling, caching, lazy loading, bundle optimization
- `fault-tolerance` — Retry, circuit breaker, bulkhead, graceful degradation
- `concurrency-async` — Event loop, promises, workers, race conditions

### Data
- `sql-database` — Schema design, indexing, migrations, query optimization

### Operations
- `monitoring-observability` — Logging, metrics, tracing, alerting
- `feature-flags` — Progressive delivery, A/B testing, kill switches
- `docker-containers` — Docker, compose, multi-stage builds, health checks
- `ci-cd-pipelines` — GitHub Actions, GitLab CI, deployment strategies

### Security
- `security-auth` — OWASP, JWT, OAuth2, rate limiting, input validation

### Quality
- `testing-fundamentals` — Unit, integration, contract, E2E testing
- `code-quality` — Clean code, PR standards, refactoring patterns
- `debugging` — Cross-layer debugging, production RCA

### Delivery
- `scrum-agile` — Sprint planning, story breakdown, estimation
- `cross-functional` — Tech specs, stakeholder communication
- `feature-ownership` — End-to-end delivery, release management

## Standards

All code: clear, concise, performant, tested, observable, maintainable, backward-compatible.

## Principles

1. Type safety first — no `any`
2. Fail fast — validate early, crash loudly
3. Readability > cleverness
4. Explicit > implicit
5. Design for change
6. Ship safely — feature flags, gradual rollout
7. Document decisions — ADR for architecture choices

## Usage

1. Identify problem → auto-select module or specify `module` param
2. Load `references/<module>/SKILL.md`
3. Apply checklist
4. Validate against standards
