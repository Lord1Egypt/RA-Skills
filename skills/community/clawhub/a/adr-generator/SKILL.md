---
name: adr-generator
description: Architecture Decision Record generator — analyze codebases and document technical decisions with context, alternatives, and consequences. Use when asked to document architecture decisions, create ADRs, or explain why technical choices were made.
---

# Architecture Decision Record Generator

Analyze a codebase or conversation to produce Architecture Decision Records (ADRs) — structured documents that capture the WHY behind technical choices so future developers understand the reasoning.

Use when: "document this decision", "create an ADR", "why did we choose X", "record our architecture decision", or when a significant technical choice is being made.

## What is an ADR?

A short document capturing one significant architectural decision: the context, the decision itself, the alternatives considered, and the consequences. ADRs form a decision log that prevents the same debates from recurring and helps new team members understand the codebase.

## When to Create an ADR

- Choosing a framework, database, or major library
- Defining API contracts or data schemas
- Setting team conventions (testing strategy, branching model, deployment process)
- Making a trade-off (performance vs maintainability, monolith vs microservices)
- Adopting or dropping a tool
- Any decision someone might later ask "why did we do it this way?"

## Analysis Steps

### 1. Identify the Decision

From conversation or code review, extract:
- What was decided
- When (date or PR/commit reference)
- Who was involved (if known)

### 2. Reconstruct Context

```bash
# Check git history for related changes
git log --oneline --all --grep="<keyword>" | head -20

# Find when a dependency was added
git log --all --diff-filter=A -- package.json | head -5
git log -p --all -S '<package-name>' -- package.json | head -40

# Look for prior discussion in docs
grep -ri "decision\|chose\|alternative\|trade-off\|migrate" docs/ README.md CONTRIBUTING.md 2>/dev/null

# Check for existing ADRs
find . -type f -name "*.md" -path "*/adr/*" -o -name "*decision*" 2>/dev/null
ls docs/adr/ docs/decisions/ doc/architecture/ 2>/dev/null
```

### 3. Analyze Alternatives

For framework/library decisions:
```bash
# What else was evaluated? Check for traces
grep -ri "considered\|vs\|compared\|evaluated\|alternative" docs/ 2>/dev/null
git log --all --oneline | grep -i "try\|experiment\|spike\|poc\|prototype" | head -10

# Check if multiple solutions were tried
git log --all --oneline --diff-filter=D -- '**/package.json' | head -10
```

### 4. Assess Consequences

Read the current implementation to understand what the decision enabled or constrained:
```bash
# How deeply is the choice embedded?
grep -rc "<framework-import>" --include="*.{ts,js,py,go}" . 2>/dev/null | sort -t: -k2 -rn | head -10

# Are there workarounds that suggest regret?
grep -ri "hack\|workaround\|todo\|fixme\|technical debt" --include="*.{ts,js,py,go}" . 2>/dev/null | head -20
```

## ADR Template

Use the Michael Nygard format (industry standard):

```markdown
# ADR-{NNN}: {Title — short, noun-phrase}

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Deciders:** [names or roles]

## Context

What is the issue that we're seeing that is motivating this decision or change?
Describe the forces at play: technical constraints, business requirements, team capabilities, timeline pressure.

## Decision

State the decision clearly in full sentences.
"We will use PostgreSQL as our primary database."
"We will adopt a monorepo structure using Turborepo."

## Alternatives Considered

### Alternative A: [name]
- **Pros:** ...
- **Cons:** ...
- **Why not:** ...

### Alternative B: [name]
- **Pros:** ...
- **Cons:** ...
- **Why not:** ...

## Consequences

### Positive
- What becomes easier or possible because of this decision

### Negative
- What becomes harder, more expensive, or is now ruled out
- What technical debt does this introduce

### Risks
- What could go wrong
- Under what conditions would we reconsider this decision

## References

- Links to relevant PRs, issues, benchmarks, or external resources
```

## File Organization

Standard locations (create if none exist):
```
docs/adr/
  0001-use-postgresql.md
  0002-adopt-monorepo.md
  0003-api-versioning-strategy.md
  README.md          # index of all ADRs with one-line summaries
```

Index format for README.md:
```markdown
# Architecture Decision Records

| # | Decision | Status | Date |
|---|----------|--------|------|
| 1 | [Use PostgreSQL](0001-use-postgresql.md) | Accepted | 2026-01-15 |
| 2 | [Adopt monorepo](0002-adopt-monorepo.md) | Accepted | 2026-02-01 |
```

## Tips

- Keep ADRs short — 1-2 pages max. If it's longer, the decision is too big (split it).
- Write ADRs at decision time, not after. Retrospective ADRs lose the "alternatives considered" context.
- ADRs are immutable once accepted. If a decision changes, create a new ADR that supersedes the old one.
- Number them sequentially. Never reuse numbers.
- Store them in the repo, next to the code they govern.
- Review ADRs in PRs — they deserve the same scrutiny as code.
