---
name: feishu-voice-chat
description: |
  飞书语音对话能力，提供语音识别（ASR）和语音合成（TTS）功能， 所有的飞书语音消息都通过该技能处理。
  完整语音交互链路：接收用户语音 → ASR 转文字 → LLM 处理 → TTS 转语音 → 通过飞书插件发送语音消息。
  当用户要求"语音回复/说给我听"时，只回复飞书语音消息（audio 气泡），不回复文本、不回复文件、只回复语音消息。
usage:
  - asr: python scripts/volc_voice.py asr <audio_path>
  - tts: python scripts/feishu_voice.py speak <text> [output_path] [reply_to_message_id]
parameters:
  asr:
    audio_path:
      type: string
      description: 待识别的音频文件绝对路径（支持 ogg、opus、mp3、wav）
      required: true
  tts:
    text:
      type: string
      description: 需要转换为语音的文本内容
      required: true
    output_path:
      type: string
      description: 生成的音频文件保存路径（可选，默认 /tmp/openclaw/voice-tts/reply_{timestamp}.ogg）
      required: false
    reply_to:
      type: string
      description: 回复目标消息 ID（可选，用于在话题中回复）
      required: false
dependencies:
  - requests
  - python-dotenv
env:
  - name: VOLC_APPID
    description: "火山引擎应用 ID"
    required: true
  - name: VOLC_ACCESS_TOKEN
    description: "火山引擎访问令牌"
    required: true
  - name: VOLC_RESOURCE_ID
    description: "TTS 资源 ID (默认: seed-tts-1.0)"
    required: false
  - name: VOLC_VOICE_TYPE
    description: "TTS 音色代码"
    required: false
  - name: VOLC_RESOURCE_ID_ASR
    description: "ASR 资源 ID"
    required: false
---

# 飞书语音对话 (Feishu Voice Chat)

本 Skill 集成了火山引擎 (Volcengine) 的语音技术，赋予 OpenClaw 机器人"听"和"说"的能力。

## 完整语音交互链路

```
用户（手机飞书 App）
    │
    ▼ 发送语音消息
┌──────────────────────────────────────────────────────────────┐
│ 飞书服务器                                                    │
│  • 语音格式：OGG 容器 + Opus 编码 + 48kHz 采样               │
│  • 消息类型：msg_type="audio"                               │
│  • content: {"file_key": "file_xxx", "duration": 5000}      │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ OpenClaw 接收事件
┌──────────────────────────────────────────────────────────────┐
│ openclaw-lark 插件                                           │
│  • convertAudio() 解析 file_key                              │
│  • 下载语音到本地临时文件（/tmp/openclaw/media/inbound/*.ogg）│
│  • AI 收到：<audio key="file_xxx" duration="5s"/> + 文件路径  │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ 调用 ASR
┌──────────────────────────────────────────────────────────────┐
│ feishu-voice-chat / ASR（语音→文字）                          │
│  • volc_voice.py asr <本地音频路径>                           │
│  • 火山引擎大模型 ASR (V3)，高精度识别                       │
│  • 返回 JSON: {"status": "success", "text": "识别出的文字"}   │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ LLM 处理
┌──────────────────────────────────────────────────────────────┐
│ OpenClaw LLM                                                 │
│  • 理解用户意图，生成回复内容                                  │
│  • 若需要语音回复 → 进入 TTS 流程                              │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ 调用 TTS
┌──────────────────────────────────────────────────────────────┐
│ feishu-voice-chat / TTS（文字→语音）                          │
│  • feishu_voice.py speak <回复文本> [output_path] [reply_to]  │
│  • 火山引擎大模型 TTS (V3)，生成 .ogg 音频文件                │
│  • 自动返回 message 工具调用指令                              │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ 调用 message 工具发送
┌──────────────────────────────────────────────────────────────┐
│ openclaw-lark 插件 / message 工具                             │
│  • message(action="send", channel="feishu",                  │
│  •           msg_type="audio", media="<audio_file_path>")    │
│  • 内部自动：uploadFileLark(file_type="opus") → 获得 file_key │
│  •          sendAudioLark(content={"file_key": "file_xxx"})  │
│  • 用户收到：语音气泡（audio 消息，可直接播放）                 │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
用户（手机飞书 App）
```

## 功能特性

*   **高精度语音识别 (ASR)**: 使用火山引擎大模型 ASR (V3)，支持长语音和流式识别，准确率高。
*   **自然语音合成 (TTS)**: 使用火山引擎 TTS (V3)，输出 .ogg 格式（适配飞书语音消息），支持流式生成。
*   **飞书插件深度集成**: 通过 openclaw-lark 的 `message` 工具自动上传并发送语音消息，用户收到的是可直接播放的语音气泡。

## 前置准备

