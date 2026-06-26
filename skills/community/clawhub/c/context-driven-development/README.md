# Context-Driven Development

Treat project context as a managed artifact alongside code. Use structured context documents (product.md, tech-stack.md, workflow.md) to enable consistent AI interactions and team alignment. Essential for projects using AI-assisted development.

## What's Inside

- Core philosophy (context precedes code, living documentation, single source of truth, AI alignment)
- The context documents: product.md, tech-stack.md, workflow.md, tracks.md
- Directory structure for context artifacts
- Setup guides for greenfield and brownfield projects
- Maintenance principles and synchronization rules
- Validation checklist
- Anti-patterns (stale context, context sprawl, implicit context, over-specification)
- Session continuity patterns

## When to Use

- Setting up new projects with AI-assisted development
- Onboarding team members to existing codebases
- Ensuring consistent AI behavior across sessions
- Documenting decisions that affect code generation
- Managing projects with multiple contributors or AI assistants

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/meta/context-driven-development
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install context-driven-development
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/meta/context-driven-development .cursor/skills/context-driven-development
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/meta/context-driven-development ~/.cursor/skills/context-driven-development
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/meta/context-driven-development .claude/skills/context-driven-development
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/meta/context-driven-development ~/.claude/skills/context-driven-development
```

---

Part of the [Meta](..) skill category.
