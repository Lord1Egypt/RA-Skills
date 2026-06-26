# Feishu Voice Send 飞书语音发送

通过 TTS 和 STT 在飞书中发送和接收原生语音消息，无需 ffmpeg。

## 功能

- **发送语音**：将文字转换为音频，作为飞书原生语音气泡发送
- **接收语音**：接收飞书语音消息并转写为文字
- **多语言**：支持中文、英文等
- **自动降级**：优先 MiniMax TTS，配额不足时降级 Edge TTS
- **原生格式**：发送的语音显示为语音气泡（非文件）

## 架构

```
用户语音 → .ogg 接收 → Whisper 语音识别 → 文字理解 → 回复内容
                                                        ↓
用户 ← 飞书语音气泡 ← Ogg/Opus 转换 ← MP3 TTS ← 文字
                                   ↑                ↑
                           PyAV 转换         MiniMax / Edge TTS
```

## TTS 引擎选择

```
发送语音请求
    ↓
检查 MiniMax speech-hd 配额
    ↓
配额 > 0 → MiniMax TTS (speech-2.8-hd)
配额 ≤ 0 → Edge TTS
```

## 依赖

- Python: `av`, `openai-whisper`, `soundfile`
- Node.js: `edge-tts`
- CLI: `mmx`（MiniMax TTS）

## 文件说明

| 文件 | 说明 |
|------|------|
| `send_feishu_voice.py` | 发送语音消息的主脚本 |
| `SKILL.md` | OpenClaw skill 规格说明 |

## 使用方法

```bash
python3 send_feishu_voice.py "你好，这是一条测试消息。"
```

## 限制

- 长音频（>30秒）建议分段
- 飞书 Ogg 格式：Ogg 容器 + Opus 编码 + 16kHz + 单声道