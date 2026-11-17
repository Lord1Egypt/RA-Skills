# 生成歌词 · lyrics

> a7w 插件 `music_generation` 的接口 `lyrics` · 平台官方文档

---

`POST /api/v1/apps/music_generation/lyrics`

# 音乐生成 · 生成歌词

根据主题或风格描述生成结构化歌词。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `lyrics` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/lyrics` |
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
| `prompt` | string | 是 | - | - | `A song about winter` | 歌词生成提示词，用于描述歌词主题、情绪或风格。 |

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
            "title": "First Light Avenue",
            "data": [
                {
                    "text": "[Verse 1]\nThe bakery opens slow\n[Chorus]\nMorning on the street",
                    "title": "First Light Avenue",
                    "status": "complete",
                    "tags": [
                        "indie pop",
                        "warm vocal"
                    ]
                }
            ]
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
  "prompt": {
    "type": "string",
    "example": "A song about winter",
    "description": "歌词生成提示词，用于描述歌词主题、情绪或风格。"
  }
}
```

## 计费

- 结算口径：按次固定价 12 点（租户价）
- 标准价：`fixed_price=12.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=12.00` / `tenant_points_per_1k_input=0.0000`
