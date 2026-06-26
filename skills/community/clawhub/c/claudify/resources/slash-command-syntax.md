# Slash Command Syntax Reference

## File Location

| Level | Location | Scope |
|-------|----------|-------|
| Project | `.claude/commands/name.md` | Team, version controlled |
| Global | `~/.claude/commands/name.md` | Personal, all projects |

Project commands take precedence over global commands with the same name.

## Frontmatter Options

```yaml
---
allowed-tools: Bash(git:*), Read, Edit    # Tools the command can use
argument-hint: [issue-number] [priority]  # Expected arguments for /help
description: Brief description            # Shown in /help output
model: claude-3-5-haiku-20241022          # Specific model to use
disable-model-invocation: false           # Prevent SlashCommand tool from calling this
---
```

| Option | Purpose | Default |
|--------|---------|---------|
| `allowed-tools` | Tools the command can use | Inherits from conversation |
| `argument-hint` | Expected arguments display | None |
| `description` | Brief description in `/help` | First line of prompt |
| `model` | Specific model to use | Inherits from conversation |
| `disable-model-invocation` | Block SlashCommand tool access | false |

## Arguments

### All Arguments: `$ARGUMENTS`

```markdown
Fix issue #$ARGUMENTS following our coding standards.
```

Usage: `/fix-issue 123 high-priority`
Result: `Fix issue #123 high-priority following our coding standards.`

### Positional Arguments: `$1`, `$2`, `$3`, etc.

```markdown
---
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
```

Usage: `/review-pr 456 high alice`
Result: `Review PR #456 with priority high and assign to alice.`

## Dynamic Content

### Bash Execution: `!`backtick`

Execute shell commands and embed output:

```markdown
## Context

- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Changed files: !`git diff --name-only`

Based on the above, create a commit message.
```

### File References: `@path`

Include file contents inline:

```markdown
Review the implementation in @src/utils/helpers.js

Compare the old version @src/old.js with new @src/new.js
```

## Examples

### Simple Git Commit

```markdown
---
allowed-tools: Bash(git:*)
description: Create a conventional commit
---

Create a git commit with conventional commit format.
Current changes: !`git diff --staged`
```

### PR Review with Arguments

```markdown
---
allowed-tools: Read, Bash(gh:*)
argument-hint: [pr-number]
description: Review a GitHub PR
---

Review PR #$1:
- PR details: !`gh pr view $1`
- Changed files: !`gh pr diff $1 --name-only`

Focus on security, performance, and code style.
```

### Build Command for Monorepo

```markdown
---
allowed-tools: Bash(pnpm:*), Bash(code:*)
description: Build and install VSCode extension
---

Build the VSCode extension:

1. Build core: `pnpm --filter @claude-sessions/core build`
2. Package vsix: `pnpm --filter claude-sessions package`
3. Install: `code --install-extension packages/vscode-extension/claude-sessions-*.vsix --force`

Run all steps and report the result.
```

### Context-Aware Debug

```markdown
---
allowed-tools: Read, Bash(npm:*), Bash(node:*)
description: Debug current file with context
---

Debug the current issue:

Project info:
- Package.json: @package.json
- Node version: !`node --version`
- Dependencies: !`npm ls --depth=0`

Analyze and suggest fixes.
```

## Namespacing

Organize commands in subdirectories:

```
.claude/commands/
├── frontend/
│   ├── component.md    # /component (shown as "project:frontend")
│   └── test.md         # /test (shown as "project:frontend")
└── backend/
    ├── api.md          # /api (shown as "project:backend")
    └── migrate.md      # /migrate (shown as "project:backend")
```

## SlashCommand Tool Integration

Claude can invoke custom commands programmatically. To enable:

1. Add `description` in frontmatter
2. Reference command in prompts: "Run /build when code changes"

Character budget: 15,000 characters (configurable via `SLASH_COMMAND_TOOL_CHAR_BUDGET`)
