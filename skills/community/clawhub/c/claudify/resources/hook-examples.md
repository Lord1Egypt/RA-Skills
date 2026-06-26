# Hook Examples

Claude Code hook patterns and usage examples.

## Hook Structure

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "ToolName|OtherTool",
        "hooks": [
          {
            "type": "command",
            "command": "shell-command-here"
          }
        ]
      }
    ]
  }
}
```

## Environment Variables

| Variable | Description | Available Events |
|----------|-------------|------------------|
| `CLAUDE_FILE_PATHS` | Affected file paths | PreToolUse, PostToolUse |
| `CLAUDE_TOOL_INPUT` | Tool input JSON | PreToolUse, PostToolUse |
| `CLAUDE_TOOL_OUTPUT` | Tool output | PostToolUse only |
| `CLAUDE_SESSION_ID` | Session ID | All events |

## Pattern Examples

### 1. Flag File Pattern (Deferred Execution)

Building on every file modification is slow; create a flag and process at session end.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -qE '\\.(ts|tsx)$'; then touch /tmp/needs-rebuild; fi"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f /tmp/needs-rebuild ]; then rm /tmp/needs-rebuild && npm run build; fi"
          }
        ]
      }
    ]
  }
}
```

**Use cases**:
- VSCode extension build + install
- TypeScript compilation
- Docker image rebuild

### 2. Auto-Lint Pattern

Auto-format on file save.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -qE '\\.(js|ts|jsx|tsx)$'; then npx prettier --write \"$CLAUDE_FILE_PATHS\"; fi"
          }
        ]
      }
    ]
  }
}
```

### 3. Validation Pattern (Blocking)

Prevent dangerous operations. Return exit 1 in `PreToolUse` to block.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'Blocked: rm -rf not allowed' && exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

### 4. Notification Pattern

Notify on completion.

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude session ended\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 5. Logging Pattern

Record all tool usage.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date): Tool used on $CLAUDE_FILE_PATHS\" >> ~/.claude/tool-usage.log"
          }
        ]
      }
    ]
  }
}
```

### 6. Git Auto-Stage Pattern

Auto-stage modified files.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "git add \"$CLAUDE_FILE_PATHS\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 7. Test Runner Pattern

Run related tests on file modification.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -qE 'src/.*\\.ts$'; then npm test -- --findRelatedTests \"$CLAUDE_FILE_PATHS\"; fi"
          }
        ]
      }
    ]
  }
}
```

## Real Project Examples

### VSCode Extension Development

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -qE 'packages/(vscode-extension|core)/'; then touch /tmp/vsix-rebuild-needed; fi"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f /tmp/vsix-rebuild-needed ]; then rm /tmp/vsix-rebuild-needed && pnpm build && code --install-extension *.vsix --force; fi"
          }
        ]
      }
    ]
  }
}
```

### Monorepo Build

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "PACKAGE=$(echo \"$CLAUDE_FILE_PATHS\" | grep -oE 'packages/[^/]+' | head -1); if [ -n \"$PACKAGE\" ]; then echo \"$PACKAGE\" >> /tmp/changed-packages; fi"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f /tmp/changed-packages ]; then sort -u /tmp/changed-packages | xargs -I{} pnpm --filter {} build && rm /tmp/changed-packages; fi"
          }
        ]
      }
    ]
  }
}
```

## Matcher Limitations

**IMPORTANT**: Matcher only supports tool name matching. Command content-based filtering is NOT supported at matcher level.

| Supported | Not Supported |
|-----------|---------------|
| `Bash` (exact match) | `Bash(git:*)` |
| `Edit\|Write` (regex OR) | `Bash(kubectl:*)` |
| `Notebook.*` (regex pattern) | `tool_input.command` conditions |
| `*` (all tools) | glob patterns |

**Solution**: Filter by command content inside hook scripts using `jq`:

```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Only process git commands
if ! [[ "$command" =~ ^git ]]; then
  exit 0
fi
# ... validation logic
```

### 8. Dispatcher Pattern (Recommended for Multiple Hooks)

When you have multiple PreToolUse hooks for the same tool, consolidate into a single dispatcher to reduce log noise and improve performance.

**Problem**: Each hook runs separately, creating verbose session logs:
```
hook_progress: PreToolUse:Bash - script1.sh
hook_progress: PreToolUse:Bash - script2.sh
hook_progress: PreToolUse:Bash - script3.sh
... (repeated per Bash call)
```

**Solution**: Single dispatcher that routes by command pattern:

```bash
#!/bin/bash
# bash-pretooluse-dispatcher.sh

INPUT="${CLAUDE_TOOL_INPUT:-}"
[ -z "$INPUT" ] && INPUT=$(cat)

COMMAND=$(echo "$INPUT" | jq -r '.command // empty' 2>/dev/null)
[ -z "$COMMAND" ] && exit 0

BLOCKED=false

# Git commands
if [[ "$COMMAND" =~ ^git[[:space:]] ]]; then
  # Dangerous command check
  if [[ "$COMMAND" =~ (reset\ --hard|push\ --force|push\ -f\ ) ]]; then
    echo "BLOCK: Dangerous git command detected"
    BLOCKED=true
  fi

  # Commit validation
  if [[ "$COMMAND" =~ git[[:space:]]commit ]]; then
    # ... commit checks
    :
  fi
fi

# kubectl/helm commands
if [[ "$COMMAND" =~ ^(kubectl|helm)[[:space:]] ]]; then
  # Production delete guard
  if [[ "$COMMAND" =~ --context[[:space:]]+prod ]] && [[ "$COMMAND" =~ delete ]]; then
    echo "BLOCK: Production delete requires confirmation"
    BLOCKED=true
  fi
fi

# cat/echo file write guard
if [[ "$COMMAND" =~ (cat[[:space:]]*\<\<|echo[[:space:]].*\>) ]]; then
  if [[ "$COMMAND" =~ \>.*\.(md|yaml|json|sh|ts|js)$ ]]; then
    echo "BLOCK: Use Write tool instead of cat/echo"
    BLOCKED=true
  fi
fi

$BLOCKED && exit 1
exit 0
```

**Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/scripts/bash-pretooluse-dispatcher.sh"
          }
        ]
      }
    ]
  }
}
```

**Benefits**:
- Single log entry per tool call
- Faster execution (one process vs many)
- Centralized logic, easier maintenance
- Conditional checks only run when relevant

## Important Notes

1. **Empty matcher**: Matches all tools
2. **exit 1**: Only blocks in PreToolUse
3. **Path spaces**: Quote `"$CLAUDE_FILE_PATHS"` required
4. **Ignore errors**: Use `2>/dev/null || true` to allow failures
5. **Performance**: PostToolUse runs on every tool use, keep commands lightweight
6. **Matcher scope**: Tool names only, not command content (use dispatcher for filtering)
