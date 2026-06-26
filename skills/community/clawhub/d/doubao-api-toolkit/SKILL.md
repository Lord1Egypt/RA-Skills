---
name: doubao-api-toolkit
version: 1.0.0
description: "Doubao (Volcengine ARK) API Toolkit - Cross-platform Python implementation for text-to-image, image-to-image, text-to-video, and vision analysis. 豆包API工具包 - 跨平台Python实现，支持文生图、图生图、文生视频和视觉分析。"
author: "OpenClaw"
tags: ["image", "video", "vision", "doubao", "volcengine", "ark", "multimodal"]
---

# Doubao API Toolkit / 豆包 API 工具包

> **English**: A cross-platform Python toolkit for Doubao (ByteDance Volcengine ARK) API, supporting text-to-image, text-to-video, image/video analysis, and more.
> 
> **中文**: 豆包（字节跳动火山引擎ARK）API的跨平台Python工具包，支持文生图、文生视频、图片/视频分析等功能。

---

## 🚀 Quick Start / 快速开始

### Prerequisites / 前置条件

- **English**: Python 3.8+ with `requests` library
- **中文**: Python 3.8+ 及 `requests` 库

```bash
pip install requests
```

### Configuration / 配置

Set your ARK API Key as an environment variable:
将 ARK API Key 设置为环境变量：

```bash
# Linux/Mac
export ARK_API_KEY="your_api_key_here"

# Windows PowerShell
$env:ARK_API_KEY="your_api_key_here"

# Windows CMD
set ARK_API_KEY=your_api_key_here
```

Get your API Key from: https://console.volcengine.com/ark
从控制台获取 API Key：https://console.volcengine.com/ark

---

## 📚 Usage / 使用方法

### 1. Generate Image from Text / 文生图

**English**: Generate an image using text description
**中文**: 使用文本描述生成图片

```bash
python doubao_toolkit.py img "一只可爱的橘猫在阳光下睡觉" --size 1024x1024
```

**Output / 输出**:
```json
{
  "status": "success",
  "image_url": "https://...",
  "local_path": "/path/to/img_20260322_201500.jpeg",
  "prompt": "一只可爱的橘猫在阳光下睡觉"
}
```

### 2. Generate Video from Text / 文生视频

**English**: Generate a video using text description
**中文**: 使用文本描述生成视频

```bash
# Synchronous mode (wait for completion) / 同步模式（等待完成）
python doubao_toolkit.py vid "一只猫在草地上奔跑" --duration 5 --ratio 16:9

# Asynchronous mode (return task ID) / 异步模式（返回任务ID）
python doubao_toolkit.py vid "一只猫在草地上奔跑" --duration 5 --async
```

### 3. Generate Video from Image / 图生视频

**English**: Generate video using an image as the first frame
**中文**: 使用图片作为首帧生成视频

```bash
python doubao_toolkit.py vid "让这只猫动起来" --image "https://example.com/cat.jpg"
```

### 4. Analyze Image / 图片分析

**English**: Analyze image content using vision model
**中文**: 使用视觉模型分析图片内容

```bash
python doubao_toolkit.py analyze-img "https://example.com/image.jpg" --prompt "描述这张图片的细节"
```

### 5. Analyze Video / 视频分析

**English**: Analyze video content using vision model
**中文**: 使用视觉模型分析视频内容

```bash
python doubao_toolkit.py analyze-vid "/path/to/video.mp4" --prompt "总结这个视频的主要内容"
```

### 6. Check Video Status / 检查视频状态

**English**: Check the status of a video generation task
**中文**: 检查视频生成任务的状态

```bash
python doubao_toolkit.py status "cgt-20260322xxxxx"
```

---

## 🔧 Available Models / 可用模型

| Model ID | Function | Description |
|----------|----------|-------------|
| `doubao-seedream-3-0-t2i-250415` | Text-to-Image / 文生图 | Generate images from text |
| `doubao-seededit-3-0-i2i-250628` | Image-to-Image / 图生图 | Edit images |
| `doubao-seedance-1-0-pro-250528` | Text-to-Video / 文生视频 | Generate videos from text or images |
| `doubao-1-5-vision-pro-32k-250115` | Vision Analysis / 视觉分析 | Analyze images and videos |
| `doubao-1-5-pro-32k-250115` | Chat / 对话 | General chat and text generation |

