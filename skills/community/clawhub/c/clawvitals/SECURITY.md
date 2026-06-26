# Security

## What this skill executes

Five CLI commands only:
- `openclaw security audit --json`
- `openclaw health --json`
- `openclaw --version`
- `openclaw update status --json`
- `node --version`

No other commands are issued. Args are never interpolated into shell strings.

## Network access

This skill declares no outbound network permissions and makes no network calls itself. Note: `openclaw update status --json` (one of the five commands this skill runs) may cause the OpenClaw CLI to contact its update registry. That is OpenClaw's own behaviour — the skill does not initiate or control it.

## Local storage

Nothing is stored. This skill is stateless — no config files, no usage files, no history, no identifiers.

## Reporting a vulnerability

Open an issue at [github.com/ANGUARDA/clawvitals](https://github.com/ANGUARDA/clawvitals).
