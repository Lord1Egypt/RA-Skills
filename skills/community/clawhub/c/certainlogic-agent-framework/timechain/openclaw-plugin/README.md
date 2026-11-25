# Cypher Tempre Enforcement Plugin for OpenClaw

This native OpenClaw plugin wires Cypher Tempre's existing `enforce.py` into
typed OpenClaw plugin hooks. It does not duplicate the Timechain engine; it calls
the `enforce.py`, `dormancy.py`, and `recall.py` files from the installed
`cypher-tempre-self-model` skill folder.

## Hook Mapping

| OpenClaw hook | Cypher Tempre action |
|---|---|
| `session_start` | `enforce.py session-start` |
| `before_prompt_build` | `enforce.py mark` and prompt reminder injection |
| `before_agent_finalize` | `enforce.py stop-check`; returns `action: "revise"` when no ring was sealed |
| `subagent_ended` | Read-only diagnostic comparing `.enforce.json` baseline to the chain head |
| `agent_end` | Clears the plugin's in-memory run marker |

`before_agent_finalize` is the Stop-equivalent hook: it runs when OpenClaw is
about to accept a natural final answer, and can request one more bounded model
pass so the agent seals before finalizing.

`subagent_ended` is diagnostic in the current OpenClaw plugin surface: it records
and logs whether the subagent advanced the chain after the turn-start baseline,
but it does not block or revise the already-finished subagent return. Treat this
as weaker than Claude Code's `SubagentStop` until OpenClaw exposes a blocking
subagent-finalize event.

## Install

After installing the OpenClaw skill bundle:

```bash
openclaw plugins install ~/.openclaw/workspace/skills/cypher-tempre-self-model/openclaw-plugin
openclaw config set 'plugins.entries.cypher-tempre-enforcement.hooks.allowConversationAccess' true --strict-json
openclaw gateway restart
```

If your skill is installed somewhere else, configure the plugin entry:

```bash
openclaw config set 'plugins.entries.cypher-tempre-enforcement.config.skillRoot' /path/to/cypher-tempre-self-model
openclaw gateway restart
```

Equivalent JSON config:

```json
{
  "plugins": {
    "entries": {
      "cypher-tempre-enforcement": {
        "enabled": true,
        "config": {
          "skillRoot": "/path/to/cypher-tempre-self-model"
        },
        "hooks": {
          "allowConversationAccess": true
        }
      }
    }
  }
}
```

`allowConversationAccess` is required by OpenClaw for non-bundled plugins that use
raw conversation lifecycle hooks such as `before_agent_finalize`.

Optional config:

- `chainRoot`: use a separate Timechain root.
- `pythonBin`: Python executable, default `python3`.
- `timeoutMs`: timeout for local enforcement calls, default `5000`.
- `maxFinalizeAttempts`: maximum extra passes requested for one unsealed turn,
  default `3`.
- `injectReminder`: set `false` to turn off reminder injection.
