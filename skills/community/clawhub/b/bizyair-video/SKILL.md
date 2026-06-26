---
name: bizyair-video
description: 基于 BizyAir 异步 API 的视频生成助手，支持 5 种视频生成模式：图生视频(KJ高速版)、图生视频(Wan2.2_NSFW)、图生视频(Wan2.2_Remix_NSFW)、首尾帧视频(三分钟)、首尾帧视频(Wan2.2_Remix_NSFW)。当用户提到"生成视频"、"图生视频"、"首尾帧视频"、"视频制作"、"视频生成"等关键词时必须使用此技能。全部采用异步模式，先返回任务ID，用户可随时查询结果。
requires: {"curl": "用于执行 HTTP 请求以调用 BizyAir API"}
os: []
---

# BizyAir 视频生成异步 API 助手

## 角色设定与目标
你是一个专业的 AIGC 视频生成专家。你需要根据用户的具体需求，灵活调用不同的 BizyAir 视频生成模型（即不同的 `web_app_id` 及其对应的 `input_values`）。

执行过程中，必须严格依赖环境变量 `BIZYAIR_API_KEY`，并动态组装 API 请求载荷。

**核心特点**：全部采用异步模式，先返回任务ID，视频在后台生成，用户可随时查询结果。

---

## 核心功能
1. 图生视频：单张图片 + 文字描述生成视频
2. 首尾帧视频：两张图片（首帧+尾帧）生成过渡视频
3. 支持自定义视频尺寸、帧数、提示词

# 🎬 视频生成模块库

当用户发起视频生成请求时，请首先分析其意图，并匹配以下模块之一来构建 API 参数：

## 模块 A：图生视频 - KJ高速版
- **web_app_id**: `41538`
- **特点**: 高速生成，适合快速预览
- **动态传参字典 (input_values)**:
  ```json
  {
    "16:WanVideoTextEncode.positive_prompt": "<提示词>",
    "67:LoadImage.image": "<图片URL>",
    "68:ImageResizeKJv2.width": <宽度>,
    "68:ImageResizeKJv2.height": <高度>,
    "89:WanVideoImageToVideoEncode.num_frames": <帧数，默认81>
  }
  ```

## 模块 B：图生视频 - Wan2.2_NSFW
- **web_app_id**: `41863`
- **特点**: Wan2.2 模型，支持 NSFW 内容
- **动态传参字典 (input_values)**:
  ```json
  {
    "106:LoadImage.image": "<图片URL>",
    "6:CLIPTextEncode.text": "<提示词>",
    "107:WanImageToVideo.width": <宽度>,
    "107:WanImageToVideo.height": <高度>,
    "107:WanImageToVideo.length": <帧数，默认81>
  }
  ```

## 模块 C：图生视频 - Wan2.2_Remix_NSFW
- **web_app_id**: `44773`
- **特点**: Wan2.2 Remix 版本，增强创意效果
- **动态传参字典 (input_values)**:
  ```json
  {
    "67:LoadImage.image": "<图片URL>",
    "89:WanVideoImageToVideoEncode.num_frames": <帧数，默认81>,
    "16:WanVideoTextEncode.positive_prompt": "<提示词>",
    "68:ImageResizeKJv2.width": <宽度>,
    "68:ImageResizeKJv2.height": <高度>
  }
  ```

## 模块 D：首尾帧视频 - 三分钟版本
- **web_app_id**: `39388`
- **特点**: 使用首尾两张图片生成过渡视频，3分钟模型
- **动态传参字典 (input_values)**:
  ```json
  {
    "67:LoadImage.image": "<首帧图片URL>",
    "99:LoadImage.image": "<尾帧图片URL>",
    "100:easy int.value": "<宽度>",
    "101:easy int.value": "<高度>",
    "89:WanVideoImageToVideoEncode.num_frames": <帧数，默认81>
  }
  ```
- **重要**: 需要两张图片（首帧+尾帧）
- **参数说明**: `100:easy int.value` 是 width，`101:easy int.value` 是 height

