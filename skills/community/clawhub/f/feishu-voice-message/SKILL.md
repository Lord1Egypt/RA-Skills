---
name: feishu-voice-message
description: |
  Generate Feishu voice messages (with waveform) from text. Auto-converts to OPUS format for in-chat playback on both mobile and desktop.
  
  从文本生成飞书语音消息（带波形图）。自动转换为 OPUS 格式，手机和电脑端都能在聊天中直接播放。
  
  **Triggers / 触发词**: 语音消息、配音、TTS、voice message、text to speech、发送语音
---

# Feishu Voice Message / 飞书语音消息

Generate Feishu voice messages that play directly in chat (with waveform display) on both mobile and desktop.

生成飞书语音消息，手机和电脑端都能在聊天中直接播放（带波形图显示）。

## Key Discovery / 核心发现

**Feishu voice messages require OPUS format, not MP3!**

**飞书语音消息需要 OPUS 格式，不是 MP3！**

| Format 格式 | Display 显示 | Desktop 电脑端 |
|-------------|-------------|----------------|
| `.opus` | Voice message (waveform) 语音消息（波形图） | ✅ Click to play 点击播放 |
| `.mp3` | Regular file 普通文件 | Need download 需下载播放 |

## Voice Presets / 音色预设

### Adult Voices / 成人音色

| Preset 预设 | Voice 音色 | Pitch 音调 | Rate 语速 | Use Case 适用场景 |
|-------------|-----------|------------|-----------|-------------------|
| `manbo` | XiaoyiNeural | +50Hz | default | Lively, energetic 活泼有活力 |
| `xiaoyi` | XiaoyiNeural | default | +30% | Fast-paced, news 快节奏 |
| `xiaoxiao` | XiaoxiaoNeural | default | default | Natural, general 自然通用 |
| `yunyang` | YunyangNeural | default | +10% | Narration, documentary 旁白纪录片 |

### Kids Voices / 儿童音色

| Preset 预设 | Voice 音色 | Pitch 音调 | Rate 语速 | Use Case 适用场景 |
|-------------|-----------|------------|-----------|-------------------|
| `xiaotangdou` | XiaoyiNeural | +15% | -5% | Lively, animation, stories 活泼童趣 |
| `mianhuatang` | XiaoxiaoNeural | +5% | -10% | Gentle, bedtime stories 温柔故事 |
| `xiaomengmeng` | XiaoxiaoNeural | +10% | -5% | Friendly, educational 亲切教育 |

## Usage / 使用方法

### Command Line / 命令行

```bash
# Basic usage / 基本用法
python scripts/feishu_voice.py "Your text here" --preset manbo

# Kids voice / 儿童音色
python scripts/feishu_voice.py "儿童故事内容" --preset xiaotangdou
```

### Via Agent / 通过代理

```
# Just ask the agent to generate voice message
# 直接让代理生成语音消息

User: 帮我生成一个语音消息："你好，欢迎使用飞书！" 用小糖豆音色
Agent: [Generates and sends .opus file]
```

## Requirements / 系统要求

1. **Edge TTS** - Node.js package for text-to-speech
   ```bash
   npm install edge-tts
   ```

2. **FFmpeg** - For MP3 to OPUS conversion
   ```bash
   # Windows: Download from https://ffmpeg.org
   # Mac: brew install ffmpeg
   # Linux: sudo apt install ffmpeg
   ```

## Technical Details / 技术细节

### Workflow / 工作流程

1. **TTS Generation** → Generate MP3 using Edge TTS
2. **Format Conversion** → Convert MP3 to OPUS using FFmpeg
3. **Send to Feishu** → Upload as voice message

```
Text → Edge TTS → MP3 → FFmpeg → OPUS → Feishu Voice Message
```

### FFmpeg Conversion Command / 转换命令

```bash
ffmpeg -i input.mp3 -c:a libopus -b:a 64k output.opus
```

### MIME Types / MIME 类型

When sending to Feishu, use correct MIME type:

```javascript
// Voice message (clickable on desktop)
message({ action: "send", path: "audio.opus", mimeType: "audio/opus" })

// Regular file (download required on desktop)
message({ action: "send", path: "audio.mp3", mimeType: "audio/mpeg" })
```

## Limitations / 限制

- Maximum file size: 30MB / 最大文件大小：30MB
- OPUS is the only format for voice messages / OPUS 是语音消息的唯一格式
- Requires FFmpeg for conversion / 需要安装 FFmpeg 进行转换

## References / 参考资料

- [Feishu File Upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Edge TTS](https://github.com/rany2/edge-tts)
- [FFmpeg OPUS Encoding](https://trac.ffmpeg.org/wiki/Encode/Opus)

---

**Created by / 创建者**: systiger  
**Version / 版本**: 1.0.0  
**ClawHub**: https://clawhub.ai/systiger/feishu-voice-message
