---
name: ace-banana2
description: Generate and edit images using the AceData Nano Banana API. Supports models like nano-banana-2, custom aspect ratios (default 16:9), and resolutions (default 2K). Handles batch generation and image-to-image (edit) tasks with local files. Use when the user wants to generate or edit high-quality images via Nano Banana.
---

# Ace Banana2 Image Generation / Ace Banana2 图像生成

**English** | **中文**

---

## Overview / 概述

**English:**  
Ace Banana2 is a powerful image generation and editing skill that leverages the AceData Nano Banana API. It provides a seamless workflow for creating high-quality images from text prompts or editing existing images with AI-powered transformations. The skill supports multiple models, customizable parameters, and automatic saving of generated images to your desktop.

**中文:**  
Ace Banana2 是一个功能强大的图像生成和编辑技能，基于 AceData Nano Banana API。它提供了一个无缝的工作流程，可以从文本提示生成高质量图像，或使用 AI 驱动的转换编辑现有图像。该技能支持多种模型、可自定义参数，并自动将生成的图像保存到桌面。

---

## Model Introduction / 模型介绍

**English:**  
The Nano Banana API offers several cutting‑edge image generation models:

- **nano‑banana‑2** (default): Professional‑quality image generation with flash speed. Ideal for most creative tasks.
- **nano‑banana‑pro**: Enhanced model for image‑to‑image editing and higher‑fidelity outputs.
- **nano‑banana**: The original model, suitable for general‑purpose generation.

All models support resolutions up to **4K** and aspect ratios such as **16:9**, **1:1**, **4:3**, etc.

**中文:**  
Nano Banana API 提供多种先进的图像生成模型：

- **nano‑banana‑2**（默认）：具有快速生成速度的专业级图像生成模型，适合大多数创意任务。
- **nano‑banana‑pro**：增强模型，适用于图像到图像的编辑和更高保真度的输出。
- **nano‑banana**：原始模型，适合通用生成。

所有模型支持高达 **4K** 的分辨率和 **16:9**、**1:1**、**4:3** 等宽高比。

---

## API Key Application / API 密钥申请说明

**English:**  
To use this skill, you need an AceData API key (Bearer Token). Follow these steps:

