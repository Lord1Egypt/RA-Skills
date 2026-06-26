---
name: airtap
description: >-
  Use this skill when the user wants to operate Airtap or complete a request
  through a mobile app on an Airtap device. It lists receivers and models,
  creates Airtap tasks, monitors them locally by default, sends follow-up
  messages, cancels tasks, updates user location, and can mirror progress
  updates into OpenClaw when needed.
metadata:
  {"clawdbot":{"emoji":"📱","requires":{"bins":["python3"],"env":["AIRTAP_PERSONAL_ACCESS_TOKEN"]},"primaryEnv":"AIRTAP_PERSONAL_ACCESS_TOKEN"}}
---

# Airtap

Use the bundled `scripts/airtap.py` CLI to interact with Airtap tasks.

## Safety

- Use this skill for Airtap or mobile-app requests that can be delegated to an Airtap device.
- Prefer `--receiver-id cloud`. Do not target a physical receiver unless the user explicitly asks
  for that device.
- `task poll` is local-only by default. Use OpenClaw delivery only when the host explicitly wants
  mirrored updates.
- Do not ask the user to paste tokens into chat. Use preconfigured environment variables or the
  local `scripts/.env` file.
- Never invent OpenClaw targets, thread IDs, reply IDs, or account scopes.

## Setup

Run commands from the skill directory.

First, sign in to `https://airtap.ai/app`, open Settings, create a personal access token, and copy
it.

Create or update `scripts/.env` with:

```bash
python3 scripts/airtap.py --add-token "your-personal-access-token"
```

Or copy the template and fill in the personal access token:

```bash
cp scripts/env.example.txt scripts/.env
```

The script loads `scripts/.env` on startup and values from that file override same-named shell
environment variables.

Requires `requests` and `python-dotenv`. If missing:

```bash
pip3 install -r requirements.txt
```

## Command Reference

Run all commands as `python3 scripts/airtap.py <resource> <action> ...`.

| Command | Use when | Notes |
| --- | --- | --- |
| `receiver get-list` | You need to choose a receiver. | Helpful before task creation. |
| `model get-list` | Model choice matters for the task. | Main Airtap choices are `airtap-1.0` and `airtap-1.0-flash`. |
| `task create` | You want to start a new task. | Add `--model-id <id>` only to override the default model. |
| `task get-list` | You need recent tasks. | Useful when you need to recover a `taskId`. |
| `task get-details` | You need a one-time task snapshot. | Useful for debugging or inspecting the final state. |
| `task poll` | You need to monitor a running task. | Polls locally by default and can optionally forward updates into OpenClaw. |
| `task add-user-message` | The task needs more input. | Use for clarification, continuation, or resuming work. |
| `task cancel` | The task should stop. | Use when the user no longer wants the task to continue. |
| `user update-location` | The task depends on user location. | Send the location as raw JSON. |

## Choosing A Model

- Only list models when model choice matters. Do not call `model get-list` for every task.
- If you do not send `modelId` during task creation, Airtap defaults to `airtap-1.0-flash`.
- `Airtap 1.0 Flash` (`airtap-1.0-flash`) is the default. Use it for shorter tasks that benefit
  from lower latency.
- `Airtap 1.0` (`airtap-1.0`) is slower. Use it for more complex tasks where better reliability
  is worth the extra latency.
- `model get-list` returns the models available to the current account. Most users see
  `airtap-1.0` and `airtap-1.0-flash`. Debug users may also see `airtap-1.0-lite`.

## Monitoring Long-Running Tasks

Airtap tasks can take a few seconds to several minutes. Treat them as long-running jobs.

1. Create the task and capture the returned `taskId`.
2. If you only need a local wait loop, call
   `python3 scripts/airtap.py task poll --task-id "<task-id>"`.
3. If the host explicitly wants OpenClaw channel updates, read `references/openclaw.md` and call
   `task poll` with `--openclaw-target` and any routing fields required for the destination
   conversation.
4. Let `task poll` keep polling until `taskState` reaches one of the states in the task-state
   glossary below.
5. Read the final JSON response from `task poll`.

`task poll` is the main monitoring command:

- It polls `task get-details` internally every 10 seconds by default.
- It stops automatically when the task completes, fails, is cancelled, or needs user input.
- It returns the same task details payload plus a `_poll` summary.
- Bare `task poll --task-id ...` only polls Airtap locally.
- OpenClaw delivery requires `--openclaw-target`.
- OpenClaw delivery is milestone-based by default: acknowledgement, one plan/start update, and the
  final or waiting-state update.
- Add `--openclaw-verbose` only when the host explicitly wants every Airtap agent update
  forwarded.
- Detailed OpenClaw routing flags and examples live in `references/openclaw.md`.

How to read the task details returned by `task poll` or `task get-details`:

- `messages` is ordered conversation history. The first message is typically the original user
  request. Later entries are usually agent updates.
- Most progress updates come from the latest `type: "agent"` message.
- Inside an agent message, inspect text parts first.
- `text` is the main progress update.
- `group` and `subGroup` are UI grouping fields that help categorize the update.
- `queuedUserMessages` may contain user follow-ups that have been accepted but not processed yet.

## Task States

- `COMPLETED`: the task finished successfully.
- `FAILED`: the task could not be completed.
- `CANCELLED`: the task was cancelled.
- `WAITING_FOR_USER_INTERVENTION`: the user must perform some action on the device.
- `WAITING_FOR_USER_INPUT`: the agent needs clarification before continuing the task.
- `WAITING_FOR_USER_CONTINUE`: the task reached the maximum step limit and needs approval to keep
  going.

## Required Agent Behavior

- If the host expects OpenClaw channel updates while Airtap is running, call `task poll` with
  `--openclaw-target` and the required routing flags. Otherwise use local-only `task poll`.
- Use milestone-only OpenClaw delivery by default. Add `--openclaw-verbose` only when the host
  explicitly wants every Airtap step forwarded.
- On `WAITING_FOR_USER_INPUT`, ask the user the needed clarification, then forward the answer with
  `task add-user-message`.
- On `WAITING_FOR_USER_INTERVENTION`, tell the user exactly what action they need to perform on the
  device, wait for confirmation, then resume with `task add-user-message`.
- On `WAITING_FOR_USER_CONTINUE`, summarize the progress so far, ask whether to continue, and if
  the user approves, resume with `task add-user-message`.
- On `COMPLETED`, summarize the result using the latest agent updates.
- On `FAILED` or `CANCELLED`, report the final state and any useful context from the latest agent
  message.
- If any Airtap API call returns `404` or another request failure, tell the user to get an updated
  version of the Airtap skill before retrying.

## Examples

Create a task with the default model:

```bash
python3 scripts/airtap.py task create --message "Open Instagram" --receiver-id cloud
```

List available models when the task is complex:

```bash
python3 scripts/airtap.py model get-list
```

Create a task with the more reliable Airtap model:

```bash
python3 scripts/airtap.py task create \
  --message "Compare the price of a product on Amazon and Zepto" \
  --receiver-id cloud \
  --model-id airtap-1.0
```

Monitor a running task locally only:

```bash
python3 scripts/airtap.py task poll --task-id "task_abc123"
```

Answer a clarification request or continue a paused task:

```bash
python3 scripts/airtap.py task add-user-message --task-id "task_abc123" --message "Continue"
```

Cancel a task:

```bash
python3 scripts/airtap.py task cancel --task-id "task_abc123"
```

## Notes

- Image attachments are supported for `task create` and `task add-user-message` via `--image-file`.
- For OpenClaw relay details and examples, read `references/openclaw.md`.
