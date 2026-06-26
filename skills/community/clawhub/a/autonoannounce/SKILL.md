---
name: autonoannounce
description: Build, operate, and troubleshoot Autonoannounce local speaker text-to-speech using the queued pipeline (enqueue to worker to ElevenLabs to playback backend). Requires ELEVENLABS_API_KEY for network synthesis, with optional ELEVENLABS_VOICE_ID and ELEVENLABS_MODEL_ID for voice/model selection. Writes local runtime state to config/tts-queue.json, .openclaw/*, and audio/earcons/*. Uses https://api.elevenlabs.io for synthesis/preflight calls. Use when creating or improving low-latency fire-and-forget TTS flows, tuning burst behavior, validating queue performance, enforcing local-only speech policy, or debugging queue/worker playback failures.
metadata: {"openclaw":{"skillKey":"autonoannounce","homepage":"https://github.com/ironystock/autonoannounce","requires":{"env":["ELEVENLABS_API_KEY"],"bins":["python3","curl"],"anyBins":["mpv","ffplay","afplay","paplay","powershell"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# Local TTS Queue

## Requirements
- Required credential: `ELEVENLABS_API_KEY`
- Recommended env vars: `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID`
- Runtime tools: `python3`, `curl`, and one local playback backend (`mpv`, `ffplay`, `afplay`, `paplay`, or PowerShell sound player)
- Network destination for synthesis/preflight: `https://api.elevenlabs.io`

## Overview
Use this skill to keep local speech fast, reliable, and policy-compliant by treating enqueue as fire-and-forget and isolating synthesis/playback inside the queue worker.

## Quick start workflow
1. Confirm queue health with `scripts/tts-queue-status.sh`.
2. Enqueue speech with `scripts/speak-local-queued.sh "text"`.
3. If audio does not play, inspect worker logs and runbook steps in `references/runbook.md`.
4. For latency tuning, run `scripts/benchmark-autonoannounce.sh` and compare against SLOs in `references/perf-slos.md`.

## Operating rules
- Keep the producer path non-blocking: enqueue then return immediately.
- Keep synthesis/playback in worker-only execution paths.
- Prefer fewer larger writes to the queue (coalesce bursty traffic when possible).
- Use policy-safe output lanes: local speaker for protected users; no Discord voice-file fallback.
- Treat one failed item as isolated: retry with bounds, then dead-letter; do not stall entire queue.

## Commands
- Enqueue: `scripts/speak-local-queued.sh "<text>"`
- Worker (foreground): `scripts/tts-queue-worker.sh`
- Worker daemon: `scripts/tts-queue-daemon.sh`
- Status: `scripts/tts-queue-status.sh`
- Benchmark harness: `scripts/benchmark-autonoannounce.sh`
  - Fast foreground benchmark: `scripts/benchmark-autonoannounce.sh 5`
  - Full diagnostic benchmark: `scripts/benchmark-autonoannounce.sh 5 --status both --output full`
- First-run interactive setup: `skills/autonoannounce/scripts/setup-first-run.sh` (shell wrapper)
- Cross-platform first-run CLI: `skills/autonoannounce/scripts/setup_first_run.py`
- Backend detection (OS-aware): `skills/autonoannounce/scripts/backend-detect.sh`
- ElevenLabs capability preflight: `skills/autonoannounce/scripts/elevenlabs-preflight.sh` (includes short 429 retry/backoff for SFX probe)
- Earcon library manager (durable categories/cache): `skills/autonoannounce/scripts/earcon-library.sh`
- Cross-platform playback runner: `skills/autonoannounce/scripts/play-local-audio.sh`
- Playback backend/device probe: `skills/autonoannounce/scripts/playback-probe.sh`
- Playback backend startup validator: `skills/autonoannounce/scripts/playback-validate.sh`
- Playback confirmation tone: `skills/autonoannounce/scripts/playback-test.sh`
- v0.2 smoke tests: `skills/autonoannounce/scripts/test-v0.2.sh`
- Race/concurrency stress checks: `skills/autonoannounce/scripts/race-stress.sh`

## References map
- Runbook: `references/runbook.md`
- Config contract: `references/config-contract.md`
- Performance SLOs and interpretation: `references/perf-slos.md`
- Foreground-latency optimization: `references/front-path-optimization.md`
- Durable earcon categories and cache: `references/earcon-library.md`

## Execution checklist
- Verify prerequisites (`ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `mpv`).
- Validate queue paths and lock behavior before tuning performance.
- Measure baseline before making queue/worker changes.
- Re-run benchmark after each material change.
- Record final p50/p95 latency and queue-wait deltas in the task summary.
