---
name: xiaoice-video
description: Use the `xiaoice_video_produce` tool when the user wants to create or check XiaoIce video generation tasks, mentions One Click Video or "一键成片", asks to generate a video from text/topic input, or asks how One Click Video credentials/config should be set.
metadata: { "openclaw": { "homepage": "https://github.com/ROUCHER27/xiaoice-video-tool" } }
---

# XiaoIce Video Tool

Use the single tool `xiaoice_video_produce`.

Activate this skill when the user:

- asks to generate a XiaoIce video from text
- asks to check a previously submitted XiaoIce video task
- mentions `xiaoice_video_produce`, `one-click-video`, "One Click Video", or "一键成片"
- asks whether a submitted task is still running, failed, or finished
- asks how to configure One Click Video / `one-click-video`
- asks how to change or rotate the XiaoIce API key, `vhBizId`, provider URL, or other service-side credentials

## Actions

### Create a task

Use `action: "create"` with:

- `topic`: required text topic
- `vhBizId`: required per-request business id
- `sessionId`: optional
- `traceId`: optional
- `title`: optional
- `content`: optional
- `materialList`: optional array
- `ttsConf`: optional object
- `aigcWatermark`: optional boolean

Example:

```json
{
  "action": "create",
  "topic": "Generate a 15 second spring product launch video in a bright style",
  "vhBizId": "demo-biz-id"
}
```

### Get task status

Use `action: "get"` with:

- `taskId`: required task id returned by `create`

If the user asks for status but no `taskId` is available in the conversation, explain that you need the task id before you can check the task.

Example:

```json
{
  "action": "get",
  "taskId": "task-123"
}
```

## Rules

- Use `vhBizId` only. Never use `vhbizmode`.
- Do not use deprecated `prompt` or `options`; always use top-level official fields.
- For new generation requests, call `create` first.
- For follow-up status checks, call `get` with the known `taskId`.
- If the user asks to "see if it finished", poll with `get`.
- Treat `submitted` and `processing` as non-terminal states.
- Terminal states are `succeeded`, `failed`, and `timeout`.
- On success, return the `videoUrl` if present.
- Always include the current `taskId` and `status` in your reply.
- If create returns `submitted` or `processing`, tell the user the task was accepted and they can check again with the returned `taskId`.
- If status is `failed` or `timeout`, surface any returned error/details instead of claiming success.
- If the tool reports a config error, explain that the OpenClaw plugin needs `plugins.entries.one-click-video.config.serviceBaseUrl` and `internalToken`.

## Configuration Ownership

- The OpenClaw plugin config only owns:
  - `plugins.entries.one-click-video.config.serviceBaseUrl`
  - `plugins.entries.one-click-video.config.internalToken`
  - `plugins.entries.one-click-video.config.requestTimeoutMs`
- The XiaoIce provider credentials belong to `video-task-service`, not the OpenClaw plugin config.
- Do not tell the user to put the XiaoIce API key into `plugins.entries.one-click-video.config`.
- 小冰 API key 指的是 `VIDEO_PROVIDER_API_KEY`。
- 小冰数字人形象模型 id 是 `vhBizId`（默认环境变量是 `VIDEO_PROVIDER_VH_BIZ_ID`，请求字段也是 `vhBizId`）。
- When the user asks to change the XiaoIce API key, explain that it must be changed in the service-side config such as:
  - `VIDEO_PROVIDER_API_KEY`
  - `VIDEO_PROVIDER_API_BASE_URL`
  - `VIDEO_PROVIDER_AUTH_HEADER`
  - `VIDEO_PROVIDER_VH_BIZ_ID`
- If the user asks to rotate the XiaoIce API key, ask for the new provider key or point them to the service `.env` / runtime config, not the plugin config.
- If the user asks for plugin setup, ask only for `serviceBaseUrl` and `internalToken` when they are missing.

### Host Paths (this machine)

- service project root: `/home/yirongbest/xiaoice-video-tool`
- service env file: `/home/yirongbest/xiaoice-video-tool/.env`
- service runtime config file: `/home/yirongbest/xiaoice-video-tool/data/runtime-config.json`
- service admin update API: `PUT http://127.0.0.1:3105/v1/admin/config`
- admin token source: `VIDEO_SERVICE_ADMIN_TOKEN` in `/home/yirongbest/xiaoice-video-tool/.env`

### Recommended Update Flow (API Key + vhBizId)

- real-time update (effective immediately for new tasks):

```bash
curl -sS -X PUT "http://127.0.0.1:3105/v1/admin/config" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: <VIDEO_SERVICE_ADMIN_TOKEN>" \
  -d '{
    "apiKey": "<NEW_VIDEO_PROVIDER_API_KEY>",
    "vhBizId": "<NEW_VH_BIZ_ID>"
  }'
```

- persistent update (survives service restart): edit `/home/yirongbest/xiaoice-video-tool/.env`
  - `VIDEO_PROVIDER_API_KEY=<NEW_VIDEO_PROVIDER_API_KEY>`
  - `VIDEO_PROVIDER_VH_BIZ_ID=<NEW_VH_BIZ_ID>`
  - optional compatibility: keep `VIDEO_PROVIDER_MODEL_ID` aligned only if your environment still relies on it

## Expected Flow

1. Submit with `create`.
2. Keep the returned `taskId`.
3. Check progress with `get`.
4. When status becomes `succeeded`, use the returned `videoUrl`.
