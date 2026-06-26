---
name: echo-memory
description: "Guide users through installing, configuring, using, and troubleshooting the EchoMemory Cloud OpenClaw Plugin. Use for plugin setup, local email OTP onboarding, manual API key fallback, local mode vs cloud mode switching, local UI startup, gateway restart checks, localhost viewer issues, normal /echo-memory command usage, and natural-language routing to current EchoMemory plugin functions."
---

# EchoMemory Plugin

Use this skill when the user is setting up, using, or debugging the EchoMemory OpenClaw plugin.

Also use it for normal EchoMemory usage requests after setup, especially when the user asks in plain language instead of naming the exact command.

Prefer the plugin's current runtime behavior over old repo habits:

- the plugin starts the local UI during `openclaw gateway` startup
- `localUiAutoOpenOnGatewayStart` defaults to `true`
- if a local UI page is already open, gateway restart should let that page reconnect and refresh instead of spawning a redundant new browser window
- packaged installs can expose a `Plugin updates` section in the local UI sidebar for version checks, release links, update actions, and gateway restart
- the `Plugin updates` section now appears at the bottom of the setup sidebar, below `Configuration`
- the top bar shows the plugin version badge beside `OpenClaw Smart Clusters`
- removing the API key from the local UI forces local-only mode for future loads
- local sync state is now kept in a stable OpenClaw-home state path so reinstalling or upgrading the plugin should not reset prior synced-file status
- sensitive files in the local UI are warning-labeled but still readable locally; the warning is for caution, not a localhost read blocker

Important install-source distinction:

- packaged installs are the intended target for in-app updates
- linked repos and local checkouts are development installs and should still be updated through local dev workflows
- do not assume the active plugin copy lives under `~/.openclaw/node_modules`; on newer OpenClaw versions the active runtime may come from `~/.openclaw/extensions`
- if the local UI looks newer than the backend behavior, check for multiple plugin copies or multiple gateway processes before assuming the repo code is active

## OpenClaw memory layout

This plugin works best when the user understands the difference between the OpenClaw workspace layout, the local UI surface, and the cloud sync surface.

Typical OpenClaw memory files:

```text
~/.openclaw/
  workspace/
    MEMORY.md
    memory/
      2026-03-17.md
      2026-03-16.md
      topics/
      private/
```

Recommended mental model:

- `workspace/MEMORY.md`: curated long-term memory and durable notes worth keeping visible
- `workspace/memory/YYYY-MM-DD.md`: daily logs and session-by-session memory capture
- `workspace/memory/topics/` or similar subfolders: topic-specific markdown files for local browsing and organization
- `workspace/memory/private/`: local private notes that may appear in the local UI scan path and should be reviewed carefully before assuming they belong in cloud sync

Important behavior difference:

- cloud sync reads top-level `.md` files from the configured `memoryDir`
- the local UI scans the wider OpenClaw workspace recursively and can show more files than the cloud sync path imports

That means a user can see a file in the local UI without that file necessarily being included in cloud sync.

## Initial setup from zero

Use this flow when the user has not installed the plugin yet.

Official references:

- OpenClaw Marketplace: `https://openclawdir.com/plugins/echomemory-ArQh3g`
- NPM package: `https://www.npmjs.com/package/@echomem/openclaw-memory`
- GitHub repo: `https://github.com/Atlas-Graph-Academy/EchoMemory-Cloud-OpenClaw-Plugin`

OpenClaw version note:

- on `2026.3.22+`, native `openclaw skills install` exists for skills, but plugin source precedence also changed
- this skill should guide plugin installs through exact local paths, `--link`, or the exact scoped npm package
- do not recommend bare `openclaw plugins install <name>` for EchoMemory because newer OpenClaw versions may resolve bare names through ClawHub first
- the published npm package is now `@echomem/openclaw-memory`, but the runtime plugin id for config and uninstall remains `echo-memory-cloud-openclaw-plugin`

Recommended setup order:

1. Confirm the user already has OpenClaw installed and can run `openclaw`.
2. Install the plugin from a published source or local repo.
3. Connect Echo Cloud from the local UI with email and OTP, or use the manual API key fallback.
4. Add the plugin config and set `tools.profile` to `"full"`.
5. Restart the gateway.
6. Verify the local UI and command surface.
7. Confirm the user understands which local markdown files are visible locally versus actually synced to cloud.

### Install options

Published package install inside the OpenClaw home directory:

```powershell
cd $HOME\.openclaw
npm install @echomem/openclaw-memory
```

