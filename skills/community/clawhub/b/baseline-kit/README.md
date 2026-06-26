# Baseline Kit

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> A baseline generator and auditor for OpenClaw configuration that pushes teams toward safer defaults.

| Item | Value |
| --- | --- |
| Package | `@mike007jd/openclaw-baseline-kit` |
| Runtime | Node.js 18+ |
| Interface | CLI + JavaScript module |
| Main commands | `generate`, `audit` |

## Why this exists

Many OpenClaw incidents are configuration problems rather than code problems. Baseline Kit helps teams start from safer profiles and then audit live configuration files for network exposure, missing controls, and obvious secret hygiene issues.

## What it does

- Generates baseline configs for `development`, `team`, `enterprise`, and `airgapped`
- Writes ready-to-review JSON files
- Audits an existing `openclaw.json`-style config
- Flags missing auth rate limits, over-broad allowed sources, missing audit logging, and more
- Associates findings with compliance tag groups such as SOC2, ISO27001, and NIST CSF

## Primary workflow

1. Generate a profile that matches the environment.
2. Review and commit the generated JSON.
3. Audit an existing config before rollout or after change review.
4. Use findings to tighten exposure, logging, and source controls.

## Quick start

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/baseline-kit
npm install
node ./bin/baseline-kit.js generate --profile enterprise --out /tmp/openclaw.json
node ./bin/baseline-kit.js audit --config ./fixtures/insecure-openclaw.json
```

## Commands

| Command | Purpose |
| --- | --- |
| `baseline-kit generate --profile <development|team|enterprise|airgapped> --out <path>` | Create a baseline JSON file |
| `baseline-kit audit --config <path>` | Audit an existing configuration file |

## Profiles

| Profile | Focus |
| --- | --- |
| `development` | Local velocity with lighter retention and rate limits |
| `team` | Shared environment defaults for small teams |
| `enterprise` | Tighter auth windows, longer audit retention, and recovery hints |
| `airgapped` | Loopback-only and local-mirror oriented settings |

## Audit coverage

- Gateway bind address and network exposure
- Authentication rate-limit completeness
- Skill source restriction quality
- Audit logging presence
- Backup hints
- Secret-like values inside config trees

## Project layout

```text
baseline-kit/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## Status

Baseline Kit is currently aimed at JSON profile generation and offline config review. It is best used as a starter baseline and policy lint step, not as a full configuration management platform.
