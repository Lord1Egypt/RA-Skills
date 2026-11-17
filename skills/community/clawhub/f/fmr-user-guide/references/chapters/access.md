# 把 agent harness 接入 FMR

## 进入条件

- 状态前置：P2/P3 正常态（Router 在跑）。
- 意图话术："把 <某 harness> 接上 FMR""端点怎么配""baseURL 填什么""别的机器能不能用"。

## 端点与凭据

| 能力 | 端点 | 说明 |
|---|---|---|
| OpenAI 对话 | `POST /v1/chat/completions` | 流式/非流式均支持 |
| Anthropic 对话 | `POST /v1/messages` | `x-api-key` 或 Bearer |
| 图片生成 | `POST /v1/images/generations` | 配 `model-router-image` |
| 模型列表 | `GET /v1/models` | 免鉴权，返回当前可用虚拟名 |

接入三要素：`base_url` = `http://127.0.0.1:5678/v1`（Anthropic 型 harness 指到 `/v1`，其自行调 `/v1/messages`）；`api_key` = 设备 API Key（`GET /api/status` 的 `apiKey` 字段或 `/admin` 概览页可见）；`model` = **虚拟名**。

**模型名一律用虚拟名**，真实模型 ID 透传会返回 400：`model-router`（文本，带图自动升级 omni）、`model-router-omni`（文本+图）、`model-router-image`（图生成）、`model-router-moa`（多模型合议）、默认分组 `model-router-max`/`model-router-pro`。以 `GET /v1/models` 实际返回为准。

鉴权：`Authorization: Bearer <设备Key>` 或 `x-api-key`。未注册设备时 `/v1` 实际免鉴权（风险见 security 章），但配置示例一律照填，避免注册后失效。

## 具名示例

一机多 harness 共用一个 Router 是官方主场景。

### Claude Code（Anthropic 协议）

```
ANTHROPIC_BASE_URL=http://127.0.0.1:5678
ANTHROPIC_AUTH_TOKEN=<设备Key或占位>
ANTHROPIC_MODEL=model-router
```

harness 若需单独的小模型/名称映射，同样填虚拟名。

### OpenClaw（openclaw.json 的 provider 条目形状）

```json
"models": { "providers": { "free-model-router": {
  "baseUrl": "http://127.0.0.1:5678/v1/",
  "api": "openai-completions",
  "apiKey": "<设备Key或占位>",
  "models": [ { "id": "model-router", "name": "model-router" } ]
}}}
```

写前备份 `openclaw.json`。`setup`/`configureModelRole` 等命令属 Skill 形态遗产，此处仅作条目形状示例，standalone 用户不执行它们。

### WorkBuddy / Hermes Agent（OpenAI 协议）

在其模型配置中设三件套：`base_url=http://127.0.0.1:5678/v1`、`api_key=<设备Key或占位>`、`model=model-router`。

### 通用 OpenAI 协议兜底

任何支持自定义 OpenAI 兼容端点的 harness 同三件套；Anthropic 兼容客户端指到 `/v1`。

## 跨机使用（另一台机器能不能用）

FMR 原生支持改监听绑定：`data/router-config.json` 的 `server.host` / `server.port`（standalone 在 Linux 默认 `0.0.0.0`，Windows/macOS 默认 `127.0.0.1`；用户自定义值保留不动）。改法与生效方式见 `${CLAUDE_SKILL_DIR}/references/data/data-map.md` 白名单表；改后重启 Router（监听地址只在启动时读取），接入三要素的 base_url 随新 host/port 变化。**强制前置**：改绑定前先过 security 章的风险告警，用户知悉后才动。

改绑定/改端口后注意：CLI 硬编码 `127.0.0.1:5678`，此时 CLI（若机器上存在）不再适用，管理走 `/admin` 面板或远程 REST。

## 管理面

本机浏览器 `http://127.0.0.1:5678/admin` 免密；远程访问需管理员账号——首次经 `/admin/setup.html` 创建（SRP-6a，密码不传输），登录 token 有效期 7 天（时点观测，以实测为准）。

## 验证移交

配置写入目标 harness 的正确位置后，把验证交给**接入层 harness 的 agent 自理**，移交话术：

1. `GET http://127.0.0.1:5678/healthz` 返回 200；
2. 用虚拟模型名 `model-router` 发一轮真实请求，收到正常回复。

## 完成判据

- 目标 harness 的配置已写入其配置文件的正确位置（能指出具体文件路径）；
- 已移交上方验证话术。接入层的真实对话结果由接入层自理，不构成本章判据。

## 禁则

- 用户可见文字不出现"standalone Router"字样（全局界面词纪律见 SKILL.md）。
- 不提供任何隧道/内网穿透/TLS 反代方案——跨机 = 改绑定 + 安全告警，到此为止。
