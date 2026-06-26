# Hooks (Optional)

LLM-Wiki is primarily **protocol-driven** and does not require hooks to function.
However, you can optionally configure hooks for enhanced integration with your agent platform.

## Philosophy

- **Default**: No hooks needed. Agent reads `CLAUDE.md` and operates directly on files.
- **Optional**: Hooks can provide reminders, validation, or automation triggers.

## Claude Code Hooks

Claude Code hooks are configured in `.claude/settings.json`.

### Example: Pre-ingest Reminder

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "摄入|ingest",
      "hooks": [{
        "type": "command",
        "command": "echo '💡 Remember to check wiki/index.md for existing pages first'"
      }]
    }]
  }
}
```

## OpenClaw Hooks

OpenClaw hooks are configured similarly in `.openclaw/settings.json` or via the web interface.

### Example: Post-ingest Validation

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "./scripts/wiki-lint.sh"
      }]
    }]
  }
}
```

## Custom Hooks

You can create custom hooks in `hooks/custom/`:

- `pre-ingest.sh` — Run before ingest operations
- `post-ingest.sh` — Run after ingest operations  
- `daily-backup.sh` — Automated backup routine

## Recommended: No Hooks

For most users, **no hooks are necessary**. The protocol in `CLAUDE.md` is sufficient for agents to operate correctly.

Hooks add complexity. Only use them if you have specific automation needs.
