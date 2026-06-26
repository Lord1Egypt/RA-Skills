# Architecture Decision Records (ADRs)

Lightweight documentation capturing the context, decision, and consequences of significant technical choices. ADRs become the institutional memory of why things are built the way they are.

## What's Inside

- Quick Decision guide — when to write an ADR vs skip
- ADR Lifecycle — Proposed → Accepted → Deprecated → Superseded
- Templates — Standard, Full (for major decisions), Lightweight, Y-Statement (one-liner), Deprecation ADR
- Directory Structure and ADR Index conventions
- Tooling — adr-tools CLI usage (init, create, supersede, generate index)
- Review Checklist — before submission, during review, after acceptance

## When to Use

- Adopting new frameworks or technologies
- Choosing between architectural approaches
- Making database or infrastructure decisions
- Defining API design patterns
- Any decision that would be hard to reverse or understand later

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/backend/architecture-decision-records
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/backend/architecture-decision-records .cursor/skills/architecture-decision-records
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/backend/architecture-decision-records ~/.cursor/skills/architecture-decision-records
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/backend/architecture-decision-records .claude/skills/architecture-decision-records
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/backend/architecture-decision-records ~/.claude/skills/architecture-decision-records
```

---

Part of the [Backend](..) skill category.
