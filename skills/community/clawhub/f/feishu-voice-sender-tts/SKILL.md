---
name: feishu-voice-sender-tts
description: |
  飞书语音发送器 | Feishu Voice Sender
  
  支持 TTS 语音合成，以及可选的 ASR 语音识别功能。
  
  当用户明确要求发送飞书语音消息时调用此工具，例如：发语音、用语音回复、发送语音消息等。
  
  This skill may be invoked only when the user explicitly requests a voice message via Feishu/Lark. It does not run automatically.

metadata:
  openclaw:
    primaryEnv: FEISHU_APP_SECRET
    requires:
      env:
        - TTS_APP_ID
        - TTS_ACCESS_KEY
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
      bins:
        - ffmpeg
    env:
      - name: TTS_APP_ID
        description: "Volcengine TTS app ID"
        required: true
        sensitive: false
      - name: TTS_ACCESS_KEY
        description: "Volcengine TTS access key"
        required: true
        sensitive: true
      - name: FEISHU_APP_ID
        description: "Feishu app ID"
        required: true
        sensitive: false
      - name: FEISHU_APP_SECRET
        description: "Feishu app secret"
        required: true
        sensitive: true
      - name: ASR_APP_ID
        description: "Volcengine ASR app ID (optional, only needed for speech recognition)"
        required: false
        sensitive: false
      - name: ASR_ACCESS_KEY
        description: "Volcengine ASR access key (optional, only needed for speech recognition)"
        required: false
        sensitive: true
      - name: DEFAULT_RECEIVE_ID
        description: "Default Feishu open_id for the recipient"
        required: false
        sensitive: false
      - name: ASR_RESOURCE_ID
        description: "Volcengine ASR resource ID for local-file recognition (optional, defaults to the flash/local-file ASR resource)"
        required: false
        sensitive: false
---

# 飞书语音发送器 Feishu Voice Sender

支持 TTS 语音合成，以及可选的 ASR 语音识别功能，同时支持基于上下文的情绪参数。

## ⚠️ 重要声明

### 执行模式 | Execution Model

- **此 Skill 不会自动运行，仅在用户明确要求时执行**
- **This skill does not monitor, intercept, or automatically process messages. It only runs when explicitly invoked.**
- **仅处理用户提供的输入，不读取任意本地文件**
- **Only processes user-provided input. Does not read arbitrary local files.**

### 外部依赖 | External Dependencies

- **ffmpeg**: 仅用于音频格式转换（mp3 → opus），不执行任意命令
- **ffmpeg is used ONLY for audio format conversion (mp3 → opus). No arbitrary command execution. No user-controlled shell input.**

## 触发场景 | Invocation Examples

当用户明确要求发送飞书语音消息时，可调用此 Skill，例如：
- "发语音给..."
- "用语音回复"
- "发送语音消息"
- "voice message"
- "send voice"

This skill may be invoked only when the user explicitly requests a voice message via Feishu/Lark. It does not run automatically.

## AI 使用方法

当用户明确要求时，使用以下方式发送语音：

```python
import sys
sys.path.insert(0, 'src')
from feishu_voice import send_voice_message

# 发送语音消息
send_voice_message(
    text="要播报的内容",
    user_input="用户的原始请求（用于情绪感知）"
)
```

**参数说明：**
- `text`: AI 生成的播报内容（必填，最大 300 字符）
- `user_input`: 用户的原始输入，用于让豆包感知情绪（可选）
- `receive_id`: 接收者 ID（可选，默认从环境变量读取）

**示例：**
```python
# 用户说："用激动的语气发语音说项目成功了"
send_voice_message(
    text="项目成功了！我们超额完成了目标！",
    user_input="用激动的语气发语音说项目成功了"
)
```

## 数据流 | Data Flow

**Text path:**
用户提供文本 → 情绪上下文参数 → TTS 语音合成 → 格式转换 → 飞书发送

**ASR path:**
用户明确提供本地音频文件（当前支持 `.ogg` / OGG Opus 输入）→ 极速版 ASR（flash recognize API）→ 返回文本结果

