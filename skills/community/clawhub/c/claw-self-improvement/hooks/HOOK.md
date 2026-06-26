---
name: claw-self-improvement
description: "Injects claw-self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# Claw Self-Improvement Hook

Injects a reminder to evaluate learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log corrections, errors, and discoveries
- Prompts the agent to distill proven patterns into `.learnings/PROMOTED.md`
- Optionally adds a stronger instruction for visible learning notices when the skill config enables it

## Configuration

Default behavior needs no config. Enable the hook with:

```bash
openclaw hooks enable claw-self-improvement
```

Optional visible-notice gate in `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "claw-self-improvement": {
        "config": {
          "message": true
        }
      }
    }
  }
}
```

When `message` is `true`, the injected reminder tells the model:
- if it updates `.learnings/*.md` during a user-visible reply, append one short formatted note at the end of that same reply
- For raw logs, say: `Noted — logged to .learnings/LEARNINGS.md.`, `Noted — logged to .learnings/ERRORS.md.` or `Noted — logged to .learnings/FEATURE_REQUESTS.md.`
- For promotions, say: `Promoted — new rule to .learnings/PROMOTED.md.`
- skip it for `NO_REPLY`, or no user-visible reply
