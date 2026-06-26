---
name: claude-code-dispatch
description: Invoke Claude Code CLI as a subprocess for coding tasks that require file access, editing, and shell execution
version: 1.0.0
author: Claude Code (Anthropic)
triggers:
  - "use claude code"
  - "have claude fix"
  - "claude code task"
  - "run claude on"
  - "send this to claude code"
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["claude","jq"]},"install":[{"id":"claude","kind":"npm","package":"@anthropic-ai/claude-code","bins":["claude"],"label":"Install Claude Code (npm)"},{"id":"jq","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq (brew)"}]}}
---

# Claude Code Dispatch

Delegate coding tasks to Claude Code CLI. Use this when a task requires capabilities beyond what the current agent can do: file editing, shell commands, multi-file debugging, code review with file access, or any work that needs direct filesystem interaction.

## Prerequisites

Claude Code must be installed and authenticated on the host machine. The host's `~/.claude/settings.json` must pre-authorize the tools this skill will use. Example minimal config:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Glob",
      "Grep",
      "Bash(git:*)",
      "Bash(npm:*)"
    ]
  }
}
```

Without pre-authorized permissions, Claude Code will fail in non-interactive mode because it cannot prompt for approval.

## When to Use

Route tasks to Claude Code when they require:
- File reading, editing, or creation on the host filesystem
- Shell command execution (builds, tests, git operations)
- Multi-file debugging or refactoring
- Code review with actual file access
- Any task where the agent needs to interact with the local filesystem

Do NOT use when:
- The task is purely conversational (answering questions, planning)
- You can handle it with your own capabilities or other skills
- The task involves external APIs you already have access to

## Usage

```bash
bash {baseDir}/scripts/invoke-claude.sh \
  --prompt "Fix the broken import in src/App.tsx" \
  --workdir "/path/to/project" \
  --model sonnet \
  --tools "Read,Edit,Glob,Grep,Bash"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--prompt` | Yes | — | Task description for Claude Code |
| `--workdir` | Yes | — | Working directory (must exist) |
| `--model` | No | `sonnet` | Model: `sonnet`, `opus`, or `haiku` |
| `--tools` | No | `Read,Edit,Glob,Grep` | Comma-separated allowed tools |
| `--budget` | No | `2.00` | Max budget in USD (for cost reporting) |
| `--timeout` | No | `300` | Timeout in seconds |
| `--system` | No | — | Additional system prompt text |

### Model Selection Guide

- **sonnet** (default): Fast. Good for single-file fixes, simple refactors, code review, running tests.
- **opus**: Slower but more capable. Use for complex multi-file debugging, architectural changes, tasks requiring deep reasoning across many files.
- **haiku**: Fastest and cheapest. Use for trivial tasks like renaming, formatting, or simple lookups.

### Tool Presets

Common tool combinations for different task types:

- **Read-only** (code review, analysis): `Read,Glob,Grep`
- **Standard editing** (default): `Read,Edit,Glob,Grep`
- **Full access** (builds, tests, git): `Read,Edit,Glob,Grep,Bash`

## Output Format

The script returns a structured summary:

```
STATUS: success|failure
MODEL: sonnet|opus|haiku
COST: $0.04
DURATION: 12s
RESULT: <Claude Code's response>
```

Exit codes: 0 = success, 1 = Claude Code error, 2 = preflight failure, 3 = timeout.

## Examples

**Fix a build error:**
```bash
bash {baseDir}/scripts/invoke-claude.sh \
  --prompt "The build is failing with 'Cannot find module ./utils'. Diagnose and fix." \
  --workdir "/Users/dave/WebProjects/summer-camps" \
  --tools "Read,Edit,Glob,Grep,Bash"
```

**Code review:**
```bash
bash {baseDir}/scripts/invoke-claude.sh \
  --prompt "Review the changes in the last commit. Focus on correctness and security." \
  --workdir "/Users/dave/WebProjects/summer-camps" \
  --model opus \
  --tools "Read,Glob,Grep,Bash"
```

**Run tests and fix failures:**
```bash
bash {baseDir}/scripts/invoke-claude.sh \
  --prompt "Run the test suite, then fix any failing tests." \
  --workdir "/Users/dave/WebProjects/summer-camps" \
  --tools "Read,Edit,Glob,Grep,Bash" \
  --timeout 600
```

## Limitations

- **No concurrent invocations** to the same working directory. Queue tasks sequentially.
- **No multi-turn conversations.** Each invocation is independent. For follow-up work, dispatch a new invocation with more context in the prompt.
- **Result truncation.** Responses longer than 2000 characters are truncated at the nearest line boundary.

## Notes

- Cost is reported for observability. Subscription users are not charged per-token but the field shows what the task would cost on the API.
- Claude Code inherits environment variables from the host, including any API keys loaded by `load-openclaw-env` or similar scripts.
- The prompt is passed via stdin pipe, not shell interpolation, so special characters in prompts are safe.
