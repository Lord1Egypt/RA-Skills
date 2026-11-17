# DuoPlus control API and routing reference

## Contents

- Authentication and limits
- Cloud-phone endpoints
- Status values
- Proxy initialization
- HTTP Gateway routing contract
- Lifecycle orchestration

## Authentication and limits

Control API bases:

- Outside mainland China: `https://openapi.duoplus.net` (skill default)
- Mainland China: `https://openapi.duoplus.cn`

All calls are `POST` with JSON and these headers:

```text
Content-Type: application/json
Lang: zh
DuoPlus-API-Key: <DUOPLUS_API_KEY>
```

For interactive AI use, require the user to provide this API key directly in the conversation and pass it with `--api-key` for the current invocation. Do not require permanent environment configuration. `DUOPLUS_API_KEY` is an optional non-interactive deployment mechanism.

The official limit is 1 QPS per endpoint. A successful envelope has `code: 200`; do not treat HTTP 200 with a non-200 envelope code as success. Source: [DuoPlus interface introduction](https://help.duoplus.cn/docs/introduction).

## Cloud-phone endpoints

| Capability | Path | Request | Notes |
|---|---|---|---|
| List | `/api/v1/cloudPhone/list` | filters plus `page`, `pagesize` | Maximum 100 per page. Returns `id`, `name`, `status`, `ip`, `http_status`, `area`, ADB data and metadata. |
| Status | `/api/v1/cloudPhone/status` | `{"image_ids":[...]}` | Use for polling asynchronous operations. |
| Detail | `/api/v1/cloudPhone/info` | `{"image_id":"..."}` | Returns proxy, GPS, locale, SIM, Wi-Fi and device details. |
| Power on | `/api/v1/cloudPhone/powerOn` | `{"image_ids":[...]}` | Asynchronous; maximum 100. Temporary compute starts billing immediately. |
| Power off | `/api/v1/cloudPhone/powerOff` | `{"image_ids":[...]}` | Maximum 20. Stops temporary-compute billing. |
| Restart | `/api/v1/cloudPhone/restart` | `{"image_ids":[...]}` | Asynchronous; maximum 20. |
| Execute shell command | `/api/v1/cloudPhone/command` | `{"image_id":"...","command":"..."}` | Fallback only; prefer Gateway `SHELL_COMMAND`. Do not add an `adb shell` prefix. Commands should finish within 10 seconds. |
| Init proxy | `/api/v1/cloudPhone/initProxy` | `{"images":[...]}` | Configure a phone before its first power-on. |
| Proxy list | `/api/v1/proxy/list` | pagination and optional status | Maximum 100 per page. |

Official sources: [list](https://help.duoplus.cn/docs/cloud-phone-list), [status](https://help.duoplus.cn/docs/cloud-phone-status), [detail](https://help.duoplus.cn/docs/huo-qu-yun-ji-xiang-qing), [power on](https://help.duoplus.cn/docs/batch-power-on), [power off](https://help.duoplus.cn/docs/pi-liang-guan-ji), [restart](https://help.duoplus.cn/docs/pi-liang-chong-qi), [execute command](https://help.duoplus.cn/docs/execute-the-adb-command), [proxy list](https://help.duoplus.cn/docs/proxy-list).

New AI-routing fields in each list item:

| Field | Meaning | Skill behavior |
|---|---|---|
| `ip` | Private CloudIP used by the public Gateway router | Send as the `CloudIP` header. |
| `http_status=1` | Supports AI HTTP access | Sort first and mark `ai_control_supported=true`. |
| `http_status=0` | Does not support AI HTTP access | Mark unsupported; block `ensure-ready` and all Gateway operations. Warn before power-on. |

Use `list --all` when selecting a phone for AI automation. It fetches every API page before sorting, so all supported phones are placed ahead of unsupported phones rather than sorting only one page.

## Status values

| Value | Meaning | Agent behavior |
|---:|---|---|
| 0 | Proxy not configured | Initialize proxy; do not power on. |
| 1 | Running | Continue to Gateway readiness. |
| 2 | Stopped | Power on when needed for the requested task. |
| 3 | Expired | Stop and report renewal required. |
| 4 | Expired, pending renewal | Stop and report renewal required. |
| 10 | Starting | Poll status. |
| 11 | Configuring | Poll status. |
| 12 | Configuration failed | Inspect detail and report/fix explicit configuration. |

## Proxy initialization

`POST /api/v1/cloudPhone/initProxy` accepts an `images` array. Each item requires:

- `image_id`
- `ip_scan_channel`: `ip2location` or `ipapi`
- `proxy`: either `{"id":"PROXY_ID"}` or connection data

Connection data supports `host`, `port`, optional `user`/`password`, and `protocol` in `socks5`, `http`, `https`. Optional phone parameters include `dpi_name`, `network_mode`, `brand`, `model`, `location`, `sim`, and `locale`. Do not synthesize identity-sensitive values. Source: [initialize proxy](https://help.duoplus.cn/docs/proxy-init).

## HTTP Gateway routing contract

After official status becomes `1`, route automation to:

```text
POST https://agent-gateway.duoplus.net/agent-command
Region: {region}
CloudIP: {phone.ip}
Authorization: Bearer {DUOPLUS_API_KEY}
Content-Type: application/json
```

The fixed external edge selects the destination from the `Region` and `CloudIP` headers, then forwards to `http://{CloudIP}:18080/agent-command`. The device compares the Bearer token with `/data/misc/dplus/init.config.auth`. To satisfy the one-key model, provisioning must set that auth to the same AI API key, or the edge must validate the AI API key and replace the downstream token.

Do not build or call a Gateway route unless the selected list item has `http_status=1`. The `ip` field is routing data, not evidence that AI HTTP access is enabled.

The client resolves CloudIP from the list response and normalizes common `area`/region values. Legacy records that omit a routable region can use `DUOPLUS_REGION`; this is deployment metadata, not another secret.

Gateway operations:

- `health`: process/backend state
- `ready`: executor readiness
- `submit`: synchronous UI-state or action execution, up to roughly 300 seconds
- `query`: retrieve a retained command result
- `stop`: stop a task

## Shell execution route priority

Use Gateway `SHELL_COMMAND` first. The official `/api/v1/cloudPhone/command` endpoint is a fallback, not a parallel or preferred route. Invoke it through:

```bash
python3 scripts/duoplus_ai.py --api-key 'API_KEY' platform-shell IMAGE_ID \
  --command 'getprop ro.build.version.release'
```

The platform endpoint returns single-phone output in `data.content` and succeeds only when the envelope has `code=200` and `data.success=true`. It accepts a command without the `adb shell` prefix and only guarantees commands that complete within 10 seconds.

Fallback is safe before Gateway submission when routing is unavailable or the executor remains unavailable after the normal readiness timeout. After submission, a timeout or connection loss is ambiguous: query the Gateway `command_id` first. Never replay a state-changing or non-idempotent command through the platform unless Gateway non-execution is known or the user explicitly accepts the duplicate-execution risk. A completed Gateway failure may still have partial side effects, so automatic replay is limited to read-only or idempotent commands.

## Lifecycle orchestration

Use this state machine:

```text
list/select -> status
  0 -> init proxy -> poll configuration -> power on
  2 -> power on
  10/11 -> poll
  1 -> resolve route -> Gateway ready -> automate
  3/4/12 -> stop with a concrete error
```

After `powerOn` or `restart`, poll `/status`; the acceptance response is not completion. After status `1`, poll Gateway `ready` because Android and the automation executor may still be starting.
