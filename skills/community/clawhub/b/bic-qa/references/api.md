# BIC-QA Open API 速查（仅创建会话 + 流式聊天）

Base URL：`https://api.bic-qa.com`。仅测试或受控代理场景可用 `BICQA_BASE_URL` 覆盖，且必须同时设置 `BICQA_ALLOW_CUSTOM_BASE_URL=1`；远程自定义地址必须使用 HTTPS。
鉴权：请求头 `Authorization: Bearer <API_KEY>`，Key 不得出现在 URL / 参数 / Body 中。

## 1. 创建会话

`POST /open-api/v1/session/create`，`Content-Type: application/json`

请求：`{"title": "数据库巡检咨询"}`（`title` 必填，不能是空白字符串）

响应：

```json
{"status":"success","data":{"conversationId":"eaf05aa6-...","chatTitle":"数据库巡检咨询"},"message":"会话创建成功"}
```

`data.conversationId` 是后续所有接口的会话标识。

## 2. 流式聊天

`POST /open-api/v1/chat`，`Accept: text/event-stream`（curl 必须加 `-N`）

请求：

```json
{"question":"请总结这次数据库巡检的主要风险。","conversationId":"eaf05aa6-...","model":"optional-model-id"}
```

- `question` 必填，最大 5000 字符
- `conversationId` 必填，必须属于当前 API Key 用户
- `batchId` 可选（已上传附件的批次 UUID）
- `model` 可选，留空用默认模型

响应为标准 SSE，每个事件一行 `data:` + JSON + 空行，没有 `event:` / `id:` / `retry:` 字段。

| type | 含义 | 关键字段 |
| --- | --- | --- |
| `meta` | 会话元数据 | `chatSessionId`（上游会话 id，≠ conversationId）、`chatTitle` |
| `delta` | 增量内容 | `delta.content` 正文；`delta.role`；`delta.tool_calls[]` |
| `file` | 生成文件 | `filename`、`file`（**不能**直接用于下载接口）、`toolUseId` |
| `error` | 流内错误 | `errorCode`、`content`，`done=true` |
| `done` | 流结束 | `totalTokens`、`questionId`、`summary` |

注意：

- **双错误通道**——建流前失败是 HTTP 非 200 + 普通 JSON；建流后失败是 HTTP 200 + `type=error`。只看 HTTP 状态不够。
- 客户端只累计 `delta.content` 正文，其他增量字段不进入输出。
- 出现 `error` 后应停止追加正文，随后通常还会再收到一个 `done`。
- 正常完成必须收到 `done`。连接在 `done` 前超时、中断或结束时，应丢弃已累计的残缺正文并保留会话，不得当作成功回答。
- `--timeout` 是流式问答的总时限（默认 600 秒），不是每次 socket 读取都重新计时。超时请求可能已被服务端部分处理，不应自动重试。

## 错误码

| HTTP | code | 处理 |
| --- | --- | --- |
| 400 | `OPEN_API_PARAMETER_INVALID` | 修正参数，不原样重试 |
| 400 | `OPEN_API_SESSION_NOT_FOUND` | 重建会话（脚本已自动处理一次） |
| 400 | `OPEN_API_TOKEN_INSUFFICIENT` | 账号余额不足，联系平台 |
| 401 | `OPEN_API_KEY_MISSING` / `OPEN_API_KEY_INVALID` | 更换 Key，不高频重试 |
| 429 | `OPEN_API_RATE_LIMITED` | 按 `Retry-After` 退避 |
| 503 | `OPEN_API_UPSTREAM_UNAVAILABLE` | 可安全重试，指数退避 |
| 500 | `OPEN_API_INTERNAL_ERROR` | 记录标识，联系平台 |

客户端本地错误：`OPEN_API_TIMEOUT` / `OPEN_API_STREAM_TIMEOUT` 表示连接或总时限超时；`OPEN_API_STREAM_INTERRUPTED` / `OPEN_API_STREAM_INCOMPLETE` 表示传输中断或缺少最终 `done`。这些错误均不自动重试聊天请求。

限流：创建会话 60 秒 60 次，流式聊天 60 秒 20 次（用户维度）。
