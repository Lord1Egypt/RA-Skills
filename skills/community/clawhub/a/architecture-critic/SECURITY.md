# Security & Privacy — Architecture Critic

## What this skill does with your data

**Data sent to your LLM provider:**
This skill sends the following to your configured LLM provider (e.g., Anthropic):
- The task brief (DONE_WHEN file) you provide
- A snapshot of your repository's file tree, dependency list, and recent git commits
- The critic system prompt

Your source code content, architecture details, and spec text leave your machine and are processed by your LLM provider. Review your provider's data retention and privacy policies before running this on sensitive or proprietary codebases.

**Files written locally:**
This skill writes one verdict file per run to:
`<workspace>/specialists/critic-verdicts/YYYY-MM-DD-<task-slug>.md`

No other files are created or modified.

**No other external transmission:**
No data is sent to any server other than your configured LLM provider. No telemetry, no analytics, no third-party services.

## Credentials used

This skill reads your configured LLM provider API key from:
1. `ANTHROPIC_API_KEY` environment variable (preferred), or
2. Your local `~/.openclaw/openclaw.json` config file

The key is read using safe JSON parsing — never via shell `eval`. Key values are validated against the expected format (`sk-ant-...`) before use. The key is passed directly to the Anthropic Python SDK and is never logged or written to disk.

Running this skill will incur LLM provider usage costs (approximately $0.03–$0.10 per review at current Sonnet pricing).

## Runtime requirements

- `python3` (3.8+) with `anthropic` package installed
- `bash` 4.0+
- A configured Anthropic API key (OpenAI and Gemini support planned)
- OpenClaw workspace (for verdict file path resolution)

## Prompt injection protection

Task brief content and repository files are wrapped in explicit `<untrusted_data>` delimiters in the critic prompt. The model is explicitly instructed to treat content inside those tags as data only — not as instructions. This isolates user-controlled content from the critic's system instructions.

## What this skill cannot do

- It cannot send email, make network requests, or call external APIs beyond your LLM provider
- It cannot modify your source code
- It cannot read files outside the specified repository path and OpenClaw workspace
- It cannot execute code found in your repository
