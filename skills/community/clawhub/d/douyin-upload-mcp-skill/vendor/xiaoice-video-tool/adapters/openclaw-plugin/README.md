# One Click Video OpenClaw Thin Plugin

This plugin uses the OpenClaw plugin id `one-click-video` and registers exactly one tool:

- `xiaoice_video_produce`

The plugin is a thin adapter only:

- validates OpenClaw tool inputs (`create` / `get`)
- reads runtime config from `plugins.entries['one-click-video'].config`
- calls the packaged client in `lib/video-service-client.js`
- returns OpenClaw tool result shape (`content[]` + `isError`)
- bundles skill metadata under `skills/xiaoice-video/SKILL.md`

The packaged client is intentionally vendored into the plugin package so the extension can load after `openclaw plugins install` without depending on this repository layout.

## Config Ownership

`one-click-video` plugin config only contains:

- `serviceBaseUrl`
- `internalToken`
- `requestTimeoutMs`

XiaoIce provider credentials are configured on the `video-task-service` side, not in `plugins.entries.one-click-video.config`.

Do not put these service-side values into the plugin config:

- `VIDEO_PROVIDER_API_KEY`
- `VIDEO_PROVIDER_API_BASE_URL`
- `VIDEO_PROVIDER_AUTH_HEADER`
- `VIDEO_PROVIDER_VH_BIZ_ID`
- `VIDEO_PROVIDER_MODEL_ID`

Changing the XiaoIce API key means updating the service-side config and restarting or refreshing the service runtime, not editing the OpenClaw plugin config.

## Tool Arguments

Supported fields:

- `action`: `create | get` (required)
- `topic`: required for `create`
- `vhBizId`: required for `create`
- `taskId`: required for `get`
- `sessionId`: optional
- `traceId`: optional
- `title`: optional
- `content`: optional
- `materialList`: optional array
- `ttsConf`: optional object
- `aigcWatermark`: optional boolean

Rejected field:

- `vhbizmode` (hard-cut, use `vhBizId`)
- `prompt` / `options` (deprecated; use top-level official fields)

## OpenClaw Config Example

```json
{
  "plugins": {
    "entries": {
      "one-click-video": {
        "enabled": true,
        "config": {
          "serviceBaseUrl": "http://127.0.0.1:3105",
          "internalToken": "video-internal-token",
          "requestTimeoutMs": 15000
        }
      }
    }
  }
}
```

## Test

Run focused plugin tests:

```bash
node --test adapters/openclaw-plugin/__tests__/openclaw-plugin.test.js
```
