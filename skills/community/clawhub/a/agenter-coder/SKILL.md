---
name: agenter-coder
description: >-
  Delegate coding tasks to a separate autonomous agent with AST validation,
  security scanning, and automatic retry. Supports 4 backends (Claude Code,
  Codex, OpenHands, Anthropic SDK) with hard budget limits on cost, tokens,
  and time. Returns structured JSON — not chat text.
tags: [coding, agent, delegation, multi-backend, validation, budget-control, autonomous, claude, codex, openhands]
user-invocable: true
metadata:
  openclaw:
    primaryEnv: ANTHROPIC_API_KEY
    requires:
      bins: [python3, uv]
    installer:
      - type: command
        command: "uv pip install agenter>=0.1.2"
---

# Agenter Coder

Instead of writing code tool-by-tool (filling your context window with file
contents), delegate to a purpose-built coding agent that runs in its own
process. It has its own tools, validates its output with AST parsing, and
comes back with structured results. Your context stays clean.

## Why this instead of coding directly

- **Your context window stays clean.** The sub-agent does all the file
  reading, editing, and bash execution in its own process. You only see
  the final result.
- **Automatic validation and retry.** Every iteration runs AST syntax checks
  (and optional Bandit security scans). If code has errors, the agent retries
  automatically — no manual back-and-forth.
- **Hard budget enforcement.** Set a dollar limit, token limit, or time limit.
  The agent stops when it hits the cap — no surprise bills.
- **Backend portability.** Same interface whether you're using Claude, GPT, or
  open-source models. Switch with one flag.

## When to use

Use this skill when the user asks to:
- Write, create, or generate code for a project
- Modify, refactor, or update existing code
- Fix bugs in a codebase
- Create entire applications or components
- Generate tests for existing code

Do NOT use for: reading files, explaining code, or answering questions. Use
your own tools for those — they don't need a sub-agent.

## How to run

```bash
python3 {SKILL_DIR}/scripts/agenter_cli.py \
  --prompt "<the coding task>" \
  --cwd "<workspace directory>" \
  --backend "anthropic-sdk" \
  --max-cost-usd 2.0 \
  --max-iterations 5 \
  --sandbox
```

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--prompt` | Yes | — | The coding task. Be specific about what to build. |
| `--cwd` | Yes | — | Working directory. Use the current workspace or a subdirectory. |
| `--backend` | No | `anthropic-sdk` | Runtime: `anthropic-sdk`, `claude-code`, `codex`, or `openhands`. |
| `--model` | No | auto | Model override (e.g., `claude-sonnet-4-20250514`, `gpt-5.4`). |
| `--max-cost-usd` | No | unlimited | Maximum spend in USD. |
| `--max-tokens` | No | unlimited | Maximum total tokens (input + output). |
| `--max-time-seconds` | No | unlimited | Maximum wall clock time. |
| `--max-iterations` | No | `5` | Max validation/retry iterations. |
| `--allowed-write-paths` | No | all in cwd | Glob patterns for allowed writes (e.g., `"*.py" "*.ts"`). |
| `--sandbox` / `--no-sandbox` | No | `--sandbox` | Sandboxed execution (recommended). |
| `--stream` | No | off | Emit NDJSON progress events for real-time updates. |

## Cost awareness

Set budget limits based on task complexity. Always tell the user the estimated cost.

| Task type | Suggested `--max-cost-usd` | Suggested `--max-iterations` |
|-----------|---------------------------|------------------------------|
| Simple script / single file | 0.50 | 3 |
| Small app / multiple files | 2.00 | 5 |
| Complex refactoring / full project | 5.00 | 7 |

## Backend selection

Default to `anthropic-sdk` unless the user asks for a specific backend. Check
`{SKILL_DIR}/references/backends.md` if the user asks about backend differences.

- **anthropic-sdk** — Default. Claude Sonnet/Opus. Works with `ANTHROPIC_API_KEY` or AWS Bedrock.
- **claude-code** — Claude Code CLI runtime. Native OS-level sandbox, battle-tested file tools.
- **codex** — OpenAI's gpt-5.4/gpt-5.4-mini. Requires `OPENAI_API_KEY`.
- **openhands** — Any model via litellm (including local). Must use `--no-sandbox`.

## Reading the output

The script outputs JSON to stdout:

```json
{
  "status": "completed",
  "summary": "Created main.py with FastAPI app and test_main.py",
  "files_modified": ["main.py", "test_main.py"],
  "files": {"main.py": "...", "test_main.py": "..."},
  "iterations": 2,
  "total_tokens": 15000,
  "total_cost_usd": 0.045,
  "total_duration_seconds": 12.3
}
```

### Status values

| Status | Meaning | What to do |
|--------|---------|------------|
| `completed` | Task succeeded, files written to disk. | Report summary and files to user. |
| `completed_with_limit_exceeded` | Task succeeded but used more resources than configured. | Report success + warn about cost. |
| `budget_exceeded` | Stopped because budget ran out before completion. | Tell user, ask if they want to retry with higher budget. |
| `refused` | The model refused the request (safety/policy). | Report refusal reason to user. |
| `failed` | Unrecoverable error. | Report error, suggest checking logs. |

## After running

1. Check the `status` field.
2. If `completed`: the files are already written to disk in `--cwd`. Use `read` to
   inspect them if the user wants to review.
3. Report the **summary**, **cost**, and **files modified** to the user.
4. If `failed` or `budget_exceeded`: report the issue and ask how to proceed.
