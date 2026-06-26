---
name: agnes-image-video
description: 使用 Agnes AI 的 Agnes-Image-2.0-Flash 模型生成和编辑图片，以及使用 Agnes-Video-V2.0 模型生成视频。支持文生图、图生图、文生视频、图生视频、多图合成等场景。当用户需要 AI 生成图片、编辑图片、生成视频，或明确提到使用 Agnes Image / Agnes Video 模型时触发此 skill。
agent_created: true
---

# Agnes Image & Video Skill

使用 Agnes AI 全模态 API 进行图片和视频生成。Agnes AI 无限期免费开放文本、图像、视频三大模态 API，OpenAI 兼容接口。

## 快速开始

### 1. 配置 API Key

在使用前，用户需要前往 [Agnes API 平台](https://platform.agnes-ai.com/) 注册并创建 API Key，然后通过对话告知助手。

API Key 以环境变量形式存储，在请求时注入到 Header 中：
```
Authorization: Bearer YOUR_API_KEY
```

### 2. 通用 API 信息

- **Base URL**: `https://apihub.agnes-ai.com/v1`
- **Content-Type**: `application/json`
- **认证**: `Authorization: Bearer {API_KEY}`

---

## 图像生成：Agnes-Image-2.0-Flash

### 端点

```
POST https://apihub.agnes-ai.com/v1/images/generations
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | `"agnes-image-2.0-flash"` |
| `prompt` | string | 是 | 图像生成的文本提示词 |
| `size` | string | 否 | 输出尺寸：`"1024x1024"`, `"1024x768"`, `"768x1024"` |
| `seed` | number | 否 | 随机种子，用于结果可复现 |
| `tags` | array | 否 | 任务类型标记 |
| `extra_body.image` | array | 图生图时是 | 输入图像 URL 数组（支持多张图合成） |
| `extra_body.response_format` | string | 否 | 输出格式：`"url"` |

### 文生图

```python
import httpx

response = httpx.post(
    "https://apihub.agnes-ai.com/v1/images/generations",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "agnes-image-2.0-flash",
        "prompt": "一只可爱的金毛犬在阳光下的草地上微笑，高清摄影风格",
        "size": "1024x1024",
    }
)
result = response.json()
image_url = result["data"][0]["url"]
```

### 图生图

图生图**必须**在 `tags` 中添加 `"img2img"`，否则模型会当作文生图处理：

```python
response = httpx.post(
    "https://apihub.agnes-ai.com/v1/images/generations",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "agnes-image-2.0-flash",
        "prompt": "将狗的衣服改成红色",
        "tags": ["img2img"],
        "extra_body.image": ["https://example.com/input.jpg"],
    }
)
```

### 多图合成

在 `extra_body.image` 中传入多个图像 URL：

```python
response = httpx.post(
    "https://apihub.agnes-ai.com/v1/images/generations",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "agnes-image-2.0-flash",
        "prompt": "将两张图片合成为一张",
        "extra_body.image": ["https://example.com/img1.jpg", "https://example.com/img2.jpg"],
    }
)
```

### 响应格式

```json
{
  "created": 1774432125,
  "data": [
    { "url": "https://..." }
  ],
  "usage": { "generated_images": 1 }
}
```

---

## 视频生成：Agnes-Video-V2.0

视频生成是**异步**过程，分为"创建任务"和"轮询结果"两步。

### 端点

- **创建任务**: `POST https://apihub.agnes-ai.com/v1/videos`
- **查询结果**: `GET https://apihub.agnes-ai.com/v1/videos/{task_id}`

