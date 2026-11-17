# 创建歌手风格 · persona

> a7w 插件 `music_generation` 的接口 `persona` · 平台官方文档

---

`POST /api/v1/apps/music_generation/persona`

# 音乐生成 · 创建歌手风格

基于已生成歌曲创建可复用的歌手风格 ID。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `persona` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/persona` |
| 调用模式 | 同步 |
| 计费方式 | 固定价 12 点/次 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `audio_id` | string | 是 | - | - | `audio_xxxxxxxxxxxx` | 音频 ID，用于定位已生成或已上传的音频片段。 |
| `name` | string | 是 | - | - | `My Singer Style` | 歌手风格名称。 |
| `description` | string | 否 | - | - | - | 歌手风格的文字描述。 |
| `vocal_start` | number | 否 | - | - | - | 人声片段开始时间，单位秒。 |
| `vocal_end` | number | 否 | - | - | - | 人声片段结束时间，单位秒。 |
| `vox_audio_id` | string | 否 | - | - | - | 用于创建新歌手风格的人声参考音频 ID。 |

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
            "persona_id": "persona_xxxxxxxxxxxx",
            "data": {
                "persona_id": "persona_xxxxxxxxxxxx"
            }
        },
        "usage": {
            "points_cost": 12,
            "actual_points": 12
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
  "name": {
    "type": "string",
    "example": "My Singer Style",
    "description": "歌手风格名称。"
  },
  "audio_id": {
    "type": "string",
    "example": "audio_xxxxxxxxxxxx",
    "description": "音频 ID，用于定位已生成或已上传的音频片段。"
  },
  "vocal_end": {
    "type": "number",
    "description": "人声片段结束时间，单位秒。"
  },
  "description": {
    "type": "string",
    "description": "歌手风格的文字描述。"
  },
  "vocal_start": {
    "type": "number",
    "description": "人声片段开始时间，单位秒。"
  },
  "vox_audio_id": {
    "type": "string",
    "description": "用于创建新歌手风格的人声参考音频 ID。"
  }
}
```

## 计费

- 结算口径：按次固定价 12 点（租户价）
- 标准价：`fixed_price=12.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=12.00` / `tenant_points_per_1k_input=0.0000`
