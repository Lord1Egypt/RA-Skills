---
name: dlazy-file-to-video
version: 1.2.2
description: "ppt to video, word to video, excel to video, pdf to video, document to video — parse, outline, storyboard, voiceover, build, validate. Use when the user gives a document and wants an explainer, report broadcast, courseware, or training video."
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@1.2.1","installAlternative":"npx @dlazy/cli@1.2.1","homepage":"https://github.com/dlazyai/cli","source":"https://github.com/dlazyai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When this skill is called, run 'dlazy chat --skill file-to-video --prompt ...' for a new task, or 'dlazy chat --project <id> --prompt ...' to continue (discover ids via 'dlazy projects list'). Never pass both --skill and --project."}}
---

# file-to-video

[English](./SKILL.md) · [中文](./SKILL-cn.md)

ppt to video, word to video, excel to video, pdf to video, document to video — parse, outline, storyboard, voiceover, build, validate. Use when the user gives a document and wants an explainer, report broadcast, courseware, or training video.

## Trigger Keywords

- 文档转视频
- PPT 转视频
- PDF 讲解
- document to video
- explainer video
- 课件视频
- 报告解读

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is:

```bash
dlazy login
```

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

### Alternative: Set the Key Manually

If you already have an API key, you can save it directly:

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.

## About & Provenance

- **CLI source code**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.2.1` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.2.1 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.2.1`). Review the GitHub source before installing.

## How It Works

This skill is a thin client over the dLazy hosted sandbox agent. When you invoke it:

- Your messages and options are sent to the dLazy API (`api.dlazy.com`), which streams the agent's reply back to your terminal.
- Any local files you attach via `--files` are uploaded to dLazy's media storage (`files.dlazy.com`) first, then referenced by url.
- Chat sessions are tracked per project so follow-up turns keep context; project ids come from `dlazy projects list`.

This is the standard SaaS pattern; the skill itself does not access network or filesystem resources beyond what the dLazy CLI already handles. See [dlazy.com](https://dlazy.com) for the full service terms.

## Usage

This skill talks to the dlazy sandbox agent, **pinned to the `file-to-video` template** — a project-scoped assistant that runs the template end-to-end across multiple turns.

### Discover Projects

```bash
# List existing projects in your organization
dlazy projects list
```

### Start or Continue

```bash
# Start a new project with this template
dlazy chat --skill file-to-video --prompt "..."

# Continue an existing project (skips --skill)
dlazy chat --project <project_id> --prompt "..."

# Attach local files (uploaded to storage first)
dlazy chat --project <project_id> --prompt "Use this reference" --files ref.png

# Session control
dlazy chat --project <project_id> --clear      # drop the saved session, start fresh
dlazy chat --project <project_id> --compact    # compact the current session's context
```

On a TTY, `dlazy chat` stays interactive after the first turn — type follow-up messages, or `exit` to leave.

**CRITICAL INSTRUCTION FOR AGENT**:

1. For a new task, run `dlazy chat --skill file-to-video --prompt "..."`.
2. To continue earlier work, use `--project <id>` (find ids via `dlazy projects list`) — never pass both `--skill` and `--project`.
3. Always pass `--prompt` for non-interactive (no-TTY) runs.
4. Run `dlazy chat -h` to see every option.

## Error Handling

| Code | Error Type                         | Example Message                                                                                                          |
| ---- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                                              |
| 501  | Missing required parameter         | `error: required option '--prompt <prompt>' not specified`                                                              |
| 502  | Local file read error              | `Error: file not found: C:\path\to\your\file`                                                          |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"` |
| 503  | API request failed (server error)  | `HTTP status code error (500 server crash)`                                                                             |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend}` |

> **AGENT CRITICAL INSTRUCTION**:
> 1. If the execution result returns `code: "insufficient_balance"`, you MUST explicitly inform the user that their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the execution result returns `code: "unauthorized"` or indicates missing API key, you MUST inform the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it using `dlazy auth set <key>` and resume the task.

## Tips

Visit https://dlazy.com for more information.
