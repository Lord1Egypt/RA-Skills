---
name: codebase-onboarder
description: AI-powered codebase analysis — generate architecture docs, onboarding guides, and key-flow walkthroughs for any project. Use when joining a new codebase, onboarding a team member, or documenting an undocumented project.
---

# Codebase Onboarder

Analyze any codebase and produce a structured onboarding guide. Covers architecture, key flows, patterns, dependencies, entry points, and gotchas — the things that take weeks to figure out by reading code.

Use when: someone says "help me understand this codebase", "onboard me", "document this project", or "what does this repo do".

## Analysis Steps

Run these in order. Each step informs the next.

### 1. Project Identity

```bash
# What is this?
cat README.md 2>/dev/null || cat readme.md 2>/dev/null
cat package.json 2>/dev/null | jq '{name, description, scripts}'
cat pyproject.toml 2>/dev/null | head -30
cat Cargo.toml 2>/dev/null | head -20
cat go.mod 2>/dev/null | head -10
cat Makefile 2>/dev/null | head -40
```

Determine: language, framework, purpose, build system.

### 2. Project Structure

```bash
# Directory tree (depth 3, ignore noise)
find . -maxdepth 3 -type d \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/vendor/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/.next/*' \
  -not -path '*/target/*' \
  | head -80

# Count files by extension
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15
```

Map the architecture: where does business logic live, where are configs, where are tests, what's the convention.

### 3. Entry Points

```bash
# Web apps
grep -rl "listen\|createServer\|app\.run\|uvicorn\|Flask(__name__)" --include="*.{js,ts,py,go,rb}" . 2>/dev/null | head -10

# CLI tools
grep -rl "if __name__\|func main\|fn main\|bin.*:" --include="*.{py,go,rs,json}" . 2>/dev/null | head -10

# Config-declared entry points
cat package.json 2>/dev/null | jq '.main, .bin, .scripts.start, .scripts.dev'
cat pyproject.toml 2>/dev/null | grep -A5 'scripts\|entry_points'
```

Identify: where does execution start, what are the main scripts/commands, how do you run it locally.

### 4. Dependencies & Stack

```bash
# Key dependencies (not all — just the important ones)
cat package.json 2>/dev/null | jq '.dependencies | keys' | head -20
cat requirements.txt 2>/dev/null | head -20
cat go.mod 2>/dev/null | grep -v '//' | tail -20
cat Cargo.toml 2>/dev/null | grep -A50 '\[dependencies\]' | head -30
```

Identify: database (postgres, mongo, redis), framework (express, fastapi, gin), ORM, auth, queue, cloud SDKs. These define the project's personality.

### 5. Data Layer

```bash
# Database schemas, migrations, models
find . -type f \( -name "*.sql" -o -name "*migration*" -o -name "*schema*" -o -name "*model*" \) \
  -not -path '*/node_modules/*' 2>/dev/null | head -20

# ORM models
grep -rl "class.*Model\|@Entity\|schema\.\|CREATE TABLE\|db\.Column" \
  --include="*.{py,ts,js,go,rb,java}" . 2>/dev/null | head -10
```

Map: what are the core data entities, how are they related, where do migrations live.

### 6. API Surface

```bash
# REST routes
grep -rn "app\.\(get\|post\|put\|delete\|patch\)\|@app\.route\|router\.\(get\|post\)\|@Get\|@Post\|@Controller" \
  --include="*.{ts,js,py,go,rb,java}" . 2>/dev/null | head -30

# GraphQL
find . -name "*.graphql" -o -name "*.gql" -o -name "*schema*" -name "*.graphql" 2>/dev/null | head -10
grep -rl "type Query\|type Mutation\|@Query\|@Mutation" --include="*.{ts,js,py,go}" . 2>/dev/null | head -10
```

List the key endpoints/operations, grouped by domain.

### 7. Config & Environment

```bash
# Environment variables
cat .env.example 2>/dev/null || cat .env.sample 2>/dev/null || cat .env.template 2>/dev/null
grep -rh "process\.env\.\|os\.environ\|os\.getenv\|env::\|std::env" \
  --include="*.{ts,js,py,go,rs,rb}" . 2>/dev/null | sort -u | head -30
```

Document: what env vars are needed, which are secrets, what services need to be running.

### 8. Testing

```bash
# Test structure
find . -type f \( -name "*test*" -o -name "*spec*" -o -name "*_test.*" \) \
  -not -path '*/node_modules/*' 2>/dev/null | head -20

# How to run tests
cat package.json 2>/dev/null | jq '.scripts.test'
grep -r "pytest\|jest\|mocha\|vitest\|go test\|cargo test" Makefile* 2>/dev/null
```

### 9. CI/CD & Deployment

```bash
ls -la .github/workflows/ 2>/dev/null
ls -la .gitlab-ci.yml 2>/dev/null
cat Dockerfile 2>/dev/null | head -20
cat docker-compose.yml 2>/dev/null | head -30
ls -la k8s/ kubernetes/ helm/ 2>/dev/null
```

## Output Template

After analysis, produce a document with these sections:

```markdown
# [Project Name] — Onboarding Guide

## What This Is
One paragraph: what it does, who it's for, what problem it solves.

## Tech Stack
- Language: X
- Framework: X
- Database: X
- Key dependencies: X, Y, Z

## Architecture
Describe the high-level architecture in 3-5 sentences. Include a simple diagram if helpful:
- Monolith / microservices / serverless
- Request flow: client → API → service → database
- Key patterns: MVC, event-driven, CQRS, etc.

## Directory Map
| Path | Purpose |
|------|---------|
| src/api/ | REST endpoints |
| src/services/ | Business logic |
| src/models/ | Database models |
| ... | ... |

## Key Flows
Walk through 2-3 critical user journeys:
1. **User signup** — POST /auth/register → validate → hash password → insert user → send email → return token
2. **Place order** — POST /orders → check inventory → charge payment → create order → notify warehouse

## Getting Started
Step-by-step: clone, install, configure env, seed database, run locally.

## Gotchas
Things that are non-obvious, surprising, or likely to trip someone up:
- "The auth middleware silently returns 200 on missing tokens (legacy behavior)"
- "Tests require a running Redis instance on port 6380 (not default)"
- "The migration in 0042 takes 20 minutes on large datasets"

## Where to Look
| I want to... | Look at... |
|--------------|-----------|
| Add an API endpoint | src/api/routes/ |
| Change the database schema | src/models/ + migrations/ |
| Debug auth issues | src/middleware/auth.ts |
| Understand the build | Makefile + .github/workflows/ |
```

## Tips

- Read tests first — they document behavior better than comments
- Check git log for the most-changed files — those are the hot paths
- Look at recent PRs for coding conventions and review standards
- If something is confusing, it's a gotcha worth documenting
