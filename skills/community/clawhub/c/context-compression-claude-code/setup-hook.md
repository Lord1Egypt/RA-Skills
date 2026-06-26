# Optional: Configure PreCompact Hook

This document explains how to make the `context-compression` skill automatically trigger during each auto-compression, without manual invocation.

**Applicable platforms**: Claude Code, OpenClaw (versions supporting PreCompact hook)

---

## Claude Code Configuration

Edit `~/.claude/settings.json` and add the following configuration:

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cat ~/.claude/skills/context-compression/SKILL.md | python3 -c \"import sys,json; content=sys.stdin.read(); print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreCompact', 'additionalContext': content}}))\"",
            "timeout": 10,
            "statusMessage": "Loading compression strategy..."
          }
        ]
      }
    ],
    "PostCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Compression complete. Please check if there's anything that needs to be written to long-term memory (user preferences, incomplete tasks, important decisions). If so, update the user's memory file in the format of ~/.claude/skills/context-compression/memory-template.md.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## OpenClaw Configuration

Add to OpenClaw's hooks configuration (refer to your OpenClaw installation docs for the specific path):

```yaml
hooks:
  pre_compact:
    - type: inject_context
      source: skill
      skill: context-compression
  post_compact:
    - type: prompt
      prompt: "After compression, write user preferences, incomplete tasks, and important decisions to the memory file."
```

---

## Manual Usage Without Hook Configuration

Just tell the agent:
- "Compress the context"
- "Context is almost full, organize it"
- "Clean up conversation history, keep the important stuff"

The skill will automatically trigger and execute according to the strategy.
