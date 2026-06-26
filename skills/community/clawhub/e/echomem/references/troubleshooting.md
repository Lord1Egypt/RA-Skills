# EchoMemory Troubleshooting

Use this reference for the common breakpoints in the plugin flow.

## Plugin installed but not behaving

Check these in order:

1. the plugin is actually installed or linked
2. `tools.profile` is `"full"` in `~/.openclaw/openclaw.json`
3. the plugin config entry key is exactly `echo-memory-cloud-openclaw-plugin`
4. `openclaw gateway restart` was run after the last change
5. there are no stale plugin entries still present under `plugins.entries`

## `plugin not found: echo-memory-cloud-openclaw-plugin`

Likely causes:

- the plugin was never installed
- the install path was not quoted on Windows
- the gateway was not restarted after install
- the package was installed globally, but not where OpenClaw discovers plugins
- the OpenClaw version is older than the plugin discovery target
- the active install is under `~/.openclaw/extensions`, but someone is only checking `node_modules`

Preferred fix:

```powershell
openclaw plugins install --link "C:\Users\Your Name\Documents\GitHub\EchoMemory-Cloud-OpenClaw-Plugin"
openclaw gateway restart
```

If discovery is still blocked, start the local UI manually with [`../scripts/start-local-ui.mjs`](../scripts/start-local-ui.mjs).

Also check for stale warnings like:

```text
plugins.entries.echomemory-cloud: plugin not found
```

That means an old config entry is still present and should be removed.

## Clean reinstall when behavior is inconsistent

Use this when the plugin is half-working, stale, or you suspect the installed build does not match the published or local source you expect.

Suggested cleanup flow:

1. `openclaw plugins uninstall echo-memory-cloud-openclaw-plugin --dry-run`
2. `openclaw plugins uninstall echo-memory-cloud-openclaw-plugin`
3. remove stale plugin config entries if any old ids remain
4. restart the gateway
5. reinstall from npm or the intended local path
6. restart the gateway again

If the user wants to keep local plugin files on disk while removing the active OpenClaw install record, use:

```powershell
openclaw plugins uninstall echo-memory-cloud-openclaw-plugin --keep-files
```

If the issue involves local UI behavior, prefer a clean reinstall before debugging deeper:

- stale frontend assets
- copied install versus linked install confusion
- old package contents still present under OpenClaw's extension path
- multiple active plugin copies under `~/.openclaw/extensions` and `~/.openclaw/node_modules`

## Local UI update panel shows `404`, `Unknown`, or mismatched version info

Likely cause:

- the frontend came from one plugin copy, but the running gateway is serving backend routes from another copy

Checks:

1. verify which active plugin path OpenClaw is actually loading
2. do not assume the runtime copy is under `~/.openclaw/node_modules`
3. check `~/.openclaw/extensions` for an older active plugin copy
4. check for duplicate gateway processes
5. confirm the active backend exposes `/api/plugin-update-status`

Interpretation:

- if the update panel renders but `plugin-update-status` returns `404`, the visible frontend is newer than the active backend
- if the install source is wrong, the gateway is likely serving a different plugin copy than the one the user expects

## Local UI does not open on gateway restart

Expected behavior:

- the service starts the local UI during gateway startup
- browser auto-open only happens on local desktop sessions

Checks:

1. find `[echo-memory] Local workspace viewer:` in gateway logs
2. verify port `17823` is listening
3. confirm `localUiAutoInstall` is not disabled before the first run
4. confirm the gateway is fully back up and not still draining from restart

Manual fallback:

```powershell
node .\echo-memory\scripts\start-local-ui.mjs
```

If the user restarted the gateway and the localhost UI server still does not return on `127.0.0.1:17823`, also check:

- whether the plugin is active from the expected install source
- whether the gateway fully restarted or left duplicate processes behind
- whether `/echo-memory view` brings the local server back up cleanly

## Local UI shows local-only mode unexpectedly

Likely causes:

1. `localOnlyMode` is still `true`
2. the API key is blank
3. `ECHOMEM_LOCAL_ONLY_MODE=true` was saved in `~/.openclaw/.env`
4. the OpenClaw plugin config is overriding what the local UI sidebar saved
5. a manually started local UI server was launched without a usable API client

Fix:

1. set `localOnlyMode` back to `false`
2. restore a valid `ec_...` API key
3. restart the gateway

Important precedence rule:

- plugin config beats `.env`
- if the sidebar writes the API key to `.env` but `openclaw.json` still says `localOnlyMode: true`, the UI can remain stuck in local mode

Manual server pitfall:

- the local UI can still show local mode if the fallback server was started without both:
  - a config with `localOnlyMode: false`
  - an initialized API client

## `/echo-memory` commands fail with authorization errors

If Slack returns `This command requires authorization`, the plugin may be loaded and OpenClaw is blocking the request.

Check:

- `channels.slack.allowFrom`
- channel-specific user allowlists
- then restart the gateway

If the failure happens immediately after config edits, also consider that the gateway may still be restarting.

## `/echo-memory sync` or search returns nothing

Check:

1. the API key includes `ingest:write` and `memory:read`
2. `memoryDir` points to the markdown directory you expect
3. the local markdown files actually exist
4. the user is testing with a known imported topic rather than a narrow literal phrase

## Version mismatch fallback

If the plugin package is installed but OpenClaw still does not discover it, check the OpenClaw version.

Observed failure pattern:

- plugin package present
- gateway restart succeeds
- local UI is not started by the plugin
- logs still imply plugin discovery failure

In that case:

1. update OpenClaw if possible
2. otherwise use [`../scripts/start-local-ui.mjs`](../scripts/start-local-ui.mjs) as a temporary fallback for the localhost UI

This fallback can get the UI working even when full plugin auto-discovery is blocked.
