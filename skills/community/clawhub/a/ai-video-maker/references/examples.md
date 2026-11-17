# Usage Examples

## 1) First MiniMax H3 video

Command:

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action doctor
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action quote --model minimax --payload '{"content":"A cinematic candle on a wooden table","duration":5,"resolution":"720p","tier":"turbo","aspectRatio":"16:9"}'
node "$SKILL_ROOT/scripts/run-workflow.mjs" --model minimax --maxCredits 15 --payload '{"content":"A cinematic candle on a wooden table","duration":5,"resolution":"720p","tier":"turbo","aspectRatio":"16:9"}'
```

Run generation only after the user authorizes the quoted cost. The skill polls automatically; preserve the returned task ID if it times out.

Skill runtime output:

```json
{
  "ok": true,
  "status": "COMPLETED",
  "taskId": "ckxxxxxxxx",
  "data": {
    "id": "ckxxxxxxxx",
    "output": {
      "url": "https://...",
      "msg": "The file will only be saved for 24 hours, please download it promptly."
    }
  }
}
```

Raw API create response (from `POST /api/v1/generate/{model}`):

```json
{
  "status": "SUBMITTED",
  "taskId": "ckxxxxxxxx",
  "creditsCharged": 15,
  "idempotentReplay": false,
  "responseUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx",
  "statusUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/status",
  "cancelUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/cancel"
}
```

## 2) MiniMax H3 generation

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action quote --model minimax --payload '{"content":"A cinematic sunset over a futuristic city skyline","aspectRatio":"16:9","duration":5,"resolution":"720p","tier":"turbo"}'
node "$SKILL_ROOT/scripts/run-workflow.mjs" --model minimax --maxCredits 15 --payload '{"content":"A cinematic sunset over a futuristic city skyline","aspectRatio":"16:9","duration":5,"resolution":"720p","tier":"turbo"}'
```

MiniMax also accepts `imageUrl`, `lastFrameUrl`, up to 4 `referenceImageUrls`, one `referenceVideoUrl`, and up to 2 `referenceAudioUrls`. Use frame inputs or reference assets, not both. `resolution` accepts only `720p` and `1080p`; `tier=base` adds 1 credit per second, and `referenceVideoUrl` adds a flat 2 credits.

At the published 720p Turbo rate, this 5-second request costs 15 API credits (USD $0.15). The first API key created by an account receives 50 introductory credits. API credits are separate from website subscription entitlements.

## 3) Query task status

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action getStatus --taskId ckxxxxxxxx
```

Skill runtime output:

```json
{
  "ok": true,
  "status": "PROGRESS",
  "taskId": "ckxxxxxxxx",
  "data": {
    "status": "PROGRESS"
  }
}
```

Raw API status response (from `GET /api/v1/tasks/{taskId}/status`):

```json
{
  "status": "COMPLETED"
}
```

## 4) Cancel task

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action cancelTask --taskId ckxxxxxxxx
```

Possible output:

```json
{
  "ok": true,
  "status": "CANCEL",
  "taskId": "ckxxxxxxxx",
  "data": {
    "status": "CANCEL"
  }
}
```

## 5) Handling insufficient credits

Typical API error:

```json
{
  "status": "FAILED",
  "errorCode": "INSUFFICIENT_CREDITS",
  "message": "Insufficient credits"
}
```

Skill runtime output:

```json
{
  "ok": false,
  "status": "FAILED",
  "errorCode": "INSUFFICIENT_CREDITS",
  "errorMessage": "Insufficient credits",
  "taskId": null
}
```

Recommended next actions:

- Reduce `duration` or use a lower-cost model.
- Ensure the account has enough credits.
- Retry after top-up.

The command exits with status `1` for this failure.

## 6) Handling 429 rate limit

Skill behavior:

1. Detect `429`.
2. Parse `Retry-After` if present.
3. Sleep and retry (up to max retries).
4. Return `RATE_LIMITED` when retries are exhausted.

Output example:

```json
{
  "ok": false,
  "status": "FAILED",
  "errorCode": "RATE_LIMITED",
  "errorMessage": "Rate limited by upstream API",
  "retryAfter": 2
}
```

## 7) List tasks raw API response

Endpoint:

```bash
GET /api/v1/tasks
```

Raw API response example:

```json
{
  "tasks": [
    {
      "id": "ckxxxxxxxx",
      "createdAt": "2026-03-19T08:00:00.000Z",
      "model": "t2v",
      "input": { "prompt": "...", "aspectRatio": "16:9" },
      "output": null,
      "status": "PROGRESS",
      "completedAt": null
    }
  ]
}
```

## 8) Resume after a polling timeout

A timeout returns exit status `2`, `errorCode: "POLL_TIMEOUT"`, and the existing `taskId`. Resume the existing paid task instead of submitting another create request:

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action getStatus --taskId ckxxxxxxxx
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action getTask --taskId ckxxxxxxxx
```

The workflow returns both the `taskId` and `idempotencyKey` on timeouts and errors. Preserve them together. If an external orchestrator retries creation before receiving a task ID, reuse the same `--idempotencyKey` with identical inputs.
