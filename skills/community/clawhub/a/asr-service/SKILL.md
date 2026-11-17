---
name: asr-service
version: 1.1.0
description: "SenseVoice-Small ASR — 中文语音识别 + 说话人分离 + SRT/VTT 字幕，IFF 托管部署"
metadata: { "openclaw": { "emoji": "🎤", "requires": { "bins": ["python3"] } } }
tags: ["asr", "speech-to-text", "sensevoice", "transcription", "audio"]
---

# ASR Service — SenseVoice-Small

中文语音识别技能，基于 IFF 托管的 FunASR SenseVoice-Small 模型。

## 架构

```
消费者 (Nova/CLI/其他 Skill)
  → ASRSkill (transcribe / serve_status)
    → IFFManager → iff switch sensevoice-small
    → httpx → http://localhost:8881/v1/audio/transcriptions (model="sensevoice")
    → Postprocessor → 返回 TranscriptionResult
```

### 职责边界

| 层 | 职责 |
|---|---|
| **IFF** | 进程生命周期、GPU 调度、健康检查 |
| **ASR Skill** | IFF 启停管理、API 调用、响应后处理 |

## 依赖

- IFF v4.7.0+ (`asr_server` type + `sensevoice-small`)
- FunASR SenseVoice-Small (Conda `sensevoice`, port 8881)
- httpx, pyyaml

## API

| 方法 | 说明 |
|------|------|
| `skill.transcribe(audio_path, language=None, response_format="json", speaker_labels=False)` | 语音转文字 |
| `skill.transcribe_srt(audio_path, language=None, speaker_labels=False)` | 转写并返回 SRT 字幕 |
| `skill.transcribe_vtt(audio_path, language=None, speaker_labels=False)` | 转写并返回 VTT 字幕 |
| `skill.serve_status()` | ASR 服务状态 |

### transcribe 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `audio_path` | (必填) | 音频文件路径 (mp3, wav, m4a 等) |
| `language` | None (自动检测) | 语言代码: zh, en, ja, ko, yue |
| `response_format` | "json" | json / text / verbose_json |
| `speaker_labels` | False | 说话人分离，segments 中包含 speaker 字段 |

### TranscriptionResult

| 字段 | 类型 | 说明 |
|------|------|------|
| `text` | str | 转写文本 |
| `language` | str \| None | 检测到的语言 |
| `duration` | float \| None | 音频时长 (秒) |
| `segments` | list \| None | 分段时间戳 (verbose_json) |

## CLI

```bash
# 基本转写
{baseDir}/scripts/asr_cli.py transcribe audio.mp3

# 指定语言
{baseDir}/scripts/asr_cli.py transcribe audio.wav --language zh

# 详细输出（含时间戳、语言、时长）
{baseDir}/scripts/asr_cli.py transcribe audio.mp3 --format verbose_json

# 带说话人分离
{baseDir}/scripts/asr_cli.py transcribe audio.mp3 --speakers

# SRT 字幕输出
{baseDir}/scripts/asr_cli.py srt audio.mp3

# VTT 字幕输出（带说话人标签）
{baseDir}/scripts/asr_cli.py vtt audio.mp3 --speakers

# 服务状态
{baseDir}/scripts/asr_cli.py serve-status
```

## 约束

- 所有请求必须显式传 `model="sensevoice"`，不依赖 API 默认值
- 不使用 `/asr` 端点（会无条件触发 vLLM 引擎加载）
- SenseVoice token 清洗（`<|zh|><|HAPPY|>` 等）由 funasr-server 端完成，Skill 不需重复处理

## 配置

`config.yaml`:

```yaml
service:
  name: sensevoice-small
  base_url: http://localhost:8881
  health_timeout: 120
  switch_timeout: 120

retry:
  max_attempts: 3

defaults:
  model: sensevoice
  language: null
  response_format: json
```
