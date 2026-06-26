---
name: agent-tab-title
description: Patch a locally installed OpenClaw Control UI so the browser tab title shows the active agent name (e.g. "Milly · OpenClaw") instead of the static "OpenClaw Control". Use when the user wants to disambiguate multiple OpenClaw Control UI browser tabs / Cmd-` switcher entries for multi-agent setups, asks how to make Control UI tab title dynamic, asks to install / apply / remove / re-apply this tab-title local patch, or to restore the patch after `openclaw update` overwrote dist files. Mirrors upstream PR openclaw/openclaw#80944 as a zero-build local override that survives by re-running apply.sh after each upgrade.
---

# agent-tab-title

Local OpenClaw Control UI patch: rewrites `document.title` to `<agent name> · OpenClaw`.

![agent-tab-title demo — multiple Control UI tabs disambiguated by agent name in the browser tab switcher](https://raw.githubusercontent.com/SymbolStar/SymbolStar/main/assets/agent-tab-title-demo.png)

Mirrors PR [openclaw/openclaw#80944](https://github.com/openclaw/openclaw/pull/80944) as an out-of-tree patch that edits the bundled Control UI `index.html` shipped inside the locally installed `openclaw` npm package. Survives gateway restarts; **does not** survive `openclaw update` (re-run apply after upgrades).

## When to use

- User wants per-agent browser tab titles for OpenClaw Control UI.
- User has multiple Control UI tabs open across agents and can't tell them apart.
- User wants to apply / remove / re-apply this patch.
- User just ran `openclaw update` and the tab title went back to `OpenClaw Control`.

## How it works

The Control UI is a static SPA shipped inside the npm package at:
```
<npm-global>/openclaw/dist/control-ui/index.html
```
Gateway serves it as a static file. The patch injects a ~25-line `<script>` block right before `</body>` that:
1. Polls `<openclaw-app>` Lit element every 200 ms.
2. Reads `assistantName` (preferred) or `assistantAgentId` (fallback) properties.
3. Sets `document.title` to ``<name> · OpenClaw`` (U+00B7 middle dot), or `OpenClaw Control` if no agent.

No build, no dependencies, no gateway restart — just refresh the browser tab.

## Apply / remove

```bash
# Apply (idempotent — safe to re-run after openclaw update)
bash scripts/apply.sh

# Remove (restores original index.html via .bak)
bash scripts/apply.sh --uninstall

# Custom Control UI path (auto-detect usually works)
bash scripts/apply.sh --target /path/to/openclaw/dist/control-ui/index.html
```

`apply.sh` auto-detects the Control UI `index.html` by probing, in order:

1. `OPENCLAW_CONTROL_UI_INDEX` env var
2. `--target <path>` flag
3. `$(npm root -g)/openclaw/dist/control-ui/index.html`
4. Common nvm path `~/.nvm/versions/node/*/lib/node_modules/openclaw/dist/control-ui/index.html`

On apply:
- Creates `index.html.bak` once (never overwrites an existing backup; that backup is the rollback point).
- Skips re-injection if the patch marker `openclaw-tab-title local patch` is already present.

## After `openclaw update`

`npm update` overwrites the whole `dist/` tree, including any prior backup. Re-run `bash scripts/apply.sh` — it will create a fresh backup off the new pristine file and inject the patch.

## Verify

1. Reload Control UI in browser (no gateway restart needed).
2. Switch between agents (Milly / Sherry / etc.) — tab title should update live to ``<agent> · OpenClaw``.
3. With no agent selected, title falls back to `OpenClaw Control`.

If title doesn't change, check Service Worker cache: DevTools → Application → Service Workers → Unregister → reload.
