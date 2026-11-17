# API 调用契约

统一前缀：`/api/public/clawhive/v1`。完整 JSON Schema 以包内 `openapi.yaml` 为准。

| 顺序 | 方法与路径 | 用途 |
|---|---|---|
| 1 | `GET /health` | 最小可用性检查 |
| 2 | `POST /sessions` | 创建匿名会话和短期 Token |
| 3 | `POST /sessions/{id}/messages` | 提交一轮回答，只获取一个主要问题 |
| 可选 | `POST /sessions/{id}/attachments` | 上传当前会话临时附件 |
| 4 | `POST /sessions/{id}/generate-map` | 生成结构化地图与 Markdown |
| 5 | `GET /sessions/{id}/map` | 读取已生成地图 |
| 6 | `POST /sessions/{id}/consent` | 保存两类独立授权 |
| 7 | `POST /sessions/{id}/convert` | 受控申请 FDE 人工复核 |
| 随时 | `DELETE /sessions/{id}` | 删除匿名会话与临时附件 |

## 请求头

- 会话端点：`Authorization: Bearer <sessionToken>`
- 所有写操作（创建会话和删除除外）：`Idempotency-Key: <8-128字符>`
- JSON 写操作：`Content-Type: application/json`

## 幂等约定

同一请求重试必须使用同一幂等键。新操作必须使用新键。同键替换内容会返回 `409 EXT-40970`。

## 统一错误

```json
{
  "code": "EXT-40020",
  "message": "消息不能为空",
  "requestId": "request-id",
  "timestamp": "2026-08-06T00:00:00.000Z",
  "data": null
}
```

不向用户展示服务器堆栈、文件路径、Token、密钥或数据库细节。

## 平台来源

`sourcePlatform` 使用服务端启用的统一枚举，例如 `CLAWHUB`、`CLAWHIVE`、`LOBSTER_AI`、`COZE`、`CHATGPT`、`DIFY`、`SMITHERY`、`GLAMA`、`MODELSCOPE`、`FDE_WEBSITE`。不得伪造用户ID；无稳定外部用户ID时可不传。
