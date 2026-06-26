---
name: audio-toolkit
version: 1.0.0
description: 音频处理工具 - 格式转换、剪辑、压缩、提取音频。适合：播客、音乐制作、视频剪辑。
license: MIT
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: ["ffmpeg"]
---

# 音频处理工具 Skill

强大的音频处理能力。

## 核心功能

### 1. 格式转换
- MP3 ↔ WAV ↔ FLAC ↔ AAC
- 批量转换
- 质量调整

### 2. 音频剪辑
- 裁剪音频片段
- 合并音频
- 调整音量

### 3. 音频提取
- 从视频提取音频
- 提取背景音乐
- 降噪处理

## 使用方法

### 格式转换

```
将 audio.wav 转换为 MP3 格式
```

### 裁剪音频

```
裁剪 audio.mp3 从 1:00 到 3:00
```

### 提取音频

```
从 video.mp4 提取音频
```

### 合并音频

```
合并 track1.mp3 和 track2.mp3
```

## 技术依赖

- FFmpeg

---

创建：2026-03-11
作者：ClawMart