## 环境变量配置

### 必需配置（TTS + Feishu）

```bash
export TTS_APP_ID="your-tts-app-id"
export TTS_ACCESS_KEY="your-tts-access-key"
export FEISHU_APP_ID="your-feishu-app-id"
export FEISHU_APP_SECRET="your-feishu-app-secret"
```

### 可选配置

```bash
# ASR 语音识别（仅在需要使用 ASR 功能时配置）
export ASR_APP_ID="your-asr-app-id"
export ASR_ACCESS_KEY="your-asr-access-key"
export ASR_RESOURCE_ID="volc.bigasr.auc_turbo"

# 默认接收者
export DEFAULT_RECEIVE_ID="ou_xxx"
```

**注意：** ASR 是可选功能，仅在调用语音识别时需要配置 ASR_APP_ID 和 ASR_ACCESS_KEY。若未显式提供 `ASR_RESOURCE_ID`，代码默认按本地文件极速识别场景使用 `volc.bigasr.auc_turbo`。

**获取方式：**
- 豆包语音：火山引擎控制台 https://console.volcengine.com/
- 飞书：飞书开放平台 https://open.feishu.cn/

## 功能特性

- 🎙️ **语音合成(TTS)** - 使用豆包 TTS 2.0 生成语音
- 🎯 **语音识别(ASR)** - 使用豆包极速版 flash recognize API 识别本地 OGG/Opus 音频
- 🎭 **情绪参数** - 支持通过 `context_texts` 传递情绪上下文
- 🔒 **安全限制** - 仅处理用户提供的输入

## 安全说明 | Security

### 输入限制
- 仅接受用户直接提供的文本输入
- ASR 当前仅处理用户明确提供的 `.ogg` 音频文件（飞书语音常见为 OGG/Opus）
- 文本长度限制 300 字符
- 不读取任意本地文件，仅处理用户明确提供的 .ogg 音频文件用于 ASR

### 音频输入限制 | Audio Input Constraints
- **仅处理用户明确提供的音频文件**
- **Only processes audio files explicitly provided by the user**
- **不访问系统音频、麦克风或消息历史**
- **Does NOT access system audio, microphone, or message history**
- **不扫描本地目录**
- **Does NOT scan local directories**

### 执行限制
- 不监听消息
- 不自动运行
- 不扫描目录
- 不执行用户控制的命令

### 临时文件
- 使用 `tempfile` 模块创建临时文件
- 处理完成后立即删除
- 不保留任何持久文件

## 依赖

```
requests>=2.28.0
```

系统依赖：
- ffmpeg（用于音频格式转换 mp3 → opus）
- Python 3.8+

## 安装

```bash
pip install -r requirements.txt
```

**注意：** 需要系统安装 ffmpeg
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`

## 项目结构

```
feishu-voice-sender-tts/
├── SKILL.md
├── requirements.txt
└── src/
    └── feishu_voice.py
```

## 更新日志

### V2.0.2 (2026-03-24)
- 🎯 修正本地音频 ASR 调用方式，改为 flash recognize API 所需的 JSON + base64 请求体
- 🔧 新增 `ASR_RESOURCE_ID` 环境变量支持，默认适配本地文件极速识别场景
- 🗣️ 明确桌面清洁版支持本地 OGG/Opus 音频识别
- 📝 同步 SKILL.md 描述与实际实现，避免文档与代码不一致

### V2.0.0 (2026-03-23)
- 🔒 安全重构：移除所有硬编码密钥，改为环境变量
- 🗑️ 删除 shell 脚本（send.sh / install.sh）
- 🐍 纯 Python 实现：使用 requests 替代 curl
- 🛡️ 增加安全限制：输入验证、文件类型检查、长度限制
- 📝 重写 SKILL.md：明确声明执行模式和安全边界
- 🧹 使用 tempfile 替代固定路径
- 🔑 ASR/TTS 密钥分离
- 💾 Feishu token 缓存
- ⏱️ 动态音频时长计算
- 🔒 ffmpeg 安全声明
- 📝 文档降调，减少营销感
