# Modifying System Prompts

> Choose between the `claude_code` preset and custom system prompts, customize behavior via CLAUDE.md, output styles, appending, or fully custom prompts.

## How System Prompts Work

The Agent SDK has three starting points:

| Starting Point | Description | Configuration |
|:---|:---|:---|
| **Minimal default** | When `systemPrompt` is not set, only covers tool calling, omits Claude Code's coding guidelines | Default |
| **`claude_code` preset** | Full system prompt from Claude Code CLI | `systemPrompt: { type: "preset", preset: "claude_code" }` |
| **Custom string** | Your own prompt, SDK sends only what you provide | `systemPrompt: "your prompt"` |

### Deciding on a Starting Point

| You're building a... | Use | What you get |
|:---|:---|:---|
| CLI/IDE-like coding tool | `claude_code` preset | Full Claude Code prompt: tool guidance, safety rules, terminal-friendly responses |
| Same + product-specific rules | `claude_code` preset + `append` | Above + your instructions added after the preset (lowest risk) |
| Different surface/identity/permission model, or non-coding agent | Custom prompt string | Only what you write, must replace tool guidance and safety instructions yourself |
| Thin tool-calling loop, no agent persona | No `systemPrompt` option | Minimal default: just tool-calling support |

"Different from Claude Code" typically means: different surface (chat UI, structured output), different persona (support bot, domain-specific agent), different permission model (autonomous operation), non-coding tasks.

## Customizing Agent Behavior

### CLAUDE.md Files (Project-Level Instructions)

CLAUDE.md content is injected into the conversation (not into the system prompt) and works with any system prompt configuration.

```typescript
// Load project CLAUDE.md + claude_code preset
options: {
  systemPrompt: { type: "preset", preset: "claude_code" },
  settingSources: ["project"]
}
```

### Output Styles (Persistent Configuration)

Output styles are saved as markdown files with frontmatter metadata. Storage locations:
- `~/.claude/output-styles/` — User-level (available across projects)
- `.claude/output-styles/` — Project-level (team sharing)

```markdown
---
name: Code Reviewer
description: Thorough code review assistant
keep-coding-instructions: true
---
You are an expert code reviewer.
For every code submission: check bugs, security, performance, suggest improvements.
```

Activation: CLI `/config`, `outputStyle` in settings.json, or `options.outputStyle` in TypeScript SDK.

### Appending to the Preset

```typescript
systemPrompt: {
  type: "preset",
  preset: "claude_code",
  append: "Always include detailed docstrings and type hints in Python code."
}
```

**Improved caching**: Setting `excludeDynamicSections: true` moves per-session context to the first user message, making the system prompt shareable across sessions for caching (requires TS v0.2.98+ / Python v0.1.58+).

```typescript
systemPrompt: {
  type: "preset", preset: "claude_code",
  append: "...",
  excludeDynamicSections: true
}
```

### Custom System Prompt String

```typescript
systemPrompt: `You are a Python coding specialist.
- Write clean, well-documented code
- Use type hints for all functions
- Include comprehensive docstrings`
```

## Comparing the Four Approaches

| Feature | CLAUDE.md | Output Styles | Preset + Append | Custom Prompt |
|:---|:---|:---|:---|:---|
| Persistence | Per-project file | Saved as file | Session only | Session only |
| Reusability | Per-project | Cross-project | Code duplication | Code duplication |
| Management | Filesystem | CLI + files | In code | In code |
| Default tools | Preserved | Preserved | Preserved | Lost (unless included) |
| Built-in safety | Maintained | Maintained | Maintained | Must add |
| Environment context | Automatic | Automatic | Automatic | Must provide |
| Customization level | Add only | Replace or extend | Add only | Full control |
| Version control | With project | Yes | With code | With code |

## Combining Approaches

Approaches can be combined — output styles set long-term behavior, append layers session-specific instructions:

```typescript
// Output style (persistent) + append (session-specific)
systemPrompt: {
  type: "preset", preset: "claude_code",
  append: "For this review, prioritize: OAuth 2.0 compliance, Token storage security"
}