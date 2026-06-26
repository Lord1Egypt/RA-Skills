---
name: acp-background-runs
description: >
  Route requests for ACP or external coding agents such as Codex, Claude Code,
  Gemini CLI, and OpenCode into non-blocking OpenClaw background ACP runs
  instead of executing synchronously in the current chat. Use when a user wants
  to hand coding work to an external agent and expects the current conversation
  to continue without waiting. Triggers: "ACP", "Codex", "Claude Code",
  "Gemini CLI", "OpenCode", "background run", "background task".
---

# ACP / Codex Background Runs

When a user asks to use ACP or an external coding agent such as Codex, Claude Code, Gemini CLI, or OpenCode, do not execute the task synchronously in the current chat. Route it through the ACP runtime instead.

## Default Rules

- Prefer `sessions_spawn` and set `runtime: "acp"` with the appropriate `agentId`
- Default to `mode: "run"`
- Only use `thread: true` or `mode: "session"` when the user explicitly asks for an ongoing interactive or thread-bound session
- Set `cwd` when the target repository or directory is known
- Prefer absolute paths for `cwd`; do not pass `~` directly, expand it first
- Use a relaxed `runTimeoutSeconds` for longer tasks; do not mechanically default to `300`
- Do not wait in the current conversation and do not poll for progress
- Reply immediately after submission that the task has been accepted and is running in the background
- Rely on `sessions_spawn` completion notifications to send the final result back to the current conversation
- Only add `streamTo: "parent"` when the user explicitly asks for progress updates

## Default Handling

If the user is simply dispatching an ACP / Codex task and does not explicitly request a persistent interactive session, treat it as a one-shot background run. Do not block the current conversation. Send the result back only when the background run completes.

## Timeout Guidance

- Quick read-only checks, short analysis, light tasks: `runTimeoutSeconds: 120-300`
- Normal coding tasks, project inspection, small scoped edits: `runTimeoutSeconds: 600`
- Research, code changes, file generation, test runs, longer reports: `runTimeoutSeconds: 1200`
- Clearly long-running tasks: increase further to `1800-3600` as needed
- Do not default to `0`; only use `0` when the user explicitly wants no timeout

## `mode` / `thread` Decision Rules

- If the user only wants the external agent to finish a task in the background, use `mode: "run"`
- If the user explicitly wants to continue talking to the same external-agent context afterward, use `thread: true`
- If the user explicitly asks for a persistent session, thread session, or long-lived context, use both `thread: true` and `mode: "session"`
- If there is no explicit need for ongoing interaction, do not open `mode: "session"`

## `cwd` Rules

- If the target repository, project directory, or work directory is known, set `cwd`
- Prefer absolute paths
- Expand `~` before passing the path into `sessions_spawn`
- If the user did not give a directory but the task clearly targets a known repo, resolve the actual path from context before spawning

## Fallback When ACP Is Unavailable

- Try `runtime: "acp"` first
- Only fall back to `runtime: "subagent"` when the ACP target `agentId` is clearly unavailable, unconfigured, or ACP cannot be used in the current environment
- When falling back, tell the user explicitly that the task is being run via `subagent`, not a native ACP session
- Do not silently fall back

## Reply After Submission

Use this short confirmation by default:

`Task accepted. It is running in the background and will report back here when complete.`

If `streamTo: "parent"` is enabled, also say that key progress updates will be streamed back.

## Prohibited Actions

- Do not execute external coding-agent tasks synchronously in the current conversation when they should go through ACP
- Do not poll after submission
- Do not call `sessions_list`, `sessions_history`, or similar tools to track child-session progress
- Do not use `sleep` or timer-based waiting to fake background orchestration
- Rely on the `sessions_spawn` completion / announce mechanism for the final result

## Recommended Parameter Template

```json
{
  "task": "<user request>",
  "runtime": "acp",
  "agentId": "<codex|claude|gemini|opencode|...>",
  "mode": "run",
  "cwd": "/abs/path/if-known",
  "runTimeoutSeconds": 300
}
```

## When To Adjust

- Need ongoing multi-turn context: add `thread: true` and, if needed, `mode: "session"`
- Task may run for many minutes: increase `runTimeoutSeconds`
- Task is only a quick read-only check: keep `runTimeoutSeconds` small
- User explicitly wants progress relayed back: add `streamTo: "parent"`
- ACP is unavailable but the task should still run in the background: explain the fallback and use `runtime: "subagent"`
