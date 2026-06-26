# Local TTS Queue Config Contract

Primary config file (current environment):
- `config/tts-queue.json`

## Required keys
- `queuePath`: JSONL queue file path
- `lockPath`: lock file path
- `logPath`: worker log path

## Recommended keys
- `earconStartPath`: start-tone audio path
- `earconEndPath`: end-tone audio path
- `earconMode`: `off|once|burst|per-job` (prefer `off` or `burst` for low latency)
- `coalesceWindowMs`: debounce window for burst merge
- `maxRetries`: retry bound per queue item
- `deadLetterPath`: failed item sink
- `ttlMs`: drop items older than this age
- `priority`: lane selector (`interactive|background`)

## Behavioral guarantees
- Producer does append-only enqueue and returns immediately.
- Worker serializes dequeue ownership with lock.
- Worker handles synth+playback; producer never blocks on playback.
- Failed queue entries do not block later entries.

## Backward compatibility
- Additive key changes are preferred.
- Keep defaults safe for missing optional keys.
- Reject malformed config with clear startup error.
