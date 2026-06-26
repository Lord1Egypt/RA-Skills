---
name: Geode On-device Transcribe & Summary
description: Transcribe and summarize audio/video files locally. Unlimited usage at a flat rate for heavy users.
---

## GeodeCLI Transcription — OpenClaw Integration Guide

This document describes the recommended async integration between OpenClaw, `GeodeCLI`, and `Geode.app`.

Architecture:

- `GeodeCLI`: the CLI entry called by OpenClaw.
- `Geode.app`: the worker app, launched with `--worker`.
- Shared storage: the App Group container `group.com.privycloudless.privyecho`.

If the Geode app is **not installed**, OpenClaw should guide the user to install it from the Mac App Store:

- App Store URL (macOS):
  `https://apps.apple.com/app/apple-store/id6752685916?pt=127800752&ct=openclaw&mt=8`

---

## 1. Shared Paths

Both `GeodeCLI` and `Geode.app` use the same App Group container:

- App Group ID: `group.com.privycloudless.privyecho`
- Shared root:
  `~/Library/Group Containers/group.com.privycloudless.privyecho/`
- Recommended audio inbox:
  `~/Library/Group Containers/group.com.privycloudless.privyecho/CLIInbox/`
- Task JSON directory:
  `~/Library/Group Containers/group.com.privycloudless.privyecho/CLITasks/`
- Transcript / summary output directory:
  `~/Library/Group Containers/group.com.privycloudless.privyecho/CLITranscriptions/`

If the source audio is outside the shared container, copy it into `CLIInbox/` first.

---

## 2. Async API

### 2.1 Submit one task

OpenClaw should call the bundled `GeodeCLI`:

```bash
"/Applications/Geode.app/Contents/Helpers/GeodeCLI" --enqueue-transcription \
  --audio "/Users/.../Library/Group Containers/group.com.privycloudless.privyecho/CLIInbox/audio.m4a" \
  --language zh \
  [--format txt|md|docx] [--summary]
```

`GeodeCLI` auto-detects the enclosing `Geode.app` and launches `Geode --worker` automatically.

Only during development or non-default installs, you may need:

```bash
"/path/to/GeodeCLI" --enqueue-transcription \
  --audio "/Users/.../CLIInbox/audio.m4a" \
  --language zh \
  --app-bundle "/path/to/Geode.app"
```

Behavior:

- Async mode accepts **exactly one** `--audio` per task.
- `GeodeCLI` persists a task JSON file into the App Group container.
- `GeodeCLI` launches `Geode --worker` and returns immediately.

### 2.2 Success output

- **stdout**:
  `TASK_ID=<uuid>`
- **exit code**:
  `0`

Example:

```text
TASK_ID=123e4567-e89b-12d3-a456-426614174000
```

### 2.3 Error output

- `stderr`: `Error: <CODE>` plus optional English detail lines
- Exit code:
  - `1`: runtime error
  - `2`: invalid arguments

Common async-specific codes:

- `TASK_CREATE_FAILED`
- `TASK_READ_FAILED`
- `WORKER_LAUNCH_FAILED`

---

## 3. Query Status

After receiving a task id, OpenClaw should poll:

```bash
"/Applications/Geode.app/Contents/Helpers/GeodeCLI" --task-status 123e4567-e89b-12d3-a456-426614174000
```

### 3.1 Success output

- `stdout`: one JSON object
- Exit code: `0`

