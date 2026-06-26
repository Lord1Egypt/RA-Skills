---
name: feishu-voice-sender-v2
description: 飞书语音消息发送技能 - 根据 channel 自动选择发送方式
metadata:
  tags: feishu, voice, tts, audio
  version: 1.0.0
  author: OpenClaw Community
  license: MIT
---

# 飞书语音消息发送技能

## 功能

根据当前 channel 自动选择语音发送方式：
- **飞书频道**: 使用小米 MiMo TTS 生成语音并发送飞书原生语音消息
- **其他频道**: 使用文字消息或相应格式

## 适用场景

- 用户要求发送语音消息时
- 需要根据 channel 自动选择发送方式时
- 想要发送语音通知时

## 核心组件

### 1. 频道检测
- 自动检测当前消息的 channel 类型
- 支持飞书、Telegram、Discord 等主流平台

### 2. 语音生成
- **飞书频道**: 使用小米 MiMo TTS (mimo-v2-tts)
- 支持多种语音风格（情感、方言、效果）
- 需要配置 `MIMO_API_KEY`

### 3. 语音发送
- **飞书频道**: 使用 OpenClaw `message` 工具发送飞书原生语音消息
- **其他频道**: 使用相应平台的语音发送方式

## 安装

### 前置要求

```bash
# 安装小米 MiMo TTS 技能
clawhub install xiaomi-mimo-tts

# 安装 ffmpeg (用于音频格式转换)
# Windows: winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# 配置 API Key
export MIMO_API_KEY=your-api-key
```

### 安装技能

```bash
# 使用 ClawHub 安装
clawhub install feishu-voice-sender
```

## 使用方法

### 方法 1：自动检测（推荐）

当用户消息包含语音相关关键词时，自动触发：

```python
# 触发关键词示例
- "发语音给我"
- "用语音说"
- "语音回复"
- "念给我听"
```

### 方法 2：指定 channel

```python
# 指定 channel 发送语音
channel = "feishu"  # 飞书
channel = "telegram"  # Telegram
channel = "discord"  # Discord
```

## 工作流

```
用户消息 → 触发语音关键词检测
    ↓
检测当前 channel 类型
    ↓
如果是飞书频道:
    - 使用小米 MiMo TTS 生成语音
    - 使用 OpenClaw message 工具发送飞书原生语音消息
如果是其他频道:
    - 使用相应平台的语音发送方式
    ↓
✅ 完成
```

## 配置

### 必需配置

```bash
# 小米 MiMo API Key
export MIMO_API_KEY=your-api-key
```

获取 API Key: https://platform.xiaomimimo.com/

### 可选配置

```bash
# 默认语音风格
export MIMO_STYLE=default

# 默认声音
export MIMO_VOICE=default_zh
```

## 支持的语音风格

### 情感
- 开心、悲伤、紧张、愤怒、惊讶、温柔

### 方言
- 东北话、四川话、台湾腔、粤语、河南话

### 效果
- 悄悄话、夹子音、唱歌

### 语速
- 变快、变慢

## 示例

### 飞书语音消息

```python
# 用户说: "发语音给我"
# 检测到 channel = "feishu"
# 自动使用小米 MiMo TTS 生成语音
# 发送飞书原生语音消息
```

### 其他频道

```python
# 用户说: "发语音给我"
# 检测到 channel = "telegram"
# 使用 Telegram 语音消息发送方式
```

## 文件结构

```
skills/feishu-voice-sender/
├── SKILL.md              # 本文件
└── feishu_voice_sender.py  # 主逻辑脚本
```

## 依赖项

### 必需依赖

- **小米 MiMo TTS 技能** (`xiaomi-mimo-tts`)
- **ffmpeg** (音频格式转换)
- **MIMO_API_KEY** (小米 MiMo API Key)

### 可选依赖

- **OpenClaw 消息工具**
  - OpenClaw 内置功能
  - 用于发送语音消息到飞书

## 故障排查

### 语音生成失败
```bash
# 检查 MIMO_API_KEY
echo $MIMO_API_KEY

# 检查 ffmpeg 安装
ffmpeg -version

# 重新安装小米 MiMo TTS 技能
clawhub install xiaomi-mimo-tts --force
```

### 语音发送失败

**检查 OpenClaw Gateway**：
```bash
# 检查 Gateway 状态
systemctl status openclaw-gateway

# 查看 Gateway 日志
journalctl -u openclaw-gateway -f
```

**检查飞书连接**：
- 确保 OpenClaw 已配置飞书凭据
- 检查飞书机器人权限

## 更新日志

### v1.0.0 (2026-03-20)
- 初始版本
- 支持飞书语音消息发送
- 支持频道自动检测
- 集成小米 MiMo TTS

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！