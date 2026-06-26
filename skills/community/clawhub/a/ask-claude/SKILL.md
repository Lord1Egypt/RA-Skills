---
name: ask-claude
description: >
  Delegate a task to Claude Code CLI and immediately report the result back in chat.
  Supports persistent sessions with full context memory. Safe execution: no data exfiltration,
  no external calls, file operations confined to workspace.
  Use when the user asks to run Claude, delegate a coding task, continue a previous Claude session,
  or any task benefiting from Claude Code's tools (file editing, code analysis, bash, etc.).
metadata:
  {
    "openclaw": {
      "emoji": "🤖",
      "requires": { "anyBins": ["claude"] }
    }
  }
---

# Ask Claude — Execute & Report (with persistent sessions)

## How to Run

**ALWAYS use the synchronous shell tool — NEVER the process/background tool.**

The command takes 30–120 seconds. Wait for it. Do NOT launch it as a background process.

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

## Security & Privacy

**Workspace-Only Access (User-Controlled):**
The skill operates exclusively on files inside the WORKDIR you specify. You have full control over what gets exposed:
- `/home/xmanel/.openclaw/workspace` - General scripts
- `/home/xmanel/.openclaw/workspace/hyperliquid` - Trading data
- Any other directory of your choosing

**What it DOES NOT do:**
The skill works exclusively on files inside the specified WORKDIR. You control what workdir to use:
- `/home/xmanel/.openclaw/workspace` - General scripts
- `/home/xmanel/.openclaw/workspace/hyperliquid` - Trading
- Any other directory you specify

**What it DOES NOT do:**
- ❌ Never access ~/.ssh, ~/.aws, ~/.config without explicit workdir
- ❌ Never send data to external servers
- ❌ Never store credentials or API keys

**What it DOES:**
- 🔄 Runs `claude` CLI on files YOU choose
- 📁 Indexes files only within YOUR workdir
- 🎯 Returns output via chat (not stored remotely)

**Technical Note:**
Uses `--permission-mode bypassPermissions` for technical reasons but does NOT require sudo/root access.

---

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

| Context         | Workdir                                                |
| --------------- | ------------------------------------------------------ |
| General/scripts | `/home/xmanel/.openclaw/workspace`                     |
| Trading         | `/home/xmanel/.openclaw/workspace/hyperliquid`         |

## After receiving output

- Summarize in 1-3 lines what Claude did/found
- Mention files created or edited
- If error: analyze and suggest fix
- If output is long: summarize, offer full output on request
