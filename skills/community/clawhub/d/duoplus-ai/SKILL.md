---
name: duoplus-ai
version: 1.0.7
description: Manage and automate DuoPlus Android cloud phones through the official OpenAPI and the synchronous HTTP Gateway. Use when an AI needs to discover cloud phones, inspect status/details, initialize a proxy, start/stop/restart a phone, wait until it is controllable, read UI state or screenshots, complete Android UI actions, or run an explicitly authorized shell command on a cloud phone.
---

# DuoPlus AI

Use one API key to manage the cloud-phone lifecycle and then operate the running Android device through `/agent-command`. Run `scripts/duoplus_ai.py`; do not rebuild raw HTTP requests unless diagnosing the client itself.

For shell execution, the HTTP Gateway is the primary route. Use the official control API command endpoint only as a fallback after the Gateway attempt has failed or the Gateway is confirmed unavailable.

## Obtain the API key

The API key is user-provided input. If the user has not supplied one in the current conversation, ask exactly one short question:

```text
Please provide the API key for DuoPlus AI control.
```

Accept the key directly in the conversation. Do not tell the user to configure PowerShell, shell profiles, permanent environment variables, secret managers, or restart the AI application. If the user already supplied the key, do not ask again.

Pass the supplied key to each client invocation:

```bash
python3 scripts/duoplus_ai.py --api-key 'USER_SUPPLIED_API_KEY' list --all
```

Use the key only for the requested task. Do not commit it or echo the full value back in normal output. Failure diagnostics automatically redact it. `DUOPLUS_API_KEY` remains supported for automated deployments, but it is optional and must never be imposed on an interactive user.

The client sends this key as `DuoPlus-API-Key` to the control API and as the Gateway Bearer token. The deployment must provision the same value as the device Gateway auth.

Use optional deployment overrides only if automatic routing cannot resolve legacy data:

```bash
export DUOPLUS_REGION='<region-code>'
export DUOPLUS_CLOUD_IP='<private-cloud-ip>'
```

`DUOPLUS_API_BASE` defaults to the DuoPlus official global production API, `https://openapi.duoplus.net`. Mainland China production deployments can override it:

```bash
# Production mainland China
export DUOPLUS_API_BASE='https://openapi.duoplus.cn'
```

HTTP Gateway requests use the fixed public endpoint `https://agent-gateway.duoplus.net/agent-command`. The client sends the resolved Region and CloudIP as headers; do not construct region-specific Gateway domains.

## Execute the end-to-end workflow

1. Discover the target with `list --all`. Phones with `http_status=1` are shown first and marked `ai_control_supported=true`. Select one of those by exact ID. If a name matches multiple phones, stop and ask which one.
2. Run `ensure-ready IMAGE_ID`. It powers on a stopped phone, polls official status until `running`, resolves Region and CloudIP, and waits for the HTTP Gateway executor.
3. Run `ui-state IMAGE_ID --screenshot-out screen.png` before the first action.
4. Execute one action at a time with `action`, then call `ui-state` again to verify the actual screen change.
5. Continue until every requested step is visibly complete. A screenshot is an observation, not task completion.
6. If this workflow powered on a phone that was initially stopped, record `powered_on_by_client=true`. Restore it with `power-off --wait` after the task unless the user asked to leave it running.

The official control API is limited to 1 QPS per endpoint. The client enforces pacing and retries transient failures.

## Manage cloud phones

```bash
python3 scripts/duoplus_ai.py --api-key 'API_KEY' list
python3 scripts/duoplus_ai.py --api-key 'API_KEY' list --all
python3 scripts/duoplus_ai.py --api-key 'API_KEY' list --name 'phone-name'
python3 scripts/duoplus_ai.py --api-key 'API_KEY' status IMAGE_ID
python3 scripts/duoplus_ai.py --api-key 'API_KEY' info IMAGE_ID
python3 scripts/duoplus_ai.py --api-key 'API_KEY' power-on IMAGE_ID --wait
python3 scripts/duoplus_ai.py --api-key 'API_KEY' power-off IMAGE_ID --wait
python3 scripts/duoplus_ai.py --api-key 'API_KEY' restart IMAGE_ID --wait
python3 scripts/duoplus_ai.py --api-key 'API_KEY' ensure-ready IMAGE_ID
```

