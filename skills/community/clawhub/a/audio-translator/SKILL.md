---
name: audio-translator
version: 2.1.0
description: 多语种语音翻译技能。支持URL或本地文件输入，自动识别源语言，翻译为目标语言，并生成目标语言的语音文件。支持中文、英文、日文、法文、西班牙文等多种语言互译。
author: winer
tags: [audio, translation, speech, multilingual, whisper, tts, url, download]
tools: [bash, python, curl]
---

# 多语种音频翻译助手

支持 URL 或本地文件输入，自动识别源语言，翻译为目标语言，并生成目标语言的语音文件。

## 触发条件

当用户提出以下请求时激活此技能：
- "翻译语音文件"
- "翻译这个音频"
- "把语音翻译成XX语"
- "下载并翻译音频"
- "translate audio from url"
- "翻译在线音频"

## 参数定义

### input_path（必需）
- **类型**: string
- **描述**: 输入音频文件路径或URL
- **支持类型**:
  - 本地文件: `/Users/winer/Downloads/audio.mp3`
  - URL: `https://example.com/audio.mp3`
- **示例**: 
  - `"/Users/winer/Downloads/录音.mp3"`
  - `"https://example.com/voice.m4a"`

### target_lang（必需）
- **类型**: string
- **描述**: 目标语言代码
- **可选值**: 
  - `en` - 英文
  - `zh` - 中文
  - `ja` - 日文
  - `fr` - 法文
  - `es` - 西班牙文
  - `de` - 德文
  - `ko` - 韩文
  - `ru` - 俄文
  - `it` - 意大利文

### output_path（可选）
- **类型**: string
- **描述**: 输出语音文件路径（默认：自动生成）
- **示例**: `"/Users/winer/Downloads/结果.mp3"`

### source_lang（可选）
- **类型**: string
- **描述**: 源语言代码（默认自动检测）

## 执行流程

### 步骤1: 输入处理
- 检测输入是 URL 还是本地文件
- URL: 使用 curl 下载到临时目录
- 本地文件: 直接使用

### 步骤2: 语音识别（Whisper 自动检测语言）

```python
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_path)
source_language = info.language
```

### 步骤3: 翻译（MyMemory API）

```bash
curl -s "https://api.mymemory.translated.net/get?q=<文本>&langpair=<源>|<目标>"
```

### 步骤4: 目标语言语音合成（edge-tts）

根据目标语言选择对应的 TTS 语音：

| 目标语言 | TTS 语音 |
|---------|---------|
| en | en-US-AriaNeural |
| zh | zh-CN-XiaoxiaoNeural |
| ja | ja-JP-NanamiNeural |
| fr | fr-FR-DeniseNeural |
| es | es-ES-ElviraNeural |
| de | de-DE-KatjaNeural |
| ko | ko-KR-SunHiNeural |
| ru | ru-RU-SvetlanaNeural |
| it | it-IT-ElsaNeural |

## 使用示例

### 示例1: 本地文件翻译
```
翻译 /Users/winer/录音.mp3 到英文
```

### 示例2: URL音频翻译
```
翻译 https://example.com/voice.m4a 到中文
```

### 示例3: 指定输出路径
```
翻译 /Users/winer/audio.mp3 en /Users/winer/result.mp3
```

### 示例4: URL到指定输出
```
翻译 https://example.com/speech.mp3 zh /Users/winer/speech_zh.mp3
```

## 注意事项

- **自动语言检测**: Whisper 会自动检测源语言
- **免费使用**: Whisper(本地)、MyMemory API、edge-tts 均免费
- **网络需求**: 翻译和TTS需要网络连接；URL输入需要网络下载
- **支持的输入格式**: mp3, wav, m4a, aac, ogg, flac, wma
- **Python 版本**: 使用 Python 3.11
