---
name: ask-claude
description: >
  Delegate a task to Claude Code CLI and immediately report the result back in chat.
  Supports persistent sessions — Claude Code remembers previous context within the same workdir.
  Use when the user asks to run Claude, delegate a coding task, continue a previous Claude session,
  or any task benefiting from Claude Code's tools (file editing, code analysis, bash, etc.).
  ALWAYS run synchronously and ALWAYS include the result in your reply.
metadata:
  {
    "openclaw": {
      "emoji": "🤖",
      "requires": { "anyBins": ["claude"] }
    }
  }
---

# Ask Claude — Execute & Report (with persistent sessions)

## The Two Modes

### New session (default)
Use when starting a fresh task or new topic.

```bash
OUTPUT=$(/home/xmanel/.openclaw/workspace/run-claude.sh "prompt" "/workdir")
echo "$OUTPUT"
```

### Continue session (--continue)
Use when the user is following up on a previous Claude task in the same workdir.
Claude Code will have full memory of what was done before — files read, edits made, context gathered.

```bash
OUTPUT=$(/home/xmanel/.openclaw/workspace/run-claude.sh --continue "prompt" "/workdir")
echo "$OUTPUT"
```

## When to use --continue

Use `--continue` when the user says things like:
- "agora corrige o que encontraste"
- "continua"
- "e o ficheiro X?"
- "faz o mesmo para..."
- "e agora?"
- "ok, e o erro de..."
- Anything that clearly references what Claude just did

Use a **new session** when:
- New unrelated task
- User says "começa do zero" / "new task" / "esquece o anterior"
- Different workdir/project

## Session storage

Claude Code stores sessions per-directory in `~/.claude/projects/`.
As long as you use the same `workdir`, `--continue` picks up exactly where it left off —
same file context, same conversation history, same edits.

## Direct command (alternative to wrapper)

```bash
# New session
OUTPUT=$(cd /workdir && env -u CLAUDECODE claude --permission-mode bypassPermissions --print "task" 2>&1)

# Continue session
OUTPUT=$(cd /workdir && env -u CLAUDECODE claude --permission-mode bypassPermissions --print --continue "task" 2>&1)
```

## Common workdirs

| Context         | Workdir                                                |
| --------------- | ------------------------------------------------------ |
| General/scripts | `/home/xmanel/.openclaw/workspace`                     |
| Trading         | `/home/xmanel/.openclaw/workspace/hyperliquid`         |

## After receiving output

- Summarize in 1-3 lines what Claude did/found
- Mention files created or edited
- If error: analyze and suggest fix
- If output is long: summarize, offer full output on request