1. Visit the [AceData registration page](https://share.acedata.cloud/r/1uN83988Tn).
2. Sign up or log in to your AceData account.
3. Navigate to the **API Keys** section in your dashboard.
4. Generate a new API key (Bearer Token) with access to the **Nano Banana** service.
5. Copy the key and keep it secure.

**中文:**  
使用本技能需要 AceData API 密钥（Bearer Token）。请按以下步骤操作：

1. 访问 [AceData 注册页面](https://share.acedata.cloud/r/1uN83988Tn)。
2. 注册或登录您的 AceData 账户。
3. 在控制台中转到 **API Keys** 部分。
4. 生成一个新的 API 密钥（Bearer Token），确保其具有 **Nano Banana** 服务的访问权限。
5. 复制密钥并妥善保管。

---

## Installation & Usage Steps / 安装与使用步骤

### Step 1: Install Dependencies / 第一步：安装依赖

**English:**  
Ensure you have Python 3.7+ installed. Then install required packages:

```bash
pip install requests pillow
```

**中文:**  
确保已安装 Python 3.7+，然后安装所需包：

```bash
pip install requests pillow
```

### Step 2: Configure API Key / 第二步：配置 API 密钥

**English:**  
Run the script once, and it will prompt you to enter your Bearer Token. The token will be saved in a `.env` file inside the skill directory for future use.

**中文:**  
运行脚本一次，它将提示您输入 Bearer Token。令牌将保存在技能目录的 `.env` 文件中，供以后使用。

### Step 3: Run the Script / 第三步：运行脚本

**English:**  
Navigate to the skill directory and execute:

```bash
python scripts/generate_images.py
```

You will be prompted for a text description (prompt) or can provide command‑line arguments.

**中文:**  
进入技能目录并执行：

```bash
python scripts/generate_images.py
```

系统将提示您输入文本描述（提示词），或者您可以直接提供命令行参数。

---

## Features / 功能特性

**English:**  
- **Dual‑mode Operation**: Supports both text‑to‑image (`generate`) and image‑to‑image (`edit`) workflows.
- **Local & Remote Images**: Upload up to 4 local images (converted to Base64) or provide image URLs.
- **Automatic Image Resizing**: Large images are automatically resized to comply with API limits.
- **Batch Generation**: Generate multiple images in a single request.
- **Smart Saving**: Images are saved to a dated folder on your desktop with unique timestamps.
- **Detailed Logging**: Full JSON response is displayed for debugging and transparency.

**中文:**  
- **双模式操作**：支持文生图（`generate`）和图生图（`edit`）工作流。
- **本地与远程图像**：最多上传 4 张本地图像（转换为 Base64）或提供图像 URL。
- **自动图像调整**：大图像自动调整大小以符合 API 限制。
- **批量生成**：单次请求生成多张图像。
- **智能保存**：图像保存到桌面的日期文件夹中，文件名包含唯一时间戳。
- **详细日志**：显示完整的 JSON 响应，便于调试和透明化。

---

## Parameters / 参数详解

| Parameter / 参数 | Default / 默认值 | Description / 说明 |
|------------------|------------------|-------------------|
| `--prompt` | (required for generate) | Text description of the desired image / 期望图像的文本描述 |
| `--count` | `1` | Number of images to generate / 要生成的图像数量 |
| `--model` | `nano-banana-2` | Model to use (`nano-banana-2`, `nano-banana-pro`, `nano-banana`) / 使用的模型 |
| `--resolution` | `2K` | Output resolution (`2K`, `4K`, etc.) / 输出分辨率 |
| `--aspect_ratio` | `16:9` | Aspect ratio (`16:9`, `1:1`, `4:3`, etc.) / 宽高比 |
| `--image` | (optional) | Local image paths or URLs for edit mode (max 4) / 编辑模式的本地图像路径或 URL（最多 4 个） |
| `--api_key` | (optional) | Bearer Token for AceData API / AceData API 的 Bearer Token |

---

## Examples / 示例

### Example 1: Basic Text‑to‑Image / 示例 1：基础文生图

**English:**  
```bash
python scripts/generate_images.py --prompt "a serene mountain landscape at sunset" --count 2 --resolution "4K"
```

**中文:**  
```bash
python scripts/generate_images.py --prompt "日落时宁静的山景" --count 2 --resolution "4K"
```

### Example 2: Image Editing / 示例 2：图像编辑

**English:**  
```bash
python scripts/generate_images.py --image "input.jpg" --prompt "make it look like a watercolor painting"
```

**中文:**  
```bash
python scripts/generate_images.py --image "input.jpg" --prompt "让它看起来像水彩画"
```

### Example 3: Batch Generation with Custom Aspect Ratio / 示例 3：自定义宽高比的批量生成

**English:**  
```bash
python scripts/generate_images.py --prompt "cyberpunk city street" --count 4 --aspect_ratio "1:1"
```

**中文:**  
```bash
python scripts/generate_images.py --prompt "赛博朋克城市街道" --count 4 --aspect_ratio "1:1"
```

---

## Notes / 注意事项

**English:**  
- The API may have rate limits and usage quotas. Check your AceData dashboard for details.
- Generated images are stored on AceData's CDN for a limited time; download them promptly.
- For large images (>1 MB), the script automatically resizes them to avoid timeout errors.
- Ensure your internet connection is stable during generation (requests can take up to 180 seconds).

**中文:**  
- API 可能有速率限制和使用配额。请查看您的 AceData 控制台了解详情。
- 生成的图像在 AceData 的 CDN 上存储时间有限，请及时下载。
- 对于大图像（>1 MB），脚本会自动调整大小以避免超时错误。
- 生成期间请确保网络连接稳定（请求可能长达 180 秒）。

---

## References / 参考资料

- [API Documentation](references/api_docs.md) – Detailed Nano Banana API specifications.
- [AceData Cloud Platform](https://platform.acedata.cloud) – Manage your API keys and usage.
