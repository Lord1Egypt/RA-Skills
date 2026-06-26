---
name: funasr-asr
description: Local speech recognition using Alibaba DAMO Academy's FunASR. Triggers: (1) user sends voice message requiring transcription, (2) need to transcribe audio/video files, (3) download video from web and transcribe, (4) speech-to-text tasks. Default SenseVoiceSmall model (~500MB), single-process segmented transcription for memory efficiency. Multilingual: Chinese, English, Japanese, Korean, Cantonese.
---

# FunASR 本地语音识别

阿里达摩院开源 ASR，完全本地部署，内存优化版。

## 快速使用

### 命令行

```bash
# 默认 small 模式（SenseVoiceSmall, ~500MB）
python3 scripts/transcribe.py /path/to/audio.wav

# 大模型模式（Paraformer-Large, ~2GB，中文极高精度）
python3 scripts/transcribe.py /path/to/audio.wav --mode large

# 自定义分段时长（默认 600 秒 = 10 分钟）
python3 scripts/transcribe.py /path/to/audio.wav --segment 300

# JSON 输出
python3 scripts/transcribe.py /path/to/audio.wav --format json

# 转录视频文件
python3 scripts/video-transcribe.py --audio /path/to/video.mp4
```

### Node.js 调用

```javascript
const funasr = require('./index.js');

const text = await funasr.transcribe('/path/to/audio.wav', {
  mode: 'small',    // 'small' 或 'large'
  format: 'text'    // 'text' 或 'json'
});
```

## 核心优化（v2.0）

| 优化项 | 旧方案 | 新方案 |
|--------|--------|--------|
| 进程模型 | 每段新进程 | 单进程，模型加载一次 |
| 默认模型 | paraformer (~2GB) | SenseVoiceSmall (~500MB) |
| 内存峰值 | ~2GB × N 次 | ~500MB 常驻 |
| 段间释放 | 进程退出 | gc.collect() |
| 任务锁 | ✅ | ✅ 保留 |

## 模式对比

| 特性 | small (默认) | large |
|------|-------------|-------|
| 模型 | SenseVoiceSmall | Paraformer-Large |
| 内存 | ~500MB | ~2GB |
| 语言 | 中英日韩粤 | 中文 |
| 精度 | 高 | 极高 |
| 速度 | 快 (~0.1 RTF) | 较慢 (~0.3 RTF) |
| 适用场景 | 日常转录 | 专业中文场景 |

## 安装

```bash
# Python 依赖
pip install funasr onnxruntime psutil

# 视频处理（可选）
pip install yt-dlp
apt install ffmpeg

# 首次运行自动下载模型
# small: ~500MB | large: ~2GB
```

## 支持格式

- **音频**: WAV, MP3, FLAC, M4A（自动转 16kHz mono）
- **视频**: MP4, WebM, AVI, MOV

## 故障排查

| 问题 | 解决 |
|------|------|
| 模型下载失败 | `pip install modelscope && modelscope download --model iic/SenseVoiceSmall` |
| 内存不足 (OOM) | 用 `--mode small --segment 300` 减小分段 |
| 音频格式错误 | `ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav` |
| 转录有奇怪标记 | 脚本自动清理 `<|en|>` 等 SenseVoice 标记 |

## 许可证

MIT License