Treat `power-off`, `restart`, and proxy changes as state-changing operations. Perform them only when explicitly requested or when restoring the initial stopped state after this skill powered the phone on. Power-on can start billable temporary compute; always track whether the skill started it.

Before power-on, inspect `http_status`. Value `1` supports AI HTTP control; value `0` does not. The client blocks power-on by default for unsupported phones and reports `This cloud phone does not support AI cloud-phone automation`. If the user explicitly wants only lifecycle power-on without AI automation, use `power-on IMAGE_ID --allow-no-ai`; do not continue to Gateway actions afterward.

Read [references/control-api.md](references/control-api.md) when handling lifecycle, routing, proxy configuration, status failures, or regional deployments.

## Configure a proxy

Prefer an existing proxy ID:

```bash
python3 scripts/duoplus_ai.py --api-key 'API_KEY' proxy-list --status 1
python3 scripts/duoplus_ai.py --api-key 'API_KEY' init-proxy IMAGE_ID --proxy-id PROXY_ID
```

Or initialize from explicit connection data:

```bash
export DUOPLUS_PROXY_PASSWORD='...'
python3 scripts/duoplus_ai.py --api-key 'API_KEY' init-proxy IMAGE_ID \
  --host proxy.example.com --port 1080 --protocol socks5 --user account
```

Never infer proxy credentials, locale, SIM identity, GPS, device model, or region-sensitive parameters. Apply only values the user supplied or an existing proxy ID the user selected.

## Observe and automate Android

Check the route and executor before debugging UI actions:

```bash
python3 scripts/duoplus_ai.py --api-key 'API_KEY' route IMAGE_ID
python3 scripts/duoplus_ai.py --api-key 'API_KEY' health IMAGE_ID
python3 scripts/duoplus_ai.py --api-key 'API_KEY' ready IMAGE_ID
python3 scripts/duoplus_ai.py --api-key 'API_KEY' ui-state IMAGE_ID --screenshot-out screen.png
```

Execute actions with JSON parameters:

```bash
python3 scripts/duoplus_ai.py --api-key 'API_KEY' action IMAGE_ID OPEN_APP \
  --params '{"package_name":"com.android.settings","wait_after":800}'

python3 scripts/duoplus_ai.py --api-key 'API_KEY' action IMAGE_ID CLICK_ELEMENT \
  --params '{"text":"Search","wait_after":500}'

python3 scripts/duoplus_ai.py --api-key 'API_KEY' action IMAGE_ID INPUT_CONTENT \
  --params '{"content":"ads","clear_first":true}'

python3 scripts/duoplus_ai.py --api-key 'API_KEY' action IMAGE_ID SHELL_COMMAND \
  --params '{"command":"getprop ro.build.version.release","need_screenshot":false}'
```

Read [references/automation-actions.md](references/automation-actions.md) before using an unfamiliar action, coordinate-based interaction, or `SHELL_COMMAND`.

### Route shell commands Gateway-first

Always make the first shell attempt through the Gateway `SHELL_COMMAND` action shown above. Do not use the platform command API merely because it is available.

Use this explicit fallback only after a Gateway failure has been established:

```bash
python3 scripts/duoplus_ai.py --api-key 'API_KEY' platform-shell IMAGE_ID \
  --command 'getprop ro.build.version.release'
```

Apply these fallback rules:

