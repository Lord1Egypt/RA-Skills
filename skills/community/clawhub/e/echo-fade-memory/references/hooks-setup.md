# Hook Setup

Use these hooks when you want the agent to behave more like the reference skills:

- recall/store discipline before and during tasks
- reminder to persist errors and learnings

The scripts are intentionally lightweight and only emit reminder text.

Assumption in this file:

- the skill is used in its installed form
- commands inside the skill use `./scripts/...`
- external hook configs should prefer explicit installed paths such as `~/.openclaw/skills/echo-fade-memory/scripts/...`

## Environment

All scripts honor:

```bash
export EFM_BASE_URL=http://127.0.0.1:8080
```

If unset, they default to `http://127.0.0.1:8080`.

## Claude Code Setup

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex Setup

Create `.codex/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Minimal Setup

If you want lower prompt overhead, install only the activator:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## What the Scripts Do

| Script | Trigger | Behavior |
|--------|---------|----------|
| `activator.sh` | `UserPromptSubmit` | Reminds the agent to recall relevant memory first, then store durable new facts |
| `error-detector.sh` | `PostToolUse` for Bash | Detects likely command failures and reminds the agent to capture the workaround as memory |

## Installed OpenClaw / Shared Skill Paths

Recommended explicit installed-path setup:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.openclaw/skills/echo-fade-memory/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Verification

### Test health

```bash
./scripts/health-check.sh
```

### Test activator output

```bash
./scripts/activator.sh
```

Expected: an XML-style reminder block mentioning recall, store, reinforce, and ground.

### Test error detector output

```bash
CLAUDE_TOOL_OUTPUT="fatal: example failure" ./scripts/error-detector.sh
```

Expected: a reminder block suggesting error-memory capture.

## Troubleshooting

### Script not found

Use absolute paths if your agent runs from a different working directory:

```json
{
  "command": "/absolute/path/to/echo-fade-memory/scripts/activator.sh"
}
```

### Permission denied

```bash
chmod +x ~/.openclaw/skills/echo-fade-memory/scripts/*.sh
```

### Too much prompt overhead

- Use only `activator.sh`
- Add a matcher like `memory|decision|preference|fix|error`
- Keep the script output short

## Security Notes

- These hook scripts only emit text
- They do not write files or mutate the service
- The error detector reads `CLAUDE_TOOL_OUTPUT` and pattern-matches common failures
