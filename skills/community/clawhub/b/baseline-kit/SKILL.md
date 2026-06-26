---
name: baseline-kit
description: Generate safer OpenClaw configuration baselines and audit existing config files for exposure, missing controls, and secret hygiene issues.
homepage: https://github.com/mike007jd/openclaw-skills/tree/main/baseline-kit
metadata: {"openclaw":{"emoji":"🧱","requires":{"bins":["node"]}}}
---

# Baseline Kit

Generate profile-based OpenClaw configuration JSON and audit an existing config before rollout.

## When to use

- You need a starting profile for `development`, `team`, `enterprise`, or `airgapped`.
- You want an offline audit for `gateway.bind`, auth rate limits, allowed skill sources, audit logging, backups, or secret-like values.
- You need a reviewable JSON artifact without contacting external services.

## Commands

```bash
node {baseDir}/bin/baseline-kit.js generate --profile enterprise --out ./openclaw.secure.json
node {baseDir}/bin/baseline-kit.js generate --profile development --out ./openclaw.dev.json
node {baseDir}/bin/baseline-kit.js audit --config ~/.openclaw/openclaw.json --format table
node {baseDir}/bin/baseline-kit.js audit --config ./openclaw.secure.json --format json
```

## Profiles

| Profile | Focus |
| --- | --- |
| `development` | Faster local iteration with lighter rate limits and shorter retention |
| `team` | Shared team defaults with moderate auth protection and audit logging |
| `enterprise` | Tighter auth windows, longer retention, and recovery guidance |
| `airgapped` | Loopback-only and local-mirror oriented settings |

## Audit checks

- `NET_EXPOSURE`: whether `gateway.bind` is loopback-only
- `AUTH_RATE_LIMIT`: whether auth rate limiting is configured completely
- `SOURCE_RESTRICTION`: whether allowed skill sources are too broad
- `AUDIT_LOGGING`: whether audit logging is enabled
- `BACKUP_HINT`: whether backup settings are present
- `SECRET_HYGIENE`: whether the config tree contains plaintext secret-like values

## Output

- Each finding includes a severity, evidence path, recommendation, and compliance tag set.
- Compliance tags currently map to `SOC2`, `ISO27001`, and `NIST CSF`.

## Boundaries

- This tool audits JSON structure only. It does not enforce runtime policy.
- Generated profiles are safer defaults, not a complete configuration management system.