---

## 📖 API Reference / API 参考

### Class: DoubaoClient

#### `generate_image(prompt, size="1024x1024", n=1)`

**English**: Generate image from text description
**中文**: 根据文本描述生成图片

**Parameters / 参数**:
- `prompt` (str): Text description / 文本描述
- `size` (str): Image size (1024x1024, 1024x1536, 1536x1024) / 图片尺寸
- `n` (int): Number of images to generate / 生成数量

**Returns / 返回**:
```python
{
    "status": "success",
    "image_url": "https://...",
    "local_path": "/path/to/image.jpeg",
    "prompt": "..."
}
```

#### `generate_video(prompt, duration=5, ratio="16:9", image_url=None, sync=True)`

**English**: Generate video from text or image
**中文**: 根据文本或图片生成视频

**Parameters / 参数**:
- `prompt` (str): Text description / 文本描述
- `duration` (int): Video duration in seconds (2-12) / 视频时长（秒）
- `ratio` (str): Aspect ratio (16:9, 4:3, 1:1, 9:16) / 宽高比
- `image_url` (str, optional): Image URL for image-to-video / 图生视频的图片URL
- `sync` (bool): Wait for completion if True / 是否同步等待

#### `analyze_image(image_url, prompt="描述这张图片")`

**English**: Analyze image content
**中文**: 分析图片内容

**Parameters / 参数**:
- `image_url` (str): URL of the image / 图片URL
- `prompt` (str): Analysis prompt / 分析提示词

**Returns / 返回**: Analysis result text / 分析结果文本

#### `analyze_video(video_path, prompt="分析这个视频")`

**English**: Analyze video content
**中文**: 分析视频内容

**Parameters / 参数**:
- `video_path` (str): Path to local video file / 本地视频文件路径
- `prompt` (str): Analysis prompt / 分析提示词

---

## 📊 Performance / 性能指标

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Text-to-Image / 文生图 | 10-30 seconds | Depends on complexity |
| Text-to-Video / 文生视频 | 1-3 minutes | 5-second video |
| Image Analysis / 图片分析 | 5-15 seconds | Depends on image size |
| Video Analysis / 视频分析 | 10-30 seconds | Depends on video length |

---

## 🐛 Troubleshooting / 故障排除

### Error: "ARK_API_KEY environment variable not set"

**Solution / 解决方法**:
```bash
export ARK_API_KEY="your_api_key"
```

### Error: "InvalidEndpointOrModel.NotFound"

**English**: The model is not activated. Go to Volcengine Console → Model Management and activate the required models.
**中文**: 模型未开通。请前往火山引擎控制台 → 模型管理，开通所需模型。

Required models / 需要开通的模型:
- Doubao-SeeDream-3.0-T2I (Text-to-Image)
- Doubao-Seedance-1.0-Pro (Text-to-Video)
- Doubao-1.5-Vision-Pro (Vision Analysis)

### Error: "Insufficient balance"

**English**: Your account balance is insufficient. Please recharge your account.
**中文**: 账户余额不足，请充值。

---

## 🔐 Security / 安全

**English**: 
- Never hardcode API keys in your code
- Use environment variables to store sensitive information
- Regularly rotate your API keys

**中文**:
- 永远不要在代码中硬编码 API Key
- 使用环境变量存储敏感信息
- 定期轮换 API Key

---

## 📁 Output Directory / 输出目录

Generated files are saved to:
生成的文件保存在：

```
~/.openclaw/workspace/output/
├── img_YYYYMMDD_HHMMSS.jpeg    # Generated images / 生成的图片
└── vid_YYYYMMDD_HHMMSS.mp4     # Generated videos / 生成的视频
```

---

## 📚 References / 参考资源

- [Volcengine ARK Documentation / 火山方舟文档](https://www.volcengine.com/docs/82379)
- [Doubao Model Pricing / 豆包模型计费](https://console.volcengine.com/ark)
- [OpenClaw Documentation / OpenClaw 文档](https://docs.openclaw.ai)

---

**Version / 版本**: 1.0.0
**Last Updated / 最后更新**: 2026-03-22