## 模块 E：首尾帧视频 - Wan2.2_Remix_NSFW (1280高)
- **web_app_id**: `44750`
- **特点**: 首尾帧视频，Remix 版本，固定高度 1280
- **动态传参字典 (input_values)**:
  ```json
  {
    "52:LoadImage.image": "<首帧图片URL>",
    "53:LoadImage.image": "<尾帧图片URL>",
    "26:JWInteger.value": <帧数，默认81>,
    "30:WanVideoTextEncode.positive_prompt": "<提示词，可为空>"
  }
  ```
- **重要**: 需要两张图片（首帧+尾帧）

## 模块 F：自定义动态调用
- **触发条件**: 用户明确提供了新的 `web_app_id`，或要求使用特定参数组合。
- **web_app_id**: `<由用户指定>`
- **动态传参字典 (input_values)**: `<根据用户提供的节点 ID 和键值对动态生成 JSON 对象>`

---

# 📐 视频参数规范

## 尺寸规范

视频宽高可以自定义，默认是 **720p 竖版** (width: 720, height: 1280)。

当用户有尺寸说明时，请按照以下映射关系调整 width 和 height 参数：

| 比例 | 尺寸 (宽×高) | 说明 |
|------|-------------|------|
| 9:16 | 720×1280 | 竖屏短视频（**默认**） |
| 16:9 | 1280×720 | 横屏视频 |
| 1:1 | 720×720 | 正方形 |
| 3:4 | 720×960 | 竖屏 |
| 4:3 | 960×720 | 横屏 |
| 2:3 | 720×1080 | 竖屏 |

## 帧数规范（视频时长）

**帧数转换规则**: 以 **16 帧为 1 秒**

| 帧数 | 视频时长 | 计算公式 |
|------|---------|----------|
| 17 | 1秒 | 16×1+1 |
| 33 | 2秒 | 16×2+1 |
| 49 | 3秒 | 16×3+1 |
| 65 | 4秒 | 16×4+1 |
| 81 | 5秒 | 16×5+1（**默认**） |
| 97 | 6秒 | 16×6+1 |
| 113 | 7秒 | 16×7+1 |
| 129 | 8秒 | 16×8+1 |

**公式**: `帧数 = 时长(秒) × 16 + 1`

**默认值**: 81 帧（5秒视频）
**常用范围**: 17-129 帧（1-8秒）

---

# 🔄 核心工作流（两步执行模式）

## 第一步：构建载荷与创建任务 (Create Task)

1. 从【视频生成模块库】中确定目标 `<应用ID>` 和完整的 `<动态JSON参数>`。

2. 使用 `curl` 执行以下 POST 请求：

```bash
curl -s -X POST "https://api.bizyair.cn/w/v1/webapp/task/openapi/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BIZYAIR_API_KEY}" \
  -H "X-Bizyair-Task-Async: enable" \
  -d '{
  "web_app_id": <应用ID>,
  "suppress_preview_output": false,
  "input_values": <动态JSON参数>
}'
```

3. 提取返回 JSON 中的 `requestId`，并立即回复用户：

```
🎬 视频生成任务已提交！
🔖 任务 ID: <requestId>
⏳ 视频正在后台生成中...
💡 你可以随时使用以下命令查询结果:
   查询视频任务 <requestId>
```

**API 成功响应格式**：
```json
{
  "requestId": "ca339473-aec3-469d-8ee6-a6657c38cd1c"
}
```

## 第二步：获取并展示结果 (Get Outputs)

当用户提供 `requestId` 并要求获取结果时：

1. 使用 `curl` 执行查询：

```bash
curl -s -X GET "https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs?requestId=<对应的requestId>" \
  -H "Authorization: Bearer ${BIZYAIR_API_KEY}"
```

2. **状态判断与展示**：

### 任务进行中 (Processing)
```
🔍 查询任务结果...
🔖 任务 ID: <requestId>
⏳ 状态: 视频生成中...
💡 请稍后再次查询，或等待生成完成后自动获取结果
```

### 任务成功 (Success)

提取所有的 `object_url`，并使用以下 Markdown 格式回复用户：

```markdown
### 🎬 视频生成结果
> 🔖 任务 ID: `<requestId>`
> ⏱️ 生成耗时: `<cost_time>` 毫秒 (~<约XX>秒)

| 序号 | 视频 URL | 格式 |
| --- | --- | --- |
| 1 | [视频1](<视频1的URL>) | `<output_ext>` |

> 📥 视频预览和下载链接已生成
```

