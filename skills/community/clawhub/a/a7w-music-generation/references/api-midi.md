# 导出 MIDI · midi

> a7w 插件 `music_generation` 的接口 `midi` · 平台官方文档

---

`POST /api/v1/apps/music_generation/midi`

# 音乐生成 · 导出 MIDI

基于音频 ID 提取 MIDI 文件。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `midi` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/midi` |
| 调用模式 | 异步 |
| 计费方式 | 固定价 14 点/次 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `audio_id` | string | 是 | - | - | `audio_xxxxxxxxxxxx` | 音频 ID，用于定位已生成或已上传的音频片段。 |
| `callback_url` | string | 否 | - | - | - | 任务完成或失败时由平台主动通知的 HTTPS 地址；同步接口可不传。 |

## 响应说明

提交成功后返回平台 `task_id`。请使用本应用查询接口或统一任务查询接口获取最终结果；如果请求传入 `callback_url`，平台会在任务终态时主动通知。

### 提交成功示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "task_id": "task_xxxxxxxxxxxx",
        "status": "processing",
        "app": "music_generation",
        "api": "midi",
        "frozen_points": 14,
        "actual_points": 0,
        "created_at": "2026-07-06T14:32:35Z"
    }
}
```

### 查询处理中示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "status": "processing"
        },
        "usage": {
            "points_cost": 0,
            "actual_points": 0
        }
    }
}
```

### 查询完成示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "task_id": "task_xxxxxxxxxxxx",
            "status": "completed",
            "file_url": "https://example.com/music/audio.mid"
        },
        "usage": {
            "points_cost": 14,
            "actual_points": 14
        }
    }
}
```

### 失败示例

```json
{
    "code": 0,
    "msg": "任务处理失败，请稍后重试",
    "data": null
}
```

## 参数（平台 schema 原文）

```json
{
  "audio_id": {
    "type": "string",
    "example": "audio_xxxxxxxxxxxx",
    "description": "音频 ID，用于定位已生成或已上传的音频片段。"
  },
  "callback_url": {
    "type": "string",
    "description": "任务完成或失败时由平台主动通知的 HTTPS 地址；同步接口可不传。"
  }
}
```

## 计费

- 结算口径：按次固定价 14 点（租户价）
- 标准价：`fixed_price=14.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=14.00` / `tenant_points_per_1k_input=0.0000`