Local repo install:

```powershell
openclaw plugins install "C:\Users\Your Name\Documents\GitHub\EchoMemory-Cloud-OpenClaw-Plugin"
```

Linked local repo install for active development:

```powershell
openclaw plugins install --link "C:\Users\Your Name\Documents\GitHub\EchoMemory-Cloud-OpenClaw-Plugin"
```

Important Windows pitfall:

- quote the plugin path if it contains spaces, or `openclaw plugins install` may parse the path incorrectly
- on `2026.3.22+`, avoid bare plugin names and use the exact scoped package or exact local path instead

### Cleanup and reinstall

When the user wants to remove an old install cleanly, use the exact OpenClaw uninstall command instead of describing manual cleanup first:

```powershell
openclaw plugins uninstall echo-memory-cloud-openclaw-plugin
```

Helpful variants:

- `openclaw plugins uninstall echo-memory-cloud-openclaw-plugin --dry-run`
- `openclaw plugins uninstall echo-memory-cloud-openclaw-plugin --keep-files`

`uninstall` removes the plugin entry, tracked install record, allowlist entry, and linked load path when applicable. By default it also removes the plugin install directory under OpenClaw's active extensions root.

Do not assume the active plugin always lives under `~/.openclaw/node_modules`. On newer OpenClaw versions the active install may be tracked under `~/.openclaw/extensions`.

After uninstall:

1. remove stale config ids like `plugins.entries.echomemory-cloud` if present
2. run `openclaw gateway restart`
3. reinstall from npm or the intended local path
4. run `openclaw gateway restart` again

Do not tell users that reinstalling the plugin should reset synced-file history. Current behavior is supposed to preserve sync state across versions under the OpenClaw home state directory.

### Account connection

Preferred path for first-time and returning users:

1. Open the plugin local UI and expand the `Setup` sidebar.
2. Under `Quick connect`, enter the user's email and click `Connect with email`.
3. Enter the 6-digit OTP sent by EchoMemory / Supabase.
4. The plugin and backend handle the rest:
   - existing users are verified
   - brand-new users are created through the OpenClaw path
   - the OpenClaw onboarding shortcut is applied server-side
   - a new scoped `ec_...` API key is generated automatically
   - the key is written to `~/.openclaw/.env`
   - the UI refreshes into connected mode

Generated key scope expectation:

- `memory:read`
- `memory:write`
- `ingest:write`

Manual fallback:

1. Expand `Advanced: enter API key manually` in the local UI Setup sidebar.
2. Paste an existing `ec_...` key and save local settings.
3. If the user needs to manage website keys directly, use `https://www.iditor.com/api` after login.

### Required host setup

In `~/.openclaw/openclaw.json`, set:

```json5
{
  "tools": {
    "profile": "full"
  }
}
```

The default `coding` profile is too restrictive for normal EchoMemory plugin usage.

If the user wants EchoMemory to fully replace OpenClaw's built-in memory recall, also guide them to disable the core memory tools in the same config:

```json5
{
  "tools": {
    "profile": "full",
    "deny": ["memory_search", "memory_get"]
  }
}
```

Important distinction:

- the local UI checkbox `Echo-only memory retrieval` blocks OpenClaw `memory_search` and `memory_get` at runtime after Echo cloud access is verified
- `tools.deny` in `~/.openclaw/openclaw.json` is the stronger and recommended setup when the user wants EchoMemory to fully own memory retrieval
- after adding `tools.deny`, the user should restart `openclaw gateway`

### Valid first config

Use this as the baseline cloud-mode setup for a new install:

```json5
{
  "tools": {
    "profile": "full"
  },
  "plugins": {
    "entries": {
      "echo-memory-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "apiKey": "ec_your_key_here",
          "memoryDir": "C:\\Users\\your-user\\.openclaw\\workspace\\memory",
          "autoSync": false,
          "localOnlyMode": false,
          "localUiAutoOpenOnGatewayStart": true,
          "localUiAutoInstall": true,
          "syncIntervalMinutes": 15,
          "batchSize": 10,
          "requestTimeoutMs": 300000
        }
      }
    }
  }
}
```

For the default OpenClaw layout, `memoryDir` is usually:

```text
~/.openclaw/workspace/memory
```

This is the cloud sync directory. By current plugin behavior, sync reads the top-level markdown files inside that directory.

Environment file alternative in `~/.openclaw/.env`:

