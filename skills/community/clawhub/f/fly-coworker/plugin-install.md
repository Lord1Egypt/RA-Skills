# Browser-first companion installation

The v0.4.0 skill defaults to Google Chrome and reuses the v0.3.0 companion. If the companion is already loaded, skip installation and restart: open Chrome using [the browser launch procedure](references/browser-launch.md), navigate to the owning conversation, and expand its Fly dashboard.

Requires OpenClaw 2026.9.4+, Node.js 22+, and a WebGL2-capable Control UI. Install the companion from its ClawHub package listing. The package command is:

```sh
openclaw plugins install clawhub:openclaw-plugin-fly-coworker
```

Follow the installer’s registry review and capability-consent requirements. Preserve existing configuration. Enable Settings → Labs → Custom plugin UI, restart the Gateway if requested, then reload Control UI. Check `openclaw plugins info fly-coworker` and `openclaw gateway call plugins.controlUi.status --json`.

The plugin bundles its renderer and anatomical assets. It requires no standalone server, iframe, API key, or external asset host. Keep the dashboard open while the fly decides. Rounds survive a Gateway restart; an unfinished flight resumes with a new trajectory, while saved picks, exclusions and accepted handoffs persist.

If the widget fails, expand Show details. `plugins.controlUi.status` reports per-client activation failures. `openclaw gateway call plugins.controlUi.reload --params '{"pluginId":"fly-coworker"}'` reloads browser metadata without restarting the backend. Verify the actual view after recovery. A generic import error is not proof that the circuit or backend failed.

### Known Mac app / local HTTP limitation

On this host, OpenClaw Mac 2026.9.2 connected to Gateway 2026.9.4 reports **Importing a module script failed**. The Gateway issues plugin asset cookies with `Secure; HttpOnly; SameSite=None`; WebKit does not return Secure cookies over HTTP, including localhost and 127.0.0.1. A focused Chromium/WebKit comparison reproduced this difference. The complete widget interaction passes in WebKit when served by the test harness, so this is separate from renderer compatibility.

Use the Gateway's Control UI in Chrome for loopback HTTP, or an already-configured authenticated HTTPS Gateway. Do not strip Secure from production cookies or disable authentication. The native Mac window remains blocked on this host; an HTTPS deployment has not been tested here. The actual Chrome Control UI has now passed the authenticated asset-loading, render, veto, acceptance, and reload checks. Check `plugins.controlUi.status` and the actual dashboard before claiming recovery.

**Accept & start** uses authenticated `chat.send` to the owning conversation. Only the chosen task is submitted. A durable one-time claim prevents duplicate sends; a connection failure after claiming is reported as uncertain and requires checking the conversation before manually resuming.

Original plugin code is MIT; preserve THIRD_PARTY.md and LICENSES. Registry availability is verified separately from local build checks.
