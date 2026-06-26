---
name: clawlock-rank
description: >
  ClawLockRank — a leaderboard upload skill built from local ClawLock 2.2.1+ inspection results.
  Trigger only when the user explicitly wants to upload a security score, submit an inspection result,
  or sync a score to ClawLockRank. Do not trigger for normal security checks, hardening, debugging,
  dependency setup, or browsing the leaderboard only.
version: 1.1.0
metadata:
  clawlock:
    version: "1.1.0"
    homepage: "https://github.com/g1at/ClawLock-Rank"
    author: "g1at"
    compatible_with: [openclaw, zeroclaw, claude-code, generic-claw]
    platforms: [linux, macos, windows, android-termux]
    requires:
      python: ">=3.9"
      pip_package: "clawlock>=2.2.1"
      bins:
        - clawlock
      bins_optional:
        - python3
        - python
      config:
        - config.json
---

# ClawLockRank

A leaderboard upload skill built from ClawLock inspection results for the specific scenario: finish a local inspection first, then optionally publish the score to ClawLockRank.

## Install and use

```bash
python scripts/submit_score.py
python scripts/submit_score.py --preview-only
```

## Trigger boundary

Only trigger this skill when the user explicitly wants to publish a leaderboard result.

| User intent | Action |
|------------|--------|
| upload a security score / submit a leaderboard result | trigger this skill |
| run a normal security inspection / hardening / version check | hand off to the main ClawLock skill or raw `clawlock` CLI |
| only browse the leaderboard / describe the project / debug scripts | do not trigger this skill |

Common trigger phrases:
- upload security score
- upload inspection result
- submit leaderboard score
- sync my score to ClawLockRank
- upload this ClawLock result to ClawLockRank

If the user only says “start a security check” or “help me harden the setup”, prefer the main ClawLock skill instead of this one.

## Single source of truth

- Treat `clawlock scan --format json` as the only source of truth.
- Use only fields that ClawLock actually returns in JSON. Do not invent extra counters, step tables, or synthetic conclusions.
- Split the user-facing result into two layers:
  - `ClawLock results`: only restate the score, grade, adapter, version, and findings from CLI output.
  - `Impact explanation`: explain what will be uploaded and why the user may or may not want to publish it.
- If the installed `clawlock` version is lower than `2.2.1`, tell the user to upgrade before continuing.

## Privacy and upload scope

Run the inspection locally first. Upload only after explicit user confirmation.

Allowed upload fields:
- `tool`
- `clawlock_version`
- `adapter`
- `adapter_version`
- `device_fingerprint`
- `evidence_hash`
- `score`
- `grade`
- `nickname`
- `findings[].scanner`
- `findings[].level`
- `findings[].title`
- `timestamp`

Never upload:
- raw config files
- remediation text
- local file paths or `location`
- environment variables
- the full raw scan report
- `scan_history.json`

Device fingerprint rules:
- the raw `device_fingerprint` is only sent to the leaderboard Worker
- the Worker salts and hashes it before storage
- the frontend never shows the raw device fingerprint

## Recommended Claw flow

Treat the scripts as backend executors. The model owns the conversation and confirmation flow.

Before generating the preview, print one short startup message:

```text
🔍 ClawLockRank is preparing a local upload preview. Please wait...
```

Recommended order:

1. Run the preview step:

```bash
python scripts/submit_score.py --preview-only
```

2. Read the preview JSON and explain:
   - score and grade
   - adapter and version
   - finding count
   - fields that will be uploaded
   - fields that will stay local

3. Tell the user the leaderboard will show a public nickname, then ask for the nickname first:
   - empty input falls back to `Anonymous`

4. Ask for explicit upload confirmation.

5. Only after the user clearly agrees, run:

```bash
python scripts/upload.py --input <payload_path> --nickname "<nickname>" --yes
```

Use the `payload_path` returned by the preview step.

For direct terminal use, this one-shot entrypoint is still valid:

```bash
python scripts/submit_score.py
```

## Compatibility and graceful degradation

- The current leaderboard scope is OpenClaw-centric, so the script defaults to `--adapter openclaw`.
- If another adapter is needed, pass `--adapter` explicitly.
- If `clawlock scan` fails, surface the CLI error directly. Do not rewrite it into a passing state.
- If the user declines the upload, say clearly: “Upload cancelled. The local result was not sent.”
- If the Worker rejects the submission because of cooldown, stale timestamp, or rate limits, show the raw Worker error.

## Server-side restrictions

The leaderboard backend also enforces:
- a default `24` hour device cooldown
- timestamp freshness checks
- a separate IP-based rate limit
- leaderboard and vulnerability hotspot aggregation based on the latest valid result per device

## Language adaptation

- User-facing explanations should follow the user’s language.
- `clawlock scan --format json` is the structured input and does not depend on terminal text output.
- If the user explicitly runs with `CLAWLOCK_LANG=zh`, a Chinese explanation is appropriate; otherwise English is fine.