```env
ECHOMEM_API_KEY=ec_your_key_here
ECHOMEM_MEMORY_DIR=C:\Users\your-user\.openclaw\workspace\memory
ECHOMEM_AUTO_SYNC=false
ECHOMEM_LOCAL_ONLY_MODE=false
ECHOMEM_LOCAL_UI_AUTO_OPEN_ON_GATEWAY_START=true
ECHOMEM_LOCAL_UI_AUTO_INSTALL=true
ECHOMEM_SYNC_INTERVAL_MINUTES=15
ECHOMEM_BATCH_SIZE=10
ECHOMEM_REQUEST_TIMEOUT_MS=300000
```

Important note:

- with the current one-click flow, users do not need to hand-edit `ECHOMEM_API_KEY`; the plugin can write it automatically after email verification

### First restart and verification

After install and config changes:

```powershell
openclaw gateway restart
```

Successful startup usually includes:

- plugin discovery succeeded
- local UI dependency install/build messages on first run if assets are missing
- `[echo-memory] Local workspace viewer: http://127.0.0.1:17823`

Successful local UI verification now also includes:

- the setup sidebar showing `Plugin updates` at the bottom
- the top bar showing the current plugin version
- packaged installs showing install-source and latest-version data inside `Plugin updates`

Recommended first smoke test order:

1. `/echo-memory whoami`
2. `/echo-memory status`
3. `/echo-memory sync`
4. `/echo-memory search <known memory topic>`

If the user is not ready for cloud setup yet, local-only mode is still valid. Read [`references/mode-switching.md`](./references/mode-switching.md).

## First checks

1. Confirm the plugin is installed or linked.

```powershell
openclaw plugins install "C:\path\to\EchoMemory-Cloud-OpenClaw-Plugin"
```

or

```powershell
openclaw plugins install --link "C:\path\to\EchoMemory-Cloud-OpenClaw-Plugin"
```

2. Confirm `tools.profile` is `"full"` in `~/.openclaw/openclaw.json`.
3. Confirm the plugin config entry exists at `plugins.entries.echo-memory-cloud-openclaw-plugin`.
4. Restart the gateway after install or config changes.

```powershell
openclaw gateway restart
```

## Mode switching

Use cloud mode when the user wants sync and retrieval from EchoMemory cloud:

- `localOnlyMode: false`
- `apiKey: "ec_..."`
- key scopes should include `ingest:write` and `memory:read`
- if they also want EchoMemory to be the only memory retrieval path, recommend `tools.deny: ["memory_search", "memory_get"]` in `~/.openclaw/openclaw.json`

Use local mode when the user only wants localhost browsing of markdown files:

- `localOnlyMode: true`
- API key can be blank
- the local UI should still be available

If the user wants to switch modes, read [`references/mode-switching.md`](./references/mode-switching.md).

## Local UI behavior

If the user asks to "view memories" and does not explicitly mention graph, public memories, or iditor.com, treat that as the local UI, not the cloud graph.

Successful gateway startup usually includes:

```text
[echo-memory] Local workspace viewer: http://127.0.0.1:17823
```

If the plugin is loaded but the user still cannot open the viewer:

1. confirm the gateway was restarted
2. confirm localhost port `17823` is listening
3. confirm `localUiAutoInstall` was not disabled before the first run
4. use the fallback script at [`scripts/start-local-ui.mjs`](./scripts/start-local-ui.mjs)

Explain the surface clearly when needed:

- the local UI is a localhost workspace browser over OpenClaw markdown files
- it can show more workspace files than the cloud sync importer uploads
- cloud mode status in the UI depends on both config and a working API client, not just the presence of a saved key string
- local UI warnings for sensitive files do not mean the file is unreadable locally; they are caution labels while the underlying localhost viewer still reads the markdown content from disk
- the setup sidebar includes a `Plugin updates` panel for packaged installs; it is not the primary update path for linked local repos
- if the update panel shows `Unknown`, `Unavailable`, or route `404` errors, verify that the running gateway is using the same plugin copy as the visible frontend

## Normal usage routing

Map normal-language requests to the current plugin surface instead of replying from generic memory or setup knowledge.

Use `echo_memory_onboard` or `/echo-memory onboard` when the user asks about:

- install or link steps
- marketplace, npm, or GitHub sources
- first-time setup from zero
- uninstall, cleanup, or clean reinstall steps
- signup, email OTP connection, local account creation, manual API key fallback
- configuration, troubleshooting, or how the plugin works
- the command list itself
- how to fully replace OpenClaw `memory_search` / `memory_get`
- what the local UI `Echo-only memory retrieval` checkbox really changes

