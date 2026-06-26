---
name: coding-standards
description: "Universal coding standards for TypeScript, JavaScript, React, and Node.js. Principles: readability first, KISS, DRY, YAGNI. Covers naming, type safety, error handling, async patterns, React hooks, API design, file organization, performance, testing, code smells. Trigger phrases: coding standards, best practices, code review, quality standards, naming conventions."
metadata: {"clawdbot":{"emoji":"📏","requires":{"bins":[],"env":[]},"os":["linux","darwin","win32"]}}
---

# Coding Standards & Best Practices

Universal standards for maintainable, scalable TypeScript/JavaScript code.

## Quick Start

1. **Readability First** — Clear names, self-documenting code
2. **Type Safety** — Avoid `any`, use explicit interfaces
3. **Error Handling** — Try-catch with specific error types
4. **Immutability** — Use spread operator, never direct mutation
5. **Test Structure** — AAA pattern (Arrange, Act, Assert)

## Core Principles

**KISS** — Simplest solution that works. No premature optimization.

**DRY** — Extract common logic into reusable functions and components.

**YAGNI** — Don't build before it's needed. Start simple, refactor when needed.

**Readability** — Code is read 10x more than written. Clarity over cleverness.

## Naming Standards

### Variables

```typescript
// Good: Descriptive, type-hinted by name
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// Bad: Single-letter, unclear
const q = 'election'
const flag = true
const x = 1000
```

### Functions

```typescript
// Good: Verb-noun pattern
async function fetchMarketData(id: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// Bad: Unclear or noun-only
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

## References

- `references/typescript.md` — type safety, immutability, async patterns
- `references/react.md` — component structure, hooks, state management
- `references/api-design.md` — REST conventions, validation, error responses
- `references/file-org.md` — project structure, file naming
- `references/testing.md` — test patterns, AAA structure, test naming
- `references/code-smells.md` — anti-patterns, long functions, deep nesting, magic numbers

---

**Adapted from everything-claude-code by @affaan-m (MIT)**
