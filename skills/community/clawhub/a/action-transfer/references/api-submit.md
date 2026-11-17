# 动作迁移 · 提交任务

> a7w 插件 `action_transfer` 的接口 `submit` · 官方文档

---

# 动作迁移 · 提交任务

提交动作迁移异步任务。接口接收一张或多张参考人物图片、一个输入视频、可选提示词、生成模式和处理人数，返回平台任务 ID。任务完成后使用“动作迁移 · 查询任务”接口获取结果。

## 接口地址

```http
POST /api/v1/apps/action_transfer/submit
```

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 计费说明

本接口按输入视频时长计费。平台会优先使用请求中的 `duration`，未传时会从 `video_url` 探测视频秒数。

| mode | 计费单位 | 默认价格 |
| --- | --- | --- |
| `fast` | 输入视频秒 | 1 点/秒 |
| `standard` | 输入视频秒 | 2 点/秒 |
| `max` | 输入视频秒 | 3 点/秒 |

实际扣费以当前租户 SKU 售价为准。提交成功时会先冻结预估点数，任务完成后按实际输入视频时长结算。

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | string | 否 | `action_transfer` | 固定值；不传时平台会按当前应用补齐。 |
| `file_url` | string / array | 是 | - | 参考人物图片 URL。单图传字符串，多图参考传 URL 数组。 |
| `video_url` | string | 是 | - | 输入视频 URL，也是本接口计费时长来源。 |
| `prompt` | string | 否 | - | 提示词，例如动作、人物、场景补充描述。 |
| `mode` | string | 否 | `standard` | 生成模式：`fast`、`standard`、`max`。 |
| `face_count` | integer | 否 | `1` | 处理人数，取值范围 `1` 到 `7`。 |
| `duration` | number | 否 | - | 输入视频时长，单位秒；通常可不传，由平台自动探测。 |

## 请求示例

单图参考：

```json
{
  "type": "action_transfer",
  "file_url": "https://example.com/person.png",
  "video_url": "https://example.com/input.mp4",
  "prompt": "一个女生在跳舞",
  "mode": "standard",
  "face_count": 1
}
```

多图参考：

```json
{
  "type": "action_transfer",
  "file_url": [
    "https://example.com/person-1.png",
    "https://example.com/person-2.png"
  ],
  "video_url": "https://example.com/input.mp4",
  "prompt": "一个女生在跳舞",
  "mode": "max",
  "face_count": 2
}
```

## cURL 示例

```bash
curl -X POST "https://你的域名/api/v1/apps/action_transfer/submit" \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "action_transfer",
    "file_url": "https://example.com/person.png",
    "video_url": "https://example.com/input.mp4",
    "prompt": "一个女生在跳舞",
    "mode": "standard",
    "face_count": 1
  }'
```

## 成功响应

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "task_xxxxxxxxxxxxxxxx",
    "status": "processing",
    "app": "action_transfer",
    "api": "submit",
    "frozen_points": 31.39,
    "actual_points": 0,
    "created_at": "2026-06-25T00:00:00Z"
  }
}
```

| 字段 | 说明 |
| --- | --- |
| `data.task_id` | 平台任务 ID，查询任务时传入。 |
| `data.status` | 平台任务状态，提交成功通常为 `processing`。 |
| `data.frozen_points` | 本次任务预冻结点数。 |
| `data.actual_points` | 已实际结算点数；任务完成前通常为 `0`。 |

## 失败响应

```json
{
  "code": 0,
  "msg": "face_count 必须为 1 到 7 的整数",
  "data": []
}
```

常见错误：

| HTTP | code | 说明 |
| --- | --- | --- |
| 400 | `invalid_request` | 参数缺失或格式错误。 |
| 400 | `billing_duration_unresolved` | 无法解析输入视频时长，可显式传入 `duration` 后重试。 |
| 400 | `billing_sku_unmatched` | `mode` 未命中可用 SKU。 |
| 401 | `auth_failed` | API Key 缺失或无效。 |
| 402 | `insufficient_points` | 用户或租户点数不足。 |
| 402 | `key_quota_exceeded` | 当前 API Key 点数额度不足。 |
| 403 | `permission_denied` | 当前 API Key 无权调用应用 API。 |
| 404 | `not_found` | 应用、API 或任务不存在。 |
| 429 | `queue_limit_exceeded` | 应用排队任务已达上限。 |
