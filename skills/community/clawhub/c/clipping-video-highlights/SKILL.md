---
name: clipping-video-highlights
description: 长视频（YouTube链接/本地视频）→ N个短高光片段+烧字幕+AI封面。100%免费方案：yt-dlp字幕提取+MiniMax LLM选高光+MiniMax图片生成封面+ffmpeg剪辑。
version: 1.0.0
platforms: [linux]
trigger: 用户提供YouTube视频URL或本地视频路径
---

# 长视频高光剪辑技能（免费方案）

> 零成本复刻Clawvard clipping-video-highlights，不花一分钱。

## 适用场景

- YouTube视频 → 抖音/小红书高光片段
- 播客/讲座/直播回放 → 短高光剪辑
- 本地视频批量剪辑

## 核心流程（4步）

```
Step 1: yt-dlp --write-subs  → 自动提取YouTube字幕（免费）
Step 2: MiniMax LLM          → 从字幕文本选高光时间点（已有配额）
Step 3: MiniMax图片生成      → AI生成封面（已有配额）
Step 4: ffmpeg剪辑+烧字幕    → 输出成品短视频
```

## 使用方法

```bash
python3 clipper.py <YouTube_URL> <输出目录> [片段数量]

# 示例：
python3 clipper.py "https://www.youtube.com/watch?v=xxx" "./output" 5
```

## 依赖

- `ffmpeg` / `ffprobe` — 视频处理
- `yt-dlp` — 字幕提取
- MiniMax API（已有：`sk-cp-qLf6tET6ParE9D35M3O0_5TE`）
- 腾讯COS（已有配置）

## 输出

- `cover.jpg` — AI生成封面
- `clip_01.mp4`, `clip_02.mp4`, ... — 剪辑成品（含烧字幕）
