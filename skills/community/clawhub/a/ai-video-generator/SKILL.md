---
name: ai-video-generator
description: AI 视频生成技能，支持 Luma Dream Machine、Runway ML、Kling AI 等多个平台。文生视频、图生视频。
author: 牛马 1 号
version: 1.0.0
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["curl","jq"]},"config":{"env":{"LUMA_API_KEY":{"description":"Luma Dream Machine API Key","required":false},"RUNWAY_API_KEY":{"description":"Runway ML API Key","required":false},"KLING_API_KEY":{"description":"Kling AI API Key","required":false}}}}}
---

# AI Video Generator - 文生视频技能

使用 AI 生成视频，支持多个平台：

- **Luma Dream Machine** - 高质量，5 秒/10 秒视频
- **Runway ML** - 专业级，Gen-2/Gen-3
- **Kling AI（可灵）** - 国产，效果优秀

## 命令

### 生成视频（Luma）
```bash
uv run {baseDir}/scripts/generate_video.py --platform luma --prompt "your video description" --filename "output-video.mp4" [--duration 5|10] [--api-key KEY]
```

### 生成视频（Runway）
```bash
uv run {baseDir}/scripts/generate_video.py --platform runway --prompt "your video description" --filename "output-video.mp4" [--api-key KEY]
```

### 生成视频（Kling）
```bash
uv run {baseDir}/scripts/generate_video.py --platform kling --prompt "your video description" --filename "output-video.mp4" [--api-key KEY]
```

### 图生视频
```bash
uv run {baseDir}/scripts/generate_video.py --platform luma --prompt "describe motion" --filename "output-video.mp4" --input-image "path/to/image.png"
```

## API Key 配置

脚本按以下顺序查找 API Key：

1. `--api-key` 参数
2. 环境变量：`LUMA_API_KEY` / `RUNWAY_API_KEY` / `KLING_API_KEY`

## 平台对比

| 平台 | 时长 | 特点 | API 文档 |
|------|------|------|----------|
| Luma | 5s/10s | 质量高，速度快 | https://docs.lumalabs.ai |
| Runway | 4s/8s | 专业级，控制多 | https://docs.runwayml.com |
| Kling | 5s/10s | 国产，中文友好 | https://klingai.com |

## 文件名生成

格式：`yyyy-mm-dd-hh-mm-ss-{platform}-{description}.mp4`

示例：
- `2026-03-17-09-30-00-luma-sunset-beach.mp4`
- `2026-03-17-10-15-00-runway-robot-walk.mp4`

## 工作流

1. **草稿**：先用短 prompt 生成 5 秒视频测试
2. **迭代**：调整 prompt 直到满意
3. **最终**：生成 10 秒高清版本

## 常见错误

- `Error: No API key provided` → 设置环境变量或传递 `--api-key`
- `Error: Quota exceeded` → API 额度用尽，等待重置或换平台
- `Error: Invalid prompt` → prompt 太短或包含敏感词

## 示例

```bash
# Luma 生成 5 秒视频
uv run ~/.openclaw/workspace/skills/ai-video-generator/scripts/generate_video.py \
  --platform luma \
  --prompt "A drone flying over a sunset beach, cinematic lighting" \
  --filename "2026-03-17-09-30-00-luma-sunset-beach.mp4" \
  --duration 5

# Kling 图生视频
uv run ~/.openclaw/workspace/skills/ai-video-generator/scripts/generate_video.py \
  --platform kling \
  --prompt "The person waves and smiles" \
  --filename "2026-03-17-10-00-00-kling-person-wave.mp4" \
  --input-image "person.png"
```
