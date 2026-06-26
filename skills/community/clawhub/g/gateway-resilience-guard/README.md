# OpenClaw Gateway Resilience Guard

External recovery guard for OpenClaw Gateway and long-lived channel plugins such as `openclaw-weixin`.

This project is for people who run OpenClaw continuously on Linux, WSL, macOS, or Windows and need the gateway to recover from channel disconnects, network sleep/resume, and long-lived session failures without babysitting the terminal.

## Problem

OpenClaw Gateway can still be alive while an individual channel is no longer healthy. This is common after laptop sleep, Wi-Fi changes, WSL network hiccups, or long idle periods.

The WeChat plugin is especially sensitive because it depends on a long-poll `getUpdates` loop. In the upstream `Tencent/openclaw-weixin` code, the monitor has a limited retry loop and session guard:

- `monitor.ts` defines `MAX_CONSECUTIVE_FAILURES = 3` and `BACKOFF_DELAY_MS = 30_000`.
- `session-guard.ts` defines `SESSION_PAUSE_DURATION_MS = 60 * 60 * 1000` and `SESSION_EXPIRED_ERRCODE = -14`.
- Issue [Tencent/openclaw-weixin#141](https://github.com/Tencent/openclaw-weixin/issues/141) reports that after a config hot reload the monitor can end without starting again; the workaround is `openclaw gateway restart`.
- Issue [Tencent/openclaw-weixin#155](https://github.com/Tencent/openclaw-weixin/issues/155) reports that `errcode=-14` can enter a 60-minute session pause loop and block outbound messages.

This watchdog does not replace the official plugin. It is an external safety net: when the gateway or channel stops behaving like a live system, it restarts the gateway with guardrails.

## Design

The script uses a layered health model before it restarts anything:

| Layer | Probe | Purpose |
| --- | --- | --- |
| Gateway | `openclaw gateway status --json --require-rpc`, local health URL, local TCP port, service/process fallback | Detect whether OpenClaw Gateway is down or locally unreachable. |
| Channel | `openclaw health --json --verbose`, `openclaw status --deep`, optional `openclaw channels status --probe`, then URL fallback | Prefer OpenClaw's own per-channel health model, then fall back to a configured URL when native probes are unavailable. |
| Runtime diagnostics | `openclaw models status --json`, `openclaw logs --plain`, warning classification | Separate provider, proxy/network, auth/rate-limit, gateway, channel-session, config reload, and task-runtime evidence before choosing an action. |
| Model API, optional | `openclaw agent --json` with the configured model provider | Detect whether the configured model path is timing out while Gateway and channels still look healthy. Disabled by default because it makes real model calls. |
| Network | multiple independent URLs, default Baidu/QQ/Weixin | Avoid restarting the gateway during whole-machine or ISP network failure. |

Only gateway failures restart immediately. Channel failures go through confirmation, network split-brain protection, exponential backoff, and restart-rate limits.
Model probe failures default to evidence logging only; users can opt in to restart or a custom command after consecutive failures.

## Recovery Policy

- Gateway down: restart immediately.
- Gateway running but channel probe fails: confirm with general network probes.
- General network also fails: do nothing except wait; restarting will not fix an offline machine.
- General network works but channel stays down: wait with exponential backoff, re-check, then restart.
- OpenClaw warning logs: classify and record evidence first; default action is log-only.
- Five consecutive successful channel probes reset the failure state.
- Restart storm protection limits gateway restarts per hour.
- Night hours can use a slower probe interval to reduce noise.

## Files

| File | Purpose |
| --- | --- |
| `gateway-watchdog.sh` | Main daemon loop: probes, backoff, restart decisions, log rotation, single-instance lock. |
| `gateway-watchdog.ps1` | Windows-native daemon loop for Task Scheduler. |
| `dashboard/` | Standalone local Web UI and API served by the watchdog, independent of Gateway. |
| `openclaw-plugin/` | Optional native OpenClaw plugin bridge that redirects `/resilience-guard` to the standalone dashboard. |
| `install-watchdog.sh` | Linux/WSL/macOS installer: copies files, writes config, creates systemd user service or macOS LaunchAgent. |
| `install-watchdog.ps1` | Windows installer: creates config and a Task Scheduler job. |
| `uninstall-watchdog.sh` | Stops and removes the service and installed scripts. |
| `uninstall-watchdog.ps1` | Windows uninstaller. |
| `SKILL.md` | ClawHub/OpenClaw skill metadata and operator instructions. |
| `README.zh-CN.md` | Chinese documentation. |

## Install

Install from ClawHub:

```bash
clawhub install gateway-resilience-guard
```

Or use this repository directly.

Linux, WSL, or macOS:

```bash
bash install-watchdog.sh
```

For unattended install:

```bash
bash install-watchdog.sh --yes
```

For a custom channel probe:

```bash
bash install-watchdog.sh --channel-url "https://your-channel.example.com/health"
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-watchdog.ps1
```

## Dashboard

The installer enables a standalone local dashboard:

```text
http://127.0.0.1:18790/
```

This dashboard is served by the watchdog, not by OpenClaw Gateway. If Gateway is down, the dashboard can still open and show the last known evidence.

It includes:

- Gateway, channel, network, OpenClaw log, and model-provider status.
- Category charts for provider timeout, proxy/network, rate-limit, auth, channel session, Gateway degraded, config reload, and task runtime warnings.
- Sidebar view switching for Overview, Trends, Strategy, Logs, and Config so monitoring, actions, and detail evidence are separated.
- Local design-system controls: native semantic selects, buttons, badges, and guarded controls styled consistently without relying on CDN or component-script upgrades.
- Denser page composition: trend digest and latest signals, strategy matrix and manual actions, config runtime map.
- Event trend chart with separate lanes for API failures, log warnings, successful model probes, and healthy diagnostics.
- Chinese/English language switching and Light, Dark, Ocean, and Forest themes.
- Status-file freshness checks so stale data is obvious.
- Quick strategy buttons: observe, overnight diagnosis, channel recovery, and conservative circuit breaker.
- Guarded actions with an unlock flow: run diagnostics, restart Gateway, apply presets, and export a diagnostic JSON bundle.

Dashboard actions are bound to localhost and protected with the generated `DASHBOARD_TOKEN`. The token is injected only into the same-origin dashboard page. A random token is written during install; the value is not shown in logs.

Optional OpenClaw plugin bridge:

```bash
openclaw plugins install ./openclaw-plugin
openclaw plugins enable resilience-guard
openclaw gateway restart
```

Then open the Gateway route while Gateway is healthy:

```text
http://127.0.0.1:18789/resilience-guard
```

That route redirects to the external dashboard. It is a convenience entry only; the external dashboard remains the recovery entry when Gateway is unavailable.

The installer writes:

- scripts to `~/.local/share/openclaw-gateway-watchdog`;
- config to `~/.config/openclaw-gateway-watchdog/watchdog.env`;
- logs to `~/.local/state/openclaw-gateway-watchdog/watchdog.log`;
- a Linux/WSL user service to `~/.config/systemd/user/gateway-watchdog.service`;
- a macOS LaunchAgent to `~/Library/LaunchAgents/ai.clawhub.gateway-resilience-guard.plist`;
- a Windows scheduled task named `OpenClaw Gateway Resilience Guard`.

If user systemd is unavailable, the installer starts a direct background fallback process and stores its pid in the state directory.

## Manage

```bash
systemctl --user status gateway-watchdog
journalctl --user -u gateway-watchdog -f
systemctl --user restart gateway-watchdog
bash ~/.local/share/openclaw-gateway-watchdog/uninstall-watchdog.sh
```

macOS:

```bash
launchctl print gui/$(id -u)/ai.clawhub.gateway-resilience-guard
tail -f ~/.local/state/openclaw-gateway-watchdog/watchdog.log
bash ~/.local/share/openclaw-gateway-watchdog/uninstall-watchdog.sh
```

Windows:

```powershell
Get-ScheduledTask -TaskName "OpenClaw Gateway Resilience Guard"
Get-Content "$env:LOCALAPPDATA\openclaw-gateway-watchdog\watchdog.log" -Wait
powershell -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\openclaw-gateway-watchdog\uninstall-watchdog.ps1"
```

Remove config and logs too:

```bash
bash ~/.local/share/openclaw-gateway-watchdog/uninstall-watchdog.sh --purge
```

## Configuration

Most users can keep the generated defaults. Advanced settings live in:

```text
~/.config/openclaw-gateway-watchdog/watchdog.env
```

Common keys:

```bash
GATEWAY_SERVICE="openclaw-gateway"
GATEWAY_HEALTH_URL="http://127.0.0.1:18789/healthz"
GATEWAY_HOST="127.0.0.1"
GATEWAY_PORT="18789"
CHANNEL_URL="https://ilinkai.weixin.qq.com"
NETWORK_URLS="https://www.baidu.com https://www.qq.com https://api.weixin.qq.com"
RESTART_COMMAND="systemctl --user restart openclaw-gateway"
OPENCLAW_NATIVE_PROBES="auto"
OPENCLAW_HEALTH_TIMEOUT_MS="12000"
OPENCLAW_GATEWAY_STRICT="0"
OPENCLAW_CHANNELS_PROBE="1"
OPENCLAW_DIAG_ENABLED="1"
OPENCLAW_DIAG_INTERVAL="300"
OPENCLAW_LOG_SCAN_ENABLED="1"
OPENCLAW_LOG_LIMIT="200"
OPENCLAW_LOG_SIGNAL_LIMIT="40"
OPENCLAW_LOG_TIMEOUT_MS="15000"
OPENCLAW_LOG_WARN_PATTERNS="fetch failed|fetch timeout|LLM idle timeout|model silent|..."
OPENCLAW_DIAG_ACTION="log"
OPENCLAW_DIAG_FAILURES_BEFORE_ACTION="2"
OPENCLAW_DIAG_COMMAND=""
DASHBOARD_ENABLED="1"
DASHBOARD_HOST="127.0.0.1"
DASHBOARD_PORT="18790"
DASHBOARD_ACTIONS_ENABLED="1"
DASHBOARD_TOKEN="generated-at-install"
DASHBOARD_DIR="~/.local/share/openclaw-gateway-watchdog/dashboard"
MODEL_PROBE_ENABLED="0"
MODEL_EDGE_PROBE_ENABLED="1"
MODEL_PROBE_INTERVAL="1800"
MODEL_PROBE_TIMEOUT="120"
MODEL_PROBE_FAILURES_BEFORE_ACTION="2"
MODEL_PROBE_ACTION="log"
MODEL_PROBE_COMMAND=""
MODEL_PROBE_MODEL=""
MODEL_PROBE_THINKING="off"
MODEL_PROBE_SESSION_ID="watchdog-model-probe"
MODEL_PROBE_MESSAGE="Reply with exactly OK."
BASE_INTERVAL="60"
NIGHT_INTERVAL="300"
MAX_INTERVAL="1800"
CHANNEL_FAILURES_BEFORE_RESTART="2"
SUCCESS_COUNT_TO_RESET="5"
MAX_RESTARTS_PER_HOUR="6"
```

Use `RESTART_COMMAND` if your OpenClaw install is not managed by a user-level systemd unit. Example:

```bash
RESTART_COMMAND="openclaw gateway restart"
```

On Windows, the generated config is JSON:

```text
%APPDATA%\openclaw-gateway-watchdog\watchdog.json
```

Set `OpenClawNativeProbes` to `false` if your OpenClaw CLI is too old for `openclaw health` or `openclaw status --deep`.

### OpenClaw diagnostics and log signals

The watchdog does more than ping one URL. Every `OPENCLAW_DIAG_INTERVAL` seconds it collects an OpenClaw diagnostic snapshot:

```text
~/.local/state/openclaw-gateway-watchdog/last-openclaw-gateway-status.json
~/.local/state/openclaw-gateway-watchdog/last-openclaw-health.json
~/.local/state/openclaw-gateway-watchdog/last-openclaw-model-status.json
~/.local/state/openclaw-gateway-watchdog/last-openclaw-status-deep.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-logs.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-log-signals.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-log-signal-categories.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-diagnostics.jsonl
```

`last-openclaw-log-signals.txt` is filtered from `openclaw logs --plain`. It classifies common failure families such as `provider_timeout`, `proxy_or_network`, `provider_rate_limit`, `provider_auth`, `abort_stuck`, `memory_dream_timeout`, `channel_session`, `gateway_degraded`, `config_reload`, and `task_runtime`.

Default action is `OPENCLAW_DIAG_ACTION="log"` because warnings are evidence, not always proof that a restart is correct. If you explicitly set `OPENCLAW_DIAG_ACTION="restart"` or `command`, the action only runs after consecutive diagnostic warnings and only when the general network probes still pass.

Practical interpretation:

| Evidence | Likely scope | Default strategy |
| --- | --- | --- |
| Gateway status/health is down | Gateway process or RPC path | Restart Gateway immediately through the normal gateway policy. |
| Channel probe fails, network probes pass | Channel/session path | Backoff, re-check, then restart Gateway if still failed. |
| OpenClaw logs show provider timeout, model probe also fails | Provider/API path | Log evidence; optional custom action. A Gateway restart may not fix provider outage. |
| OpenClaw logs show provider timeout, model probe succeeds | OpenClaw runtime, task, session, or specific request path | Keep evidence, inspect logs; avoid blaming the provider alone. |
| Logs show proxy/DNS/TLS errors | Local proxy, DNS, TLS, or ISP route | Log evidence and avoid restart storms; fix network/proxy route first. |
| Logs show session expiry or monitor stopped | Channel plugin/session | Gateway restart is often useful after confirmation. |

### Optional model probe

Set `MODEL_PROBE_ENABLED="1"` when you need to prove whether failures are in the model-provider path instead of Gateway or channel health.

When enabled, the watchdog first reads OpenClaw's configured model provider and probes its provider `baseUrl` without credentials. Then it runs the end-to-end model probe:

```bash
openclaw agent --session-id "$MODEL_PROBE_SESSION_ID" \
  --thinking "$MODEL_PROBE_THINKING" \
  --timeout "$MODEL_PROBE_TIMEOUT" \
  --json \
  --message "$MODEL_PROBE_MESSAGE"
```

If `MODEL_PROBE_MODEL` is empty, OpenClaw's configured default model is used. Results are written to the main log and to:

```text
~/.local/state/openclaw-gateway-watchdog/model-probe-history.jsonl
~/.local/state/openclaw-gateway-watchdog/last-openclaw-model-probe.json
~/.local/state/openclaw-gateway-watchdog/last-model-api-edge-probe.txt
```

Recommended diagnostic settings for overnight provider issues:

```bash
MODEL_PROBE_ENABLED="1"
MODEL_EDGE_PROBE_ENABLED="1"
MODEL_PROBE_INTERVAL="600"
MODEL_PROBE_TIMEOUT="120"
MODEL_PROBE_ACTION="log"
MODEL_PROBE_THINKING="off"
MODEL_PROBE_MESSAGE="Reply with exactly OK."
```

`MODEL_PROBE_ACTION` can be:

- `log`: record evidence only. This is the default.
- `restart`: restart Gateway after `MODEL_PROBE_FAILURES_BEFORE_ACTION` consecutive model failures, but only if general network probes still pass.
- `command`: run `MODEL_PROBE_COMMAND` after consecutive failures.

This feature sends real model requests and may consume provider quota or money. It does not print API keys, but it does store provider/model names, timing, exit status, and the first non-empty error line.
`MODEL_EDGE_PROBE_ENABLED` does not use credentials and does not call `/chat/completions`; it only checks whether the provider API edge such as `https://api.deepseek.com` is reachable quickly.

## Safety Notes

This project intentionally avoids destructive behavior. It does not edit OpenClaw configuration, tokens, sessions, or plugin files. By default it only probes URLs and restarts the gateway through the configured command. The optional model probe makes real model calls only after you explicitly enable it.

Before sharing logs, review them for local paths, service names, and channel URLs.

## License

MIT-0. This matches ClawHub's skill publishing requirement and allows reuse without attribution requirements.

## Publish To ClawHub

Published package:

- ClawHub: <https://clawhub.ai/zc-kama/gateway-resilience-guard>
- Slug: `gateway-resilience-guard`

This repository includes `SKILL.md`, so it can also be republished as an OpenClaw skill bundle:

```bash
clawhub publish . \
  --slug gateway-resilience-guard \
  --name "OpenClaw Gateway Resilience Guard" \
  --version 1.4.4 \
  --changelog "Make dashboard controls robust with native semantic buttons/selects, fixed hover states, centered brand mark, and non-overlapping config rows"
```

ClawHub requires CLI authentication. Run `clawhub login` first.
