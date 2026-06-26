# Fast Claw 服务接口说明

只有在随附客户端脚本不够用时，才需要读取这个参考文档。

## 本地状态

- 服务地址：`FAST_CLAW_SERVICE_URL`，默认 `http://localhost:8033`
- API key 文件：`FAST_CLAW_API_KEY_PATH`，默认 `~/.fast-claw/api-key.json`
- 兼容旧变量：`FAST_CLAW_TOKEN_PATH`
- 本地文件只是 API key 缓存，余额和账户状态始终以服务端数据库为准。

## 接口列表

### `POST /v1/checkout-sessions`

创建一个 checkout 会话。

请求体：

```json
{
  "account_name": "demo-account",
  "credits": 10,
  "api_key": null,
  "success_url": "http://localhost:3000/after-pay"
}
```

规则：

- 首次购买时传 `account_name`。
- 给已有账户充值时传 `api_key`。
- `success_url` 是可选字段。传了以后，浏览器流程在支付完成后会跳转过去。
- `success_url` 可以是外部链接，例如 `https://www.baidu.com`。

### `GET /v1/checkout-sessions/{session_id}`

轮询 checkout 是否完成。完成后会返回稳定 API key 和当前余额。兼容字段 `token` 也会继续返回。

### `GET /checkout/{session_id}`

打开托管的购买页。

### `POST /checkout/{session_id}/complete`

模拟购买页里的支付成功动作。首次购买会创建 API key，充值则会给现有 API key 增加额度。

### `GET /v1/account`

查询账户状态。

请求头：

```text
X-API-Key: <api_key>
```

兼容旧头：

```text
Authorization: Bearer <api_key>
```

`GET /v1/token` 仍保留为兼容别名。

### `POST /v1/invoke`

调用演示微服务。每次请求会消耗 1 次额度。

请求体：

```json
{
  "prompt": "Summarize my request"
}
```

### `POST /v1/report-jobs`

创建一个异步分析报告任务。接口会立即返回 `job_id`，同时消耗 1 次额度。

请求头：

```text
X-API-Key: <api_key>
```

请求体：

```json
{
  "prompt": "Analyze refund risk for the last 7 days"
}
```

### `GET /v1/report-jobs/{job_id}`

轮询 report job 的状态。状态会经历 `pending`、`running`，完成后返回 `completed` 和最终报告内容；失败时返回 `failed` 和错误信息。
