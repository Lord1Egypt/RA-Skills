# Agent Skills in the SDK

> Extend Claude with specialized capabilities using Agent Skills. Skills are packaged as `SKILL.md` files.

## How Skills Work with the SDK

1. **Defined as filesystem artifacts**: Created as `SKILL.md` files in `.claude/skills/`
2. **Loaded from filesystem**: Loaded via `settingSources` / `setting_sources`
3. **Auto-discovered**: Metadata discovered from user/project directories at startup; full content loaded when triggered
4. **Invoked by the model**: Claude selects based on context automatically
5. **Filtered via `skills` option**: Enabled by default, can pass list of names, `"all"`, or `[]`

Skills must be created as filesystem artifacts; the SDK has no programmatic API for them.

## Using Skills

```typescript
query({
  prompt: "Help me process this PDF document",
  options: {
    cwd: "/path/to/project",
    settingSources: ["user", "project"],
    skills: "all",  // or ["pdf", "docx"], or [] to disable
    allowedTools: ["Read", "Write", "Bash"]
  }
})
```

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],
    skills="all",
    allowed_tools=["Read", "Write", "Bash"],
)
```

### Filtering Specific Skills

```typescript
options: { skills: ["pdf", "docx"] }  // Enable only these
options: { skills: [] }               // Disable all
```

The `skills` option is a context filter (not a sandbox). Skills not listed are hidden from the model, but files remain on disk.

## Skill Locations

| Type | Location | Load Condition |
|:---|:---|:---|
| Project Skills | `.claude/skills/` | `settingSources` includes `"project"` |
| User Skills | `~/.claude/skills/` | `settingSources` includes `"user"` |
| Plugin Skills | Bundled with plugins | Loaded via `plugins` option |

## Creating Skills

```
.claude/skills/processing-pdfs/
└── SKILL.md
```

SKILL.md contains YAML frontmatter + Markdown content. The `description` field determines when Claude invokes it.

> ⚠️ The `allowed-tools` frontmatter in SKILL.md is only supported in the CLI; it does not apply when using the SDK. Use the main `allowedTools` for tool access control.

## Tool Restrictions (in SDK)

```typescript
options: {
  settingSources: ["user", "project"],
  skills: "all",
  allowedTools: ["Read", "Grep", "Glob"],
  permissionMode: "dontAsk"  // Deny everything not in allowedTools
}
```

## Discovering Available Skills

```typescript
query({ prompt: "What Skills are available?", options: { skills: "all" } })
```

## Troubleshooting

| Issue | Solution |
|:---|:---|
| Skills not found | Check `settingSources` includes `"user"`/`"project"`; verify `cwd` points to correct directory |
| Skill not used | Check `skills` list includes the name; ensure description is specific and relevant |
| File locations | `ls .claude/skills/*/SKILL.md` and `ls ~/.claude/skills/*/SKILL.md` |