Example:

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "recordingId": "6a9b17c5-6c9d-4f0b-8401-f0d7f06a5e48",
  "audioPath": "/Users/.../Library/Group Containers/group.com.privycloudless.privyecho/CLIInbox/audio.m4a",
  "language": "zh",
  "outputFormat": "txt",
  "summarize": true,
  "status": "summarizing",
  "transcriptPath": "/Users/.../Library/Group Containers/group.com.privycloudless.privyecho/CLITranscriptions/audio_2026-03-18T07-00-00Z.txt",
  "summaryPath": null,
  "errorCode": null,
  "errorDetail": null,
  "workerId": "pid-12345",
  "createdAt": "2026-03-18T07:00:00Z",
  "updatedAt": "2026-03-18T07:02:10Z",
  "startedAt": "2026-03-18T07:00:02Z",
  "finishedAt": null
}
```

### 3.2 Status values

| Status | Meaning |
|--------|---------|
| `queued` | Task is persisted and waiting for a worker. |
| `running` | Transcription is in progress. |
| `summarizing` | Transcript is written; AI summary is still running. |
| `succeeded` | Task completed successfully. |
| `failed` | Task failed. Check `errorCode` / `errorDetail`. |
| `cancelled` | Reserved for future use. |

### 3.3 Task status error

- `stderr`: `Error: TASK_NOT_FOUND`
- Exit code: `1`

---

## 4. Common Error Codes

These codes may appear in task status JSON:

| Code | Meaning |
|------|---------|
| `INVALID_ARGS` | Missing required arguments or invalid usage. |
| `AUDIO_NOT_FOUND` | Audio file does not exist. |
| `AUDIO_UNREADABLE` | Audio file cannot be opened. |
| `NOT_LOGGED_IN` | User is not logged in to Geode. |
| `INSUFFICIENT_QUOTA` | Not enough transcription quota. |
| `EMPTY_RESULT` | Transcription returned no text. |
| `OUTPUT_DIR_CREATE_FAILED` | Failed to create the output directory. |
| `OUTPUT_WRITE_FAILED` | Failed to write an output file. |
| `TRANSCRIPTION_FAILED` | Internal transcription failure. |
| `SUMMARY_NOT_LOGGED_IN` | User is not logged in for AI summary. |
| `SUMMARY_INSUFFICIENT_QUOTA` | Not enough AI summary quota. |
| `SUMMARY_FAILED` | AI summary generation failed. |
| `WORKER_INTERRUPTED` | The worker stopped before finishing the task. |

---

## 5. Recommended Workflow

When the user wants to transcribe an audio file and later retrieve the result:

1. Copy the source audio into:
   `~/Library/Group Containers/group.com.privycloudless.privyecho/CLIInbox/`
2. Call:
   `/Applications/Geode.app/Contents/Helpers/GeodeCLI --enqueue-transcription --audio "P" --language <lang> [--format ...] [--summary]`
3. Read `TASK_ID=<uuid>` from stdout.
4. Poll:
   `/Applications/Geode.app/Contents/Helpers/GeodeCLI --task-status <uuid>`
5. When status becomes `succeeded`:
   - read `transcriptPath`
   - read optional `summaryPath`
   - copy result files to the user-requested destination if needed
6. When status becomes `failed`:
   - use `errorCode` for branching logic
   - use `errorDetail` for logs or user-facing context

Recommended polling behavior:

- first poll after 1 to 2 seconds
- then every 2 to 5 seconds
- stop polling when status is `succeeded`, `failed`, or `cancelled`

## 6. Summary

- OpenClaw should call the bundled `GeodeCLI` inside `Geode.app` for async submission and status polling.
- `GeodeCLI` returns `TASK_ID=<uuid>` immediately.
- `Geode.app` performs the actual transcription in `--worker` mode.
- Audio, task JSON, transcript, and summary files all live in the shared App Group container.


## 7. Agent Instructions

- This skill is designed for **asynchronous transcription**. Tasks may take a long time to complete.

### Submission behavior
- When the user requests audio transcription, use `--enqueue-transcription` to submit a task.
- Always return the `TASK_ID` immediately after submission.
- Do NOT wait for transcription to finish (non-blocking behavior).
- After submission, allow the conversation to continue normally.

### Progress & retrieval
- Only check task status when:
  - the user explicitly asks for progress or results, OR
  - you proactively decide to check in the background (without blocking the user conversation).
- Poll task status using `--task-status <TASK_ID>`.

### While task is running
- If the task is still in `queued`, `running`, or `summarizing`:
  - Inform the user that the task is still in progress.
  - Suggest checking again later.
  - Do NOT block or repeatedly poll in a tight loop.

### Completion
- When status is `succeeded`:
  - Return the `transcriptPath`.
  - Return `summaryPath` if available.

### Failure handling
- When status is `failed`:
  - Explain the failure using `errorCode`.
  - Include `errorDetail` if available.
  - Suggest corrective actions if applicable (e.g., login, quota, file issues).

### Environment handling
- If the Geode app is not installed:
  - Guide the user to install it from the App Store before retrying.
