---
name: audio-transcriber
description: >
  音频转录技能 — 使用 OpenAI Whisper 将音频转录为文本，支持实时录音转写、情感分析和多语言翻译。
  Trigger: 当用户需要录音转写、实时翻译、语音转录、会议记录、或音频分析时。
core: hear
metadata:
  author: system
  version: "2.0"
tags: [transcription, whisper, speech-to-text, translation, emotion, 转录, 翻译, 音频, hear]
---

## 何时使用

满足以下条件时加载此技能：
- 需要将录音或实时音频转录为文本
- 需要从语音中检测情绪（高兴/悲伤/愤怒/恐惧/惊讶/厌恶）
- 需要进行多语言翻译（通过 --target-lang 指定目标语言）
- 需要分析音频信号特征（能量、过零率、频谱质心）

## 子命令

### 1. hear_enhanced — 增强听力（转录 + 情绪 + 翻译）

```bash
cd D:\coze-local\db
python audio.py hear_enhanced [选项]
```

**参数：**
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--duration` | 15 | 录音时长 (秒) |
| `--device` | 0 | 音频输入设备ID |
| `--model` | tiny | Whisper 模型大小 |
| `--target-lang` | en | 目标翻译语言 (en/zh/ja/ko/fr/de/es/ru) |

**输出示例：**
```
[Enhanced Hear] Transcript: 今天天气真好
[Enhanced Hear] Emotion detected: happy
[Enhanced Hear] Translated: The weather is really nice today
```

### 2. transcribe — 录音转录

```bash
python audio.py transcribe --duration 10 --model base --output result.wav
```

### 3. analyze — 音频信号分析

```bash
python audio.py analyze --duration 5
# 输出: 能量(RMS)、过零率、频谱质心、信号时长
```

### 4. capture — 音频降噪处理

```bash
python audio.py capture --duration 15
# 输出: 原始WAV + 降噪后WAV (_clean.wav)
```

## 核心实现

### 无ffmpeg转录（直接numpy数组）

```python
import numpy as np
import whisper

def transcribe_from_bytes(audio_bytes: bytes, model_size: str = "tiny") -> str:
    """直接从音频字节转写，无需ffmpeg"""
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_np)
    return result["text"].strip()

def transcribe_from_file(audio_path: str, model_size: str = "base") -> str:
    """从文件转写（支持mp3/wav/m4a）"""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"].strip()
```

### 情绪检测（基于词典）

```python
def detect_emotion(text: str) -> str:
    """基于关键词的情绪检测"""
    emotion_words = {
        'happy': ['高兴','开心','快乐','愉快','喜悦','兴奋','欢喜'],
        'sad': ['悲伤','难过','痛苦','忧郁','沮丧','失落','眼泪'],
        'angry': ['愤怒','生气','恼火','愤慨'],
        'fear': ['恐惧','害怕','担心','焦虑','紧张','惊慌'],
        'surprise': ['惊讶','意外','震惊','吃惊','诧异'],
        'disgust': ['厌恶','反感','憎恶','恶心','嫌弃']
    }
    text_lower = text.lower()
    for emotion, words in emotion_words.items():
        if any(w in text_lower for w in words):
            return emotion
    return 'neutral'
```

## 相关文件

- `D:\coze-local\db\audio.py` — 核心实现：`transcribe_audio()`, `cmd_hear_enhanced()`, `cmd_transcribe()`, `cmd_analyze()`, `cmd_capture()`
- `D:\coze-local\db\AudioProcessor` — 守护进程集成（`process_continuous()`, `get_last_command()`）
- `D:\coze-local\external\clawhub_skills\wake-word-detector\SKILL.md` — 唤醒词检测技能
- `D:\coze-local\external\clawhub_skills\audio-device-diagnostic\SKILL.md` — 音频设备诊断
- `D:\coze-local\external\clawhub_skills\core-daemon-launcher\SKILL.md` — 守护进程启动

## 依赖

```bash
pip install openai-whisper pyaudio numpy
```
