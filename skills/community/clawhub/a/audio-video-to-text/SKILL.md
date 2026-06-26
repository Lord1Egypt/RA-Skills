---
name: audio-video-to-text
description: 音视频转文字技能，使用 Whisper 进行语音识别。支持多种音视频格式，可输出纯文本、SRT/VTT 字幕或 JSON 格式。适用于会议记录、视频字幕生成、采访整理、播客转录等场景。
---

# 音视频转文字

## 概述

本技能使用 OpenAI Whisper 模型将音频/视频文件转换为文字。支持自动语言检测和多种输出格式。

## 何时使用

- 会议录音转文字记录
- 视频内容生成字幕（SRT/VTT）
- 采访/播客内容整理
- 语音备忘录转文本
- 多语言视频翻译准备

## 快速开始

### 1. 安装依赖

```bash
pip install openai-whisper ffmpeg-python
```

确保系统已安装 ffmpeg：
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载
```

### 2. 基本用法

```bash
python scripts/transcribe.py <输入文件> [输出文件] [选项]
```

### 3. 示例

```bash
# 转录 MP4 视频，输出文本
python scripts/transcribe.py meeting.mp4

# 转录音频，输出 SRT 字幕
python scripts/transcribe.py podcast.mp3 podcast.srt --output-format srt

# 指定中文和较小模型（更快）
python scripts/transcribe.py interview.wav --model tiny --language zh

# 输出带时间戳的 JSON
python scripts/transcribe.py video.mp4 result.json --output-format json
```

## 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型大小：tiny, base, small, medium, large | base |
| `--language` | 语言代码：zh, en, ja 等 | 自动检测 |
| `--output-format` | 输出格式：txt, srt, vtt, json | txt |
| `--device` | 运行设备：cpu, cuda | cpu |
| `--keep-audio` | 保留临时音频文件 | false |

## 模型选择指南

| 模型 | 大小 | 速度 | 精度 | 适用场景 |
|------|------|------|------|----------|
| tiny | 39M | 最快 | 一般 | 快速测试、短音频 |
| base | 74M | 快 | 良好 | 日常使用 |
| small | 244M | 中等 | 较好 | 正式场合 |
| medium | 769M | 慢 | 很好 | 高精度需求 |
| large | 1550M | 最慢 | 最佳 | 专业转录 |

## 输出格式说明

### TXT（纯文本）
```
这是转录的完整文本内容，适合阅读和编辑。
```

### SRT（字幕格式）
```
1
00:00:01,000 --> 00:00:04,000
这是第一句字幕。

2
00:00:04,500 --> 00:00:07,000
这是第二句字幕。
```

### VTT（Web 字幕）
```
WEBVTT

00:00:01.000 --> 00:00:04.000
这是第一句字幕。

00:00:04.500 --> 00:00:07.000
这是第二句字幕。
```

### JSON（完整数据）
包含分段、时间戳、置信度等完整信息，适合程序处理。

## 支持的文件格式

**音频：** MP3, WAV, FLAC, OGG, M4A, AAC

**视频：** MP4, AVI, MOV, MKV, WEBM, FLV

## 性能优化建议

1. **短音频优先用 tiny/base 模型** - 速度快，精度够用
2. **长内容用 CPU** - 避免 GPU 内存不足
3. **指定语言** - 可提升准确率和速度
4. **批量处理** - 脚本可循环调用处理多个文件

## 常见问题

### 转录质量不佳
- 尝试更大的模型（small/medium/large）
- 指定正确的语言代码
- 确保音频质量清晰

### 处理速度慢
- 使用更小的模型（tiny/base）
- 如有 GPU，使用 `--device cuda`
- 缩短音频长度或分段处理

### 内存不足
- 使用更小的模型
- 将长文件分割后分别处理
- 关闭其他占用内存的程序

## 脚本

- `scripts/transcribe.py` - 主转录脚本

## 参考资料

- [OpenAI Whisper 文档](https://github.com/openai/whisper)
- [ffmpeg 文档](https://ffmpeg.org/documentation.html)
- [ISO 639-1 语言代码](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
