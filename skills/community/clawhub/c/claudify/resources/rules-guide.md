# Rules Guide

Claude Code rules for AI behavior constraints and project conventions.

## Basic Structure

```markdown
# Rule Title

## Purpose
What this rule enforces

## Guidelines
- Specific constraint 1
- Specific constraint 2
- Specific constraint 3

## Examples

**Do:**
- Correct behavior example

**Don't:**
- Incorrect behavior example
```

## Location

| Scope | Path |
|-------|------|
| Global (all projects) | `~/.claude/rules/*.md` |
| Project-specific | `.claude/rules/*.md` |

Rules are automatically loaded at session start.

## Rule Categories

### 1. Code Style Rules

```markdown
# TypeScript Conventions

## Purpose
Enforce consistent TypeScript code style across the project.

## Guidelines
- Use `interface` over `type` for object shapes
- Prefer `const` assertions for literal types
- Always use explicit return types on exported functions
- No `any` type - use `unknown` if type is truly unknown

## Examples

**Do:**
```typescript
interface User {
  id: string;
  name: string;
}

export function getUser(id: string): Promise<User> {
  // ...
}
```

**Don't:**
```typescript
type User = { id: any; name: any };

export function getUser(id) {
  // ...
}
```
```

### 2. Git Workflow Rules

```markdown
# Git Commit Rules

## Purpose
Maintain consistent git history and commit quality.

## Guidelines
- Use Conventional Commit format (feat, fix, docs, etc.)
- Keep commits atomic - one logical change per commit
- Never force push to main/master
- Always sign commits with `-S` flag for open source

## Examples

**Do:**
```
feat(auth): add OAuth2 login flow
fix(api): handle null response from external service
```

**Don't:**
```
fixed stuff
WIP
asdf
```
```

### 3. Security Rules

```markdown
# Security Constraints

## Purpose
Prevent accidental security issues and data loss.

## Guidelines
- Never commit secrets or API keys
- Backup before destructive operations
- Validate user input at system boundaries
- Use parameterized queries for database operations

## Forbidden Commands (require user confirmation)
- `git reset --hard`
- `rm -rf` (use backup instead)
- `docker volume rm`
- Any command that deletes persistent data
```

### 4. Documentation Rules

```markdown
# Documentation Standards

## Purpose
Keep documentation current and useful.

## Guidelines
- Update README when adding features
- Document breaking changes immediately
- Keep CLAUDE.md concise - detail goes in separate docs
- Use Mermaid or PlantUML for diagrams
```

### 5. Architecture Rules

```markdown
# Project Architecture

## Purpose
Maintain consistent project structure and patterns.

## Guidelines
- Components in `src/components/`
- Utilities in `src/utils/`
- Types in `src/types/`
- Tests adjacent to source files (`*.test.ts`)

## File Size Limits
- Components: Max 200 lines (split if larger)
- Utility files: Max 150 lines
- Test files: No strict limit

## Import Order
1. External packages
2. Internal aliases (@/)
3. Relative imports
4. Type imports
```

## Multiple Rules Files

You can have multiple rule files for different concerns:

```
.claude/rules/
├── code-style.md
├── git-workflow.md
├── security.md
└── architecture.md
```

## Best Practices

1. **Be specific**: Vague rules are ignored. Give concrete examples.
2. **Keep focused**: One concern per rule file
3. **Include examples**: Show both correct and incorrect patterns
4. **Explain why**: Help understand the reasoning behind rules
5. **Update regularly**: Remove outdated rules, add new learnings

## Interaction with Other Types

| With | Behavior |
|------|----------|
| Skills | Rules constrain how skills operate |
| Agents | Agents inherit rules from session |
| Hooks | Hooks can enforce rules automatically |
| Commands | Commands follow rule constraints |
