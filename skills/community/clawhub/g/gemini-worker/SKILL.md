---
name: gemini-worker
description: >
  Run Gemini CLI as a headless worker agent for long-running or parallelizable tasks.
  Use when: (1) Anthropic API is overloaded/unavailable (529 errors) and you need a fallback
  worker, (2) spawning parallel analysis jobs that benefit from Gemini's 1M context window,
  (3) running validation, deep research, or code analysis without blocking the main agent,
  (4) any task where `gemini -p "..." --yolo --include-directories ...` is the right pattern.
  NOT for: interactive sessions, tasks requiring OpenClaw tools (web_search, memory, cron),
  or tasks needing the full agent loop.
bins:
  - gemini
requires:
  - gemini-cli
install: |
  npm install -g @google/gemini-cli
  # Authenticate once interactively (OAuth cached at ~/.gemini/oauth_creds.json):
  gemini
---

# Gemini Worker

Run Gemini CLI headlessly as a background worker. Gemini handles its own OAuth via
`~/.gemini/oauth_creds.json` — authenticate once interactively, then all headless runs
use cached credentials.

**Key insight:** `gemini --acp` requires a TTY and hangs headlessly. Use `gemini -p "..." --yolo`
instead — it takes a prompt as argument, runs to completion, and exits. See
`references/acp-vs-headless.md` for the full technical explanation.

## Quick Start

```bash
# Simple prompt
gemini -p "Your prompt here" --yolo

# With workspace access (required for file reads/writes outside ~/.gemini)
gemini \
  --include-directories /path/to/dir1,/path/to/dir2 \
  --yolo \
  -p "Your prompt here"

# Long prompts via file (recommended for >1KB prompts)
gemini \
  --include-directories /tmp/task-dir \
  --yolo \
  -p "$(cat /tmp/task-dir/prompt.txt)"
```

## Key Flags

| Flag | Purpose |
|---|---|
| `-p "..."` | **Headless mode** — prompt as argument, no TTY needed |
| `--yolo` | Auto-approve all tool calls (required for headless) |
| `--include-directories a,b` | Grant read/write access to dirs outside workspace |
| `--model gemini-2.5-pro-preview-03-25` | Override model (default: gemini-2.5-pro) |

**Critical:** Gemini CLI restricts file access to its workspace (`~/.gemini/tmp/workspace`
and `--cwd`). Use `--include-directories` to grant access to your project directories.
`/tmp` is outside the default workspace — include it explicitly if needed.

## Anthropic Fallback Pattern

When Anthropic returns `529 Overloaded`, Gemini is a capable drop-in worker:

```bash
cat > /tmp/fallback-task.txt << 'TASK'
You are a senior engineer. Read the spec at /path/to/spec.md.
Implement the feature. Write code to /path/to/output.ts.
Write a summary to /tmp/summary.md.
TASK

timeout 600 gemini \
  --include-directories /path/to/project,/tmp \
  --yolo \
  -p "$(cat /tmp/fallback-task.txt)"
```

## Parallel Workers Pattern

```bash
# Spawn 3 parallel Gemini workers
gemini --include-directories /path/to/task1 --yolo -p "$(cat /tmp/task1.txt)" > /tmp/out1.txt &
gemini --include-directories /path/to/task2 --yolo -p "$(cat /tmp/task2.txt)" > /tmp/out2.txt &
gemini --include-directories /path/to/task3 --yolo -p "$(cat /tmp/task3.txt)" > /tmp/out3.txt &
wait  # Wait for all 3
```

## Pre-fetch Pattern (WebFetchTool Workaround)

Gemini CLI's WebFetchTool is unreliable in headless mode. Pre-fetch with `curl`:

```bash
# Pre-fetch a URL to a file Gemini can read
curl -sL https://example.com/doc | python3 -c "
from html.parser import HTMLParser; import sys
class S(HTMLParser):
    def __init__(self): super().__init__(); self.t=[]
    def handle_data(self, d):
        if d.strip(): self.t.append(d.strip())
p=S(); p.feed(sys.stdin.read()); print('\n'.join(p.t[:500]))
" > /tmp/fetched-doc.txt

# Then run Gemini with access to /tmp
gemini --include-directories /tmp --yolo -p "Read /tmp/fetched-doc.txt and ..."
```

## Wrapper Script

Use `scripts/gemini-run.sh` (Linux/macOS) or `scripts/gemini-run.ps1` (Windows/PowerShell)
for timeout handling, logging, and output capture:

### Linux/macOS (bash)
```bash
scripts/gemini-run.sh /tmp/prompt.txt "/path/to/project,/tmp" /tmp/output.txt
```

### Windows (PowerShell)
```powershell
.\scripts\gemini-run.ps1 C:\tmp\prompt.txt "C:\path\to\project,C:\tmp" C:\tmp\output.txt
```

### Windows (Command Prompt)
```cmd
scripts\gemini-run.cmd C:\tmp\prompt.txt "C:\path\to\project,C:\tmp" C:\tmp\output.txt
```

## Known Limitations

- No access to OpenClaw tools (web_search, memory_search, cron, etc.)
- WebFetchTool unreliable headlessly — pre-fetch with `curl` instead
- `/tmp` outside workspace — add `--include-directories /tmp/your-dir`
- Large prompts (>4KB): write to file, reference by path in prompt
- Auth required once: run `gemini` interactively to complete OAuth, then headless works
- Output truncation: ask Gemini to write to file instead of relying on stdout for large outputs

## References

- `references/acp-vs-headless.md` — Why ACP fails, how `-p --yolo` works, decision matrix
- `references/prompt-patterns.md` — Reusable prompt templates
- `references/troubleshooting.md` — Common errors and fixes
- `scripts/gemini-run.sh` — Wrapper with timeout and error handling
