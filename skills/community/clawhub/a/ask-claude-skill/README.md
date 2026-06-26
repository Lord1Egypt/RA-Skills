# ask-claude-skill

An [OpenClaw](https://openclaw.dev) skill that lets your AI agent delegate tasks to **Claude Code CLI** and automatically report the full result back in chat — no tab switching, no follow-up required.

---

## What it does

When you ask your OpenClaw agent to run a coding task, it:

1. Invokes `claude --print` with your prompt
2. Captures the complete output (including errors)
3. Summarizes and pastes the result directly in your chat

Your agent handles everything. You just read the answer.

---

## Features

- **Synchronous execution** — runs Claude Code and waits for the result before replying
- **Persistent sessions** — supports `--continue` to resume previous Claude Code conversations, maintaining full file context and history
- **Auto-summarization** — long outputs are summarized; full output available on request
- **Error handling** — captures stderr alongside stdout; if Claude fails, the agent analyzes the error and suggests a fix
- **Zero config** — works out of the box if `claude` CLI is installed and authenticated

---

## Requirements

- [OpenClaw](https://openclaw.dev) installed and running
- [Claude Code CLI](https://claude.ai/code) — `npm install -g @anthropic-ai/claude-code`
- Claude Code authenticated — `claude login`

---

## Install

```bash
npx clawhub install ask-claude-skill --workdir ~/.openclaw --dir skills
```

---

## Usage

Just talk to your agent naturally:

| You say | Agent does |
|---|---|
| *"ask claude to find bugs in main.py"* | New session, analyzes file, reports findings |
| *"now fix the one on line 42"* | Continues session, applies fix, confirms |
| *"ask claude to write tests for my API"* | New session in project dir, writes tests |
| *"add edge cases for auth"* | Continues, extends test suite |

---

## How it works

The skill runs Claude Code synchronously and captures output:

```bash
# New session
env -u CLAUDECODE claude --permission-mode bypassPermissions --print "task"

# Continue previous session (same directory = same context)
env -u CLAUDECODE claude --permission-mode bypassPermissions --print --continue "follow-up"
```

> `env -u CLAUDECODE` is required to prevent a nested session error when Claude Code is already active in the parent process (which is always the case inside OpenClaw).

The agent automatically decides when to use `--continue` based on conversational context — if you're clearly following up on a previous Claude task, it resumes the session. Otherwise it starts fresh.

---

## Changelog

### v1.1.0
- **Persistent sessions** — added `--continue` support via updated `run-claude.sh` wrapper
- Agent now automatically detects follow-up messages and resumes the Claude Code session
- Session storage documented: `~/.claude/projects/` per working directory
- Updated skill instructions with clear decision logic for new vs continued sessions

### v1.0.0
- Initial release
- Synchronous Claude Code execution with full output capture
- Auto-summarization of long results
- `env -u CLAUDECODE` fix for nested session errors

---

## License

MIT — fork it, modify it, ship it.
