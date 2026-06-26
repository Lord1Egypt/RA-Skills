---
name: follow-builders-sidecar
description: OpenClaw-only sidecar for the original follow-builders skill. Use when the user wants to take over scheduling and delivery without modifying the upstream skill, configure digest delivery, inspect takeover status, or roll back to the original cron.
homepage: https://github.com/AMortalsOdyssey/follow-builders-sidecar
metadata:
  clawdbot:
    requires:
      bins:
        - node
        - python3
        - openclaw
    files:
      - README.md
      - README.zh-CN.md
      - SKILL.md
      - assets/*
      - config/*
      - prompts/*
      - scripts/*
    config:
      stateDirs:
        - .follow-builders-sidecar
      example: >-
        Reads ~/.follow-builders/config.json once during takeover, reuses
        OpenClaw-configured delivery accounts or optional local Feishu app
        credentials, and writes ~/.follow-builders-sidecar/config.json plus
        state.json.
---

# Follow Builders Sidecar

This skill is the external delivery/scheduling layer for the original
`follow-builders` skill.

It does **not** patch the upstream repo. It only:

- imports the original config once
- disables the original digest cron
- creates and owns its own hourly cron
- checks upstream feed commits
- builds the digest
- delivers it through OpenClaw or Feishu card

## Runtime requirements

This skill expects:

- `node` for all sidecar scripts
- `python3` for avatar circle-cropping
- `openclaw` for cron inspection, job takeover, and message delivery

It also reads and writes local files during normal operation:

- reads `~/.follow-builders/config.json` once during takeover
- writes `~/.follow-builders-sidecar/config.json`
- writes `~/.follow-builders-sidecar/state.json`
- optionally writes `~/.follow-builders-sidecar/credentials.json` for local-only direct Feishu app credentials
- can reuse OpenClaw-configured Feishu account settings when Feishu card delivery is enabled

## When to use this skill

Use this skill when the user asks to:

- install or take over from the original `follow-builders`
- switch digest delivery to the sidecar flow
- configure timezone / language / daily-vs-weekly / delivery driver
- check whether takeover worked
- disable sidecar and optionally restore the original cron

## Primary commands

### Takeover / setup

Before running setup, ask the user which Feishu card mode they want:

1. Reuse an existing OpenClaw Feishu account
2. Configure a local direct Feishu app for this sidecar

If the user chooses direct Feishu app mode, collect:

- `appId`
- `appSecret`
- `chatId`
- optional `domain` (`feishu` by default, `lark` when needed)

Run:

```bash
node scripts/sidecar-setup.js
```

Optional flags:

- `--driver openclaw_announce|feishu_card`
- `--channel <channel>`
- `--to <target>`
- `--account <accountId>`
- `--feishu-mode openclaw_account|direct_credentials`
- `--feishu-account <accountId>`
- `--feishu-chat-id <chatId>`
- `--feishu-app-id <appId>`
- `--feishu-app-secret <appSecret>`
- `--feishu-domain feishu|lark`
- `--avatar-fallback-account <accountId>`

### Configure

Run:

```bash
node scripts/sidecar-configure.js ...
```

Common flags:

- `--language zh|en|bilingual`
- `--timezone <IANA timezone>`
- `--frequency daily|weekly`
- `--weekly-day monday|...|sunday`
- `--driver openclaw_announce|feishu_card`
- `--channel <channel>`
- `--to <target>`
- `--account <accountId>`
- `--feishu-mode openclaw_account|direct_credentials`
- `--feishu-account <accountId>`
- `--feishu-chat-id <chatId>`
- `--feishu-app-id <appId>`
- `--feishu-app-secret <appSecret>`
- `--feishu-domain feishu|lark`

Important:

- After takeover, configuration belongs to the sidecar.
- Do not tell the user to keep changing the original skill's delivery time.
- If the user wants a different trigger window, tell them to edit the sidecar cron itself.

### Status

Run:

```bash
node scripts/sidecar-status.js
```

### Rollback

Run:

```bash
node scripts/sidecar-rollback.js --reenable-original
```

Use `--reenable-original` only when the user explicitly wants to restore the original cron.

## Manual test run

To test the pipeline without sending anything:

```bash
node scripts/run-sidecar.js --skip-delivery
```

## Delivery rules

- default driver is `openclaw_announce`
- optional driver is `feishu_card`
- Feishu card mode supports:
  - `openclaw_account`: reuse a Feishu app already configured in OpenClaw
  - `direct_credentials`: store a local-only Feishu `appId/appSecret/chatId` for this sidecar
- feed freshness is based on upstream GitHub commit time
- only same-local-day commits are valid
- `daily`: one successful send per local day
- `weekly`: only on the configured weekday, one successful send per week

## Upstream compatibility rules

The upstream `follow-builders` skill may evolve beyond the current three feeds.

When working with this sidecar, always treat upstream evolution as a first-class concern:

1. Before changing sidecar compatibility logic, inspect the upstream `SKILL.md`.
2. Inspect the upstream repo root for all `feed-*.json` files, not just:
   - `feed-x.json`
   - `feed-podcasts.json`
   - `feed-blogs.json`
3. If a new upstream feed appears, do **not** silently ignore it.
4. First determine whether the new feed can be handled by:
   - an existing adapter
   - a generic pass-through adapter
   - or a new dedicated adapter that must be added
5. If the sidecar cannot safely interpret the new feed schema yet, explicitly surface that limitation to the user instead of pretending nothing changed.

Design intent:

- `SKILL.md` is for agent/operator understanding
- code-level adapter/registry logic is for runtime compatibility

Do not rely on prose alone for runtime support. A note in `SKILL.md` helps the agent understand what to inspect, but actual support for a new feed still requires code or schema-level compatibility logic.

## External endpoints

The sidecar may contact these external services:

- `https://api.github.com/` to discover upstream feed files and latest relevant commits
- `https://raw.githubusercontent.com/` to load upstream feed JSON and prompts
- `https://publish.twitter.com/oembed` to expand quoted tweets
- podcast RSS hosts declared in `config/default-sources.json` to repair episode links
- `https://unavatar.io/` to fetch public avatar images
- `https://open.feishu.cn/open-apis/` or `https://open.larksuite.com/open-apis/` when Feishu card delivery is enabled

## Security and privacy

- The sidecar does not modify the upstream `follow-builders` repo.
- The sidecar does not send local files to arbitrary third-party endpoints.
- OpenClaw and Feishu routing are used only to deliver the digest the user asked for.
- Direct Feishu app credentials, when configured, stay in `~/.follow-builders-sidecar/credentials.json` and are not intended for repository storage.
- The sidecar's own local state lives under `~/.follow-builders-sidecar/`.

## Trust statement

Installing this skill means allowing it to read the user's local
`follow-builders` config once during takeover, call the upstream public feed
sources, reuse OpenClaw-configured delivery accounts or optional local direct
Feishu credentials, and optionally send digest data to OpenClaw or Feishu. Only
install it if you trust that behavior.

## Safety rules

- Never modify the original `follow-builders` repo during normal operation
- Never silently re-enable the original cron unless the user asks for rollback
- If the original cron is found enabled again during runtime, disable it and keep the sidecar as source of truth
