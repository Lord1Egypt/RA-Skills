---
name: doubao-media
version: 1.0.0
description: "Doubao (Volcengine ARK) 文生图、文生视频工具 - 生成后自动发送到对话，无需手动查找文件。Text-to-image and text-to-video with auto-send to chat."
author: "systiger"
tags: ["image", "video", "doubao", "volcengine", "ark", "multimodal", "ai-generation"]
---

# Doubao Media / 豆包媒体生成

> **中文**: 豆包（字节跳动火山引擎ARK）文生图、文生视频工具。生成后自动发送到对话，无需手动查找文件。
>
> **English**: Doubao (ByteDance Volcengine ARK) text-to-image and text-to-video tool. Auto-sends generated content to chat, no manual file search needed.

---

## Features / 功能特点

| Feature | 中文 | English |
|---------|------|---------|
| Text-to-Image | ✅ 文生图 | ✅ Generate images from text |
| Text-to-Video | ✅ 文生视频 | ✅ Generate videos from text |
| Image-to-Video | ✅ 图生视频 | ✅ Generate videos from images |
| Auto-Send to Chat | ✅ 自动发送到对话 | ✅ Auto-send to conversation |
| Windows Compatible | ✅ Windows 兼容 | ✅ Windows compatible |

---

## Prerequisites / 前置条件

### Required / 必需

- **ARK_API_KEY** - Get from / 从控制台获取: https://console.volcengine.com/ark
- **Python 3.8+** with `requests` library

### Install Dependencies / 安装依赖

```bash
pip install requests
```

### Set API Key / 设置 API Key

```bash
# Windows PowerShell
$env:ARK_API_KEY="your_api_key_here"

# Linux/Mac
export ARK_API_KEY="your_api_key_here"
```

---

## Usage / 使用方法

### Generate Image / 生成图片

```bash
python scripts/doubao_media.py img "一只可爱的橘猫在阳光下睡觉"
```

**Result / 结果:**
- Image saved to `output/` directory / 图片保存到 `output/` 目录
- Auto-sent to chat / 自动发送到对话

### Generate Video / 生成视频

```bash
# Sync mode (wait for completion) / 同步模式（等待完成）
python scripts/doubao_media.py vid "一只猫在草地上奔跑" --duration 5

# Async mode (return task ID) / 异步模式（返回任务ID）
python scripts/doubao_media.py vid "一只猫在草地上奔跑" --async
```

### Generate Video from Image / 图生视频

```bash
python scripts/doubao_media.py vid "让这只猫动起来" --image "https://example.com/cat.jpg"
```

### Check Video Status / 检查视频状态

```bash
python scripts/doubao_media.py status "task_xxxxx"
```

---

## Parameters / 参数说明

### Image Generation / 图片生成

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | Required | Text description / 文本描述 |
| `--size` | 1024x1024 | Image size: 1024x1024, 1024x1536, 1536x1024 |

### Video Generation / 视频生成

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | Required | Text description / 文本描述 |
| `--duration` | 5 | Duration in seconds (2-12) / 时长（秒） |
| `--ratio` | 16:9 | Aspect ratio: 16:9, 4:3, 1:1, 9:16 |
| `--image` | None | Image URL for image-to-video / 图生视频的图片URL |
| `--async` | False | Async mode / 异步模式 |

---

## Available Models / 可用模型

| Model ID | Function | Description |
|----------|----------|-------------|
| `doubao-seedream-3-0-t2i-250415` | Text-to-Image / 文生图 | Generate images from text |
| `doubao-seedance-1-0-pro-250528` | Text-to-Video / 文生视频 | Generate videos from text or images |

---

## Output / 输出

Generated files are saved to / 生成的文件保存到:

```
~/.openclaw/workspace/output/
├── img_YYYYMMDD_HHMMSS.jpeg    # Images / 图片
└── vid_YYYYMMDD_HHMMSS.mp4     # Videos / 视频
```

---

## Performance / 性能指标

| Operation | Time | Description |
|-----------|------|-------------|
| Text-to-Image / 文生图 | 10-30s | Depends on complexity |
| Text-to-Video / 文生视频 | 1-3min | 5-second video |

---

## Troubleshooting / 故障排除

### Error: ARK_API_KEY not set

**Solution / 解决方案:**
```bash
$env:ARK_API_KEY="your_api_key"  # Windows
export ARK_API_KEY="your_api_key"  # Linux/Mac
```

### Error: InvalidEndpointOrModel.NotFound

**Solution / 解决方案:**
Go to Volcengine Console → Model Management and activate the required models.
前往火山引擎控制台 → 模型管理，开通所需模型。

Required models / 需要开通的模型:
- Doubao-SeeDream-3.0-T2I (Text-to-Image)
- Doubao-Seedance-1.0-Pro (Text-to-Video)

### Error: UnicodeEncodeError (Windows)

**Solution / 解决方案:**
The script handles this automatically with `PYTHONIOENCODING=utf-8`.

---

## Security / 安全

- Never hardcode API keys / 永远不要硬编码 API Key
- Use environment variables / 使用环境变量存储敏感信息
- Regularly rotate keys / 定期轮换 API Key

---

## References / 参考资源

- [Volcengine ARK Documentation / 火山方舟文档](https://www.volcengine.com/docs/82379)
- [Doubao Model Pricing / 豆包模型计费](https://console.volcengine.com/ark)

---

**Version / 版本**: 1.0.0
**Last Updated / 最后更新**: 2026-03-29
