# CLAUDE.md — {Project Name}

## Project Overview
<!-- One paragraph: what is this project, who is it for -->

## Architecture
<!-- From Design Brief: key modules, data flow, dependencies -->

## ⛔ Hard Constraints (violate = reject)

- All API responses MUST conform to `contracts/api-spec.yaml`
- Shared types MUST be imported from `contracts/shared-types.ts` — no local redefinitions
- Error codes MUST use codes defined in `contracts/errors.yaml`
- Database migrations MUST be reversible
- No business logic in controller layer (controller → service → repository)
- No hardcoded environment variable values
- No `any` type (TypeScript) / equivalent escape hatches without justification

## 📋 Code Standards

### Naming Conventions
- Files: kebab-case
- Functions/variables: camelCase (TS/JS) / snake_case (Python/Go)
- Database fields: snake_case
- Constants: UPPER_SNAKE_CASE

### Directory Structure
<!-- Project-specific directory layout and responsibilities -->

### Import Order
1. Standard library
2. Third-party packages
3. Internal packages
4. Relative imports

### Comments
- Public APIs MUST have JSDoc/docstring
- Complex logic MUST have inline explanation
- No commented-out code in commits

### Error Handling
- Use typed errors, not generic strings
- Always include context in error messages
- Log errors at the boundary, not deep in the stack

### Logging
- Structured logging (JSON)
- MUST include `requestId` in all request-scoped logs
- Levels: debug/info/warn/error (no console.log in production code)

## 🧪 Testing Requirements

- New APIs MUST have contract tests
- Business logic MUST have unit tests
- Modifying existing APIs MUST update contracts + related tests
- Coverage floor: core modules > 80%

## 📁 Project Structure
<!-- Current directory layout with per-directory responsibility notes -->

```
src/
├── controllers/    # HTTP handlers — thin, delegates to services
├── services/       # Business logic
├── repositories/   # Data access layer
├── middleware/      # Express/Koa middleware
├── utils/          # Pure utility functions
└── types/          # TypeScript type definitions
```

## 🔗 Dependencies & Contracts

- API Contract: `contracts/api-spec.yaml`
- Shared Types: `contracts/shared-types.ts`
- Error Codes: `contracts/errors.yaml`

## 🐛 Known Issues & Gaps
<!-- Auto-synced from Gap Registry -->

## 📝 Recent Decisions
<!-- Last 5 design decisions for historical context -->

## 🎨 Code Style

<!-- Add language-specific authority style guides here -->
<!-- Examples:
- Go → Effective Go, Go Code Review Comments
- Rust → Rust API Guidelines
- TypeScript → typescript-eslint recommended
- Python → PEP 8, Google Python Style Guide
-->
