# openclaw-gemini-worker

![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-blue?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDJMMiA3bDEwIDUgMTAtNS0xMC01ek0yIDE3bDEwIDUgMTAtNS0xMC01LTEwIDV6TTIgMTJsMTAgNSAxMC01LTEwLTUtMTAgNXoiLz48L3N2Zz4=)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-required-orange?logo=google)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Free with Google One AI Ultra](https://img.shields.io/badge/Free_with-Google_One_AI_Ultra-4285F4?logo=google)

> **What happens when Anthropic goes down at 3 AM?**
>
> You keep shipping. With Gemini.

An [OpenClaw](https://openclaw.dev) skill that turns `gemini -p --yolo` into a drop-in headless worker — for parallel jobs, long-context analysis, and Anthropic fallback.

---

## The Story

On **2026-03-27**, Anthropic's API went down. Both `claude-opus-4-6` and `claude-sonnet-4-6` started returning `529 Overloaded` for hours. Claude Max subscribers paying $200/mo were blocked.

The solution: pivot to **Google Gemini CLI**, which ships free with Google One AI Ultra.

But there was a catch.

### Why `gemini --acp` fails headlessly

OpenClaw's `sessions_spawn` runtime expects agents to communicate via [ACP (Agent Client Protocol)](https://agentcommunicationprotocol.dev/). When you map Gemini to ACP, you'd naturally reach for `gemini --acp`.

**Problem:** `gemini --acp` opens an interactive REPL. It requires a TTY. Run it headlessly and it hangs, waiting for input that never comes.

```bash
# ❌ Hangs forever — needs a TTY
gemini --acp

# ✅ Works perfectly headless
gemini -p "Your task here" --yolo
```

The `-p` flag is Gemini CLI's *print mode* — it takes a prompt as an argument, runs to completion, and exits. No TTY. No interaction. Pure worker.

### The discovery: `--include-directories`

By default, Gemini CLI restricts file access to its own workspace (`~/.gemini/tmp/workspace`). For agent tasks, you need access to your project directories.

The fix is `--include-directories`:

```bash
gemini \
  --include-directories /root/.openclaw/workspace,/tmp/my-task \
  --yolo \
  -p "Read /root/.openclaw/workspace/spec.md and implement the feature"
```

Combine `-p`, `--yolo`, and `--include-directories` and you have a fully capable headless worker with 1M token context.

---

## Install

```bash
clawhub install heintonny/gemini-worker
```

Or clone directly:

```bash
mkdir -p ~/.openclaw/workspace/skills
cd ~/.openclaw/workspace/skills
git clone https://github.com/heintonny/openclaw-gemini-worker.git gemini-worker
```

### Requirements

1. **Gemini CLI** installed:
   ```bash
   npm install -g @google/gemini-cli
   ```

2. **Authenticated once interactively** (OAuth is cached after first run):
   ```bash
   gemini  # Opens browser for OAuth — do this once
   ```
   Credentials cached at `~/.gemini/oauth_creds.json`. All subsequent headless runs use cached auth.

3. **Google One AI Ultra** subscription (or a Gemini API key)

---

## Quick Start

```bash
# One-shot analysis
gemini -p "Summarize the architecture in /tmp/docs/arch.md" \
  --include-directories /tmp/docs \
  --yolo

# Write output to file
gemini \
  --include-directories /root/.openclaw/workspace,/tmp/task \
  --yolo \
  -p "Read /tmp/task/spec.md. Implement the feature. Write code to /tmp/task/output.ts"

# With timeout (recommended for CI/agent loops)
timeout 300 gemini \
  --include-directories /path/to/project \
  --yolo \
  -p "$(cat /tmp/prompt.txt)" \
  2>&1
```

---

## ACP vs Skill: When to Use What

| | `gemini --acp` | `gemini -p --yolo` (this skill) |
|---|---|---|
| **TTY required** | ✅ Yes | ❌ No |
| **Headless** | ❌ Hangs | ✅ Works |
| **Tool calls** | Via ACP protocol | Native Gemini tools |
| **OpenClaw tools** | Via ACP bridge | ❌ Not available |
| **Best for** | Interactive dev with Claude Code-like UX | Worker jobs, parallel tasks, fallback |
| **Context window** | 1M | 1M |
| **Setup** | Needs ACP harness | Drop-in |

**Rule of thumb:** Use ACP when you need OpenClaw tools (web_search, memory, cron). Use this skill when you need headless execution, parallelism, or Anthropic is down.

---

## Patterns

### Anthropic Fallback (Drop-in Replacement)

When you get `529 Overloaded` from Anthropic:

```bash
# ❌ Was: sessions_spawn with model=sonnet (529 error)
# ✅ Now: direct Gemini worker

cat > /tmp/fallback-task.txt << 'TASK'
You are a senior TypeScript engineer. 
Read the spec at /path/to/spec.md and implement the feature.
Write the implementation to /path/to/output.ts
Write a brief summary to /tmp/summary.md
TASK

timeout 600 gemini \
  --include-directories /path/to/project,/tmp \
  --yolo \
  -p "$(cat /tmp/fallback-task.txt)"
```

### Parallel Workers

Gemini's 1M context means you can run multiple large analyses in parallel:

```bash
# Spawn 3 parallel workers
gemini --include-directories /path/to/codebase --yolo \
  -p "$(cat /tmp/task-frontend.txt)" > /tmp/out-frontend.txt &

gemini --include-directories /path/to/codebase --yolo \
  -p "$(cat /tmp/task-backend.txt)" > /tmp/out-backend.txt &

gemini --include-directories /path/to/codebase --yolo \
  -p "$(cat /tmp/task-db.txt)" > /tmp/out-db.txt &

wait  # Block until all 3 complete
echo "All workers done"
cat /tmp/out-frontend.txt /tmp/out-backend.txt /tmp/out-db.txt
```

### Pre-fetch Pattern (WebFetchTool Workaround)

Gemini CLI's WebFetchTool is unreliable in headless mode. Pre-fetch with `curl`:

```bash
# Pre-fetch documentation
curl -sL https://example.com/api-docs \
  | python3 -c "
import sys
from html.parser import HTMLParser
class S(HTMLParser):
    def __init__(self): super().__init__(); self.t=[]
    def handle_data(self, d):
        if d.strip(): self.t.append(d.strip())
p=S(); p.feed(sys.stdin.read()); print('\n'.join(p.t[:500]))
" > /tmp/fetched-docs.txt

# Now run Gemini with the pre-fetched content
gemini \
  --include-directories /tmp \
  --yolo \
  -p "Read /tmp/fetched-docs.txt and write a TypeScript SDK for this API to /tmp/sdk.ts"
```

### Long-Context Document Analysis

Gemini's 1M token window handles entire codebases:

```bash
gemini \
  --include-directories /path/to/large-repo \
  --yolo \
  -p "Read all TypeScript files in /path/to/large-repo/src. 
      Identify all places where error handling is missing. 
      Write a detailed report to /tmp/error-handling-audit.md"
```

---

## Using the Wrapper Script

The included `scripts/gemini-run.sh` adds timeouts, logging, and error handling:

```bash
# Write prompt to file
cat > /tmp/my-prompt.txt << 'PROMPT'
You are a code reviewer. Read /path/to/pr-diff.txt and write a review to /tmp/review.md.
PROMPT

# Run with wrapper
./gemini-worker/scripts/gemini-run.sh \
  /tmp/my-prompt.txt \
  "/path/to/pr-diff.txt,/tmp" \
  /tmp/review.md
```

---

## How It Works

```
OpenClaw Agent
     │
     │ exec: gemini -p "..." --yolo --include-directories ...
     ▼
Gemini CLI (headless)
     │
     ├─ Reads files via read_file tool
     ├─ Writes files via write_file tool  
     ├─ Runs code via run_bash (with --yolo)
     └─ Returns: stdout + any written files
     │
     ▼
OpenClaw Agent reads results
```

No ACP. No TTY. No intermediate server. Just a subprocess that runs to completion.

---

## Known Limitations

- **No OpenClaw tools** — Gemini can't call `web_search`, `memory_search`, or other OpenClaw tools
- **WebFetchTool unreliable** — Pre-fetch with `curl` instead (see Pre-fetch Pattern above)
- **Auth must be bootstrapped** — Run `gemini` interactively once before using headlessly
- **`/tmp` not in default workspace** — Always add `--include-directories /tmp/your-dir` if writing there
- **Large prompts** — For prompts >4KB, write to a file and use `$(cat /tmp/prompt.txt)` pattern

---

## Technical Deep Dive

See [`references/acp-vs-headless.md`](gemini-worker/references/acp-vs-headless.md) for a detailed explanation of:
- Why ACP mode requires a TTY
- The exact headless execution model
- A concept for a proper Gemini ACP harness
- Decision matrix for when to use each approach

---

## Contributing

PRs welcome. Especially:
- New prompt patterns for `references/prompt-patterns.md`
- More troubleshooting entries
- A proper Node.js ACP harness for Gemini

---

## License

MIT — see [LICENSE](LICENSE)
