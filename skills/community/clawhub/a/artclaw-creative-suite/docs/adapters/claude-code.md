# Claude Code Adapter

Use this adapter in Claude Code.

## Execution Model

Do not use `--spawn` unless the current Claude Code environment explicitly provides an OpenClaw-compatible spawn tool.

Claude Code has two different async modes. Prefer the first one.

### Preferred: Claude Code Background Task

Use this when Claude Code's `Bash` tool supports `run_in_background`.

Run generation/workflow commands without `--no-wait` and set `run_in_background: true` on the Bash tool call. This creates a Claude Code background task visible through `/tasks`.

Example Bash tool input:

```json
{
  "command": "python3 /absolute/path/to/scripts/artclaw.py generate-image --prompt \"A cute kitten rolling on the floor\" --aspect-ratio 1:1 --resolution 2K",
  "description": "Generate ARTCLAW image",
  "run_in_background": true
}
```

**CRITICAL Rules:**

1. Use `run_in_background: true`, not a long foreground Bash timeout.
2. Do not add `--no-wait` in this mode, because the background task should wait, poll, and return the final media URL.
3. Immediately tell the user that a Claude Code background task was started.
4. The user can inspect it with `/tasks`.
5. **DO NOT manually poll with `job-status` after the background task completes.** The background task already polls internally and returns the final result in its output. When the background task completes, use the `Read` tool to read the output file path (provided in the task completion notification) to get the final result JSON.
6. **The background task output contains the complete result** including `status: "success"` and the media URL. No further polling is needed.

**Do not use `TaskOutput` to check or wait for task status.** Claude Code automatically notifies the agent when the background task finishes. After submission, simply tell the user the task was started and wait for the automatic notification.

### Fallback: ARTCLAW Server Async

**Do not use this fallback unless Claude Code's Bash tool does not support `run_in_background`.** Most Claude Code environments support it.

1. Run `python3 scripts/artclaw.py generate-* ... --no-wait` or `run-workflow ... --no-wait`.
2. Immediately tell the user the job has been submitted and include the `job_id`.
3. Use `job-status` or `last-job` only for follow-up when the user asks.
4. Do not tell the user this created a Claude Code background task; it did not.

Analysis commands are synchronous and may run normally.
