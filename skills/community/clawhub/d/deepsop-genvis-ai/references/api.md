# AI Artist API 详细文档

## API 端点

### 1. 预估生成费用

**POST** `/ai/estimate/cost`

**请求头:**
```
Content-Type: application/json
X-Api-Key: <api_key>
```

**请求体:**
```json
{
  "type": "10",
  "methodType": "4",
  "parameter": "{...}"
}
```

说明：请求体与创建生成任务时使用的参数完全一致，需要在正式创建任务前先调用本接口。

**成功响应:**
```json
{
  "msg": "操作成功",
  "code": 200,
  "data": {
    "estimatedCost": 3.500000,
    "sufficientBalance": true
  }
}
```

当 `sufficientBalance` 为 `false` 时，表示余额不足，不应继续提交创建任务，需要提醒用户先充值 K 币。

### 2. 创建生成任务

**POST** `/ai/AiArtistRecord`

**请求头:**
```
Content-Type: application/json
X-Api-Key: <api_key>
```

**请求体:**
```json
{
  "type": "10",
  "methodType": "4",
  "parameter": "{...}"
}
```

**支持的图片模型（`type="10"`）：**

| 模型 Key | sourceName | methodType | 默认尺寸 | 说明 |
|---------|-----------|-----------|---------|------|
| `S5.0L` | DeepSop·S5.0L | `"4"` | `2048x2048` | 默认模型，生成快、风格全、支持联网 |
| `N2` | DeepSop·N2 | `"2"` | `1:1` | 多模态输入，卓越文字渲染与角色一致性 |
| `W2.7` | DeepSop.W2.7 | `"6"` | `2048x2048` | 文生图/图生图多模态输入 |
| `W2.7Pro` | DeepSop.W2.7Pro | `"7"` | `2048x2048` | 精准控图与风格迁移 |
| `3.1Nano2-Evo` | DeepSop·Nano2 | `"8"` | `1:1` | N2 Evo 版（服务端称 Nano2），支持 `imageSearch` |
| `Nano2-Beta-Evo` | DeepSop·Nano2 Beta-Evo | `"9"` | `1:1` | N2 Beta Evo 版 |
| `Image2` | DeepSop·Image2 | `"10"` | `auto` | GPTimage-2 接入；新增 `imageSearch`、`ratiocination`(low/medium/high)、`n`(1–10) |

**支持的视频模型（`type="9"`）：** `S1.5Pro`(2)、`V3.1FB`(3)、`V3.1PB`(4)、`V3.1Fast`(5)、`W2.6t`(7)、`W2.6i`(8)、`W2.6r`(9)、`klingV3Omni`(10)、`W2.7i`(14)、`W2.7t`(15)、`W2.7r`(16)。

> 模型列表来源：`POST /ai/consumeSource/list?pageNum=1&pageSize=999`，Body：`{"sourceTypeList":["IMAGE_MODEL"|"VIDEO_MODEL"],"hiddenState":"0"}`；`hiddenState=1` 表示已停用。

**parameter 字段说明（图片）:**

| 字段 | 类型 | 说明 |
|------|------|------|
| `methodType` | string | API sourceValue，对应表中的 methodType |
| `prompt` | string | 图片生成提示词 |
| `image` | array | 参考图片（可选） |
| `quality` | string | 图片质量: "2K" / "4K" |
| `size` | string | 尺寸格式因模型而异：`S5.0L`/`W2.7`/`W2.7Pro` 用 "2048x2048"，`N2`/`3.1Nano2-Evo`/`Nano2-Beta-Evo` 用 "1:1" |
| `webSearch` | boolean | 是否启用网络搜索（仅 `S5.0L` / `3.1Nano2-Evo`）|
| `imageSearch` | boolean | 是否启用图像搜索（仅 `3.1Nano2-Evo`）|
| `ratiocination` | string | 渲染质量预设（仅 `Image2`）：`low` / `medium` / `high` |
| `n` | number | 生成数量（仅 `Image2`，1–10）|
| `targetMaxSize` | number | 目标最大尺寸（MB）|
| `targetMaxLength` | number | 目标最大长度（像素）|
| `duration` | number | 持续时间（仅 `S5.0L`）|

**成功响应:**
```json
{
  "msg": "操作成功",
  "code": 200,
  "data": ["<task_id>"]
}
```

**失败响应:**
```json
{
  "msg": "错误信息",
  "code": 400,
  "data": null
}
```

### 3. 查询任务状态

**GET** `/ai/AiArtistImage/getInfoByArtistId/{artistId}`

**成功响应:**
```json
{
  "msg": "操作成功",
  "code": 200,
  "data": {
    "message": "生成成功",
    "url": "https://...",
    "status": "SUCCESS"
  }
}
```

**状态值说明:**

| 状态 | 含义 |
|------|------|
| `PENDING` | 等待中 |
| `RUNNING` / `GENERATING` | 生成中 |
| `SUCCESS` | 生成成功 |
| `FAILED` | 生成失败 |

## 错误码

| Code | 含义 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（token无效） |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

## 完整请求示例

```bash
# 使用 S5.0L（DeepSop·S5.0L）模型创建图片任务
curl -X POST "https://ai.deepsop.com/prod-api/ai/AiArtistRecord" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: <api_key>" \
  -d '{
    "type": "10",
    "methodType": "4",
    "parameter": "{\"methodType\":\"4\",\"prompt\":\"风景画\",\"image\":[],\"quality\":\"2K\",\"size\":\"2048x2048\",\"webSearch\":false,\"targetMaxSize\":10,\"targetMaxLength\":6000,\"duration\":10}"
  }'

# 使用 N2（DeepSop·N2）模型创建图片任务
curl -X POST "https://ai.deepsop.com/prod-api/ai/AiArtistRecord" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: <api_key>" \
  -d '{
    "type": "10",
    "methodType": "2",
    "parameter": "{\"methodType\":\"2\",\"prompt\":\"生成一只狗\",\"image\":[],\"quality\":\"2K\",\"size\":\"1:1\",\"webSearch\":false,\"targetMaxSize\":10,\"targetMaxLength\":6000}"
  }'

# 查询状态
curl -X GET "https://ai.deepsop.com/prod-api/ai/AiArtistImage/getInfoByArtistId/<task_id>" \
  -H "X-Api-Key: <api_key>"
```