1.  **注册火山引擎账号**: 访问 [火山引擎语音服务控制台](https://console.volcengine.com/speech/app)。
2.  **创建应用**: 在控制台创建一个应用，获取 `AppID` 和 `Access Token`（**注意**：这是语音服务的凭证，不同于火山引擎 ARK API 的 Key）。
3.  **开通服务**: 为应用开通「**大模型语音合成 TTS**」和「**大模型录音文件识别 ASR**」两个服务。
4.  **安装依赖**: `pip install -r requirements.txt`

## 配置说明

1.  复制 `.env.example` 为 `.env`：
    ```bash
    cp .env.example .env
    ```
2.  编辑 `.env`，填入你的火山引擎凭证：
    ```bash
    VOLC_APPID=你的AppID
    VOLC_ACCESS_TOKEN=你的Access Token
    ```

| 变量名 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `VOLC_APPID` | 火山引擎应用 ID（必填） | - |
| `VOLC_ACCESS_TOKEN` | 访问令牌（必填） | - |
| `VOLC_RESOURCE_ID` | TTS 资源 ID | `seed-tts-1.0` |
| `VOLC_VOICE_TYPE` | TTS 音色代码 | `zh_female_sajiaonvyou_moon_bigtts` |
| `VOLC_RESOURCE_ID_ASR` | ASR 资源 ID | `volc.bigasr.auc` |

## 使用指南

### 1. 语音识别（ASR）—— 语音 → 文字

当机器人收到用户语音消息时，使用此命令将音频转为文本。

```bash
python3 scripts/volc_voice.py asr /path/to/user_audio.ogg
```

**输出示例 (JSON)**:
```json
{"status": "success", "text": "你好，请问今天天气怎么样？"}
```

### 2. 语音合成（TTS）—— 文字 → 语音

当需要回复语音时，使用此命令将文本转为音频，并自动生成 message 工具调用指令。

```bash
# 基本用法
python3 scripts/feishu_voice.py speak "今天天气不错，适合出去玩哦。"

# 指定输出路径和回复目标（在话题中回复）
python3 scripts/feishu_voice.py speak "好的没问题！" /tmp/reply.ogg om_xxx
```

**输出示例**:
```
🔊 正在合成语音: 今天天气不错...
✅ 合成成功: /tmp/openclaw/voice-tts/reply_1234567890.ogg
{"status": "success", "audio_file": "/tmp/openclaw/voice-tts/reply_1234567890.ogg", "message_cmd": "message(action=\"send\", channel=\"feishu\", msg_type=\"audio\", media=\"/tmp/openclaw/voice-tts/reply_1234567890.ogg\")"}

============================================================
音频文件 / Audio file: /tmp/openclaw/voice-tts/reply_1234567890.ogg
发送指令 / Send command: message(action="send", channel="feishu", msg_type="audio", media="/tmp/openclaw/voice-tts/reply_1234567890.ogg")
============================================================
```

## OpenClaw Agent 接入指南

### 在 Agent System Prompt 中添加以下指令

> **语音交互能力**:
> *   当用户发送语音消息（你会收到一个文件路径或 `<audio key="..."/>` 占位符）时，请调用 `feishu-voice-chat` 的 ASR 功能识别内容。
> *   当用户要求"语音回复/说给我听"时，请先生成文本回复，然后调用 `feishu-voice-chat` 的 TTS 功能生成 .ogg 音频文件，最后使用飞书插件的 `message` 工具将音频以 `msg_type="audio"` 发送给用户。
> *   **重要**：语音回复只发送语音消息，不发送文本消息，不发送文件附件。用户收到的是可直接播放的语音气泡。

### 工具调用示例（供 Agent 参考）

**接收用户语音**:
```
# 用户发送语音 → AI 调用 ASR
python3 scripts/volc_voice.py asr /tmp/openclaw/media/inbound/voice_xxx.ogg
# → 返回: {"status": "success", "text": "你好"}

# AI 处理后决定语音回复 → 调用 TTS
python3 scripts/feishu_voice.py speak "你好，有什么可以帮助你的吗？"
# → 返回 JSON 含 audio_file 和 message_cmd

# AI 调用 message 工具发送语音
message(action="send", channel="feishu", msg_type="audio", media="/tmp/openclaw/voice-tts/reply_xxx.ogg")
# → 用户在飞书收到语音气泡
```

## 测试步骤

1.  **配置凭证后，运行 TTS 测试**:
    ```bash
    cd /Users/bytedance/.openclaw/workspace/skills/feishu-voice-chat
    python3 scripts/feishu_voice.py speak "你好，这是飞书语音对话测试。"
    ```
    *验证*: 终端输出 `✅ 合成成功`，且生成 `/tmp/openclaw/voice-tts/reply_*.ogg` 文件。

2.  **运行 ASR 测试**:
    ```bash
    python3 scripts/volc_voice.py asr /tmp/openclaw/voice-tts/reply_*.ogg
    ```
    *验证*: 终端输出 `{"status": "success", "text": "..."}`，识别出的文字与 TTS 输入一致。

3.  **完整链路测试**: 在飞书 App 中对机器人发送一条语音，观察 Agent 是否正确识别并语音回复。

## 故障排除

*   **Error: 请在 .env 文件中配置...**: 检查 `.env` 文件是否存在且内容正确。
*   **Requested resource not granted (45000030)**:
    *   检查 `VOLC_RESOURCE_ID` 是否正确。
    *   如果是 TTS，尝试使用 `seed-tts-1.0`。
    *   如果是 ASR，尝试使用 `volc.bigasr.auc`。
    *   确认你的火山引擎应用是否已关联了相应的语音技术服务。
*   **TTS/ASR Timeout**: 检查网络连接，确保能访问 `openspeech.bytedance.com`。
*   **飞书发送失败**: 确认 openclaw-lark 插件已正确安装并配置了飞书机器人。
