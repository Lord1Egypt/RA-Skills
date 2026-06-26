# Hook Setup

Configure automatic pipeline reminders via agent hooks. This is **opt-in** — you must explicitly configure hooks in your agent's settings.

## Overview

The pipeline works without hooks — the skill description triggers it. Hooks are for users who want **proactive phase reminders** injected automatically, especially at the start of a task (to nudge toward Phase 1) or after a tool failure (to nudge toward Phase 4's attempt log).

## Claude Code Setup

### Project-Level

Create `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/coding-pipeline/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a reminder at the start of every prompt — roughly 60-80 tokens — asking whether the task is non-trivial and nudging toward Phase 1.

### User-Level

If you want the pipeline reminder across all projects, put the same hook in `~/.claude/settings.json`. Use an absolute path for the command:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "/absolute/path/to/coding-pipeline/scripts/activator.sh"
      }]
    }]
  }
}
```

## Codex CLI Setup

Same pattern, using `.codex/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/coding-pipeline/scripts/activator.sh"
      }]
    }]
  }
}
```

Codex supports the same hook events as Claude Code — point both at the same scripts.

## OpenClaw Setup

OpenClaw uses workspace-based injection rather than hooks. Install the skill via ClawdHub:

```bash
clawdhub install coding-pipeline
```

The skill's `SKILL.md` is injected into every session automatically. No hook configuration required. See `references/openclaw-integration.md` for details.

## Hook Script Details

`scripts/activator.sh` is short and side-effect-free. It writes a context block to stdout that the agent consumes:

```
<coding-pipeline-reminder>
If this task is non-trivial (bug, feature, refactor, error investigation):
  1. Start in Phase 1 (Planner) — hypothesis + scope + success criteria
  2. Do NOT skip to Phase 2 (Coder)
  3. Phase 3 (Validator) must verify root cause, not just build success
  4. Phase 4 (Debugger) caps at 3 attempts, then escalates

Trivial tasks (typos, formatting, one-line config) skip the pipeline.
</coding-pipeline-reminder>
```

It takes <10ms to run and adds ~80 tokens per prompt. The overhead is deliberate — a small, consistent nudge is more effective than occasional reminders.

## Disabling

### Claude Code / Codex

Remove the hooks block from `settings.json`.

### OpenClaw

```bash
clawdhub uninstall coding-pipeline
```

Or edit `~/.openclaw/workspace/skills/` to remove the folder.

## Troubleshooting

**Hook not firing:**

- Verify the script is executable: `chmod +x scripts/activator.sh`
- Verify the path in `settings.json` resolves from the working directory where the agent runs
- Check agent logs for hook invocation errors

**Token overhead too high:**

- Reduce the hook trigger — use a `matcher` regex to only fire on certain prompt patterns
- Disable the hook and rely on the skill description for activation instead

**Multiple skills competing:**

- Phase reminders from multiple skills can add up. If you're running `coding-pipeline` + `self-improving-agent` + `systematic-debugging` all with hooks, consider consolidating to one activator that covers all three.
