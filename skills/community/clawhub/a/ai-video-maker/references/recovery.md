# Recovery and delivery

## Private recovery state

For a new generation, choose a writable absolute file path in a private work
directory outside source control. Pass `--stateFile <path>` when creating.
The parent directory must already exist. The helper creates a mode-0600 file
before submitting the billable request and records the returned task ID before
waiting. It stores model, input fingerprint, approved credit limit, stable key
and timestamps; it stores no prompt, media URL, data URI or credential.
Keep the original approved inputs separately if submission recovery is needed.

An existing state file can only be reused with the same model, payload and budget.
Equivalent JSON object ordering is accepted. A different request must use a new
file and key. Do not overwrite a state file to bypass a mismatch. Existing
orchestrators can still pass their own `--idempotencyKey` without a state file,
but must persist that key themselves before submission.

```bash
# After spending approval; parent directory exists, payload is the actual approved JSON.
node "$SKILL_ROOT/scripts/run-workflow.mjs" --model minimax --payload '<approved_json>' --maxCredits <approved_limit> --stateFile <absolute_private_state_path>

# Continue waiting using saved task identity; no create, quote or spend.
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action wait --stateFile <absolute_private_state_path>

# Or wait with a known task ID, including tasks from older versions.
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action wait --taskId <task_id>
```

If interrupted after submission but before a task ID was saved, replay the
identical creation arguments with the same state file. The saved key recovers the
original server task. First-video retries also retain `first-video:<flowId>`.
Once a task ID is known, use wait/getTask; do not start a replacement.
`--maxWaitMs`, `--pollMinMs` and `--pollMaxMs` also apply to `wait`.

| Failure                                 | Next action                                                                        |
| --------------------------------------- | ---------------------------------------------------------------------------------- |
| Input validation                        | Correct fields before quoting; do not submit a malformed request                   |
| Authentication                          | Reverify or reconnect privately; never paste keys into chat                        |
| 429                                     | Respect Retry-After and backoff; retain task/key                                   |
| Ambiguous submission                    | Same state/key and identical inputs; no replacement task                           |
| Poll timeout/network failure            | `--action wait` with the existing task ID                                          |
| Completed but retrieval failed          | `--action getTask`; no new generation                                              |
| Confirmed terminal failure/cancellation | Report it. Any new generation needs its own quote and sufficient authorized budget |

Do not infer a refund from a local timeout; report only account/task facts that
were returned. Respect content refusals rather than proposing bypasses.

## Delivery

Lead with the actual playable/download URL and a brief duration/ratio/resolution
summary. Include task ID, confirmed status, known charge and the 24-hour retention
warning. Label a quote as a quote when a confirmed charge is unavailable. Do not
paste the whole runtime JSON into a normal chat reply; preserve it for automation.

When the user requests a local copy, use available authorized download tools and
return the saved path only after verifying it exists and is nonempty. If media
inspection tools are available, check actual duration/ratio, subject continuity,
cropping and motion; inspect audio/subtitles only when requested and supported.
Otherwise state that the output has not been visually inspected. This helper does
not automatically download or validate video content, so never claim it did.
