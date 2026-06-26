# Giggle Pro API 完整工作流程笔记

> 2026-02-06 实测记录

## 测试项目

- **Project ID**: `b61b4f33-46ac-48e3-a23a-5ce9da4c7822`
- **Project Name**: flow-test-v2

## API Base URL

⚠️ **重要**: 使用 `https://giggle.pro/api/v1/...`，不是 `https://api.giggle.pro/...`

## 完整流程步骤

| 步骤 | API                                              | 状态 | 备注                        |
| ---- | ------------------------------------------------ | ---- | --------------------------- |
| 1    | `POST /project/create`                           | ✅   | 创建项目                    |
| 2    | `POST /script/update` (第一次)                   | ✅   |                             |
| 3    | `PUT /server/chat-with-writer`                   | ❌   | Unauthorized，前端专用      |
| 4    | `POST /script/storyExpansion`                    | ✅   | 用这个替代 chat-with-writer |
| 5    | `GET /project/detail?id=xxx`                     | ✅   | 查询项目状态                |
| 6    | `POST /script/update` (第二次)                   | ✅   |                             |
| 7    | `POST /character/generate`                       | ✅   |                             |
| 8    | `POST /project/update`                           | ✅   | **每个环节后都要调用**      |
| 9    | 轮询 `GET /character/list?project_id=xxx`        | ✅   | 等 image URL                |
| 10   | `POST /storyboard-shots/auto-generate`           | ✅   |                             |
| 11   | `POST /project/update`                           | ✅   |                             |
| 12   | `POST /payment/model-price` (图片)               | ✅   | 见下方参数                  |
| 13   | `POST /storyboard-shots/auto-generate-image`     | ✅   | **需要传 model 参数**       |
| 14   | `POST /project/update`                           | ✅   |                             |
| 15   | `POST /storyboard-shots/optimize-prompt`         | ✅   | **需要传 model 参数**       |
| 16   | `POST /project/update`                           | ✅   |                             |
| 17   | `POST /payment/model-price` (视频)               | ✅   | 见下方参数                  |
| 18   | `POST /storyboard-shots/generate-video`          | ✅   | **逐个 shot 调用**          |
| 19   | 轮询 `GET /storyboard-shots/list?project_id=xxx` | ✅   | 等 video URL                |
| 20   | `POST /project/update`                           | ✅   | 最后再 update 一次          |

## 关键 API 调用详情

### project/update（核心同步接口）

每个环节完成后都需要调用！

```bash
curl -X POST "https://giggle.pro/api/v1/project/update" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "xxx"}'
```

**响应示例**:

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "project_id": "b61b4f33-46ac-48e3-a23a-5ce9da4c7822",
    "project_name": "flow-test-v2",
    "current_step": "storyboard",
    "project_status": "completed",
    "completed_steps": "script,character,storyboard,image",
    "character_edit_status": true,
    "mode": "professional"
  }
}
```

### model-price（查询价格）

**图片生成价格**:

```bash
curl -X POST "https://giggle.pro/api/v1/payment/model-price" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedream45",
    "generate_type": "ImageService.Txt2Img",
    "duration": 0
  }'
```

**视频生成价格**:

```bash
curl -X POST "https://giggle.pro/api/v1/payment/model-price" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan25",
    "generate_type": "VideoService.Img2Video",
    "duration": 5
  }'
```

**响应示例** (视频):

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "model": "wan25",
    "generate_type": "VideoService.Img2Video",
    "price": 88
  }
}
```

**支持的模型**:

- 图生图: `kling25`, `kling21`, `seedream45`
- generate_type:
  - `VideoService.Img2Video` - 图生视频
  - `ImageService.Txt2Img` - 文生图

### optimize-prompt（提示词优化）

用 wan2.5 模型时需要先优化提示词：

```bash
curl -X POST "https://giggle.pro/api/v1/storyboard-shots/optimize-prompt" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "xxx",
    "model": "wan25"
  }'
```

### generate-video（逐个 shot 生成视频）⭐

⚠️ **注意**: `auto-generate-video` 已 deprecated，使用 `generate-video` 逐个 shot 调用

```bash
curl -X POST "https://giggle.pro/api/v1/storyboard-shots/generate-video" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "8df7ef7e-9ed5-43c1-b856-13e17",
    "shot_id": 30542,
    "model": "kling25",
    "prompt": "主体：身穿红色古装...",
    "start_frame": "p2v6c56gwt",
    "end_frame": "",
    "duration": 5,
    "used": true,
    "generating_count": 1,
    "generate_audio": true,
    "optimize_prompt": false,
    "second_model": "wan22",
    "kling26_option": {
      "sync_mode": "voice_sync",
      "is_sync": false
    }
  }'
```

**必需参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| project_id | string | 项目 ID |
| shot_id | integer | 镜头 ID（从 storyboard-shots/list 获取） |
| model | string | 视频模型 |
| prompt | string | 视频提示词（从 shot 的 video_prompt 获取） |
| start_frame | string | 起始帧 asset_id |
| end_frame | string | 结束帧 asset_id（可为空） |
| duration | integer | 视频时长（秒） |
| used | boolean | 生成后是否直接标记为 used |
| generating_count | integer | 生成数量 |
| generate_audio | boolean | 是否生成音频 |
| optimize_prompt | boolean | 是否优化提示词 |

**可选参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| second_model | string | 备用模型 |
| kling26_option | object | kling26 专用选项 |

### ~~auto-generate-video~~ (DEPRECATED)

```bash
# ⚠️ DEPRECATED - 请使用 generate-video 逐个调用
curl -X POST "https://giggle.pro/api/v1/storyboard-shots/auto-generate-video" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "xxx",
    "model": "wan25",
    "duration": 5,
    "generate_audio": true
  }'
```

### auto-generate-image

```bash
curl -X POST "https://giggle.pro/api/v1/storyboard-shots/auto-generate-image" \
  -H "x-auth: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "xxx",
    "model": "seedream45"
  }'
```

## 关键发现

1. **`/project/update` 是核心同步接口** — 每个环节完成后都需要调用
2. **`chat-with-writer`** 返回 Unauthorized，只限前端 Session，API 用 `storyExpansion` 替代
3. **`auto-generate-image`** 和 **`optimize-prompt`** 都需要传 `model` 参数
4. **`model-price`** 需要正确的 `generate_type`:
   - 图片: `ImageService.Txt2Img`
   - 视频: `VideoService.Img2Video`
5. 之前 model-price 报 "record not found" 是因为 model 名或 generate_type 不匹配
6. **`auto-generate-video` 已 deprecated** — 使用 `generate-video` 逐个 shot 调用

## 视频模型

可用模型: `wan25`, `kling25`, `kling26`, `minimax`, `sora2`, `veo31` 等

## 价格参考

| 类型 | 模型       | 单价     |
| ---- | ---------- | -------- |
| 视频 | wan25      | 88 点/个 |
| 图片 | seedream45 | (待查)   |
