# Feishu Voice Clone TTS Skill

一个 OpenClaw skill，使用火山引擎 TTS 将文本转换为语音，并发送到飞书。

支持两种方式：
1. 使用火山引擎预置的声音
2. 使用你自己克隆的声音

## 功能特性

- 支持单聊和群聊
- 使用火山引擎 TTS（支持预置声音和音色克隆）
- 自动将音频转换为飞书支持的 Opus 格式

## 火山引擎配置

### 方式一：使用预置声音（无需克隆）

直接在火山引擎控制台选择预置的声音：

https://console.volcengine.com/speech/new/experience/tts?projectName=default

- 获取火山引擎 API Key
- 选择一个预置的声音，获取音色 ID

### 方式二：使用你自己克隆的声音

#### 1. 声音克隆

首先，在火山引擎上克隆你想要的声音：

https://console.volcengine.com/speech/new/experience/clone?projectName=default

- 上传一段 5-30 秒的清晰音频样本
- 等待声音克隆完成
- 获取你的音色 ID

#### 2. 语音合成

然后，使用语音合成 API 调用你克隆的声音：

https://console.volcengine.com/speech/new/experience/tts?projectName=default

- 获取火山引擎 API Key
- 使用你克隆的音色 ID 进行语音合成

## 前置要求

- 飞书机器人应用（App ID, App Secret）
- 火山引擎 API Key 和音色 ID（预置声音或克隆声音均可）
- OpenClaw 环境
- ffmpeg 和 ffprobe

## 安装

### 1. 作为 OpenClaw Skill 安装

将此目录复制到 OpenClaw 的 skills 目录：

```bash
cp -r feishu-voice-clone-tts ~/.openclaw/skills/
```

### 2. 配置环境变量

```bash
export FEISHU_APP_ID="你的飞书AppID"
export FEISHU_APP_SECRET="你的飞书AppSecret"
export FEISHU_CHAT_ID="user:你的用户OpenID"  # 或 chat:群聊ID
export VOLC_API_KEY="你的火山引擎APIKey"
export VOLC_VOICE_TYPE="你的音色ID"  # 预置声音或克隆声音均可
```

### 3. 或使用配置文件

创建 `~/.volcengine_key`：

```json
{
  "api_key": "你的火山引擎APIKey"
}
```

## 使用方法

### 命令行使用

```bash
# 发送到默认聊天
python feishu_tts.py "你好，这是一条语音消息"

# 发送到指定群聊
python feishu_tts.py -c "chat:oc_xxxxx" "群聊消息"

# 发送到指定单聊
python feishu_tts.py -c "user:ou_xxxxx" "单聊消息"
```

### 聊天 ID 格式

| 格式 | 类型 |
|-----|------|
| `user:ou_xxxxx` | 单聊（Open ID） |
| `chat:oc_xxxxx` | 群聊（Chat ID） |

## 作为 OpenClaw Skill 使用

在 OpenClaw 对话中，直接让它发送语音消息即可。

## 文件说明

- `feishu_tts.py` - 主脚本
- `SKILL.md` - OpenClaw Skill 说明
- `package.json` - Skill 元数据
- `README.md` - 本文件

## License

MIT
