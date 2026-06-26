# 飞书语音回复技能

## 简介

这是一个 OpenClaw 技能，可以将文本转换为飞书原生语音消息并发送。

## 功能特点

- ✅ 使用微软 Edge Neural TTS（高质量语音）
- ✅ 完全免费，无需 API Key
- ✅ 支持 5 种中文声音
- ✅ 飞书原生语音格式（波形播放）
- ✅ 自动触发关键词检测
- ✅ 完全静默发送（不发送多余文字）

## 快速开始

### 1. 安装依赖

```bash
pip3 install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置飞书 Bot

参考 `feishu-bot` 技能配置飞书机器人。

### 3. 使用

```bash
# 方法 1：命令行
python3 edge_tts_async.py "你好，世界！" xiaoxiao voice.mp3

# 方法 2：Python API
from edge_tts_async import generate_voice
generate_voice("你好，世界！", "xiaoxiao", "voice.mp3")
```

## 支持的声音

- **xiaoxiao**（女声，活泼专业）⭐⭐⭐⭐⭐
- **xiaoyi**（女声，温柔亲切）⭐⭐⭐⭐
- **yunyang**（男声，沉稳）⭐⭐⭐⭐
- **yunxi**（男声，北京话）⭐⭐⭐
- **yunze**（男声，活力）⭐⭐⭐

## 触发关键词

- "用语音回复"
- "发语音给我"
- "语音说"
- "念给我听"

## 重要规则

⚠️ **语音发送后，绝对不做任何回复操作！**

## 性能

- 生成速度：3-5 秒（100 字）
- 文件大小：20-30 KB（每 100 字）
- 音频质量：高（微软 Neural）

## 相关技能

- [feishu-bot](../feishu-bot/) - 飞书 Bot 基础功能
- [edge-tts](../edge-tts/) - Edge TTS 语音生成

## 许可证

MIT