Use `echo_memory_local_ui` or `/echo-memory view` when the user asks to:

- open, browse, launch, or get the URL for local memories
- view markdown memories on localhost
- open the workspace viewer or local UI

Use `echo_memory_search` or `/echo-memory search <query>` when the user asks:

- "what do you remember about ..."
- "search my memories for ..."
- "find my notes about ..."
- for prior facts, plans, dates, preferences, or decisions already stored in EchoMemory cloud

If the user says they enabled the local UI `Echo-only memory retrieval` option but OpenClaw still reaches for core memory tools, explicitly tell them to add `tools.deny: ["memory_search", "memory_get"]` to `~/.openclaw/openclaw.json` and restart the gateway.

If the user expects a local file to appear in cloud search, verify that the file is actually inside the sync directory and not only visible through the wider local UI workspace scan.

Use `echo_memory_status` or `/echo-memory status` when the user asks about:

- whether EchoMemory is working
- sync health, last sync, import progress, or recent imports

Use `echo_memory_sync` or `/echo-memory sync` when the user asks to:

- sync, refresh, import, upload, or push local markdown memories to the cloud

Use `/echo-memory whoami` when the user wants to verify:

- the current EchoMemory identity
- the token type
- the active scopes on the current API key

Use `echo_memory_graph_link` or graph commands when the user asks for:

- the memory graph
- the cloud graph or graph view
- an iditor.com memory page
- the public memories page

Choose the graph target carefully:

- private graph: `echo_memory_graph_link` with `visibility: private` or `/echo-memory graph`
- public memories page: `echo_memory_graph_link` with `visibility: public` or `/echo-memory graph public`

Use `/echo-memory help` when the user explicitly asks for the command list.

## Working flow

1. Install or link the plugin.
2. Set `tools.profile` to `"full"`.
3. If the user wants EchoMemory to fully replace OpenClaw memory recall, also set `tools.deny` for `memory_search` and `memory_get`.
4. Set plugin config or `~/.openclaw/.env`.
5. Restart `openclaw gateway`.
6. Verify the localhost viewer URL appears in gateway logs.
7. For cloud mode, run:

```text
/echo-memory whoami
/echo-memory status
/echo-memory sync
/echo-memory search <known topic>
```

If the user is already set up and wants a quick usage reference, read [`references/normal-usage.md`](./references/normal-usage.md).

## Configuration examples

Cloud mode:

```json5
{
  "plugins": {
    "entries": {
      "echo-memory-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "apiKey": "ec_your_key_here",
          "localOnlyMode": false,
          "memoryDir": "C:\\Users\\your-user\\.openclaw\\workspace\\memory",
          "localUiAutoOpenOnGatewayStart": true,
          "localUiAutoInstall": true
        }
      }
    }
  }
}
```

Local mode:

```json5
{
  "plugins": {
    "entries": {
      "echo-memory-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "localOnlyMode": true,
          "memoryDir": "C:\\Users\\your-user\\.openclaw\\workspace\\memory",
          "localUiAutoOpenOnGatewayStart": true,
          "localUiAutoInstall": true
        }
      }
    }
  }
}
```

Cloud mode with OpenClaw core memory tools disabled:

```json5
{
  "tools": {
    "profile": "full",
    "deny": ["memory_search", "memory_get"]
  },
  "plugins": {
    "entries": {
      "echo-memory-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "apiKey": "ec_your_key_here",
          "localOnlyMode": false,
          "memoryDir": "C:\\Users\\your-user\\.openclaw\\workspace\\memory",
          "localUiAutoOpenOnGatewayStart": true,
          "localUiAutoInstall": true,
          "disableOpenClawMemoryToolsWhenConnected": true
        }
      }
    }
  }
}
```

## References

- [`references/initial-setup.md`](./references/initial-setup.md): zero-to-working install path, account creation, config, and first verification checks
- [`references/normal-usage.md`](./references/normal-usage.md): current commands, plain-language trigger mapping, and when to use local UI versus graph
- [`references/mode-switching.md`](./references/mode-switching.md): exact local/cloud toggles, config precedence, and restart rules
- [`references/troubleshooting.md`](./references/troubleshooting.md): failure patterns for plugin discovery, local UI startup, auth, and sync
- [`scripts/start-local-ui.mjs`](./scripts/start-local-ui.mjs): manual fallback to launch the local UI when the gateway cannot start it
