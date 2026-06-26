---
name: echoflow-image-gen
description: |
  通过清云 EchoFlow API 生成和编辑图片（基于 Nano Banana Pro / Gemini 3 Pro Image）。
  支持图片生成、单图编辑、多图合成（最多14张）、多种分辨率（1K/2K/4K）。
  触发词：图像生成、图片生成、AI绘画、生成美女、生成图片、Nano Banana Pro、Gemini 图片生成。
  English: Generate or edit images via EchoFlow API using Nano Banana Pro (Gemini 3 Pro Image).
  Supports image generation, editing, and multi-image composition (up to 14 images) with resolutions 1K/2K/4K.
homepage: https://api.echoflow.cn/
metadata:
  openclaw:
    emoji: "🍌"
    requires:
      bins: ["uv"]
      env: ["ECHOFLOW_API_KEY"]
    primaryEnv: "ECHOFLOW_API_KEY"
---

# EchoFlow 图片生成 (Nano Banana Pro) / Image Generation

通过清云 EchoFlow API 使用 Nano Banana Pro (Gemini 3 Pro Image) 生成或编辑图片。

Generate or edit images using EchoFlow API with Nano Banana Pro (Gemini 3 Pro Image).

## 需求 / Requirements

- **`uv`** 运行时 — 用于执行捆绑的 Python 脚本，自动管理依赖
  *uv runtime — runs the bundled Python script with auto-managed dependencies*
- **`ECHOFLOW_API_KEY`** — 你的清云 API 密钥 / Your EchoFlow API key: https://api.echoflow.cn/
- Python 包（由 `uv` 自动安装）: `httpx>=0.25.0`, `pillow>=10.0.0`
  *(auto-installed by `uv`)*

## 安装 / Setup

**第一步 — 安装 `uv`** / Install `uv`:

```powershell
# Windows (pip)
pip install uv

# Windows (Scoop)
scoop install uv

# macOS (Homebrew)
brew install uv

# Linux (curl | sh — 检查脚本后再运行 / Inspect script before running)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**第二步 — 设置 API 密钥** / Set your API key:

```powershell
# Windows — 当前会话 / Current session
$env:ECHOFLOW_API_KEY = "sk-..."

# Windows — 永久设置 / Permanent (user-level)
[Environment]::SetEnvironmentVariable("ECHOFLOW_API_KEY", "sk-...", "User")

# macOS / Linux
export ECHOFLOW_API_KEY="sk-..."
```

> ⚠️ **安全建议 / Security note**: 优先使用环境变量而非 `--api-key`，因为命令行参数会暴露在进程列表和 shell 历史中。  
> *Prefer the `ECHOFLOW_API_KEY` env var over `--api-key` to avoid key exposure in process lists and shell history.*

## 快速开始 / Quick Start

### 生成图片 / Generate Image

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "a serene mountain landscape at sunset" --filename "mountain.png"
```

### 编辑单张图片 / Edit Single Image

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "add a rainbow in the sky" --filename "edited.png" -i "input.png"
```

### 多图合成（最多14张）/ Multi-Image Composition (up to 14)

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "combined.png" -i img1.png -i img2.png -i img3.png
```

## 参数 / Parameters

| 参数 | 描述 / Description | 默认值 |
|------|---------------------|--------|
| `--prompt`, `-p` | 图片描述（必填）| — |
| `--filename`, `-f` | 输出文件名（必填）| — |
| `--input-image`, `-i` | 输入图片用于编辑/合成（可重复，最多14张）| — |
| `--resolution`, `-r` | 输出分辨率: `1K`, `2K`, `4K` | `1K` |
| `--model`, `-m` | 模型名称 | `gemini-3.1-flash-image-preview` |
| `--api-key`, `-k` | API 密钥（优先使用环境变量）| — |
| `--api-base` | API 地址（见安全警告）| `https://api.echoflow.cn/v1` |

## 可用模型 / Available Models

- **`gemini-3.1-flash-image-preview`** (默认) — 更快，更稳定 / faster, more stable
- **`gemini-3-pro-image-preview`** — 更高质量，可能遇到 429 限流 / higher quality, may hit 429

## 分辨率 / Resolutions

- **1K** (默认 / default) — 标准画质
- **2K** — 高画质 / high quality
- **4K** — 超高画质 / ultra high quality

**自动检测 / Auto-detection**: 编辑图片时，分辨率根据最大输入图片尺寸自动调整（≥3000px → 4K, ≥1500px → 2K, 否则 1K）

## 安全说明 / Security Notes

> **API 密钥范围**: 脚本仅从 `ECHOFLOW_API_KEY` 环境变量或 `--api-key` 参数读取密钥，**不会**回退到 `OPENAI_API_KEY` 或 `GEMINI_API_KEY`。

> **`--api-base` 风险**: API 密钥会以 Authorization 头发送到指定的主机。**不要**将其指向不信任的端点，始终使用默认地址 `https://api.echoflow.cn/v1` 或你完全信任的主机。

> **CLI 密钥暴露**: 通过 `--api-key` 传入密钥会暴露在进程列表和 shell 历史中。请使用 `ECHOFLOW_API_KEY` 环境变量。

## 示例 / Examples

```bash
# 简单生成
uv run {baseDir}/scripts/generate_image.py -p "a cute cat wearing a hat" -f "cat.png"

# 高分辨率
uv run {baseDir}/scripts/generate_image.py -p "futuristic city" -f "city.png" -r 4K

# 编辑单图 — 添加雪花
uv run {baseDir}/scripts/generate_image.py -p "add snow to the scene" -f "snowy.png" -i summer.png

# 多图合成
uv run {baseDir}/scripts/generate_image.py -p "create a collage" -f "collage.png" -i a.png -i b.png -i c.png

# 使用 Pro 模型
uv run {baseDir}/scripts/generate_image.py -p "abstract art" -f "art.png" -m "gemini-3-pro-image-preview"
```

## API 参考 / API Reference

详细 API 文档见 / See detailed API docs at: [echoflow_api.md](references/echoflow_api.md)
