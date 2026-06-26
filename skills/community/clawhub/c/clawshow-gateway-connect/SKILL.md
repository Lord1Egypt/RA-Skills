---
name: clawshow-gateway-connect
description: Install and activate @bowong/clawshow-gateway in OpenClaw, then migrate existing Gateway channel configuration to ClawShow with rollback safety. Use when a user wants one-step plugin install plus config migration without repeating requirements each run, applying changes via Config RPC config.apply full replace with minimal file access and no default outbound test traffic.
metadata:
  openclaw:
    primaryEnv: CLAWSHOW_AUTH_TOKEN
    requires:
      bins:
        - openclaw
---

# Clawshow Gateway Connect

Execute a safe, minimal install-and-migrate flow from current OpenClaw settings to ClawShowGateway without breaking unrelated configuration.

## Runtime Inputs

- Required: `authToken`
- Optional: `relayUrl` (default `wss://clawshow-api.bowong.cc`)
- If `authToken` is missing, ask once and stop before editing.

## Workflow

1. Install ws dependency
- Run `npm i ws` in the project root before proceeding.
- Confirm installation succeeds before continuing.

2. Identify current config source
- Search only OpenClaw gateway config files (`*.json`, `*.yaml`, `*.yml`) in the active project path.
- Do not read `.env`, secrets files, deployment manifests, or unrelated workspace files.
- Prefer editing the project-tracked config over user-global config when both exist.
- If multiple candidate files exist, pick the file currently used by the running Gateway process.

3. Create rollback copy before edits
- Save a sibling backup copy of the target config file with timestamp suffix (for example `.bak.20260313-1405`).
- Never delete the backup in the same task.

4. Check OpenClaw version gate (before plugin install)
- Query current OpenClaw version using the supported command only:
  - `openclaw version`
- Compare against `2026.3.2` using OpenClaw's version ordering.
- If current version is earlier than `2026.3.2`, upgrade OpenClaw using `openclaw update` first, then re-run:
  - `openclaw version`
- Continue only after version check/upgrade is complete.

5. Install plugin/package
- Install using OpenClaw plugin manager only:
  - `openclaw plugins install @bowong/clawshow-gateway`
- Verify installation:
  - `openclaw plugins list`
- Confirm package id is exactly `@bowong/clawshow-gateway`.
- If already installed, do not reinstall unless version repair is needed.

6. Migrate channel config to ClawShow
- Ensure package id references `@bowong/clawshow-gateway` where plugin/package declarations are required.
- Ensure channel section exists under `channels.clawshow`.
- Set:
  - `channels.clawshow.enabled: true` (required)
  - `channels.clawshow.relayUrl: "wss://clawshow-api.bowong.cc"` (optional)
  - `channels.clawshow.authToken: "<real token>"` (required)
  - `channels.clawshow.name: "ClawShow Gateway"` (required)
  - `channels.clawshow.dmPolicy: "open"` (required)
  - `channels.clawshow.allowFrom: ["*"]` (required)
- Preserve unrelated channels, plugins, and runtime options unchanged.

7. Remove conflicting legacy routing only when necessary
- If older channel config routes the same outbound traffic target, disable only the overlapping route.
- Do not remove entire legacy channel blocks unless user explicitly asks.

8. Validate config shape
- Confirm JSON/YAML syntax after edit.
- Confirm required keys exist for ClawShow (`authToken` at minimum).
- Confirm package/plugin id and channel id are consistent (`clawshow`).
- Confirm `enabled`, `relayUrl`, `authToken`, `name`, `dmPolicy`, and `allowFrom` are directly under `channels.clawshow` (no `default` layer).

9. Apply config (Config RPC only)
- Follow `Config RPC (programmatic updates)` exactly, using `config.apply (full replace)`.
- Do not use direct file-edit-only activation, `config.patch`, or manual restart as the primary path.
- Execute:
  - `openclaw gateway call config.get --params '{}'`
  - Capture `payload.hash` as `baseHash`.
  - Build the full post-migration config as one JSON5 string in `raw`.
  - `openclaw gateway call config.apply --params '{ "raw": "<full-json5-config>", "baseHash": "<hash>", "note": "migrate to @bowong/clawshow-gateway" }'`
- Respect control-plane rate limits for write RPCs (`config.apply`, `config.patch`, `update.run`): 3 requests per 60 seconds per `deviceId+clientIp`.
- If apply fails due to stale hash/conflict, call `config.get` again, rebase on newest config, and retry once.

10. Verify runtime behavior
- Do not force a manual restart here; `config.apply` already validates, writes, and restarts in one step.
- Run status/probe command if available.
- Do not send outbound test messages by default.
- Only send an external test message if the user explicitly asks for network verification.

11. Report outcome
- Include the backup file path.
- Include verification command results.
- If verification is blocked, state the blocker and provide the exact next command.

## Canonical Target Snippet

Use this structure when writing or repairing JSON config:

```json
{
  "channels": {
    "clawshow": {
      "enabled": true,
      "relayUrl": "wss://clawshow-api.bowong.cc",
      "authToken": "YOUR_CLAWSHOW_AUTH_TOKEN",
      "name": "ClawShow Gateway",
      "dmPolicy": "open",
      "allowFrom": [
        "*"
      ]
    }
  }
}
```

## Guardrails

- Keep edits minimal and reversible.
- Never invent secrets; leave placeholders for missing keys.
- Never exfiltrate secrets from local files.
- Never rewrite formatting style of the whole file.
- Never remove unrelated keys to "clean up".
