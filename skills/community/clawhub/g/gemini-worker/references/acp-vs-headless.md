# ACP vs Headless: Why `gemini --acp` Fails and `gemini -p --yolo` Works

*Discovered 2026-03-27 during an Anthropic outage. This document exists so the next person doesn't have to figure it out from scratch.*

---

## What is ACP?

[Agent Communication Protocol (ACP)](https://agentcommunicationprotocol.dev/) is an open standard for agent-to-agent communication. It defines how an orchestrator (like OpenClaw) communicates with a worker agent (like Claude Code, Codex, or Gemini CLI) via a structured message protocol over stdin/stdout.

OpenClaw's `sessions_spawn` runtime uses ACP to manage sub-agents:

```
OpenClaw Orchestrator
       │
       │ ACP messages (JSON over stdin/stdout)
       ▼
    Sub-agent (e.g. claude --acp, codex --acp)
```

The OpenClaw `acpx` extension maps provider CLIs to ACP sessions:
- `claude --acp` → works (Claude Code supports ACP natively)
- `codex --acp` → works (Codex CLI supports ACP natively)
- `gemini --acp` → **hangs**

---

## Why `gemini --acp` Requires a TTY

Gemini CLI's `--acp` flag is documented as "AI Client Protocol mode." However, the implementation opens an **interactive REPL** that requires a terminal.

When OpenClaw's `acpx` driver tries to spawn it headlessly:

1. `gemini --acp` starts and waits for a terminal prompt
2. No TTY → the process blocks indefinitely on stdin
3. No ACP handshake messages are sent (it never reaches that code path)
4. Session hangs

You can verify this:
```bash
# Verify TTY requirement
echo '{"type":"ping"}' | gemini --acp
# → Hangs (no output)

# Compare to Claude Code (works headlessly)
echo '{"type":"ping"}' | claude --acp
# → {"type":"pong",...}
```

The root cause: Gemini CLI uses its TTY check to decide whether it's in interactive vs. pipe mode. Without a TTY, it enters a blocking wait for interactive input before ever reaching the ACP message loop.

---

## The Solution: `gemini -p --yolo`

Gemini CLI has a separate execution path via the `-p` (print) flag:

```
gemini --acp        ← Interactive REPL → requires TTY → hangs headlessly
gemini -p "prompt"  ← Single-shot execution → no TTY → works headlessly
```

The `-p` flag is designed for scripted use:
- Takes the prompt as a command-line argument
- Runs the model with the prompt
- Executes all tool calls
- Prints the final response to stdout
- Exits with code 0 on success

Add `--yolo` to auto-approve all tool calls without prompting:

```bash
# Fully headless, no interaction required
gemini -p "Summarize /path/to/doc.md" --yolo --include-directories /path/to
```

This is the pattern that works.

---

## `--include-directories` Solves Workspace Restrictions

Gemini CLI, like Claude Code, restricts file access to a workspace. By default:
- Allowed: `~/.gemini/tmp/workspace/`
- Allowed: The directory passed to `--cwd` (if any)
- Blocked: Everything else

This means `/tmp`, `/root`, your project directories — all blocked unless you grant access.

The `--include-directories` flag grants read/write access to additional paths:

```bash
gemini \
  --include-directories /root/.openclaw/workspace,/tmp/task-output \
  --yolo \
  -p "Read /root/.openclaw/workspace/spec.md and write output to /tmp/task-output/result.md"
```

**Rules:**
- Must be absolute paths
- Paths must exist before running (Gemini won't create them)
- Multiple paths: comma-separated, no spaces
- Grants both read and write access

---

## Decision Matrix: ACP vs Skill Approach

| Scenario | Use ACP | Use this skill |
|---|---|---|
| Need `web_search`, `memory_search` | ✅ | ❌ |
| Need cron, alerts, OpenClaw tools | ✅ | ❌ |
| Anthropic is down / 529 errors | ❌ | ✅ |
| Parallel worker jobs | ❌ | ✅ |
| Long-context analysis (>200K tokens) | ❌ | ✅ |
| CI pipeline / cron script | ❌ | ✅ |
| Interactive coding session | ✅ | ❌ |
| One-shot code generation | ❌ | ✅ |
| File analysis, review, audit | ❌ | ✅ |

**Short rule:** If the task needs OpenClaw-native tools → ACP. If the task is self-contained file work → this skill.

---

## What a Proper Gemini ACP Harness Would Look Like

For completeness: here's the concept for a Node.js wrapper that would make Gemini CLI speak ACP properly. This is not implemented — it's a design sketch.

```javascript
// gemini-acp-harness.js (~200 lines concept)
// Bridges OpenClaw ACP protocol ↔ Gemini -p --yolo execution

const readline = require('readline');
const { execSync, spawn } = require('child_process');

// ACP message framing (JSON-lines over stdin/stdout)
const rl = readline.createInterface({ input: process.stdin });

rl.on('line', (line) => {
  const msg = JSON.parse(line);
  
  if (msg.type === 'ping') {
    respond({ type: 'pong', version: '1.0' });
    return;
  }
  
  if (msg.type === 'run') {
    // Extract task from ACP message
    const prompt = msg.content;
    const dirs = msg.metadata?.includeDirs || [];
    
    // Build Gemini command
    const cmd = [
      'gemini',
      '--yolo',
      dirs.length ? `--include-directories ${dirs.join(',')}` : '',
      '-p', prompt
    ].filter(Boolean);
    
    // Stream output back via ACP
    const proc = spawn(cmd[0], cmd.slice(1));
    let buffer = '';
    
    proc.stdout.on('data', (chunk) => {
      buffer += chunk.toString();
      respond({ type: 'output', content: chunk.toString() });
    });
    
    proc.on('close', (code) => {
      respond({ type: 'done', exitCode: code, fullOutput: buffer });
    });
  }
});

function respond(msg) {
  process.stdout.write(JSON.stringify(msg) + '\n');
}
```

The key insight: instead of `gemini --acp` (which expects interactive TTY), the harness accepts ACP messages on its own stdin, translates them to `gemini -p` calls, and streams results back as ACP output messages.

This would enable full `sessions_spawn(runtime: "acp", ...)` integration. PRs welcome.

---

## Summary

| | `gemini --acp` | `gemini -p --yolo` |
|---|---|---|
| **TTY required** | Yes — blocks headlessly | No |
| **Headless** | ❌ Hangs | ✅ Works |
| **Tool calls** | Blocked (never reached) | Auto-approved |
| **File access** | N/A | `--include-directories` |
| **ACP protocol** | Intended but broken | Not used |
| **Practical use** | None (currently) | All agent tasks |

Until a proper ACP harness is built for Gemini CLI, `gemini -p --yolo --include-directories` is the correct pattern for headless agent use.
