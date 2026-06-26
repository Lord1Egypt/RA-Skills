---
name: dlazy-chat
version: 1.2.0
description: Chat with the dlazy sandbox agent — a project-scoped assistant that runs skills end-to-end over multiple turns. Discover skills and projects with dlazy skills list / dlazy projects list.
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@1.0.9","installAlternative":"npx @dlazy/cli@1.0.9","homepage":"https://github.com/dlazyai/cli","source":"https://github.com/dlazyai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When this skill is called, use `dlazy chat`; discover ids via `dlazy skills list` and `dlazy projects list`."}}
---

# dlazy-chat

[English](./SKILL.md) · [中文](./SKILL-cn.md)


Chat with the dlazy sandbox agent — a project-scoped assistant that runs skills end-to-end over multiple turns. Discover skills and projects with `dlazy skills list` / `dlazy projects list`.

## Trigger Keywords

- chat, talk to the agent
- sandbox agent, project conversation
- continue a project, multi-turn task

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is:



```bash

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
- **npm package**: `@dlazy/cli` (pinned to `1.0.9` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.0.9 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.0.9`). Review the GitHub source before installing.

## How It Works

This skill is a thin client over the dLazy hosted sandbox agent. When you invoke it:

- Your messages and options are sent to the dLazy API (`api.dlazy.com`), which streams the agent's reply back to your terminal.
- Any local files you attach via `--files` are uploaded to dLazy's media storage (`files.dlazy.com`) first, then referenced by url.
- Chat sessions are tracked per project so follow-up turns keep context; project and skill ids come from `dlazy projects list` / `dlazy skills list`.

This is the standard SaaS pattern; the skill itself does not access network or filesystem resources beyond what the dLazy CLI already handles. See [dlazy.com](https://dlazy.com) for the full service terms.

## Usage

This skill talks to the dlazy sandbox agent — a project-scoped assistant that can run skills (templates) end-to-end. Use it for conversational, multi-turn work rather than one-shot generation.

### Discover Skills and Projects

```bash
# List the skills/templates you can start a chat with
dlazy skills list

# List existing projects in your organization
dlazy projects list
```

### Start or Continue a Chat

```bash
# Auto-select a template from your prompt (creates a new project)
dlazy chat --prompt "Make a 3-scene storyboard about a city at night"

# Start a new project with a specific skill/template
dlazy chat --skill storyboard --prompt "..."

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

1. Run `dlazy skills list` (and `dlazy projects list` when continuing work) to discover valid ids.
2. Pick `--skill` for a new project, or `--project` to continue an existing one — never both.
3. Always pass `--prompt` for non-interactive (no-TTY) runs.
4. Run `dlazy chat -h` to see every option.


## Error Handling

| Code | Error Type                         | Example Message                                                                                                          |
| ---- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                                              |
| 501  | Missing required parameter         | `error: required option '--prompt <prompt>' not specified`                                                              |
| 502  | Local file read error              | `Error: Image file/Video file not found: C:\path\to\your\file`                                                          |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"` |
| 503  | API request failed (server error)  | `HTTP status code error (500 server crash)`                                                                             |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend, for example "Prompt violates safety policy"}` |

> **AGENT CRITICAL INSTRUCTION**: 
> 1. If the execution result returns `code: "insufficient_balance"`, you MUST explicitly inform the user that their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the execution result returns `code: "unauthorized"` or indicates missing API key, you MUST inform the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it using `dlazy auth set <key>` and resume the task.

## Tips

Visit https://dlazy.com for more information.