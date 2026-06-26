# API Design Principles

Design intuitive, scalable REST and GraphQL APIs that developers love. Covers resource modeling, HTTP semantics, pagination, error handling, versioning, and GraphQL schema patterns.

## What's Inside

- Decision Framework — REST vs GraphQL comparison
- REST API Design — resource naming rules, HTTP methods and status codes, complete status code reference
- Pagination — offset-based and cursor-based strategies
- Filtering and Sorting patterns
- Error Response Format with consistent structure
- FastAPI Implementation example with CRUD, pagination, and filtering
- GraphQL API Design — schema structure, Relay-style pagination, input/payload mutation pattern
- DataLoader for N+1 prevention
- Query Protection — depth limiting, complexity limiting, timeout
- Versioning Strategies — URL versioning, header versioning, deprecation strategy
- Rate Limiting headers and implementation
- Pre-Implementation Checklist — resources, HTTP, data, security, documentation

## When to Use

- Designing new REST or GraphQL APIs
- Reviewing API specifications before implementation
- Establishing API design standards for teams
- Refactoring APIs for better usability
- Migrating between API paradigms

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/backend/api-design-principles
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/backend/api-design-principles .cursor/skills/api-design-principles
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/backend/api-design-principles ~/.cursor/skills/api-design-principles
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/backend/api-design-principles .claude/skills/api-design-principles
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/backend/api-design-principles ~/.claude/skills/api-design-principles
```

---

Part of the [Backend](..) skill category.
