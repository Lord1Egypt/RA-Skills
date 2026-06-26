# Migrating to Claude Agent SDK

> Guide for migrating from Claude Code SDK to Claude Agent SDK.

## What Changed

| Aspect | Old Version | New Version |
|:---|:---|:---|
| Package name (TS/JS) | `@anthropic-ai/claude-code` | `@anthropic-ai/claude-agent-sdk` |
| Python package | `claude-code-sdk` | `claude-agent-sdk` |
| Documentation location | Claude Code docs | API Guides → Agent SDK section |

## TypeScript/JavaScript Migration

```bash
npm uninstall @anthropic-ai/claude-code
npm install @anthropic-ai/claude-agent-sdk
```

```typescript
// Before
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";

// After
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
```

```json
// package.json
{
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.2.0"
  }
}
```

## Python Migration

```bash
pip uninstall claude-code-sdk
pip install claude-agent-sdk
```

```python
# Before
from claude_code_sdk import query, ClaudeCodeOptions

# After
from claude_agent_sdk import query, ClaudeAgentOptions
```

## Breaking Changes

### 1. ClaudeCodeOptions → ClaudeAgentOptions

```python
# Before
from claude_code_sdk import query, ClaudeCodeOptions
options = ClaudeCodeOptions(model="claude-opus-4-7", permission_mode="acceptEdits")

# After
from claude_agent_sdk import query, ClaudeAgentOptions
options = ClaudeAgentOptions(model="claude-opus-4-7", permission_mode="acceptEdits")
```

### 2. System Prompt No Longer Default

The SDK no longer uses Claude Code's system prompt by default. It now uses a minimal system prompt by default.

```typescript
// Restore old behavior
const result = query({
  prompt: "Hello",
  options: { systemPrompt: { type: "preset", preset: "claude_code" } }
});

// Or custom
const result = query({
  prompt: "Hello",
  options: { systemPrompt: "You are a helpful coding assistant" }
});
```

```python
# Restore old behavior
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"}
)

# Or custom
options = ClaudeAgentOptions(system_prompt="You are a helpful coding assistant")
```

### 3. Setting Sources Defaults

Current behavior: Omitting `settingSources` loads user, project, and local filesystem settings (matching CLI).

To run in isolation:
```typescript
options: { settingSources: [] }  // Load no filesystem settings
options: { settingSources: ["project"] }  // Only project settings
```

## Reasons for Renaming

- Expanding beyond coding tasks to all types of AI agents
- Applicable to business agents, coding agents, custom agents for any domain

## Troubleshooting

**TypeScript**: Check imports updated to `@anthropic-ai/claude-agent-sdk`, run `npm install`

**Python**: Check imports updated to `claude_agent_sdk`, confirm requirements.txt updated, run `pip install claude-agent-sdk`