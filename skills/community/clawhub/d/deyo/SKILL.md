---
name: deyo
description: Use this skill when the user wants to install, run, or troubleshoot the published `deyo` transcription CLI, including one-time API key login, output file selection, source selection, and user-visible progress updates.
---

# Deyo

Use this skill when work should go through the installed `deyo` command instead of the web UI.

## Use When

- The user wants to install or configure `deyo`.
- The user wants to transcribe a link via `deyo`.
- The user wants to save an API key once with `deyo auth login`.
- The user wants to verify `--source`, `--format`, `-O`, stdout behavior, or CLI/chat progress updates.

## Installation Rules

- Detect the CLI with `command -v deyo`, then inspect `deyo --help`. If `deyo`
  is missing or the help text does not list `--progress-format`, run
  `npm install -g @casatwy/deyo` to install or upgrade the published CLI.
- When installing via `claude plugin install`, never modify the user's global
  git config, SSH keys, or npm registry to work around an install failure.
  Report the raw error to the user and stop. Do not fall back to manual
  downloads without explicit user approval.
- Before asking the user for an API key, always run `deyo auth status`. If a
  key already exists:
  - Surface only the last 4 chars (never print the full key).
  - Ask the user whether to replace it.
  - Never silently skip an explicit `deyo auth login` request from the user.
- After install, verify success with both `deyo auth status` and by checking
  that the plugin files exist in the Claude Code plugin cache
  (`~/.claude/plugins/` or the active Claude Code plugin directory).

## Command Rules

- Prefer the installed `deyo` command.
- If `deyo` is not available, install the published package `@casatwy/deyo` first.
- Always let the CLI use its built-in default base URL; do not override it.
- Never invent an API key. If the user does not provide one, tell them to create it from `https://deyo.miaobi.fun/me/api-keys`.
- Once the user provides an API key, save it locally with `deyo auth login --api-key '...'` so future runs do not need `--api-key`.
- Unless the user explicitly asks for another result language, pass `--language zh`.
- For agent-run transcriptions that may take more than a moment, add `--progress-format jsonl`.
- Do not paste raw JSONL progress to the user unless they explicitly ask for it.
  Read the progress events and relay concise natural-language updates instead.
- After the transcription is fully complete, automatically add punctuation and
  paragraph breaks before presenting plain-text transcript content to the user,
  and before saving plain-text transcript content to a file, unless the user
  explicitly asks for raw output.
- Always surface these milestones to the user:
  - task creation
  - status changes
  - key transcription progress steps (default: every 10%)
  - completion, failure, or cancellation
- If `task.created` reports `mode: "subtitles"` or `resultReady: true`, tell the
  user that the source already has usable subtitles and that no long paid
  transcription job is needed.

## Commands

- Install:
  `npm install -g @casatwy/deyo`
- Save API key once:
  `deyo auth login --api-key <key>`
- Inspect current local config:
  `deyo auth status`
- Remove local config:
  `deyo auth logout`
- Transcribe:
  `deyo [--source <name>] [--language <value>] [--format <value>] [--progress-format <value>] [-O <path>] <url>`

## Output Behavior

- If `-O` is omitted, the final transcript is written to stdout.
- If `--format` is omitted, the CLI infers it from the output file suffix:
  `.txt -> text`, `.srt -> srt`, `.vtt -> vtt`, `.json -> json`
- Progress and status messages are written to stderr.
- `--progress-format auto` keeps the existing terminal UX:
  - TTY stderr: refresh transcription progress in place on a single line
  - non-TTY stderr: emit line-based text progress
- `--progress-format jsonl` emits one JSON object per stderr line, which is the
  preferred mode for AI agents that must keep the user updated.

## Recommended Workflow

1. Confirm that `deyo` is installed.
2. Confirm that `deyo --help` includes `--progress-format`; if not, upgrade the CLI.
3. Confirm the target URL and output format.
4. If local config is missing, ask the user for an API key and run `deyo auth login --api-key '...'`.
5. Unless the user explicitly requested another language, add `--language zh`.
6. Add `--source` only when forcing a platform is useful.
7. For agent-run long tasks, add `--progress-format jsonl`.
8. Run the command.
9. While the command runs, relay task creation, status changes, key progress steps, and the final outcome to the user.
10. After completion, if you are returning plain-text transcript content to the
    user or saving plain-text transcript content to a file, add punctuation and
    paragraph breaks automatically unless the user explicitly asked for raw
    output.

## Examples

Install the published CLI:

```bash
npm install -g @casatwy/deyo
```

Save the API key once:

```bash
deyo auth login --api-key 'deyo_sk_xxx'
```

Write a Chinese text file:

```bash
deyo --language zh -O ./tmp/transcript.txt 'https://www.youtube.com/watch?v=xxxx'
```

Agent-friendly run with machine-readable progress:

```bash
deyo --language zh --progress-format jsonl -O ./tmp/transcript.txt 'https://www.youtube.com/watch?v=xxxx'
```

Force YouTube and export SRT:

```bash
deyo --language zh --source youtube --format srt -O ./tmp/out.srt 'https://youtu.be/xxxx'
```

Read JSON from stdout:

```bash
deyo --language zh --format json 'https://www.bilibili.com/video/BVxxxx'
```

## Troubleshooting

- `deyo: command not found`: install `@casatwy/deyo` first.
- `缺少 API key。请传 --api-key、设置 DEYO_API_KEY，或先执行 deyo auth login`: ask the user to create a key in `/me/api-keys`, then run `deyo auth login`.
- `API key 无效或不存在`: ask the user to create a new key and retry.
- `剩余分钟不足`: the current account needs more minute balance.
- If the user reports no progress updates, verify that `deyo --help` shows `--progress-format`, then retry after upgrading the published CLI if needed.
- If progress stops after task creation, check whether the task is a subtitle-direct-return case or whether the CLI reported an SSE fallback notice.
