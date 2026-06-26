---
name: douyin-video-analyzer
description: 深度拆解抖音视频，自动生成包含数据、结构、视觉、文案的完整分析报告。
version: 3.7.4
metadata:
  {
    "openclaw":
      {
        "requires":
          { "bins": ["ffmpeg", "yt-dlp", "node"], "env": ["ZHIPU_API_KEY"] },
        "install":
          [
            {
              "id": "playwright-deps",
              "label": "安装 Playwright 依赖",
              "kind": "exec",
              "command": "npx playwright install --with-deps chromium",
            },
          ],
      },
  }
---

# 抖音视频深度拆解分析器 (Pro版)

> ⚠️ **重要提示：数据流向与隐私说明**
> 本技能执行本地媒体处理（FFmpeg/yt-dlp），并会将视频的关键帧与音频片段（分段）上传至 **智谱 AI (open.bigmodel.cn)** 的 API 接口进行识别与分析。

## 核心特性

- ✅ **旗舰级视觉分析**: 使用 `GLM-4.6V` 对 20 帧/段进行分段视觉采样。
- ✅ **全量语音转录**: 集成 `GLM-ASR-2512` 对 20 秒/段进行语音分段转录。
- ✅ **高性能后端**: 基于 `Playwright` 与 `yt-dlp` 进行内容抓取。

## 环境要求

1. **二进制工具**: `ffmpeg`, `yt-dlp`, `node` 必须在系统 PATH 中。
2. **凭据**: 需要有效的 `ZHIPU_API_KEY` 环境变量。

## 使用

```bash
# 输入抖音链接执行拆解
node scripts/analyze.js "https://v.douyin.com/xxxxxx/"
```

## 数据安全说明

*   **本地处理**: 视频下载与初步抽帧在您的本地环境完成。
*   **外部传输**: 仅选定的关键帧（Base64 格式）与音频片段会被发送至智谱 AI 服务器。
*   **临时清理**: 每次分析结束后，系统会自动删除 `temp/` 目录下的所有临时媒体文件。

## 作者

Leo & Neo (Startup Partners)
