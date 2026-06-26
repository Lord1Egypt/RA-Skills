---
name: douyin-reverse-engineer
description: 从抖音视频反推AI绘画提示词和分镜脚本。当用户提到反推提示词、视频反推、抖音分析、分镜反推、游戏改写、视频转提示词时触发。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python"],"env":["ARK_API_KEY"]},"primaryEnv":"ARK_API_KEY"}}
---

# Douyin Reverse Engineer

从**抖音视频URL**出发，自动完成：下载视频 → 豆包AI分析 → 反推AI绘画提示词 + 分镜脚本 → 游戏风格改写。

## 前置依赖

使用前请先安装以下 skill：

```bash
npx clawhub install doubao-video-analyzer
npx clawhub install video-downloader
```

同时需要配置环境变量：
- `ARK_API_KEY`：火山引擎 ARK API Key（用于豆包视频分析）

系统依赖：
- Python 3.8+
- ffmpeg（video-downloader 需要）
- yt-dlp（video-downloader 需要）

## 用法

```bash
# 完整流程（需要 ARK_API_KEY 环境变量）
python skills/douyin-reverse-engineer/reverse_video.py "抖音URL"

# 分析本地视频
python skills/douyin-reverse-engineer/reverse_video.py --local ./video.mp4

# 仅下载（不分析）
python skills/douyin-reverse-engineer/reverse_video.py "抖音URL" --download-only

# 自定义输出目录
python skills/douyin-reverse-engineer/reverse_video.py "URL" --output ./out

# 跳过游戏向改写
python skills/douyin-reverse-engineer/reverse_video.py "URL" --no-rewrite

# 启用锈湖（Rusty Lake）风格改写（调用 Seed-2.0-lite 大模型逐场景改写）
python skills/douyin-reverse-engineer/reverse_video.py "URL" --rusty-lake
```

## 依赖

- `doubao-video-analyzer` skill（volcenginesdkarkruntime + ARK_API_KEY）
- `video-downloader` skill（yt-dlp + ffmpeg）

> **注意**：首次使用请先运行 `npx clawhub install doubao-video-analyzer` 和 `npx clawhub install video-downloader` 安装依赖 skill。
