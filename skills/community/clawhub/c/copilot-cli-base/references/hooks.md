---
title: "Hooks"
source:
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks
  - https://docs.github.com/en/copilot/reference/hooks-configuration
category: reference
---

Hooks execute shell commands at key points during agent execution. They can log, display messages, and approve/deny tool calls. Only `preToolUse` can control execution.

## Configuration

Place JSON files in `.github/hooks/` (repo-scoped). Any `*.json` in that directory is loaded. User-level hooks go in `config.json` under `hooks` key.

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "./scripts/policy.sh",
        "cwd": ".github/hooks",
        "timeoutSec": 15,
        "env": { "LOG_LEVEL": "INFO" }
      }
    ]
  }
}
```

**Hook entry fields:** `type` (`"command"` or `"prompt"`), `bash`/`powershell` (script, for command type), `prompt` (text, for prompt type), `cwd` (optional), `timeoutSec` (default 30), `env` (optional key-value pairs).

**Prompt hooks** (`sessionStart` only): auto-submit text as if the user typed it. Runs before any `--prompt`. Useful for slash commands or setup prompts.

```json
{"type": "prompt", "prompt": "/compact"}
```

## Hook Types

| Hook | Trigger | Key Input Fields | Can Control? |
|------|---------|-----------------|-------------|
| `sessionStart` | New/resumed session | `source` (`new`/`resume`/`startup`), `initialPrompt` | No |
| `sessionEnd` | Session completes | `reason` (`complete`/`error`/`abort`/`timeout`/`user_exit`) | No |
| `userPromptSubmitted` | User sends prompt | `prompt` | No |
| `preToolUse` | Before tool runs | `toolName`, `toolArgs` (JSON string) | **Yes** |
| `postToolUse` | After tool completes | `toolName`, `toolArgs`, `toolResult` (`{resultType, textResultForLlm}`) | No |
| `errorOccurred` | Error during execution | `error` (`{message, name, stack}`) | No |

All hooks receive `timestamp` (Unix ms) and `cwd`. `toolArgs` is JSON-encoded string (requires double-parse).

## Denial Response (preToolUse only)

Output this JSON to deny:

```json
{"permissionDecision":"deny","permissionDecisionReason":"Reason shown to agent"}
```

Values: `"deny"` to block, `"allow"` to permit, `"ask"` to defer to user (only `"deny"` actively enforced). Exit code `0` always — non-zero = script failure, not denial.

## Example: Security Policy Script

```bash
#!/bin/bash
set -euo pipefail
INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.toolName // empty')"
if [ "$TOOL_NAME" != "bash" ]; then exit 0; fi

TOOL_ARGS="$(echo "$INPUT" | jq -r '.toolArgs // empty')"
COMMAND="$(echo "$TOOL_ARGS" | jq -r '.command // empty')"

# Block privilege escalation
if echo "$COMMAND" | grep -qE '\b(sudo|su)\b'; then
  jq -n --arg r "Privilege escalation blocked" \
    '{permissionDecision:"deny",permissionDecisionReason:$r}'
  exit 0
fi

# Block destructive ops
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s*/'; then
  jq -n --arg r "Destructive operation blocked" \
    '{permissionDecision:"deny",permissionDecisionReason:$r}'
  exit 0
fi
exit 0
```

## Example: File Permission Enforcement

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.toolName')
if [ "$TOOL_NAME" = "edit" ]; then
  PATH_ARG=$(echo "$INPUT" | jq -r '.toolArgs' | jq -r '.path')
  if [[ ! "$PATH_ARG" =~ ^(src/|test/) ]]; then
    echo '{"permissionDecision":"deny","permissionDecisionReason":"Can only edit src/ or test/"}'
    exit 0
  fi
fi
```

## Example: Audit Trail

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [{"type": "command", "bash": "./audit/log-session.sh"}],
    "preToolUse": [{"type": "command", "bash": "./audit/log-tool.sh"}],
    "postToolUse": [{"type": "command", "bash": "./audit/log-result.sh"}],
    "sessionEnd": [{"type": "command", "bash": "./audit/log-end.sh"}]
  }
}
```

## Example: Post-Tool Logging

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.toolName')
RESULT_TYPE=$(echo "$INPUT" | jq -r '.toolResult.resultType')
echo "$(date),${TOOL_NAME},${RESULT_TYPE}" >> tool-stats.csv

if [ "$RESULT_TYPE" = "failure" ]; then
  RESULT_TEXT=$(echo "$INPUT" | jq -r '.toolResult.textResultForLlm')
  echo "FAILURE: $TOOL_NAME - $RESULT_TEXT" | mail -s "Agent Tool Failed" admin@example.com
fi
```

## Multiple Hooks

Same-type hooks execute in array order:

```json
"preToolUse": [
  {"type": "command", "bash": "./security-check.sh"},
  {"type": "command", "bash": "./audit-log.sh"}
]
```

## Script Best Practices

- **Read input:** `INPUT=$(cat)` then parse with `jq` (Bash) or `$input = [Console]::In.ReadToEnd() | ConvertFrom-Json` (PowerShell)
- **Output JSON:** use `jq -c` (Bash) or `ConvertTo-Json -Compress` (PowerShell) for compact single-line output
- **Error handling:** `set -e` and always `exit 0` (Bash) or `$ErrorActionPreference = "Stop"` (PowerShell)
- **Redact secrets** before logging
- **Test locally:** `echo '{"toolName":"bash","toolArgs":"{\"command\":\"git status\"}"}' | ./my-hook.sh`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Not executing | Verify file in `.github/hooks/`, valid JSON, `version: 1`, script executable, correct shebang |
| Timing out | Increase `timeoutSec`, optimize script |
| Invalid JSON output | Ensure single line; use `jq -c` |

## Debugging

```bash
#!/bin/bash
set -x
INPUT=$(cat)
echo "DEBUG: Received input" >&2
echo "$INPUT" >&2
```

Validate: `./my-hook.sh | jq . && echo $?`
