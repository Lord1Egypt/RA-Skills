---
name: video-transcriber
description: (已验证) 强大的抖音视频批量转写器，集成了下载、音频提取和本地 Whisper 模型转写功能。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/video-transcriber
  author: an
  tags: [douyin, video, transcription, whisper, ffmpeg, social-media]
  license: MIT
  requirements:
    - python
    - "pip:requests"
    - "pip:openai-whisper"
    - "exec:ffmpeg"
---

# SKILL.md for video-transcriber

## Description

这是一个功能强大且经过实战检验的抖音视频批量转写技能。它将视频下载、音频提取和**本地 AI 模型 (OpenAI Whisper)** 转写三个核心步骤整合进一个自动化的工作流中，能够高效地将一个或多个抖音视频的语音内容，提取为纯文本。

该技能已被完全重构，实现了良好的可移植性和安全性，是进行视频内容分析、文案提取等任务的基础工具。

## ⚠️ Prerequisites (前置条件)

**在使用本技能前，您必须在您的系统上完成以下配置：**

1.  **安装 ffmpeg**: 本技能需要使用 `ffmpeg` 工具来从视频中提取音频。
    *   请从 [ffmpeg 官网](https://ffmpeg.org/download.html) 下载适合您操作系统的版本。
    *   安装后，**必须将 `ffmpeg` 的可执行文件路径添加到您系统的 `PATH` 环境变量中**，以确保本技能可以从任何位置调用它。

2.  **配置 TikHub Token**: 视频下载功能需要一个有效的 TikHub API Token。请在您的 `~/.openclaw/config.json` 文件中添加 `tikhub_api_token`。
    ```json
    {
      "tikhub_api_token": "YOUR_TIKHUB_API_TOKEN"
    }
    ```

## How to Use

该技能的核心脚本 (`scripts/run.py`) 是一个功能完善的命令行工具。

### Parameters

*   **`--url`** (必填, 可重复): 要转写的抖音视频的分享链接。您可以多次使用此参数以进行批量处理。
*   **`--output-file`**: 指定输出报告的 Markdown 文件路径。如果省略，将自动在 `workspace/data/video-transcriber/` 目录下生成一个带时间戳的报告文件。

### Example Invocation

**转写单个视频:**
```powershell
# AI应动态查找 python 路径
python path/to/run.py --url "https://v.douyin.com/iY8K3Nqk/" --output-file "report.md"
```

**批量转写多个视频:**
```powershell
# AI应动态查找 python 路径
python path/to/run.py --url "URL_1" --url "URL_2" --url "URL_3"
```
*在批量处理时，建议省略 `--output-file` 参数，让技能自动生成报告文件。*
