# Agnes Video V2.0 API

## 端点

### 创建视频任务

```
POST https://apihub.agnes-ai.com/v1/videos
```

### 查询任务状态

```
GET https://apihub.agnes-ai.com/agnesapi?video_id={video_id}
```

## 请求格式

### 文生视频

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "A cat walking on the beach at sunset, cinematic, golden hour lighting",
  "mode": "ti2vid",
  "width": 1152,
  "height": 768,
  "num_frames": 121,
  "frame_rate": 24
}
```

### 图生视频

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "The woman slowly turns around and looks back",
  "mode": "ti2vid",
  "image": "https://example.com/photo.jpg",
  "width": 1152,
  "height": 768,
  "num_frames": 121,
  "frame_rate": 24
}
```

### 多图视频

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "Create a smooth transformation between the two images",
  "mode": "multi",
  "extra_body": {
    "image": ["https://example.com/a.png", "https://example.com/b.png"]
  },
  "width": 1152,
  "height": 768,
  "num_frames": 121,
  "frame_rate": 24
}
```

### 关键帧动画

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "Smooth cinematic transition between keyframes",
  "mode": "keyframes",
  "extra_body": {
    "image": ["https://example.com/kf1.png", "https://example.com/kf2.png"],
    "mode": "keyframes"
  },
  "width": 1152,
  "height": 768,
  "num_frames": 121,
  "frame_rate": 24
}
```

## 响应格式

### 创建任务响应

```json
{
  "video_id": "video_123456789",
  "task_id": "task_123456789",
  "status": "pending"
}
```

### 查询状态响应

```json
{
  "video_id": "video_123456789",
  "task_id": "task_123456789",
  "status": "completed",
  "progress": 100,
  "remixed_from_video_id": "https://cdn.example.com/video.mp4"
}
```

### 失败响应

```json
{
  "video_id": "video_123456789",
  "task_id": "task_123456789",
  "status": "failed",
  "progress": 0,
  "error": "Error message here"
}
```

## 参数说明

### 必填参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型名称：`agnes-video-v2.0` |
| `prompt` | string | 视频内容的文本描述 |
| `mode` | string | 工作流模式：`ti2vid` / `multi` / `keyframes` |
| `width` | integer | 视频宽度 |
| `height` | integer | 视频高度 |
| `num_frames` | integer | 帧数（必须遵循 `8n + 1` 规则） |
| `frame_rate` | integer | 帧率 |

### 可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `image` | string | 单张图片 URL（用于图生视频） |
| `extra_body.image` | array | 多张图片 URL 列表（用于多图视频/关键帧） |
| `extra_body.mode` | string | 关键帧模式标识 |
| `negative_prompt` | string | 反向提示词 |
| `seed` | integer | 随机种子 |

## 分辨率档位

| 档位 | 尺寸 | 推荐场景 |
|------|------|----------|
| 480p | `854x480` | 移动端预览、快速测试 |
| 720p | `1152x768` (16:9) / `768x1152` (9:16) | 标准视频、社交内容 |
| 1080p | `1920x1080` (16:9) / `1080x1920` (9:16) | 高品质输出 |

## 时长与帧数

| 目标时长 | 推荐 `num_frames` |
|----------|-------------------|
| 约 3 秒 | 81 |
| 约 5 秒 | 121 |
| 约 10 秒 | 241 |
| 约 18 秒 | 441 |

> **注意**：`num_frames` 必须 ≤ 441 且遵循 `8n + 1` 规则。

## 认证

使用 Bearer Token 认证：

```
Authorization: Bearer YOUR_API_KEY
```

## 错误处理

### 常见错误

| 错误码 | 说明 |
|--------|------|
| 401 | API Key 无效或未提供 |
| 400 | 请求格式错误 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## 最佳实践

1. **异步处理**：视频生成是异步的，需要轮询状态
2. **帧数规则**：严格遵循 `8n + 1` 帧数规则
3. **超时设置**：建议设置 300 秒超时
4. **轮询间隔**：建议每 5 秒查询一次状态
5. **错误重试**：实现指数退避重试机制

## 工作流程

```
1. 创建任务 → 获取 video_id 和 task_id
2. 轮询状态 → 每 5 秒查询一次
3. 获取结果 → 任务完成后下载视频
4. 超时处理 → 最多等待 300 秒
```
