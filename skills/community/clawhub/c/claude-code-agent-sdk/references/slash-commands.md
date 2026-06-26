# Slash Commands in the SDK

> Use slash commands to control Claude Code sessions via the SDK.

Slash commands start with `/`. Commands that only work without an interactive terminal can be dispatched via the SDK. The `system/init` message lists available commands.

## Discovering Available Commands

```typescript
for await (const message of query({ prompt: "Hello", options: { maxTurns: 1 } })) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Available:", message.slash_commands);
    // Example: ["/compact", "/context", "/usage", "/refactor"]
  }
}
```

## Sending a Command

Send the slash command as the prompt string:

```typescript
for await (const message of query({ prompt: "/compact", options: { maxTurns: 1 } })) {
  if (message.type === "result" && message.subtype === "success") {
    console.log("Done:", message.result);
  }
}
```

## Built-in Commands

### `/compact` — Compress Conversation History

```typescript
if (message.type === "system" && message.subtype === "compact_boundary") {
  console.log("Pre-compaction tokens:", message.compact_metadata.pre_tokens);
  console.log("Trigger:", message.compact_metadata.trigger);
}
```

### Clearing Conversation

The interactive `/clear` command is not available in the SDK. Each `query()` call already starts with a fresh conversation. You can return to previous sessions via the `resume` option.

## Custom Slash Commands

Recommended format: `.claude/skills/<name>/SKILL.md` (supports both autonomous invocation + slash command invocation)

Legacy format: `.claude/commands/` (slash command invocation only, still supported in CLI)

### File Locations

- Project: `.claude/commands/` (legacy) or `.claude/skills/` (recommended)
- Personal: `~/.claude/commands/` (legacy) or `~/.claude/skills/` (recommended)

### Basic Example

`.claude/commands/refactor.md`:
```markdown
Refactor the selected code to improve readability and maintainability.
Focus on clean code principles and best practices.
```

Creates the `/refactor` command.

### With Frontmatter

```markdown
---
allowed-tools: Read, Grep, Glob
description: Run security vulnerability scan
model: claude-opus-4-7
---
Analyze the codebase for security vulnerabilities...
```

### Advanced Features

**Arguments and placeholders**:
```markdown
---
argument-hint: [issue-number] [priority]
---
Fix issue #$1 with priority $2.
```

Usage: `prompt: "/fix-issue 123 high"` → `$1="123"`, `$2="high"`

**Bash command execution** (`!` prefix):
```markdown
- Current status: !`git status`
- Current diff: !`git diff HEAD`
```

**File references** (`@` prefix):
```markdown
- Package config: @package.json
- TypeScript config: @tsconfig.json
```

**Namespace organization** (subdirectories):
```
.claude/commands/
├── frontend/component.md    → /component
├── backend/api-test.md      → /api-test
└── review.md                → /review
```
Subdirectories affect command description but not command name.