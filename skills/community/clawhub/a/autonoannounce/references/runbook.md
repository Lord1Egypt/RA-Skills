# Local TTS Queue Runbook

## 1) Validate prerequisites
- Environment:
  - `ELEVENLABS_API_KEY`
  - `ELEVENLABS_VOICE_ID` (recommended)
- Runtime:
  - local playback backend available (`mpv`, `afplay`, etc.)

Quick checks:
```bash
printenv ELEVENLABS_API_KEY | wc -c
printenv ELEVENLABS_VOICE_ID | wc -c
skills/autonoannounce/scripts/playback-probe.sh auto
skills/autonoannounce/scripts/playback-validate.sh
skills/autonoannounce/scripts/playback-test.sh
```

## 2) Run capability preflight (ElevenLabs + SFX)
```bash
skills/autonoannounce/scripts/elevenlabs-preflight.sh
```
Optional retry tuning:
```bash
SFX_MAX_RETRIES=3 SFX_BASE_DELAY_MS=250 SFX_MAX_DELAY_MS=2000 \
  skills/autonoannounce/scripts/elevenlabs-preflight.sh
```
Interpretation:
- `sfx_status="ok"` → SFX generation available now.
- `sfx_status="rate_limited"` → retries exhausted under 429 pressure; fallback to cached/local earcons.
- `sfx_status="forbidden_or_missing_permission"` → key lacks permission (or access denied).
- `sfx_status="upstream_error"` → transient server-side fault; keep local fallback and retry later.


## 3) Validate queue plumbing
```bash
scripts/tts-queue-status.sh
```
Confirm queue file, lock file, and log path exist and are writable.

## 4) Smoke test end-to-end
```bash
scripts/speak-local-queued.sh "Queue smoke test"
```
Then monitor worker log for dequeue/synth/playback completion.

## 5) Worker/startup failure triage
Common failures:
- Missing env vars: worker cannot synthesize
- Invalid/missing playback backend: synth may succeed but local playback fails
- Queue lock stale: queue appears stuck

Actions:
1. Run `skills/autonoannounce/scripts/playback-validate.sh`.
2. Fix missing dependency or choose a different backend in setup/config.
3. Restart daemon/worker.
4. Re-enqueue one test item.
5. Confirm queue drains.

## 6) Playback contract
Use `skills/autonoannounce/scripts/play-local-audio.sh <file>` as the unified local player interface.

Contract:
- Input: readable local audio file path.
- Backend resolution order: explicit flag -> config playback.backend -> auto-detect.
- Output: zero exit on successful playback, non-zero with reason on failure.

## 7) Burst latency triage
If queue wait ramps quickly during bursts:
- Reduce or disable earcons in worker critical path.
- Enable/adjust burst coalescing window.
- Add stale-item TTL for superseded chatter.
- Consider prefetching next synth while current audio plays.

## 8) Concurrency/race stress check
Run:
```bash
skills/autonoannounce/scripts/race-stress.sh
```
Expected output includes:
- `config_json_ok`
- `metadata_race_ok`
- `race_stress_ok`

## 9) Policy checks
For protected users (Brad/RECTANGL):
- Use local speaker path only.
- Do not emit Discord TTS attachments as fallback.
