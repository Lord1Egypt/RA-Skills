# Platform setup

This skill is portable, but automation differs by environment.

## Manual use (works everywhere)

The safest baseline is manual activation:
1. determine the workspace root
2. run `python3 scripts/learnings.py ... --root /path/to/workspace`
3. promote or extract only after the pattern is proven

## Claude Code / Claude-style hook configs

Example prompt-start reminder:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/self-improvement/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

Example error reminder:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/self-improvement/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex / other skills-aware CLIs

Use the same manual workflow unless your client supports equivalent command hooks.

## GitHub Copilot

When hooks are unavailable, add a compact reminder to `.github/copilot-instructions.md`:

```markdown
## Self-improvement
After solving non-obvious issues or learning project-specific conventions, consider logging the durable lesson to `.learnings/` and promoting proven rules into shared memory.
```

## OpenClaw

OpenClaw-specific workspace and hook notes are in `references/openclaw-integration.md`.