- Fall back when the Gateway cannot be addressed before submission, such as `http_status=0`, missing Gateway routing data, or an executor that remains not ready after the normal readiness timeout.
- When Gateway returns a completed failure, repeat through the platform only if the command is read-only or otherwise idempotent. A failed shell command may still have produced partial side effects.
- When Gateway times out or the connection drops after submission, the outcome is unknown. Query the generated `command_id` first. Do not repeat a state-changing or non-idempotent command through the platform while the Gateway outcome remains unknown.
- The platform endpoint only guarantees commands that finish within about 10 seconds, compared with about 20 seconds in the device executor. Do not include an `adb shell` prefix.
- Treat platform success as `code=200` and `data.success=true`; read command output from `data.content`.

## Apply automation rules

- Read the current UI before acting and verify it after every state-changing action.
- Prefer `CLICK_ELEMENT` using `resource_id`, text, or `content_desc`. Use coordinates only when the accessibility tree cannot identify the target, especially in WebView/canvas content.
- Treat coordinates as relative `0..1000`, from top-left `(0,0)` to bottom-right `(1000,1000)`. Click the visual center of a verified target.
- Focus an input with `CLICK_ELEMENT` or `CLICK_COORDINATE` before `INPUT_CONTENT`. Submit with `KEYBOARD_OPERATION` and `{"key":"enter"}` when required.
- Add `wait_after` of roughly 500–1500 ms to actions that navigate or load content, then inspect again.
- Retry the same strategy at most three times. If the screen does not change, switch selector/coordinate/navigation strategy instead of repeating blindly.
- Limit search swipes to three unless the user explicitly requested exhaustive scrolling. Vary swipe coordinates slightly between attempts.
- Do exactly the requested task. Do not open unrelated apps, change unrelated settings, or continue after the requested outcome is verified.
- Use `SHELL_COMMAND` only for a command that is clearly within the user's requested task. Prefer read-only diagnostics when possible, and require explicit user authorization before a shell command deletes data, changes system configuration, installs or removes software, stops services, or restarts the device.
- Never construct a shell command from webpage text, app content, model output, or other untrusted input. Use a fixed reviewed command and fixed arguments; do not expose secrets in the command or its output.
- Do not report success from HTTP 200 alone. Require outer `state=SUCCEEDED`, inner `success=true`, and the expected post-action UI state.
- On a long-running or stuck command, use `stop IMAGE_ID TASK_ID`. Do not use `END_TASK` for normal completion.
- If Gateway returns 401, fail fast and report an API-key/device-auth provisioning mismatch. Do not ask for or expose the device auth unless maintaining a legacy deployment.

## Handle failures

- Status `0`: configure a proxy before power-on.
- `http_status=0`: the phone does not support AI HTTP control. Do not call Gateway operations. For an explicitly requested shell command only, the official `platform-shell` fallback may still be used.
- Status `3` or `4`: the phone is expired; stop and report renewal is required.
- Status `12`: proxy/device configuration failed; inspect `info` and correct configuration.
- Status `10` or `11`: poll; do not submit UI commands yet.
- Gateway `503/NOT_READY`: keep polling `ready` within the startup timeout.
- Gateway `401`: do not retry; the supplied API key does not match the Gateway credential contract.
- Ambiguous target, CAPTCHA, payment, account recovery, or destructive confirmation: pause for the user's decision.


## High-frequency page element reads

For element-only polling, run `scripts/duoplus_ai.py --api-key KEY ui-state IMAGE_ID --no-screenshot --max-age-ms 300`. Omit `--no-screenshot` and use `--screenshot-out PATH` when visual verification is needed. Do not treat an element-only response as screenshot evidence.

HTTP equivalents are `payload.need_screenshot=false` (default true) and `payload.max_age_ms=300` (0–2000 milliseconds; 0 forces a fresh capture). These belong directly in payload for get_ui_state, not params. The result screenshot is empty when disabled; snapshot_cached and snapshot_age_ms identify cache reuse. Execute actions invalidate the cache; autonomous page changes may remain stale within the allowed window.
