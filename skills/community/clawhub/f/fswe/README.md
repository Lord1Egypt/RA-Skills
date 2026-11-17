# Full-Stack Web Engineer 🏗️

Full-stack engineering skill with **24 modules** covering architecture, API, performance, testing, DevOps, security, and modern TypeScript stack.

## What's Inside

| Category | Modules |
|----------|---------|
| Architecture | system-design, bun-typescript |
| API & Networks | api-development, http-grpc, graphql-api, websocket-realtime |
| Frontend | vue3-modernization, state-management |
| Performance | performance, fault-tolerance, concurrency-async |
| Data | sql-database |
| Operations | monitoring-observability, feature-flags, docker-containers, ci-cd-pipelines |
| Security | security-auth |
| Quality | testing-fundamentals, code-quality, debugging |
| Delivery | scrum-agile, cross-functional, feature-ownership |

## Parameters

| Parameter | Default | Options | Description |
|-----------|---------|---------|-------------|
| module | — | (24 modules) | Target module |
| language | en | en, id | Output language |
| depth | standard | quick, standard, deep | Detail level |
| stack | bun | bun, node, deno | Runtime |
| database | postgres | postgres, mysql, sqlite, redis, mongodb | Database |
| framework | vue3 | vue3, react, next, nuxt | Frontend framework |
| output | markdown | markdown, code, checklist, both | Output format |

## Auto-Select

The skill automatically routes to the right module based on your input keywords. See SKILL.md for full routing table.

## Installation

```bash
openclaw skills install @khamalismadie/fswe
```

## Usage

```
Load fswe module: api-development
Load fswe module: performance with depth=deep
Load fswe module: sql-database with database=postgres
```

## What's New in v2.0.0

- 6 new modules: docker-containers, ci-cd-pipelines, security-auth, graphql-api, websocket-realtime, state-management
- Auto-select routing by keyword
- Complete parameter schemas per module
- English-only (cleaned up mixed language)
- Proper YAML frontmatter

## Links

- [ClawHub](https://clawhub.ai/khamalismadie/fswe)
- [Publisher](https://clawhub.ai/user/khamalismadie)
