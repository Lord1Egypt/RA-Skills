# Codex Delegate 🔧

**Delegate coding tasks to the local Codex CLI without embedding API keys.**

## What It Does

Hands OpenClaw to a coding or repository task via the **Codex CLI** — using your existing ChatGPT authentication, not an inline API key.

- Repository analysis, summaries, and risk assessment
- Code generation and multi-file edits
- Test runs and debugging
- Code review and refactoring

## Why This Skill Exists

Embedding an OpenAI API key in agent prompts is a security risk. Codex Delegate solves this by invoking the **local `codex` CLI** which already has your ChatGPT sign-in authenticated. The wrapper script strips all API-key env vars before calling `codex exec`.

## Installation

### Prerequisites

1. **Codex CLI installed and authenticated**
   ```bash
   npm i -g codex
   codex login  # Complete ChatGPT browser sign-in
   ```

2. **OpenClaw** with the skill installed in your workspace

### Install via ClawHub

```bash
clawhub install codex-delegate
```

### Manual Install

```bash
cp -r skills/codex-delegate ~/.openclaw/workspace/skills/
```

## Usage

### Ask Jarvis to use Codex

Just say "use Codex" or "delegate to Codex" for any coding task. I'll handle the rest.

### CLI Usage (direct)

```bash
# Analysis (read-only)
codex-delegate.sh --cwd /path/to/repo --prompt "summarize the repository and list the riskiest files"

# File edits (workspace-write sandbox)
codex-delegate.sh --cwd /path/to/repo --sandbox workspace-write --prompt "Create docs/architecture.md explaining the current service layout."

# Piped context (e.g., test output)
npm test 2>&1 | codex-delegate.sh --cwd /path/to/repo --sandbox workspace-write --prompt "Summarize the failing tests and make the smallest safe fix."

# JSON event logging
codex-delegate.sh --cwd /path/to/repo --sandbox workspace-write \
  --json-log .openclaw/codex-runs/last.jsonl \
  --output .openclaw/codex-runs/last.md \
  --prompt "Review the auth changes and fix any failing tests."
```

## Sandbox Levels

| Sandbox | What it can do | When to use |
|---------|---------------|-------------|
| `read-only` | Read files, analyze, summarize | Always start here |
| `workspace-write` | Create/edit files in the repo | When edits are needed |
| `danger-full-access` | Unrestricted system access | Isolated machines only, with approval |

## Security

- **Never** passes `OPENAI_API_KEY`, `CODEX_API_KEY`, or raw tokens to Codex
- **Never** reads or reveals `~/.codex/auth.json`
- Uses saved Codex CLI authentication (ChatGPT sign-in)
- Do not use in public or untrusted chat channels
- Prefer isolated checkouts or git worktrees for write tasks

## Failure Recovery

| Error | Fix |
|-------|-----|
| `codex: command not found` | Install Codex CLI: `npm i -g codex` |
| Authentication failure | Run `codex login` with ChatGPT sign-in |
| Git repo error | Run inside a git repo, or use `--skip-git-repo-check` |
| Permission error on edits | Retry with `--sandbox workspace-write` |

## License

MIT
