# 上传参考音频 · upload_audio

> a7w 插件 `music_generation` 的接口 `upload_audio` · 平台官方文档

---

`POST /api/v1/apps/music_generation/upload_audio`

# 音乐生成 · 上传参考音频

提交可访问的音频地址并返回可用于后续创作的音频 ID。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `upload_audio` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/upload_audio` |
| 调用模式 | 同步 |
| 计费方式 | 固定价 13 点/次 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `audio_url` | string | 是 | - | - | `https://example.com/ref.mp3` | 可公开访问的音频文件 URL，用于生成后续创作需要的音频 ID。 |

## 响应说明

同步返回处理结果。媒体类结果可能包含 `audio_url`、`video_url`、`file_url`、`image_url`、`audio_id`、`persona_id` 等字段，具体以接口实际结果为准。

### 成功示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "status": "completed",
            "audio_id": "audio_xxxxxxxxxxxx",
            "audio_url": "https://example.com/music/reference.mp3",
            "title": "reference_audio",
            "duration": 198,
            "data": {
                "audio_id": "audio_xxxxxxxxxxxx",
                "audio_url": "https://example.com/music/reference.mp3",
                "duration": 198
            }
        },
        "usage": {
            "points_cost": 13,
            "actual_points": 13
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
  "audio_url": {
    "type": "string",
    "example": "https://example.com/ref.mp3",
    "description": "可公开访问的音频文件 URL，用于生成后续创作需要的音频 ID。"
  }
}
```

## 计费

- 结算口径：按次固定价 13 点（租户价）
- 标准价：`fixed_price=13.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=13.00` / `tenant_points_per_1k_input=0.0000`