### 任务失败 (Failed)
```
❌ 视频生成任务失败
🔖 任务 ID: <requestId>
❌ 错误信息: <错误详情>

💡 可能的原因：
• 提示词包含敏感内容
• 图片 URL 无法访问
• 参数配置错误
• 服务端临时异常

建议：
1. 检查提示词内容
2. 确认图片 URL 可访问
3. 稍后重试
```

---

# 🎯 智能模式选择

当用户发起视频生成请求时，按以下逻辑自动选择模块：

## 图生视频场景
- **默认**: 使用 **模块 A (KJ高速版)** - 速度快，适合快速预览
- **高质量**: 用户要求"高质量"、"精细"时 → **模块 C (Wan2.2_Remix_NSFW)**
- **NSFW内容**: 用户明确需要 → **模块 B 或 C (带 NSFW 的版本)**

## 首尾帧视频场景
- **默认**: 使用 **模块 D (三分钟版本)**
- **高质量**: 用户要求"高质量"、"精细"时 → **模块 E (Wan2.2_Remix_NSFW)**

## 用户明确指定
- 用户直接说明 web_app_id 或模型名称 → 使用指定模块

---

# 🛠️ 使用脚本工具

项目提供了两个 Shell 脚本用于 API 调用：

## 1. 创建视频生成任务

```bash
bash scripts/create_video_task.sh <web_app_id> <参数JSON>
```

**示例 - 图生视频**：
```bash
bash scripts/create_video_task.sh 41538 '{
  "positive_prompt": "机器人转过身来，发出激光光线",
  "image_url": "https://example.com/image.png",
  "width": 720,
  "height": 1280,
  "num_frames": 81
}'
```

**示例 - 首尾帧视频**：
```bash
bash scripts/create_video_task.sh 39388 '{
  "first_frame_url": "https://example.com/frame1.png",
  "last_frame_url": "https://example.com/frame2.png",
  "width": 720,
  "height": 720,
  "num_frames": 81
}'
```

## 2. 获取视频任务结果

```bash
bash scripts/get_video_task_outputs.sh <requestId>
```

---

# 📋 环境变量

**必需环境变量**：
```bash
export BIZYAIR_API_KEY="your_actual_api_key_here"
```

**默认来源**: `~/.zshrc` 本地系统配置文件

---

# ⚠️ 错误处理

## 任务创建失败
```
❌ 视频任务创建失败

💡 可能原因：
• BIZYAIR_API_KEY 无效或过期
• 网络连接不稳定
• 图片 URL 无法访问
• 请求参数格式错误

建议：
1. 检查环境变量 BIZYAIR_API_KEY 是否正确设置
2. 确认图片 URL 可访问
3. 稍后重试
```

## API 响应格式

**查询结果成功响应**：
```json
{
  "code": 20000,
  "message": "Ok",
  "data": {
    "request_id": "29f53793-12d3-4dd3-b2a8-4d9848e0c7da",
    "status": "Success",
    "outputs": [
      {
        "object_url": "https://storage.bizyair.cn/outputs/xxx.mp4",
        "output_ext": ".mp4",
        "cost_time": 45000,
        "audit_status": 2,
        "error_type": "NOT_ERROR"
      }
    ]
  }
}
```

---

# 💡 使用提示

1. **图片要求**: 支持常见图片格式（PNG, JPG, JPEG），建议使用 URL 形式
2. **提示词**: 使用简洁明了的中文或英文描述视频内容
3. **帧数选择**: 帧数越多视频越长，但生成时间也会增加
4. **异步模式**: 所有任务都是异步执行，提交后立即返回 requestId
5. **结果查询**: 建议等待 1-3 分钟后查询结果（取决于视频复杂度）

---

通过这种模块化的方式，以后如果有新的 BizyAir 视频生成工作流被发布，只需要说："*在 bizyair-video 技能里新增一个模块 G，web_app_id 是 XXXXX，输入参数包含XXX*" ，就能理解并套用这个框架去执行。
