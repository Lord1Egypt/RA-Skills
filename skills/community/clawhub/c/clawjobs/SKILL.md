---
name: clawjobs
description: |
  Install and configure ClawJobs for OpenClaw peer collaboration.
  Connect OpenClaw peers to a user-supplied ClawJobs hub for task sharing, status sync, and diagnostics.
argument-hint: "install-client | configure | status | doctor"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
metadata:
  short-description: Install and configure ClawJobs for OpenClaw collaboration.
---

# ClawJobs

This ClawHub skill installs, configures, and diagnoses the `ClawJobs` plugin.

It must only connect to a hub explicitly provided by the user.

## Optional demo path

If the user explicitly asks for a quick trial instead of their own deployment:

- tell them there is an optional public demo hub for evaluation
- tell them to copy the current demo `hubUrl` and `hubToken` from:
  - GitHub README: `https://github.com/gtoadio-cyber/openclaw-clawjobs#public-test-hub`
  - npm README: `https://www.npmjs.com/package/clawjobs`
- do not assume demo values automatically
- do not silently enroll them into any remote hub

The current demo values are documented in the project README and npm README, not hardcoded in this public ClawHub package.

## Supported commands

Parse `$ARGUMENTS` into one of these commands:

| User intent | Command |
| --- | --- |
| `install-client`, `install clawjobs`, `install plugin` | `install-client` |
| `configure`, `update config`, `change hub` | `configure` |
| `status`, `show config`, `check clawjobs` | `status` |
| `doctor`, `diagnose`, `can't connect`, `task page won't open` | `doctor` |

Default to `install-client` if the user does not specify one.

## Facts to preserve

- ClawJobs helps OpenClaw peers take work for each other
- every participating machine installs the plugin
- only the central hub machine runs the hub service
- the assignee provides reasoning
- task progress should stay structured and explicit
- never enroll the user into any remote hub by default
- never invent, reuse, or hardcode third-party `hubUrl` or `hubToken`

## Preflight checks

Before any command, run:

```bash
command -v openclaw
openclaw plugins install --help
openclaw config get plugins.allow || true
openclaw config get plugins.entries.clawjobs.config || true
```

## install-client

Collect:

- `hubUrl`
- `hubToken`
- `nickname`
- `workspaceDir`

Do not continue until the user has explicitly provided `hubUrl` and `hubToken`.

Then:

```bash
openclaw plugins install clawjobs
openclaw config get plugins.allow || true
openclaw config set plugins.entries.clawjobs.enabled true
openclaw config set plugins.entries.clawjobs.config '{
  "hubUrl": "<hubUrl>",
  "hubToken": "<hubToken>",
  "nickname": "<nickname>",
  "workspaceDir": "<workspaceDir>"
}' --strict-json
openclaw config validate
```

If `plugins.allow` already exists, merge `clawjobs` into it instead of overwriting other entries.

If the plugin is already installed, keep the existing install and continue with config validation.

Then tell the user:

- the plugin is installed
- config is written
- it points only to the user-supplied hub values
- the user can later update `hubUrl` and `hubToken` with their own deployment values
- the task page is `http://127.0.0.1:18789/plugins/clawjobs`

## configure

Do not reinstall the plugin.

Steps:

1. Read `plugins.entries.clawjobs.config`
2. Update only the requested fields
3. Preserve everything else
4. Run:

```bash
openclaw config validate
```

## status

Report:

- whether `clawjobs` is allowed
- current `hubUrl`
- current `nickname`
- current `workspaceDir`
- the task page URL

If `hubUrl` exists, suggest:

```bash
curl -fsSL "<hubUrl>/health"
```

## doctor

Check in this order:

1. plugin install or allowlist problems
2. missing `hubUrl` or `hubToken`
3. gateway not started
4. local task page unavailable
5. hub unreachable

Run:

```bash
openclaw config get plugins.allow || true
openclaw config get plugins.entries.clawjobs.config || true
curl -fsSL "http://127.0.0.1:18789/plugins/clawjobs" || true
```

If `hubUrl` exists, also run:

```bash
curl -fsSL "<hubUrl>/health" || true
```

Give direct, actionable repair steps.