### 创建任务参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | `"agnes-video-v2.0"` |
| `prompt` | string | 是 | 视频内容的文本描述 |
| `image` | string/array | 否 | 输入图片 URL（图生视频时） |
| `mode` | string | 否 | `"ti2vid"` (文生视频) 或 `"keyframes"` (关键帧) |
| `height` | integer | 否 | 视频高度，默认 `768` |
| `width` | integer | 否 | 视频宽度，默认 `1152` |
| `num_frames` | integer | 否 | 视频总帧数，**必须满足 `8n+1` 且 `<= 441`** |
| `num_inference_steps` | integer | 否 | 推理步数，使用默认值即可 |
| `seed` | integer | 否 | 随机种子 |
| `frame_rate` | number | 否 | 视频 FPS，推荐 `24` (范围 1-60) |
| `negative_prompt` | string | 否 | 负向提示词 |
| `extra_body.image` | array | 多图/关键帧时是 | 多图或关键帧的输入图片 URL |
| `extra_body.mode` | string | 关键帧时是 | `"keyframes"` |

### 帧数合法值

`num_frames` 必须满足：`8n + 1` (n 为正整数) 且 `num_frames ≤ 441`。

**合法值**: 81, 121, 161, 201, 241, 281, 321, 361, 401, 441

**非法值**: 100, 150, 200

### 视频时长计算

```
时长(秒) = num_frames / frame_rate
```

例如 `num_frames=121`, `frame_rate=24` → 时长约 5.04 秒。

### 完整调用流程

```python
import httpx
import time

# Step 1: 创建视频任务
create_resp = httpx.post(
    "https://apihub.agnes-ai.com/v1/videos",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "agnes-video-v2.0",
        "prompt": "一只猫在日落时的沙滩上散步，电影级镜头",
        "height": 768,
        "width": 1152,
        "num_frames": 121,
        "frame_rate": 24,
    }
)
task_id = create_resp.json()["task_id"]

# Step 2: 轮询等待结果
while True:
    result = httpx.get(
        f"https://apihub.agnes-ai.com/v1/videos/{task_id}",
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    data = result.json()
    status = data.get("status")

    if status == "completed":
        video_url = data.get("remixed_from_video_id")
        print(f"视频就绪: {video_url}")
        break
    elif status == "failed":
        print("生成失败:", data.get("error"))
        break
    else:
        time.sleep(5)  # 每5秒轮询一次
```

### 响应格式

**创建任务响应**:
```json
{
  "id": "task_xxx",
  "task_id": "task_xxx",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1780457477,
  "seconds": "5.0",
  "size": "1280x768"
}
```

**完成时响应**:
```json
{
  "id": "task_xxx",
  "model": "agnes-video-v2.0",
  "status": "completed",
  "progress": 100,
  "seconds": "5.0",
  "size": "1280x768",
  "remixed_from_video_id": "https://storage.../video_xxxxxx.mp4"
}
```

### 任务状态说明

| 状态 | 说明 |
|------|------|
| `queued` | 排队中，继续轮询 |
| `in_progress` | 生成中，继续轮询 |
| `completed` | 完成，从 `remixed_from_video_id` 获取视频 URL |
| `failed` | 失败，检查 `error` 字段 |

---

## 使用脚本 (scripts/generate.py)

本 skill 附带 Python 脚本 `scripts/generate.py`，可快速调用 API 生成图片或视频。

### 使用方式

```bash
# 设置环境变量
export AGNES_API_KEY="your-api-key-here"

# 生成图片
python scripts/generate.py --mode image --prompt "一只可爱的小猫" --size 1024x1024

# 生成视频
python scripts/generate.py --mode video --prompt "日落时海滩上的猫散步" --height 768 --width 1152 --num_frames 121 --frame_rate 24
```

---

## 注意事项

1. **图生图必须加 `tags: ["img2img"]`**，否则模型会当作文生图处理
2. **视频 `num_frames` 必须满足 `8n+1` 且 `<= 441`**，否则 API 会返回错误
3. 视频生成是异步的，需要轮询 `task_id` 获取结果
4. 所有 API 无限期免费，无需绑定信用卡
5. 生成的图片和视频默认以 URL 形式返回，下载后保存为本地文件
